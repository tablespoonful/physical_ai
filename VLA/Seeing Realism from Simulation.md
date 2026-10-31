---
title: "Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation"
date: "2026-05-04"
authors: "Chenyu Hui; Xiaodi Huang; Siyu Xu; Yunke Wang; Shan You; Fei Wang"
venue: "ICML 2026"
url: https://arxiv.org/abs/2605.02757
pdf: https://arxiv.org/pdf/2605.02757
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.02757)** / [論文ページ](https://arxiv.org/abs/2605.02757)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

**Chenyu Hui**<sup>1 2 *</sup> **Xiaodi Huang**<sup>1 3 *</sup> **Siyu Xu**<sup>4</sup> **Yunke Wang**<sup>4</sup> **Shan You**<sup>5</sup> **Fei Wang**<sup>6</sup> **Tao Huang**<sup>1</sup><sup>_†_</sup> **Chang Xu**<sup>4</sup> 

# **Abstract** 

Vision-language-action (VLA) models typically rely on large-scale real-world videos, whereas simulated data, despite being inexpensive and highly parallelizable to collect, often suffers from a substantial visual domain gap and limited environmental diversity, resulting in weak real-world generalization. We present an efficient video augmentation framework that converts simulated VLA videos into realistic training videos while preserving task semantics and action trajectories. Our pipeline extracts structured conditions from simulation via video semantic segmentation and video captioning, rewrites captions to diversify environments, and uses a conditional video transfer model to synthesize realistic videos. To make augmentation practical at scale, we introduce a diffusion feature-reuse mechanism that reuses video tokens across adjacent timesteps to accelerate generation, and a coreset sampling strategy that identifies a compact, non-redundant subset for augmentation under limited computation. Extensive experiments on Robotwin 2.0, LIBERO, LIBERO-Plus, and a real robotic platform demonstrate consistent improvements. For example, our method improves RDT-1B by 8% on Robotwin 2.0, and boosts _π_ 0 by 5.1% on the more challenging LIBERO-Plus benchmark. Code is available at: CODE. 

# **1. Introduction** 

The advent of large-scale Vision-Language-Action (VLA) models has marked a significant milestone in robotics (Liu 

> _∗_ Equal contribution. Work was done during internship at SJTU.<sup>1</sup> Shanghai Jiao Tong University<sup>2</sup> Xi’an Jiaotong University<sup>3</sup> Institute of Automation, Chinese Academy of Sciences<sup>4</sup> The University of Sydney<sup>5</sup> SenseTime Research<sup>6</sup> University of Science and Technology of China. Correspondence to: Tao Huang _<_ t.huang@sjtu.edu.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

et al., 2024; Black et al., 2024; Intelligence et al., 2025b;a; Liu et al., 2024; Zhao et al., 2023; Xu et al., 2025a), enabling robots to interpret natural language instructions and execute complex manipulation tasks. These models typically rely on extensive datasets of real-world robotic trajectories to learn generalizable policies. However, collecting such real-world data is inherently costly, time-consuming, and difficult to scale, posing a major bottleneck to broader development and deployment. In contrast, simulated data offers a highly inexpensive alternative. But as noted in recent studies, models that achieve near-perfect performance within a specific simulation benchmark often fail catastrophically when faced with minor perturbations in object layout, lighting, camera viewpoint, or instruction phrasing in scenarios with disturbances (Fei et al., 2025; Zhou et al., 2025b; Xu et al., 2025b; Pei et al., 2025), revealing that many models merely memorize training sequences rather than learning robust, semantic task understanding. 

We address the critical lack of visual and environmental diversity in robotic training data by proposing an efficient, scalable video augmentation framework. Our approach transforms source video sequences into visually diverse training videos while strictly preserving underlying task semantics and action trajectories. The pipeline first extracts structured conditions from simulation, diversifies the environmental context, and then synthesizes high-fidelity videos using a conditional video diffusion model. To mitigate the substantial computational cost of video transfer, we propose accelerating the diffusion generation by caching velocity during the denoising process. We design adaptive strategies that optimize the trade-off between quality and efficiency. Consequently, this velocity-caching mechanism achieves an over 60% reduction in generation time while maintaining high model accuracy. 

Furthermore, a coreset sampling method is designed to achieve efficient scalability by only augmenting a subset of the large-scale dataset. For the sake of sampling diverse trajectories that maximize the performance, we build a graph structure that balances the difficulty and diversity among data nodes, where the difficulty and diversity are estimated by a video embedding model and a pretrained VLA policy. By prioritizing samples that are both challenging and highly 

1 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 


_Figure 1._ Overall framework of the proposed method. Given a large-scale simulation training set, we introduce a coreset sampling algorithm to select important and diverse samples, which are then augmented to realistic video strips and used for training. 

diverse, we ensure the significance of the augmentation effect in large-scale datasets. 

We conduct extensive experiments across multiple benchmarks, including Robotwin 2.0 (Chen et al., 2025), LIBERO (Liu et al., 2023), and the more challenging LIBERO-Plus (Fei et al., 2025) to demonstrate the effectiveness of our framework. We also conduct real-world robotic experiments. 

In summary, our contributions are threefold: 

- We present an end-to-end video transfer named efficient transfer framework that effectively bridges the sim-to-real gap for VLA data augmentation. 

- We design a segmented (three-stage) velocity caching strategy, which better matches the dynamics of conditional video generation. It is proven that adopting this strategy can save over 60% transferring time. 

- We propose a trajectory-level coreset formulation that combines policy difficulty (measured by the policy loss of RDT-1B), and visual diversity (measured via Cosmos-Embed1 representations), leading to more effective selection of high-value training trajectories. 

# **2. Related Work** 

## **2.1. Vision-Language-Action Models** 

Since the development of VLM and its been pivotal in advancing robotic control by providing rich multi-modal representations. Recent VLA models are finetuned on largescale robotic trajectory data in an end-to-end mode to ob- 

tain more generalizable policies (Brohan et al., 2022; Ebert et al., 2021). Widely used OpenVLA (Kim et al., 2024) is based on prismatic (Karamcheti et al., 2024). RDT combines the advantage of diffusion model and transformer (Liu et al., 2024). ACT (Zhao et al., 2023) introduced chunking for actions based on transformer. The OpenPi series like _π_ 0 (Black et al., 2024), _π_ 0 _._ 5 (Intelligence et al., 2025b) and the newest _π_ 0 _._ 6 (Intelligence et al., 2025a) gains significant performance superiority by enhancing existing VLMs with a dual-system VLA architecture, retaining the text-generation ability of the VLM, and combining with reinforcement learning (Li et al., 2026b), respectively. 

## **2.2. Video Generation** 

Recent advances in diffusion-based video generation and style transfer have established this as a pivotal area in multimodal modeling, building upon foundational works like Stable Diffusion (Rombach et al., 2022), Stable Video Diffusion (Blattmann et al., 2023). Contemporary research has expanded these frontiers: Sora incorporates a temporal VAE and Transformer backbone; Wan (Wan et al., 2025) and VACE (Jiang et al., 2025) employ mixture-of-experts architectures; while NVIDIA’s Cosmos series (Alhaija et al., 2025), particularly Cosmos Transfer (Ali et al., 2025), provides a robust foundation for world model-based video transfer. Concurrently, generative techniques are increasingly applied to embodied data, with methods like Rebot (Fang et al., 2025b), EgoDemoGen (Xu et al., 2025c), EMMA (Dong et al., 2025), Embodied Dreamer (Wang et al., 2025), Gigaworld-0 (Team et al., 2025b), RoboTransfer (Liu et al., 2025b) and Gigabrain-0 (Team et al., 2025a) demonstrating effective real-to-sim and sim-to-real data generation. 

2 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

## **2.3. Data Centric AI and Efficient Training** 

Data-centric approaches have proven crucial for enhancing model performance and training efficiency, evolving from early heuristic-based filtering methods like CCNet (Wenzek et al., 2020) and C4 (Raffel et al., 2020) to sophisticated techniques emphasizing deduplication (Lee et al., 2022) and semantic redundancy elimination (Abbas et al., 2023). Beyond quality filtering, data diversity plays an equally vital role in robustness, as demonstrated by The Pile’s emphasis on heterogeneous data (Gao et al., 2020) and Falcon Series’ success with web-scale curation (Penedo et al., 2023). Domain-specific selection methods like DSIR (Xie et al., 2023) leverage importance resampling for target distribution alignment, while theoretical advances (Sorscher et al., 2022) show intelligent pruning can achieve exponential efficiency gains. This paradigm culminates in D<sup>2</sup> Pruning (Maharana et al., 2023), which advocates balanced coreset selection based on complementary diversity-difficulty criteria. 

# **3. Method** 

We propose a VLA data augmentation framework to improve sim-to-real generalization. We first analyze the generalization failures of simulation-trained models, then introduce an end-to-end pipeline that generates realistic videos from semantic and structural cues. To scale augmentation efficiently, we develop a diffusion acceleration method based on velocity caching and a coreset sampling strategy for selective data generation. 

## **3.1. Motivation: The Brittleness of VLA Models** 

VLA models trained on robotic manipulation data often achieve high in-distribution performance but fail under distribution shifts. The core issue is **limited visual and environmental diversity** in training data: simulated environments are overly clean and static, while real-world datasets cover only narrow conditions due to collection constraints. This lets models **overfit to spurious regularities** rather than learning robust instruction-to-action mappings. 

Recent benchmarks quantify this brittleness: LIBEROPlus (Fei et al., 2025) shows success rates dropping from 95% to under 30% with minor perturbations in object layout, camera angle, or lighting; LIBERO-PRO (Zhou et al., 2025b) reports near-zero accuracy when object positions and instructions are modified. As illustrated in Figure 2, baseline VLA models fail under such perturbations, revealing memorization of fixed action sequences rather than semantic task understanding. 

The root cause lies in sterile training data that lacks the complexity of real-world contexts. Without diverse backgrounds, lighting, viewpoints, and object configurations, models latch onto superficial correlations (Xu et al., 2025b; 


Original VLA Augmented VLA 

_Figure 2._ Examples from LIBERO-Plus evaluation. The baseline VLA model fails under environment perturbations such as texture change (upper) and lighting change (lower), while the model trained with our augmented data performs the tasks correctly, showing stronger generalization. 

Fang et al., 2025a) and under-utilize language inputs (Fei et al., 2025; Zhou et al., 2025b; Li et al., 2026a). This motivates our approach: augmenting training distributions with visually varied yet semantically faithful data to enable robust generalization. 

## **3.2. Diversifying Data via Conditional Video Transfer** 

We present a video augmentation framework that transforms source robotic videos into visually diverse counterparts while preserving task semantics and action fidelity. As illustrated in Figure 1, our pipeline consists of four stages: caption generation, caption rewriting, structured condition extraction, and conditional video synthesis. 

**Semantic and Structural Condition Extraction.** We first extract descriptive captions from source videos using a temporal video captioning model ( _i.e._ , VideoChat2 (Li et al., 2025)), which summarizes interactions, objects, and spatial relations. These captions are then rewritten by a large language model ( _i.e._ , Qwen3-8B (Yang et al., 2025)) to introduce environmental variations such as background and object color changes, yielding diverse scene contexts while preserving task intent (details in B.2). To maintain geometric consistency, we also extract depth maps from source videos as structural control signals, which provide stable, geometry-preserving guidance compared to alternatives like blur, edge, or segmentation (Ravi et al., 2024). 

**Conditional Video Synthesis.** The final stage employs a conditional video diffusion model ( _i.e._ , Cosmos-Transfer 2.5 (Ali et al., 2025)) to synthesize realistic videos conditioned on the rewritten caption and depth input. The model iteratively denoises video tokens, generating temporally coherent scenes that retain the original action trajectory while varying the visual context. This process enriches the training distribution with diverse visual conditions without requiring additional real-world data collection. 

3 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 


_Figure 3._ Euclidean distance between adjacent velocity predictions. A stable phase with minimal changes enables caching and reuse. 

## **3.3. Efficient Video Generation via Velocity Caching** 

Recent conditional video diffusion models such as CosmosTransfer (Ali et al., 2025) and Wan (Wan et al., 2025) achieve strong visual fidelity but suffer from prohibitively high inference costs<sup>1</sup> , posing a major obstacle to large-scale data augmentation. We propose a velocity caching mechanism that exploits temporal redundancy in the diffusion process to significantly accelerate generation while preserving quality. 

**Observation: Redundancy in Denoising.** In flow-based diffusion models (Lipman et al., 2022), each denoising step computes a velocity field _vθ_ ( _xt, t_ ) to update the latent: 


This velocity prediction accounts for over 70% of per-step runtime due to the full forward pass through a large video diffusion transformer. Inspired by recent caching strategies (Liu et al., 2025a; Zhou et al., 2025a; Li et al., 2023), we analyze the temporal dynamics of velocity predictions during denoising. 

As shown in Figure 3, measuring the Euclidean distance _∥vt_ +1 _− vt∥_ across timesteps reveals three distinct phases: (1) an _initial phase_ with rapidly changing predictions, (2) a _stable phase_ with minimal variation, and (3) a _final adjustment phase_ for fine-grained refinement. This suggests that we can avoid re-computing _vθ_ at every step during the stable phase by reusing previously cached values. 

**Three-Stage Caching Strategy.** Based on this observation, we divide the _N_ -step denoising into three stages: (1) **Initial Phase** ( _t < ts_ ): velocity predictions are computed at each step due to high variability; (2) **Stable Phase** ( _ts ≤ t < tf_ ): velocities are computed every _α_ steps and cached values are reused in between; (3) **Adjustment Phase** ( _t ≥ tf_ ): full computation resumes for final refinement. We detect the 

> 1Cosmos-Transfer 1 takes _∼_ 40 minutes for a 5-second 720p video on one A100 GPU. 


_Figure 4._ The proposed VLA coreset sampling algorithm. 

stable phase onset using a relative smoothness threshold: 


With _k_ = 0 _._ 4, _α_ = 8, and _m_ = 3 adjustment steps, this strategy achieves an average **61.2%** time reduction on RoboTwin 2.0 with negligible quality degradation, enabling efficient scaling of our augmentation pipeline. 

## **3.4. Selective Augmentation via Coreset Sampling** 

Although our video augmentation framework enhances VLA training, applying it to all trajectories in a large-scale dataset is computationally prohibitive. To maximize augmentation utility under limited resources, we propose a coreset sampling strategy that identifies trajectories which are both challenging for policy models and visually diverse, as illustrated in Figure 4. Our method extends D<sup>2</sup> Pruning (Maharana et al., 2023) to embodied video data. 

Given a set of simulated trajectories _S_ = _{s_ 1 _, . . . , sn}_ , our objective is to select a compact subset _S_<sup>_′_</sup> _⊂S_ that maximizes downstream benefit for sim-to-real transfer. 

**Difficulty Estimation via Policy Loss** We quantify trajectory difficulty using a pre-trained VLA policy, such as RDT-1B (Liu et al., 2024). For each trajectory _si_ , we compute the average action prediction loss over a sampled subset of time steps _Ti_ (to reduce computational cost): 


A higher _xi_ indicates that the policy finds the trajectory more challenging, which typically corresponds to edge cases or difficult configurations for manipulation. 

4 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

## **Diversity Estimation via Visual Embedding Topology** 

To capture visual and semantic diversity, we extract trajectory embeddings and define neighbors using a state-of-theart video representation model, Cosmos-Embed1 (NVIDIA et al., 2025), denoted _ϕ_ ( _si_ ) _∈_ R<sup>768</sup> . We build a sparse _k_ -NN graph over these embeddings with nodes _vi_ = _ϕ_ ( _si_ ) and edges weighted by an RBF kernel: 


This graph captures the topological structure of the visual space, enabling both forward and reverse message passing to score and prune redundant samples. 

**Scoring via Forward Message Passing** To prioritize clusters of difficult and non-redundant samples, we compute an updated difficulty score _x_<sup>_′_</sup> _i_<sup>thataggregatesneighborhood</sup> difficulty: 


This promotes samples that are not only hard in isolation but are also surrounded by similarly hard cases, emphasizing policy failure regions in the data. 

**Coreset Construction with Redundancy Suppression** We perform greedy selection using _x_<sup>_′_</sup> _i_<sup>scores and penalize neigh-</sup> bors of selected samples to avoid redundancy: 

1. Select the trajectory with the highest score _s_<sup>_∗_</sup> = arg max _i∈S_ remaining _xi_<sup>_′_, and add</sup><sup>_s∗_to selected coreset</sup><sup>_S′_.</sup> 

2. Suppress scores of visually similar neighbors using reverse message passing: 


This iterative procedure balances sample hardness and coverage, yielding trajectories that are visually diverse and strategically valuable for sim-to-real transfer. By targeting augmentation toward this curated coreset, we achieve computational savings while preserving augmentation benefits. The details of hyperparameters above are as follows: _k_ = 5 _, γr_ = 0 _._ 1 _, γf_ = 0 _._ 1. 

# **4. Experiments** 

In the experiments below, first we prove the effectiveness of our augmentation method on single-task from Robotwin 2.0. Then, we move on to large-scale learning using a coreset sampling policy. To verify the advantages of our method under environment with specific disturbances, we evaluate on LIBERO-Plus. Finally, to study the validity of our method in a real-world experiment, we design tasks and evaluate with an AgileX Piper robot arm under distributed environments, as shown in Figure 5. 


_Figure 5._ Two manipulation tasks (Slot Pen and Stack Tape) under three test conditions: (a) In-Distribution, (b) Position Shift, and (c) Background Shift. 

_Table 1._ Performance (%) comparison of Hard and Easy scenarios of Robotwin 2.0 (Chen et al., 2025) - single-task learning. We train RDT (Liu et al., 2024) with the original simulation data (Ori.) _vs._ augmented data (Aug.). 

|**Task Name**|Ori.|**Hard**<br>Aug.|Ori.|**Easy**<br>Aug.|
|---|---|---|---|---|
|adjust<br>~~b~~ottle|72.0|82.0 (+10.0)|74.0|90.0 (+16.0)|
|beat<br>~~b~~lock<br>~~h~~ammer|36.0|48.0 (+12.0)|76.0|84.0 (+12.0)|
|pick<br>~~d~~ual<br>~~b~~ottles|14.0|20.0 (+6.0)|40.0|36.0 (-4.0)|
|place<br>~~b~~urger<br>~~f~~ries|26.0|38.0 (+12.0)|46.0|54.0 (+8.0)|
|open<br>~~l~~aptop|30.0|44.0 (+14.0)|56.0|56.0|
|move<br>~~c~~an<br>~~p~~ot|12.0|18.0 (+6.0)|26.0|34.0 (+8.0)|
|rotate<br>~~q~~rcode|4.0|8.0 (+4.0)|4.0|10.0 (+6.0)|
|grab<br>~~r~~oller|40.0|50.0 (+10.0)|72.0|74.0 (+2.0)|
|average|29.0|39.0 (+10.0)|49.0|55.0 (+6.0)|


## **4.1. Experimental Results on Robotwin 2.0** 

Following the experimental framework established by Robotwin 2.0 (Chen et al., 2025), this study utilizes the Aloha AgileX dual-arm robot system. For the strategy model selection, we adopted both RDT-1B (Liu et al., 2024) ACT (Zhao et al., 2023) and _π_ 0 (Black et al., 2024) architectures, both fine-tuned based on officially pre-trained weights. 

**<u>(1) Experiments on single-task learning.</u>** We use 50 expert demonstration trajectories in a clean environment to train 10 tasks independently as the original baseline for single-task learning. For our method, we extend augmented first-person perspective video data of all the trajectories, then train the same model for the same steps. We conducted 50 tests on each task under both “Easy” and “Hard” settings. The “Easy” mode corresponds to a _clean_ environment, while the “Hard” mode introduces _domain-randomized_ factors, including clutter, lighting, textures, and height variations. 

**Results.** Table 1 reports the performance of RDT-1B. Compared to the original baseline, our method yields substantial 

5 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

gains, most notably a 10% improvement in “Hard”, which includes domain-randomized factors and better reflects realworld complexity. Even in the clean and easy scenario, we observe a 6% increase, highlighting our method’s ability to enhance generalization and mitigate overfitting. 

Additional results in the Appendix further validate our approach. We report an average increase of 2.0 in _π_ 0 (Table 9) and 3.0 in ACT (Table 8) under the hard setting of Robotwin 2.0 single-task learning, confirming the robustness of our augmentation strategy across different VLA policies. 

**<u>(2) Experiments on multi-task learning</u>** <u>.</u> We expanded the experimental scope to 32 diverse robot operation tasks with 300 trajectories on each task, resulting in a larger amount of 9600 training trajectories. For our method, we adopt a coreset sampling algorithm to select 10% key samples in the full set, resulting in 9600 training samples with 90% original and 10% augmented. When training, both experiments utilize the official pre-trained weights of RDT1B and undergo large-scale multi-task joint training (100k steps). For evaluation metrics, we evaluated nine representative tasks for 50 times in “Hard” scenario. 

_Table 2._ Performance (%) comparison of Hard scenarios of Robotwin 2.0 (Chen et al., 2025) - multi-task learning. We train RDT (Liu et al., 2024) with the original simulation data (Ori.) _vs._ augmented data (Aug.). 

|**Task Name**|**Ori.**|**Aug.**|
|---|---|---|
|adjust<br>~~b~~ottle|20.0|56.0(+36.0)|
|beat<br>~~b~~lock<br>~~h~~ammer|22.0|30.0(+8.0)|
|place<br>~~b~~urger<br>~~f~~ries|22.0|18.0(-4.0)|
|pick<br>~~d~~ual<br>~~b~~ottles|6.0|10.0 (+4.0)|
|place<br>~~o~~bject<br>~~b~~asket|6.0|14.0 (+8.0)|
|move<br>~~c~~an<br>~~p~~ot|8.0|16.0 (+8.0)|
|stack<br>~~b~~owls<br>~~t~~hree|20.0|22.0 (+2.0)|
|click<br>~~a~~larmclock|48.0|52.0 (+4.0)|
|move<br>~~p~~layingcard<br>~~a~~way|16.0|22.0 (+6.0)|
|open<br>~~l~~aptop|60.0|66.0 (+6.0)|
|average|23.0|31.0 (+8.0)|


**Results** . As shown in Table 2, despite having 300 training trajectories per task, the baseline model struggles to generalize in the highly repetitive and visually uniform Robotwin environment. In contrast, augmenting just 10% of the data with our method yields a significant performance boost. This demonstrates that our approach provides valuable visual and semantic diversity that the original dataset lacks, effectively regularizing the model and enhancing generalization, even under strong simulation constraints. 

## **4.2. Experiments on LIEBRO-Plus and LIBERO** 

To validate the effectiveness and generality of our proposed method on widely accepted public benchmarks, we selected 

LIBERO (Liu et al., 2023), and LIBERO-Plus (Fei et al., 2025) to conduct experiments using _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025b). 

