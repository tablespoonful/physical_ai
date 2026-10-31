---
title: "What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?"
date: "2025-12-30"
authors: "Basile Terver; Tsung-Yen Yang; Jean Ponce; Adrien Bardes; Yann LeCun"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2512.24497
pdf: https://arxiv.org/pdf/2512.24497
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.24497)** / [論文ページ](https://arxiv.org/abs/2512.24497)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

# **What Drives Success in Physical Planning with JointEmbedding Predictive World Models?** 

**Basile Terver** _Meta FAIR Inria Paris_ 

_basile.terver@ens.psl.edu_ 

**Tsung-Yen Yang** _jimmytyyang@meta.com Meta FAIR_ **Jean Ponce** _jean.ponce@ens.fr Ecole normale supérieure / PSL New York University_ **Adrien Bardes** _abardes@meta.com Meta FAIR_ 

_abardes@meta.com_ 

**Yann Le Cun** _New York University_ 

_yann.lecun@nyu.edu_ 

**Reviewed on OpenReview:** _`https: // openreview. net/ forum? id= cHZn5Gdh8e`_ 

## **Abstract** 

A long-standing challenge in AI is to develop agents capable of solving a wide range of physical tasks and generalizing to new, unseen tasks and environments. A popular recent approach involves training a world model from state-action trajectories and subsequently using it with a planning algorithm to solve new tasks. Planning is commonly performed in the input space, but a recent family of methods has introduced planning algorithms that optimize in the learned representation space of the world model, with the promise that abstracting irrelevant details yields more efficient planning. In this work, we characterize models from this family as JEPA-WMs and investigate the technical choices that make algorithms from this class work. We propose a comprehensive study of several key components with the objective of finding the optimal approach within the family. We conducted experiments using both simulated environments and real-world robotic data, and studied how the model architecture, the training objective, and the planning algorithm affect planning success. We combine our findings to propose a model that outperforms two established baselines, DINO-WM and V-JEPA-2-AC, in both navigation and manipulation tasks. Code, data and checkpoints are available at `https://github.com/facebookresearch/jepa-wms` . 

## **1 Introduction** 

In order to build capable physical agents, Ha & Schmidhuber (2018) proposed the idea of a world model, that is, a model predicting the future state of the world, given a context of past observations and actions. Such a world model should perform predictions at a level of abstraction that allows training policies on top of it (Hafner et al., 2024; Mendonca et al., 2021; Guo et al., 2022) or perform planning in a sample efficient manner (Sobal et al., 2025; Hansen et al., 2024). While model-free RL (Mnih et al., 2015; Fujimoto et al., 2018; Mnih et al., 2016; Haarnoja et al., 2018; Schulman et al., 2017; Yarats et al., 2022) requires a 

1 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

considerable number of samples, model-based RL (MBRL), combined with self-supervised pretraining, has led to powerful world modeling algorithms (Ha & Schmidhuber, 2018; Seo et al., 2022; Schrittwieser et al., 2020; Hafner et al., 2024; Hansen et al., 2024). More recently, large-scale world models have flourished (Hu et al., 2023; Yang et al., 2023; Brooks et al., 2024; Bruce et al., 2024; Parker-Holder et al., 2024; Bartoccioni et al., 2025; Agarwal et al., 2025; Bar et al., 2025), achieving impressive simulation accuracy in specific domains such as driving (Hu et al., 2023; Bartoccioni et al., 2025) or egocentric video games (Bruce et al., 2024; Parker-Holder et al., 2024; Ball et al., 2025). 

In this presentation, we model a world in which some (robotic) agent equipped with a (visual) sensor operates as a dynamical system where the states, observations and actions are all embedded in feature spaces by parametric encoders, and the dynamics itself is also learned, in the form of a parametric predictor depending on these features. The encoder/predictor pair is what we will call a _world model_ . We will focus on _action-conditioned Joint-Embedding Predictive World Models_ (or _JEPA-WMs_ ) learned from videos (Sobal et al., 2025; Zhou et al., 2024a; Assran et al., 2025). These models adapt to the planning problem the Joint-Embedding Predictive Architectures (JEPAs) proposed by LeCun (2022), where a representation of some data is constructed by learning an encoder/predictor pair such that the embedding of one view of some data sample predicts well the embedding of a second view. We use the term JEPA-WM to refer to this family of methods, that we formalize in Equations (1) to (4) as a unified implementation recipe rather than a novel algorithm. The term JEPA-WM designates a specific recipe in which the dynamics model is trained solely through a predictive loss in embedding space, with no reconstruction, reward prediction, or value/policy heads, unlike methods such as MuZero (Schrittwieser et al., 2020), PlaNet (Hafner et al., 2019) or the Dreamer series (Hafner et al., 2020; 2021; 2024) (see Section B for a per-method comparison). Note that JEPA-WMs are not restricted to frozen encoders: PLDM (Sobal et al., 2025) and EB-JEPA (Terver et al., 2026) learn the encoder and predictor jointly. In practice, we optimize to find an action sequence without theoretical guarantees on the feasibility of the plan, which is closer to _trajectory optimization_ , but we stick to the widely-used term _planning_ . 

Among these JEPA-WMs, PLDM (Sobal et al., 2025) shows that, on 2D navigation tasks, world models learned in a latent space, trained as JEPAs, generalize better than the GCRL baselines considered in that work (Park et al., 2025), especially on suboptimal training trajectories. DINO-WM (Zhou et al., 2024a) shows that, in absence of reward, when comparing latent world models on goal-conditioned planning tasks, a JEPA model trained on a frozen DINOv2 encoder outperforms DreamerV3 (Hafner et al., 2024) and TDMPC2 (Hansen et al., 2024), when we deprive these of reward annotation. DINO-World (Baldassarre et al., 2025) shows the capabilities in dense prediction and intuitive physics of a JEPA-WM trained on top of DINOv2 are superior to COSMOS. The V-JEPA-2-AC (Assran et al., 2025) model is able to beat Vision Language Action (VLA) baselines like Octo (Octo Model Team et al., 2024) in greedy planning for object manipulation using image subgoals. 

In this paper, we focus on the learning of the dynamics (predictor) rather than of the representation (encoder), as in DINO-WM and V-JEPA-2-AC (Zhou et al., 2024a; Assran et al., 2025). Given the increasing importance of such models, we aim at filling what we see as a gap in the literature, i.e., a thorough study answering: _how to efficiently learn a dynamics model in the embedding space of a pretrained visual encoder for manipulation and navigation planning tasks ?_ 

Our contributions can be summarized as follows: **(i)** We study several key components of training and planning with JEPA-WMs: multistep rollout, predictor architecture, training context length, using or not proprioception, encoder type, model size, data augmentation; and the planning optimizer. **(ii)** We use these insights to propose an optimum in the class of JEPA-WMs, outperforming DINO-WM and V-JEPA-2-AC. 

## **2 Related work** 

**World modeling and planning.** ‘A path towards machine intelligence’ (LeCun, 2022) presents planning with Model Predictive Control (MPC) as the core component of Autonomous Machine Intelligence (AMI). World Models learned via Self-Supervised Learning (SSL) (Fung et al., 2025) have been used in many reinforcement learning works to control exploration using information gain estimation (Sekar et al., 2020) or curiosity (Pathak et al., 2017), to transfer to robotic tasks with rare data by first learning a world 

2 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 1: Left: Training of JEPA-WM: the encoder _Eϕ,θ_ embeds video and optionally proprioceptive observation, which is fed to the predictor _Pθ_ , along with actions, to predict (in parallel across timesteps) the next state embedding. Right: Planning with JEPA-WM: sample action sequences, unroll the predictor on them, compute a planning cost _L_<sup>_p_</sup> for each trajectory, and use this cost to iteratively refine the action sampling. The action encoder _Aθ_ and proprioceptive encoder _Eθ_<sup>_prop_</sup> are not explicitly displayed in this figure for readability. 

model (Mendonca et al., 2023) or to improve sample efficiency (Łukasz Kaiser et al., 2020). In addition, world models have been used in planning, to find sub-goals (Nair & Finn, 2020) by using the inverse problem of reconstructing previous frames to reach the objective represented as the last frame, or by imagining goals in unseen environments (Mendonca et al., 2021). World models can be generative (Brooks et al., 2024; Hu et al., 2023; Ball et al., 2025; Agarwal et al., 2025), using diffusion-based backbones to model multi-modal transition distributions, or deterministic and trained in a latent space via a JEPA loss (Garrido et al., 2024; Sobal et al., 2025; Terver et al., 2026; Assran et al., 2025; Zhou et al., 2024a; Bar et al., 2025), trading stochastic expressiveness for computational efficiency and latent abstraction. They can be used to plan in the latent space (Zhou et al., 2024a; Sobal et al., 2025; Bar et al., 2025), to maximize a sum of discounted rewards (Hansen et al., 2024; Hafner et al., 2019), or to learn a policy (Hafner et al., 2024). Other approaches for latent-space planning include locally-linear dynamics models (Watter et al., 2015), gradient-based trajectory optimization (Srinivas et al., 2018), and diffusion-based planners (Janner et al., 2022; Zhou et al., 2024b), details in Section B. While the present study focuses on the predictor given a frozen encoder, concurrent works explore lightweight adaptation of frozen VFM encoders for control, e.g. by training a bisimulation-based encoder on top of the frozen backbone (Toso et al., 2026), by learning sparse autoencoders on frozen features (Zhao et al., 2026), or by decoupling dynamics-relevant from dynamicsirrelevant representations (Yin et al., 2026). These directions are complementary to our predictor-focused investigation. 

**Explicit and implicit world models.** Our study focuses on _explicit_ world models with autoregressive dynamics in latent space. _Implicit_ alternatives such as TD-JEPA (Bagatella et al., 2026) fold temporal abstraction into the representation via successor features; we compare both paradigms in Section B. 

**Goal-conditioned RL.** Goal-conditioned RL (GCRL) offers a self-supervised approach to leverage largescale pretraining on unlabeled (reward-free) data. Foundational methods show that goal-conditioned policies can be incorporated into planning (Nasiriany et al., 2019; Li et al., 2022), decomposed hierarchically with sub-goal generators (Fang et al., 2022a;b), or combined with offline RL (Shah et al., 2021; Xu et al., 2023; Park et al., 2023). More recent methods learn geometrically grounded distances (Park et al., 2024; Myers et al., 2025), and the OGBench benchmark (Park et al., 2025) provides a systematic evaluation of offline GCRL across locomotion and manipulation. 

**Robotics.** Classical approaches rely on MPC loops (Garcia et al., 1989; Borrelli et al., 2017) leveraging analytical models of the robot Chignoli et al.; Meduri et al. (2022). For exteroception, our study relies on a camera, akin to the visual servoing problem Hutchinson et al. (1996). The current state-of-the-art in manipulation has been reached by Vision-Language-Action (VLA) models such as RT-X (Vuong et al., 2023), RT-1 (et al., 2023), and RT-2 (Zitkovich et al., 2023). Physical Intelligence’s _π_ series (Black et al., 

3 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 2: Comparison of different methods on the counterfactual Franka arm lift cup task, where we hardcode 2 actions, either “open and move up" or “close and move up". Each shows 5 model actions in open-loop rollout. Left: “open and move up" action. Right: “close and move up". First row: V-JEPA-2-AC. Second row: DINO-WM. Third row: our best model, described in Section 5.3. 

2024; Intelligence et al., 2025b;a) uses flow matching on the Open-X embodiment dataset to generate action trajectories. 

## **3 Background** 

This section formalizes the common setup of JEPA-WMs learned from pretrained visual encoders, but does not introduce novel methods. We summarize JEPA-WM training and planning in Figure 1. A consolidated notation reference is provided in Section A. 

**Training method.** In a JEPA-WM, we embed the observations with a frozen visual encoder _Eϕ_<sup>_vis_,and</sup> an (optional) shallow proprioceptive encoder _Eθ_<sup>_prop_</sup> . Applying each encoder to the corresponding modality constitutes the global state encoder, which we denote _Eϕ,θ_ = ( _Eϕ_<sup>_vis, E_</sup> _θ_<sup>_prop_</sup> ). An action encoder _Aθ_ embeds the robotic actions. On top of these, a predictor _Pθ_ takes both the state and action embeddings as input. _Eθ_<sup>_prop_</sup> , _Aθ_ and _Pθ_ are jointly trained, while _Eϕ_<sup>_vis_</sup> remains frozen. For a past window of _w_ observations _ot−w_ : _t_ := ( _ot−w, . . . , ot_ ) including visual and (optional) proprioceptive input and past actions _at−w_ : _t_ , their common training prediction objective on _B_ elements of the batch is 


where _L_ is a loss, computed pairwise between visual prediction and target, and proprioceptive prediction and target. In our experiments, we chose _L_ as the Mean Squared Error (MSE). The architecture chosen for the encoder and predictor in this study is ViT (Dosovitskiy et al., 2021), as in our baselines (Zhou et al., 2024a; Assran et al., 2025). In DINO-WM (Zhou et al., 2024a), the action and proprioceptive encoder are just linear layers, and their output is concatenated to the visual encoder output along the embedding dimension, which is known as _feature conditioning_ (Garrido et al., 2024), as opposed to _sequence conditioning_ , where the action and proprioception are encoded as tokens, concatenated to the visual tokens sequence, which is adopted in V-JEPA-2 (Assran et al., 2025). We stress that _Pθ_ is trained with a frame-causal attention mask, thus, it is simultaneously trained to predict from all context lengths from _w_ = 0 to _w_ = _W −_ 1, where _W_ is a training hyperparameter, set to _W_ = 3. The causal predictor is trained to predict the outcome of several actions instead of one action only. To do so, one can skip _f_ observations and concatenate the _f_ corresponding actions to form an action of higher dimension _f × A_ , as in DINO-WM (Zhou et al., 2024a). More details on the training procedure in Section C. 

**Planning.** Planning at horizon _H_ is an optimization problem over the product action space R<sup>_H×A_</sup> , where each action is of dimension _A_ , which can be taken to be _f × A_ when using frameskip at training time. Given an initial and goal observation pair _ot, og_ , each action trajectory _at_ : _t_ + _H−_ 1 := ( _at, . . . , at_ + _H−_ 1) should be evaluated with a planning objective _L_<sup>_p_</sup> . Like at training time, consider a dissimilarity metric _L_ , (e.g. the 

4 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 1: Summary of all candidate design choices studied in this work and recommended recipe per task category. Each row lists the options evaluated; the two rightmost columns report the empirically best option for simulated navigation and real-world manipulation, respectively. 

|Component|Candidates|Best:<br>Simu. Nav.|Best:<br>Real Manip.|
|---|---|---|---|
|**Encoder**||||
|Visual encoder|DINOv2 (ViT-S/B/L), DINOv3 (L), V-JEPA (L), V-JEPA-2 (L)|**DINOv2-S**|**DINOv3-L**|
|**Predictor**||||
|Architecture|Feat. cond. + sincos, Seq. cond. + RoPE, Feat. cond. + RoPE,<br>AdaLN + RoPE, AdaLN-zero + RoPE|**AdaLN + RoPE**|**AdaLN + RoPE**|
|Depth|3, 6, 9, 12|**6**|**12**|
|**Training**||||
|Rollout steps|1-step (teacher forcing), 2-step, 3-step, 6-step|**2**|**6**|
|Context length (_W_)|1, 2, 3, 5, 7, 9, 14|**3**|**5**|
|Proprioception|With / Without|✓|✓|
|**Planning**||||
|Optimizer|CEM, NG (NeverGrad), Adam, GD|**CEM**|**CEM**|
|Cost|_L_1, _L_2|**_L_2**|**_L_2**|


_L_ 1, _L_ 2 distance or minus the cosine similarity), applied pairwise on each modality, denoted _Lvis_ between two visual embeddings and _Lprop_ for proprioceptive embeddings. When planning with a model trained with both proprioception and visual input, given _α ≥_ 0, the planning objective _L_<sup>_p_</sup> _α_<sup>weaimtominimizeis</sup> 


with a function _Gϕ,θ_ depending on our world model. We define recursively _Fϕ,θ_ as the unrolling of the predictor from _zt_ = _Eϕ,θ_ ( _ot_ ) on the actions, with a maximum context length of _w_ , (fixed to _W_<sup>_t_</sup> at train time and to _W_<sup>_p_</sup> at test time Table 10) 


In our case, we take _Gϕ,θ_ to be the unrolling function _Fϕ,θ_ , but could choose _Gϕ,θ_ to be a function of all the intermediate unrolling steps, instead of just the last one. We provide details about the planning optimizers in Section F. 

## **4 Studied design choices** 

Our base configuration is DINO-WM without proprioception, with a ViT-S encoder and depth-6 predictor of same embedding dimension. A summary of all candidate design choices is provided in Table 1. We prioritize design choices based on their scope of impact: planning-time choices affect all evaluations, so we optimize these first and _fix the best planner for each environment for the subsequent experiments_ ; training and architecture choices follow; scaling experiments validate our findings. Each component is independently varied from the base configuration to isolate its effect. 

**Planner.** Various optimization algorithms can be relevant to solve the problem of minimizing equation 2, which is differentiable. Zhou et al. (2024a); Hansen et al. (2024); Sobal et al. (2025); Assran et al. (2025); Bar et al. (2025) use the Cross-Entropy Method (CEM) (or a variant called Model Predictive Path Integral (MPPI) (Williams et al., 2015)), depicted in Section F. Since this is a population-based optimization method which does not rely on the gradient of the cost function, we introduce a planner that can make use of any of the optimization methods from NeverGrad (Bennet et al., 2021). For our experiments, we choose the default NGOpt optimizer (Anonymous, 2024), which is designated as a “meta”-optimizer. We do not tune any of the parameters of this optimizer. We denote this planner NG in the remainder of this paper, see details in Section F. We also experiment with gradient-based planners (GD and Adam) that directly optimize the action sequence through backpropagation, see details in Section F. The planning hyperparameters common to the four considered optimizers are those which define the predictor-dependent cost function _Gθ_ , the planning 

5 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

horizon _H_ , the number of actions of the plan that are stepped in the environment _m ≤ H_ , the maximum sliding context window size of past predictions fed to the predictor, denoted _W_<sup>_p_</sup> . The ones common to either CEM and NG or to Adam and GD are the number of candidate action trajectories of which we evaluate the cost in parallel, denoted _N_ , and the number of iterations _J_ of parallel cost evaluations. After some exploration of the impact of planning hyperparameters common to both CEM and NG on success, we fix them to identical values for both, as summarized in Table 10 in appendix. We plan using either the _L_ 1 or _L_ 2 embedding space distance as dissimilarity metric _L_ in the cost _L_<sup>_p_</sup> _α_<sup>.TheresultsinFigure3(left)arean</sup> average across the models considered in this study. 

**Multistep rollout training.** At each training iteration, in addition to the frame-wise teacher forcing loss of equation 1, we compute additional loss terms as the _k_ -step rollout losses _Lk_ , for _k ≥_ 1, defined as 


where _z_ ˆ _t_<sup>_b_</sup> + _k−_ 1<sup>=</sup><sup>_Fϕ,θ_(</sup><sup>_ot, at−w_:</sup><sup>_t_+</sup><sup>_k−_2),seeequation3.</sup> We note that _L_ 1 = _L_ . In practice, we perform truncated backpropagation over time (TBPTT) (Elman, 1990; Jaeger, 2002), which means that we discard the accumulated gradient to compute _z_ ˆ _t_ + _H_ and only backpropagate the error in the last prediction. We study variants of this loss, as detailed in Section C, including the one used in V-JEPA-2-AC. We denote the model trained with a sum of loss terms up to the _Lk_ loss as _k_ -step. We train models with up to a 6-step loss, which requires more than the default _W_ = 3 maximum context size, hence we set _W_ = 7 to train them, similarly to the models with increased _W_ introduced afterwards. 

**Proprioception.** We compare the standard setup of DINO-WM (Zhou et al., 2024a), where we train a proprioceptive encoder jointly with the predictor and the action encoder to a setup with visual input only. We stress that, contrary to V-JEPA-2-AC, we use both the visual and proprioceptive loss terms to train the predictor, proprioceptive encoder and action encoder. 

**Training context size.** We aim to test whether allowing the predictor to see a longer context at train time allows to better unroll longer sequences of actions. We test values from _W_ = 1 to _W_ = 14. 

**Encoder type.** As posited by Zhou et al. (2024a), local features preserve spatial details that are crucial to solve the tasks at hand. Hence we use the local features of DINOv2 and the recently proposed DINOv3 (Siméoni et al., 2025), even stronger on dense tasks. We train a predictor on top of video encoders, namely V-JEPA (Bardes et al., 2024) and V-JEPA-2 (Assran et al., 2025). We consider their ViT-L version. After exploration of the frame encoding strategy to adopt Section C, we settle on the highest performing one, which consists in duplicating each of the _ot−W_ +1 _, . . . , ot_ +1 frames and encoding each pair independently as a 2-frame video. Details comparing the encoding methods for all encoders considered are in Section C. The frame preprocessing and encoding is equalized to have the same number of visual embedding tokens per timestep, so the main difference lies in the weights of these encoders that we use out-of-the-box. 

**Predictor architecture.** The main difference between the predictor architecture of Zhou et al. (2024a), and the one of Assran et al. (2025), is that the first uses feature conditioning, with sincos positional embedding, whereas the latter performs sequence conditioning with RoPE (Su et al., 2024). In the first, action embeddings _Aθ_ ( _a_ ) are concatenated with visual features _Eθ_ ( _o_ ) along the embedding dimension, and the hidden dimension of the predictor is increased from _D_ to _D_ + _fa_ , with _fa_ the embedding dimension of actions. The features are then processed with 3D sincos positional embeddings. In the second, actions are encoded as separate tokens and concatenated with visual tokens along the sequence dimension, keeping the predictor’s hidden dimension to _D_ (as in the encoder). Rotary Position Embeddings (RoPE) is used at each block of the predictor. We also test an architecture mixing feature conditioning with RoPE. Another efficient conditioning technique is Adaptive Layer Normalization (AdaLN) (Xu et al., 2019), as adopted by Bar et al. (2025), which we also put to the test, using RoPE in this case. This approach allows action information to influence all layers of the predictor rather than only at input, potentially preventing vanishing of action information through the network. We also study the AdaLN-zero variant (Peebles & Xie, 2023), which initializes the 

6 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 3: (a) Comparison of planning optimizers: NG is the Nevergrad-based interface that we introduce, compared to the Cross-Entropy Method (CEM), Adam, and Gradient Descent (GD), with _L_ 1 or _L_ 2 distance. (b) Effect of adding multistep rollout loss terms: models are trained with total loss _L_ 1 + _· · ·_ + _Lk_ . Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. 

conditioning MLP to output the zero-vector, so that the predictor behaves like an unconditional ViT block at the beginning of training. Details are provided in Section C. 

**Model and data scaling.** We increase the encoder size to ViT-B and ViT-L, using DINOv2 ViT-B and ViT-L with registers (Darcet et al., 2024). When increasing encoder size, we expect the prediction task to be harder and thus require a larger predictor. Hence, we increase accordingly the predictor embedding dimension to match the encoder. We also study the effect of predictor depth, varying it from 3 to 12. Regarding data scaling, we ablate the impact of these design choices on the sample-efficiency of JEPA-WMs, by training on 2%, 10%, 50% or 100% of the available training data. We compare our optimal JEPA-WM, detailed in Section 5.3 below, to the DINO-WM and V-JEPA-2-AC baselines for each of the data scale regimes considered. 

## **5 Experiments** 

### **5.1 Evaluation Setup.** 

**Datasets.** For Metaworld, we gather a dataset by training TD-MPC2 (Hansen et al., 2024) online agents and evaluate two tasks, “Reach" and “Reach-Wall", denoted _MW-R_ and _MW-RW_ , respectively. We use the offline trajectory datasets released by Zhou et al. (2024a), namely Push-T (Chi et al., 2023), Wall and PointMaze. The train split represents 90% of each dataset. We train on DROID (et al., 2024) and evaluate zero-shot on Robocasa (Nasiriany et al., 2024) by defining custom pick-and-place tasks from teleoperated trajectories, namely “Place" and “Reach", denoted _Rc-Pl_ and _Rc-R_ . We _do not finetune_ the DROID models on Robocasa trajectories. We also evaluate on a set of 16 videos of a real Franka arm filmed in our lab, closer to the DROID distribution, and denote this task _DROID_ . On DROID, we track the _L_ 1 error between the actions outputted by the planner and the groundtruth actions of the trajectory from the dataset that defines initial and goal state. We then rescale the opposite of this _Action Error_ , to constitute the _Action Score_ , a metric to maximize. We provide details about our datasets and environments in Section E. 

**Goal definition.** We sample the goal frame from an expert policy provided with Metaworld, from the dataset for Push-T, DROID and Robocasa, and from a random 2D state sampler for Wall and Maze, more details in Section E. For the models with proprioception, we plan using proprioceptive embedding distance, by setting _α_ = 0 _._ 1 in equation 2, except for DROID and Robocasa, where we set _α_ = 0, to be comparable to V-JEPA-2-AC. 

**Metrics.** The main metric we seek to maximize is success rate, but track several other metrics, that track the world model quality, independently of the planning procedure, and are less noisy than success rate. These metrics are embedding space error throughout predictor unrolling, proprioceptive decoding error throughout unrolling, visual decoding of open-loop rollouts (and the Learned Perceptual Image Patch 

7 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 4: (a) Models trained with proprioceptive input are denoted “prop", while pure visual world models are named “no-prop". (b) Comparison of JEPA-WMs trained on top of various pretrained visual encoders, all of size ViT-L for fair comparison. Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. 

Similarity (LPIPS) (Zhang et al., 2018) between these decodings and the groundtruth future frames). More details in Section G.2. 

**Statistical significance.** To account for training variability, we train with 3 seeds per model for our final models in Table 2. We evaluate on _e_ episodes per epoch ( _e_ =96 for most environments, _e_ =64 for DROID, _e_ = 32 for Robocasa) and average success over the last _n_ training epochs to obtain aggregate scores; full details on aggregation and error bars are provided in Section G.2. 

### **5.2 Results** 

One important fact to note is that, even with models which are able to faithfully unroll a large number of actions, success at the planning task is not an immediate consequence. We develop this claim in Section G.1, and provide visualizations of rollouts of studied models and planning episodes. 

**Comparing planning optimizers.** We compare four planning optimizers: Cross-Entropy Method (CEM), Nevergrad (NG), Adam, and Gradient Descent (GD). CEM is a variant of the Covariance Matrix Adaptation Evolution Strategy (CMA-ES) family (Hansen & Ostermeier, 1996; Hansen, 2023) with diagonal covariance and simplified update rules. NG uses the NGOpt wizard, which selects diagonal CMAES (Hansen et al., 2019) based on optimization space parametrization and budget, see Algorithm 2. We observe in Figure 3a that the CEM _L_ 2 planner performs best overall. 

_(i) Gradient-based methods:_ Adam _L_ 2 achieves the best overall performance on Metaworld, outperforming all other optimizers, and GD is also competitive with CEM. This can be explained by the nature of Metaworld tasks: they have relatively smooth cost landscapes where the goal is greedily reachable, allowing gradientbased methods to excel. In contrast, on 2D navigation tasks (Wall, Push-T, Maze) that require non-greedy planning, gradient-based methods perform very poorly compared to sampling-based ones, as GD gets stuck in local minima. On DROID, gradient-based methods also perform significantly worse than sampling-based approaches: these tasks require rich and precise understanding of complex real-world object manipulation, leading to multi-modal cost landscapes. Robocasa tasks, being simulated but closer in nature to Metaworld, allow gradient-based methods to perform reasonably well again. 

_(ii) Sampling-based methods:_ On 2D navigation tasks, CEM clearly outperforms NG, as these tasks require precise action sequences where CEM’s faster convergence to tight action distributions is beneficial, while NG’s slower, more exploratory optimization is detrimental. To compare both methods, we plot the convergence of the optimization procedure at each planning step in Figure 9, and observe that NG converges more slowly, indicating more exploration in the space of action trajectories. On DROID and Robocasa, CEM and NG perform similarly. When using NG, we have fewer planning hyperparameters than with CEM, which requires specifying the top- _Ke_ trajectories parameter and the initialization of the proposal Gaussian distribution _µ_<sup>0</sup> _, σ_<sup>0</sup> —parameters that heavily impact performance. Crucially, on real-world manipulation data (DROID and Robocasa), NG performs on par with CEM while requiring no hyperparameter tuning, 

8 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 5: (a) Comparing predictor architectures: we denote positional embedding in the predictor as sincos or RoPE; the feature conditioning technique as “ftcond" and the sequence conditioning as “seqcond". The Adaptive LayerNorm conditioning technique is denoted “AdaLN". (b) Maximum number of timesteps of state embedding seen by the predictor at train time in equation 1, the predictor takes up to ( _Eϕ,θ_ ( _ot−W_ +1: _t_ ) _, Aθ_ ( _at−W_ +1: _t_ )) as context. Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. making it a practical alternative when transitioning to new tasks or datasets where CEM tuning would be costly. 

On all planning setups and models, _L_ 2 cost consistently outperforms _L_ 1 cost. To minimize the number of moving parts in the subsequent study, we _fix the planning setup_ for each dataset to CEM _L_ 2, which is either best or competitive on all environments. 

**Multistep rollout predictor training.** At planning time, the predictor is required to faithfully roll out an action sequence by predicting future embeddings from its previous predictions. We observe in Figure 3b that the performance increases when going from pure teacher-forcing models to 2-step rollout loss models, but then decreases for models trained in simulated environments. At train time, during the predictor rollout, the context window for rollout steps _k >_ 1 is set to a maximum of _W_<sup>_t_</sup> = 3 timesteps. At test time, we start the predictor unrolling from one groundtruth (visual and optionally proprioceptive) embedding and unroll the predictor for _H_ steps, with a predictor sliding context window of length _W_<sup>_p_</sup> = 2, as explained in equation 4 and Section C. Because the predictor _Pθ_ is a neural network with Lipschitz constant Λ _≥_ 1 in general (Miyato et al., 2018; Virmaux & Scaman, 2018), compounding prediction errors in continuous embedding space grow exponentially with the horizon _H_ (we formalize this in Section D). This creates an _accuracy-robustness tradeoff_ when choosing the number of rollout steps _K_ for training: increasing _K_ raises _δK_ (the one-step error on groundtruth inputs) but reduces the effective Lipschitz constant Λ _K_ (see Remark 1 for a detailed analysis). The multi-step rollout loss thus acts as data augmentation against compounding error: the model learns to remain on the data manifold after several autoregressive steps, analogous to scheduled sampling (Bengio et al., 2015; Ross et al., 2011; Bengio et al., 1994). In simulated environments, the accuracy term dominates and the optimum is at small _K_ ; on DROID, reducing Λ _K_ more than compensates the increase in _δK_ , and the optimal tradeoff point shifts to _K_ =6. 

**Impact of proprioception.** We observe in Figure 4a that models trained with proprioceptive input are consistently better than without. Visual embeddings from a frozen encoder capture appearance and coarse spatial layout, but precise metric quantities (joint positions, end-effector coordinates) are only implicitly encoded and subject to quantization by the patch-based architecture. Proprioception provides a metrically precise complement, particularly near goal states where small physical displacements yield negligible changes in embedding distance. On Metaworld, this explains the observed failure mode: without proprioception, the arm reaches the vicinity of the goal but oscillates, unable to resolve the remaining distance from vision alone. We do not display the results on Robocasa as the proprioceptive space is not aligned between DROID and Robocasa, making models using proprioception irrelevant for zero-shot transfer. 

**Maximum context size. (i)** A first experiment confirms a well-known but fundamental property: the training maximum context _W_ and planning maximum context _W_<sup>_p_</sup> must be chosen so that _W_<sup>_p_</sup> _≤ W_ . Otherwise, we ask the model to perform a prediction task it has not seen at train time, and we see the 

9 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 6: (a) Comparison of model size: we vary from ViT-S to ViT-L the visual encoder size, as well as the predictor embedding dimension, keeping predictor depth constant at 6. (b) Comparison of predictor depth: we vary the predictor depth from 3 to 12, keeping the encoder fixed to DINOv2-S. Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. 

predictions degrading rapidly throughout unrolling if _W_<sup>_p_</sup> _> W_ . To account for this, the _W_ = 1 model performance displayed in Figure 5b is from planning with _W_<sup>_p_</sup> = 1. **(ii)** We recall that we chose to plan with _W_<sup>_p_</sup> = 2 in all our experiments, since it yields the maximal success rate while being more computationally efficient. The predictor needs two frames of context to infer velocity and use it for the prediction task. It requires 3 frames to infer acceleration. We indeed see in Figure 5b a big performance gap between models trained with _W_ = 1 and _W_ = 2, which indicates that the predictor benefits from using this context to perform its prediction. Interestingly, we observe that models trained on DROID have their optimal _W_ at 5, higher than on simulated datasets, for which it is 3. It is likely due to the more complex dynamics of DROID, requiring longer context to notably infer real-world arm and object dynamics. While longer context could in principle help capture phenomena such as object permanence or long-term momentum, occlusions are rare on DROID and Robocasa, as they can mostly occur between the arm the manipulated objects. Moreover, we sample the DROID dataset (natively at 30 fps) at 4 fps, so a training slice of _W_ + 1 = 8 frames already spans over 2 seconds of video, covering most occlusion events in the dataset. **(iii)** Increasing _W_ also reduces the number of unique training slices, which, even with a fixed number of training iterations, can harm performance on small datasets (e.g. on DROID, _W_ =14 retains only 86% of videos); see Section E for details. This is in line with the observation made by Sobal et al. (2025), that world models are good at "stitching suboptimal trajectories", compared to GCRL. 

**Encoder type.** In Figure 4b, we see a clear advantage of DINO encoders compared to V-JEPA encoders. We posit this is due to the well-known fact that DINO has better fine-grained object segmentation capabilities, which is crucial in tasks requiring a precise perception of the location of the agent and objects. For a frozen-encoder JEPA-WM, the predictor must learn dynamics entirely in the encoder’s representation space. DINO’s finer object segmentation means that distinct objects occupy distinct spatial tokens with sharp boundaries, so that object motion translates into localized, sparse token changes that the predictor can learn efficiently. Coarser segmentation, as exhibited by V-JEPA even in image mode (Section C), spreads object information across overlapping sets of tokens, making it harder for the predictor to isolate per-object dynamics. Interestingly, DINOv3 clearly outperforms DINOv2 only on the more photorealistic environments, Robocasa and DROID, likely due to the pretraining dataset of DINOv3 being more adapted to such images. On synthetic environments, DINOv2 already captures the simpler visual appearance; DINOv3’s additional capacity may produce representations unnecessarily complex for the predictor, explaining why on Maze and Wall, models trained on DINOv3 take longer to converge to a lower success rate. 

**Predictor architecture.** In Figure 5a, we observe that, while AdaLN with RoPE achieves the best average performance across environments, the advantage is slight, and results are task-dependent: on Metaworld, sincos+ftcond actually performs best. We do not see a substantial improvement when using RoPE instead of sincos positional embedding. As discussed when introducing AdaLN, its per-block conditioning may help avoid vanishing of the action information through the predictor’s layers, while being more compute-efficient than other conditioning schemes (Peebles & Xie, 2023). We also study AdaLN-zero, following Peebles & Xie 

10 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 7: Data scaling ablation: we display planning performance for models trained on 2%, 10%, 50% or 100% of the entire dataset, fixing the number of iterations across runs, independently of dataset size, with dataset metrics in Table 8. (a) Models trained on simulated environments, namely Metaworld, Maze, PushT and Wall. (b) Models trained on the real-world robotic DROID dataset, evaluated on real-world videos (DROID) and on the Robocasa simulator. Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. 

(2023)’s naming. Although Peebles & Xie (2023) find AdaLN-zero to outperform AdaLN in their setup, we observe that, despite a higher average performance, AdaLN-zero underperforms AdaLN on the environments that provide the most reliable signal (DROID, PushT, Maze), which are less prone to noise in success rate and yield more consistent results across our other design choice experiments. Hence, we will consider, for our final JEPA-WMs optimum, the AdaLN variant. One important consideration when scaling predictor embedding dimension is maintaining the ratio of action to visual dimensions, which requires increasing the action embedding dimension in the feature conditioning case. To isolate the effect of the conditioning scheme from capacity differences due to different action ratios, we conduct additional experiments with equalized action ratios (see Section G.1), which reveal task-dependent preferences between conditioning schemes that cannot be attributed to action ratio alone. 

**Model scaling.** We show in Figures 6a and 6b that increasing encoder size (with predictor width) or predictor depth does not improve performance on simulated environments. We identify three complementary hypotheses for this behavior: **(a)** simulated tasks are simple enough to saturate at small model sizes, so additional capacity brings no benefit; **(b)** larger embedding spaces make the planning optimization landscape harder to navigate, as the planner must distinguish nearby states in a higher-dimensional space (see Figure 18); **(c)** with fixed training compute, larger models see fewer gradient updates per parameter, potentially leading to underfitting. Notably, the optimal predictor depth appears to be 6 for most simulated environments, and possibly as low as 3 for the simplest 2D navigation tasks (Wall, Maze). However, on DROID, we observe a clear and consistent positive correlation between both encoder size and predictor depth with planning performance. This indicates that real-world data with complex visual dynamics benefits from higher-capacity models. This contrast provides a practical guideline for practitioners: scaling model capacity is most beneficial when the environment exhibits complex, high-dimensional dynamics (as in real-world robotics), while simulated environments with simple dynamics saturate at small model sizes. 

**Data scaling.** The results in Figure 7 provide three insights. **(i)** For all datasets and methods considered, performance clearly increases when scaling data, as the world model captures more diverse dynamics and nuances of the environment, allowing for more accurate predictions and better-informed planner optimization. This is expected, as the three methods rely on the same main learning signal, which is the one-step teacherforcing loss in state embedding space. **(ii)** Our method outperforms baselines especially on DROID and Wall, where the data scaling seems less saturated. On the Push-T and Metaworld tasks, it also seems like increasing data diversity would increase performance by a large margin, yet our method’s advantage is less clear. **(iii)** The results for models trained on DROID are in Figure 7b. When evaluating these on offline planning on Franka videos (denoted DROID), we clearly see performance scaling with data quantity. Yet, for Robocasa Place and Reach, scaling is less clear, due to the domain gap between DROID and Robocasa. 

11 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 2: Comparison of our best model to DINO-WM and V-JEPA-2-AC. MW-R and MW-RW denote the Reach and Reach-Wall tasks of Metaworld. Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. V-JEPA-2-AC numbers are obtained from our retrained model with the rollout-loss bug fix described in Section C, not from the public checkpoint. Best model is in **bold** . 

|Model|Maze|Wall|Push-T|MW-R|MW-RW|Rc-R|Rc-Pl<br>DR|OID|
|---|---|---|---|---|---|---|---|---|
|DWM|81.6 (3.4)|64.1 (4.6)|66.0 (4.7)|44.8 (8.9)|35.1 (9.4)|19.1 (13.4)|21.7 (7.2)<br>39.4|(2.1)|
|VJ2AC|—|—|—|—|—|16.2 (8.3)|**33.1 (7.2)**<br>42.9|(2.5)|
|Ours|**83.9 (2.3)**|**78.8 (3.9)**|**70.2 (2.8)**|**58.2 (9.3)**|**41.6 (10.0)**|**25.4 (16.6)**|30.7 (8.0)<br>**48.2 **|**(1.8)**|


### **5.3 Our proposed optimum in the class of JEPA-WMs** 

We combine the findings of our study and propose optimal models for each of our robotic environments, that we compare to concurrent JEPA-WM approaches: DINO-WM (Zhou et al., 2024a) and V-JEPA-2AC (Assran et al., 2025). For simulated environments, we use a ViT-S encoder and a ViT-S predictor with depth 6, AdaLN conditioning, and RoPE positional embeddings. We train our models with proprioception and a 2-steps rollout loss, with a maximum context of _W_ = 3. For DROID and Robocasa, following our model size findings, we use a ViT-L encoder with a ViT-L predictor of depth 12, without proprioception. We plan with CEM _L_ 2 for all environments. We use DINOv2 on all environments, except on the photorealistic DROID and Robocasa, where we use DINOv3. We summarize the recommended recipe per task type in Table 1. As presented in Table 2, we outperform DINO-WM and V-JEPA-2-AC in most environments. We provide a full comparison across all planner configurations in Table 11. We propose in Figure 2 a qualitative comparison of the object interaction abilities of our model against DINO-WM and V-JEPA-2-AC, in a simple counterfactual experiment, where we unroll two different action sequences from the same initial state, one where the robot lifts a cup, and one where it does not. Our model demonstrates a better prediction of the effect of its actions on the environment. 

## **6 Conclusion** 

In this paper, we studied the effect of several training and planning design choices of JEPA-WMs on planning in robotic environments. We found that several components play an important role, such as the use of proprioceptive input, the multistep rollout loss, or the choice of visual encoder. We found that image encoders with fine object segmentation capabilities are better suited for the manipulation and navigation tasks that we considered compared to video encoders. We found that having enough context to infer velocity is important, but that too long context harms performance, obviously due to seeing less unique trajectories during training and likely also having less useful gradient from predicting from long context. On the architecture side, we found that the action conditioning technique matters, with AdaLN being a strong choice on average, compared to sequence and feature conditioning, though results are task-dependent. We found that scaling model size (encoder size with predictor width, and predictor depth) does not improve performance on simulated environments. However, on real-world data (DROID and Robocasa), both larger encoders and deeper predictors yield consistent improvements, suggesting that scaling benefits depend on task complexity. We introduced an interface for planning with Nevergrad optimizers, leaving room for exploration of optimizers and hyperparameters. On the planning side, we found that CEM _L_ 2 performs best overall. The NG planner performs similarly to CEM on real-world manipulation data (DROID and Robocasa) while requiring less hyperparameter tuning, making it a practical alternative when transitioning to new tasks or datasets. Gradient-based planners (GD and Adam) excel on tasks with smooth cost landscapes like Metaworld, but fail on 2D navigation or contact-rich manipulation tasks due to local minima. Finally, we applied our learnings and proposed models outperforming concurrent JEPA-WM approaches, DINO-WM and V-JEPA-2-AC. A limitation of this class of approaches is the deterministic predictor: the MSE loss learns the conditional mean of potentially genuinely multi-modal futures. This is mitigated in our benchmarks by their deterministic dynamics, by the latent abstraction of task-irrelevant variability and closed-loop MPC providing robustness to prediction errors. For environments with aleatoric uncertainty, JEPA-WMs would require stochastic extensions such as latent variable injection (LeCun, 2022) or diffusion in latent space. 

12 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

### **Broader Impact Statement** 

This work focuses on learning world models for physical agents, with the aim of enabling more autonomous and intelligent robots. We do not anticipate particular risk of this work, but acknowledge that further work building on it could have impact on the field of robotics, which is not exempt of risks of misuse. We also acknowledge the environmental impact of training large models, and we advocate for efficient training procedures and sharing of pretrained models to reduce redundant computation. 

### **Author Contributions** 

Basile Terver led the project, implemented the code, managed the experiments and wrote the paper. TsungYen Yang helped with setting a custom robocasa evaluation pipeline. Quentin Garrido proposed the AdaLN conditioning implementation. Adrien Bardes, Jean Ponce and Yann Le Cun provided research directions guidance on the project and supervised the framing of the paper. All authors discussed the results and commented on the paper. 

### **Acknowledgments** 

We thank Quentin Garrido for his help and insightful methodology and conceptualization advice throughout the project. We thank Daniel Dugas for the constructive discussions we had throughout the project, and for helping provide the Franka Arm videos we use for evaluation. 

This work was supported in part by the French government under management of Agence Nationale de la Recherche as part of the “France 2030” program, PR[AI]RIE-PSAI project, reference ANR-23-IACL0008. J.P. was supported in part by the Institute of Information & Communications Technology Planning & Evaluation (IITP) grant funded by the Korean Government (MSIT) (No. RS-2024-00457882, National AI Research Lab Project), and a Global Distinguished Professorship at the Courant Institute of Mathematical Sciences and the Center for Data Science at New York University. 

13 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

## **References** 

- Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- Anonymous. Ngiohtuned, a new black-box optimization wizard for real world machine learning. _Submitted to Transactions on Machine Learning Research_ , 2024. URL `https://openreview.net/forum?id= 0FDiCoIStW` . Rejected. 

- Kavosh Asadi, Dipendra Misra, and Michael L. Littman. Combating the compounding-error problem with a multi-step model. _arXiv preprint arXiv:1905.13320_ , 2019. URL `https://arxiv.org/abs/1905.13320` . 

- Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba, Komeili, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, and Nicolas Ballas. V-jepa 2: Self-supervised video models enable understanding, prediction and planning, 2025. 

- Marco Bagatella, Matteo Pirotta, Ahmed Touati, Alessandro Lazaric, and Andrea Tirinzoni. TD-JEPA: Latent-predictive representations for zero-shot reinforcement learning. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL `https://openreview.net/forum?id=SzXDuBN8M1` . 

- Federico Baldassarre, Marc Szafraniec, Basile Terver, Vasil Khalidov, Francisco Massa, Yann LeCun, Patrick Labatut, Maximilian Seitzer, and Piotr Bojanowski. Back to the features: Dino as a foundation for video world models, 2025. URL `https://arxiv.org/abs/2507.19468` . 

- Philip J. Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, Agrim Gupta, Kristian Holsheimer, Aleksander Holynski, Jiri Hron, Christos Kaplanis, Marjorie Limont, Matt McGill, Yanko Oliveira, Jack Parker-Holder, Frank Perbet, Guy Scully, Jeremy Shar, Stephen Spencer, Omer Tov, Ruben Villegas, Emma Wang, Jessica Yung, Cip Baetu, Jordi Berbel, David Bridson, Jake Bruce, Gavin Buttimore, Sarah Chakera, Bilva Chandra, Paul Collins, Alex Cullum, Bogdan Damoc, Vibha Dasagi, Maxime Gazeau, Charles Gbadamosi, Woohyun Han, Ed Hirst, Ashyana Kachra, Lucie Kerley, Kristian Kjems, Eva Knoepfel, Vika Koriakin, Jessica Lo, Cong Lu, Zeb Mehring, Alex Moufarek, Henna Nandwani, Valeria Oliveira, Fabio Pardo, Jane Park, Andrew Pierson, Ben Poole, Helen Ran, Tim Salimans, Manuel Sanchez, Igor Saprykin, Amy Shen, Sailesh Sidhwani, Duncan Smith, Joe Stanton, Hamish Tomlinson, Dimple Vijaykumar, Luyu Wang, Piers Wingfield, Nat Wong, Keyang Xu, Christopher Yew, Nick Young, Vadim Zubov, Douglas Eck, Dumitru Erhan, Koray Kavukcuoglu, Demis Hassabis, Zoubin Gharamani, Raia Hadsell, Aäron van den Oord, Inbar Mosseri, Adrian Bolton, Satinder Singh, and Tim Rocktäschel. Genie 3: A new frontier for world models. 2025. 

- Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation world models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 15791–15801, June 2025. 

- Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mido Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video, 2024. ISSN 2835-8856. 

- Florent Bartoccioni, Elias Ramzi, Victor Besnier, Shashanka Venkataramanan, Tuan-Hung Vu, Yihong Xu, Loick Chambon, Spyros Gidaris, Serkan Odabas, David Hurych, Renaud Marlet, Alexandre Boulch, Mickael Chen, Éloi Zablocki, Andrei Bursuc, Eduardo Valle, and Matthieu Cord. Vavim and vavam: Autonomous driving through video generative modeling. _arXiv preprint arXiv:2502.15672_ , 2025. 

- Samy Bengio, Oriol Vinyals, Navdeep Jaitly, and Noam Shazeer. Scheduled sampling for sequence prediction with recurrent neural networks, 2015. URL `https://arxiv.org/abs/1506.03099` . 

14 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

- Yoshua Bengio, Patrice Simard, and Paolo Frasconi. Learning long-term dependencies with gradient descent is difficult. _IEEE Transactions on Neural Networks_ , 5(2):157–166, 1994. 

- Pauline Bennet, Carola Doerr, Antoine Moreau, Jeremy Rapin, Fabien Teytaud, and Olivier Teytaud. Nevergrad: black-box optimization platform. _SIGEVOlution_ , 14(1):8–15, April 2021. doi: 10.1145/3460310. 3460312. URL `https://doi.org/10.1145/3460310.3460312` . 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL `https://arxiv.org/abs/2410.24164` . 

- Francesco Borrelli, Alberto Bemporad, and Manfred Morari. _Predictive Control for Linear and Hybrid Systems_ . Cambridge University Press, USA, 1st edition, 2017. ISBN 1107652871. 

- Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, et al. Video generation models as world simulators, 2024. URL `https: //openai.com/research/video-generation-modelsas-world-simulators` . 

- Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Matthew Chignoli, Donghyun Kim, Elijah Stanger-Jones, and Sangbae Kim. The mit humanoid robot: Design, motion planning, and control for acrobatic behaviors. In _2020 IEEE-RAS 20th International Conference on Humanoid Robots (Humanoids)_ , pp. 1–8. doi: 10.1109/HUMANOIDS47582.2021.9555782. 

- Timothée Darcet, Maxime Oquab, Julien Mairal, and Piotr Bojanowski. Vision transformers need registers. In _ICRL_ , 2024. 

- Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In _International Conference on Learning Representations_ , 2021. 

- Jeffrey L. Elman. Finding structure in time. _Cognitive Science_ , 14(2):179–211, 1990. ISSN 0364-0213. doi: https://doi.org/10.1016/0364-0213(90)90002-E. URL `https://www.sciencedirect.com/science/ article/pii/036402139090002E` . 

- Alexander Khazatsky et al. Droid: A large-scale in-the-wild robot manipulation dataset, 2024. 

- Anthony Brohan et al. Rt-1: Robotics transformer for real-world control at scale, 2023. 

- Kuan Fang, Patrick Yin, Ashvin Nair, and Sergey Levine. Planning to practice: Efficient online fine-tuning by composing goals in latent space. In _ICLR 2022 Workshop on Generalizable Policy Learning in Physical World_ , 2022a. 

- Kuan Fang, Patrick Yin, Ashvin Nair, Homer Rich Walke, Gengchen Yan, and Sergey Levine. Generalization with lossy affordances: Leveraging broad offline data for learning visuomotor tasks. In _6th Annual Conference on Robot Learning_ , 2022b. 

- Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4rl: Datasets for deep datadriven reinforcement learning. _arXiv preprint arXiv:2004.07219_ , 2020. 

15 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

- Scott Fujimoto, Herke van Hoof, and David Meger. Addressing function approximation error in actor-critic methods. In Jennifer Dy and Andreas Krause (eds.), _Proceedings of the 35th International Conference on Machine Learning_ , volume 80 of _Proceedings of Machine Learning Research_ , pp. 1587–1596. PMLR, 10–15 Jul 2018. 

- Pascale Fung, Yoram Bachrach, Asli Celikyilmaz, Kamalika Chaudhuri, Delong Chen, Willy Chung, Emmanuel Dupoux, Hongyu Gong, Hervé Jégou, Alessandro Lazaric, Arjun Majumdar, Andrea Madotto, Franziska Meier, Florian Metze, Louis-Philippe Morency, Théo Moutakanni, Juan Pino, Basile Terver, Joseph Tighe, Paden Tomasello, and Jitendra Malik. Embodied ai agents: Modeling the world, 2025. URL `https://arxiv.org/abs/2506.22355` . 

- C. E. Garcia, D. M. Prett, and M. Morari. Model predictive control: theory and practice—a survey. _Automatica_ , 25(3):335–348, May 1989. ISSN 0005-1098. doi: 10.1016/0005-1098(89)90002-2. URL `https: //doi.org/10.1016/0005-1098(89)90002-2` . 

- Quentin Garrido, Mahmoud Assran, Nicolas Ballas, Adrien Bardes, Laurent Najman, and Yann LeCun. Learning and leveraging world models in visual representation learning, 2024. 

- Zhaohan Guo, Shantanu Thakoor, Miruna Pislar, Bernardo Avila Pires, Florent Altché, Corentin Tallec, Alaa Saade, Daniele Calandriello, Jean-Bastien Grill, Yunhao Tang, Michal Valko, Remi Munos, Mohammad Gheshlaghi Azar, and Bilal Piot. Byol-explore: Exploration by bootstrapped prediction. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), _Advances in Neural Information Processing Systems_ , volume 35, pp. 31855–31870, 2022. 

