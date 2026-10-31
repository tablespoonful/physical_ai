---
title: "Factored Latent Action World Models"
date: "2026-02-18"
authors: "Zizhao Wang; Chang Shi; Jiaheng Hu; Kevin Rohling; Roberto Martín-Martín; Amy Zhang"
url: https://arxiv.org/abs/2602.16229
pdf: https://arxiv.org/pdf/2602.16229
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.16229)** / [論文ページ](https://arxiv.org/abs/2602.16229)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Factored Latent Action World Models** 

**Zizhao Wang**<sup>* 1</sup> **Chang Shi**<sup>* 1</sup> **Jiaheng Hu**<sup>1</sup> **Kevin Rohling**<sup>1</sup> **Roberto Mart´ın-Mart´ın**<sup>1</sup> **Amy Zhang**<sup>1</sup> **Peter Stone**<sup>1 2</sup> 

# **Abstract** 

Learning latent actions from action-free video has emerged as a powerful paradigm for scaling up controllable world model learning. Latent actions provide a natural interface for users to iteratively generate and manipulate videos. However, most existing approaches rely on monolithic inverse and forward dynamics models that learn a single latent action to control the entire scene, and therefore struggle in complex environments where multiple entities act simultaneously. This paper introduces Factored Latent Action Model (FLAM), a factored dynamics framework that decomposes the scene into independent factors, each inferring its own latent action and predicting its own nextstep factor value. This factorized structure enables more accurate modeling of complex multi-entity dynamics and improves video generation quality in action-free video settings compared to monolithic models. Based on experiments on both simulation and real-world multi-entity datasets, we find that FLAM outperforms prior work in prediction accuracy and representation quality, and facilitates downstream policy learning, demonstrating the benefits of factorized latent action models. 

# **1. Introduction** 

Recent advances in Latent Action Models (LAM) (Schmidt & Jiang, 2023; Bruce et al., 2024) have unlocked the possibilities of learning world models from action-free videos that are abundant on the web. Specifically, these approaches use an inverse dynamics model to encode environmental changes into a _single_ latent action. The latent action is then used to train a forward dynamics model, allowing controllable predictions of future frames from in-the-wild videos. 

However, in-the-wild videos often contain complex scenes 

*Equal contribution 1University of Texas at Austin 2Sony AI. Correspondence to: Zizhao Wang _<_ zizhao.wang@utexas.edu _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

where many entities may be taking actions simultaneously: for instance, a robot video may include independent arm movements and shifting camera perspectives; while a soccer game involves several players, the ball, and even background audience motion, each of which acts independently. Compressing all these motions into a _single_ latent action is challenging, since the complexity of the underlying action space grows exponentially with the number of movable entities (Fig. 1). Consequently, existing methods struggle with latent action learning in such settings, which severely limits their applicability to diverse scenarios. 

This paper introduces the Factored Latent Action Model (FLAM), where the latent state is decomposed into a set of factors, each independently predicting its latent action and its next-step value via shared factored inverse and forward dynamics models. Compared to prior work that must capture all joint action combinations within a single latent action space, FLAM assumes a shared latent action space across factors and thereby reduces the learning problem to modeling each entity’s action patterns within this common space. Additionally, regarding forward dynamics, unlike most prior LAM approaches that use a monolithic scene representation entangling all entities, FLAM factorizes the scene into compositional entities with a shared forward dynamics model, inherently supporting permutation invariance and enabling stronger generalization. With next frame prediction as the training objective, FLAM learns factorized state and action representations from action-free video data, leading to more accurate modeling of complex, multi-entity dynamics and improved prediction quality compared to previous work. 

Based on experiments on both simulated and real-world multi-entity datasets, including autonomous driving videos, we find that FLAM outperforms prior state-of-the-art methods in both prediction quality and factor-entity correspondence. Moreover, the inferred latent actions capture essential entity behaviors and enable sample-efficient policy learning. Qualitative results are available at https: //sites.google.com/view/factored-lam. 

# **2. Related Work** 

In this section, we first discuss previous works in learning world models from action-free videos. Next, we dis- 

1 

**Factored Latent Action World Models** 


_Figure 1._ In multi-entity scenarios, **(left)** such as an intersection with three road users: **(middle)** a vanilla latent action model encodes the scene change with a _single_ latent action of dimension _d_ , which makes learning challenging as this latent action space needs to model all _|A|_<sup>_K_</sup> joint action combinations. **(right)** In contrast, FLAM decomposes the state into _K_ factors, each with its own latent action of dimension _Kd_<sup>.Additionally, we assume all latent actions share the same space (i.e., with the same prior / codebook), which reduces the</sup> learning problem to modeling the _|A|_ actions per factor rather than their _|A|_<sup>_K_</sup> joint combinations. 

cuss prior works in factorized decision making and objectcentric representations, whose strength and weakness inspire FLAM. 

**Dynamics Modeling without Action Labels** . Given the abundant source of videos and the scarcity of action labels, several methods have been developed to learn from pure observations. ILPO (Edwards et al., 2019) learns a latent policy with forward dynamics model only, and later maps the latent policy output to real action through an action remapping network. LAPO (Schmidt & Jiang, 2023) and Genie (Bruce et al., 2024) jointly learn an inverse dynamics model jointly with a forward dynamics model. Nikulin et al. (2025) then introduce a small portion of ground-truth actions as dynamics modeling supervision. Ye et al. (2024) expand learning from observation from vision only to vision and language modalities. Past work (Zhang et al., 2022; Ye et al., 2022; Baker et al., 2022; Ye et al., 2024) has proven the value of dynamics modeling without action labels in applications such as learning to drive, play games, and manipulate with robot arms from videos. However, many domains include multiple entities with independent actions, and prior work falls short in modeling such complex action combinations, motivating our work to address this challenge through factorization. 

**Factorization in Decision Making** . Factorization has long been used to exploit structured state and action spaces in complex environments, often through the factored MDP formulation (Osband & Van Roy, 2014; Guestrin et al., 2003). Recent works have applied this principle to derive factored forward dynamics (Pitis et al., 2020; Wang et al., 2022), factored policies (Hu et al., 2025; 2024), and factored value functions (Sodhani et al., 2022). FLAM is motivated by the same principle that factorization simplifies complexity into manageable components. However, it applies this idea to learning world models from action-free video, where the 

underlying factorization is not given. Compared to prior work (Klepach et al., 2025; Daniel et al., 2026) that also focuses on world models from action-free video, FLAM is the first factored latent world model that does not use pretrained object-centric representation and specifically focus on multi-entity scenarios. 

**Object-Centric Representation Learning** . Object-centric learning aims to represent complex scenes by isolating individual objects from the background and from each other, leading to improved generalization and modeling capabilities. Key challenges include the need for supervision, leading to the development of many unsupervised methods. MONet (Burgess et al., 2019) and IODINE (Greff et al., 2019) achieved unsupervised multi-object segmentation through attention and iterative amortized inference. Slot Attention (Locatello et al., 2020a) uses iteratively updated slots to learn disentangled, object-based representations. Recent work has focused on improving object-centric learning fidelity in noisy real-world data (Jiang et al., 2023; Wang et al., 2025; Qi et al., 2025). In our work, we use Slot Attention (Locatello et al., 2020b) as the factorizer for the state representation and use the forward prediction task as the learning signal. In contrast to object-centric representation work that separates entities based on visual similarity, our representation separates entities based on the independence of their actions, yielding representations that are actiondriven. 

# **3. Preliminaries** 

Given a video dataset, we aim to model dynamics from observations alone, without any action labels. A Latent Action Model (LAM) learns an inverse dynamics model (IDM) to infer latent actions and a forward dynamics model (FDM) to predict the next observation. The inferred latent 

2 

**Factored Latent Action World Models** 

action captures the most essential changes during a transition that cannot be predicted from the current observation alone, and thus usually correspond to entities’ underlying actions. As a result, although they may not align exactly with real, physically meaningful actions, these latent actions can still provide useful information for downstream policy learning. 


- **Latent action model (LAM) learning** (Sec. 4.2): Using the extracted features, FLAM decomposes the scene into several independent factors, also referred to as _slots_ . For each slot, an inverse dynamics model infers a separate latent action from its current and next-frame values. Then, based on its current value and the corresponding latent action, a forward dynamics model independently predicts the next-frame value for each slot. Finally, all predicted slots are mapped back to the feature space and decoded into the next video frame. 

After FLAM learns to model the world from action-free videos, its inferred latent actions can be used for either controllable video generation or policy learning to solve downstream tasks. We refer to this utilization as the third phase, and discuss how to leverage FLAM for both settings in Sec. 4.3. 

_Figure 2._ Latent action model. 

## **4.1. Pretrained Encoder** 

As shown in Fig. 2, both the IDM and the FDM observe _ot_ , but only the IDM observes _ot_ +1. Therefore, to accurately predict _ot_ +1, the IDM must extract useful transition information through the latent action _at_ . However, without an explicit bottleneck on _at_ , the model can collapse to a trivial solution where _at_ simply copies _ot_ +1. To prevent this shortcut, prior work typically constrains the capacity of _at_ , for example by discretizing it with vector quantization into a small set of codes or by regularizing it toward a prior using a VAE-style objective (Kingma & Welling, 2013; Van Den Oord et al., 2017). 

While latent action models provide a general framework for learning controllable world models from videos alone, they typically use a single latent action to represent the change of an entire scene, which becomes restrictive when multiple entities act independently. For example, in crowded intersections where many cars and pedestrians are driven by independent actions, learning to compress all entities’ actions into one latent action can be challenging. To address this limitation, FLAM decomposes both the state representation and the latent action into independent factors, enabling efficient modeling of multi-entity dynamics, as discussed in Sec. 4. 

# **4. Factored Latent Action Model (FLAM)** 

From a high-level perspective, FLAM enables efficient latent action model learning in multi-entity scenarios by inferring a set of factorized latent actions rather than a single latent action between each pair of frames, via the two learning phases shown in Fig. 3 and Alg. 1: 

- **Encoder learning** (Sec. 4.1): FLAM pre-trains a VQVAE to extract high-level features from pixels, allowing the latent action model to learn in the feature space rather than the pixel space for the purpose of efficient learning. 

As shown in Fig. 3 (a), FLAM learns a VQ-VAE (Van Den Oord et al., 2017) to extract features from raw pixels, enabling fast LAM learning. For each frame _o ∈_ R<sup>_H×W ×_3</sup> , a CNN encoder first extracts _N_ patch-level features _z ∈_ R<sup>_N×dz_</sup> . The features are then quantized from continuous encoder outputs to the nearest entry in a discrete codebook, denoted as _zq ∈_ R<sup>_N×dz_</sup> , using finite scalar quantization FSQ (Mentzer et al., 2023), which forces features into a finite set of learned embeddings. Finally, a decoder reconstructs the frame from the quantized feature: 


The VQ-VAE is trained by minimizing the following image reconstruction loss: 


## **4.2. Factored Latent Action Model (FLAM)** 

As shown in Fig. 3 (b), our latent action model contains four key components: 1) a factorizer that decomposes the scene _z_ into a set of independent slots _s_ , 2) a shared inverse dynamics model that infers a separate latent action _a_<sup>_i_</sup> for each slot, 3) a shared forward dynamics model that, given the current slot value and latent action, predicts the nextframe value for each slot, and 4) an aggregator that maps the predicted slots back to the feature space. These four components are jointly trained to minimize the next frame prediction error. 

