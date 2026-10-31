---
title: "VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling"
date: "2025-12-02"
authors: "Weiqi Li; Quande Zhang; Ruifeng Zhai; Liang Lin; Guangrun Wang"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.02902
pdf: https://arxiv.org/pdf/2512.02902
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.02902)** / [論文ページ](https://arxiv.org/abs/2512.02902)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling** 

Weiqi Li<sup>1</sup> Quande Zhang<sup>1</sup> Ruifeng Zhai<sup>1</sup> Liang Lin<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup> Guangrun Wang<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_,∗_</sup> 1Sun Yat-sen University 2Guangdong Key Laboratory of Big Data Analysis and Processing 3X-Era AI Lab 

liwq229@mail2.sysu.edu.cn, zhangqd8@mail2.sysu.edu.cn, wanggrun@gmail.com 


Figure 1. **Illustration of Spatial Modeling Adaptation.** (a) Our two proposed one-shot adaptation methods—Feature Token Modulation (FTM) and Feature Linear Adaptation (FLA)—which adapt visual representations to new spatial domains. After adaptation, all multimodal tokens are processed by the pretrained VLM and action expert to generate the final policy. (b) Parameter efficiency versus performance on the LIBERO benchmark under novel viewpoints. Our model exceeds the average success rate of the _π_ 0 _._ 5 (LoRA) baseline while using only 4.7M parameters compared to 467M. 

## **Abstract** 

_to restore viewpoint generalization._ 

_Vision-language-action (VLA) models achieve strong indistribution performance but degrade sharply under novel camera viewpoints and visual perturbations. We show that this brittleness primarily arises from misalignment in Spatial Modeling, rather than Physical Modeling. To address this, we propose a one-shot adaptation framework that recalibrates visual representations through lightweight, learnable updates. Our first method, Feature Token Modulation (FTM), applies a global affine transformation to visual tokens and improves Libero viewpoint accuracy from 48.5% to 87.1% with only 4K parameters. Building on this, Feature Linear Adaptation (FLA) introduces low-rank updates to the ViT encoder, achieving 90.8% success with 4.7M parameters—matching LoRA-scale finetuning at far lower cost. Together, these results reveal substantial untapped robustness in pretrained VLA models and demonstrate that targeted, minimal visual adaptation is sufficient_ 

> *Corresponding author: Guangrun Wang. 

## **1. Introduction** 

Recent advances in vision-language-action (VLA) models have significantly advanced the field of embodied intelligence. By extending pretrained vision-language foundations [5, 7, 12, 15, 17, 19, 28, 43] to robotic control, these models can interpret visual observations and follow natural language instructions across diverse manipulation tasks [2, 3]. Pretraining on large-scale and varied robot datasets [5, 14, 30] has led to strong in-domain performance, demonstrating the potential of languageconditioned visual grounding for general-purpose robots. 

However, robustness and generalization remain critical challenges [18, 21, 33, 34, 36, 39, 42]. Despite large and diverse training corpora, VLA models often fail to generalize to out-of-distribution scenarios, exhibiting pronounced degradation when exposed to unseen camera viewpoints, lighting changes, or scene perturbations [8, 47]. Such brit- 

35025 

tleness limits their applicability in real-world environments, where visual conditions are inherently dynamic and unpredictable [4]. 

Existing approaches to improving VLA robustness can be broadly categorized into data-centric and representationcentric paradigms. Data-centric approaches seek to enhance robustness by increasing visual diversity, typically through large-scale, multi-view robotic datasets such as Libero-Plus [8]. Although this strategy exposes models to a wider range of visual conditions, scaling data collection to real-world settings remains costly and labor-intensive, making continual adaptation impractical. In contrast, representation-centric approaches aim to achieve robustness through geometric consistency, learning geometry-aware or 3D-consistent representations [1, 23, 31, 35, 38]. By leveraging multi-view supervision [31] or specialized 3D-aware architectures [1], these methods improve viewpoint invariance. However, despite being geometry-aware, these methods remain sensitive to task-irrelevant visual factors such as background clutter and illumination changes [31], highlighting a persistent gap between viewpoint robustness and general visual adaptability. Prior methods implicitly assume that robustness requires additional data or 3D-consistent architectures, yet few works explicitly identify whether the failure actually arises from the spatial representation itself. 

To investigate this question, motivated by recent discussions on the limitations of visual spatial reasoning in VLAs [1, 24, 41], we propose a conceptual framework that decomposes a VLA model into two components (see Fig.1(a)): (1) **Spatial Modeling** , implemented by the visual encoder, which constructs spatial relationships between objects—such as positions, orientations, contact relations, and occlusion structure—from the image, producing the spatial representations required for downstream tasks; (2) **Physical Modeling** , implemented by the VLM and the action expert, which integrates the task language, spatial representations, and action history to perform high-level reasoning and generate executable action sequences. A viewpoint shift primarily alters the spatial configuration of the observed scene, rather than the underlying task semantics or action dynamics. This suggests that the degradation of VLA performance under viewpoint changes is largely due to misalignment in Spatial Modeling, while the Physical Modeling components remain functionally competent. In other words, the highlevel policy still retains its reasoning and control capability, but receives spatially distorted visual embeddings, leading to failures in downstream coordination. 

In light of the fact that Spatial Modeling is the primary bottleneck under viewpoint shifts, we propose a oneshot robustness adaptation framework that enables pretrained vision-language-action models to recalibrate their visual representations through lightweight, learnable modulation. Specifically, we introduce Feature Token Modula- 


Figure 2. **Visualization of a sample rollout generated by our method.** Each row shows how observations from different viewpoints evolve over time (columns). The rollout demonstrates the adaptability of _π_ 0 _._ 5 equipped with our proposed One-Shot Feature Linear Adaptation. 

tion (FTM), a simple yet effective mechanism that applies a global affine transformation to visual token embeddings using only two learnable parameter vectors ( _γ, β_ ). This operation re-scales and re-centers feature distributions, allowing the model to adapt rapidly to new visual domains. Despite involving fewer than 4K parameters, FTM significantly improves viewpoint robustness, raising accuracy from 48.5% to 87.1% (see Fig. 1(b)). 

Motivated by this result, we further propose Feature Linear Adaptation (FLA), a lightweight enhancement applied to the ViT encoder via low-rank updates to its linear layers. This adaptation realigns internal features with modest parameter overhead (4.7M parameters in total), further boosting the average success rate to 90.8% (see Fig. 1(b)), comparable to full-parameter fine-tuning approaches such as LoRA, but at a fraction of the cost. 

To enable systematic evaluation, we construct the Libero-V (Visual) benchmark, which integrates varying levels of viewpoint and visual perturbations from LiberoPlus [8]. Libero-V introduces four controlled perturbation types—camera viewpoint [31], lighting, background texture, and visual noise—providing a unified framework for assessing robustness under diverse distribution shifts. Our empirical findings reveal that pretrained VLA models in- 

35026 

herently encode latent robustness, which can be efficiently activated through minimal adaptation rather than large-scale retraining. This perspective highlights that achieving robust embodied perception does not necessarily require more data or complex architectures but rather efficient mechanisms for perturbation-invariant feature adaptation (See Fig. 2). 

   - Our main contributions are summarized as follows: 

- We reassess the robustness of pretrained VLA models and show that performance degradation under visual perturbations primarily arises from representation shifts within Spatial Modeling. 

- We propose a unified one-shot robustness adaptation framework, consisting of Feature Token Modulation (FTM) and Feature Linear Adaptation (FLA), which efficiently recalibrates visual representations with minimal parameter updates. 

- Our approach achieves state-of-the-art generalization to unseen camera viewpoints and visual perturbations on the Libero benchmark, revealing the untapped robustness potential within existing VLA models. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

VLA models aim to unify visual perception, language grounding, and action generation within a single policy framework [25, 26, 40]. By extending pretrained vision– language foundations to the robotic domain, recent VLAs such as RT-2 [3], Pi0 [2], PaLM-E [6], Octo [28], and OpenVLA [15] demonstrate strong in-distribution generalization across diverse manipulation tasks. These systems leverage large-scale embodiment datasets [5, 14] to integrate varied visual inputs, language instructions, and proprioceptive states, along with noisy actions, to generate a shared action policy that enables robots to perform versatile behaviors. 

Despite these advances, recent analyses reveal that stateof-the-art VLAs, even after being pre-trained and subsequently fine-tuned on datasets, remain surprisingly brittle under distribution shifts [8, 47]. Performance degrades sharply when models are exposed to unseen camera viewpoints, novel lighting conditions, or scene noise perturbations—a limitation that persists even in models trained on millions of demonstrations. Understanding and addressing this brittleness is therefore essential for deploying VLA systems in real-world environments, where the visual environments are significantly more complex than Libero settings. 

### **2.2. Viewpoint Robustness & Embedding Stability** 

Robustness to visual perturbations is a long-standing challenge in improving VLA performance [44]. Prior work has explored data-centric strategies to improve viewpoint invariance by increasing visual diversity through domain ran- 

domization, multi-view demonstrations, or large-scale visual perturbation datasets [8, 47]. While effective, these approaches require extensive data collection or annotation, which limits their scalability. 

Another line of research focuses on representationcentric robustness by enforcing geometric consistency[1, 31, 35]. Recent studies further indicate that viewpoint shifts can induce significant drifts in the embedding space of pretrained ViT encoders [33], disrupting the coordination between perception and downstream policy modules. 

Motivated by these findings, we investigate whether correcting such embedding misalignment—without modifying the overall VLA architecture or collecting additional data— is sufficient to restore viewpoint robustness. 

### **2.3. Parameter-Efficient Adaptation** 

Parameter-efficient finetuning (PEFT) has emerged as an effective alternative to full-model adaptation, enabling models to specialize to new tasks or domains with minimal trainable parameters. Representative approaches include adapters [10], LoRA [11], Prefix-Tuning [20], and BitFit [37], all of which introduce small learnable modules while keeping the majority of the backbone frozen. These techniques have been widely adopted in large language models and multimodal foundations due to their efficiency and stability. 

In embodied AI, PEFT has primarily been applied to language or policy components, such as lightweight updates to decision transformers or instruction encoders [2, 15, 28]. When addressing viewpoint shifts, most existing methods rarely solve the problem by directly finetuning the visual module itself. Approaches that perform lightweight and targeted adaptation of the visual pathway within VLA models remain particularly scarce. 

In contrast to these approaches, which often adapt the entire VLA stack, our work focuses on parameter-efficient adaptations of the visual pathway, investigating whether lightweight adaptation of vision tokens or the vision encoder alone is sufficient to recover robustness. 

## **3. Method** 

Prior works typically address brittleness to visual perturbations by finetuning large portions of the VLA or retraining the entire visuomotor policy, as illustrated in Fig. 3 (a, b). In contrast, we argue that global adaptation is unnecessary: shifts caused by visual perturbations mainly induce systematic drifts in the visual embedding space—disrupting the coordination between the visual encoder and the VLM head rather than exposing a lack of visuomotor capacity. This observation suggests adapting only the visual module through lightweight mechanisms—either token modulation or a LoRA-based update—instead of globally finetuning the VLA. 

35027 

### **3.1. Preliminaries** 

**Original** _π_ 0 _._ 5 **formulation.** We adopt _π_ 0 _._ 5 [13] as our base vision-language-action (VLA) policy. The policy operates on language and visual observations and autoregressively produces discrete action tokens at each control timestep. Concretely, at time _t_ the agent observes a visual input _vt_ (an image or multi-view image set) and a language instruction/goal _l_ , which together we denote by the observation _ot_ = ( _vt, l_ ). The policy parametrized by _θ_ defines a distribution over an action token sequence _a_ 1: _T_ : 


where _at_ is represented as a short sequence of discrete tokens encoding robot control (e.g., position, orientation, and gripper commands). 

Architecturally, _π_ 0 _._ 5 decomposes into three conceptual modules: a visual encoder _fv_ ( _·_ ) that maps images to token embeddings, a language encoder _fℓ_ ( _·_ ) that maps text to embeddings, and a multimodal transformer decoder _g_ ( _·_ ), equipped with separate expert weights, that autoregressively predicts action tokens conditioned on the fused embeddings. Denoting the visual-token sequence by **z** = _fv_ ( _v_ ) and the language embedding by _ℓ_ = _fℓ_ ( _l_ ), the decoder operates on the concatenated multimodal sequence: 


**Notation for adaptation.** In the remainder of the paper we distinguish between (i) the pretrained VLA parameters _θ_ and (ii) lightweight adaptation parameters _ϕ_ that we introduce to improve robustness under visual perturbations. Adaptation interventions will be applied only to the visualside representations (i.e., the output of _fv_ or to linear layers inside the visual encoder) while keeping the decoder _g_ and language encoder _fℓ_ fixed. Formally, after adaptation the prediction distribution becomes 


where _Aϕ_ ( _·_ ) denotes a lightweight, learnable transformation applied to visual tokens (for example, the Feature Token Modulation described in Sec. 3.3 or the Feature Linear Adaptation in Sec. 3.4). 

### **3.2. Approaches for Robustness Adaptation** 

To mitigate brittleness to visual perturbations, several adaptation strategies have been explored in prior work, as illustrated in Fig. 3: 

- (a) **LoRA Fine-tuning.** A common solution is to perform full or parameter-efficient fine-tuning of the VLA backbone _θ_ , such as LoRA-based updates (Fig. 3a), 


Figure 3. **Comparison of methods for adapting to new visual perturbations in VLA models.** Panels (a) and (b) show existing finetuning-based approaches for adapting VLA models to new visual features. Panel (c) illustrates a potential meta-learning strategy using concatenated learnable prompts. Panels (d) and (e) present our proposed methods—Feature Token Modulation and Feature Linear Adaptation. 

   - which adjust intermediate feature mappings while preserving pretrained weights. This post-training technique is widely adopted in large language and visionlanguage models [22, 27], and has been further incorporated into the training paradigm of VLAs. 

- (b) **Alternative Visual Backbones.** Another line of work replaces the visual encoder entirely with a more robust backbone [1, 31] (Fig. 3b), aiming to improve invariance through stronger visual representations. Such replacement, however, necessitates additional training of the VLA to reestablish consistency between the updated visual features and its language-conditioned action head. 

- (c) **Prompt-based Adaptation.** Prompt-based adaptation [45, 46] (Fig. 3c) introduces learnable tokens concatenated directly to multi-modal embeddings, conditioning the model on perturbation contexts and enabling partial alignment across domains. 

While these approaches can improve performance under distribution shifts, they often incur substantial parameter overhead or require extensive retraining. In contrast, our method focuses on lightweight, modular adaptation of the pretrained visual backbone without altering its architecture or data distribution. 

In contrast, we pursue a more lightweight and modular solution that adapts the pretrained VLA without altering 

35028 

its architecture, in a one-shot manner. As shown in Fig. 3 (d–e), our framework introduces two simple yet effective mechanisms: **Feature Token Modulation (FTM)** , which globally adjusts visual token embeddings through learnable affine transformations, and **Feature Linear Adaptation (FLA)** , a low-rank update to the visual backbone for deeper feature realignment. Together, these mechanisms form a unified one-shot robustness adaptation framework that efficiently restores viewpoint and perturbation robustness with minimal parameter updates. 

### **3.3. Feature Token Modulation** 

Inspired by the principles of meta-learning [9], we believe that robust behavior can be generated through effective adaptation rather than extensive retraining. To implement this idea, we first apply a lightweight modulation on the output token embeddings _F ∈_ R<sup>_N×D_ViT</sup> extracted from the camera image, introducing two learnable parameters _γ, β ∈_ R<sup>_D_ViT</sup> to scale and shift the feature distribution: 


This form of modulation can be viewed as an affine correction to the visual embedding space, effectively recentering and re-scaling feature dimensions distorted by viewpoint shifts, while keeping the VLA backbone frozen, as illustrated in Fig. 3 (d) and Fig. 4 (a). In practice, unlike conditional modulation methods that generate inputdependent parameters, our _γ_ and _β_ are globally applied yet learnable, jointly optimized during adaptation while keeping the backbone frozen. This design introduces only 2 _D_ ViT trainable parameters in total. 

We treat this modulation as a controlled probe to examine whether viewpoint brittleness primarily originates from embedding misalignment rather than insufficient model capacity. If the hypothesis holds, adjusting only ( _γ, β_ ) should be sufficient to partially restore viewpoint alignment without global finetuning; the empirical evidence is presented in Table 1. 

### **3.4. Feature Linear Adaptation** 

Given the effectiveness of Feature Token Modulation (Sec. 3.3), we further explore whether viewpoint-induced misalignment can also be corrected by directly adapting the visual backbone itself. Specifically, instead of adjusting the output tokens, we apply a parameter-efficient LoRA[11] update to the linear layers inside the ViT encoder, as illustrated in Fig. 3 (e). 

Let _h_ = _Wx_ denote a linear transformation within the ViT, where _W ∈_ R<sup>_d_out</sup><sup>_×d_in</sup> is frozen during adaptation. LoRA introduces a low-rank decomposition, 


where _A ∈_ R<sup>_r×d_in</sup> and _B ∈_ R<sup>_d_out</sup><sup>_×r_</sup> with _r ≪_ min( _d_ in _, d_ out). Only ( _A, B_ ) are trainable, allowing ViT to adjust its feature extraction with minimal parameter overhead. 

This linear adaptation serves as a second minimal intervention on the Spatial Modeling, allowing us to test whether adjusting internal layers yields effects comparable to, or slightly better than, token-level modulation. Empirical comparisons are reported in Table 1 and Table 3. 

## **4. Experiment** 

### **4.1. Libero-V Benchmarks** 

To systematically evaluate the generalization of current VLA policies for visual perturbations, we construct the Libero-V (Visual) benchmark, which extends the original LIBERO benchmark to incorporate diverse visual perturbations. The original LIBERO benchmark [21] assesses knowledge transfer in multitask and lifelong robot learning for manipulation tasks. It consists of four task suites, and each suite contains 10 tasks. 

Following [31] we evaluate each policy with 50 trials per task on novel camera viewpoints. In addition, Libero-V integrates visual perturbations from Libero-Plus [8], covering four types of visual variation: (1) different camera viewpoints, (2) lighting changes, (3) background and tabletop textures, and (4) sensor-induced image noise. These perturbations simulate realistic distribution shifts and allow for a unified evaluation of robustness under visual domain changes. Importantly, our method performs one-shot adaptation — it requires only a single human demonstration per task to adapt to the new visual domain. 

### **4.2. Baselines** 

We adopt _π_ 0 _._ 5 [13] as our base vision-language-action (VLA) policy, which operates on visual and language inputs to generate action sequences autoregressively. We compare our proposed one-shot adaptation methods—Feature Token Modulation (FTM) and Feature Linear Adaptation (FLA)—against a range of strong baselines, including: 

- GeoAware-VLA [1], which replaces the visual backbone with a geometry-aware encoder and retrains the policy from scratch. 

- OpenVLA-OFT and OpenVLA-OFT-m [16], where the latter is fine-tuned on Libero-Plus to improve viewpoint robustness. 

- LoRA-based One-Shot Fine-tuning on both _π_ 0 and _π_ 0 _._ 5, which updates the policy parameters through low-rank adaptation. 

- Prompt Learning, which introduces additional learnable tokens concatenated to multimodal embeddings. Our proposed FTM and FLA differ in adaptation scope: 

- FTM applies a global affine modulation on the visual token 

35029 


Figure 4. **Overview of feature adaptation and benchmark design.** (a) Illustration of the proposed Feature Token Modulation mechanism. The dashed box denotes components used only during training and removed at inference. (b) The LIBERO-V (Visual) benchmark, created by combining multiple levels of viewpoint variation [31] with visual-perturbation tasks from LIBERO-Plus [8]. It covers four perturbation types: camera viewpoint, lighting, background texture, and image noise. 

Table 1. **Success rates on the LIBERO benchmark under novel camera viewpoints.** We report Success Rate (SR) across all unseen viewpoints [31] in the LIBERO suites [21]. GeoAware-VLA [1] replaces its visual backbone with VGGT and trains policies from scratch (results taken from the original paper). The two OpenVLA variants include OpenVLA-OFT (zero-shot) and OpenVLA-OFT-m, which is finetuned on LIBERO-Plus [8] using large-scale multi-view data. We additionally evaluate one-shot adaptations applied to pretrained _π_ 0 and _π_ 0 _._ 5, including LoRA, Feature Token Modulation (FTM), and Feature Linear Adaptation (FLA). 

||Libero S|uites (Acr|oss Novel|Camera)|Average|
|---|---|---|---|---|---|
|Model|Spatial<br>SR(%)|Object<br>SR(%)|Goal<br>SR(%)|Long<br>SR(%)|Across Suites<br>SR(%)|
|GeoAware-VLA(GeoAware VQ-BeT)|54.3|99.0|85.7|72.7|77.9|
|GeoAware-VLA(GeoAware BAKU)|94.3|98.0|90.7|47.3|82.6|
|OpenVLA-OFT|90.0|15.7|81.7|13.7|50.3|
|OpenVLA-OFT-m(Fine-Tuned on Libero-Plus [8])|67.1|72.4|72.0|49.2|65.2|
|_π_0(One-Shot Lora Fine-tuned)|95.4|96.6|79.1|63.2|83.6|
|_π_0_._5(One-Shot Lora Fine-tuned)|**97.2**|95.3|91.4|77.1|90.3|
|_π_0_._5(One Shot FTM)(ours)|95.4|95.5|87.7|70.0|87.2|
|_π_0_._5(One-Shot FLA)(ours)|96.5|**97.5**|**91.7**|**77.5**|**90.8**|


embeddings with only 4K parameters, while FLA performs a low-rank linear adaptation within the ViT encoder using 4.7M parameters. 

era and a third-person camera) to provide complementary visual information. We follow [13] to implement the Lora fine-tuning for baselines [2, 13]. 

