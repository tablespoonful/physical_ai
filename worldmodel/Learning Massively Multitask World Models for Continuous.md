---
title: "Learning Massively Multitask World Models for Continuous Control"
date: "2025-11-24"
authors: "Nicklas Hansen; Hao Su; Xiaolong Wang"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2511.19584
pdf: https://arxiv.org/pdf/2511.19584
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.19584)** / [論文ページ](https://arxiv.org/abs/2511.19584)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Preprint 


## Learning Massively Multitask World Models for Continuous Control 

**Nicklas Hansen**<sup>_⋆_</sup> **, Hao Su**<sup>_⋆†_</sup> **, Xiaolong Wang**<sup>_⋆†_</sup> 

> _⋆_ University of California San Diego, _†_ Equal advising 

_{_ nihansen,haosu,xiw012 _}_ @ucsd.edu 

**Abstract.** General-purpose control demands agents that act across many tasks and embodiments, yet research on reinforcement learning (RL) for continuous control remains dominated by single-task or offline regimes, reinforcing a view that online RL does not scale. Inspired by the foundation model recipe (large-scale pretraining followed by light RL) we ask whether a single agent can be trained on hundreds of tasks with online interaction. To accelerate research in this direction, we introduce a new benchmark with 200 diverse tasks spanning many domains and embodiments, each with language instructions, demonstrations, and optionally image observations. We then present _Newt_ , a language-conditioned multitask world model that is first pretrained on demonstrations to acquire task-aware representations and action priors, and then jointly optimized with online interaction across all tasks. Experiments show that Newt yields better multitask performance and data-efficiency than a set of strong baselines, exhibits strong open-loop control, and enables rapid adaptation to unseen tasks. We release our environments, demonstrations, code for training and evaluation, as well as 200+ checkpoints. 

**Webpage: https://www.nicklashansen.com/NewtWM** 

### **1 Introduction** 

Learning a generalist control policy that can perform a wide variety of tasks is an ambitious goal shared by many researchers, and significant progress has already been made towards that goal (Jang et al., 2021; Reed et al., 2022; Brohan et al., 2023; Open X-Embodiment Collaboration et al., 2023; Black et al., 2024). However, the dominant approach among current efforts is to train a large policy with supervised learning on an enormous dataset of near-expert trajectories collected by _e.g._ human teleoperation. 


0.0 This approach has two major drawbacks: _(i)_ it greatly lim0 20M 40M 60M 80M 100M its the amount of data available for training, and _(ii)_ perEnvironment steps formance of the resulting policy is ultimately bounded by BC Single-task BC the quality of demonstrations. For these reasons, the comPPO Ours (no demos) munity is increasingly turning to reinforcement learning FastTD3 **Ours** (RL) for continuous improvement of large models. While _Figure 1._ **Massively multitask RL.** this new paradigm of large-scale pretraining followed by Average score when training a _single_ light RL has led to impressive capabilities in game-playing agent via online interaction on **200** (Baker et al., 2022; Vasco et al., 2025) and reasoning (Opetasks spanning **10** task domains. nAI, 2024; Guo et al., 2025; Su et al., 2025), the continuous control community remains dominated by narrow training tasks (Tassa et al., 2018; Cobbe et al., 2019; Kostrikov et al., 2020; Hafner et al., 2023; Cheng et al., 2024; Joshi et al., 2025) or strictly offline regimes (Lee et al., 2022; Hansen et al., 2024; Park et al., 2025), reinforcing a view that RL from online interaction does not scale in this domain. 

1 

Preprint 


_Figure 2._ **Tasks.** Our proposed benchmark, MMBench, consists of **200** distinct tasks across **10** task domains, including 41 new tasks. See Appendix A for a detailed overview of our task set. 

In this work, we challenge this assumption and ask the following question: can a _single_ policy be trained with online RL on hundreds of control tasks at once? To answer this question, we introduce **MMBench** : the first benchmark for massively multitask RL. MMBench comprises of 200 diverse tasks spanning multiple domains and embodiments, each with language instructions, demonstrations, and optionally image observations, enabling research on both multitask pretraining, offline-to-online RL, and RL from scratch. 

We then present **Newt** , a language-conditioned multitask world model based on TD-MPC2 (Hansen et al., 2024), which we first pretrain on demonstrations to acquire task-aware representations and action priors, and then jointly optimize with online interaction across all tasks. To extend TD-MPC2 to the massively multitask online setting, we propose a series of algorithmic improvements including a refined architecture, model-based pretraining on the available demonstrations, additional action supervision in RL policy updates, and a drastically accelerated training pipeline. 

We validate our method on our proposed benchmark, and demonstrate that effective policy learning across hundreds of tasks is feasible with online RL and in fact can lead to strong multitask policies. Our experiments demonstrate that Newt _(1)_ outperforms a set of strong baselines when training from state observations, _(2)_ can be rapidly adapted to unseen tasks and embodiments by finetuning with online RL, _(3)_ is capable of open-loop control over surprisingly long time horizons, and _(4)_ benefits from access to high-resolution image observations. In support of open-source science, **_we release 200+ model checkpoints, 4000+ task demonstrations, code for training and evaluation of Newt agents, as well as all 220 MMBench tasks (including 20 test tasks) considered in this work_** ; all of our resources can be found at **https://www.nicklashansen.com/NewtWM** . In the following, we first introduce our benchmark MMBench, and then present our Newt world model. 

### **2 Benchmark for Massively Multitask Reinforcement Learning** 

To study the feasibility of **M** assively **M** ultitask RL, we introduce **MMBench** : the first benchmark of its kind. MMBench contains a total of **200** unique continuous control tasks for training of massively multitask RL policies. The task suite consists of 159 existing tasks proposed in previous work, 22 new tasks and task variants for these existing domains, as well as 19 entirely new arcade-style tasks that we dub _MiniArcade_ . The overarching goal of MMBench is to provide a common framework and infrastructure for research and prototyping of massively multitask RL. Figure 2 provides an overview of the **10** domains included in MMBench, Figure 3 shows tasks included in MiniArcade, and Appendix A provides a detailed description of each task domain. In the following, we discuss key features of our benchmark, as well as our efforts in making MMBench accessible to the broader research community. 

2 

Preprint 


_Figure 3._ **MiniArcade.** We release a new task suite, dubbed _MiniArcade_ , that consists of 22 tasks spanning **14** unique arcade-style environments (depicted). All tasks support both low-dimensional state representations and RGB observations, and have well-defined reward functions for RL. 

##### **Ant Ball (OGBench)** 

**Embodiment:** Ant (quadruped) with 8 controllable joints (4 legs). **Instruction:** Push the soccer ball to the goal location. 

**Rocket Collect (MiniArcade) Embodiment:** 2D space rocket with 2 controllable actions: main engine and side thruster. **Instruction:** Collect coins while avoiding asteroids. 

_Figure 4._ **Sample language instructions.** All instructions in MMBench provide a description of embodiment and action space followed by a task description. Refer to Appendix B for more samples. 

#### **2.1 Problem formulation** 

Online reinforcement learning (RL) aims to learn a policy (agent) from interaction with an (in our case: multitask) environment. This interaction is commonly modeled as an infinite-horizon Partially Observable Markov Decision Process (Bellman, 1957; Kaelbling et al., 1998) formalized as a tuple ( _S, A, T , R, γ_ ). Here, environment dynamics _T_ : _S × A �→S_ are governed by generally unobservable states **s** _∈S_ approximated as **s** =<sup>_._</sup> ( _s_ state _, s_ img _, s_ lang) where _s_ state _, s_ img _, s_ lang are low-dimensional state inputs, image observations, and language instructions, respectively, **a** _∈A_ are actions, _R_ : _S × A �→_ R is a reward function that produces task-specific rewards _r_ , and _γ_ is a task-specific discount factor. Our overarching goal is to learn a _single_ policy _π_ s.t. return E _π_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtrt_]</sup><sup>_,rt_=</sup><sup>_R_(</sup><sup>**s**</sup><sup>_t, π_(</sup><sup>**s**</sup><sup>_t_)) is maximized in expectation across all time steps and tasks,</sup><sup>_i.e._,</sup> a massively multitask policy trained to perform hundreds of tasks simultaneously via online RL. 

#### **2.2 Environments** 

**Observations, actions, and rewards.** Our task suite comprises of diverse continuous control tasks spanning locomotion, tabletop manipulation, navigation, arcade games, classic control problems, and more. Tasks vary greatly in observation and action space dimensionality, task horizon, and reward specification. All tasks support three observation modes: _(1)_ lowdimensional states, _(2)_ 224 _×_ 224 RGB images, or _(3)_ both. To unify state observations and actions across tasks and domains, we provide a mask such that invalid dimensions can be taken into account during policy learning and inference. Unification of visual observations is done on a per-domain basis, with some domains readily supporting rendering at 224 _×_ 224, while others require resizing (Box2D) or zero-padding (Atari). Refer to Appendix A for a table detailing the observations, actions, rewards, and episode lengths in each task domain. 


_Figure 5._ **Language embeddings.** First 2 principal components of CLIP-ViT/B embeddings shown for a subset of tasks. 

3 

Preprint 

**Language instructions.** While some tasks can be differentiated solely based on observations, this is not universally true. For example, the manipulation tasks in _RoboDesk_ share a common observation space (pose and velocity of robot and objects), and thus it is not clear from observations alone which object is to be manipulated. A simple solution would be to provide agents with a one-hot encoding of task indices, but this greatly limits the potential for transfer to new tasks since it provides no mechanism for representing unseen tasks. Instead, we choose to provide language instructions for every task in MMBench. Two sample language instructions are shown in Figure 4, with additional samples available in Appendix B. To verify that language instructions adequately differentiate tasks and embodiments, we encode all MMBench language instructions with CLIP-ViT/B (Radford et al., 2021), and visualize their first two principal components in Figure 5. 

#### **2.3 Accessibility** 

Training agents with online RL on a large number of tasks is challenging from a learning perspective and may be prohibitively expensive for researchers and practitioners with limited computational resources. To make MMBench accessible to the broader RL community, we have devoted significant time and effort to reduce computational costs. 

**Demonstrations.** Exploration has historically been a key challenge in online RL, and a large body of literature is dedicated to exploration strategies (Brafman & Tennenholtz, 2003; Bellemare et al., 2016; Pathak et al., 2017; Sekar et al., 2020; Ecoffet et al., 2021; Ladosz et al., 2022). However, as problem scope and task complexity grows, learning an agent from scratch (“tabula rasa”) via RL is becoming infeasible. Demonstrations serve as a strong behavior prior that dramatically reduces the exploration burden and variance of online RL, creating a practical path for researchers with limited compute to still contribute to the field. To this end, we provide 10-40 demonstrations for each task in MMBench, collected by single-task TD-MPC2 (Hansen et al., 2024) agents trained from lowdimensional state observations. While we do not directly leverage the trained single-task agents in this work (beyond collecting demonstrations), _we make all_ 200 _model checkpoints available_ for use by other researchers, and are excited to see what the community will use them for. 

**Asynchronous environments.** Our benchmark consists of hundreds of environments in multiple robotics simulators, 2D game engines, and emulators, which complicates parallelization and overall software integration. To aid adoption, we provide a ready-to-use docker image and fast, easy-touse environment wrappers that enable asynchronous environment stepping and rendering, batched frame-stacking and image encoding using large pretrained backbones, cached language embeddings, easy handling of diverse observation and action spaces, as well as auto-resetting whenever a task completes. These measures drastically reduce wall-time and allow users to get started _immediately_ . 

### **3 Newt: A Multitask World Model for Continuous Control** 

To learn RL agents effectively in a massively multitask setting like ours, the algorithm of choice needs to satisfy the following criteria: it needs to _(i)_ scale with increasing model and data size, _(ii)_ be robust to various observation and action spaces, reward functions, and task horizons, _(iii)_ be able to adequately differentiate tasks, and _(iv)_ train in a reasonable time frame. We choose to base our agent, Newt, on model-based RL algorithm TD-MPC2 (Hansen et al., 2022; 2024) as it satisfies the first two criteria. Concretely, TD-MPC2 performs trajectory optimization (planning) in the latent space of a learned self-predictive (decoder-free) world model, and it has demonstrated robust learning across a variety of single-task (online RL) and multitask (offline RL) environments. We extend TD-MPC2 to the massively multitask online RL setting, and describe our algorithmic improvements in the following. Figure 6 summarizes our approach. 

#### **3.1 Learning a Massively Multitask World Model** 