**Factorizer** . To decompose the scene into a set of factors with independent actions, FLAM uses slot attention (Locatello et al., 2020a). For each frame, _K_ slots _st ∈_ R<sup>_K×ds_</sup> 

3 

**Factored Latent Action World Models** 


_Figure 3._ Two training stages of FLAM. **(a)** A VQ-VAE is pretrained to extract features for latent action model learning. **(b)** FLAM infers latent actions and makes predictions for each factor independently, with all modules trained jointly to minimize the prediction error. 

are initialized from learned embeddings and then compete to bind to different regions in the frame through iterative slot attention. Meanwhile, to ensure that each slot consistently binds to the same object, we add an additional causal temporal attention layer so that each slot can refer to its values at all previous timestamps. Overall, the factorizer computes the slots as follows: 

for each slot attention iteration 


**Inverse dynamics model (IDM)** . After extracting independent slots, the IDM aims to infer a latent action _a_<sup>_i_</sup> _t_<sup>for each</sup> slot _i_ , based on all current slots _s_<sup>1:</sup> _t_<sup>_K_</sup> and its next-frame value _s_<sup>_i_</sup> _t_ +1<sup>:</sup> 


where for a variable _x_ , _x_<sup>1:</sup><sup>_K_</sup> denotes the set _{x_<sup>_i_</sup> _}_<sup>_K_</sup> _i_ =1<sup>, and</sup> we use _s_<sup>1:</sup> _t_<sup>_K_</sup> and _st_ interchangeably. We use all current slots rather than just _s_<sup>_i_</sup> _t_<sup>as inputs to account for interactions</sup> between factors, enabling more accurate latent action prediction (e.g., a person in a car moves because of the car rather than by themself). 

To implement the IDM, we adopt the spatio-temporal model introduced in Genie (Bruce et al., 2024). The spatial block applies self-attention to capture interaction information across _s_<sup>1:</sup> _t_<sup>_K_</sup> , while the temporal block applies cross-attention to compare _s_<sup>_i_</sup> _t_ +1<sup>with its current value and encode the most</sup> meaningful changes between them: 


Note that although we use only the current and next values in the temporal block, the model can be easily extended to 

condition on the full history _s_<sup>_i_</sup> 1: _t_<sup>or a fixed window</sup><sup>_s_</sup> _t_<sup>_i_</sup> _−w_ : _t_<sup>,</sup> where _w_ denotes the window length. 

Similar to prior LAM methods, we regularize the capacity of the latent action to prevent it from simply copying the next state _s_<sup>_i_</sup> _t_ +1<sup>and thereby bypassing dynamics learning.</sup> Concretely, following the variational autoencoder (VAE) framework (Kingma & Welling, 2013), we project _u_<sup>_i_</sup> _t_<sup>to a</sup> normal posterior distribution _q_ ( _a_<sup>_i_</sup> _t_<sup>) and impose a KL diver-</sup> gence regularization toward a unit normal prior _p_ ( _a_<sup>_i_</sup> _t_<sup>).The</sup> latent action is then sampled from this posterior as: 


where _µ_ and _σ_ are the projection networks that map _u_<sup>_i_</sup> _t_<sup>to the</sup> mean and standard deviation of the posterior distribution. **Forward dynamics model (FDM)** . To provide the learning signals for the IDM, the forward dynamics model takes all current slots _s_<sup>1:</sup> _t_<sup>_K_</sup> together with the latent action _a_<sup>_i_</sup> _t_<sup>and</sup> predicts the next-frame value for each slot ˆ _s_<sup>_i_</sup> _t_ +1<sup>:</sup> 


Similarly to the IDM, the same FDM is shared across all slots, and we use all current slots instead of just _s_<sup>_i_</sup> _t_<sup>asin-</sup> puts to capture interactions between slots, as they are not intended to be encoded by the latent action. For implementation, we use the same spatio-temporal model as the IDM, except that the temporal attention uses different queries and keys: 


**Aggregator** . Finally, the aggregator maps the predicted slots back into the feature space, enabling decoding into the nextframe prediction. Instead of relying solely on ˆ _s_<sup>_i_</sup> _t_ +1<sup>to predict</sup> 

4 

**Factored Latent Action World Models** 

## **Algorithm 1** FLAM 

Prepare a video dataset of ( _o_ 1: _T_ ). 