- David Ha and Jürgen Schmidhuber. Recurrent world models facilitate policy evolution. In S. Bengio, H. Wallach, H. Larochelle, K. Grauman, N. Cesa-Bianchi, and R. Garnett (eds.), _Advances in Neural Information Processing Systems_ , volume 31, 2018. 

- Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _ICML_ , volume 80, pp. 1856–1865. PMLR, 2018. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _Proceedings of the 36th International Conference on Machine Learning_ , volume 97, pp. 2555–2565. PMLR, 2019. 

- Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2020. URL `https://openreview.net/forum?id=S1lOTC4tDS` . 

- Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2021. URL `https: //openreview.net/forum?id=0oabwyZbOu` . 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models, 2024. 

- N. Hansen and A. Ostermeier. Adapting arbitrary normal mutation distributions in evolution strategies: the covariance matrix adaptation. In _Proceedings of IEEE International Conference on Evolutionary Computation_ , pp. 312–317, 1996. doi: 10.1109/ICEC.1996.542381. 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- Nikolaus Hansen. The cma evolution strategy: A tutorial, 2023. URL `https://arxiv.org/abs/1604.00772` . 

- Nikolaus Hansen, Youhei Akimoto, and Petr Baudis. CMA-ES/pycma on Github. Zenodo, DOI:10.5281/zenodo.2559634, February 2019. URL `https://doi.org/10.5281/zenodo.2559634` . 

