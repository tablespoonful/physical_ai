---
title: "Improving Robustness of Vision-Language-Action Models by Restoring Corrupted Visual Inputs"
date: "2026-02-01"
authors: "Daniel Yezid Guarnizo Orjuela; Leonardo Scappatura; Veronica Di Gennaro; Riccardo Andrea Izzo; Gianluca Bardaro; Matteo Matteucci"
url: https://arxiv.org/abs/2602.01158
pdf: https://arxiv.org/pdf/2602.01158
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.01158)** / [論文ページ](https://arxiv.org/abs/2602.01158)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Improving Robustness of Vision-Language-Action Models by Restoring Corrupted Visual Inputs 

Daniel Yezid Guarnizo Orjuela<sup>_†_</sup> , Leonardo Scappatura<sup>_†_</sup> , Veronica Di Gennaro<sup>_†_</sup> , 

Riccardo Andrea Izzo<sup>_‡_</sup> , Gianluca Bardaro<sup>_‡_</sup> , and Matteo Matteucci<sup>_‡_</sup> 

Department of Electronics, Information, and Bioengineering 

Politecnico di Milano, Milano 

_†_ (danielyezid.guarnizo, leonardo.scappatura, veronica.digennaro)@mail.polimi.it 

_‡_ (riccardo.izzo, gianluca.bardaro, matteo.matteucci)@polimi.it 

**_Abstract_ —Vision-Language-Action (VLA) models have emerged as a dominant paradigm for generalist robotic manipulation, unifying perception and control within a single end-to-end architecture. However, despite their success in controlled environments, reliable real-world deployment is severely hindered by their fragility to visual disturbances. While existing literature extensively addresses** **_physical occlusions_ caused by scene geometry, a critical mode remains largely unexplored:** **_image corruptions_ . These sensor-level artifacts, ranging from electronic noise and dead pixels to lens contaminants, directly compromise the integrity of the visual signal prior to interpretation. In this work, we quantify this vulnerability, demonstrating that state-of-the-art VLAs such as** _π_ 0 _._ 5 **and SmolVLA, suffer catastrophic performance degradation, dropping from 90% success rates to as low as 2%, under common signal artifacts. To mitigate this, we introduce the Corruption Restoration Transformer (CRT), a plug-and-play and model-agnostic vision transformer designed to immunize VLA models against sensor disturbances. Leveraging an adversarial training objective, CRT restores clean observations from corrupted inputs without requiring computationally expensive fine-tuning of the underlying model. Extensive experiments across the LIBERO and Meta-World benchmarks demonstrate that CRT effectively recovers lost performance, enabling VLAs to maintain near-baseline success rates, even under severe visual corruption.** 

**_Index Terms_ —Vision-Language-Action Models, Image Corruption, Vision Transformer, Adversarial Training** 

## I. INTRODUCTION 

Recent advancements in robotic control tasks have been driven by Vision-Language-Action (VLA) models. By unifying perception, language understanding, and action prediction within a single architecture, these systems enable robots to execute complex manipulation tasks grounded in both visual observations and natural language instructions. 

VLAs have the potential to bring significant advancements to numerous domains, ranging from industrial automation to the medical field. However, despite the impressive capabilities demonstrated in controlled research environments, widespread real-world deployment remains challenging due to significant reliability issues. These include satisfying real-time inference constraints while ensuring safety and robustness in dynamic and unstructured environments. 

For a VLA to be deployable in the real world, it must exhibit _Environmental Robustness_ [1], which refers to the 

capacity to maintain stable and accurate performance despite unpredictable variations in the input stream. Real-world environments are inherently complex, presenting challenges such as inconsistent lighting, adverse weather conditions, or instances where the target object is physically hidden by obstacles. 

Current literature actively addresses challenges arising from _physical occlusions_ in the scene, often resolving them through active perception or multi-view reasoning [2], [3]. However, a distinct and equally critical source of visual degradation remains under-explored: _image corruption_ . Unlike physical obstacles, these are artifacts, ranging from water droplets and dead pixels to electronic interference, that directly compromise the integrity of the visual signal before it is interpreted by the VLA. Existing studies indicate that standard VLAs, trained on clean, unobstructed visual data, exhibit significant performance degradation when key features are obscured, with a drop of 20–30% under noisy conditions [1]. 

Nonetheless, a systematic quantification of how severely such image corruption artifacts impact the end-to-end success rates of modern VLAs is lacking in the current literature. 

This paper addresses this gap through two contributions. First, we provide a rigorous quantitative analysis of performance degradation in state-of-the-art VLA models, specifically SmolVLA and _π_ 0 _._ 5, under diverse image corruption scenarios. Our findings confirm that, without mitigation, these artifacts cause significant performance degeneration. 

Second, we introduce the **Corruption Restoration Transformer (CRT)** to handle these vulnerabilities. We adopt the efficient Transformer-based architecture proposed by [4], originally designed for image reconstruction, and repurpose it for the domain of robotics within high-resolution simulation environments. We designed it as a modular unit upstream of the VLA. This approach offers a strategic advantage: rather than retraining or fine-tuning from scratch a VLA, which would be computationally prohibitive, CRT acts as a specialized, lightweight module that restores observations before they reach the policy network. 

The integration of CRT effectively minimizes divergence between actions derived from clean and corrupted inputs. effectively neutralizing the impact of image corruptions on the VLA. To facilitate reproducibility, we release our code, 

model and dataset<sup>1</sup> . 

## II. RELATED WORK 

## _A. Vision-Language-Action Models (VLAs)_ 

Building upon the architectural foundations of Large Language Models (LLMs) and Vision-Language Models (VLMs), Vision-Language-Action (VLA) models extend these capabilities into the physical domain. This results in end-to-end systems, capable of reasoning and directly executing actions [1], [5]. VLAs are trained on internet-scale multimodal data paired with robot trajectories, such as the Open X-Embodiment dataset [6]. Pioneering works, such as RT-2 [7], demonstrated that VLMs could be directly fine-tuned to output robotic actions by tokenizing continuous motions into discrete text tokens. This allows the model to leverage the intrinsic semantic reasoning of LLMs to enable zero-shot generalization to novel objects and instructions. Building on this, OpenVLA [8] introduced an open-source 7B-parameter architecture that integrates robust visual encoders (e.g., DINOv2 [9] and SigLIP [10]) with a Llama-2 [11] language backbone, establishing a robust baseline for generalist robot manipulation through discrete action token prediction. 

Despite their success, treating continuous motor control as a discrete token prediction task often compromises the smoothness and precision required for manipulation. Consequently, recent architectures have transitioned towards diffusion-based or flow-matching heads to represent multimodal action distributions in continuous space. For instance, _π_ 0 [12] employs flow-matching [13] to predict continuous action chunks, while SmolVLA [14] integrates cross-attention layers with a flowmatching action expert. While these models excel in semantic generalization and task execution, their efficacy is highly dependent on the integrity of the visual encoder’s feature space. Since they are primarily trained on curated datasets, their performance tends to degrade significantly when encountering visual corruptions, highlighting a critical lack of robustness. 

## _B. Visual Degradation in Robotic Perception_ 

Visual degradation poses a persistent challenge to reliable robotic control. We categorize these challenges into two classes based on their origin: _Physical Occlusions_ (e.g., scenedependent) and _Image Corruptions_ (e.g., sensor-dependent). **Physical Occlusion** : In unstructured real-world environments, target objects are frequently physically hidden behind other obstacles. The prevailing solution in the literature is active perception, where the robot autonomously adjusts its viewpoint to gather missing information. Recent frameworks such as VISO-Grasp [15] and Next-Best-View (NBV) planners [16] utilize VLMs to reason about spatial relationships and identify occluders, guiding the camera to a vantage point that reveals the target. Similarly, models like WoW [17] infer and remove obstructions through spatial reasoning. These methods rely on the premise that the obstructions are extrinsic; by changing the 


Fig. 1. **System Pipeline.** The CRT module is inserted upstream of the VLA. It intercepts the corrupted simulator observation _x_<sup>_′_</sup> , restores it to _x_ ˆ, and passes the clean estimate to the policy network for action prediction. 

sensor’s pose relative to the scene, the target can be revealed through multi-view fusion or scene repositioning. **Image Corruption** : Unlike physical occlusions, sensor-based corruptions arise from artifacts inherent to the perception hardware or the signal transmission pipeline. These include water droplets, cracks, dead pixels, or electronic interference. While existing computer vision literature offers solutions for similar issues [18]–[20], these have rarely been adapted for end-to-end robotic systems. Crucially, standard techniques effective for physical occlusion are ineffective in this context. Active perception fails due to the corruption (e.g., a spot on the lens) being fixed in the camera frame and continuously obstructing a portion of the field of view regardless of the robot’s position. Given that standard VLAs suffer performance drops of 20–30% under these conditions [1], there is a critical need for a modular restoration approach that cleanses the image observation before it reaches the policy network. 

## III. METHODOLOGY 

## _A. Overall Architecture_ 

To address the problem of image corruptions, we introduce a dedicated restoration module, the **Corruption Restoration Transformer (CRT)** , into the standard robotic control pipeline. Leveraging the LeRobot library [5], we position the restoration module immediately upstream of the VLA model. In this configuration, every raw observation frame retrieved from the camera is processed to reduce corruptions before it is processed by the policy network 

Let _x ∈_ R<sup>_H×W ×_3</sup> be a clean observation frame from the robot camera. The spatial dimensions _H×W_ are adapted to the simulator environment, with a resolution of 360 _×_ 360 for the LIBERO [21] benchmark and 480 _×_ 480 for Meta-World [22]. 

We define a corruption process _C_ , such that the observed input is formulated as _x_<sup>_′_</sup> = _C_ ( _x, M_ ), where _M_ represents the specific artifact type applied to the clean frame. As illustrated in Figure 1, the objective of CRT is to invert this process and recover the original signal _x_ from the corrupted input _x_<sup>_′_</sup> , ensuring that the VLA operates on a restored observation. 

## _B. Corruption Restoration Transformer (CRT)_ 

We propose the Corruption Restoration Transformer (CRT), _G_ , a Transformer-based reconstruction model trained to map the corrupted image observation back to its original version. 

1https://huggingface.co/collections/AIRLab-POLIMI/ corruption-restoration-transformer 

To achieve this, we draw inspiration from the image restoration framework introduced by [4], and specialize the approach for the robotic perception domain. This architecture’s ability to handle dense prediction tasks with high computational efficiency aligns with the needs of our target domain. We identify three critical architectural mechanisms to ensure that CRT provides the precision and efficiency required by the VLA: 

- **Shifted Patch Tokenization (SPT)** : Used to preserve spatial relationships between neighbouring pixels. SPT directly addresses the lack of local inductive bias in standard Vision Transformers (ViT) [23]. 

- **Rotary Position Embeddings (RoPE)** : Adopted to encode both absolute and relative positions, allowing the model to generalize across longer action sequences used in action prediction [24]. 

- **Locality Self-Attention (LSA)** : Employed to sharpen attention scores and focus on local texture details. 

The baseline architecture from [4] was originally designed for low-resolution (64 _×_ 64 pixels) tasks, whereas our application requires processing higher resolution visual inputs (up to 480 _×_ 480 pixels) that contain dense semantic information. Therefore, it was necessary to significantly scale the model capacity to meet the requirements of the VLA. We increased the latent vector size to preserve fine-grained textures and object details critical for robotic manipulation with VLAs, but easily removed by corruption artifacts. Moreover, we expanded the number of transformer blocks, increasing the number of stacked encoder layers. In a Transformer, earlier layers typically process local patterns (edges, textures), while deeper layers aggregate this information into global semantic concepts. This increased depth provides the necessary capacity to model the complex statistics of the corruption artifacts over the whole image. Finally, to complement the increased depth, we also scaled the number of attention heads. This allows the model to reason about multiple relationships (e.g., distinguishing between a scene edge and a corruption line) in parallel. 

## _C. Adversarial Training_ 

While standard pixel-wise reconstruction losses, such as _L_ 1 or Mean Squared Error (MSE), are effective at recovering low-frequency global structures, they often result in blurry outputs when handling high-frequency details. In the context of robotic manipulation, preserving these details is critical for the downstream VLA to correctly interpret object affordances and boundaries. To mitigate this, we employ and extend the adversarial training framework suggested in [4], treating the CRT module as a generator _G_ within a GAN. Figure 2 outlines our approach. 

We introduce a discriminator network _D_ trained to differentiate between ground-truth clean observations _x_ and the reconstructed observations _x_ ˆ = _G_ ( _x_<sup>_′_</sup> ). The discriminator architecture mirrors the transformer-based design of the generator but is optimized for classification. It processes inputs through a patch embedding layer and a sequence of Transformer blocks, 


Fig. 2. **CRT Adversarial Training.** The CRT Generator ( _G_ ) receives a corrupted input _x_<sup>_′_</sup> and produces a reconstructed observation _x_ ˆ. The network is optimized via a multi-objective loss function that combines pixel-wise fidelity _LL_ 1, structural similarity _LSSIM_ , and adversarial feedback _Ladv_ from the Discriminator _D_ to ensure effective reconstructions. 

with a final multi-layer perceptron (MLP) head to output a validity score. The training objective follows a multi-objective optimization strategy, utilizing a weighted combination of three distinct loss components: 

**Adversarial Loss** : to encourage perceptual realism, we employ a standard binary cross-entropy objective. The discriminator aims to maximize the probability of correctly classifying real and reconstructed images, while the generator aims to minimize the probability that _D_ recognizes _x_ ˆ as fake: 


**Reconstruction Losses** : to ensure the reconstructed image remains faithful to the ground truth content, we utilize a pixelwise _L_ 1 loss, which promotes sparsity and reduces blurring compared to _L_ 2 [25]: 


**Structural Similarity Index Measure (SSIM) loss** [26]: to preserve structural information such as brightness, contrast, and structure: 


The final objective function for the generator _G_ is a weighted sum of these terms: 


where _L_<sup>_G_</sup> _adv_<sup>representsthegenerator’scomponentofthead-</sup> versarial loss. Through empirical optimization, we set the hyperparameters to _λL_ 1 = 10 _._ 0, _λSSIM_ = 1 _._ 0, and _λadv_ = 0 _._ 05. The relatively low weight of the adversarial term ensures that the training remains grounded in content reconstruction while providing sufficient gradient signal to refine textural details and eliminate artifacts. 


Fig. 3. **Architecture of Corruption Restoration Transformer (CRT)** The model utilizes four specialized mechanisms: 1) Shifted Patch Tokenization (SPT) to recover local spatial dependencies; 2) Rotary Positional Embeddings (RoPE) for robust relative spatial encoding; 3) Locality Self-Attention (LSA) to sharpen textural details. The deep Transformer backbone enables the model to decouple complex corruption artifacts from the underlying semantic scene, finally reshaping the latent tokens into a restored RGB observation. 