We train all the models using the default standard configuration of OpenPi<sup>2</sup> . For the baseline, we finetune the pretrained models with the original dataset. While for our method, we augment a coreset of 50% samples under two data compositions: (1) mixture strategy for mixing the augmented samples and all the original samples together; (2) replacement strategy for replacing the selected coreset with augmented ones. 

_Table 3._ Performance (%) comparison of spatial suite of LIBEROPlus (Fei et al., 2025) using _π_ 0 and _π_ 0 _._ 5. 

|**Perturbation Types**|Ori.|_π_0<br>Aug.|Ori.|_π_0_._5<br>Aug.|
|---|---|---|---|---|
|light conditions|75.0|78.7 (+3.7)|94.5|97.9 (+3.2)|
|objects layout|69.6|86.2(+16.6)|97.9|97.4 (-0.5)|
|background textures|81.1|87.6 (+6.5)|95.7|95.3 (-0.4)|
|sensor noise|19.9|18.2(-1.7)|91.2|93.4 (+2.2)|
|language instructions|37.9|55.9(+22.0)|90.0|90.0|
|robot initial states|10.3|6.3(-4.0)|82.6|84.9 (+2.3)|
|camera view points|21.3|15.2(-6.1)|79.3|79.5 (+0.2)|
|average|42.7|47.8 (+5.1)|89.8|90.8 (+1.0)|