16 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

- Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving, 2023. URL `https:// arxiv.org/abs/2309.17080` . 

- S. Hutchinson, G. Hager, and P. Corke. A tutorial on visual servo control. _IEEE Trans. on Robotics and Automation_ , 12(5):651–670, October 1996. 

- Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachy Groom, Hunter Hancock, Karol Hausman, Gashon Hussein, Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim Jones, Ben Katz, Liyiming Ke, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow, James Tanner, Marcel Torne, Quan Vuong, Anna Walling, Haohuan Wang, Blake Williams, Sukwon Yoo, Lili Yu, Ury Zhilinsky, and Zhiyuan Zhou. _π_ 0<sup>_∗_</sup> _._ 6<sup>:avlathatlearnsfromexperience,2025a.URL</sup> `https://arxiv.org/abs/2511.14759` . 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with openworld generalization, 2025b. URL `https://arxiv.org/abs/2504.16054` . 

- Herbert Jaeger. Tutorial on training recurrent neural networks, covering bppt, rtrl, ekf and the echo state network approach. _GMD-Forschungszentrum Informationstechnik, 2002._ , 5, 01 2002. 

- Michael Janner, Yilun Du, Joshua Tenenbaum, and Sergey Levine. Planning with diffusion for flexible behavior synthesis. In _ICML_ , 2022. 

- Yann LeCun. A path towards autonomous machine intelligence. _Open Review_ , Jun 2022. 

- Jinning Li, Chen Tang, Masayoshi Tomizuka, and Wei Zhan. Hierarchical planning through goal-conditioned offline reinforcement learning, 2022. 

- Avadesh Meduri, Paarth Shah, Julian Viereck, Majid Khadiv, Ioannis Havoutis, and Ludovic Righetti. Biconmp: A nonlinear model predictive control framework for whole body motion planning. _IEEE Transactions on Robotics_ , 39:905–922, 2022. URL `https://api.semanticscholar.org/CorpusID:246035621` . 

- Russell Mendonca, Oleh Rybkin, Kostas Daniilidis, Danijar Hafner, and Deepak Pathak. Discovering and achieving goals via world models. In M. Ranzato, A. Beygelzimer, Y. Dauphin, P.S. Liang, and J. Wortman Vaughan (eds.), _Advances in Neural Information Processing Systems_ , volume 34, pp. 24379–24391, 2021. 

- Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos, 2023. 

- Takeru Miyato, Toshiki Kataoka, Masanori Koyama, and Yuichi Yoshida. Spectral normalization for generative adversarial networks. In _International Conference on Learning Representations_ , 2018. URL `https://openreview.net/forum?id=B1QRgziT-` . 

- Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A. Rusu, Joel Veness, Marc G. Bellemare, Alex Graves, Martin Riedmiller, Andreas K. Fidjeland, Georg Ostrovski, Stig Petersen, Charles Beattie, Amir Sadik, Ioannis Antonoglou, Helen King, Dharshan Kumaran, Daan Wierstra, Shane Legg, and Demis Hassabis. Human-level control through deep reinforcement learning. _Nature_ , 518:529–533, 2015. 

- Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, Alex Graves, Timothy Lillicrap, Tim Harley, David Silver, and Koray Kavukcuoglu. Asynchronous methods for deep reinforcement learning. In _Proceedings of The 33rd International Conference on Machine Learning_ , volume 48 of _Proceedings of Machine Learning Research_ , pp. 1928–1937. PMLR, 20–22 Jun 2016. 

17 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

- Vivek Myers, Bill Zheng, Benjamin Eysenbach, and Sergey Levine. Offline goal-conditioned reinforcement learning with quasimetric representations. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL `https://openreview.net/forum?id=P23UMiw7iJ` . 

- Suraj Nair and Chelsea Finn. Hierarchical foresight: Self-supervised learning of long-horizon tasks via visual subgoal generation. In _International Conference on Learning Representations_ , 2020. 

- Soroush Nasiriany, Vitchyr H. Pong, Steven Lin, and Sergey Levine. Planning with goal-conditioned policies. In _NeurIPS_ , 2019. 

- Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. In _Robotics: Science and Systems (RSS)_ , 2024. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Seohong Park, Dibya Ghosh, Benjamin Eysenbach, and Sergey Levine. Offline goal-conditioned RL with latent states as actions. In _ICML Workshop on New Frontiers in Learning, Control, and Dynamical Systems_ , 2023. 

- Seohong Park, Tobias Kreiman, and Sergey Levine. Foundation policies with hilbert representations. In _Proceedings of the 41st International Conference on Machine Learning_ , ICML’24. JMLR.org, 2024. 

- Seohong Park, Kevin Frans, Benjamin Eysenbach, and Sergey Levine. OGBench: Benchmarking offline goalconditioned RL. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL `https://openreview.net/forum?id=M992mjgKzI` . 

- Jack Parker-Holder, Philip Ball, Jake Bruce, Vibhavari Dasagi, Kristian Holsheimer, Christos Kaplanis, Alexandre Moufarek, Guy Scully, Jeremy Shar, Jimmy Shi, Stephen Spencer, Jessica Yung, Michael Dennis, Sultan Kenjeyev, Shangbang Long, Vlad Mnih, Harris Chan, Maxime Gazeau, Bonnie Li, Fabio Pardo, Luyu Wang, Lei Zhang, Frederic Besse, Tim Harley, Anna Mitenkova, Jane Wang, Jeff Clune, Demis Hassabis, Raia Hadsell, Adrian Bolton, Satinder Singh, and Tim Rocktäschel. Genie 2: A large-scale foundation world model. 2024. URL `https://deepmind.google/discover/blog/ genie-2-a-large-scale-foundation-world-model/` . 

- Arjun Parthasarathy, Nimit Kalra, Rohun Agrawal, Yann LeCun, Oumayma Bounou, Pavel Izmailov, and Micah Goldblum. Closing the train-test gap in world models for gradient-based planning, 2025. URL `https://arxiv.org/abs/2512.09929` . 

- Razvan Pascanu, Tomas Mikolov, and Yoshua Bengio. On the difficulty of training recurrent neural networks. In _International Conference on Machine Learning_ , 2013. URL `https://arxiv.org/abs/1211.5063` . 

- Deepak Pathak, Pulkit Agrawal, Alexei A. Efros, and Trevor Darrell. Curiosity-driven exploration by selfsupervised prediction. In _Proceedings of the 34th International Conference on Machine Learning - Volume 70_ , ICML’17, pp. 2778–2787. JMLR.org, 2017. 

- William Peebles and Saining Xie. Scalable diffusion models with transformers. In _ICCV_ , 2023. 

- Stéphane Ross, Geoffrey J. Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _International Conference on Artificial Intelligence and Statistics_ , 2011. URL `https://arxiv.org/abs/1011.0686` . 

- Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap, and David Silver. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, December 2020. ISSN 1476-4687. doi: 10.1038/s41586-020-03051-4. 

18 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _CoRR_ , abs/1707.06347, 2017. 

- Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, and Deepak Pathak. Planning to explore via self-supervised world models. In _Proceedings of the 37th International Conference on Machine Learning_ , ICML’20. JMLR.org, 2020. 

- Younggyo Seo, Danijar Hafner, Hao Liu, Fangchen Liu, Stephen James, Kimin Lee, and Pieter Abbeel. Masked world models for visual control. In _6th Annual Conference on Robot Learning_ , 2022. 

- Dhruv Shah, Benjamin Eysenbach, Nicholas Rhinehart, and Sergey Levine. Rapid exploration for open-world navigation with latent goal models. In _5th Annual Conference on Robot Learning_ , 2021. 

- Oriane Siméoni, Huy V. Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, Francisco Massa, Daniel Haziza, Luca Wehrstedt, Jianyuan Wang, Timothée Darcet, Théo Moutakanni, Leonel Sentana, Claire Roberts, Andrea Vedaldi, Jamie Tolan, John Brandt, Camille Couprie, Julien Mairal, Hervé Jégou, Patrick Labatut, and Piotr Bojanowski. DINOv3, 2025. URL `https://arxiv.org/abs/2508.10104` . 

- Vlad Sobal, Wancong Zhang, Kynghyun Cho, Randall Balestriero, Tim Rudner, and Yann Lecun. Learning from reward-free offline data: A case for planning with latent dynamics models, 02 2025. 

- Aravind Srinivas, Allan Jabri, Pieter Abbeel, Sergey Levine, and Chelsea Finn. Universal planning networks: Learning generalizable representations for visuomotor control. In _ICML_ , 2018. 

- Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu. Roformer: Enhanced transformer with rotary position embedding. _Neurocomput._ , 568, 2024. 

- Erik Talvitie. Self-correcting models for model-based reinforcement learning. In _AAAI Conference on Artificial Intelligence_ , 2016. 

- Basile Terver, Randall Balestriero, Megi Dervishi, David Fan, Quentin Garrido, Tushar Nagarajan, Koustuv Sinha, Wancong Zhang, Mike Rabbat, Yann LeCun, and Amir Bar. A lightweight library for energy-based joint-embedding predictive architectures, 2026. URL `https://arxiv.org/abs/2602.03604` . 

- Leonardo F. Toso, Davit Shadunts, Yunyang Lu, Nihal Sharma, Donglin Zhan, Nam H. Nguyen, and James Anderson. Learning invariant visual representations for planning with joint-embedding predictive world models, 2026. URL `https://arxiv.org/abs/2602.18639` . 