Fig. 4. **Visual Corruption Types.** From top-left: (a) Clean Baseline, (b) Centered Square, (c) Gaussian Noise, (d) Horizontal Lines (0.5), (e) Horizontal Lines (0.2), (f) Water Drops. 

## _D. Dataset_ 

For the CRT training, we constructed two distinct paired datasets derived from successful execution trajectories within the LIBERO-10 and Meta-World MT50 benchmarks. We trained a dedicated reconstruction model for each benchmark, ensuring that CRT adapts to the distinct visual and semantic distributions of each simulation environment. 

To create the ground-truth reference dataset, we leveraged the pre-trained VLAs as expert demonstrators. For every task defined in the LIBERO-10 and Meta-World MT50 benchmarks, we executed the corresponding VLA policy in a noisefree environment. We strictly curated these rollouts, retaining only trajectories where the agent successfully achieved the goal state. To ensure a balanced distribution of visual semantics, we sampled exactly one successful trajectory for each distinct task (i.e., 10 for LIBERO, 50 for Meta-World). 

TABLE I 

**TRAINING HYPERPARAMETERS.** WE REPORT THE HYPERPARAMETERS USED TO TRAIN CRT USING A SINGLE NVIDIA RTX QUADRO 6000. 

|**Parameter**|**LIBERO**|**Meta-World**|
|---|---|---|
|Epochs|30|37|
|Learning Rate|1e-4|7e-4|
|Batch Size|12|8|
|Accumulation Steps|12|32|
|Training Time|1d 8h 14m|2d 22h 36m|