Initialize the VQ-VAE (Encoder, FSQ, Decoder) and the latent action model (Factorizer, IDM, FDM, Aggregator). 

Pretrain the VQ-VAE with the reconstruction loss in Eq. (1). // Train the latent action model 

Extract features with the encoder: 


Map predicted slots back to the feature space: 

_z_ ˆ2: _T_ = Aggregator( _z_ 1: _T −_ 1 _,_ ˆ _s_<sup>1:</sup> 2:<sup>_K_</sup> _T_<sup>).</sup> Optimize the latent action model with the prediction loss in Eq. (6). 

the feature, the aggregator also conditions on the current feature _zt_ . This design allows _s_ ˆ<sup>_i_</sup> _t_ +1<sup>to focus on capturing</sup> changes between current and next time steps, rather than redundantly encoding static visual details. Concretely, the aggregator uses cross-attention to update each patch feature based on the predicted slots: 


**Training objective** . The four components of the latent action model (Factorizer, IDM, FDM, and Aggregator) are trained jointly to minimize the feature prediction error and the KL regularization: 


where _β_ is the KL regularization coefficient. 

Note that although FLAM adopts components similar to prior work (Villar-Corrales & Behnke, 2025; Klepach et al., 2025), such as slot attention and latent action model, it fundamentally differs in its training paradigm and the resulting inductive bias. Prior work typically follows a two-stage procedure: object-centric representations are first learned in isolation, and a latent action model is then trained on top of these fixed representations. As a result, the learned slots largely mirror conventional object-centric representations and are primarily organized according to visual appearance. In contrast, FLAM jointly optimizes slot extraction and latent action model with the prediction loss, with each slot 

endowed with an independent latent action in both the IDM and FDM. This end-to-end factorized dynamics learning encourages the model to separate entities based on the independence of their dynamics rather than visual similarity, yielding representations that are action-driven. 

## **4.3. Learned Latent Actions Utilization** 

The latent actions learned by FLAM implicitly capture the controllable dynamics of individual entities in the environment, providing a natural interface for manipulating video generation. In particular, users can specify latent actions by sampling or selecting values from the prior distribution and use them as control variables during generation, resulting in diverse future trajectories. 

In addition to generation, the learned latent actions encode rich information about agent behavior and enable efficient policy learning directly from video. Using a small demonstration dataset with action labels, we first train an action decoder _f_ via supervised learning to map latent actions _a_ to real actions. For larger datasets that contain only videos without action annotations, we extract latent actions using FLAM and apply the learned decoder to generate pseudolabels for the real actions. These inferred action labels are then used to train a behavior cloning policy: 


# **5. Experiments** 

Our central hypothesis is that the proposed factorized state representation and latent action formulation can better capture the features and dynamics of each entity, leading to more accurate world modeling on multi-entity videos. When used for policy learning, these improved world models should in turn yield higher downstream performance. To test this hypothesis, we evaluate FLAM on both simulation and real-world datasets and provide empirical evaluations pertaining to the following questions that support the indicated answers. 

- **Q1)** Can FLAM learn more accurate world models than baselines? **Yes** (Section 5.1). 

- **Q2)** Does FLAM learn action-driven factorization, grouping entities that share the same action into the same factor while separating entities with different actions? **Yes** (Section 5.2). 

- **Q3)** Do latent actions extracted by FLAM enable more sample-efficient policy learning than learning without them? **Yes** (Section 5.3). 

- **Q4)** How do architecture designs and hyperparameters affect performance? (Section 5.4). 

5 

**Factored Latent Action World Models** 

**Datasets** . We conducted experiments on 4 simulation datasets and 1 real-world dataset. The simulation datasets are collected from the MultiGrid environment (Oguntola et al., 2023) and the Procgen benchmark (Cobbe et al., 2019). From Procgen, we use 3 environments: Bigfish, Leaper, and Starpilot. For a real-world dataset, we use nuPlan (Karnchanachari et al., 2024), an autonomous driving dataset. We use these datasets because they include multiple independent entities, such as agents, enemies, and cars. See details in Appendix A. 

**Implementations** . As introduced in Sec. 4, the encoder is pretrained and frozen during latent action model learning. Rather than training a universal feature extractor across all datasets, we train a separate encoder for each dataset, as our work focuses on demonstrating the benefits of factorization for world models, rather than developing a universal world model. Dataset-specific encoder learning ensures that representation learning is not the performance bottleneck, enabling a meaningful comparison across different methods. Further FLAM implementation details are provided in Appendix B. 

**Baselines** . We compare FLAM against the following baselines. 

- **Genie** (Bruce et al., 2024) and **AdaWorld** (Gao et al., 2025) are vanilla latent action models that infer a single scene-level latent action. Genie constrains latent action capacity via vector quantization, while AdaWorld adopts a VAE-style regularization. Since Genie shares a similar implementation with LAPO, we omit LAPO from our comparisons. 

- **World Model** uses ground-truth actions instead of inferred latent actions and only learns the forward dynamics model. It is evaluated only on simulation datasets where action labels are available. 

- **PlaySlot** (Villar-Corrales & Behnke, 2025) first learns object-centric representations using SAVi (Kipf et al., 2021) and then trains a latent action model on top of the frozen representations. 

- **SlotFormer** (Wu et al., 2022) similarly learns objectcentric representations with SAVi, but trains a slot-based prediction model that conditions only on the current slots (i.e., without latent actions). 

For a fair comparison, all methods use the same pretrained encoder for feature extraction and, when applicable, the same architectures for the factorizer, IDM, and FDM. In addition, to match latent action capacity across methods, while Genie and AdaWorld use a single latent action of dimension _d_ , FLAM and PlaySlot use _K_ factor-wise latent actions of dimension _d/K_ each. 

## **5.1. World Model Accuracy** 

We first evaluate FLAM’s dynamics modeling accuracy, i.e., how accurately the model predicts future frames, and controllability, i.e., how much users can steer video generation via latent actions. 

**Prediction Accuracy** . To assess dynamics modeling accuracy, we first infer latent actions _a_ 1: _T_ from the _unseen_ ground-truth frames _o_ 1: _T_ and then generate _T_ -step predictions ˆ _o_ 1: _T_ autoregressively. We measure prediction quality using peak signal-to-noise ratio (PSNR), learned perceptual image patch similarity (LPIPS), structural similarity index measure (SSIM), and Frechet video distance (FVD).´ Finally, to contextualize the scores, we also report the reconstruction performance of the pretrained VQ-VAE on the future frames (denoted as **Recon** ), which reflects the _best achievable quality_ given the frozen encoder-decoder. 

As shown in Tab. 1, FLAM achieves the best average performance and outperforms most baselines across datasets, highlighting the effectiveness of factored state representations and latent actions in multi-entity domains. Notably, FLAM even outperforms the World Model baseline. We attribute this result to two factors: in Procgen, only the player action is provided, so inferred latent actions help capture the stochastic motion of other entities (e.g., enemies); in MultiGrid, although actions for all agents are available, we follow the standard practice of treating them as a single monolithic action token. Compared to FLAM, World Model’s underperformance further illustrate the limited generalization of monolithic models to state–action pairs that are rare or unseen during training. Meanwhile, as shown in Fig. 10-14, object-centric baselines such as PlaySlot perform competitively in the simple MultiGrid domain but degrade on datasets with more complex visuals, where they often fail to maintain temporally consistent slots. This inconsistency leads to unreliable latent action inference and inaccurate predictions. These results demonstrate the benefit of jointly learning representations and dynamics, rather than training them in separate stages. Appendix C.1 includes some example rollouts. 

**Controllable video generation** . The factored latent actions learned by FLAM not only help with accurate world modeling, but can also serve as a manipulation surrogate to guide the video generation. We let human users specify an entity to control, together with sampling a latent action from the prior distribution for each time step, and then roll out multiple steps. Meanwhile, the remaining entities that are not manipulated would follow their original latent actions. As shown in Fig. 6, latent actions can be used as a control variable to generate various video frames even with the same initial frame. 