**Results** . After 30k-step training, we evaluate on both _π_ 0 (mixture strategy) and _π_ 0 _._ 5 (replacement strategy) on the spatial suite of LIEBRO-plus, which contains **2402** evaluation settings. According to the results in Table 3, especially on _π_ 0 ’s performance comparison, it shows that adopting our augmentation method along with a training strategy can enhance models’ ability in simulated environments with disturbances like changing light conditions. The slight drop in camera viewpoints and robot initial states stems from a limitation of the current method: it mainly augments appearance, while these perturbations are geometry- and viewpoint-dependent. The results on _pi_ 0 _._ 5 also denote that even with a high-performance model, using our method can still lead to an obvious increase in some disturbance dimensions like sensor noise, light conditions, and robot initial states. 

Additionally, we also evaluate on LIBERO and observe a slight performance drop when training with augmented data: _π_ 0 decreases by an average of 0.2 and _π_ 0 _._ 5 by 0.5 across four task suites. This is expected, as LIBERO’s evaluation settings are nearly identical to its original training distribution—making aggressive augmentation introduce distributional disturbances rather than helpful diversity. Full results are provided in Table 10 (Appendix). 

2https://github.com/Physical-Intelligence/openpi 

6 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

We further compare mixture _vs._ replacement strategies for incorporating augmented data. Interestingly, _π_ 0 performs best under the mixture strategy, while _π_ 0 _._ 5 sees greater gains with replacement. This suggests that stronger pretrained models like _π_ 0 _._ 5 benefit more from challenging augmentations that shift the training distribution, while weaker models prefer a balance between clean and augmented samples. See Table 11 in the Appendix for details. 