TD-MPC2 learns its world model with a combination of joint-embedding prediction (self-predictive dynamics modeling), reward prediction, and TD-learning (Sutton, 1998); this is in contrast to generative world models that are typically trained to decode raw future observations ( _e.g._ RGB images) using an auxiliary decoder network. A key benefit of self-predictive world models is, in addition to being computationally cheap due to not having a decoder, that they are trained to be _control-centric_ : accurately predicting outcome (return) conditioned on a sequence of actions. Our proposed world 

4 

Preprint 


_Figure 6._ **Method.** Our agent ( ) iteratively collects data via multitask environment ( ) interaction, and optimizes its world model on the collected data. The world model takes a state vector, language instruction, and optionally RGB observations as input, and outputs actions via planning. model extends the TD-MPC2 architecture to support language instructions and optionally RGB observations in addition to low-dimensional state observations. Specifically, our world model consists of the following components: 

|Language encoder|**g**=CLIPtext(**s**lang)|▷Encodes natural language instruction|
|---|---|---|
|Image encoder|**x**=DINOv2(**s**img)|▷Encodes RGB image observation (_optional_)|
|State encoder|**z**=_h_(**s**state_,_**x**_,_**g**)|▷Computes latent state representation|
|Latent dynamics|**z**<sup>_′_ </sup>=_d_(**z**_,_**a**_,_**g**)|▷Predicts latent forward dynamics<br>(1)|
|Reward|ˆ_r_ =_R_(**z**_,_**a**_,_**g**)|▷Predicts reward_r_of a transition|
|Terminal value|ˆ_q_ =_Q_(**z**_,_**a**_,_**g**)|▷Predicts discounted sum of rewards (return)|
|Policy prior|ˆ**a**=_p_(**z**_,_**g**)|▷Predicts optimal action**a**<sup>_∗_</sup>|


where **s** = _{_ **s** lang _,_ **s** img _,_ **s** state _}_ are language, image, and state observations, respectively, **a** are actions. In practice, we use (frozen) pretrained backbones for language and image inputs which allows us to cache embeddings, and we choose to implement all other components as MLPs. Components that take multiple arguments as input fuse their inputs via concatenation before feeding them into the first dense layer, _i.e._ , we let _h_ ( **s** state _,_ **x** _,_ **g** ) =<sup>_._</sup> _h_ ([ **s** state _,_ **x** _,_ **g** ]) where [ _·_ ] denotes concatenation. 

Following TD-MPC2, we jointly optimize _h, d, R, Q_ by gradient descent on the objective 


where _τ_ = ( **s** _,_ **a** _, r,_ **s**<sup>_′_</sup> )0: _H_ is a subsequence sampled from a replay buffer _B_ , _λ ∈_ (0 _,_ 1] is a constant coefficient which weighs temporally distant samples exponentially less, `sg` is a `stop` _−_ `grad` operator that helps mitigate representation collapse (Grill et al., 2020), _ℓ_ CE is the cross-entropy loss, and predictions ( **z**<sup>_′_</sup> _t_<sup>_,_ˆ</sup><sup>_rt,_ˆ</sup><sup>_qt_)areasdefinedinEquation1.RegressingrewardsandvaluesusingaMSE</sup> loss is challenging in a multitask setting as reward distributions may be drastically different between tasks and task domains. Therefore, we opt for a discrete regression objective (the cross-entropy loss) and model values in a log-transformed space such that we are able to model a wide range of values with a single prediction head (Bellemare et al., 2017; Kumar et al., 2023; Hafner et al., 2023; Hansen et al., 2024; Farebrother et al., 2024). We use _qt_ = _rt_ + _γQ_ tgt( **z** _t_<sup>_′, p_(</sup><sup>**z**</sup><sup>_′_</sup> _t_<sup>)</sup><sup>_,_</sup><sup>**g**)asourone-</sup> step TD-target (Sutton, 1998), and let _Q_ tgt be an exponential moving average (EMA) of the online _Q_ network (Lillicrap et al., 2016). In practice, we optimize a small ensemble of _Q_ -networks and define the target _Q_ -value as the minimum of a random subset of _Q_ tgt estimates (Chen et al., 2021). We choose to use per-task discount factors ( _γ_ ) since episode lengths vary drastically between tasks; we use the domain-default discount factor when one is available and otherwise estimate it using a heuristic described in Appendix F. 

The policy prior _p_ is formulated as a stochastic maximum entropy policy (Ziebart et al., 2008) that learns to maximize _Q_ -values as estimated by the _Q_ -network defined above. However, we find that naive application of this policy objective to our problem setting leads to subpar performance 

5 

Preprint 

in tasks where _Q_ -values are difficult to estimate. Instead, we choose to leverage a small set of demonstrations (more on this in Appendix C) and add an additional behavior cloning loss to the policy prior of TD-MPC2. This serves two purposes: _(i)_ directly leveraging expert demonstrations as action supervision, and _(ii)_ explicitly distilling actions selected via planning into the less expressive policy prior. Concretely, we define the policy objective as 


where **z** _t_ +1 = _d_ ( **zt** _,_ **at** _,_ **g** ) _,_ **z** 0 = _h_ ( **s** state0 _,_ **x** 0 _,_ **g** ) is the latent rollout of _τ_ . During environment interaction, TD-MPC2 selects actions by planning with the learned world model, with the planning procedure warm-started by the policy prior _p_ . Refer to Appendix E for details on our planning algorithm. In the following, we describe other ways in which we leverage demonstrations. 

#### **3.2 Leveraging Demonstrations for World Model Learning** 

To overcome the difficulty of exploration in massively multitask online RL, we choose to leverage a small number of demonstrations for each task. Although one could naively add demonstrations to the replay buffer at the start of training and indeed benefit from the model-based BC term introduced in Equation 3, we would like to utilize demonstrations to their full extent. Concretely, we propose to use demonstrations in four distinct ways: 

( _1_ ) **Model-based pretraining.** Prior to any online interaction, we first pretrain all learnable components from Equation 1 on the provided demonstrations. Specifically, we assume that demonstrations consist of ( **s** _,_ **a** _, r_ ) tuples and jointly optimize all components by minimizing _L_ ( _θ_ ) + _Lp_ ( _θ_ ), but with the _Q_ -value term in Equation 3 temporarily disabled such that we can fully leverage the strong action supervision from the demonstrations. This is in contrast to prior work (Zhan et al., 2020; Hansen et al., 2023a) that pretrains only encoder and/or policy. 

( _2_ ) **Constrained planning.** When transitioning from pretraining to online RL, we empirically observe that (at the start of RL) planning with the world model yields a weaker behavior policy than directly using the pretrained policy due to a (comparably) inaccurate value function. To retain performance when switching to planning, we initially bias the planner towards the pretrained policy and linearly anneal this bias to zero during the first 12% of training. See Appendix E for details. 

( _3_ ) **Oversampling of demonstrations.** We maintain separate replay buffers for demonstrations and online interactions, and sample subsequences at equal proportions (50% from each) during agent updates (Feng et al., 2023; Ball et al., 2023). This means that demonstrations are (artificially) overrepresented in the training data, and ensures that the demonstration data remains available to the agent throughout training regardless of the capacity of the online interaction buffer. 

( _4_ ) **Action supervision in RL policy updates.** As discussed in Section 3.1, adding a (model-based) BC loss term in the policy objective of Equation 3 provides direct action supervision and helps regularize the RL-based policy objective when _Q_ -value estimation is inaccurate (Lin et al., 2025). 

In summary, our Newt agent is a model-based RL method for language- and optionally imageconditioned massively multitask continuous control. It aims to fully leverage available demonstrations as well as online interaction data, resulting in a data-efficient yet computationally inexpensive method. In addition to the algorithmic improvements discussed in this section, we also **drastically accelerate training speed** by distributing both model updates, environment interactions, and replay buffers across multiple processes and GPUs, compiling training and inference code with torch.compile (Bou et al., 2023), and other implementation details described in Appendix F. 

### **4 Experiments** 

We evaluate **Newt** on our proposed benchmark **MMBench** which consists of **200** tasks across **10** task domains: DMControl (Tassa et al., 2018), DMControl Extended, Meta-World (Yu et al., 2019), ManiSkill3 (Tao et al., 2025), MuJoCo (Todorov et al., 2012), MiniArcade (a contribution of this work), Box2D (Brockman et al., 2016), RoboDesk (Kannan et al., 2021), OGBench (Park et al., 

6 

Preprint 


_Figure 7._ **Per-domain performance.** Average score of a _single_ state-based agent on MMBench (10 task domains; 200 tasks). See Appendix H for more baselines, and Appendix I for per-task curves. 

2025), and Atari (Bellemare et al., 2013; Farebrother & Castro, 2024). See Figure 2 for a visual overview of task domains, and refer to Appendix A for a detailed description of each task domain. Although our method can readily be applied to visual RL, experiments in this section use state observations unless we explicitly state otherwise. In support of open-source science, **_we publicly release 200+ model checkpoints, 4000+ task demonstrations, code for training and evaluation of Newt agents, as well as all 220 MMBench tasks considered in this work._** We seek to answer: 

( **_Q1_** ) **Performance.** Can a _single_ agent be trained on hundreds of unique tasks with online RL? How does our model-based approach (Newt) compare to a set of strong baselines? 

( **_Q2_** ) **Learning from demonstration.** Do demonstrations alleviate the difficulty of exploration in a massively multitask setting? How do we leverage demonstrations effectively for model-based RL? ( **_Q3_** ) **Model capabilities.** What are the downstream capabilities of a massively multitask world model? Can we leverage our trained model for zero-shot or few-shot transfer to unseen tasks/embodiments? Can we perform open-loop control? 

( **_Q4_** ) **Analysis & ablations.** What makes a good multitask world model? What role does language and vision play? What are the current capabilities and limitations of Newt? 

**Baselines.** Our baselines represent the state-of-the-art in data-efficient RL, learning from demonstrations, and RL with large amounts of parallel environments. Specifically, our baselines include: 

_•_ **Behavior cloning** (BC) (Pomerleau, 1988; Atkeson & Schaal, 1997) on demonstrations. We compare against a language-conditioned multitask BC policy, as well as _•_ **200 single-task BC policies** . 

_•_ **Proximal Policy Optimization** (PPO) (Schulman et al., 2017) is an on-policy actor–critic method that maximizes a clipped surrogate objective, and it has gained popularity in part due to its fast wall-time training when combined with massive parallel simulation. We base our experiments on the cleanRL (Huang et al., 2022b) implementation, and extend it to support language-conditioning and per-task discount factors. We also tune hyperparameters; see Appendix H for results before/after. _•_ **FastTD3** (Seo et al., 2025), a modern implementation of TD3 (Fujimoto et al., 2018) designed for RL with parallel environments. We extend FastTD3 to support language-conditioning and per-task discount factors, and find that _n_ -step returns of 8 are critical in our challenging multitask setting. 

_•_ **Model-based pretraining** of our Newt world model on the same demonstrations as for BC. During pretraining, we optimize the model as described in Section 3.2. 

_•_ **TD-MPC2** (Hansen et al., 2022; 2024) trained with multitask online RL. This baseline can be considered a more naive implementation of Newt without language-conditioning, pretraining, demonstrations, nor the BC loss term introduced in Equation 3. We match the parameter count of Newt. 

_•_ **200 single-task TD-MPC2** (Hansen et al., 2022; 2024) agents trained on individual tasks for 5M environment steps (1B total steps). We collect demonstrations for BC and Newt using these agents. 

See Appendix D for more information on baselines, including implementation and hyperparameters. 

**Implementation details.** Language is encoded using CLIP-ViT/B (Radford et al., 2021) and images using DINOv2/B (Oquab et al., 2023), which results in embeddings of dimensions 512 and 

7 

Preprint 


_Figure 8._ **Ablations** of our key design choices. Our default formulation of Newt is shown in **bold** . 

768, respectively. State observations are 128-dim vectors, actions are 16-dim vectors, and our Newt agents have 20M learnable parameters unless stated otherwise. We use a replay buffer capacity of 10M to ensure that the agent has sufficient data for all tasks. See Appendix F for more details. 

#### **4.1 Results** 

**Benchmarking algorithms.** We evaluate the performance of our method, Newt, and baselines on our proposed MMBench task suite. Methods are trained for 100M environment steps (in total across all tasks) using low-dimensional state observations. Our main result is shown in Figure 1, and perdomain scores are shown in Figure 7. These results indicate that **_Newt is more data-efficient and achieves a higher overall performance_** than PPO, FastTD3, and TD-MPC2, which we attribute in part to its significantly better performance in _DMControl_ , _DMControl Ext._ , _ManiSkill_ , and _MiniArcade_ . However, we also observe subpar performance across all RL methods in the _MuJoCo_ , _Box2D_ , and _Atari_ domains, with the performance of Newt often being similar to that of the simpler BC baseline. We conjecture that this may be due to the relative uniqueness of tasks in these domains; for example, many Atari games have little in common beyond their action space. While we observe that the addition of demonstrations in many cases leads to better asymptotic performance as it alleviates the difficulty of exploration, we recognize that there is still room for improvement; developing methods that yield more consistent improvement across tasks is thus an exciting future research direction. Please refer to Appendix H and Appendix I for additional experiments and baseline comparisons. 

