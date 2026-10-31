---
title: "RopeDreamer: A Kinematic Recurrent State Space Model for Dynamics of Flexible Deformable Linear Objects"
date: "2026-04-30"
authors: "Tim Missal; Lucas Domingues; Berk Guler; Simon Manschitz; Jan Peters; Paula Dornhofer Paro Costa"
url: https://arxiv.org/abs/2604.28161
pdf: https://arxiv.org/pdf/2604.28161
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.28161)** / [論文ページ](https://arxiv.org/abs/2604.28161)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RopeDreamer: A Kinematic Recurrent State Space Model for Dynamics of Flexible Deformable Linear Objects** 

Tim Missal<sup>_⋆_†1</sup> , Lucas Domingues<sup>_⋆_2</sup><sup>_,_3</sup> , Berk Guler<sup>1</sup><sup>_,_4</sup> , Simon Manschitz<sup>4</sup> , Jan Peters<sup>1</sup><sup>_,_5</sup><sup>_−_8</sup> , Paula Dornhofer Paro Costa<sup>2</sup><sup>_,_9</sup> 


Fig. 1. After observing an initial state _s_ 0 from simulation, RopeDreamer predicts the following evolution of the Deformable Linear Object given a sequence of actions _u_ 0: _T_ . 

**_Abstract_ — The robotic manipulation of Deformable Linear Objects (DLOs) is a fundamental challenge due to the highdimensional, non-linear dynamics of flexible structures and the complexity of maintaining topological integrity during contact-rich tasks. While recent data-driven methods have utilized Recurrent and Graph Neural Networks for dynamics modeling, they often struggle with self-intersections and nonphysical deformations, such as tangling and link stretching. In this paper, we propose a latent dynamics framework that combines a Recurrent State Space Model with a Quaternionic Kinematic Chain representation to enable robust, long-term forecasting of DLO states. By encoding the DLO as a sequence of relative rotations (quaternions) rather than independent Cartesian positions, we inherently constrain the model to a physically valid manifold that preserves link-length constancy.** 

> _⋆_ Equal contribution; † Part of this work was performed during an exchange at UNICAMP<sup>1</sup> Technical University of Darmstadt<sup>2</sup> School of Electrical and Computer Engineering, Universidade Estadual de Campinas (UNICAMP), Brazil 3Instituto de Pesquisas Eldorado, Brazil 4Honda Research Institute Europe GmbH<sup>5</sup> German Research Center for Artificial Intelligence (DFKI) 6hessian.AI 7Robotics Institute Germany (RIG) 

> 8Centre for Cognitive Science 9Artificial Ingelligence Lab, Recod.ai; Corresponding authors: tim.missal@stud.tu-darmstadt.de, lucas.domingues@eldorado.org.br 

This work was partially funded by the Coordenac¸˜ao de Aperfeic¸oamento de Pessoal de N´ıvel Superior – Brasil (CAPES) – Finance Code 001, by the S˜ao Paulo Research Foundation (FAPESP) under grant #2020/09838-0 (BI0S - Brazilian Institute of Data Science), and by the Ministry of Science, Technology, and Innovations, with resources from Law No. 8.248, of October 23, 1991, under the PPI-SOFTEX program, DOU 01245.003479/202410. 

**Furthermore, we introduce a dual-decoder architecture that decouples state reconstruction from future-state prediction, forcing the latent space to capture the underlying physics of deformation. We evaluate our approach on a large-scale simulated dataset of complex pick-and-place trajectories involving self-intersections. Our results demonstrate that the proposed model achieves a 40.52% reduction in open-loop prediction error over 50-step horizons compared to the state-of-the-art baseline, while reducing inference time by 31.17%. Our model further maintains superior topological consistency in scenarios with multiple crossings, proving its efficacy as a compositional primitive for long-horizon manipulation planning. Code, models and dataset will be released in a future revision.** 

## I. INTRODUCTION 

Robotic manipulation of Deformable Linear Objects (DLOs), such as cables, ropes, and sutures, remains one of the most challenging frontiers in autonomous manipulation while having a wide range of applications, such as Cable Routing [1], [2] Knot Tangling [3] and Untangling [4], [5]. Unlike rigid bodies, DLOs possess an infinite-dimensional state space and exhibit complex, non-linear dynamics governed by internal material constraints, self-intersections, and environmental interactions like friction. Predicting the evolution of a DLO’s shape during a manipulation task is critical for planning. Yet, it requires a model that is both computationally efficient for real-time use and robust enough to maintain topological integrity over long horizons. 

Recent advances in learning-based dynamics have shifted from analytical physical engines to data-driven models. Among these, Graph Neural Networks with segment-level encoders, such as GA-Net [6] have shown promise by treating the DLO as a series of interacting nodes. However, these methods often suffer from two primary drawbacks: first, they frequently struggle with over-smoothing [7] and over-squashing [8], [9] during long-range temporal dependencies, where the effect of an action at one end of the DLO fails to propagate accurately across many segments. Second, segment-level encoders lack inherent physical constraints, leading to non-physical “stretching” or “clipping” when the DLO undergoes complex deformations or self-intersections. 

In this paper, we propose a novel latent dynamics framework for DLO manipulation that addresses these limitations by combining structured kinematic priors with state-of-theart world models. We leverage the Recurrent State Space Model (RSSM) [10] to project DLO states into a latent manifold, effectively separating deterministic temporal dependencies from stochastic environmental uncertainties. 

To ensure physical consistency, we depart from standard Cartesian position representations and introduce a Quaternionic Kinematic Chain. By modeling the DLO as a sequence of unit quaternions representing relative rotations between equidistant segments, we inherently constrain the state space to a valid manifold, preventing non-physical stretching by design. Furthermore, we introduce a dual-decoder strategy that separates state reconstruction from predictive forecasting, ensuring that the model remains grounded in the current observation while optimizing the latent space specifically for multi-step “dreaming” of future DLO configurations. 

Our contributions are three-fold: 

- 1) We adapt the RSSM framework for high-segment DLO dynamics, enabling stable open-loop predictions over long horizons without ground-truth correction. 