### **4.3. Implementation details** 

All experiments are conducted on a single NVIDIA A100 GPU with 80GB of VRAM. In Feature Token Modulation (FTM), the learnable parameters _γ, β ∈_ R<sup>_D_ViT</sup> correspond to the hidden dimension of the visual encoder in _π_ 0 _._ 5, where _D_ ViT = 2048. As a result, FTM introduces only 4K trainable parameters in total. For Feature Linear Adaptation (FLA), we fine-tune only the linear layers within the SigLIP visual backbone [29] of _π_ 0 _._ 5. To ensure a fair comparison, both LoRA and FLA one-shot adaptation procedures are trained for 2000 steps using the Adam optimizer. Across all experiments, we use a batch size of 32, and the policy receives observations from two cameras (a wrist cam- 

### **4.4. Results and Analysis** 

**Robustness to Novel Camera Viewpoints.** Table 1 summarizes the performance of all methods on the LIBERO benchmark suites across novel camera viewpoints, while Fig. 5 visualizes the success rate before and after distinct adaptations. Our method achieves consistent improvements across all four LIBERO suites (Spatial, Object, Goal, Long), demonstrating its effectiveness in mitigating the brittleness of pretrained VLAs under viewpoint shifts. 

Specifically, the Feature Token Modulation (FTM) variant achieves an average success rate of 87.1%, surpassing the _π_ 0 baseline (83.6%) despite updating only a pair of global affine parameters. This result highlights a key in- 

35030 

Table 2. **Success Rate (SR) on Novel View Across all four Libero sub-suites.** 

||Lib|ero Suites (|Novel Ca|mera)|
|---|---|---|---|---|
|Model|Small<br>SR(%)|Medium<br>SR(%)|Large<br>SR(%)|Average<br>SR(%)|
|GeoAware-VLA|88.0|74.5|71.2|77.9|
|OpenVLA-oft-m(fine-tuned on Libero-Plus)|88.1|65.5|42.1|65.2|
|_π_0(One-Shot Lora Fine-tuned)|88.3|83|79.5|83.6|
|_π_0_._5(One-Shot Lora Fine-tuned)|**94.8**|**90.5**|85.6|90.3|
|Ours|94.6|90.0|**87.9**|**90.8**|


Figure 5. **Success rates before and after adaptation on the LIBERO benchmark under novel camera viewpoints.** We report Success Rate (SR) across all unseen viewpoints [31] in the LIBERO suites [21]. “Before” corresponds to the zero-shot performance of pretrained policies without any adaptation. 

sight of our study: under viewpoint perturbations, the visual tokens produced by Spatial Modeling become misaligned with the Physical Modeling components, yet even minimal token-level modulation is sufficient to substantially recover robustness. 

Building on this observation, the Feature Linear Adaptation (FLA) variant further improves performance to 90.8%, surpassing the strong _π_ 0 _._ 5 One-Shot LoRA baseline (90.3%) while using less than 1% of its parameters (4.7M vs. 467M). That a targeted, lightweight update to Spatial Modeling alone can outperform full-model LoRA fine-tuning provides compelling evidence that viewpoint brittleness originates primarily within the spatial representation, rather than the visuomotor policy. 

Furthermore, Fig. 2 and Table 2 show that our model maintains stable performance as the degree of viewpoint perturbation increases (Small → Large), indicating strong invariance to spatial transformations and validating our hypothesis that latent robustness can be recovered through efficient adaptation instead of retraining or large-scale data augmentation. 

**Robustness to Visual Perturbations (Libero-V).** We further evaluate all methods on the Libero-V (Visual) benchmark (Table 3), which introduces four controlled perturbations: camera, lighting, texture, and noise. Across all visual domains, our proposed one-shot adaptations deliver 

robust and consistent performance. 

In particular, FLA achieves an average success rate of 94.8%, matching or surpassing LoRA fine-tuning while being two orders of magnitude more parameter-efficient. Despite the already strong performance of the One-Shot LoRA baseline, our FLA slightly outperforms LoRA on the camera perturbation subset (90.8% vs. 90.3%) and also maintains excellent performance on lighting, texture, and noise perturbations, indicating better cross-perturbation generalization. Meanwhile, FTM, with only 4K parameters, already recovers most of the viewpoint robustness (87.2%), confirming that even simple token-level spatial adaptation can reactivate latent invariances within pretrained VLA representations. 

These results reinforce our central claim: robustness under visual perturbations is limited primarily by Spatial Modeling, and targeted lightweight adaptation is sufficient to reactivate the latent robustness of pretrained VLA models—without large-scale retraining or extensive domain randomization. 

**Ablation on Adaptation Rank and Baselines.** We conduct ablation studies on both the adaptation rank of the Feature Linear Adaptation (FLA) module and the choice of baselines. Table 5 reports results on the Libero suites under novel camera viewpoints. As shown in Table 5, increasing the adaptation rank from 16 to 32 results in a modest im- 

35031 

Table 3. **Success rates on the LIBERO-V (Visual) benchmark.** The benchmark evaluates robustness across four visual perturbations: camera viewpoint, lighting, background texture, and noise. Results marked with<sup>_∗_</sup> are taken from [8]. 

||Vi|sual Per|turbation|s|Average|
|---|---|---|---|---|---|
|Model|camera|light|texture|noise|Across Subsets|
|OpenVLA-OFT|50.3|92.7|92.3|78.6<sup>_∗_</sup>|78.5|
|OpenVLA-OFT-m(Fine-Tuned on Libero-Plus [8]))|65.2|94.9|93.9|89.9<sup>_∗_</sup>|86.0|
|_π_0(One-Shot Lora Fine-tuned)|83.6|90.7|86.7|87.0<sup>_∗_</sup>|87.0|
|_π_0_._5(Zero-Shot)|48.5|96.2|96.0|93.5|83.6|
|_π_0_._5(One-Shot Lora Fine-tuned)|90.3|96.5|**97.2**|94.5|94.6|
|_π_0_._5(One Shot FTM)(ours)|87.1|96.0|96.0|93.6|90.5|
|_π_0_._5(One-Shot FLA)(ours)|**90.8**|**96.8**|97.1|**94.6**|**94.8**|