**Analysis & ablations.** We ablate all key design choices, including model and batch size, use of language instructions, as well as all the different ways in which we can leverage demonstrations. Ablations are conducted with 20M parameter agents on the full 200-task set. Our main ablations are shown in Figure 8; additional experiments and per-domain results can be found in Appendix H. We make the following observations: 

( _1_ ) **_Scaling model and batch size is beneficial when the number of training tasks increases._** In contrast to previous work that shows only marginal improvements from model scaling in a single-task RL setting (Hansen et al., 2024; Nauman et al., 2025), we see a clear benefit in scaling model _and_ batch size in a multitask setting, up to a point; see Appendix F for details on scaling. We conjecture that there exists a compute-optimal ( _model_ , _batch_ ) size for any given number of tasks in which learning is stable, and that further scaling of training tasks will require proportionally larger models and batches than presently. 

**Few-shot finetuning** (20 unseen tasks/embodiments) 


( _2_ ) **_Language helps differentiate tasks._** We find that con- _Figure 9._ **Few-shot finetuning.** Averditioning the agent on language instructions provides clear age score when transferring our agent performance benefits (0 _._ 371 _→_ 0 _._ 438 normalized score), to new tasks/embodiments. 5 seeds. with the greatest improvement in domains where tasks cannot be differentiated by observations alone ( _e.g._ RoboDesk); see Appendix H for a detailed performance comparison of Newt with and without access 

8 

Preprint 


_Figure 10._ **Open-loop control.** Executing open-loop plans without any environment feedback. These results indicate that our world model learns meaningful representations of the environment. 

to language instructions. Additionally, as shown in Appendix J, this difference in downstream performance also translates to a lower training loss for the language-conditioned agent. In fact, we find language conditioning to match the performance of task indices (as used in TD-MPC2) on training tasks while _also_ providing a mechanism for generalization to unseen tasks. 

( _3_ ) **_Demonstrations improve performance in hard exploration tasks._** We find that any individual way of using demonstrations (pretraining, oversampling, model-based BC loss) is helpful, but that using them all in conjunction yields the best performance. 

**Task transfer.** To investigate whether our multitask agent transfers to unseen tasks/embodiments, we develop a held-out task set that spans multiple task domains and finetune our agent to each task individually using online RL and no demonstrations. Transfer tasks and aggregate finetuning results are shown in Figure 9. We observe that the pretrained Newt agent achieves a zero-shot score of **0** _._ **192** compared to 0 _._ 013 when trained from scratch, and reaches an average score of **0** _._ **868** at 100k environment steps vs. just 0 _._ 480 for the baseline. These results demonstrate non-trivial transferability, and we expect transfer results to get better as more and more training data becomes available. As shown in Table 1, we find that unseen language instructions can greatly inhibit zero-shot generalization of our agent, depending on the task. Replacing the noun describing the object to be manipulated (unseen instruction) with cube (inaccurate but seen instruction) improves zero-shot success rate by 20 _._ 7% across 6 pushing tasks, whereas we see the reverse trend for pick-and-place tasks. To best reflect the _true_ capabilities of our agent, _we use unseen instructions_ in all transfer experiments. 

**Open-loop control.** Model-based approaches are uniquely positioned to perform open-loop control (planning and executing actions without environment feedback). To better understand the current capabilities of Newt, we compare its open-loop planning performance relative to the default closed-loop planning. We evaluate on 8 diverse tasks and with planning horizons of **up to 48 time steps** – **16** _×_ **longer** than its training horizon of 3. Qualitative re- 

_Table 1._ **Language** **_sometimes_ inhibits zeroshot generalization.** Success rate with seen and unseen instructions in 10 unseen manipulation tasks. 100 trials per task. 

||Instruction|Success (%)|
|---|---|---|
|**(Default)**|Push <unseen>|0_._3|
||Push <cube>|**21**_._**0**|
|**(Default)**|Pick <unseen>|**10**_._**5**|
||Pick <cube>|0|


_Table 2._ **Visual RL.** Agent performance after finetuning with visual inputs for 30M steps. 

||Domain|Score|Gain|
|---|---|---|---|
|State|**All**|0_._438|_−_|
|+RGB|**All**|**0**_._**442**|+**0**_._**004**|
|↰|RoboDesk|0_._500|+**0**_._**125**|
|↰|Meta-World|0_._572|+**0**_._**069**|
|↰|MiniArcade|0_._437|_−_**0**_._**004**|
|↰|DMControl|0_._471|_−_**0**_._**029**|


_Table 3._ **Training cost.** Expected wall-time when training on 200 tasks for 100M environment steps in total (20M params). Reported for different hardware configurations. 

|Observation|Hardware|Days|
|---|---|---|
|State|1_×_RTX 3090|11_._2|
|State|2_×_RTX 3090|7_._3|
|**State**|**2**_×_**RTX 5090**|**4**_._**6**|
|State+RGB|2_×_RTX PRO 6000|4_._7|


sults are shown in Figure 10, and the full quantitative results are provided in Appendix G. We find 

9 

Preprint 

that Newt can plan over long time horizons without being explicitly trained to do so, with performance closely matching closed-loop control in most tasks. Common failure modes include drifting dynamics ( _Walker Walk_ , DMControl), failing to decelerate after reaching the target ( _Lunarlander Takeoff_ , Box2D), or the inability to predict stochastic elements ( _Assault_ , Atari). Refer to Appendix G for more open-loop results. 

**Visual observations.** The majority of our experiments are conducted with low-dimensional states due to ( _i_ ) added computational costs of visual RL, and ( _ii_ ) lack of available baselines for massively multitask visual RL. However, we hypothesize that some task domains stand to benefit more from vision than others. To test this hypothesis, we add 224 _×_ 224 RGB inputs to our state-based agent as described in Equation 1 and finetune the entire model for 30M environment steps. We report average score across all domains as well as for a select few domains where the score change is noteworthy. We observe only a marginal overall improvement (+0 _._ 004) with visual observations, but find that performance _improves_ significantly for manipulation (RoboDesk and Meta-World) and _decreases_ in domains such as DMControl where learning from vision is known to be more challenging than from state (Hafner et al., 2019; Srinivas et al., 2020; Kostrikov et al., 2020). 

**Training cost.** Table 3 shows the expected wall-time when training on 200 tasks from MMbench, for various hardware configurations and observation modes (state and state+RGB with rendering at 224 _×_ 224). Machines are equipped with an AMD EPYC 9354 CPU and _≥_ 128 GB of RAM. The demonstration dataset requires 32 GB of disk space. 

### **5 Related Work** 

Our work spans multiple research topics including _(i)_ the development of new training environments, _(ii)_ benchmarks for evaluation of multitask policies, _(iii)_ algorithms and infrastructure for large-scale RL, and _(iv)_ learning from demonstration. In the following, we aim to provide a comprehensive yet concise overview of related work along each of these axes. 

**Benchmarks for multitask RL.** Historically, most RL benchmarks have been designed for singletask training and evaluation (Bellemare et al., 2013; Brockman et al., 2016; Tassa et al., 2018; Cobbe et al., 2019; Tao et al., 2025). While some benchmarks evaluate policy learning and generalization within a narrow task (Cobbe et al., 2019; Hansen & Wang, 2021; Kirk et al., 2023) or task family (Kolve et al., 2017; Yu et al., 2019; Savva et al., 2019; Kannan et al., 2021; Liu et al., 2023; Shukla et al., 2024; Park et al., 2025; Joshi et al., 2025), multi-domain learning and generalization in the context of RL remains mostly unexplored. Similarly, several works propose multi-embodiment datasets for imitation learning in robotics (Open X-Embodiment Collaboration et al., 2023; Li et al., 2024; Khazatsky et al., 2024) but we have yet to see a comparably large initiative for multitask and multi-embodiment RL, let alone multi- _domain_ RL. Our proposed benchmark **MMBench** consists of 10 distinct task domains, each of which contains a variety of different tasks and embodiments that all have reward functions, demonstrations, language instructions, and optionally visual observations. 

**Scaling RL.** Existing literature has predominantly explored scaling of control policies in the context of imitation learning, where access to large demonstration datasets for supervised policy learning ( _e.g._ behavior cloning) is assumed (Jang et al., 2021; Reed et al., 2022; Schubert et al., 2023; Brohan et al., 2023; Open X-Embodiment Collaboration et al., 2023; Octo Model Team et al., 2024; Black et al., 2024). Perhaps most similar to ours, Reed et al. (2022) learns a multi-domain control policy via supervised learning on more than 63M demonstrations collected in various simulation environments. Although this is an impressive feat, relying on the availability of large amounts of expert demonstrations is highly impractical if not infeasible for many downstream applications, and the capabilities of the resulting agent is inherently limited by the behavior policy ( _e.g._ a human or learned specialist policy) that generated the demonstrations. For this reason, the community is increasingly turning to RL for training and finetuning of agents with superhuman capabilities in game-playing (Berner et al., 2019; Schrittwieser et al., 2020; Lee et al., 2022; Baker et al., 2022; Vasco et al., 2025), reasoning and agentic AI (OpenAI, 2024; Guo et al., 2025; Su et al., 2025), and most recently robotics (Hafner et al., 2023; Hansen et al., 2024; Cheng et al., 2024; Miller et al., 2025; Nauman et al., 2025; DYNA Robotics, 2025). In particular, TD-MPC2 (Hansen et al., 2024) presents a model-based RL algorithm that can be trained on up to 80 tasks across 2 domains (DMControl and Meta-World) using offline RL on a large dataset of 545M transitions collected by specialist policies. However, RL still remains brittle to changes in learning dynamics (Fujimoto 

10 

Preprint 

et al., 2018; Chen et al., 2021; Kostrikov et al., 2020; Hansen et al., 2023b; Farebrother et al., 2024), hyperparameters (Huang et al., 2022a; Hussing et al., 2024), and task specification (Clark & Amodei, 2016; Kirk et al., 2023) as evidenced by our ablations in Figure 8 and our zero-shot results in Table 1. Additionally, scaling of RL is often bottlenecked by training infrastructure and interaction throughput (Espeholt et al., 2019; Weng et al., 2022; Tao et al., 2025; Shukla, 2025; Seo et al., 2025). We provide a comprehensive benchmark for multi-domain RL accompanied by robust training infrastructure and a practical RL algorithm ( **Newt** ) that consumes various data sources and modalities. 

**Learning from demonstration.** Demonstrations and offline data have been used to bootstrap policies (Nakanishi et al., 2003; Ross et al., 2011; Ho & Ermon, 2016; Pinto et al., 2017; Duan et al., 2017; Peng et al., 2019; Kalashnikov et al., 2021; Baker et al., 2022; Ball et al., 2023), overcome the difficulty of exploration in sparse reward tasks (Vecerik et al., 2017; Hester et al., 2018; Rajeswaran et al., 2018; Zhan et al., 2020; Hansen et al., 2023a; Feng et al., 2023), and initialize multitask skills before online improvement with RL (Shi et al., 2022; Shukla et al., 2024; Zhang et al., 2024; Lu et al., 2025). By providing demonstrations for 200 tasks, MMBench provides a new, challenging testbed for massively multitask imitation learning, online RL, and offline-to-online RL in a common task suite that allows for fast, reliable, and reproducible measures of algorithmic improvement, and our agent Newt serves as a strong baseline for the community to build upon in this new paradigm. A research direction that we believe MMBench is especially suited for is finetuning of pretrained generalist models such as vision-language-action models (VLAs) using online RL as explored in Lu et al. (2025) for a narrower set of tasks than we consider in this work. 

### **6 Recommendations for Future Work** 

This work introduces MMBench, a benchmark for massively multitask RL, as well as Newt, a language-conditioned multitask world model trained with online RL. We demonstrate that online RL on hundreds of tasks simultaneously is indeed feasible, and that it can lead to world models with surprisingly strong generalization and open-loop control capabilities. We are excited by these encouraging results, and look forward to seeing in which ways the research community will build upon our work. In the following, we detail interesting open research questions and opportunities for future work in this area in hopes of inspiring new innovations. Specifically, we believe that the following 7 topics will have great potential for impact over the coming years: 