- 2) We introduce a quaternionic state representation that enforces link-length constancy and provides superior topological consistency during complex maneuvers involving self-intersections. 

- 3) We demonstrate through extensive simulation<sup>1</sup> that our approach outperforms current baselines in longhorizon accuracy and maintains the DLOs topology better, while reducing inference latency by at least 31.17%. 

The remainder of this paper is organized as follows: Section III formalizes the DLO dynamics problem; Section IV details our RSSM-based architecture and quaternionic representation; Section V presents quantitative results against a baseline model; and concludes with a discussion. 

## II. RELATED WORK 

Robotic manipulation of DLOs spans a broad set of tasks and approaches. In this section, we review shape matching tasks and the dynamics prediction of DLOs. 

1The dataset, models, and evaluation scripts are available at: to be released 

## _A. DLO Shape Matching_ 

Existing research on robotic shape matching of DLOs can be categorized into physical properties and manipulation settings. A common distinction is between rope-like DLOs that behave as highly flexible objects and cable-like DLOs whose internal stiffness strongly constrains deformation. Research on ropes focuses on flexible DLOs with negligible bending stiffness [11], [12], [13], [14]. These objects are typically manipulated on a planar surface, where they maintain their state through friction and are unconstrained, thus allowing for manipulation at any point along their length. Ropes are challenging to work with because of their non-linear dynamics and their diverse set of possible states. In contrast, research on cables focuses on DLOs characterized by significant internal stiffness. As cables do not maintain their shape solely through surface friction, the problem statements involving cables generally assume boundary conditions where both ends of the DLO are secured, either to a rigid fixture or a robotic end-effector [6], [15], [16], [17], [18]. This work specifically addresses the challenges of manipulating unconstrained, flexible DLOs. 

## _B. Data-Driven DLO Dynamics Prediction_ 

The data-driven dynamics models utilized in DLO manipulation can be further classified by their state representation. One approach typically followed in rope manipulation employs latent visual models, which predict changes in the DLO state by encoding visual input into a latent space and predicting visual observations of following timesteps [11], [12], [13], [19]. However, these latent models frequently struggle to correctly interpret self-intersecting rope structures, such as loops or knots, while state-estimation frameworks such as TrackDLO [20] or other image-based methods [21], [22] demonstrate greater robustness in such scenarios. It has further been shown that predicting dynamics from pixels is outperformed by direct state representation, highlighting the need to split DLO Tracking and Dynamics Modeling [14]. 

Alternatively, other models represent the DLO explicitly as a sequence of discrete segments [14], [6], [15], [16], [17], [18]. These state-based models are further divided into recurrent architectures, such as Long Short-Term Memory (LSTM) networks [14], [18], and structural representations utilizing Graph Neural Networks (GNNs) or hybrids of both [15], [16], [17]. While showing promise in handling constrained, short DLOs, these methods are limited by selfintersections (e.g. a segment at one end of the DLO affects a segment in the middle of it), as local message-passing is fundamentally unfit to handle long-range dependencies [9]. Although some approaches attempt to mitigate this by incorporating attention mechanisms, these techniques still face challenges; for instance, in a non-intersected DLO configuration, the state of a segment typically does not affect distant segments, which can make attention weights unreliable in such situations [23]. Furthermore, attention mechanisms scale poorly ( _O_ ( _N_<sup>2</sup> )) to large sequence lengths [24]. 


Fig. 2. Problem formulation of DLO shape prediction task. a) The DLO lies on a work plane without fixation and can be moved by the end-effector at an arbitrary point. Overlaps between rope segments are thus possible. b) The affected segment is moved downwards, affecting the entirety of the DLO. 

Another approach to learn dynamics of a DLO from data is to approximate the Jacobian Matrix of the DLO locally [25], [26]. While making efficient use of sparse data, they are limited to small deformations [27]. RSSMs have further shown promising results in modeling deformables [19]. 

Our approach synthesizes key strengths from these previous works. We represent the DLO state as coordinates in R<sup>3</sup> , but rather than leveraging GNNs to model local graph-based connectivity, we treat the DLO as a kinematic chain. While prior methods rely on local neighbor interactions, attention mechanisms, or LSTMs to capture segment-wise dependencies, we utilize an RSSM to encode the global state into a latent manifold. The RSSM captures the underlying system dynamics in a latent space that is split into a deterministic and a stochastic part, which is better suited for modeling long-term temporal dependencies and maintaining physical consistency over extended horizons than purely deterministic approaches [28], [10]. 