## **4.3. Real-World Experiments and Results** 

To validate the effectiveness of our video augmentation framework in bridging the sim-to-real gap, we conduct comprehensive experiments on a physical robotic platform with diverse out-of-distribution (OOD) test scenarios. 

**Experimental setup.** We deploy our method on an AgileX Piper manipulator using two state-of-the-art VLA model variants: _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025b). We evaluate on two representative manipulation tasks: (1) _Stack Tape_ : “stacking a brown tape roll on top of another brown tape”; and (2) _Slot Pen_ : “inserting a yellow pen into a holder”. To systematically evaluate generalization capability, we design three test conditions with increasing levels of distribution shift, namely In-Distribution, Position Shift (OOD), and Background Shift (OOD). For details, see Figure 5 and Section B.4 in Appendix. 

**Results.** Table 4 presents the real-world experimental results across all tasks and test conditions. Our video augmentation method demonstrates consistent and substantial improvements over the baselines across both models. 

_Table 4._ Real-world results showing success counts (out of 10 trials) under three test conditions. 

|**Method**|**In-**<br>Slot.|**Dist.**<br> Stack.|**Pos**<br>Slot.|**ition**<br> Stack.|**Back**<br>Slot.|**ground**<br> Stack.|**Avg.**|
|---|---|---|---|---|---|---|---|
|_π_0_._5|9/10|10/10|5/10|4/10|4/10|4/10|60%|
|+ Ours|**10/10 **|**10/10**|**7/10**|**6/10**|**6/10**|**5/10**|**73%**|
|_π_0|9/10|9/10|3/10|5/10|6/10|4/10|60%|
|+ Ours|**10/10 **|**10/10**|**5/10**|**8/10**|**5/10**|**7/10**|**75%**|


**Analysis.** Several key observations emerge: 

_(1) Consistent improvements across VLA architectures._ Our model-agnostic method yields 13% and 15% absolute gains in average success rates for _π_ 0 _._ 5 and _π_ 0, respectively. This validates that the visual diversity from our video transfer pipeline benefits various VLA backbones without requiring architecture-specific modifications. 

_(2) Enhanced robustness to spatial perturbations._ Significant gains under position shifts (e.g., _π_ 0 on Stack Tape: 5/10 _→_ 8/10) suggest the model learns generalizable spatial rea- 

soning rather than memorizing fixed object configurations or action sequences. 

_(3) Improved visual domain generalization._ Improved performance under background shifts (e.g., _π_ 0 on Stack Tape: 4/10 _→_ 7/10) indicates that our synthetic diversity fosters robust feature representations that are resilient to taskirrelevant visual changes. 

_(4) Maintained in-distribution performance._ Augmented models maintain near-perfect in-distribution success rates (9–10/10), confirming that our pipeline preserves taskrelevant semantics and action fidelity while introducing beneficial diversity. 

## **4.4. Ablation Study** 

**Video augmentation with or without velocity cache.** To find the influence of using cache-based acceleration on augmented videos, we train RDT-1B on four tasks from Robotwin 2.0 - single-task learning with or without velocity cache. As the results summarized in Table 5, both cases obtain similar accuracies and achieve significant improvements over the original baseline. We also compare their visual quality in Figure 13 and Figure 14 of Appendix. Although the cache acceleration technique introduces minor degradation in texture details at the pixel level, our method successfully preserves environmental semantic information, which is essential for downstream policy learning, significantly reducing generation overhead without compromising the effectiveness of the augmented data. 

_Table 5._ Comparison of RDT-1B model finetuned using augmented data with or without velocity cache acceleration on Robotwin 2.0. 

|**Task Name**|**H**<br>w/ acc.|**ard**<br> w/o acc.|**E**<br>w/ acc.|**asy**<br> w/o acc.|
|---|---|---|---|---|
|move<br>~~c~~an<br>~~p~~ot|16.0|18.0|34.0|34.0|
|open<br>~~l~~aptop|42.0|44.0|54.0|56.0|
|rotate<br>~~q~~rcode|10.0|8.0|8.0|10.0|
|place<br>~~b~~urger<br>~~f~~ries|38.0|38.0|54.0|52.0|
|average|26.5|27.0|37.5|38.0|


**Evaluation of coreset sampling.** Figure 6 visualizes the video embeddings using t-SNE. The original dataset exhibits distinct clusters, each corresponding to semantically different tasks or visual contexts, with varying difficulty levels. Our selected coreset samples are well distributed across these clusters, covering both common and rare regions of the data manifold. Compared to random sampling, our method avoids over-representing redundant trajectories and instead targets high-loss, underrepresented areas. This balanced selection ensures that the augmented data introduces both semantic richness and policy-critical challenge, reinforcing 

7 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

generalization while avoiding unnecessary redundancy. 

To evaluate how the proportion of selected samples affects performance, we conduct an ablation using _π_ 0 across 796 evaluation settings from LIBERO-Plus’s spatial suite. 


_Figure 6._ Visualization of coreset sampling on the LIBERO training dataset with a 10% sampling budget. Right: the global difficulty distribution, where the color spectrum represents the mean policy loss (redder colors indicate higher difficulty). Left: the selected coreset overlaid on the full dataset. 


_Figure 7._ Performance comparison of different coreset sampling percentages on LIBERO-Plus spatial suite. 

As shown in Figure 7, even a small augmentation ratio (10%) yields a substantial improvement, with performance continuing to rise as more samples are included. However, the gain between 30% and 50% is only 0.9%, indicating diminishing returns and highlighting the effectiveness of our coreset sampling in identifying critical and diverse samples. 

## **4.5. Video Transferring Performance Assessment** 

To validate the efficacy of our proposed framework, we conducted a comparative study against the state-of-the-art baseline, RoboTransfer (Liu et al., 2025b). We evaluated performance across five representative tasks to assess both geometric consistency and semantic alignment. We employed two distinct sets of metrics to evaluate the synthesized video quality: 

**Geometric Consistency** : We measured the depth fidelity between generated sequences and original sequences using Video Depth Anything (Yang et al., 2024). Metrics include 

the Root Mean Square Error (RMSE), Absolute Relative Error (Abs.Rel), and Squared Relative Error (Sq.Rel). Lower values indicate higher geometric consistency. 

**Semantic Alignment** : We utilized VideoCLIP-XL (Wang et al., 2024) to compute the prompt-video similarity, quantifying how well the generated video adheres to the provided textual instructions. Higher similarity scores indicate better semantic correspondence. 

The quantitative results are summarized in Table 6 and Table 7. Our method consistently outperforms RoboTransfer across all evaluated tasks. 

_Table 6._ RoboTransfer Results 

|**task**|**RMSE **|**Abs.Rel **|**Sq.Rel**|**sim**|**time**|
|---|---|---|---|---|---|
|adjust bottle|0.46|0.37|0.39|21.5|340s|
|beat hammer|0.30|0.28|0.16|22.3|368s|
|handover|0.49|0.32|0.20|18.6|710s|
|hanging mug|0.41|0.34|0.26|24.2|814s|
|pick bottles|0.37|0.30|0.18|20.3|372s|
|**task**|_Table 7_<br>**RMSE **|_._ Ours Res<br> **Abs.Rel **|ults<br> **Sq.Rel**|**sim**|**time**|
|adjust bottle|0.28|0.16|0.07|26.3|441s|
|beat hammer|0.18|0.14|0.03|25.6|453s|
|handover block|0.23|0.17|0.06|27.7|619s|
|hanging mug|0.13|0.12|0.02|26.4|783s|
|pick bottles|0.12|0.11|0.03|26.8|448s|