- **Visual RL.** While MMBench and Newt fully support high-resolution (224 _×_ 224) RGB observations, the majority of our experiments in this work are limited to low-dimensional (128-d) state observations. Training visual RL policies has substantially higher hardware requirements, particularly so in terms of GPU memory if one is to store the replay buffer in GPU memory for fast sampling – and this is especially true in the massively multitask setting since it is necessary to retain some amount of data for each task. We believe that improving the practicality of visual RL remains an important research goal, and we see two future directions that could help alleviate the computational cost: _(1)_ further pretraining of the visual encoder and world model, and _(2)_ innovations in data pipelines that go beyond the typical first-in-first-out replay buffer. 

- **Language understanding.** We find that language understanding is currently a bottleneck for task generalization despite leveraging pretrained language embeddings from CLIP (Radford et al., 2021). This may, in part, be due to the limited number of language instructions: one fixed instruction per task for a total of 200 tasks. We expect language understanding to improve as the number of training tasks increases, but we also believe that additional techniques such as data augmentation, pretraining on external datasets that contain language instructions, learning from language at the token-level rather than embeddings, or any other techniques that seek to improve the agent’s ability to interpolate instructions will be immensely helpful. 

- **Pretraining and improved base models.** Pretraining of the Newt agent is currently limited to supervised learning on a demonstration dataset. Our ablations show that improving the pretraining stage leads to consistently better performance both pre- and post-RL, so we expect further improvements and scaling of the model pretraining to be a valuable research direction. We expect training of agents for embodied decision-making and control to eventually resemble the training recipe of contemporary reasoning models (OpenAI, 2024; Guo et al., 2025) in which significant resources are invested into large-scale pretraining of an agent before any RL is performed. 

11 

Preprint 

- **Neural architectures.** Our Newt agent is based on the TD-MPC2 (Hansen et al., 2024) architecture which has proven to perform well across a variety of tasks and model sizes. However, the architecture remains rather simple: each component of the world model architecture is a deterministic MLP (except for the Gaussian policy prior). We believe that leveraging more recent architectural innovations such the Transformer (Vaswani et al., 2017) and Diffusion Policy (Chi et al., 2023) could potentially lead to further performance improvements, but their integration into model-based RL algorithms remains relatively unexplored. 

- **Model capabilities.** Our initial explorations into the capabilities of our Newt agent indicate that it is capable of open-loop control across hundreds of tasks, and that it can be rapidly adapted to new tasks and embodiments using online RL. However, further research into the emerging capabilities (and current limitations) of massively multitask agents is warranted. For example, the structure of the emerging (learned) latent state space and by extension dynamics modeling is not well understood, but we believe that improved understanding of emerging behavior in agents will help inform the design of future agents and neural architectures for model-based RL. 

- **Learning strategies.** We find convergence rate to differ substantially between tasks and task domains. This is perhaps not surprising as tasks vary greatly in complexity, degree of randomization, and reward specification. While our experiments show that the provided demonstrations greatly improve data-efficiency as well as asymptotic performance of our Newt agent, we believe that more sophisticated training strategies may also lead to better data-efficiency and asymptotic performance. Two directions that appear particularly interesting are _(1)_ learning curricula that dynamically balance environment interaction (data collection) for each task based on task progress, and _(2)_ non-uniform sampling methods or training objectives that prioritize sampling from tasks or subtrajectories that are particularly useful. 

- **Training environments and datasets.** We believe that further scaling of the environments and datasets used for training of world models will continue to drive performance and lead to better generalization abilities. Development of additional RL environments using _e.g._ procedural generation, agentic AI, or other generative methods is thus a promising research direction, in addition to training techniques that incorporate existing large-scale datasets from other domains. 

Overall, we remain very optimistic about the future of massively multitask RL training, and hope that our emphasis on transparency and sharing of code, data, and checkpoints will inspire other researchers to do the same. 

### **Acknowledgments** 

The authors thank the following people for helpful discussions and feedback on paper drafts, in alphabetical order: Adrian Remonda, Arth Shukla, Bo Ai, Hansen Lillemark, Jiajun Xi, Lars Paulsen, Stone Tao, and Yutao Xie. A special thanks is also extended to the open-source RL community, without whom this project would not have been possible; particularly the original developers of MuJoCo, DMControl, Meta-World, ManiSkill3, RoboDesk, OGBench, Arcade Learning Environment, Gym and Gymnasium, TorchRL (Vincent Moens), as well as their numerous individual contributors. 

### **Statements** 

**A statement on reproducibility.** Reproducibility is important to us. We release 200+ model checkpoints, 4000+ task demonstrations, code for training and evaluation of Newt agents, as well as all 220 MMBench tasks (200 training tasks and 20 test tasks) considered in this work; all of our artifacts are made publicly available at **https://www.nicklashansen.com/NewtWM** . We also provide extensive implementation details and empirical results in the appendices. Most notably, Appendix A provides an overview of task domains, Appendix C provides details on demonstrations, Appendix D and Appendix F provide implementation details for baselines and Newt, respectively, and Appendix I provides learning curves for all 200 tasks. 

**A statement on ethics.** We propose a benchmark, MMBench, that is comprised of both entirely new tasks, tasks that are derivative work based on existing task domains, and existing tasks that are used as is. All task domains and baselines for which we rely on third-party code are open-source and have permissible licenses. For example, DMControl is licensed under an Apache 2.0 License, 

12 

Preprint 

OGBench is licensed under an MIT License, and Arcade Learning Environment (ALE; also known as Atari) is licensed under a GNU General Public License v2.0. Any derivative work of existing task domains is licensed under their respective licenses; code contributed as part of our work ( _e.g._ , MiniArcade and Newt) is licensed under an MIT License. 

### **References** 

Christopher G. Atkeson and Stefan Schaal. Robot learning from demonstration. In _ICML_ , 1997. 

- Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. _Advances in Neural Information Processing Systems_ , 2016. 

- Bowen Baker, Ilge Akkaya, Peter Zhokov, Joost Huizinga, Jie Tang, Adrien Ecoffet, Brandon Houghton, Raul Sampedro, and Jeff Clune. Video pretraining (vpt): Learning to act by watching unlabeled online videos. _Advances in Neural Information Processing Systems_ , 35:24639–24654, 2022. 

- Philip J Ball, Laura Smith, Ilya Kostrikov, and Sergey Levine. Efficient online reinforcement learning with offline data. In _International Conference on Machine Learning_ , pp. 1577–1594. PMLR, 2023. 

- M. G. Bellemare, Y. Naddaf, J. Veness, and M. Bowling. The arcade learning environment: An evaluation platform for general agents. _Journal of Artificial Intelligence Research_ , 47:253–279, jun 2013. 

- Marc Bellemare, Sriram Srinivasan, Georg Ostrovski, Tom Schaul, David Saxton, and Remi Munos. Unifying count-based exploration and intrinsic motivation. In D. Lee, M. Sugiyama, U. Luxburg, I. Guyon, and R. Garnett (eds.), _Advances in Neural Information Processing Systems_ , volume 29, 2016. 

- Marc G Bellemare, Will Dabney, and R´emi Munos. A distributional perspective on reinforcement learning. In _International Conference on Machine Learning_ , pp. 449–458. PMLR, 2017. 

- Richard Bellman. A markovian decision process. _Indiana Univ. Math. J._ , 6:679–684, 1957. ISSN 0022-2518. 

- Christopher Berner, Greg Brockman, Brooke Chan, Vicki Cheung, Przemyslaw Debiak, Christy Dennison, David Farhi, Quirin Fischer, Shariq Hashme, Chris Hesse, et al. Dota 2 with large scale deep reinforcement learning. _arXiv preprint arXiv:1912.06680_ , 2019. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. pi0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Albert Bou, Matteo Bettini, Sebastian Dittert, Vikash Kumar, Shagun Sodhani, Xiaomeng Yang, Gianni De Fabritiis, and Vincent Moens. Torchrl: A data-driven decision-making library for pytorch, 2023. 

- Ronen I. Brafman and Moshe Tennenholtz. R-max - a general polynomial time algorithm for nearoptimal reinforcement learning. _J. Mach. Learn. Res._ , 3:213–231, March 2003. ISSN 1532-4435. doi: 10.1162/153244303765208377. 

- Greg Brockman, Vicki Cheung, Ludwig Pettersson, Jonas Schneider, John Schulman, Jie Tang, and Wojciech Zaremba. Openai gym, 2016. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- Xinyue Chen, Che Wang, Zijian Zhou, and Keith Ross. Randomized ensembled double q-learning: Learning fast without a model. _International Conference on Learning Representations_ , 2021. 

13 

Preprint 

- Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 11443– 11450. IEEE, 2024. 

- Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- Jack Clark and Dario Amodei. Faulty reward functions in the wild. _OpenAI Blog_ , 2016. 

- Karl Cobbe, Christopher Hesse, Jacob Hilton, and John Schulman. Leveraging procedural generation to benchmark reinforcement learning. _arXiv preprint arXiv:1912.01588_ , 2019. 

- Yan Duan, Marcin Andrychowicz, Bradly C. Stadie, Jonathan Ho, Jonas Schneider, Ilya Sutskever, P. Abbeel, and Wojciech Zaremba. One-shot imitation learning. _ArXiv_ , abs/1703.07326, 2017. 

- DYNA Robotics. Dynamism v1 (dyna-1) model: A breakthrough in performance and productionready embodied ai. https://www.dyna.co/research, June 2025. 

- Adrien Ecoffet, Joost Huizinga, Joel Lehman, Kenneth O Stanley, and Jeff Clune. First return, then explore. _Nature_ , 590(7847):580–586, 2021. 

- Lasse Espeholt, Rapha¨el Marinier, Piotr Stanczyk, Ke Wang, and Marcin Michalski. Seed rl: Scalable and efficient deep-rl with accelerated central inference. _arXiv preprint arXiv:1910.06591_ , 2019. 

- Jesse Farebrother and Pablo Samuel Castro. Cale: Continuous arcade learning environment. _Advances in Neural Information Processing Systems_ , 37:134927–134946, 2024. 

- Jesse Farebrother, Jordi Orbay, Quan Vuong, Adrien Ali Taiga, Yevgen Chebotar, Ted Xiao, Alex Irpan, Sergey Levine, Pablo Samuel Castro, Aleksandra Faust, Aviral Kumar, and Rishabh Agarwal. Stop regressing: Training value functions via classification for scalable deep RL. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Yunhai Feng, Nicklas Hansen, Ziyan Xiong, Chandramouli Rajagopalan, and Xiaolong Wang. Finetuning offline world models in the real world. _Conference on Robot Learning_ , 2023. 

- Scott Fujimoto, Herke Hoof, and David Meger. Addressing function approximation error in actorcritic methods. In _International conference on machine learning_ , pp. 1587–1596. PMLR, 2018. 

- Jean-Bastien Grill, Florian Strub, Florent Altch’e, Corentin Tallec, Pierre H. Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires, Zhaohan Daniel Guo, Mohammad Gheshlaghi<sup>´</sup> Azar, Bilal Piot, Koray Kavukcuoglu, R´emi Munos, and Michal Valko. Bootstrap your own latent: A new approach to self-supervised learning. _Advances in Neural Information Processing Systems_ , 2020. 

- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International Conference on Machine Learning_ , pp. 2555–2565, 2019. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Nicklas Hansen and Xiaolong Wang. Generalization in reinforcement learning by soft data augmentation. In _International Conference on Robotics and Automation_ , 2021. 

- Nicklas Hansen, Xiaolong Wang, and Hao Su. Temporal difference learning for model predictive control. In _ICML_ , 2022. 

- Nicklas Hansen, Yixin Lin, Hao Su, Xiaolong Wang, Vikash Kumar, and Aravind Rajeswaran. Modem: Accelerating visual model-based reinforcement learning with demonstrations. 2023a. 

14 

Preprint 

- Nicklas Hansen, Zhecheng Yuan, Yanjie Ze, Tongzhou Mu, Aravind Rajeswaran, Hao Su, Huazhe Xu, and Xiaolong Wang. On pre-training for visuo-motor control: Revisiting a learning-fromscratch baseline. In _International Conference on Machine Learning (ICML)_ , 2023b. 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control, 2024. 

- Todd Hester, Matej Vecerik, Olivier Pietquin, Marc Lanctot, Tom Schaul, Bilal Piot, Dan Horgan, John Quan, Andrew Sendonaris, Ian Osband, et al. Deep q-learning from demonstrations. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

- Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. _Advances in neural information processing systems_ , 29, 2016. 

- Shengyi Huang, Rousslan Fernand Julien Dossa, Antonin Raffin, Anssi Kanervisto, and Weixun Wang. The 37 implementation details of proximal policy optimization. In _ICLR Blog Track_ , 2022a. URL https://iclr-blog-track.github.io/2022/03/ 25/ppo-implementation-details/. https://iclr-blog-track.github.io/2022/03/25/ppoimplementation-details/. 