III. PROBLEM FORMULATION 

We consider the task of modeling the dynamics of a highly flexible DLO during planar manipulation by a robotic endeffector, as depicted in Fig. 2. The DLO is assumed to have low bending stiffness, allowing for a wide range of DLO states. We treat the DLO as a free-moving multi-body system consisting of L segments, where each segment lives in R<sup>3</sup> . The system’s behavior is governed by internal bending constraints, friction with the ground plane, and interactions with a robotic end effector. 

## _A. State and Action Representation_ 

The DLO is discretized into a sequence of _L_ equidistant segments. The state of the DLO at timestep _t_ is denoted as **s** _t ∈_ R<sup>_L×_3</sup> , representing the positions of all _L_ segments: 


where _pi ∈_ R<sup>3</sup> is the position of the _i_ -th segment. 

The robotic interaction is defined by a pick-and-place action _ut_ = ( _ig,_ ∆ _p_ ), where _ig ∈{_ 1 _,..., L}_ denotes the index of the specific segment grasped by the robotic end-effector and ∆ _p_ = [∆ _x,_ ∆ _y_ ]<sup>_⊤_</sup> _∈_ R<sup>2</sup> represents the relative displacement vector of the grasped segment during the translation phase of the pick-and-place trajectory. This action consists of a grasp at an arbitrary point along the DLO’s length, followed by a trajectory comprising a vertical lift along the Z axis, a translation in the _XY_ -plane, and a subsequent vertical descent along the Z axis to the support surface. 

## _B. Objective_ 

The goal of this work is to develop a dynamics model _fθ_ capable of accurately predicting future DLO states in 3Dspace given the current state, a historical context, and an intended action. Given the state _st_ , a history of _n_ previous states _st−n_ : _t−_ 1, and an action _u_ , the model seeks to predict the subsequent state _s_ ˆ _t_ +1 = _fθ_ ( _st−n_ : _t , ut_ ). 

By formulating the problem around relative displacements on the _XY_ -plane and making the assumption that the DLO has already been picked up at the time of planning, the resulting model can be used to predict various displacement lengths without retraining by simply splitting up large actions into smaller ones. This incremental approach allows the model to generalize to large-scale deformations by iteratively compounding small-scale displacements. 

## _C. Evaluation Metric_ 

To quantify the accuracy of the dynamics model, we employ the Root Mean Square Error (RMSE) between the predicted segment positions _s_ ˆ _t_ +1 and the ground truth positions _st_ +1. The RMSE for a DLO state is defined as 


where _pi_ and _p_ ˆ _i_ are the ground truth and predicted coordinates for the _i_ -th segment, respectively. 

## IV. DYNAMICS MODEL FOR DEFORMABLE LINEAR OBJECTS 

In this section, we describe our proposed latent dynamics framework for modeling the transitions of DLOs. 

## _A. Quaternionic Kinematic Chain_ 

To treat the DLO as a rigid-link structure, as part of preprocessing, we transform the state _st_ into a hybrid representation. The first segment of the DLO is represented by its position _p_<sup>0</sup> _∈_ R<sup>3</sup> , while the configuration of all subsequent segments is defined by unit quaternions _q_<sup>_i_</sup> _∈_ H representing the relative rotation between link _i −_ 1 and link _i_ . 


Fig. 3. Architecture of the World Model for DLO manipulation. The current DLO state and manipulation actions are first fed into their respective encoders to generate latent embeddings. These representations are passed to the Recurrent State Space Model (RSSM) cell, alongside the previous deterministic and stochastic states, to update the current deterministic memory ( _ht_ ) and compute both the prior (ˆ _zt_ ) and posterior ( _zt_ ) distributions. In our dual-decoder setup, the posterior and deterministic states are used by the Reconstruction Decoder to reconstruct the current observation for spatial grounding. Simultaneously, the prior is chained through a subsequent RSSM step to forecast future latent variables, which the Prediction Decoder uses to predict the next physical rope state. Dashed lines indicate pathways and components utilized exclusively during the training phase. 

Assuming a fixed link length, the position of any segment position _p_<sup>_i_</sup> can be reconstructed via forward kinematics. This formulation constrains the state-space to a valid manifold, inherently preventing the model from predicting nonphysical stretching. Furthermore, as the model is solely presented with the DLO’s geometry and does not have to encode the distance between segments as in previous approaches, this pre-processing allows to scale a pretrained model to DLOs of varying length. The full state vector 


is derived by concatenating the position of the base _p_<sup>0</sup> and the relative rotations of all subsequent segments in quaternion form _q_<sup>1:</sup><sup>_L−_1</sup> . 

## _B. Latent Dynamics Learning using RSSM_ 

Our objective is to train a dynamics model capable of predicting the evolving state _st_ +1 given a history of past states and control actions _ut_ . Standard sequential predictors (e.g. LSTMs) often struggle with the information washout inherent in high-segment DLOs, where local perturbations propagate complexly across the entire structure. GNNs suffer from over-smoothing [7] and over-squashing [8], [9]. Attention mechanisms only partially solve these problems for self-intersecting DLOs and their computational complexity grows exponentially with sequence length [24]. To mitigate these long-range dependencies, we propose predicting dynamics within a latent state-space using an RSSM [28]. 

