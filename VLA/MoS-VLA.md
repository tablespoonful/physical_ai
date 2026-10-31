---
title: "MoS-VLA: A Vision-Language-Action Model with One-Shot Skill Adaptation"
date: "2025-10-18"
authors: "Ruihan Zhao; Tyler Ingebrand; Sandeep Chinchali; Ufuk Topcu"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2510.16617
pdf: https://arxiv.org/pdf/2510.16617
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.16617)** / [論文ページ](https://arxiv.org/abs/2510.16617)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

MOS-VLA: A VISION-LANGUAGE-ACTION MODEL WITH ONE-SHOT SKILL ADAPTATION 

**Ruihan Zhao**<sup>_∗_</sup> 

University of Texas at Austin ruihan.zhao@utexas.edu 

**Tyler Ingebrand**<sup>_∗_</sup> University of Texas at Austin tyleringebrand@utexas.edu 

## **Sandeep Chinchali** 

University of Texas at Austin sandeepc@utexas.edu 

## **Ufuk Topcu** 

University of Texas at Austin utopcu@utexas.edu 

# ABSTRACT 

Vision-Language-Action (VLA) models trained on large robot datasets promise general-purpose, robust control across diverse domains and embodiments. However, existing approaches often fail out-of-the-box when deployed in novel environments, embodiments, or tasks. We introduce Mixture of Skills VLA (MoSVLA), a framework that represents robot manipulation policies as linear combinations of a finite set of learned basis functions. During pretraining, MoS-VLA jointly learns these basis functions across datasets from the Open X-Embodiment project, producing a structured skill space. At test time, adapting to a new task requires only a single expert demonstration. The corresponding skill representation is then inferred via a lightweight convex optimization problem that minimizes the L1 action error, without requiring gradient updates. This gradient-free adaptation incurs minimal overhead while enabling rapid instantiation of new skills. Empirically, MoS-VLA achieves lower action-prediction error on five out of five unseen datasets and succeeds in both simulation and real-robot tasks where a pretrained VLA model fails outright. 

**Project page** : mos-vla.github.io/ 

# 1 INTRODUCTION 

Inspired by the success of large language models, modern robotics aims to achieve generalization and human-like performance through the use of internet-scale data and large, attention-based architectures. To this end, researchers have collected enormous datasets of robotic arm trajectories (Open X-Embodiment Collaboration et al., 2023) and trained so-called vision-language-action foundation models to map natural language task descriptions and state observations to robot actions (Kim et al., 2024; Octo Model Team et al., 2024; Brohan et al., 2023b;a; Ma et al., 2024). While these models achieve acceptable performance on in-distribution tasks and lab settings, they are so far brittle to out-of-distribution data. The key challenge is that there is no preexisting dataset of robotic demonstrations analogous to the enormous amount of natural language data present on the internet, and collecting data in robotics settings is expensive and difficult to scale. Thus, there is currently not enough data to achieve generalization through scale alone. Therefore, creating a generalist robotic policy inherently requires a more principled approach to transfer. 

The current state-of-the-art approach to transfer is to finetune a pretrained vision-language-action model on a (relatively) small calibration dataset collected on the new task and/or lab setting. Often, this calibration dataset consists of 10s or 100s of expert demonstrations, and finetuning the models requires significant resources. Even parameter-efficient finetuning techniques (e.g., LoRA, QLora) (Han et al., 2024; Hu et al., 2022; Dettmers et al., 2023) inherently require significant resources as numerous forward and backward passes are required during gradient descent. 

In contrast to finetuning, we present a gradient-free adaptation method based on function encoders. The function encoder algorithm learns a set of neural network basis functions to span a space of in- 

> _∗_ Equal Contribution 

1 


Figure 1: **In-context adaptation with function encoders.** ( _Left_ ) A human expert collects one trajectory of data in the new context. ( _Middle_ ) The model is calibrated by solving a small, least absolute error optimization problem. This process takes only a few seconds, even on an RTX 3090. ( _Right_ ) The adapted model autonomously executes actions in the new environment. 

terest. In this case, the basis functions span the space of policies, where a given policy is specialized to a specific lab setting. After training, a new policy for a new lab setting is computed as a linear combination of the basis functions, where the coefficients are calculated as the solution to a least absolute error regression problem. Because the optimization space is small and well-structured, only a tiny calibration dataset consisting of one expert trajectory is needed. Furthermore, the least absolute error problem is just a linear program written in terms of the basis function outputs. Therefore, no gradient calculations are needed and the model adaptation has the smallest possible overhead: only forward passes are necessary. Lastly, due to the simplicity of least absolute error optimization, we demonstrate the ability to adapt to a new lab setting given one expert demonstration in only a few seconds, using only an RTX 3090 GPU. 

We empirically verify our approach by building on top of OpenVLA (Kim et al., 2024) and training on the RT-X dataset (Open X-Embodiment Collaboration et al., 2023). We demonstrate that our approach achieves improved accuracy on the training and evaluation datasets. Additionally, we evaluate the policies on a Franka Emika Panda robot arm in unseen lab settings in both simulation and the real world. The pretrained OpenVLA model achieves a 0% success rate due to the domain gap. In contrast, after calibrating with one expert trajectory, our approach achieves a 70 to 100% success rate across all tasks, demonstrating in-context transfer. 

## **Main Contributions:** 

- We introduce a one-shot, in-context adaptation method for vision-language-action models. Our method has a significantly reduced overhead relative to prior works because it does not require gradient computations after training. 

- We are the first to demonstrate that the function encoder algorithm is applicable to billionparameter architectures and mixed vision-language datasets. 

- We empirically validate that the proposed method outperforms baselines both on datasets and in real-world experiments. 

# 2 RELATED WORKS 

**Foundation Models for Robotics** A recent paradigm for robotics to replicate the successful formula of language models, which is internet-scale data combined with billion-parameter attentionbased architectures. The Open X-Embodiment dataset is a massive collection of robotic data designed to mimic a internet-scale training regime (Open X-Embodiment Collaboration et al., 2023). Numerous works train large transformer models using this data, which may be diffusion models (Octo Model Team et al., 2024) and/or auto-regressive (Kim et al., 2024), and tend to incorporate pretrained language and vision models such as Llama 2 (Touvron et al., 2023), Google-T5 (Raffel et al., 2020), SigLIP (Zhai et al., 2023), and DinoV2 (Oquab et al., 2024). Despite the magnitude 

2 


Figure 2: **Discrete vs. Continuous Skill Primitives.** _(Left)_ A discrete policy restricted to “right” or “up” yields inefficient, Manhattan-style paths and cannot reach all goals. _(Right)_ Continuous combinations of skills enable direct movement in any direction, allowing the robot to reach all goals. 

of resources dedicated to these approaches, empirically they fail to generalize to out-of-distribution tasks and lab settings. Furthermore, given the expense of robotic data collection and the diminishing returns implied by the so-called scaling laws (Kaplan et al., 2020), robotic foundation models require the development of more sophisticated and principled methods of transferring to new tasks and settings. We present one such method based on transfer within the span of a set of neural network basis functions (Ingebrand et al., 2025). 

**Adaptation and In-Context Learning** The principle method for adaptation is to finetune the foundation model on a relatively small dataset collected from the new setting and/or task (Kim et al., 2025). While this dataset is typically orders of magnitude smaller than the pretraining dataset, it may still consists of many trajectories collected over many tasks. Thus, there is still significant overhead in finetuning as these datasets must be collected for every new setting. Furthermore, given the size of foundation models, which are often billions of parameters, full-finetuning requires a powerful machine, often consisting of numerous GPUs. Parameter-efficient fine-tuning methods such as LoRA are used to reduce the finetuning overhead at the cost of expressivity and performance (Han et al., 2024; Hu et al., 2022; Wang et al., 2024). Nonetheless, any method with leverages gradient descent requires significant overhead, both in compute and in memory, due to the numerous forward and backward passes required for gradient descent. 

Rather than computing gradient updates, a natural solution is to append expert demonstrations as another input to the foundation model (Fu et al., 2024), in the style of in-context learning for language models (Dong et al., 2024; Min et al., 2022). As is typical for transformers, this method is quadratic in both memory and compute with respect to the expert trajectory length. In contrast to this approach, our method treats the expert trajectory as a _set_ of input-output pairs rather than a _sequence_ , which removes the need to compute attention between all data pairs. Consequently, our method is linear with respect to the expert trajectory length during an initial calibration step, and constant thereafter. 

**Skill Learning and Task Representations** Prior methods, especially from the reinforcement learning (RL) community, learn diverse skills and/or task representations. These methods often leverage information-theoretic proxy objectives such as cross entropy (Eysenbach et al., 2019; Hausman et al., 2018). Other approaches investigate how to best leverage pretrained skills for downstream tasks (Lim et al., 2019). Meta-RL aims to learn policies that are quickly adapted to new tasks (Lan et al., 2019), while zero-shot RL uses offline datasets to learn spaces of task solutions that do not require extra training at inference time (Touati & Ollivier, 2021; Ingebrand et al., 2024b). Our method is similar to these approaches in that we learn a space of policies, although we only leverage supervised learning techniques rather than dynamic programming. Additionally, our space of policies encodes different behaviors _and_ different contexts due to the visual variations between lab settings. Lastly, mixture of experts is common technique for foundation models that creates sub-networks specialized to certain tasks. Each task is routed to a different sub-network via a learned gating mechanism (Cai et al., 2025; Puigcerver et al., 2024). The intention is to lower the computational complexity of inference, since only a subset of the total parameters are active. As a consequence, only one or a few experts are active for any given input. In contrast to learning a finite _set_ of experts, our method trains basis functions to work in tandem, creating a _space_ of policies. See Figure 2 for a thought experiment motivating the use of continuous policy spaces over discrete sets. 

3 

# 3 BACKGROUND 

## 3.1 FUNCTION ENCODERS 

The function encoder algorithm (Ingebrand et al., 2025) learns basis functions for an arbitrary function space. Given a Hilbert space _H_ = _{f_ : _X → Y }_ with an inner product _⟨·, ·⟩H_ and an induced norm _|| · ||H_ , function encoders learn a set of neural network basis functions _{g_ 1 _, ..., gk}_ , where _k_ is a hyper-parameter, to span the space _H_ . Any function _f ∈H_ is represented as a linear combination of the basis functions, _f_ =<sup>�</sup><sup>_k_</sup> _i_ =1<sup>_αigi_,where</sup><sup>_α∈_R</sup><sup>_k_.Furthermore,giventhe</sup> basis functions and a function _f_ , _α_ is calculated as the solution to the least-squares minimization, _α_ := arg min _α∈_ R _k ||f −_<sup>�</sup><sup>_k_</sup> _i_ =1<sup>_αigi||_2</sup> _H_<sup>.</sup> 

The training procedure requires a set of datasets, _D_ = _{D_ 1 _, ..., Dn}_ , where each dataset _Di_ = _{xj, fi_ ( _xj_ ) _}_<sup>_m_</sup> _j_ =1<sup>isasetofinput-outputpairsforafunction</sup><sup>_fi∈H_.Thetrainingprocedureuses</sup> gradient descent. At each gradient step, the coefficients _α_ for function _fi_ are calculated by solving the least-squares minimization. Then, the function is approximated as a linear combination of the learned basis, and the loss is the error of this approximation. See Ingebrand et al. (2025) for more information. 

In contrast to the typical function encoder definitions, we will leverage Banach spaces and _L_<sup>1</sup> optimization rather than _L_<sup>2</sup> optimization. We define the coefficients as 


We use least absolute error instead of least squares because the RTX dataset is noisy. Ignoring outliers and emphasizing precise control is crucial for good performance. However, the only practical difference is the optimization procedure to compute the coefficients, where we solve a linear program instead of an unconstrained quadratic program. The rest of the algorithm remains unchanged. 

# 4 METHOD 

To enable in-context transfer with minimal overhead and minimal calibration data, we leverage the function encoder algorithm with a few modifications. For simplicity, we build upon the OpenVLA foundation model (Kim et al., 2024), although we highlight that the following approach can be applied to any model architecture. The method section is outlined as follows. In Section 4.1, we formally define in-context adaptation. In Section 4.2, we define the core technical idea of our approach. In Section 4.3, we describe the necessary architecture changes to create _k_ basis functions. In Section 4.4, we outline the training procedure. 

## 4.1 PROBLEM FORMULATION 

We consider the following setup. The robot observes its environment through RGB images of a fixed size, denoted by the set _I_ . Tasks are described in natural language and drawn from a set _T_ . For simplicity, both _I_ and _T_ are assumed finite, representing the (large but bounded) number of images and tasks the robot may feasibly encounter. A robot’s state is defined as a pair _s ∈ S_ = _I × T_ , consisting of an image and a task description. The robot’s action space is denoted _A ⊂_ R<sup>_m_</sup> , where each output dimension corresponds to a robot end effector’s translation, rotation, etc. A trajectory _τ_ = _{_ ( _st, at_ ) _}_<sup>_T_</sup> _t_ =1<sup>is a sequence of states and actions of length</sup><sup>_T_.Each trajectory is collected under</sup> a fixed but unobserved context _c ∈ C_ , which captures factors such as lighting, camera position, robot morphology, decision rate, etc. We write _τ_<sup>_c_</sup> to highlight that a trajectory was collected under context _c_ , and we emphasize that the context is relevant for decision making but it is not extractable from the state directly. Lastly, we assume there exists an expert policy _πexp_ : _S × C → A_ , which is by definition optimal with respect to some objective function. The expert policy, typically a human, is assumed to take the context into consideration as part of its decision making. We seek to train a policy _πθ_ : _S → A_ such that _πθ_ ( _s_ ) = _πexp_ ( _s, c_ ) for all states and contexts. In other words, we seek to train a model to clone the expert policy. However, this objective is ill-posed because the expert observes the context but our learned model does not. We argue that the ill-posed nature of 

4 


Figure 3: **The MoS-VLA Architecture and Training Pipeline** . _(Left)_ MoS-VLA builds on the OpenVLA backbone where images and instructions are processed by a Llama 2 model. The language modeling head is replaced with _k_ basis action heads. The action predictions are linearly combined via vector operations as described in Section 3.1. _(Right)_ During training, we iterate between context estimation and parameter updates. We utilize parallelism in both stages: during calibration, each training node computes and broadcasts the coefficient only for the datasets it hosts. During model updates, the context coefficients are held constant and trainable weights are adjusted with DDP. 

this problem explains why VLA models fail to generalize despite the large amount of training data, and later we will argue how in-context adaptation methods address this problem. 

Next, we will define the data assumptions. Let _D_<sup>_c_</sup> = _{τ_ 1<sup>_c, τ_</sup> 2<sup>_c, ...}_beasetofexperttrajectories</sup> collected in one lab setting. Note that we assume that the context is fixed for a given lab setting, as robot implementation details are unlikely to change between trajectories. Let _D_ = _{D_<sup>_c_1</sup> _, D_<sup>_c_2</sup> _, ...}_ be a set of such datasets. For the purposes of this paper, _D_ is the Open X-embodiment dataset, as it consists of data from multiple labs, where each lab’s dataset consists of multiple trajectories. The in-context adaptation problem consists of two stages: First, there is an offline training period for _πθ_ using _D_ , where training time is not a concern. Second, there is an online adaptation phase. The trained model _πθ_ is provided with one additional trajectory _τexp_<sup>_c_collected by the expert policy under</sup> a context _c_ . Typically, _c_ is an unseen context that was not present in the offline training data set. Then _πθ_ outputs an action _a_ for a new state _s_ , and should reproduce the behavior of _πexp_ . Thus, _πθ_ should use the additional information provided by _τexp_<sup>_c_to improve its accuracy on this new context.</sup> In this second phase, adaptation time should be minimized, ideally to seconds or less. 

## 4.2 MAIN IDEA 

To design a policy that adapts to the context given the trajectory _τexp_<sup>_c_,wewillformulatetheset</sup> of context-dependent expert policies as a function space, and use _τexp_<sup>_c_to identify a function within</sup> this space. Formally, let _πexp_<sup>_c_(</sup><sup>_·_)=</sup><sup>_πexp_(</sup><sup>_·, c_)betheexpertpolicyconditionedonacontext</sup><sup>_c_,</sup> where this notation makes the dependence on the context implicit. Consider the set of such policies Π _exp_ = _{πexp_<sup>_c|c∈C}_.We define the vector operations for this space as the standard element-wise</sup> operations, and the norm is defined as _||f ||_ 1 := � _S_ �dim _i_ =1 _A_<sup>_|fi_(</sup><sup>_s_)</sup><sup>_|ds_.Thus,weequipΠ</sup><sup>_exp_witha</sup> Banach space structure. Then, by using the function encoder algorithm, we can learn a set of neural network basis functions _{g_ 1 _, ..., gk}_ to span Π _exp_ , where any policy _πexp_<sup>_c_=�</sup> _i_<sup>_k_</sup> =1<sup>_α_</sup> _i_<sup>_cgi_.During</sup> the online adaptation phase, we compute _α_<sup>_c_</sup> _∈_ R<sup>_k_</sup> by a least absolute error optimization problem. Once we have these coefficients _α_<sup>_c_</sup> , we may approximate _πexp_<sup>_c_foranynewstate</sup><sup>_s_usingalinear</sup> combination of the basis functions. A key advantage of this approach is its computational simplicity during the online phase. The function encoder adapts to new contexts via the least absolute error calculation, which has two simple steps. First, we must forward pass the basis functions on each state _s_ in _τexp_<sup>_c_.Notethat</sup> we can forward pass all states in parallel. Second, we solve the least absolute error problem (1), which is effectively just a linear program solvable in a negligible amount of time. The function encoder’s overhead for in-context adaptation is minimal. Crucially, no backpropagation is required. Thus, our method adapts to new contexts in the same amount of time required to forward pass the 

5 

model, which is only seconds even for relatively weak GPUs. Furthermore, once we have computed the coefficients _α_<sup>_c_</sup> , we output actions as a linear combination of the basis functions. Therefore, the computational and memory costs after calibration is constant with respect to the expert trajectory length. 

## 4.3 ARCHITECTURE 

To make OpenVLA amenable to the function encoder algorithm, we require _k_ separate output actions conditioned on the state, where _k_ is a hyper-parameter. Furthermore, the input has variable length depending on the task description, and so each basis function must accept variable length sequences as input, i.e., each basis function must use attention. While prior works have used nontraditional architectures such as neural ODEs for the basis functions (Ingebrand et al., 2024a), we are the first to leverage transformers as basis functions for the function encoder algorithm, and the first to demonstrate that the algorithm scales to function spaces with images and natural language as inputs. 

Due to the large number of parameters in OpenVLA, creating _k_ fully independent copies is infeasible. Instead, we leverage a single OpenVLA network body with multiple output heads. Specifically, we remove the Llama 2 output head and replace it with _k_ randomly initialized output heads. In addition, we utilize the parallel decoding technique in OpenVLA-OFT to model all action dimensions simultaneously. The output of each head acts as a separate basis function, and each outputs an action. See Figure 3. Note that the original OpenVLA implementation uses the Llama 2 head rather then training a new one from scratch. Thus, it outputs a distribution over Llama 2’s vocab, which contains 32,000 tokens, and the least-used 256 tokens are replaced with action tokens. In contrast, each basis function only outputs scalar action values directly. Thus, MoS-VLA uses a smaller total number of parameters compared to OpenVLA. In general, the overhead in terms of parameter count is small, and this same procedure can be applied to other foundation models as well. 


Figure 4: **Validation Action L**<sup>**1**</sup> **Error Across Train and OOD Datasets** . We train MoS-VLA on the same Open X-Embodiment Magic Soup Plus data mixture as OpenVLA. Each subset is annotated with its proportion in the training set. Datasets marked as OOD are unseen during training. MoS-VLA, calibrated on only 512 training examples, achieves lower error than OpenVLA on 18 of 27 training subsets and on all 5 OOD datasets. 

## 4.4 TRAINING PROCEDURE 

We start with the pretrained OpenVLA model. After removing the Llama 2 output head and initializing the _k_ basis function heads, it is clear we must train these parameters directly. For the rest of the OpenVLA parameters, we may choose to either finetune them using LoRA or to fully finetune them. For the sake of computational efficiency, we use LoRA for the results in this paper. Training progresses according to the modified function encoder algorithm using Banach definitions and _L_<sup>1</sup> optimization. See Appendix B for the pseudocode. 

Starting with a pretrained OpenVLA is a design choice to reduce the length of the offline training period. In principle, we could instead start with pretrained vision and language models, as other 

6 

VLA models do (Bjorck et al., 2025), and train the basis functions from there. Doing so may improve the performance, as the pretrained OpenVLA model may trap the model’s performance at a local optimum given that OpenVLA was trained on classification instead of regression. We leave this direction for future work. 

# 5 EXPERIMENTS 

**Implementation Details.** We train 16 basis functions by finetuning OpenVLA on the RTX dataset as described in Section 4. We utilize 32 distributed compute nodes, each of which has a GH200, using data parallelism (DDP) (Li et al., 2020). We train for a total of 5000 gradient steps, which takes approximately 24 hours. In order to fairly compare against OpenVLA, we use the same _OpenX Magic Soup Plus_ data mixture from Kim et al. (2024) with a global batch size of 320. We use an Adam optimizer with a learning rate of 1 _e_<sup>_−_4</sup> and a warmup of 10 steps. 

**Scalable Skill Calibration.** In the standard function encoder algorithm, the coefficients for each context are calculated every training step using a batch of training data, and gradients are backpropagated through this computation. This procedure requires a reasonably large batch size to ensure stable estimation of the context coefficients, which is practically infeasible for VLA training. For the sake of memory efficiency, and scalability to distributed training of a large model, we instead maintain a calibration buffer with a capacity of 512 training samples for each dataset. During DDP training, the calibration buffers are evenly spread across computation nodes. In our case, with 32 nodes and 27 datasets, the first 27 nodes each hosts a unique dataset. We compute a new set of coefficients every 16 gradient steps: nodes hosting the calibration buffer compute and broadcast the coefficients across all nodes. After each calibration, the coefficients are held constant, and gradients are not back-propagated through this process. We find that this implementation is memory efficient, since it does not have to solve a linear program each gradient step, but it does not negatively impact performance. Additionally, it allows us to easily maintain the data sampling ratio from the data mixture, whereas the standard function encoder approach would not. We solve the linear program corresponding to (1) via CVXPY (Agrawal et al., 2019). 

## 5.1 RESULTS 

**L**<sup>**1**</sup> **Error on Datasets.** After training, we evaluate our model against OpenVLA on both indistribution and out-of-distribution datasets, with results shown in Figure 4. Specifically, we compute the context coefficients for each subset from 512 random data points from its training split. While OpenVLA achieves similar performance on in-distribution datasets, it is significantly worse when evaluated out-of-distribution. We attribute this behavior to a phenomenon we term _mixedcontext overfitting_ . This occurs when an over-parameterized model, lacking mechanisms to distinguish between contexts, is trained on a mixed-context dataset. In such cases, the model learns a single function to approximate many contexts simultaneously, resulting in sharp, unstable outputs across contexts. Note this type of overfitting occurs even if the data itself is noise-free. In contrast, using the function encoder algorithm mitigates this type of overfitting because there is effectively a different model for each context. See Appendix A for a visualization of this phenomenon in a 1D setting. 

Additionally, we leverage the collected data to visualize the learned function space. For each task across all lab settings, we compute the corresponding skill coefficients and apply dimensionality reduction techniques to reveal the structure of the learned landscape. As shown in Figure 6, the coefficients form clusters that align with lab settings, supporting our hypothesis that each lab environment is effectively captured by a unique function. Notably, three Austin datasets—treated as separate during training—naturally cluster together, reflecting their underlying similarity in lab con- 

||**Simulatio**|**n (**_m_= 20**)**|**O**|**n-robot (**_m_|= 10**)**|
|---|---|---|---|---|---|
|Method|Lift Block|Open Door|Reach|Lift Block|Insert Pen|
|**OpenVLA**|0%|0%|0%|0%|0%|
|**MoS-VLA(1-shot)**|70%|75%|100%|100%|100%|


Table 1: Success rate comparison between OpenVLA and MoS-VLA. 

7 


Figure 5: **Illustration of simulated and real robot tasks.** MoS-VLA rollouts across five tasks in both simulated and on-robot experiments. Having never seen these tasks during training, MoS-VLA needs only one demonstration for gradient-free adaptation. Note that the objective for goal reaching is to hover above the block. 

ditions. These results highlight the potential of the learned skill space to provide interpretability and to expose similarities across datasets. 

**Policy Performance.** To further evaluate our model, we run simulated and on-robot experiments with the Franka Emika Panda robot arm. For simulation, we use two tasks from Robosuite (Zhu et al., 2020): block lifting and door opening. For on-robot experiments, we solve three tasks: goal reaching, block lifting, and pen insertion. In all experiments, the model is calibrated using one expert trajectory only. Due to the use of a single RGB camera in front of the robot and lack of proprioceptive state inputs to the VLA models, we simplify some of our test environments to alleviate the challenge in depth estimation by disabling forward/backward motions. Detailed descriptions of the test domains are as follows: 

(1) **Simulated Block Lifting:** A red block is placed on a table beneath the robot gripper randomly to the left or right. The robot is allowed to move sideways or up/down to grasp and lift the block away from the table. (2) **Simulated Door Opening:** A door is placed to the right of the robot about the same height as its base. The robot gripper is allowed to move sideways and up/down to push and grab the handle. (3) **Goal Reaching:** A blue block is placed at a fixed location on the mat in front of the robot. The robot can move in _x, y_ and _z_ directions to reach and hover above the block. (4) **Block Lifting:** A larger yellow block is placed in front of the robot. The robot can move in _x, y_ and _z_ directions to grasp and lift the block. (5) **Pen Insertion:** The robot is initialized with a pen in its gripper. It is allowed to move sideways and up/down to insert the pen into the pen holder. 

Our robot evaluation results are shown in Table 5. We find that the base OpenVLA model is brittle to unseen environments and completely fails both in simulation and on the real robot. This is because 

8 


Figure 6: **Visualization of the Coefficients.** Coefficients for each task and lab setting are computed from expert trajectories, then visualized using PCA and t-SNE. We observe that tasks from the same lab setting generally cluster together in the learned function space. The PCA visualization shows that the first two principle components only poorly distinguish between datasets, suggesting that more than two basis functions are needed. We also plot three Austin datasets in black because they are known to have similar lab setups. In both PCA and t-SNE, these datasets appear as one cluster, demonstrating that the coefficient space captures this similarity. 

neither the simulation nor our lab setting appears in the training set, and OpenVLA struggles to generalize. In contrast, by calibrating with a single expert demonstration, MoS-VLA adapts to the new settings. 

While MoS-VLA demonstrates clear advantages in our test environments, its success remains limited to relatively short-horizon tasks. Extending the framework to long-horizon problems will likely require additional mechanisms for temporal abstraction or hierarchical skill composition. Moreover, environments with higher stochasticity—such as the simulated block lifting task—may demand more than one demonstration to achieve consistent success. 

# 6 CONCLUSION 

We introduced a method for training VLA models to form a structured skill space that enables oneshot domain adaptation. Adaptation is achieved via least absolute error optimization, requiring no gradient calculations. This design makes the approach especially suitable for hardware-constrained settings where fine-tuning is impractical. Empirically, we demonstrate that our method improves performance on unseen robot experiments, outperforming a pretrained OpenVLA model that lacks domain transfer capability. 

This work represents a first step toward gradient-free, in-context adaptation of robot foundation models. We argue that the need to fine-tune robot policies for every new domain remains a major barrier to the deployment of general-purpose robotics. Future directions include exploring alternative functional spaces, training schemes, and architectural choices. By building expandable skill spaces, our paradigm opens the door to VLA models that can rapidly acquire new skills without erasing prior knowledge. 

# REFERENCES 

- A. Agrawal, B. Amos, S. Barratt, S. Boyd, S. Diamond, and Z. Kolter. Differentiable convex optimization layers. In _Advances in Neural Information Processing Systems_ , 2019. 

- Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith LLontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, 

9 

Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. GR00T N1: an open foundation model for generalist humanoid robots. _CoRR_ , abs/2503.14734, 2025. doi: 10.48550/ARXIV.2503.14734. URL https://doi.org/10. 48550/arXiv.2503.14734. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alex Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt2: Vision-language-action models transfer web knowledge to robotic control. In _arXiv preprint arXiv:2307.15818_ , 2023a. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J. Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael S. Ryoo, Grecia Salazar, Pannag R. Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong T. Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. RT-1: robotics transformer for real-world control at scale. In _Robotics: Science and Systems_ , 2023b. 

- Weilin Cai, Juyong Jiang, Fan Wang, Jing Tang, Sunghun Kim, and Jiayi Huang. A survey on mixture of experts in large language models. _IEEE Trans. Knowl. Data Eng._ , 37(7):3896–3915, 2025. 

- Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. Qlora: Efficient finetuning of quantized llms. In _NeurIPS_ , 2023. 

- Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia, Jingjing Xu, Zhiyong Wu, Baobao Chang, Xu Sun, and Zhifang Sui. A survey on in-context learning. In _EMNLP_ , pp. 1107–1128. Association for Computational Linguistics, 2024. 

- Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine. Diversity is all you need: Learning skills without a reward function. In _ICLR_ , 2019. 

- Letian Fu, Huang Huang, Gaurav Datta, Lawrence Yunliang Chen, William Chung-Ho Panitch, Fangchen Liu, Hui Li, and Ken Goldberg. In-context imitation learning via next-token prediction. _CoRR_ , abs/2408.15980, 2024. 

- Zeyu Han, Chao Gao, Jinyang Liu, Jeff Zhang, and Sai Qian Zhang. Parameter-efficient fine-tuning for large models: A comprehensive survey. _CoRR_ , abs/2403.14608, 2024. 

- Karol Hausman, Jost Tobias Springenberg, Ziyu Wang, Nicolas Heess, and Martin A. Riedmiller. Learning an embedding space for transferable robot skills. In _ICLR_ , 2018. 

- Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. 

- Tyler Ingebrand, Adam J. Thorpe, and Ufuk Topcu. Zero-shot transfer of neural odes. In _NeurIPS_ , 2024a. 

- Tyler Ingebrand, Amy Zhang, and Ufuk Topcu. Zero-shot reinforcement learning via function encoders. In _ICML_ . OpenReview.net, 2024b. 

10 

- Tyler Ingebrand, Adam J. Thorpe, and Ufuk Topcu. Function encoders: A principled approach to transfer learning in hilbert spaces. _CoRR_ , abs/2501.18373, 2025. 

- Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. _CoRR_ , abs/2001.08361, 2020. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Lin Lan, Zhenguo Li, Xiaohong Guan, and Pinghui Wang. Meta reinforcement learning with task embedding and shared policy. In _IJCAI_ , pp. 2794–2800, 2019. 

- Shen Li, Yanli Zhao, Rohan Varma, Omkar Salpekar, Pieter Noordhuis, Teng Li, Adam Paszke, Jeff Smith, Brian Vaughan, Pritam Damania, and Soumith Chintala. Pytorch distributed: Experiences on accelerating data parallel training. _Proc. VLDB Endow._ , 13(12):3005–3018, 2020. 

- Jungsub Lim, Eunseok Yang, and Taesup Kim. Efficient task adaptation by mixing discovered skills. In _ICML (Workshop)_ , 2019. 

- Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on visionlanguage-action models for embodied AI. _CoRR_ , abs/2405.14093, 2024. 

- Sewon Min, Xinxi Lyu, Ari Holtzman, Mikel Artetxe, Mike Lewis, Hannaneh Hajishirzi, and Luke Zettlemoyer. Rethinking the role of demonstrations: What makes in-context learning work? In _EMNLP_ , pp. 11048–11064. Association for Computational Linguistics, 2022. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homanga Bharadhwaj, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, Jo˜ao Silv´erio, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan 

11 

Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi ”Jim” Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick ”Tree” Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart’in-Mart’in, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open X-Embodiment: Robotic learning datasets and RT-X models, 2023. 

- Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mido Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herv´e J´egou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision. _Trans. Mach. Learn. Res._ , 2024, 2024. 

- Joan Puigcerver, Carlos Riquelme Ruiz, Basil Mustafa, and Neil Houlsby. From sparse to soft mixtures of experts. In _ICLR_ . OpenReview.net, 2024. 

- Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of Machine Learning Research_ , 21(140):1–67, 2020. 

- Ahmed Touati and Yann Ollivier. Learning one representation to optimize all rewards. In _NeurIPS_ , pp. 13–23, 2021. 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton-Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aur´elien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. Llama 2: Open foundation and fine-tuned chat models. _CoRR_ , abs/2307.09288, 2023. 

- Luping Wang, Sheng Chen, Linnan Jiang, Shu Pan, Runze Cai, Sen Yang, and Fei Yang. Parameterefficient fine-tuning in large models: A survey of methodologies. _CoRR_ , abs/2410.19878, 2024. 

12 

Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _ICCV_ , pp. 11941–11952. IEEE, 2023. 

- Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Mart´ın-Mart´ın, Abhishek Joshi, Kevin Lin, Soroush Nasiriany, and Yifeng Zhu. robosuite: A modular simulation framework and benchmark for robot learning. In _arXiv preprint arXiv:2009.12293_ , 2020. 

# A MIXED-CONTEXT OVERFITTING 


Figure 7: **Visualization of the Mixed-Context Overfitting Phenomenon.** _(Left)_ The two training functions, _f_ 1 and _f_ 2, are shown in red and blue along with the training data points. The third function, _f_ 3, is held out. _(Middle)_ A single, over-parameterized function approximator is fit to the training data. _(Right)_ A set of basis functions is fit to the training data. After calibrating, the basis functions may approximate all three functions accurately. 

In Figure A, we visualize how overfitting is especially problematic for over-parameterized approximators in a mixed-context (mixed-function) setting. Suppose we have a dataset consisting of two functions, _f_ 1 and _f_ 2, along with some data points from each. If we fit a single function approximator, e.g., a neural network, it may perfectly fit the training data so long as there is no input _x_ common to both functions’ datasets. However, this fit generalizes poorly, and cannot be calibrated to fit _f_ 3 without further training. 

On the other hand, a function encoder approximation computes coefficients for any given function, and so it effectively learns a space of functions rather than a single approximation. Assuming that the basis functions have been trained to span the training functions, each training function will be well-represented as a linear combination of the basis. After calibration, the function encoder even fits the unseen function so long as it is within the span of the basis. See Ingebrand et al. (2025) for more details on generalization to out-of-distribution functions. In summary, the function encoder avoids mixed-context overfitting by learning a separate function for each context. 

# B ALGORITHM PSEUDOCODE 

The algorithm is similar to the function encoder algorithm in Ingebrand et al. (2025), where the primary difference is the minimization problem solved to compute the coefficients. We additionally regularize the Gram matrix to be close to identity, i.e., the basis functions are approximately orthonormal. For completeness, we include the pseudocode in Algorithm 1. Note that the inner product is defined as _⟨f, g⟩_ = � _X_<sup>_f_(</sup><sup>_x_)</sup><sup>_T g_(</sup><sup>_x_)</sup><sup>_dx_, which is approximated using the trajectory datasets.</sup> 

# C FUNCTION ENCODER ACTION HEAD ARCHITECTURE 

The function encoder action head maps backbone features into _k_ basis action predictions. It is implemented as a two-block MLPResNet, following the parallel decoding strategy from OpenVLAOFT. The input is a feature vector of dimension 28672 (flattened from 4096 _×_ 7). This vector is 

13 

**Algorithm 1** Modified Function Encoder Algorithm (LAE) **given** expert policy space Π _exp_ , learning rate _α_ Initialize basis _{g_ 1 _, . . . , gk}_ with parameters _θ_ **while** not converged **do for all** _πexp_<sup>_c∈_Π</sup><sup>_exp_</sup><sup>**do**</sup> _α_<sup>_c_</sup> = arg min _αc∈_ R _k ||πexp_<sup>_c−_�</sup> _i_<sup>_k_</sup> =1<sup>_α_</sup> _i_<sup>_cgi||_1</sup> _π_ ˆ _exp_<sup>_c_= �</sup> _i_<sup>_k_</sup> =1<sup>_α_</sup> _i_<sup>_cgi_</sup> **end for** _L ←_<sup>�</sup> _πexp_<sup>_c_</sup> _∈_ Π _exp_<sup>_∥π_</sup> _exp_<sup>_c−π_ˆ</sup> _exp_<sup>_c∥_1</sup> _Lreg ←_<sup>�</sup><sup>_k_</sup> _i_ =1 � _kj_ =1<sup>(</sup><sup>_⟨gi, gj⟩−δij_)2</sup> _θ ← θ − α∇θ_ ( _L_ + _Lreg_ ) **end while return** _{g_ 1 _, . . . , gk}_ 

projected into a hidden dimension of 4096, processed through two residual MLP blocks, and then mapped to the output dimension _k × da_ , where the action dimension is _da_ = 7. Thus, the output corresponds to _k_ basis functions, each producing a 7-dimensional action vector. Formally, given input _h ∈_ R<sup>28672</sup> , the head produces _B_ ( _h_ ) _∈_ R<sup>_k×_7</sup> , where each row _Bi_ ( _h_ ) denotes the prediction of the _i_ -th basis function. 

14 