These trajectories were decomposed into individual frames to constitute the ground-truth observation set _x_ , preserving the native simulation resolutions (i.e., 360 _×_ 360 for LIBERO and 480 _×_ 480 for Meta-World). Subsequently, for every extracted clean frame _x_ , we applied the corruption generation process _C_ ( _x, M_ ) described in Section IV-A, to generate a corresponding corrupted _x_<sup>_′_</sup> . This procedure resulted in perfectly aligned ( _x_<sup>_′_</sup> _, x_ ) pairs suitable for supervised training. 

The resulting datasets comprise 48,660 image pairs: 27,310 frames from LIBERO-10 and 21,350 from Meta-World MT50. Each dataset was partitioned into an 80/20 split for training and validation. We report training hyperparameters in Table I. 

## IV. EXPERIMENTS AND RESULTS 

We evaluated the effectiveness of the CRT module using two widely recognized robotic manipulation benchmarks: LIBERO and Meta-World. These environments provide a diverse array of task complexities and semantic variations, while their integration with the LeRobot library ensures a standardized framework for reproducibility. We integrated our pipeline with two state-of-the-art VLAs: SmolVLA, evaluated on both LIBERO and Meta-World task suites, and _π_ 0 _._ 5, evaluated exclusively on the LIBERO suite, as a fine-tuned checkpoint for Meta-World was unavailable at the time of the study. 