The RSSM operates directly on latent representations by first projecting inputs into embeddings via an encoder. It then decomposes the model’s dynamics into distinct deterministic and stochastic components. The deterministic state _ht_ (maintained by a Gated Recurrent Unit (GRU)) captures long-term memory and temporal dependencies, while the stochastic state _zt_ captures the uncertainty and variability of the environment that a single vector cannot represent [28]. During training, the model uses a _Posterior_ distribution grounded in actual observations to learn the latent space, while simultaneously training a _Prior_ (Transition Predictor) 

to forecast the next latent state without seeing the future, optimizing the model to keep these distributions similar to each other. This allows the agent to “dream” or simulate long sequences entirely in the latent space by chaining the prior and the recurrent model [10]. 

Unlike existing latent models that typically operate on high-dimensional raw visual input, our approach leverages an explicit kinematic representation, available via groundtruth data in simulation or through state-of-the-art tracking algorithms such as TrackDLO [20] in real-world settings. This decoupling allows the RSSM to focus specifically on the highly non-linear transitions of DLO dynamics while maintaining the flexibility to incorporate various perception backbones. Given that DLO tracking is a standalone research challenge, our framework is designed to be modular, ensuring compatibility with evolving state-estimation methods. By integrating this structured representation with a world-model framework, we address the gap in scaling latent dynamics to high-segment, potentially overlapping DLOs, a domain currently underexplored in frameworks using segment-level encoding like GA-Net [6]. The main components of our RSSM are: 

|**Action Encoder:**|_at_ = _fφ_(u_t_)|
|---|---|
|**Recurrent Model:**|_ht_ = _fφ_(_ht−_1_,zt−_1_,at−_1)|
|**State Encoder:**|_et_ = _fφ_(_st_)|
|**Posterior:**|_zt ∼qφ_(_zt | ht,et_)|
|**Prior:**|ˆ_zt ∼pφ_(ˆ_zt | ht_)|
|**Reconstruction Decoder:**|ˆ_s_<sup>recon</sup><br>_t_<br>_∼pφ_(ˆ_st | ht,zt_)|
|**Prediction Decoder:**|ˆ_s_<sup>pred</sup><br>_t_+1 <sup>_∼pφ_(ˆ</sup><sup>_st_+1</sup><sup>_| ht_+1</sup><sup>_,_ ˆ</sup><sup>_zt_+1)</sup>|


The key aspects of this RSSM implementation designed to fulfill the supervised objective of predicting the next state rely on the following points: 

_1) Link-Aware Action Encoding:_ The model employs a specialized **Action encoder** . It uses a learnable embedding layer for the DLO link index and a separate MLP for the link displacement. This allows the model to learn specific physical dynamics for different segments of the rope, capturing the non-homogeneous behavior often seen in DLO manipulation. 

_2) Dual-Decoder Strategy:_ The architecture splits the decoding task into a **Reconstruction Decoder** and a **Prediction Decoder** . The reconstruction decoder acts similarly to a traditional self-supervised auto-encoder [29], grounding the latent representations in the current state’s geometry and position. Conversely, the prediction decoder explicitly forecasts the next state _st_ +1 based on the prior “dream” step. Separating these tasks prevents the reconstruction loss from dominating the predictive dynamics, allowing the model to learn a transition space optimized for long-horizon DLO deformation forecasting. 

_3) Optimization and Loss:_ The model’s optimization is rooted in maximizing the Evidence Lower Bound (ELBO), a fundamental concept derived from variational inference [30]. ELBO is widely used in domains where the true underlying probability distribution is computationally intractable to calculate directly. Fundamentally, it balances two competing objectives: it forces the model to accurately reconstruct the observed data while simultaneously keeping the learned latent representations organized and close to a known prior distribution. By leveraging the ELBO, the RSSM is compelled to learn a compressed, probabilistic latent space that effectively captures the uncertainty of the DLO’s physical deformations. 

To adapt this framework specifically for multi-step DLO forecasting, we modify the standard ELBO objective into a composite loss function [30]. Instead of relying on a single observation target, our architecture minimizes the two distinct decoder losses alongside the latent regularization: 


**Reconstruction Loss** : Penalizes errors in recovering the current state _st_ from the posterior latent distribution, ensuring that the embedding captures the DLO’s immediate geometry. 


**Predictive Loss** : Forces the transition dynamics to be consistent with the physical evolution of the DLO by predicting the subsequent state. 


**KL Regularization** : Minimizes the divergence between the representation model (posterior) and the transition predictor (prior). This prevents the posterior from straying too far from the prior, ensuring the latent space remains stable and predictable when the model “dreams” future trajectories. 


A diagram containing a summary of the model architecture can be seen in Fig. 3. 


We evaluate our model and demonstrate that our architecture can accurately predict unconstrained DLO states, even under self-intersection, while maintaining the topology of the DLO. We further show that our model outperforms 

the strong learning-based baselines GA-Net [6] and INBiLSTM [18] in long-horizon accuracy, topology fidelity and inference time. We choose to evaluate our method against GA-Net as it outperformed the Interaction Network (IN) [31], PropNet [32] and the IN-BiLSTM [18] in the longhorizon DLO prediction task, thus we consider it state-ofthe-art although the IN-BiLSTM was not outperformed by a significant margin. We further evaluate against IN-BiLSTM to include a fundamentally different architectures than the combination of a Transformer-Encoder and an Attention Network used in GA-Net in our evaluation. Despite showing promising results, we decide not to compare our work against EA-PE-GAT [16] as it incorporates forces affecting the DLO. This strictly requires the DLO to be fixed on at least one end to sense force, making it an unfitting candidate for comparison. 