Table 4. **Parameter count and accuracy on the LIBERO-V (Visual) benchmark.** 

|Methods|#Params (M)|Libero-V(%)|
|---|---|---|
|_π_0(One-Shot Lora Fine-tuned)|468.04|87|
|_π_0_._5(Prompt Learning)|0.131|75.1|
|_π_0_._5(One-Shot Lora Fine-tuned)|466.96|94.6|
|_π_0_._5(One Shot FTM)(ours)|**0.004**|90.5|
|_π_0_._5(One-Shot FLA)(ours)|4.7|**94.8**|


provement in success rate (from 90.8% to 91.2%). This is expected, since a higher rank corresponds to a larger number of learnable parameters in the visual backbone, enabling finer-grained feature realignment and improved robustness under complex visual perturbations. 

In addition, Table 5 compares FLA with LoRA using two different pretrained policies, _π_ 0 and _π_ 0 _._ 5. For both baselines, applying FLA (rank=16) achieves accuracy comparable to—or slightly higher than—LoRA, while requiring only 4.7M trainable parameters compared to LoRA’s 467M. Notably, on _π_ 0 _._ 5, FLA reaches 90.8% success rate with a 99× reduction in parameters, highlighting its effectiveness and efficiency across different base models. 

**Parameter Efficiency and Adaptation Strategy.** Table 4 compares all adaptation mechanisms in terms of trainable parameter count and Libero-V accuracy. Prompt Learning (Fig. 3c) achieves modest improvement (75.1%) with negligible parameters (0.13M), but its shallow conditioning is insufficient for full feature realignment. In contrast, FTM (0.004M) achieves substantially higher robustness (90.5%), showing that direct modulation of visual tokens is a more effective adaptation pathway. FLA further extends this idea by introducing low-rank structure into the ViT encoder, achieving 94.8% success rate with 4.7M parameters—a 99× reduction compared to LoRA while maintaining nearly identical accuracy. 

