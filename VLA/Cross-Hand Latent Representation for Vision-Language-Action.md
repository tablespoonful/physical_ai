---
title: "Cross-Hand Latent Representation for Vision-Language-Action Models"
date: "2026-03-10"
authors: "Guangqi Jiang; Yutong Liang; Jianglong Ye; Jia-Yang Huang; Changwei Jing; Rocky Duan"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2603.10158
pdf: https://arxiv.org/pdf/2603.10158
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.10158)** / [論文ページ](https://arxiv.org/abs/2603.10158)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Cross-Hand Latent Representation for Vision-Language-Action Models** 

Guangqi Jiang<sup>1</sup><sup>_∗_</sup> Yutong Liang<sup>1</sup><sup>_∗_</sup> Jianglong Ye<sup>1</sup> Jia-Yang Huang<sup>1</sup> Changwei Jing<sup>1</sup> Rocky Duan<sup>2</sup> Pieter Abbeel<sup>2</sup><sup>_,_3</sup> Xiaolong Wang<sup>1</sup><sup>_†_</sup> Xueyan Zou<sup>1</sup><sup>_†_</sup> 1UC San Diego 2Amazon FAR 3UC Berkeley _∗_ Equal Contribution _†_ Equal Advising https://xl-vla.github.io 


Figure 1. **Overview.** XL-VLA enables direct decoding of a single latent action into multiple dexterous hand embodiments. Shown above, an action prediction can be instantiated on the Ability hand, Paxini DexH13 hand, X-Hand1, and Inspire hand for languageguided manipulation. We show our experiment settings on the right figure with collected objects and DexHands. 

## **Abstract** 

_Dexterous manipulation is essential for real-world robot autonomy, mirroring the central role of human hand coordination in daily activity. Humans rely on rich multimodal perception—vision, sound, and languageguided intent—to perform dexterous actions, motivating vision-based, language-conditioned manipulation systems for robots. However, training reliable visionlanguage-action (VLA) models for dexterous manipulation requires large-scale demonstrations across many robotic hands. In addition, as new dexterous embodiments appear rapidly, collecting data for each becomes costly and impractical, creating a need for scalable cross-embodiment learning. We introduce XL-VLA, a vision-language-action framework integrated with a unified latent action space shared across diverse dex-_ 

_terous hands. This embodiment-invariant latent space is directly pluggable into standard VLA architectures, enabling seamless cross-embodiment training and efficient reuse of both existing and newly collected data. Experimental results demonstrate that XL-VLA consistently outperforms baseline VLA models operating in raw joint spaces, establishing it as an effective solution for scalable cross-embodiment dexterous manipulation._ 

## **1. Introduction** 

Recent progress in vision-language-action (VLA) modeling has begun to extend the successes of large-scale vision and language models into robotics, enabling robots to interpret visual scenes, follow natural language instructions, and execute complex behaviors in the physical world. A key insight behind these advances is that 

13496 

|**Paper**|**Data**|**Deploy**|**ment**||**Input**||**Out**|**put**|
|---|---|---|---|---|---|---|---|---|
||**Type(s)**|**Embodiment**|**EEF**_↔_**EEF**|**Vision**|**Lang**|**Prop**|**Decod**|**er ZS**|
|**UniVLA**[8]|human video; teleoperation|1 arm+1 gripper|gripper_↔_gripper|✓|✓|✗|✓|✗|
|**ATE**[71]|teleoperation; simulation|2 arms+2 grippers|—|✓|✓|✗|✗|✗|
|**LAD**[3]|teleoperation|1 arm+1 hand/gripper|hand_↔_hand/gripper|✓|✗|✗|✓|✗|
|**EgoBridge**[45]|human video; teleoperation|2 arms+2 pushers|—|✓|✗|✓|✗|✗|
|**CoMo**[65]|internet video; teleoperation|1 arm+1 gripper|—|✓|✗|✗|✗|✗|
|**Tenma**[17]|teleoperation|2 arms+2 grippers|—|✓|✓|✓|✗|✗|
|**CycleVAE**[16]|teleoperation|1 arm+1 hand|hand_↔_hand|✗|✗|✓|✓|✗|
|**CETransfer**[53]|simulation (sim_→_real)|1 arm+1 gripper|gripper_↔_gripper|✗|✗|✓|✓|✓|
|**Ours**|teleoperation|2 arm+2 hand|hand_↔_hand|✓|✓|✓|✓|✓|


Table 1. **Related Work Summary.** Summary of related work comparing data sources, deployment settings, and input/output capabilities for latent-based cross-embodiment methods. Data indicates the training modalities used in each work. Deployment specifies the robot embodiments evaluated and whether cross–end-effector transfer is supported. Input denotes which modalities (vision, language, proprioception) are used for training. Output reports whether a method includes a cross-embodiment decoder and whether it enables zero-shot transfer to unseen embodiments. 

unifying vision and language can be naturally expressed through sequence-to-sequence modeling, and VLA systems can adopt the same abstraction by treating actions as an additional output modality. 

However, a fundamental obstacle emerges when moving from vision and language to action: while language possesses a relatively stable and universal vocabulary, robotic action spaces are inherently tied to the morphology of the robot. For dexterous hands in particular, action parameterizations—joint positions—vary significantly across embodiments and continue to evolve rapidly with new hardware designs. This raises two key questions for scalable robot learning: (1) _How can we define a unified action representation within a family of robots?_ (2) _How can we seamlessly integrate a new robot whose action space differs from existing ones?_ 

In this work, we address these challenges by introducing a _shared latent action space_ tailored for **dexterous hands** . This latent space serves as an embodimentinvariant representation that enables joint training across heterogeneous hands. While prior VLA and crossembodiment efforts have primarily focused on robotic arms equipped with parallel grippers, we focus on the substantially more complex, and more capable domain of dexterous manipulation. Moreover, we emphasize _real-world_ datasets and physical robot evaluation, demonstrating that our method remains robust under significant cross-embodiment variation. 

We summarize our contributions as follows: 

- We collect a large-scale teleoperation dataset covering 10 manipulation tasks across four newly introduced dexterous hands—Ability, Paxini DexH13, X-Hand1, and Inspire—containing 2M state-action pairs. 

- We propose an unsupervised latent autoencoder framework that learns a unified action space applicable to a wide range of hands. 

- We introduce XL-VLA, a full VLA pipeline built upon the cross-embodiment latent action space. XL-VLA achieves significantly stronger cross-embodiment performance than standard VLA baselines and exhibits **zero-shot generalization** to untrained crossembodiment task configurations. 

## **2. Related Work** 

**Dexterous Manipulation.** The direction of dexterous manipulation focuses on utilizing DexHand for standard manipulation tasks, aiming to enable more complex operations. This field encompasses various areas of focus, including manipulator hardware [34, 48, 67], sensors [51, 63], learning and control algorithms [12, 28, 31, 40], and human-robot interaction [13, 23, 61]. In this work, we specifically concentrate on learning and control algorithms, leveraging vision-language-action (VLA) models [30, 36, 46, 50, 69]. Furthermore, we define a unified action space to support cross-embodiment dexterous manipulation [24, 44, 55]. 

**Cross Embodiment.** Cross embodiment typically refers to learning a _single_ policy that can flexibly adapt across diverse embodiments—e.g., different humanoids or dexterous hands—without per-robot retraining [21, 22, 25, 26, 43, 52, 66, 74]. Within this area, approaches leverage human video for supervision [15, 32, 42, 45, 47, 70], apply imitation learning with motion retargeting to bridge morphology gaps [11, 39, 49, 59], and employ generative models to synthesize action-consistent trajectories across bodies [1, 3, 27, 57, 75]. A complementary line of work constructs unified latent action spaces that factor out embodiment-specific details, enabling transfer and zero-shot reuse across platforms [3, 9, 17, 54, 71, 73]. This paper follows the latter paradigm, aligning actions in a shared representation for robust cross-embodiment control. 

13497 


Figure 2. **Model Pipeline.** XL-VLA builds on _π_ 0 [6] with vision and language encoders paired with an action expert that operates in a shared latent action space for cross-embodiment control. During VLA training, the action expert is finetuned while the pretrained latent encoders and decoders remain frozen. 

**Hand/Dex Retargeting.** Hand retargeting for teleoperation and imitation learning has progressed from kinematic pipelines to fast, principled learning: GeoRT delivers 1 kHz unsupervised mapping [68]; contact-aware and unified formulations improve human–object fidelity [35, 37], with objective ablations [60] and practical systems spanning real-time teleop and hardware-agnostic platforms [14, 19, 58]. Beyond copying humans, functional and policy-centric retargeting improves task outcomes [41, 62], while type-guided teleop exploits robotspecific dexterity [38]. 

**Latent Action Space.** As shown in Table. 1, latent action spaces provide embodiment agnostic control codes that align input modalities (vision, language, proprioception) and decode to diverse robots. Examples span discrete VQ tokens with per-robot decoders [8], continuous end-effector latents trained on retargeted pairs and generated by diffusion [3], and unified action VAEs that steer existing VLA policies [71]. Other directions align policy features or motion rather than a single EEF space optimal-transport co-training [45], Internet-video motion embeddings [65], diffusion transformers with standardized tokens [17] and cycle/adversarial mappings enabling cross-embodiment decoding and sim→real transfer [16, 53]. 

**Vision-Language-Action Model.** VLA models adapt large vision–language models (VLMs) to robot control by discretizing actions and predicting them autoregressively, enabling transfer of web-scale priors to manipulation [7, 29, 33, 56]. While these systems demonstrate broad generalization, their tokenized action decoding can hinder high-rate, dexterous control [72]. In contrast, we fine-tune a pre-trained VLM backbone initialized from PaliGemma [5] on teleoperated trajectories. Our action expert regresses continuous _latent action chunks_ : each target is represented by a single latent vector produced by our hand-specific encoder. During training, we replace _π_ 0’s original state tokens with these latent tokens and finetune on the next latent chunk, allowing a single hand-agnostic VLA policy to operate across multiple dexterous hands while preserving the 

benefits of VLM pretraining. 

## **3. Method** 

### **3.1. Preliminary** 

**Problem Formulation.** In this work, we address the problem of _language-guided cross-embodiment dexterous manipulation_ based on visual perception. For a dexterous hand _h ∈H_ with _dh_ actuated joints we control absolute joint rotations **q**<sup>(</sup><sup>_h_)</sup> _∈_ R<sup>_dh_</sup> . At the policy level we operate on _action chunks_ : each action **q**<sup>(</sup> _t_<sup>_h_)</sup> _∈_ R<sup>64</sup><sup>_×dh_</sup> is a sequence of 64 joint-position commands sampled at 20 Hz (3.2 s of motion). At control step _t_ , the policy receives a short history of joint states, the previously executed action chunk **q**<sup>(</sup> _t_<sup>_h_)</sup> , the current image observations **V** , and a language instruction **T** , and predicts the next chunk **q**<sup>(</sup> _t_ +1<sup>_h_)via</sup><sup>**q**(</sup> _t_ +1<sup>_h_)=</sup><sup>_F_(</sup><sup>**q**</sup> _t_<sup>(</sup><sup>_h_)</sup> _,_ **V** _,_ **T** ). The objective is to predict embodiment-consistent joint-rotation trajectories conditioned on these multimodal inputs with a unified multi-task VLA model. Although the continuous joint spaces **q**<sup>(</sup><sup>_h_)</sup> are handspecific, the sequence model _F_ itself is hand-agnostic; the hand identity _h_ is used only to choose the appropriate encoder/decoder that maps between joint space and the shared latent action space described below. To evaluate this setting, we consider a diverse set of dexterous robotic hands, including the _Ability Hand_ , _Inspire Hand_ , _X-Hand1_ , and _Paxini DexH13_ , which vary in structure, actuation, and kinematics. 

To tackle this problem, we introduce an embodimentinvariant latent action space that integrates seamlessly into a vision–language–action (VLA) framework. This latent space provides a unified representation across diverse dexterous hands, enabling the model to train effectively on cross-embodiment data and generalize manipulation skills beyond a single hand morphology. Furthermore, the proposed latent space supports transferring control policies across different embodiments without requiring hand-specific retraining. **Pipeline.** As illustrated in Fig. 2, our proposed framework consists of two main components: (1) a VLA back- 

13498 

bone that encodes multimodal inputs ( **V** _,_ **T** ), and (2) a pretrained set of latent encoders and decoders designed for cross-embodiment transfer. Our VLA design follows _π_ 0 [6], which employs vision and language encoders together with an action expert. In the original _π_ 0, proprioceptive history is provided through a stack of state tokens. In XL-VLA we instead feed _latent action tokens_ : for each hand _h_ , a hand-specific encoder _Eh_ maps the previous absolute joint-position action chunk **q**<sup>(</sup> _t_<sup>_h_)</sup> (64 frames at 20 Hz) into a compact latent vector **z** _t_ = _Eh_ ( **q**<sup>(</sup> _t_<sup>_h_)</sup> ). The VLA model conditions on a short history of such latent tokens, together with vision and language tokens, and predicts the next latent chunk � **z** _t_ +1. This latent is decoded by the embodiment-specific decoder _Dh_ to obtain the next joint command chunk **q** �<sup>(</sup> _t_ +1<sup>_h_)=</sup><sup>_Dh_(�</sup><sup>**z**</sup><sup>_t_+1).DuringVLAfinetuningwekeep</sup> all latent encoders and decoders frozen. 

This embodiment-invariant latent representation **z** acts as a unified action space shared across heterogeneous dexterous hands. By learning and decoding actions within this latent space, the model effectively bridges differences in morphology and actuation across embodiments, enabling a single hand-agnostic VLA policy to operate on diverse robotic hands. The hand identity _h_ is used only to select the appropriate encoder _Eh_ and decoder _Dh_ and is never provided as an explicit input token to the VLA backbone. We describe the detailed design and training of this latent action space in the following sections. 

### **3.2. Latent Space** 

**Definition.** Rather than defining a separate action space for each dexterous hand, we introduce a _shared latent action space_ that provides a unified representation for all dexhand embodiments. This latent space is pretrained independently of the VLA model through a set of handspecific encoders and decoders that all map to the same latent distribution. As a result, the latent embedding acts as an implicit, embodiment-agnostic action space that can be used by downstream policies to seamlessly control different dexterous hands. 

#### **3.2.1. Modeling** 

To construct the latent representation, we employ a multi-headed VAE-style autoencoder. For each hand type _h ∈H_ (e.g., X-Hand, Ability, Inspire, Paxini), we define a hand-specific encoder _Eh_ and decoder _Dh_ . Each hand provides a joint configuration **q**<sup>(</sup><sup>_h_)</sup> _∈_ R<sup>_dh_</sup> , where **q**<sup>(</sup><sup>_h_)</sup> denotes the joint position values (q-pos) and _dh_ is the dimensionality of that embodiment. The encoder outputs the parameters of a Gaussian posterior ( **_µ_**<sup>(</sup><sup>_h_)</sup> _,_ **_σ_**<sup>(</sup><sup>_h_)</sup> ) = _Eh_ ( **q**<sup>(</sup><sup>_h_)</sup> ), from which we sample a latent code **z** using the reparameterization trick, _q_ ( **z** _|_ **q**<sup>(</sup><sup>_h_)</sup> ) = _N_ ( **_µ_**<sup>(</sup><sup>_h_)</sup> _,_ diag(( **_σ_**<sup>(</sup><sup>_h_)</sup> )<sup>2</sup> )). The decoder recon- 


Figure 3. **Latent space pretraining pipeline.** For each hand type, joint positions **q** _h_ are mapped through an encoder MLP into a shared latent space and reconstructed by a decoder MLP. The diagram also indicates the placement of the reconstruction loss _L_ 1, retargeting loss _L_ 2 via differentiable forward kinematics, and latent regularization loss _L_ 3. 

structs back into the corresponding joint space **q** ˆ<sup>(</sup><sup>_h_)</sup> = _Dh_ ( **z** ). 

In practice, each encoder and decoder is implemented as a lightweight MLP: the input q-pos vector **q**<sup>(</sup><sup>_h_)</sup> is projected into a common latent space through the encoder MLP, and the decoder MLP reprojects the latent embedding back into the hand’s original joint configuration. This architecture provides a unified latent manifold while preserving the structure of each embodiment. To shape a meaningful cross-embodiment latent space, we impose three training constraints: (1) a _reconstruction constraint L_ 1 ensuring **q** ˆ<sup>(</sup><sup>_h_)</sup> matches **q**<sup>(</sup><sup>_h_)</sup> , (2) a _retargeting constraint L_ 2 aligning fingertip geometry across hands using differentiable forward kinematics, and (3) a _latent constraint L_ 3 regularizing the latent embedding to follow a smooth prior distribution. Together, these constraints encourage the latent space to capture embodiment-invariant structure, enabling consistent decoding into any dexterous hand. 

#### **3.2.2. Objective** 

**Reconstruction Loss (** _L_ 1 **).** Since each DexHand embodiment has its own joint space, we first require that the hand-specific encoder-decoder pair behaves as an autoencoder on that hand. Given a joint configuration **q**<sup>(</sup><sup>_h_)</sup> and its reconstruction **q** ˆ<sup>(</sup><sup>_h_)</sup> for hand _h ∈H_ , the reconstruction loss averaged over all hands is 


which ensures that the latent space preserves handspecific kinematics and that no embodiment is degraded by sharing the latent representation. 

**Retargeting Loss (** _L_ 2 **).** To make the latent space truly cross-embodiment, we align fingertip geometry between different DexHand robots. For each hand _h_ , we use differentiable forward kinematics (FK) to map joints to fingertip positions **p**<sup>(</sup> _i_<sup>_h_)</sup> , and define fingertip displacements **_δ_**<sup>(</sup> _ij_<sup>_h_)</sup> = **p**<sup>(</sup> _i_<sup>_h_)</sup> _−_ **p**<sup>(</sup> _j_<sup>_h_)</sup> for fingertip pairs ( _i, j_ ) _∈P_ . The pair set _P_ contains thumb–finger pairs for the four aligned digits (thumb–index, thumb–middle, thumb– ring, thumb–little). We manually align finger indices 

13499 

|**Method**|**Hand**|**PF**|**SC**|**SoC**|**HB**|**RL**|**PS**|**RB**|**PuS**|**PoS**|**PC**|**Mean**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Ability|0.10|0.10|0.00|0.70|0.20|0.80|0.60|0.30|0.30|0.60|0.37|
|6|Inspire|0.10|0.20|0.00|0.30|0.10|0.50|0.30|0.20|0.20|0.80|0.27|
|_π_0 []|Paxini|0.40|0.40|0.30|0.20|0.00|0.80|0.60|0.30|0.10|0.40|0.35|
||XHand|0.20|0.40|0.00|0.40|0.10|0.60|0.30|0.20|0.30|0.40|0.29|
||Mean|0.20|0.28|0.08|0.40|0.10|0.68|0.45|0.25|0.23|0.55|0.32|
||Ability|**0.80**|**0.80**|0.40|**1.00**|0.70|**1.00**|0.70|0.30|0.90|0.70|0.73|
|XLVLA|Inspire|0.60|0.50|0.50|0.80|0.40|0.80|**1.00**|**0.40**|0.80|**1.00**|0.68|
|-|Paxini|**0.80**|0.70|**0.80**|**1.00**|0.30|**1.00**|**1.00**|**0.40**|0.80|**1.00**|**0.78**|
||XHand|0.60|0.50|0.50|**1.00**|0.30|**1.00**|0.90|0.30|**1.00**|0.90|0.70|
||Mean|0.70+50%|0.63+35%|0.55+47%|0.95+55%|0.43+33%|0.95+27%|0.90+45%|0.35+10%|0.88+65%|0.90+35%|0.72+40%|


Table 2. **Vision-Language-Action Modeling.** We compare XL-VLA with _π_ 0 under cross-embodiment training. Although _π_ 0 can handle different embodiments by adjusting sequence length, our method achieves consistently higher success rates across all hands and tasks. The first row PF, SC, SoC, etc. denote each task introduced in Task & Dataset, and each task is executed for 10 times, and we compute the success rate for each task cross hand. 

across hands so that these digits correspond semantically; for Paxini DexH13, which lacks a little finger, we drop any pairs involving that digit when evaluating _L_ 2. The retargeting loss penalizes discrepancies in pinch distances and directions between source hands _s_ and target hands _t_ : 


where **_δ_**<sup>ˆ</sup> ( _ijt_ )<sup>iscomputedfromthedecodedconfigura-</sup> tion of hand _t_ , _c_<sup>(</sup> _ij_<sup>_s,t_)</sup> denotes the cosine of the angle be( _t_ ) tween the pinch directions **_δ_**<sup>(</sup> _ij_<sup>_s_)</sup> and **_δ_**<sup>ˆ</sup> _ij_<sup>,and</sup><sup>_w_</sup> _ij_<sup>(</sup><sup>_s_)</sup> = exp( _−λ_<sup>exp</sup> dis<sup>_∥_</sup><sup>**_δ_**(</sup> _ij_<sup>_s_)</sup><sup>_∥_2)emphasizestighterpinches.</sup> This loss encourages the same latent code to produce geometrically consistent pinch behaviors across different hands. 

**Latent Loss (** _L_ 3 **).** Finally, we regularize the DexHand latent space to be smooth and well-behaved by imposing a standard Gaussian prior on the latent variables. For the approximate posterior _q_ ( **z** _|_ **q** ) produced by the handspecific encoders, the latent loss is 


which encourages the shared DexHand latent space to follow a _N_ (0 _, I_ ) distribution and facilitates sampling and interpolation across embodiments. 

**Training Data and Protocol.** The latent autoencoder is trained _without_ any demonstration or IK-generated trajectories. Instead, for each hand _s ∈H_ we randomly sample joint configurations within the hardware joint limits to form synthetic joint-position vectors **q**<sup>(</sup><sup>_s_)</sup> . For every such sample we encode **q**<sup>(</sup><sup>_s_)</sup> to a latent **z** , decode it through all decoders _{Dt}t∈H_ , and accumulate reconstruction and retargeting losses: the self-decoding 

_Ds_ ( **z** ) contributes to _L_ 1, while cross-hand decodings _Dt_ ( **z** ) for _t̸_ = _s_ contribute to _L_ 2. Losses from all hands are aggregated and a single backward pass is applied, so all encoders and decoders are optimized jointly. Because _L_ 2 uses only forward kinematics of each hand and decoded poses, the alignment of the latent space across embodiments is completely self-supervised and does not require any paired cross-hand trajectories. 

**Total Latent Objective.** The full latent training loss combines reconstruction, retargeting, and KL regularization: 


In all experiments we fix the weights to _β_ = 10<sup>_−_5</sup> , _λ_ dis = 2000 _._ 0, _λ_ dir = 5 _._ 0, and _λ_<sup>exp</sup> dis<sup>= 12</sup><sup>_._0.These val-</sup> ues yield a latent space that is both geometrically wellaligned across hands and smooth enough to support sampling and interpolation. 

## **4. Experiments** 

**Tasks & Dataset.** We design 10 diverse tasks with different skills and objects to evaluate our VLA models. For each task, we collect 50 demonstrations each task per hand via [18], with 2000 demonstrations collected in total. Task descriptions are listed below: 

- (a) Prepare Fruits (PF). Put the banana and orange on the green board for cutting. 

- (b) Stack Cans (SC). Stack the cheese can on top of the salt. 

- (c) Sort Cans (SoC). Put the tomato can and the cheese can into the container. 

- (d) Hand over Bottle (HB). Hand over the white bottle from right hand to left hand. 

- (e) Re-organize Lemons (RL). Put the yellow lemon and the green lime into the bowl. 

- (f) Pour Sauce (PS). Pour mustard sauce into the meat can. 

- (g) Re-arrange Boxes (RB). Keep the table organized by 

13500 


Figure 4. **Zero-shot Unseen Tasks Generalization** . For each hand, we randomly select some tasks as unseen tasks, whose data are held out from the training dataset. Then we test the unseen tasks with model trained on other data. Results show that by training with an aligned latent action space, XL-VLA gets the ability to generalize to novel hand-task combination in a zero-shot manner. PSR stands for “Partial Success Rate”, where policy is rewarded with half success if only one arm finishes its task. 

re-arranging the two boxes. 

- (h) Push Sugar (PuS). Push the sugar boxes together. 

- (i) Pour Sugar (PoS). Add sugar to the starfruit. 

- (j) Push Cans (PC). Push the two tomato cans together. 

**Hardware.** To evaluate our method, we conduct comprehensive experiments on our real-world robot platform. We use a bimanual 7-DoF xArm and a Unitree G1 humanoid with various robot hands, shown in table 3. 

||Ability|Inspire|X-Hand1|Paxini DexH13|
|---|---|---|---|---|
|#Fingers|5|5|5|4|
|#DoF(mimic)|12(6)|12(6)|12|16(3)|


Table 3. **Dexterous Hand Comparison.** 

**Experiment Settings.** We initialize the XL-VLA with weights from [6], then train the model on our collected multi-embodiment dataset. We use 8 NVIDIA H100 GPUs to train XL-VLA, each having 80GB memory. The model is trained 60K steps with a batch size of 128. Note that XL-VLA is a unified cross-embodiment multitask policy. We use language to condition the policy on multiple tasks. 

### **4.1. Main Results** 

In this section, we are trying to answer the following questions that mainly focus on _Effectiveness of VLA + Latent Integration:_ (1) Does XL-VLA outperform standard VLA models in cross-embodiment training? (2) Does XL-VLA enable zero-shot cross-embodiment skill transfer? 

**Cross-Hand Data Scaling.** Tab.2 presents the crossembodiment manipulation results for XL-VLA compared with a strong _π_ 0 baseline trained on the same multi-hand, multi-task dataset as a single shared policy across all four hands—Ability, Inspire, Paxini, and X-Hand—and ten manipulation tasks. Although _π_ 0 can nominally accommodate different embodiments by varying sequence lengths, its performance remains inconsistent and generally low due to substantial kinematic and actuation differences across hands. In contrast, XL-VLA achieves strong and consistent improvements for every hand and task, demonstrating the benefit of learning a shared latent action representation. 

Across hands, XL-VLA yields notable perembodiment gains. The Ability Hand, which features relatively simple actuation, benefits from a large boost in reliability, improving from 0.37 to 0.73 overall. The Paxini Hand achieves highest performance among all embodiments (0.78 overall) , indicating strong compatibility between its actuation structure and the learned latent mapping. XHand , which is the most mechanically distinct from the rest, also improves significantly from 0.29 to 0.70, showing that XL-VLA can bridge large embodiment gaps. Averaged over all tasks and hands, XL-VLA increases the mean success rate from 0.55 to 0.90 (+0.35). Particularly large improvements are observed for dexterity-heavy tasks such as Sort Cans, Hand over Bottle, and Re-arrange Boxes, underscoring the effectiveness of our embodiment-invariant latent space in capturing fine-grained manipulation behavior. Overall, these results demonstrate that XL-VLA enables robust cross-embodiment action prediction and consistently surpasses VLA models that lack a unified action representation. 

**Cross-Robot Data Scaling.** To show the unified latent space benefit even for different robot systems, we test four manipulation tasks with data from the tabletop xArm and humanoid G1. We co-train the data from all embodiments on the four tasks with the same training parameters and show the G1 success rates in figure 5. We can see that simply using aligned latent action space boost the performance of training on the raw action space, which has varied state/action lengths. 

**Zero-Shot Task Generalization.** A key advantage of using an embodiment-invariant latent action space is its ability to support seamless _zero-shot generalization_ to unseen tasks. Because all dexterous hands share the same latent representation, a policy trained on a subset of tasks with one embodiment can transfer to a different task–hand combination without requiring additional training or retargeting. 

To evaluate this capability, we hold out several manipulation tasks as _unseen tasks_ for each hand and train XL-VLA on the remaining tasks. At test time, 

13501 

|**Model**|**Combination**|**PF**|**SC**|**SoC**|**HB**|**RL**|**PS**|**RB**|**PuS**|**PoS**|**PC**|**Mean**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**LAD [3]**|Ability+Inspire|0.8|0.4|0.5|0.4|0.6|0.6|0.6|0.5|0.7|0.9|0.60|
||Paxini+XHand|0.7|0.5|0.6|0.7|0.5|0.8|0.7|0.4|0.6|0.6|0.61|
|**XLVLA**|Ability+Inspire|**0.9**|**0.7**|0.8|0.7|**0.8**|0.7|0.8|**0.8**|**1.0**|**1.0**|**0.82**|
|**-**|Paxini+XHand|0.8|**0.7**|**0.9**|**0.8**|0.6|**0.9**|**0.9**|0.6|**1.0**|0.9|0.81|


Table 4. **Latent replay comparison** . We compare our latent space with Latent Action Diffusion (LAD) [3]. For each hand combination, teleoperated trajectories collected on one source hand are encoded into the latent space, decoded onto the target hand, and replayed on real hardware. A replay is counted as successful if the encoded–decoded sequence can be executed without breaking contact or causing self-collisions. Higher replay success indicates better cross-embodiment consistency of the latent representation. 


Figure 5. **G1 Cross-Robot Performance.** Co-training with latent xArm and humanoid data outperforms using raw actions. 

the trained policy is applied directly to the unseen task through the corresponding embodiment-specific decoder. As shown in Fig. 4, we report both _absolute success rate_ (SR) and _partial success rate_ (PSR), where PSR accounts for intermediate progress (0.25, 0.5, 0.75, 1.0) to provide a more fine-grained measure of policy performance. 

For comparison, we construct a _π_ 0+RT baseline in which a policy is trained on all tasks using only the XHand embodiment. During evaluation, we apply a standard _kinematic retargeting_ algorithm to map the predicted XHand joint trajectories to the other embodiments (Inspire, Ability, Paxini) by aligning fingertip positions. This baseline reflects common practice in cross-embodiment manipulation and allows us to assess whether our latent action representation provides genuine zero-shot benefits over retargeting-based transfer. 

Across all embodiments and tasks, XL-VLA consistently outperforms the retargeting VLA baseline, often by a substantial margin. Notably, XL-VLA _never_ underperforms the baseline on any hand or task, highlighting the robustness of the latent action representation. The gains are especially pronounced on fine-grained dexterous tasks (e.g., HB, RB), where geometric retargeting struggles to maintain coordinated finger motion. 

### **4.2. Ablation Results** 

In this section, we are trying to answer the question about _Effectiveness of the Latent Action Space:_ (1) How well does the learned latent space function as a retar- 

geting mechanism on its own? (2) What is the impact of different design choices within the latent space, as shown through ablation studies? 

**Latent Replay Comparison.** We further compare our latent action space against LAD [2], a supervised latentspace retargeting method. To ensure a fair and challenging evaluation, we perform _latent replay_ by taking demonstrations from two embodiments and replaying them on the other two embodiments using each method’s latent mapping. As shown in Table 4, our approach achieves a mean success rate of **0.82** and **0.81** on the two hand pairs (Ability+Inspire and Paxini+XHand), substantially outperforming LAD, which attains only **0.60** and **0.61** . This improvement is consistent across all tasks, with gains particularly pronounced on finegrained manipulation tasks such as _SC_ , _SoC_ , and _HB_ , where LAD exhibits noticeable degradation. Notably, our method achieves these results without any supervision data or paired labels, relying solely on unsupervised latent alignment. These findings highlight that our latent space captures embodiment-invariant structure more effectively than supervised alternatives, enabling significantly more reliable cross-hand trajectory replay. 

**Visual Result.** Figure 6 shows latent decoding across different dexterous hands. We visualize one hand at full opacity and others with partial transparency, with the target grasp point marked in blue. Despite differing kinematics, all hands produce consistent poses from the same latent code, indicating that the learned latent space captures embodiment-invariant control. (a) X-Hand (b) Inspire Hand 

Figure 6. **Latent Visualizations.** Latent decoding results cross embodiment. 

**Design Choice Comparison.** We conduct a compre- 

13502 

||**Reconstr**|**uction**_↓_|**Cr**|**oss Emb**|**odiment**_↓_||**Latent Co**|**ntinuity**_↓_|**Interpol**|**ation**_↓_|
|---|---|---|---|---|---|---|---|---|---|---|
|**Exp**|**Joint**|**Tip**|**PT**<sup>**dir**</sup>|**PT**<sup>**dist**</sup>|**RT**<sup>**dir**</sup>|**RT**<sup>**dist**</sup>|**Joint**|**Tip**|**Accel.**|**Jerk**|
|Ours|5_._476|3_._703|11_._857|1_._872|10_._492|6_._295|4_._492|8_._534|8_._683|9_._659|
|_−L_1|61.672|39_._400|11_._741|1_._857|10_._398|6_._375|24_._784|58_._858|12_._028|16_._852|
|_−L_<sup>dist</sup><br>2|5_._195|3_._580|3_._972|4_._413|6_._788|24.488|4_._073|8_._168|8_._525|9_._240|
|_−L_<sup>dir</sup><br>2|4_._966|3_._378|46_._217|2_._251|53.546|5_._518|4_._451|9_._217|8_._742|9_._551|
|_−L_2(both)|3_._781|2_._602|62_._733|8_._080|71.765|62_._809|2_._823|6_._757|8_._602|9_._426|
|_H_<sup>128</sup><br>256|5_._897|3_._908|9_._073|1_._613|10_._432|6_._277|3_._104|6_._410|9_._213|10.406|
|_H_<sup>64</sup><br>128 <sup>_×_ 2</sup>|8.216|4_._280|9_._027|1_._513|10_._572|6_._713|5_._004|8_._832|8_._559|9_._479|
|_H_<sup>64</sup><br>64|4_._979|3_._411|9_._010|1_._655|10_._702|6.985|2_._922|6_._298|8_._618|9_._296|
|_H_<sup>64</sup>|5_._021|3_._445|9_._010|1_._518|10_._213|6.435|4_._174|8_._132|8_._246|8_._740|
|**L**8|20.913|6_._499|9_._217|1_._557|10_._960|6_._805|8_._164|11_._720|8_._758|9_._778|
|**L**16|8.416|4_._159|13_._624|1_._989|11_._084|6_._558|5_._445|9_._192|8_._436|8_._996|
|**L**64|5_._542|3_._583|8_._314|1_._549|10_._995|6.955|4_._140|8_._174|8_._299|8_._944|
|**L**96|5_._239|3_._422|9_._332|1_._562|10_._516|6.554|3_._498|7_._072|8_._700|9_._703|
|**L**128|5_._324|3_._543|8_._736|1_._529|10_._286|6_._215|3_._282|6_._882|8_._607|9_._294|


Table 5. **Ablations.** Ablation results comparing reconstruction accuracy, cross-embodiment retargeting, latent-space continuity, and interpolation smoothness. **Exp** denotes model variants: removing losses ( _−L_ 2, _−L_ 2<sup>_dist_</sup> , _−L_<sup>_dir_</sup> 2<sup>,orboth),changinghidden</sup> sizes ( _Ha_<sup>_b_), or changing latent dimension (</sup><sup>_L_</sup> _d_<sup>).Metrics include joint and tip RMSE for reconstruction; pinch- and random-motion</sup> direction/distance errors for retargeting; joint/tip latent continuity; and mean acceleration/jerk for interpolation. 

hensive ablation study to evaluate architectural and lossdesign choices for the latent action space, summarized in Tab. 5. Our final configuration uses the _H_ 64<sup>128</sup><sup>_→_64</sup> architecture with a latent dimension of 32. All metrics follow a “lower is better” convention, and the worst result compared with our method within each row are highlighted in green. Across reconstruction, cross-embodiment retargeting, latent continuity, and interpolation smoothness, our design choice achieves relatively stronger performance. Notably, performance remains stable across a wide range of architectures and latent dimensions, with degradation only occurring when the latent size is significantly increased (e.g., _L_ 128), suggesting that excessively large latent spaces hinder embodiment-invariant structure. These results indicate that our chosen configuration offers an effective balance between model capacity and latent compactness. 

Evaluation metrics we designed: 

_Recon Joint/Tip RMSE._ Measures single-hand reconstruction accuracy. Random joint configurations are encoded and decoded; we compute RMSE of joint angles (radians) and fingertip positions (meters) via forward kinematics. Lower values indicate better fidelity. 

_Pinch & Random Tip Dir./Dist. Error._ Evaluates crosshand transfer. Pinch and random poses are encoded on a source hand and decoded on target hands. We compute directional error (angle) and distance error (thumb– finger distance). Lower values indicate more accurate transfer and stable pinch geometry. 

_Latent Continuity (Joint/Tip)._ Measures local smoothness of the latent space. Gaussian noise ( _ϵ_ = 0 _._ 05) is added to latents before decoding; we compute joint deviation (radians) and fingertip displacement (meters). Smaller values indicate smoother latent variations. _Interp. Accel./Jerk Mean._ Measures interpolation smoothness. Latent codes are linearly interpolated and decoded to fingertip trajectories. We compute mean acceleration and jerk. Lower values indicate smoother interpolation paths. 

## **5. Conclusion.** 

In this work, we introduced XL-VLA, a vision–language–action framework equipped with a unified latent action space for scalable crossembodiment dexterous manipulation. By learning an embodiment-invariant latent representation, our approach enables seamless training across diverse robotic hands and supports zero-shot generalization to new hand–task combinations. Extensive real-world experiments demonstrate that XL-VLA consistently outperforms standard VLA models and retargeting-based baselines, while offering a flexible and plug-and-play interface for newly introduced hands. Overall, our results highlight latent action spaces as a powerful foundation for building generalizable, data-efficient dexterous manipulation systems. We believe this work takes a step toward more unified and adaptable robotic manipulation frameworks capable of keeping pace with rapid hardware innovation. 

13503 

## **6. Acknowledgment** 

This project was supported, in part, by gifts from Amazon, Meta, and Qualcomm, and the Technology Innovation Program (20018112, Development of autonomous manipulation and gripping technology using imitation learning based on visual and tactile sensing) funded by the Ministry of Trade, Industry & Energy (MOTIE), Korea. 

## **References** 

- [1] Yang Bai, Liudi Yang, George Eskandar, Fengyi Shen, Dong Chen, Mohammad Altillawi, Ziyuan Liu, and Gitta Kutyniok. Roboswap: A gan-driven video diffusion framework for unsupervised robot arm swapping. _arXiv preprint arXiv:2506.08632_ , 2025. 2 

- [2] Erik Bauer, Elvis Nava, and Robert K. Katzschmann. Latent action diffusion for cross-embodiment manipulation. _arXiv preprint arXiv:2506.14608_ , 2025. 7 

- [3] Erik Bauer, Elvis Nava, and Robert K. Katzschmann. Latent action diffusion for cross-embodiment manipulation. _arXiv preprint arXiv:2506.14608_ , 2025. 2, 3, 7 

- [4] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 14, 15 

- [5] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 3 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 3, 4, 5, 6, 15 

- [7] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 3 

- [8] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Learning to Act Anywhere with Task-centric Latent Actions. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, 2025. 2, 3 

- [9] Qingwen Bu, Yanting Yang, Jisong Yang, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 2 

- [10] Berk Calli, Arjun Singh, James Bruce, Aaron Walsman, Kurt Konolige, Siddhartha Srinivasa, Pieter Abbeel, and Aaron M Dollar. Yale-cmu-berkeley dataset for robotic manipulation research. _The International Journal of Robotics Research_ , 36(3):261–268, 2017. 14 

- [11] Zhefeng Cao, Ben Liu, Sen Li, Wei Zhang, and Hua Chen. G-dream: Graph-conditioned diffusion retargeting across multiple embodiments. _arXiv preprint arXiv:2505.20857_ , 2025. 2 

- [12] Annie S Chen, Philemon Brakel, Antonia Bronars, Annie Xie, Sandy Huang, Oliver Groth, Maria Bauza, Markus Wulfmeier, Nicolas Heess, and Dushyant Rao. Exploiting policy idling for dexterous manipulation. In _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. 2 

- [13] Xu Chi, Chao Zhang, Yang Su, Lingfeng Dou, Fujia Yang, Jiakuo Zhao, Haoyu Zhou, Xiaoyou Jia, Yong Zhou, and Shan An. Open teledex: A hardware-agnostic teleoperation system for imitation learning based dexterous manipulation. _arXiv preprint arXiv:2510.14771_ , 2025. 2 

- [14] Xu Chi, Chao Zhang, Yang Su, Lingfeng Dou, Fujia Yang, Jiakuo Zhao, Haoyu Zhou, Xiaoyou Jia, Yong Zhou, and Shan An. Open teledex: A hardware-agnostic teleoperation system for imitation learning based dexterous manipulation. _arXiv preprint arXiv:2510.14771_ , 2025. 3 

- [15] Prithwish Dan, Kushal Kedia, Angela Chao, Edward Weiyi Duan, Maximus Adrian Pace, Wei-Chiu Ma, and Sanjiban Choudhury. X-sim: Cross-embodiment learning via real-to-sim-to-real. In _Proceedings of the 9th Conference on Robot Learning (CoRL 2025)_ , pages 816–833. PMLR, 2025. 2 

- [16] Apan Dastider, Hao Fang, and Mingjie Lin. Crossembodiment robotic manipulation synthesis via guided demonstrations through cyclevae and human behavior transformer. _arXiv preprint arXiv:2503.08622_ , 2025. 2, 3 

- [17] Travis Davies, Yiqi Huang, Yunxin Liu, Xiang Chen, Huxian Liu, and Luhui Hu. Tenma: Robust crossembodiment robot manipulation with diffusion transformer. _arXiv preprint arXiv:2509.11865_ , 2025. 2, 3 

- [18] Runyu Ding, Yuzhe Qin, Jiyue Zhu, Chengzhe Jia, Shiqi Yang, Ruihan Yang, Xiaojuan Qi, and Xiaolong Wang. Bunny-visionpro: Real-time bimanual dexterous teleoperation for imitation learning. 2024. 5, 14 

- [19] Yunlong Dong, Xing Liu, Jun Wan, and Zelin Deng. Gex: Democratizing dexterity with fully-actuated dexterous hand and exoskeleton glove. _arXiv preprint arXiv:2506.04982_ , 2025. 3 

- [20] Zhao Dong, Ka Chen, Zhaoyang Lv, Hong-Xing Yu, Yunzhi Zhang, Cheng Zhang, Yufeng Zhu, Stephen Tian, Zhengqin Li, Geordie Moffatt, et al. Digital twin catalog: A large-scale photorealistic 3d object digital twin dataset. _arXiv preprint arXiv:2504.08541_ , 2025. 14 

- [21] Ria Doshi, Homer Walke, Oier Mees, Sudeep Dasari, and Sergey Levine. Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and avi- 

13504 

   - ation. In _Proceedings of the 8th Conference on Robot Learning (CoRL 2024)_ , pages 496–512. PMLR, 2025. 2 

- [22] Ainaz Eftekhar, Rose Hendrix, Luca Weihs, Jiafei Duan, Ege Caglar, Jordi Salvador, Alvaro Herrasti, Winson Han, Eli VanderBil, Aniruddha Kembhavi, Kiana Ehsani, Kuo-Hao Zeng, and Ranjay Krishna. The one ring: a robotic indoor navigation generalist. _arXiv preprint arXiv:2412.14401_ , 2024. 2 

- [23] Hao-Shu Fang, Branden Romero, Yichen Xie, Arthur Hu, Bo-Ruei Huang, Juan Alvarez, Matthew Kim, Gabriel Margolis, Kavya Anbarasu, Masayoshi Tomizuka, et al. Dexop: A device for robotic transfer of dexterous human manipulation. In _Workshop on Dexterous Manipulation at Robotics: Science and Systems (RSS)_ , 2025. Workshop paper. 2 

- [24] Xin Fei, Zhixuan Xu, Huaicong Fang, Tianrui Zhang, and Lin Shao. T(r,o) grasp: Efficient graph diffusion of robot-object spatial transformation for crossembodiment dexterous grasping. _arXiv preprint arXiv:2510.12724_ , 2025. 2 

- [25] Mateo Guaman Castro, Sidharth Rajagopal, Daniel Gorbatov, Matt Schmittle, Rohan Baijal, Octi Zhang, Rosario Scalise, Sidharth Talia, Emma Romig, Celso de Melo, Byron Boots, and Abhishek Gupta. Vamos: A hierarchical vision-language-action model for capabilitymodulated and steerable navigation. _arXiv preprint arXiv:2510.20818_ , 2025. 2 

- [26] Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, and Yuntao Chen. Dita: Scaling diffusion transformer for generalist vision-languageaction policy. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 2 

- [27] Tao Huang, Guangqi Jiang, Yanjie Ze, and Huazhe Xu. Diffusion reward: Learning rewards via conditional video diffusion. In _European Conference on Computer Vision_ , pages 478–495. Springer, 2024. 2 

- [28] Adam Hung, Fan Yang, Abhinav Kumar, Sergio Aguilera Marinovic, Soshi Iba, Rana Soltani Zarrin, and Dmitry Berenson. Avo: Amortized value optimization for contact mode switching in multi-finger manipulation. _arXiv preprint arXiv:2510.07548_ , 2025. 2 

- [29] Guangqi Jiang, Yifei Sun, Tao Huang, Huanyu Li, Yongyuan Liang, and Huazhe Xu. Robots pretrain robots: Manipulation-centric robotic representation from large-scale robot datasets. _arXiv preprint arXiv:2410.22325_ , 2024. 3 

- [30] Guangqi Jiang, Haoran Chang, Ri-Zhao Qiu, Yutong Liang, Mazeyu Ji, Jiyue Zhu, Zhao Dong, Xueyan Zou, and Xiaolong Wang. Gsworld: Closed-loop photorealistic simulation suite for robotic manipulation. _arXiv preprint arXiv:2510.20813_ , 2025. 2 

- [31] Changwei Jing, Jai Krishna Bandi, Jianglong Ye, Yan Duan, Pieter Abbeel, Xiaolong Wang, and Sha Yi. Contact-aware neural dynamics. _arXiv preprint arXiv:2601.12796_ , 2026. 2 

- [32] Hanjung Kim, Jaehyun Kang, Hyolim Kang, Meedeum Cho, Seon Joo Kim, and Youngwoon Lee. Uniskill: 

   - Imitating human videos via cross-embodiment skill representations. In _Proceedings of the 9th Conference on Robot Learning (CoRL 2025)_ . PMLR, 2025. 2 

- [33] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 3 

- [34] Yuki Kuroda, Tomoya Takahashi, Cristian C BeltranHernandez, Masashi Hamaya, and Kazutoshi Tanaka. Plexus hand: Lightweight four-motor prosthetic hand enabling precision-lateral dexterous manipulation. In _Proceedings of the IEEE International Conference on Rehabilitation Robotics (ICORR)_ , 2025. 2 

- [35] Arjun S. Lakshmipathy, Jessica K. Hodgins, and Nancy S. Pollard. Kinematic motion retargeting for contact-rich anthropomorphic manipulations. _arXiv preprint arXiv:2402.04820_ , 2024. 3 

- [36] Qixiu Li, Yu Deng, Yaobo Liang, Lin Luo, Lei Zhou, Chengtang Yao, Lingqi Zeng, Zhiyuan Feng, Huizhi Liang, Sicheng Xu, et al. Scalable visionlanguage-action model pretraining for robotic manipulation with real-life human activity videos. _arXiv preprint arXiv:2510.21571_ , 2025. 2 

- [37] Xiaoyi Lin, Kunpeng Yao, Lixin Xu, Xueqiang Wang, Xuetao Li, Yuchen Wang, and Miao Li. Dexflow: A unified approach for dexterous hand pose retargeting and interaction. _arXiv preprint arXiv:2505.01083_ , 2025. 3 

- [38] Yuhao Lin, Yi-Lin Wei, Haoran Liao, Mu Lin, Chengyi Xing, Hao Li, Dandan Zhang, Mark Cutkosky, and WeiShi Zheng. Typetele: Releasing dexterity in teleoperation by dexterous manipulation types. _arXiv preprint arXiv:2507.01857_ , 2025. 3 

- [39] Jiacheng Liu, Pengxiang Ding, Qihang Zhou, Yuxuan Wu, Da Huang, Zimian Peng, Wei Xiao, Weinan Zhang, Lixin Yang, Cewu Lu, and Donglin Wang. Trajbooster: Boosting humanoid whole-body manipulation via trajectory-centric learning. _arXiv preprint arXiv:2509.11839_ , 2025. 2 

- [40] Xueyi Liu, He Wang, and Li Yi. Dexndm: Closing the reality gap for dexterous in-hand rotation via joint-wise neural dynamics model. _arXiv preprint arXiv:2510.08556_ , 2025. 2 

- [41] Zhao Mandi, Yifan Hou, Dieter Fox, Yashraj Narang, Ajay Mandlekar, and Shuran Song. Dexmachina: Functional retargeting for bimanual dexterous manipulation. _arXiv preprint arXiv:2505.24853_ , 2025. 3 

- [42] Yaru Niu, Yunzhe Zhang, Mingyang Yu, Changyi Lin, Chenhao Li, Yikai Wang, Yuxiang Yang, Wenhao Yu, Tingnan Zhang, Zhenzhen Li, Jonathan Francis, Bingqing Chen, Jie Tan, and Ding Zhao. Human2locoman: Learning versatile quadrupedal manipulation with human pretraining. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 2 

- [43] Guoping Pan, Qingwei Ben, Zhecheng Yuan, Guangqi Jiang, Yandong Ji, Jiangmiao Pang, Houde Liu, and Huazhe Xu. Roboduet: A framework affording mobilemanipulation and cross-embodiment. _arXiv preprint arXiv:2403.17367_ , 6, 2024. 2 

13505 

- [44] En Yen Puang, Federico Ceola, Giulia Pasquale, and Lorenzo Natale. Pchands: Pca-based hand pose synergy representation on manipulators with n-dof. In _Proceedings of the IEEE-RAS International Conference on Humanoid Robots (Humanoids)_ , 2025. 2 

- [45] Ryan Punamiya, Dhruv Patel, Patcharapong Aphiwetsa, Pranav Kuppili, Lawrence Y. Zhu, Simar Kareer, Judy Hoffman, and Danfei Xu. Egobridge: Domain adaptation for generalizable imitation from egocentric human data. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. Poster. 2, 3 

- [46] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, et al. Eo-1: Interleaved visiontext-action pretraining for general robot control. _arXiv preprint arXiv:2508.21112_ , 2025. 2 

- [47] Juntao Ren, Priya Sundaresan, Dorsa Sadigh, Sanjiban Choudhury, and Jeannette Bohg. Motion tracks: A unified representation for human-robot transfer in few-shot imitation learning. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 2 

- [48] Benjamin A Richardson, Felix Gr¨uninger, Lukas Mack, Joerg Stueckler, and Katherine J Kuchenbecker. Isyhand: A dexterous multi-finger robot hand with an articulated palm. In _Proceedings of the IEEE-RAS International Conference on Humanoid Robots (Humanoids)_ , Seoul, Korea, 2025. 2 

- [49] Mingyo Seo, H. Andy Park, Shenli Yuan, Yuke Zhu, and Luis Sentis. Legato: Cross-embodiment imitation using a grasping tool. _arXiv preprint arXiv:2411.03682_ , 2024. 2 

- [50] Wenxuan Song, Jiayi Chen, Pengxiang Ding, Yuxin Huang, Han Zhao, Donglin Wang, and Haoang Li. Ceedvla: Consistency vision-language-action model with early-exit decoding. _arXiv preprint arXiv:2506.13725_ , 2025. 2 

- [51] Kit-Wa Sou, Junhao Gong, Shoujie Li, Chuqiao Lyu, Ziwu Song, Shilong Mu, and Wenbo Ding. Moir´etac: A dual-mode visuotactile sensor for multidimensional perception using moir´e pattern amplification. _arXiv preprint arXiv:2509.12714_ , 2025. 2 

- [52] Wentao Tan, Bowen Wang, Heng Zhi, Chenyu Liu, Zhe Li, Jian Liu, Zengrong Lin, Yukun Dai, Yipeng Chen, Wenjie Yang, Enci Xie, Hao Xue, Baixu Ji, Chen Xu, Zhibin Wang, Tianshi Wang, Lei Zhu, and Heng Tao Shen. Blm1: A boundless large model for crossspace, cross-task, and cross-embodiment learning. _arXiv preprint arXiv:2510.24161_ , 2025. 2 

- [53] Tianyu Wang, Dwait Bhatt, Xiaolong Wang, and Nikolay Atanasov. Cross-embodiment robot manipulation skill transfer using latent space alignment. _arXiv preprint arXiv:2406.01968_ , 2024. 2, 3 

- [54] Tianyu Wang, Dwait Bhatt, Xiaolong Wang, and Nikolay Atanasov. Cross-embodiment robot manipulation skill transfer using latent space alignment. _arXiv preprint arXiv:2406.01968_ , 2024. 2 

- [55] Yi-Lin Wei, Zhexi Luo, Yuhao Lin, Mu Lin, Zhizhao Liang, Shuoyu Chen, and Wei-Shi Zheng. Om- 

nidexgrasp: Generalizable dexterous grasping via foundation model and force feedback. _arXiv preprint arXiv:2510.23119_ , 2025. 2 

- [56] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 3 

- [57] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control. In _Proceedings of the 9th Conference on Robot Learning (CoRL 2025)_ . PMLR, 2025. 2 

- [58] Ruoshi Wen, Jiajun Zhang, Guangzeng Chen, Zhongren Cui, Min Du, Yang Gou, Zhigang Han, Junkai Hu, Liqun Huang, Hao Niu, Wei Xu, Haoxiang Zhang, Zhengming Zhu, Hang Li, and Zeyu Ren. Dexterous teleoperation of 20-dof bytedexter hand via human motion retargeting. _arXiv preprint arXiv:2507.03227_ , 2025. 3 

- [59] Zhiyuan Wu, Rolandos Alexandros Potamias, Xuyang Zhang, Zhongqun Zhang, Jiankang Deng, and Shan Luo. Cedex: Cross-embodiment dexterous grasp generation at scale from human-like contact representations. _arXiv preprint arXiv:2509.24661_ , 2025. 2 

- [60] Chendong Xin, Mingrui Yu, Yongpeng Jiang, Zhefeng Zhang, and Xiang Li. Analyzing key objectives in human-to-robot retargeting for dexterous manipulation. _arXiv preprint arXiv:2506.09384_ , 2025. 3 

- [61] Mengda Xu, Han Zhang, Yifan Hou, Zhenjia Xu, Linxi Fan, Manuela Veloso, and Shuran Song. Dexumi: Using human hand as the universal manipulation interface for dexterous manipulation. In _Proceedings of the 9th Conference on Robot Learning (CoRL)_ , pages 437–459, 2025. 2 

- [62] Sirui Xu, Yu-Wei Chao, Liuyu Bian, Arsalan Mousavian, Yu-Xiong Wang, Liang-Yan Gui, and Wei Yang. Dexplore: Scalable neural control for dexterous manipulation from reference-scoped exploration. _arXiv preprint arXiv:2509.09671_ , 2025. 3 

- [63] Zhuowei Xu, Zilin Si, Kevin Zhang, Oliver Kroemer, and Zeynep Temel. A multi-modal tactile fingertip design for robotic hands to enhance dexterous manipulation. _arXiv preprint arXiv:2510.05382_ , 2025. 2 

- [64] Rui Yan, Jiajian Fu, Shiqi Yang, Lars Paulsen, Xuxin Cheng, and Xiaolong Wang. Ace-f: A cross embodiment foldable system with force feedback for dexterous teleoperation, 2025. 14 

- [65] Jiange Yang, Yansong Shi, Haoyi Zhu, Mingyu Liu, Kaijing Ma, Yating Wang, Gangshan Wu, Tong He, and Limin Wang. Como: Learning continuous latent motion from internet videos for scalable robot learning. _arXiv preprint arXiv:2505.17006_ , 2025. 2, 3 

- [66] Shunpeng Yang, Zhen Fu, Zhefeng Cao, Guo Junde, Patrick Wensing, Wei Zhang, and Hua Chen. Multi-loco: Unifying multi-embodiment legged locomotion via reinforcement learning augmented diffusion. In _Proceedings of the 9th Conference on Robot Learning (CoRL 2025)_ , pages 1030–1048. PMLR, 2025. 2 

13506 

- [67] Jianglong Ye, Lai Wei, Guangqi Jiang, Changwei Jing, Xueyan Zou, and Xiaolong Wang. From power to precision: Learning fine-grained dexterity for multi-fingered robotic hands. _arXiv preprint arXiv:2511.13710_ , 2025. 

   - 2 

- [68] Zhao-Heng Yin, Changhao Wang, Luis Pineda, Krishna Bodduluri, Tingfan Wu, Pieter Abbeel, and Mustafa Mukadam. Geometric retargeting: A principled, ultrafast neural hand retargeting algorithm. _arXiv preprint arXiv:2503.07541_ , 2025. 3 

- [69] Jiawen Yu, Hairuo Liu, Qiaojun Yu, Jieji Ren, Ce Hao, Haitong Ding, Guangyu Huang, Guofan Huang, Yan Song, Panpan Cai, et al. Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. Poster. 2 

- [70] Kevin Zakka, Andy Zeng, Pete Florence, Jonathan Tompson, Jeannette Bohg, and Debidatta Dwibedi. Xirl: Cross-embodiment inverse reinforcement learning. In _Proceedings of the 5th Conference on Robot Learning (CoRL 2021)_ , pages 537–546. PMLR, 2021. 2 

- [71] Yang Zhang, Chenwei Wang, Ouyang Lu, Yuan Zhao, Yunfei Ge, Zhenglong Sun, Xiu Li, Chi Zhang, Chenjia Bai, and Xuelong Li. Align-then-steer: Adapting the vision-language action models through unified latent guidance. _arXiv preprint arXiv:2509.02055_ , 2025. 2, 3 

- [72] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 3 

- [73] Jinliang Zheng, Jianxiong Li, Dongxiu Liu, Yinan Zheng, Zhihao Wang, Zhonghong Ou, Yu Liu, Jingjing Liu, Ya-Qin Zhang, and Xianyuan Zhan. Universal actions for enhanced embodied foundation models. _arXiv preprint arXiv:2501.10105_ , 2025. 2 

- [74] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, Ya-Qin Zhang, Jiangmiao Pang, Jingjing Liu, Tai Wang, and Xianyuan Zhan. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 2 

- [75] Hongyan Zhi, Peihao Chen, Siyuan Zhou, Yubo Dong, Quanxi Wu, Lei Han, and Mingkui Tan. 3dflowaction: Learning cross-embodiment manipulation from 3d flow world model. _arXiv preprint arXiv:2506.06199_ , 2025. 2 

13507 