Empirical evaluation across our models hyperparameters led to the selection of three model scales (Small, Medium, Large). The variants were chosen based on their optimal tradeoff between RMSE and parameter count. The respective and total parameter counts can be seen in Table I. 

TABLE I 

CONFIGURATION OF OUR MODELS’ HYPERPARAMETERS 

|**Model**|_dembed_|_daction_|_drnn_|_dz_|_dhidden_|**Params**|
|---|---|---|---|---|---|---|
|Small (S)|1024|1024|512|64|512|7.85M|
|Medium (M)|1024|1024|512|64|1024|15.83M|
|Large (L)|2048|512|1024|64|2048|47.86M|


_A. Experiment Setup_ 

The proposed method is evaluated on a simulated dataset containing 10,000 DLO trajectories, with a fixed horizon of 100 steps per trajectory, resulting in a dataset of 1 million transitions. The dataset is divided into training (80%), validation (10%), and test (10%) subsets. The simulation is implemented in MuJoCo 3.3.7 [33], where the DLO is modeled as a chain of 70 capsules with a length of 10 _mm_ and a thickness of 10 _mm_ , connected by ball joints. The capsules’ friction is set to 0 _._ 8, bending stiffness of the joints is set to 0 _._ 005. The chain lies on a ground plane with ground friction set to 1 _._ 0 and damping set to 0 _._ 05. For each trajectory, the DLO is initialized by picking up a random segment and lifting it 50 _mm_ along the Z axis to allow the following displacements to produce crossings. The resting position after initial lift denotes _s_ 0. We then sample and execute a sequence of 100 random actions _ut_ . Each individual action is defined by a 50 _mm_ translation in the _XY_ -plane, with the heading angle sampled randomly from a uniform distribution [0 _,_ 2 _π_ ). The action is executed via a mocap object welded to the targeted segment. Each resulting trajectory consists of _T_ +1 states and _T_ actions. After the final action, the segment is returned to the planar surface. 

The proposed models and all baselines were optimized for up to 200 epochs using a learning rate of 1 _×_ 10<sup>_−_4</sup> , _β_ set to 1 and a batch size of 32, with model checkpointing ensuring the selection of the best-performing iteration on the validation set. Early Stopping was set to 10 epochs without 

TABLE II 

HYPERPARAMETER CONFIGURATIONS OF THE BASELINES. GA-NET USES A TRANSFORMER ENCODER AND ATTENTION NETWORK, WHILE IN-BILSTM USES AN INTERACTION NETWORK AND AN LSTM TO MODEL LONG RANGE DEPENDENCIES. AS A CONSEQUENCE, THE CONFIGURABLE PARAMETERS OF THE IN-BILSTM ARE A SUBSET OF GA-NET’S. XS, S, M, L, XL DENOTE SIZES XSMALL, SMALL, MEDIUM, LARGE, XLARGE. 

|**Model**|_dmodel_|_dhidden_|num<br>~~h~~eads|num<br>~~l~~ayers|**Params**|
|---|---|---|---|---|---|
|GA-Net XS|144|150|12|6|2.45M|
|GA-Net S|288|150|12|6|5.83M|
|GA-Net M|432|150|12|6|10.21M|
|GA-Net L1|720|150|12|6|21.94M|
|GA-Net L2|432|2048|12|6|26.86M|
|GA-Net XL|1440|150|12|6|68.69M|
|IN-BiLSTM S|-|512|-|3|18.64M|
|IN-BiLSTM M|-|512|-|5|31.28M|
|IN-BiLSTM L|-|1024|-|3|74.52M|


performance increase on the validation set. In practice, most configurations reached convergence near epoch 50. While the GA-Net (XS) baseline maintains the original layer depth and attention head count, the larger variants were derived by scaling both the embedding dimension _dmodel_ and the hidden layer width _dhidden_ to increase model capacity. We did not find that increasing layer depth and head count over the recommended values increased accuracy, For the IN-BiLSTM [18], we followed the recommended number of LSTM-Layers for two of the models, while increasing hidden state size to respect the higher complexity of our problem compared to the original source. To ensure that the models aren’t limited by layer count, we also increased this hyperparameter. The model configurations are shown in Table II. Training sessions were conducted on an Nvidia RTX Pro 6000 Blackwell Series. 

## _B. Prediction Error_ 

We evaluate the predictive performance of our models on a long-horizon, open-loop task using the previously simulated dataset’s testing subset. 

To ground our models’ latent state _h_ , we perform a warmup phase of 5 steps, where the model is provided with ground-truth state-action pairs ( _st , ut_ ). Subsequently, we assess the models’ ability to predict future states given only an action for 50 consecutive timesteps. During this phase, the model receives only the sequence of future actions _{ut }t_<sup>54</sup> =5 and must iteratively predict the subsequent states _{s_ ˆ _t_ +1 _}t_<sup>54</sup> =5 without further ground-truth corrections. We conduct 500 independent rollouts and report the average RMSE standard deviation over timesteps _t_ . 