- Aladin Virmaux and Kevin Scaman. Lipschitz regularity of deep neural networks: analysis and efficient estimation. In _Advances in Neural Information Processing Systems_ , 2018. URL `https://arxiv.org/ abs/1805.10965` . 

- Quan Vuong, Sergey Levine, Homer Rich Walke, Karl Pertsch, Anikait Singh, Ria Doshi, Charles Xu, Jianlan Luo, Liam Tan, Dhruv Shah, Chelsea Finn, Max Du, Moo Jin Kim, Alexander Khazatsky, Jonathan Heewon Yang, Tony Z. Zhao, Ken Goldberg, Ryan Hoque, Lawrence Yunliang Chen, Simeon Adebola, Gaurav S. Sukhatme, Gautam Salhotra, Shivin Dass, Lerrel Pinto, Zichen Jeff Cui, Siddhant Haldar, Anant Rai, Nur Muhammad Mahi Shafiullah, Yuke Zhu, Yifeng Zhu, Soroush Nasiriany, Shuran Song, Cheng Chi, Chuer Pan, Wolfram Burgard, Oier Mees, Chenguang Huang, Deepak Pathak, Shikhar Bahl, Russell Mendonca, Gaoyue Zhou, Mohan Kumar Srirama, Sudeep Dasari, Cewu Lu, Hao-Shu Fang, Hongjie Fang, Henrik I Christensen, Masayoshi Tomizuka, Wei Zhan, Mingyu Ding, Chenfeng Xu, Xinghao Zhu, Ran Tian, Youngwoon Lee, Dorsa Sadigh, Yuchen Cui, Suneel Belkhale, Priya Sundaresan, Trevor Darrell, Jitendra Malik, Ilija Radosavovic, Jeannette Bohg, Krishnan Srinivasan, Xiaolong Wang, Nicklas Hansen, Yueh-Hua Wu, Ge Yan, Hao Su, Jiayuan Gu, Xuanlin Li, Niko Suenderhauf, Krishan Rana, Ben BurgessLimerick, Federico Ceola, Kento Kawaharazuka, Naoaki Kanazawa, Tatsuya Matsushima, Yutaka Matsuo, Yusuke Iwasawa, Hiroki Furuta, Jihoon Oh, Tatsuya Harada, Takayuki Osa, Yujin Tang, Oliver Kroemer, Mohit Sharma, Kevin Lee Zhang, Beomjoon Kim, Yoonyoung Cho, Junhyek Han, Jaehyung Kim, Joseph J Lim, Edward Johns, Norman Di Palo, Freek Stulp, Antonin Raffin, Samuel Bustamante, João Silvério, 

19 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Abhishek Padalkar, Jan Peters, Bernhard Schölkopf, Dieter Büchler, Jan Schneider, Simon Guist, Jiajun Wu, Stephen Tian, Haochen Shi, Yunzhu Li, Yixuan Wang, Mingtong Zhang, Heni Ben Amor, Yifan Zhou, Keyvan Majd, Lionel Ott, Giulio Schiavi, Roberto Martín-Martín, Rutav Shah, Yonatan Bisk, Jeffrey T Bingham, Tianhe Yu, Vidhi Jain, Ted Xiao, Karol Hausman, Christine Chan, Alexander Herzog, Zhuo Xu, Sean Kirmani, Vincent Vanhoucke, Ryan Julian, Lisa Lee, Tianli Ding, Yevgen Chebotar, Jie Tan, Jacky Liang, Igor Mordatch, Kanishka Rao, Yao Lu, Keerthana Gopalakrishnan, Stefan Welker, Nikhil J Joshi, Coline Manon Devin, Alex Irpan, Sherry Moore, Ayzaan Wahid, Jialin Wu, Xi Chen, Paul Wohlhart, Alex Bewley, Wenxuan Zhou, Isabel Leal, Dmitry Kalashnikov, Pannag R Sanketi, Chuyuan Fu, Ying Xu, Sichun Xu, brian ichter, Jasmine Hsu, Peng Xu, Anthony Brohan, Pierre Sermanet, Nicolas Heess, Michael Ahn, Rafael Rafailov, Acorn Pooley, Kendra Byrne, Todor Davchev, Kenneth Oslund, Stefan Schaal, Ajinkya Jain, Keegan Go, Fei Xia, Jonathan Tompson, Travis Armstrong, and Danny Driess. Open x-embodiment: Robotic learning datasets and RT-x models. In _Towards Generalist Robots: Learning Paradigms for Scalable Skill Acquisition @ CoRL2023_ , 2023. 

- Manuel Watter, Jost Tobias Springenberg, Joschka Boedecker, and Martin Riedmiller. Embed to control: A locally linear latent dynamics model for control from raw images. In _NeurIPS_ , 2015. 

- Grady Williams, Andrew Aldrich, and Evangelos Theodorou. Model predictive path integral control using covariance variable importance sampling, 2015. 

- Jingjing Xu, Xu Sun, Zhiyuan Zhang, Guangxiang Zhao, and Junyang Lin. _Understanding and improving layer normalization_ . Curran Associates Inc., Red Hook, NY, USA, 2019. 

- Yingchen Xu, Rohan Chitnis, Bobak T Hashemi, Lucas Lehnert, Urun Dogan, Zheqing Zhu, and Olivier Delalleau. IQL-TD-MPC: Implicit q-learning for hierarchical model predictive control. In _ICML Workshop on New Frontiers in Learning, Control, and Dynamical Systems_ , 2023. 

- Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. In _ICLR_ , 2023. 

- Denis Yarats, Rob Fergus, Alessandro Lazaric, and Lerrel Pinto. Mastering visual continuous control: Improved data-augmented reinforcement learning. In _ICLR_ , 2022. 

- Shicheng Yin, Kaixuan Yin, Weixing Chen, Yang Liu, Guanbin Li, and Liang Lin. Ddp-wm: Disentangled dynamics prediction for efficient world models, 2026. URL `https://arxiv.org/abs/2602.01780` . 

- Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Avnish Narayan, Hayden Shively, Adithya Bellathur, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning, 2019. 

- Richard Zhang, Phillip Isola, Alexei A. Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _CVPR_ , 2018. 

- Qilong Zhao, Fan Feng, Housheng Hai, and Biwei Huang. Sparse world models: Visual world modeling with sparse representations, 2026. URL `https://openreview.net/forum?id=e0mUayPl40` . 

- Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pre-trained visual features enable zero-shot planning, 2024a. URL `https://arxiv.org/abs/2411.04983` . 

- Guangyao Zhou, Sivaramakrishnan Swaminathan, Rajkumar Vasudeva Raju, J. Swaroop Guntupalli, Wolfgang Lehrach, Joseph Ortiz, Antoine Dedieu, Miguel Lázaro-Gredilla, and Kevin Murphy. Diffusion model predictive control. _arXiv preprint arXiv:2410.05364_ , 2024b. 

- Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Martín-Martín, Abhishek Joshi, Soroush Nasiriany, Yifeng Zhu, and Kevin Lin. robosuite: A modular simulation framework and benchmark for robot learning. In _arXiv preprint arXiv:2009.12293_ , 2020. 

20 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, TsangWei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Jie Tan, Marc Toussaint, and Kourosh Darvish (eds.), _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pp. 2165–2183. PMLR, 06–09 Nov 2023. 

- Łukasz Kaiser, Mohammad Babaeizadeh, Piotr Miłos, Błażej Osiński, Roy H Campbell, Konrad Czechowski, Dumitru Erhan, Chelsea Finn, Piotr Kozakowski, Sergey Levine, Afroz Mohiuddin, Ryan Sepassi, George Tucker, and Henryk Michalewski. Model based reinforcement learning for atari. In _International Conference on Learning Representations_ , 2020. 

21 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

## **Appendix** 

|**C**|**ontents**||
|---|---|---|
|**1**|**Introduction**|**1**|
|**2**|**Related work**|**2**|
|**3**|**Background**|**4**|
|**4**|**Studied design choices**|**5**|
|**5**|**Experiments**|**7**|
||5.1<br>Evaluation Setup. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>7|
||5.2<br>Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>8|
||5.3<br>Our proposed optimum in the class of JEPA-WMs . . . . . . . . . . . . . .|. . . . . . . . . .<br>12|
|**6**|**Conclusion**|**12**|
|**A**|**ppendix**|**22**|
|**A **|**Notation**|**23**|
|**B **|**Extended Related Work**|**24**|
|**C **|**Training details**|**26**|
|**D **|**Error propagation in autoregressive latent prediction**|**31**|
|**E **|**Planning environments and datasets**|**35**|
|**F **|**Planning Optimization**|**39**|
|**G **|**Additional experiments**|**41**|
||G.1 Additional results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>41|
||G.2 Evaluation metrics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>44|
||G.3 Is there a proxy for success rate? . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>46|
||G.4 Success over epochs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>49|


22 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

## **A Notation** 

Table 3: Summary of notation used throughout this paper. 

|Symbol|Description|
|---|---|
|_Observations_|_, actions and embeddings_|
|_ot_|Observation (image frame) at time _t_|
|_at_|Action at time _t_|
|_zt_|State embedding at time _t_, i.e. _zt_ =_Eϕ,θ_(_ot_)|
|ˆ_zt_|Predicted state embedding at time _t_|
|_Model compo_|_nents_|
|_Eϕ,θ_|Encoder (visual, and optionally proprioceptive)|
|_E_<sup>_prop_</sup><br>_θ_|Proprioceptive encoder|
|_Pθ_|Predictor|
|_Aθ_|Action encoder|
|_Fϕ,θ_|Predictor unrolling function (Equations (3) and (4))|
|_Gϕ,θ_|Planning evaluation function|
|_Parameters_||
|_ϕ_|Encoder parameters (frozen)|
|_θ_|Learnable parameters (predictor, action encoder, proprioceptive encoder)|
|_Losses and o_|_bjectives_|
|_L_|Teacher-forcing training loss (Equation (1))|
|_Lk_|_k_-step rollout loss (Equation (5))|
|_L_<sup>_p_</sup><br>_α_|Planning objective (Equation (2))|
|_Lvis_, _Lprop_|Visual and proprioceptive dissimilarity metrics|
|_α_|Proprioceptive loss weight in planning|
|_Dimensional _|_and architectural parameters_|
|_D_|Embedding dimension of encoder / predictor|
|_A_|Action dimension|
|_f_|Frameskip factor|
|_fa_|Action embedding dimension (feature conditioning)|
|_h × w_|Number of spatial patches of the visual encoder|
|_B_|Training batch size|
|_Training para_|_meters_|
|_W_|Maximum teacher-forcing context length at training time|
|_W _<sup>_t_</sup>|Maximum rollout context length at training time|
|_Planning par_|_ameters (see also Table 10)_|
|_W _<sup>_p_</sup>|Maximum rollout context length at planning time|
|_H_|Planning horizon (number of predicted steps)|
|_N_|Number of candidate action trajectories|
|_J_|Number of optimizer iterations|
|_Ke_|Number of top trajectories retained (CEM)|
|_m_|Number of planned actions stepped in environment|
|_M_|Maximum number of steps per planning episode|


23 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

## **B Extended Related Work** 

**Alternative latent-space planning paradigms.** Several approaches have been proposed for planning in learned latent spaces, differing from JEPA-WMs in their dynamics model class, optimization strategy, or training assumptions. _Locally-linear latent dynamics models_ , such as Embed to Control (E2C) (Watter et al., 2015), learn a latent space where dynamics are locally linear, enabling the use of iterative Linear Quadratic Regulator (iLQR) for trajectory optimization. E2C is derived directly from an optimal control formulation in latent space and can operate on raw pixel observations without requiring explicit reward signals during training, using instead a reconstruction-based objective combined with dynamics constraints. _Gradient-based trajectory optimization_ through learned dynamics, as in Universal Planning Networks (UPN) (Srinivas et al., 2018), uses differentiable forward models to directly backpropagate planning gradients through predicted trajectories. We compare to this paradigm in our experiments (gradient descent planner in Section 5.2), finding it effective for smooth cost landscapes but prone to local minima in navigation tasks. _Diffusion-based planners_ (Janner et al., 2022; Zhou et al., 2024b) generate trajectory distributions via iterative denoising, offering multi-modal planning and implicit constraint satisfaction. While Diffuser typically requires offline RL datasets with reward annotations (Janner et al., 2022), recent work like DMPC (Zhou et al., 2024b) demonstrates diffusion-based MPC on continuous control tasks, though direct comparison with visual goalconditioned JEPA-WMs remains challenging due to different experimental settings and assumptions. Our work focuses on systematically studying design choices within the JEPA-WM framework, which offers rewardfree training from visual observations and flexible test-time goal specification—a complementary setting to these alternative paradigms. Regarding robustness to out-of-distribution trajectories, Parthasarathy et al. (2025) show that adversarial perturbations of latent states and actions during training smooth the world model’s loss landscape and substantially improve gradient-based planning on tasks that we also study (PushT, PointMaze, Wall); their approach is complementary to ours, which relies on the inherently more robust CEM planner. 

**Explicit and implicit world models.** We distinguish two paradigms for learning world models in latent space. _Explicit world models_ learn an autoregressive, action-conditioned predictor _z_ ˆ _t_ +1 = _Pθ_ ( _zt, Aθ_ ( _at_ )) that generates task-agnostic state embeddings one step at a time. Because training is decoupled from any reward or task specification, test-time planning algorithms (CEM, MPPI, gradient-based optimization) can optimize arbitrary cost functions over rolled-out trajectories in embedding space. This makes explicit models highly flexible: the cost function is fully decoupled from the learned dynamics. _Implicit world models_ fold multi-step temporal abstraction into the representation itself, bypassing the need for autoregressive rollouts. TD-JEPA (Bagatella et al., 2026) is a canonical example: it trains a _policy-conditioned_ multi-step predictor that approximates successor features, enabling zero-shot reward optimization for any reward function lying in the span of the learned features. Note that setting the discount factor _γ_ = 0 in TD-JEPA recovers one-step prediction, collapsing the model to the explicit, action-conditioned paradigm. 

_The two paradigms trade off compute allocation_ . Explicit models defer computation to test-time planning, but their training can be lightweight: JEPA-WMs that jointly learn a shallow encoder and predictor, such as PLDM (Sobal et al., 2025) or the action-conditioned video JEPA example of EB-JEPA (Terver et al., 2026), converge in as few as thousands of gradient steps on simple simulated tasks. Implicit models like TD-JEPA front-load computation into training (authors report 1-2 million gradient steps to capture longhorizon occupancies), yet at test time they can evaluate new reward functions in a single forward pass (zero-shot RL) without any search loop. _Explicit world models allow for a broader range of use cases at test time._ With an explicit world model, one can generate counterfactual trajectories in state embedding space, by hardcoding action trajectories corresponding to different future scenarios, as we showcase in Figure 2. Implicit world models like TD-JEPA are non-generative (in embedding space), hence cannot perform such counterfactual generation. Additionally, TD-JEPA relies on zero-shot RL, which allows the deployment of policies that are optimal for rewards that belong to the span of the learned feature space. With our explicit world models, since the cost functions are independent of the learned world model, we have more freedom on defining cost (reward) functions at test time, which can be any function from the feature space to R+. _A middle ground is occupied by hybrid methods_ . TD-MPC2 (Hansen et al., 2024) learns an explicit actionconditioned latent dynamics model alongside a reward predictor and a learned policy, then uses the policy 

24 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

to warm-start MPPI planning at test time. This combination retains the flexibility of explicit trajectory optimization while amortizing part of the search cost through the learned policy. Our study focuses on the explicit paradigm. A direct empirical comparison between explicit and implicit world models, including training-cost, inference-cost, and generalization trade-offs, is an important direction that we leave for future work. 

**Reward- and reconstruction-based latent world models vs. JEPA-WMs.** We provide here a permethod discussion of how established MBRL methods differ from the JEPA-WM recipe defined in the main text (training via embedding prediction only; planning via goal-distance minimization). _PlaNet_ (Hafner et al., 2019) learns a Recurrent State-Space Model (RSSM) with a deterministic recurrent component and a stochastic latent variable, trained via a variational objective combining pixel reconstruction, reward prediction, and a KL regularizer; at test time it runs CEM to maximize predicted cumulative rewards. _The Dreamer series_ (Hafner et al., 2020; 2021; 2024) inherits the RSSM but replaces online planning with an actor-critic trained entirely on imagined rollouts, still relying on reconstruction and reward prediction for the world model. _MuZero_ (Schrittwieser et al., 2020) learns a latent dynamics model, a reward predictor, and value/policy heads trained end-to-end via MCTS; its latent space is optimized solely to predict policies, values, and rewards, making it fundamentally reward-driven. _TD-MPC2_ (Hansen et al., 2024) pairs an action-conditioned latent dynamics model with a reward predictor and a learned policy used to warm-start MPPI planning, again maximizing predicted rewards. All four methods therefore rely on reward prediction, reconstruction, or both for training, and on reward maximization for planning. The reward-free, goal-conditioned nature of JEPA-WMs is both a strength (no reward engineering, flexible goal specification at test time) and a limitation (no straightforward way to optimize cumulative reward without a separate reward model). 

25 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

## **C Training details** 

**Predictor.** We train using the AdamW optimizer, with a constant learning rate on the predictor, action encoder and optional proprioceptive encoder. We use a cosine scheduler on the weight decay coefficient. For the learning rate, we use a constant learning rate without any warmup iterations. We summarize training hyperparameters common to environments in Table 4. We display the environment-specific ones in Table 5. Both the action and proprioception are first embedded with a linear kernel applied to each timestep, of input dimension action_dim or proprio_dim (equal to the unit action or proprioceptive dimension times the frameskip) and output dimension action_embed_dim or proprio_embed_dim. We stress that, for memory requirements, for our models with 6-step and _W_ = 7, the batch size is half the default batch size displayed in Table 5, which leads to longer epochs, as in Table 6. For our models trained on DROID, to compare to V-JEPA-2-AC and because of the dataset complexity compared to simulated ones, we increase the number of epochs to 315, and limit the iterations per epoch to 300, as displayed in Table 5. 

**Action conditioning of the predictor.** We study four predictor conditioning variants to inject action information in Figure 5a. The conditioning method determines where and how action embeddings are incorporated into the predictor architecture: 

- **Feature conditioning with sincos positional embeddings** : Action embeddings _Aθ_ ( _a_ ) are concatenated with visual token features _Eθ_ ( _o_ ) along the embedding dimension. Each timestep’s concatenated features are then processed with 3D sinusoidal positional embeddings. This increases the feature dimension and the hidden dimension of the predictor from _D_ to _D_ + _fa_ , where _fa_ is the action embedding dimension. 

- **Sequence conditioning with RoPE** : Actions are encoded as separate tokens and concatenated with visual tokens along the sequence dimension, keeping the predictor’s hidden dimension to _D_ (as in the encoder). Rotary Position Embeddings (RoPE) is used at each block of the predictor. 

- **Feature conditioning with RoPE** : This conditioning scheme combines feature concatenation (as in the first variant) with RoPE positional embeddings instead of sincos. 

- **AdaLN conditioning with RoPE** : Action embeddings modulate the predictor through Adaptive Layer Normalization at each transformer block. Specifically, action embeddings are projected to produce scale and shift parameters that modulate the layer normalization statistics. This approach allows action information to influence all layers of the predictor rather than only at input, potentially preventing vanishing of action information through the network. Combined with RoPE for positional encoding, this design is also more compute-efficient as it avoids increasing feature or sequence dimensions. 

One can estimate the strength of the action conditioning of the predictor by looking at the _action ratio_ , i.e., the ratio of dimensions (processed by the predictor) corresponding to action, on the total number of dimensions. With feature conditioning, this ratio is _Df_ + _<u>afa</u>_<sup>,where</sup><sup>_fa_istheactionembeddingdimension.</sup> When performing sequence conditioning, this ratio is _hw_ <u>1+1</u><sup>=</sup> 2571<sup>forstandardpatchsizes,with</sup><sup>_h_and</sup><sup>_w_</sup> being the height and width of the token grid, namely 16 (as explained in Table 7). Thus, feature conditioning typically yields a higher action ratio than sequence conditioning. 

The inductive bias we expect from these designs relates to how strongly actions can influence predictions. AdaLN’s per-layer modulation should provide the most consistent action conditioning throughout the predictor depth, which may explain its superior empirical performance, see Figure 5a. 

**Train time.** We compute the average train time per epoch for each combination of world model and dataset in Table 6. 

**Visual decoder.** We train one decoder per encoder on VideoxMix2M (Bardes et al., 2024) with a sum of L2 pixel space and perceptual loss (Zhang et al., 2018). With a ViT-S encoder, we choose a ViT-S decoder 

26 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 4: Training hyperparameters of some of the studied models common to all environments. If left empty, the hyperparameter value is the same as the leftmost column. WM-V refers to models trained with V-JEPA and V-JEPA2 encoders. 