## _A. Image Corruptions_ 

To evaluate the robustness of VLA models against sensorlevel disturbances, we selected a set of five distinct corruption 

TABLE II 

**QUANTITATIVE ANALYSIS OF CRT ON LIBERO-10 AND META-WORLD MT50 BENCHMARKS.** COMPARISON OF AVERAGE SUCCESS RATES (SR) AND RELATIVE PERFORMANCE DEGRADATION (∆) ACROSS CLEAN AND CORRUPTED OBSERVATIONS. 

|**Benchmark**|**Model**|**Baseli**<br>Avg. SR (_↑_)|**ne**<br>∆|**Centered **<br>Avg. SR (_↑_)|**Square**<br>∆|**Gaussian **<br>Avg. SR (_↑_)|**Noise**<br>∆|**Horiz. Lin**<br>Avg. SR (_↑_)|**es (0.5)**<br>∆|**Horiz. Li**<br>Avg. SR (_↑_)|**nes (0.2)**<br>∆|**Water **<br>Avg. SR (_↑_)|**Drops**<br>∆|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**LIBERO-10**|_π_0_._5<br>_π_0_._5 + **CRT**|**90.0**%<br>89.0%|–<br>-1.11%|65.0%<br>**89.0**%|-27.78%<br>-1.11%|**87.0**%<br>79.0%|-3.33%<br>-12.22%|2.0%<br>**87.0**%|-97.78%<br>-3.33%|62.0%<br>**89.0**%|-31.11%<br>-1.11%|68.0%<br>**87.0**%|-24.44%<br>-3.33%|
||SmolVLA|**43.0**%|–|**16.0**%|-62.79%|**13.0**%|-69.77%|0.0%|-100%|1.0%|-97.67%|11.0%|-74.42%|
||SmolVLA + **CRT**|33.0%|-23.26%|11.0%|-74.42%|4.0%|-90.70%|**3.0**%|-93.02%|**15.0**%|-65.12%|**15.0**%|-65.12%|
|**Meta-World**|SmolVLA<br>SmolVLA + **CRT**|**58.0**%<br>47.0%|–<br>-18.96%|33.0%<br>**40.6**%|-43.10%<br>-30.0%|27.6%<br>**34.6**%|-52.41%<br>-40.34%|20.6%<br>**32.2**%|-64.48%<br>-44.48%|20.0%<br>**41.4**%|-65.52%<br>-28.62%|40.0%<br>**43.34**%|-31.03%<br>-25.17%|