To evaluate the model’s capacity for simultaneous state estimation, we conduct an experiment requiring the joint prediction of the DLO’s shape and its global translation. Quantitative results for this prediction task are reported in Fig. 4, which illustrates the RMSE across the open-loop horizon. 

Analysis of the data reveals a fundamental trade-off between local reconstruction precision and long-term dy- 


Fig. 4. Comparison of RopeDreamer variants (Ours) and baseline variants on the open-loop RMSE development over 50 steps. Lower is better. (a) Ours vs. GA-Net, (b) Ours vs. IN-BiLSTM 

namical stability. As depicted in Fig. 4a, most GA-Net configurations demonstrate higher accuracy in the immediate short-term, suggesting that its per-segment encoding is effective at preserving local geometric information during the initial state transitions. However, this local precision does not reliably translate to long-term stability. The sharp error growth observed, increasing by **15.68mm** at _t_ = 10 from _t_ = 1 and reaching **64.94mm** by _t_ = 50 for the best baseline (S), highlights a failure to model the cumulative global effects of actions over time. The IN-BiLSTM (Fig. 4b) mirrors the downward trend observed in GA-Net, albeit with a more accelerated rate of RMSE increase across the prediction horizon. This suggests that while the purely deterministic nature is accurate for single-step transitions, it suffers from significant drift during long-horizon propagation. The combination of the Transformer Encoder and an Attention Network used in GA-Net seems superior to the Interaction Network paired with a Sequential Model used in IN-BiLSTM. 

In contrast, our model begins with a higher RMSE than GA-Net, which can be attributed to the information bottleneck inherent in encoding the entire DLO configuration into a latent manifold. Following this initial reconstruction penalty, our architecture exhibits stable error growth, with an increase of only **5.44mm** at _t_ = 10 and **19.05mm** at _t_ = 50 for our best model (Large). Our model further shows stable standard deviation over all timesteps while the baselines follows an exponential trend. This stability indicates that the RSSM framework effectively internalizes the underlying physics of the actions, allowing the model to maintain the 

Fig. 5. Comparison of mean single-step inference time over different model architectures. S, M and L denote the model sizes as described in Tables I and II. GA is short for GA-Net. Red lines represent standard deviation. Lower is better. All experiments were conducted on an Nvidia 4060Ti GPU. 

global structure of the DLO even as errors in the segmentbased baseline begin to diverge. At _t_ = 50, our best model decreases RMSE by **40** _._ **52** % when compared against the best baseline model. 

Our ablation study using the quaternionic representation within the GA-Net framework (GA-Net XS / Quat) further clarifies these findings. While the quaternionic constraints improve GA-Net’s short-term consistency, they fail to arrest the long-term divergence. This suggests that the predictive stability of our approach is primarily driven by the RSSM’s latent temporal modeling rather than the coordinate representation alone. 

Finally, we report inference latencies of our models and the best-performing baseline models in Fig. 5 (log-scaled). Despite its higher parameter count, our large model achieves a **31.17%** reduction in computation time per prediction step compared to the small GA-Net (0 _._ 53 ms vs. 0 _._ 77 ms). Our smaller models widen this gap further at the cost of accuracy. IN-BiLSTM (S) shows inference times unsuitable for practical usage, with the larger models taking notably longer to perform a single prediction step. The superior inference speed of our architecture stems from projecting the state sequence into a compact latent space. Unlike GNNbased models, which must explicitly compute pairwise edge interactions and decode to physical positions at every time step, our RSSM performs temporal rollouts entirely within the latent space using lightweight recurrent updates. This allows the model to bypass the heavy graph construction overhead during multi-step forecasting. Consequently, our approach drastically accelerates the massively parallel trajectory sampling required for Model Predictive Control. 

## _C. Topology Error_ 

To evaluate the topological fidelity of the learned dynamics, we conduct a quantitative analysis of the models’ ability to maintain physical consistency during self-intersections. To automate this, we represent the DLO’s topology using Gauss Codes. This numerical form models the DLO as a directed curve and assigns a signed integer to each crossing: positive for an over-crossing (+ _i_ ) and negative for an under-crossing ( _−i_ ) [34]. For example, the configuration in Fig. 7 yields a Gauss code of [1 _,_ 2 _, −_ 1 _, −_ 2] when traversed from the right terminus to the left. By comparing predicted and ground- 

Fig. 6. Comparison of Topology Accuracy. Percentage denotes the amount of Gauss Codes exactly matching the ground truth. Higher is better. 


Fig. 7. Example of a loop and prediction at _t_ = 20 of our small model (red) and GA-Net S (blue) compared against the ground truth (black). Our model effectively identifies the loop and accurately reconstructs the rope. GA-Net fails to maintain DLO topology and predicts physically unrealistic link lengths. 

truth codes at each step, we measure the model’s preservation of the DLO’s structural identity. A match in Gauss codes implies topological equivalence. 

Following a 5-step warmup phase, each model was evaluated using open-loop rollouts across 50-step horizons over 500 unique trajectories. The mean performance and corresponding standard deviation are illustrated in Fig. 6. 

