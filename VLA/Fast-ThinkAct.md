---
title: "Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning"
date: "2026-01-14"
authors: "Chi-Pin Huang; Yunze Man; Zhiding Yu; Min-Hung Chen; Jan Kautz; Yu-Chiang Frank Wang"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2601.09708
pdf: https://arxiv.org/pdf/2601.09708
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.09708)** / [論文ページ](https://arxiv.org/abs/2601.09708)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_2026-2-25_ 


# **Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning** 

**Chi-Pin Huang**<sup>1</sup> **, Yunze Man**<sup>2</sup> **, Zhiding Yu, Min-Hung Chen, Jan Kautz, Yu-Chiang Frank Wang**<sup>1</sup> **, Fu-En Yang** NVIDIA 

## **Abstract** 

**Vision-Language-Action (VLA) tasks require reasoning over complex visual scenes and executing adaptive actions in dynamic environments. While recent studies on reasoning VLAs show that explicit chain-of-thought (CoT) can improve generalization, they suffer from high inference latency due to lengthy reasoning traces. We propose Fast-ThinkAct, an efficient reasoning framework that achieves compact yet performant planning through verbalizable latent reasoning. Fast-ThinkAct learns to reason efficiently with latent CoTs by distilling from a teacher, driven by a preference-guided objective to align manipulation trajectories that transfers both linguistic and visual planning capabilities for embodied control. This enables reasoning-enhanced policy learning that effectively connects compact reasoning to action execution. Extensive experiments across diverse embodied manipulation and reasoning benchmarks demonstrate that Fast-ThinkAct achieves strong performance with up to 89.3% reduced inference latency over state-of-the-art reasoning VLAs, while maintaining effective long-horizon planning, few-shot adaptation, and failure recovery.** 

#### **Links: Project Page** 

## **1. Introduction** 

Recent large vision-language models (VLMs) Liu et al. (2023); Comanici et al. (2025); Liu et al. (2024); Bai et al. (2025); Shi et al. (2024); Li et al. (2025); Chen et al. (2025); Wang et al. (2025); Xie et al. (2024) have achieved remarkable capabilities in visual-language understanding across diverse multimodal tasks. To extend these capabilities to embodied-centric tasks, recent works leverage large-scale robot demonstrations O’Neill et al. (2024) to develop Vision-Language-Action (VLA) foundation models Brohan et al. (2022, 2023); Team et al. (2024); Bjorck et al. (2025); Li et al. (2025); Black et al. (2024); Yang et al. (2025); Kim et al. (2024). These VLA tasks require agents to perceive complex visual scenes, reason over spatial and temporal contexts, and execute adaptive actions within dynamic environments, demanding robust long-horizon planning and contextual adaptation. However, 


Figure 1: **Overview of Fast-ThinkAct.** Previous reasoning VLAs generate lengthy reasoning traces ( _∼_ 250 tokens). Our approach learns compact continuous tokens (e.g., 6) (blue) and parallel spatial tokens (green) as internal reasoning. The bottom-right plot shows that we achieve 9 _._ 3 _×_ faster inference than ThinkAct-7B Huang et al. (2025), while delivering improved performance on the SimplerEnv-Google benchmark. 

as these VLA models primarily rely on supervised training from action data, they excel at basic skills (e.g., pick-and-place) but struggle to generalize beyond training distributions, such as long-horizon planning, self- 

Additional affiliations:<sup>1</sup> National Taiwan University.<sup>2</sup> University of Illinois Urbana-Champaign. © 2026 NVIDIA. All rights reserved. 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

correction from failures, and adaptation to novel scenarios, due to the impracticality of collecting exhaustive robot demonstrations. 

Reasoning VLAs Zawalski et al. (2024); Zhao et al. (2025); Lee et al. (2025); Wu et al. (2025); Qu et al. (2025); Huang et al. (2025); Kim et al. (2025) address these limitations by incorporating intermediate thinking processes, improving generalization and task-solving capability. Supervised chain-of-thought (CoT) methods Zawalski et al. (2024); Zhao et al. (2025); Lee et al. (2025); Qu et al. (2025) address this by learning from intermediate reasoning annotations. These approaches can be categorized into textual reasoning methods that leverage off-the-shelf LLMs and VLMs to generate pseudo CoT labels Zawalski et al. (2024), and visual reasoning methods that generate structured visual reasoning representations such as sub-goal images, image depth, and 2D visual traces Zhao et al. (2025); Lee et al. (2025). However, these supervised approaches require substantial reasoning annotations and remain limited by training data coverage. To address this, ThinkAct Huang et al. (2025) employs RL-based reasoning Shao et al. (2024) to generate long textual CoTs guided by action-aligned visual rewards. While these reasoning methods effectively improve task generalization and planning capabilities, they require generating lengthy chain-of-thought steps that introduce substantial reasoning latency, which hampers embodied applications with _real-time_ requirements. 

In embodied AI applications such as robotic manipulation and autonomous driving, agents must make rapid decisions at high frequencies (e.g., 1-15 Hz) Guan et al. (2025). However, generating lengthy reasoning traces can take several seconds per decision (e.g., 0.1 Hz) Huang et al. (2025); Lee et al. (2025), creating a critical bottleneck that limits real-time performance Guan et al. (2025); Yu et al. (2025) and poses safety risks in time-critical scenarios Wang et al. (2025). To mitigate this efficiency bottleneck while preserving reasoning capabilities, very recent works Chen et al. (2025); Yu et al. (2025); Guan et al. (2025) have explored approaches to reduce inference latency in embodied reasoning. For instance, ECoT-Lite Chen et al. (2025) proposes reasoning dropout to accelerate inference, yet directly reducing textual reasoning length risks performance degradation due to critical information loss. How to preserve reasoning capability while enabling compact representations that properly capture essential spatial-temporal dynamics remains a crucial challenge for reasoning VLA models. 

In this paper, we propose _Fast-ThinkAct_ , an efficient embodied reasoning framework for Vision-Language-Action tasks that achieves compact yet expressive planning through verbalizable latent reasoning. As depicted in Figure 1, unlike prior reasoning VLAs that generate lengthy explicit textual CoT traces, we introduce rewardguided preference distillation with visual trajectory alignment to compress linguistic and visual planning into compact continuous latents that enable implicit internal reasoning. Our student VLM encodes reasoning into compact latents decodable by a verbalizer, enabling preference-based optimization that leverages RL-derived reward signals to distill high-quality reasoning patterns from a textual teacher VLM while suppressing lowquality ones. We further align trajectory latents between teacher and student to transfer visual planning capabilities essential for embodied control. Once trained, the student VLM enables reasoning-enhanced policy learning that bridges implicit multimodal planning with action execution, achieving significantly faster inference while outperforming existing reasoning VLAs. 

Our contributions can be summarized as follows: 

- We propose _Fast-ThinkAct_ , an efficient reasoning framework that compresses reasoning into verbalizable latent thoughts while maintaining expressive planning abilities. 

- We introduce preference-guided distillation with manipulation trajectory alignment that compresses linguistic and visual planning into compact continuous latents. 

- We bridge high-level visual planning to low-level action execution through reasoning-enhanced policy learning guided by manipulation trajectory latents. 

- We achieve up to 89.3% inference latency reduction over state-of-the-art reasoning VLAs while maintaining strong performance across diverse embodied benchmarks. 

2 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

## **2. Related Works** 

### **2.1. Vision-Language-Action (VLA) Models** 

**Foundation VLAs.** Vision-Language-Action (VLA) models Brohan et al. (2022, 2023); Team et al. (2024); Bjorck et al. (2025); Li et al. (2025); Black et al. (2024); Yang et al. (2025); Pertsch et al. (2025); Driess et al. (2025); Bu et al. (2025); Team et al. (2025); Wang et al. (2025) have recently emerged as a promising paradigm for embodied AI by training vision-language backbones on large-scale robot demonstrations. Works such as OpenVLA Kim et al. (2024) and _𝜋_ 0 Black et al. (2024) achieve language-conditioned manipulation through end-to-end policy learning, while Magma Yang et al. (2025) co-trains on heterogeneous human and robot data. HAMSTER Li et al. (2025) and TraceVLA Zheng et al. (2024) further leverage 2D visual trajectories to boost spatial-action connections. Despite success on routine manipulation, these imitation-based approaches struggle with long-horizon planning and generalization to novel scenarios due to limited training data coverage. 

**Reasoning VLAs.** To overcome these limitations, recent works Zawalski et al. (2024); Zhao et al. (2025); Lee et al. (2025); Wu et al. (2025); Qu et al. (2025); Huang et al. (2025); Kim et al. (2025); Yuan et al. (2025); Abdolmaleki et al. (2025) integrate explicit reasoning mechanisms into VLA architectures. Supervised approaches Zawalski et al. (2024); Zhao et al. (2025); Lee et al. (2025); Qu et al. (2025) introduce intermediate reasoning through chain-of-thought annotations. Embodied CoT Zawalski et al. (2024) and Hi-Robot Shi et al. (2025) synthesize reasoning labels via pretrained foundation models. To perform vision-centric reasoning Man et al. (2025); Sarch et al. (2025) beyond pure text, CoT-VLA Zhao et al. (2025) employs visual goal generation and MolmoAct Lee et al. (2025) structures reasoning by spatial representations. Additionally, EO-1 Qu et al. (2025) introduces interleaved vision-language-action pre-training to bridge reasoning and interaction. Recent works Yuan et al. (2025); Huang et al. (2025) alternatively leverage reinforcement fine-tuning to generate reasoning chains with designed rewards. Despite improved generalization, these reasoning VLAs suffer from high inference latency and inevitably introduce extraneous information that degrades action quality. 

### **2.2. Efficient Reasoning** 

To address the inference latency of reasoning, recent LLM research explores various efficiency techniques Lee et al. (2025); Dai et al. (2025); Yuan et al. (2025); Xiang et al. (2025); Aggarwal and Welleck (2025); Lee et al. (2025). For example, RL-based approaches Dai et al. (2025); Yuan et al. (2025); Xiang et al. (2025); Aggarwal and Welleck (2025) introduce length penalties to encourage shorter reasoning chains, though such methods can suffer from training instability. Beyond length control, latent reasoning methods Hao et al. (2024); Shen et al. (2025); Zhang et al. (2025); Cheng and Van Durme (2024); Xu et al. (2025) enable reasoning in continuous spaces, such as Coconut Hao et al. (2024) using hidden states as continuous thoughts, CODI Shen et al. (2025) distilling explicit CoT into continuous space via teacher-student alignment, and Soft Thinking Zhang et al. (2025) generating weighted concept tokens. However, these LLM techniques cannot directly transfer to VLA tasks due to the need for spatial-temporal understanding and bridging semantic reasoning with embodied control. Recently, ECoT-Lite Chen et al. (2025) proposes reasoning dropout to accelerate embodied reasoning by skipping test-time reasoning traces. However, reasoning dropout can lead to inconsistent planning as it builds on supervised embodied CoT. Our proposed Fast-ThinkAct distills reasoning into compact latent representations that naturally encode multimodal information, enabling robust reasoning-enhanced policy learning. 

## **3. Method** 

### **3.1. Problem Formulation** 

We first define the setting and notations. At each timestep _𝑡_ , given a language instruction _𝑙_ , the model observes a visual input _𝑜𝑡_ and generates an action chunk _𝑎𝑡_ , represented as a sequence of continuous robot control vectors (e.g., 7- or 14-DOF for single- or bimanual robots, respectively). 

To address this problem, we propose Fast-ThinkAct, an efficient reasoning framework that bridges high-level 

3 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 


Figure 2: **Overview of Fast-ThinkAct.** (a) Given observation _𝑜𝑡_ and instruction _𝑙_ , the Textual Teacher VLM _ℱ𝜃_<sup>_𝑇_generates explicit reasoning chains.The Latent Student VLM</sup><sup>_ℱ𝜃_distills these into compact latent tokens</sup> **z** guided by reward preferences. Verbalizer LLM _𝒱𝜓_ decodes latents to text for preference-based learning via _ℒ_ verb, while _ℒ_ distill transfers visual planning capability from teacher, and spatial tokens enable parallel visual trajectory prediction via _ℒ_ ans, ensuring latents are verbalizable and grounded in visual planning. (b) Reasoning-Enhanced Policy Learning. The Action Model _𝜋𝜑_ is trained with _ℒ_ IL while freezing the latent student _ℱ𝜃_ and state encoder. 

planning with low-level action execution. Our approach employs a VLM _ℱ𝜃_ to perform reasoning in _continuous latent space_ , integrated with an action model _𝜋𝜑_ for executable action generation. Specifically, _ℱ𝜃_ processes observation-instruction pairs ( _𝑜𝑡, 𝑙_ ) through latent chain-of-thought (CoT) reasoning to produce a compact visual plan latent _𝑐𝑡_ that encapsulates the intended trajectory in visual space (Sec. 3.2). This _𝑐𝑡_ subsequently guides _𝜋𝜑_ to predict executable actions _𝑎𝑡_ (Sec. 3.3). By distilling reasoning into a continuous latent space rather than discrete text, Fast-ThinkAct achieves significantly improved inference efficiency while enhancing action performance through better preservation of spatial and visual information. 

### **3.2. Efficient Embodied Reasoning** 

To enable efficient embodied reasoning that meets the real-time requirements of embodied AI tasks, we aim to compress long textual CoTs into a compact set of continuous latent representations. However, compressing reasoning traces into latents is challenging, as there is no direct supervision signal in the latent space to guide what reasoning patterns should be encoded. 

#### **3.2.1. Verbalizable Latent CoT by Reward Preferences** 

To address this challenge, we propose to perform distillation in natural language space by introducing a verbalizer LLM that decodes latents into verbalizable reasoning. This approach grounds latent learning in an interpretable textual form, ensuring that the learned latents faithfully preserve the underlying reasoning structure. Since reasoning traces generated by the teacher model _ℱ𝜃_<sup>_𝑇_exhibitvaryingquality,weadopta</sup> preference-based learning framework that exploits reward signals from the teacher’s GRPO training to guide the latent student _ℱ𝜃_ toward high-quality reasoning patterns while suppressing low-quality ones. 

Specifically, we employ a teacher-student framework where a textual teacher model _ℱ𝜃_<sup>_𝑇_first learns explicit</sup> reasoning through GRPO Shao et al. (2024) training by maximizing: 


where _𝜏_ denotes a reasoning trace and _𝑟𝜃_ ( _𝜏_ ) = _ℱ_<sup>_ℱ_</sup> old _<u>𝜃</u>_<sup>_𝑇𝑇_</sup><sup><u>((</u></sup><sup>_𝜏𝜏_</sup><sup><u>))</u>is the probability ratio.The advantage function for group</sup> 

4 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

rewards _{𝑅𝑖}𝑖∈𝐺_ ( _𝜏_ ) is represented as: 


This training process produces textual CoTs with varying quality, where the advantage function _𝐴_ ( _𝜏_ ) naturally serves as a quality indicator. To construct preference pairs for distillation, we select the highest and lowest advantage traces from each rollout group: 


Instead of generating textual tokens, the student model _ℱ𝜃_ performs latent reasoning by autoregressively generating _𝑀_ continuous latent vectors **z** = _{𝑧𝑚}_<sup>_𝑀_</sup> _𝑚_ =1<sup>with</sup><sup>_𝑧𝑚∈_R</sup><sup>_𝑑_, where</sup><sup>_𝑑_is the hidden size.We then train</sup> the verbalizer LLM _𝒱𝜓_ to decode these latents **z** into natural language. The training objective encourages the verbalizer to assign a higher likelihood to decoding latents into high-quality reasoning _𝜏_<sup>+</sup> than low-quality reasoning _𝜏_<sup>_−_</sup> . Inspired by DPO Rafailov et al. (2023), we formulate this as an optimization guided by the reward preferences: 


where _𝑝_ ref is the reference model (i.e., _𝒱𝜓_ without latent conditioning), _𝜎_ is the sigmoid function, and _𝛽_ = 0 _._ 1 controls preference strength. This encourages the student VLM _ℱ𝜃_ to encode latents that the verbalizer decodes into high-quality reasoning while suppressing low-quality patterns. 

#### **3.2.2. Action-Aligned Visual Plan Distillation** 

While the verbalizer loss (Eq. 4) enables the student _ℱ𝜃_ to capture high-level reasoning patterns, it does not explicitly ensure that latent representations encode the visual planning capability crucial for embodied control. To address this, we introduce action-aligned visual plan distillation to transfer the teacher _ℱ𝜃_<sup>_𝑇_’s spatial</sup> reasoning ability to the student _ℱ𝜃_ . 

We distill spatial reasoning from the teacher, which is trained with trajectory-level rewards (e.g., goal completion and trajectory alignment Huang et al. (2025)) for grounded visual planning. We align the trajectory-level representations by minimizing the L2 distance between hidden states of the `<answer>` token that encodes the visual plan: 


where _ℎ_<sup>_𝑇_</sup> _𝑡_<sup>and</sup><sup>_ℎ𝑡_are the hidden states from teacher (corresponding to</sup><sup>_𝜏_+) and student, respectively.</sup> 

To enable efficient parallel trajectory prediction, unlike the textual teacher that autoregressively generates verbose text sequences of waypoints _{𝑝𝑘}_<sup>_𝐾_</sup> _𝑘_ =1<sup>with</sup><sup>_𝑝𝑘∈_[0</sup><sup>_,_1]2(tokenized into 60-70 tokens when</sup><sup>_𝐾_= 5), the</sup> student uses _𝐾_ learnable spatial tokens _{_ **s** _𝑖}_<sup>_𝐾_</sup> _𝑖_ =1<sup>appended to the reasoning latent sequence, with each output</sup> hidden state simultaneously projected to a waypoint via an MLP. The total objective for training _ℱ𝜃_ combines all three components: 


where _ℎ_<sup>_′_</sup> ( **s** _𝑖_ ) denotes the output hidden state of the _𝑖_ -th spatial token and _𝑝_ ˆ _𝑖_ are ground-truth waypoints. Through this unified framework, the student model _ℱ𝜃_ performs compact yet expressive latent reasoning and generates visual trajectory plans efficiently. 

5 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 


Figure 3: **Evaluation of robot manipulation and reasoning efficiency.** (a)-(e) Success rates on LIBERO Liu et al. (2023) and SimplerEnv Li et al. (2024) benchmarks compared with state-of-the-art 7B reasoning VLAs. (f) Latency comparison across 3B and 7B reasoning VLAs. Our approach achieves up to 89.3% inference latency reduction while maintaining superior task success rates. 

### **3.3. Reasoning-Enhanced Policy Learning** 

After the student VLM _ℱ𝜃_ performs compact latent reasoning and generates visual trajectory planning through spatial tokens, we leverage these representations to guide a diffusion Transformer-based action model _𝜋𝜑_ (e.g., RDT Liu et al. (2024)) for action prediction. To bridge the high-level visual planning with low-level action generation, we connect the visual latent planning _𝑐𝑡_ encoded in the key-value cache corresponding to the spatial tokens to the action model. 

Specifically, we extract visual latent planning _𝑐𝑡_ from the KV cache of spatial tokens in earlier VLM layers (since _ℱ𝜃_ has more layers than _𝜋𝜑_ ) and concatenate with KV pairs from the action model’s state encoder. The action model’s cross-attention then attends to both the visual planning context and state observations. We post-train on action-annotated robot data by _freezing ℱ𝜃_ and the state encoder while updating only _𝜋𝜑_ with the imitation learning objective: 


where _ℓ_ denotes the denoising objective for diffusion policy and ˆ _𝑎𝑡_ is the ground-truth action. Through this posttraining, the action model effectively translates visual planning from compact latent reasoning into low-level robot actions. 

### **3.4. Learning Strategy and Inference** 

**Training Strategy.** We initialize both teacher _ℱ𝜃_<sup>_𝑇_and student</sup><sup>_ℱ𝜃_from the same checkpoint obtained through</sup> SFT and CoT-SFT on a pre-trained VLM. The teacher is trained with GRPO using action-aligned rewards Huang et al. (2025), while the student is trained with _ℒ_ student to compress reasoning into compact latents. We then connect the trained _ℱ𝜃_ with action model _𝜋𝜑_ (initialized from Liu et al. (2024)) by freezing _ℱ𝜃_ and the state encoder while updating the latent projector and _𝜋𝜑_ with _ℒ_ IL on large-scale robotic data. For target environment adaptation (e.g., LIBERO Liu et al. (2023), RoboTwin2.0 Chen et al. (2025)), we fine-tune on environment-specific demonstrations. 

**Inference.** The _ℱ𝜃_ processes ( _𝑜𝑡, 𝑙_ ) by compact latent reasoning, generating visual trajectories via _𝐾_ spatial tokens. The visual latent planning _𝑐𝑡_ , extracted from the spatial tokens’ KV cache, conditions _𝜋𝜑_ to predict 

6 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

actions _𝑎𝑡_ . Inference requires only _ℱ𝜃_ and _𝜋𝜑_ ; the verbalizer _𝒱𝜓_ is used solely during training and optionally for interpretability. 

## **4. Experiment** 

### **4.1. Experimental Setup** 

#### **Implementation Details.** 

We use Qwen2.5-VL 3B Bai et al. (2025) as the VLM backbone. The SFT stage runs for 1 epoch with batch size 64 and learning rate 1e _−_ 5, followed by CoT-SFT for 15K iterations with the same hyperparameters. For teacher-student training, both _ℱ𝜃_<sup>_𝑇_and</sup><sup>_ℱ𝜃_are initialized from the CoT-SFT checkpoint and trained for 4,500</sup> iterations with batch size 128 and learning rate 1e _−_ 6. The teacher is optimized with GRPO Shao et al. (2024) using action-aligned visual rewards Huang et al. (2025) and QA-style rewards (detailed in supplementary material). For the first 3,000 iterations of the student training, we train the verbalizer _𝒱𝜓_ with standard language modeling loss, then switch to _ℒ_ verb for the remaining 1,500 iterations. For reasoning-enhanced policy learning, we initialize _𝜋𝜑_ from DiT-Policy Chi et al. (2023) pre-trained on OXE O’Neill et al. (2024) for SimplerEnv, and from RDT Liu et al. (2024) for LIBERO and RoboTwin2.0. A linear projection adapts the VLM’s KV cache to the action model dimension (1,024 for DiT-Policy and 2,048 for RDT). Training runs for 20K iterations with batch size 256 and learning rate 1e _−_ 4. All diffusion hyperparameters follow those of the respective action models. All experiments are conducted on 16 NVIDIA A100 GPUs with 80 GB memory. 

#### **Training Datasets and Evaluation Benchmarks.** 

For reasoning VLM training, we utilize single-arm visual trajectories labeled by Lee et al. (2025) and dual-arm visual trajectories from the AIST dataset Motoda et al. (2025), along with QA tasks from PixMo Deitke et al. (2024), RoboFAC Lu et al. (2025), RoboVQA Sermanet et al. (2024), ShareRobot Ji et al. (2025), EgoPlan Chen et al. (2023), and Video-R1 Feng et al. (2025). For reasoning-enhanced policy learning, we use action data from the OXE dataset O’Neill et al. (2024) (following OpenVLA Kim et al. (2024)) when training with DiT-Policy, and augment with bimanual data from the static Aloha dataset Shi et al. (2023); Zhao et al. (2023) when training with RDT. 

We evaluate Fast-ThinkAct on four embodied reasoning benchmarks and three robot manipulation benchmarks. For embodied reasoning, we use EgoPlan-Bench2 Qiu et al. (2024) (accuracy on multiple-choice questions), RoboVQA Sermanet et al. (2024) (BLEU score Papineni et al. (2002)), OpenEQA Majumdar et al. (2024), and RoboFAC Lu et al. (2025) (both using LLM-based scoring). Notably, RoboVQA and RoboFAC contain videos captured from real robots. For robot manipulation, we evaluate on SimplerEnv Li et al. (2024), which demonstrates strong correlation with real-world performance, LIBERO Liu et al. (2023) covering diverse manipulation tasks including long-horizon scenarios, and RoboTwin2.0 Chen et al. (2025) for complex bimanual manipulation. All robot manipulation tasks use task success rate as the metric. Additional details are provided in the supplementary material. 

### **4.2. Quantitative Evaluation** 

#### **Robot Manipulation.** 

We evaluate Fast-ThinkAct on robotic manipulation using LIBERO Liu et al. (2023) and SimplerEnv Li et al. (2024) benchmarks. LIBERO covers diverse subtasks, including Spatial, Object, Goal, and Long, while SimplerEnv provides a simulated benchmark with strong real-world correlation, featuring variations in lighting, object appearance, and camera viewpoints. As shown in Fig. 3(a)-(e), Fast-ThinkAct consistently outperforms all baselines, achieving the highest success rates across all LIBERO subtasks and SimplerEnv-Google. This includes substantial improvements over foundation VLAs such as OpenVLA Kim et al. (2024), and reasoning VLAs including CoT-VLA Zhao et al. (2025), ThinkAct Huang et al. (2025), and MolmoAct Lee et al. (2025). Moreover, as shown in Fig. 3(f), our compact latent reasoning achieves 89.3% and 88.0% latency reduction 

7 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

Table 1: **Quantitative evaluation on RoboTwin2.0 Chen et al. (2025).** E and H denote easy and hard settings (without/with domain randomization). Background colors indicate task length based on expert demonstrations: <mark>short (80-100) , medium (110-220)</mark> , long (270-470) steps. 

|Model|clic<br>alar|k<br>m|click<br>bell|tur<br>swit|n<br>ch|adjust<br>bottle|be<br>blo|at<br>ck|hand<br>m|over<br>ic|hand<br>blo|over<br>ck|hanging<br>mug|stack<br>blocks two|st<br>bowl|ack<br>s three|Ave|rage|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||E|H|E<br>H|E|H|E<br>H|E|H|E|H|E|H|E<br>H|E<br>H|E|H|E|H|
|DPChi et al.(2023)|61|5|54<br>0|36|1|97<br>0|42|0|53|0|10|0|8<br>0|7<br>0|63|0|43.1|0.6|
|ACTZhao et al.(2023)|32|4|58<br>3|5|2|97<br>23|56|3|85|0|42|0|7<br>0|25<br>0|48|0|45.5|3.5|
|_𝜋_0 Black et al.(2024)|63|11|44<br>3|27|23|90<br>56|43|21|98|13|45|8|11<br>3|42<br>1|66|24|52.9|16.3|
|RDTLiu et al.(2024)|61|12|80<br>9|35|15|81<br>75|77|37|90|31|45|14|23<br>16|21<br>2|51|17|56.4|22.8|
|ThinkActHuang et al.(2025)|64|13|84<br>11|40|19|94<br>70|79|33|92|40|56|15|31<br>18|30<br>5|54|23|62.4|24.7|
|**Fast-ThinkAct**|70|17|82<br>12|37|21|92<br>72|82|33|99|42|65|15|30<br>22|45<br>5|55|25|**65.7**|**26.4**|


Table 2: **Quantitative evaluation on EgoPlan-Bench2 Qiu et al. (2024), RoboVQA Sermanet et al. (2024), and OpenEQA Majumdar et al. (2024) benchmarks for embodied reasoning.** 

|**Method**||**Ego**|**Plan-Be**|**nch2**||||**RoboVQ**|**A**||**OpenEQA**|**Overall**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Daily.|Work.|Rec.|Hobbies|Avg.|B-1|B-2|B-3|B-4|B-Avg.|Score|Avg.|
|GPT-4VAchiam et al.(2023)|36.7|27.7|33.9|32.5|32.6|32.2|26.5|24.7|23.9|26.8|49.6|36.4|
|Gemini-2.5-FlashComanici et al.(2025)|44.2|42.3|43.2|39.1|42.4|39.1|31.6|22.9|22.1|28.9|45.3|38.9|
|InternVL2.5-2BChen et al.(2024)|30.9|27.8|28.6|33.1|30.1|36.6|33.7|31.0|29.4|32.7|47.1|36.6|
|InternVL3-2BZhu et al.(2025)|36.9|29.9|35.6|31.5|33.4|34.4|33.9|33.5|33.3|33.8|48.8|38.7|
|NVILA-2BLiu et al.(2024)|34.6|26.7|33.3|31.6|31.4|38.7|34.3|31.1|29.2|33.3|47.0|37.2|
|Qwen2.5-VL-3BBai et al.(2025)|29.0|27.0|30.2|28.9|28.5|42.5|36.3|28.7|31.8|34.8|43.4|35.6|
|Magma-8BYang et al.(2025)|32.1|25.7|34.4|29.3|29.8|38.6|31.5|28.1|26.7|31.2|49.1|36.7|
|RoboBrain2.0-3BTeam et al.(2025)|45.3|37.6|45.9|39.7|41.8|54.4|47.7|43.1|41.0|46.5|50.1|46.1|
|ThinkAct-3BHuang et al.(2025)|46.6|41.4|45.9|42.5|44.0|62.4|57.3|52.0|49.6|55.3|48.9|49.4|
|**Fast-ThinkAct-3B**|**50.3**|**44.3**|**46.4**|**43.2**|**46.4**|**70.1**|**63.0**|**57.2**|**53.0**|**60.8**|**51.2**|**52.8**|


compared to ThinkAct-7B Huang et al. (2025) and MolmoAct-7B Lee et al. (2025) respectively, and 7 _×_ faster inference than ThinkAct-3B, demonstrating substantial efficiency gains without sacrificing performance. 

To further validate Fast-ThinkAct on more complex scenarios, we evaluate on RoboTwin2.0 Chen et al. (2025), a challenging bimanual manipulation benchmark requiring long-horizon planning. As shown in Tab. 1, FastThinkAct significantly outperforms previous VLAs including DP Chi et al. (2023), ACT Zhao et al. (2023), _𝜋_ 0 Black et al. (2024), RDT Liu et al. (2024), and ThinkAct Huang et al. (2025) across both easy and hard settings. Compared to RDT, Fast-ThinkAct achieves 9.3% and 3.6% higher success rates on easy and hard settings, respectively. Against the reasoning VLA ThinkAct, it improves success by 3.3% and 1.7% while maintaining substantially higher efficiency, as shown in Fig. 3(f). These results demonstrate that our compact reasoning design enables both superior accuracy and computational efficiency on complex bimanual manipulation tasks. 

#### **Embodied Reasoning.** 

In Tab. 2, we evaluate the reasoning capabilities of Fast-ThinkAct in embodied scenarios across three benchmarks: EgoPlan-Bench2 Qiu et al. (2024), RoboVQA Sermanet et al. (2024), and OpenEQA Majumdar et al. (2024). These benchmarks assess multi-step planning in egocentric everyday scenarios, long-horizon reasoning for robotic manipulation tasks, and zero-shot understanding of embodied scenes in diverse environments, respectively. We observed that, Fast-ThinkAct surpasses all comparison methods, including two proprietary models (i.e., GPT-4V Achiam et al. (2023) and Gemini-2.5-Flash Comanici et al. (2025)), exceeding the runner-up by 2.4% on EgoPlan-Bench2, 5.5 BLEU score on RoboVQA, and 1.1 points on OpenEQA. These results demonstrate that Fast-ThinkAct effectively handles complex planning sequences and extended reasoning horizons while generalizing to novel environments, showcasing robust capabilities for scene comprehension and multi-step task execution in embodied AI applications. 

### **4.3. Analysis of Fast-ThinkAct** 

#### **Reasoning Enables Long-Horizon Planning.** 

8 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 


Figure 4: **Visualization of predicted visual trajectories and action execution results on long-horizon tasks.** Examples from (a) SimplerEnv-Google, (b) LIBERO-Long, and (c) RoboTwin2.0-Hard with long (278) steps. Yellow traces indicate single-arm/left gripper trajectories; red traces indicate right gripper trajectories for bimanual tasks. 

Figure 5: **Failure recovery capability on RoboFAC Lu et al. (2025).** Left: Qualitative examples (from both simulation and real robot) of corrective guidance for manipulation errors. Right: Quantitative evaluation on simulation (RoboFAC-Sim) and real-robot (RoboFAC-Real) settings. 

We analyze Fast-ThinkAct’s capability on long-horizon tasks in Tab. 1 and Fig. 4. We focus on longhorizon tasks (average length exceeding 270 steps) in RoboTwin2.0 Chen et al. (2025) that require multistep reasoning and extended planning horizons. As shown in Tab. 1, Fast-ThinkAct achieves average scores of 48.8 and 16.8 on easy and hard settings of longhorizon tasks, respectively, surpassing RDT (35.0/12.3) and ThinkAct (42.8/15.3). Fig. 4 visualizes predicted 2D visual traces and execution results on representative tasks from SimplerEnv-Google Li et al. (2024), LIBEROLong Liu et al. (2023), and RoboTwin2.0 Chen et al. (2025). For example, the LIBERO-Long task requires se- 


Figure 6: **Few-shot adaptation results on RoboTwin2.0 benchmark.** We use 10 demonstrations per task for fine-tuning. 

quentially turning on the stove and placing a moka pot on it, while the RoboTwin2.0 handover task requires bimanual coordination to transfer a block between grippers. The visual traces successfully predict feasible solution paths, with their corresponding representations serving as visual planning guidance for successful execution. These results demonstrate that our compact latent reasoning effectively supports long-horizon 

9 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

#### planning in complex manipulation scenarios. 

#### **Reasoning Enables Failure Recovery.** 

A key advantage of reasoning-based VLAs Huang et al. (2025); Abdolmaleki et al. (2025) is their ability to identify runtime failures and provide corrective guidance for recovery. To evaluate this capability, we conduct experiments on RoboFAC Lu et al. **Question:** Pick up the glass. Is it satisfied? **GT:** yes (2025), a benchmark specifically designed to assess failure identification and correction in embodied Let me think about this. I can see a cluttered table with several objects scattered around. The robot arm moves slowly toward the VLMs. As shown in Fig. 5, Fast-ThinkAct substanglass, adjusting its position to avoid bumping into nearby items. The gripper closes gently around the glass and lifts it from the tially outperforms the second-best baseline RoboFACtable with a steady motion. The glass is held securely and remains 3B Lu et al. (2025) by 10.9 points on the simulation stable in the air. Everything looks correct, so the action is satisfied. split and 16.4 points on the real-world split. The (a) Textual reasoning (from teacher model) qualitative examples demonstrate Fast-ThinkAct’s Let me think. The robot arm moves carefully over the table, aligns ability to reason over manipulation videos, identify with the glass, and grips it. The glass lifts smoothly without tipping or slipping. It looks like the task is successful and satisfied. failures, and propose recovery steps. For instance, (b) Verbalized reasoning in the right example where the target object drops mid-execution, Fast-ThinkAct generates a concrete Figure 7: **Reasoning trace comparison on RoboVQA.** recovery plan: first moving the arm backward to cre(a) Teacher’s textual reasoning. (b) Student’s verbalized ate space, then adjusting laterally to align with the latent reasoning. Green:: relevant content; orange: orange:: less relevant content. target object, and finally lowering to the appropriate height for a secure grasp. These results demonstrate that our latent reasoning supports both fast task execution and crucial failure analysis capabilities essential for robust robotic manipulation. 

Figure 7: **Reasoning trace comparison on RoboVQA.** (a) Teacher’s textual reasoning. (b) Student’s verbalized latent reasoning. Green:: relevant content; orange: orange:: less relevant content. 

#### **Reasoning Enables Few-Shot Adaptation.** 

To assess how reasoning capability improves few-shot adaptation, we conduct few-shot experiments on the RoboTwin2.0 benchmark Chen et al. (2025), fine-tuning models using only 10 demonstrations per task. As illustrated in Fig. 6, Fast-ThinkAct significantly enhances our adopted action model RDT Liu et al. (2024) and outperforms the state-of-theart VLAs, including _𝜋_ 0 Black et al. (2024) and ThinkAct Huang et al. (2025) on both medium and long-horizon tasks. Notably, our method achieves these gains while operating with significantly lower reasoning latency compared to ThinkAct, highlighting the advantage of ef- 

Table 3: **Ablation study of training objectives and learning stages.** Note that Fast-ThinkAct w/o _ℒ_ verb _, ℒ_ distill denotes the student VLM _ℱ𝜃_ trained without the corresponding loss components. 

|**Method**|**EgoPlan**|**RoboVQA**|**OpenEQA**|**Average**|
|---|---|---|---|---|
|**Fast-ThinkAct**|**46.4**|**60.8**|**51.2**|**52.8**|
|w/o_ℒ_verb|42.1|53.8|49.5|48.5|
|w/o_ℒ_verb_, ℒ_distill|41.6|52.7|48.9|47.7|
|Textual Teacher_ℱ_<sup>_𝑇_</sup><br>_𝜃_|41.7|58.2|49.4|49.8|
|SFT + CoT-SFT|40.0|46.1|48.8|45.0|
|SFT only|40.5|53.6|45.3|46.5|


ficient yet effective reasoning for few-shot action adaptation in complex robot manipulation scenarios. 

#### **Visualization of Verbalizable Latent Reasoning.** 

In Fig. 7, we compare the teacher’s textual reasoning with the student’s verbalized latent reasoning on RoboVQA. While both capture task-relevant information (green), the teacher generates verbose outputs with less directly relevant content (orange), whereas our student produces more concise and focused responses when verbalized. This demonstrates that our preference-guided distillation not only reduces computational cost but also distills concise reasoning patterns while filtering out redundant information. 

10 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

#### **Ablation Study.** 

In Tab. 3, we ablate training stages and loss components. Starting from the full Fast-ThinkAct, removing _ℒ_ verb causes performance drops as latent CoTs lack preference-based guidance to align with high-quality reasoning and suppress low-quality patterns. Further removing _ℒ_ distill leads to additional decline, indicating that aligning trajectory-level representations is crucial for transferring visual planning capabilities. Comparing training strategies, CoT-SFT underperforms SFT on EgoPlan-Bench2 and RoboVQA but improves on OpenEQA, suggesting naïve chain-of-thought supervision benefits open-ended QA but introduces verbosity that hinders structured reasoning tasks. Our preference-guided approach distills high-quality reasoning while maintaining efficiency. This validates the necessity of our proposed distillation framework and visual trajectory alignment. We provide additional ablation studies in the supplementary material. 

## **5. Conclusion** 

We presented _Fast-ThinkAct_ , an efficient reasoning framework for vision-language-action tasks that achieves compact yet expressive planning through verbalizable latent reasoning. By distilling lengthy textual reasoning into compact latent representations via preference-guided distillation and visual trajectory alignment, our approach bridges high-level embodied reasoning with low-level action execution through reasoning-enhanced policy learning. Extensive experiments across diverse robotic manipulation and embodied reasoning benchmarks demonstrate that Fast-ThinkAct achieves strong performance with significantly reduced inference latency while enabling effective long-horizon planning, few-shot adaptation, and failure recovery capabilities. 

**Limitations and Future Works.** As our verbalizer _𝒱𝜓_ is built upon a pre-trained LLM, it inevitably inherits language model limitations, including hallucination, occasionally producing plausible but inaccurate descriptions. However, this does not affect action execution during inference, as the verbalizer serves only for interpretability while action prediction uses the grounded latent representations from visual plan distillation. To further improve the faithfulness of verbalized reasoning, we can consider incorporating grounding-aware objectives or hallucination suppression techniques in future work. 

11 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

## **A. Additional Experimental Setup** 

### **A.1. Algorithm** 

**Algorithm 1:** Training Fast-ThinkAct (Sec. 3.2) 

**Input:** CoT-SFT checkpoint _ℱ𝜃_ 0, training data _𝒟_ , rollout size _𝑁_ , latent reasoning steps _𝑀_ , number of waypoints _𝐾_ , total iterations _𝑇_ total 

**Output:** Trained student model _ℱ𝜃_ 

`// Initialize models` _ℱ𝜃_<sup>_𝑇←ℱ𝜃_</sup> 0<sup>,</sup><sup>_ℱ𝜃←ℱ𝜃_</sup> 0<sup>;</sup> Initialize verbalizer _𝒱𝜓_ from pre-trained LLM; _𝑡 ←_ 0; **while** _𝑡< 𝑇total_ **do** Sample batch ( _𝑜, 𝑙,_ ˆ _𝑝_ ) from _𝒟_ ; 

```
//Supposebs=1forsimplicity
```

`// Teacher GRPO training` Generate _𝑁_ rollouts _{𝜏𝑖}_<sup>_𝑁_</sup> _𝑖_ =1<sup>from</sup><sup>_ℱ_</sup> _𝜃_<sup>_𝑇_(</sup><sup>_𝑜, 𝑙_);</sup> Compute trajectory rewards _{𝑟𝑖}_<sup>_𝑁_</sup> _𝑖_ =1<sup>;</sup> Compute group-wise advantages _{𝐴𝑖}_<sup>_𝑁_</sup> _𝑖_ =1<sup>;</sup> Update _ℱ𝜃_<sup>_𝑇_with</sup><sup>_𝒥_GRPO(Eq. 1);</sup> _𝜏_<sup>+</sup> _←_ arg max _𝑖 𝐴𝑖_ , _𝜏_<sup>_−_</sup> _←_ arg min _𝑖 𝐴𝑖_ (Eq. 3) ; `// For student distillation` _ℎ_<sup>_𝑇_</sup> _𝑡_<sup>_←_hidden state of</sup><sup>_𝜏_+at</sup><sup>`<answer>`token from</sup><sup>_ℱ_</sup> _𝜃_<sup>_𝑇_;</sup> `// For distillation loss` 

`// Student latent distillation` **z** = _{𝑧𝑚}_<sup>_𝑀_</sup> _𝑚_ =1<sup>_←ℱ𝜃_(</sup><sup>_𝑜, 𝑙_) ;</sup> `// Perform auto-regressive latent reasoning` Compute _ℒ_ verb with **z** , _𝒱𝜓_ , _𝜏_<sup>+</sup> , _𝜏_<sup>_−_</sup> (Eq. 4); Forward _𝐾_ spatial tokens from _ℱ𝜃_ ( _𝑜, 𝑙,_ **z** ) to obtain _ℎ𝑡_ and _{ℎ_<sup>_′_</sup> ( **s** _𝑖_ ) _}_<sup>_𝐾_</sup> _𝑖_ =1<sup>;</sup> Compute _ℒ_ distill with _ℎ_<sup>_𝑇_</sup> _𝑡_<sup>,</sup><sup>_ℎ𝑡_(Eq. 5);</sup> Compute _ℒ_ ans with _{ℎ_<sup>_′_</sup> ( **s** _𝑖_ ) _}_<sup>_𝐾_</sup> _𝑖_ =1<sup>,</sup><sup>_𝑝_ˆ(Eq. 6);</sup> Update _ℱ𝜃_ with _ℒ_ student = _ℒ_ verb + _ℒ_ distill + _ℒ_ ans; _𝑡 ← 𝑡_ + 1; 

#### **end** 

**return** _ℱ𝜃_ ; 

Algorithm 1 presents the complete training procedure corresponding to Sec. 3.2. It shows how we jointly optimize the teacher model with GRPO and distill its reasoning into the student’s compact latent representations. 

### **A.2. Implementation Details** 

Our implementation follows the setup described in Sec. 4.1 of the main paper. Here we provide additional details. The verbalizer _𝒱𝜓_ is initialized from a small LLM, Qwen3-0.6B, with cross-attention layers inserted at each layer to condition on latent CoTs **z** . For the student model training, in the first 3,000 iterations, we replace verbalization loss _ℒ_ verb with language modeling loss using _𝜏_<sup>+</sup> as ground truth to warm up _𝒱𝜓_ ’s alignment with the latent representations **z** . We then freeze _𝒱𝜓_ and use the _ℒ_ verb for the remaining 1,500 iterations. The student _ℱ𝜃_ is optimized throughout both phases. For waypoint prediction in Eq. 6, each _𝑝𝑖 ∈_ R<sup>6</sup> encodes coordinates in the format [ _𝑥_ single _, 𝑦_ single _, 𝑥_ left _, 𝑦_ left _, 𝑥_ right _, 𝑦_ right], where the first two dimensions are for single-arm and the last four are for bimanual robot. For ground-truth _𝑝𝑖_ ˆ , we fill the corresponding dimensions based on robot type and mask out the unused dimensions when computing _ℒ_ ans. For GRPO training, we follow the configuration of ThinkAct Huang et al. (2025), using rollout size _𝑁_ = 5. Following Lee et al. (2025), we set the number of waypoints in trajectory to _𝐾_ = 5. We use _𝑀_ = 6 latent reasoning tokens, with ablation study provided in Fig. 8. 

12 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

During reasoning-enhanced policy learning, for SimplerEnv Li et al. (2024) evaluation, to ensure fair comparison with previous works Kim et al. (2024); Lee et al. (2025), we initialize _𝜋𝜑_ from DiT-Policy Chi et al. (2023) pre-trained on the same OXE dataset O’Neill et al. (2024); Kim et al. (2024) and conduct reasoning-enhanced policy learning (Sec. 3.3) using the same OXE data. For LIBERO Liu et al. (2023) and RoboTwin2.0 Chen et al. (2025) evaluations, we initialize _𝜋𝜑_ from RDT Liu et al. (2024), which has demonstrated strong performance on RoboTwin2.0, and conduct policy learning using OXE O’Neill et al. (2024) and static ALOHA datasets Shi et al. (2023); Zhao et al. (2023). Our method further enhances RDT’s manipulation capabilities on both benchmarks. The use of different action models also demonstrates that our approach is agnostic to the underlying action model choice. 

### **A.3. Training Data Details** 

#### **A.3.1. Dataset Sources** 

#### **2D Visual Trace of Manipulation Tasks.** 

For single-arm manipulation, we utilize 2D visual trajectories labeled by MolmoAct Lee et al. (2025) from the Open X-Embodiment (OXE) dataset O’Neill et al. (2024), comprising approximately 1.3M trajectories. For bimanual manipulation, we extract dual-arm visual trajectories from the AIST dataset Motoda et al. (2025), resulting in approximately 92K trajectory samples. Specifically, we first use Molmo-72B Deitke et al. (2024) to detect left and right gripper positions (following Lee et al. (2025)) in the first frame, then apply CoTracker3 Karaev et al. (2025) to track and parse the manipulation trajectories throughout the video sequences. 

#### **RoboFAC Lu et al. (2025).** 

RoboFAC is a robotic failure analysis dataset containing 9,440 erroneous manipulation trajectories across 16 tasks in both simulated and real-world environments. We utilize the training set with 64K QA pairs covering various failure types for developing failure identification and correction planning capabilities. 

#### **RoboVQA Sermanet et al. (2024).** 

RoboVQA contains robot manipulation videos with QA tasks covering task understanding. The dataset includes approximately 5K long-horizon and 92K medium-horizon video sequences from diverse robotic platforms, resulting in total 798K QA pairs. Videos are annotated with multiple questions probing spatial reasoning, action prediction, and task comprehension. 

#### **ShareRobot Ji et al. (2025).** 

ShareRobot is a large-scale dataset collected by RoboBrain Ji et al. (2025), containing over 1M QA pairs covering task planning, object affordances, and manipulation strategies across diverse robot embodiments and scenes. The dataset features fine-grained annotations linking task descriptions to frame-level execution details, facilitating learning of transferable manipulation knowledge. 

#### **EgoPlan-Bench Chen et al. (2023).** 

EgoPlan-Bench features egocentric videos of daily activities annotated with task planning information including goals, execution history, and current states. The dataset contains approximately 53K video-text pairs for training long-horizon planning and progress tracking capabilities from egocentric view. 

#### **Video-R1-CoT Feng et al. (2025).** 

Video-R1 comprises 165K video question-answer pairs with chain-of-thought reasoning annotations generated by large-scale vision-language models. The dataset covers diverse reasoning domains including mathematical logic, spatial understanding, OCR, and visual analytics. All samples are quality-filtered to ensure annotation consistency and correctness. 

#### **PixMo Deitke et al. (2024).** 

PixMo is a general-purpose vision-language dataset with diverse image captions and question-answer pairs. Following MolmoAct Lee et al. (2025), we incorporate PixMo dataset to preserve general visual understanding 

13 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

Table 4: **Quantitative results with larger model size (7B or 8B) on embodied reasoning benchmarks.** 

|**Method**||**Ego**|**Plan-Be**|**nch2**||||**RoboV**|**QA**||**OpenEQA**|**Overall**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Daily.|Work.|Rec.|Hobbies|Avg.|B-1|B-2|B-3|B-4|B-Avg.|Score|Avg.|
|InternVL2.5-8BChen et al.(2024)|36.2|28.7|34.4|35.4|33.5|40.5|33.3|29.6|27.5|32.7|54.4|40.2|
|InternVL3-8BZhu et al.(2025)|38.5|32.9|36.1|37.2|36.2|44.3|36.5|31.6|28.9|35.3|55.5|42.3|
|NVILA-8BLiu et al.(2024)|35.8|28.7|37.2|35.4|33.7|42.7|39.7|37.6|36.1|39.0|54.0|42.2|
|Qwen2.5-VL-7BBai et al.(2025)|31.4|26.7|29.5|28.6|29.1|47.8|41.2|36.2|33.7|39.7|50.8|39.9|
|Magma-8BYang et al.(2025)|32.1|25.7|34.4|29.3|29.8|38.6|31.5|28.1|26.7|31.2|49.1|36.7|
|RoboBrain2.0-7BTeam et al.(2025)|39.4|27.0|33.9|32.2|33.2|44.9|38.2|34.7|33.5|37.8|51.1|40.7|
|ThinkAct-7BHuang et al.(2025)|50.1|49.8|44.8|45.2|48.2|69.1|61.8|56.0|52.4|59.8|56.2|54.7|
|Fast-ThinkAct-7B|51.3|47.3|41.5|45.9|47.5|70.4|63.3|57.3|53.2|61.1|59.0|**55.9**|


Table 5: **Results on LIBERO and SimplerEnv benchmarks with additional ThinkAct-3B comparison.** 

|**Method**|**LIBERO**|**SimplerEnv-Google**|**Latency (**_↓_**)**|
|---|---|---|---|
|OpenVLA-7BKim et al.(2024)|76.5|40.2|N/A|
|CoT-VLA-7BZhao et al.(2025)|83.9|N/A|N/A|
|ThinkAct-7BHuang et al.(2025)|84.4|68.3|7513|
|MolmoAct-7BLee et al.(2025)|86.8|64.9|6723|
|ThinkAct-3BHuang et al.(2025)|83.1|64.7|5674|
|**Fast-ThinkAct-3B**|**89.7**|**68.7**|**805 (**_↓_**7.0**_×_**)**|


and prevent catastrophic forgetting when training on embodied dataset. Specifically, we use approximately 726K samples from the `ask_model_anything` , `cap` , and `cap-qa` splits. 

#### **A.3.2. Data Processing and Formatting** 

#### **Supervised Fine-Tuning (SFT).** 

To enhance foundational embodied knowledge, we perform supervised fine-tuning on approximately 4M samples combining 2D visual trajectories from MolmoAct Lee et al. (2025) and AIST Motoda et al. (2025), along with QA data from PixMo Deitke et al. (2024), RoboFAC Lu et al. (2025), RoboVQA Sermanet et al. (2024), ShareRobot Ji et al. (2025), and EgoPlan Chen et al. (2023). This stage enables the model to acquire basic visual understanding, task comprehension, and manipulation knowledge across diverse embodiments and scenarios. 

#### **Chain-of-Thought SFT (CoT-SFT).** 

To develop reasoning capabilities while preserving embodied understanding, we sample 5% from the SFT data (approximately 200K samples) and augment with 165K samples from Video-R1-CoT Feng et al. (2025). For data with CoT annotations, we format prompts to elicit structured reasoning enclosed in `<think>` tags followed by answers in `<answer>` tags; for data without CoT annotations, we prompt for direct answers only. This enables the model to learn reasoning capabilities from CoT-annotated data and generalize them to embodied tasks. 

#### **Teacher-Student Training.** 

Building upon the CoT-SFT checkpoint, we curate a balanced training set by sampling approximately 5,000 instances from each dataset and data type, totaling nearly 50K samples. We adopt the prompt formatting strategy from CoT-SFT for both teacher GRPO training and student latent distillation. We train both the teacher with GRPO and the student with latent distillation (as detailed in Sec. 3.2) on this data, efficiently transferring high-quality reasoning patterns into compact latent representations. 

14 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

Table 6: **Comparison with efficient textual reasoning methods.** 

||**Method**|**EgoPlan-**<br>**Bench2**|**RoboVQA**<br>**OpenEQA**|**Average**|
|---|---|---|---|---|
||Textual Teacher_ℱ_<sup>_𝑇_</sup><br>_𝜃_<br>_ℱ_<sup>_𝑇_</sup><br>_𝜃_<sup>Inference w/o thinking</sup><br>_ℱ_<sup>_𝑇_</sup><br>_𝜃_<sup>Inference w/ 6 textual tokens</sup><br>_ℱ_<sup>_𝑇_</sup><br>_𝜃_<sup>w/ RL Length-Penalty Arora and Zanette (2025)</sup>|41.7<br>42.7<br>39.3<br>41.2|58.2<br>49.4<br>55.0<br>41.7<br>53.0<br>46.5<br>57.5<br>44.7|49.8<br>46.5<br>46.3<br>47.8|
||Fast-ThinkAct-3B|**46.4**|**60.8**<br>**52.8**|**53.3**|
|Observ|ation<br>Visualized Trace<br>Instruction||Execution Result||
|(a)|"Lift the medium mug<br>for hot drinks from<br>the table, spin it, set<br>it down, and hang it<br>on the dark gray rack<br>with flat back."||||
|(b)|"Grab the handheld<br>microphone from<br>the table and pass<br>it over."||||


Figure 8: **Visualization of predicted visual trajectories and action execution results on RoboTwin2.0.** Yellow traces indicate left gripper trajectories; red traces indicate right gripper trajectories for bimanual tasks. 

### **A.4. Evaluation Setup** 

#### **A.4.1. Embodied Reasoning Benchmarks** 

We evaluate on three benchmarks assessing different aspects of embodied reasoning. EgoPlan-Bench2 Chen et al. (2023) tests egocentric task planning across 24 daily-life scenarios with 1,321 multiple-choice questions, measuring accuracy in predicting next steps given task goals and progress history. RoboVQA Sermanet et al. (2024) evaluates visual reasoning in manipulation contexts through 1,893 free-form QA pairs from robot and human demonstrations, assessed via BLEU score. OpenEQA Majumdar et al. (2024) assesses spatial and functional understanding through 1,600+ questions spanning 180+ real-world environments, evaluated using LLM-based scoring aligned with human preferences. These benchmarks comprehensively evaluate embodied reasoning capability across planning, manipulation, and spatial understanding. 

#### **A.4.2. Robotic Manipulation Benchmarks** 

We evaluate on three simulation benchmarks covering diverse manipulation scenarios. SimplerEnv Li et al. (2024) provides manipulation tasks with strong sim-to-real correlation, featuring diverse visual variations in lighting, textures, backgrounds, and camera poses. Following MolmoAct Lee et al. (2025), we evaluate on the Google Robot tasks using the standard protocol Kim et al. (2024); Lee et al. (2025) of directly evaluating on SimplerEnv after training on OXE. LIBERO Liu et al. (2023) targets different generalization challenges through four task suites: spatial layout variation (LIBERO-Spatial), object diversity (LIBERO-Object), goal variation (LIBERO-Goal), and long-horizon planning with mixed variations (LIBERO-Long). We evaluate each suite over 500 trials using 3 random seeds following prior works Kim et al. (2024); Lee et al. (2025). RoboTwin2.0 Chen et al. (2025) features challenging bimanual manipulation with easy and hard difficulty settings, where the hard setting introduces domain randomization including clutter, lighting variations, diverse textures, and height changes. Following the original protocol, we train on 50 clean expert demonstrations per task and evaluate with 100 rollouts under both settings. We assess 10 tasks categorized into short, medium, and long horizons based on demonstration lengths. 

15 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 


Figure 9: **Failure identification and analysis capabilities on RoboFAC Lu et al. (2025).** Top row shows identification of failure types and execution stages. Bottom row demonstrates failure root cause analysis. 

## **B. Additional Experiment Results** 

### **B.1. Additional Quantitative Results** 

#### **Results of Larger Model Size.** 

To demonstrate the scalability of our approach, we apply Fast-ThinkAct to a larger backbone, Qwen2.5-VL-7B, and evaluate its performance on embodied reasoning benchmarks. As shown in Tab. 4, Fast-ThinkAct consistently achieves strong performance across EgoPlan-Bench2 Qiu et al. (2024), RoboVQA Sermanet et al. (2024), and OpenEQA Majumdar et al. (2024), validating that our latent reasoning distillation method effectively scales to larger model backbones. 

#### **Performance Comparison with ThinkAct-3B.** 

Tab. 5 presents detailed numerical results corresponding to Fig. 3 with additional ThinkAct-3B results. At the same 3B model size, Fast-ThinkAct achieves notable performance gains (89.7 vs. 83.1 on LIBERO, 68.7 vs. 64.7 on SimplerEnv-Google) while dramatically improving efficiency with **7** _×_ faster inference (805ms vs. 5674ms). 

#### **Comparison with Efficient Reasoning Baselines.** 

Table 6 compares our method with efficient textual reasoning alternatives applied to the textual teacher _ℱ𝜃_<sup>_𝑇_.</sup> We evaluate three baselines: removing reasoning during inference entirely (0 tokens), constraining the teacher to generate only 6 textual tokens during inference, and applying RL training with a length penalty Arora and Zanette (2025) to encourage concise reasoning ( _∼_ 50 tokens). These achieve 46.5, 46.3, and 47.8 respectively, all degrading from the teacher’s 49.8. In contrast, Fast-ThinkAct uses only 6 latent tokens and achieves **53.3** , demonstrating superior efficiency and performance. 

16 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 


**Question:** Is this room on the ground floor of the building? **GT:** no Let's carefully analyze the image to determine if this room is on the ground floor of the building. First, I notice that there is a window with a view of greenery outside. This suggests we are at a level that allows natural light to filter in, which is typical for ground floor windows. Next, I see a white desk and a chair, which seem like standard office furniture for a ground floor workspace. The desk appears to be at a height that would be comfortable for someone to sit and work, which is also consistent with a ground floor layout. Additionally, there's a white bookshelf that looks like it could be used for storage and decoration, which is a common feature in office spaces on the ground floor. However, there is a cabinet in the background that seems a bit unusual for a ground floor room. It could be a storage cabinet for a specific purpose, but it might not be typical for a ground floor space. Let's also consider the lighting. The natural light coming through the window seems to be coming from the side, which is more likely if we are on the ground floor and looking towards a window that is part of the building's exterior. After considering all these factors, I think the room is likely on the ground floor, but it's not impossible for it to be on an upper floor with a unique window design or a specialized storage cabinet. Final thought: Given the typical layout of office spaces and the visible elements, it's reasonable to conclude that this room is on the ground floor. 

(a) Textual reasoning (from teacher model) Let's break this down. The image shows a study room scene with a desk, a chair, and some shelves. There's no clear indication that this is on the ground floor. It's obviously indoors, but I should check if anything suggests a different level. Wait, I should also consider if there's any sign of elevation. Hmm, it seems like the view outside the window shows that the room is positioned above the ground. Oh, I see, the perspective through the window suggests it’s not on the ground floor. Let's confirm that. Yes, it checks out. 

- (b) Verbalized reasoning 

Figure 10: **Reasoning trace comparison on OpenEQA.** (a) Teacher’s textual reasoning. (b) Student’s verbalized latent reasoning. Green: reasonable reasoning trace; red: incorrect trace. 

### **B.2. Additional Qualitative Results** 

#### **Qualitative Robot Execution.** 

We provide qualitative robot execution comparisons between the base action model RDT Liu et al. (2024) and Fast-ThinkAct in the supplementary video `Fast-ThinkAct.mp4` . Our method shows substantial improvements on challenging robotic execution tasks, where reasoning capabilities provide better spatial understanding and coordination for successful manipulation. 

#### **Bimanual Manipulation Results.** 

In Fig. 8, we present visualized trajectories and execution results for `hanging mug` and `handover mic` tasks under easy and hard settings in RoboTwin2.0 Chen et al. (2025). The hard setting includes different backgrounds and distractor objects. These examples show successful bimanual coordination where predicted waypoints accurately guide both grippers through the manipulation sequence, demonstrating Fast-ThinkAct’s spatial reasoning ability across varied visual conditions. 

17 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

#### Table 7: **Additional ablation study of training objectives and learning stages on robot manipulation benchmarks.** 

|**Method**|**LIBERO**|**SimplerEnv**<br>**Google**|**RoboTwin2.0**|**Average**|
|---|---|---|---|---|
|**Fast-ThinkAct**|**89.7**|**68.7**|**46.1**|**68.2**|
|w/o_ℒ_verb|88.6|67.3|44.9|66.9|
|w/o_ℒ_verb_, ℒ_distill|86.3|65.7|42.6|64.9|
|Textual Teacher|88.5|67.3|45.8|67.2|
|SFT + CoT-SFT|87.2|65.8|43.3|65.4|
|SFT only|86.9|64.5|42.8|64.7|


Table 8: **Ablation of Latent Reasoning Steps** _𝑀_ **.** 

#### **Failure Identification and Recovery.** 

In Fig. 9, we demonstrate Fast-ThinkAct’s failure identification and analysis capabilities, complementing the recovery planning shown in the main paper. The top row shows that Fast-ThinkAct identifies failure types (e.g., position deviation) and execution stages (e.g., reaching for the cube). The bottom row illustrates root cause analysis, for instance, in the bottom-right example, the model correctly infers that the failure to push the cube with an L-shaped tool stems from an improper initial grasp. These results demonstrate Fast-ThinkAct’s comprehensive understanding of manipulation failures beyond recovery planning. 

#### **Verbalized Latent Reasoning.** 

Fig. 10 visualizes teacher textual reasoning and student verbalized reasoning. While the student generates compact and correct (green) reasoning, the teacher’s lengthy output sometimes contains erroneous steps (red) that might degrade the performance. 

### **B.3. Additional Ablation Study and Analysis** 

#### **Additional Ablation Results on Manipulation Benchmarks.** 

Table 7 shows ablation results on LIBERO Liu et al. (2023), SimplerEnv-Google Li et al. (2024), and RoboTwin2.0 Chen et al. (2025). Removing _ℒ_ verb or _ℒ_ distill progressively degrades performance, confirming their contributions. Our full model consistently outperforms the textual teacher and models without teacher-student training (CoT-SFT, SFT only), demonstrating the benefits of compact latent reasoning distillation. 

#### **Ablation Study on Action Model Conditioning.** 

In Sec. 3.3, we extract visual latent planning _𝑐𝑡_ from early-layer KV cache of spatial tokens to condition the action model. We compare this against using late-layer KV cache (last _𝑁_ layers, where _𝑁_ is the action model depth) and directly using spatial tokens’ output hidden states. Our approach achieves **89.7** on LIBERO, outperforming late-layer KV at 88.3 and output hidden states at 87.1, demonstrating that early-layer representations better capture visual planning information for action prediction. Therefore, we adopt early-layer KV conditioning as our default configuration. 

#### **Ablation Study on Latent Reasoning Steps.** 

In Fig. 8, we study the effect of latent reasoning steps _𝑀_ . We observe that too few steps ( _𝑀_ = 1) limit reasoning capacity, while excessive steps ( _𝑀_ = 30 _,_ 100) might introduce redundant or noisy information. Therefore, we adopt _𝑀_ = 6, which achieves optimal performance, as our default. 

18 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

## **References** 

- [1] Abbas Abdolmaleki, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Ashwin Balakrishna, Nathan Batchelor, Alex Bewley, Jeff Bingham, Michael Bloesch, et al. Gemini robotics 1.5: Pushing the frontier of generalist robots with advanced embodied reasoning, thinking, and motion transfer. _arXiv preprint arXiv:2510.03342_ , 2025. 3, 10 

- [2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 8 

- [3] Pranjal Aggarwal and Sean Welleck. L1: Controlling how long a reasoning model thinks with reinforcement learning. _arXiv preprint arXiv:2503.04697_ , 2025. 3 

- [4] Daman Arora and Andrea Zanette. Training language models to reason efficiently. _arXiv preprint arXiv:2502.04463_ , 2025. 15, 16 

- [5] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 1, 7, 8, 14 

- [6] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 3 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _𝜋_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 3, 8, 10 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 3 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 1, 3 

- [10] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 3 

- [11] Guo Chen, Zhiqi Li, Shihao Wang, Jindong Jiang, Yicheng Liu, Lidong Lu, De-An Huang, Wonmin Byeon, Matthieu Le, Tuomas Rintamaki, et al. Eagle 2.5: Boosting long-context post-training for frontier vision-language models. _arXiv preprint arXiv:2504.15271_ , 2025. 1 

- [12] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 6, 7, 8, 9, 10, 13, 15, 17, 18 

- [13] William Chen, Suneel Belkhale, Suvir Mirchandani, Oier Mees, Danny Driess, Karl Pertsch, and Sergey Levine. Training strategies for efficient embodied reasoning. _arXiv preprint arXiv:2505.08243_ , 2025. 2, 3 

- [14] Yi Chen, Yuying Ge, Yixiao Ge, Mingyu Ding, Bohao Li, Rui Wang, Ruifeng Xu, Ying Shan, and Xihui Liu. Egoplan-bench: Benchmarking multimodal large language models for human-level planning. _arXiv preprint arXiv:2312.06722_ , 2023. 7, 13, 14, 15 

19 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

- [15] Zhe Chen, Weiyun Wang, Yue Cao, Yangzhou Liu, Zhangwei Gao, Erfei Cui, Jinguo Zhu, Shenglong Ye, Hao Tian, Zhaoyang Liu, et al. Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling. _arXiv preprint arXiv:2412.05271_ , 2024. 8, 14 

- [16] Jeffrey Cheng and Benjamin Van Durme. Compressed chain of thought: Efficient reasoning through dense representations. _arXiv preprint arXiv:2412.13171_ , 2024. 3 

- [17] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 7, 8, 13 

- [18] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 1, 8 

- [19] Muzhi Dai, Shixuan Liu, and Qingyi Si. Stable reinforcement learning for efficient reasoning. _arXiv preprint arXiv:2505.18086_ , 2025. 3 

- [20] Matt Deitke, Christopher Clark, Sangho Lee, Rohun Tripathi, Yue Yang, Jae Sung Park, Mohammadreza Salehi, Niklas Muennighoff, Kyle Lo, Luca Soldaini, et al. Molmo and pixmo: Open weights and open data for state-of-the-art multimodal models. _arXiv e-prints_ , pages arXiv–2409, 2024. 7, 13, 14 

- [21] Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, et al. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. _arXiv preprint arXiv:2505.23705_ , 2025. 3 

- [22] Kaituo Feng, Kaixiong Gong, Bohao Li, Zonghao Guo, Yibing Wang, Tianshuo Peng, Junfei Wu, Xiaoying Zhang, Benyou Wang, and Xiangyu Yue. Video-r1: Reinforcing video reasoning in mllms. _arXiv preprint arXiv:2503.21776_ , 2025. 7, 13, 14 

- [23] Weifan Guan, Qinghao Hu, Aosheng Li, and Jian Cheng. Efficient vision-language-action models for embodied manipulation: A systematic survey. _arXiv preprint arXiv:2510.17111_ , 2025. 2 

- [24] Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, and Yuandong Tian. Training large language models to reason in a continuous latent space. _arXiv preprint arXiv:2412.06769_ , 2024. 3 

- [25] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, Yu-Chiang Frank Wang, and Fu-En Yang. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 1, 2, 3, 5, 6, 7, 8, 10, 12, 14 

- [26] Yuheng Ji, Huajie Tan, Jiayu Shi, Xiaoshuai Hao, Yuan Zhang, Hengyuan Zhang, Pengwei Wang, Mengdi Zhao, Yao Mu, Pengju An, et al. Robobrain: A unified brain model for robotic manipulation from abstract to concrete. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1724–1734, 2025. 7, 13, 14 

- [27] Nikita Karaev, Yuri Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker3: Simpler and better point tracking by pseudo-labelling real videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6013–6022, 2025. 13 

- [28] Dongyoung Kim, Sumin Park, Huiwon Jang, Jinwoo Shin, Jaehyung Kim, and Younggyo Seo. Robot-r1: Reinforcement learning for enhanced embodied reasoning in robotics. _arXiv preprint arXiv:2506.00070_ , 2025. 2, 3 

20 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

- [29] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 3, 7, 13, 14, 15 

- [30] Byung-Kwan Lee, Ryo Hachiuma, Yong Man Ro, Yu-Chiang Frank Wang, and Yueh-Hua Wu. Unified reinforcement and imitation learning for vision-language models. _arXiv preprint arXiv:2510.19307_ , 2025. 3 

- [31] Byung-Kwan Lee, Ryo Hachiuma, Yu-Chiang Frank Wang, Yong Man Ro, and Yueh-Hua Wu. Vlsi: Verbalized layers-to-interactions from large to small vision language models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 29545–29557, 2025. 3 

- [32] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. 2, 3, 7, 8, 12, 13, 14, 15 

- [33] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 6, 7, 9, 13, 15, 18 

- [34] Yi Li, Yuquan Deng, Jesse Zhang, Joel Jang, Marius Memmel, Raymond Yu, Caelan Reed Garrett, Fabio Ramos, Dieter Fox, Anqi Li, et al. Hamster: Hierarchical action models for open-world robot manipulation. _arXiv preprint arXiv:2502.05485_ , 2025. 1, 3 

- [35] Zhiqi Li, Guo Chen, Shilong Liu, Shihao Wang, Vibashan VS, Yishen Ji, Shiyi Lan, Hao Zhang, Yilin Zhao, Subhashree Radhakrishnan, et al. Eagle 2: Building post-training data strategies from scratch for frontier vision-language models. _arXiv preprint arXiv:2501.14818_ , 2025. 1 

- [36] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 6, 7, 9, 13, 15, 18 

- [37] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 1 

- [38] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 6, 7, 8, 10, 13, 17 

- [39] Zhijian Liu, Ligeng Zhu, Baifeng Shi, Zhuoyang Zhang, Yuming Lou, Shang Yang, Haocheng Xi, Shiyi Cao, Yuxian Gu, Dacheng Li, et al. Nvila: Efficient frontier visual language models. _arXiv preprint arXiv:2412.04468_ , 2024. 1, 8, 14 

- [40] Weifeng Lu, Minghao Ye, Zewei Ye, Ruihan Tao, Shuo Yang, and Bo Zhao. Robofac: A comprehensive framework for robotic failure analysis and correction. _arXiv preprint arXiv:2505.12224_ , 2025. 7, 9, 10, 13, 14, 16 

- [41] Arjun Majumdar, Anurag Ajay, Xiaohan Zhang, Pranav Putta, Sriram Yenamandra, Mikael Henaff, Sneha Silwal, Paul Mcvay, Oleksandr Maksymets, Sergio Arnaud, et al. Openeqa: Embodied question answering in the era of foundation models. In _CVPR_ , pages 16488–16498, 2024. 7, 8, 15, 16 

21 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

- [42] Yunze Man, De-An Huang, Guilin Liu, Shiwei Sheng, Shilong Liu, Liang-Yan Gui, Jan Kautz, Yu-Xiong Wang, and Zhiding Yu. Argus: Vision-centric reasoning with grounded chain-of-thought. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 14268–14280, 2025. 3 

- [43] Tomohiro Motoda, Masaki Murooka, Ryoichi Nakajo, Muhammad A. Muttaqien, Koshi Makihara, Hanbit Oh, Keisuke Shirai, Floris Erich, Ryo Hanai, and Yukiyasu Domae. Aist-bimanual manipulation, 2025. 7, 13, 14 

- [44] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 1, 7, 13 

- [45] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. Bleu: a method for automatic evaluation of machine translation. In _Proceedings of the 40th annual meeting of the Association for Computational Linguistics_ , pages 311–318, 2002. 7 

- [46] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 3 

- [47] Lu Qiu, Yi Chen, Yuying Ge, Yixiao Ge, Ying Shan, and Xihui Liu. Egoplan-bench2: A benchmark for multimodal large language model planning in real-world scenarios. _arXiv preprint arXiv:2412.04447_ , 2024. 7, 8, 16 

- [48] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, et al. Eo-1: Interleaved vision-text-action pretraining for general robot control. _arXiv preprint arXiv:2508.21112_ , 2025. 2, 3 

- [49] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances in neural information processing systems_ , 36:53728–53741, 2023. 5 

- [50] Gabriel Sarch, Snigdha Saha, Naitik Khandelwal, Ayush Jain, Michael J Tarr, Aviral Kumar, and Katerina Fragkiadaki. Grounded reinforcement learning for visual reasoning. _arXiv preprint arXiv:2505.23678_ , 2025. 3 

- [51] Pierre Sermanet, Tianli Ding, Jeffrey Zhao, Fei Xia, Debidatta Dwibedi, Keerthana Gopalakrishnan, Christine Chan, Gabriel Dulac-Arnold, Sharath Maddineni, Nikhil J Joshi, et al. Robovqa: Multimodal long-horizon reasoning for robotics. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 645–652. IEEE, 2024. 7, 8, 13, 14, 15, 16 

- [52] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 2, 4, 7 

- [53] Zhenyi Shen, Hanqi Yan, Linhai Zhang, Zhanghao Hu, Yali Du, and Yulan He. Codi: Compressing chain-of-thought into continuous space via self-distillation. _arXiv preprint arXiv:2502.21074_ , 2025. 3 

- [54] Lucy Xiaoyang Shi, Archit Sharma, Tony Z Zhao, and Chelsea Finn. Waypoint-based imitation learning for robotic manipulation. _arXiv preprint arXiv:2307.14326_ , 2023. 7, 13 

- [55] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, et al. Hi robot: Open-ended instruction following with hierarchical vision-language-action models. _arXiv preprint arXiv:2502.19417_ , 2025. 3 

22 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

- [56] Min Shi, Fuxiao Liu, Shihao Wang, Shijia Liao, Subhashree Radhakrishnan, Yilin Zhao, De-An Huang, Hongxu Yin, Karan Sapra, Yaser Yacoob, et al. Eagle: Exploring the design space for multimodal llms with mixture of encoders. _arXiv preprint arXiv:2408.15998_ , 2024. 1 

- [57] BAAI RoboBrain Team, Mingyu Cao, Huajie Tan, Yuheng Ji, Xiansheng Chen, Minglan Lin, Zhiyu Li, Zhou Cao, Pengwei Wang, Enshen Zhou, et al. Robobrain 2.0 technical report. _arXiv preprint arXiv:2507.02029_ , 2025. 8, 14 

- [58] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 3 

- [59] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 1, 3 

- [60] Weiyun Wang, Zhangwei Gao, Lixin Gu, Hengjun Pu, Long Cui, Xingguang Wei, Zhaoyang Liu, Linglin Jing, Shenglong Ye, Jie Shao, et al. Internvl3. 5: Advancing open-source multimodal models in versatility, reasoning, and efficiency. _arXiv preprint arXiv:2508.18265_ , 2025. 1 

- [61] Yan Wang, Wenjie Luo, Junjie Bai, Yulong Cao, Tong Che, Ke Chen, Yuxiao Chen, Jenna Diamond, Yifan Ding, Wenhao Ding, et al. Alpamayo-r1: Bridging reasoning and action prediction for generalizable autonomous driving in the long tail. _arXiv preprint arXiv:2511.00088_ , 2025. 2 

- [62] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _arXiv preprint arXiv:2509.09372_ , 2025. 3 

- [63] Yilin Wu, Anqi Li, Tucker Hermans, Fabio Ramos, Andrea Bajcsy, and Claudia P’erez-D’Arpino. Do what you say: Steering vision-language-action models via runtime reasoning-action alignment verification. _arXiv preprint arXiv:2510.16281_ , 2025. 2, 3 

- [64] Violet Xiang, Chase Blagden, Rafael Rafailov, Nathan Lile, Sang Truong, Chelsea Finn, and Nick Haber. Just enough thinking: Efficient reasoning with adaptive length penalties reinforcement learning. _arXiv preprint arXiv:2506.05256_ , 2025. 3 

- [65] Jinheng Xie, Weijia Mao, Zechen Bai, David Junhao Zhang, Weihao Wang, Kevin Qinghong Lin, Yuchao Gu, Zhijie Chen, Zhenheng Yang, and Mike Zheng Shou. Show-o: One single transformer to unify multimodal understanding and generation. _arXiv preprint arXiv:2408.12528_ , 2024. 1 

- [66] Yige Xu, Xu Guo, Zhiwei Zeng, and Chunyan Miao. Softcot: Soft chain-of-thought for efficient reasoning with llms. _arXiv preprint arXiv:2502.12134_ , 2025. 3 

- [67] Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, et al. Magma: A foundation model for multimodal ai agents. _arXiv preprint arXiv:2502.13130_ , 2025. 1, 3, 8, 14 

- [68] Zhaoshu Yu, Bo Wang, Pengpeng Zeng, Haonan Zhang, Ji Zhang, Lianli Gao, Jingkuan Song, Nicu Sebe, and Heng Tao Shen. A survey on efficient vision-language-action models. _arXiv preprint arXiv:2510.24795_ , 2025. 2 

- [69] Danlong Yuan, Tian Xie, Shaohan Huang, Zhuocheng Gong, Huishuai Zhang, Chong Luo, Furu Wei, and Dongyan Zhao. Efficient rl training for reasoning models via length-aware optimization. _arXiv preprint arXiv:2505.12284_ , 2025. 3 

23 

Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning 

- [70] Yifu Yuan, Haiqin Cui, Yaoting Huang, Yibin Chen, Fei Ni, Zibin Dong, Pengyi Li, Yan Zheng, and Jianye Hao. Embodied-r1: Reinforced embodied reasoning for general robotic manipulation. _arXiv preprint arXiv:2508.13998_ , 2025. 3 

- [71] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 2, 3 

- [72] Zhen Zhang, Xuehai He, Weixiang Yan, Ao Shen, Chenyang Zhao, Shuohang Wang, Yelong Shen, and Xin Eric Wang. Soft thinking: Unlocking the reasoning potential of llms in continuous concept space. _arXiv preprint arXiv:2505.15778_ , 2025. 3 

- [73] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 2, 3, 7, 14 

- [74] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 7, 8, 13 

- [75] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 3 

- [76] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 8, 14 

24 