Table 5. **Efficiency of our FLA adaptation.** FLA (rank = 16) achieves a 90.8% success rate using only 4.7M parameters, compared to LoRA’s 467M parameters at 90.3%. 

|Model|#Params|Success Rate(%)|
|---|---|---|
|_π_0(One-Shot Lora Fine-tuned)|468M|83.6|
|_π_0_._5(One-Shot Lora Fine-tuned)|467M|90.3|
|_π_0(One-Shot FLA)(ours, rank=16)|**4.7M**|84.0|
|_π_0_._5(One-Shot FLA)(ours, rank=16)|**4.7M**|90.8|
|_π_0_._5(One-Shot FLA)(ours, rank=32)|9.4M|**91.2**|
|This efficiency-performance t<br>scalability and practicality of|rade-off <br> our on|demonstrates the<br>e-shot adaptation|
|framework. It supports our overa<br>covering robustness in embodied<br>quire more data or complex archit<br>plished through simple, efficient, <br>adaptation.|rching c<br>VLA m<br>ectures,<br> and we|onclusion that re-<br>odels does not re-<br>but can be accom-<br>ll-targeted feature|


## **5. Conclusion** 

We show that this brittleness primarily arises from misalignment in Spatial Modeling rather than limitations in Physical Modeling, indicating that the visuomotor policy itself remains fundamentally capable. We introduced two lightweight mechanisms—Feature Token Modulation (FTM) and Feature Linear Adaptation (FLA)—that recalibrate visual representations with minimal parameters. Across the Libero-V benchmarks, our framework achieves state-of-the-art generalization under novel camera viewpoints and diverse visual perturbations, while being up to 99× more parameter-efficient than LoRA fine-tuning. These results suggest that enhancing embodied visual robustness does not require larger models or more data; instead, efficient, targeted adaptation can unlock the inherent generalization potential of existing VLA architectures. 