6 

**Factored Latent Action World Models** 

_Table 1._ Prediction performance of all methods on simulation and real-world datasets. **Recon** reports the reconstruction quality of the pretrained VQ-VAE, serving as a reference upper bound for prediction performance. 

|Dataset|Metric|FLAM (ours)|AdaWorld|Genie|World Model|PlaySlot|SlotFormer|Recon|
|---|---|---|---|---|---|---|---|---|
||PSNR (_↑_)|**34.9**|24.7|28.1|N/A|29.1|19.9|37.1|
|Averae|SSIM (_↑_)|**0.890**|0.862|0.859|N/A|0.847|0.814|0.909|
|g|LPIPS (_↓_)|**0.051**|0.096|0.091|N/A|0.120|0.223|0.035|
||FVD (_↓_)|**419.6**|749.5|717.5|N/A|858.0|1597.7|215.1|
||PSNR (_↑_)|**56.5**|24.0|33.9|56.1|**56.5**|24.9|56.5|
|MliGid|SSIM (_↑_)|**0.944**|0.909|0.933|0.943|**0.944**|0.912|0.944|
|utr|LPIPS (_↓_)|**3e-4**|0.08|0.014|6e-4|**3e-4**|0.056|3e-4|
||FVD (_↓_)|**2.9**|913.6|177.5|5.5|**2.9**|451.6|2.5|
||PSNR (_↑_)|**30.8**|30.3|28.5|23.9|26.0|19.6|34.4|
|i|SSIM (_↑_)|**0.983**|0.982|0.974|0.949|0.962|0.934|0.992|
|Bigfish|LPIPS (_↓_)|**0.011**|0.012|0.021|0.049|0.038|0.221|0.004|
||FVD (_↓_)|63.6|**63.3**|106.5|168.9|227.4|1455|16.8|
||PSNR (_↑_)|**38.1**|23.3|35.0|24.7|27.5|21.4|40.3|
||SSIM (_↑_)|**0.976**|0.924|0.973|0.924|0.945|0.913|0.977|
|Leaper|LPIPS (_↓_)|**0.002**|0.072|0.005|0.044|0.031|0.164|0.001|
||FVD (_↓_)|**12.1**|348.1|27.3|127.3|361.5|1151|6.27|
||PSNR (_↑_)|**29.3**|27.8|27.0|25.8|18.3|19.8|32.6|
|Sil|SSIM (_↑_)|**0.971**|0.965|0.962|0.959|0.886|0.907|0.980|
|tarpot|LPIPS (_↓_)|**0.015**|0.023|0.028|0.040|0.187|0.166|0.006|
||FVD (_↓_)|**73.4**|113.4|141.0|194.9|792.0|720.9|24.7|
||PSNR (_↑_)|**19.7**|18.1|16.0|N/A|17.2|14.0|21.7|
|Pl|SSIM (_↑_)|**0.577**|0.529|0.453|N/A|0.498|0.405|0.650|
|nuan|LPIPS (_↓_)|**0.229**|0.292|0.389|N/A|0.344|0.508|0.163|
||FVD (_↓_)|**1946**|2309|3135|N/A|2906|4210|1025|


## **5.2. FLAM State Representation** 

Next, we evaluate whether FLAM factorizes state representations according to entities’ actions. Intuitively, the learned factorization is jointly determined by the degree of action independence among entities and the number of factors _K_ . When many entities have similar or correlated actions (e.g., a flock of birds flying together), a smaller _K_ encourages the model to merge them into the same factor, whereas a larger _K_ allows the model to allocate separate factors to individual entities and capture finer-grained action differences. Conversely, when entities act largely independently, FLAM requires a sufficiently large _K_ to model each entity accurately. 

**Correlated Entities** . We construct a controlled MultiGrid dataset where two of four agents always execute identical actions at every timestamp (i.e., their action sequences are strongly correlated), while other aspects of the scene (e.g., positions) may vary. Using _K_ = 3, we evaluate whether FLAM maps the two correlated agents to the same factor. As shown in Fig. 7, FLAM consistently assigns the correlated agents into a single factor, demonstrating that FLAM groups and separates entities based on their dynamics rather than visual appearance. 

**Independent Entities** . On a separate MultiGrid dataset where four agents act independently, we evaluate whether 

FLAM separates them into different factors with _K_ = 4. We adopt the DCI (disentanglement, completeness, informativeness) metric (Eastwood & Williams, 2018) by treating each factor as a latent variable and measuring how well it encodes each agent’s information with a linear probe (see details in Appendix C.2). High disentanglement and completeness indicates that each agent is primarily captured by a distinct factor, rather than being spread across multiple factors. High informativeness indicates that the corresponding factor captures a good amount of information about the agent and has good position prediction accuracy. As shown in Tab. 2, FLAM achieves the highest disentanglement and completeness, suggesting that it more reliably assigns each agent to an independent factors than the object-centric baselines. It also attains competitive informativeness, indicating that this improved factor–agent correspondence does not come at the cost of predictive accuracy. For reference, we also report the DCI scores obtained from randomly generated representations, denoted as **Random** . 

**Number of factors** _K_ . Finally, on the same domain with four independently acting agents, we study the effect of the number of factors by sweeping _K ∈{_ 2 _,_ 4 _,_ 8 _,_ 16 _}_ . 

As shown in Tab. 3, when _K_ is smaller than the number of entities, prediction performance degrades, as expected. Once _K_ is at least the number of entities, performance be- 

7 

**Factored Latent Action World Models** 

_Table 2._ Factor-agent correspondence in the MultiGrid environments, evaluated by DCI (disentanglement, completeness, informativeness) metrics. 

||FLAM(ours)|PlaySlot|SlotFormer|Random|
|---|---|---|---|---|
|D (_↑_)|**0.91**|0.81|0.85|0.32|
|C (_↑_)|**0.91**|0.81|0.85|0.30|
|I (_↑_)|**0.93**|0.86|0.90|0.10|


_Table 4._ Behavior cloning policy performance, evaluated by mean episodic return. 

|Dataset|FLAM|vanilla BC|random|
|---|---|---|---|
|Bigfish (1k)|**1.8**|1.0|09|
|Bigfish (10k)|**8.8**|3.6|.|
|Starpilot (1k)|1.8|**1.9**|11|
|Starpilot (10k)|**9.1**|6.4|.|


## **5.4. Ablation Studies** 

_Table 3._ Prediction performance of FLAM on the MultiGrid dataset with 4 agents and different number of factors _K_ . 

|_K_|2|4|8|16|
|---|---|---|---|---|
|PSNR (_↑_)|53.4|**56.5**|**56.5**|**56.5**|
|SSIM (_↑_)|0.943|**0.944**|**0.944**|**0.944**|
|LPIPS (_↓_)|4e-4|**3e-4**|**3e-4**|**3e-4**|
|FVD (_↓_)|3.62|2.87|2.80|**2.73**|


comes stable across different choices of _K_ , with negligible differences due to training stochasticity. Moreover, as shown in Fig. 8, even with excessive _K_ , FLAM still consistently assigns each entity to a distinct factor across timestamps, demonstrating robustness to over-specifying _K_ . 

Therefore, for datasets where the number of entities varies across scenarios, one can choose a sufficiently large _K_ to cover the maximum number of entities, allowing unused factors to remain inactive when fewer entities are present. 

## **5.3. Latent Action Policy Learning** 

We evaluate whether FLAM can facilitate policy learning from video with limited action supervision. First, for each environment, we train an expert policy using RL and collect an expert demonstration dataset containing 1M frames. Next, we train an action decoder on a small labeled subset of the demonstrations, where ground-truth actions are available, and we vary the labeled subset size (1k and 10k frames) to study label efficiency. We then use learned IDM and action decoder to infer pseudo action labels on the full 1M-frame demonstration dataset, yielding state-action pairs without using the true action labels for training. Finally, we train a behavior cloning policy on these pseudo-labeled data and evaluate its performance in unseen environments. To quantify the benefit of pseudo labels, we compare against a behavior cloning policy trained only on the labeled subset. For reference, we also report the performance of a random policy. 