- Shengyi Huang, Rousslan Fernand Julien Dossa, Chang Ye, Jeff Braga, Dipam Chakraborty, Kinal Mehta, and Jo˜ao G.M. Ara´ujo. Cleanrl: High-quality single-file implementations of deep reinforcement learning algorithms. _Journal of Machine Learning Research_ , 23(274):1–18, 2022b. 

- Marcel Hussing, Claas A. Voelcker, Igor Gilitschenski, Amir-massoud Farahmand, and Eric Eaton. Dissecting deep rl with high update ratios: Combatting value overestimation and divergence. _Reinforcement Learning Conference_ , August 2024. 

- Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _CoRL_ , 2021. 

- Viraj Joshi, Zifan Xu, Bo Liu, Peter Stone, and Amy Zhang. Benchmarking massively parallelized multi-task reinforcement learning for robotics tasks. In _Reinforcement Learning Conference_ , 2025. URL https://openreview.net/forum?id=z0MM0y20I2. 

- Leslie Pack Kaelbling, Michael L. Littman, and Anthony R. Cassandra. Planning and acting in partially observable stochastic domains. _Artificial Intelligence_ , 1998. 

- Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. Mt-opt: Continuous multi-task robotic reinforcement learning at scale. _ArXiv_ , abs/2104.08212, 2021. 

- Harini Kannan, Danijar Hafner, Chelsea Finn, and Dumitru Erhan. Robodesk: A multi-task reinforcement learning benchmark. https://github.com/google-research/robodesk, 2021. 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha, Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel, Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Beltran Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R Sanketi, Archit Sharma, Cody Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, Vitor Guizilini, David Antonio Herrera, Minho Heo, Kyle Hsu, Jiaheng Hu, Muhammad Zubair Irshad, Donovon Jackson, Charlotte Le, Yunshuang Li, Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran, Andrew E. Wang, Yilin Wu, Annie Xie, Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Abhishek Gupta, Dinesh Jayaraman, Joseph J 

15 

Preprint 

Lim, Jitendra Malik, Roberto Mart´ın-Mart´ın, Subramanian Ramamoorthy, Dorsa Sadigh, Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn. Droid: A large-scale in-the-wild robot manipulation dataset. 2024. 

- Robert Kirk, Amy Zhang, Edward Grefenstette, and Tim Rockt¨aschel. A survey of zero-shot generalisation in deep reinforcement learning. _Journal of Artificial Intelligence Research_ , 76:201–264, 2023. 

- Eric Kolve, Roozbeh Mottaghi, Winson Han, Eli VanderBilt, Luca Weihs, Alvaro Herrasti, Daniel Gordon, Yuke Zhu, Abhinav Gupta, and Ali Farhadi. AI2-THOR: An Interactive 3D Environment for Visual AI. _arXiv_ , 2017. 

- Ilya Kostrikov, Denis Yarats, and Rob Fergus. Image augmentation is all you need: Regularizing deep reinforcement learning from pixels. _International Conference on Learning Representations_ , 2020. 

- Aviral Kumar, Rishabh Agarwal, Xinyang Geng, George Tucker, and Sergey Levine. Offline q- learning on diverse multi-task data both scales and generalizes. _International Conference on Learning Representations_ , 2023. 

- Pawel Ladosz, Lilian Weng, Minwoo Kim, and Hyondong Oh. Exploration in deep reinforcement learning: A survey. _Information Fusion_ , 85:1–22, 2022. 

- Samuel Lavoie, Christos Tsirigotis, Max Schwarzer, Ankit Vani, Michael Noukhovitch, Kenji Kawaguchi, and Aaron Courville. Simplicial embeddings in self-supervised learning and downstream classification. In _International Conference on Learning Representations_ , 2023. URL https://openreview.net/forum?id=RWtGreRpovS. 

- Kuang-Huei Lee, Ofir Nachum, Mengjiao Sherry Yang, Lisa Lee, Daniel Freeman, Sergio Guadarrama, Ian Fischer, Winnie Xu, Eric Jang, Henryk Michalewski, et al. Multi-game decision transformers. _Advances in Neural Information Processing Systems_ , 35:27921–27936, 2022. 

- Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Mart´ınMart´ın, Chen Wang, Gabrael Levine, Wensi Ai, Benjamin Martinez, Hang Yin, Michael Lingelbach, Minjune Hwang, Ayano Hiranaka, Sujay Garlanka, Arman Aydin, Sharon Lee, Jiankai Sun, Mona Anvari, Manasi Sharma, Dhruva Bansal, Samuel Hunter, Kyu-Young Kim, Alan Lou, Caleb R Matthews, Ivan Villa-Renteria, Jerry Huayang Tang, Claire Tang, Fei Xia, Yunzhu Li, Silvio Savarese, Hyowon Gweon, C. Karen Liu, Jiajun Wu, and Li Fei-Fei. Behavior-1k: A human-centered, embodied ai benchmark with 1,000 everyday activities and realistic simulation. _arXiv preprint arXiv:2403.09227_ , 2024. 

- T. Lillicrap, J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, and Daan Wierstra. Continuous control with deep reinforcement learning. _CoRR_ , abs/1509.02971, 2016. 

- Haotian Lin, Pengcheng Wang, Jeff Schneider, and Guanya Shi. Td-m(pc)2: Improving temporal difference mpc through policy constraint. _arXiv preprint arXiv:2502.03550_ , 2025. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- AJ Miller, Fangzhou Yu, Michael Brauckmann, and Farbod Farshidian. High-performance reinforcement learning on spot: Optimizing simulation parameters with distributional measures. _arXiv preprint_ , 2025. 

- Diganta Misra. Mish: A self regularized non-monotonic neural activation function. _arXiv preprint arXiv:1908.08681_ , 2019. 

16 

Preprint 

- Jun Nakanishi, Jun Morimoto, G. Endo, Gordon Cheng, Stefan Schaal, and Mitsuo Kawato. Learning from demonstration and adaptation of biped locomotion with dynamical movement primitives. _Robotics and Autonomous Systems - RaS_ , 2004, 01 2003. doi: 10.1299/jsmermd.2004.32 ~~2~~ . 

- Michal Nauman, Marek Cygan, Carmelo Sferrazza, Aviral Kumar, and Pieter Abbeel. Bigger, regularized, categorical: High-capacity value functions are efficient multi-task learners. _arXiv preprint arXiv:2505.23150_ , 2025. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Aaron van den Oord, Oriol Vinyals, and Koray Kavukcuoglu. Neural discrete representation learning. _arXiv preprint arXiv:1711.00937_ , 2017. 

- Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homanga Bharadhwaj, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, Jo˜ao Silv´erio, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi ”Jim” Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Muhammad Zubair Irshad, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick ”Tree” Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart’in-Mart’in, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Vitor Guizilini, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, 

17 

Preprint 

Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open X-Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/2310.08864, 2023. 

OpenAI. Introducing openai o1-preview. https://openai.com/index/ introducing-openai-o1-preview/, September 2024. 

- Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- Seohong Park, Kevin Frans, Benjamin Eysenbach, and Sergey Levine. Ogbench: Benchmarking offline goal-conditioned rl. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- Deepak Pathak, Pulkit Agrawal, Alexei A Efros, and Trevor Darrell. Curiosity-driven exploration by self-supervised prediction. In _International conference on machine learning_ , pp. 2778–2787. PMLR, 2017. 

- Xue Bin Peng, Aviral Kumar, Grace Zhang, and Sergey Levine. Advantage-weighted regression: Simple and scalable off-policy reinforcement learning. _arXiv preprint arXiv:1910.00177_ , 2019. 

- Lerrel Pinto, James Davidson, Rahul Sukthankar, and Abhinav Gupta. Robust adversarial reinforcement learning. In Doina Precup and Yee Whye Teh (eds.), _Proceedings of the 34th International Conference on Machine Learning_ , volume 70 of _Proceedings of Machine Learning Research_ , pp. 2817–2826. PMLR, 06–11 Aug 2017. 

- Dean A. Pomerleau. Alvinn: An autonomous land vehicle in a neural network. In D. Touretzky (ed.), _Advances in Neural Information Processing Systems_ , volume 1. Morgan-Kaufmann, 1988. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pp. 8748–8763. PmLR, 2021. 

- Aravind Rajeswaran, Vikash Kumar, Abhishek Gupta, Giulia Vezzani, John Schulman, Emanuel Todorov, and Sergey Levine. Learning Complex Dexterous Manipulation with Deep Reinforcement Learning and Demonstrations. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2018. 

- Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, et al. A generalist agent. _arXiv preprint arXiv:2205.06175_ , 2022. 

- St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pp. 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, and Dhruv Batra. Habitat: A Platform for Embodied AI Research. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2019. 

- Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

18 

Preprint 

- Ingmar Schubert, Jingwei Zhang, Jake Bruce, Sarah Bechtle, Emilio Parisotto, Martin Riedmiller, Jost Tobias Springenberg, Arunkumar Byravan, Leonard Hasenclever, and Nicolas Heess. A generalist dynamics model for control. _arXiv preprint arXiv:2305.10912_ , 2023. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, and Deepak Pathak. Planning to explore via self-supervised world models. In Hal Daum´e III and Aarti Singh (eds.), _Proceedings of the 37th International Conference on Machine Learning_ , volume 119 of _Proceedings of Machine Learning Research_ , pp. 8583–8592. PMLR, 13–18 Jul 2020. 

- Younggyo Seo, Carmelo Sferrazza, Haoran Geng, Michal Nauman, Zhao-Heng Yin, and Pieter Abbeel. Fasttd3: Simple, fast, and capable reinforcement learning for humanoid control. _arXiv preprint arXiv:2505.22642_ , 2025. 

- Lucy Xiaoyang Shi, Joseph J. Lim, and Youngwoon Lee. Skill-based model-based reinforcement learning. In _Conference on Robot Learning_ , 2022. 

- Arth Shukla. Speeding up sac with massively parallel simulation. _https://arthshukla.substack.com_ , Mar 2025. URL https://arthshukla.substack. com/p/speeding-up-sac-with-massively-parallel. 

- Arth Shukla, Stone Tao, and Hao Su. Maniskill-hab: A benchmark for low-level manipulation in home rearrangement tasks. _arXiv preprint arXiv:2412.13211_ , 2024. 

- Aravind Srinivas, Michael Laskin, and Pieter Abbeel. Curl: Contrastive unsupervised representations for reinforcement learning. _arXiv preprint arXiv:2004.04136_ , 2020. 

- Yi Su, Dian Yu, Linfeng Song, Juntao Li, Haitao Mi, Zhaopeng Tu, Min Zhang, and Dong Yu. Crossing the reward bridge: Expanding rl with verifiable rewards across diverse domains. _arXiv preprint arXiv:2503.23829_ , 2025. URL https://arxiv.org/abs/2503.23829. 

- R. Sutton. Learning to predict by the methods of temporal differences. _Machine Learning_ , 3:9–44, 1998. 

- Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse kai Chan, Yuan Gao, Xuanlin Li, Tongzhou Mu, Nan Xiao, Arnav Gurha, Viswesh Nagaswamy Rajesh, Yong Woo Choi, Yen-Ru Chen, Zhiao Huang, Roberto Calandra, Rui Chen, Shan Luo, and Hao Su. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _Robotics: Science and Systems_ , 2025. 

- Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, et al. Deepmind control suite. Technical report, DeepMind, 2018. 

- Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012.6386109. 

- Miguel Vasco, Takuma Seno, Kenta Kawamoto, Kaushik Subramanian, Peter R. Wurman, and Peter Stone. A super-human vision-based reinforcement learning agent for autonomous racing in Gran Turismo. _Reinforcement Learning Journal_ , 4:1674–1710, 2025. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Mel Vecerik, Todd Hester, Jonathan Scholz, Fumin Wang, Olivier Pietquin, Bilal Piot, Nicolas Heess, Thomas Roth¨orl, Thomas Lampe, and Martin Riedmiller. Leveraging demonstrations for deep reinforcement learning on robotics problems with sparse rewards. _arXiv preprint arXiv:1707.08817_ , 2017. 

19 

Preprint 

- Jiayi Weng, Min Lin, Shengyi Huang, Bo Liu, Denys Makoviichuk, Viktor Makoviychuk, Zichen Liu, Yufan Song, Ting Luo, Yukun Jiang, et al. Envpool: A highly parallel reinforcement learning environment execution engine. _Advances in Neural Information Processing Systems_ , 35:22409– 22421, 2022. 

- Grady Williams, Andrew Aldrich, and Evangelos A. Theodorou. Model predictive path integral control using covariance variable importance sampling. _ArXiv_ , abs/1509.01149, 2015. 