types illustrated in Figure 4. These artifacts are designed to model specific hardware failures, environmental conditions, and signal transmission errors commonly encountered in realworld robotic deployment. 

- **Centered Square** : In most manipulation tasks, the workspace and the main object of interest are centered in the frame. We simulate a catastrophic sensor failure that challenges the model by applying a black square to the image center, compromising the primary interaction zone. 

- **Gaussian Noise** : This simulates electronic sensor noise typical of low-light conditions, high ISO settings, or thermal interference. We inject zero-mean Gaussian noise with a standard deviation of 0.20 into each pixel, degrading fine-grained visual features. 

- **Horizontal Lines** : Represents scan-line artifacts from interlaced video transmission, rolling shutter effects, or electromagnetic interference. Black horizontal lines are randomly placed across the image, corrupting either 20% (low intensity) or 50% (high intensity) of the scene. 

- **Water Drops** : Reproduces lens contamination from liquid splashes, condensation, or humidity. These conditions are frequently encountered in industrial or outdoor environments. Semi-transparent circular regions with Gaussian blur are applied at multiple random locations. 

## _B. Results_ 

Our evaluation followed a three-stage protocol to validate the effectiveness of our CRT module across diverse manipulation tasks: 

- 1) We first evaluated SmolVLA and _π_ 0 _._ 5 on clean, uncorrupted observations to establish a baseline and confirm the validity of the simulation environment. 