Regarding geometric consistency, we observed a substantial reduction in error rates. Notably, the RMSE improved from 0.46 to 0.28 in the ”adjust bottle” task with Abs.Rel and Sq.Rel metrics demonstrating a 2–6× reduction across the board. Furthermore, our approach achieved superior semantic alignment, with prompt similarity scores consistently increasing from the 18.6–24.2 range to 25.6–27.7, while our method incurs a marginal increase in average runtime. 

# **5. Conclusion** 

We present a scalable video augmentation framework designed to address the generalization limitations of visionlanguage-action models trained on simulation. Our method introduces semantic and visual diversity into synthetic training data by combining structured caption rewriting, conditional video generation, efficient velocity-prediction caching, and coreset-based selective augmentation. Through experiments on Robotwin, LIBERO, and LIBERO-Plus, we demonstrate consistent performance improvements and enhanced robustness to real-world perturbations. Our results highlight that when diverse and targeted, even modest augmentation is effective in improving model generalization. 

8 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

# **Acknowledgements** 

This work was supported by the National Natural Science Foundation of China under Grant 62506235. 

# **Impact Statement** 

**Ethical Considerations** This research focuses on enhancing the generalization of Vision-Language-Action models through efficient sim-to-real video augmentation. While aiming to reduce reliance on costly real-world data, we emphasize the need for ethical vigilance in deploying such technologies. Key considerations include ensuring transparency in generated data, mitigating biases inherited from simulations or language models, and maintaining alignment with human values in autonomous decision-making. We encourage ongoing community efforts to address these ethical challenges alongside technical progress. 

**Societal Implications** By lowering barriers to robust robotic system development, this work could positively impact fields like industrial automation and assisted services. However, broader adoption may also introduce societal shifts, such as changes in labor dynamics or unintended use cases. We advocate for proactive dialogue to guide responsible innovation, ensuring benefits are widely distributed while risks are carefully managed. In line with standard practice, we defer detailed societal impact discussions to broader interdisciplinary efforts. 

# **References** 

- Abbas, A., Tirumala, K., Simig, D., Ganguli, S., and Morcos, A. S. Semdedup: Data-efficient learning at webscale through semantic deduplication. <u>arXiv preprint arXiv:2303.09540, 2023.</u> 

- Alhaija, H. A., Alvarez, J., Bala, M., Cai, T., Cao, T., Cha, L., Chen, J., Chen, M., Ferroni, F., Fidler, S., et al. Cosmos-transfer1: Conditional world generation with adaptive multimodal control. <u>arXiv preprint arXiv:2503.14492, 2025.</u> 

- Ali, A., Bai, J., Bala, M., Balaji, Y., Blakeman, A., Cai, T., Cao, J., Cao, T., Cha, E., Chao, Y.-W., et al. World simulation with video foundation models for physical ai. <u>arXiv preprint arXiv:2511.00062, 2025.</u> 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. <u>arXiv preprint arXiv:2410.24164,</u> 2024. 

- Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., 

Letts, A., et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. <u>arXiv preprint arXiv:2311.15127, 2023.</u> 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. <u>arXiv preprint arXiv:2212.06817, 2022.</u> 

- Chen, T., Chen, Z., Chen, B., Cai, Z., Liu, Y., Li, Z., Liang, Q., Lin, X., Ge, Y., Gu, Z., et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. <u>arXiv preprint arXiv:2506.18088, 2025.</u> 

- Dong, Z., Wang, X., Zhu, Z., Wang, Y., Wang, Y., Zhou, Y., Wang, B., Ni, C., Ouyang, R., Qin, W., et al. Emma: Generalizing real-world robot manipulation via generative visual transfer. <u>arXiv preprint arXiv:2509.22407, 2025.</u> 

- Ebert, F., Yang, Y., Schmeckpeper, K., Bucher, B., Georgakis, G., Daniilidis, K., Finn, C., and Levine, S. Bridge data: Boosting generalization of robotic skills with crossdomain datasets. <u>arXiv preprint arXiv:2109.13396, 2021.</u> 

- Fang, I., Zhang, J., Tong, S., and Feng, C. From intention to execution: Probing the generalization boundaries of vision-language-action models. <u>arXiv preprint arXiv:2506.09930, 2025a.</u> 

- Fang, Y., Yang, Y., Zhu, X., Zheng, K., Bertasius, G., Szafir, D., and Ding, M. Rebot: Scaling robot learning with realto-sim-to-real robotic video synthesis. <u>arXiv preprint arXiv:2503.14526, 2025b.</u> 

- Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., Ji, L., He, X., Zhang, S., Fei, Z., et al. Libero-plus: In-depth robustness analysis of vision-language-action models. <u>arXiv preprint arXiv:2510.13626, 2025.</u> 

- Gao, L., Biderman, S., Black, S., Golding, L., Hoppe, T., Foster, C., Phang, J., He, H., Thite, A., Nabeshima, N., et al. The pile: An 800gb dataset of diverse text for language modeling. <u>arXiv preprint arXiv:2101.00027,</u> 2020. 

- Intelligence, P., Amin, A., Aniceto, R., Balakrishna, A., Black, K., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., DiCarlo, J., et al. _π_ *0 _._ 6: a vla that learns from experience. <u>arXiv preprint arXiv:2511.14759, 2025a.</u> 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. <u>arXiv preprint arXiv:2504.16054,</u> 2025b. 

9 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

- Jiang, Z., Han, Z., Mao, C., Zhang, J., Pan, Y., and Liu, Y. Vace: All-in-one video creation and editing. <u>arXiv preprint arXiv:2503.07598, 2025.</u> 

- Karamcheti, S., Nair, S., Balakrishna, A., Liang, P., Kollar, T., and Sadigh, D. Prismatic vlms: Investigating the design space of visually-conditioned language models. In <u>Forty-first International Conference on Machine Learning, 2024.</u> 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. <u>arXiv preprint arXiv:2406.09246, 2024.</u> 

- Lee, K., Ippolito, D., Nystrom, A., Zhang, C., Eck, D., Callison-Burch, C., and Carlini, N. Deduplicating training data makes language models better. In <u>Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp.</u> 8424–8445, 2022. 

- Li, K., He, Y., Wang, Y., Li, Y., Wang, W., Luo, P., Wang, Y., Wang, L., and Qiao, Y. Videochat: Chat-centric video understanding. <u>Science China Information Sciences, 68</u> (10):200102, 2025. 

- Li, W., Su, X., You, S., Wang, F., Qian, C., and Xu, C. Diffnas: Bootstrapping diffusion models by prompting for better architectures. In <u>2023 IEEE International Conference on Data Mining (ICDM), pp. 1121–1126. IEEE, 2023.</u> 

- Li, W., Su, X., Cao, Y., Xu, H., Xia, X., You, S., Chen, Y., and Xu, C. Sentinel-vla: A metacognitive vla model with active status monitoring for dynamic reasoning and error recovery. <u>arXiv preprint arXiv:2605.01191, 2026a.</u> 

- Li, W., Su, X., Niu, D., Cao, Y., Xu, H., Qu, Z., Fan, L., You, S., and Xu, C. Vla-attc: Adaptive test-time compute for vla models with relative action critic model. <u>arXiv preprint arXiv:2605.01194, 2026b.</u> 

- Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling. <u>arXiv preprint arXiv:2210.02747, 2022.</u> 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. <u>Advances in Neural Information Processing Systems, 36:44776–44791, 2023.</u> 

- Liu, F., Zhang, S., Wang, X., Wei, Y., Qiu, H., Zhao, Y., Zhang, Y., Ye, Q., and Wan, F. Timestep embedding tells: It’s time to cache for video diffusion model. In <u>Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 7353–7363, 2025a.</u> 

- Liu, L., Wang, X., Zhao, G., Li, K., Qin, W., Zhu, J., Qiu, J., Zhu, Z., Huang, G., and Su, Z. Robotransfer: Geometryconsistent video diffusion for robotic visual policy transfer. 2025b. 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. <u>arXiv preprint arXiv:2410.07864, 2024.</u> 