As shown in Tab. 4, FLAM provides the largest gains at the intermediate label size (10k). With very few action labels (1k), it is challenging to learn a reliable action decoder, so the resulting noisy pseudo labels provide limited benefit. 

We further evaluate how architecture designs and hyperparameters affect FLAM’s prediction performance. 

**Factorizer architecture** . As described in Sec. 4.2, a key design of FLAM’s factorizer is the causal temporal attention, which allows each slot to attend to its past values across timestamps and improves slot consistency. We ablate this component by removing temporal attention from the factorizer. Instead, the factorizer follows SAVi by computing slots autoregressively and initializing the slots at each timestamp using the slots from the previous timestamp. As detailed in Appendix. C.4, this removal significantly hurts prediction performance and slot consistency. 

**Latent action model architecture** . In FLAM, for slot _i_ , the IDM infers the latent action _a_<sup>_i_</sup> _t_<sup>from</sup><sup>_s_1:</sup> _t_<sup>_K_</sup> and _s_<sup>_i_</sup> _t_ +1<sup>, while</sup> the FDM predicts _s_<sup>_i_</sup> _t_ +1<sup>conditioned on</sup><sup>_s_</sup> _t_<sup>1:</sup><sup>_K_</sup> and _a_<sup>_i_</sup> _t_<sup>.This</sup> design encourages per-slot action independence while still accounting for slot interactions. To evaluate this architectural choice, we compare against an ablation, where the IDM infers actions from all slots ( _s_<sup>1:</sup> _t_<sup>_K_</sup> _, s_<sup>1:</sup> _t_ +1<sup>_K_) and the FDM</sup> predicts _s_<sup>_i_</sup> _t_ +1<sup>conditioned on (</sup><sup>_s_</sup> _t_<sup>1:</sup><sup>_K_</sup> _, a_<sup>1:</sup> _t_<sup>_K_</sup> ). As detailed in Appendix C.4, although conditioning on all slots achieves prediction performance similar to the original FLAM, it tends to assign multiple entities into the same factor since there is no explicit incentive to keep them separate, resulting in less disentangled representations. 

**KL regularization coefficient** _β_ controls trade-off between latent action capacity and prediction quality. We report FLAM’s prediction performance across different _β_ values. As detailed in Appendix C.4, FLAM is robust across a wide range of _β_ values, which makes it easy to tune. 

# **6. Conclusion** 

We present FLAM, a factored latent action model that addresses a limitation of prior work in challenging multi-entity scenarios, where the underlying action space grows exponentially with the number of entities. Specifically, FLAM decomposes both the state and latent action representations into independent factors, and assumes all factor share in a common latent action space. Compared to prior work that must capture multi-entity behavior within a single monolithic latent action space, FLAM instead models each entity’s action patterns within this shared space. This factor- 

8 

**Factored Latent Action World Models** 

ized structure enables more accurate modeling of complex multi-entity dynamics and improves both prediction quality and controllability over prior methods. 

**Limitation** In this work, we train a VQ-VAE from scratch for each dataset; adopting and fine-tuning pretrained tokenizers is a promising step toward sharing the encoder across datasets and moving toward a universal latent action model. Moreover, FLAM predicts in latent space using a transformer-based aggregator and relies on a pretrained decoder for visualization. Exploring more expressive decoders, such as diffusion or flow-matching models, could further improve the visual quality of generated rollouts. 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of machine learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

**Acknowledgments** This work has taken place in the Learning Agents Research Group (LARG), Machine Intelligence through Decision-making and Interaction (MIDI) Lab, and Robot Interactive Intelligence (RobIn) Lab at the Artificial Intelligence Laboratory, The University of Texas at Austin. LARG research is supported in part by the National Science Foundation (FAIN-2019844, NRT-2125858), the Office of Naval Research (N00014-24-1-2550), Army Research Office (W911NF-17-2-0181, W911NF-23-2-0004, W911NF-25-1-0065), DARPA (Cooperative Agreement HR00112520004 on Ad Hoc Teamwork), Lockheed Martin, and Good Systems, a research grand challenge at the University of Texas at Austin. MIDI research is supported in part by the National Science Foundation (NSF-2340651, NSF2402650), DARPA (HR00112490431), Army Research Office (W911NF-24-1-0193). The views and conclusions contained in this document are those of the authors alone. Peter Stone serves as the Chief Scientist of Sony AI and receives financial compensation for that role. The terms of this arrangement have been reviewed and approved by the University of Texas at Austin in accordance with its policy on objectivity in research. 

# **References** 

- Baker, B., Akkaya, I., Zhokov, P., Huizinga, J., Tang, J., Ecoffet, A., Houghton, B., Sampedro, R., and Clune, J. Video pretraining (vpt): Learning to act by watching unlabeled online videos. _Advances in Neural Information Processing Systems_ , 35:24639–24654, 2022. 

- Bruce, J., Dennis, M. D., Edwards, A., Parker-Holder, J., Shi, Y., Hughes, E., Lai, M., Mavalankar, A., Steigerwald, R., Apps, C., et al. Genie: Generative interactive 

environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Burgess, C. P., Matthey, L., Watters, N., Kabra, R., Higgins, I., Botvinick, M., and Lerchner, A. Monet: Unsupervised scene decomposition and representation. _arXiv preprint arXiv: 1901.11390_ , 2019. 

- Caesar, H., Kabzan, J., Tan, K. S., Fong, W. K., Wolff, E., Lang, A., Fletcher, L., Beijbom, O., and Omari, S. Nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles, 2022. URL https://arxiv. org/abs/2106.11810. 

- Cobbe, K., Hesse, C., Hilton, J., and Schulman, J. Leveraging procedural generation to benchmark reinforcement learning. _arXiv preprint arXiv:1912.01588_ , 2019. 

- Cobbe, K. W., Hilton, J., Klimov, O., and Schulman, J. Phasic policy gradient. In _International Conference on Machine Learning_ , pp. 2020–2027. PMLR, 2021. 

- Daniel, T., Qi, C., Haramati, D., Zadeh, A., Li, C., Tamar, A., Pathak, D., and Held, D. Latent particle world models: Self-supervised object-centric stochastic dynamics modeling. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL https: //openreview.net/forum?id=lTaPtGiUUc. 

- Eastwood, C. and Williams, C. K. A framework for the quantitative evaluation of disentangled representations. In _International conference on learning representations_ , 2018. 

- Edwards, A., Sahni, H., Schroecker, Y., and Isbell, C. Imitating latent policies from observation. In _International conference on machine learning_ , pp. 1755–1763. PMLR, 2019. 

- Gao, S., Zhou, S., Du, Y., Zhang, J., and Gan, C. Adaworld: Learning adaptable world models with latent actions. _arXiv preprint arXiv:2503.18938_ , 2025. 

- Greff, K., Kaufman, R. L., Kabra, R., Watters, N., Burgess, C., Zoran, D., Matthey, L., Botvinick, M., and Lerchner, A. Multi-object representation learning with iterative variational inference. _arXiv preprint arXiv: 1903.00450_ , 2019. 

- Guestrin, C., Koller, D., Parr, R., and Venkataraman, S. Efficient solution algorithms for factored mdps. _Journal of Artificial Intelligence Research_ , 19:399–468, 2003. 

- Hu, J., Wang, Z., Stone, P., and Mart´ın-Mart´ın, R. Disentangled unsupervised skill discovery for efficient hierarchical reinforcement learning. _Advances in Neural Information Processing Systems_ , 37:76529–76552, 2024. 

9 

**Factored Latent Action World Models** 

- Hu, J., Stone, P., and Mart´ın-Mart´ın, R. Slac: Simulationpretrained latent action space for whole-body real-world rl. _arXiv preprint arXiv:2506.04147_ , 2025. 