- 2) We then introduced the corruption process _C_ ( _x, M_ ), applying each of the five corruption types individually. We recorded the performance drop for each model without any mitigation strategies. 

- 3) Finally, we integrated the CRT module upstream of the VLA. We repeated the evaluation under the same corruption conditions to measure the system’s ability to recover its performance. 

The outcomes of our evaluations are summarized in Table II. Our analysis focuses on three key dimensions: resilience to corruption of VLAs, CRT effectiveness, and the sensitivity of different VLAs on the restoration process. 

**Vulnerability of VLAs to Image Corruptions** : Consistent with previous literature, our results confirm that state-of-theart VLA models are highly sensitive to sensor artifacts. As shown in Table II, performance collapses significantly under corruptions. For instance, _π_ 0 _._ 5 on LIBERO-10 drops from a 90% success rate to just 2% under horizontal line corruption (0.5 intensity). Similarly, SmolVLA on Meta-World MT50 sees its performance halved from 58% to 20.6% under the identical conditions. These outcomes validate the premise that geometric generalization (e.g., active perception) is insufficient to mitigate cases when the underlying visual features are structurally compromised. 

**Effectiveness of CRT** : The integration of CRT demonstrates a significant recovery, particularly for the _π_ 0 _._ 5 architecture. As reported in Table II, _π_ 0 _._ 5 equipped with CRT achieves almost full recovery. Under the most severe “Horizontal Lines (0.5)” corruption, the success rate rebounds from 2% to 87%, effectively matching the clean baseline. Similar recovery is observed for “Water Drops” (68% to 87%) and “Gaussian Noise” (87% to 79%). Regarding SmolVLA on Meta-World, CRT consistently outperforms the unmitigated model across all corruption types. Notably, it improves success rates on “Horizontal Lines” by over 11%, going from 20.6% to 32.2%, and shows strong resilience also to “Centered Square” occlusions, with an increment of 7.6%. 