|Hyperparameter|WM|WM-L|WM-V|
|---|---|---|---|
|_data_||||
|_W_|3|3|3|
|_f_|5|-|-|
|resolution|224|224|256|
|_optimization_||||
|lr|5e-4|-|-|
|start_weight_decay|1e-7|-|-|
|final_weight_decay|1e-6|-|-|
|AdamW _β_1|0.9|-|-|
|AdamW _β_2|0.995|-|-|
|clip_grad|1|-|-|
|_architecture_||||
|patch_size|14|-|16|
|pred_depth|6|-|-|
|pred_embed_dim|384|1024|1024|
|enc_embed_dim|384|1024|1024|
|_hardware_||||
|dtype|bfloat16|-|-|
|accelerator|H100 80G|-|-|


Table 5: Environment-specific training hyperparameters. proprio_embed_dim is used only for models using proprioception. For WM _W_ -6-step, the batch size is half the default batch size displayed here. We do not train but only evaluate DROID models on Robocasa. 

|Hyperparameter|Metaworld|Push-T|Maze|Wall|DROID|
|---|---|---|---|---|---|
|_optimization_||||||
|batch_size|256|256|128|128|128|
|epochs|50|50|50|50|315|
|_architecture_||||||
|action_dim|20|10|10|10|7|
|action_embed_dim|20|10|10|10|10|
|proprio_dim|4|4|4|4|7|
|proprio_embed_dim|20|20|20|10|10|


with depth 12. When the encoder is a ViT-L we choose a ViT-L decoder with depth 12. We train this decoder for 50 epochs with batch size 128 on trajectory slices of 8 frames. 

**State decoder.** We train a depth 6 ViT-S decoder to regress the state from one `CLS` token (Darcet et al., 2024). A linear projection at the entry projects each patch token from the frozen encoder to the right embedding dimension, 384. At the exit, a linear layer projects the `CLS` token to a vector with the same number of dimensions as the state to decode. 

**V-JEPA-2-AC reproduction.** To reproduce the V-JEPA-2-AC results, we find a bug in the code that yields the official results of the paper. The 2-step rollout loss is miscomputed, what is actually computed for this loss term is _∥Pϕ_ ( _a_ 1: _T , s_ 1 _, z_ 1) _− zT ∥_ 1 in the paper’s notations. This means that the model, when 

27 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 6: Model-specific training times in minutes per epoch on 16 H100 80 GB GPUs for Maze and Wall, on 32 H100 GPUs for Push-T and Metaworld. We denote WM-B, WM-L the variants of the base model with size ViT-B and ViT-L, WM-prop the variant with proprioception and WM-V the variant with V-JEPA encoders. For DROID, we display the train time for 10 epochs since we train for 315 epochs. 

|Model|Metaworld|Push-T|Maze|Wall|DROID|
|---|---|---|---|---|---|
|1-step|23|48|5|1|7|
|2-step|23|49|5|1|8|
|3-step|23|50|5|1|9|
|6-step|30|64|16|2|17|
|_W_ = 7|20|42|5|1|13|
|WM-B|23|50|5|1|8|
|WM-L|25|50|5|1|8|
|WM-prop|24|50|5|1|7|
|WM-V|25|60|7|2|9|


receiving as input a groundtruth embedding _z_ 1, concatenated with a prediction _z_ ˆ2, is trained to output _z_ ˆ2. We fix this bug and retrain the models. When evaluating the public checkpoint of the V-JEPA-2-AC on our DROID evaluation protocol, the action score is much lower than our retrained V-JEPA-2-AC models after bug fixing. Interestingly, the public checkpoint of the V-JEPA-2-AC predictor, although having much worse performance at planning, yields image decodings after unrolling very comparable to the fixed models, and seems to pass the simple counterfactual test, as shown in Figure 2. 

Regarding planning, VJEPA2-AC does not normalize the action space to mean 0 and variance 1, contrary to DINO-WM, so we also do not normalize with our models, for comparability to V-JEPA-2-AC. The VJEPA2AC CEM planner does clip the norm of the sampled actions to 0.1, which is below the typical std of the DROID actions. We find this clipping useful to increase planning performance and adopt it. Moreover, the authors use momentum in the update of the mean and std, which should be useful when the number of CEM iterations is high, but we do not find it to make a difference although we use 15 CEM iterations, hence do not adopt it in the planning setup on DROID. The planning procedure in V-JEPA-2-AC optimizes over four dimensions, the first three ones corresponding to the delta of the end-effector position in cartesian space, and the last one to the gripper closure. The 3 orientation dimensions of the proprioceptive state are 2 _π_ -periodic, so they often rapidly vary from a negative value above _π_ to one positive below _π_ . The actions do not have this issue and have values continuous in time. 

**Data augmentation ablations.** In V-JEPA-2-AC, the adopted random-resize-crop effectively takes a central crop with aspect ratio 1.35, instead of the original DROID (et al., 2024) aspect ratio of 1280 _/_ 720 _≃_ 1 _._ 78, and resizes it to 256x256. On simulated datasets where videos are natively of aspect ratio 1, this augmentation does not have effect. DINO-WM does not use any data augmentation. We try applying the pretraining augmentation of V-JEPA2, namely a random-resize-crop with aspect ratio in [0 _._ 75 _,_ 1 _._ 33] and scale in [0 _._ 3 _,_ 1 _._ 0], but without its random horizontal flip with probability 0.5 (which would change the action-state correspondence), and resizing to 256x256. We find this detrimental to performance, as the agent sometimes is not fully visible in the crop. 

**Ablations on models trained with video encoders.** When using V-JEPA and V-JEPA-2 encoders, before settling on training loss and encoding procedure, we perform some ablations. First, we find that the best performing loss across MSE, _L_ 1 and smooth _L_ 1 is the MSE prediction error, even though V-JEPA and V-JEPA-2 were trained with an _L_ 1 prediction error. Then, to encode the frame sequence, one could also leverage the ability of video encoders to model dependency between frames. To avoid leakage from information of future frames to past frames, we must in this case use a frame-causal attention mask in the encoder, just as in the predictor. We have a frameskip _f_ between the consecutive frames sampled from the trajectory dataset, considering them consecutive without duplicating them will result in ( _W_ + 1) _/_ 2 visual embedding timesteps. In practice, we find that duplicating each frame before encoding them as a video gives 

28 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 7: Detailed comparison of encoder configurations used in our experiments. All encoders use frozen weights during predictor training. 

|**Configuration**|**DINOv2 ViT-L**|**DINOv3 ViT-L**|**V-JEPA ViT-L**|**V-JEPA2 ViT-L**|
|---|---|---|---|---|
|_Encoder Architecture_|||||
|Encoder type|Image|Image|Video|Video|
|Model size|ViT-L/14|ViT-L/16|ViT-L/16|ViT-L/16|
|Patch embedding|Conv2d(14, 14)|Conv2d(16, 16)|Conv3d(2, 16, 16)|Conv3d(2, 16, 16)|
|Embedding dimension|1024|1024|1024|1024|
|Patches per timestep|16_×_16 = 256|16_×_16 = 256|16_×_16 = 256|16_×_16 = 256|
|Input normalization|ImageNet stats|ImageNet stats|ImageNet stats|ImageNet stats|
|Positional encoding|Sincos|RoPE|Sincos|RoPE|
|Attention mask|Full|Full|Full|Full|
|_Input Preprocessing_|||||
|Input resolution|224_×_224|256_×_256|256_×_256|256_×_256|
|Input frame count|1 per timestep|1 per timestep|2 per timestep|2 per timestep|
|Frame duplication|No|No|Yes (duplicate each)|Yes (duplicate each)|


better performance than without duplication. Still, these two alternative encoding techniques yield much lower performance than using video encoders as frame encoders by duplicating each frame and encoding each pair independently. V-JEPA-2-AC (Assran et al., 2025) does use the latter encoding technique. They encode the context video by batchifying the video and duplicating each frame, accordingly to the method which we find to work best by far on all environments. In this case, for each video of _T_ frames, the encoder processes a batch of _T_ frames, so having a full or causal attention mask is equivalent. 

**Encoder comparison details.** Given the above chosen encoding method for video encoders, we summarize the encoder configurations in Table 7. The key differences are: (1) encoder weights themselves—DINOv2/v3 trained with their several loss terms on images vs V-JEPA/2 trained with masked prediction on videos; (2) frame preprocessing—video encoders require frame duplication (each frame duplicated to form a 2-frame input); (3) patch sizes—14 for DINOv2 (256 tokens/frame, 224 resolution) vs 16 for others (256 tokens/frame, 256 resolution for V-JEPA/2, DINOv3). We use raw patch tokens without aggregation or entry/exit projections and use all encoders frozen, without any finetuning. DINOv2/v3’s superior performance on our tasks likely stems from better fine-grained object segmentation capabilities crucial for manipulation and navigation, as discussed in the main text. 

**Multistep rollout variants ablations.** We ablate several rollout strategies as illustrated in Figure 8, following the scheduled sampling (Bengio et al., 2015) and TBPTT (Jaeger, 2002) literature for sequence prediction in embedding space. When using transformers, one advantage we have compared to the classical RNN architecture, is the possibility to perform next-timestep prediction **in parallel for all timesteps** in a more computationally efficient way, thanks to a carefully designed attention mask. In our case, each timestep is a frame, made of _H × W_ patch tokens. We seek to train a predictor to minimize rollout error, similarly to training RNNs to generate text (Bengio et al., 2015). One important point is that, in our planning task, we feed a context of one state (frame and optionally proprioception) _ot_ , then recursively call the predictor as described in equation 3, equation 4 to produce a sequence of predictions _z_ ˆ _t_ +1 _, . . . ,_ ˆ _zt_ + _k_ . Since our predictor is a ViT, the input and output sequence of embeddings have same length. At each unrolling step, we only take the last timestep of the output sequence and concatenate it to the context for the next call to the predictor. We use a maximum sliding window _W_<sup>_p_</sup> of two timesteps in the context at test time, see Section 4 and Table 10. At training time, we add multistep rollout loss terms, defined in equation 5 to better align training task and unrolling task at planning time. Let us define the _order_ of a prediction as the number of calls to the predictor function required to obtain it from a groundtruth embedding. For a predicted embedding _zt_<sup>(</sup><sup>_k_)</sup> , we denote the timestep it corresponds to as _t_ and its prediction order as _k_ . There are various ways to implement such losses with a ViT predictor. 

29 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

1. Increasing order rollout illustrated in Figure 8. In this setup, the prediction order is increasing with the timestep. This strategy has two variants. 

   - (a) The “Last-gradient only" variant is the most similar to the unrolling at planning time. We concatenate the latest timestep outputted by the predictor to the context for the next unrolling step. 

   - (b) The “All-gradients" variant generalizes the previous variant, by computing strictly more (nonredundant) additional loss terms although using the same number of predictor unrolling steps. These additional loss terms correspond to other combinations of context embeddings. 

2. “Equal-order": In this variant, at each unrolling step _k_ , the predictor input is the full output of the previous unrolling step, denoted _zt_<sup>(</sup><sup>_k−_1)</sup> _, . . . , zt_<sup>(</sup> +<sup>_k−_</sup> _τ_<sup>1)</sup> , deprived of the rightmost timestep _zt_<sup>(</sup> +<sup>_k−_</sup> _τ_<sup>1)</sup> since it has no matching target groundtruth embedding _zt_ + _τ_ . 

In all the above methods, we can add sampling schedule (Bengio et al., 2015), i.e. have a probability _p_ to flip one of the context embeddings _zt_<sup>(</sup><sup>_k_)</sup> to the corresponding groundtruth embedding _zt_ . 

The takeaways from our ablations are the following: 

- The “Equal-order" strategy gives worse results. This is due to the fact that, with this implementation, the predictor does not take as input a concatenation (over time dimension) of ground truth embeddings and its predictions. Yet, at planning time, the unrolling function keeps a sliding context of ground truth embeddings as well as predictions. Hence, although this strategy uses more gradient (more timesteps have their loss computed in parallel) than the “Last-gradient only" variant, it is less aligned with the task expected from the predictor at planning time. 

- The strategy that yields best success rate is the 2-step “Last-gradient only" variant with random initial context. 

- Even though the “All-gradients" variant has an ensemble of loss terms that strictly includes the ones of the “Last-gradient only" strategy, it does not outperform it. 

- Across all strategies, we find simultaneously beneficial in terms of success rate and training time to perform TBPTT (Jaeger, 2002), detaching the gradient on all inputs before each pass in the predictor. 

In a nutshell, what matters is to train the predictor to receive as input a mix of encoder outputs and predictor outputs. This makes the predictor more aligned with the planning task, where it unrolls from some encoder outputs, then concatenates to it its own predictions. 

30 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 8: Two rollout strategies with any predictor network predicting the next timestep (frame) simultaneously for all timesteps. Predictor is used as an RNN by recursively feeding it a mix of its previous predictions and groundtruth embeddings. We vertically represent the “predictor unrolling step" dimension. For a predicted embedding _zt_<sup>(</sup><sup>_k_)</sup> , we denote the timestep it corresponds to as _t_ and its prediction order as _k_ . The embeddings that enter in the loss computation are in grey whereas those which do not are in light grey. Left: “Last-gradient-only" strategy. We sample a random groundtruth embedding prefix, ( _z_ 1 _, . . . , zt_ ) (in this figure _t_ = 2), and concatenate only the latest prediction to the predictor context at the next unrolling step. Strategy used in V-JEPA-2-AC with a groundtruth embedding prefix always equal to _z_ 1. Right: “Allgradients" strategy, we compute all available prediction tasks without redundancies, e.g. we exclude from loss computation prediction tasks that have already been included in loss computation at previous timesteps, i.e. _L_ ( _zt_<sup>(</sup><sup>_t−_1)</sup> _, zt_ ). 

## **D Error propagation in autoregressive latent prediction** 

We formalize the exponential error growth claim made in the main text. Consider the autoregressive predictor recurrence from equation 4: 


Here _w_ denotes the maximum context length during rollout (set to _W_<sup>_t_</sup> at training time and to _W_<sup>_p_</sup> at planning time, see Table 10), while _W_ +1 denotes the number of frames per training slice. Let _zi_ = _Eϕ,θ_ ( _oi_ ) denote the groundtruth embedding at step _i_ , and define the prediction error _ϵ_<sup>(</sup><sup>_k_)</sup> = _∥z_ ˆ _t_ + _k − zt_ + _k∥_ at horizon _k_ . We denote the intrinsic one-step prediction error (the residual on groundtruth inputs) by _δ_ = sup _i ∥Pθ_ ( _zi−w_ : _i, Aθ_ ( _ai−w_ : _i_ )) _− zi_ +1 _∥_ . 

**Proposition 1** (Error bound, simplified case _w_ = 0) **.** _Assume Pθ_ ( _·, Aθ_ ( _ai_ )) _is_ Λ _-Lipschitz with respect to its state input for every action ai, with ϵ_<sup>(0)</sup> = 0 _(the initial embedding is groundtruth). Then:_ 


_For_ Λ _>_ 1 _, the error grows as O_ (Λ<sup>_H_</sup> ) _, i.e., exponentially in the horizon H. For_ Λ = 1 _(isometric predictor), the error grows linearly: ϵ_<sup>(</sup><sup>_H_)</sup> _≤ H δ. For_ Λ _<_ 1 _(contractive predictor), the error saturates at δ/_ (1 _−_ Λ) _, independently of H._ 

31 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

_Proof._ From the Lipschitz property and the triangle inequality: 


Solving the linear recurrence _ϵ_<sup>(</sup><sup>_k_+1)</sup> _≤_ Λ _ϵ_<sup>(</sup><sup>_k_)</sup> + _δ_ with _ϵ_<sup>(0)</sup> = 0 yields equation 7. 

**Proposition 2** (Tightness of the bound) **.** _The upper bound in Proposition 1 is tight in the following senses._ **_(a) Achievability by affine predictors._** _For any_ Λ _>_ 0 _and δ >_ 0 _, there exist a_ Λ _-Lipschitz affine predictor Pθ on_ R _with one-step error δ and a groundtruth trajectory for which the bound in equation 7 is achieved with equality: ϵ_<sup>(</sup><sup>_k_+1)</sup> = Λ _ϵ_<sup>(</sup><sup>_k_)</sup> + _δ for all k ≥_ 0 _, giving ϵ_<sup>(</sup><sup>_H_)</sup> = _δ_ (Λ<sup>_H_</sup> _−_ 1) _/_ (Λ _−_ 1) _when_ Λ _̸_ = 1 _and ϵ_<sup>(</sup><sup>_H_)</sup> = _H δ when_ Λ = 1 _._ 

**_(b) Nonlinear predictors, lower bound._** _Suppose the Jacobian JPθ along the error trajectory has a minimal singular value σ_ min( _JPθ_ ) _≥ ℓ>_ 1 _, and the one-step error has a component of magnitude at least δ_<sup>_′_</sup> _> δ/_ ( _ℓ −_ 1) _aligned with the right singular vector corresponding to σ_ min( _JPθ_ ) _. Then ϵ_<sup>(</sup><sup>_H_)</sup> _≥_ � _δ_<sup>_′_</sup> _− δ/_ ( _ℓ −_ 1)� _ℓ_<sup>_H−_1</sup> = Ω( _ℓ_<sup>_H_</sup> ) _, giving a lower bound that matches the O_ (Λ<sup>_H_</sup> ) _upper bound in growth rate._ 

_Proof._ **Part (a).** We construct a one-dimensional example that saturates the bound. Let _z ∈_ R, define _Pθ_ ( _z_ ) = Λ _z_ + _δ_ , and let the groundtruth trajectory be constant: _zt_ + _k_ = 0 for all _k ≥_ 0. The predictor is Λ-Lipschitz since _|Pθ_ ( _x_ ) _− Pθ_ ( _y_ ) _|_ = Λ _|x − y|_ , and the one-step error on groundtruth inputs is _|Pθ_ (0) _−_ 0 _|_ = _δ_ . Since _z_ ˆ _t_ +0 = _zt_ = 0, an induction gives _z_ ˆ _t_ + _k ≥_ 0 for all _k_ (because _z_ ˆ _t_ + _k_ +1 = Λ ˆ _zt_ + _k_ + _δ ≥_ 0). At each step, the two terms in the triangle inequality equation 8 are _Pθ_ (ˆ _zt_ + _k_ ) _−Pθ_ (0) = Λ ˆ _zt_ + _k ≥_ 0 and _Pθ_ (0) _−zt_ + _k_ +1 = _δ >_ 0. Because both terms are non-negative, the triangle inequality holds with equality: _ϵ_<sup>(</sup><sup>_k_+1)</sup> = Λ _ϵ_<sup>(</sup><sup>_k_)</sup> + _δ_ . Solving this recurrence with _ϵ_<sup>(0)</sup> = 0 yields the claimed formula by direct computation. 

**Part (b).** Define the error vector _ek_ = _z_ ˆ _t_ + _k − zt_ + _k_ and the one-step residual _rk_ = _Pθ_ ( _zt_ + _k, Aθ_ ( _at_ + _k_ )) _− zt_ + _k_ +1, so that _∥rk∥≤ δ_ for all _k_ . Decomposing the error at step _k_ +1: 


By the mean value theorem, _Pθ_ (ˆ _zt_ + _k_ ) _− Pθ_ ( _zt_ + _k_ ) = _JPθ_ ( _ξk_ ) _ek_ for some _ξk_ on the segment between _zt_ + _k_ and _z_ ˆ _t_ + _k_ . Since _σ_ min� _JPθ_ ( _ξk_ )� _≥ ℓ_ along the error trajectory by assumption, the first term satisfies _∥JPθ_ ( _ξk_ ) _ek∥≥ ℓ ∥ek∥_ . Rearranging equation 9 as _JPθ_ ( _ξk_ ) _ek_ = _ek_ +1 _− rk_ and applying the triangle inequality gives _∥JPθ_ ( _ξk_ ) _ek∥≤∥ek_ +1 _∥_ + _∥rk∥_ , hence: 


By assumption the initial error satisfies _∥e_ 1 _∥≥ δ_<sup>_′_</sup> . Unrolling the recurrence equation 10 from _k_ = 1 to _k_ = _H−_ 1: 


32 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Since _δ_<sup>_′_</sup> _> δ/_ ( _ℓ −_ 1) by assumption, the leading coefficient is strictly positive, giving _∥eH ∥≥_ � _δ_<sup>_′_</sup> _− δ/_ ( _ℓ −_ 1)� _ℓ_<sup>_H−_1</sup> = Ω( _ℓ_<sup>_H_</sup> ). Combined with the _O_ (Λ<sup>_H_</sup> ) upper bound from Proposition 1, this confirms that the error grows exponentially. Note, however, that the bases may differ: _ℓ_ lower-bounds _σ_ min( _JPθ_ ) while Λ upperbounds _σ_ max( _JPθ_ ), so in general _ℓ ≤_ Λ and a gap remains between the lower bound Ω( _ℓ_<sup>_H_</sup> ) and the upper bound _O_ (Λ<sup>_H_</sup> ). The two rates coincide when the Jacobian is conformal ( _ℓ_ = Λ), e.g. for the scalar predictor constructed in Part (a). 

**Proposition 3** (Error bound with sliding window _w ≥_ 1) **.** _Let Pθ be_ Λ _j-Lipschitz with respect to its j-th state input (j_ = 0 _, . . . , w) for fixed actions. Then the error dynamics satisfy:_ 