- Jiang, J., Deng, F., Singh, G., and Ahn, S. Object-centric slot diffusion. _Neural Information Processing Systems_ , 2023. doi: 10.48550/arXiv.2303.10834. 

- Karnchanachari, N., Geromichalos, D., Tan, K. S., Li, N., Eriksen, C., Yaghoubi, S., Mehdipour, N., Bernasconi, G., Fong, W. K., Guo, Y., et al. Towards learning-based planning: The nuplan benchmark for real-world autonomous driving. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 629–636. IEEE, 2024. 

- Kingma, D. P. and Welling, M. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- Kipf, T., Elsayed, G. F., Mahendran, A., Stone, A., Sabour, S., Heigold, G., Jonschkowski, R., Dosovitskiy, A., and Greff, K. Conditional object-centric learning from video. _arXiv preprint arXiv:2111.12594_ , 2021. 

- Klepach, A., Nikulin, A., Zisman, I., Tarasov, D., Derevyagin, A., Polubarov, A., Lyubaykin, N., and Kurenkov, V. Object-centric latent action learning. _arXiv preprint arXiv:2502.09680_ , 2025. 

- Locatello, F., Weissenborn, D., Unterthiner, T., Mahendran, A., Heigold, G., Uszkoreit, J., Dosovitskiy, A., and Kipf, T. Object-centric learning with slot attention. _Advances in neural information processing systems_ , 33:11525–11538, 2020a. 

- Locatello, F., Weissenborn, D., Unterthiner, T., Mahendran, A., Heigold, G., Uszkoreit, J., Dosovitskiy, A., and Kipf, T. Object-centric learning with slot attention, 2020b. 

- McInnes, L., Healy, J., and Melville, J. Umap: Uniform manifold approximation and projection for dimension reduction. _arXiv preprint arXiv:1802.03426_ , 2018. 

- Mentzer, F., Minnen, D., Agustsson, E., and Tschannen, M. Finite scalar quantization: Vq-vae made simple. _arXiv preprint arXiv:2309.15505_ , 2023. 

- Nikulin, A., Zisman, I., Tarasov, D., Lyubaykin, N., Polubarov, A., Kiselev, I., and Kurenkov, V. Latent action learning requires supervision in the presence of distractors. _arXiv preprint arXiv:2502.00379_ , 2025. 

- Oguntola, I., Campbell, J., Stepputtis, S., and Sycara, K. Theory of mind as intrinsic motivation for multi-agent reinforcement learning. _arXiv preprint arXiv:2307.01158_ , 2023. 

- Osband, I. and Van Roy, B. Near-optimal reinforcement learning in factored mdps. _Advances in Neural Information Processing Systems_ , 27, 2014. 

- Pitis, S., Creager, E., and Garg, A. Counterfactual data augmentation using locally factored dynamics. _Advances in Neural Information Processing Systems_ , 33:3976–3990, 2020. 

- Qi, C., Haramati, D., Daniel, T., Tamar, A., and Zhang, A. EC-diffuser: Multi-object manipulation via entitycentric behavior generation. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum? id=o3pJU5QCtv. 

- Schmidt, D. and Jiang, M. Learning to act without actions. _arXiv preprint arXiv:2312.10812_ , 2023. 

- Sodhani, S., Levine, S., and Zhang, A. Improving generalization with approximate factored value functions. _Transactions on Machine Learning Research_ , 2022. 

- Van Den Oord, A., Vinyals, O., et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- Villar-Corrales, A. and Behnke, S. Playslot: Learning inverse latent dynamics for controllable object-centric video prediction and planning. In _International Conference on Machine Learning (ICML)_ , 2025. 

- Wang, Z., Xiao, X., Xu, Z., Zhu, Y., and Stone, P. Causal dynamics learning for task-independent state abstraction. _arXiv preprint arXiv:2206.13452_ , 2022. 

- Wang, Z., Wang, K., Zhao, L., Stone, P., and Bian, J. Dyno: Building structured world models with object-centric representations. _arXiv preprint arXiv:2507.03298_ , 2025. 

- Wu, Z., Dvornik, N., Greff, K., Kipf, T., and Garg, A. Slotformer: Unsupervised visual dynamics simulation with object-centric models. _arXiv preprint arXiv:2210.05861_ , 2022. 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 

- Ye, W., Zhang, Y., Abbeel, P., and Gao, Y. Become a proficient player with limited data through watching pure videos. In _The Eleventh International Conference on Learning Representations_ , 2022. 

- Zhang, Q., Peng, Z., and Zhou, B. Learning to drive by watching youtube videos: Action-conditioned contrastive policy pretraining. In _European Conference on Computer Vision_ , pp. 111–128. Springer, 2022. 

10 

**Factored Latent Action World Models** 

# **A. Dataset Details** 

We summarize here the datasets used in our experiments with additional implementation details. All datasets are split into train/validation/test with an 80-10-10 ratio by frame count, unless otherwise specified. Frames are normalized to [0 _,_ 1] and resized to the image resolutions reported in Table 5. 

**MultiGrid (Simulation).** We adopt the MultiGrid environment (Oguntola et al., 2023) that supports multiple independently moving agents. Each video consists of a 8 _×_ 8 grid world rendered at 128 _×_ 128 resolution, with between 2 - 16 agents moving simultaneously. Unless specified otherwise, we use the dataset where all videos consist of 4 agents and the number of factors _K_ is set to 4. 

**Procgen (Simulation).** We adopt the Procgen benchmark (Cobbe et al., 2019) with background rendering disabled for consistency. Videos are rendered at 224 _×_ 224 resolution. 

**nuPlan (Real-world).** We use the nuPlan benchmark (Caesar et al., 2022), restricting to front-facing camera streams only. Frames are resized to 224 _×_ 224, and the number of factors is set to _K_ = 16 to capture vehicles and pedestrians in each scene. 

# **B. Implementation Details** 

The hyperparameters used during encoder and factored latent action model training can be found in Table 5. 

_Table 5._ Experiment hyperparameters. Simulation datasets are Multigrid and Procgen, while the real-world dataset is nuPlan. 

||**Simulation**|**Real-world**|
|---|---|---|
|Encoder architecture|IMPALA|MAGVIT-v2|
|Decoder architecture|IMPALA|MAGVIT-v2|
|Image size|128 (Multigrid), 224 (Procgen)|224|
|_dz_|128|128|
|Tokenizer quantizer|FSQ|FSQ|
|Tokenizer codebook size|1024|16384|
|Tokenizer codebook levels|[4,4,4,4,4]|[4,4,4,4,4,4,4]|
|Optimizer|AdamW|AdamW|
|Learning rate|1e-4|1e-4|
|Batch size|64|64|
|Attention model dimension|256|256|
|Number of attention heads|8|8|
|Number of attention layers|2|3|
|Number of factors_K_|4 (Multigrid), 16 (Procgen)|16|
|KL regularization coefficient_β_|2e-4|2e-4|
|i<br>Optimizer|AdamW|AdamW|
|Learning rate|1e-4|1e-4|
|Batch size|32|32|


**Computational Cost** Let _N_ denote the number of patch-level features. FLAM’s computation cost primarily consists of the attention between patches and slots, which scales as _O_ ( _NK_ ), and interaction modeling among slots in the IDM/FDM, which scales as _O_ ( _K_<sup>2</sup> ) per timestep. Since _K_ is chosen to reflect the number of high-level entities and is typically much smaller than the number of patch tokens _N_ , this slot-level interaction cost is modest in our experiments. In contrast, dense patch-level video models often perform attention over all patch tokens, which scales as _O_ ( _N_<sup>2</sup> ). 

11 

**Factored Latent Action World Models** 

# **C. Experiments** 

## **C.1. World Model Accuracy** 

We evaluate FLAM from two perspectives, dynamics modeling accuracy, i.e., how accurately the model predicts future frames, and controllability, i.e., how much users can steer video generation via latent actions. 

