---
title: "Interactive Post-Training for Vision-Language-Action Models"
date: "2025-05-22"
authors: "Shuhan Tan; Kairan Dou; Yue Zhao; Philipp Krähenbühl"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2505.17016
pdf: https://arxiv.org/pdf/2505.17016
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.17016)** / [論文ページ](https://arxiv.org/abs/2505.17016)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Interactive Post-Training for Vision-Language-Action Models** 

**Shuhan Tan**<sup>1</sup> **, Kairan Dou**<sup>2</sup> **, Yue Zhao**<sup>1</sup> **, Philipp Krähenbühl**<sup>1</sup> UT Austin<sup>1</sup> , Nankai University<sup>2</sup> `Code & Model: https://ariostgx.github.io/ript`<sup>`_`</sup> `vla/` 

## **Abstract** 

We introduce `RIPT-VLA` , a simple and scalable reinforcement-learning-based interactive post-training paradigm that fine-tunes pretrained Vision-Language-Action (VLA) models using only sparse binary success rewards. Existing VLA training pipelines rely heavily on offline expert demonstration data and supervised imitation, limiting their ability to adapt to new tasks and environments under low-data regimes. `RIPT-VLA` addresses this by enabling interactive post-training with a stable policy optimization algorithm based on dynamic rollout sampling and leaveon-out advantage estimation. `RIPT-VLA` has the following characteristics. First, `RIPT-VLA` applies to various VLA models, resulting in an improvement on the lightweight QueST model by 21.2%, and the 7B OpenVLA-OFT model to an unprecedented **97.5%** success rate. Second, `RIPT-VLA` is computationally efficient and data-efficient: With only one demonstration, `RIPT-VLA` enables an unworkable SFT model ( **4%** ) to succeed with a **97%** success rate within **15** iterations. Furthermore, we demonstrate that the policy learned by `RIPT-VLA` generalizes across different tasks and scenarios and is robust to the initial state context. These results highlight `RIPT-VLA` as a practical and effective paradigm for post-training VLA models through minimal supervision. 


Figure 1: Overview of `RIPT-VLA` . While VLA models are typically trained with two supervised stages, we propose a third stage: Reinforcement Interactive Post-Training for VLA. `RIPT-VLA` sets state-of-the-art results across diverse benchmarks. It also presents remarkable improvement under the low-data regime, transforming an SFT model from near failure to 97% with one demonstration. 

## **1 Introduction** 

Vision-Language-Action (VLA) models [40] aim to enable agents to perceive, reason, and act in the physical world with a unified interface. Current VLA models are trained with two supervised stages: large-scale pretraining on diverse human demonstrations, followed by supervised fine-tuning (SFT) on smaller-scale task-specific datasets. This paradigm has some distinct advantages: Pre-training enables the VLA model to build general visuomotor skills while SFT allows it to specialize in specific environments [15]. Supervised training allows VLA models to learn from large-scale pre-recorded vision-language-action datasets. However, this supervised approach also has two core limitations: First, data are collected offline. The VLA model learns to imitate interactions with the environment, but never sees the consequences of its own actions. As a result, the learned policy often fails to handle the complexities of real-world scenarios, especially for long-horizon tasks. Second, task-specific SFT via imitation learning relies heavily on large-scale, high-quality human demonstrations. These data are expensive and time-consuming to collect, and performance degrades significantly when only a small number of demonstrations are available. 

In this paper, we propose `RIPT-VLA` : a third stage for VLA training paradigm with **R** einforcement **I** nteractive **P** ost- **T** raining. After pretraining and supervised fine-tuning, we allow the VLA model to interact with the multitask environment and receive binary success/failure rewards. We then optimize the VLA model to directly improve its success rate across multiple tasks through reinforcement learning. Inspired by prior RL frameworks for LLMs reasoning [9], we propose a stable and efficient RL framework for VLA finetuning in Section 4. Specifically, we extend the LOOP framework [4] which combines REINFORCE leave-one-out (RLOO) advantage estimation [16] and proximal policy optimization (PPO) [28]. Unlike LOOP, we construct uniform batches of non-zero advantage samples, filtering out any group of trajectories with zero-advantage, and sampling rollouts until sufficient samples exist. This uniform batch construction leads to improved training stability, especially as training progresses and the VLA becomes more successful. `RIPT-VLA` allows efficient and stable VLA policy update _without_ relying on shaped or learned rewards, or critic models. Using Reinforcement Learning in a third training stage has a few distinct advantages: It is more data efficient, yielding close to state-of-the-art performance with only a single SFT demonstration. The resulting VLA model achieves a much higher performance on the end-task, as it gets to see interactions with the environment during training. `RIPT-VLA` works with both tokenized [22] and continuous actions [14]. 

`RIPT-VLA` resonates with the recent trend of paradigm shift in LLM training [24, 9]. While pretraining on large-scale text corpora equips LLMs with broad knowledge and powerful skills, they often struggle with challenging tasks that require precise reasoning, multi-step planning, or tool using [34]. To address these limitations, reinforcement learning has emerged as a critical post-training stage to reactivate and steer pretrained knowledge with only a small amount of interactive feedback [24]. Similarly, we observe that pretrained VLA models also encode rich visuomotor skills, yet struggle to apply them effectively for new tasks and scenarios. `RIPT-VLA` bridges this gap by using only sparse binary rewards to unlock these latent skills with a small number of optimization steps. 

Through comprehensive experiments in Section 5, we demonstrate that `RIPT-VLA` achieves state-ofthe-art results when combined with both large-scale and lightweight VLA models across a diverse set of tasks. On the LIBERO benchmark [21], `RIPT-VLA` improves QueST [22], the best lightweight VLA model, on all four task suites by **10.9%** absolute success rate (SR) on average (Table 1). When evaluated on OpenVLA-OFT [14], the best-performing large VLA model with an already high success rate (96.7%), `RIPT-VLA` still helps by further reducing the failure rate from 3.3% to 2.5%. We also achieve top performance on many-task benchmarks LIBERO-90 **(94.3%)** and MetaWorld45 [36] ( **92.2%** ), showing the effectiveness of `RIPT-VLA` in improving multi-task (up to 90) performance with a single model (Table 2). Most notably, in the extreme low-data regime with only a single training demo, `RIPT-VLA` adapts pretrained knowledge to new task goals or scenarios with remarkable efficiency, boosting success rate from below 4% to over 97% within only 15 RL iterations. 

## **2 Related Works** 

**Vision-Language-Action Models.** Vision-Language-Action (VLA) models empower embodied agents to interpret multimodal inputs—such as visual observations and natural-language instructions—and translate them into meaningful actions within the physical world [40]. Seminal works like RT-2 [40], RT-1 [2], PaLM-E [7], Octo [32], Dita [11], _π_ 0 [1], and _π_ 0 _._ 5 [13], together with 

2 

OpenVLA [15], showcase VLAs achieving emergent semantic reasoning and generalization to novel tasks and environments. These models are typically developed through a two-stage supervisedlearning paradigm that begins with an initial pre-training phase on extensive, web-scale datasets [7, 3], which is crucial for acquiring generalizable visuomotor skills, grounding language in perception, and building robust internal representations. While this two-stage approach has advanced the field, its offline nature imposes key limitations. The supervised fine-tuning (SFT) stage typically requires vast expert demonstrations for new tasks or environments, thereby degrading few-shot performance. This highlights a critical gap: the need for methods that adapt pretrained VLAs beyond static imitation by leveraging interactive experience and reducing reliance on extensive expert data. 

**Reinforcement Learning for Large Language Models.** Large Language Models (LLMs) offer a precedent for enhancing pretrained models. While LLMs gain broad capabilities via pre-training and SFT, they often struggle with complex reasoning, planning, or constraint satisfaction [34]. To address this, Reinforcement Learning (RL) has emerged as a transformative third stage in LLM training—enabling learning from interactive feedback rather than static datasets [24]. Recent progress shows RL can unlock latent capabilities for math [19, 29], self-verifiable proofs [20], long-horizon planning through tree-of-thoughts [35], and preference-aligned generation with AI feedback [17]. This paradigm, in which pretrained knowledge is steered by targeted feedback, strongly motivates a similar approach for Vision-Language-Action models: RL has the potential to adapt pretrained VLAs more effectively to the interactive and consequential nature of embodied tasks. 

**Reinforcement Learning for VLA.** Recent works have explored applying reinforcement learning to pretrained VLA models to overcome limitations of supervised fine-tuning and adapt to novel tasks without collecting new demonstrations. iRe-VLA [10] addresses optimization instability by alternating between PPO-based updates on a frozen VLM backbone and supervised distillation stages. However, it still relies on a learned value critic during PPO, and requires shaped reward functions or success weighting to guide policy learning. ConRFT [5] further combines offline Q-learning with online consistency-policy updates, but similarly depends on a parameterized value function. Both methods require careful coordination between offline and online stages to stabilize critic learning. In contrast, `RIPT-VLA` introduces a fully critic-free optimization framework with simpler training dynamics under sparse binary rewards. 

## **3 Preliminary** 

### **3.1 Vision-Language-Action Models** 

**Autoregressive VLA rollout.** A vision-language-action (VLA) model _πθ_ maps a sequence of observations and previous actions ( _o_ 1: _t, a_ 1: _t−_ 1), along with a natural language goal _g_ , to a probability distribution over the next action _at_ . These models operate autoregressively: _at ∼ πθ_ ( _· | o_ 1: _t, g, a_ 1: _t−_ 1). Given an initial observation-goal pair context **c** = ( _o_ 1 _, g_ ), the model generates a sequence of actions conditioned on past information in an autoregressive way: 


We denote this sampling process as **a** = _a_ 1: _T ∼ πθ_ ( _· |_ **c** ), the observation sequence as **o** = _o_ 1: _T_ . Sequences terminate upon task success or reaching a time limit. For each rollout sequence and task goal _g_ , the environment _E_ returns a binary reward _R_ = 1 when the task goal is successfully reached, and _R_ = 0 otherwise. The environment _E_ can be either a simulator [36, 21] or the real world. 

There are two common ways of action prediction in VLA models. The _tokenized action head_ represents actions as discrete tokens from a fixed vocabulary and predicts actions via classification over the token set. In contrast, the _regression action head_ directly predicts real-values action vectors via regression. 

**Current VLA training paradigm.** Current Vision-Language-Action (VLA) models are typically trained in two stages: **Stage 1: Pretraining** and **Stage 2: Supervised Fine-tuning** . 

In Stage 1, a base policy _πθ_ is pretrained on a large-scale, diverse dataset of real-world demonstrations, denoted by _D_ pretrain = _{_ ( **o** _,_ **a** _, g_ ) _}i_<sup>_N_</sup> =1<sup>.The policy is trained to imitate the ground-truth actions given</sup> 

3 

offline data in _D_ pretrain. For VLA models with a tokenized action head, the loss is: 


while for regression action head _L_ pre( _θ_ ) is implemented as an MSE or L1 loss. This stage enables VLA models to capture strong representations and learn general visuomotor and instruction-following capabilities. 

In Stage 2, the pretrained policy is supervised fine-tuned on a smaller, multitask dataset to improve performance on a small set of target tasks, denoted by _D_ sft = _{_ ( **o** _,_ **a** _, g_ ) _}_<sup>_N_</sup> _i_ =1<sup>_′_.Typically,</sup><sup>_D_sftcontains</sup> around 50 high-quality human demonstrations per task [22]. The VLA model is trained with the same objective function as in Stage 1. This stage enables the model to adapt its learned skills from Stage 1 to a specialized set of skills for the target tasks. 

Although being the standard process of VLA training, this two-stage process has two significant issues. Firstly, it relies only on offline supervision and lacks interactive feedback from the environment. Therefore, the learned policy may often fail in real rollouts due to distribution shift and cascading errors, especially for long-term rollouts. Furthermore, the performance of VLA heavily relies on the high quality and quantity of the task-specific data in _D_ sft, which is often hard and costly to obtain. 

**VLA as Markov decision processes.** To better optimize VLA models, we define its task as a Markov decision process (MDP). Each episode is initialized with a context **c** = ( _o_ 1 _, g_ ). The _state_ is represented as [ _o_ 1: _t, g, a_ 1: _t−_ 1], which includes the language goal _g_ , the sequence of past observations _o_ 1: _t_ , and past actions _a_ 1: _t−_ 1. At each timestep _t_ , the VLA policy produces an _action_ sampled from the policy distribution: _at ∼ πθ_ ( _· | o_ 1: _t, g, a_ 1: _t−_ 1). The environment transitions to the next observation _ot_ +1 based on hidden environment dynamics, producing a new state [ _o_ 1: _t_ +1 _, g, a_ 1: _t_ ]. After a sequence of actions _a_ 1: _T_ , the agent receives a binary _reward R_ ( **c** _,_ **a** ) _∈{_ 0 _,_ 1 _}_ from the environment _E_ , indicating task success or failure. The objective of VLA optimization is essentially learning a policy _πθ_ that maximizes expected task success reward: 


### **3.2 Reinforcement Policy Optimization** 

We consider the reinforcement learning setting where an agent interacts with an environment _E_ to learn a policy _πθ_ ( **a** _|_ **c** ) that maximizes the expected return: E **c** _∼D_ context _,_ **a** _∼πθ_ [ _R_ ( **c** _,_ **a** )] _,_ where **c** is the context (e.g., goal and initial observation), **a** is a trajectory (e.g., sequence of actions), and _R_ ( **c** _,_ **a** ) _∈{_ 0 _,_ 1 _}_ is a sparse binary reward returned by the environment. To optimize this objective, a standard approach is policy gradient, which updates _πθ_ with: 


where _A_ ( **c** _,_ **a** ) is the advantage function indicating how much better the action **a** is compared to a baseline. In practice, it is hard to compute _A_ ( **c** _,_ **a** ), especially under sparse rewards. To address this issue, a recent work proposed a critic-free optimization framework called Leave-One-Out Proximal Policy Optimization ( **LOOP** ) [4]. Specifically, it combines the two methods below. 

**Leave-One-Out Advantage Estimation (RLOO) [16].** For each sampled context **c** , we draw _K_ rollouts _{_ **a** _k ∼ πψ_ ( _· |_ **c** ) _}_<sup>_K_</sup> _k_ =1<sup>underafixedsamplingpolicy</sup><sup>_πψ_.Eachrolloutreceivesabinary</sup> reward _Rk_ = _R_ ( **c** _,_ **a** _k_ ). The leave-one-out baseline for rollout _k_ is computed by averaging the other rewards: 


This group-normalized advantage indicates how much better or worse a rollout performance is relative to others given the same context. This allows us to efficiently compute a stable advantage signal from sparse binary rewards, without requiring learning value functions. 

**Proximal Policy Optimization (PPO) [28].** To update _πθ_ using collected rollouts _{_ ( **c** _k,_ **a** _k, Ak_ ) _}_ , we compute the importance ratio _rk_ = _πθ_ ( **a** _k |_ **c** _k_ ) _/πψ_ ( **a** _k |_ **c** _k_ ), where _πθ_ is the current updating policy and _πψ_ is the fixed sampling policy (normally set to the latest checkpoint of _πθ_ ). We then optimize _πθ_ with the following clipped objective: 


4 

|**Algorit**|**hm 1**`RIPT-VLA`:**R**einforcement**I**nteractive**P**ost-**T**raining|for**VLA**Model|
|---|---|---|
|**Input:** <br>1: **for**|Pretrained VLA_πθ_, reward function_R_(**c**_,_**a**), context datas<br>step= 1to_M_ **do**<br>|et_D_context|
|2:|Update sampling VLA_πψ ←πθ_||
|3:|Initialize empty dataset_D_rollout _←∅_||
|4:|**while**_|D_rollout_| < B_**do**<br>|_▷_**Rollout Collection**|
|5:|Sample a context**c**_←_(_g, o_1)_∼D_context<br>||
|6:|Generate_K_ rollouts_{_**a**_k ∼πψ_(_· |_**c**)_}_<sup>_K_</sup><br>_k_=1<br>|_▷_**Group Sampling**|
|7:|Compute rewards_{Rk ←R_(**c**_,_**a**_k_)_}_<sup>_K_</sup><br>_k_=1<br>||
|8:|Compute baselines: _bk ←_<br>1<br>_K−_1<br>�<br>_j̸_=_k _<sup>_Rj_</sup>|_▷_**Leave-One-Out Baseline**|
|9:|Compute advantages: _Ak ←Rk −bk_ for each_k_<br>||
|10:|**if**all_A_= 0**then**<br>|_▷_**Dynamic Rejection**|
|11:|**continue**<br>||
|12:|**end if**||
|13:|Add(**c**_,_**a**_k, Ak_)for all_k_to_D_rollout||
|14:|**end while**||
|15:|**for**iteration= 1to_N_ **do**||
|16:<br>17:<br>|Update_πθ_ with PPO loss (Equation 6) over_D_rollout<br>**end for**<br>|_▷_**Policy Optimization**|
|18: **en**|**d for**||


where _ϵ_ is a small updating threshold (we use 0.2). This objective encourages rollouts with positive advantages while preventing unstable updates when _πθ_ deviates too far from its previous version _πψ_ . 

LOOP adopts PPO to optimize the advantage estimated by RLOO, which enables sample-efficient policy optimization in sparse reward settings without critics. It serves as an out-of-box working implementation for our interactive post-training framework in Section 4. 

## **4** `RIPT-VLA` 

As mentioned above, there is a gap between the current VLA training paradigm and our essential goal of making it work in our downstream tasks. On one hand, pure supervised training on offline data makes the policy fragile in real rollout due to compounding errors and the distribution gap between the offline dataset and online rollout. Furthermore, one has to collect a sufficient number of high-quality demonstrations for offline datasets, especially _D_ sft, the model can easily overfit to the training distribution. In other words, optimizing VLA through Equation 2 does not necessarily improve the VLA’s task execution success rate in Equation 3. To bridge this gap, we propose a new VLA training paradigm that directly optimize pretrained VLA through interaction with the environment _E_ through **R** einforcement **I** nteractive **P** ost- **T** raining, or `RIPT-VLA` for short. 

### **4.1 Reinforcement Interactive Post-Training for VLA Models** 

The first two stages of our VLA training paradigm are the same as the standard setting. In Stage 1, we pretrain the VLA model on a large, diverse dataset _D_ pretrain to learn visual-language representation and general visuomotor skills. Then, in Stage 2, we finetune VLA on a small dataset _D_ sft to adapt it to follow instructions to solve a small set of target tasks. These stages produce a pretrained VLA policy _πθ_ that can achieve a non-zero success rate (can be very low) on the target tasks. 

In `RIPT-VLA` , we then conduct **Stage 3: Reinforcement Interactive Post-Training** . In this stage, we assume we can rollout _πθ_ in an environment _E_ and receive a binary reward _R_ ( **c** _,_ **a** ) _∈{_ 0 _,_ 1 _}_ given **a** _∼ πθ_ ( _· |_ **c** ), where **c** is the initial context. In addition, we use an initial context dataset _D_ **c** = _{_ ( _o_ 1 _, g_ ) _}_ to set up task initializations for model rollouts. Typically, we obtain _D_ **c** by directly extracting the initial states from sequences in _D_ sft. For each optimization step, we iterate between two steps: **rollout collection** and **policy optimization** . 

During _rollout collection_ , we randomly sample contexts **c** _i ∼D_ **c** and let _πθ_ interact with the environment _E_ to output a sequence **a** _i_ . For each rollout we collect its reward _R_ ( **c** _i,_ **a** _i_ ) and compute its advantage _Ai_ = _A_ ( **c** _i,_ **a** _i_ ), which indicate how strong the model should be encouraged ( _A >_ 0) or 

5 

penalized ( _A <_ 0) for generating rollout **a** . We add all rollouts and rewards ( **c** _i,_ **a** _i, Ai_ ) to a rollout dataset _D_ rollout until we obtain _B_ rollouts: _D_ rollout = _{_ ( **c** _i,_ **a** _i, Ai_ ) _}_<sup>_B_</sup> _i_ =1 

During _policy optimization_ , we optimize _πθ_ with reinforcement learning algorithms on _D_ rollout to maximize its expected task success rate in Equation 3 for _N_ iterations. After optimization, we use the updated VLA policy _πθ_<sup>_′_to collect new rollouts and a new step begins.This process repeats until</sup> we reach _M_ steps and outputs the final policy _πθ_<sup>_∗_, concluding the full VLA training paradigm.We</sup> then deploy _πθ_<sup>_∗_in the environment for testing.</sup> 

Although `RIPT-VLA` is simple in concept, it presents several challenges. First, we only have sparse binary rewards from each rollout sequence, no shaped reward is available. Training a learned reward model to predict shaped reward values can easily lead to reward hacking [30], especially with limited rollout data. Second, as VLA models operate over long-horizon, multi-task environments, credit assignment becomes highly ambiguous. This causes the value target (e.g., from TD error) to be extremely noisy and uninformative. Third, training a stable value function for VLA requires a model of comparable capacity to the VLA itself, which significantly increases GPU memory usage and training cost for large VLA models [38]. Finally, in multitask environments, different task contexts can vary significantly in difficulty: some lead to trivial success while others consistently fail across all rollouts. This results in highly imbalanced success rates and unstable policy gradient updates. 

### **4.2 Dynamic-Sampling Leave-One-Out Proximal Policy Optimization** 

To implement `RIPT-VLA` in a stable and sample-efficient way, we propose a simple yet effective policy optimization framework in Algorithm 1. First, we adopt LOOP (Section 3.2) as the foundation of our implementation. LOOP is particularly well-suited for our VLA setting, where rollouts are long-horizon and efficient advantage estimation is required for its sparse reward signal. Furthermore, for VLA in multitask environments, we design a dynamic rollout sampling mechanism to filter out uninformative contexts for more stable and efficient policy optimization. 

**LOOP for** `RIPT-VLA` **.** We apply LOOP [4] for both the rollout collection and policy optimization stage. During rollout collection, we conduct RLOO [16] advantage estimation. In this step, we use the most recent policy _πθ_ as the sampling policy _πψ_ . Given a single context **c** _∼D_ **c** , we collect _K_ trajectories by repeatingly sampling _K_ times from the policy given the same context: _{_ **a** _k ∼ πψ_ ( _· |_ **c** ) _}k_<sup>_K_</sup> =1<sup>.We obtain their corresponding rewards</sup><sup>_{Rk}K_</sup> _k_ =1<sup>from the environment</sup><sup>_E_.For</sup> each rollout _k_ , we compute the advantage _Ak_ with Equation 5. For each epoch, we conduct group sampling on _B/K_ contexts sampled from _D_ **c** , obtaining _D_ rollout with _B_ rollouts. 

During policy optimization, we use PPO [28] to stabilize policy gradient updates. For each rollout sample ( **c** _i,_ **a** _i, Ai_ ) _∈D_ rollout, we can compute its training objective _L_ PPO with Equation 6. We perform this update over the collected rollout dataset _D_ rollout using mini-batches for _N_ optimization steps each epoch. When _N_ = 1, the method corresponds to on-policy RLOO; when _N >_ 1, the same samples are reused for additional updates, resulting in a partially off-policy optimization. 

**Dynamic rollout sampling.** VLA models often operate in multitask environments [15, 22, 31], where task difficulty varies widely across different contexts. Some contexts have already been well solved by the VLA model, leading to trivial success across _K_ -group sampling, while others consistently fail due to inherent task complexity or distribution gap. Both cases result in rollout groups where all rollout samples receive identical rewards (all ones or all zeros), producing all-zero advantages in Equation 5. Therefore there is no gradient signal from Equation 6. Adding these samples to _D_ rollout makes unstable gradient updates during batch optimization, as they contribute zero gradients that can dilute meaningful learning signals. 

To address this, we apply a simple yet effective dynamic rejection strategy: we discard any sampled context for which all _K_ rollouts receive the same reward and resample a new context from _D_ context for group sampling. As training progresses and the policy improves, an increasing number of task contexts yield uniformly successful rollouts. Dynamic rejection naturally filters out these solved contexts, allowing optimization to concentrate on the remaining harder contexts. Importantly, this method make the batch optimization of the PPO loss (Equation 6) to have the same effective batch size over all the minibatches across _D_ rollout, which we empirically found to be important for stable policy optimization in `RIPT-VLA` . 

The full implementation of our optimization procedure is summarized in Algorithm 1. 

6 

### **4.3 Generalizing** `RIPT-VLA` **to Different VLA models** 

`RIPT-VLA` is compatible with both discrete and continuous action representations commonly used in VLA models. `RIPT-VLA` requires the VLA model being able to output a probability distribution over actions at each step, which is used in two key steps. First, during rollout collection, to support diverse rollouts in group sampling for the same initialization context, we need to randomly sample different actions from its output distribution: 


On the other hand, to perform stable policy optimization, we compute the trust region _ri_ =<sup>_πθ_</sup><sup><u>(</u></sup><sup>**a**</sup><sup>_i|_</sup><sup>**c**</sup><sup>_i_</sup><sup><u>)</u></sup> _πψ_ ( **a** _i|_ **c** _i_ ) in Equation 6 to constrain policy updates within a small region of the original policy. A key component in this formulation is computing the log-probability of the sampled action sequences under both policies. We compute the log-probability of a sampled action sequence **a** = ( _a_ 1 _, . . . , aT_ ) as the sum of the per-step log-probabilities: 


In other words, we can apply `RIPT-VLA` to any VLA model _πθ_ that we sample a random action _at_ from the per-step action distribution and compute log _πθ_ ( _at | a<t,_ **c** ). 

**Tokenized action head.** For VLA models with discrete action outputs, _e.g._ QueST [22], actions are predicted as sequences of discrete tokens from a fixed vocabulary, where the action header is a classification head trained with NLL loss. Therefore, log _πθ_ ( _at | a<t,_ **c** ) is directly obtained from applying softmax function to the model’s classification head output logits. We can also simply sample action tokens from the distribution after softmax. 

**Regression action head.** For continuous-action VLA models [14], actions are regressed using MSE or L1 loss, which do not produce a log-probability. To enable policy gradient optimization, we extend the model with a light-scale prediction head that estimates the scale _σθ_ of the action value. Assuming the original output head provides the mean _µθ_ , we treat the policy as a factorized Gaussian (MSE) or Laplace (L1) distribution and train the scale head using the NLL loss in Equation 2 for a few iterations on _D_ sft. After that, we can sample action _at_ and compute log _πθ_ ( _at | a<t,_ **c** ) with predicted _µθ_ and _σθ_ in a closed form. 

## **5 Experiments** 

We evaluate `RIPT-VLA` on two widely used benchmarks for VLA learning: LIBERO [21] and MetaWorld [36]. We study several settings: (1) standard multitask (up to 90 tasks) setting in Sec. 5.2, (2) few-shot (1 _∼_ 5 demonstration) setting in Sec. 5.3, and (3) cross-task and cross-scenario setting in Secs. 5.4 and 5.5 to showcase the ability of fast generalization leveraging prior knowledge during pretraining. Additionally, we conducted studies to analyze the practical behavior of `RIPT-VLA` , including training curves, ablation studies as well as its sensitivity to the variance and diversity of the context dataset. 

### **5.1 Setup** 

**Benchmark.** LIBERO [21] is a lifelong learning benchmark with 5 task suites. Each suite consists of a set of language-guided manipulation tasks across multiple object types, task definitions and environment scenarios. Specifically, it includes 4 suites: **Goal** , **Spatial** , **Object** , and **Long** . Each suite is designed to evaluate a specific aspect of object manipulation and containing 10 distinct tasks. In addition, it also includes a **LIBERO-90** suite that contains 90 different tasks to assess multitask performance at scale. MetaWorld [36] is a manipulation task benchmark for few-shot learning models. We use Meta-Learning 45 (ML45) suite that contains 45 training tasks and 5 held-out tasks. 

For both benchmarks, each task comes with 50 expert demonstrations for training. At evaluation time, a single VLA model is deployed across all tasks in a suite and performs rollouts on 50 held-out test contexts per task. We measure performance with the average task success rate (SR). 

7 

||**Stag**|**e 1 + Stage 2**|**Models**|||
|---|---|---|---|---|---|
|**Method**|**Goal**|**Spatial**|**Object**|**Long**|**Average**|
|Octo [32]|84.6|78.9|85.7|51.1|75.1|
|OpenVLA [15]|79.2|84.7|88.4|53.7|76.5|
|Dita [11]|85.4|84.2|96.3|63.8|82.4|
|_π_0 + FAST [26]|88.6|96.4|96.8|60.2|85.5|
|_π_0 [1]|95.8|96.8|**98.8**|85.2|94.2|
|OpenVLA-OFT* [14]|97.9|97.6|98.4|92.9|96.7|
|**OpenVLA-OFT +**`RIPT`|**99.0 (+1.1)**|**98.6 (+1.0)**|98.6<br>**(+0.2)**|**93.8 (+0.9)**|**97.5 (+0.8)**|
|||**Stage-2 Mode**|**ls**|||
|**Method**|**Goal**|**Spatial**|**Object**|**Long**|**Average**|
|Diffusion Policy [6]|68.3|78.3|92.5|50.5|72.4|
|Seer [33]|–|–|–|78.7|–|
|MDT [27]|73.5|78.5|87.5|64.8|76.1|
|MDT+ [27]|–|95.2|97.8|83.0|–|
|QueST [22]|80.8|87.4|93.6|68.8|82.7|
|**QueST +**`RIPT`|**92.7 (+11.9)**|**95.6 (+8.2)**|**98.4 (+4.8)**|**87.5 (+18.7)**|**93.6 (+10.9)**|


Table 1: Multitask SR(%) on the four LIBERO suites. **Bold** indicates best result and underline marks the second-best. Improvements from `RIPT-VLA` are **marked in red** . *: OpenVLA-OFT results are obtained from running official checkpoints for each suite. 

**Base models.** We conduct `RIPT-VLA` on two pretrained VLA models with different design choices. OpenVLA-OFT [14] is an _Optimized Fine-Tuned_ variant of the 7B OpenVLA model [15]. OpenVLA is initialized from a multimodal backbone that combines a _Llama-2 7B_ language model with dual vision encoders [23, 37] and is pretrained on 970k robot-manipulation demonstrations. OFT replaces the original tokenized action decoder with a continuous decoding head and trains with an L1 regression loss. This architecture represents the _large-scale regression action_ VLA. 

QueST [22], on the other hand, is a _small-scale tokenized action_ VLA model with 20 million parameters. QueST first learns a VQ-VAE that compresses short motion segments into a discrete _skill codebook_ ; a GPT-style transformer then autoregressively predicts these skill tokens conditioned on images and language, and a small decoder turns tokens back into continuous joint commands. 

**Implementation details.** For OpenVLA-OFT, we fine-tune the model using the official checkpoints provided for each task suite. Training is conducted on 4 NVIDIA RTX A5000 GPUs, each with 24 GB memory. We use LoRA [12] with rank 32, and set _K_ = 8, _B_ = 192(8 _×_ 24), _N_ = 1 and _ϵ_ = 0 _._ 1, PPO mini-batch size of 4 per GPU. We set a learning rate of 1e _−_ 4 for the LoRA modules and 1e _−_ 5 for the action head. Following Section 4.3, before applying `RIPT-VLA` , we first train a small Laplace scale header from scratch (with the same architecture as the action header) with NLL loss on _D_ sft for 500 steps. For rollout collection during training, we randomly sample actions according to the Laplace distribution with scale predicted by this header. For evaluation, we directly use the mean value predicted by the original action header. 

For QueST, as official checkpoints are not provided, we first train the base model from scratch for each task suite following the official code and hyperparameters. In the multitask setting, we conduct `RIPT-VLA` on 3 GPUs with _K_ = 16, _B_ = 2880 (16 _×_ 180). For the single-task setting, we use 1 GPU with _K_ = 16, _B_ = 160. For both settings, we set _N_ = 20, PPO mini-batch size of 8 per GPU, a learning rate of 1e _−_ 6, and the clipping parameter _ϵ_ = 0 _._ 2. 

### **5.2 Standard Multitask Training** 

In this section, we evaluate `RIPT-VLA` under standard multitask benchmarks. For each suite, we use all 50 expert demonstrations per task as its SFT dataset _D_ sft. We conduct `RIPT-VLA` to finetune a base model on the corresponding dataset for each task suite. 

Table 1 compares multitask performance on four LIBERO suites for different VLA models. We organize the results into two sets based on VLA training paradigm. In the **Stage 1+ Stage 2** set, we include 5 state-of-the-art large VLA models: Octo [32], OpenVLA [15], Dita [11], _π_ 0 [1] and 

8 

||**Full Dat**|**a**|**5-shot**|**Data**||LIBERO-LONG (5-shot)|
|---|---|---|---|---|---|---|
|**Method**|**LIBERO-90**|**ML45**|**LONG**|**ML45**|80||
|ACT [8]|50.8|90.8|42.0|70.8|||
|PRISE [39]|54.4|80.4|52.7|66.8|60||
|DP [6]|75.4|90.3|45.9|65.0|||
|VQ-BeT [18]|81.3|87.6|41.8|65.6||RIPT|
|ResNet-T [22]|84.4|88.4|51.9|54.0|40||
|QueST [22]|88.6|91.0|50.2|63.6||SFT|
|**QueST +**`RIPT`|**94.3**|**92.2**|**71.4**|**76.0**||1<br>3<br>5<br>10|
|(improvement)|**(+5.7)**|**(+1.2)**|**(+21.2)**|**(+12.4)**||Number of Demos|


Table 2: Mean Success Rate (SR%) across four evaluation settings: LIBERO-90 and ML45 (Full data), LONG and ML45 (5-shot). 

Figure 2: Few-shot curve on LIBERO-LONG. 

OpenVLA-OFT [14]. These models are typically larger than 500M parameters, pretrained (Stage-1) on large-scale general-purpose datasets, _e.g.,_ Open-X Embodiment [25], and then finetuned using 50 demonstrations per task for each LIBERO suite (Stage-2). In contrast, the **Stage 2** set includes 4 representative small models: Diffusion Policy [6], Seer [33], MDT [27] and QueST [22]. These models are within 50M parameters and are directly trained on each LIBERO suite from scratch. 

We show that `RIPT-VLA` significantly improves the best-performing VLA model in both types, setting new state-of-the-art performance on the 4 LIBERO suites. Specifically, `RIPT-VLA` improves QueST on all four task suites by **10.9** absolute SR on average, and yields even larger gains of **18.7** for the challenging LONG suite. Notably, with `RIPT-VLA` , the small 20M QueST model achieves much better performance with large models like Dita (334M) and comparable with _π_ 0 (2B). When applying to OpenVLA-OFT, the best-performing large VLA model with already high SR, `RIPT-VLA` still further reduces the average failure rate from 3.3% to 2.4%. By applying `RIPT-VLA` , we set new state-of-the-art performance on 3 out of the 4 LIBERO suites (with only a 0.2 gap on the Object suite), and achieve the highest average success rate across all tasks. These results show the `RIPT-VLA` is broadly effective: it can both unlock latent capabilities in small-scale models and further push the limits of the high-performing ones. 

In addition, in the left two columns of Table 2, we show the results on LIBERO-90 and ML45, which contain 90 and 45 diverse tasks respectively. These benchmarks assess the scalability and generalization of a single VLA model across many skills. We apply `RIPT-VLA` to QueST and compare with representative imitation learning methods: ACT [8], PRISE [39], Diffusion Policy [6], VQ-BeT [18] and ResNet-T [22]. We show that `RIPT-VLA` improves performance of QueST by **5.7** and **1.2** absolute SR for LIBERO-90 and ML45, again setting new SOTA performance for both benchmarks. This confirms the utility of `RIPT-VLA` not only for improving performance on a few related tasks, but also for scaling up to broader, more realistic scenarios where a single model solves many different tasks. 

### **5.3 Few-shot Multitask Training** 

In this section we evaluate `RIPT-VLA` under few-shot multitask setting. For each suite, we uniformly sample 1 to 10 expert demonstrations from each task to constitute the few-shot SFT dataset _D_ sft. This setting reflects practical situation where large-scale data collection is not available. 

The right two columns of Table 2 show results under the 5-shot setting, where each task in the LIBERO-LONG and ML45 suites is trained with only 5 demonstrations. While baseline models struggle in this low-data regime, `RIPT-VLA` significantly improves QueST by **21.2** on LIBEROLONG and **12.4** on ML45. These results demonstrate that `RIPT-VLA` effectively addresses a key limitation of standard VLA training with SFT: it enables strong performance even with minimal demonstrations, alleviating concerns about data scarcity in real-world multitask deployment. 

To further investigate the effect of the number of few-shot demonstrations, we conduct experiments under varying few-shot settings with QueST, ranging from 1 to 10 demonstrations per task on LIBERO-LONG. As shown in Figure 2, `RIPT-VLA` consistently largely improves the performance of the standard SFT model across all data scales. Note that even for the extremely low-data regime, where we only have 1 demonstration per task, `RIPT-VLA` can still achieve a **20.8** absolute gain. As 

9 


Figure 4: Cross-goal task generalization from Goal A to Goal B in the same scenario. 

the number of demonstrations increases, `RIPT-VLA` continues to yield performance improvements, indicating its strong sample efficiency and scalability. These results confirm that `RIPT-VLA` is robust across different levels of data scarcity and is applicable in both low- and high-data settings. 

### **5.4 Cross-scenario Generalization** 

Recent paradigm shift in LLM training demonstrates that reinforcement learning can reactivate and steer pretrained knowledge with only a small amount of interactive feedback [24]. We adopt a similar approach for VLA and ask: can `RIPT-VLA` enable sample-efficient pretrained visuomotor skill transfer across scenarios and goals? 

In this section, we experiment on the few-shot cross-scenario generalization setup. For each experiment, we consider a pair of tasks that have the same task goal (e.g., _’turn on the stove and put the frying pan on it’_ ), but operate in different scenarios: Scenario A and Scenario B - with distanct background layouts and object configurations. In Stage 1, we pretrain QueST on _|D_ pretrain _|_ = 50 demonstrations from Scenario A to acquire a general visuomotor skill for this task goal. In Stage 2, we conduct SFT on _|D_ sft _|_ = _{_ 1 _,_ 2 _,_ 3 _,_ 4 _,_ 5 _}_ demonstrations from Scenario B. Then, in Stage 3, we apply `RIPT-VLA` to optimize the policy through interactive rollouts on contexts _D_ context extracted from _D_ sft. We then evaluate the model on the 50 testing contexts of Scenario B. We conduct experiments with 3 random seeds and plot the mean and variance across different sizes of _D_ sft. 

Figure 3 show results on 5 scenario pairs. We observe that standard SFT on VLA models clearly struggles in the **1-shot** regime, achieving an average success rate of only around 5%, and in some cases dropping as low as 2%. Clearly, SFT fails to generalize the task knowledge from the pretraining stage to the new scenario. In contrast, `RIPT-VLA` dramatically improves performance, with absolute SR gain as high as **93.7%** (from 3.5% SFT to 97.2%). As the size of _D_ sft increases, both SFT and `RIPT-VLA` performance improve, but `RIPT-VLA` consistently maintains a strong improvement, often reaching near-100% performance with just 3-5 demonstrations. These results supports our core assumption: `RIPT-VLA` enables pretrained VLA models to rapidly activate and adapt learned skills with sparse binary reward feedback. 

### **5.5 Cross-goal Generalization** 

In this section, we investigate `RIPT-VLA` in a cross-goal generalization setting. Here we focus on task pairs that operate in the same scenario but with different goals. Specifically, we select Task A and Task B such that they require the same visuomotor skills but have different goals. For example, Task 

10 


Figure 5: Training curve analysis of dynamic sampling. 

|**Method**|**Goal**|**Spatial**|**Object**|**Long**|**90**|**ML45**|**Average**|
|---|---|---|---|---|---|---|---|
|QueST|80.8|87.4|93.6|68.8|88.6|91.0|85.0|
|+`RIPT-VLA`w/o Dynamic Sampling|90.6|91.3|97.5|78.3|92.2|91.3|90.2|
|**+**`RIPT-VLA`**(Ours)**|**92.7**|**95.6**|**98.4**|**87.5**|**94.3**|**92.2**|**93.5**|


Table 3: Ablation on dynamic sampling. We compare full `RIPT-VLA` against a variant without dynamic sampling and the QueST baseline across task types and multitask suites. 

A is _"put the red mug on the_ **_right_** _plate"_ while Task B is _"put the red mug on the_ **_left_** _plate"_ . This setting tests whether pretrained visuomotor primitive skills (e.g., pick up and move) can be reused and recomposed to solve novel task goals (e.g., left vs. right). We again follow the 3-Stage paradigm: pretrain QueST on 50 demonstrations of Task A, SFT on 3-10 demonstrations on Task B, and then apply `RIPT-VLA` for Task B. 

Figure 4 presents results over 5 sets of tasks. We observe that cross-goal generalization is significantly more challenging. With 3 demonstrations, SFT models still struggle and reach only **0.7%** success rate on average, almost not workable at all. With `RIPT-VLA` , we can improve model performance to **59.7%** on average. Remarkably, for one task pair, `RIPT-VLA` improves the performance from near **0%** success rate to **84.7%** . As the number of demonstrations increases, `RIPT-VLA` consistently maintains a large advantage across all data regions. At 10 demonstrations, the average success rate of `RIPT-VLA` reaches **79.7%** , compared to only **29.4%** for SFT. 

These results further show the limitation of SFT paradigm for VLA generalization under lowdata regime. In contrast, we show that `RIPT-VLA` not only helps adapt pre-trained skills to new environments, but also excels in fast generalization of task goal semantics. 

### **5.6 Aditional Study** 

**Effect of dynamic rollout sampling.** We ablate the impact of our dynamic rollout sampling strategy described in Section 4.2. We compare the full `RIPT-VLA` method with a variant that disables dynamic rejection. As shown in Table 3, dynamic sampling significantly boosts performance across all task categories and suites. By filtering out uninformative rollout groups, dynamic sampling ensures stable and efficient learning with a consistent gradient signal across batches. On average, we observe a **+3.3** absolute improvement in success rate compared to the non-dynamic variant, demonstrating its crucial role in stabilizing `RIPT-VLA` training. In Figure 5, we show the training curve (averaged over 3 seeds) of Column 2 of Figure 4. We see that dynamic rollout sampling accelerates convergence of `RIPT-VLA` , achieving consistently higher performance and more stable optimization. 

**Effect of context dataset size.** To study how the size of the context dataset _D_ **c** impacts performance, we fix the QueST model SFT-trained with only 1 demonstration for Column 2 of Figure 3 and vary the number of rollout contexts used in the `RIPT-VLA` stage. As shown in Figure 6, increasing the number of rollout contexts significantly improves performance. This is because more contexts provide greater diversity in initial states for the rollout interaction, allowing the model to better generalize across different setups in the testing environments. Notably, expanding _D_ **c** requires no additional human annotations: each context only consists of the initial observation state and no action is needed. This makes context dataset scaling a cost-effective way to enhance generalization of `RIPT-VLA` . 

11 

**Effect of context variance in RLOO group.** In Equation 5, each batch of rollouts is grouped by shared initial state contexts. In realistic deployments, however, perfectly matching initial states is impractical due to inevitable setup noise. To simulate this, we compute the standard deviation of object initial positions across LIBERO-LONG, which is around 2.5 cm. Starting with a QueST model SFT on 1 demo, we run `RIPT-VLA` while injecting Gaussian noise into the initial states with increasing scales of std. As shown in Figure 7, performance remains stable up to 1.0× (2.5 cm), and only begins to degrade beyond 2.0×. Remarkably, even at 7.0× variance (17.5 cm), `RIPT-VLA` still outperforms the SFT baseline by a significant margin. 

## **6 Conclusion** 

We presented `RIPT-VLA` , a simple yet powerful reinforcement learning paradigm for post-training pretrained Vision-Language-Action (VLA) models using sparse binary task rewards. `RIPT-VLA` enables stable and data-efficient optimization without the need for shaped rewards, value functions, or reward modeling. Our method significantly improves performance across multiple VLA benchmarks and demonstrates remarkable adaptability even in extremely low-data settings. `RIPT-VLA` serves as a scalable third-stage training paradigm that complements existing pretraining and supervised fine-tuning pipelines, unlocking the latent potential of large VLA models through direct environment interaction. An exciting future direction is to combine `RIPT-VLA` with reasoning and planning in VLA models to enable more sophisticated and generalizable behaviors in complex environments. 

## **References** 

- [1] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [2] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [3] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for real-world control at scale. In _arXiv preprint arXiv:2212.06817_ , 2022. 

- [4] Kevin Chen, Marco Cusumano-Towner, Brody Huval, Aleksei Petrenko, Jackson Hamburger, Vladlen Koltun, and Philipp Krähenbühl. Reinforcement learning for long-horizon interactive llm agents, 2025. 

- [5] Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. Conrft: A reinforced fine-tuning method for vla models via consistency policy, 2025. 

- [6] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2023. 

- [7] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multimodal language model. In _ICML_ . PMLR, 2023. 

- [8] Chen-Xiao Gao, Chenyang Wu, Mingjun Cao, Rui Kong, Zongzhang Zhang, and Yang Yu. Act: empowering decision transformer with dynamic programming via advantage conditioning. In _AAAI_ , 2024. 

12 

- [9] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- [10] Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, Yen-Jen Wang, Yucheng Hu, and Jianyu Chen. Improving vision-language-action model with online reinforcement learning, 2025. 

- [11] Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, et al. Dita: Scaling diffusion transformer for generalist vision-language-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. 

- [12] Edward J Hu, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. In _ICLR_ , 2022. 

- [13] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. Pi0.5: a visionlanguage-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [14] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. In _RSS_ , 2025. 

- [15] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In _CoRL_ , 2024. 

- [16] Wouter Kool, Herke van Hoof, and Max Welling. Attention, learn to solve routing problems! In _ICLR_ , 2019. 

- [17] Harrison Lee, Samrat Phatale, Hassan Mansoor, Kellie Ren Lu, Thomas Mesnard, Johan Ferret, Colton Bishop, Ethan Hall, Victor Carbune, and Abhinav Rastogi. Rlaif: Scaling reinforcement learning from human feedback with ai feedback. In _ICML_ , 2024. 

- [18] Seungjae Lee, Yibin Wang, Haritheja Etukuru, H Jin Kim, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. Behavior generation with latent actions. In _ICML_ , 2024. 

- [19] Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In _The Twelfth International Conference on Learning Representations_ . 

- [20] Aiwei Liu, Haoping Bai, Zhiyun Lu, Xiang Kong, Xiaoming Wang, Jiulong Shan, Meng Cao, and Lijie Wen. Direct large language model alignment through self-rewarding contrastive prompt distillation. In _ACL_ , 2024. 

- [21] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer in lifelong robot learning. In _NeurIPS_ , 2023. 

- [22] Atharva Mete, Haotian Xue, Albert Wilcox, Yongxin Chen, and Animesh Garg. Quest: Selfsupervised skill abstractions for learning continuous control. In _NeurIPS_ , 2024. 

- [23] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- [24] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. In _NeurIPS_ , 2022. 

- [25] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x- embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _ICRA_ , 2024. 

13 

- [26] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [27] Moritz Reuss, Ömer Erdinç Ya˘gmurlu, Fabian Wenzel, and Rudolf Lioutikov. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. _arXiv preprint arXiv:2407.05996_ , 2024. 

- [28] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [29] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [30] Joar Skalse, Nikolaus Howe, Dmitrii Krasheninnikov, and David Krueger. Defining and characterizing reward gaming. In _NeurIPS_ , 2022. 

- [31] Lingfeng Sun, Haichao Zhang, Wei Xu, and Masayoshi Tomizuka. Paco: Parametercompositional multi-task reinforcement learning. In _NeurIPS_ , 2022. 

- [32] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [33] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 

- [34] Chaojie Wang, Yanchen Deng, Zhiyi Lyu, Liang Zeng, Jujie He, Shuicheng Yan, and Bo An. Q*: Improving multi-step reasoning for llms with deliberative planning. _arXiv preprint arXiv:2406.14283_ , 2024. 

- [35] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. _NeurIPS_ , 2023. 

- [36] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 

- [37] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023. 

- [38] Yuexiang Zhai, Hao Bai, Zipeng Lin, Jiayi Pan, Shengbang Tong, Yifei Zhou, Alane Suhr, Saining Xie, Yann LeCun, Yi Ma, and Sergey Levine. Fine-tuning large vision-language models as decision-making agents via reinforcement learning. In _NeurIPS_ , 2024. 

- [39] Ruijie Zheng, Ching-An Cheng, Hal Daumé Iii, Furong Huang, and Andrey Kolobov. Prise: Llm-style sequence compression for learning temporal action abstractions in control. In _ICML_ , 2024. 

- [40] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _CoRL_ , 2023. 

14 