_which is a_ ( _w_ +1) _-th order linear recurrence. The asymptotic growth rate is governed by the spectral radius ρ of the companion matrix_ 


_If ρ >_ 1 _, errors grow as O_ ( _ρ_<sup>_H_</sup> ) _. For typical neural networks without explicit contractivity regularization, ρ >_ 1 _(Miyato et al., 2018; Virmaux & Scaman, 2018; Pascanu et al., 2013)._ 

_Proof._ We adopt the convention _ϵ_<sup>(</sup><sup>_k_)</sup> = 0 for _k ≤_ 0, since all inputs at or before time _t_ are groundtruth embeddings. For _k ≥_ 0, the predicted embedding at step _t_ + _k_ +1 is ˆ _zt_ + _k_ +1 = _Pθ_ (ˆ _zt_ + _k−w_ : _t_ + _k, Aθ_ ( _at_ + _k−w_ : _t_ + _k_ )), and the corresponding groundtruth embedding satisfies _zt_ + _k_ +1 = _Pθ_ ( _zt_ + _k−w_ : _t_ + _k, Aθ_ ( _at_ + _k−w_ : _t_ + _k_ )) + _rk_ with _∥rk∥≤ δ_ . By the triangle inequality: 


To bound the first term, we change one state argument at a time. Define intermediate sequences ( _v_<sup>(</sup><sup>_m_)</sup> )<sup>_w_</sup> _m_<sup>+1</sup> =0 by setting _v_<sup>(0)</sup> = (ˆ _zt_ + _k,_ ˆ _zt_ + _k−_ 1 _, . . . ,_ ˆ _zt_ + _k−w_ ) and, for _m_ = 1 _, . . . , w_ + 1, replacing the _m_ -th most recent predicted state with its groundtruth value: 


Note that _v_<sup>(</sup><sup>_w_+1)</sup> = ( _zt_ + _k, zt_ + _k−_ 1 _, . . . , zt_ + _k−w_ ). By telescoping and using the Λ _j_ -Lipschitz property of _Pθ_ in its _j_ -th state argument (the other arguments being held fixed): 


Substituting equation 16 into equation 14 gives the recurrence _ϵ_<sup>(</sup><sup>_k_+1)</sup> _≤_<sup>�</sup><sup>_w_</sup> _j_ =0<sup>Λ</sup><sup>_j ϵ_(</sup><sup>_k−j_) +</sup><sup>_δ_.</sup> 

It remains to relate the growth rate to the spectral radius of **C** . Consider the auxiliary sequence (¯ _ϵ_<sup>(</sup><sup>_k_)</sup> ) satisfying the equality recurrence _ϵ_ ¯<sup>(</sup><sup>_k_+1)</sup> =<sup>�</sup><sup>_w_</sup> _j_ =0<sup>Λ</sup><sup>_j_¯</sup><sup>_ϵ_(</sup><sup>_k−j_) +</sup><sup>_δ_withthesameinitialconditions</sup><sup>_ϵ_¯(</sup><sup>_k_)=0for</sup> _k ≤_ 0. We have _ϵ_<sup>(</sup><sup>_k_)</sup> _≤ ϵ_ ¯<sup>(</sup><sup>_k_)</sup> for all _k ≥_ 0. Setting **e** ¯ _k_ = (¯ _ϵ_<sup>(</sup><sup>_k_)</sup> _, ϵ_ ¯<sup>(</sup><sup>_k−_1)</sup> _, . . . , ϵ_ ¯<sup>(</sup><sup>_k−w_)</sup> )<sup>_⊤_</sup> , the equality recurrence can be written in matrix form as 


33 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

where **b** = (1 _,_ 0 _, . . . ,_ 0)<sup>_⊤_</sup> and **C** is the companion matrix from the proposition statement. By unrolling, **e** ¯ _k_ = _δ_<sup>�</sup><sup>_k_</sup> _i_ =0<sup>_−_1</sup><sup>**C**</sup><sup>_i_</sup><sup>**b**.Thespectralradius</sup><sup>_ρ_=</sup><sup>_ρ_(</sup><sup>**C**)governstheasymptoticgrowthof</sup><sup>_∥_</sup><sup>**C**</sup><sup>_k∥_:forany</sup><sup>_ε>_0,</sup> there exists a constant _Mε_ such that _∥_ **C**<sup>_k_</sup> _∥≤ Mε_ ( _ρ_ + _ε_ )<sup>_k_</sup> for all _k ≥_ 0 (Gelfand’s formula). Hence _ϵ_ ¯<sup>(</sup><sup>_k_)</sup> _≤ ∥_ **e** ¯ _k∥_ = _O_ ( _ρ_<sup>_k_</sup> ), so _ϵ_<sup>(</sup><sup>_H_)</sup> _≤ ϵ_ ¯<sup>(</sup><sup>_H_)</sup> = _O_ ( _ρ_<sup>_H_</sup> ), which is exponential when _ρ >_ 1. **Remark 1** (Accuracy-robustness tradeoff and dependence on _K_ ) **.** _The k-step rollout loss Lk (see equation 5) trains Pθ on inputs z_ ˆ _that are_ ( _k−_ 1) _-order predictions. For small k, ϵ_<sup>(</sup><sup>_k−_1)</sup> _is small and the training inputs lie near the encoder manifold; for large k, ϵ_<sup>(</sup><sup>_k−_1)</sup> _may be large and the inputs drift off-manifold. Including large-k losses thus improves robustness to out-of-distribution (predicted) inputs but may reduce accuracy on in-distribution (groundtruth) inputs, a phenomenon also observed in imitation learning (Ross et al., 2011) and model-based reinforcement learning (Talvitie, 2016; Asadi et al., 2019). The error bound in Proposition 1 involves two quantities that both depend on the converged predictor Pθ, and therefore on the number of rollout steps K used for training. We write δK and_ Λ _K, where the subscript indicates that the predictor was trained with the aggregate loss_<sup>�</sup><sup>_K_</sup> _k_ =1<sup>_Lk.Thetest-timeerrorsatisfiesϵ_</sup> _K_<sup>(</sup><sup>_H_)</sup> _≤ δK_ (Λ<sup>_H_</sup> _K_<sup>_−_1)</sup><sup>_/_(Λ</sup><sup>_K−_1)</sup><sup>_._</sup> 

**_Effect of_** _K_ **_on_** _δK_ **_._** _The predictor Pθ is a single function optimized under the aggregate loss_<sup>�</sup><sup>_K_</sup> _k_ =1<sup>_Lk._</sup> _Each term Lk trains Pθ on a different input distribution: L_ 1 _uses groundtruth embeddings z ∈M (the encoder manifold), while Lk for k >_ 1 _uses_ ( _k−_ 1) _-order predictions z_ ˆ _that lie at distance ϵ_<sup>(</sup><sup>_k−_1)</sup> _from M. With finite model capacity, distributing the optimization across input distributions that are increasingly far from M reduces specialization on M itself. We therefore expect δK, the one-step error on groundtruth inputs, to be non-decreasing in K._ 

**_Effect of_** _K_ **_on_** Λ _K_ **_._** _Note that we use truncated backpropagation through time (TBPTT, see Section 4): the gradient of Lk does not flow back through all k applications of Pθ, so the multi-step loss does not directly penalize the Jacobian norm via the chain rule. Nevertheless, including Lk for large k still reduces the effective Lipschitz constant in the region visited during rollout. To see why, note that Lk trains the predictor to map_ ( _k−_ 1) _-order predictions, which lie at distance ϵ_<sup>(</sup><sup>_k−_1)</sup> _from the encoder manifold M, to the correct targets on M. As a result, Pθ produces accurate outputs over a wider neighborhood of M, which reduces the rate of variation of Pθ in directions away from M, i.e., reduces the effective Lipschitz constant_ Λ _in the neighborhood of the rollout trajectory. We therefore conjecture that the effective_ Λ _K is non-increasing in K under favorable optimization conditions._ 

**_Environment-dependent tradeoff._** _The test-time error ϵ_<sup>(</sup> _K_<sup>_H_)</sup> _≤ δK_ (Λ<sup>_H_</sup> _K_<sup>_−_1)</sup><sup>_/_(Λ</sup><sup>_K−_1)</sup><sup>_reflectsthecom-_</sup> _petition between these two effects. For clean simulated dynamics (deterministic transitions, noise-free rendering), δ_ 1 _is small and_ Λ1 _is already moderate: increasing K raises δK without proportionally reducing_ Λ _K, so the accuracy term dominates, which suggests the optimum is at small K, consistent with our experimental observations. For noisy real-world data (sensor noise, physical uncertainty, visual variability), δ_ 1 _is larger and_ Λ1 _is large: training on off-manifold inputs from large-K rollouts reduces the effective_ Λ _K, which more than compensates the increase in δK, consistent with the experimental shift of the optimum to larger K._ 

**Remark 2** (Growth regimes and Lipschitz regularization) **.** _Proposition 1 distinguishes three regimes:_ **_(i)_** Λ _<_ 1 _(contractive): errors saturate and long rollouts are stable;_ **_(ii)_** Λ = 1 _(isometric): errors grow linearly with the horizon, ϵ_<sup>(</sup><sup>_H_)</sup> _≤ Hδ;_ **_(iii)_** Λ _>_ 1 _(expansive): errors grow exponentially as O_ (Λ<sup>_H_</sup> ) _. For transformer-based predictors with residual connections, the per-block Jacobian is I_ + _Jblock, whose spectral norm is generically greater than one. Without explicit Lipschitz constraints, the overall constant satisfies_ Λ _≫_ 1 _, which places the predictor in regime_ **_(iii)_** _. Applying spectral normalization (Miyato et al., 2018) to each layer constrains_ Λ _≈_ 1 _, transitioning the predictor to regime_ **_(ii)_** _and reducing error growth from exponential to linear. In the sliding window case (Proposition 3), polynomial growth O_ ( _H_<sup>_m−_1</sup> ) _can arise when the spectral radius ρ_ = 1 _and the companion matrix_ **C** _has a Jordan block of size m >_ 1 _; however, this is a degenerate (measure-zero) configuration that is unlikely to occur in practice. Exploring Lipschitz-constrained predictors to enable longer stable rollouts is an interesting direction for future work._ 

34 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

## **E Planning environments and datasets** 

At train time, we normalize the action and optional proprioceptive input by subtracting the empirical mean and dividing by the empirical standard deviation, which are computed on each dataset. At planning time, we sample candidate actions in the normalized action space directly. When stepping the plan in the simulator, we thus denormalize the plan resulting from the optimization before stepping it in the environment. For comparability with V-JEPA-2-AC, we do not normalize actions for DROID. We stress that, in all environments considered, we are scarce in data, except for Push-T, where we have a bigger dataset, compared to the task complexity. 

**Data slicing.** We summarize dataset statistics in Table 8. Each _trajectory dataset_ (set of trajectories) is transformed into a _dataset of trajectory slices_ , with each slice of length _W_ + 1 for training. We split, at the level of trajectories, the dataset into training and validation sets, with a ratio of 0.9/0.1. Within each split, we split trajectories as follows. For each trajectory, we take the maximum number of contiguous slices of length _W_ + 1 that can be extracted from it. For a trajectory of length _L_ , we thus have _L −_ ( _W_ + 1) _f_ such slices. For DROID only, for consistency with V-JEPA-2-AC (Assran et al., 2025), we do not preslice the dataset into a slice dataset as above. This means that, after having split the set of trajectories into training and validation sets, at dataloading time, we sample uniformly a slice of length _W_ + 1 from each trajectory among the _L −_ ( _W_ +1) _f_ valid slices. If the trajectory is shorter than _W_ +1 frames, we sample a new random trajectory index and retry, until a maximum number of attempts. 

Hence, varying _W_ has a different effect on the dataset size for both the above categories. For DROID, _W_ does affect the actual number of unique trajectories seen, but does not affect the number of training iterations. For the other environments, _W_ would affect the number of training iterations, with a larger _W_ leading to fewer slices, thus smaller dataset and fewer iterations per epoch. In any case, we account for this by setting the number of training iterations per epoch to a fixed value, for all values of _W_ . We choose this value to be the number of iterations for one epoch with the default _W_ = 3 and total batch size detailed in Table 5, namely 3543 for Metaworld, 1139 for Maze, 7741 for Push-T, 418 for Wall and the default 300 for DROID, as in V-JEPA-2-AC. On DROID, setting too high _W_ leads to discarding videos shorter than _W_ + 1 frames: at _W_ = 3, we retain 99.2% of the dataset, at _W_ = 9, 96.4%, and at _W_ = 14, only 86%. For the Wall dataset, which has trajectories of length _L_ = 50, we can only increase _W_ to 9, as this requires data slices of length ( _W_ + 1) _f_ = 10 _×_ 5 = 50, where _f_ is the frameskip parameter. For datasets with longer trajectories (Push-T) or more data relative to task complexity (Maze), this effect of dataset reduction is not present and performance is essentially constant beyond _W_ = 3. 

Table 8: Datasets statistics. We denote the number of trajectories in the dataset under _Dataset Size_ , the length of trajectories under _Traj. Len. L_ . 

||Dataset Size|Traj. Len. _T_|
|---|---|---|
|PointMaze|2000|100|
|Push-T|18500|100-300|
|Wall|1920|50|
|Metaworld|12600|100|
|DROID|8000|20-50|


**DROID.** We use the same dataloader as in V-JEPA-2-AC, which defines actions as delta in measured robot positions. One could either feed all three available cameras of DROID (left, right, wrist) simultaneously (e.g. by concatenating them) or alternatively to the model. We choose to use only one view point as simultaneous input. For training, we find that allowing the batch sampler to sample from either the left or right camera allows for slightly lower validation loss than using only one of them. 

For evaluation, we collected a set of 16 videos with our own DROID setup, positioning the camera to closely match the left camera setup from the original DROID dataset. These evaluation videos specifically focus on 

35 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

object interaction and arm navigation scenarios, allowing us to assess the model’s performance on targeted manipulation tasks. 

As discussed in Section 5.1, we define the _Action Score_ as a rescaling of the opposite of the Action Error, namely 800(0 _._ 1 _− E_ ) if _E <_ 0 _._ 1 else 0, where _E_ is the Action Error. We display the Action Score in all figures discussed in Section 5.2. 

**Robocasa.** Robocasa (Nasiriany et al., 2024) is a simulation framework, based on Robosuite (Zhu et al., 2020), with several robotic embodiments, including the Franka Panda Arm, which is the robot used in the DROID dataset. Robocasa features over 2,500 3D assets across 150+ object categories and numerous interactable furniture pieces. The framework includes 100 everyday tasks and provides both human demonstrations and automated trajectory generation to efficiently expand training data. It is licensed under the MIT License. 

We evaluate DROID models on Robocasa. The already existing pick-and-place tasks require too long horizons to be solved by our current planning procedure. Hence, we need to define custom easier pick-and-place tasks where the arm and target object start closer to the target position. To get a goal frame, we need to teleoperate a trajectory to obtain successful pick-and-place trajectories. We can then use the last frame of these trajectories as goal frame for planning. We needed to tune the camera view point to roughly correspond to the DROID left or right camera viewpoint, otherwise our models were not able to unroll well a sequence of actions. We also customize the gripper to use the same RobotiQ gripper as in DROID. We collect 16 such trajectories to form our evaluation set in the kitchen scene with various object classes. We define the “Reach" condition as having the end-effector at less than 0.2 (in simulator units, corresponding to roughly 5 cms in DROID) from the target object, the “Pick" condition as having lifted the object at more than 0.05 from its initial altitude, and the “Place" condition as having the object at less than 0.15 from the target position of the object. Our teleoperated trajectories all involve three segments, namely reaching the object (segment 1), picking it up (segment 2), and placing it at the target position (segment 3), delimited by these conditions. These three segments allow to define 6 subtasks, namely “Reach-Pick-Place", “Reach-Pick", “Pick-Place", “Reach", “Pick", and “Place". The success definition of each of these tasks is as follows: 

- “Reach-Pick-Place": starting from the beginning of segment 1, success is 1 if the “Pick" and “Place" conditions are met. 

- “Reach-Pick": starting from the beginning of segment 1, success is 1 if the “Pick" condition is met. 

- “Pick-Place": starting from the beginning of segment 2, success is 1 if the “Place" condition is met. 

- “Reach": starting from the beginning of segment 1, success is 1 if the “Reach" condition is met. 

- “Pick": starting from the beginning of segment 2, success is 1 if the “Pick" condition is met. 

- “Place": starting from the beginning of segment 3, success is 1 if the “Place" condition is met. 

We focus on the “Place" and “Reach" tasks. Our models have low success rate on the “Pick" task, as they slightly misestimate the position of the end-effector, which proves crucial, especially for small objects. 

To allow for zero-shot transfer from DROID to Robocasa, we perform 5 times action repeat of the actions outputted by our DROID model, since we trained on DROID sampled at 4 fps and the control frequency of Robocasa is 20 Hz. We also rescale the actions outputted by our planner to match the action magnitude of Robocasa, namely [-1, 1] for the delta position of the end-effector in cartesian space, and [0, 1] for the gripper closure. 

**Metaworld.** The Metaworld (Yu et al., 2019) environment is licensed under the MIT License. The 42 Metaworld tasks we consider are listed in Table 9. We gather a Metaworld dataset via TD-MPC2 online agents trained on the visual and full state (39-dimensional) input from the Metaworld environment, on 42 Metaworld tasks, listed in Table 9. We launch the training of each TD-MPC2 agent for three seeds per task. The re-initialization of the environment at each new training episode is therefore different, even within a 

36 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

given seed and task. This randomness governs the initial position of the arm and of the objects present in the scene, as well as the goal positions of the arm and potential objects. Each episode has length 100. We keep the first 100 episodes of each combination of seed and task, to limit the proportion of “expert" trajectories in the dataset, thus promoting data diversity. This results in 126 buffers, each of 100 episodes, hence 12600 episodes of length 100. 

We introduce a planning evaluation procedure for each of the Metaworld tasks considered. These are longhorizon tasks that require to perform at least 60 actions to be solved, meaning it should be solvable if planning at horizon _H_ = 60 _/f_ , if using frameskip _f_ . This allows us to explore the use of JEPA-WMs in a context where MPC is a necessity. At planning time, we reset the environment with a different seed for each episode, randomizing the initial position of the arm, of the objects present in the scene, as well as the goal positions of the arm and potential objects. We then play the expert policy provided in the open-source Metaworld package for 100 steps. The last frame (and optionally proprioception) of this episode is set as the goal _og_ for the planning objective of equation 2. We then reset the environment again with the same random seed, and let the agent plan for 100 steps to reach the goal. 

|Task|Description|
|---|---|
|turn on faucet<br>sweep<br>assemble nut<br>turn off faucet<br>push<br>pull lever<br>push with stick<br>get coffee<br>pull handle side<br>pull with stick<br>disassemble nut<br>place onto shelf<br>press handle side<br>hammer<br>slide plate<br>slide plate side<br>press button wall<br>press handle<br>pull handle<br>soccer|Rotate the faucet counter-clockwise. Randomize faucet positions<br>Sweep a puck off the table. Randomize puck positions<br>Pick up a nut and place it onto a peg. Randomize nut and peg positions<br>Rotate the faucet clockwise. Randomize faucet positions<br>Push the puck to a goal. Randomize puck and goal positions<br>Pull a lever down 90 degrees. Randomize lever positions<br>Grasp a stick and push a box using the stick. Randomize stick positions.<br>Push a button on the coffee machine. Randomize the position of the coffee machine<br>Pull a handle up sideways. Randomize the handle positions<br>Grasp a stick and pull a box with the stick. Randomize stick positions<br>pick a nut out of the a peg. Randomize the nut positions<br>pick and place a puck onto a shelf. Randomize puck and shelf positions<br>Press a handle down sideways. Randomize the handle positions<br>Hammer a screw on the wall. Randomize the hammer and the screw positions<br>Slide a plate into a cabinet. Randomize the plate and cabinet positions<br>Slide a plate into a cabinet sideways. Randomize the plate and cabinet positions<br>Bypass a wall and press a button. Randomize the button positions<br>Press a handle down. Randomize the handle positions<br>Pull a handle up. Randomize the handle positions<br>Kick a soccer into the goal. Randomize the soccer and goal positions|
|retrieve plate side<br>retrieve plate<br>close drawer<br>press button top<br>reach<br>press button top wall<br>reach with wall<br>insert peg side<br>pull<br>push with wall<br>pick out of hole<br>pick&place w/ wall<br>press button<br>pick&place<br>unplug peg<br>close window<br>open door|Get a plate from the cabinet sideways. Randomize plate and cabinet positions<br>Get a plate from the cabinet. Randomize plate and cabinet positions<br>Push and close a drawer. Randomize the drawer positions<br>Press a button from the top. Randomize button positions<br>reach a goal position. Randomize the goal positions<br>Bypass a wall and press a button from the top. Randomize button positions<br>Bypass a wall and reach a goal. Randomize goal positions<br>Insert a peg sideways. Randomize peg and goal positions<br>Pull a puck to a goal. Randomize puck and goal positions<br>Bypass a wall and push a puck to a goal. Randomize puck and goal positions<br>Pick up a puck from a hole. Randomize puck and goal positions<br>Pick a puck, bypass a wall and place the puck. Randomize puck and goal positions<br>Press a button. Randomize button positions<br>Pick and place a puck to a goal. Randomize puck and goal positions<br>Unplug a peg sideways. Randomize peg positions<br>Push and close a window. Randomize window positions<br>Open a door with a revolving joint. Randomize door positions|
|close door<br>open drawer|Close a door with a revolving joint. Randomize door positions<br>Open a drawer. Randomize drawer positions|
|close box|Grasp the cover and close the box with it. Randomize the cover and box positions|
|lock door<br>pick bin|Lock the door by rotating the lock clockwise. Randomize door positions<br>Grasp the puck from one bin and place it into another bin. Randomize puck positions|