- Denis Yarats, Rob Fergus, Alessandro Lazaric, and Lerrel Pinto. Mastering visual continuous control: Improved data-augmented reinforcement learning. _International Conference on Learning Representations_ , 2021. 

- Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning_ , 2019. 

- Albert Zhan, Philip Zhao, Lerrel Pinto, Pieter Abbeel, and Michael Laskin. A framework for efficient robotic manipulation. _arXiv preprint arXiv:2012.07975_ , 2020. 

- Jesse Zhang, Minho Heo, Zuxin Liu, Erdem Biyik, Joseph J Lim, Yao Liu, and Rasool Fakoor. EXTRACT: Efficient policy learning by extracting transferrable robot skills from offline data. In _8th Annual Conference on Robot Learning_ , 2024. 

- Brian D Ziebart, Andrew Maas, J Andrew Bagnell, and Anind K Dey. Maximum entropy inverse reinforcement learning. In _Proceedings of the 23rd National Conference on Artificial Intelligence_ , volume 3, 2008. 

20 

Preprint 

### **Appendices** 

**Webpage: https://www.nicklashansen.com/NewtWM** 


**MMBench:** Appendices A _−_ D 

**Newt:** Appendices E _−_ F **Additional results:** Appendices G _−_ J 

|**A **|**Task domains**|**22**|
|---|---|---|
|**B**|**Sample language instructions**|**25**|
|**C **|**Demonstrations**|**27**|
|**D **|**Baselines**|**27**|
|**E**|**Description of Planning Algorithm**|**29**|
|**F**|**Implementation Details**|**30**|
|**G **|**Open-Loop Control**|**33**|
|**H **|**Additional Experiments**|**34**|
|**I**|**Per-Task Results**|**36**|
|**J**|**Loss Curves**|**43**|


21 

Preprint 


# **MMBench** 

Appendices A _−_ D 

### **A Task domains** 

We consider **200** tasks across **10** domains. Our task set is comprised of diverse continuous control tasks spanning robot manipulation, locomotion, navigation, arcade games, and classic control problems, each varying in task complexity, time horizon, observation and action space dimensionality, and reward formulation. Although we cannot provide detailed information about every task due to the sheer number of tasks considered, this section aims to give the reader a brief overview of the _types_ of tasks used in our experiments. Table 4 provides an overview of the task domains considered. 

_Table 4._ **Overview of task domains.** Our selection of tasks cover a wide range of task types, state and action dimensionalities, time horizons, and reward formulations. We summarize them below. 

|**Task domain**|**State**<br>min|**dim**<br>max|**Actio**<br>min|**n dim**<br>max|**Ep. le**<br>min|**ngth**<br>max|**Reward**|**RGB**|
|---|---|---|---|---|---|---|---|---|
|DMControl|3|78|1|12|500|500|dense/sparse|224_×_224|
|DMControl Ext.|3|19|1|7|500|500|dense/sparse|224_×_224|
|Meta-World|39|39|4|4|100|100|dense|224_×_224|
|ManiSkill3|10|42|1|12|25|500|dense/sparse|224_×_224|
|MuJoCo|4|105|1|8|50|1000|dense/sparse|224_×_224|
|MiniArcade|4|44|1|2|200|500|dense/sparse|224_×_224|
|Box2D|8|24|2|4|500|500|dense|224_×_224|
|RoboDesk|73|73|5|5|100|100|dense|224_×_224|
|OGBench|9|42|2|8|100|1000|dense|224_×_224|
|Atari|128|128|3|3|1000|1000|sparse|224_×_224|


#### **A.1 DMControl** 

DMControl (Tassa et al., 2018) is a benchmark for continuous control and features a variety of locomotion, manipulation, and control tasks with simple embodiments. It is available at https:// github.com/google-deepmind/dm_control. All tasks are designed as infinite-horizon MDPs (no termination conditions), and all tasks have a fixed episode length of 500 when an action repeat of 2 is applied, as is standard practice for this benchmark (Yarats et al., 2021; Hafner et al., 2023; Hansen et al., 2024). Reward formulation varies between tasks; some tasks have dense (shaped) rewards whereas others are sparse and only provide a non-zero reward on success. DMControl tasks do not have a notion of success, but episode returns are designed to be in [0 _,_ 1000] for every task, so we produce a normalized score for this benchmark by scaling the returns to the [0 _,_ 1] interval. Note that this does not guarantee that a score of 1 _._ 0 can be obtained in all DMControl tasks, 

22 

Preprint 

it is simply an upper bound. We consider **21** tasks from this domain. Examples of tasks included in our DMControl training set are _Finger Turn Hard_ , _Fish Swim_ , and _Quadruped Run_ . 

#### **A.2 DMControl Extended** 