- Maharana, A., Yadav, P., and Bansal, M. D2 pruning: Message passing for balancing diversity and difficulty in data pruning. <u>arXiv preprint arXiv:2310.07931, 2023.</u> 

- NVIDIA, Ferroni, F., Chattopadhyay, P., Heinrich, G., Ranzinger, M., Amoroso, R., Luo, A., Wang, A., and Liu, M.-Y. Cosmos-embed1: A joint video-text embedder for physical ai, 2025. URL https://research .nvidia.com/labs/dir/cosmos-embed1. 

- Pei, X., Chen, Y., Xu, S., Wang, Y., Shi, Y., and Xu, C. Action-aware dynamic pruning for efficient vision-language-action manipulation. <u>arXiv preprint arXiv:2509.22093, 2025.</u> 

- Penedo, G., Malartic, Q., Hesslow, D., Cojocaru, R., Cappelli, A., Alobeidli, H., Pannier, B., Almazrouei, E., and Launay, J. The refinedweb dataset for falcon llm: outperforming curated corpora with web data, and web data only. <u>arXiv preprint arXiv:2306.01116, 2023.</u> 

- Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., and Liu, P. J. Exploring the limits of transfer learning with a unified text-to-text transformer. <u>Journal of machine learning research,</u> 21 (140):1–67, 2020. 

- Ravi, N., Gabeur, V., Hu, Y.-T., Hu, R., Ryali, C., Ma, T., Khedr, H., Radle,¨ R., Rolland, C., Gustafson, L., et al. Sam 2: Segment anything in images and videos. <u>arXiv preprint arXiv:2408.00714, 2024.</u> 

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P., and Ommer, B. High-resolution image synthesis with latent diffusion models. In <u>Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,</u> pp. 10684–10695, 2022. 

- Sorscher, B., Geirhos, R., Shekhar, S., Ganguli, S., and Morcos, A. Beyond neural scaling laws: beating power law scaling via data pruning. <u>Advances in Neural Information Processing Systems, 35:19523–19536, 2022.</u> 

- Team, G., Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., Li, H., Li, J., Zhu, J., Feng, L., et al. Gigabrain-0: A world model-powered vision-language-action model. <u>arXiv preprint arXiv:2510.19430, 2025a.</u> 

10 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

- Team, G., Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., Li, H., Zhu, J., Li, K., Xu, M., et al. Gigaworld-0: World models as data engine to empower embodied ai. <u>arXiv preprint arXiv:2511.19861, 2025b.</u> 

- Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.-W., Chen, D., Yu, F., Zhao, H., Yang, J., et al. Wan: Open and advanced large-scale video generative models. <u>arXiv preprint arXiv:2503.20314, 2025.</u> 

- Wang, B., Meng, X., Wang, X., Zhu, Z., Ye, A., Wang, Y., Yang, Z., Ni, C., Huang, G., and Wang, X. Embodiedreamer: Advancing real2sim2real transfer for policy training via embodied world modeling. <u>arXiv preprint arXiv:2507.05198, 2025.</u> 

   - Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. <u>arXiv preprint arXiv:2304.13705, 2023.</u> 

   - Zhou, X., Liang, D., Chen, K., Feng, T., Chen, X., Lin, H., Ding, Y., Tan, F., Zhao, H., and Bai, X. Less is enough: Training-free video diffusion acceleration via runtimeadaptive caching. <u>arXiv preprint arXiv:2507.02860,</u> 2025a. 

   - Zhou, X., Xu, Y., Tie, G., Chen, Y., Zhang, G., Chu, D., Zhou, P., and Sun, L. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization. <u>arXiv preprint arXiv:2510.03827, 2025b.</u> 

- Wang, J., Wang, C., Huang, K., Huang, J., and Jin, L. Videoclip-xl: Advancing long description understanding for video clip models. <u>arXiv preprint arXiv:2410.00741,</u> 2024. 

- Wenzek, G., Lachaux, M.-A., Conneau, A., Chaudhary, V., Guzman,´ F., Joulin, A., and Grave, E. Ccnet: Extracting high quality monolingual datasets from web crawl data. In <u>Proceedings of the twelfth language resources and evaluation conference, pp. 4003–4012, 2020.</u> 

- Xie, S. M., Santurkar, S., Ma, T., and Liang, P. S. Data selection for language models via importance resampling. <u>Advances in Neural Information Processing Systems, 36:</u> 34201–34227, 2023. 

- Xu, S., Wang, Y., Xia, C., Zhu, D., Huang, T., and Xu, C. Vla-cache: Efficient vision-language-action manipulation via adaptive token caching. <u>arXiv preprint arXiv:2502.02175, 2025a.</u> 

- Xu, S., Wang, Z., Wang, Y., Xia, C., Huang, T., and Xu, C. Affordance field intervention: Enabling vlas to escape memory traps in robotic manipulation. <u>arXiv preprint arXiv:2512.07472, 2025b.</u> 

- Xu, Y., Yang, J., Wang, X., Chen, Y., Zhu, Z., Fang, B., Huang, G., Chen, X., Ye, Y., Zhang, Q., et al. Egodemogen: Novel egocentric demonstration generation enables viewpoint-robust manipulation. <u>arXiv preprint arXiv:2509.22578, 2025c.</u> 

- Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical report. <u>arXiv preprint arXiv:2505.09388, 2025.</u> 

- Yang, L., Kang, B., Huang, Z., Zhao, Z., Xu, X., Feng, J., and Zhao, H. Depth anything v2. <u>Advances in Neural Information Processing Systems,</u> 37:21875– 21911, 2024. 

11 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

# **A. Additional Experiments** 

## **A.1. Results of More Model Variants on RoboTwin 2.0** 

For ACT and _π_ 0, we carry out an experiment on a single task from RoboTwin 2.0 using 50 trajectories collected in a clean environment for finetuning. The average increase on hard mode is 3.0 for ACT and 2.0 for _π_ 0. These results show that our method is suitable for both the VLA framework, including a pre-trained model (ACT), and the finetuning model ( _π_ 0). 

_Table 8._ ACT: Performance (%) comparison of the original simulation data (Ori.) _vs._ augmented data (Aug.) on ACT (Zhao et al., 2023) in Hard vs. Easy scenarios of Robotwin 2.0 (Chen et al., 2025) 

|**Task Name**|Ori.|**Hard**<br>Aug.|Ori.|**Easy**<br>Aug.|
|---|---|---|---|---|
|adjust<br>~~b~~ottle|20.0|26.0 (+6.0)|92.0|94.0 (+2.0)|
|beat<br>~~b~~lock<br>~~h~~ammer|2.0|2.0|56.0|52.0 (-4.0)|
|pick<br>~~d~~ual<br>~~b~~ottles|0.0|4.0 (+4.0)|30.0|34.0 (+4.0)|
|place<br>~~b~~urger<br>~~f~~ries|0.0|0.0|46.0|52.0 (+6.0)|
|open<br>~~l~~aptop|0.0|0.0|54.0|58.0 (+4.0)|
|move<br>~~c~~an<br>~~p~~ot|2.0|4.0 (+2.0)|20.0|28.0 (+8.0)|
|rotate<br>~~q~~rcode|0.0|0.0|2.0|2.0|
|grab<br>~~r~~oller|22.0|32.0 (+10.0)|94.0|90.0 (-4.0)|
|average|6.0|9.0 (+3.0)|49.0|51.0 (+2.0)|


_Table 9. π_ 0: Performance (%) comparison of the original simulation data (Ori.) _vs._ augmented data (Aug.) on _π_ 0 (Black et al., 2024) in Hard vs. Easy scenarios of Robotwin 2.0 (Chen et al., 2025) 

|**Task Name**|Ori.|**Hard**<br>Aug.|Ori.|**Easy**<br>Aug.|
|---|---|---|---|---|
|adjust<br>~~b~~ottle|74.0|78.0 (+4.0)|90.0|92.0 (+2.0)|
|beat<br>~~b~~lock<br>~~h~~ammer|20.0|16.0(-4.0)|42.0|48.0 (-6.0)|
|pick<br>~~d~~ual<br>~~b~~ottles|12.0|10.0 (-2.0)|56.0|60.0 (+4.0)|
|place<br>~~b~~urger<br>~~f~~ries|4.0|10.0 (+6.0)|80.0|76.0 (+6.0)|
|open<br>~~l~~aptop|46.0|54.0(+8.0)|84.0|84.0|
|move<br>~~c~~an<br>~~p~~ot|2.0|4.0 (+2.0)|56.0|64.0 (+8.0)|
|rotate<br>~~q~~rcode|16.0|20.0 (+4.0)|66.0|68.0 (+2.0)|
|grab<br>~~r~~oller|78.0|76.0 (-2.0)|84.0|96.0 (+12.0)|
|average|31.5|33.5 (+2.0)|69.8|73.5 (+3.7)|