Table 9: A list of all of the Meta-World tasks and a description of each task. 

37 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

**Push-T.** In this environment introduced by (Chi et al., 2023) (MIT License), a pusher ball agent interacts with a T-shaped block. Success is achieved when both the agent and the T-block, which start from a randomly initialized state, reach a target position. For Push-T, the dataset provided in DINO-WM is made of 18500 samples, replays of the original released expert trajectories with various levels of noise. At evaluation time, we sample an initial and goal state from the validation split, such that the initial state attains the goal in _H_ steps, with _H_ the planning horizon. Indeed, otherwise, the task can require very long-horizon planning, and is not well solved with our planners. 

**PointMaze.** In this environment introduced by (Fu et al., 2020) (Apache 2.0 license), a force-actuated 2- DoF ball in the Cartesian directions _x_ and _y_ must reach a target position. The agent’s dynamics incorporate its velocity, acceleration, and inertia, making the movement realistic. The PointMaze train set is made of 2000 fully random trajectories. At evaluation time, we sample a random initial and goal state from the simulator’s sampler. 

**Wall.** This 2D navigation environment introduced in (Zhou et al., 2024a) (MIT License) features two rooms separated by a wall with a door. The agent’s task is to navigate from a randomized starting location in one room to a goal in one of the two rooms, potentially passing through the door. The Wall dataset is made of 1920 random trajectories each with 50 time steps. At planning time, we also sample a random initial and goal state from the simulator’s sampler. 

38 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

## **F Planning Optimization** 

In this section, we detail the optimization procedures for planning in our experiments. Given a modeling function _Fϕ,θ_ , a dissimilarity criterion ( _Lvis_ + _αLprop_ ), and an initial and goal observation pair _ot, og_ , we recall the objective function _L_<sup>_p_</sup> _α_<sup>(</sup><sup>_ot, at_:</sup><sup>_t_+</sup><sup>_H−_1</sup><sup>_, og_) = (</sup><sup>_Lvis_+</sup><sup>_αLprop_)(</sup><sup>_Fϕ,θ_(</sup><sup>_ot, at_:</sup><sup>_t_+</sup><sup>_H−_1)</sup><sup>_, Eϕ,θ_(</sup><sup>_og_)).</sup> 

**Model Predictive Control.** In Metaworld only we perform MPC, a procedure where replanning is allowed after executing a plan in the environment. We set the maximum number of actions that can be stepped in the environment to 100, which constitutes an episode. At each step of the episode where we plan, we use either the CEM or NG planner. 

**Cross-Entropy Method.** The CEM optimisation algorithm proceeds as in Algorithm 1. In essence, we fit parameters of a time-dependent multivariate Gaussian with diagonal covariance. 

**Algorithm 1** Cross-Entropy Method 

- 1: _µ_<sup>0</sup> _∈_ R<sup>_H×A_</sup> is zero and covariance matrix _σ_<sup>0</sup> I _∈_ R<sup>(</sup><sup>_H×A_)2</sup> is the identity. Number of optimisation steps _J_ . 

- 2: **for** _j_ = 1 to _J_ **do** 

- 3: Sample _N_ independent trajectories ( _{at, . . . , at_ + _H−_ 1 _}_ ) _∼N_ ( _µ_<sup>_j_</sup> _,_ ( _σ_<sup>_j_</sup> )<sup>2</sup> I) 

- 4: For each of the _N_ trajectories, unroll predictor to predict the resulting trajectory, _z_ ˆ _i_ = _Pθ_ (ˆ _zi−_ 1 _, ai−_ 1) _, i_ = _t_ + 1 _, . . . , t_ + _H_ . Compute cost _L_<sup>_p_</sup> _α_<sup>(</sup><sup>_ot, at_:</sup><sup>_t_+</sup><sup>_H−_1</sup><sup>_, og_)foreachcandidatetrajectory.</sup> 

- 5: Select top _Ke_ action sequences with the lowest cost, denote them ( _{at, . . . , at_ + _H−_ 1 _}_ )1 _,...,Ke_ . Update 


### 6: **end for** 

- 7: Step the first _m_ actions of _µ_<sup>_J_</sup> , where _m ≤ H_ is a planning hyperparameter in the environment. If we are in MPC mode, the process then repeats at the next time step with the new context observation. 


Figure 9: Planning a 100-steps Metaworld episode with the base DINO-WM at the end of training of WM, for the same Metaworld environment episode seed, with our two planners. We display the average objective of the top _Ke_ imagined trajectories and its standard deviation (orange), and the best imagined trajectory’s planning loss _L_<sup>_p_</sup> _α_<sup>(blue).Bottom:PlanningwithCEM.Top:PlanningwithNG.Failureepisodeforboth:</sup> with NG the arms stays stuck against the wall, hence the higher planning objective, whereas with CEM this episode fails because of imprecision around the goal position. 

**NG Planner.** We design a procedure to use any NeverGrad optimizer with our planning objective _L_<sup>_p_</sup> _α_<sup>(</sup><sup>_ot, at_:</sup><sup>_t_+</sup><sup>_H−_1</sup><sup>_, og_),withthesamenumberofactiontrajectoriesevaluatedinparallelandtotalbudget</sup> as CEM, as detailed in Algorithm 2. As discussed in Section 5.2, in all the evaluation setups we consider in 

39 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

this study, the NGOpt meta-optimizer always chooses the diagonal variant of the CMA-ES algorithm with a particular parameterization. The diagonal version of CMA is advised when the search space is big. We stress that after trying other parameterizations of the Diagonal CMA algorithm, like its elitist version (with a scale factor of 0.895 instead of 1, which is the default value), success rate can drop by 20% on Wall, Maze and Push-T. 

### **Algorithm 2** NeverGrad <u>planner</u> 

- 1: `optimizer` chosen by `nevergrad.optimizers.NGOpt` from budget _N × J_ , on space R<sup>_H×A_</sup> , with _N_ workers. 

- 2: **for** _j_ = 1 to _J_ **do** 

- 3: `optimizer.ask()` _N_ trajectories sequentially. 

- 4: For each of the _N_ trajectories, unroll predictor to predict the resulting trajectory, _z_ ˆ _i_ = _Pθ_ (ˆ _zi−_ 1 _, ai−_ 1) _, i_ = _t_ + 1 _, . . . , t_ + _H_ . Compute cost _L_<sup>_p_</sup> _α_<sup>(</sup><sup>_ot, at_:</sup><sup>_t_+</sup><sup>_H−_1</sup><sup>_, og_)foreachcandidatetrajectory.</sup> 

- 5: `optimizer.tell()` the cost _L_<sup>_p_</sup> _α_<sup>(</sup><sup>_ot, at_:</sup><sup>_t_+</sup><sup>_H−_1</sup><sup>_, og_)ofthe</sup><sup>_N_trajectoriessequentially.</sup> 

- 6: **end for** 

- 7: Step the first _m_ actions of `optimizer.provide_recommendation()` , where _m ≤ H_ is a planning hyperparameter in the environment. If we are in MPC mode, the process then repeats at the next time step with the new context observation. 

**Gradient Descent Planner.** We also experiment with gradient-based planners that directly optimize the action sequence through backpropagation. Unlike sampling-based methods (CEM, NG), these planners leverage the differentiability of the world model to compute gradients of the planning objective _L_<sup>_p_</sup> _α_<sup>with</sup> respect to actions. The Gradient Descent (GD) planner initializes actions either from a standard Gaussian (scaled by _σ_ 0) or from zero, then performs _J_ gradient descent steps with learning rate _λ_ . After each gradient step, Gaussian noise with standard deviation _σ_ noise is added to the actions to encourage exploration and help escape local minima. Action clipping is applied to enforce bounds on specific action dimensions. The default hyperparameters are _J_ = 500 iterations, _λ_ = 1, _σ_ 0 = 1, and _σ_ noise = 0 _._ 003. 

**Adam Planner.** The Adam planner extends the GD planner by using the Adam optimizer instead of vanilla stochastic gradient descent. Adam maintains exponential moving averages of the gradient (first moment) and squared gradient (second moment), which can provide more stable optimization dynamics. The default hyperparameters are _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 995, _ϵ_ = 10<sup>_−_8</sup> , with the same defaults as GD for other parameters ( _J_ = 500, _λ_ = 1, _σ_ 0 = 1, _σ_ noise = 0 _._ 003). 

**Planning hyperparameters.** We display in Table 10 the hyperparameters used to plan on each environment. We keep the planning hyperparameters of DINO-WM (Zhou et al., 2024a) for Push-T, Wall and Maze, but reduce the number of “top" actions, denoted _Ke_ , to 10 instead of 30. We obtain these parameters after careful grid search on DINO-WM. The success rate is very sensitive to these parameters, keeping the world model fixed. 

40 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 10: Environment-specific hyperparameters for planning, corresponding to the notations of Section F. The number of steps per planning episode is denoted _M_ and the frameskip is denoted _f_ . _H_ is the planning horizon, _m_ the number of actions to step in the environment, _Ke_ the number of top actions in CEM, _N_ the number of trajectories evaluated in parallel, _J_ the number of iterations of the optimizer. The total number of replanning steps for an evaluation episode is _fmM_<sup>.</sup> 

||_N_|_H_|_m_|_Ke_|_J_|_W _<sup>_p_</sup>|_f_|_M_|
|---|---|---|---|---|---|---|---|---|
|PointMaze|300|6|6|10|30|2|5|30|
|Push-T|300|6|6|10|30|2|5|30|
|Wall|300|6|6|10|30|2|5|30|
|Metaworld|300|6|3|10|15|2|5|100|
|Robocasa|300|3|1|10|15|2|5|60|
|DROID|300|3|3|10|15|2|1|_m_|


## **G Additional experiments** 

### **G.1 Additional results** 

**Equalized action ratio experiments.** To isolate the effect of the conditioning scheme from capacity differences due to action ratio, we train new models for each of the considered environments where we downscale the image resolution to 128 _×_ 128 with a DINOv3-L encoder (patch size 16), yielding 8 _×_ 8 = 64 visual patches. This produces matched action ratios: sequence conditioning achieves 1 _/_ ( _hw_ +1) = 1 _/_ 65, while feature conditioning achieves _fa/_ ( _D_ + _fa_ ) = 16 _/_ 1040. Both variants use the same predictor architecture, RoPE positional encoding, frozen encoder, and training data. 

_Results reveal task-dependent preferences_ : Sequence conditioning outperforms feature conditioning on DROID, Robocasa, and Metaworld (3D manipulation tasks). Conversely, feature conditioning significantly outperforms on Wall (2D navigation). Performance is comparable on Maze and Push-T. Notably, the Wall result replicates the trend from Figure 5a (different resolution/model size), confirming statistical robustness. 

We cannot provide a precise explanation of the underlying mechanism explaining why we observe such differences. What we can say for sure is that, despite matched action ratios, the conditioning schemes differ fundamentally in how action information propagates: 

- _Feature conditioning_ : Action embeddings are concatenated to each visual token. At the first transformer block, action-visual mixing occurs only within the MLP (after self-attention), which combines information across embedding dimensions but processes each spatial token separately. 

- _Sequence conditioning_ : The action token participates in self-attention from the first block, allowing immediate broadcasting to all visual tokens through attention mechanisms. 

_Observations on Wall task_ : Training and validation rollout losses are identical between methods, indicating both models predict dynamics equally well. However, during planning, sequence-conditioned models occasionally select very high magnitude actions, while feature-conditioned models consistently choose moderate actions. This suggests the conditioning scheme affects not only prediction but also the structure of the learned latent dynamics relevant for planning. 

We hypothesize that for spatially simple tasks (Wall), feature conditioning’s direct action-to-token pathway yields dynamics better suited for planning optimization, while sequence conditioning’s attention-based routing is more beneficial for complex spatial reasoning in manipulation. However, further analysis would be needed to conclusively establish this mechanism. 

**Additional planner ablations.** In Table 11, we compare the performance of our model to the DINO-WM and VJEPA-2-AC baselines across all planner configurations tested in Figure 3. Our optimal JEPA-WM consistently outperforms the baselines on most tasks and planners, as in Table 2. 

41 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 11: Comparison of different models across all planner configurations. MW-R and MW-RW denote the Reach and Reach-Wall tasks of Metaworld. Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. In **bold** is the best of the three models for a given planning optimizer, <u>underlined</u> is the best across all planning optimizers. 

|Model|Planner|Maze|Wall|Push-T|MW-R|MW-RW|Rc-R|Rc-Pl|DROID|
|---|---|---|---|---|---|---|---|---|---|
|CEM _L_2|DWM<br>VJ2AC<br>Ours|81.6 (3.4)<br>—<br>**83.9 (2.3)**|64.1 (4.6)<br>—<br>**78.8 (3.9)**|66.0 (4.7)<br>—<br>**70.2 (2.8)**|44.8 (8.9)<br>—<br>**58.2 (9.3)**|35.1 (9.4)<br>—<br>**41.6 (10.0)**|19.1 (13.4)<br>16.2 (8.3)<br>**25.4 (16.6)**|21.7 (7.2)<br>**33.1 (7.2)**<br>30.7 (8.0)|39.4 (2.1)<br>42.9 (2.5)<br>**48.2 (1.8)**|
|CEM _L_1|DWM<br>VJ2AC<br>Ours|78.8 (2.9)<br>—<br>**79.7 (3.1)**|**48.7 (4.0)**<br>—<br>46.7 (3.6)|61.6 (4.5)<br>—<br>**63.4 (2.1)**|45.1 (10.4)<br>—<br>**55.1 (8.5)**|34.0 (9.1)<br>—<br>**40.8 (9.2)**|14.4 (11.3)<br>13.2 (10.3)<br>**17.6 (12.3)**|19.6 (7.4)<br>**30.9 (7.3)**<br>30.5 (8.7)|41.7 (2.7)<br>38.5 (5.7)<br>**47.2 (1.8)**|
|NG _L_2|DWM<br>VJ2AC|54.2 (3.8)<br>—|25.3 (4.2)<br>—|47.6 (5.4)<br>—|28.1 (7.8)<br>—|**27.9 (10.0)**<br>—|25.8 (16.7)<br>22.1 (8.9)|27.1 (8.6)<br>31.1 (7.0)|36.0 (3.6)<br>36.2 (3.2)|
||Ours|**72.7 (4.5)**|**35.4 (5.9)**|**48.0 (3.0)**|**29.3 (8.6)**|21.0 (7.7)|**30.5 (10.7)**|**36.9 (9.1)**|**39.9 (1.9)**|
|NG _L_1|DWM<br>VJ2AC|52.3 (4.0)<br>—|24.6 (5.2)<br>—|46.2 (5.1)<br>—|27.5 (8.5)<br>—|**28.6 (8.9)**<br>—|21.6 (15.5)<br>18.4 (11.8)|26.0 (8.0)<br>29.4 (5.1)|35.4 (3.3)<br>33.7 (3.9)|
||Ours|**69.5 (2.1)**|**30.9 (4.1)**|**48.2 (5.1)**|**27.8 (8.2)**|21.3 (8.9)|**25.7 (12.0)**|**32.0 (9.9)**|**40.0 (2.2)**|
|Adam _L_2|DWM<br>VJ2AC|14.8 (1.5)<br>—|0.1 (0.3)<br>—|8.0 (2.4)<br>—|**62.0 (8.3)**<br>—|**49.9 (9.9)**<br>—|**2.8 (3.7)**<br>0.0 (0.0)|**21.5 (8.6)**<br>5.9 (5.1)|0.0 (0.0)<br>0.0 (0.0)|
||Ours|**17.7 (3.3)**|**1.1 (1.1)**|**9.0 (2.1)**|55.3 (9.9)|39.7 (9.7)|0.0 (0.0)|10.5 (5.0)|0.0 (0.0)|
|Adam _L_1|DWM<br>VJ2AC|12.6 (2.8)<br>—|**0.1 (0.3)**<br>—|**2.1 (1.5)**<br>—|50.7 (8.5)<br>—|37.2 (8.3)<br>—|**0.9 (1.4)**<br>0.0 (0.0)|**22.1 (7.5)**<br>3.5 (2.8)|0.0 (0.0)<br>0.0 (0.0)|
||Ours|**16.1 (3.5)**|0.0 (0.2)|0.9 (0.9)|**53.2 (7.4)**|**43.1 (6.4)**|0.2 (0.7)|7.5 (3.9)|0.0 (0.0)|
|GD _L_2|DWM|14.5 (1.9)|0.1 (0.3)|8.1 (2.4)|**62.2 (8.2)**|**50.0 (10.1)**|**2.9 (3.8)**|**21.9 (8.4)**|0.0 (0.0)|
||VJ2AC|—|—|—|—|—|0.0 (0.0)|8.1 (3.6)|0.0 (0.0)|
||Ours|**17.7 (3.3)**|**1.1 (1.1)**|**9.1 (1.9)**|55.3 (9.9)|39.7 (9.7)|0.0 (0.0)|10.5 (5.0)|0.0 (0.0)|
|GD _L_1|DWM<br>VJ2AC|12.4 (2.6)<br>—|**0.1 (0.3)**<br>—|**2.0 (1.3)**<br>—|50.9 (8.5)<br>—|37.1 (8.4)<br>—|**1.0 (1.4)**<br>0.0 (0.0)|**22.2 (7.3)**<br>4.0 (2.6)|0.0 (0.0)<br>0.0 (0.0)|
||Ours|**16.1 (3.5)**|0.0 (0.2)|0.9 (0.9)|**53.3 (7.3)**|**40.1 (12.3)**|0.2 (0.7)|7.5 (3.9)|0.0 (0.0)|


For completeness, we also report in Table 12 the per-seed variance at the final checkpoint, which isolates reproducibility across random seeds from training stability. Results are consistent with Table 11, confirming that our method reliably outperforms baselines across both metrics. 

In Figure 11 (Left), we display Figure 3 again for completeness, along with Figure 11 (Right), where we compare the performance of all planners on all environments but _with proprioception_ . We adopt the default configuration described in the beginning of Section 4, namely DINO-WM ViT-S but with proprioception. We can draw the same conclusions as for without proprioception, in Figure 3. 

Let us detail the failure cases of the GD planner. On the Wall task, the GD planner gets zero performance, although the task is visually simplistic. We identify two main failure cases. Either the agent goes into the wall without being able to pass the door, which is a classical failure case for better CEM or NG planners. Or the agent finds a local planning cost minimum by going to the borders of the image, when starting close to them. We illustrate both of these in Figure 10. 

**Object manipulation on Robocasa and DROID.** We show in Figure 13 a successful planning episode with our proposed JEPA-WM on Robocasa on the “Place" task. Our model is able to perform the “Place" task but has a much lower success rate at the “Pick" task, as it misestimates the position of the arm. We illustrate the shift in camera calibration / action calibration in Figure 12 on the “Reach" task. On all episodes, the model always predicts a state shifted to the left compared to the ground-truth. This phenomenon is less clear on DROID, as we illustrate in Figure 14. 

**Object manipulation on Metaworld.** Our agent solves the pose control tasks like reach and reach-wall. In addition, long-term action unrolling with object interaction seems to be well-captured by our models, as shown in Figure 15 for the bin-picking task. Yet, for tasks involving object manipulation, it hallucinates grasping the object. In Figure 16, the visual decoding of the unrolling of the action plan shows a gap between 

42 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 12: Comparison of the final checkpoint of three methods, displaying the variance across three seeds, for all planner configurations. MW-R and MW-RW denote the Reach and Reach-Wall tasks of Metaworld. Rc-Pl and Rc-R denote the Place and Reach tasks of Robocasa. In **bold** is the best of the three models for a given planning optimizer, <u>underlined</u> is the best across all planning optimizers. 