35032 

## **6. Acknowledgments** 

This work was supported in part by National High-Level Young Talent Program (Grant 2025HY00260104), in part by the Fundamental Research Funds for Higher Education Institutions allocated to Sun Yat-sen University (Grants 25hytd007 and 2025RGZN009), in part by the Guangdong Provincial High-Level Young Talent Program (Grant 2025HYSPT0707), in part by the Tuoyuan Grant (HT99982025-0564), in part by the Faculty Start-up Research Fund (Grant 67000-12255002), and in part by the Huawei Strategic Research Institute Talent Fund. 

## **References** 

- [1] Ali Abouzeid, Malak Mansour, Zezhou Sun, and Dezhen Song. Geoaware-vla: Implicit geometry aware visionlanguage-action model, 2025. 2, 3, 4, 5, 6 

- [2] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 1, 3, 6 

- [3] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 1, 3 

- [4] Yuhao Chen, Zhihao Zhan, Xiaoxin Lin, Zijian Song, Hao Liu, Qinhan Lyu, Yubo Zu, Xiao Chen, Zhiyuan Liu, Tao Pu, et al. Radar: Benchmarking vision-language-action generalization via real-world dynamics, spatial-physical intelligence, and autonomous evaluation. _arXiv preprint arXiv:2602.10980_ , 2026. 2 