## **A.2. Experiments on LIBERO and LIBERO-Plus** 

As showed in Table 10, we also evaluate on LIBERO using _π_ 0 and _π_ 0 _._ 5 and observe a slight performance drop when training with augmented data: _π_ 0 decreases by an average of 0.2 and _π_ 0 _._ 5 by 0.5 across four task suites. This slight drop is caused by the evaluation environment of LIBERO, which is almost identical to the original training data, making aggressive augmentation introduce distributional disturbances. What ’s more, with the performance of _π_ 0 and _π_ 0 _._ 5 approach full scores, it can hardly evaluate improvement. 

**Comparison of mixture and replacement strategies on LIBERO-Plus.** In Table 11, by comparing the use of mixture and replacement on both _π_ 0 and _π_ 0 _._ 5, it is proved that using both strategies can help to boost models’ performance on the evaluation benchmark. However, whether to choose the mixture strategy or the replacement strategy depends on the models’ features. For example, using the mixture strategy on _π_ 0 can surpass using the replacement strategy. 

12 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

_Table 10._ Performance of _π_ 0 (mixture strategy) and _π_ 0 _._ 5(replacement strategy) on LIBERO. 

|**Task Name**|_π_<br>Ori.|0<br>Aug.|_π_<br>Ori.|0_._5<br>Aug.|
|---|---|---|---|---|
|libero spatial|96.8|96.4|98.8|97.8|
|libero object|98.8|98.5|98.2|98.4|
|libero goal|95.8|96.1|98.0|98.2|
|libero 10|85.2|84.7|92.4|91.0|
|average|94.1|93.9|96.8|96.3|


_Table 11._ Performance (%) comparison on spatial suite from LIBERO-Plus using _π_ 0 and _π_ 0 _._ 5, “Rep” means using the Replacement strategy, “Mix” means using the mixture strategy 

|**Task Name**|Ori.|_π_0<br>Aug. (Rep)|Aug. (Mix)|Ori.|_π_0_._5<br>Aug. (Rep)|Aug. (Mix)|
|---|---|---|---|---|---|---|
|light conditions|75.0|75.7|78.7|94.5|97.9|99.3|
|objects layout|69.6|66.2|86.2|97.9|97.4|97.1|
|background textures|81.1|83.4|87.6|95.7|95.3|95.3|
|sensor noise|19.9|16.2|18.2|91.2|93.4|93.4|
|language instructions|37.9|43.2|55.9|90.0|90.0|89.1|
|robot initial states|10.3|8.1|6.3|82.6|84.9|83.2|
|camera view points|21.3|17.4|15.2|79.3|79.5|79.3|
|average|42.7|43.3|47.8|89.8|90.8|90.2|


## **A.3. Computation analysis** 

During the full procedure for transferring video, the computation costs are computed based on setting the pixels of the input video to 960*720 (width, height). We use one A800 80GB GPU for generating, the average time saving percentage (Acceleration Rate) is shown in Figure 8. The average time on the selected ten tasks to augment one video (episode) is 560 seconds on one GPU. Augmenting the full dataset of 50 videos requires 7.7 GPU hours. Training the RDT-1B model on 50 episodes requires 56 GPU hours; augmentation adds only 13.8% overhead. 


_Figure 8._ Acceleration rates across 10 Robotwin 2.0 tasks. Our method reduces runtime by over 60% on average. Task 1-10: beat block hammer, adjust bottle, handover block, haing mug, pick dual bottles, place a2b right, place burger fries, place dual shoes, stack blocks two, pick diverse bottles. 

## **A.4. Justification on hyperparameters** 

The choice of k=0.4 and a=8 when transferring videos is based on a trade-off between efficiency and visual–geometric fidelity, validated through ablations on a representative task: Adjust Bottle. We vary k from 0.2 to 0.8 while keeping a=8 constant. As shown in Table 12, increasing k generally leads to a slight degradation in geometric fidelity (e.g., RMSE and 

13 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

Abs.Rel increase), while time cost decreases marginally. However, the overall performance remains stable. 

_Table 12._ Varying k (with a=8) 

|_k_|RMSE|Abs.Rel|Sq.Rel|sim|time cost|
|---|---|---|---|---|---|
|0.2|0.26|0.14|0.06|25.04|467s|
|0.4|0.28|0.16|0.07|26.37|441s|
|0.6|0.24|0.13|0.04|25.17|446s|
|0.8|0.32|0.18|0.08|25.16|425s|


We then fix k=0.4 and vary a from 4 to 12. As reported in Table 13, the configuration a=8 achieves the best balance: it maintains high semantic alignment with stable geometry (lowest Sq.Rel and competitive RMSE/Abs.Rel), while achieving the lowest time cost (441 s). Smaller values of a lead to higher time costs without significant accuracy gains, while larger values of a degrade geometric fidelity. 

_Table 13._ Varying a (with k=0.4) 

|_a_|RMSE|Abs.Rel|Sq.Rel|sim|time cost|
|---|---|---|---|---|---|
|4|0.26|0.16|0.06|25.47|501s|
|6|0.24|0.15|0.06|25.14|446s|
|8|0.28|0.16|0.07|26.37|441s|
|12|0.26|0.14|0.05|25.36|395s|


We further validate robustness on real-world tasks using the same parameters. The results in Table 14 show that the chosen configuration generalizes well across both simulated and real-world scenarios. 

_Table 14._ Real-world Tasks Validation 

|Task|RMSE|Abs.Rel|Sq.Rel|sim|
|---|---|---|---|---|
|slot pen into holder|0.156|0.150|0.02|27.04|
|stack pipe|0.20|0.14|0.03|26.8|


# **B. Implementation Details** 

## **B.1. Using details of cosmos-transfer2.5** 

We use the original video as input, the depth video obtained from depth anything, and the prompt generated by our method as the control condition. The input pixels is set to be 960*720 (height, width). The total diffusion steps are set to 35. The number of frames per chunk is set to be 93. 

## **B.2. LLM Rewriter** 

The designed prompt we are using to ask Qwen3-8B to rewrite the conditional prompt is as follows, where “video ~~d~~ escription” means video caption, “task ~~i~~ nstruction” means instruction got from the original dataset. 

**<user>:** You are given a video caption describing a robot manipulation scene and a brief origin video description. Your task is to generate a new video caption for a text-to-video generation model. The new captions should: 

- <sup>Onlychangethetablesurfaceortheobject’ssurface,likechangingthematerialto</sup> 

- create differences. 

- <sup>Outputstyleisexpectedtolooklikethefollowingstrictly:</sup> The video is a 

- demonstration of robotic manipulation, likely in a laboratory or industrial setting. It features a single robotic arm interacting with a plastic bottle. The setting is a room with a polished stainless steel countertop, which reflects overhead lights and provides a sterile, metallic backdrop for the activity. The robotic arm, marked 

14 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

‘AGILE X’, is positioned above the bottle, which is filled with a dark liquid. At the beginning, the bottle is standing upright on the counter. The robotic arm approaches the bottle, its gripper maneuvering with precision as it positions itself. The arm’s gripper then grasps the bottle firmly by its neck. As the arm lifts the bottle smoothly, the liquid inside sways gently. The entire process highlights the precision and control of the robotic arm. The camera remains static throughout, focusing on the interaction between the robotic arm and the bottle, allowing viewers to observe the detailed movements involved in the task. 

*<sup>Thecentralfocusofthecaptionshouldbeonatable’ssurface.</sup> The table should be made of wood, stainless steel, or marble. 

*<sup>Outputisexpectedtobebriefandeasyenoughforthediffusionmodeltounderstand.</sup> 

*<sup>Thefinaloutputshouldcontainonlythenewcaptionwithnoadditionalcommentaryor</sup> explanation. The video caption is: **_{_ video** **~~d~~ escription** **_}_** 

*<sup>Thebrieforiginvideodescriptionfrominstructionis:</sup> **_{_ task** **~~i~~ nstruction** **_}_** , make sure that the output content has the same meaning and object name as the given brief description. 