**Prediction Accuracy** To assess dynamics modeling accuracy, we first infer latent actions _a_ 1: _T_ from the ground-truth frames _o_ 1: _T_ and then generate _T_ -step predictions ˆ _o_ 1: _T_ autoregressively, where we use _T_ = 10 across all datasets. In addition to the quantitative results in Sec. 5.1, we visualize example rollouts in Fig. 10-14. Across most datasets, FLAM generates more consistent factor-entity bindings and more accurate predictions than the baselines. 

**Scaling with the number of entities** To investigate whether FLAM facilitates dynamics modeling in complex multi-entity videos, we conduct an ablation study on MultiGrid by varying the number of entities. For a fair comparison, we match the total latent action capacity between FLAM and AdaWorld. For instance, on the 8-agent setting, AdaWorld uses a single 256-dimensional latent action, while FLAM uses eight 32-dimensional latent actions. For Genie, we similarly ensure its latent action capacity by matching the codebook size to the number of joint action combinations. As shown in Fig. 4, as the number of entities increases, FLAM remains substantially more robust than a non-factored LAM. 


_Figure 4._ Prediction performance variation along with increasing number of entities in the scene. 

**Controllable video generation** The factored latent actions learned by FLAM not only help with accurate world modeling, but can also serve as a manipulation surrogate to guide the video generation. We let human users specify an entity to control, together with sampling a latent action from the prior distribution for each time step, and then roll out multiple steps. Meanwhile, the remaining entities that are not manipulated would follow their original latent actions. An example of generated videos is shown in Fig. 6. The first row is the original video. Take the first frame of the original video as the initial start, each of the following rows represents the generated video of manipulating one entity. It demonstrates that latent actions can be used as a control variable to generate various video frames even with the same initial frame. This indicates 

12 

**Factored Latent Action World Models** 

that factorization offers the freedom of manipulating each entity independently instead of the monolithic scene, therefore leading to more diversity in video generation. 


_Figure 5._ UMAP projection of the learned latent actions on the MultiGrid dataset. Each point corresponds to a latent action inferred by the IDM for one factor on a single transition from the observation-only dataset. Points are colored by the ground-truth actions taken by the corresponding agent at that transition (action labels are used only for visualization and are not used for training). 

To demonstrate that FLAM learns latent actions that are well separated across different ground-truth actions and thus easy for humans to specify, we visualize the extracted latent actions for all agents by projecting them to 2D with UMAP (McInnes et al., 2018). As shown in Fig. 5, the latent actions form well-separated clusters that align with the true actions, with only a small number of move forward samples overlapping with stay still clusters. This overlap is expected, as, in many scenarios, an agent may take a move forward action but remain stationary due to being blocked. In such cases, the observed transition is indistinguishable from stay still, and the inferred latent action accordingly falls into the stay still cluster. 

## **C.2. FLAM State Representation** 

**Correlated Entities** We construct a controlled MultiGrid dataset where two of four agents always execute identical actions at every timestamp (i.e., their action sequences are strongly correlated), while other aspects of the scene (e.g., positions) may vary. Using _K_ = 3, we evaluate whether FLAM maps the two correlated agents to the same factor. As shown in Fig. 7, FLAM is able to group the entities that share the same action into the same factor, while separating the entities with different actions, based on their dynamics rather than visual appearance. **Independent Entities** In this section, we provide details of the DCI (disentanglement, completeness, informativeness) evaluation used in Sec. 5.2. 

We use an unseen MultiGrid dataset with 4 agents for evaluation, and all evaluated methods use _K_ = 4 factors during training. To compute the DCI score, we first extract slots _s_<sup>1:</sup><sup>_K_</sup> _∈_ R<sup>_K×d_</sup> for each frame. We also record the agent position _y_<sup>1:</sup><sup>_K_</sup> , each _y_<sup>_i_</sup> _∈{_ 1 _, . . . , C}_ is a discrete scalar indicating which grid the agent _i_ is at among _C_ potential locations. Then we split the data into a train set for probe learning and a validation sets for DCI computation. 

During training, we learn a linear classifier probe _f_ : R<sup>_d_</sup> _→_ ∆<sup>_C_</sup> that predicts the agent position from each slot. Slots are permutation-equivariant, i.e., slot _i_ can correspond to different agents across frames. We therefore learn probes using permutation-invariant assignment. To compare a slot _i_ against a candidate agent _j_ , we use the negative log-likelihood as the 

13 

### **Factored Latent Action World Models** 


_Figure 6._ FLAM allows for changing / editing the motion of one entity without affecting the others. Here we show controllable video generation on MultiGrid through specifying latent actions for one of the movable agents, while other agents follow their original inferred latent actions. 

cost and solve a matching problem to enforce a one-to-one correspondence _τ_ between slots and agents: 


where _SK_ is the set of permutations of _{_ 1 _, . . . , K}_ and _τ_ is computed with the Hungarian algorithm. Given _τ_ , the probe is trained with cross-entropy on the matched labels. 

After training, we follow (Eastwood & Williams, 2018) to compute DCI metrics as follows. 

- **Disentanglement and completeness** : To quantify whether each slot corresponds to a single agent (disentanglement) and each agent is covered by a single slot (completeness), we convert likelihood into soft assignment distributions. We define disentanglement and completeness distributions: 


14 

### **Factored Latent Action World Models** 


_Figure 7._ Two example rollouts where two entities (green and red ones) share the same actions. FLAM consistently maps the two correlated agents to the same factor. 

We then compute disentanglement and completeness using normalized entropy with base _K_ : 


We report _D_ and _C_ averaged over all slots / agents and over all frames in the validation set. 

- **Informativeness** : We measure informativeness as the classification accuracy under the optimal matching and report _I_ averaged over all frames in the validation set. 


**Number of factors** _K_ Finally, on the same domain with four independently acting agents, we study the effect of the number of factors by sweeping _K ∈{_ 2 _,_ 4 _,_ 8 _,_ 16 _}_ . 

In datasets where the number of entities varies across scenarios, one can choose a sufficiently large _K_ to cover the maximum number of entities, allowing unused factors to remain inactive when fewer entities are present. 

## **C.3. Latent Action Policy Learning** 

During data collection, for each Procgen environment, we train an expert policy using Phasic Policy Gradient (Cobbe et al., 2021) on all levels for 25M environment steps. We then collect demonstrations on disjoint sets of levels for training, validation, and testing, ensuring that the behavior cloning policy is evaluated on unseen environments. For a fair comparison, FLAM and the vanilla behavior cloning baseline use the same policy architecture and training setup, and the only difference is that FLAM additionally trains on pseudo action labels inferred from unlabeled videos. 

15 

**Factored Latent Action World Models** 

_Table 6._ Prediction performance of FLAM and its ablative variants on the MultiGrid dataset. 

|Metric|FLAM (ours)|FLAM w/o Factorizer Temporal Attention|Global-Coupled FLAM|
|---|---|---|---|
|PSNR (_↑_)|**56.5**|51.6|56.3|
|SSIM (_↑_)|**0.944**|0.941|**0.944**|
|LPIPS (_↓_)|**3e-4**|3e-3|4e-4|
|FVD (_↓_)|**2.9**|36.6|3.72|


_Table 7._ Factor-agent correspondence of FLAM and its ablative variants on the MultiGrid dataset, evaluated by DCI (disentanglement, completeness, informativeness) metrics. 

||FLAM(ours)|FLAM w/o Factorizer Temporal Attention|Global-Coupled FLAM|Random|
|---|---|---|---|---|
|D (_↑_)|**0.91**|0.33|0.79|0.32|
|C (_↑_)|0.91|0.23|**1.00**|0.30|
|I (_↑_)|**0.93**|0.20|0.58|0.10|


## **C.4. Ablation Studies** 

We further evaluate how architecture designs and hyperparameters affect FLAM’s prediction performance. 