- [5] Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, et al. Open x-embodiment: Robotic learning datasets and rt-x models, 2025. 1, 3 

- [6] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. Palm-e: An embodied multimodal language model. In _arXiv preprint arXiv:2303.03378_ , 2023. 3 

- [7] Zane Durante, Bidipta Sarkar, Ran Gong, Rohan Taori, Yusuke Noda, Paul Tang, Ehsan Adeli, Shrinidhi Kowshika Lakshmikanth, Kevin Schulman, Arnold Milstein, Demetri Terzopoulos, Ade Famoti, Noboru Kuno, Ashley Llorens, Hoi Vo, Katsu Ikeuchi, Li Fei-Fei, Jianfeng Gao, Naoki Wake, and Qiuyuan Huang. An interactive agent foundation model, 2024. 1 

- [8] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, Jinlan Fu, Jingjing Gong, and Xipeng Qiu. Libero-plus: Indepth robustness analysis of vision-language-action models, 2025. 1, 2, 3, 5, 6, 8 

- [9] Chelsea Finn, Pieter Abbeel, and Sergey Levine. Modelagnostic meta-learning for fast adaptation of deep networks, 2017. 5 

- [10] Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin de Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly. Parameter-efficient transfer learning for nlp, 2019. 3 

- [11] Edward J Hu, yelong shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. 3, 5 