Our proposed architecture demonstrates a high degree of topological stability, maintaining mean success rates between 65% and 38% throughout the full prediction horizon regardless of model size. In contrast, the baseline models exhibit a precipitous decline in accuracy. The most competitive GA-Net baseline drops to 40% accuracy by step 10, with all baseline methods falling below the 10% mark by step 30. Notably, the GA-Net model using our quaternion representation (XS / Quat) drops to 0% accuracy by step 15. This suggests that while baselines may capture local geometric features in short-term prediction, they fail to preserve the structural identity of the DLO. In contrast, our model maintains topological accuracy in short- and longhorizon prediction. 

## VI. CONCLUSION AND FUTURE WORK 

In this paper, we introduced _RopeDreamer_ , a latent dynamics framework that leverages the synergy between Recurrent State Space Models and a Quaternionic Kinematic representation for the manipulation of DLOs. Our experiments demonstrate that by shifting dynamics modeling from local Cartesian graphs to a global latent manifold, we can 

effectively mitigate the information washout and temporal drift common in existing state-of-the-art baselines. While the latent bottleneck necessitates an initial reconstruction trade-off, our approach achieves a **40.52% reduction** in RMSE over 50-step horizons in complex deformation tasks. Crucially, our approach further delivers a substantial increase in topological integrity. Combined with a **31.17% improvement** in inference efficiency, this framework provides a robust and scalable backbone for real-time Model Predictive Control in high-dimensional manipulation of DLOs. 

Despite these gains, several research avenues remain open. We intend to explore hierarchical latent architectures to further reduce the initial reconstruction error. Another key objective is closing the sim-to-real gap through the integration of online system identification to adapt the latent dynamics to varying material properties, such as cable stiffness or surface friction. Finally, we aim to close the loop by deploying _RopeDreamer_ as a predictive primitive within a reinforcement learning framework for various rope manipulation tasks, validating its performance on physical robotic platforms using marker-free vision-based tracking. 

## REFERENCES 

- [1] G. A. Waltersson, R. Laezza, and Y. Karayiannidis, “Planning and Control for Cable-routing with Dual-arm Robot,” in _2022 International Conference on Robotics and Automation (ICRA)_ , (Philadelphia, PA, USA), pp. 1046–1052, IEEE, May 2022. 

- [2] A. Wilson, H. Jiang, W. Lian, and W. Yuan, “Cable Routing and Assembly using Tactile-driven Motion Primitives,” 2023. 

- [3] M. Sudry, T. Jurgenson, A. Tamar, and E. Karpas, “Hierarchical Planning for Rope Manipulation using Knot Theory and a Learned Inverse Model,” in _Proceedings of The 7th Conference on Robot Learning_ , vol. 229 of _Proceedings of Machine Learning Research_ , pp. 1596–1609, PMLR, 2023. 

- [4] J. Grannen, P. Sundaresan, B. Thananjeyan, J. Ichnowski, A. Balakrishna, V. Viswanath, M. Laskey, J. Gonzalez, and K. Goldberg, “Untangling Dense Knots by Learning Task-Relevant Keypoints,” in _Proceedings of the 2020 Conference on Robot Learning_ , pp. 782–800, PMLR, Oct. 2021. ISSN: 2640-3498. 

- [5] B. Guler, K. Pompetzki, S. Manschitz, and J. Peters, “Towards Assistive Teleoperation for Knot Untangling,” in _German Robotics Conference (GRC)_ , Mar. 2025. 

- [6] F. Gu, H. Sang, Y. Zhou, J. Ma, R. Jiang, Z. Wang, and B. He, “Learning Graph Dynamics With Interaction Effects Propagation for Deformable Linear Objects Shape Control,” _IEEE Transactions on Automation Science and Engineering_ , vol. 22, pp. 10881–10892, 2025. 

- [7] K. Oono and T. Suzuki, “Graph Neural Networks Exponentially Lose Expressive Power for Node Classification,” Jan. 2021. arXiv:1905.10947 [cs]. 

- [8] F. D. Giovanni, T. K. Rusch, M. M. Bronstein, A. Deac, M. Lackenby, S. Mishra, and P. Veliˇckovi´c, “How does over-squashing affect the power of GNNs?,” Feb. 2024. arXiv:2306.03589 [cs]. 

- [9] U. Alon and E. Yahav, “On the Bottleneck of Graph Neural Networks and its Practical Implications,” Mar. 2021. arXiv:2006.05205 [cs]. 

- [10] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to Control: Learning Behaviors by Latent Imagination,” Mar. 2020. arXiv:1912.01603 [cs]. 

- [11] W. Yan, A. Vangipuram, P. Abbeel, and L. Pinto, “Learning Predictive Representations for Deformable Objects Using Contrastive Estimation,” Mar. 2020. arXiv:2003.05436 [cs]. 

- [12] W. Zhang, K. Schmeckpeper, P. Chaudhari, and K. Daniilidis, “Deformable Linear Object Prediction Using Locally Linear Latent Dynamics,” Mar. 2021. arXiv:2103.14184 [cs]. 

- [13] R. Lee, M. Hamaya, T. Murooka, Y. Ijiri, and P. Corke, “SampleEfficient Learning of Deformable Linear Object Manipulation in the Real World Through Self-Supervision,” _IEEE Robotics and Automation Letters_ , vol. 7, pp. 573–580, Jan. 2022. 

