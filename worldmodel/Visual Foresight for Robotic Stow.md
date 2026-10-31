---
title: "Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots"
date: "2026-02-12"
authors: "Lijun Zhang; Nikhil Chacko; Petter Nilsson; Ruinian Xu; Shantanu Thakar; Bai Lou"
url: https://arxiv.org/abs/2602.13347
pdf: https://arxiv.org/pdf/2602.13347
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.13347)** / [論文ページ](https://arxiv.org/abs/2602.13347)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

**Lijun Zhang**<sup>1</sup> **Nikhil Chacko**<sup>1</sup> **Petter Nilsson**<sup>1</sup> **Ruinian Xu**<sup>1</sup> **Shantanu Thakar**<sup>1</sup> **Xibai Lou**<sup>1</sup> **Harpreet S. Sawhney**<sup>1</sup> **Zhebin Zhang**<sup>1</sup> **Mudit Agrawal**<sup>1</sup> **Bhavana Chandrashekhar**<sup>1</sup> **Aaron Parness**<sup>1</sup> 

# **Abstract** 

Automated warehouses execute millions of stow operations, where robots place objects into storage bins. For these systems it is valuable to anticipate how a bin will look from the current observations and the planned stow behavior before real execution. We propose FOREST, a stow-intentconditioned world model that represents bin states as item-aligned instance masks and uses a latent diffusion transformer to predict the post-stow configuration from the observed context. Our evaluation shows that FOREST substantially improves the geometric agreement between predicted and true post-stow layouts compared with heuristic baselines. We further evaluate the predicted poststow layouts in two downstream tasks, in which replacing the real post-stow masks with FOREST predictions causes only modest performance loss in load-quality assessment and multi-stow reasoning, indicating that our model can provide useful foresight signals for warehouse planning. 

# **1. Introduction** 

Stow is the operation of placing objects into storage containers such as bins or shelves (Cosgun et al., 2011; Basu et al., 2012; Chen et al., 2023). Humans perform similar actions when organizing books on a bookshelf or loading a cabinet. In large fulfillment centers, the same operation must be carried out millions of times per day, making manual execution costly and limiting overall throughput. As a result, advanced warehouses deploy robotic systems that automate the stow process. Stow has become an important task in robotic manipulation aimed at improving storage efficiency while maintaining inventory accuracy (Hudson et al., 2025; Park et al., 2025). 

In this work we study a complementary capability for 

> 1Amazon, Seattle, US. Correspondence to: Lijun Zhang _<_ ljzhang@amazon.com _>_ . 

_Preprint. February 17, 2026._ 

robotic stow that we call _visual foresight for stow_ . Visual foresight broadly denotes predicting how future visual observations will look given a current state and an intended physical action, and is closely related to world models in robotics and control (Finn & Levine, 2017; Ebert et al., 2018; Bar et al., 2025). Such predictive models do not replace but complement planners by providing useful supervision about dynamics that serve as signals when choosing from candidate actions. In this paper, we consider the visual foresight problem in a bin-based stow system. Given a pre-stow bin observation, the item to be stowed, and a high-level description of how the robot intends to place the item, we wish to forecast the bin layout after the specified stow, before physical execution. Accurate forecasts can support downstream decision making, for example by estimating how a proposed stow will affect storage density or by performing long-horizon planning. 


_Figure 1._ Examples of visual foresight for robotic stow. 

Studying visual foresight for stow in a real production poses several challenges. First, supervision is inherently sparse because continuous video capture at warehouse scale is impractical, and intermediate motion is frequently occluded by the robot and the incoming item. Consequently, production datasets commonly provide only pre- and post-stow RGB snapshots, as in ARMBench (Hudson et al., 2025). Second, real deployments exhibit substantial diversity, including thousands of distinct items that vary in size, shape, and rigidity, as well as storage bins with different geometries, which jointly affect perception and contact outcomes. Third, stow is interaction intensive because the incoming item can push, slide, or topple existing items and induce non-local rearrangements that are difficult to infer from 

1 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

sparse observations (see Figures 1). These factors motivate the world-modeling framework proposed in this work for learning object dynamics in real stow scenarios. 

Given these challenges, we approach visual foresight for stow as learning a stow-intent-conditioned world model and propose FOREST (FOREST, <u>Foresight</u> for <u>STow).</u> Starting from the sparse pre- and post-stow snapshots, we first derive a structured prediction target by extracting instance masks and aligning items before and after stow via item matching, so that each physical item occupies a dedicated slot in both the pre- and post-stow bin states. FOREST then learns to map the pre-stow bin state, a new-item observation, and a high-level stow intent to a predicted post-stow bin state in this slot-based representation. Specifically, a transformer-based latent diffusion model, conditioned on the stow context, is designed to approximate the item-level rearrangements induced by real stow operations. 

Our main contributions are: 

- _FOREST_ — a framework for visual foresight of robotic stow from sparse pre- and post-stow snapshots in the real production. To the best of our knowledge, FOREST is the first learned world model that operate in real stow scenario with only snapshot supervision. 

- _Direct evaluation_ — we quantify post-stow prediction performance using instance-level IoU between the predicted and ground-truth post-stow masks. FOREST consistently improves IoU for the newly inserted item over heuristic baselines by 0 _._ 3-0 _._ 5, while maintaining high IoU for pre-existing items. 

- _Downstream evaluation_ — we further evaluate whether predicted post-stow masks are effective inputs for two downstream tasks. For bin free-space change prediction, which measures the change in available horizontal stow space and serves as a load-related proxy, replacing ground-truth post-stow masks with FORESTpredicted masks increases prediction MAE by only 0 _._ 0016-0 _._ 0025. For multi-stow reasoning, we roll out FOREST over consecutive stows in the same bin and show that it supports long-horizon prediction. 

# **2. Problem Statement and Preliminaries** 

We first introduce the targeted stow data, formalize the visual foresight problem for robotic stow, and then review the diffusion model background necessary for our world model. Additional related work is provided in Appendix A. 

**Stow Data in Production.** We target ARMBench (Hudson et al., 2025), a large-scale dataset of real stows collected from robotic warehousing systems in production (see Figure 2). Specifically, items are stored in rectangular fabric bins observed by a frontal camera, and a _stow event_ corresponds to placing one item into a target bin. For each stow 

event, ARMBench provides: (i) a pre-stow RGB image of the bin, (ii) a post-stow RGB image of the same bin, (iii) an top-down RGB image of the incoming item captured at the induction station, (iv) the incoming item’s physical properties, and (v) the stow intent, that is, high-level metadata indicating how the robot plans to execute the stow. 

The system follows a bookshelf-like stowing paradigm in which item side faces are generally oriented toward the camera for subsequent picking (Hudson et al., 2025; Park et al., 2025). Accordingly, the stow intent specifies a planned placement pose and, when necessary, a sweeping operation that first creates free space by pushing existing items before inserting the new item. This induces an unobserved intermediate state between the pre- and post-stow snapshots, making post-stow state prediction particularly difficult. Also despite this coarse intent taxonomy, the task remains challenging due to the massive variety of incoming items and the use of deformable fabric bins, whose effective geometry and available space can change under contact. 


_Figure 2._ Examples in ARMBench with pre-stow RGB, post-stow RGB, and induct-view new item image. The stow intents are depicted by bounding box overlayed on the pre-stow RGB image, in which green one refers to the planned position for new item placement while the blue one is the location of sweeping operation. 

**Visual Foresight for Stow.** We view visual foresight for stow as learning a transition model over bin states. Given the bin state before a stow, an observation of the new item, and the planned stow intent, the model should anticipate how the bin state will change after executing that stow. Unlike many prior visual foresight settings that rely on dense video sequences (Finn & Levine, 2017; Ebert et al., 2018), each stow event in ARMBench is observed only through a pair of temporally sparse snapshots, a pre-stow bin state and a post-stow bin state. Our goal is to learn from these sparse observations a single-step world model (Ha & Schmidhuber, 2018) that predicts a structured future bin state. 

Formally, let _X_ denote the space of bin states, _O_ the space of new-item observations, and _U_ the space of stow intents. Each stow event is represented as a tuple ( _x_ pre _, o_ new _, u, x_ post), where _x_ pre _∈X_ is the pre-stow bin state, _o_ new _∈O_ is the observation of the item to 

2 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

be stowed, _u ∈U_ is the associated stow intent, and _x_ post _∈X_ is the post-stow bin state. Given a dataset _D_ = _{_ ( _x_<sup>(</sup> pre<sup>_i_)</sup><sup>_, o_</sup> new<sup>(</sup><sup>_i_)</sup><sup>_, u_(</sup><sup>_i_)</sup><sup>_, x_(</sup> post<sup>_i_))</sup><sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>, we aim to learn a world</sup> model _Fθ_ : _X × O × U →X_ that maps the current state, new item, and intent to a prediction of the future state: _x_ ˆpost = _Fθ_ � _x_ pre _, o_ new _, u_ � _._ (1) In §3, we instantiate _x_ pre and _x_ post with an instance-maskbased representation of bin states, and _Fθ_ with a diffusionbased world model. 

**Diffusion-Based World Models.** Diffusion models (SohlDickstein et al., 2015) are generative models that synthesize data by learning to invert a gradual noising process. We summarize the basics in Appendix B. For high-resolution vision tasks, it is effective to apply diffusion in a compact latent space rather than directly in pixel space. For instance, Stable Diffusion (Rombach et al., 2022) operates on the latent space of a pre-trained variational autoencoder (VAE). Beyond image synthesis, recent work show that diffusion models can serve as world models, learning predictive dynamics that map current states and actions to future states in domains such as games, autonomous driving, and robotic manipulation (Alonso et al., 2024; Gao et al., 2024; Huang et al., 2025). Motivated by these findings, we instantiate visual foresight for stow as a latent diffusion world model conditioned on the stow context, as detailed in §3.4. 

# **3. FOREST: A Diffusion-Based World Model for Visual Foresight in Stow** 

## **3.1. Overview of FOREST** 

Figure 3 summarizes the overall pipeline of FOREST with three stages. We first explain the high-level idea, and then detail each stage. 

**Stage 1: From ARMBench Snapshots to Supervised Signals.** We first extract instance masks for all items in the preand post-stow RGB snapshots of each stow event. An itemmatching procedure then establishes a one-to-one correspondence between pre- and post-stow instances. Stacking the binary masks according to this mapping yields slot-based pre- and post-stow bin states that describe how items occupy the bin before and after the operation. The unmapped extra mask in the post-stow instances is the mask of the newly stowed item and is canonicalized before being fed into the model. These item-aligned bin states and the identified new item mask serve as supervision for training the world model. §3.2 details mask extraction and item matching steps. 

**Stage 2: Input Modeling and Tokenization.** Next, we encode both the stow context and the future bin layout into latent features and tokens. An off-the-shelf VAE (Stability AI) transforms inputs, including the slot-based pre- and 

post-stow bin states, the canonical item mask, and the prestow snapshot, from either binary masks or RGB image to latent feature maps. For the post-stow latent, we sample a diffusion timestep, add Gaussian noise according to the diffusion forward process, and patchify the noisy latent into a sequence of input tokens during training. The other latents as well as the conditioned item property embedding are structured into condition tokens, augmenting with learned instance and condition-type embeddings such that the model can distinguish different items and conditioning sources. §3.3 presents this modeling and tokenization step. 

**Stage 3: Diffusion-based World Model.** Finally, we instantiate FOREST as a transformer-based latent diffusion model. At each diffusion timestep, the model takes the noisy post-stow tokens as queries and the condition tokens from the stow context as keys and values in cross-attention layers, so that the denoising updates depend explicitly on the pre-stow configuration and the new item information. A joint embedding of the stow intent and diffusion timestep modulates every transformer block through Adaptive Layer Normalization (AdaLN) (Xu et al., 2019). §3.4 describes the architecture in detail. 

## **3.2. From ARMBench Snapshots to Supervised Signals** 

FOREST is trained from raw ARMBench streams by converting each stow event into (i) a pair of slot-aligned preand post-stow bin states and (ii) a canonical new-item mask used as the item observation. 

**Instance Masks Extraction.** Since our goal is to predict how a stow rearranges the bin at the object level, we represent bin states as sets of binary instance masks, one per visible item. This object-centric representation makes item contacts explicit while avoiding the need to model finegrained textures that are less relevant to stow outcomes. As ARMBench does not provide instance masks, we derive from the RGB images using a MaskDINO-based instance segmentation model (Li et al., 2022), and use the resulting masks as the starting point for bin-state construction. 

**Item Matching.** Based on the extracted instance masks, we construct slot-based, item-aligned bin states via item matching. For each stow event, since we focus on singletransition cases where exactly one new item is stowed into the bin, the numbers of instances in the pre-and post-stow snapshots satisfy _N_ post = _N_ pre + 1. In each snapshot, we first stack the binary instance masks as channels and refer to each channel as a _slot_ , so that each slot corresponds to a single physical item. An item-matching procedure then establishes a one-to-one correspondence between preand post-stow instance slots such that every pre-existing item, visible in both snapshots, is assigned the same slot index before and after the stow, and the remaining post-stow instance is identified as the newly stowed item. 

3 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 


_Figure 3._ Overview of FOREST, our diffusion-based world model for visual foresight of stow with three stages. Stage 1 constructs slot-aligned pre- and post-stow bin states from ARMBench snapshots via instance masks extraction and item matching. Stage 2 encodes bin states and stow context into latent vectors and then noisy tokens and condition tokens. Stage 3 uses a transformer-based latent diffusion model with cross-attention and adaptive layer normalization to incorporate condition tokens. 

We formulate item matching as an assignment problem with priors derived from the stow behavior. Let _{m_<sup>pre</sup> _i_<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>preand</sup> _{m_<sup>post</sup> _j }_<sup>_N_</sup> _j_ =1<sup>postdenote the pre- and post-stow instance masks.</sup> For each mask, we crop the RGB patch and extract a visual embedding with pretrained DINOv2 (Oquab et al., 2023), obtaining _{e_<sup>pre</sup> _i_<sup>_}_and</sup><sup>_{e_post</sup> _j }_ , and build a base cost matrix from their cosine similarity _Dij_ . We then add two priors derived from the stow intent, a placement prior that favors assignments placing the new item near the planned insertion position and, when present, the sweeping position, and an order-preservation prior that discourages changes in the leftto-right ordering of pre-existing items. The final cost is 


where Φpos and Φord encode placement and order penalties (see details in Appendix C). We solve this assignment with Hungarian algorithm (Kuhn, 1955) to obtain a one-to-one matching consistent with visual similarity and stow priors. 

Given the matching result, we reserve the first slot for the newly stowed item and assign all matched pre-existing items to the remaining slots. In particular, the first slot is set to all zeros for the pre-stow bin state, reflecting that the new item is not yet present. These slot-aligned bin states serve as the supervision signal for training the world model. 

**New Item Canonicalization.** ARMBench provides a separate induct-view image for the new item, however, the post-stow bin layout is more directly related to the in-bin contact-surface view recovered from item matching. We therefore rely on the post-stow instance mask of the new item as the basis for the new-item representation. Particularly, the mask is canonicalized to avoid leaking post-stow pose and location information into the model input. We 

define a canonical pose and location by translating the newitem mask to the center of a fixed-size canvas and rotating it so that its principal axis is upright. The resulting canonical binary mask serves as the new-item observation to FOREST. 

**Clarifications.** Instance-mask extraction and item matching can introduce noisy supervision. We mitigate obvious failures by filtering out stows whose post-stow instance count does not equal the pre-stow count plus one, and by discarding stows whose matches disagree with an automatic consistency check from large vision–language model based on the pre- and post-stow RGB images. In addition, the canonical new-item mask extracted from the ground-truth post-stow bin state is used in both training and evaluation, so that we can isolate the quality of the predicted post-stow layouts under the assumption that an in-bin contact-surface view of the new item is available (see details in Appendix C). 

## **3.3. Input Modeling and Tokenization** 

We now describe how we represent the bin state, the new item, and the stow intent as latent tokens or embeddings that serve as inputs and conditions for the diffusion model. 

**Bin State Tokens.** We construct pre- and post-stow bin state tokens from the slot-based, item-aligned binary masks. We first apply the off-the-shelf VAE encoder on each item slot, independently transforming the multi-channel binary masks into latent feature maps. Then each latent feature map is patchified into a sequence of tokens with 2D positional embeddings to preserve spatial structure within each slot. We further introduce two types of additional embeddings that are added to the token features. 

First, each item slot is associated with a learnable _instance embedding_ , which is added to all tokens originating from 

4 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

that slot so that the model can distinguish different items and track across layers. When training, we randomly shuffle the slots of the pre-existing items, and rely on the instance embeddings to emphasize the one-to-one correspondence. Second, the tokens from pre-stow bin state is associated with a _condition-type embedding_ that indicates whether a token represents a bin state or other conditioning sources. 

We also include tokens generated from the pre-stow RGB image, encoded by the same VAE, patchified into tokens, and augmented with positional and condition-type embeddings, as additional context. This extra stream provides richer visual information about the storage bin (see ablation study in Appendix F). 

**New Item Tokens.** We construct new item tokens from the canonical new-item mask. The processing mirrors that of the bin state tokens with positional and condition-type embeddings. ARMBench also provides discrete item properties, which we encode as a multi-hot vector over six attributes, rigid, round, square, conveyable, foldable, and fragile. This multi-hot vector is embedded into a single property token using a two-layer MLP and is augmented with conditiontype embedding. The contribution of the property token is demonstrated in Appendix F. 

**Stow Intent Embeddings.** The stow intent describes how the robot plans to execute the stow. As discussed in §2, the system follows a vertical, bookshelf-like stowing strategy, and the intent includes the planned position for placing the new item and, when necessary, a sweeping operation used to create additional free space. Both operations are represented as bounding boxes in the bin coordinate frame. Formally, we denote the placement intent by _u_ place _∈_ R<sup>4</sup> and the sweeping intent, when present, by _u_ push _∈_ R<sup>4</sup> , each encoding ( _x_ 1 _, y_ 1 _, x_ 2 _, y_ 2). To condition on the stow intent _u_ = _{u_ place _, u_ push _}_ , we first map each scalar coordinate to a _d/_ 4-dimensional sine–cosine feature, concatenate the four features into a _d_ -dimensional vector, and then apply a twolayer MLP to obtain intent embeddings Ψ _u_ place _,_ Ψ _u_ push _∈_ R<sup>_d_</sup> . We follow a similar procedure to map the diffusion timestep _t ∈_ R to a timestep embedding Ψ _t ∈_ R<sup>_d_</sup> . Finally, we sum all embeddings into a single conditioning vector 


which is used to modulate every transformer block via AdaLN in the diffusion architecture described in §3.4. 

## **3.4. Diffusion-Based World Model Architecture** 

We now describe how the tokens and embeddings are used in a diffusion-based world model that predicts the post-stow bin state in latent space. Our architecture follows the latent diffusion with a transformer backbone with the main design choices lying in how we inject stow context and how we handle variable-length bin layouts. Training and 

sampling follow the conventional noise-prediction objective and denoising procedure used in prior latent diffusion models (Rombach et al., 2022) as described in Appendix B. 

**Conditioning Mechanism.** At each diffusion timestep _t_ , the model operates on two token sequences: (i) the noisy tokens from the diffused post-stow latent, and (ii) the condition tokens, i.e., the pre-stow tokens and the new item tokens. Within each transformer block, we use cross-attention to incorporate these condition tokens into the denoising update. Specifically, the noisy post-stow tokens are used as queries, and all condition tokens are used as keys and values, so that the updated latent representation of each post-stow patch is computed explicitly as a function of the pre-stow bin configuration and the new item. 

To inject intent information, the conditioning vector _ξ_ in Eq. 3 modulates every transformer block through AdaLN (Xu et al., 2019), providing a global signal without introducing additional intent tokens into the attention layers. 

**Varied-Length Attention.** Because different stow events contain different numbers of pre-existing items in pre-stow bins, the number of tokens per stow varies with the number of occupied slots. Naively padding all sequences to the same length would introduce many uninformative tokens and waste computation. Instead, we adopt a packedsequence attention scheme. For a mini-batch of stows, we concatenate all tokens along the slot dimension and construct a block-diagonal attention mask (Dao et al., 2022) that restricts attention to tokens belonging to the same stow. This allows all tokens to be processed in a single batched attention operation, while preserving independence across stows and avoiding padding overhead. 

# **4. Empirical Evaluation** 

## **4.1. Experimental Setup** 

**Datasets.** We conduct all experiments on ARMBench. We retain only successful stow events, so that post-stow bin layouts provide reliable supervision, and group them into two intent modes, **direct insert** , where only insertion is used, and **sweep insert** , where an additional sweeping operation creates free space. For each mode, we randomly split stows into train and test sets with an 8:2 ratio. The resulting counts are reported in Appendix D. 

**Baselines and Comparisons.** To the best of our knowledge, FOREST is the first method to address visual foresight for stow from temporally sparse pre- and post-stow snapshots rather than dense videos. Because there is no existing baseline in this setting, we compare against heuristic baselines and design both direct and downstream evaluations to obtain a comprehensive assessment. The **copy-paste** baseline places the new item mask into the pre-stow bin state at 

5 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

the intended insertion region without modeling interactions with existing items. The **copy-paste with gravity** baseline further applies a vertical settling step that moves the pasted item downward until it hits the bin ground, approximating a simple drop of the new item into the bin. The direct evaluation then compares the synthetic post-stow bin state with the ground-truth in terms of binary instance masks. 

We also ask whether predicted post-stow bin states are useful for downstream tasks. Our first task is **Delta Linear Opportunity (DLO) prediction** , which measures how much usable linear space in the bin changes after a stow. In ARMBench (Hudson et al., 2025), Linear Opportunity (LO) is a scalar that represents the remaining available space in the horizontal direction of the bin in meters, and DLO is the difference between post- and pre-stow LO. In production, observing DLO only after execution is mainly diagnostic, while forecasting DLO for candidate stows can help choose among alternative policies. 

Predicted post-stow layouts are a natural input for such forecasts, since DLO depends on how the bin changes between the pre- and post-stow states. However, if we trained a DLO predictor directly on FOREST outputs, the error would mix the quality of the synthetic masks with the capacity of the DLO model itself. Instead, we train a vision-based DLO predictor on ground-truth post-stow masks (see architecture in Appendix D). The predictor takes as inputs the pre-stow RGB image, pre-stow instance masks, and a post-stow instance mask. During training, this post-stow mask is always the ground-truth one, so the network learns the best achievable mapping from true pre and post states to DLO, independent of any visual foresight method. At test time, we freeze this predictor and keep the pre-stow inputs fixed, but replace the post-stow mask with either the FOREST-predicted mask or the mask from the copy-paste baselines. Differences in DLO prediction accuracy can then be attributed purely to the quality of the synthetic post-stow masks, and thus quantify how well visual foresight can stand in for ground-truth supervision in this downstream task. 

The second downstream task is **multi-stow reasoning** , which evaluates the ability of FOREST to support longhorizon forecasting over multiple stows in the same bin. We link individual stows in ARMBench into chains based on bin identifiers and timestamps, forming 1,581 multi-stow sequences with chain length up to four. Then the visual foresight model is applied sequentially along these chains, where the predicted post-stow bin state from one step becomes the pre-stow bin state for the next. Since FOREST also requires a pre-stow RGB image as input, we synthesize the post-stow RGB image by rendering the new item into the bin using its induct view texture and the predicted mask. The synthesized post-stow RGB image then serves as the pre-stow RGB input for the next stow in the chain. Details 

of this synthesis procedure are in Appendix D. 

We consider two evaluation modes for multi-stow reasoning. In the _rollout_ mode, the predicted post-stow bin state at each step are fed into the next step, so that errors can accumulate over time. In the _teacher forcing_ mode, we instead provide ground-truth pre-stow bin states at every step, without feeding previous predictions forward. 

**Metrics.** For direct evaluation of post-stow bin states, we report instance-level intersection-over-union (IoU) for both the newly inserted item (N-IoU) and pre-existing items (OIoU). And we further perform two fine-grained analyses. We first measure the size of the new item and partition stow events into small, medium, large buckets based on quantiles of the item size distribution and report N-IoU respectively. We also explore performance regarding stow events difficulty. Specifically, we use the N-IoU achieved by the copy-paste baseline as a proxy for how surprising or obvious a stow is. Details of the stow partitions are provided in Appendix D. 

For DLO prediction, we report the mean absolute error (MAE) between the predicted and ground-truth DLO. Using ground-truth post-stow masks gives an upper bound on the achievable performance of the trained DLO predictor, while the increase in MAE when using synthetic post-stow masks measures the loss due to imperfect post-stow predictions. 

In addition, we assess prediction-level agreement via a linear regression between DLO obtained with ground-truth masks and with synthetic masks. For each setting, we fit a line _y_ = _a_ + _bx_ , where _x_ is the DLO predicted using groundtruth post-stow masks and _y_ is the DLO predicted using synthetic masks from either FOREST or the baselines. We report the slope _b_ , the intercept _a_ , and the coefficient of determination _R_<sup>2</sup> , defined as 


where _yi_ is the synthetic-mask DLO prediction, _y_ ˆ _i_ is its regression fit, and _y_ ¯ is the mean of _{yi}_ . The ideal case, where synthetic-mask predictions exactly match groundtruth–based predictions, would have _a_ = 0, _b_ = 1, and _R_<sup>2</sup> = 1. 

For multi-stow reasoning, we report N-IoU at each step under both teacher-forcing and rollout modes, and use their gap as a measure of accumulated error over longer horizons. 

**FOREST Settings.** FOREST has 50M parameters and we evaluate two variants. **FOREST-DI** and **FOREST-SI** are trained separately on direct-insert and bin-sweep stows, while **FOREST-J** is trained jointly on both modes. In the joint setting, the architecture adapts to different stow intents through the intent-conditioned AdaLN layers described in §3.4. The models are evaluated with 50 denoising steps. 

6 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

## **4.2. Direct Evaluation** 

**Quantitative Results.** Table 1 summarizes instance-level IoU between predicted and ground-truth post-stow bin states. Overall, FOREST markedly improves N-IoU over copypaste baselines in both stow modes. On direct insert, N- IoU rises from 0 _._ 28–0 _._ 36 for copy-paste to about 0 _._ 70 for FOREST-DI and FOREST-J, while on sweep insert it increases from 0 _._ 12–0 _._ 22 to 0 _._ 62–0 _._ 64. 

We highlight two observations. First, small items are intrinsically harder to predict, since even a minor spatial deviation leads to a large drop in IoU. This is reflected in the baselines, whose N-IoU for small items is only 0 _._ 11 for direct insert and 0 _._ 05 for sweep insert. Despite this difficulty, FOREST attains N-IoU above 0 _._ 5 for small items in both scenarios, and further improves to around 0 _._ 73–0 _._ 80 for medium and large items. Second, the difficulty-based breakdown clarifies FOREST’s advantage in solving hard cases. For surprising stows, where copy-paste often fails with N-IoU near zero, FOREST raises N-IoU to around 0 _._ 56–0 _._ 61, while maintaining competitive performance on the obvious stows. 

Besides, for pre-existing items, the heuristic baselines are able to achieve high O-IoU, which is consistent with the stow process. In direct insert, pre-existing items are rarely disturbed, and even when a sweeping operation is present, their relative ordering and approximate positions remain stable. In such cases, simple copy-paste can already reproduce much of the pre-existing layout. Nevertheless, FOREST matches or slightly improves O-IoU while delivering much larger gains on N-IoU. 

**Visualizations.** Figure 4 illustrates two stow events with predicted post-stow bin states (see more visualizations in Appendix E). Compared to the copy-paste with gravity baseline, FOREST better captures the underlying world dynamics of the stow. For instance, in the direct-insert case, where the new item is tall and unstable, FOREST successfully predicts the item tipping and coming to rest against existing objects, in agreement with the ground truth. And in the bin-sweep example, where the sweeping operation shifts multiple pre-existing items to make room for the new item, FOREST anticipates both the displacement of old items and the final resting pose of the new item. These results indicate that FOREST goes beyond learning a static placement heuristic and acquires a useful modeling of how stow actions reconfigure the bin. 

## **4.3. Downstream Evaluations** 

**Delta Linear Opportunity (DLO) Prediction.** We first study DLO prediction and compare the DLO predictor’s performance when driven by different post-stow masks. 

Table 2 reports the MAE between the predicted and groundtruth DLO under three choices of post-stow masks at test 

_Table 1._ IoU between the predicted and the ground-truth post-stow bin states in instance-mask space. We report N-IoU for the newly inserted item and O-IoU for pre-existing items, along with finegrained N-IoU analysis by new-item size and stow difficulty. 

|Mode|Metric|Copy-Pas|te<br>Copy-Paste<br>+ Gravity|FOREST-DI<br>/ FOREST-SI|FOREST-J|
|---|---|---|---|---|---|
||||<br>_Overall_|||
||N-IoU|0.2846|0.3632|0.7017|**0.7021**|
||O-IoU|0.8563|0.8563|**0.8550**|0.8536|
|Direct|||_N-IoU by item s_|_ize_||
|It||||||
|nser|Small|0.1076|0.2284|**0.5771**|0.5745|
||Medium|0.2920|0.3766|0.7263|**0.7311**|
||Large|0.4544|0.4849|**0.8021**|0.8010|
||||_N-IoU by difficu_<br>|_ilty_<br>||
||Surprises|0.0079|0.1034|**0.5623**|0.5569|
||Non-obvious|0.3138|0.3980|0.7354|**0.7379**|
||Obvious|0.6996|0.7069|**0.7920**|**0.7920**|
||||_Overall_|||
||N-IoU|0.1214|0.2167|0.6166|**0.6422**|
||O-IoU|0.5287|0.5287|0.6878|**0.6906**|
|Bin<br>|||_N-IoU by item s_|_ize_||
|Sweep|Small|0.0457|0.1502|0.4791|**0.5108**|
||Medium|0.1212|0.2270|0.6276|**0.6521**|
||Large|01974|02732|07434|**0.7641**|
|||.|.<br>_N-IoU by difficu_|.<br>_ilty_||
||Surprises|0.0065|0.0857|0.5855|**0.6117**|
||Non-obvious|0.2181|0.3332|0.6483|**0.6737**|
||Obvious|0.6922|**0.7201**|0.6394|0.6561|


_Table 2._ MAE between predicted and ground-truth DLO when using ground-truth (GT), copy-paste with gravity (CP+G), or FOREST-predicted post-stow masks. 

|Stow Intent||Direct Inse|rt||Sweep Ins|ert|
|---|---|---|---|---|---|---|
|Post Mask|GT|CP + G|FOREST|GT|CP + G|FOREST|
|DLO MAE|**0.0168**|0.0225|0.0184|**0.0255**|0.0353|0.0280|
|- GT|-|0.0057|**0.0016**|-|0.0098|**0.0025**|


time, ground-truth (GT), copy-paste with gravity (CP+G), and FOREST-predicted. Using GT post-stow masks gives the best achievable MAE for the trained DLO predictor, 0 _._ 0168 for direct insert and 0 _._ 0255 for sweep insert. Replacing GT masks with CP+G masks substantially increases the error for about 0 _._ 0057 and 0 _._ 0098 in the two modes, reflecting the limitations of the heuristic post-stow layouts. In contrast, using FOREST masks increases MAE by only 0 _._ 0016 and 0 _._ 0025, reducing the additional error by roughly 70% compared to CP+G. 

Figure 5 provides the linear regression between DLO predictions obtained with GT post-stow masks and those obtained with synthetic masks. Under CP+G, the slopes are noticeably below one and _R_<sup>2</sup> drops to even 0 _._ 37 in sweep insert, indicating that CP+G-based predictions deviate substantially from GT-based predictions, especially in the more challenging bin-sweep mode. With FOREST masks, the slopes move much closer to one and _R_<sup>2</sup> increases to 0 _._ 83 and 0 _._ 68. Together with Table 2, these trends show that DLO predictions based on FOREST-predicted post-stow masks closely imitate those derived from ground-truth masks. 

7 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 


_Figure 4._ Examples of post-stow bin state prediction (1st row: direct insert, 2nd row: sweep insert). 


_Figure 5._ Linear regression between DLO predictions obtained with ground-truth (GT) post-stow masks and those obtained from copy-paste with gravity (CP+G) or from FOREST. 

**Multi-Stow Reasoning.** We next show that the learned world model can be rolled out over multiple stows in the same bin. Figure 6 reports N-IoU as a function of the step index in the multi-stow chain. Both the joint model, FORESTJ, and the intent-specific models, FOREST-DI and FORESTSI, start from single-step N-IoU around 0 _._ 7 at step 1 and remain around 0 _._ 4 at step 4, whereas the copy-paste-withgravity (CP+G) baseline quickly degrades below 0 _._ 2 after step 3. These results indicate that FOREST ’s predicted post-stow masks can be composed across several stows to support multi-step foresight. 

We plot both teacher-forcing and rollout modes to examine how prediction errors accumulate over multiple stows. Under teacher forcing, each step is evaluated from the groundtruth pre-stow state, so errors do not propagate across time. The mild downward trend mainly reflects that later steps occur in more cluttered, higher fill-level bins, which are intrinsically harder to predict. Under rollout, the model instead consumes its own predicted post-stow masks and synthesized RGB as inputs, so small errors at early steps 

are fed back and amplified over time, widening the gap between the two curves as the horizon grows. Per-step N- IoU numbers and additional visualizations are provided in Appendix E. 

To rule out the synthesized RGB as a confounding factor, we additionally evaluate a rollout-style setting that keeps the pre-stow RGB real at every step while still feeding predicted post-stow masks forward. The resulting curve is nearly identical to full rollout, indicating that the degradation is primarily driven by accumulated mask errors rather than RGB synthesis (see Appendix Figure 10). 


_Figure 6._ N-IoU of predicted post-stow states along multi-stow chains. CP+G: the copy-paste-with-gravity baseline. 

# **5. Conclusion** 

We presented FOREST, a stow-intent-conditioned world model for robotic stow that operates on real production data. By representing bin states as item-aligned instance masks and applying a latent diffusion transformer conditioned on the new item and stow intent, FOREST predicts structured post-stow layouts that closely match those observed in practice. Direct evaluation shows that FOREST improves the geometric agreement between predicted and ground-truth post-stow bin states over heuristic baselines. Downstream evaluations further show that substituting ground-truth poststow masks with FOREST predictions leads to only modest degradation in load-quality prediction and multi-stow forecasting, suggesting that such world models can provide useful foresight signals for stow-related decision making. The limitations of FOREST are discussed in Appendix G. 

8 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning and Robotics. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

# **References** 

- Jan 2026. URL https://en.wikipedia.org/ wiki/Claude_(language_model). 

- Alonso, E., Jelley, A., Micheli, V., Kanervisto, A., Storkey, A. J., Pearce, T., and Fleuret, F. Diffusion for world modeling: Visual details matter in atari. _Advances in Neural Information Processing Systems_ , 37:58757–58791, 2024. 

- Bar, A., Zhou, G., Tran, D., Darrell, T., and LeCun, Y. Navigation world models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 15791– 15801, 2025. 

- Basu, G., Jiang, Y., and Saxena, A. Learning to place objects: Organizing a room. In _2012 IEEE International Conference on Robotics and Automation_ , pp. 3545–3546. IEEE, 2012. 

- Chen, H., Niu, Y., Hong, K., Liu, S., Wang, Y., Li, Y., and Driggs-Campbell, K. R. Predicting object interactions with behavior primitives: An application in stowing tasks. In _7th Annual Conference on Robot Learning_ , 2023. 

- Corbato, C. H., Bharatheesha, M., Van Egmond, J., Ju, J., and Wisse, M. Integrating different levels of automation: Lessons from winning the amazon robotics challenge 2016. _IEEE Transactions on Industrial Informatics_ , 14 (11):4916–4926, 2018. 

- Correll, N., Bekris, K. E., Berenson, D., Brock, O., Causo, A., Hauser, K., Okada, K., Rodriguez, A., Romano, J. M., and Wurman, P. R. Analysis and observations from the first amazon picking challenge. _IEEE Transactions on Automation Science and Engineering_ , 15(1):172–188, 2016. 

- Cosgun, A., Hermans, T., Emeli, V., and Stilman, M. Push planning for object placement on cluttered table surfaces. In _2011 IEEE/RSJ international conference on intelligent robots and systems_ , pp. 4627–4632. IEEE, 2011. 

- Dao, T., Fu, D. Y., Ermon, S., Rudra, A., and R’e, C. Flashattention: Fast and memory-efficient exact attention with io-awareness. _ArXiv_ , abs/2205.14135, 2022. 

- Ebert, F., Finn, C., Dasari, S., Xie, A., Lee, A., and Levine, S. Visual foresight: Model-based deep reinforcement learning for vision-based robotic control. _arXiv preprint arXiv:1812.00568_ , 2018. 

- Finn, C. and Levine, S. Deep visual foresight for planning robot motion. In _2017 IEEE international conference on robotics and automation (ICRA)_ , pp. 2786–2793. IEEE, 2017. 

- Gao, S., Yang, J., Chen, L., Chitta, K., Qiu, Y., Geiger, A., Zhang, J., and Li, H. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Advances in Neural Information Processing Systems_ , 37: 91560–91596, 2024. 

- Ha, D. and Schmidhuber, J. Recurrent world models facilitate policy evolution. _Advances in neural information processing systems_ , 31, 2018. 

- Hafner, D., Lillicrap, T., Ba, J., and Norouzi, M. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019a. 

- Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H., and Davidson, J. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pp. 2555–2565. PMLR, 2019b. 

- Huang, Y., Zhang, J., Zou, S., Liu, X., Hu, R., and Xu, K. Ladi-wm: A latent diffusion-based world model for predictive manipulation. _arXiv preprint arXiv:2505.11528_ , 2025. 

- Hudson, N., Hooks, J., Warrier, R., Salisbury, C., Hartley, R., Kumar, K., Chandrashekhar, B., Birkmeyer, P., Tang, B., Frost, M., Thakar, S., Piaskowy, T., Nilsson, P., Petersen, J., Doshi, N., Slatter, A., Bhatia, A., Meeker, C., Xue, Y., Cox, D., Kyriazis, A., Lou, B., Hasan, N., Rana, A., Chacko, N., Xu, R., Faal, S., Seraj, E., Agrawal, M., Jamieson, K., Bisagni, A., Samzun, V., Fuller, C., Keklak, A., Frenkel, A., Ratliff, L., and Parness, A. Stow: Robotic packing of items into fabric pods. _arXiv preprint arXiv:2505.04572_ , 2025. 

- Kuhn, H. W. The hungarian method for the assignment problem. _Naval research logistics quarterly_ , 2(1-2):83– 97, 1955. 

- Li, F., Zhang, H., xu, H., Liu, S., Zhang, L., Ni, L. M., and Shum, H.-Y. Mask dino: Towards a unified transformerbased framework for object detection and segmentation, 2022. 

- Morrison, D., Tow, A. W., Mctaggart, M., Smith, R., KellyBoxall, N., Wade-Mccue, S., Erskine, J., Grinover, R., Gurman, A., Hunn, T., et al. Cartman: The low-cost cartesian manipulator that won the amazon robotics challenge. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pp. 7757–7764. IEEE, 2018. 

9 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H. V., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., El-Nouby, A., Howes, R., Huang, P.-Y., Xu, H., Sharma, V., Li, S.-W., Galuba, W., Rabbat, M., Assran, M., Ballas, N., Synnaeve, G., Misra, I., Jegou, H., Mairal, J., Labatut, P., Joulin, A., and Bojanowski, P. Dinov2: Learning robust visual features without supervision, 2023. 

- Park, K., Kulick, J., Melkozerov, A., Vilagrasa, R. A., Lembono, T. S., Neubauer, V., Minichev, A., Turner, K., Agrigoroaiei, O., Klink, P., et al. Vulcan pick: A robotic system for picking targeted objects from fabric pods. 2025. 

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P., and Ommer, B. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 10684–10695, 2022. 

- Sohl-Dickstein, J., Weiss, E., Maheswaranathan, N., and Ganguli, S. Deep unsupervised learning using nonequilibrium thermodynamics. In _International conference on machine learning_ , pp. 2256–2265. PMLR, 2015. 

- Stability AI. sd-vae-ft-mse. URL https: //huggingface.co/stabilityai/ sd-vae-ft-mse. 

- Xie, A., Ebert, F., Levine, S., and Finn, C. Improvisation through physical understanding: Using novel objects as tools with visual foresight. _arXiv preprint arXiv:1904.05538_ , 2019. 

- Xu, J., Sun, X., Zhang, Z., Zhao, G., and Lin, J. Understanding and improving layer normalization. _Advances in neural information processing systems_ , 32, 2019. 

- Yang, Y., Wu, X., He, T., Zhao, H., and Liu, X. Sam3d: Segment anything in 3d scenes. _arXiv preprint arXiv:2306.03908_ , 2023. 

10 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

# **A. Related Work** 

**Robotic Stow Task.** Robotic object placement has been studied in several settings, including clearing space in cluttered scenes (Cosgun et al., 2011), using semantic cues for in-home manipulation (Basu et al., 2012), and predicting object motion and stability when placing items on shelves (Chen et al., 2023). The last line of work explicitly formulates a _stow_ task, where a robot relocates an object from a table to a cluttered shelf, closely mirroring one of the core activities in warehouse operations. The 2015–2017 Amazon Robotics Challenges (Corbato et al., 2018; Correll et al., 2016; Morrison et al., 2018) further emphasized this setting by requiring teams to pick diverse items from a source tote and stow them onto shelves or into other containers. More recently, industrial research has moved beyond challenge-style demonstrations toward deployed systems in real fulfillment centers (Hudson et al., 2025). The associated ARMBench benchmark provides large-scale perception data from production workcells in Amazon warehouses, capturing diverse objects and cluttered container configurations. Our work is complementary to these systems-oriented efforts. Whereas prior work focuses on building and evaluating end-to-end stow hardware and control stacks in production (Hudson et al., 2025), we study visual foresight for the stow task, aiming to predict post-stow bin layouts in this real production setting. 

**Visual Foresight.** Visual foresight (Finn & Levine, 2017) refers to learning predictive models that anticipate future visual observations conditioned on current images and candidate actions, and then using these predictions for planning. Early work in this area developed action-conditioned video prediction models for robot manipulation, where a convolutional network predicts future frames given past images and a sequence of actions, and downstream control chooses actions that lead predicted pixels to desired goal locations or goal images (Finn & Levine, 2017; Ebert et al., 2018). These visual model-predictive control methods showed that self-supervised video prediction can support nonprehensile manipulation and generalize to novel objects and tasks, and were later extended to more complex settings such as tool use (Xie et al., 2019). However, they typically assume dense frame observations and are designed around tabletop manipulation scenarios rather than real warehouse stow in the cluttered environment. 

**World Models.** Within reinforcement learning, visual foresight can be viewed as a special case of learning a _world model_ (Ha & Schmidhuber, 2018), i.e., a generative model of environment dynamics that predicts future observations and rewards conditioned on current state and actions. Typical world models employ recurrent neural networks and convolution networks to learn compact latent dynamics and then perform planning or policy learning in that latent space (Ha & Schmidhuber, 2018; Hafner et al., 2019b;a). More recently, diffusion models have been adopted as expressive world models that can better capture multi-modal interactions and fine-grained visual details. For instance, DIAMOND introduces a diffusion-based world model for Atari, showing that modeling environment with diffusion improves visual fidelity and in turn agent performance on Atari 100k benchmarks (Alonso et al., 2024). In robotic manipulation, LaDi-WM (Huang et al., 2025) proposes a latent diffusion world model on top of pre-trained visual foundation model features, and finds that predicting the evolution of such latent representations yields accurate future states and substantially improves policy performance in manipulation benchmarks. 

Our work extends diffusion-based world models to a distinct problem, i.e., visual foresight for warehouse stow in real production systems. In contrast to prior visual foresight and world-model approaches that typically predict dense video sequences or multi-step trajectories in laboratory environments, we study single-step transitions between pre- and post-stow snapshots observed only as temporally sparse RGB images. The objective is to anticipate how a storage container will be reconfigured after executing a stow, conditioned on the current snapshot, the new item, and the stow intent. 

# **B. Diffusion Models Basis** 

We begin by recalling the _forward_ diffusion process. Given a data point sampled from the real data distribution _x_ 0 _∼ q_ ( _x_ ), the forward process progressively corrupts _x_ 0 into a noisy variable _xT_ through _T_ steps of Gaussian noise addition. In the commonly used variance-preserving formulation, this process admits a closed-form expression: 


where _{α_ ¯ _t}_<sup>_T_</sup> _t_ =1<sup>is a deterministic noise schedule with</sup><sup>_α_¯</sup><sup>_t_= �</sup><sup>_t_</sup> _i_ =1<sup>(1</sup><sup>_−βi_),</sup><sup>_βi∈_(0</sup><sup>_,_1) controls the amount of noise added at</sup> step _i_ , and _ε ∼N_ ( **0** _,_ **I** ). As _t_ increases, the influence of _x_ 0 vanishes and _xT_ converges to isotropic Gaussian noise. 

To turn this noising process into a generative model, diffusion models learn an approximate _reverse_ process that reconstructs samples from noise back to data. A neural network _εθ_ ( _xt, t_ ) is trained to predict the injected noise _ε_ given a noisy sample _xt_ and a timestep embedding _t_ . The standard training objective is 


**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

which encourages _εθ_ to recover the noise that produced _xt_ from _x_ 0. At inference time, one initializes _xT_ from a standard Gaussian and iteratively applies the reverse process parameterized by _εθ_ to obtain a synthetic sample _x_ ˆ0 from the learned distribution. 

# **C. FOREST Details** 

**About Item Matching.** In §3.2, we describe the item matching procedure which is designed to construct slot-based, item-aligned bin states. Specifically, we formulate item matching as a Hungarian matching problem with priors derived from the stow behavior, in which the cost function is defined as, 


where _Dij_ is pairwise cosine similarity between instance visual embeddings, and Φpos and Φord encode the placement and order-preservation penalties, respectively. We solve the linear assignment problem defined by _Cij_ using the Hungarian algorithm to obtain the final one-to-one correspondence between pre- and post-stow instances. For completeness, we describe the concrete form of the placement and order-preservation penalties used in the matching cost. 

_Position Prior._ Let _{m_<sup>pre</sup> _i_<sup>_}N_</sup> _i_ =1<sup>preand</sup><sup>_{m_post</sup> _j }_<sup>_N_</sup> _j_ =1<sup>postdenote the instance masks in the pre- and post-stow snapshots, respectively,</sup> and let _c_<sup>post</sup> _j ∈_ R<sup>2</sup> be the center of the _j_ -th post-stow instance (e.g., the center of its bounding box), and _p_ ins _∈_ R<sup>2</sup> and _p_ push _∈_ R<sup>2</sup> denote that of the planned insertion and sweeping positions from the stow intent. We first compute a distance to the intended placement region, 


where the term involving _p_ push is omitted if no sweeping is performed. We then convert this distance into a penalty 


where _σ_ pos controls the spatial decay. This term penalizes matching pre-existing items to post-stow instances that lie very close to the intended insertion region, which are more likely to be the newly stowed item. 

_Order-Preservation Prior._ Let _x_<sup>pre</sup> _i_ and _x_<sup>post</sup> _j_ denote the normalized horizontal coordinates of the pre- and post-stow instances (e.g., the centers normalized to [0 _,_ 1] along the bin width). We obtain left-to-right ranks _ri_<sup>pre</sup> and _rj_<sup>post</sup> by sorting instances by _x_ , and normalize them to [0 _,_ 1], 


The order-preservation penalty for a candidate match ( _i, j_ ) is then 


which discourages assignments that significantly change the left–right order of pre-existing items. When only one item is in the pre-stow state, the order-preservation prior will be skipped. 

**More Clarifications.** We clarify two practical aspects of the data processing steps introduced in §3.2. 

First, both the instance mask extraction and the item matching procedure are imperfect and can introduce noise into the supervision. Quantifying this noise would require ground-truth instance masks and correspondences, which is infeasible to obtain at scale. Instead, we apply simple post-processing to suppress obvious errors. For each stow event, the number of post-stow instances must equal the number of pre-stow instances plus one. If this constraint is violated, we discard the stow as a likely failure of the instance segmentation step. For the remaining stows, we further audit the one-to-one matching with a large vision-language model, Claude-3.7 (cla, 2026) in a visual question answering setup, which inspects the pre- and post-stow RGB images and judges whether the proposed correspondences are consistent. Some residual noise may remain, and we treat it as label noise in the training data. 

Second, the canonical new-item mask extracted from the ground-truth post-stow masks is used in both training and evaluation. This choice reflects our focus on evaluating how well the model can predict post-stow layouts when given the in-bin contact-surface view of the new item. In ARMBench, only an induct-view image of the new item is available, which 

12 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

does not directly correspond to the surface that faces outward once the item is placed in the bin. Using the canonical mask derived from ground-truth post-stow masks therefore serves as a proof-of-concept proxy for this view. When targeting for a real deployed system, one could obtain the required view by adding a camera that observes the item surface that will face outward in the bin, or by learning a separate model that predicts this view from the induct observation, for example via 3D reconstruction (Yang et al., 2023). Designing such a module is beyond the scope of this work and we leave it to future research. 

# **D. More Experimental Settings** 

**About Dataset Statistics.** Table 3 summarizes the data statistics. As described in §4.1, we focus on successful stow events in ARMBench and group them by stow intent into two modes. _Direct insert_ only execute an insertion action, and _sweep insert_ uses an additional sweeping action to create space. Within each mode we randomly split stows into training and test sets using an 8:2 ratio. 

_Table 3._ Dataset statistics 

|Intent|Direct|Insert|Sweep|Insert|
|---|---|---|---|---|
|Sli|Train|Test|Train|Test|
|pt|26,531|6,558|20,678|5,350|


**About the Downstream Evaluations.** Here we provide additional details for the two downstream evaluations, Delta Linear Opportunity (DLO) prediction and multi-stow reasoning. 

For DLO prediction, we train a vision-based DLO predictor that takes as input the pre-stow bin RGB image, the pre-stow instance masks, and a candidate post-stow instance mask. Each of the three inputs is encoded separately by a frozen DINOv2 backbone (Oquab et al., 2023), yielding three sets of tokens. We then add a learnable input-type embedding to the tokens from each stream so that the model can distinguish them, and concatenate all tokens along the sequence dimension. A learnable class token is further concatenated to this sequence and passes through two transformer blocks with self-attention, which fuse information across all inputs. Finally, the class token output is fed to a small MLP head that produces a single scalar, the predicted DLO. This predictor is trained with ground-truth post-stow masks so that it learns the best achievable mapping from the combination of pre-stow state and true post-stow state to DLO, and the post-stow mask is only swapped at test time when comparing different synthetic post-stow state. 

For multi-stow reasoning, FOREST requires a pre-stow RGB image at each step, but only the first pre-stow RGB is directly available. To obtain RGB inputs for later steps, we synthesize post-stow RGB images from the predicted post-stow masks. Specifically, we first extract the item texture from its induct RGB view provided in ARMBench by segmenting out the new item and removing its background. Given a predicted post-stow mask for the new item in the bin, we then paste this texture into the pre-stow RGB image at the mask location, producing a synthetic post-stow RGB image. This synthesized image serves as the pre-stow RGB input for the next stow in the chain during multi-stow rollout. 

**About Fine-Grained IoU Analysis.** For the fine-grained IoU analysis in §4.2, we further partition test stows along two axes, the size of the newly inserted item and the difficulty of the stow derived from the copy-paste baseline. 


_Figure 7._ Fined-grained IoU partition according to the normalized new item size (left) and the difficulty of the stow events derived from the performance of the copy-paste baseline (right) for (a) direct insert and (b) sweep insert modes respectively. 

For the size buckets, we measure the normalized new-item size as the area of the new-item mask divided by the bin area in the stow view. Within each stow mode , we compute the 1 _/_ 3 and 2 _/_ 3 quantiles of this normalized size distribution. Stows with size below the first quantile are labeled small, those between the first and second quantiles are medium, and those above the second quantile are large. This evenly spaced quantile partition yields three groups of comparable size and isolates very small items, for which IoU is particularly sensitive to small spatial errors. The left plots in Figure 7 visualize this partition, along with the number of stows in each bucket. 

For the difficulty buckets, we instead threshold the N-IoU achieved by the copy-paste baseline. We run this naive baseline on all test stows and collect its N-IoU scores. Within each stow mode, stows are then grouped by these scores into three difficulty levels. Specifically, stows with baseline N-IoU below 0 _._ 05 are surprising cases, where the naive copy-paste rarely 

13 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

places the new item correctly and often yields near-zero overlap. Stows with N-IoU between 0 _._ 05 and 0 _._ 60 are non-obvious cases, where the baseline achieves partial overlap but still leaves room for improvement. Finally, stows with N-IoU above 0 _._ 60 are labeled obvious cases, where the simple strategy already performs well. The right plots in Figure 7 show the N-IoU histograms and the counts in each difficulty bucket. 

# **E. More Visualizations** 

**Single-Step Stow.** Figure 8 and Figure 9 provide additional single-step qualitative examples for direct insert and sweep insert stows. Each row shows one stow event, with columns corresponding to pre-stow RGB, pre-stow bin state with stow intent, new item mask, post-stow RGB, ground-truth post-stow bin state, copy-paste with gravity, and FOREST-J predictions. In the two visualizations, we select representative stows from the small, medium, and large new-item size buckets and from the surprise, non-obvious, and obvious difficulty groups. FOREST-J consistently produces post-stow layouts that closely align with the ground-truth masks, while copy-paste with gravity often misses item tipping, sliding, or coordinated motion of pre-existing items. 


_Figure 8._ More examples of post-stow bin state prediction for **direct insert** stow events. Representatives are selected from stows with small, medium, large item or surprise, non-obvious, obvious stow events. 

**Multi-Step Stow.** Table 4 reports per-step N-IoU of predicted post-stow masks along multi-stow chain. For the copypaste-with-gravity (CP+G) baseline, N-IoU drops quickly below 0 _._ 2 from step 3 onward, showing that this heuristic cannot support long-horizon rollouts. In contrast, both FOREST-DI+FOREST-SI and FOREST-J maintain much higher N-IoU under rollout, and their teacher-forcing curves stay relatively stable across steps. The gap between teacher-forcing and 

14 

### **Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 


_Figure 9._ More examples of post-stow bin state prediction for **sweep insert** stow events. Representatives are selected from stows with small, medium, large item or surprise, non-obvious, obvious stow events. 

## rollout therefore reflects accumulated prediction error. 

One concern in the rollout evaluation is that the synthesized pre-stow RGBs may also introduce error, which could confound the analysis of error accumulation from the predicted post-stow masks. To isolate this effect, we run an additional multi-stow experiment where we keep the pre-stow RGB images _real_ at every step, but feed the _predicted_ post-stow masks from FOREST-J as the bin-state input for the next step. Figure 10 compares three settings, (i) rollout with synthetic RGB and predicted masks, (ii) teacher forcing with real RGB and ground-truth masks, and (iii) rollout-style evaluation with real RGB and predicted masks. The curves for (i) and (iii) are almost identical across steps, while both remain clearly below (ii), indicating that the degradation comes primarily from accumulating errors in the predicted masks rather than from the synthesized RGB. 

Figures 11 to 16 provide additional visualizations. Each figure shows one multi-stow chain, with one row per stow step. From left to right, we display the ground-truth pre-stow RGB image, the synthesized pre-stow RGB image used as input to the next step, the ground-truth post-stow RGB image, the ground-truth post-stow mask, and the FOREST-J predicted post-stow mask. These examples include both typical successes, where the model tracks how items accumulate and reconfigure over several stows, and failure cases, where unstable items lead to larger drift in the rolled-out predictions (Figures 15 and 16). 

15 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

_Table 4._ N-IoU of predicted post-stow masks along multi-stow chains (table version of Figure 6). We compare FOREST-J and the intent-specific models, FOREST-DI+FOREST-SI, under teacher-forcing and rollout modes, together with the copy-paste-with-gravity (CP+G) baseline. The number of stows for each step are included as reference. 

|Multi-<br>Step|Step Chain<br>Count|CP + G|N-IoU<br>FOREST-DI + FOREST-SI (Rollout)<br>FOREST-DI + FOREST-SI (Teacher-Forcing)|FOREST-J (Rollout)|FOREST-J (Teacher-Forcing)|
|---|---|---|---|---|---|
|1|1581|0.2868|0.6934<br>0.6911|0.6992|0.6993|
|2|1581|0.2353|0.6069<br>0.6478|0.6211|0.6606|
|3|189|0.2|0.4755<br>0.5590|0.4980|0.5810|
|4|16|0.1393|0.4458<br>0.5773|0.3871|0.5471|


_Figure 10._ We compare N-IoU along multi-stow chains under three settings for FOREST-J: rollout with synthetic RGB and predicted masks, teacher forcing with real RGB and ground-truth masks, and rollout-style evaluation with real RGB and predicted masks. 


_Figure 11._ Multi-step stow examples (Ex.1). Each row is one stow in a chain and each column shows, from left to right: ground-truth pre-stow RGB, synthesized pre-stow RGB, ground-truth post-stow RGB, ground-truth post-stow mask, and FOREST-J predicted post-stow mask. In the post-stow mask, the red mask represents the new item, while the green one are pre-existing items. 

16 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 


_Figure 12._ More multi-step stow examples (Ex.2). 


_Figure 13._ More multi-step stow examples (Ex.3). 

17 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 


_Figure 14._ More multi-step stow examples (Ex.4; long chain case with last step not accurate). 


_Figure 15._ More multi-step stow examples (Ex.5; failure case). 

18 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 


_Figure 16._ More multi-step stow examples (Ex.6; failure case). 

19 

**Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots** 

# **F. Ablation Study on Conditions** 

We ablate the conditioning signals used by FOREST, namely the pre-stow RGB image and the item property token, on direct insert stow events. Table 5 reports N-IoU and O-IoU, together with fine-grained N-IoU by item size and stow difficulty. Overall, removing either signal degrades performance, and removing both yields the largest drop. N-IoU falls from 0 _._ 701 to 0 _._ 579 without RGB, to 0 _._ 661 without the property token, and to 0 _._ 509 when both are removed. The degradation is especially pronounced for small and difficult stows, suggesting that these challenging cases benefit most from richer conditioning. 

_Table 5._ Ablation on conditioning signals for FOREST-DI on _direct insert_ stows. We report N-IoU for the newly inserted item and O-IoU for pre-existing items, together with fine-grained N-IoU by new-item size and stow difficulty. 

|**F**|**OREST-DI **|**w/o RGB **|**w/o Prop **|**w/o RGB + Prop**|
|---|---|---|---|---|
|||_Overall_|||
|N-IoU|**0.7017**|0.5799|0.6619|0.5089|
|O-IoU|**0.8550**|0.8232|0.8321|0.7675|
||_N-I_|_oU by item_|_size_||
|Small|**0.5771**|0.4549|0.5215|0.3799|
|Medium|**0.7263**|0.6093|0.6881|0.5311|
|Large|**0.8021**|0.6756|0.7764|0.6158|
||_N-I  i_|_oU by diffic_|_iulty_||
|Surprises|**0.5623**|0.4238|0.5042|0.3448|
|Non-obvious|**0.7354**|0.6186|0.7004|0.5468|
|Obvious|**0.7920**|0.6745|0.7619|0.6257|


# **G. Limitations** 

This work has several limitations. FOREST focuses on single-step transitions and mask-based bin states, leaving richer visual channels and multi-step training for future exploration. Moreover, due to limitations of ARMBench, our new-item representation relies on a canonical mask extracted from the ground-truth post-stow view rather than a true contact-surface view. Reproducing FOREST using contact surfaces derived from induct views is an important next step to better match deployment conditions. Addressing these limitations and coupling FOREST more tightly with stow policy learning and planning are promising directions for future work. 

20 

