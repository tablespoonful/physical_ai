---
title: "OMG: Omni-Modal Motion Generation for Generalist Humanoid Control"
date: "2026-06-09"
authors: "Siqiao Huang; Kun-Ying Lee; Dongming Qiao; Guanqi He; Zhenyu Wang; Yitang Li"
url: https://arxiv.org/abs/2606.10340
pdf: https://arxiv.org/pdf/2606.10340
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.10340)** / [論文ページ](https://arxiv.org/abs/2606.10340)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **OMG: Omni-Modal Motion Generation for Generalist Humanoid Control** 

**Siqiao Huang**<sup>_∗_</sup> **, Kun-Ying Lee**<sup>_∗_</sup> **, Dongming Qiao**<sup>_∗_</sup> **, Guanqi He**<sup>_∗_</sup> **, Zhenyu Wang, Yitang Li, Shaoting Zhu, Hang Zhao**<sup>_†_</sup> Tsinghua University 

> _∗_ Equal contribution _†_ Corresponding author **Project Page:** `https://tsinghua-mars-lab.github.io/OMG/` 


Figure 1: **Overview. OMG** decomposes humanoid whole-body control into a scalable motion generation brain and a reactive motion tracking cerebellum. Built on **OMG-Data** , a curation of 1000+ hours omni-modal humanoid motion data, **OMG-DiT** maps language, audio, human reference, and their compositions into robot-executable future motions, which are deployed on a Unitree G1 in real time, paired with a pretrained motion tracker [1]. This unified generator-tracker hierarchy enables general-purpose omni-modal control and sample-efficient adaptation to new tasks and modalities. 

**Abstract:** Humanoid whole-body control has made significant progress in recent years, yet existing approaches remain limited to few-skill policies with heavy reward engineering, or motion trackers that are difficult to extend to new input modalities. We argue that the key to general-purpose humanoid control is to build a scalable _brain_ , a module capable of reasoning with diverse conditioning modalities, atop a reactive motion tracking _cerebellum_ , mirroring the hierarchical structure of biological motor systems. Two challenges arise in realizing this vision: acquiring a vast amount of high-quality data to achieve general purpose control, and equipping the generator with the capability to condition on compositional, extensible multi-modal inputs. We present **OMG** , which addresses these challenges with a meticulous data curation, filtering and labeling pipeline, as well as a diffusion-based motion generation backbone that conditions on language, audio, and human reference motions. Extensive experiments validate **OMG** as an omnimodal whole-body controller exhibiting state-of-the-art performance, model scaling behavior and efficient adaptation to new distributions and modalities, marking a concrete step toward foundation models for humanoid robots. 

**Keywords:** Humanoid Whole-Body Control, Foundation Model 

## **1 Introduction** 

Humanoid whole-body control has made rapid progress, enabling agile locomotion and dexterous loco-manipulation with reinforcement learning [2, 3, 4, 5]. However, most existing policies remain tied to specific skills and reward designs, making them difficult to scale. Motion tracking provides a more scalable alternative by learning to follow reference motions [6, 7, 8], but tracking alone largely replays given motions and offers limited autonomy under high-level, multi-modal human intent. 

A promising abstraction is a generator-tracker hierarchy [9, 10, 11, 12, 13], where an upstream motion generator translates high-level conditions into future whole-body trajectories, and a downstream tracker executes them on the robot [1, 6]. Yet realizing this paradigm requires overcoming two key challenges. First, high-quality humanoid motion data is scarce, fragmented, and heterogeneous, unlike web-scale text or visual data [14, 15]. Second, the motion generator must support diverse, composable, and extensible control modalities while remaining adaptable to new control interfaces. 

To this end, we introduce **OMG** , an **<u>O</u>** <u>mni-Modal</u> **<u>M</u>** <u>otion</u> **<u>G</u>** <u>eneration framework for generalist hu-</u> manoid whole-body control. At the data level, we curate **OMG-Data** , a large-scale multi-modal humanoid motion corpus of **1000+** hours, by retargeting, filtering, annotating, and aligning heterogeneous motions into the Unitree G1 embodiment. At the model level, we instantiate **OMG-DiT** , a diffusion transformer backbone that maps language, audio, human-reference motions, and their compositions into robot-executable future trajectories. Importantly, new modalities can be incorporated through lightweight condition encoders while reusing the pretrained motion prior; unseen control signal combinations can be composed at inference through guidance. 

Extensive experiments demonstrate **OMG** ’s capabilities in producing high-quality, physically executable motions across diverse modalities. Furthermore, **OMG** exhibits foundation-model-like properties, including predictable scaling, sample-efficient adaptation, and zero-shot composition of control signals. These results suggest that generalist humanoid control can be advanced not only by stronger low-level controllers, but also by scaling the motion-generation brain that interfaces human intents with physical execution. In summary, our contributions are as follows: 

- We introduce **OMG** , an omni-modal motion generation framework for generalist humanoid whole-body control, unifying diverse conditioning modalities under a shared backbone, mapping diverse human intents into physically executable robot trajectories. 

- We curate **OMG-Data** , a large-scale omni-modal humanoid motion corpus of **1000+** hours. Through a unified pipeline of retargeting, filtering, and annotation, we align motions into a unified motion space, making supervised scaling of humanoid motion generation possible. 

- We introduce **OMG-DiT** , a diffusion-based motion generation backbone that supports extensible and compositional conditioning from language, audio, and human reference motions, allowing new modalities to be incorporated through lightweight adaptation. 

- Through extensive experiments, we validate **OMG** as an omni-modal whole-body controller, demonstrating foundation-model-like properties including model scaling behavior, few-shot adaptation, and zero-shot composition of control signals. 

## **2 Related Works** 

**Humanoid Whole-Body Control and Motion Tracking.** Recent advances in reinforcement learning have greatly expanded the capability of humanoid whole-body controllers [2, 3, 4, 5]. However, these systems are often specialized to particular task objectives and reward designs. Motion tracking [16, 17] offers a more scalable alternative, training a policy to execute human reference motions on the humanoid. Recent works [18, 6, 1, 7, 8] scale this paradigm with broader motion corpora, yielding stronger controllers that robustly track out-of-domain reference motions. These trackers form a powerful low-level execution layer for humanoid control, yet they assume availability of reference motions or low-level commands at inference time, leaving open the upstream problem of generating robot-executable motions from high-level and multi-modal conditions. 

2 


Figure 2: **Dataset Statistics of OMG-Data** . We curate a large-scale omni-modal humanoid motion corpus by aggregating heterogeneous datasets and unifying them into the Unitree G1 motion space. Left: processed data statistics across conditioning modalities and source datasets. Right: representative conditioning modalities, including language, audio, and human reference motions. 

**Interactive and Multi-Modal Motion Generation.** Motion generation [19, 20] addresses the complementary problem of translating high-level conditions into motion references. In graphics, modern generative architectures [21, 22] have substantially advanced motion generation systems, enabling expressive conditioning on text, audio, keypoints, and human references [23, 24, 25, 26], while benefiting from scaling data [27] and model parameters. However, most such models remain human-motion generators that operate in an offline manner, neglecting the need for _real-time interactive_ control. Conversely, coupling motion generation with tracking systems has garnered increasing interest in the humanoid community [12, 8, 10, 9, 13], yet these systems are typically limited to a single command modality or narrow task domain. This highlights an important missing intersection: general-purpose, omni-modal motion generation for real-time, robot-executable humanoid control. 

## **3 OMG-Data: Scaling Multi-Modal Data for Humanoid Motion Generation** 

A central obstacle to scaling humanoid whole-body motion generation is the lack of a unified, robotexecutable, and multi-modal motion corpus. Existing motion datasets are highly fragmented, and datasets differ substantially in their available label modality, motion quality, and annotation granularity. To address this challenge, we curate **OMG-Data** , a large-scale omni-modal humanoid motion corpus unified in the Unitree G1 embodiment of **1174.66** hours, realized through a carefully designed pipeline of curation, preprocessing, retargeting, annotating and filtering. 

**Data Curation and Preprocessing.** To establish a comprehensive corpus, we aggregate a diverse set of publicly available motion datasets across graphics and humanoid domains [28, 29, 30, 31, 27, 32, 33, 23, 34, 35, 36, 37, 26, 38, 39, 40, 24]. The consolidated dataset spans multiple modalities, encompassing text labels, audios, and human reference motions. Upon curation, the files first go through a validation check: all corrupted files, samples with broken links, and instances suffering from severe missing frames or invalid joint attributes are purged. For multi-modal sequence blocks that contain synchronized audio inputs (e.g., dance or co-speech gesture datasets like AIST++ [34] and BEAT2 [23]), we additionally preprocess the raw acoustic streams and audio feature vectors to be frame-aligned and temporally synchronized with corresponding motion clip trajectories. 

**Motion Retargeting and Annotation.** Since human motion representations vary across datasets, unifying the topology of motion representation becomes essential. Using General Motion Retar- 

3 


Figure 3: **OMG-DiT** learns a shared diffusion backbone while enabling conditioning with modalityspecific encoders. History motion and language are injected as global context tokens via crossattention, whereas frame-aligned signals (i.e., audio and human reference motions) are injected through FiLM [45] adapters. New modalities are attached non-invasively through zero-initialized adapters, and multiple conditions can be composed at inference via classifier-free guidance. 

geting (GMR, [41, 18, 42]), we retarget all motion representations to the motion space of Unitree G1 humanoids. To enrich datasets that lack native language descriptions or require granular crossmodal semantics, we render the retargeted motion sequences in simulation and label them with `Seed-1.8` [43], using multi-view rendered videos or representative keyframes as visual inputs. We then segment motions into training clips according to language annotation boundaries, audio phrase cuts, uniform windows, or sliding windows for long episodes. 

**Simulation-In-The-Loop Filtering.** To prevent kinematically invalid, self-colliding, or physically impossible joint configurations from contaminating the training mixture, we apply a filtering step via tracker execution in simulation. Concretely, given a sample, we roll out this motion sequence in the MuJoCo rigid-body simulator [44] using a joint-space PD tracking controller. We design the fall detection heuristics as follows: Let _ht_ denote root height and _θt_ denote root tilt angle. We mark a frame as a fall frame if _ht <_ 0 _._ 20, _θt >_ 85<sup>_◦_</sup> , or ( _ht <_ 0 _._ 35 _∧ θt >_ 60<sup>_◦_</sup> ). If the fall frame condition persists for over 10 consecutive frames, the trajectory is rejected. This physics-in-the-loop screening ensures that the processed dataset contains dynamically feasible and safe trajectories for humanoid deployment. Further details are provided in the Supplementary Material. 

## **4 OMG-DiT: Unified Diffusion Backbone for Motion Generation** 

Equipped with this large-scale multi-modal motion corpus, we instantiate **OMG-DiT** , a unified diffusion backbone that maps heterogeneous control modalities into robot-executable whole-body trajectories in real time. The key design principle is to decouple the _motion prior_ from the _condition interface_ : a shared denoising backbone maps the distribution of feasible motions, while modalityspecific encoders translate high-level intents into steerable conditions over the shared manifold. 

### **4.1 Problem Formulation** 

We consider the problem of controlling a humanoid robot to perform whole-body motions specified by multi-modal conditions. Given a set of conditioning variables _C_ = _{c_<sup>(1)</sup> _, c_<sup>(2)</sup> _, . . . , c_<sup>(</sup><sup>_N_)</sup> _}_ , which may include language, audio and other modalities, our goal is to learn a policy _π_ that produces physically realizable whole-body actions **a** _t_ conditioned on _C_ and history observations **o** _≤t_ . We decompose this policy learning problem into a cascaded generation-and-tracking formulation, or 

4 

more commonly termed planning and inverse dynamics models in manipulation [46, 47]: 


where _πϕ_ is a high-level motion generator that predicts future whole-body reference observations from multi-modal conditions, and _πψ_ is a low-level motion tracker that converts these references into executable robot actions. In this work, we focus on motion generation, and leverage pre-existing general-purpose trackers (HoloMotion [1]) as our low-level tracker. 

### **4.2 Diffusion Transformer Backbone** 

**Motion Representation.** We represent each frame in a canonical root-centric coordinate frame defined by the last observed state **x** _t_ = [˜ **p** _t,_ ˜ **r** _t,_ **_θ_** _t,_<sup>˜</sup> **j** _t_ ] _∈_ R<sup>125</sup> , where **p** ˜ _t_ and ˜ **r** _t_ denote the canonicalized root position and rotation, **_θ_** _t_ denotes joint angles, and<sup>˜</sup> **j** _t_ denotes body-link positions. This root-centric representation removes global translation and heading ambiguity while preserving the full-body geometric structure required for motion generation and downstream tracking. 

**Model Architecture. OMG-DiT** is instantiated as a Diffusion Transformer (DiT [22]) backbone trained with an **x** -prediction objective [48]. Drawing inspiration from recent advances in pixel-space diffusion [48, 49], we generate directly in motion space, avoiding training of motion encoders. History motion is injected via cross-attention, whereas the denoising timesteps are injected via channelwise concatenating with the noisy motion features before input projection. 

**Training Objective.** We train **OMG-DiT** as a conditional diffusion model generating future motion trajectories **x** _t_ +1: _t_ + _H_ conditioned on recent history **x** _t−L_ : _t_ and a subset of available conditioning modalities _Cs ⊆C_ . Given a diffusion timestep _τ_ , we corrupt the future segment as 


To enable classifier-free guidance and improve robustness, we randomly drop each available conditioning modality during training with probability _p_ drop. The resulting training objective is: 

_L_ = E **x** _,Cs,τ,_ **_ϵ_** � _∥_ **x** ˆ _t_ +1: _t_ + _H −_ **x** _t_ +1: _t_ + _H ∥_<sup>2</sup> 2� _,_ where **x** ˆ _t_ +1: _t_ + _H_ = **x** _θ_ � **x**<sup>_τ_</sup> _t_ +1: _t_ + _H_<sup>_, τ,_</sup><sup>**x**</sup><sup>_t−L_:</sup><sup>_t, Cs_</sup> � _._ (2) This objective trains a single denoising backbone to model the feasible Unitree G1 motion manifold, while allowing different condition encoders to steer generation through a shared motion prior. 

### **4.3 Omni-Modal Condition Encoding** 

**Pretraining Condition Encoders.** During pretraining, **OMG-DiT** supports conditioning on language, audio, and human-reference motion. Language annotations are encoded by a frozen T5 encoder [50] and injected into each DiT block through cross-attention, alongside encoded history frames. Frame-aligned modalities, including audio and human-reference motion, are projected through MLPs and injected into corresponding frames through per-layer FiLM modulation [45]. 

**Task-specific Finetuning Encoders.** To enable sample-efficient adaptation to downstream tasks with new modalities, we adopt non-invasive injection methods with zero-initialization. For example, while fine-tuning for Pico keypoint-conditioned teleoperation, Pico keypoints are represented as 18D frame-aligned features, and injected through zero-initialized FiLM [45] adapters. 

## **5 Experiments** 

Our experiments aim to answer the following questions: (1) How does **OMG** compare against previous hierarchical humanoid control frameworks, such as graphics-based generation plus retargeting; (2) Does pretraining lead to more efficient adaptation to new modalities/datasets compared to training from scratch; and (3) Does the shared diffusion backbone exhibit foundation-model-like properties, including data scaling and zero-shot composition of control signals? 

5 

Figure 4: **Real-World Omni-Modal Control. OMG** generates diverse Unitree G1 motions across various conditioning modalities in real time, executable in the real world. 

### **5.1 Experiment Setup** 

**Evaluation Protocol.** We evaluate **OMG** in two regimes: pretrained omni-modal motion generation and downstream finetuning. For pretraining, we consider language-, audio-, and humanreference-conditioned motion generation, where the model predicts future Unitree G1 whole-body trajectories from recent motion history and the corresponding control signal. For finetuning, we evaluate two downstream settings: text-conditioned generation on unseen data, and Pico keypointconditioned teleoperation. Unless otherwise specified, generated trajectories are executed by a pretrained HoloMotion [1] tracker. All evaluations use validation motions unseen during training. 

**Metrics.** We evaluate **OMG** along two axes: motion generation quality and tracking fidelity. For generation quality, we use modality-specific metrics, including Matching Score, R-Precision, FID, and Diversity [51] for language; BeatAlign, FID _k_ , FID _g_ , and PFC [34, 52] for audio; and MPJPE, global MPJPE, end-effector error, velocity error, and acceleration error [53, 13] for human-reference generation. For tracking fidelity, we report contact sliding, body jerk, tracker MPJPE, tracker global MPJPE, tracker velocity error and acceleration error, fall rate, and joint-limit violation rate [54, 55]. For downstream finetuning, we additionally report task-specific metrics, including keypoint tracking error [56] for Pico teleoperation. More details are provided in the supplementary material. 

6 

Table 1: **Text-conditioned motion benchmark.** For better display, R@K, Fall, and J-Limit are reported in percentage. FID and C-Slide are scaled by 10<sup>_−_2</sup> and 10<sup>_−_1</sup> , respectively. Lower is better for metrics marked with _<u>↓</u>_ <u>, and higher is better for metrics marked with</u> _<u>↑</u>_ . 

|Methods|||Mo|tion Gen|eration Q|uality||||Tracking Fid|elity and E|xecution|Failures||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||FID_↓_|Matching_↓_|R@1_↑_|R@2_↑_|R@3_↑_|Diversity_↑_|C-Slide_↓_|Jerk_↓_|MPJPE_↓_|g-MPJPE_↓_|E_vel_↓_|E_acc_↓_|Fall_↓_|J-Limit_↓_|
|GENMO|43.78|1.33|12.99|23.83|30.86|1.28|**2.66**|173.54|50.35|150.71|6.91|2.51|1.46|29.10|
|HYMotion|24.68|1.30|31.84|48.73|57.71|1.29|12.20|112.56|69.05|287.71|11.94|3.24|4.98|55.57|
|Kimodo-SMPLX-RP|38.44|1.31|26.27|39.36|46.48|1.25|4.52|189.39|43.51|198.96|7.80|2.64|2.64|23.63|
|Kimodo-G1-RP|46.36|1.32|25.59|36.13|44.63|1.21|3.92|81.44|**37.25**|125.04|5.72|1.68|1.46|19.14|
|Kimodo-G1-SEED|50.22|1.33|22.46|33.69|41.11|1.20|4.30|99.47|37.26|161.63|6.38|1.84|1.56|20.70|
|**OMG-L**|9.55|1.14|58.50|74.90|81.45|**1.39**|3.68|56.03|39.06|**98.37**|**5.11**|**1.47**|**0.29**|**14.94**|
|**OMG-XL**|**6.03**|**1.11**|**65.43**|**80.37**|**86.91**|**1.39**|3.98|**52.31**|42.68|111.41|5.48|1.53|0.78|19.34|


Table 2: **Audio-conditioned motion benchmark.** For better display, Fall and J-Limit are reported in percentage. Lower is better for metrics with _<u>↓</u>_ <u>, and higher is better for metrics with</u> _<u>↑</u>_ . 

|Methods|Audio Align|ment and|Target Mot|ion Quality|||Target Phys|ical Quality a|nd Tracke|r Fidelity|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||BeatAlign_↑_|FID_k ↓_|FID_g ↓_|PFC_↓_|C-Slide_↓_|Jerk_↓_|MPJPE_↓_|g-MPJPE_↓_|E_vel_↓_|E_acc_↓_|Fall_↓_|J-Limit_↓_|
|GENMO|0.57|506.07|9.42|**0.02**|**0.03**|**72.56**|**35.73**|111.69|**3.87**|**1.22**|0.39|12.50|
|LODGE|**0.58**|390.06|11.98|1.41|0.65|471.45|149.19|363.24|18.89|6.96|39.45|66.80|
|Bailando|0.56|134.90|15.71|0.39|0.25|117.45|38.30|106.39|5.55|1.99|**0.00**|**1.76**|
|**OMG-L**|0.49|59.20|0.74|0.57|0.41|95.73|41.07|**95.10**|6.10|1.90|**0.00**|14.26|
|**OMG-XL**|0.51|**40.46**|**0.63**|0.64|0.43|106.06|41.47|97.60|6.03|1.94|**0.00**|15.43|


Table 3: **Human-reference-conditioned motion benchmark.** For better display, Fall and J-Limit are reported in percentage. Lower / higher is better for metrics marked with _<u>↓</u>_ / _<u>↑</u>_ . 

|Methods||Tar|get Motion a|nd Physica|l Quality||||Tracker-Execut|ed Target Fidelit|y and Failures|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||MPJPE_↓_|g-MPJPE_↓_|EE Error_↓_|E_vel_↓_|E_acc_↓_|C-Slide_↓_|Jerk_↓_|Target MPJPE_↓_|Target g-MPJPE_↓_|Target E_vel_↓_|Target E_acc|_↓_Fall_↓_|J-Limit_↓_|
|GMR|81.95|223.69|219.23|11.72|10.41|0.45|404.80|90.54|249.47|12.52|5.22|11.33|68.75|
|NMR|173.77|390.82|477.08|14.87|7.43|0.77|97.75|102.28|299.27|11.26|3.32|14.84|87.89|
|PHC|51.44|153.44|152.18|5.06|3.97|0.45|131.38|47.80|115.92|5.86|1.99|3.71|39.45|
|OmniRetarget|56.90|119.71|131.14|5.55|4.87|**0.31**|188.92|44.34|111.58|5.94|2.35|0.98|24.22|
|**OMG-L**|26.40|64.64|72.39|6.16|3.91|0.35|**61.01**|**42.81**|**110.66**|5.63|**1.62**|**0.20**|**22.66**|
|**OMG-XL**|**18.84**|**47.83**|**52.26**|**5.03**|**3.69**|0.32|64.04|43.07|112.60|**5.55**|1.63|0.39|23.05|


### **5.2 Pretraining Experiments** 

**Text to Motion.** We compare OMG against recent human motion generation models, including GENMO [25], HYMotion [57], and Kimodo [26], where generated human motions are retargeted to the Unitree G1 when necessary via GMR [41]. As shown in Table 1, **OMG** achieves substantial gains in motion generation quality, while retaining high tracking fidelity, showcasing its capability to generate high-quality and robot-executable motions conditioned on text. 

**Audio to Motion.** We next evaluate audio-conditioned motion generation, comparing against both generalist and dedicated audio-to-motion baselines, including GENMO [25], LODGE [58], and Bailando [59]. As shown in Table 2, **OMG** maintains superior performance in audio alignment and motion quality, while achieving comparable performance in tracking fidelity. 

**Human Reference to Motion.** Finally, we evaluate human-reference-conditioned motion generation. We compare against both optimization and learning based retargeting methods, including GMR [41], NMR [60], PHC [61], and OmniRetarget [62]. As shown in Table 3, **OMG** substantially outperforms these baselines in both motion quality and tracking fidelity, demonstrating that the learned generator can serve as an implicit yet highly-effective retargeting module for humanoid control. 

### **5.3 Finetuning Experiments** 

**Few-shot Text-to-Motion Finetuning.** To evaluate whether motion-generation pretraining provides positive transfer to unseen data distributions, we finetune **OMG** on AMASS-CMU, held out 

7 

Table 4: **Text-to-Motion Finetuning.** 

Table 5: **Pico Keypoint-Based Teleoperation.** 

|Finetuning Data %|FID_↓_|R@1_↑_|R@2_↑_|R@3_↑_|Finetuning Data %|MPJPE_↓_|g-MPJPE_↓_|E_vel_↓_|E_acc_↓_|
|---|---|---|---|---|---|---|---|---|---|
||_From_|_Scratch_||||_From_|_Scratch_|||
|1%|0.6615|0.0430|0.0762|0.1025|1%|128.24|448.09|24.34|17.13|
|10%|0.1763|0.1162|0.2080|0.2998|10%|82.46|279.21|14.90|3.92|
|100%|0.1001|0.1689|0.2764|0.3779|100%|39.42|134.85|8.03|2.95|
||**OMG**_F_|_inetuned_||||**OMG**|_Finetuned_|||
|1%|0.1378|0.1533|0.2637|0.3428|1%|93.61|286.84|16.11|3.74|
|10%|0.0886|0.1816|0.3096|0.3994|10%|52.99|164.91|9.91|3.09|
|100%|**0.0827**|**0.2021**|**0.3115**|**0.4141**|100%|**25.73**|**77.01**|**5.70**|**2.62**|


during pretraining. As shown in Table 4, the pretrained model consistently outperforms the fromscratch counterpart across all finetuning fractions. Notably, with only 1% of the target data, finetuning already yields comparable motion quality to training from scratch with the full data budget. 

**Pico Keypoint-Based Teleoperation.** To test if positive transfer extends to novel _modalities_ , we adapt **OMG** to condition on Pico keypoints, enabling teleoperation. As shown in Table 5, finetuned models consistently outperform training from scratch under the same data budgets, suggesting that the pretrained model serves as a reusable prior when incorporating a new control interface. 

### **5.4 Analysis** 

**Zero-shot Compositionality.** A hallmark of foundation models is _compositional generalization_ , i.e. the ability to combine capabilities learned independently. We test this by composing novel language and audio conditions at inference. As shown in Figure 4, the humanoid successfully follows both the language instruction and the audio rhythm simultaneously, producing motions that are qualitatively distinct from either condition applied alone. 

**Scaling Behavior.** Finally, we ask whether motion generation is a scalable objective: do larger diffusion backbones yield better humanoid motion quality, given the same data and evaluation protocol? To answer this, we pretrain three **OMG-DiT** variants with increasing numbers of parameters. As shown in Figure 5, performance improves consistently with model size, suggesting that humanoid motion generation benefits from increased model capacity. 


Figure 5: **Scaling OMG-DiT.** 

## **6 Conclusion** 

We present **OMG** , an omni-modal motion generation framework for generalist humanoid wholebody control. **OMG** combines **OMG-Data** , a large-scale corpus unified in Unitree G1 motion space, with **OMG-DiT** , a shared diffusion backbone that maps language, audio, human references, and their compositions into robot-executable future motions. Experiments show strong motion quality, physical executability, sample-efficient adaptation, scaling behavior, and zero-shot compositionality, positioning scaling motion generation as a promising path toward humanoid foundation models. 

## **7 Limitations** 

This work has several limitations. First, our training data mainly cover flat-ground motions; extending **OMG** to uneven and in-the-wild terrain remains challenging. Second, **OMG** uses a modular generator-tracker hierarchy, however, we focus only on motion generation for simplicity. We believe jointly adapting the generator and tracker, or incorporating execution feedback into generation, is an important direction for improving performance of the system, which we leave for future work. 

8 

### **Acknowledgments** 

The authors would like to sincerely thank Ziwen Zhuang, Zekun Qi, Haoyang Weng, and Yue Chen for their insightful discussions and feedback. 

## **References** 

- [1] M. Chen, K. Wang, B. Zhang, X. Ma, Z. Yang, Y. Ren, Q. Huang, Z. Zhu, Y. Wang, and Z. Su. Holomotion-1 technical report, 2026. URL `https://arxiv.org/abs/2605.15336` . 

- [2] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. _arXiv preprint arXiv:2406.10759_ , 2024. 

- [3] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik. Learning humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2410.03654_ , 2024. 

- [4] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [5] Y. Li, Y. Zhang, W. Xiao, C. Pan, H. Weng, G. He, T. He, and G. Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control. _arXiv preprint arXiv:2505.24198_ , 2025. 

- [6] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [7] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [8] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [9] A. Serifi, R. Grandia, E. Knoop, M. Gross, and M. Bächer. Robot motion diffusion model: Motion generation for robotic characters. In _SIGGRAPH asia 2024 conference papers_ , pages 1–9, 2024. 

- [10] G. Tevet, S. Raab, S. Cohan, D. Reda, Z. Luo, X. B. Peng, A. Bermano, and M. Van de Panne. Closd: Closing the loop between simulation and diffusion for multi-task character control. In _International Conference on Learning Representations_ , volume 2025, pages 46506–46520, 2025. 

- [11] M. Xu, Y. Shi, K. Yin, and X. B. Peng. Parc: Physics-based augmentation with reinforcement learning for character controllers. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , pages 1–11, 2025. 

- [12] Z. Zhang, K. Wen, M. Xu, J. He, C. Li, T. Miki, C. Schwarke, C. Zhang, X. B. Peng, and M. Hutter. Learning whole-body humanoid locomotion via motion generation and motion tracking. _arXiv preprint arXiv:2604.17335_ , 2026. 

- [13] W. Xie, J. Zheng, J. Han, J. Shi, W. Zhang, C. Bai, and X. Li. Textop: Real-time interactive text-driven humanoid robot motion generation and control. _arXiv preprint arXiv:2602.07439_ , 2026. 

- [14] C. Schuhmann, R. Beaumont, R. Vencu, C. Gordon, R. Wightman, M. Cherti, T. Coombes, A. Katta, C. Mullis, M. Wortsman, et al. Laion-5b: An open large-scale dataset for training next generation image-text models. _Advances in neural information processing systems_ , 35: 25278–25294, 2022. 

9 

- [15] G. Penedo, H. Kydlíˇcek, A. Lozhkov, M. Mitchell, C. Raffel, L. Von Werra, T. Wolf, et al. The fineweb datasets: Decanting the web for the finest text data at scale. _Advances in Neural Information Processing Systems_ , 37:30811–30849, 2024. 

- [16] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi. Learning human-to-humanoid real-time whole-body teleoperation. _arXiv preprint arXiv:2403.04436_ , 2024. 

- [17] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [18] Y. Ze, Z. Chen, J. P. Araújo, Z. ang Cao, X. B. Peng, J. Wu, and C. K. Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [19] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ , 2022. 

- [20] M. Zhang, Z. Cai, L. Pan, F. Hong, X. Guo, L. Yang, and Z. Liu. Motiondiffuse: Text-driven human motion generation with diffusion model. _arXiv preprint arXiv:2208.15001_ , 2022. 

- [21] L. Yang, Z. Zhang, Y. Song, S. Hong, R. Xu, Y. Zhao, W. Zhang, B. Cui, and M.-H. Yang. Diffusion models: A comprehensive survey of methods and applications. _ACM computing surveys_ , 56(4):1–39, 2023. 

- [22] W. Peebles and S. Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 

- [23] H. Liu, Z. Zhu, G. Becherini, Y. Peng, M. Su, Y. Zhou, X. Zhe, N. Iwamoto, B. Zheng, and M. J. Black. Emage: Towards unified holistic co-speech gesture generation via expressive masked audio gesture modeling, 2024. URL `https://arxiv.org/abs/2401.00374` . 

- [24] J. Zhang, Z. Kang, L. Liu, J. Chang, Q. Tian, F. Gao, and Y. Wang. Opendance: Multimodal controllable 3d dance generation with large-scale internet data, 2025. URL `https://arxiv. org/abs/2506.07565` . 

- [25] J. Li, J. Cao, H. Zhang, D. Rempe, J. Kautz, U. Iqbal, and Y. Yuan. Genmo: A generalist model for human motion. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [26] D. Rempe, M. Petrovich, Y. Yuan, H. Zhang, X. B. Peng, Y. Jiang, T. Wang, U. Iqbal, D. Minor, M. de Ruyter, J. Li, C. Tessler, E. Lim, E. Jeong, S. Wu, E. Hassani, M. Huang, J.-B. Yu, C. Chung, L. Song, O. Dionne, J. Kautz, S. Yuen, and S. Fidler. Kimodo: Scaling controllable human motion generation. _arXiv:2603.15546_ , 2026. 

- [27] K. Fan, S. Lu, M. Dai, R. Yu, L. Xiao, Z. Dou, J. Dong, L. Ma, and J. Wang. Go to zero: Towards zero-shot motion generation with million-scale data, 2025. URL `https://arxiv. org/abs/2507.07095` . 

- [28] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [29] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal. Robust motion in-betweening. _arXiv:2102.04942_ , 39(4), 2020. 

- [30] J. Li, J. Wu, and C. K. Liu. Object motion guided human motion synthesis. _ACM Trans. Graph._ , 42(6), 2023. 

10 

- [31] I. Mason, S. Starke, and T. Komura. Real-time style modelling of human locomotion via feature-wise transformations and local motion phases. _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , 5(1):1–18, 2022. 

- [32] C. Guo, I. Hwang, J. Wang, and B. Zhou. Snapmogen: Human motion generation from expressive texts, 2025. URL `https://arxiv.org/abs/2507.09122` . 

- [33] R. Li, J. Zhao, Y. Zhang, M. Su, Z. Ren, H. Zhang, Y. Tang, and X. Li. Finedance: A fine-grained choreography dataset for 3d full body dance generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10234–10243, 2023. 

- [34] R. Li, S. Yang, D. A. Ross, and A. Kanazawa. Learn to dance with aist++: Music conditioned 3d dance generation, 2021. 

- [35] Y. Zhang, J. Lin, A. Zeng, G. Wu, S. Lu, Y. Fu, Y. Cai, R. Zhang, H. Wang, and L. Zhang. Motion-x++: A large-scale multimodal 3d whole-body human motion dataset. _arXiv preprint arXiv:2501.05098_ , 2025. 

- [36] J. Lin, A. Zeng, S. Lu, Y. Cai, R. Zhang, H. Wang, and L. Zhang. Motion-x: A large-scale 3d expressive whole-body human motion dataset. _Advances in Neural Information Processing Systems_ , 2023. 

- [37] B. Kim, H. I. Jeong, J. Sung, Y. Cheng, J. Lee, J. Y. Chang, S.-I. Choi, Y. Choi, S. Shin, J. Kim, and H. J. Chang. Personabooth: Personalized text-to-motion generation. _arXiv preprint arXiv:2503.07390_ , 2025. 

- [38] K. Chen, Z. Tan, J. Lei, S.-H. Zhang, Y.-C. Guo, W. Zhang, and S.-M. Hu. Choreomaster: choreography-oriented music-driven dance synthesis. _ACM Trans. Graph._ , 40(4), July 2021. ISSN 0730-0301. doi:10.1145/3450626.3459932. URL `https://doi.org/10.1145/ 3450626.3459932` . 

- [39] B. Burkanova, P. J. Yazdian, C. Zhang, T. Evans, P. Tuttösí, and A. Lim. Salsa as a nonverbal embodied language – the compas3d dataset and benchmarks, 2025. URL `https://arxiv. org/abs/2507.19684` . 

- [40] N. Le, T. Pham, T. Do, E. Tjiputra, Q. D. Tran, and A. Nguyen. Music-driven group choreography. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023. 

- [41] Y. Ze, J. P. Araújo, J. Wu, and C. K. Liu. Gmr: General motion retargeting, 2025. URL `https://github.com/YanjieZe/GMR` . GitHub repository. 

- [42] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [43] B. Seed. Seed1. 8 model card: Towards generalized real-world agency. _arXiv preprint arXiv:2603.20633_ , 2026. 

- [44] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026– 5033. IEEE, 2012. doi:10.1109/IROS.2012.6386109. 

- [45] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

- [46] Y. Du, S. Yang, B. Dai, H. Dai, O. Nachum, J. Tenenbaum, D. Schuurmans, and P. Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

11 

- [47] Y. Du, S. Yang, P. Florence, F. Xia, A. Wahid, P. Sermanet, T. Yu, P. Abbeel, J. B. Tenenbaum, L. Kaelbling, et al. Video language planning. In _International Conference on Learning Representations_ , volume 2024, pages 31138–31155, 2024. 

- [48] T. Li and K. He. Back to basics: Let denoising generative models denoise. _arXiv preprint arXiv:2511.13720_ , 2025. 

- [49] Y. Lu, S. Lu, Q. Sun, H. Zhao, Z. Jiang, X. Wang, T. Li, Z. Geng, and K. He. One-step latent-free image generation with pixel mean flows. _arXiv preprint arXiv:2601.22158_ , 2026. 

- [50] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of machine learning research_ , 21(140):1–67, 2020. 

- [51] J. Zhang, Y. Zhang, X. Cun, Y. Zhang, H. Zhao, H. Lu, X. Shen, and Y. Shan. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 14730–14740, 2023. 

- [52] J. Tseng, R. Castellon, and K. Liu. Edge: Editable dance generation from music. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 448–458, 2023. 

- [53] J. Jiang, P. Streli, H. Qiu, A. Fender, L. Laich, P. Snape, and C. Holz. Avatarposer: Articulated full-body pose tracking from sparse motion sensing. In _European conference on computer vision_ , pages 443–460. Springer, 2022. 

- [54] X. Yi, Y. Zhou, M. Habermann, S. Shimada, V. Golyanik, C. Theobalt, and F. Xu. Physical inertial poser (pip): Physics-aware real-time human motion tracking from sparse inertial sensors. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 13167–13178, 2022. 

- [55] H. Cho, S.-H. Kim, J. Kang, and D. Koo. Safeflow: Real-time text-driven humanoid wholebody control via physics-guided rectified flow and selective safety gating. _arXiv preprint arXiv:2603.23983_ , 2026. 

- [56] R. Nai, B. Zheng, J. Zhao, H. Zhu, S. Dai, Z. Chen, Y. Hu, Y. Hu, T. Zhang, C. Wen, et al. Humanoid manipulation interface: Humanoid whole-body manipulation from robot-free demonstrations. _arXiv preprint arXiv:2602.06643_ , 2026. 

- [57] Y. Wen, Q. Shuai, D. Kang, J. Li, C. Wen, Y. Qian, N. Jiao, C. Chen, W. Chen, Y. Wang, et al. Hy-motion 1.0: Scaling flow matching models for text-to-motion generation. _arXiv preprint arXiv:2512.23464_ , 2025. 

- [58] R. Li, Y. Zhang, Y. Zhang, H. Zhang, J. Guo, Y. Zhang, Y. Liu, and X. Li. Lodge: A coarse to fine diffusion network for long dance generation guided by the characteristic dance primitives. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1524–1534, 2024. 

- [59] L. Siyao, W. Yu, T. Gu, C. Lin, Q. Wang, C. Qian, C. C. Loy, and Z. Liu. Bailando: 3d dance generation by actor-critic gpt with choreographic memory. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11050–11059, 2022. 

- [60] Q. Zhao, K. Yang, X. Wang, S. Zhao, Y. Lu, X. Zhang, Q. Shen, X.-X. Long, and X. Cao. Make tracking easy: Neural motion retargeting for humanoid whole-body control. _arXiv preprint arXiv:2603.22201_ , 2026. 

- [61] Z. Luo, J. Cao, A. W. Winkler, K. Kitani, and W. Xu. Perpetual humanoid control for real-time simulated avatars. In _International Conference on Computer Vision (ICCV)_ , 2023. 

12 

- [62] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [63] W. Zeng, S. Lu, K. Yin, X. Niu, M. Dai, J. Wang, and J. Pang. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 

- [64] M. Yuan, T. Yu, W. Ge, X. Yao, D. Li, H. Wang, J. Chen, B. Li, W. Zhang, W. Zeng, et al. A survey of behavior foundation model: Next-generation whole-body control system of humanoid robots. _IEEE transactions on pattern analysis and machine intelligence_ , 2025. 

- [65] A. Tirinzoni, A. Touati, J. Farebrother, M. Guzek, A. Kanervisto, Y. Xu, A. Lazaric, and M. Pirotta. Zero-shot whole-body humanoid control via behavioral foundation models. _arXiv preprint arXiv:2504.11054_ , 2025. 

- [66] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati, et al. Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. _arXiv preprint arXiv:2511.04131_ , 2025. 

- [67] Z. Tao, Z. Su, P. Liu, J. Sun, W. Que, J. Ma, J. Yu, J. Cao, P. Sun, H. Liang, et al. Heracles: Bridging precise tracking and generative synthesis for general humanoid control. _arXiv preprint arXiv:2603.27756_ , 2026. 

- [68] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black. SMPL: A skinned multiperson linear model. _ACM Transactions on Graphics, (Proc. SIGGRAPH Asia)_ , 34(6):248:1– 248:16, Oct. 2015. 

- [69] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. A. Osman, D. Tzionas, and M. J. Black. Expressive body capture: 3d hands, face, and body from a single image. In _Proceedings IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2019. 

- [70] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li. On the continuity of rotation representations in neural networks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5745–5753, 2019. 

- [71] J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu. Roformer: Enhanced transformer with rotary position embedding. _Neurocomputing_ , 568:127063, 2024. 

- [72] J. Song, C. Meng, and S. Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 

- [73] F. Liu, S. Zhang, X. Wang, Y. Wei, H. Qiu, Y. Zhao, Y. Zhang, Q. Ye, and F. Wan. Timestep embedding tells: It’s time to cache for video diffusion model. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 7353–7363, 2025. 

- [74] I. Loshchilov and F. Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 

13 

## **A Extended Related Work** 

**Behavior Foundation Models for Humanoid Robots.** Going beyond isolated skills, recent works have started to explore systems that capture broad, reusable behavioral knowledge for humanoid robots, often referred to as _Behavior Foundation Models_ [63, 64]. Using forward-backward representations, Meta Motivo [65] and BFM-Zero [66] learn promptable latent-conditioned policies for zero-shot behavior selection, enabling multiple objectives such as motion tracking and goal reaching. Other representative works learn structured generative behavior priors with masked control interfaces for multiple low-level control modes [63], or introduce a generative middleware that rewrites reference commands for robust recovery [67]. Together, these works show that general humanoid behavior benefits from reusable priors, but their priors are primarily instantiated as motion primitives that operate close to low-level execution. In contrast, **OMG** focuses on the upstream motion-generation interface, addressing how to translate heterogeneous _human_ commands, such as language, audio, or human reference motions, into robot-executable motion references. 

## **B Details on OMG-Data** 

### **B.1 Dataset Composition** 

We report statistics for **OMG-Data** , as shown in Table 6. All motion sequences are represented at a temporal resolution of 30 Hz. AMASS-CMU and Weizmann are held out during pretraining. 

Table 6: **Statistics of the Pretraining Dataset by Conditioning Modality.** We curate publicly available motion datasets from graphics and humanoid domains and then apply careful filtering, annotation, and augmentation, yielding 1174.66 hours of data in total. � , � , and � denote text descriptions, <u>paired audio, and human reference motion, respectively.</u> 

|Dataset|Label||Original|||Processed||
|---|---|---|---|---|---|---|---|
|||# Samples|Avg. Length|Total Hours|# Samples|Avg. Length|Total Hours|
|AMASS [28]|�,<br>�|17.9K|1.4K|94.8|51.1K|111|52.7|
|AMASS (holdout CMU & WEIZMANN) [28]|�,<br>�|13.65K|1.4K|44.9|39.0K|105|38|
|LAFAN1 [29]|�|40|6.6K|2.5|977|240|2.2|
|OMOMO [30]|�,<br>�|5.9K|179|10|15K|67|9.4|
|100style [31]|�,<br>�|0.8K|2.9K|22.12|10.7K|223|22.10|
|HumanML [27]|�,<br>�|26.8K|219|54.5|25.7K|218|52.04|
|Kungfu [27]|�|1.0K|453|4.3|–|–|–|
|MotionGV [27]|�,<br>�|56K|140|727|53.8K|128|637.14|
|fitness [27]|�,<br>�|262|610|1.48|337|244|0.76|
|MotionLLAMA (subset) [27]|�,<br>�|4.5K|286|12|4.9K|236|10.7|
|SnapMoGen [32]|�,<br>�|50K|407|188.7|41.0K|222|84.01|
|FineDance [33]|�,<br>�,<br>�|0.2K|4.0K|14.6|6.0K|240|13.26|
|BEAT2 [23]|�,<br>�|1.7K|3.4K|60|417|2.0K|8.06|
|AIST++ [34]|�,<br>�,<br>�|1.4K|400|5.2|2.2K|240|4.98|
|IDEA400 [35,36]|�,<br>�|12.5K|176|20|10K|177|17.24|
|PerMo [37]|�,<br>�|6.6K|140|8.6|6.5K|139|8.38|
|BONES-SEED [26]|�|71K|219|144|79K|182|134.35|
|ChoreoMaster [38]|�,<br>�|2.7K|46.7|1.2|2.5K|47|1.11|
|CoMPAS3D [39]|�,<br>�|4.8K|138|6.2|4.66K|129|5.57|
|AIOZ-GDANCE [40]|�,<br>�|6K|1.1K|60.8|5.8K|1091|59.05|
|OpenDance [24]|�,<br>�|5.0K|300|14.0|4.9K|300|13.61|
|**Total**|�,<br>�,<br>�|**288.8K**|**411**|**1496.9**|**364.5K**|**177**|**1174.66**|


### **B.2 Details on Retargeting** 

For motion represented in SMPL [68] or SMPL-X [69] format, body parameters are directly translated and mapped onto the skeletal frame of the G1 robot via geometric optimization in GMR. For datasets derived from raw videos, we employ the GENMO framework [25] to recover 3D human body meshes, which are subsequently passed into GMR to compute G1 joint trajectories. For motions represented in the FBX format, we convert them using standardized joint-mapping heuristics or GMR, depending on the structural complexity of the source skeleton hierarchy. 

14 

### **B.3 Details on Labeling** 

We provide the prompt used for Seed-1.8 VLM annotation below: 

#### **Prompt B.1: Prompt used for VLM-based temporal motion annotation.** 

```
Youareahumanoidrobotmotionlabelingmodel(VLM).Yourtaskistoperformstructuredmotion
labelingfortheinputvideo,ratherthangeneratingdescriptivetext.
[MostImportantRule]
Youmustsegmentwhenthereisachangein"motionatomicaction".Ifthespecificactionchanges,
eveniftheoverallstyleremainsconsistent,youstillneedtocreateanewsegment.
[CoreRequirement]
Pleasedividetheinputvideointomultipleconsecutivetimesegments,andgenerateastructured
actionlabelforeachsegment.
Theoutputofeachsegmentmustinclude:
1.starttime
2.endtime
3.style
4.action
[SegmentationCriteria]
Youshoulddecidewhethertosplitmainlybasedon:
-whetherthemotionstylechanges
-whetherafinermotionstyle/typecanbejudgedtohavechanged
-whetherthemainactionchanges
Ifthemotionremainscontinuousandnoobviouschangeoccurs,donotover-segment.
[ActionRequirements]
1.actionmustbewritteninEnglish
2.actionshouldsummarizetheconcretemotionperformedinthissegment
3.actionshoulddescribethemotionitselfasmuchaspossible,andshouldnotwriteoverlyabstract
content
4.actionshouldbeconcise,andnomorethan25words
5.actionshouldbehelpfulfortrainingatext-to-motiongenerationmodel
[StyleRequirements]
1.stylemustbewritteninEnglish
2.styleshouldsummarizethemotionstyleofthissegment,suchassmooth,intense,rhythmic,
explosive,etc.
3.styleshouldbeconcise
[OutputFormat]
PleaseoutputinJSONformat:
{
"video_summary":"overallsummaryofthevideo",
"segments":[
{
"start_time":0.0,
"end_time":1.5,
"style":"smooth",
"action":"raisebotharmsandstepslowlytotheleft"
},
{
"start_time":1.5,
"end_time":3.0,
"style":"rhythmic",
"action":"turntorsoandswingarmsinalternatingbeats"
}
]
}
[OutputConstraints]
1.OutputvalidJSONonly
2.Donotoutputanyexplanatorytext
3.Timemustbeinseconds
4.Keepallstart_timeandend_timevaluestoonedecimalplace
5.Segmentsmustbeconsecutiveandnon-overlapping
6.start_timemustbelessthanend_time
7.video_summaryshouldbeabriefsummaryofthewholevideo
[Goal]
Youroutputshouldhelptrainamotiongenerationmodel,sothelabelsshouldpreservemotioncontent,
motionstyle,andtemporalchangesasmuchaspossible.
```

15 

### **B.4 Segmentation Details** 

For text-conditioned sequences, motions are sliced according to the temporal boundaries of their language annotations. For audio-paired datasets, motion and audio sequences are segmented according to existing music phrase cuts or partitioned into uniform window lengths. For datasets with prohibitively long motion sequences, e.g., LAFAN1, 100style, FineDance, and AMASS, we further decompose each sequence into fixed-length sub-clips using a sliding-window strategy. 

### **B.5 Simulation-in-the-Loop Filtering Details** 

For each generated motion, we first execute the sequence in the MuJoCo rigid-body simulator using the same tracker runtime used for deployment. The tracker predicts joint-space actions, which are clipped by `action_clip` =10.0 and converted to desired joint positions. At each control step, we apply a joint-space PD executor for `control_substeps` =10 simulation substeps: 


where _q_ des is the desired joint configuration, _q_ and _q_ ˙ are the simulated joint position and velocity, and _Kp, Kd_ are the actuator gains from the robot model. 

After rollout, filtering is performed on the executed trajectory rather than on the original kinematic reference. We compute the root height _ht_ and root tilt angle _θt_ from the simulated root pose. A trajectory is rejected if non-finite states occur, or if a fall condition persists for at least 10 consecutive frames. Following the main text, a frame is considered a fall frame when 


For datasets where strict robot feasibility is required, we additionally discard samples whose executed joint positions exceed the G1 joint limits. The remaining samples are kept as tracker-executed training data. 

## **C Details of OMG-DiT** 

### **C.1 Motion Representation and Canonicalization** 

**Motion Representation. OMG-DiT** operates directly in the Unitree G1 motion space, without a learned motion tokenizer or latent autoencoder. Each motion frame is represented by a 125dimensional feature vector 


Here **p** ˜ _i ∈_ R<sup>3</sup> is the root position in a canonical local coordinate frame, ˜ **r** _i ∈_ R<sup>6</sup> is the root orientation represented by the continuous 6D rotation representation [70], **_θ_** _i ∈_ R<sup>29</sup> contains the G1 joint degrees of freedom, and<sup>˜</sup> **j** _i ∈_ R<sup>29</sup><sup>_×_3</sup> contains local positions of non-root body links. This yields a 3 + 6 + 29 + 29 _×_ 3 = 125-dimensional motion vector per frame. 

**Root Rotation Parameterization.** Concretely, a quaternion represents orientation as **q** = ( _qw, qx, qy, qz_ ) _∈_ R<sup>4</sup> with the unit-norm constraint _∥_ **q** _∥_ 2 = 1. An axis-angle (rotation-vector) representation uses **r** = _α_ **u** _∈_ R<sup>3</sup> , where **u** is a unit rotation axis and _α_ is the rotation angle. The 6D representation stores the first two columns of a rotation matrix, **R** 6 _D_ = [ **r** 1 _,_ **r** 2] _∈_ R<sup>6</sup> , and recovers a valid rotation by orthonormalizing these two vectors. We use 6D root rotation features by default. Compared with directly regressing quaternions, the 6D representation avoids unit-norm and sign discontinuities in the network output space; compared with axis-angle vectors, it provides a smooth over-parameterized representation that was empirically more stable during large-scale pretraining. 

**Canonicalization.** For every training sample, the model observes a history window of _L_ = 10 frames and predicts a future horizon of _H_ = 60 frames at 30 FPS. We use the _last history frame_ as the canonical anchor. Concretely, let ( **p** _i,_ **q** _i_ ) denote the world-frame root position and quaternion 

16 

orientation at motion frame _i_ , and let ( **p** _a,_ **q** _a_ ) be the anchor root state. We extract the yaw-only heading quaternion **h** _a_ from **q** _a_ and canonicalize the root trajectory as 


where _⊗_ denotes quaternion rotation or composition depending on whether it is applied to a vector or a quaternion. The canonicalized quaternion **q** ˜ _i_ is then converted to the 6D root rotation feature ˜ **r** _i_ . For each non-root body-link position **j** _i,ℓ_ , we similarly compute 


The resulting canonical features remove arbitrary world-frame placement and heading, while retaining temporal motion trends from the history frames and the full G1 pose information required by the downstream tracker. At inference time, generated local features are decoded back to world-frame G1 states by composing them with the current anchor state. 

As illustrated in Figure 6, before canonicalization, root trajectories are widely scattered in the world frame: their coordinates are dominated by arbitrary global positions and headings, even when the underlying local motion patterns are similar. This creates a highly multi-modal input distribution that forces the model to explain nuisance variation unrelated to the commanded behavior. This motivates us to apply canonicalization. After canonicalization, trajectories collapse into a compact anchor-centered distribution, where remaining variation primarily reflects 


the robot’s local motion dynamics rather than its absolute placement in the scene. This reduces the modeling burden of the diffusion backbone while preserving the temporal motion trend and fullbody pose information required by the downstream tracker. 

**Normalization.** After canonicalization, every feature channel is normalized using training-set statistics: 


where **_µ_** and **_σ_** are computed from the training split. We clamp **_σ_** by a small positive minimum value for numerical stability. The diffusion model is trained and sampled in this normalized feature space, and outputs are denormalized before decoding to G1 joint states. 

### **C.2 Denoising Backbone** 

The generator is implemented as a Diffusion Transformer trained with the **x** -prediction objective. Here **x** denotes the normalized canonical motion feature defined above. Given a corrupted future motion segment **x**<sup>_τ_</sup> _t_ +1: _t_ + _H_<sup>_∈_R</sup><sup>_H×_125,diffusiontimestep</sup><sup>_τ_,recentmotionhistory</sup><sup>**x**</sup><sup>_t−L_:</sup><sup>_t_,anda</sup> subset of available conditioning modalities _Cs ⊆C_ , the denoiser predicts the clean future motion as 


**Architecture.** The denoiser first projects the corrupted future motion features into the Transformer hidden dimension. Each DiT block applies bidirectional temporal self-attention over the _H_ future frames. The recent history **x** _t−L_ : _t_ and the condition subset _Cs_ are encoded into context tokens and injected through cross-attention, while temporally aligned modalities such as audio or human reference motion can additionally be incorporated through frame-wise modulation. We use rotary positional embeddings (RoPE, [71]) for temporal self-attention, sinusoidal embeddings for the diffusion timestep _τ_ , and feed-forward blocks with GELU activations. The final prediction is a sequence 

17 

Table 7: **Architecture variants of OMG-DiT.** To understand the scalability of motion generation, we introduce three variants of the denoising backbone randing from 50M to 500M parameters (B / L / XL), differing in transformer width, depth, and number of attention heads. 

|Model|Params|Hidden Dim.|Layers|Heads|
|---|---|---|---|---|
|**OMG-DiT-B**|50M|512|10|8|
|**OMG-DiT-L**|300M|1152|14|18|
|**OMG-DiT-XL**|500M|1536|13|24|


of normalized clean motion features in the same 125D motion representation in Unitree G1 motion space. We list the architecture specifications for **OMG-DiT-B / L / XL** in Table 7. All variants share the same motion representation, diffusion objective, and conditioning interface architecture; they differ only in Transformer width, depth, and number of attention heads. 

**Denoising Objective and Sampling.** We train the model to predict the clean future motion **x** 0 from a noisy future trajectory. We use discrete diffusion timesteps with a cosine noise schedule. Given a clean normalized future sequence **x** 0, timestep _τ_ , and Gaussian noise **_ϵ_** , the noisy input is 


At inference time, we use DDIM [72] sampling with 50 denoising steps and _η_ = 0. The default global guidance scale is 2.5 when a single guidance scale is used. For composed modalities, modality-specific scales can be set separately as described in Section C.5. 

### **C.3 Omni-Modal Condition Encoders** 

We provide details on condition encoders for different modalities in **OMG-DiT** . 

**Motion History.** The 10-frame motion history is first canonicalized and normalized using the same feature statistics as the future target. A two-layer MLP maps each history frame to the Transformer hidden dimension. The resulting history tokens are appended to the global context token sequence and interact with generated motion latents through per-block cross-attention layers. 

**Language.** Text annotations are encoded by a frozen T5-Base [50] encoder with maximum length 50. The T5 language embeddings are projected into the transformer hidden dimension and injected as global context tokens alongside motion history through cross-attention. During training, text conditioning is randomly dropped with probability 0.3. 

**Audio.** Audio is encoded as frame-aligned 35D acoustic features. Given a raw waveform, we first average stereo channels to mono and peak-normalize the signal. For audio sample rate _s_ and motion frame rate _f_ = 30 Hz, the hop size is 


and each audio frame uses a Hann window of length 


corresponding to at least a 50 ms analysis window. The feature vector at motion frame _i_ is extracted from the waveform segment starting at sample _ih_ and is defined as 


Here **e**<sup>1:32</sup> _i_ are 32 log FFT band energies computed by splitting the magnitude spectrum into 32 bands and normalizing by the maximum band energy within the same frame, rms _i_ is root-meansquare energy, zcr _i_ is zero-crossing rate, flux _i_ is spectral flux from the previous audio frame, and centroid _i_ is the normalized spectral centroid. Audio features are trimmed or zero-padded to the motion horizon, with a validity mask for padded frames. During training, these features are stored 

18 

offline as `.npy` arrays; at inference time, the same extractor can also be applied to raw WAV input before planning. The 35D features are passed through a LayerNorm and projected by an MLP into the denoiser hidden dimension. Since audio is temporally aligned with the future motion horizon, we inject it as a frame-wise condition using per-layer FiLM modulation. Audio conditioning is randomly dropped with probability 0.1 during training. 

**Human Reference Motion.** We represent human reference motions as 66D frame-aligned features, corresponding to 22 human joints in 3D space. As with audio, the human reference signal is projected by an MLP and injected through per-layer FiLM modulation at the corresponding motion frame. Human-reference conditioning is randomly dropped with probability 0.5 during training. 

For samples where a modality is unavailable, we set its availability mask to false. The mask gates the corresponding condition encoder and modulation, so the denoiser receives no conditioning signal from that modality. The same mechanism is used for modality dropout during training, allowing one shared model to train on heterogeneous datasets with different subsets of available conditions. 

### **C.4 Adapting to New Modalities** 

**OMG-DiT** is designed so that new control modalities can be included while preserving as much of the pretrained motion prior as possible. During adaptation, we reuse the pretrained denoising backbone and add new modalities with lightweight encoders. 

For global conditioning signals, such as visual features for perceptive locomotion, the encoded tokens are appended to the cross-attention context, following the same interface as language and history tokens. For frame-aligned signals, such as Pico sparse keypoints for teleoperation, the encoded features are injected into each denoising block through lightweight adapters. In our implementation, these adapters can be per-layer FiLM modules or AdaLN-style modulation modules. The final linear layer of each newly added adapter is initialized to zero, so the adapter initially outputs no modulation and the pretrained generator’s function is preserved at the start of finetuning. 

This non-invasive initialization makes sample-efficient finetuning practical. The default adaptation setting trains the new modality encoder and its adapters while reusing the pretrained motion backbone. In our experiments, we use full finetuning across all backbone parameters, but parameterefficient finetuning may also be feasible for simple tasks. 

### **C.5 Classifier-Free Guidance and Composition** 

**Classifier-Free Guidance and Multi-Modal Composition.** We train with modality dropout and use classifier-free guidance at inference time. For a single condition, the denoiser prediction is guided by comparing a conditional branch with a null-condition branch. For composed conditions, we additionally support modality-specific guidance branches. Given text, audio, and humanreference conditions, the guided prediction can be written as 


where ˆ **x**<sup>∅</sup> 0<sup>is the null-condition prediction and</sup><sup>_ω_text,</sup><sup>_ω_audio, and</sup><sup>_ω_human are modality-specific guid-</sup> ance scales. By composing the guidance directions from different modalities, **OMG-DiT** enables zero-shot composition of command combinations previously unseen during training. 

**Practical Implementation.** We instantiate classifier-free guidance in two ways during inference. If only a single global scale _ω_ is specified, we use a full-condition branch: 


where **x** ˆ<sup>all</sup> 0<sup>is predicted with all available external modalities unmasked.If modality-specific scales</sup> are specified, we use separate guidance branches instead of a full-condition branch. 

Unless otherwise specified, we use global scale _ω_ = 2 _._ 5 for single-modality motion generation. For composed audio-language generation, we use _ω_ text = 3 _._ 0 and _ω_ audio = 1 _._ 5, giving text a stronger 

19 

semantic prior while retaining audio rhythm. For human-reference conditioning, we use _ω_ human = 2 _._ 0. Intuitively, increasing _ω_ text favors semantic instruction following, whereas increasing _ω_ audio favors rhythmic and dance-style adherence. We provide further visualizations in Appendix E.4. 

**Extending Classifier-Free Guidance to New Modalities.** Classifier-free guidance extends naturally to newly added modalities. We construct a null branch and a modality-specific conditional branch for the new signal, and use 


where _ω_ new is the guidance scale for the new modality. This branch can be combined with the existing modalities, enabling new control interfaces to be participate in compositional generation. 

### **C.6 Real-Time Deployment** 

To enable real-time inference, we use a combination of existing runtime acceleration methods, including ONNX/TensorRT export, FP16 precision, and DiT caching [73]. We provide runtime analysis and additional details in Appendix E.1. At deployment, the motion tracker runs onboard on the NVIDIA Orin chip, while the motion generator runs on an off-board NVIDIA RTX 4090 workstation connected to the robot through a wired Ethernet link. 

### **C.7 Training Hyperparameters** 

We summarize key training hyperparameters for pretraining in Table 8. We train in mixed bfloat16 precision with the AdamW optimizer [74], and apply standard techniques including gradient clipping, a linear-warmup cosine-decay learning-rate schedule, and weight decay. Training is completed on 8 NVIDIA A800 GPUs in under 10 hours. 

Table 8: **Hyperparameters for OMG-DiT Pretraining.** Unless otherwise specified, evaluation is conducted on the **-L** <u>(300M) version of the model.</u> 

|**Hyperparameter**|**Value**|
|---|---|
||**Motion Setup**<br>|
|Prediction / history length|60 / 10 frames|
|Motion frame rate|30 FPS|
|Motion representation|125D G1 features with 6D root rotation|
||**Optimization**|
|Optimizer|AdamW|
|Learning rate|6_._0_×_10<sup>_−_5</sup>|
|Weight decay|0_._01|
|LR schedule|Linear warmup, cosine decay|
|Warmup steps|2_,_000|
|Minimum LR|1_._0_×_10<sup>_−_6</sup>|
|Gradient clipping|Global norm1_._0|
||**Training**|
|Max training steps|100_,_000|
|Precision|bf16 mixed precision|
|GPUs|8|
|Per-GPU batch size|128|
|Global batch size|1,024|
||**Inference**|
|Method|DDIM|
|NFE calls|50|


20 

## **D Experiment Details** 

### **D.1 Evaluation Protocols** 

We provide details on evaluation protocols shared across different experiments, including the evaluated tasks, motion format, and data splits. Unless otherwise stated, all experiments follow these defaults. 

### **D.1.1 Evaluated Tasks and Motion Format** 

**Evaluated Tasks.** We evaluate six tasks: text-to-motion, audio-to-motion, human reference-tomotion, Pico keypoint-based teleoperation, text-to-motion finetuning, and perceptive locomotion. Although the conditions differ, all methods output Unitree G1 motion in the same G1 qpos space, making different methods and baselines directly comparable. 

**Motion Format.** Each robot frame is represented by a 36D qpos vector in G1 motion space: 


where **x**<sup>root</sup> _t ∈_ R<sup>3</sup> , **r**<sup>root</sup> _t ∈_ R<sup>4</sup> , and **q**<sup>joint</sup> _t ∈_ R<sup>29</sup> denote root position, root quaternion, and G1 joint DOFs. A sequence of length _T_ is **q** _∈_ R<sup>_T ×_36</sup> . For body-level metrics, we use forward kinematics: 


where the 90 dimensions are 3D positions of 30 G1 body/joint points. For baselines whose native outputs are not G1 qpos, such as SMPL-X, SMPL/SMPL-H motion, SMPL pickle files, or dance motion arrays, we first convert or retarget them to G1 qpos and then use the same evaluation pipeline. 

### **D.1.2 Evaluation Data Settings** 

**Evaluation Data Split.** Evaluations are performed on validation splits. The default generated sequence has 60 frames at 30 FPS. Generated motions are stored as G1 qpos, and body-level metrics are computed from FK-derived 90D body positions. 

Table 9: **Evaluation data and sampling settings.** 

|Task|Evaluation data|# samples|
|---|---|---|
|Text-to-motion|Caption-bearing validation samples|1024|
|Audio-to-motion|Validation samples with audio/music features|512|
|Human reference-to-motion|Validation samples with human reference motion|512|
|Pico teleoperation|AMASS (CMU + WEIZMANN), with Pico keypoints|512|
|Text-to-motion finetuning|AMASS (CMU + WEIZMANN), with captions|1024|


As shown in Table 9, for text-to-motion, we sample 1024 caption-bearing validation conditions without replacement. R-precision uses batch size 32, giving 32 retrieval batches, and constructs candidates by dataset-stratified reordering. FID reference motions are sampled from real data; if the reference count is unspecified, it equals the generated sample count. AMASS CMU and WEIZMANN are used only for text-to-motion finetuning and Pico teleoperation from-scratch/finetuning experiments, and held out during pretraining, to avoid data leakage. 

### **D.2 Evaluation Metrics** 

In this section, we provide an overview of metrics used during evaluation, including general metrics shared across experiments and specific metrics for text-to-motion and audio-to-motion experiments. We additionally provide details on evaluator training for text-to-motion evaluation. 

21 

### **D.2.1 Shared Evaluation Metrics** 

We use the same set of metrics for evaluating physical plausibility, reconstruction error relative to reference motion, and tracker execution failures across experiments, as shown in Table 10. Here **p**<sup>_pred_</sup> and **p**<sup>_ref_</sup> are predicted and reference G1 body positions, and **p** ˜ is the root-relative position. Velocity and acceleration are computed as first- and second-order finite differences of body positions. 

**v** _b,t,j_ = **p** _b,t_ +1 _,j −_ **p** _b,t,j,_ **a** _b,t,j_ = **p** _b,t_ +2 _,j −_ 2 **p** _b,t_ +1 _,j_ + **p** _b,t,j._ (19) 

For c-slide, _C_ is the set of valid foot-contact intervals and _Sf_ contains sole proxy points for foot _f_ . Fall Rate is determined by root height and tilt. For J-Limit, _ei,t,j_ is the joint-limit violation magnitude and _ϵ_ = 10<sup>_−_4</sup> . 

Table 10: **Shared Evaluation Metrics.** 

|Metric|Formula|Description|
|---|---|---|
|c-slide|1<br>_|C|_<br>�<br>(_t,f_)_∈C_ <sup>max</sup><sup>_p∈S_</sup>_f _<sup>_∥_</sup><sup>**s**</sup><sup>_xy_</sup><br>_t_+1_,p _<sup>_−_</sup><sup>**s**</sup><sup>_xy_</sup><br>_t,p_<sup>_∥_2</sup> <sup>_· f_fps</sup><br><br>|Horizontal foot sliding speed during contact|
|Jerk|1<br>_|V|_<br>�<br>(_t,j_)_∈V_<sup>_∥_</sup><sup>**p**</sup><sup>_t_+3</sup><sup>_,j −_3</sup><sup>**p**</sup><sup>_t_+2</sup><sup>_,j_ + 3</sup><sup>**p**</sup><sup>_t_+1</sup><sup>_,j −_</sup><sup>**p**</sup><sup>_t,j∥_2</sup><sup>_· f_ 3</sup><br>fps<br><br><br>|Third-order motion variation|
|g-MPJPE|1000_·_<br>1<br>_BT J_<br>�<br>_b,t,j_<sup>_∥_</sup><sup>**p**</sup><sup>_pred_</sup><br>_b,t,j _<sup>_−_</sup><sup>**p**</sup><sup>_ref_</sup><br>_b,t,j_<sup>_∥_2</sup><br><br><br>|Global body position error in mm|
|MPJPE|1000_·_<br>1<br>_BT J_<br>�<br>_b,t,j_<sup>_∥_˜</sup><sup>**p**</sup><sup>_pred_</sup><br>_b,t,j _<sup>_−_˜</sup><sup>**p**</sup><sup>_ref_</sup><br>_b,t,j_<sup>_∥_2</sup><br><br><br>|Root-relative body position error in mm|
|e-vel|1000_·_<br>1<br>_B_(_T −_1)_J_<br>�<br>_b,t,j_<sup>_∥_</sup><sup>**v**</sup><sup>_pred_</sup><br>_b,t,j _<sup>_−_</sup><sup>**v**</sup><sup>_ref_</sup><br>_b,t,j_<sup>_∥_2</sup><br><br><br>|Velocity error in mm/frame|
|e-acc|1000_·_<br>1<br>_B_(_T −_2)_J_<br>�<br>_b,t,j_<sup>_∥_</sup><sup>**a**</sup><sup>_pred_</sup><br>_b,t,j _<sup>_−_</sup><sup>**a**</sup><sup>_ref_</sup><br>_b,t,j_<sup>_∥_2</sup><br><br>|Acceleration error in mm/frame<sup>2</sup>|
|Fall Rate|1<br>_N_<br>�_N_<br>_i_=1 <sup>I[sequence</sup>_i_ <sup>fallen]</sup><br><br>|Sequence-level fall rate|
|J-Limit|1<br>_N_<br>�_N_<br>_i_=1 <sup>I[max</sup><sup>_t,j ei,t,j > ϵ_]</sup>|Sequence-level joint-limit violation rate|


### **D.2.2 Text-to-Motion Metrics** 

For text-to-motion, we additionally evaluate text-motion alignment and the generated motion distribution. Each generated G1 qpos is converted via FK to 90D body positions, encoded as a motion embedding, and compared with the corresponding text embedding. We report Matching Score, R- precision, FID, and Diversity, as shown in Table 11. 

Table 11: **Text-to-motion metrics.** 

|Metric|Formula|Description|
|---|---|---|
|Matching Score|1<br>_N_<br>�_N_<br>_i_=1<sup>_∥_</sup><sup>**m**</sup><sup>_i −_</sup><sup>**t**</sup><sup>_i∥_2</sup><br><br>|Average distance between paired text-motion embeddings|
|R-precision@K|1<br>_N_<br>�_N_<br>_i_=1 <sup>I[rank</sup><sup>_i_(</sup><sup>_i_)</sup><sup>_≤K_]</sup><br><br>|Whether the ground-truth text is in the top-_K_ retrieval results|
|FID|_∥_**_µ_**_r −_**_µ_**_g∥_<sup>2</sup><br>2 <sup>+ Tr(</sup><sup>**Σ**</sup><sup>_r_</sup> <sup>+</sup><sup>**Σ**</sup><sup>_g_</sup> <sup>_−_2(</sup><sup>**Σ**</sup><sup>_r_</sup><sup>**Σ**</sup><sup>_g_)1</sup><sup>_/_2)</sup><br>|Fréchet distance between real and generated motion embeddings|
|Diversity|1<br>_|P|_<br>�<br>(_a,b_)_∈P_<sup>_∥_</sup><sup>**m**</sup><sup>_a −_</sup><sup>**m**</sup><sup>_b∥_2</sup>|Average embedding distance between generated samples|


Here **m** _i_ and **t** _i_ are motion and text embeddings, and _N_ is the number of samples. For R-precision, candidate texts are ranked by 


and rank _i_ ( _i_ ) is the rank of the paired text. We report _R_ @1, _R_ @2, and _R_ @3. For FID, ( **_µ_** _r,_ **Σ** _r_ ) and ( **_µ_** _g,_ **Σ** _g_ ) are the empirical mean and covariance of real and generated motion embeddings. For Diversity, _P_ contains randomly sampled generated embedding pairs; we use 300 pairs by default. 

### **D.2.3 Audio-to-Motion Metrics** 

Specific audio-to-motion metrics evaluate beat alignment and compare generated and real motions using kinetic and geometric statistics. 

Here _B_<sup>_a_</sup> is the music beat set and _di_ is the distance from music beat _i_ to the nearest motion beat. The Gaussian kernel width is _σ_ = 3 _/f_ fps, with _f_ fps = 30. FID-k uses kinetic features, FID-g uses geometric features, and PFC uses left/right foot sliding _Lt, Rt_ with normalized root upward acceleration _A_<sup>ˆ</sup> _t_ . 

22 

Table 12: **Audio-to-motion metrics.** 

|Metric|Formula|Description|
|---|---|---|
|Beat Align|1<br>_|B_<sup>_a_</sup>_|_<br>�<br>_i_ <sup>exp(</sup><sup>_−d_2</sup><br>_i _<sup>_/_(2</sup><sup>_σ_2))</sup>|Temporal alignment between music and motion beats|
|FID-k|_∥_**_µ_**_k,r −_**_µ_**_k,g∥_<sup>2</sup><br>2 <sup>+ Tr(</sup><sup>**Σ**</sup><sup>_k,r_</sup> <sup>+</sup><sup>**Σ**</sup><sup>_k,g_</sup> <sup>_−_2(</sup><sup>**Σ**</sup><sup>_k,r_</sup><sup>**Σ**</sup><sup>_k,g_)1</sup><sup>_/_2)</sup><br><br>|Fréchet distance over kinetic features|
|FID-g|_∥_**_µ_**_geo,r −_**_µ_**_geo,g∥_<sup>2</sup><br>2 <sup>+ Tr(</sup><sup>**Σ**</sup><sup>_geo,r_</sup> <sup>+</sup><sup>**Σ**</sup><sup>_geo,g_</sup> <sup>_−_2(</sup><sup>**Σ**</sup><sup>_geo,r_</sup><sup>**Σ**</sup><sup>_geo,g_)1</sup><sup>_/_2)</sup><br><br><sup>ˆ</sup>|Fréchet distance over geometric features|
|PFC|10000_·_<br>1<br>_T −_2<br>�<br>_t _<sup>_LtRt_ </sup><sup>_At_</sup>|Penalizes foot sliding during root upward acceleration|


### Table 13: **Motion Evaluator architecture used for evaluation.** 

|Stage|Architecture|Output|
|---|---|---|
|Movement encoder|Linear + LayerNorm + GELU + Dropout|Per-frame feature|
|Hidden projection|Linear or Identity|Hidden sequence|
|Temporal encoder|RoPE Transformer|Temporal feature sequence|
|Pooling/projection|Mean pooling + MLP projection|Motion embedding|
|Normalization|L2 normalization|Unit-norm embedding|


### **D.2.4 Details on Evaluator Training for Text-to-Motion Evaluation** 

Text-to-motion embedding metrics use a separately trained text-motion evaluation encoder, following a CLIP-style contrastive retrieval protocol with symmetric InfoNCE loss. The evaluator is used only for evaluation and is not part of the generator. It contains a motion encoder and a text encoder that map motions and texts into a shared embedding space. We provide architecture details and key hyperparameters for evaluator training in Table 13 and Table 14, respectively. 

Table 14: **Hyperparameters for Text-to-Motion Evaluator Training.** 

|Hyperparameter|Value|
|---|---|
|Motion input dim|90|
|Movement dim|512|
|Hidden dim|512|
|Output dim|512|
|Transformer layers|4|
|Attention heads|8|
|MLP ratio|4|


The text encoder consists of a pretrained frozen T5-3B encoder followed by a trainable linear projection to the shared embedding space, where T5-3B denotes a T5 encoder with approximately 3 billion parameters. For sample _i_ , the motion encoder takes the FK-derived 90D body-position sequence and the text encoder takes the corresponding text: 


where **p** _i ∈_ R<sup>_T ×_90</sup> , **c** _i_ is the text condition, and **m** _i,_ **t** _i_ are motion and text embeddings. 

The two encoders are trained with symmetric InfoNCE: 


where 


_Lt→m_ is symmetric. Here _B_ is the batch size, _τ_ is temperature, and sim( _·, ·_ ) is embedding similarity. 

For standard text-to-motion evaluation, the encoder is trained on the full train split and evaluated on the validation split. For finetuning, it is trained and evaluated only on AMASS CMU and WEIZMANN, which are excluded from regular pretraining. 

23 

### **D.3 Details of Evaluation Baselines** 

We compare against a wide variety of baselines from both the graphics and humanoid communities. For motion generation baselines in graphics, we use GMR [42] to retarget the generated human poses into G1 motion space. 

### **D.3.1 Text-to-Motion Baselines** 

We compare against state-of-the-art motion generation baselines, including GENMO [25], HYMotion [57], and Kimodo [26]. For Kimodo, we compare against variants trained with different datasets, including Bones Seed and Bones Rigplay, as well as generation in SMPL-X space or G1 space. All final outputs are evaluated as G1 `qpos_36` . These baselines operate in a full-sequence manner, generating in advance instead of interactively in real time. 

Table 15: **Text-to-motion Baselines.** 

|Baseline|Original output space|Conversion to G1|Final artifact|
|---|---|---|---|
|GENMO [25] + GMR|SMPL-X motion|GMR retargeting|G1`qpos_36`|
|HYMotion [57] + GMR|SMPL/SMPL-H style motion|Convert to SMPL-X, then GMR|G1`qpos_36`|
|Kimodo-SMPLX-RP-v1 [26] + GMR|SMPL-X motion|GMR retargeting|G1`qpos_36`|
|Kimodo-G1-RP-v1 [26]|G1 qpos|Direct use|G1`qpos_36`|
|Kimodo-G1-SEED-v1 [26,43]|G1 qpos|Direct use|G1`qpos_36`|


### **D.3.2 Audio-to-Motion Baselines** 

For audio-to-motion baselines, we compare against motion generation models that can condition on multiple modalities, i.e. GENMO [25], as well as single-purpose state-of-the-art audio-to-motion generation baselines, such as LODGE [58] and Bailando++ [59]. Their outputs are first converted to G1 qpos with GMR [42] and then evaluated with audio-motion and physical metrics. Specifically, GENMO [25] + GMR directly generates SMPL-X motion and retargets it to G1. LODGE [58] and Bailando++ [59] are first converted to SMPL/SMPL-X-compatible representations and then retargeted. After conversion, all baselines share the same G1 qpos evaluation. 

Table 16: **Audio-to-motion Baselines.** 

|Baseline|Condition input|Original output|Conversion to G1|Final artifact|
|---|---|---|---|---|
|GENMO [25] + GMR|Raw audio/music embedding|SMPL-X motion|GMR retargeting|G1`qpos_36`|
|LODGE [58] + GMR|Music feature`.npy`|Dance motion array|Convert to SMPL/SMPL-X, then GMR|G1`qpos_36`|
|Bailando++ [59] + GMR|Raw audio/extracted feature|SMPL pickle|Convert to SMPL-X, then GMR|G1`qpos_36`|


### **D.3.3 Human Reference-to-Motion Baselines** 

We represent the human reference using the 3D coordinates of 22 human joints, i.e., 


This is essentially a _retargeting_ problem, in which motion in human motion space is retargeted to G1 motion space. Here, we compare against well-established optimization-based retargeting methods, including GMR [42], PHC [61], and OmniRetarget [62], as well as the recently proposed learningbased method NMR [60]. 

Table 17: **Human reference-to-motion Baselines.** 

|Baseline|Type|Intermediate representation|Final artifact|
|---|---|---|---|
|GMR [42]|Geometric/rule-based retargeting|Compact SMPL-X motion|G1`qpos_36`|
|PHC [61]|Physics/fitting-based retargeting|AMASS-style SMPL motion|G1`qpos_36`|
|OmniRetarget [62]|Optimization-based retargeting|Holosoma-compatible SMPL-X motion|G1`qpos_36`|
|NMR [60]|Learned retargeting model|Standard SMPL-X motion|G1`qpos_36`|


24 

### **D.4 Details on Finetuning and Scaling Experiments** 

**Datasets and Evaluation Splits.** We use the AMASS CMU and WEIZMANN subsets for textto-motion finetuning and Pico teleoperation from-scratch/finetuning comparisons. To avoid leakage, these subsets are excluded from pretraining and used only for these experiments and evaluations. For scaling experiments, we pretrain on the exact **OMG-Data** pretraining corpus. For sample-efficient finetuning with varying percentages of included data, data are controlled at the slice level. Each annotated motion segment is exhaustively sliced with a 2-second window at 30 FPS, so each slice has 60 frames and the full candidate slice pool is materialized. We shuffle this pool with a fixed random seed and keep the first specified percentage as the training set. 

**Setup.** We compare finetuning and from-scratch training under the same model size and split. Finetuning initializes from **OMG-DiT-L** , the 300M pretrained checkpoint. The from-scratch setting uses the same architecture with randomly initialized parameters. For the model-parameter scalinglaw experiment, we vary only the model size and keep all other hyperparameters unchanged. 

We additionally include an adaptation experiment for perceptive locomotion in Appendix E.5. 

## **E Extended Experiments and Visualizations** 

We include additional experiments and visualizations in this section. We provide runtime acceleration analysis, extended visualizations on real-time omni-modal control, finetuning experiments on perceptive locomotion tasks, and analysis of classifier-free guidance. 

### **E.1 Runtime Acceleration Analysis** 

We report speedups from different inference optimization techniques for **OMG-DiT-B** in Table 18. Performance is measured on a text-conditioned 60-frame future chunk at 30 FPS, corresponding to a two-second planning horizon, on a single NVIDIA A800 GPU. 

Table 18: **Runtime Acceleration Analysis.** Inference time is measured while generating a 60frame future chunk with text conditioning, running **OMG-DiT-B** on a single NVIDIA A800 GPU. We report the mean and standard deviation over five steady-state runs. 

|Optimization|Sampling (ms)|Denoiser infer (ms)|NFE (calls)|Speedup|
|---|---|---|---|---|
|PyTorch eager|1297.9_±_12.5|1265.0_±_12.4|100 (100)|1.0_×_|
|+`torch.compile`|467.9_±_2.9|435.6_±_2.8|100 (100)|2.8_×_|
|+ ONNX Runtime CUDA|358.2_±_24.2|337.0_±_22.7|100 (50)|3.6_×_|
|+ TensorRT engine|127.3_±_7.3|100.9_±_4.3|100 (50)|10.2_×_|
|+ TensorRT FP16|99.8_±_5.2|73.3_±_5.2|100 (50)|13.0_×_|
|+ DiT cache|51.7_±_1.5|31.2_±_1.3|38 (19)|25.1_×_|


Sampling time refers to the total time from receiving cached condition tensors to outputting future motion predictions, while Denoiser infer denotes the forward-pass time inside the sampler. NFE counts conditional/null CFG branch predictions; values in parentheses report backend forward calls after CFG parallelism. 

### **E.2 Extended Visualizations on Real-Time Omni-Modal Control** 

We provide extended qualitative visualizations on real-time omni-modal control. Motions are generated by the same pretrained model in real time, with conditions unseen during training. As shown in Figure 7, **OMG** generates diverse and robot-executable motions conditioned on various signals, showcasing strong capabilities as a foundation model for generalist humanoid control. 

25 


Figure 7: **Qualitative visualization.** Unitree G1 execution sequences produced by **OMG** under text, audio, human-reference, and composed text-audio conditions. Frames are uniformly sampled within each sequence, and embedded prompts are preserved. 

26 


Figure 8: **Interactive Control: Composition in the Temporal Horizon.** 

### **E.3 Interactive Control with Temporal Composition** 

We showcase our model’s capability for real-time _interactive_ control. We feed the model timevarying commands from different modalities over the temporal horizon. As shown in Figure 8, **OMG** follows local temporal conditions while maintaining smooth transitions between conditions. 

### **E.4 Analysis on Classifier-Free Guidance** 

In this section, we focus on answering the following questions: 

1. For single-modality conditioning, does classifier-free guidance improve instruction following? How does the scale of classifier-free guidance affect performance? 

2. For compositional modality conditioning, does increasing the guidance scale for one modality steer the behavior toward better alignment with instructions in that modality? 

**Single-Modality Classifier-Free Guidance.** We aim to understand whether classifier-free guidance improves the instruction-following capability of **OMG** through the lens of human-reference conditioning. As shown in Figure 9, increasing the guidance scale for human-reference motion makes the generated motion more aligned with the reference, with the effect becoming more pronounced over longer horizons. We further measure MPJPE and g-MPJPE between the generated motion and ground truth under varying guidance scales. As shown in Table 19, moderate guidance improves alignment, whereas overly strong guidance hurts performance. 

27 


Figure 9: **Human-reference CFG sweep.** The translucent reference overlay shows the target motion, and the opaque robot shows the generated motion. 

Table 19: **Human-reference CFG sweep.** We report MPJPE and g-MPJPE under varying classifierfree guidance scales for human-reference motion across different rollout lengths. MPJPE and g- MPJPE are reported in millimeters; lower is better. 

|Human CFG|MPJPE|g-MPJPE|1s|3s|5s|7s|9s|
|---|---|---|---|---|---|---|---|
|0.5|190.3|557.0|62.7|407.2|236.1|213.2|91.5|
|1.0|96.6|261.8|42.9|59.3|117.3|144.0|216.6|
|1.5|74.0|218.9|38.5|51.6|108.9|93.2|139.2|
|2.0|71.0|343.9|38.3|60.4|109.5|82.6|73.4|


**Multi-Modality Classifier-Free Guidance.** Next, we study the effects of guidance under multimodal conditioning. As shown in Figure 10, we compose text and audio conditions: the audio condition specifies the dance rhythm, while the language condition asks the robot to raise its hands. Increasing the text guidance scale strengthens semantic alignment to the language instruction while preserving the audio-conditioned temporal structure. 

### **E.5 Adaptation to New Modalities: Perceptive Locomotion** 

**Task and Environment.** We evaluate whether the pretrained motion prior can be adapted to a new egocentric visual control task. We place three adjacent, differently colored square targets in front of the robot. The robot receives an egocentric RGB observations from a mounted camera and categorical target-color commands, and asked to locomote to the commanded square. 

**Training Data.** We leverage Kimodo [26] to generate demonstrations in advance, using its capability to condition on 2D paths. We collect 300 episodes per target color. Each episode contains 210 frames at 30 Hz, corresponding to roughly 7 s of source motion, and includes an appended 

28 


Figure 10: **Text-audio CFG sweep.** Columns show snapshots over time and rows vary the text guidance scale while keeping the audio condition fixed. Larger text guidance improves adherence to the language instruction in the composed audio-language setting. 


Figure 11: **Perceptive Locomotion setup.** The dataset contains 300 Kimodo-generated demonstrations per target color. The policy observes only low-resolution egocentric RGB and a discrete color command. The goal is to follow the command and locomote to the corresponding color. 

target-hold segment so that the reference motion stops after reaching the target. To train the diffusion model, we sample 2 s windows using the same G1 state representation as the motion-generation model. The visual input is the current mounted-camera RGB frame resized to 64 _×_ 64 and encoded as RGB patches. For fair comparison, we disable the language prompt and instead inject the target as a learned categorical color embedding for {yellow, blue, red}. 

**Model and Training Details.** We compare two initializations under the same architecture and optimization hyperparameters. The _scratch_ model is randomly initialized, while the _pretrained_ model initializes the motion backbone from the 300M mixed-modality **OMG-DiT-L** . The newly introduced RGB patch encoder, visual cross-attention, and target-color embedding are trained in both cases. The visual patch gate is initialized to 0 _._ 05 so that visual conditioning is active from the start of finetuning. Both models are trained on one GPU with a local batch size of 16, and a learning rate of 6 _×_ 10<sup>_−_5</sup> . 

29 

Table 20: **Success Rate on Perceptive Locomotion.** We report success rate over 90 rollouts. 

|Initialization|Step|Success Rate|
|---|---|---|
|Scratch|500|44/90 (48.9%)|
|Pretrained|500|**53/90 (58.9%)**|


Figure 12: **Third-person timelapse of a successful rollout by the pretrained checkpoint.** The robot enters the commanded blue target. 

**Evaluation and Results.** At test time, we use online replanning from a canonical standing G1 state. Each replan samples a 2 s motion window, executes the first 0.5 s, and then replans from the updated state; the rollout budget is 210 source frames. We evaluate 30 held-out validation rollouts per target color, for 90 rollouts per checkpoint. Because this experiment is intended to measure whether the model can visually ground the target, we measure success as follows: a rollout succeeds if, at some time in the trajectory, the root/pelvis horizontal position lies within the commanded target square during execution. As shown in Table 20, pretraining yields a higher success rate than training from scratch, showing that the pretrained motion prior transfers positively to new scenarios. 

30 