- [14] M. Yan, Y. Zhu, N. Jin, and J. Bohg, “Self-Supervised Learning of State Estimation for Manipulating Deformable Linear Objects,” Oct. 2020. arXiv:1911.06283 [cs]. 

- [15] Z. Yue, X. Zhang, Y. Wang, S. Jiang, and J. Zhao, “LSTM-GCN Hybrid Architecture for Model Predictive Control of Deformable Linear Objects,” in _2025 IEEE International Conference on Mechatronics and Automation (ICMA)_ , pp. 303–309, Aug. 2025. ISSN: 2152-744X. 

- [16] Y. Yu, H. Yang, J. Tan, and X. Wang, “A Hybrid Force-Position Strategy for Shape Control of Deformable Linear Objects With Graph Attention Networks,” Aug. 2025. arXiv:2508.07319 [cs]. 

- [17] M. Yu, H. Zhong, and X. Li, “Shape Control of Deformable Linear Objects with Offline and Online Learning of Local Linear Deformation Models,” Feb. 2022. arXiv:2109.11091 [cs]. 

- [18] Y. Yang, J. A. Stork, and T. Stoyanov, “Learning to Propagate Interaction Effects for Modeling Deformable Linear Objects Dynamics,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1950–1957, May 2021. ISSN: 2577-087X. 

- [19] C. Li, Z. Ai, T. Wu, X. Li, W. Ding, and H. Xu, “DeformNet: Latent Space Modeling and Dynamics Prediction for Deformable Object Manipulation,” Feb. 2024. arXiv:2402.07648 [cs]. 

- [20] J. Xiang, H. Dinkel, H. Zhao, N. Gao, B. Coltin, T. Smith, and T. Bretl, “TrackDLO: Tracking Deformable Linear Objects Under Occlusion With Motion Coherence,” _IEEE Robotics and Automation Letters_ , vol. 8, pp. 6179–6186, Oct. 2023. 

- [21] A. Choi, D. Tong, B. Park, D. Terzopoulos, J. Joo, and M. K. Jawed, “mBEST: Realtime Deformable Linear Object Detection Through Minimal Bending Energy Skeleton Pixel Traversals,” _IEEE Robotics and Automation Letters_ , vol. 8, pp. 4863–4870, Aug. 2023. arXiv:2302.09444 [cs]. 

- [22] A. Caporali, K. Galassi, B. L. Zagar,<sup>ˇ</sup> R. Zanella, G. Palli, and A. C. Knoll, “RT-DLO: Real-Time Deformable Linear Objects Instance Segmentation,” _IEEE Transactions on Industrial Informatics_ , vol. 19, pp. 11333–11342, Nov. 2023. 

- [23] T. Mudarisov, M. Burtsev, T. Petrova, and R. State, “Limitations of Normalization in Attention Mechanism,” Oct. 2025. arXiv:2508.17821 [cs]. 

- [24] B. N. Patro and V. S. Agneeswaran, “Mamba-360: Survey of State Space Models as Transformer Alternative for Long Sequence Modelling: Methods, Applications, and Challenges,” Apr. 2024. arXiv:2404.16112 [cs]. 

- [25] M. Yu, K. Lv, H. Zhong, S. Song, and X. Li, “Global Model Learning for Large Deformation Control of Elastic Deformable Linear Objects: An Efficient and Adaptive Approach,” _IEEE Transactions on Robotics_ , vol. 39, pp. 417–436, Feb. 2023. 

- [26] S. Jin, C. Wang, and M. Tomizuka, “Robust Deformation Model Approximation for Robotic Cable Manipulation,” in _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 6586–6593, Nov. 2019. ISSN: 2153-0866. 

- [27] F. Gu, Y. Zhou, Z. Wang, S. Jiang, and B. He, “A Survey on Robotic Manipulation of Deformable Objects: Recent Advances, Open Challenges and New Frontiers,” Dec. 2023. arXiv:2312.10419 [cs]. 

- [28] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning Latent Dynamics for Planning from Pixels,” in _Proceedings of the 36th International Conference on Machine Learning_ , pp. 2555–2565, PMLR, May 2019. ISSN: 2640-3498. 

- [29] G. E. Hinton and R. R. Salakhutdinov, “Reducing the Dimensionality of Data with Neural Networks,” _Science_ , vol. 313, pp. 504–507, July 2006. 

- [30] D. P. Kingma and M. Welling, “Auto-Encoding Variational Bayes,” Dec. 2022. arXiv:1312.6114 [stat]. 

- [31] P. W. Battaglia, R. Pascanu, M. Lai, D. Rezende, and K. Kavukcuoglu, “Interaction Networks for Learning about Objects, Relations and Physics,” Dec. 2016. arXiv:1612.00222 [cs]. 

- [32] Y. Li, J. Wu, J.-Y. Zhu, J. B. Tenenbaum, A. Torralba, and R. Tedrake, “Propagation Networks for Model-Based Control Under Partial Observation,” Apr. 2019. arXiv:1809.11169 [cs]. 

- [33] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 5026–5033, Oct. 2012. ISSN: 2153-0866. 

- [34] L. H. Kauffman, “The Unknotting Problem,” in _Open Problems in Mathematics_ (J. Nash, John Forbes and M. T. Rassias, eds.), pp. 303– 345, Cham: Springer International Publishing, 2016. 

