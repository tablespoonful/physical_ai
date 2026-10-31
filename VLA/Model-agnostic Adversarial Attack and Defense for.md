---
title: "Model-agnostic Adversarial Attack and Defense for Vision-Language-Action Models"
date: "2025-10-15"
authors: "Haochuan Xu; Yun Sing Koh; Shuhuai Huang; Zirun Zhou; Di Wang; Jun Sakuma"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2510.13237
pdf: https://arxiv.org/pdf/2510.13237
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.13237)** / [論文ページ](https://arxiv.org/abs/2510.13237)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# MODEL-AGNOSTIC ADVERSARIAL ATTACK AND DEFENSE FOR VISION-LANGUAGE-ACTION MODELS 

**Haochuan Xu**<sup>1</sup> **Yun Sing Koh**<sup>1</sup> **Shuhuai Huang**<sup>1</sup> **Zirun Zhou**<sup>1</sup> **Di Wang**<sup>2</sup> **Jun Sakuma**<sup>3</sup><sup>_,_4</sup> **Jingfeng Zhang**<sup>1</sup><sup>_,_2</sup><sup>_,_4</sup><sup>_∗_</sup> 

1The University of Auckland 

2King Abdullah University of Science and Technology 

3Tokyo University of Science 

4RIKEN Center for Advanced Intelligence Project 

## ABSTRACT 

Vision-Language-Action (VLA) models have achieved revolutionary progress in robot learning, enabling robots to execute complex physical robot tasks from natural language instructions. Despite this progress, their adversarial robustness remains underexplored. In this work, we propose both adversarial patch attack and corresponding defense strategies for VLA models. We first introduce the Embedding Disruption Patch Attack (EDPA), a model-agnostic adversarial attack that generates patches directly placeable within the camera’s view. In comparison to prior methods, EDPA can be readily applied to different VLA models without requiring prior knowledge of the model architecture, or the controlled robotic manipulator. EDPA constructs these patches by (i) disrupting the semantic alignment between visual and textual latent representations, and (ii) maximizing the discrepancy of latent representations between adversarial and corresponding clean visual inputs. Through the optimization of these objectives, EDPA distorts the VLA’s interpretation of visual information, causing the model to repeatedly generate incorrect actions and ultimately result in failure to complete the given robotic task. To counter this, we propose an adversarial fine-tuning scheme for the visual encoder, in which the encoder is optimized to produce similar latent representations for both clean and adversarially perturbed visual inputs. Extensive evaluations on the widely recognized LIBERO robotic simulation benchmark demonstrate that EDPA substantially increases the task failure rate of cutting-edge VLA models, while our proposed defense effectively mitigates this degradation. The codebase is accessible via the homepage at https://edpa-attack.github.io/. 

## 1 INTRODUCTION 

Vision-Language-Action (VLA) models (Zitkovich et al., 2023; Team et al., 2024; Kim et al., 2024; Black et al., 2024) built on vision-language foundation models (Touvron et al., 2023; Beyer et al., 2024; Achiam et al., 2023; Liu et al., 2023b) have recently emerged to enable robots to perform complex physical tasks from high-level instructions. Through integrating vision and language understanding, VLAs leverage powerful perceptual and reasoning abilities, allowing robots to generalize to previously unseen environments (Zitkovich et al., 2023). 

As the increasing attention on VLA models, concerns about their reliability become particularly urgent, since failures in VLAs deployed on physical robotic platforms can lead to tangible consequences such as robots mishandling objects and resulting in property damage or performing incorrect actions that endanger human safety. Adversarial robustness (Carlini et al., 2019; Goodfellow et al., 2014; Madry et al., 2017) has long been recognized as a critical security challenge in computer vision. Given the VLA models reliance on visual inputs captured from camera, these models are likely 

> _∗_ Corresponding to jingfeng.zhang@auckland.ac.nz 

1 

to inherit similar vulnerabilities. While adversarial robustness has been extensively investigated in traditional deep learning models, its implications for VLA models remain largely underexplored. 

A recent study (Wang et al., 2024) highlighted the vulnerability of VLA models to adversarial attacks. The authors proposed several adversarial patch methods, each employing loss functions tailored to the robotic arm’s action trajectory for the OpenVLA (Kim et al., 2024) model controlling a 7-degree-of-freedom (DoF) robotic arm (Zitkovich et al., 2023). Their experiments showed that OpenVLA exhibited almost no resistance to such attacks. However, these attacks depend on stringent requirements: the attacker must have prior knowledge of the victim model, and full access to all model parameters to compute gradients for generating adversarial patches. These constraints substantially limit the practicality of the attacks in real-world scenarios (see Section 2.2). 

To address this limitation, we propose the Embedding Disruption Patch Attack (EDPA), designed to generate adversarial patches that disrupt a VLA’s interpretation of visual information. In contrast to prior attacks, EDPA requires only access to the VLA’s encoder parameters and does not rely on knowledge of the VLA’s architecture or the controlled robot platform. EDPA optimizes patches with two complementary objectives: (i) disrupting the semantic alignment between the visual latent representation and the corresponding instruction’s language latent representation, and (ii) maximizing the deviation between the latent representations of adversarial and corresponding clean visual inputs. Through jointly optimizing these objectives, EDPA produces adversarial patches that markedly distort visual understanding in VLAs, leading to a substantial reduction in the success rate of robotic tasks across the latest VLA models. 

In addition, we introduce a complementary adversarial fine-tuning scheme for the visual encoder to enhance the robustness of VLA models against such attacks. Specifically, all adversarial patches generated during the EDPA optimization process are applied to construct adversarial visual samples, which are then used to fine-tune the visual encoder. This method encourages the encoder to produce latent representations for adversarial visual inputs that match those of the corresponding clean inputs, while simultaneously ensuring that the fine-tuned encoder preserves performance for clean inputs by maintaining latent representations similar to those produced by the original encoder. Due to our experimental results showed that OpenVLA exhibited the weakest robustness against EDPA, it was chosen as the primary model for defense evaluation. The results demonstrate that adversarial fine-tuning not only strengthens OpenVLA’s resistance to EDPA but also significantly improves its robustness against previously proposed untargeted adversarial patch attacks (Wang et al., 2024). 

## 2 RELATED WORK 

### 2.1 VLA FOR EMBODIMENTS 

The concept of embodied AI was introduced by Machinery (1950) to examine whether agents can demonstrate intelligence through interaction with and navigation in complex physical environments, rather than just solving abstract problems in the digital world. In the early stages of developing generalist robots, prevailing approaches (Silva et al., 2021; Nair et al., 2022; Jang et al., 2022; Brohan et al., 2023) primarily relied on reinforcement learning or traditional imitation learning paradigms to acquire task-specific policies. 

In recent years, the advent of Large-scale Vision-Language Models (LVLMs) has shifted the paradigm toward leveraging these models to enhance generalization and language grounding in embodied agents, enabling robots to execute tasks directly from natural language instructions. Generalist robotic models such as RT-2 (Zitkovich et al., 2023), Octo (Team et al., 2024), OpenVLA (Kim et al., 2024), and _π_ 0 (Black et al., 2024), typically built upon LVLMs and commonly referred to as Vision-Language-Action (VLA) models, demonstrate strong generalization across diverse scenes and tasks, facilitating effective transfer to previously unseen scenarios. 

### 2.2 ADVERSARIAL ROBUSTNESS IN VLA 

Adversarial robustness is a fundamental challenge in securing deep learning models in computer vision. It concerns the resilience of these models to malicious input, known as adversarial attacks. Although primitive adversarial attacks (Goodfellow et al., 2014; Madry et al., 2017; Croce & Hein, 2020; Carlini & Wagner, 2017) demonstrate strong effectiveness in deceiving models through im- 

2 


Figure 1: **Overview of OpenVLA architecture and patch attack requirements.** Given a visual observation and a language instruction, the OpenVLA model first encodes the inputs into token-level latent representations. These representations are processed by the LVLM to produce action tokens, which are subsequently decoded into executable actions for the robotic platform. The colored dashed lines highlight the prior knowledge and/or access required by different patch attacks for various modules within the VLA: green for EDPA, purple for UADA, and red for UPA. 

perceptible pixel-level additive noise, they are often impractical in physical-world applications, as adversaries typically have limited access to the resources (Sharma et al., 2022) (e.g., adversary may not be able to directly modify the pixel of image). In this context, adversarial patch attacks (Brown et al., 2017; Karmon et al., 2018; Liu et al., 2018; Li et al., 2019) focus on manipulating a contiguous region of an image with perceptible but implementable perturbations (e.g., printed as stickers). Given that VLA models incorporate visual input, their adversarial robustness raises concerns analogous to those observed in other computer vision tasks, but studies in this field remain limited. 

|Category|Requirement|UADA (Wang et al., 2024)|UPA (Wang et al.|, 2024)<br>**EDPA (Ours)**|
|---|---|---|---|---|
|Knowledge|Victim Model<br>Robotic Manipulator|✓<br>✗|✗<br>✓|✗<br>✗|
|Access|Encoder Parameters<br>LVLM Parameters|✓<br>✓|✓<br>✓|✓<br>✗|


Table 1: Comparison of attack requirements between UADA, UPA, and EDPA. 

To the best of our knowledge, Wang et al. (2024) conducted the first systematic study on the robustness of VLA models against adversarial patch attacks. They proposed two untargeted adversarial patch attacks to explore the adversarial robustness of VLA: the Untargeted Action Discrepancy Attack (UADA) and the Untargeted Position-aware Attack (UPA). These attacks generate adversarial patches that aim to cause OpenVLA to produce action trajectories that deviate from the intended trajectories when controlling a 7-DoF robotic arm. UADA exploits the fact that OpenVLA uses part of the language model’s output tokens as action tokens that can be mapped to physical actions, and the differences in the numerical values of action tokens are correlated with differences in action magnitudes. Utilizing this property, UADA induces OpenVLA to output action tokens that deviate maximally from the ground-truth action tokens. In contrast, UPA directly operates on the first three components of the action vector. These components represent the 3D directional movements of the 

3 

7-DoF robotic arm, with UPA forcing OpenVLA to produce action vectors that deviate from the intended ones along these dimensions. 

These attacks exhibit limited generality, as they are specifically tailored to the unique characteristics of OpenVLA and the 7-DoF robotic arm, making them difficult to transfer to other VLA models or embodied agents. Furthermore, their execution relies on stringent conditions: the attacker must possess prior knowledge of the victim model design and the robotic manipulator, as well as access to all model parameters to compute gradients. In comparison, our proposed EDPA can operate without detailed knowledge of the victim model or the controlled robotic manipulator, relying solely on access to the encoder parameters, which makes it more practical for real-world scenarios (see Table 1 and Figure 1). 

## 3 METHODOLOGY 

### 3.1 PRELIMINARIES 

**Vision-language Action Models.** The architecture of SOTA VLA models built on top of largescaled LVLM commonly consist of three main components: 

(1) A **visual encoder** _Ev_ ( _·_ ) that transforms the visual input _v_ (i.e., an image) captured by a camera into a sequence of _image patch embeddings_ and projects them into the input space of the language model: 


where **p** _i_ denotes the _d_ -dimensional embedding of the _i_ -th image patch, and _N_ is the total number of patches. 

(2) A **language encoder** _Et_ ( _·_ ) that tokenizes the natural language instruction _t_ into a sequence of textual tokens and encodes them into _language tokens embeddings_ : 


where **w** _j_ denotes the _d_ -dimensional embedding of the _j_ -th token, and _M_ is the total number of tokens in the instruction. 

(3) The **LVLM backbone** _f_ ( _·_ ) processes the concatenated _image patch embeddings_ and _language token embeddings_ to generate an action vector: 


where _A_ denotes the generated action vector can be executed by robot manipulator. 

**Adversarial Patch Attack.** An adversarial patch attack is a specific type of adversarial attack in which the perturbation is applied to a localized area of the image, known as an adversarial patch. The patch is typically of a fixed shape (e.g., square or arbitrary) and can be randomly placed at any location within the image to mislead the model. 

Formally, given a clean visual input _v ∈_ [0 _,_ 1]<sup>_H×W ×C_</sup> and an adversarial patch _δ ∈_ [0 _,_ 1]<sup>_h×w×C_</sup> , the adversarial patch attack applies the patch _δ_ to _v_ by replacing the pixel values within the patch region: 


where _p_ is a binary mask indicating the patch’s shape and location, and _h_ and _w_ are the height and width of the patch. The operator _⊙_ denotes Hadamard element-wise multiplication. 

### 3.2 EMBEDDING DISRUPTION PATCH ATTACK 

A number of studies (Zhang et al., 2022; Zhao et al., 2023; Bagdasaryan et al., 2024; Lu et al., 2023; Zhang et al., 2025) have shown that adversarial attacks targeting embedding representations are generally highly effective against LVLMs. Since VLAs are built upon LVLMs, they likely inherit similar vulnerabilities. As these attacks typically rely on traditional pixel-level perturbations, directly applying them to VLAs that interact with the physical environment is impractical. Motivated 

4 

by this insight, we propose an untargeted adversarial patch method, **Embedding Disruption Patch Attack (EDPA)** , which specifically targets latent representations within VLA models. This method requires no access to the VLM backbone or prior knowledge of the model design and is agnostic to the type of robotic manipulator. The learning objective of the EDPA comprises two components: (1) disrupting the original semantic alignment between the _image patch embeddings_ of _v_ and the _language token embeddings_ of the language instruction _t_ , and (2) maximizing the discrepancy between the _image patch embeddings_ of the clean visual input _v_ and the adversarial visual input _v_<sup>_′_</sup> . To this end, we introduce the corresponding loss functions: the image-instruction alignment loss and the patch contrastive loss. 

**Image-Instruction Alignment Loss.** The semantic alignment between visual and language information is crucial for a model to correctly understand and execute language instructions. We aim to introduce our generated adversarial patch to alter the alignment between the visual and language in the embedding space, thereby disrupting the model’s perception of their semantic correspondence and interfering with its understanding and execution of the instruction. To quantify this effect, we define the image-instruction alignment loss, which measures the change in semantic alignment between the _image patch embeddings_ and the _language token embeddings_ of the corresponding language instruction. Formally, given a language instruction _t_ corresponding to the visual input _v_ , we measure the change in alignment between the _image patch embeddings Ev_ ( _v_ ) and _Ev_ ( _v_<sup>_′_</sup> ) with respect to the _language token embeddings Et_ ( _t_ ). To this end, we define the loss function as follow: 


where **p** _i_ and **p**<sup>_′_</sup> _i_<sup>denote the</sup><sup>_i_-th</sup><sup>_image patch embeddings_in</sup><sup>_Ev_(</sup><sup>_v_) and</sup><sup>_Ev_(</sup><sup>_v′_), respectively.Here,</sup><sup>_τ_</sup> is a scalar hyperparameter, and cos( _·, ·_ ) is the cosine similarity function. 

**Patch Contrastive Loss.** However, some VLA models exhibit limited capability in understanding the alignment between visual and language information (Kim et al., 2025). Therefore, we also aim to directly use an adversarial patch to induce the visual encoder to generate latent representations that substantially deviate from those produced in the absence of the patch, thereby disrupting the model’s understanding of essentially identical visual information and altering its outputs. To explicitly quantify this effect, we introduce the patch contrastive loss, which measures the discrepancy between the _image patch embeddings_ of the clean and perturbed visual inputs. Specifically, given a clean input visual input _v_ and its perturbed counterpart _v_<sup>_′_</sup> = _v ⊕ δ_ , we measure the embedding deviation between _Ev_ ( _v_ ) and _Ev_ ( _v_<sup>_′_</sup> ). Inspired by the InfoNCE (Oord et al., 2018), we define the loss function as follows: 


where **w** _j_ denotes the _j_ -th _language token embedding_ in _Et_ ( _t_ ). 

**Adversarial Patch Generation.** To construct a universal adversarial patch _δ_ , we formulate an optimization problem that jointly maximizes the patch contrastive loss (equation 2) and the imageinstruction alignment loss (equation 3) as following: 


where _D_ is the data distribution of visual inputs and _α_ 1 _∈_ [0 _,_ 1] is a hyperparameter controlling the relative contributions of each loss function. In practice, we find this objective effective in constructing adversarial patches that degrade the ultimate performance of the VLA model. 

5 

**Algorithm 1:** Adversarial Finetuning on Visual Encoder **Input:** Original visual encoder _Ev_<sup>orig</sup> , language encoder _Et_ , robotic dataset _D_ , hyperparameter _α_ 1, hyperparameter _α_ 2, step size _ηδ_ , patch reset frequency _φ_ , inner attack iterations _K_ , learning rate _η_ , max training iterations _T_ **Output:** visual encoder _Ev_<sup>_∗_</sup> Initialize _Ev ←Ev_<sup>orig</sup> , _δ ∼U_ (0 _,_ 1); **for** _i_ = 1 **to** _T_ **do** Sample minibatch ( _v, t_ ) _⊂D_ ; **if** _i_ mod _φ_ = 0 **then** Reinitialize _δ ∼U_ (0 _,_ 1); **for** _k_ = 1 **to** _K_ **do** _J ← α_ 1 _· L_ patch( _Ev_ ( _v_ ) _, Ev_ ( _v ⊕ δ_ )) + (1 _− α_ 1) _· L_ align( _Ev_ ( _v_ ) _, Ev_ ( _v ⊕ δ_ ) _, Et_ ( _t_ )); _δ ←_ clip( _δ_ + _ηδ ·_ sign( _∇δJ_ ) _,_ 0 _,_ 1) _L ← α_ 2 _· ∥Ev_ ( _v_ ) _−Ev_<sup>orig</sup> ( _v_ ) _∥_<sup>2</sup> 2<sup>+ (1</sup><sup>_−α_2)</sup><sup>_· ∥Ev_(</sup><sup>_v ⊕δ_)</sup><sup>_−E_</sup> _v_<sup>orig</sup> ( _v_ ) _∥_ 2<sup>2;</sup> Update _Ev_ by gradient descent with learning rate _η_ ; **return** _Ev_ ; 

### 3.3 ADVERSARIAL FINETUNING ON VISUAL ENCODER 

In the Section 3.2, we demonstrate that an effective adversarial patch _δ_ can be derived by directly targeting the embedding space of the VLA. In this section, we present a complementary adversarial finetuning scheme aimed at improving the robustness of the visual encoder _Ev_ ( _·_ ) within the VLA. 

The finetuning scheme incorporates adversarial visual inputs constructed from adversarial patches _δ_ generated by EDPA. Instead of relying solely on the final optimized _δ_ , the training process utilizes all intermediate patches produced during the EDPA training. Throughout the process, the current _δ_ is applied to the visual inputs to generate perturbed samples (refer to equation 1), which are then used to optimize the visual encoder. In addition, we adopt a fixed reset frequency for _δ_ , periodically reinitializing the patch during training to prevent overfitting to a specific patch and to ensure that the visual encoder is exposed to a diverse set of adversarial patches. 

The learning objective of the finetuning process mainly consists of two complementary objectives: (i) to encourage the fine-tuned visual encoder to produce latent representations of adversarially perturbed visual inputs that are close to those of the corresponding clean visual inputs produced by the original visual encoder, thereby enhancing the visual encoder’s robustness against adversarial patches; and (ii) to ensure that the latent representations generated by the fine-tuned visual encoder on clean visual inputs remain consistent with those generated by the original visual encoder, thereby preserving fidelity on clean visual inputs. As a result, the fine-tuned visual encoder can be directly integrated into the VLA without any modification or further fine-tuning of the LVLM backbone, mitigating the impact of adversarial patches while preserving overall performance. 

To formalize the learning objective of the finetuning scheme, let _Ev_<sup>orig</sup> ( _·_ ) denote the original visual encoder without being adversarial finetuned. The objective is to optimize the parameters of the updated visual encoder by solving the following optimization problem: 


where _δ_ denotes an adversarial patch generated by EDPA during its training procedure, and _α_ 2 _∈_ [0 _,_ 1] controls the relative contributions of the two learning objectives. The pseudocode of our finetuning scheme is shown in Algorithm 1. 

6 

## 4 EXPERIMENT 

### 4.1 EXPERIMENT SETTINGS 

**Dataset.** The adversarial patch generation through EDPA are conduct on LIBERO (Liu et al., 2023a), a simulation dataset specifically designed for robotic manipulation. The datasets comprises four distinct task suites: Spatial, Object, Goal, and Long. 

**Victim Models.** We evaluate recent open-source VLA models, including OpenVLA Kim et al. (2024), OpenVLA-OFT (Kim et al., 2025), and _π_ 0 (Black et al., 2024), all of which provide finetuned variants for LIBERO. Specifically, OpenVLA and OpenVLA-OFT each offer separate finetuned models for individual task suites, whereas _π_ 0 provides a single model fine-tuned across all task suites. 

**Baseline Method.** Given the limited research in this domain, no existing baseline directly matches our experimental setting. The most relevant untargeted adversarial patch attacks are UADA and UPA. However, these attacks are difficult to transfer to models other than OpenVLA due to their stringent application requirements. Therefore, we compare EDPA with UADA and UPA in terms of attack performance only on the OpenVLA model, while also evaluating the effectiveness of our defense method against them. Details of both experiments are provided in Section 4.2. For general experiments, we use a random noise baseline following Wang et al. (2024), where patches are sampled from a Gaussian distribution _N_ (0 _,_ 1) and evaluated under the same settings as EDPA. 

**Hyperparameter Settings.** In all experiments, the sizes of both adversarial and noise patches are fixed at 50×50 pixels, following Wang et al. (2024), while VLAs commonly receive visual inputs at a resolution of 224×224. During the generation of adversarial patches with EDPA, the hyperparameter _α_ 1, which controls the relative contribution of each loss, is set to 0.8, and the number of inner attack iterations _K_ is fixed at 1. Since the two losses may operate on different scales, exponential moving average (EMA) normalization is applied to each loss to ensure that _α_ 1 accurately governs their relative contributions. The step size _ηδ_ is set to 2 _/_ 255, and training proceeds for a maximum of _T_ = 50 _,_ 000 iterations with a batch size of 16. For the adversarial fine-tuning scheme, we set _α_ 2 = 0 _._ 5 to balance the two learning objectives, and the patch reset frequency _φ_ is set to 1000. The visual encoder is optimized using the Adam optimizer with a learning rate of _η_ = 1 _×_ 10<sup>_−_5</sup> . The sensitivity to some of these hyperparameter settings are reported in Appendix C. 

**Simulation and Evaluation Metric.** We evaluate our methods on all four task suites of the LIBERO simulation benchmark, with each suite comprising 10 tasks and 50 executions per task. Performance is measured using the Failure Rate (FR) metric following Wang et al. (2024), representing the proportion of tasks that were not successfully completed after a certain number of steps (defined as Failure Rate = 1 - Success Rate). To account for stochastic variability, reported FRs are averaged over three experiments with different random seeds, following Kim et al. (2024). 

### 4.2 EVALUATING ON SINGLE-CAMERA VLA 

In this subsection, we focus on evaluating the performance of our attack and defense methods on a single-camera VLA. We adopt OpenVLA as the representative model, which relies solely on visual input from the primary camera. In our evaluation, we measure the performance of OpenVLA before and after adversarial fine-tuning of the visual encoder when subjected to various patch-based attacks in the libero simulation benchmark. 

As shown in Table 2, the OpenVLA without adversarial fine-tuned visual encoder demonstrates almost no resilience to the adversarial patch attacks designed to mislead the model. Compared to common baselines, the adversarial patches generated via EDPA causes OpenVLA to increase its average failure rate on LIBERO tasks by approximately around 74.7% relative to the clean condition and by 53.0% relative to the random noise patch. For comparison with untargeted adversarial patch attacks specifically designed for OpenVLA, we also evaluated adversarial patches generated by UADA and UPA on the LIBERO dataset. The results show that UADA, UPA, and EDPA differ only marginally in effectiveness, as OpenVLA demonstrates minimal resilience against such adversarial patches. 

We then evaluate OpenVLA models integrated with an adversarially fine-tuned visual encoder against patch attacks. The results in Table 2 demonstrate such models exhibit substantially re- 

7 

Table 2: **Attack and defense performance on OpenVLA.** Average failure rates (FR) of OpenVLA models across four task suites in the LIBERO benchmark under different attacks, reported before and after adversarial fine-tuning. 

|**Source**|**Method**|**Failure**|**Rate (FR**_↑_**)**|
|---|---|---|---|
|||Original|Adversarial Finetuned|
||Clean|14.1_±_0.5|17.9_±_0.8|
||Random|34.8_±_1.1|19.4_±_1.4|
|**Spatial**|UADA|98.9_±_0.1|**65.4**_±_**1.0**|
||UPA|99.1_±_0.3|46.6_±_1.0|
||EDPA (Ours)|**100.0**_±_**0.0**|39.4_±_1.0|
||Clean|12.0_±_0.4|17.3_±_0.7|
||Random|39.2_±_1.4|16.0_±_0.9|
|**Object**|UADA|92.5_±_0.7|**58.8**_±_**1.4**|
||UPA|92.1_±_0.8|43.9_±_1.4|
||EDPA (Ours)|**100.0**_±_**0.0**|58.6_±_0.6|
||Clean|26.9_±_1.5|22.8_±_0.4|
||Random|37.9_±_0.7|23.0_±_1.1|
|**Goal**|UADA<br>UPA|98.6_±_0.1<br>98.9_±_0.2|**91.6**_±_**0.4**<br>68.3_±_1.7|
||EDPA (Ours)|**100.0**_±_**0.0**|73.9_±_1.1|
||Clean|48.1_±_1.9|49.0_±_0.3|
||Random|74.9_±_2.4|50.2_±_0.5|
|**Long**|UADA|99.6_±_0.2|**97.4**_±_**0.4**|
||UPA|99.6_±_0.3|86.7_±_0.9|
||EDPA (Ours)|**100.0**_±_**0.0**|91.2_±_0.5|


duced failure rates, with average decreases of 34.2% against EDPA and 21.5% against random noise patches in the LIBERO simulation environment. In parallel, the results demonstrate that adversarially fine-tuning the visual encoder not only mitigates the impact of EDPA but also confers improved robustness to OpenVLA against adversarial patches produced by other methods, with reductions in failure rates of 19.1% for UADA and 36.0% for UPA. Importantly, this improvement results in only a minor 1.6% increase in failure rate under clean conditions, reflecting the well-known trade-off between robustness and standard performance. 

### 4.3 EVALUATING ON MULTI-CAMERA VLA 

In this subsection, we evaluate the effectiveness of EDPA attacks on multi-camera VLAs. We use OpenVLA-OFT and _π_ 0 as the victim models, both of which rely on visual inputs from the primary camera as well as the wrist camera. In contrast to the primary camera, the wrist camera’s viewpoint changes substantially as the robot arm moves. Since real-time alignment of primary and wrist camera observations for the same patch is not feasible, we apply separate adversarial patches to each camera independently for evaluation. As UADA and UPA are difficult to transfer to models other than OpenVLA due to their stringent application requirements, we do not include them in the comparisons in this subsection. 

As shown in Table 3, EDPA increases the average failure rate on LIBERO tasks by approximately 62.0% for OpenVLA-OFT and 31.4% for _π_ 0. Compared with random noise, EDPA induces markedly higher increases in average failure rates of around 50.5%, and 26.5% for OpenVLA-OFT, and _π_ 0, respectively. These results indicate that EDPA remains highly effective against other (SOTA) multi-camera VLA models. Although the differences between OpenVLA, OpenVLA-OFT, and _π_ 0 extend beyond camera settings, the results suggest that VLAs processing multiple camera views may exhibit improved robustness to adversarial patches, potentially due to the additional visual information provided by multiple viewpoints. 

8 

Table 3: **Attack performance on Other VLAs.** The average failure rates (FR) of various finetuned VLA models on the four task suites in the LIBERO simulation benchmark under different perturbation levels. 

|**Source**|**Method**|**Failure Ra**|**te (FR)**_↑_|
|---|---|---|---|
|||OpenVLA-OFT|_π_0|
|**Spatial**|Clean<br>Random<br>EDPA|1.4_±_0.4<br>8.1_±_2.1<br>**39.7**_±_**0.9**|3.5_±_0.3<br>4.0_±_0.9<br>**29.8**_±_**1.6**|
||Clean|2.0_±_0.0|2.3_±_0.5|
|**Object**|Random<br>EDPA|15.9_±_0.4<br>**52.3**_±_**0.8**|4.3_±_0.3<br>**39.5**_±_**1.7**|
||Clean|2.8_±_0.7|12.0_±_1.6|
|**Goal**|Random<br>EDPA|5.1_±_0.1<br>**80.8**_±_**0.4**|17.5_±_1.3<br>**44.3**_±_**2.0**|
||Clean|4.9_±_0.6|40.8_±_1.6|
|**Long**|Random|28.1_±_2.4|51.9_±_0.8|
||EDPA|**86.4**_±_**1.9**|**70.7**_±_**1.6**|


(a) EDPA patches on OpenVLA, OpenVLA-OFT, and _π_ 0. 


(b) Patches generated through UADA and UPA on OpenVLA. 

Figure 2: **Visualization of Patch.** All the patches are generated on LIBERO dataset. 

## 5 PATCH VISUALIZATION AND DISCUSSION 

The Figure 2 illustrates representative adversarial patches produced by various patch-based attack methods on the LIBERO dataset. Specifically, Figure 2a shows patches generated by EDPA on OpenVLA, OpenVLA-OFT, and _π_ 0, while Figure 2b displays patches produced by UADA and UPA on OpenVLA (Wang et al., 2024). An interesting observation is that all generated patches consistently exhibit structural patterns reminiscent of a robotic arm. In particular, EDPA patches targeting OpenVLA and OpenVLA-OFT more closely resemble a robotic manipulator than those targeting _π_ 0. 

In light of these observations, we propose a hypothesis that slightly differs from Wang et al. (2024). We posit that the visual encoder of VLA models overfits to the appearance of robotic arms. This overfitting may be attributed to two factors: (1) the datasets used for robotic learning are much smaller in scale compared to internet-scale datasets; (2) the visual samples used for training are primarily captured from third-person camera viewpoints, which causes the robotic arm to appear in every visual sample and occupy a substantial portion of it. 

This hypothesis is also supported by our experimental findings. OpenVLA-OFT and _π_ 0 demonstrate greater robustness to EDPA compared to OpenVLA, likely because OpenVLA was trained primarily on visual input from the third-person camera. Although both OpenVLA-OFT and _π_ 0 can process multiple camera views, _π_ 0 exhibits superior robustness. This is likely because OpenVLA-OFT, even with wrist camera data added during fine-tuning, is based on the original OpenVLA model whose visual encoder had already overfitted during pretraining. In contrast, _π_ 0 incorporates wrist camera data from the pretraining stage, increasing the diversity of visual training data and thereby mitigating overfitting. 

9 

## 6 LIMITATION 

Despite the effectiveness of our methods, there are still some limitations that need to be acknowledged: (i) in multi-camera settings, we cannot compute the alignment of observations from different camera views for the same patch in real time. This limits EDPA’s ability to optimize patches under conditions that fully reflect their physical observation, potentially reducing attack effectiveness; and (ii) object position information cannot be directly obtained from static data, meaning the adversarial patch may occasionally occlude important objects. In such cases, our adversarial fine-tuning scheme on the visual encoder could potentially have a negative impact on the encoder’s performance. 

## 7 CONCLUSION 

In this study, we investigated the robustness of VLA models against adversarial patch attacks, a critical yet underexplored threat to their reliability. We first introduced a novel patch generation method, targeting the latent representation space of VLA models. We then proposed an adversarial fine-tuning strategy to enhance VLA robustness against such attacks. Our empirical results reveal significant vulnerabilities in current SOTA models and demonstrate that the proposed defense can effectively mitigate these threats. We hope this work will inspire future research efforts toward developing robust and secure vision-language embodied agents capable of safe deployment in complex real-world environments. 

## REPRODUCIBILITY STATEMENT 

Following the details provided in the main text, we ensure the reproducibility of our results by providing the loss functions, pseudocode, and the specific hyperparameters used in our experiments. Researchers can replicate our experiments and verify our findings using these descriptions and settings. While the results may not be exactly identical due to randomness factor in the experiments, they are expected to fall within a reasonable range. The codebase have released on github already. 

## ETHICS STATEMENT 

This work demonstrates a potential security threat in VLAs: carefully crafted adversarial patches can significantly degrade the performance of a VLA when placed within the camera’s view, causing the embodied agent to misinterpret visual information in the physical environment. This not only reduces the agent’s task success rate but also results in unexpected movement trajectories during task execution, posing hazards such as object mishandling, property damage, or actions endangering human safety. In this work, we do provide a method for generating such adversarial patches. We acknowledge that similar methods could be misused maliciously, but our intention is to highlight potential vulnerabilities in VLAs and to encourage the development of defenses methods against such attacks. Our goal is to promote the creation of embodied AI systems that are more robust, secure, and reliable. 

## REFERENCES 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Eugene Bagdasaryan, Rishi Jha, Vitaly Shmatikov, and Tingwei Zhang. Adversarial illusions in _{_ Multi-Modal _}_ embeddings. In _33rd USENIX Security Symposium (USENIX Security 24)_ , pp. 3009–3025, 2024. 

- Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow 

10 

model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ , 2024. 

- Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol Hausman, Alexander Herzog, Daniel Ho, Julian Ibarz, Alex Irpan, Eric Jang, Ryan Julian, et al. Do as i can, not as i say: Grounding language in robotic affordances. In _Conference on robot learning_ , pp. 287–318. PMLR, 2023. 

- Tom B Brown, Dandelion Man´e, Aurko Roy, Mart´ın Abadi, and Justin Gilmer. Adversarial patch. _arXiv preprint arXiv:1712.09665_ , 2017. 

- Nicholas Carlini and David Wagner. Towards evaluating the robustness of neural networks. In _2017 ieee symposium on security and privacy (sp)_ , pp. 39–57. Ieee, 2017. 

- Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry, and Alexey Kurakin. On evaluating adversarial robustness. _arXiv preprint arXiv:1902.06705_ , 2019. 

- Francesco Croce and Matthias Hein. Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks. In _International conference on machine learning_ , pp. 2206– 2216. PMLR, 2020. 

- Ian J Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. _arXiv preprint arXiv:1412.6572_ , 2014. 

- Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pp. 991–1002. PMLR, 2022. 

- Danny Karmon, Daniel Zoran, and Yoav Goldberg. Lavan: Localized and visible adversarial noise. In _International conference on machine learning_ , pp. 2507–2515. PMLR, 2018. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Juncheng Li, Frank Schmidt, and Zico Kolter. Adversarial camera stickers: A physical camerabased attack on deep learning systems. In _International conference on machine learning_ , pp. 3896–3904. PMLR, 2019. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023a. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023b. 

- Xin Liu, Huanrui Yang, Ziwei Liu, Linghao Song, Hai Li, and Yiran Chen. Dpatch: An adversarial patch attack on object detectors. _arXiv preprint arXiv:1806.02299_ , 2018. 

- Dong Lu, Zhiqiang Wang, Teng Wang, Weili Guan, Hongchang Gao, and Feng Zheng. Set-level guidance attack: Boosting adversarial transferability of vision-language pre-training models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 102–111, 2023. 

- Computing Machinery. Computing machinery and intelligence-am turing. _Mind_ , 59(236):433, 1950. 

- Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, and Adrian Vladu. Towards deep learning models resistant to adversarial attacks. _arXiv preprint arXiv:1706.06083_ , 2017. 

- Suraj Nair, Eric Mitchell, Kevin Chen, Silvio Savarese, Chelsea Finn, et al. Learning languageconditioned robot behavior from offline data and crowd-sourced annotation. In _Conference on Robot Learning_ , pp. 1303–1315. PMLR, 2022. 

11 

- Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- Abhijith Sharma, Yijun Bian, Phil Munz, and Apurva Narayan. Adversarial patch attacks and defences in vision-based tasks: A survey. _arXiv preprint arXiv:2206.08304_ , 2022. 

- Andrew Silva, Nina Moorman, William Silva, Zulfiqar Zaidi, Nakul Gopalan, and Matthew Gombolay. Lancon-learn: Learning with language to enable generalization in multi-task manipulation. _IEEE Robotics and Automation Letters_ , 7(2):1635–1642, 2021. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 

- Taowen Wang, Cheng Han, James Chenhao Liang, Wenhao Yang, Dongfang Liu, Luna Xinyu Zhang, Qifan Wang, Jiebo Luo, and Ruixiang Tang. Exploring the adversarial vulnerabilities of vision-language-action models in robotics. _arXiv preprint arXiv:2411.13587_ , 2024. 

- Jiaming Zhang, Qi Yi, and Jitao Sang. Towards adversarial attack on vision-language pre-training models. In _Proceedings of the 30th ACM International Conference on Multimedia_ , pp. 5005– 5013, 2022. 

- Jiaming Zhang, Junhong Ye, Xingjun Ma, Yige Li, Yunfan Yang, Yunhao Chen, Jitao Sang, and Dit-Yan Yeung. Anyattack: Towards large-scale self-supervised adversarial attacks on visionlanguage models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 19900–19909, 2025. 

- Yunqing Zhao, Tianyu Pang, Chao Du, Xiao Yang, Chongxuan Li, Ngai-Man Man Cheung, and Min Lin. On evaluating adversarial robustness of large vision-language models. _Advances in Neural Information Processing Systems_ , 36:54111–54138, 2023. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

## APPENDIX 

## A ATTENTION VISUALIZATION 

To gain deeper insight into how EDPA disrupts the performance of VLAs, we examine the average attention weights from linguistic tokens to visual input locations. Specifically, we use OpenVLA as the victim model and visualize the averaged attention weights across all heads in both the first and last layers under three perturbation conditions: clean, random, and EDPA. Here, clean denotes unperturbed inputs, random corresponds to patches generated from Gaussian noise, and EDPA refers to adversarial patches produced by our method (Section 3.2). To isolate their effects, all perturbation patches are fixed at the top-left corner of the visual input. 

In Figure 3, we present the first-layer average attentions of OpenVLA for three sampled linguistic tokens with respect to their corresponding image regions. For clean samples, the tokens correctly attend to the robot arm and other salient objects visible in the camera view. Under random perturbations, the attention distributions remain largely stable. In contrast, when adversarial patches generated by EDPA are applied, the first-layer attentions shift dramatically: the tokens concentrate predominantly on the patch location, while their focus on the originally relevant objects and the robot arm is markedly reduced. 

Figure 4 shows that this phenomenon also persists in the final attention layer of OpenVLA. Compared to the first layer, the linguistic tokens in the last layer exhibit more localized focus on specific 

12 


Figure 3: Average attention weights of each linguistic token to the primary camera input in the first layer of OpenVLA. 

regions within the image. However, when adversarial patches derived from EDPA are introduced, a clear change in the attention distribution emerges: the patch location receives disproportionately high attention, while focus on originally important objects is markedly diminished. 

In summary, these visualizations demonstrate that adversarial patches generated by EDPA can substantially distort the attention distribution of linguistic tokens over the visual input, thereby undermining model performance. 

## B TRANSFERABILITY OF EDPA 

In practice, an adversary may not have full access to the finetuned model or the dataset of downstream task. Here, we evaluate the transferability of EDPA under two scenarios: (1) _cross-dataset transferability_ , where the adversary lacks access to downstream task data; and (2) _cross-model transferability_ , where the adversary has access only to the victim’s base model. 

To evaluate _cross-dataset transferability_ , we generate adversarial patches on LIBERO-Spatial and apply them to the other three task suites within the LIBERO simulation benchmark. As shown in Table 4, EDPA demonstrates strong dataset-level transferability, substantially increasing the average failure rates about 74.7%, 52.4%, and 33.7% for OpenVLA, OpenVLA-OFT, and _π_ 0, respectively. Interestingly, the attack performance of EDPA is comparable to that observed under fully white-box settings, suggesting that EDPA requires minimal knowledge of the training data and that an adver- 

13 


Figure 4: Average attention weights of each linguistic token to the primary camera input in the last layer of OpenVLA. 

Table 4: The average failure rates (FR) of different fine-tuned VLA models on the other three task suites in the LIBERO simulation benchmark on EDPA adversarial patches derived from LIBEROSpatial. 

|**Source**||**Failure Rate (FR)**||
|---|---|---|---|
||OpenVLA|OpenVLA-OFT|_π_0|
|**Object**|100.0_±_0.0|32.2_±_1.0|30.3_±_1.2|
|**Goal**|100.0_±_0.0|71.8_±_0.9|42.7_±_2.2|
|**Long**|100.0_±_0.0|61.4_±_1.6|71.9_±_0.9|


sary can effectively compromise VLA performance even without access to data from the targeted task. 

In parallel, we examine the _cross-model transferability_ of EDPA in a scenario where the adversary has no access to the victim model but can leverage its corresponding base model to generate adversarial patches, which are subsequently transferred to the downstream variant. As summarized in Table 5, these transferred patches increase the average failure rates around 49.8%, 26.98%, and 9.3% for OpenVLA, OpenVLA-OFT, and _π_ 0, respectively, evaluated across the four task suites within the LIBERO simulation benchmark. These findings indicate that, although the _cross-model transferability_ of EDPA is generally lower than that observed under fully white-box settings or in cross-dataset 

14 

Table 5: The average failure rates (FR) of different fine-tuned VLA models on the four task suites in the LIBERO simulation benchmark on EDPA adversarial patches derived from the base model. 

|**Source**||**Failure Rate (FR)**||
|---|---|---|---|
||OpenVLA|OpenVLA-OFT|_π_0|
|**Spatial**|71.5_±_1.4|12.3_±_0.6|7.1_±_0.3|
|**Object**|69.4_±_1.7|31.6_±_1.6|10.0_±_1.4|
|**Goal**|67.4_±_1.7|32.8_±_0.2|22.7_±_0.8|
|**Long**|91.9_±_1.8|42.3_±_3.2|55.8_±_1.1|


transfer scenarios, it nonetheless maintains significant attack effectiveness against downstream VLA variants. 

- C ABLATION STUDY 

- C.1 IMPACT OF ADVERSARIAL PATCH SIZE ON VLA PERFORMANCE 


Figure 5: **Impact of patch size.** The figure shows how varying patch sizes of EDPA affect the average failure rate (FR) across different VLA models on the LIBERO simulation benchmark. 

In our primary experiments, we fix the patch size at 50 _×_ 50 pixels, consistent with prior work, to enable a fair comparison with baseline. In this section, we further investigate how varying the size of adversarial patches generated by EDPA influences the performance of VLA models. In our experimental setup, we generate adversarial patches using EDPA with sizes determined as 2%, 4%, 8%, and 10% of the total visual observation area, study their impact on different VLA model performance. We report the average failure rate across four task suites in the LIBERO simulation benchmark for each model under different patch sizes in Figure 5. 

The experimental results demonstrate that the performance of all VLA models is consistently affected by the size of adversarial patches. As the patch size increases, the failure rate of all models in executing robotic tasks also rises. This trend suggests that larger adversarial patches lead to stronger degradation of the model’s performance. 

15 

### C.2 ANALYZING THE IMPACT OF _α_ 1 ON EDPA’S EFFECTIVENESS IN VLAS 

To investigate how the hyperparameter _α_ 1 influences the effectiveness of EDPA, we conduct a series of experiments by systematically varying _α_ 1 while keeping all other settings fixed. This hyperparameter controls the relative contribution of the two loss functions during patch optimization and is expected to impact the failure rate of VLAs in robotic task execution. In the main experiments, we set _α_ 1 to 0.8. We further evaluate EDPA with _α_ 1 set to 0, 0.2, 0.5, 0.8, and 1 to examine how different trade-offs between these objectives affect the performance of various VLAs in the LIBERO simulation benchmark. 


Figure 6: **Impact of hyperparameter** _α_ 1 **.** The figure illustrates how varying _α_ 1 affects the performance of EDPA in terms of average failure rate (FR) across different VLA models on the LIBERO simulation benchmark. 

The results are summarized in Figure 6. EDPA generates effective adversarial patches for OpenVLA across all _α_ 1 settings, indicating that both loss terms contribute to attacks that the model cannot resist. On OpenVLA-OFT, the highest failure rate occurs at _α_ 1 = 0 _._ 2, but variations in _α_ 1 do not result in substantial differences in attack performance. However, the failure rate of _π_ 0 increases clearly with higher _α_ 1, suggesting that a larger contribution of _L_ patch enhances the effectiveness of EDPA on this model. In summary, the effectiveness of EDPA varies across different VLA models. The sensitivity of each model to the hyperparameter _α_ 1 differs, suggesting that the two loss functions have varying effectiveness depending on the target VLA. 

## D LARGE LANGUANGE MODEL USAGE STATEMENT 

The large language model was only used to polish the language during the preparation of this manuscript. Specifically, we used the well-known LLM ChatGPT<sup>1</sup> for this purpose. The model was not used to generate any technical content, ideas, or analyses. 

1https://chatgpt.com 

16 

