---
title: "Vision-Language Models Unlock Task-Centric Latent Actions"
date: "2026-01-30"
authors: "Alexander Nikulin; Ilya Zisman; Albina Klepach; Denis Tarasov; Alexander Derevyagin; Andrei Polubarov"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2601.22714
pdf: https://arxiv.org/pdf/2601.22714
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.22714)** / [論文ページ](https://arxiv.org/abs/2601.22714)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Vision-Language Models Unlock Task-Centric Latent Actions** 

**Alexander Nikulin**<sup>1 2</sup> **Ilya Zisman**<sup>3 †</sup> **Albina Klepach**<sup>1</sup> **Denis Tarasov**<sup>1 †</sup> **Alexander Derevyagin**<sup>1</sup> **Andrei Polubarov**<sup>1 4 5</sup> **Lyubaykin Nikita**<sup>1 6</sup> **Vladislav Kurenkov**<sup>1 6</sup> 

# **Abstract** 

Latent Action Models (LAMs) have rapidly gained traction as an important component in the pre-training pipelines of leading VisionLanguage-Action models. However, they fail when observations contain action-correlated distractors, often encoding noise instead of meaningful latent actions. Humans, on the other hand, can effortlessly distinguish task-relevant motions from irrelevant details in any video given only a brief task description. In this work, we propose to utilize the common-sense reasoning abilities of Vision-Language Models (VLMs) to provide promptable representations, effectively separating controllable changes from the noise in unsupervised way. We use these representations as targets during LAM training and benchmark a wide variety of popular VLMs, revealing substantial variation in the quality of promptable representations as well as their robustness to different prompts and hyperparameters. Interestingly, we find that more recent VLMs may perform worse than older ones. Finally, we show that simply asking VLMs to ignore distractors can substantially improve latent action quality, yielding up to a six-fold increase in downstream success rates on Distracting MetaWorld. 

# **1. Introduction** 

Latent action models (LAMs) (Schmidt & Jiang, 2023; Ye et al., 2024) have quickly become integral to the pre-training pipelines of leading Vision–Language–Action (VLA) models (Bjorck et al., 2025; Bu et al., 2025a; Zhong et al., 2025; Bruce et al., 2024; Jang et al., 2025). By inferring compact, semantically meaningful latent action representations at scale, LAMs mitigate the scarcity of high-quality action- 

†Work done while at AIRI 1AIRI 2MSU 3Humanoid 4Skoltech 5Research Center for Trusted Artificial Intelligence, ISP RAS 6Innopolis University. Correspondence to: Alexander Nikulin _<_ nikulin@airi.net _>_ . 

_Preprint. February 2, 2026._ 


_Figure 1._ **Main result** . Success rate on MetaWorld-10 benchmark for LAPO and proposed LAPO+VLM (Molmo), which uses promptable representations. We use three random seeds and report IQM and 95%-CI based on stratified bootstrapping, following the Agarwal et al. (2021). See Section 7 for full results. 

labeled data, removing the data bottleneck in embodied AI and robotics (McCarthy et al., 2025). Unfortunately, early LAMs that gained recognition (Schmidt & Jiang, 2023; Ye et al., 2024; Chen et al., 2024b; Gao et al., 2025) were trained on relatively clean datasets, where changes between observations could be explained almost entirely by groundtruth actions, such as in static scenes with a single manipulator. In contrast, real-world data often contains numerous action-correlated distractors, including background human movement or other spurious correlations. 

However, as shown by Nikulin et al. (2025); Zhang et al. (2025); Klepach et al. (2025), without explicit supervision, LAMs struggle to disentangle controllable changes from noise, completely failing to produce meaningful latent actions in the presence of action-correlated distractors. Humans, however, interpret the world through semantics rather than raw pixels, and with only a brief task description can easily separate task-relevant features from irrelevant details. Wouldn’t it also be convenient to simply ask LAM to focus on the relevant features, e.g. robotic arm, and ignore any other details? 

Inspired by the work of Chen et al. (2024a) on promptable representations, we propose to utilize the Vision-Language 

1 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 2._ Visualization of the task-relevant promptable representations extraction from the VLMs and their subsequent use as targets during latent action learning. 

Models (VLMs) common-sense reasoning abilities as an unsupervised approach for effectively separating controllable changes from noise, thereby restoring the LAM’s ability to recover ground-truth actions even in the presence of distractors. Using a controlled Distracting MetaWorld (Yu et al., 2020) setup, we show that representations produced by prompting VLMs to focus on task-specific details can serve as an effective target for LAMs in the presence of distractors, increasing the success rate six-fold (see Figure 1). 

As a motivation for our approach, we begin from a simple demonstration experiment, showing that limitations of LAM can be mitigated with the clean target (Section 5). We then conduct large-scale benchmarking of different VLMs, comprising over 29k+ experiments, to assess their effectiveness at providing promptable representations (Section 6), revealing substantial variation in quality and robustness to hyperparameters. In addition, we show that VLMs significantly outperform self-supervised methods, such as DINOv2 (Oquab et al., 2023) or CLIP (Radford et al., 2021), confirming our hypothesis that language based filtering is essential for performance. Finally, using the best setup found, we demonstrate that, without any supervision, promptable representations can significantly improve latent action quality and downstream performance (Section 7), outperforming OTTER (Huang et al., 2025) and UniVLA (Bu et al., 2025b) baselines. 

# **2. Preliminaries** 

**Problem setting.** We consider a setting of offline imitation learning from observation (Liu et al., 2018; Torabi et al., 2019). Our goal is to pre-train a policy _π_ ( _o|a_ ), given a large dataset of expert trajectories _D_ := _{_ ( _o_<sup>_n_</sup> _i_<sup>)</sup><sup>_}τ_</sup> _i_ =1<sup>,containing</sup> observations but not actions (e.g. videos), and a limited number of real action labels. Ideally, the pre-trained agent should achieve maximum performance (e.g. success rate) in the environment after fine-tuning with a minimum amount of action-labeled data. The commonly considered ratio of labeled to unlabeled data is around 2 _−_ 10% in the existing 

work (Zheng et al., 2023; Nikulin et al., 2025), while in our experiments, we consider a ratio as low as _<_ 1%. 

**Promptable representations.** We follow the Chen et al. (2024a) and define promptable representations _simply as a process of obtaining observation embeddings from the VLMs given a task-specific prompt and some extraction and aggregation strategy_ (see Figure 2). We obtain such representations from the last and next-to-last layers (Chen et al., 2024a). In contrast to the Chen et al. (2024a); Huang et al. (2025) we cannot learn pooling from the data to better predict true actions or obtain better reward. Thus, we experiment only with simple fixed strategies, such as taking the mean over all output embeddings or taking only the embedding of the last token from either prompt or the generated answer. Thus, the final promptable representations of an observation _ot_ is always just a single vector _st ∈ R_<sup>_D_</sup> , where _D_ is a VLMs hidden size. 

**Latent action models.** Given the dataset of observations _D_ := _{_ ( _o_<sup>_n_</sup> _i_<sup>)</sup><sup>_}τ_</sup> _i_ =1<sup>, LAMs (Rybkin et al., 2018; Edwards et al.,</sup> 2019; Schmidt & Jiang, 2023) try to infer latent actions _zt_ such that they are maximally predictive of observed transitions ( _ot, ot_ +1) while being minimal (Schmidt & Jiang, 2023), i.e. describe changes only relevant to control. After pre-training, LAM is used to supply latent actions for behavioral cloning (BC) on unlabeled dataset to obtain useful behavioral priors. As a final stage, decoder is trained to map from latent to ground-truth actions on a small labeled dataset. 

Modern LAMs (Bruce et al., 2024; Ye et al., 2024; Cui et al., 2024; Chen et al., 2024c;b; Gao et al., 2025) mostly follow the same high-level architecture introduced by LAPO (Schmidt & Jiang, 2023), which uses a combination of inverse (IDM) and forward (FDM) dynamics models to infer latent actions. Given a transition ( _ot, ot_ +1), IDM first infers latent action _zt ∼ f_ IDM( _·|ot, ot_ +1), which FDM further uses to predict the next observation ˆ _ot_ +1 _∼ f_ FDM( _·|ot, zt_ ). Both models are trained jointly to minimize the loss _L_ MSE = . E( _ot,ot_ +1) _∼D_ � _∥f_ FDM( _f_ IDM( **_o_** _t,_ **_o_** _t_ +1) _,_ **_o_** _t_ ) _−_ **_o_** _t_ +1 _∥_<sup>2�</sup> 

2 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 3._ Visualization of observations with and without distractors in our modification of MetaWorld environment. 

To avoid shortcut learning, i.e. IDM just passing _ot_ +1 as is, the information bottleneck is usually applied to latent actions, with quantization via VQ-VAE (Van Den Oord et al., 2017) as a popular choice (Schmidt & Jiang, 2023; Bruce et al., 2024; Chen et al., 2024c). There is, however, growing evidence that quantization is harmful (Nikulin et al., 2025; Liang et al., 2025; Yang et al., 2025b) and simply restricting dimensionality is enough. 

# **3. Related Work** 

**Latent action learning.** Edwards et al. (2019) was among the first to introduce the problem of recovering latent actions, demonstrating limited success on simple tasks. LAPO (Schmidt & Jiang, 2023) substantially simplified the approach, eliminated key scalability barriers, and achieved high success in the challenging, procedurally generated tasks, helping to popularize LAMs. Subsequent work further scaled latent action learning to larger models and datasets, and to increasingly complex and diverse robotics domains (Bruce et al., 2024; Cui et al., 2024; Ye et al., 2024; Chen et al., 2024c;b; Jang et al., 2025; Bjorck et al., 2025). 

Recent studies (Nikulin et al., 2025; Klepach et al., 2025; Zhang et al., 2025) have highlighted the failure of LAMs in the presence of action-correlated distractors. Both Nikulin et al. (2025) and Zhang et al. (2025) proposed incorporating supervision from a small number of true actions during LAM training to help identify controllable changes. While this approach is effective, it is not generalizable, since in many domains, such as egocentric human videos (Yang et al., 2025c), true actions cannot be obtained in a practical manner. In contrast, we propose leveraging promptable representations from VLMs as an unsupervised approach to separate controllable changes from noise. We empirically demonstrate that, without any supervision, this enables LAMs to recover the performance in the presence of distractors (see Figure 1). 

The work most closely related to ours is UniVLA (Bu et al., 2025b), which also focuses on task-centric latent actions. UniVLA uses DINOv2 features, which are intended to provide priors that better capture task-relevant information. In 

addition, it proposes a two-stage LAM training pipeline that incorporates language task instruction embeddings as inputs to the LAM in the first stage. However, UniVLA design has important limitations. While conditioning the LAM on task instructions may help separate task-relevant videos from noise at a high level, it does not provide the per-step learning signal required to accurately recover lowlevel ground-truth actions. As a result, in the single-task learning setting the task instruction remains a constant vector, and UniVLA effectively reduces to LAPO, leading to noisy latent actions. In contrast, we provide the task instruction to the VLM, and while the instruction itself is constant, the VLM produces different language-conditioned representations for each observation, which LAM can use as prediction targets (see Figure 2). Thus, our approach is simpler, does not require multiple stages, provides clean targets at each step, and remains effective in the single-task regime, significantly outperforming UniVLA (see Section 7) and DINOv2 (see Section 6). 

**Promptable representations.** Recently, Chen et al. (2024a) proposed using VLM embeddings generated with taskspecific prompts to extract improved state representations, which enhance sample efficiency in online reinforcement learning. Our work is heavily inspired by this approach, and we closely follow their methodology for extracting promptable representations. Our contribution, however, is a new setting and novel empirical insights. Results of Chen et al. (2024a) do not guarantee the minimality of representations and, as a consequence, success in latent action learning. In contrast, our work shows that VLMs differ substantially in their zero-shot suitability for LAMs, and that selecting an appropriate VLM can make LAMs effective in the presence of distractors, increasing success rates by up to sixfold, a result that has not been documented in prior work. 

# **4. Experimental Setup** 

**Environments and datasets.** We use MetaWorld (Yu et al., 2020) Multi-Task 10 (MT10) as our primary benchmark, as it allows us to conduct experiments in controlled setting while being lightweight enough for exhaustive experimentation with VLMs under limited resources. We modify MetaWorld to include distracting videos in the background, using the DAVIS (Pont-Tuset et al., 2017) videos, which depict different real world scenes, including humans. We also move the default camera position farther back and remove borders around the table to include more of the background video in the observation, making latent action learning more challenging. See Figure 3 for a visualization. 

We follow the standard three-stage pipeline (Schmidt & Jiang, 2023; Ye et al., 2024; Nikulin et al., 2025): (1) pretrain the LAM, (2) train behavioral cloning (BC) agent on latent actions, and (3) train a decoder head on a small num- 

3 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 4._ Demonstration that quality of latent actions learned by LAPO completely degrades in the presence of distractors, which results in almost zero success rate. We show that with the ideal target for FDM, which perfectly disentangles controllable features from the noise, performance may be restored, serving as a main motivation for us to explore promptable representations. Action probe represents MSE of a linear probe trained to predict real actions from latent actions. See Section 4 for detailed explanation. We use three random seeds and report IQM and 95%-CI based on stratified bootstrapping, following the Agarwal et al. (2021). See Section 5 for details. 


_Figure 5._ Baseline LAPO action probes on MT10. Averaged over 3 random seeds. Action probe represents MSE of a linear probe trained to predict real actions from latent actions. See Section 4 for detailed explanation. 

ber of true-action labels. For each task, we collect 5k trajectories from the scripted experts provided by MetaWorld and up to 16 additional labeled trajectories for the final stage, which is less than 1% of the full datasets. 

**Latent action model architecture.** We use the architecture proposed by Schmidt & Jiang (2023), omitting action quantization (Nikulin et al., 2025; Liang et al., 2025; Yang et al., 2025b). We use frame stacking, but only in IDM, while FDM uses only the current frame and latent action to predict the next frame, as in Chen et al. (2024b). Other than that, in our main experiments, we do not use any improvements upon LAPO (unless explicitly stated otherwise), such as augmentations or multi-step predictions in FDM (Nikulin et al., 2025; Chen et al., 2024b; Ye et al., 2024; Cui et al., 2024), to eliminate possible confounders on latent action quality. We use ResNet (He et al., 2016) or ViT (Dosovitskiy, 2020) as IDM and FDM backbones. When predicting in the latent space instead of images, we follow Nikulin et al. (2025) and use multiple MLP blocks similar to those used in Transformers (Vaswani et al., 2017). For action decoder head, we use a small three-layer MLP. For actor itself, we always used ResNet (He et al., 2016). For hyperparameters 

## see Section D in the Appendix. 

**Evaluation.** For evaluation we use **action probe** and **success rate** . Specifically, we train linear probes to predict real actions from the latent ones during LAM training, while stopping the gradient through the latent actions. The final MSE serves as our quality metric, as it indicates whether the latent actions encode the real ones. This metric is also used for hyperparameter tuning, which may be impractical in realworld settings but allows us to estimate the upper-bound performance of each method for fair comparison. 

However, as Nikulin et al. (2025) notes, linear probing has a key limitation: it can reveal whether true actions are present in the latent space, but it does not guarantee minimality, meaning that exogenous noise may still be encoded. Thus, to measure the true usefulness of pretraining with latent actions, we evaluate the success rate in the environments after fine-tuning on true action labels. 

# **5. The Importance of Right Target** 

We begin with a simple demonstration that the limitation of LAMs in the presence of distractors arises entirely from the poor FDM target (e.g. next frame in pixel space), rather than from flaws in the overall idea or architecture. By construction, latent actions are optimized to maximally explain the dynamics. Therefore, the root of the failure to recover true actions lies in the dynamics we predict, which is directly determined by the target in FDM: _o_ ˆ _t_ +1 _∼ f_ FDM( _·|ot, zt_ ). What would be the ideal target for FDM? And if it exists, what would be the final performance? Could LAM possibly recover the ground-truth actions despite distractors in the input observations? 

**Setup.** To answer these questions we construct a special dataset with twin observations for each task: during data 

4 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 6._ Benchmarking the effectiveness of promptable representations provided by different VLMs for latent action learning on all tasks from MT10. Action probe represents MSE of a linear probe trained to predict real actions from latent actions. See Section 4 for detailed explanation. Overall, all VLMs provide some improvement over LAPO, with Molmo performing the best and Gemma-3 the worst. For details and exact experimental protocol see Section 6. We additionally provide the ranking for each combination of hyperparameters in the Figure 15 in the Section B. 

collection we render and save same observation with and without distractors. Next, during training we feed observations with distractors as inputs to IDM and FDM, but as the target for FDM we use next observation without distractors. As the actual controllable changes are preserved (the underlying state is the true next state), it serves as a target with ideal disentanglement of controllable features from exogenous noise (see Figure 3). To show that existing limitations are agnostic to the architecture of FDM and IDM, we explore both ResNet (Schmidt & Jiang, 2023) and transformer (Bruce et al., 2024; Ye et al., 2024) backbones. 

**Results.** First of all, as can be seen in Figure 5, we confirm that simply adding distractors results in complete degradation of latent actions quality regardless of backbone used. This subsequently leads to almost zero success rate after fine-tuning on true actions (see Figure 4c). Ideally, probes should be close to each other, as real underlying actions are identical between both settings. Next, in Figures 4a and 4b we show the effect of using perfect targets during LAPO training (with -Twin postfix). To better illustrate the trend, in Figure 4a we report the ratio of probes with and without distractors for each method. With the ideal target action probes immediately drop to the level of LAPO without distractors, and ratio converges to one. Finally, improvement in latent action quality directly results in leveling success rates (see Figure 4c). Overall, this result supports that the right target is the key to unlock latent action learning in the presence of distractors. Although these experiments may seem obvious in hindsight, they allow us to convey a key empirical observation, one that provides the same intuition 

that originally led us to explore promptable representations. 

# **6. The Promise of Promptable Representations** 

Our main hypothesis is that representations provided by VLMs can serve as an effective, unsupervised way to disentangle controllable features from the noise. As we demonstrated in the previous section, it would be enough to unlock latent action learning in the presence of distractors. 

Modern VLMs easily identify the robotic arm location in the image (like Figure 3) and describe it in detail, even in the presence of background noise. However, the ability to generate valid text does not necessarily imply that the underlying embeddings are suitable for our purposes. For a representation to serve as an effective target for LAM, it should (1) contain task-centric visual information, (2) be minimal by filtering out visual details irrelevant to the prompt, and (3) remain consistent across observations to mimic changes caused by real actions. Unfortunately, current VLMs are known to struggle with visual focus (Rahmanzadehgervi et al., 2024; Sim et al., 2025) and pixel-level understanding (Gou et al., 2024; Dahou et al., 2025; Li et al., 2025). Given these limitations, we begin by benchmarking a wide variety of modern VLMs to assess their viability. As a baseline, we included representations from self-supervised methods such as CLIP (Radford et al., 2021) and DINOv2 (Oquab et al., 2023), which are not promptable but were pre-trained on large amounts of visual data. Based on this benchmark, we then select the most effective VLM along with the best hyperparameters (e.g., prompt, aggregation strategy, and 

5 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

## others). 

**Setup.** Conducting large scale VLMs evaluation on the full datasets would be prohibitively expensive. Instead, we train LAPO+VLM on a small subsets of 64 trajectories instead of full 5k for each dataset and measure the resulting latent action quality. As we will show in Section 7, hyperparameter rankings obtained this way transfer reasonably well to the full dataset performance. For each VLM, we evaluated eight prompt variants designed in different styles to exploit diverse VLM capabilities (e.g., CLIP-style captions, pointing, segmentation; see Table 1 in Section C). We further varied the source of representations (last vs. next-to-last layer, prompt vs. generated embeddings) and the aggregation strategy (averaging vs. last non-padding token). This yields 64 runs per VLM, per task, per dataset. The full list of VLMs, including exact model names, sizes, and prompt templates, is provided in Section C. 

**Benchmarking VLMs.** We summarize our main benchmarking results in Figure 6 and provide full perhyperparameter rankings in Figure 15 (Section B). As can be seen in Figure 6a, overall all VLMs provide some degree of improvement over LAPO in terms of the median action probe. However, some of them, especially Molmo (Deitke et al., 2025), are generally preferable and have lower variance, indicating higher robustness to different hyperparameters. In Figure 6b we visualize ranking by averaging best scores for each task. While this changes ranking a bit, we still observe that among VLMs Gemma-3 (Team et al., 2025) is the worst and Molmo (Deitke et al., 2025) is consistently the best. Based on Figure 15, we observe that in general, promptable representations aggregated by averaging next-to-last layer prompt embeddings perform the best. From a practical standpoint, this is beneficial, as it eliminates the additional time for answer generation. Ironically, the best prompt is _Do not describe background features. Focus on the robot arm and the [task-obj]_ , which explicitly asks VLM to filter out distractors. 

This brings us to a striking conclusion that state-of-the-art VLMs do not necessarily provide better promptable representations. For example, InstructBLIP (Dai et al., 2023) outperforms both Gemma-3 (Team et al., 2025) and Pixtral (Agrawal et al., 2024), despite being considerably older. Furthermore, Cosmos-Reason (Azzolini et al., 2025) results indicate that explicit fine-tuning on robotics data is not sufficient to guarantee improved representations. We believe that our results, besides relevance to LAMs, reveal a large blind spot in how VLMs are currently evaluated, with critical implications for robotics and VLA models. 

In addition, DINOv2 and CLIP (see Figure 6) results highlight the vital importance of language conditioning. Due to large-scale pretraining both may possess helpful inductive biases, for example by attending to moving objects, but with- 

out language conditioning there is no guarantee that these objects are the ones that are controllable. Both methods achieve the worst latent action quality among all approaches we considered. For instance, OTTER (Huang et al., 2025) uses the same CLIP model but applies simple training-free filtering using text CLIP embeddings. This small modification significantly improves latent action quality, although still not to the level of VLMs such as Molmo. 

**Benchmarking embedding VLMs.** In our main benchmark (see Figure 6), we evaluated conventional VLMs, which were not explicitly trained to produce strong unified representations and therefore required heuristics such as embedding pooling. Recently, a new class of embedding VLMs has emerged (Jiang et al., 2024b; Meng et al., 2025). These models are designed specifically to learn high-quality, promptable, and multimodal embeddings for zero-shot retrieval. Given the similarity of their objective to ours, one might expect them to perform better. To test this, we evaluated three recent state-of-the-art models (Jiang et al., 2024a; Meng et al., 2025; Gu et al., 2025) using the same protocol as earlier, but separately as they require different prompt formats. As can be seen in Figure 7, such models do not deliver any substantial gains. In fact, VLM2Vec-V2 (Meng et al., 2025), best model in its class, performed worse than Gemma-3, which was the weakest model in the main benchmark, and none of the models surpassed Molmo. Our results indicate that embedding VLMs do not actually encode only prompt-specific visual information into the embeddings and fail to deliver the anticipated benefits for our use case. 

**Why does Molmo perform so well?** Given Molmo’s strong performance, it is natural to ask what drives its improved representations. Directly answering this is difficult, but we can gather indirect evidence suggesting that the gains stem primarily from pre-training data rather than from the specific architecture. Fortunately, Molmo provides two variants: Molmo-D, which uses Qwen2 as its backbone (Yang et al., 2025a), and Molmo-O, which uses OLMo (Groeneveld et al., 2024), while both employ CLIP (Radford et al., 2021) as the vision encoder. In contrast, Qwen2-VL (Wang et al., 2024) does not use CLIP, offering a useful comparison point to disentangle architectural effects. In Figure 8 we show that CLIP alone performs the worst, Molmo-O ranks second after Molmo-D, and Qwen2-VL performs worse still. Since the Molmo variants share the same pre-training data but differ in backbone architecture, we conclude that the likely source of their superior performance lies in the data rather than the architecture. A further hypothesis is that Molmo’s advantage may come from its visual pointing abilities, but this seems unlikely since Moondream-2 also has this ability yet performs worse. 

6 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 7._ Benchmarking the effectiveness of promptable representations provided by recent _embedding_ VLMs for latent action learning on all tasks from MT10. Overall, embedding VLMs, despite their promise, do not deliver any substantial gains compared to traditional VLMs, such as Molmo. We include Gemma-3 and Molmo results here for convineince. 


_Figure 8._ Molmo performance investigation, using aggregation over the best hyperparameters. We benchmark both Molmo versions, which both use CLIP but differ in LLM backbones (OLMo vs Qwen2), as well as Qwen2-VL. Since both Molmo share the pre-training data but differ in architecture, we conclude that the likely source of their superior performance lies in the data. 


_Figure 9._ Action probes comparison for LAPO, baselines and LAPO with promptable representations on full datasets for all tasks in MT10. Results are averaged over three random seeds. As can be seen, promptable representations significantly improves upon LAPO in terms of the latent actions quality, and without any supervision with true actions closes the gap with LAPO without distractors. While all VLMs bring improvements, Molmo achieve best results overall, especially given it high robustness to hyperparameter choices (see Figure 6a). UniVLA uses two-stage pipeline, each half of total epochs and we visualize the second stage, where task-centric latent actions should be learned. For resulting success rates see Figure 10. We provide per-environment probes in Figure 14, Section B. 

# **7. Promptable Representations Unlock Task-Centric Latent Actions** 

**Setup.** Based on the benchmark results, we selected multiple VLMs for further experiments: Phi-4, Molmo and GraspMolmo. Although all of them achieved improvements in latent action quality upon LAPO on small datasets, it remains necessary to validate whether this performance transfers to the full 5k datasets and yields improved success rates, as this is not guaranteed (Nikulin et al., 2025). We chose the best hyperparameters for each VLM and trained LAPO+VLM on the full datasets, using three random seeds. As specified in Section 4 we used 16 labeled trajectories with ground-truth actions for final fine-tuning. See Section D for hyperparameters. 

**Baselines.** As our primary baselines, we additionally evaluated OTTER (Huang et al., 2025) and UniVLA (Bu et al., 

2025b). We note, however, that we are not competing with the VLAs proposed in these works. For UniVLA, we reimplemented their proposed two-stage task-centric LAM training pipeline using our transformer backbone and task instructions provided by MetaWorld (Yu et al., 2020), which we encoded by a pretrained T5 text encoder (Raffel et al., 2020). For OTTER, we adopted their CLIP training-free text-aware visual feature extraction approach to construct a target for FDM in LAPO. All stages other than latent action learning are unified (e.g. share BC actor architecture) across all considered methods to ensure a fair comparison. 

**Results.** We present the resulting action probes in Figure 9 and the final success rates after fine-tuning on real actions in Figure 10. As shown in Figure 9, LAPO with promptable representations achieves a substantial improvement in latent action quality, both with and without distractors. 

7 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 10._ Success rate on MT10 for LAPO and LAPO+VLMs, which uses promptable representations. We use three random seeds and report IQM and 95%-CI based on stratified bootstrapping, following the Agarwal et al. (2021). 

In the presence of distractors, it nearly closes the gap to LAPO trained without distractors, and without distractors, it slightly outperforms it (e.g., Molmo). 

Among the baselines, only UniVLA does not show any improvement in the presence of distractors. As we discussed in Section 3, UniVLA adds a language task instruction embedding to the IDM and FDM inputs, which may help disentangle task-relevant videos from noise at a high level but does not provide the per-step learning signal required to accurately recover low-level ground-truth actions. As a result, during single-task learning the task instruction remains a constant vector, and UniVLA effectively reduces to LAPO. 

Crucially, the improvement in action probes on full datasets carries over to downstream performance (see Figure 10): success rates increase by a factor of six at max in the presence of distractors, while remaining almost unchanged without them. Interestingly, we found Phi-4 to outperform GraspMolmo, despite having worse probes on small datasets. On full datasets (Figure 9), however, Phi-4 is better. This indicates, that while results from a small dataset may carry over to a larger one with some error, probes on the full dataset predict the final success rate with high accuracy. Overall, our results confirm the viability of promptable representations as a clean target for latent action modeling in the presence of distractors. 

**Varying the latent action information bottleneck.** In all previous experiments, we fixed the latent action dimension to 128 to ensure a consistent level of latent action minimality across all methods. However, this choice was inherited from LAPO and may not be optimal. Moreover, as shown by LAPA (Ye et al., 2024), smaller latent action spaces make the perception-and-language-to-action generation problem 


_Figure 11._ Success rate on MT10 for LAPO and LAPO+Molmo, with varying latent action dimension to control the information bottleneck. We use three random seeds and report IQM and 95%CI based on stratified bootstrapping, following the Agarwal et al. (2021). 

significantly easier to learn. We therefore conducted additional experiments that vary the latent action dimension, using the full datasets and three random seeds. The results are summarized in Figure 11. We observe that promptable representations not only increase success rates in the presence of distractors, but also significantly outperform LAPO without distractors under stronger minimality constraints, such as 16 action dimensions. These results provide further evidence that VLMs help filter out information irrelevant to controllable changes, enabling a more compact latent action space. 

# **8. Conclusion** 

In this work, we demonstrated that promptable representations provided by Vision-Language Models can effectively filter out action-correlated distractors, enabling task-centric latent actions. Our experiments on the Distracting MetaWorld benchmark confirmed that using task-centric promptable representations as targets for LAPO substantially improves both latent action quality and downstream success rates. We hope that our results will inspire the community to explore promptable representations at scale for the next generation of Vision-Language-Action models. We discuss the limitations of our work in the Section A. 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

8 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

# **References** 

- Agarwal, R., Schwarzer, M., Castro, P. S., Courville, A. C., and Bellemare, M. Deep reinforcement learning at the edge of the statistical precipice. _Advances in neural information processing systems_ , 34:29304–29320, 2021. 

- Agrawal, P., Antoniak, S., Hanna, E. B., Bout, B., Chaplot, D., Chudnovsky, J., Costa, D., De Monicault, B., Garg, S., Gervet, T., et al. Pixtral 12b. _arXiv preprint arXiv:2410.07073_ , 2024. 

- Azzolini, A., Bai, J., Brandon, H., Cao, J., Chattopadhyay, P., Chen, H., Chu, J., Cui, Y., Diamond, J., Ding, Y., et al. Cosmos-reason1: From physical common sense to embodied reasoning. _arXiv preprint arXiv:2503.15558_ , 2025. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Bruce, J., Dennis, M. D., Edwards, A., Parker-Holder, J., Shi, Y., Hughes, E., Lai, M., Mavalankar, A., Steigerwald, R., Apps, C., et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025a. 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with taskcentric latent actions, 2025b. URL https://arxiv. org/abs/2505.06111. 

- Chen, W., Mees, O., Kumar, A., and Levine, S. Visionlanguage models provide promptable representations for reinforcement learning. _arXiv preprint arXiv:2402.02651_ , 2024a. 

- Chen, X., Guo, J., He, T., Zhang, C., Zhang, P., Yang, D. C., Zhao, L., and Bian, J. Igor: Image-goal representations are the atomic control units for foundation models in embodied ai. _arXiv preprint arXiv:2411.00785_ , 2024b. 

- Chen, Y., Ge, Y., Li, Y., Ge, Y., Ding, M., Shan, Y., and Liu, X. Moto: Latent motion token as the bridging language for robot manipulation. _arXiv preprint arXiv:2412.04445_ , 2024c. 

- Cui, Z. J., Pan, H., Iyer, A., Haldar, S., and Pinto, L. Dynamo: In-domain dynamics pretraining for visuo-motor control. _arXiv preprint arXiv:2409.12192_ , 2024. 

- Dahou, Y., Huynh, N. D., Le-Khac, P. H., Para, W. R., Singh, A., and Narayan, S. Vision-language models can’t see the obvious. _arXiv preprint arXiv:2507.04741_ , 2025. 

- Dai, W., Li, J., Li, D., Tiong, A., Zhao, J., Wang, W., Li, B., Fung, P. N., and Hoi, S. Instructblip: Towards generalpurpose vision-language models with instruction tuning. _Advances in neural information processing systems_ , 36: 49250–49267, 2023. 

- Deitke, M., Clark, C., Lee, S., Tripathi, R., Yang, Y., Park, J. S., Salehi, M., Muennighoff, N., Lo, K., Soldaini, L., et al. Molmo and pixmo: Open weights and open data for state-of-the-art vision-language models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 91–104, 2025. 

- Dosovitskiy, A. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ , 2020. 

- Edwards, A., Sahni, H., Schroecker, Y., and Isbell, C. Imitating latent policies from observation. In _International conference on machine learning_ , pp. 1755–1763. PMLR, 2019. 

- Gao, S., Zhou, S., Du, Y., Zhang, J., and Gan, C. Adaworld: Learning adaptable world models with latent actions. _arXiv preprint arXiv:2503.18938_ , 2025. 

- Gou, C., Felemban, A., Khan, F. F., Zhu, D., Cai, J., Rezatofighi, H., and Elhoseiny, M. How well can vision language models see image details? _arXiv preprint arXiv:2408.03940_ , 2024. 

- Groeneveld, D., Beltagy, I., Walsh, P., Bhagia, A., Kinney, R., Tafjord, O., Jha, A. H., Ivison, H., Magnusson, I., Wang, Y., et al. Olmo: Accelerating the science of language models. _arXiv preprint arXiv:2402.00838_ , 2024. 

- Gu, T., Yang, K., Feng, Z., Wang, X., Zhang, Y., Long, D., Chen, Y., Cai, W., and Deng, J. Breaking the modality barrier: Universal embedding learning with multimodal llms. _arXiv preprint arXiv:2504.17432_ , 2025. 

- He, K., Zhang, X., Ren, S., and Sun, J. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 770–778, 2016. 

- Huang, H., Liu, F., Fu, L., Wu, T., Mukadam, M., Malik, J., Goldberg, K., and Abbeel, P. Otter: A vision-languageaction model with text-aware visual feature extraction. _arXiv preprint arXiv:2503.03734_ , 2025. 

- Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.-C., et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

9 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

- Jiang, T., Song, M., Zhang, Z., Huang, H., Deng, W., Sun, F., Zhang, Q., Wang, D., and Zhuang, F. E5-v: Universal embeddings with multimodal large language models. _arXiv preprint arXiv:2407.12580_ , 2024a. 

- Jiang, Z., Meng, R., Yang, X., Yavuz, S., Zhou, Y., and Chen, W. Vlm2vec: Training vision-language models for massive multimodal embedding tasks. _arXiv preprint arXiv:2410.05160_ , 2024b. 

- Klepach, A., Nikulin, A., Zisman, I., Tarasov, D., Derevyagin, A., Polubarov, A., Lyubaykin, N., and Kurenkov, V. Object-centric latent action learning. _arXiv preprint arXiv:2502.09680_ , 2025. 

- Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C. H., Gonzalez, J., Zhang, H., and Stoica, I. Efficient memory management for large language model serving with pagedattention. In _Proceedings of the 29th symposium on operating systems principles_ , pp. 611–626, 2023. 

- Li, W., Tang, R., Li, C., Zhang, C., Vulic, I., and Søgaard, A.´ Lost in embeddings: Information loss in vision-language models. _arXiv preprint arXiv:2509.11986_ , 2025. 

- Liang, A., Czempin, P., Hong, M., Zhou, Y., Biyik, E., and Tu, S. Clam: Continuous latent action models for robot learning from unlabeled demonstrations. _arXiv preprint arXiv:2505.04999_ , 2025. 

- Liu, Y., Gupta, A., Abbeel, P., and Levine, S. Imitation from observation: Learning to imitate behaviors from raw video via context translation. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pp. 1118– 1125. IEEE, 2018. 

- McCarthy, R., Tan, D. C., Schmidt, D., Acero, F., Herr, N., Du, Y., Thuruthel, T. G., and Li, Z. Towards generalist robot learning from internet video: A survey. _Journal of Artificial Intelligence Research_ , 83, 2025. 

- Meng, R., Jiang, Z., Liu, Y., Su, M., Yang, X., Fu, Y., Qin, C., Chen, Z., Xu, R., Xiong, C., et al. Vlm2vec-v2: Advancing multimodal embedding for videos, images, and visual documents. _arXiv preprint arXiv:2507.04590_ , 2025. 

- Nikulin, A., Zisman, I., Tarasov, D., Lyubaykin, N., Polubarov, A., Kiselev, I., and Kurenkov, V. Latent action learning requires supervision in the presence of distractors. _arXiv preprint arXiv:2502.00379_ , 2025. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., ElNouby, A., et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. 

- Pont-Tuset, J., Perazzi, F., Caelles, S., Arbelaez, P., Sorkine-´ Hornung, A., and Van Gool, L. The 2017 davis challenge on video object segmentation. _arXiv preprint arXiv:1704.00675_ , 2017. 

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pp. 8748–8763. PmLR, 2021. 

- Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., and Liu, P. J. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of Machine Learning Research_ , 21(140):1–67, 2020. URL http://jmlr. org/papers/v21/20-074.html. 

- Rahmanzadehgervi, P., Bolton, L., Taesiri, M. R., and Nguyen, A. T. Vision language models are blind: Failing to translate detailed visual features into words. _arXiv preprint arXiv:2407.06581_ , 2024. 

- Rybkin, O., Pertsch, K., Derpanis, K. G., Daniilidis, K., and Jaegle, A. Learning what you can do before doing anything. _arXiv preprint arXiv:1806.09655_ , 2018. 

- Schmidt, D. and Jiang, M. Learning to act without actions. _arXiv preprint arXiv:2312.10812_ , 2023. 

- Sim, M. Y., Zhang, W. E., Dai, X., and Fang, B. Can VLMs actually see and read? a survey on modality collapse in vision-language models. In Che, W., Nabende, J., Shutova, E., and Pilehvar, M. T. (eds.), _Findings of the Association for Computational Linguistics: ACL 2025_ , pp. 24452–24470, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 9798-89176-256-5. doi: 10.18653/v1/2025.findings-acl. 1256. URL https://aclanthology.org/2025. findings-acl.1256/. 

- Team, G., Kamath, A., Ferret, J., Pathak, S., Vieillard, N., Merhej, R., Perrin, S., Matejovicova, T., Rame, A.,´ Riviere,` M., et al. Gemma 3 technical report. _arXiv preprint arXiv:2503.19786_ , 2025. 

- Torabi, F., Warnell, G., and Stone, P. Recent advances in imitation learning from observation. _arXiv preprint arXiv:1905.13566_ , 2019. 

10 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

- Van Den Oord, A., Vinyals, O., et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Wang, P., Bai, S., Tan, S., Wang, S., Fan, Z., Bai, J., Chen, K., Liu, X., Wang, J., Ge, W., et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

- Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025a. 

- Yang, J., Shi, Y., Zhu, H., Liu, M., Ma, K., Wang, Y., Wu, G., He, T., and Wang, L. Como: Learning continuous latent motion from internet videos for scalable robot learning. _arXiv preprint arXiv:2505.17006_ , 2025b. 

- Yang, R., Yu, Q., Wu, Y., Yan, R., Li, B., Cheng, A.-C., Zou, X., Fang, Y., Yin, H., Liu, S., et al. Egovla: Learning vision-language-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ , 2025c. 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 

- Yu, T., Quillen, D., He, Z., Julian, R., Hausman, K., Finn, C., and Levine, S. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pp. 1094–1100. PMLR, 2020. 

- Yuan, H., Li, X., Zhang, T., Huang, Z., Xu, S., Ji, S., Tong, Y., Qi, L., Feng, J., and Yang, M.-H. Sa2va: Marrying sam2 with llava for dense grounded understanding of images and videos. _arXiv preprint arXiv:2501.04001_ , 2025. 

- Zhang, C., Pearce, T., Zhang, P., Wang, K., Chen, X., Shen, W., Zhao, L., and Bian, J. What do latent action models actually learn? _arXiv preprint arXiv:2506.15691_ , 2025. 

- Zheng, Q., Henaff, M., Amos, B., and Grover, A. Semisupervised offline reinforcement learning with actionfree trajectories. In _International conference on machine learning_ , pp. 42339–42362. PMLR, 2023. 

- Zhong, Y., Bai, F., Cai, S., Huang, X., Chen, Z., Zhang, X., Wang, Y., Guo, S., Guan, T., Lui, K. N., et al. A survey on vision-language-action models: An action tokenization perspective. _arXiv preprint arXiv:2507.01925_ , 2025. 

11 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

# **A. Discussion and Limitations** 

**Segmentation, while simple, is not enough.** The concept of extracting VLM embeddings with the hope that they will filter out distractors may initially seem strange. If the goal is to filter out distractors, would not it be more straightforward to simply segment the relevant parts and train LAPO directly in image space using masks? In fact, our benchmark includes VLMs capable of segmentation, such as Sa2VA (Yuan et al., 2025), and we even utilize such prompts (see Table 1), yet we still rely on embeddings instead of masks. While segmentation is appealing, it does not address the fundamental problem. Consider a scenario with a robotic arm and varying lighting conditions. Even if we segment the arm, we will still get changes in our observations that are not related to the actual actions, such as color shifts and reflections on the arm. The same issue arises with camera movement and changes in perspective. The key, therefore, is to work in a semantic latent space, which is where the common-sense reasoning capabilities of VLMs become crucial. 

**On the choice of MetaWorld benchmark.** One notable limitation of our study is its small scale, as we rely on MetaWorld as our primary benchmark and do not extend our analysis to large VLAs and datasets, such as Open-X (O’Neill et al., 2024). However, this choice is deliberate for two reasons. First, while MetaWorld is simple, with distractors, it is difficult enough to completely break traditional LAMs and to distinguish different VLMs in terms of the promptable representations’ quality (as we demonstrate in Section 6). As an early exploration, it was crucial to expand in variety (e.g., exploring more VLMs) within our limited resources. We hope that our analysis provides practitioners with valuable insights into the available options. Second, encoding entire datasets is both expensive and time-consuming, as it involves inference with large VLMs (e.g., 8B parameters) and generating answers. For our 5k trajectory datasets, the process can quickly exceed 24 hours, let alone for truly large datasets. Since this is purely inference and gradients are not required, the process can be significantly accelerated, for example, using vLLM (Kwon et al., 2023). However, we have left this as future work. 

12 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

# **B. Additional Figures** 


_Figure 12._ Aggregation over all hyperparameters for each task in MT10. 

13 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 13._ Probe values for best hyperparameters for each task in MT10. 

14 

**Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 14._ Action probes comparison for LAPO and LAPO+VLMs on full datasets for all tasks in MT10. Results are averaged over three random seeds. As can be seen, LAPO+VLM significantly improves upon LAPO in terms of the latent actions quality, and without any supervision with true actions closes the gap with LAPO without distractors. While all VLMs bring improvements, Molmo achieve best results overall. For resulting success rates see Figure 10 

15 

### **Vision-Language Models Unlock Task-Centric Latent Actions** 


_Figure 15._ Action probe rankings across all explored hyperparameter combinations. Smaller probe is better. Values are averaged over all VLMs, tasks and settings, e.g. with and without distractors. Hyperparameters in order: prompt, layer, reduction type and source of the embeddings. Feel free to zoom in! 


_Figure 16._ Action probes ranking for all combinations of hyperparameters explored for Molmo VLM. Values are averaged over all tasks and settings, e.g. with and without distractors. 

16 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

# **C. Vision-Language Models Details** 

_Table 1._ Prompt templates used in our experiments. We adapt them to each task by inserting information relevant to the task. All VLMs explored share the same prompts per task. 

## **Prompt** 

The robot task is to [task]. Briefly, what is the next logical action for the robotic arm? Do not describe background features. Focus on the robot arm and the [task-obj]. Do you see a robot gripper? Is there [task-obj] and a robot in the image? Robot [doing task] on a table. Point to the robotic arm gripper. Point to where I should grasp to accomplish the following task - [task]. Segment a robot. 

17 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

_Table 2._ Exact HuggingFace IDs for all VLMs we used. We shortened their names in Figures to save some space. 

|**Name**|**HuggingFace ID**|
|---|---|
|InstructBLIP|Salesforce/instructblip-vicuna-7b|
|Molmo|allenai/Molmo-7B-D-0924|
|Gemma-3|google/gemma-3-12b-it|
|Llama-3.2|unsloth/Llama-3.2-11B-Vision-Instruct|
|Qwen2.5-VL|Qwen/Qwen2.5-VL-7B-Instruct|
|InternVL3|OpenGVLab/InternVL3-8B|
|Cosmos-Reason|nvidia/Cosmos-Reason1-7B|
|Phi-4|microsoft/Phi-4-multimodal-instruct|
|LLaVA-OneVision|llava-hf/llava-onevision-qwen2-7b-ov-hf|
|SmolVLM|HuggingFaceTB/SmolVLM2-2.2B-Instruct|
|Pixtral|mistral-community/pixtral-12b|
|GraspMolmo|allenai/GraspMolmo|
|Qwen2-VL|Qwen/Qwen2-VL-7B-Instruct|
|Phi-3.5|Lexius/Phi-3.5-vision-instruct|
|LLaVA-NeXT|llava-hf/llava-v1.6-mistral-7b-hf|
|Aya-Vision|CohereLabs/aya-vision-8b|
|MiMo-VL|XiaomiMiMo/MiMo-VL-7B-RL|
|Molmo-O|allenai/Molmo-7B-O-0924|
|SAIL|ByteDance-Seed/SAIL-7B|
|Moondream-2|vikhyatk/moondream2|
|VLM2Vec|VLM2Vec/VLM2Vec-V2.0|
|UniME|DeepGlint-AI/UniME-LLaVA-1.6-7B|
|E5-V|royokong/e5-v|
|Janus-Pro|deepseek-community/Janus-Pro-7B|
|Sa2VA|ByteDance/Sa2VA-4B|


18 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

# **D. Hyperparameters** 

_Table 3._ LAPO-ResNet hyperparameters. Names are exactly follow the configuration files used in code. 

|**Part**|**Parameter**|**Value**|
|---|---|---|
||frame<br>~~s~~tack|4|
|General|probe<br>~~l~~earning<br>~~r~~ate<br>disable<br>~~d~~istractors<br>seed|0.0003<br>True<br>0|
||eval<br>~~s~~eed|0|
||eval<br>~~e~~pisodes|50|
||latent<br>~~a~~ction<br>~~d~~im|128|
||idm<br>~~e~~ncoder<br>~~s~~cale|5|
||idm<br>~~e~~ncoder<br>~~n~~um<br>~~r~~es<br>~~b~~locks|1|
||idm<br>~~e~~ncoder<br>~~c~~hannels|[16, 16, 32, 32, 128, 128, 256]|
||fdm<br>~~e~~ncoder<br>~~s~~cale|1|
||fdm<br>~~e~~ncoder<br>~~n~~um<br>~~r~~es<br>~~b~~locks|1|
|Latent action learning|fdm<br>~~e~~ncoder<br>~~c~~hannels|[16, 16, 32, 32, 128, 128, 256]|
||num<br>~~e~~pochs|10|
||batch<br>~~s~~ize|64|
||learning<br>~~r~~ate|0.0001|
||weight<br>~~d~~ecay|0.0|
||warmup<br>~~e~~pochs|1|
||grad<br>~~n~~orm|-|
||num<br>~~e~~pochs|10|
||batch<br>~~s~~ize|64|
||learning<br>~~r~~ate|0.0001|
|bhi li|weight<br>~~d~~ecay|0.0|
|Latent eavor conng|warmup<br>~~e~~pochs|0|
||encoder<br>~~s~~cale|5|
||encoder<br>~~n~~um<br>~~r~~es<br>~~b~~locks|1|
||encoder<br>~~c~~hannels|[16, 16, 32, 32, 128, 128, 256]|
||total<br>~~u~~pdates|100000|
||batch<br>~~s~~ize|64|
|Latent actions decoding|learning<br>~~r~~ate|0.001|
||hidden<br>~~d~~im|128|
||num<br>~~l~~abeled<br>~~t~~rajectories|[16, 8, 2, 4]|


19 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

_Table 4._ LAPO-Trans hyperparameters. Names exactly follow the configuration files used in code. 

|**Part**|**Parameter**|**Value**|
|---|---|---|
||frame<br>~~s~~tack|4|
||probe<br>~~l~~earning<br>~~r~~ate|0.0003|
|Gl|disable<br>~~d~~istractors|True|
|enera|seed|0|
||eval<br>~~s~~eed|0|
||eval<br>~~e~~pisodes|50|
||latent<br>~~a~~ction<br>~~d~~im|128|
||patch<br>~~s~~ize|32|
||fdm<br>~~u~~se<br>~~c~~ross<br>~~a~~ttn|False|
||idm<br>~~h~~idden<br>~~d~~im|896|
||idm<br>~~n~~um<br>~~l~~ayers|4|
||idm<br>~~n~~um<br>~~h~~eads|16|
||fdm<br>~~h~~idden<br>~~d~~im|256|
||fdm<br>~~n~~um<br>~~l~~ayers|4|
|Latent action learning|fdm<br>~~n~~um<br>~~h~~eads|8|
||normalize<br>~~q~~k|False|
||pre<br>~~n~~orm|True|
||num<br>~~e~~pochs|10|
||batch<br>~~s~~ize|64|
||learning<br>~~r~~ate|0.0001|
||weight<br>~~d~~ecay|0.0|
||warmup<br>~~e~~pochs|1|
||grad<br>~~n~~orm|-|
||num<br>~~e~~pochs|10|
||batch<br>~~s~~ize|64|
||learning<br>~~r~~ate|0.0001|
|L bhi li|weight<br>~~d~~ecay|0.0|
|atent eavor conng|warmup<br>~~e~~pochs|0|
||encoder<br>~~s~~cale|5|
||encoder<br>~~n~~um<br>~~r~~es<br>~~b~~locks|1|
||encoder<br>~~c~~hannels|[16, 16, 32, 32, 128, 128, 256]|
||total<br>~~u~~pdates|100000|
||batch<br>~~s~~ize|64|
|Latent actions decoding|learning<br>~~r~~ate|0.001|
||hidden<br>~~d~~im|128|
||num<br>~~l~~abeled<br>~~t~~rajectories|[16, 8, 2, 4]|


20 

**Vision-Language Models Unlock Task-Centric Latent Actions** 

_Table 5._ LAPO+VLM hyperparameters. Names exactly follow the configuration files used in code. 

|**Part**|**Parameter**|**Value**|
|---|---|---|
||frame<br>~~s~~tack|4|
||probe<br>~~l~~earning<br>~~r~~ate|0.0003|
||disable<br>~~d~~istractors|True|
|l|seed|0|
|Genera|eval<br>~~s~~eed|0|
||eval<br>~~e~~pisodes|50|
||type|molmo|
||prompt|Point to the robotic arm gripper.|
|VLM (example)|layer|27|
||target|output|
||reduce<br>~~s~~trategy|mean|
||latent<br>~~a~~ction<br>~~d~~im|128|
||idm<br>~~e~~ncoder<br>~~s~~cale|5|
||idm<br>~~e~~ncoder<br>~~n~~um<br>~~r~~es<br>~~b~~locks|1|
||idm<br>~~e~~ncoder<br>~~c~~hannels|[16, 16, 32, 32, 128, 128, 256]|
||fdm<br>~~h~~idden<br>~~d~~im|1024|
|Latent action learning|fdm<br>~~n~~um<br>~~l~~ayers|4|
||fdm<br>~~e~~xpand|4|
||num<br>~~e~~pochs|200|
||batch<br>~~s~~ize|64|
||learning<br>~~r~~ate|0.0001|
||weight<br>~~d~~ecay|0.0|
||warmup<br>~~e~~pochs|1|
||grad<br>~~n~~orm|-|
||num<br>~~e~~pochs|10|
||batch<br>~~s~~ize|64|
||learning<br>~~r~~ate|0.0001|
|Latent behavior cloning|weight<br>~~d~~ecay|0.0|
||warmup<br>~~e~~pochs|0|
||encoder<br>~~s~~cale|5|
||encoder<br>~~n~~um<br>~~r~~es<br>~~b~~locks|1|
||encoder<br>~~c~~hannels|[16, 16, 32, 32, 128, 128, 256]|
||total<br>~~u~~pdates|100000|
||batch<br>~~s~~ize|64|
|Latent actions decoding|learning<br>~~r~~ate|0.001|
||hidden<br>~~d~~im|128|
||num<br>~~l~~abeled<br>~~t~~rajectories|[16, 8, 2, 4]|


21 