DMControl Extended is, as the name implies, an extended task set based on the original DMControl environment. We include 11 custom tasks previously proposed by Hansen et al. (2024) (which are all available at https://www.tdmpc2.com), and design an additional 5 locomotion tasks across 3 new embodiments: _Jumper_ , _Spinner_ , and _Giraffe_ . Tasks included in this task set follow the same recipe as the original DMControl benchmark: a fixed episode length of 500 steps, and episode returns in [0 _,_ 1000] which we normalize by scaling down to [0 _,_ 1]. We consider **16** tasks from this domain. Examples of tasks included in our DMControl Extended training set are _Walker Run Backward_ , _Cheetah Jump_ , and _Spinner Spin_ . 

#### **A.3 Meta-World** 

Meta-World (Yu et al., 2019) is a benchmark for robotic table-top manipulation tasks with a Sawyer robot and end-effector position control, and it is readily available at https://github.com/ Farama-Foundation/Metaworld. It consists of 50 diverse manipulation tasks that all share a common observation- and action space to facilitate multitask learning. We use a fixed episode length of 100 steps (after applying an action repeat of 2), and no terminal conditions. Meta-World provides dense reward functions and success criteria for each task in the task suite; we report binary task success at end of episode as the normalized score for Meta-World tasks. We exclude one task, _Shelf Place_ , from our training set due to an issue with the simulation, and consider the remaining **49** tasks from this domain. Examples of tasks included in our Meta-World training set are _Assembly_ , _Bin Picking_ , and _Lever Pull_ . 

#### **A.4 ManiSkill3** 

ManiSkill3 (Tao et al., 2025) is an open-source simulator and task suite for embodied AI. It features a wide range of tasks and embodiments including tabletop manipulation, quadruped locomotion, whole-body humanoid control, mobile manipulation, as well as reproductions of popular control tasks from MuJoCo and DMControl. Official documentation is available at https: //maniskill.readthedocs.io. Observation and action spaces are defined on a per-task basis but is relatively consistent within a specific group of tasks. For example, most ManiSkill3 tabletop robotic manipulation tasks share a common observation space, but the action space depends on the specific robot embodiment and control mode. Robot embodiments in our ManiSkill3 task set include Franka Emika Panda, SO100, and xArm6 for manipulation, and Anymal for locomotion, in addition to simpler MuJoCo-like embodiments such as Ant, Hopper, and Cartpole. Control modes include end-effector position control, end-effector 6D pose control, and joint position control. We use the default episode lengths for each task but apply an action repeat of 2 and use no terminal conditions. ManiSkill3 provides dense reward functions and success critera for most tasks in the task suite, but not all. We use a dense reward function when one is available. We report binary task success at end of episode as the normalized score for ManiSkill3 tasks whenever one is available, and episode return normalized to the [0 _,_ 1] interval otherwise. Note that this does not guarantee that a score of 1 _._ 0 can be obtained in all ManiSkill3 tasks, it is simply an upper bound. We consider a total of **36** tasks from this domain, of which 5 tasks are new and created specifically for our paper; we intend to submit a pull request to the official ManiSkill3 code repository with our proposed task additions. Examples of tasks included in our ManiSkill3 training set are _Stack Cube_ , _Pick Screwdriver_ , and _Anymal Reach_ . 

#### **A.5 MuJoCo** 

MuJoCo (Todorov et al., 2012) is an open-source physics simulator and classic benchmark in the reinforcement learning and continuous control research communities. Official documentation for the tasks is available at https://gymnasium.farama.org/environments/mujoco. Tasks in this suite are diverse in terms of embodiments and all have different observation and action spaces. We use the default episode lengths for each taks but apply an action repeat of 2 for some of the tasks. 

23 

Preprint 

We use the v4 version of the tasks and disable all termination conditions to be in line with our other task domains. All tasks have pre-defined reward functions, some of which are sparse (only non-zero reward when success is reached), and we report episode return normalized to the [0 _,_ 1] interval as normalized score for MuJoCo tasks. We consider a total of **6** tasks from this domain. Examples of tasks included in our MuJoCo training set are _Ant_ , _Half-cheetah_ , and _Reacher_ . 

#### **A.6 MiniArcade** 

MiniArcade is a new task suite created specifically for this paper, implemented using pygame (https://github.com/pygame/pygame). It consists of 22 tasks spanning 14 unique arcade-style environments. Tasks vary greatly in task objective, episode length, observation and action space dimensionality, as well as reward formulation. All tasks have a fixed episode length and no termination conditions. We design each task to fully support low-dimensional state representations, RGB image observations, and a combination of the two. We define normalized return by pre-defined success criteria for tasks where it is appropriate to do so, and otherwise use episode return normalized to the [0 _,_ 1] interval. As a result, there is no guarantee that a score of 1 _._ 0 can be obtained in all MiniArcade tasks, it is simply an upper bound. We consider a total of **19** tasks from this domain for training, and have **fully open-sourced the entire task suite** for the community to build upon. Examples of tasks included in our MiniArcade training set are _Spaceship_ , _Coconut Dodge_ , and _Chase-Evade_ . 

#### **A.7 Box2D** 

Box2D is a small collection of 2D environments created for the original release of OpenAI Gym (Brockman et al., 2016). Official documentation for the environments is available at https: //gymnasium.farama.org/environments/box2d. The tasks vary in task objective, episode length, and observation and action space dimensionalities. We use a fixed episode length for every task by disabling termination conditions. The Box2D tasks that we consider were originally designed for low-dimensional state observations, so we have modernized the implementations and added support for visual observations, including (visual) domain randomization to promote more generalizable visual control policies. Tasks in this task suite have pre-defined dense reward functions that we use for policy learning, and we report normalized score as episode return normalized to the [0 _,_ 1] interval. Note that this does not guarantee that a score of 1 _._ 0 can be obtained in all Box2D tasks, it is simply an upper bound. We consider a total of **8** tasks and task variations based on the original OpenAI Gym environments; 5 for the _Bipedal Walker_ environnment and 3 for the _Lunarlander_ environment. Examples of tasks included in our Box2D training set are _Bipedal Walker (Obstacles)_ , _Lunarlander Land_ , and _Lunarlander Takeoff_ . 

#### **A.8 RoboDesk** 

RoboDesk (Kannan et al., 2021) is a small suite of robotic manipulation tasks designed for multitask RL research. It includes 9 object manipulation tasks in a single desk-themed environment, and all tasks share a common observation and action space. An implementation of RoboDesk is available at https://github.com/google-research/robodesk. The benchmark is explicitly designed for visual RL but also supports low-dimensional state observations. All tasks have a fixed episode length and no terminal conditions, and both dense reward functions for policy learning and success criteria for evaluation are provided; we use the success rate as normalized score for RoboDesk. We consider **6** tasks from this domain. Examples of tasks included in our RoboDesk training set are _Push Green_ , _Open Drawer_ , and _Place Flat Block in Bin_ . 

#### **A.9 OGBench** 

OGBench (Park et al., 2025) is a benchmark designed to facilitate research in offline goalconditioned RL. It consists of multiple distinct environments and embodiments, and supports both low-dimensional state representations as well as RGB image observations. OGBench was developed with multi-goal but not multi-embodiment learning in mind, and the action space dimensionality thus depends on the particular task. Tasks vary greatly in episode length, but we use a fixed episode length for each task without any terminal conditions. Because OGBench was not designed for online 

24 

Preprint 

RL, we define dense reward functions for tasks where one was not previously defined, and modify the observation space to include all relevant task information ( _e.g._ goal position). Unlike the original OGBench environments available at https://github.com/seohongpark/ogbench, we treat different goal positions within the same scene configuration as the same task. To increase environment difficulty and diversity, we create a series of novel scene configurations for the 2D point mass and Ant (quadruped) goal-conditioned navigation environments. We use success rate as normalized score for all but one task ( _Ant_ locomotion) which does not have a clear metric of success; we thus use episode return normalized to the [0 _,_ 1] interval for this task. We consider **12** tasks based on the original OGBench environments; 5 tasks for the 2D point mass embodiment and 7 for the Ant embodiment. Examples of tasks included in our OGBench training set are _Ant Soccer_ , _Point Mass (Maze)_ , and _Ant (Bottleneck)_ . 

#### **A.10 Atari** 

The Arcade Learning Environment (Bellemare et al., 2013), often referred to as simply Atari or ALE, is an interface for a collection of diverse and often challenging Atari 2600 games originally designed for human play. The ALE is a long-standing benchmark for RL algorithms, and has traditionally been used primarily for single-task visual RL benchmarking with a discrete action space. More recently, Farebrother & Castro (2024) has proposed a non-linear continuousto-discrete action transformation that extends support to agents with continuous action spaces, which makes it a suitable task suite for our purposes. An implementation of ALE with support for continuous action spaces is available at https://github.com/Farama-Foundation/ Arcade-Learning-Environment. However, several properties of ALE still make it challenging to apply directly to our problem setting: _(1)_ the ALE is built for visual RL and unlike our other task domains it does not support low-dimensional state representations for each game; and _(2)_ games vary by several orders of magnitude in terms of episode length, with a single episode in games like Assault sometimes exceeding 100 _,_ 000 steps with a human-level agent. To address the first challenge, we opt for the (admittedly not ideal) solution of using the raw game RAM state, which can be represented as a 128-dim vector, as our low-dimensional state representation. While we have verified that single-task agents are able to achieve non-trivial performance in all games considered, we recognize that using the raw RAM state as observation limits the potential for cross-task knowledge transfer. We therefore expect visual policies to have better potential for generalization in the Atari domain. To address the second challenge, we simplify our problem setting by limiting agents to a fixed episode length of 1 _,_ 000. Each Atari game varies greatly in their reward formulation, but games generally assign sparse rewards only at key events such as scoring a goal or losing a life. The games have no clear success criteria and we thus choose to use episode return normalized to the [0 _,_ 1] interval as normalized score for this domain. The linear transformation between episode return and normalized score is defined for each task and takes the shorter episode length into account. However, this does not guarantee that a score of 1 _._ 0 can be obtained in all Atari games, it is simply an upper bound. We consider **27** tasks (games) from this domain. Examples of tasks included in our Atari training set are _Ms. Pacman_ , _Bowling_ , and _Space Invaders_ . 

### **B Sample language instructions** 

We manually define language instructions for all 200 training tasks considered in this work. Our language instructions have two components: _(1)_ a description of the embodiment, including how many controllable joints or action dimensions the given task has; and _(2)_ a short task instruction in plain language. We make an effort to be consistent in our description of embodiments, action spaces, and tasks, while still providing enough language variation for generalization to be feasible. We provide a small subset of our language instructions in the following. 

**Walker Run (DMControl) Embodiment:** 2D walker with 6 controllable joints across 2 legs. **Instruction:** Run forward as fast as possible. 

25 

Preprint 

##### **Walker Run Backward (DMControl Ext.)** 

**Embodiment:** 2D walker with 6 controllable joints across 2 legs. **Instruction:** Run backward quickly. 

##### **Jumper Jump (DMControl Ext.)** 

**Embodiment:** 2D jumper with 2 controllable joints across 2 legs. **Instruction:** Jump as high as possible. 

##### **Plate Slide (Meta-World)** 

**Embodiment:** Sawyer robot with a 2-finger gripper and delta end-effector position control. **Instruction:** Slide the hockey puck into the goal. 

##### **Anymal Reach (ManiSkill3)** 

**Embodiment:** Quadruped (Anymal robot) with 12 controllable joints across 4 legs. **Instruction:** Reach target. 

##### **Stack Cube (ManiSkill3)** 

**Embodiment:** Franka robot with a 2-finger gripper and delta end-effector 6D-pose control. **Instruction:** Stack the red cube on top of the green cube. 

##### **Half-cheetah (MuJoCo)** 

**Embodiment:** 2D MuJoCo half-cheetah with 6 controllable joints. **Instruction:** Run forward as fast as possible. 

##### **Bipedal Walker Obstacles (Box2D)** 

**Embodiment:** 2D cartoonish bipedal walker with 4 controllable joints across 2 legs. **Instruction:** Traverse the various obstacles quickly. 

##### **Lunarlander Land (Box2D)** 

**Embodiment:** 2D lunar lander with 2 controllable thrusters. **Instruction:** Land safely on the landing pad. 

##### **Open Slide (RoboDesk)** 

**Embodiment:** Franka robot with a 2-finger gripper and delta joint position control. **Instruction:** Open the sliding door. 

##### **Ant Maze (OGBench)** 

**Embodiment:** Ant (quadruped) with 8 controllable joints (4 legs). **Instruction:** Navigate through a maze to reach the red goal. 

##### **Bird Attack (MiniArcade)** 

**Embodiment:** 2D shooter game with 2 controllable actions: move and fire. **Instruction:** Eliminate all enemies in a space-invaders style game. 

##### **Chase & Evade (MiniArcade)** 

**Embodiment:** 2D chase and evade game with X and Y movement. **Instruction:** Take turns being the chaser or evader. 

##### **Ms. Pacman (Atari)** 

**Embodiment:** Atari game with 3 controllable actions: radius, theta, and fire. **Instruction:** Eat pellets and avoid ghosts in a game of Ms. Pacman. 

26 

Preprint 

### **C Demonstrations** 

To aid in research on pretraining + finetuning of massively multitask agents we provide an expert demonstration dataset for MMBench. This dataset contains 10-40 demonstrations per task (depending on task difficulty) for a total of 4020 demonstrations, which are all collected by singletask TD-MPC2 (Hansen et al., 2024) agents trained from low-dimensional state observations. Each single-task agent is trained for 5M environment steps (Atari: 10M) to ensure that performance has converged, although we observe that training converges earlier than that on most tasks. Training a single-task agent for 5M environment steps takes approx. 6 hours on a single NVIDIA RTX 5090 GPU, totaling an estimated 1,300 GPU hours to train expert policies for every task in MMBench. To ensure that only successful demonstrations are collected, we reject episodes that do not result in success (when available) or have episode returns that are substantially ( _>_ 25%) lower than the median for that task. Table 5 provides an overview of our demonstration dataset. For completeness, we also release all 200 checkpoints that generated the provided demonstrations; these checkpoints can be used to generate additional checkpoints, or be used for _e.g._ teacher-student policy distillation. 

_Table 5._ **Demonstrations.** An overview of the demonstrations provided for each task domain. 

|**Task domain**|**Num. tasks**|**Demos per task**|**Total demos**|
|---|---|---|---|
|DMControl|21|20|420|
|DMControl Ext.|16|20|320|
|Meta-World|49|10|490|
|ManiSkill3|36|20|720|
|MuJoCo|6|20|120|
|MiniArcade|19|10|190|
|Box2D|8|40|320|
|RoboDesk|6|20|120|
|OGBench|12|20|240|
|Atari|27|40|1080|
|**Total**|**200**|_−_|**4020**|


### **D Baselines** 

**BC.** Our multitask behavior cloning (BC) implementation closely follows that of our pretraining stage for Newt, except that it only consists of two components: the encoder _h_ and policy _p_ . Both encoder and policy are conditioned on language instructions, and are trained with a BC objective that mask invalid action dimensions such that all action vectors contribute equally to the loss regardless of number of valid dimensions for that particular task. Our single-task BC policies are identical to the multitask BC policies except they are not conditioned on language instructions. 

**PPO.** We base our PPO implementation off of the cleanRL (Huang et al., 2022b) implementation available here: https://github.com/vwxyzjn/cleanrl/tree/master/cleanrl/ 

ppo_continuous_action_isaacgym, and extend it to support language-conditioning and per-task discount factors such that comparison to our method is fair. We find that the default implementation and hyperparameters performs poorly in our massively multitask RL setting, so we make a number of additional changes. Specifically, we find that _(i)_ using a tanh-Normal policy improves training stability, that _(ii)_ increasing the number of trainable parameters from 0.5M to 3.5M leads to marginally better performance throughout training, and that _(iii)_ using longer policy rollouts (128), more mini-batches and epochs (8), a smaller value loss coefficient (1), scaled down environment 

27 

Preprint 

rewards (0 _._ 1 _×_ ), and clipping of both the surrogate objective and value function. An empirical comparison of our PPO implementation before and after these changes can be found in Appendix H; we find that these changes approximately double its average score at 100M environment steps, but that both implementations perform relatively poorly compared to FastTD3 and Newt. 

**FastTD3.** We base our TD3 implementation off of FastTD3 (Seo et al., 2025) which is available here: https://github.com/younggyoseo/FastTD3, an improved implementation of TD3 designed for the era of RL with large amounts of parallel environments. FastTD3 demonstrates robust learning across a number of different benchmarks described in Seo et al. (2025), but has not previously been evaluated in a multi-domain setting. We extend FastTD3 to support language-conditioning for compatibility with MMBench, as well as per-task discount factors to make value estimation easier across tasks. We find that _n_ -step returns of 8 are critical in our challenging multitask setting and we thus use that value by default. Appendix H shows the performance of FastTD3 for different values of _n_ . 

**Model-based pretraining.** This baseline is equivalent to the pretraining stage of Newt. Specifically, we pretrain all components from Equation 1 as described in Section 3.2 for a total of 200 _,_ 000 iterations, and report performance results without planning (simply using the policy prior as behavior policy) as we find it to perform the best immediately following the pretraining stage; planning eventually outperforms the policy prior but initially suffers from an inaccurate value function. 

**—— Appendices continue on the next page ——** 

28 

Preprint 


# **Newt** 

Appendices E _−_ F 

### **E Description of Planning Algorithm** 

Our planning algorithm closely follows that of TD-MPC2, which uses a variant of the CrossEntropy Method (CEM) or Model Predictive Path Integral (MPPI; (Williams et al., 2015)) for trajectory optimization with the learned world model. Specifically, TD-MPC2 plans trajectories by fitting a time-dependent multivariate Gaussian with diagonal covariance to a value landscape estimated with rollouts from the world model. Starting from an initial distribution parameterized by ( _µ_<sup>0</sup> _, σ_<sup>0</sup> ) _t_ : _t_ + _H , µ_<sup>0</sup> _, σ_<sup>0</sup> _∈_ R<sup>_m_</sup> _, A ∈_ R<sup>_m_</sup> , where _t_ is the current time step and _H_ is the planning horizon, we iteratively refit parameters ( _µ, σ_ ) to a weighted average of the value estimates of a small set of “elite” trajectories (those whose estimates are in the top- _K_ of trajectories sampled that given iteration), and sample another set of trajectories based on the updated parameters. After a fixed number of planning iterations, the algorithm samples a trajectory from the final optimized distribution and the agent executes the first action in the returned sequence. 

When evaluating our agent in a closed-loop manner, we replan trajectories at every time step and initialize _µ_<sup>0</sup> _, σ_<sup>0</sup> with the one-step shifted parameters of the previous time step (receding horizon MPC). When evaluating in an open-loop manner, the planning procedure returns the entire action sequence and we execute them one by one without replanning nor any environment feedback. To warm-start the planning procedure, TD-MPC2 generates a fixed number of action sequences by rolling out the model (in the latent space) using actions coming from the policy prior and adds them to the set of action sequences sampled at every iteration of the planning procedure. Our proposed constraint on the planning procedure early in training (when the model is less accurate than the policy prior pretrained on demonstrations, as we discuss in Section 3.2) initializes ( _µ_<sup>0</sup> _, σ_<sup>0</sup> ) as a linear interpolation between the action distribution coming from the policy prior _p_ and the Guassian prior used in TD-MPC2. Our annealing schedule is visualized in Figure 11. We refer the reader to Hansen et al. (2022) and Hansen et al. (2024) for more information about the planning procedure. 


_Figure 11._ **Constrained planning.** We find that biasing planning towards the action distribution of the pretrained policy helps with exploration early in training and mitigates a drop in performance when switching from the pretrained model-free policy to planning with a world model. We use a simple linear annealing schedule (from 2M to 12M steps) as shown here. 

29 

Preprint 

### **F Implementation Details** 

**Language embeddings.** We use text embeddings from openai/clip-vit-base-patch32 (CLIP; (Radford et al., 2021)) which outputs continuous embeddings of 512 dimensions. Embeddings are visualized in a low-dimensional space in Figure 5. 

**Image embeddings.** We use RGB image embeddings from facebook/dinov2-base (DINOv2; Oquab et al. (2023)) which outputs continuous embeddings of 768 dimensions. We do not use frame stacking in our experiments, but expect it to improve downstream performance as the added history information allows models to infer _e.g._ velocity information from visual observations. 

**Network architecture.** All learnable components from Equation 1 are implemented as MLPs. The encoder _h_ contains a variable number of layers depending on the architecture size, and we also vary the number of _Q_ -functions in our ensemble when training larger or smaller models than our default model size of 20M learnable parameters. MLPs consist of linear layers followed by LayerNorm (Ba et al., 2016) and Mish (Misra, 2019) activation functions, and the latent state representation is normalized using a simplicial embedding as originally proposed by Lavoie et al. (2023) and later applied in an RL context by Hansen et al. (2024). We summarize our Newt architecture for the default 20M parameter state-based agent with language-conditioning using a PyTorch-like notation: 

Encoder (2,235,904 parameters): ModuleDict( (state): Sequential( (0): NormedLinear(in_features=640, out_features=1024, bias=True, act=Mish) (1): NormedLinear(in_features=1024, out_features=1024, bias=True, act=Mish) (2): NormedLinear(in_features=1024, out_features=512, bias=True, act=Simplicial) ) ) Dynamics (2,645,504 parameters): Sequential( (0): NormedLinear(in_features=1040, out_features=1024, bias=True, act=Mish) (1): NormedLinear(in_features=1024, out_features=1024, bias=True, act=Mish) (2): NormedLinear(in_features=1024, out_features=512, bias=True, act=Simplicial) ) Reward (2,223,205 parameters): Sequential( (0): NormedLinear(in_features=1040, out_features=1024, bias=True, act=Mish) (1): NormedLinear(in_features=1024, out_features=1024, bias=True, act=Mish) (2): Linear(in_features=1024, out_features=101, bias=True) ) Policy prior (2,136,096 parameters): Sequential( (0): NormedLinear(in_features=1024, out_features=1024, bias=True, act=Mish) (1): NormedLinear(in_features=1024, out_features=1024, bias=True, act=Mish) (2): Linear(in_features=1024, out_features=32, bias=True) ) 

Q-functions (11,116,025 parameters): QEnsemble( (_Qs): ModuleList( (0-4): 5 x Sequential( (0): NormedLinear(in_features=1040, out_features=1024, bias=True, act=Mish) (1): NormedLinear(in_features=1024, out_features=1024, bias=True, act=Mish) (2): Linear(in_features=1024, out_features=101, bias=True) ) 

) ) 

When the agent is conditioned on image embeddings in addition to state and language, the encoder is expanded as follows: 

Encoder (3,022,336): ModuleDict( 

(state): Sequential( 

(0): NormedLinear(in_features=1408, out_features=1024, bias=True, act=Mish) 

(1): NormedLinear(in_features=1024, out_features=1024, bias=True, act=Mish) 

(2): NormedLinear(in_features=1024, out_features=512, bias=True, act=Simplicial) 

) 

and the total parameter count increases to 21M. We experiment with four model sizes: 2M parameters, 5M parameters, our default model with 20M parameters, and a larger model with 80M parameters; Table 6 details the specific architecture for each model size. 

**Latent state normalization.** The simplicial embedding (Lavoie et al., 2023) is a simple method for normalization of the latent representation **z** by projecting it into _L_ fixed-dimensional simplices using a softmax operation, which was first applied in an RL context by Hansen et al. (2024). A key benefit of embedding **z** as simplices (as opposed to _e.g._ a discrete representation or squashing) is that it naturally biases the representation towards sparsity without enforcing hard constraints. Intuitively, 

30 

Preprint 

the simplicial embedding can be thought of as a _”soft”_ variant of the vector-of-categoricals approach to representation learning proposed by Oord et al. (2017) (VQ-VAE). Whereas VQ-VAE represents latent codes using a set of discrete codes ( _L_ vector partitions each consisting of a one-hot encoding), a simplicial embedding partitions the latent state into _L_ vector partitions of continuous values that each sum to 1 due to the softmax operator. This relaxation of the latent representation is akin to softmax being a relaxation of the arg max operator. We follow Lavoie et al. (2023) and TD-MPC2 (Hansen et al., 2024) without modification and implement the simplicial normalization layer using PyTorch-like notation as follows: 

**def** simplicial(self, z, V=8): shape = z.shape z = z.view(*shape[:-1], -1, V) z = softmax(z, dim=-1) **return** z.view(*shape) 

Here, z is the latent representation **z** , and _V_ is the dimensionality of each simplex. The number of simplices _L_ can be inferred from _V_ and the dimensionality of **z** . We apply a softmax to each of _L_ partitions of **z** to form simplices, and then reshape to the original shape of **z** . Refer to Lavoie et al. (2023) for more details. 

_Table 6._ **Model sizes.** Architecture changes that we make for our scaling experiments. _Encoder dim_ is the dimensionality of each hidden layer in the state encoder, _MLP dim_ is the dimensionality of hidden layers in all other parts of the agent, _Latent dim_ is the dimensionality of the latent state representation, _# enc layers_ is the number of encoder layers, and _Q-ensemble_ is the number of _Q_ - functions in the ensemble. We highlight our default model parameters in **bold** . 

|Parameters|**2M**|**5M**|**20M**|**80M**|
|---|---|---|---|---|
|Encoder dim|128|256|**1024**|2048|
|MLP dim|256|512|**1024**|2048|
|Latent dim|384|512|**512**|704|
|# enc layers|2|2|**3**|4|
|Q-ensemble|3|5|**5**|7|


**Heuristic for discount factors.** Following TD-MPC2, we use the following heuristic to determine a suitable discount factor for tasks for which no default discount factor is available: 


where _T_ is the episode length _after_ applying action repeat, and clip bounds the discount factor to the interval [0 _._ 95 _,_ 0 _._ 995]. This heuristic ensures that tasks with short episodes are assigned a low discount factor, and vice-versa for tasks with long episodes. 

**Hyperparameters.** Our hyperparameters are listed in Table 7 for the default 20M parameter agent. 

31 

Preprint 

_Table 7._ **Hyperparameters.** We detail relevant hyperparameters for our method below, corresponding to our default 20M parameter agent. Our choice of hyperparameters closely follow that of TD-MPC2 (Hansen et al., 2024) with a few exceptions which we highlight in **bold** . 

|**Hyperparameter**|**Value**|
|---|---|
|**Planning**||
|Horizon (_H_)|3|
|Iterations<br>|6|
|Population size|512|
|Policy prior samples<br>|24<br>|
|Number of elites<br>|64<br>|
|Minimum std.<br>|0_._05|
|Maximum std.|2|
|Temperature<br>|0_._5<br>|
|Momentum<br>|No<br>|
|**Constrained planning**|**Anneal from 2M**_→_**12M steps**|
|**Policy prior**||
|Log std. min.|_−_10|
|Log std. max.|2|
|**Replay buffer**||
|**Capacity**|**10**_,_**000**_,_**000**|
|Sampling|Uniform|
|**Architecture (5M)**||
|**Encoder layers**|**3**|
|**Encoder dim**|**1024**|
|**MLP dim**|**1024**|
|Latent state dim|512|
|Activation|LayerNorm + Mish|
|Number of_Q_-functions|5|
|Number of reward/value bins|101|
|Simplicial dim (_V_)<br>|8<br>|
|Simplicial temperature (_τ_)|1|
|**Optimization**||
|**Update-to-data ratio**|**0**_._**075**|
|<br>**Batch size**|**1024**|
|Joint-embedding coef.|20|
|Reward prediction coef.|0_._1|
|Value prediction coef.|0_._1|
|**BC coef.**|**10**|
|Temporal coef. (_λ_)|0_._5|
|_Q_-fn. momentum coef.|0_._99|
|Policy prior entropy coef.|1_×_10<sup>_−_4</sup>|
|<br>Policy prior loss norm.|Moving(5%_,_95%)percentiles|
|<br>Optimizer|<br>Adam<br>|
|Learning rate|3_×_10<sup>_−_4</sup><br>|
|Encoder learning rate|1_×_10<sup>_−_4</sup>|
|Gradient clip norm|20|
|<br>Discount factor|Heuristic|


32 

Preprint 


# **Additional results** 

Appendices G _−_ J 

### **G Open-Loop Control** 


_Figure 12._ **Additional qualitative results for open-loop control.** Executing open-loop plans without any environment feedback. Our results demonstrate that Newt learns meaningful representations. 

_Table 8._ **Open-loop control.** Quantitative results when planning for 48 or 24 consecutive time steps, depending on the task. We report the fraction of original closed-loop control performance achieved in an open-loop manner after 33%, 66%, and 100% of the planned time steps. Higher is better _↑_ . 

|Task|_t_= 16|_t_= 32|_t_= 48|
|---|---|---|---|
|Walker Walk|0_._68|0_._40|0_._25|
|Finger Turn Hard|0_._41|0_._39|0_._29|
|Assault|0_._00|0_._10|0_._08|
|Lunarlander Takeoff|0_._67|0_._40|0_._34|
|**Average**|**0**_._**44**|**0**_._**32**|**0**_._**24**|
|Task|_t_= 8|_t_= 16|_t_= 24|
|Point Maze|0_._88|0_._67|0_._37|
|Pick Screwdriver|0_._95|0_._89|0_._83|
|Poke Cube|0_._50|0_._38|0_._35|
|Push Green|0_._95|0_._89|0_._83|
|**Average**|**0**_._**82**|**0**_._**71**|**0**_._**60**|


33 

Preprint 

### **H Additional Experiments** 


_Figure 13._ **Per-domain performance (additional baselines).** Average score of a _single_ agent in each of the 10 task domains in MMBench (200 tasks). These baselines complement the results shown in Figure 7. 


_Figure 14._ **Per-domain performance (ablation on planning).** Average score of a _single_ agent in each of the 10 task domains in MMBench (200 tasks). We compare the performance of our method with and without planning with MPC. The default formulation of Newt uses planning; the baseline without planning instead uses the learned policy prior for decision-making. Our results indicate that planning plays a key role in massively multitask online RL, but that the policy prior in rare cases (MuJoCo) may outperform planning. 

34 

Preprint 


_Figure 15._ **Ablations on baselines.** We compare baseline performance across different hyperparameter configurations, and find that it has moderate impact on data-efficiency and overall performance. 

_Table 9._ **Comparison to single-task TD-MPC2 agents.** Performance (normalized score; higher is better _↑_ ) comparison between our multitask Newt agent trained for a total of 100M environment steps across all tasks (500k per task), and single-task TD-MPC2 agents trained until convergence (5M environment steps per task; 1B total steps across all tasks). We also include more fair comparisons in which the population of single-task agents have been exposed to the _same_ total number of environment steps as our Newt agent. We observe that the multitask agent generally lags behind the population of single-task agents in terms of performance but that the extent to which that is the case varies drastically between task domains. 

|||Mul|titask|S|ingle-task||
|---|---|---|---|---|---|---|
|**Task domain**|**Num. tasks**|**N**|**ewt**|**T**|**D-MPC2**||
|||@20M|@100M|@20M|@100M|@1B|
|DMControl|21|0_._49|0_._50|0_._32|0_._67|0_._81|
|DMControl Ext.|16|0_._26|0_._37|0_._24|0_._60|0_._78|
|Meta-World|49|0_._32|0_._50|0_._53|0_._70|0_._79|
|ManiSkill3|36|0_._52|0_._69|0_._36|0_._77|0_._92|
|MuJoCo|6|0_._18|0_._20|0_._35|0_._64|0_._82|
|MiniArcade|19|0_._40|0_._44|0_._50|0_._75|0_._94|
|Box2D|8|0_._19|0_._33|0_._60|0_._87|0_._86|
|RoboDesk|6|0_._42|0_._38|0_._48|0_._67|0_._82|
|OGBench|12|0_._29|0_._30|0_._43|0_._65|0_._93|
|Atari|27|0_._14|0_._13|0_._13|0_._24|0_._51|
|**Total**|**200**|**0**_._**31**|**0**_._**44**|**0**_._**38**|**0**_._**65**|**0**_._**80**|


35 

Preprint 

### **I Per-Task Results** 


_Figure 16._ **DMControl.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 

36 

Preprint 


_Figure 17._ **DMControl Extended.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 

37 

Preprint 


_Figure 18._ **Meta-World.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 

38 

Preprint 


_Figure 19._ **ManiSkill.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 

39 

Preprint 


_Figure 20._ **MuJoCo.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 


_Figure 21._ **Box2D.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 


_Figure 22._ **RoboDesk.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 

40 

Preprint 


_Figure 23._ **OGbench.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 


_Figure 24._ **MiniArcade.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 

41 

Preprint 


_Figure 25._ **Atari.** Per-task normalized scores for our 20M parameter Newt agent jointly trained on all 200 tasks from MMBench. _Environment steps_ refers to **total** steps across all tasks. 

42 

Preprint 

### **J Loss Curves** 


_Figure 26._ **Loss curves** for our method with and without language instructions. These curves indicate that learning is stable across both agents, but that the agent with access to language instructions generally has a lower loss during training. 

43 