- [12] Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. An embodied generalist agent in 3d world, 2024. 1 

- [13] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. 4, 5, 6 

- [14] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, et al. Droid: A largescale in-the-wild robot manipulation dataset, 2025. 1, 3 

- [15] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model, 2024. 1, 3 

- [16] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success, 2025. 5 

- [17] Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Peiyuan Zhang, Yanwei Li, Ziwei Liu, and Chunyuan Li. Llava-onevision: Easy visual task transfer, 2024. 1 

- [18] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating realworld robot manipulation policies in simulation, 2024. 1 

- [19] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, 

35033 

Huaping Liu, Hang Li, and Tao Kong. Vision-language foundation models as effective robot imitators, 2024. 1 

- [20] Xiang Lisa Li and Percy Liang. Prefix-tuning: Optimizing continuous prompts for generation, 2021. 3 

- [21] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023. 1, 5, 6, 7, 4 

- [22] OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, et al. Gpt-4 technical report, 2024. 4 

- [23] Jing-Cheng Pang, Nan Tang, kaiyuan Li, Yuting Tang, XinQiang Cai, Zhen-Yu Zhang, Gang Niu, Sugiyama Masashi, and Yang Yu. Learning view-invariant world models for visual robotic manipulation. In _International Conference on Learning Representations (ICLR)_ , 2025. 2 