**<example output 1>:** The video is a demonstration of robotic manipulation, likely in a laboratory or industrial setting. It features a single robotic arm interacting with a green plastic bottle. The setting is a room with a polished wooden table, which provides a warm, natural backdrop for the activity. The robotic arm, marked ’AGILE’, is positioned above the bottle. At the beginning, the bottle is standing upright on the table. The robotic arm approaches the bottle, its gripper maneuvering with precision as it positions itself. The arm’s gripper then grasps the bottle firmly by its neck. As the arm lifts the bottle smoothly, the process highlights the precision and control of the robotic arm. The camera remains static throughout, focusing on the interaction between the robotic arm and the bottle, allowing viewers to observe the detailed movements involved in the task. **<example output 2>:** The video is a demonstration of robotic manipulation, likely in a laboratory or industrial setting. It features a single robotic arm interacting with a metal kitchen pot. The setting is a room with a polished wooden countertop, which contrasts with the metallic elements and provides a warm, natural backdrop for the activity. The robotic arm, marked ’AGILE X’, is positioned above the pot, which is empty and neatly placed. At the beginning, the kitchen pot is resting on the counter. The robotic arm approaches the pot, its gripper maneuvering with precision as it positions itself. The arm’s gripper then grasps the pot firmly by its handles. As the arm lifts the pot smoothly, the action demonstrates meticulous control. The entire process showcases the precision and dexterity of the robotic arm. The camera remains static throughout, focusing on the interaction between the robotic arm and the pot, allowing viewers to observe the detailed movements involved in the task. **<example output 3>:** The video is set in an experimental lab, featuring a robotic arm labeled ’AGILE’. The arm hovers above a white sneaker on a blue mat, which rests on an elegant wooden table. Surrounding the sneaker, various items such as a trophy, a can, and a small bell are visible. The robotic arm approaches the sneaker, implying an interaction, possibly for cleaning or maintenance. **<example output 4>:** The video is a demonstration of robotic manipulation, likely in a laboratory or industrial setting. It features a single robotic arm interacting with a slanted rectangular soap. The setting is a room with a polished marble countertop, which beautifully reflects overhead lights and provides an elegant, smooth backdrop for the activity. The robotic arm, marked ’AGILE X’, is positioned above a light wood cabinet. At the beginning, the cabinet drawer is closed. The robotic arm approaches, its gripper maneuvering with precision as it opens the drawer. The arm’s gripper then gently grasps the soap, noted for its slight groove pattern, and places it inside the open drawer. The entire process highlights the precision and control of the robotic arm. The camera remains static throughout, focusing on the interaction between the robotic arm, the soap, and the drawer, allowing viewers to observe the detailed movements involved in the task. 

## **B.3. Velocity Caching Strategy** 

Algorithm 1 provides pseudocode for our velocity caching mechanism. In practice, we set _k_ = 0 _._ 4, _α_ = 8, and _m_ = 3 based on empirical tuning. 

15 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

**Algorithm 1** Three-Stage Velocity Caching 

**Require:** Total steps _N_ , stable threshold _k_ , cache interval _α_ , adjustment steps _m_ 1: **for** _t_ = 0 _→ N −_ 1 **do** 2: Determine current phase (Initial, Stable, Adjustment) 3: **if** Stable Phase and _t_ mod _α̸_ = 0 **then** 4: _vt ← v_ cache _{_ Reuse previous value _}_ 5: **else** 6: _vt ← vθ_ ( _xt, t_ ) _{_ Recompute _}_ 7: Update _v_ cache _← vt_ 8: **end if** 9: _xt_ +1 _← xt_ + ∆ _t · vt_ 10: **end for** 

## **B.4. Real-World Experiments** 

**Experimental setup.** We deploy our method on an AgileX Piper manipulator equipped with a wrist-mounted camera for visual observation. Data collection is performed via teleoperation using a master-follower arm configuration. We evaluate on two representative manipulation tasks: (1) _Stack Tape_ : “stacking a brown tape roll on top of another brown tape”; and (2) _Slot Pen_ : “inserting a yellow pen into a holder.” For each task, we collect approximately 80 teleoperated demonstrations (80 episodes for Stack Tape, 77 episodes for Slot Pen). Using our proposed video augmentation pipeline, we generate an equal number of augmented trajectories at a 1:1 ratio, resulting in 160 and 154 total training episodes, respectively. 

**Distribution shift settings.** To systematically evaluate generalization capability, we design three test conditions with increasing levels of distribution shift: 

_(1) In-Distribution (I.D.)._ Target objects (tape or pen) are randomly displaced within a 5cm range from training positions, using the original white table background. 

_(2) Position Shift (OOD)._ Target objects are displaced beyond the 5cm training range, introducing spatial perturbations while maintaining the standard white background. 

_(3) Background Shift (OOD)._ Objects remain within the 5cm training range, but the table background is changed from white to black to introduce a visual domain shift. These three scenarios are visualized in Figure 5. 

**Evaluation protocol.** Each task is evaluated over 10 trials per test condition. A trial is considered successful if the robot completes the full manipulation sequence: for Stack Tape, the robot must grasp and place the tape stably on top of the target tape; for Slot Pen, the pen must be fully inserted into the holder slot. We compare models fine-tuned on original data (baseline) against models fine-tuned on augmented data (ours) using the official OpenPi framework with default full-parameter fine-tuning settings on an NVIDIA H200 GPU. 

# **C. Training configurations** 

We provide detailed training configurations below: 

**Pi0 for LIBERO and LIBERO-Plus in experiment 4.2** followed the standard full fine-tuning configurations provided by the OpenPi repository, which was trained for 30,000 steps with a global batch size of 32 . 

**Pi0.5 for LIBERO and LIBERO-Plus in experiment 4.2** followed the standard full fine-tuning configurations provided by the OpenPi repository, which was trained for 30,000 steps with a global batch size of 256 . 

**RDT for RoboTwin 2.0 multi-tasks training in experiment 4.1** followed the standard training configurations provided by the RoboTwin 2.0 repository, which was trained for 100,000 steps with a batch size of 16 per GPU on 8 GPUs. 

**RDT for RoboTwin 2.0 single-task training in experiment 4.1** followed the standard training configurations provided by the RoboTwin 2.0 repository, which was trained for 10,000 steps with a batch size of 16 per GPU on 4 GPUs. 

**Pi0 for RoboTwin 2.0 single-task training in experiment 4.1** followed the standard training configurations provided by the RoboTwin 2.0 repository, which was performed for 30,000 steps using the global batch size of 32. 

16 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 

**ACT for RoboTwin 2.0 single-task training in experiment 4.1** followed the standard training configurations provided by the RoboTwin 2.0 repository, which was trained under a unified setup with a chunk size of 50, batch size of 8, and single-GPU training for 6,000 epochs. 

# **D. Visualization of Augmented Videos** 

## **D.1. Augmented Video** **_vs._ Original Video** 

In Figure 9, we visualize the transferred videos along with their original videos obtained from Robotwin 2.0’s domain randomized tasks, including lift pot and pick bottle. 


_Figure 9._ Visualizations of augmented videos and origin videos from Robotwin 2.0 

In Figure 10, we visualize the transferred videos along with their original videos obtained from the LIBERO official dataset. 

17 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 


_Figure 10._ Visualizations of augmented videos and origin videos from LIBERO 

In Figure 11, we visualize the transferred videos along with their original videos, which were obtained from real-world recordings, including tasks “pick and place carrot” and “remove lid from pot”. 


_Figure 11._ Visualizations of augmented videos and original videos from a real robot experiment 

In Figure 12, we visualize the transferred videos along with their original videos got from real-world recordings, including tasks “slot pen into holder” and “stack tapes”. 

18 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 


_Figure 12._ Visualizations of augmented videos and original videos from a real robot experiment 

## **D.2. Augmenting Videos with or without Velocity Caching** 

In Figure 13, we visualize the transferred videos along with their original videos obtained from Robotwin 2.0’s domain clean tasks and compare between using acceleration and not using acceleration. 


_Figure 13._ Comparing between using cache-based acceleration and not using 

In Figure 14, we visualize the transferred videos along with their original videos obtained from Robotwin 2.0 ’s domain clean tasks and compare using acceleration and not using acceleration. 

19 

**Efficient Video Transfer for Vision-Language-Action Data Augmentation** 


_Figure 14._ Comparing between using cache-based acceleration and not using 

20 