**Factorizer architecture** As described in Sec. 4.2, a key design of FLAM’s factorizer is the causal temporal attention, which allows each slot to attend to its past values across timestamps and improves slot consistency. We ablate this component by removing temporal attention from the factorizer. Instead, the factorizer follows SAVi by computing slots autoregressively and initializing the slots at each timestamp using the slots from the previous timestamp. Then we evaluate its impact on prediction performance and representation quality. 

As shown in Tab. 6 and Fig. 9, removing temporal attention leads to temporally inconsistent factor assignments and degraded predictions. Moreover, Tab. 7 shows that this ablation substantially reduces factor-entity correspondence, demonstrating the importance of temporal attention in maintaining consistent bindings over time. 

**Latent action model architecture** In FLAM, for slot _i_ , the IDM infers the latent action _a_<sup>_i_</sup> _t_<sup>from</sup><sup>_s_1:</sup> _t_<sup>_K_</sup> and _s_<sup>_i_</sup> _t_ +1<sup>, while the</sup> FDM predicts _s_<sup>_i_</sup> _t_ +1<sup>conditioned on</sup><sup>_s_</sup> _t_<sup>1:</sup><sup>_K_</sup> and _a_<sup>_i_</sup> _t_<sup>.This design encourages per-slot action independence while still accounting</sup> for slot interactions. To evaluate this architectural choice, we compare against an ablation, **Global-Coupled FLAM** , where the IDM infers actions from all slots ( _s_<sup>1:</sup> _t_<sup>_K_</sup> _, s_<sup>1:</sup> _t_ +1<sup>_K_) and the FDM predicts</sup><sup>_si_</sup> _t_ +1<sup>conditioned on (</sup><sup>_s_</sup> _t_<sup>1:</sup><sup>_K_</sup> _, a_<sup>1:</sup> _t_<sup>_K_</sup> ). 

As shown in Tab. 6, this ablation achieves prediction performance similar to the original FLAM, as it retains the same overall capacity for encoding transition information. However, because both the IDM and FDM condition on all slots and all latent actions, the model has little incentive to maintain a one-to-one correspondence between entities and factors. In particular, the FDM can attend to _a_<sup>_j_</sup> _t_<sup>when predicting</sup><sup>_si_</sup> _t_ +1<sup>and still achieve accurate prediction.Consequently, as shown in</sup> Tab. 7 and Fig. 9, Global-Coupled FLAM tends to merge multiple entities into the same factor, yielding less disentangled representations. 

**KL regularization coefficient** _β_ controls the trade-off between latent action capacity and prediction quality. We report prediction performance across different _β_ values to quantify FLAM’s sensitivity to this hyperparameter. As shown in Tab. 8, FLAM is robust across a wide range of _β_ values, which makes it easy to tune. 

_Table 8._ Prediction performance of FLAM on the MultiGrid dataset with different KL regularization coefficient _β_ values. 

|Metric|_β_ = 1_e −_5|_β_ = 1_e −_4|_β_ = 1_e −_3|_β_ = 1_e −_2|
|---|---|---|---|---|
|PSNR (_↑_)|**56.5**|**56.5**|56.3|24.9|
|SSIM (_↑_)|**0.944**|**0.944**|**0.944**|0.911|
|LPIPS (_↓_)|**3e-4**|**3e-4**|4e-4|0.057|
|FVD (_↓_)|**2.84**|3.40|3.78|479.9|


16 

**Factored Latent Action World Models** 


_Figure 8._ Ablation of FLAM on 4-agent MultiGrid dataset, with _K ∈{_ 2 _,_ 4 _,_ 8 _,_ 16 _}_ . When _K_ is less than the number agents, FLAM assigns two agents to each factor to maximize latent action utilization. When _K_ is equal to or greater than the number of agents, FLAM consistently assigns each entity to a distinct factor, even with excessive _K_ , demonstrating FLAM’s robustness to over-specifying _K_ . 

17 

**Factored Latent Action World Models** 


_Figure 9._ Architecture ablations of FLAM on the 4-agent MultiGrid dataset. Removing temporal attention from the factorizer leads to temporally inconsistent factor assignments and degraded long-horizon predictions (notably in the last few timestamps). In contrast, the Global-Coupled variant can produce accurate predictions but tends to assign multiple entities into the same factor, resulting in poorer disentanglement than the original FLAM implementation. 

18 

**Factored Latent Action World Models** 


_Figure 10._ Prediction rollouts of all methods on the MultiGrid dataset, with inaccuracies highlighted by red boxes (except for SlotFormer, where the errors are visually apparent). When applicable, we also show the slot-patch binding masks from slot attention, displayed on top of the ground-truth observations. FLAM maintains consistent factor-entity bindings over time and generates accurate predictions. In contrast, AdaWorld and SlotFormer fail to generate accurate predictions from the start, and Genie makes mistakes at a few steps. Meanwhile, PlaySlot and SlotFormer rely on object-centric representations learned from reconstruction which incorrectly bind the red and purple entities to the same slot. 

19 

**Factored Latent Action World Models** 


_Figure 11._ Prediction rollouts of all methods on the Bigfish dataset, with inaccuracies highlighted by red circles (except for SlotFormer, where the errors are visually apparent). When applicable, we also show the slot-patch binding masks from slot attention, displayed on top of the ground-truth observations. FLAM maintains consistent factor-entity bindings over time, e.g., the brown slot consistently attends to the green fish controlled by the player. In terms of prediction quality, FLAM and Genie only make errors on the occluded fish. AdaWorld to track the speeds of the circled yellow and red fish, which move more slowly than in the ground truth. The World Model baseline also struggles to capture the motion of non-controllable fish, since only the player’s action is available. PlaySlot and SlotFormer rely on reconstruction-based object-centric representations that do not yield consistent slot assignments. As a result, PlaySlot fails to preserve consistent shapes and colors for multiple fish. 

20 

**Factored Latent Action World Models** 


_Figure 12._ Prediction rollouts of all methods on the Leaper dataset, with inaccuracies highlighted by red boxes (except for PlaySlot and SlotFormer, where the errors are visually apparent). When applicable, we also show the slot-patch binding masks from slot attention, displayed on top of the ground-truth observations. FLAM generates accurate predictions, in particular capturing how the frog jumps between logs. Genie and World Model achieve the second best prediction quality, but fails to model the frog’s jumps in some timestamps. In contrast, AdaWorld and PlaySlot generate inaccurate predictions from the start, either removing the frog and cars from the scene or hallucinating non-existent. 

21 

**Factored Latent Action World Models** 


_Figure 13._ Prediction rollouts of all methods on the Starpilot dataset, with inaccuracies highlighted by red circles (except for PlaySlot and SlotFormer, where the errors are visually apparent). When applicable, we also show the slot-patch binding masks from slot attention, displayed on top of the ground-truth observations. FLAM maintains a consistent binding for the player in the bottom-left corner (shown in cyan) and generates accurate predictions, except for the enemy bullet heading toward the player. Other entities (e.g., bullets, enemies, and meteors) move at constant speed, so even with less consistent bindings, FLAM can still achieve reasonable predictions. In contrast, AdaWorld, Genie, and the World Model baseline generate inaccurate predictions from the start, frequently shifting enemy appearances and missing the enemy bullet toward the player. 

22 

**Factored Latent Action World Models** 


_Figure 14._ Prediction rollouts of all methods on the nuPlan dataset, with inaccuracies highlighted by red boxes (except for SlotFormer, where the errors are visually apparent). Models are conditioned on a fixed history window of size _w_ = 5. When applicable, we also show the slot-patch binding masks from slot attention, displayed on top of the ground-truth observations. Compared to the baselines, FLAM generates relatively accurate predictions for the grey car moving from the center to the right. In contrast, AdaWorld and Genie fail to maintain a consistent appearance for this moving car. Meanwhile, PlaySlot and SlotFormer fail to model the dynamics and largely ignore the cars in the scene. 

23 