**Baseline Preservation and Trade-offs** : A critical requirement for CRT is the preservation of performance on already clean observations. For the _π_ 0 _._ 5 model, CRT exhibits negligible overhead, maintaining an 89% success rate on clean data compared to the 90% baseline. However, we observe a performance trade-off for the lighter SmolVLA architecture, where the baseline performance with CRT drops from 58% to 47% on Meta-World. This suggests that, while CRT successfully restores global semantic structure, smaller VLAs are less robust to feature perturbations and lack the capacity to generalize across subtle distributional shifts inherent to the reconstruction process. Nevertheless, this trade-off is significantly outweighed by the massive gains in reliability provided under adverse conditions. Furthermore, the CRT module is a lightweight neural network that introduces minimal overhead to the robotic control loop. Empirical tests indicated that CRT requires only 10-50 ms of inference time and approximately 1 GB of VRAM. In contrast, VLAs such as _π_ 0 or SmolVLA require significantly higher computational resources with latencies in the order of hundreds of milliseconds for token generation. 

Consequently, CRT introduces a negligible overhead while increasing the robustness of the underlying model. 

## V. CONCLUSION 

In this work, we identified a critical vulnerability in current Vision-Language-Action (VLA) models: their lack of robustness to image corruptions. While prior research has actively addressed physical occlusions through active perception, we demonstrated that sensor-level artifacts, such as lens contaminants, electronic noise, and signal loss, require a fundamentally different approach. Our systematic evaluation revealed that, even state-of-the-art models such as _π_ 0 _._ 5 and SmolVLA, suffer catastrophic failure when subjected to these disturbances, with success rates dropping by nearly 90% in severe cases. To bridge this gap, we introduced the Corruption Restoration Transformer (CRT), a specialized module designed to restore visual integrity upstream of the VLA. By leveraging advanced architectural mechanisms (e.g., SPT, RoPE, LSA) alongside an adversarial training objective, CRT effectively reconstructs clean observations from corrupted inputs, without requiring computationally prohibitive fine-tuning of the underlying VLA. Experimental results across LIBERO and Meta-World benchmarks confirm that CRT provides a robust solution against sensor artifacts. For large VLAs such as _π_ 0 _._ 5, CRT acts as a near-perfect reconstructive layer, recovering performance to within 1-3% of the clean baseline, even under heavy corruptions. We also observed that smaller architectures, such as SmolVLA, exhibit higher sensitivity to the subtle distributional shifts introduced by the reconstruction process, highlighting a trade-off between restoration effectiveness and input preservation. This limitation opens a clear avenue for future work. Given the modularity of CRT, the entire pipeline can be adapted to engage the restoration process only when a corruption is detected. Such an adjustment would maintain the original performance of the VLA, but also compensate for issues caused by image corruption. Ultimately, the CRT offers a scalable path towards more robust VLAs, deployable in the unpredictable and corrupted real-world environments. 

## REFERENCES 

- [1] R. Sapkota, Y. Cao, K. I. Roumeliotis, and M. Karkee, “Vision-languageaction models: Concepts, progress, applications and challenges,” _arXiv preprint arXiv:2505.04769_ , 2025. 

- [2] S. Wang and X. Cao, “Peafowl: Perception-enhanced multi-view vision-language-action for bimanual manipulation,” in _unknown_ , 2026. [Online]. Available: https://arxiv.org/pdf/2601.17885.pdf 

