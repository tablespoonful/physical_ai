---
title: "From Language to Locomotion: Retargeting-free Humanoid Control via Motion Latent Guidance"
date: "2025-10-16"
authors: "Zhe Li; Cheng Chi; Yangyang Wei; Boan Zhu; Yibo Peng; Tao Huang"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2510.14952
pdf: https://arxiv.org/pdf/2510.14952
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.14952)** / [論文ページ](https://arxiv.org/abs/2510.14952)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# FROM LANGUAGE TO LOCOMOTION: RETARGETING-FREE HUMANOID CONTROL VIA MOTION LATENT GUIDANCE 

**Zhe Li**<sup>1</sup><sup>_∗_</sup> **, Cheng Chi**<sup>2</sup><sup>_∗†_</sup> **, Yangyang Wei**<sup>3</sup> **, Boan Zhu**<sup>4</sup> **, Yibo Peng**<sup>2</sup> **, Tao Huang**<sup>5</sup> **Pengwei Wang**<sup>2</sup> **, Zhongyuan Wang**<sup>2</sup> **, Shanghang Zhang**<sup>2</sup><sup>_,_6�</sup> **, Chang Xu**<sup>1�</sup> 

1 University of Sydney, 2 BAAI, 3 Harbin Institute of Technology 4 Hong Kong University of Science and Technology, 5 Shanghai Jiao Tong University 6 Peking University 


Figure 1: **RoboGhost** is a retargeting-free latent driven policy for language-guided humanoid locomotion. By removing the dependency on motion retargeting, it thus allows robots to be controlled directly via open-ended language commands. The figure showcases (a) the previous pipeline with motion retargeting, (b) our proposed retargeting-free latent-driven pipeline, (c) quantitative comparisons of success rate and time cost between baseline and RoboGhost, (d) performing the backflip, and (e) dancing and leaping forward. 

## ABSTRACT 

Natural language offers a natural interface for humanoid robots, but existing language-guided humanoid locomotion pipelines remain cumbersome and unreliable. They typically decode human motion, retarget it to robot morphology, and then track it with a physics-based controller. However, this multi-stage process is prone to cumulative errors, introduces high latency, and yields weak coupling between semantics and control. These limitations call for a more direct pathway from language to action, one that eliminates fragile intermediate stages. Therefore, we present **_RoboGhost_** , a retargeting-free framework that directly conditions humanoid policies on language-grounded motion latents. By bypassing explicit motion decoding and retargeting, RoboGhost enables a diffusion-based policy to denoise executable actions directly from noise, preserving semantic intent and supporting fast, reactive control. A hybrid causal transformer–diffusion motion generator further ensures long-horizon consistency while maintaining stability and diversity, yielding rich latent representations for precise humanoid behavior. Extensive experiments demonstrate that RoboGhost substantially reduces deploy- 

> _∗_ Equal Contribution _†_ Project Leader � Corresponding Author 

1 

ment latency, improves success rates and tracking accuracy, and produces smooth, semantically aligned locomotion on real humanoids. Beyond text, the framework naturally extends to other modalities such as images, audio, and music, providing a general foundation for vision–language–action humanoid systems. **_Project Page_** 

## 1 INTRODUCTION 

Natural language provides an intuitive interface for humanoid robots, enabling users to translate freeform instructions into physically feasible humanoid motion. Recent text-to-motion (T2M) models can generate diverse and semantically meaningful human motions (Li et al., 2024d; Chen et al., 2023; Guo et al., 2024; Li et al., 2024b; Tevet et al., 2022). However, deploying these models on real robots typically requires a hierarchical pipeline: decoding human motion from language, retargeting it to robot morphology, and tracking the trajectory with a physics-based controller (Peng et al., 2018; Ji et al., 2024; Chen et al., 2025; He et al., 2025a). 

This pipeline, while functional in constrained settings, suffers from systemic drawbacks. (1) **_Errors accumulate_** across decoding, retargeting, and tracking, degrading both semantic fidelity and physical feasibility. (2) **_High latency_** from multiple sequential stages, making real-time interaction difficult. (3) **_Loose coupling_** between language and control, since each stage is optimized in isolation rather than end-to-end. Recent refinements (Yue et al., 2025; Serifi et al., 2024; Shao et al., 2025) attempt to mitigate these issues, but improvements are applied locally to decoders or controllers, leaving the overall pipeline fragile and inefficient. 

**_Our key insight is simple: treat motion latents as first-class conditioning signals, directly use them as conditions to generate humanoid actions without decoding and retargeting altogether._** We therefore propose **_RoboGhost_** , a retargeting-free framework named to _highlight the latent representations that are invisible like a ghost yet strongly drive humanoid behavior_ . As shown in Fig 1, rather than producing explicit human motion, RoboGhost leverages language-conditioned motion latents as semantic anchors to guide a diffusion-based humanoid policy. The policy denoises executable actions directly from noise, eliminating error-prone intermediate stages while preserving fine-grained intent and enabling fast, reactive control. To our knowledge, this is **_the first diffusion-based humanoid policy driven by motion latents_** , achieving smooth and natural locomotion with DDIM-accelerated sampling (Song et al., 2020) for real-time deployment. 

To enhance temporal coherence and motion diversity, RoboGhost employs a hybrid causal transformer–diffusion architecture. The transformer backbone captures long-horizon dependencies and ensures global consistency (Zhou et al., 2024; 2025; Han et al., 2025). The diffusion component contributes stability and stochasticity for fine-grained motion synthesis. Together, this design mitigates drift and information loss typical of autoregressive models, while producing expressive motion latents that provide downstream policies with rich semantic conditioning for precise control. 

Extensive experiments validate the effectiveness and practicality of RoboGhost. We dramatically accelerate the full pipeline from motion generation to humanoid deployment, cutting the time from 17.85 _s_ to 5.84 _s_ . Beyond sheer speed, our approach yields higher-quality control by circumventing retargeting losses and improving generalization, which is reflected in a 5% higher success rate and reduced tracking error compared to baseline methods. Our framework achieves robust, semantically aligned locomotion on real humanoids, substantially reducing latency compared to retargeting-based pipelines. We can further extend this framework to support other input modalities such as images, audio, and music, thereby offering a reference architecture for humanoid vision-language-action systems. In short, **_RoboGhost moves text-driven humanoid control from fragile pose imitation to robust, real-time interaction._** 

In summary, our key contributions can be summarized as follows: 

- We propose RoboGhost, a retargeting-free framework that directly leverages languagegenerated motion latents for end-to-end humanoid policy learning, eliminating error-prone decoding and retargeting stages. 

- We introduce the first diffusion-based humanoid policy conditioned on motion latents, which denoises executable actions directly from noise and achieves smooth, diverse, and physically plausible locomotion with DDIM-accelerated sampling. 

2 

- We design a hybrid transformer–diffusion architecture that unifies long-horizon temporal coherence with stochastic stability, yielding expressive motion latents and strong language–motion alignment. 

- We validate RoboGhost through extensive experiments, demonstrating its effectiveness and generality in enabling robust and real-time language-guided humanoid locomotion. 

## 2 RELATED WORK 

### 2.1 HUMAN MOTION SYNTHESIS 

Language-guided humanoid locomotion leverages advances in text-to-motion generation, which primarily uses transformer-based discrete modeling or diffusion-based continuous modeling. Discrete methods model motion as tokens, evolving from early vector quantization (Guo et al., 2022c) to GPTstyle autoregression (Zhang et al., 2023a), scaling with LLMs (Jiang et al., 2023; Zhang et al., 2024) or improved attention (Zhong et al., 2023), and recently, bidirectional masking (Guo et al., 2023) and enhanced text alignment (Li et al., 2024d). In parallel, diffusion models excel in synthesis (Kim et al., 2023; Hu et al., 2023; Tevet et al., 2022; Li et al., 2024c; Bai et al., 2025; Li et al., 2023b; **?** ), with progress in efficiency (Chen et al., 2023), retrieval-augmentation (Zhang et al., 2023b), controllability (Li et al., 2024b), and architectures (Meng et al., 2024; Li et al., 2025). Our work builds on the continuous autoregressive framework (Li et al., 2024a), combining the benefits of both paradigms. 

### 2.2 HUMANOID WHOLE-BODY CONTROL 

Whole-body control (WBC) is crucial for humanoids, yet learning a general-purpose policy remains challenging. Existing approaches exhibit inherent trade-offs: methods like OmniH2O (He et al., 2024) and HumanPlus (Fu et al., 2024) prioritize specific robustness at the cost of generality or long-term accuracy, while others like Hover (He et al., 2025b), ExBody2 (Ji et al., 2024), and GMT (Chen et al., 2025) employs strategies (e.g., masking, curriculum learning, MoE) to enhance adaptability, though generalization is not guaranteed. Recent language-guided works also face limitations. LangWBC (Shao et al., 2025) scales poorly and offers no guarantee of generalization to unseen instructions, and RLPF (Yue et al., 2025) risks catastrophic forgetting and limited output diversity. To overcome these issues, we propose a MoE-based oracle paired with a latent-driven diffusion student, enhancing generalization while reducing deployment cost. 

## 3 METHOD 

This section presents the core components of our framework, which is depicted in Fig 2. We begin with an overview of our method in Section 3.1, providing a high-level description of the architecture and motivation. Section 3.2 details the construction of our motion generator, which leverages continuous autoregression and a causal autoencoder. Furthermore, Section 3.3 elaborates on our novel retargeting-free, latent-driven reinforcement learning architecture based on diffusion models, including its training and inference procedures. Finally, we present our causal adaptive sampling strategy in Section 3.4. Other details can be found in appendix 6.2. 

### 3.1 OVERVIEW 

Our work introduces a novel retargeting-free, latent-driven reinforcement learning architecture for language-guided humanoid control, which fundamentally diverges from conventional motion-tracking pipelines. As depicted in Fig. 2, our approach comprises three core components: a continuous autoregressive motion generator, a MoE-based teacher policy, and a latent-driven diffusion-based student policy. We focus on the challenge of generating diverse, physically plausible motions from high-level instructions without the need for complex kinematic retargeting. 

The process begins by feeding a textual prompt _T_ into the continuous autoregressive motion generator. Unlike prior works that decode the generated motion into an explicit kinematic sequence requiring tedious retargeting to the robot, our generator produces a compact latent motion representation _lref_ . 

3 


Figure 2: Overview of RoboGhost. We propose a two-stage approach: a motion latent is first generated, then a MoE-based teacher policy is trained with RL and a diffusion-based student policy is trained to denoise actions conditioned on motion latent. This latent-driven scheme bypasses the need for motion retargeting. 

This design is pivotal, as it bypasses the error-prone retargeting step and mitigates performance degradation caused by limited generator capability. The generation process can be formulated as: _lref_ = _G_ ( _T_ ), where _G_ denotes our motion generator. This latent representation _lref_ , alongside proprioceptive states and historical observations, then conditions a diffusion-based student policy _πs_ . The policy operates a denoising process to output actions directly executable on the physical humanoid. This latent-driven paradigm eliminates the dependency on privileged information and explicit reference motions during deployment, significantly streamlining the sim-to-real pipeline. 

To efficiently train the high-level oracle teacher policy, we introduce a causal adaptive sampling strategy. It dynamically prioritizes challenging motion segments by attributing failures to their causal antecedents, thereby maximizing sample efficiency and enabling the learning of long-horizon, agile motor skills. Finally, a meticulously designed reward function ensures accurate and expressive whole-body motion tracking. Collectively, our framework achieves robust, direct-drive control from language commands, setting a new paradigm for retargeting-free humanoid locomotion. 

### 3.2 CONTINUOUS AUTOREGRESSIVE MOTION GENERATOR 

Given that discretized models are prone to information loss and to leverage the advantages of both masked modeling and autoregressive approaches, we adopt a causal autoencoder and continuous masked autoregressive architecture with causal attention mask, which effectively captures temporal dependencies between tokens and produces rich contextual conditions for the subsequent diffusion process. Specifically, we first randomly mask motion tokens following the practice in language models (Devlin et al., 2019), obtaining a set of masked tokens. The temporal masking strategy follows the same mask ratio scheduling as (Chang et al., 2022), defined by the function: 


where _τ ∈_ [0 _,_ 1]. During training, _τ_ is uniformly sampled from **U** (0 _,_ 1), yielding a mask ratio _γ_ ( _τ_ ). Accordingly, _γ_ ( _τ_ ) _× N_ tokens are randomly selected for masking. 

Unlike previous masked autoregressive methods (Li et al., 2024a; Meng et al., 2024; Li et al., 2023a), our approach does not involve random token shuffling or batch-token prediction. Moreover, to mitigate the limitation in model expressiveness caused by low-rank matrix approximations during training, we replace bidirectional attention masks with causal attention masking. And for the input 

4 

text prompt _T_ , we use the LaMP (Li et al., 2024d) text transformer to extract textual features. This model captures linguistic nuances and semantic structures effectively, resulting in high-dimensional feature representations that provide essential guidance for motion generation. 

After the transformer completes the masked token prediction task, the predicted latent representations are used to condition the diffusion model, guiding the denoising process to produce more accurate and semantically rich latent representations. This enables downstream latent-driven action generation. 

### 3.3 LATENT-DRIVEN DIFFUSION POLICY FOR RETARGETING-FREE DEPLOYMENT 

### 3.3.1 MOE-BASED TEACHER POLICY 

The core challenge in text-to-locomotion is the inherent open-endedness of language. Therefore, generalization capability is the key enabler for policies to respond successfully to novel prompts and achieve true deployment flexibility. First, we train an oracle teacher policy using PPO (Schulman et al., 2017) with privileged simulator-state information. To learn a policy _πt_ that generalizes across diverse motion inputs, we first train an initial policy _π_ 0 on a curated motion dataset _D_ 0 of high diversity. We then evaluate the tracking accuracy of _π_ 0 for each motion sequence _s ∈D_ 0, focusing on the lower body through an error metric _e_ ( _s_ ) = _α · E_ key( _s_ ) + _β · E_ dof( _s_ ), where _E_ key( _s_ ) denotes the mean key-body position error and _E_ dof( _s_ ) the mean joint angle tracking error of the lower body. Motion sequences with _e_ ( _s_ ) _>_ 0 _._ 6 are filtered out, and the remaining data _D_ are used to train a general teacher policy. 

The teacher policy _πt_ is trained as an oracle in simulation using PPO, leveraging privileged information unavailable in the real world—including ground-truth root velocity, global joint positions, physical properties (e.g., friction coefficients, motor strength), proprioceptive state, and reference motion. The policy outputs target joint positions ˆ _at ∈_ R<sup>23</sup> for proportional derivative (PD) control, maximizing cumulative rewards to achieve accurate motion tracking and robust behavior, resulting in a high-performance expert policy trained solely on simulated data. Finally, we seek: 


To enhance the expressive power and generalization capability of the model, we incorporate a Mixture of Experts (MoE) module into the training of the teacher policy. The policy network consists of a set of expert networks and a gating network. The expert networks take as input both the robot state observations and reference motion, and output the final action _at_ . The gating network receives the same input observations and produces a probability distribution over all experts. The final action is computed as a weighted combination of actions sampled from each expert’s output distribution: _a_ =<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_pi · ai_, where</sup><sup>_pi_denotes the probability assigned to the</sup><sup>_i_-th expert by the gating network,</sup> and _ai_ represents the output of the _i_ -th expert policy. This architecture enhances the policy’s generalization capacity and obtains actions that accurately track reference motions, thereby providing more precise supervised signals for the student policy. 

### 3.3.2 DIFFUSION-BASED STUDENT POLICY 

Unlike prior approaches where the student policy _πs_ distills knowledge from the teacher using reference motion, we propose a novel latent-driven student policy that takes motion latent representations as input. In addition to the observation history, it incorporates a latent representation _lref_ from the motion generator as input. This implicit design enables the policy to operate during inference without retargeted explicit reference motion, thereby streamlining deployment, reducing performance degradation caused by limitations of motion generator capability and retargeting. 

Following a DAgger-like (Ross et al., 2011) approach, we roll out the student policy in simulation and query the teacher for optimal actions ˆ _at_ at visited states. During training, we progressively inject Gaussian noise _ϵt_ into the teacher’s actions and use the first-stage pretrained motion generator to obtain a latent representation with textual descriptions. The forward process can be modeled as a Markov nosing process using: 


where the constant _αt ∈_ (0 _,_ 1) is a hyper-parameter for sampling. Here, we denote the denoiser as _ϵθ_ , use _{xt}_<sup>_T_</sup> _t_ =0<sup>to denote the noising sequence, and</sup><sup>_xt−_1=</sup><sup>_ϵθ_(</sup><sup>_xt, t_) for the t-step denoising.</sup> 

5 

While the motion generator can produce motions lacking physical realism, our method does not blindly follow its output. Instead, a trainable latent encoder intelligently conditions the policy, translating raw proposals into actionable and stable commands. This enables the policy to generate diverse and robust actions even from imperfect guidance. This representation, along with proprioceptive states and historical observations, serves as conditioning to guide the denoising process. For tractability, we adopt an _x_ 0-prediction strategy and supervise the student policy by minimizing the mean squared 1 _−α_ ¯ _t·ϵθ_ <u>(</u> _xt,t_ <u>)</u> error loss _L_ = _∥a − a_ ˆ _t∥_ 2<sup>2,where</sup><sup>_a_=</sup><sup>_xt−_</sup><sup>_~~<u>√</u>~~_</sup> _~~√~~_ _<u>α</u>_ <u>¯</u> _t_ . The process iterates until convergence, yielding a policy that requires neither privileged knowledge nor explicit reference motion, and is suitable for real-world deployment. 

### 3.3.3 INFERENCE PIPELINE 

To ensure motion fluency and smoothness, it is essential to minimize the time required for the denoising process. We therefore adopt DDIM sampling (Song et al., 2020) and an MLP-based diffusion model to generate actions for deployment. The reverse process can be formulated as: 


Our framework is entirely retargeting-free and latent-driven. During inference, the textual description is first input into a motion generator and obtains a latent motion representation _lref_ . Crucially, we bypass the decoding of this latent into explicit motion sequences, thus eliminating the need for retargeting to the robot. We sample a random noise as input to the student policy and condition the diffusion model via AdaLN (Huang & Belongie, 2017) on the motion latent, proprioceptive states _po_ and historical observations _ot−H_ : _t_ , producing a clean action _a_ = _ϵθ_ ( _ϵ|lref , po, ot−H_ : _t_ ), that is directly executable on the physical robot. This streamlined pipeline not only reduces complexity but also mitigates issues such as low-quality motion generation due to limited generator capability, retargeting-induced errors, and insufficient action diversity. 

### 3.4 CAUSAL ADAPTIVE SAMPLING 

RoboGhost aims at tracking a reference motion more expressively in the whole body. To this end, we employ a novel sampling method to facilitate the teacher policy in mastering more challenging and longer motion sequences. Details about various reward functions, curriculum learning, and domain randomizations can be found in appendix 6.2. 

Training long-horizon motor skills faces a fundamental challenge: motion segments exhibit heterogeneous difficulty levels. Conventional approaches typically employ uniform sampling across trajectories (He et al., 2025a; Truong et al., 2024), which leads to oversampling of trivial segments and under-sampling of challenging ones, resulting in high reward variance and suboptimal sample efficiency. To address this, we propose a causality-aware adaptive sampling mechanism. The motion sequence is divided into _K_ equal-length intervals, and the sampling probability for each interval is dynamically adjusted based on empirical failure statistics. Let _kt_ denote the interval in which a rollout terminates due to failure. We hypothesize that the root cause often arises _s_ steps prior to _kt_ —such as a misstep or collision—that propagates into eventual failure at _kt_ . To enable corrective learning, we increase the sampling likelihood of these antecedent intervals. 

Motivated by the temporal structure of failures—typically preceded by suboptimal actions—we apply an exponential decay kernel _α_ ( _u_ ) = _γ_<sup>_u_</sup> ( _γ ∈_ (0 _,_ 1)) to assign higher weights to time steps leading up to termination. The base sampling probability for interval _s_ is defined as: 


where _K_ controls the backward horizon for causal attribution. Subsequently, we update and normalize the sampling probabilities across all intervals. Let _pi_ denote the base probability for interval _i_ . The updated probability is given by: _p_<sup>_′_</sup> _i_<sup>_←pi_+ ∆</sup><sup>_pi_,where ∆</sup><sup>_pi_denotes the increment derived from</sup> failure attribution. The distribution is then renormalized to ensure<sup>�</sup> _i_<sup>_p_</sup> 1<sup>_′_=1.Finally, the initial</sup> interval is sampled from the multinomial distribution Multinomial( _p_ 1<sup>_′, . . . , p′_</sup> _K_<sup>), enabling selective</sup> 

6 

focus on high-difficulty segments. Since each interval consists of multiple frames, after sampling the restart interval, we further select the exact restart frame uniformly within that interval. 

## 4 EXPERIMENT 

We present a rigorous empirical evaluation of our proposed method in this section, structured to systematically address three core research questions central to its design and efficacy. We organize our analysis around the following three research questions: 

- **Q1: Advantages of Latent-driven Pipeline.** To what extent does a retargeting-free, latentdriven approach improve efficiency, robustness, and generalization in motion generation, and how do these advantages manifest in real-world deployment scenarios? 

- **Q2: Generalization Gains via Diffusion Policy.** Does replacing MLP-based policies with diffusion-based policies enhance generalization to unseen instructions or environments? 

- **Q3: Better Motion Generator.** Does the continuous autoregressive architecture yield more semantically and kinematically precise latent embeddings than standard alternatives? Further, how do architectural variants of the diffusion model (e.g., MLP and DiT (Peebles & Xie, 2023)) affect motion generation quality? 

### 4.1 EXPERIMENTS SETTINGS 

**Datasets and Metrics** We evaluate on two MotionMillion (Fan et al., 2025) subsets: HumanML and Kungfu. For policy training, we use only index-0 sequences per motion name (e.g., “00000_0.npy”), excluding mirrored variants to reduce redundancy. Motions with non-planar terrains or infeasible contacts are filtered to ensure flat-ground consistency. The curated set is split 8:2 (train:test) with stratified category balance. For motion generator training, we leverage the full subsets. Evaluation metrics include motion generation and motion tracking. Generation follows Guo et al. (2022b) with retrieval precision R@1 _,_ 2 _,_ 3, MM Dist, FID, and Diversity. Tracking is assessed in physics simulators, consistent with OmniH2O (He et al., 2024) and PHC (Luo et al., 2023), using success rate (primary), mean per-joint error ( _Empjpe_ ), and mean per-keypoint error ( _Empkpe_ ). Success rate reflects both accuracy and stability. Further details are in appendix 6.3. 

### 4.2 EVALUATION OF MOTION GENERATION 

To validate the effectiveness of our continuous autoregressive motion generation model, we train and evaluate it on two distinct skeleton representations: the 263-dim HumanML3D (Guo et al., 2022a) and the 272-dim Humanml and Kungfu subsets of MotionMillion. We benchmark against text-to-motion methods, including diffusion- and transformer-based approaches. Motivated by SiT (Ma et al., 2024) and MARDM (Meng et al., 2024), we reformulate the training objective of the motion generator from noise prediction to velocity prediction, leading to improved motion quality and enhanced dynamic consistency in generated sequences. As summarized in Table 1, our model achieves competitive performance across both formats, demonstrating robustness to representation variation. 

### 4.3 EVALUATION OF MOTION TRACKING POLICY 

To further validate the efficacy of our motion tracking policy, we conduct evaluations on the HumanML and Kungfu subsets of MotionMillion, measuring _Empjpe_ and _Empkpe_ under physics-based simulation in both IsaacGym and MuJoCo. The pipeline operates as follows: textual descriptions are first input into the motion generator to produce a latent motion representation, which is subsequently input by the student policy for action execution. As summarized in Table 2, our method achieves high success rates on HumanML, alongside low joint and keypoint errors, indicating robust alignment between generated motion semantics and physically executable trajectories. Here, Baseline refers to the conventional, explicit framework where both the teacher and student policies use MLP backbones. 

7 

|Methods|R<br>Top 1|Precisio<br>Top 2|n_↑_<br>Top 3|FID_↓_|MM-Dist_↓_|Diversity_→_|
|---|---|---|---|---|---|---|
||H|umanML|3D||||
|Ground Truth|0.702|0.864|0.914|0.002|15.151|27.492|
|MDM (Tevet et al., 2023)|0.523|0.692|0.764|23.454|17.423|26.325|
|MLD (Chen et al., 2023)|0.546|0.730|0.792|18.236|16.638|26.352|
|T2M-GPT (Zhang et al., 2023a)|0.606|0.774|0.838|12.475|16.812|27.275|
|MotionGPT (Jiang et al., 2023)|0.456|0.598|0.628|14.375|14.892|27.114|
|MoMask (Guo et al., 2023)|0.621|0.784|0.846|12.232|16.138|27.127|
|AttT2M (Zhong et al., 2023)|0.592|0.765|0.834|15.428|15.726|26.674|
|<br>MotionStreamer (Xiao et al., 2025)|0.631|0.802|0.859|11.790|16.081|27.284|
|Ours-DDPM|0.639|0.808|0.867|11.706|15.978|27.230|
|Ours-SiT|0.641|0.812|0.870|11.743|15.972|27.307|
||HumanM|L (Motio|nMillion|)|||
|Ground Truth|0.714|0.876|0.920|0.002|14.984|26.571|
|Ours-DDPM|0.644|0.819|0.873|11.724|15.870|26.395|
|Ours-SiT|0.646|0.818|0.872|11.716|15.603|26.471|


Table 1: Quantitative results of text-to-motion generation on the HumanML3D dataset and HumanML subset. _→_ denotes that if the value is closer to the ground truth, the metric is better. 

|Method||IsaacGym|||MuJoCo||
|---|---|---|---|---|---|---|
||Succ_↑_|_Empjpe ↓_|_Empkpe ↓_|Succ_↑_|_Empjpe ↓_|_Empkpe ↓_|
|||Human|ML (MotionM|illion)|||
|Baseline|0.92|0.23|0.19|0.64|0.34|0.31|
|Ours-DDPM|0.97|0.12|0.09|0.74|0.24|0.20|
|Ours-SiT|0.98|0.14|0.08|0.72|0.26|0.23|
|||Kungf|u (MotionMil|lion)|||
|Baseline|0.66|0.43|0.37|0.51|0.58|0.52|
|Ours-DDPM|0.72|0.34|0.31|0.57|0.54|0.50|
|Ours-SiT|0.71|0.36|0.32|0.55|0.53|0.48|


Table 2: Motion tracking performance comparison in simulation on the HumanML and Kungfu test sets. 

### 4.4 QUALITATIVE EVALUATION 

We present a qualitative evaluation of the motion tracking policy across three deployment stages: simulation (IsaacGym), cross-simulator transfer (MuJoCo), and real-world execution on the Unitree G1 humanoid. Fig 3 visualizes representative tracking sequences, highlighting the policy’s ability to preserve motion semantics, maintain balance under dynamic transitions, and generalize across physics engines and hardware. In particular, real-robot deployments demonstrate that our latentdriven, retargeting-free framework enables smooth, temporally coherent motion execution without manual tuning, validating its readiness for practical embodied applications. 

### 4.5 ABLATION STUDIES 

To systematically answer the three research questions posed at the outset of this section, we conduct various ablation studies. 

To answer **Q1 (Advantages of Retargeting-free Pipeline)** , we evaluate the conventional pipeline: text prompts are fed to the motion generator, the output latent is decoded into explicit motion, which is then retargeted to the G1 robot and executed by the policy. As shown in Table 3, this approach underperforms due to its multi-stage complexity and error accumulation, and incurs higher real-world 

8 


Figure 3: Qualitative results in the IsaacGym and MuJoCo. 

|Method||IsaacGym|||MuJoCo||Time Cost (s)|
|---|---|---|---|---|---|---|---|
||Succ_↑_|_Empjpe ↓_|_Empkpe ↓_|Succ_↑_|_Empjpe ↓_|_Empkpe ↓_||
|Ours-Explicit|0.93|0.21|0.17|0.66|0.32|0.27|17.85|
|Ours-Implicit|0.97|0.12|0.09|0.74|0.24|0.20|5.84|


Table 3: Motion tracking performance comparison across different simulators on the HumanML and Kungfu test sets. Explicit version including PHC retargeting (1000 interations) and latent decode processes. 

deployment time cost. This confirms the efficiency and performance advantage of our retargeting-free, latent-driven framework. 

To answer **Q2 (Generalization Gains via Diffusion Policy)** , we conduct an ablation by replacing the diffusion policy with an MLP-based policy that concatenates latent and other observations to predict actions. Diffusion policies, by design, better capture various action distributions, enabling more robust adaptation to diverse or imperfect latents. As shown in Table 4, the diffusion policy significantly outperforms its MLP counterpart. 

To further evaluate generalization, we test both policies on 10 randomly sampled motions from unseen MotionMillion subsets (fitness, perform, 100style, haa). Although the motion generator was not trained on these subsets — resulting in suboptimal latents — the diffusion-based policy still achieves substantially better tracking and robustness than MLP, as evidenced in Table 4. This highlights the humanoid diffusion policy’s superiority. 

|Method||IsaacGy|m|Method||IsaacGy|m|
|---|---|---|---|---|---|---|---|
||Succ_↑_|_Empjpe ↓_|_Empkpe ↓_||Succ_↑_|_Empjpe ↓_|_Empkpe ↓_|
|MLP Policy|0.96|0.17|0.11|MLP Policy|0.54|0.48|0.45|
|Diffusion Policy|0.97|0.12|0.09|Diffusion Policy|0.68|0.42|0.39|


Table 4: Comparison of MLP-based and diffusion-based policy. The left table shows the tracking performance on HumanML subset, and the right table presents the generalization ability of two different policy architectures. 

To address **Q3 (Better Motion Generator)** , we conduct an ablation study on the diffusion backbone in our framework, comparing a 16-layer MLP and a 4-layer DiT under identical settings. As shown in Table 5, DiT offers slight gains in generation metrics but no measurable improvement in tracking success or joint accuracy, while incurring higher latency due to larger model size. Balancing effectiveness and efficiency, we therefore adopt the 16-layer MLP as our default backbone. 

9 

|Method||IsaacGy|m|Human|ML3D|Time Cost (s)_↓_|
|---|---|---|---|---|---|---|
||Succ_↑_|_Empjpe ↓_|_Empkpe ↓_|Top 3_↑_|FID_↓_||
|DiT|0.96|0.11|0.11|0.870|11.697|14.28|
|MLP|0.97|0.12|0.09|0.867|11.706|5.84|


Table 5: Comparison of tracking performance across different diffusion backbones for motion generation. 

## 5 CONCLUSION 

In this paper, we introduce RoboGhost, a retargeting-free, latent-driven framework that bridges natural language instructions with physically feasible humanoid motion control. Our method harnesses rich semantic representations from a pretrained text-to-motion model and integrates them into a diffusion-based humanoid policy, thereby bypassing motion decoding and retargeting stages that are not only error-prone but also time-consuming. This design enables real-time, language-guided humanoid locomotion with improved adaptability. Extensive experiments show that RoboGhost reduces cumulative distortions and execution latency while preserving semantic alignment and physical realism. Beyond advancing efficiency and robustness, RoboGhost offers a new and practical pathway toward more intuitive, responsive, and deployable humanoid robots in real-world environments. 

## REFERENCES 

- Shuanghao Bai, Wenxuan Song, Jiayi Chen, Yuheng Ji, Zhide Zhong, Jin Yang, Han Zhao, Wanqi Zhou, Wei Zhao, Zhe Li, Pengxiang Ding, Cheng Chi, Haoang Li, Chang Xu, Xiaolong Zheng, Donglin Wang, Shanghang Zhang, and Badong Chen. Towards a unified understanding of robot manipulation: A comprehensive survey. _arXiv preprint arXiv:2510.10903_ , 2025. 

- Huiwen Chang, Han Zhang, Lu Jiang, Ce Liu, and William T Freeman. Maskgit: Masked generative image transformer. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 11315–11325, 2022. 

- Xin Chen, Biao Jiang, Wen Liu, Zilong Huang, Bin Fu, Tao Chen, and Gang Yu. Executing your commands via motion diffusion in latent space. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 18000–18010, 2023. 

- Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , pp. 4171–4186, 2019. 

- Ke Fan, Shunlin Lu, Minyue Dai, Runyi Yu, Lixing Xiao, Zhiyang Dou, Junting Dong, Lizhuang Ma, and Jingbo Wang. Go to zero: Towards zero-shot motion generation with million-scale data. _arXiv preprint arXiv:2507.07095_ , 2025. 

- Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ , 2024. 

- Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 

- Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 5152–5161, June 2022a. 

- Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 5152–5161, 2022b. 

10 

- Chuan Guo, Xinxin Zuo, Sen Wang, and Li Cheng. Tm2t: Stochastic and tokenized modeling for the reciprocal generation of 3d human motions and texts. In _European Conference on Computer Vision_ , pp. 580–597. Springer, 2022c. 

- Chuan Guo, Yuxuan Mu, Muhammad Gohar Javed, Sen Wang, and Li Cheng. Momask: Generative masked modeling of 3d human motions. 2023. 

- Chuan Guo, Yuxuan Mu, Muhammad Gohar Javed, Sen Wang, and Li Cheng. Momask: Generative masked modeling of 3d human motions. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 1900–1910, 2024. 

- Yi Han, Cheng Chi, Enshen Zhou, Shanyu Rong, Jingkun An, Pengwei Wang, Zhongyuan Wang, Lu Sheng, and Shanghang Zhang. Tiger: Tool-integrated geometric reasoning in vision-language models for robotics. _arXiv preprint arXiv:2510.07181_ , 2025. 

- Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025a. 

- Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural whole-body controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 9989–9996. IEEE, 2025b. 

- Vincent Tao Hu, Wenzhe Yin, Pingchuan Ma, Yunlu Chen, Basura Fernando, Yuki M Asano, Efstratios Gavves, Pascal Mettes, Bjorn Ommer, and Cees GM Snoek. Motion flow matching for human motion synthesis and editing. _arXiv preprint arXiv:2312.08895_ , 2023. 

- Albert S Huang, Edwin Olson, and David C Moore. Lcm: Lightweight communications and marshalling. In _2010 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 4057–4062. IEEE, 2010. 

- Xun Huang and Serge Belongie. Arbitrary style transfer in real-time with adaptive instance normalization. In _Proceedings of the IEEE international conference on computer vision_ , pp. 1501–1510, 2017. 

- Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- Yuheng Ji, Huajie Tan, Jiayu Shi, Xiaoshuai Hao, Yuan Zhang, Hengyuan Zhang, Pengwei Wang, Mengdi Zhao, Yao Mu, Pengju An, et al. Robobrain: A unified brain model for robotic manipulation from abstract to concrete. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1724–1734, 2025. 

- Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. Motiongpt: Human motion as a foreign language. _Advances in Neural Information Processing Systems_ , 36:20067–20079, 2023. 

- Jihoon Kim, Jiseob Kim, and Sungjoon Choi. Flame: Free-form language-based motion synthesis & editing. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 37, pp. 8255–8263, 2023. 

- Tianhong Li, Yonglong Tian, He Li, Mingyang Deng, and Kaiming He. Autoregressive image generation without vector quantization. _Advances in Neural Information Processing Systems_ , 37: 56424–56445, 2024a. 

- Zhe Li, Zhangyang Gao, Cheng Tan, Stan Z Li, and Laurence T Yang. General point model with autoencoding and autoregressive. _arXiv preprint arXiv:2310.16861_ , 2023a. 

11 

- Zhe Li, Laurence T Yang, Xin Nie, BoCheng Ren, and Xianjun Deng. Enhancing sentence representation with visually-supervised multimodal pre-training. In _Proceedings of the 31st ACM International Conference on Multimedia_ , pp. 5686–5695, 2023b. 

- Zhe Li, Yisheng He, Lei Zhong, Weichao Shen, Qi Zuo, Lingteng Qiu, Zilong Dong, Laurence Tianruo Yang, and Weihao Yuan. Mulsmo: Multimodal stylized motion generation by bidirectional control flow. _arXiv preprint arXiv:2412.09901_ , 2024b. 

- Zhe Li, Laurence T Yang, Bocheng Ren, Xin Nie, Zhangyang Gao, Cheng Tan, and Stan Z Li. Mlip: Enhancing medical visual representation with divergence encoder and knowledge-guided contrastive learning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 11704–11714, 2024c. 

- Zhe Li, Weihao Yuan, Yisheng He, Lingteng Qiu, Shenhao Zhu, Xiaodong Gu, Weichao Shen, Yuan Dong, Zilong Dong, and Laurence T Yang. Lamp: Language-motion pretraining for motion generation, retrieval, and captioning. _arXiv preprint arXiv:2410.07093_ , 2024d. 

- Zhe Li, Weihao Yuan, Weichao Shen, Siyu Zhu, Zilong Dong, and Chang Xu. Omnimotion: Multimodal motion generation with continuous masked autoregression, 2025. URL https: //arxiv.org/abs/2510.14954. 

- Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 10895–10904, 2023. 

- Nanye Ma, Mark Goldstein, Michael S Albergo, Nicholas M Boffi, Eric Vanden-Eijnden, and Saining Xie. Sit: Exploring flow and diffusion-based generative models with scalable interpolant transformers. In _European Conference on Computer Vision_ , pp. 23–40. Springer, 2024. 

- Zichong Meng, Yiming Xie, Xiaogang Peng, Zeyu Han, and Huaizu Jiang. Rethinking diffusion for text-driven human motion generation. _arXiv preprint arXiv:2411.16575_ , 2024. 

- William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 4195–4205, 2023. 

- Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Exampleguided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pp. 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Agon Serifi, Ruben Grandia, Espen Knoop, Markus Gross, and Moritz Bächer. Robot motion diffusion model: Motion generation for robotic characters. In _SIGGRAPH asia 2024 conference papers_ , pp. 1–9, 2024. 

- Yiyang Shao, Xiaoyu Huang, Bike Zhang, Qiayuan Liao, Yuman Gao, Yufeng Chi, Zhongyu Li, Sophia Shao, and Koushil Sreenath. Langwbc: Language-directed humanoid whole-body control via end-to-end learning. _arXiv preprint arXiv:2504.21738_ , 2025. 

- Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 

- BAAI RoboBrain Team, Mingyu Cao, Huajie Tan, Yuheng Ji, Minglan Lin, Zhiyu Li, Zhou Cao, Pengwei Wang, Enshen Zhou, Yi Han, et al. Robobrain 2.0 technical report. _arXiv preprint arXiv:2507.02029_ , 2025. 

- Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ , 2022. 

12 

- Guy Tevet, Sigal Raab, Brian Gordon, Yoni Shafir, Daniel Cohen-or, and Amit Haim Bermano. Human motion diffusion model. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Shashank Tripathi, Lea Müller, Chun-Hao P Huang, Omid Taheri, Michael J Black, and Dimitrios Tzionas. 3d human pose estimation via intuitive physics. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 4713–4725, 2023. 

- Takara Everest Truong, Michael Piseno, Zhaoming Xie, and Karen Liu. Pdp: Physics-based character animation via diffusion policy. In _SIGGRAPH Asia 2024 Conference Papers_ , pp. 1–10, 2024. 

- Lixing Xiao, Shunlin Lu, Huaijin Pi, Ke Fan, Liang Pan, Yueer Zhou, Ziyong Feng, Xiaowei Zhou, Sida Peng, and Jingbo Wang. Motionstreamer: Streaming motion generation via diffusion-based autoregressive model in causal latent space. _arXiv preprint arXiv:2503.15451_ , 2025. 

- Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _arXiv preprint arXiv:2506.12851_ , 2025. 

- Junpeng Yue, Zepeng Wang, Yuxuan Wang, Weishuai Zeng, Jiangxing Wang, Xinrun Xu, Yu Zhang, Sipeng Zheng, Ziluo Ding, and Zongqing Lu. Rl from physical feedback: Aligning large motion models with humanoid control. _arXiv preprint arXiv:2506.12769_ , 2025. 

- Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Yong Zhang, Hongwei Zhao, Hongtao Lu, Xi Shen, and Ying Shan. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 14730–14740, 2023a. 

- Mingyuan Zhang, Xinying Guo, Liang Pan, Zhongang Cai, Fangzhou Hong, Huirong Li, Lei Yang, and Ziwei Liu. Remodiffuse: Retrieval-augmented motion diffusion model. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 364–373, 2023b. 

- Yaqi Zhang, Di Huang, Bin Liu, Shixiang Tang, Yan Lu, Lu Chen, Lei Bai, Qi Chu, Nenghai Yu, and Wanli Ouyang. Motiongpt: Finetuned llms are general-purpose motion generators. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pp. 7368–7376, 2024. 

- Chongyang Zhong, Lei Hu, Zihao Zhang, and Shihong Xia. Attt2m: Text-driven human motion generation with multi-perspective attention mechanism. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 509–519, 2023. 

- Enshen Zhou, Qi Su, Cheng Chi, Zhizheng Zhang, Zhongyuan Wang, Tiejun Huang, Lu Sheng, and He Wang. Code-as-monitor: Constraint-aware visual programming for reactive and proactive robotic failure detection. _arXiv preprint arXiv:2412.04455_ , 2024. 

- Enshen Zhou, Jingkun An, Cheng Chi, Yi Han, Shanyu Rong, Chi Zhang, Pengwei Wang, Zhongyuan Wang, Tiejun Huang, Lu Sheng, et al. Roborefer: Towards spatial referring with reasoning in vision-language models for robotics. _arXiv preprint arXiv:2506.04308_ , 2025. 

13 

## 6 APPENDIX 

## APPENDIX OVERVIEW 

This appendix provides additional details and results, organized as follows: 

- **Section 6.1** : Detailed information of implementation, including detailed proprioceptive states, privileged information and hyper-parameters of network structure. 

- **Section 6.2** : Elaboration on some details during training, including dataset details, motion filter and retargeting, simulator, domain randomization, regularization, reward functions, penalty and curriculm learning. 

- **Section 6.3** : Details about evaluation, including metrics about motion generation and motion tracking. 

- **Section 6.4** : Deployment details, including sim-to-sim and sim-to-real. 

- **Section 6.5** : Extra qualitative experiment results and visualizations, including in the simulation and in the real-world. 

- **Section 6.6** : Extra ablation experiment results and visualizations, including the effect of causal adaptive sampling (CAS), hyper-parameter _λ_ , and the number of experts in MoE of teacher policy. 

### 6.1 IMPLEMENTATION DETAILS 

In this section, we describe the state representation used for policy training, covering proprioceptive states, privileged information, and hyper-parameters of our network. The proprioceptive state components for both the teacher and student policies are summarized in Table 6. A key distinction is that the student policy utilizes a longer history of observations, compensating for its lack of access to privileged information by relying on extended temporal context. 

For privileged information, the teacher policy incorporates privileged information to achieve precise motion tracking. The full set of privileged state features is provided in Table 6. Previous methods receive motion target information as part of the observation in both teacher and student policy, which includes keypoint positions, desired joint (DoF) positions, and root velocity. But in our method, only the teacher policy receives these information, and the student policy only receives the latent from motion generator. A detailed target state composition is presented in Table 7. The action output corresponds to target joint positions for proportional-derivative (PD) control, with a dimensionality of 23 for the Unitree G1 humanoid platform. 

RoboGhost employs a teacher-student training framework. The teacher policy, trained via standard PPO (Schulman et al., 2017), utilizes privileged information, tracking targets, and proprioceptive states. In contrast, the student policy is trained using Dagger without access to privileged information, but instead relies on an extended history of observations. Furthermore, while the teacher policy uses explicit reference motion information, the student policy replaces this with a latent representation from a motion generator, resulting in a retargeting-free and latent-driven approach. For the teacher policy, inputs are concatenated and processed by a Mixture-of-Experts (MoE) network for policy learning. The student policy feeds its concatenated inputs as conditions to a diffusion model with an MLP backbone. Furthermore, we employ AdaLN to inject conditional information throughout the denoising process within the diffusion model. A final MLP layer is appended to the backbone network, which projects the output to a 23-dimensional action space while additionally incorporating the conditional signals. Detailed hyperparameters for both policies are provided in Table 8. 

### 6.2 TRAINING DETAILS 

**Dataset Details** Our motion generator is pretrained on the MotionMillion dataset (Fan et al., 2025). Given the substantial scale of this dataset, we restrict pretraining to the humanml and kungfu subsets from the MotionUnion branch, comprising a total of 50,378 motion sequences. During policy training, we again draw data from the humanml and kungfu subsets. However, due to the presence of extensive duplicate and mirrored sequences, we perform a data cleaning process to remove redundancies and 

14 

|**Proprioceptive States**|**Teacher Polic**|**y**|
|---|---|---|
|State Comonent<br>Dim|||
|p<br>.|State Component|Dim.|
|DoF position<br>23<br>DoF velocity<br>23<br>Last Action<br>23|DoF position<br>Keypoint position<br>|23<br>36<br>|
|Root Angular Velocity<br>3<br>Roll<br>1<br>Pitch<br>1<br>Yaw<br>1|Root Velocity<br>Root Angular Velocit<br>Roll<br>Pitch<br>Yaw|3<br>y<br>3<br>1<br>1<br>1|
|Total dim<br>75_×_10|Height|1|
|**Privileged Information**|Total dim|69|
|DoF Difference<br>23|**Student Polic**|**y**|
|Keybody Difference<br>36<br>Root velocity<br>3|Latent|64|
|<br>Total dim<br>62|Total dim|64|


Table 6: Proprioceptive states and privileged information. 

Table 7: Reference information in the teacher and student policies. 

|**Hyperparameter**|**Value**|
|---|---|
|Optimizer|AdamW|
|_β_1_, β_2|0.9, 0.999<br>|
|Learning Rate|1_×_10<sup>_−_4</sup>|
|Batch Size|4096|
|**Teacher Pol**|**icy**|
|Discount factor (_γ_)|0.99|
|Clip Parameter|0.2|
|Entropy Coefficient|0.005|
|Max Gradient Norm|1|
|Learning Epochs|5|
|Mini Batches|4|
|Value Loss Coefficient|1|
|Value MLP Size|[512, 256, 128]|
|Actor MLP Size|[512, 256, 128]|
|Experts|5|
|**Student Pol**|**icy**|
|MLP Layers|4|
|MLP Size|[256, 256, 256]|


Table 8: Hyperparameters for teacher and student policy training. 

non-flat-ground motions. Using this filtered dataset, we first train an initial policy, denoted as _π_ 0. This policy is then used to further filter the dataset by excluding sequences with a tracking error exceeding 0.6. After this refinement, the humanml subset contains 3,261 motion sequences, and the kungfu subset contains 200. And due to the significant domain gap and difference in complexity between these two subsets, we opt to train two separate policies, each specialized on one subset. 

**Motion Filter and Retargeting** Following Xie et al. (2025) and Tripathi et al. (2023), we compute the ground-projected distance between the center of mass (CoM) and center of pressure (CoP) for each frame and apply a stability threshold. Let **p** ¯<sup>CoM</sup> _t_ = ( _p_<sup>CoM</sup> _t,x_<sup>_, p_CoM</sup> _t,y_<sup>) and</sup><sup>**p**¯</sup> _t_<sup>CoP</sup> = ( _p_<sup>CoP</sup> _t,x_<sup>_, p_CoP</sup> _t,y_<sup>) denote</sup> the 2D ground projections of CoM and CoP at frame _t_ , respectively. Let ∆ _dt_ = _∥_ **p** ¯<sup>CoM</sup> _t −_ **p** ¯<sup>CoP</sup> _t ∥_ 2. We define the stability criterion of a frame as ∆ _dt < ϵ_ stab. A motion sequence will not be filtered if its first and last frames are stable, and the longest consecutive unstable segment is shorter than 100. 

15 

**Simulator** Following established protocols in motion tracking policy research (Ji et al., 2024; He et al., 2025a; Ji et al., 2025; Team et al., 2025), we also adopt a three-stage evaluation pipeline: (1) large-scale reinforcement learning training in IsaacGym; (2) zero-shot transfer to MuJoCo to assess cross-simulator generalization; and (3) physical deployment on the Unitree G1 humanoid platform to validate the performance in real-world. 

**Reference State Initialization** Task initialization is a critical factor in reinforcement learning (RL) training. We observe that naïvely initializing episodes from the beginning of the reference motion frequently leads to policy failure, especially for difficult motions. This can cause the environment to overfit to easier frames and fail to learn the most challenging segments of the motion. 

To mitigate this issue, we employ the Reference State Initialization (RSI) framework (Peng et al., 2018). Concretely, we sample time-phase variables uniformly over [0 _,_ 1], randomizing the starting point within the reference motion that the policy must track. The robot’s state—including root position, orientation, linear and angular velocities, as well as joint positions and velocities—is then initialized to the values from the reference motion at the sampled phase. This approach substantially enhances motion tracking performance, particularly for highly-dynamic whole-body motions, by enabling the policy to learn various segments of the movement in parallel rather than being limited to a strictly sequential learning process. 

**Domain Randomization and Regularization** To improve the robustness and generalization of the pretrained policy, we utilize the domain randomization techniques and regularization items, which are listed in Table 9. 

|**Domain Randomization**||
|---|---|
|**Term**|**Value**|
|Friction<br>P Gain<br>_U_(0_._<br>Control delay|_U_(0_._5_,_2_._2)<br>75_,_1_._25)_×_default<br>_U_(20_,_40)ms|
|<br>**External Perturbation**<br> <br>|<br>|
|Push robot<br>interval|= 8s_, vxy_ = 0_._5m/s|
|**Regularization**||
|**Term Expression**|**Weight**|
|DoF position limits**1**(_dt /∈_[_q_min_, q_max])<br>|_−_10|
|DoF acceleration_∥_<sup>¨</sup>_dt∥_<sup>2</sup><br>2|_−_3_×_10<sup>_−_7</sup>|
|DoF error_∥dt −d_0_∥_<sup>2</sup><br>2<br>|_−_0_._1|
|Action rate_∥at −at−_1_∥_<sup>2</sup><br>2|_−_0_._5|
|Feet air time_T_air_−_0_._5|10|
|Feet contact force_∥F_feet_∥_<sup>2</sup><br>2<br>Stumble**1**(_F _<sup>_x_</sup><br>feet <sup>_>_ 5</sup><sup>_× F z_</sup><br>feet<sup>)</sup>|_−_0_._003<br>_−_2|
|<br><br>Waist roll pitch error_∥p_<sup>wrp</sup><br>_t_<br>_−p_<sup>wrp</sup><br>0 <sup>_∥_2</sup><br>2|_−_0_._5|
|Ankle Action_∥a_<sup>ankle</sup><br>_t_<br>_∥_<sup>2</sup><br>2|_−_0_._3|


Table 9: Domain randomization and regularization parameters. 

**Motion Tracking Rewards** We define the reward function as the sum of penalty, regularization, and task rewards, which is meticulously designed to improve both the performance and motion realism of the humanoid robot. It consists of terms that incentivize accurate tracking of root velocity, direction, and orientation, as well as precise keypoints and joints position tracking. Inspired by ASAP (He et al., 2025a), we additionally incorporate regularization terms to enhance stability and sim-to-real transferability, including torques, action rate, feet orientation, feet heading, and slippage. In terms of penalty, we adopt penalty terms for DoF position limits, torque limits, and termination. The detailed reward functions are summarized in Table 10, more terms can be seen in the supplementary material. 

16 

||_Task R_|_eward_||
|---|---|---|---|
|Root velocity|10_._0|Root velocity direction|6_._0|
|<br>Root angular velocity|1_._0|<br>Keypoint position|10_._0|
|Feet position|12_._0|DoF position|6_._0|
|DoF velocity|6_._0|||
||_Pena_|_lty_||
|DoF position limits|_−_10_._0|Torque limits|_−_5_._0|
|Termination|_−_200_._0|||


Table 10: Reward terms for pretraining 

**Curriculum Learning** Training policies to track agile motions in simulation is challenging, as certain dynamic behaviors are too difficult for the policy to learn effectively from the outset. To mitigate this issue, we utilize a termination curriculum (He et al., 2025a) that progressively tightens the motion tracking error tolerance during training, thereby guiding the policy to gradually improve its tracking fidelity. Initially, we set a lenient termination threshold of 1.5m—episodes are terminated if the robot deviates from the reference motion by more than this margin. As training progresses, the threshold is annealed down gradually, incrementally increasing the precision required for successful tracking. This curriculum enables the policy to first acquire basic balancing skills before refining them under stricter tracking constraints, ultimately facilitating the successful execution of highly dynamic behaviors. 

### 6.3 EVALUATION DETAILS 

**Motion Generation Metrics** Following (Guo et al., 2022c; Li et al., 2024d;b), we evaluate our approach using established text-to-motion metrics: retrieval accuracy (R@1, R@2, R@3), Multimodal Distance (MMDist), and Fréchet Inception Distance (FID). 

- Retrieval Accuracy (R-Precision): These metrics measure the relevance of generated motions to text descriptions in a retrieval setup. R@1 denotes the fraction of text queries for which the correct motion is retrieved as the top match, reflecting the model’s precision in identifying the most relevant motion. R@2 and R@3 extend this notion, indicating recall within the top two and three retrieved motions, respectively. 

- Multimodal Distance (MMDist): This quantifies the average feature-space distance between generated motions and their corresponding text embeddings, typically extracted via a pretrained retrieval model. Smaller MMDist values indicate stronger semantic alignment between text descriptions and motion outputs. 

- Fr échet Inception Distance (FID): FID assesses the quality and realism of generated motions by comparing their feature distribution to that of real motion data using a pretrained feature encoder (e.g., an Inception-style network). It computes the Fréchet distance between multivariate Gaussian distributions fitted to real and generated motion features. Lower FID scores reflect better distributional similarity and higher perceptual quality. 

- Diversity: Diversity quantifies the variance of motion sequences within the dataset. It is computed by randomly sampling _N_ diver = 300 pairs of motions, denoted as ( _fi,_ 1 _, fi,_ 2) for each pair _i_ . The metric is calculated as _N_ diver1 � _Ni_ =1diver<sup>_∥fi,_1</sup><sup>_−fi,_2</sup><sup>_∥_</sup> 

**Motion Tracking Metrics** For motion tracking evaluation, we adopt metrics commonly used in prior work (Ji et al., 2024): Success Rate (Succ), Mean Per Joint Position Error ( _Empjpe_ ), and Mean Per Keybody Position Error ( _Empkpe_ ). 

- Success Rate (Succ): This metric evaluates whether the humanoid robot successfully follows the reference motion without falling. A trial is considered a failure if the average trajectory deviation exceeds 0.5 meters at any point, or if the root pitch angle passes a predefined threshold. 

17 

- Mean Per Joint Position Error ( _Empjpe_ in rad): _Empjpe_ measures joint-level tracking accuracy by computing the average error in degrees of freedom (DoF) rotations between the reference and generated motion. 

- Mean Per Keybody Position Error ( _Empkpe_ in m): _Empkpe_ assesses keypoint tracking performance based on the average positional discrepancy between reference and generated keypoint trajectories. 

### 6.4 DEPLOYMENT DETAILS 

**Sim-to-Sim** As demonstrated in Humanoid-Gym (Gu et al., 2024), MuJoCo exhibits more realistic dynamics compared to Isaac Gym. Following established practices in motion tracking policy research (Ji et al., 2024), we perform reinforcement learning training in Isaac Gym to leverage its computational efficiency. To assess policy robustness and generalization, we then conduct zero-shot transfer to the MuJoCo simulator. Finally, we deploy the policy on a physical humanoid robot to evaluate the effectiveness of our RoboGhost framework for real-world motion tracking. 

**Sim-to-Real** Our real-world experiments utilize a Unitree G1 humanoid robot, equipped with an onboard Jetson Orin NX module for computation and communication. The control policy takes motion-tracking targets as input, computes target joint positions, and issues commands to the robot’s low-level controller at 50Hz. Command transmission introduces a latency of 18–30ms. The low-level controller operates at 500Hz to ensure stable real-time actuation. Communication between the policy and the low-level interface is implemented using the Lightweight Communications and Marshalling (LCM) (Huang et al., 2010). 

### 6.5 ADDITIONAL QUALITATIVE RESULTS 

To further validate the effectiveness of our method, we provide additional qualitative results in this section, including motion tracking visualizations in IsaacGym and MuJoCo (Fig 4) and real-world locomotion demonstrations on the physical robot (Fig 5). Moreover, we provide additional motion generation qualtative results in Fig 6. A supplementary video showcasing real-robot deployments is provided in the supplementary material. 

### 6.6 ADDITIONAL ABLATION STUDIES 

To rigorously evaluate the effectiveness of causal adaptive sampling (CAS), we conduct various ablation studies examining both its performance gains and sensitivity to hyperparameters. As shown in Table 11, causal adaptive sampling increases the sampling probability of kinematically challenging frames within a motion sequence, thereby improving training efficiency and enhancing model generalization. Furthermore, as illustrated in Fig 7a and 7b, optimal performance is achieved when the adaptation parameters are set to _λ_ = 0 _._ 8 and _p_ = 0 _._ 005. 

Furthermore, we conduct an ablation study on the number of experts in the MoE architecture. As illustrated in Fig 8, the variation in the number of experts has a measurable yet limited impact on the policy’s performance, with the optimal result achieved when the number of experts is set to 5. 

18 


Figure 4: Qualitative results in the IsaacGym and MuJoCo. 

|Method||IsaacGy|m||MuJoCo||
|---|---|---|---|---|---|---|
||Succ_↑_|_Empjpe ↓_|_Empkpe ↓_|Succ_↑_|_Empjpe ↓_|_Empkpe ↓_|
|||Huma|nML (Motion|Million)|||
|w/o CAS<br>Ours|0.92<br>0.97|0.18<br>0.12|0.14<br>0.09|0.68<br>0.74|0.32<br>0.24|0.28<br>0.20|
|||Kun|gfu (MotionM|illion)|||
|w/o CAS|0.62|0.42|0.41|0.48|0.67|0.63|
|Ours|0.72|0.34|0.31|0.57|0.54|0.50|


Table 11: Ablation study on causal adaptive sampling. 

19 


Figure 5: Qualitative results on the Unitree G1. 


Figure 6: Qualitative results of motion generator. 

20 


Figure 7: The impact of different _λ_ values on tracking performance in IsaacGym and MuJoCo. 


Figure 8: The impact of different number of experts in MoE on tracking performance in IsaacGym and MuJoCo. 

21 