|Model|Planner|Maze|Wall|Push-T|MW-R|MW-RW|Rc-R|Rc-Pl|DROID|
|---|---|---|---|---|---|---|---|---|---|
|CEM _L_2|DWM<br>VJ2AC<br>Ours|79.2 (2.9)<br>—<br>**83.3 (3.1)**|63.1 (2.3)<br>—<br>**80.9 (4.9)**|63.3 (3.9)<br>—<br>**69.4 (4.0)**|44.4 (5.5)<br>—<br>**49.0 (9.4)**|**31.9 (2.6)**<br>—<br>29.2 (11.5)|11.5 (7.8)<br>7.3 (6.4)<br>**22.9 (21.4)**|20.8 (9.7)<br>33.3 (5.9)<br>**34.4 (7.7)**|40.4 (1.6)<br>43.2 (1.9)<br>**46.5 (0.4)**|
|CEM _L_1|DWM<br>VJ2AC|78.3 (2.1)<br>—|**50.0 (3.7)**<br>—|**60.6 (2.2)**<br>—|**49.3 (5.5)**<br>—|**38.2 (10.4)**<br>—|13.5 (8.2)<br>8.3 (3.9)|14.6 (5.3)<br>**31.2 (6.8)**|41.6 (1.8)<br>40.9 (3.1)|
||Ours|**81.2 (4.7)**|47.6 (2.1)|55.9 (3.0)|48.4 (10.7)|30.7 (7.0)|**20.8 (22.9)**|29.2 (11.8)|**45.0 (0.3)**|
|NG _L_2|DWM<br>VJ2AC|55.6 (2.3)<br>—|25.2 (4.3)<br>—|48.8 (3.0)<br>—|**25.7 (2.0)**<br>—|**27.1 (1.7)**<br>—|20.8 (7.8)<br>18.8 (4.4)|33.3 (8.2)<br>29.2 (2.9)|35.4 (2.2)<br>35.7 (2.1)|
||Ours|**76.4 (0.5)**|**38.9 (4.2)**|**49.7 (2.7)**|23.4 (8.4)|13.0 (5.6)|**26.0 (16.6)**|**35.4 (6.4)**|**39.8 (0.7)**|
|NG _L_1|DWM<br>VJ2AC|52.3 (2.0)<br>—|23.1 (6.6)<br>—|42.1 (4.4)<br>—|**31.2 (6.1)**<br>—|**29.2 (3.4)**<br>—|**24.0 (8.2)**<br>9.4 (2.6)|28.1 (15.9)<br>28.1 (2.6)|38.4 (3.2)<br>34.0 (4.9)|
||Ours|**73.6 (3.0)**|**30.6 (1.3)**|**43.8 (0.9)**|27.6 (6.5)|12.5 (6.4)|18.8 (19.9)|**32.3 (12.6)**|**39.9 (1.3)**|
|Adam _L_2|DWM<br>VJ2AC|14.6 (3.1)<br>—|0.0 (0.0)<br>—|**8.9 (0.5)**<br>—|**60.4 (2.9)**<br>—|**44.4 (7.7)**<br>—|**7.3 (2.9)**<br>0.0 (0.0)|**24.0 (10.3)**<br>12.5 (5.1)|0.0 (0.0)<br>0.0 (0.0)|
||Ours|**21.5 (4.2)**|**1.0 (0.9)**|8.3 (0.9)|45.8 (3.9)|25.5 (10.6)|3.1 (3.1)|9.4 (3.1)|0.0 (0.0)|
|Adam _L_1|DWM|12.0 (1.6)|0.0 (0.0)|**3.1 (1.0)**|**45.8 (6.8)**|**34.7 (5.2)**|**3.1 (4.4)**|**21.9 (0.0)**|0.0 (0.0)|
||VJ2AC|—|—|—|—|—|0.0 (0.0)|4.2 (1.5)|0.0 (0.0)|
||Ours|**17.7 (1.5)**|0.0 (0.0)|1.0 (0.0)|**45.8 (2.6)**|33.9 (3.1)|0.0 (0.0)|7.8 (4.7)|0.0 (0.0)|
|GD _L_2|DWM|13.5 (2.1)|0.0 (0.0)|**8.3 (1.0)**|**61.8 (2.0)**|**45.8 (6.8)**|**7.3 (2.9)**|**25.0 (9.2)**|0.0 (0.0)|
||VJ2AC|—|—|—|—|—|0.0 (0.0)|5.2 (1.5)|0.0 (0.0)|
||Ours|**21.5 (4.2)**|**1.0 (0.9)**|**8.3 (0.9)**|45.8 (3.9)|25.5 (10.6)|3.1 (3.1)|9.4 (3.1)|0.0 (0.0)|
|GD _L_1|DWM<br>VJ2AC|12.0 (1.6)<br>—|0.0 (0.0)<br>—|**2.1 (0.0)**<br>—|**45.8 (6.8)**<br>—|**34.7 (5.2)**<br>—|**3.1 (4.4)**<br>0.0 (0.0)|**21.9 (0.0)**<br>4.2 (1.5)|0.0 (0.0)<br>0.0 (0.0)|
||Ours|**17.7 (1.5)**|0.0 (0.0)|1.0 (0.0)|**45.8 (2.6)**|33.9 (3.1)|0.0 (0.0)|7.8 (4.7)|0.0 (0.0)|


the imagined consequences of the actions and their consequences in the simulator. This calls for a separate optimization procedure for the action dimension that corresponds to the end-effector’s gripper. 

**Action precision Push-T.** The results in Figure 21 clearly show that CEM performs better than NG for the Push-T task. The Push-T task requires very precise actions, since if the ball is slightly off the position where it should be to push the T-shape, it misses the shape and fails at the task. Hence it proves essential to only step actions after convergence of the planner. Yet, we see in Figure 17 that the NG planner is more explorative and should therefore be parametrized differently for this type of task. Interestingly, the larger model converges faster and brings higher maximal success rate on this task. 

**Embedding space and model size.** We see in Figure 18 that the relative difference in embedding space distance to the goal is approximately ten times smaller in the ViT-L model than in the ViT-S model. This is consistent with the fact that the ViT-L model has a higher capacity and can therefore embed more information in its latent space, in which two states of Metaworld are closer to each other than in the ViT-S model embedding space. 

43 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 10: Two typical failure cases with the Gradient-Descent (GD) planner on the Wall task. For each failure case, we show: (top) the planned trajectory visualization, (bottom left) initial and goal states, (bottom right) planning cost evolution throughout gradient descent iterations. First failure case (top 3 subfigures): the agent finds a local planning cost minimum by going to the borders of the image when starting close to them. Second failure case (bottom 3 subfigures): the agent goes into the wall without being able to pass the door. 

### **G.2 Evaluation metrics** 

**Statistical significance.** To account for the evaluation variability, at each epoch, we launch _e_ = 96 episodes, each with a different initial and goal state, either sampled from the dataset (Push-T, Robocasa, DROID) or by the simulator (Metaworld, PointMaze, Wall). We take _e_ = 64 for evaluation on DROID, which proves essential to get a reliable evaluation, even though we compare a continuous action score metric. We use _e_ = 32 for Robocasa given the higher cost of a planning episode, which requires replanning 12 times, as 

44 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 11: Comparison of planning optimizers. NG is the Nevergrad-based interface for trajectory optimization that we introduce, CEM is the Cross-Entropy Method, and GD is the Gradient Descent Planner with _L_ 1 or _L_ 2 distance. Left: comparison of the GD, CEM and NG planners on DINO-WM without proprioception. Right: comparison of CEM and NG planners on DINO-WM with proprioception. 


Figure 12: Planning at horizon 3 with our proposed JEPA-WM on Robocasa, with our best model presented in Section 5.3. The model is trained on DROID and evaluated zero-shot on Robocasa on the “Reach" task, where the goal is to reach the object. Top: the model’s visual decoding of the action plan. Bottom: the ground-truth action stepping in simulator. The model predicts a state shifted to the left compared to the ground-truth. 

explained in Table 10. We average over these episodes to get a success rate. Although we average success at each epoch over three seeds and their evaluation episodes, we still find high variability throughout training. Hence, to get an aggregate score per model, we average success over the last _n_ training epochs, with _n_ = 10 for all datasets, except for models trained on DROID, for which _n_ = 100. The error bars displayed in the plots comparing design choices are the standard deviation across the last epochs’ success rate, to reflect this variability only. 

The metric we seek to optimize for planning tasks is the success rate, which can be noisy, highly dependent on the initial seed, and sparse at the beginning of training. We therefore derive several other useful metrics and study their correlation with the success rate. 

**Embedding space error throughout unrolling.** Throughout training, every 300 training iterations, we unroll the predictor on a batch of the validation split for _n_ steps. For each of these steps, we compute the _L_ 1 and _L_ 2 loss between the predicted embedding and the embedding of the ground truth corresponding future frame. The _L_ 2 loss at step 1 is the teacher-forcing loss term _L_ . 

45 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Init state Goal state 


Figure 13: Planning episode with our proposed JEPA-WM on Robocasa, with DINOv2 ViT-S encoder, 2-step rollout, AdaLN predictor. The model is trained on DROID and evaluated zero-shot on Robocasa on the ’place’ task. The planning cost is the embedding space distance to the goal frame embedding. 

**Proprioceptive decoding error throughout unrolling.** Prior to training of the predictors, we train a small ViT probe, called “state decoder" on top of the frozen encoder to regress the state, i.e. proprioception and optionally other simulator state information. Then, when training the predictors we study in this paper, every 300 training iterations, we unroll the predictor for _n_ steps on a batch of the validation split and use our state decoder on the predicted features. This yields _n_ state predictions, of which we compute the distance to the ground truth future _n_ states. 

**Visual decoder.** Just like the state decoder, we train a visual decoder to reconstruct, from the embeddings outputted by the frozen encoder, the associated frames. We decode each frame independently to avoid artificial consistency across frames, as the decoder is a probing tool. Indeed, in models like COSMOS (Agarwal et al., 2025), the powerful diffusion decoder accounts for beautiful visualisations, although the underlying latent world model might not be as accurate. Every 300 training iterations, we unroll the predictor on a given sequence of actions, and compare the decoding of the predicted embeddings to the ground truth future frames, both qualitatively and with the LPIPS metric (Zhang et al., 2018). 

**Action error.** To evaluate models without having to step actions in a real robot or a simulator, we compare the actions outputted by the planner and the groundtruth actions of the trajectory sampled from the dataset to define initial and goal state. On DROID, throughout training, the total action error increases, and even more if we do not clip the actions magnitude in the planner, as done in V-JEPA-2-AC, since we do not normalize the actions. This is because most of the action error comes from the gripper closure and gripper orientation action dims, as detailed in Figure 19. Hence, on DROID, we track the action error on the three first dimensions, corresponding to the end-effector position control, which is more relevant for the tasks we consider. 

### **G.3 Is there a proxy for success rate?** 

Evaluating several independent planning recipes is compute-intensive, even more so as the model size increases, as well as the planning budget _N × H × J × W_<sup>_p_</sup> , see Table 10. Hence, we look for validation metrics to track throughout the training that correlate well with the success rate. Each epoch of each model and evaluation setup (among four) is a data point with a value for a validation metric and an associated success rate. Considering each epoch as an independent sample allows us to compute the Spearman correlation between each quantitative metric and the success rate. The results in Table 13, Table 16, Table 14 and Table 15 first show that the correlation with training loss (Vis emb) is higher for the easier Wall task. Since we want to find the metric that correlates most to the success rate, we average the Spearman correlations instead of computing them on the union of data points, to avoid Simpson’s paradox. This yields the rightmost column of each table. In both environments, the metric most correlated with the success rate is the planning objective, that is, the Vis Emb loss. Interestingly, only in Metaworld, which requires better long-horizon unrolling capability, do the unroll metrics at step _H >_ 1 correlate better than step-1 metrics. 

46 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 13: Negative Spearman Correlation Coefficients between smoothed success rate and several validation metrics on Metaworld. In **bold** is highest value, <u>underlined</u> is 2nd highest. We denote the visual embedding prediction errors Vis Emb and the proprioceptive decoding error Proprio dec, at horizons _H_ from one to three. We display the mean success rate over the last 10 epochs averaged over the four eval setups in the last row. 

|Model name|WM|WM_W_|WM-prop|WM-2-step|WM-L|Mean|
|---|---|---|---|---|---|---|
|Proprio dec _H_ = 1|0.40|0.44|0.40|0.26|0.20|0.34|
|Proprio dec _H_ = 2|0.41|0.34|0.45|0.27|0.21|0.34|
|Proprio dec _H_ = 3|0.38|0.44|0.40|0.33|0.18|0.35|
|Vis emb _L_2 _H_ = 1|0.44|0.51|0.62|0.39|0.23|0.44|
|Vis emb _L_2 _H_ = 2|0.42|0.46|0.62|0.39|0.24|0.42|
|Vis emb _L_2 _H_ = 3|0.36|0.44|0.59|0.37|0.20|0.39|
|Vis emb _L_1 _H_ = 1|0.45|**0.55**|0.69|0.41|0.24|0.47|
|Vis emb _L_1 _H_ = 2|**0.45**|0.52|0.72|**0.43**|**0.25**|**0.47**|
|Vis emb _L_1 _H_ = 3|0.42|0.52|**0.72**|0.42|0.22|0.46|
|SR|29.7 ±3.8|24.9 ±7.6|**39.2 ±4.1**|28.7 ±5.8|19.4 ±5.8||


Table 14: Negative Spearman Correlation Coefficients across data points of the four eval setups between smoothed success rate and several validation metrics on the Push-T task. The rightmost mean column is the average of Spearman correlation of each model. In **bold** is highest value, <u>underlined</u> is 2nd highest. We display the mean success rate over the last 10 epochs in the last row. 

|Model name|WM|WM_W_|WM-prop|WM-2-step|WM-L|Mean|
|---|---|---|---|---|---|---|
|Proprio dec _H_ = 1|0.70|0.73|0.85|0.71|0.81|0.76|
|Proprio dec _H_ = 2|0.78|0.66|0.87|0.79|0.84|0.79|
|Proprio dec _H_ = 3|0.76|0.70|0.78|0.83|0.86|0.79|
|Vis emb _L_2 _H_ = 1|0.80|0.73|0.88|0.82|0.87|0.82|
|Vis emb _L_2 _H_ = 2|0.85|0.76|0.91|**0.84**|0.87|0.85|
|Vis emb _L_2 _H_ = 3|0.86|0.70|0.89|0.80|0.87|0.82|
|Vis emb _L_1 _H_ = 1|0.87|**0.79**|0.92|0.83|**0.90**|**0.86**|
|Vis emb _L_1 _H_ = 2|**0.88**|0.78|**0.93**|0.84|0.88|0.86|
|Vis emb _L_1 _H_ = 3|0.87|0.75|0.91|0.83|0.87|0.85|


Since we are essentially in a supervised learning setting, training a regressor of future embeddings, it is clear that lower validation prediction losses (at all unrolling steps) means a more accurate world model. This is best observed in the visual decodings of validation rollouts throughout training. 

Why the success rate does not correlate well to these losses is due to several factors. The validation prediction task is not fully aligned with the goal-conditioned planning task. The planning optimization task we use to evaluate models is a heuristic, where the objective is to minimize the embedding space distance of the last imagined state to the goal. 

As we see in DROID experiments Figure 19, letting the planner sample actions that are OOD for the predictor can severely harm the plan accuracy and occult the improvement of the predictor throughout training. Another caveat is that a better world model that does not prevent the planning procedure from getting stuck in local cost minima, as we see with the score obtained with gradient-based planners in Table 11. 

47 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

Table 15: Negative Spearman Correlation Coefficients across data points of the eight eval setups between smoothed success rate and several validation metrics on the Wall task. In **bold** is highest value, <u>underlined</u> is 2nd highest. We denote the visual embedding prediction errors Vis Emb and the proprioceptive decoding error Proprio dec, at horizons _H_ from one to three. 

|Model name|WM|WM_W_|WM-prop|WM-2-step|WM-3-step|WM-L|Mean|
|---|---|---|---|---|---|---|---|
|Proprio dec _H_ = 1|0.25|0.38|0.19|0.23|0.26|0.16|0.25|
|Proprio dec _H_ = 2|0.23|0.51|0.22|0.30|0.14|0.28|0.28|
|Proprio dec _H_ = 3|0.22|0.49|0.39|0.26|0.34|0.23|0.32|
|Vis emb _L_2 _H_ = 1|0.72|0.94|0.74|0.73|0.69|0.75|0.76|
|Vis emb _L_2 _H_ = 2|0.69|0.94|0.69|0.70|0.61|0.74|0.73|
|Vis emb _L_2 _H_ = 3|0.68|0.94|0.65|0.69|0.56|0.70|0.70|
|Vis emb _L_1 _H_ = 1|**0.78**|**0.96**|**0.81**|**0.77**|**0.73**|**0.80**|**0.81**|
|Vis emb _L_1 _H_ = 2|0.74|0.96|0.76|0.72|0.69|0.79|0.78|
|Vis emb _L_1 _H_ = 3|0.73|0.96|0.73|0.72|0.64|0.75|0.75|


Table 16: Negative Spearman Correlation Coefficients across data points of the eight eval setups between smoothed success rate and several validation metrics on the Point Maze environment. The rightmost mean column is the average of Spearman correlation of each model. In **bold** is highest value, <u>underlined</u> is 2nd highest. 

|Model name|WM|WM_W_|WM-prop|WM-2-step|WM-3-step|WM-L|Mean|
|---|---|---|---|---|---|---|---|
|Proprio dec _H_ = 1|0.15|0.19|0.15|0.14|0.25|0.09|0.16|
|Proprio dec _H_ = 2|0.13|0.21|0.10|0.35|0.23|0.21|0.21|
|Proprio dec _H_ = 3|0.10|0.34|0.25|0.10|0.27|0.10|0.19|
|Vis emb _L_2 _H_ = 1|0.43|0.50|0.82|0.53|0.42|0.19|0.48|
|Vis emb _L_2 _H_ = 2|0.23|0.24|0.74|0.50|**0.53**|0.03|0.38|
|Vis emb _L_2 _H_ = 3|0.21|0.30|0.67|0.46|0.49|0.17|0.38|
|Vis emb _L_1 _H_ = 1|**0.58**|**0.68**|**0.86**|0.54|0.38|**0.36**|**0.57**|
|Vis emb _L_1 _H_ = 2|0.37|0.49|0.78|**0.55**|0.50|0.19|0.48|
|Vis emb _L_1 _H_ = 3|0.29|0.38|0.74|0.51|0.50|0.29|0.45|


48 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 

### **G.4 Success over epochs** 

We display in Figure 20 and Figure 21 the evolution of success rate over training epochs for some of the models that compose the design choice study of this paper. 

49 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 14: Unrolling a trajectory with our proposed JEPA-WM on some of our collected Franka arm trajectories, with our best model presented in Section 5.3. For each pair of rows, the top one is the model’s visual decoding of the action unrolling, the bottom one is the ground-truth trajectory of the dataset. The model sometimes does not grasp well interaction with objects, which is the most frequent failure case. 

50 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 15: Samples of DINO-WM open-loop rollouts on the validation split, each on 18 model actions corresponding to 90 elementary actions in simulator. For each of the three pairs of rows, the groundtruth action stepping in simulator is below the decoding of the predictor rollout. 


Figure 16: Upper row: Visual decoding of the unrolling of the action plan outputted by the NG planner, at step 1 of the Metaworld episode, on the bin-picking task. The world model’s predictions resulting from the plan indicate that the object is picked. Lower row: Stepping of half of the plan in the simulator. The object is not picked and the plan leads the robotic arm to the target location without the object. 

51 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 17: Convergence of planning optimization for all 2D environments and DROID. The model evaluated is the base WM model, at the end of training. Left: episode initial and goal state. Center: CEM planner. Right: NG planner. We display the planning cost of the best trajectory throughout the optimization steps. 

52 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 18: Same Metaworld reach-wall task setup: trajectory of the Base model (bottom center), the Large model (bottom right) and the expert policy (all other subfigures). Left: expert’s executed episode first and last state at top, expert’s distance of arm to goal position in the simulator space at bottom. Center: WM ViT-S encoder embedding space _L_ 2 distance to goal, expert trajectory on top, WM planned episode at bottom. Right: WM-L encoder embedding space, expert trajectory on top, WM planned episode at bottom. 


Figure 19: Top row: model at the end of the first training epoch. Bottom row: model at the end of training. Left: visual decoding of the horizon 1 plan. Right: comparison of the actions outputted by the planner (blue) and the groundtruth actions (orange) for the 7 action dimensions. The first three dimensions correspond to end-effector position control, the three next to end-effector orientation control, the last one to the gripper closure. The action error mostly comes from the gripper and orientation control dimensions. Hence, although only the model at the end of training correctly plans to approach the gripper from the box, its total action error is higher than at the beginning of training, if we consider all 7 dimensions. 

53 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 20: Success rate evolution for several evaluation setups on all tasks, comparing image and video encoders. At each epoch, we evaluate the success rate on 96 independent episodes and report the average. We denote WM the base model for the design choice study, namely DINO-WM (Zhou et al., 2024a) without proprioception, and WM-L its Vit-L version. We display the results for the models learned on top of V-JEPA and V-JEPA2. 

54 

Published in Transactions on Machine Learning Research <u>(05/2026)</u> 


Figure 21: Success rate evolution for several evaluation setups on all tasks, comparing multistep rollout, proprioception and model size. We denote WM-B, WM-L the variants of the base model with size ViT-B and ViT-L, WM-prop the variant with proprioception, and the multistep rollout models as WM- _k_ -step. Row 1: Metaworld reach, row 2: Metaworld reach-wall, row 3: Wall, row 4: Push-T, row 5: Point Maze. At each epoch, we evaluate the success rate on 96 independent episodes and report the average. 

55 