- [3] J. Liu, Y. Qi, J. Zhang, M. Li, S. Wang, K. Wu, H. Ye, H. Zhang, Z. Chen, F. Zhong _et al._ , “Trackvla++: Unleashing reasoning and memory capabilities in vla models for embodied visual tracking,” _arXiv preprint arXiv:2510.07134_ , 2025. 

- [4] N. Verma, D. Kaur, and L. Chau, “Image reconstruction using enhanced vision transformer,” _arXiv preprint arXiv:2307.05616_ , 2023. 

- [5] R. Cadene, S. Alibert, A. Soare, Q. Gallouedec, A. Zouitine, and T. Wolf, “Lerobot: State-of-the-art machine learning for real-world robotics in pytorch,” 2024. 

- [6] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6892–6903. 

- [7] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [8] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2679–2713. 

- [9] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby _et al._ , “Dinov2: Learning robust visual features without supervision,” _arXiv preprint arXiv:2304.07193_ , 2023. 

- [10] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, “Sigmoid loss for language image pre-training,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 11 975–11 986. 

- [11] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale _et al._ , “Llama 2: Open foundation and fine-tuned chat models,” _arXiv preprint arXiv:2307.09288_ , 2023. 

- [12] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ <u>0: A vision-language-action</u> flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [13] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” _arXiv preprint arXiv:2210.02747_ , 2022. 

- [14] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [15] Y. Shi, D. Wen, G. Chen, E. Welte, S. Liu, K. Peng, R. Stiefelhagen, and R. Rayyes, “Viso-grasp: Vision-language informed spatial object-centric 6-dof active view planning and grasping in clutter and invisibility,” _arXiv preprint arXiv:2503.12609_ , 2025. 

- [16] Z. Jia, Y. Li, Q. Hao, and S. Zhang, “Pb-nbv: Efficient projectionbased next-best-view planning framework for reconstruction of unknown objects,” _IEEE Robotics and Automation Letters_ , 2025. 

- [17] X. Chi, P. Jia, C.-K. Fan, X. Ju, W. Mi, K. Zhang, Z. Qin, W. Tian, K. Ge, H. Li _et al._ , “Wow: Towards a world omniscient world model through embodied interaction,” _arXiv preprint arXiv:2509.22642_ , 2025. 

- [18] H. Xu, A. A. Baniya, S. Wells, M. R. Bouadjenek, R. Dazeley, and S. Aryal, “Totnet: Occlusion-aware temporal tracking for robust ball detection in sports videos,” _Computer Vision and Image Understanding_ , p. 104657, 2026. 

- [19] Q. Li and Y. Cao, “Seeing through unclear glass: Occlusion removal with one shot,” _arXiv preprint arXiv:2509.01033_ , 2025. 

- [20] R. Mallick, S. Dong, N. Ruiz, and S. A. Bargal, “D-feat occlusions: Diffusion features for robustness to partial visual occlusions in object recognition,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1722–1731. 

- [21] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44 776–44 791, 2023. 

- [22] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine, “Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning,” in _Conference on robot learning_ . PMLR, 2020, pp. 1094–1100. 

- [23] G. J. Ferdous, K. A. Sathi, M. A. Hossain, and M. A. A. Dewan, “Spt-swin: A shifted patch tokenization swin transformer for image classification,” _IEEE Access_ , 2024. 

- [24] J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu, “Roformer: Enhanced transformer with rotary position embedding,” _Neurocomputing_ , vol. 568, p. 127063, 2024. 

- [25] H. Zhao, O. Gallo, I. Frosio, and J. Kautz, “Loss functions for image restoration with neural networks,” _IEEE Transactions on computational imaging_ , vol. 3, no. 1, pp. 47–57, 2016. 

- [26] D. Brunet, E. R. Vrscay, and Z. Wang, “On the mathematical properties of the structural similarity index,” _IEEE Transactions on Image Processing_ , vol. 21, no. 4, pp. 1488–1499, 2011. 