- [24] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model, 2025. 2 

- [25] Zijian Song, Sihan Qin, Tianshui Chen, Liang Lin, and Guangrun Wang. Physical autoregressive model for robotic manipulation without action pretraining. _arXiv preprint arXiv:2508.09822_ , 2025. 3 

- [26] Zijian Song, Qichang Li, Sihan Qin, Yuhao Chen, Tianshui Chen, Liang Lin, and Guangrun Wang. Learning physics from pretrained video models: A multimodal continuous and sequential world interaction models for robotic manipulation. _arXiv preprint arXiv:2603.00110_ , 2026. 3 

- [27] Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M. Dai, Anja Hauth, Katie Millican, et al. Gemini: A family of highly capable multimodal models, 2025. 4 

- [28] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy, 2024. 1, 3 

- [29] Michael Tschannen, Alexey Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, Olivier H´enaff, Jeremiah Harmsen, Andreas Steiner, and Xiaohua Zhai. Siglip 2: Multilingual visionlanguage encoders with improved semantic understanding, localization, and dense features, 2025. 6 

- [30] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe HansenEstruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale, 2024. 1 

- [31] Albert Wilcox, Mohamed Ghanem, Masoud Moghani, Pierre Barroso, Benjamin Joffe, and Animesh Garg. Adapt3r: Adaptive 3d scene representation for domain transfer in imitation learning, 2025. 2, 3, 4, 5, 6, 7 

- [32] Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, and Pieter Abbeel. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators, 2023. 1 

- [33] Annie Xie, Lisa Lee, Ted Xiao, and Chelsea Finn. Decomposing the generalization gap in imitation learning for visual robotic manipulation, 2023. 1, 3 

- [34] Eliot Xing, Abhinav Gupta, Sam Powers*, and Victoria Dean*. Kitchenshift: Evaluating zero-shot generalization of imitation-based policy learning under domain shifts. In _NeurIPS 2021 Workshop on Distribution Shifts: Connecting Methods and Applications_ , 2021. 1 

- [35] Rujia Yang, Geng Chen, Chuan Wen, and Yang Gao. Fp3: A 3d foundation policy for robotic manipulation, 2025. 2, 3 

- [36] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Avnish Narayan, Hayden Shively, Adithya Bellathur, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning, 2021. 1 

- [37] Elad Ben Zaken, Shauli Ravfogel, and Yoav Goldberg. Bitfit: Simple parameter-efficient fine-tuning for transformer-based masked language-models, 2022. 3 

- [38] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations, 2024. 2 

- [39] Zhihao Zhan, Yuhao Chen, Jiaying Zhou, Qinhan Lv, Hao Liu, Keze Wang, Liang Lin, and Guangrun Wang. Stable language guidance for vision-language-action models, 2026. 1 

- [40] Zhihao Zhan, Jiaying Zhou, Likui Zhang, Qinhan Lv, Hao Liu, Jusheng Zhang, Weizheng Li, Ziliang Chen, Tianshui Chen, Ruifeng Zhai, Keze Wang, Liang Lin, and Guangrun Wang. E0: Enhancing generalization and fine-grained control in vla models via tweedie discrete diffusion, 2026. 3 

- [41] Jianke Zhang, Xiaoyu Chen, Qiuyue Wang, Mingsheng Li, Yanjiang Guo, Yucheng Hu, Jiajun Zhang, Shuai Bai, Junyang Lin, and Jianyu Chen. Vlm4vla: Revisiting visionlanguage-models in vision-language-action models, 2026. 2 

- [42] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, YuGang Jiang, and Xipeng Qiu. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks, 2024. 1 

- [43] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model, 2024. 1 

- [44] Jiaying Zhou, Zhihao Zhan, Ruifeng Zhai, Qinhan Lyu, Hao Liu, Keze Wang, Liang Lin, and Guangrun Wang. Tag: Target-agnostic guidance for stable object-centric inference in vision-language-action models, 2026. 3 

- [45] Kaiyang Zhou, Jingkang Yang, Chen Change Loy, and Ziwei Liu. Conditional prompt learning for vision-language models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 4 

- [46] Kaiyang Zhou, Jingkang Yang, Chen Change Loy, and Ziwei Liu. Learning to prompt for vision-language models. _International Journal of Computer Vision (IJCV)_ , 2022. 4 

35034 

- [47] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. Libero-pro: Towards robust and fair evaluation of visionlanguage-action models beyond memorization, 2025. 1, 3 

35035 

