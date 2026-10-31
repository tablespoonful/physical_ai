---
title: "Skill-Based Reinforcement Learning with Intrinsic Reward Matching"
date: "2022-10-14"
authors: "Ademi Adeniji; Amber Xie; Pieter Abbeel"
url: https://arxiv.org/abs/2210.07426
pdf: https://arxiv.org/pdf/2210.07426
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2210.07426)** / [論文ページ](https://arxiv.org/abs/2210.07426)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Skill-Based Reinforcement Learning with Intrinsic Reward Matching** 

**Ademi Adeniji**<sup>_∗_</sup> **Amber Xie**<sup>_∗_</sup> UC Berkeley UC Berkeley 

**Pieter Abbeel** UC Berkeley 

## **Abstract** 

While unsupervised skill discovery has shown promise in autonomously acquiring behavioral primitives, there is still a large methodological disconnect between task-agnostic skill pretraining and downstream, task-aware finetuning. We present Intrinsic Reward Matching (IRM), which unifies these two phases of learning via the _skill discriminator_ , a pretraining model component often discarded during finetuning. Conventional approaches finetune pretrained agents directly at the policy level, often relying on expensive environment rollouts to empirically determine the optimal skill. However, often the most concise yet complete description of a task is the reward function itself, and skill learning methods learn an _intrinsic_ reward function via the discriminator that corresponds to the skill policy. We propose to leverage the skill discriminator to _match_ the intrinsic and downstream task rewards and determine the optimal skill for an unseen task without environment samples, consequently finetuning with greater sample-efficiency. Furthermore, we generalize IRM to sequence skills for complex, long-horizon tasks and demonstrate that IRM enables us to utilize pretrained skills far more effectively than previous skill selection methods on both the Fetch tabletop and Franka Kitchen robot manipulation benchmarks. 

## **1 Introduction** 

Generalist agents must possess the ability to execute a diverse set of behaviors and flexibly adapt them to complete novel tasks. Although deep reinforcement learning has proven to be a potent tool for solving complex control and reasoning tasks such as in-hand manipulation [25] and the game of Go [30], specialist deep RL agents learn new tasks from scratch, possibly collecting new data and learning to new objectives with no prior knowledge. This presents a massive roadblock in the integration of RL in many real-time applications, such as robotic control, where collecting data and resetting robot experiments is prohibitively costly [17]. 

Recent progress in scaling multitask reinforcement learning [27, 18] has revealed the potential of multitask agents to encode vast skill repertoires, rivaling the performance of specialist agents and even generalizing to out-of-distribution tasks. Moreover, skill-based unsupervised RL [19, 22, 29] shows promise of acquiring similarly useful behaviors but without the expensive per-task supervision required for conventional multitask RL. Recent skill-based RL results suggest that unsupervised RL can distill diverse behaviors into distinguishable skill policies; however, such approaches lack a principled framework for connecting unsupervised pretraining and downstream finetuning. The current state-of-the-art leverages inefficient skill search methods at the policy level such as performing a sampling-based optimization or sweeping a coarse discretization of the skill space [20]. However, such methods still exhibit key limitations; namely they (1) rely on expensive environment trials to 

> _∗_ Equal Contribution 

> Correspondence to `ademi_adeniji@berkeley.edu` , `amberxie@berkeley.edu` Code and visualizations are available at `https://github.com/ademiadeniji/irm` 

Preprint. Under review. 


Figure 1: Intrinsic Reward Matching (IRM) Framework. IRM takes place in three stages: (1) Taskagnostic RL pretraining learns skill primitives in conjunction with a skill discriminator _qϕ_ ( _τ, z_ ), described in Section 2.1. (2) With no environment interaction, IRM minimizes the EPIC Loss between the intrinsic reward parameterized by the discriminator and the extrinsic reward, which we assume access to, with respect to the skill vector _z_ . (3) The skill policy conditioned on the optimal _z_<sup>_∗_</sup> finetunes to task reward to solve the downstream task. 

evaluate which skill is optimal, and (2) are likely to select suboptimal behaviors as the continuous skill space grows due to the curse of dimensionality. 

In this work, we present Intrinsic Reward Matching (IRM), a scalable algorithmic methodology for unifying unsupervised skill pretraining and downstream task finetuning by leveraging the learned intrinsic reward function parameterized by the skill discriminator. Centrally, we introduce a novel approach to leveraging the intrinsic reward model as a multitask reward function that, via interactionfree task inference, enables us to select the most optimal pretrained policy for the extrinsic task reward. During pretraining, unsupervised skill discovery methods learn a discriminator-parameterized, family of reward functions that correspond to a family of policies, or skills, through a shared latent code. Instead of discarding the discriminator during finetuning as is done in prior work, we observe that the discriminator is an effective task specifier for its corresponding policy that can be _matched_ with the extrinsic reward, allowing us to perform skill selection while bypassing brute force environment trials. Our approach views the extrinsic reward as a distribution with measurable proximity to a pretrained multitask reward distribution and formulates an optimization with respect to skills over a reward distance metric called EPIC [12]. 

**Contributions** The key contributions of this paper are summarized as follows: 

- We describe a unifying discriminator reward matching framework and introduce a practical algorithm for selecting skills without relying on environment samples (Section 3). 

- We evaluate IRM on a suite of robot manipulation environments, underscoring the limitations of previous approaches and showing that our method enables more efficient finetuning (Section 4.1). 

- We generalize IRM to sequence pretrained skills and solve more challenging, long-horizon manipulation tasks (Section 4.2), as well as ablate key algorithmic components. 

- We provide analysis and visualizations that yield insight into how skills are selected and further justify the generality of IRM (Section 5). 

## **2 Background** 

### **2.1 Unsupervised Skill Pretraining** 

The skill learning literature has long sought to design agents that autonomously acquire structured behaviors in new environments [33, 32, 26]. Recent work in competence-based unsupervised RL proposes generic objectives encouraging the discovery of skills representing diverse and useful behaviors [7, 29, 19]. A skill is defined as a latent code vector _z ∈Z_ that indexes the conditional policy _π_ ( _a|s, z_ ). In order to learn such a policy, this class of skill pretraining algorithms maximizes the mutual information between sampled skills and their resulting trajectories _τ_ [13, 6, 28] : 

_I_ ( _τ_ ; _z_ ) = _H_ ( _z_ ) _−H_ ( _z|τ_ ) = _H_ ( _τ_ ) _−H_ ( _τ |z_ ) (1) 

2 

Commonly, methods consider _τ_ = _s_ or _τ_ = ( _s, s_<sup>_′_</sup> ), and we leave more details in Appendix 8.2. Since the mutual information _I_ ( _s_ ; _z_ ) is intractable to calculate in practice, competence-based methods instead maximize a variational lower bound proposed in [2] which is parameterized by a learned neural network function _qϕ_ ( _τ, z_ ) called a skill discriminator. This discriminator, along with other terms independent of _z_ , parameterizes an intrinsic reward that the skill policy _π_ ( _·|s, z_ ) maximizes during pretraining. Given an unseen task specification, the agent needs to infer which skill will finetune to solve the task with the fewest samples. For more detailed explanations of the mutual information decompositions of various skill discovery algorithms, refer to Appendix 8.2. 

**Pretrained Multitask Reward Functions:** We observe that the intrinsic reward function learned during skill pretraining can be viewed as a multitask reward function, where the continuous skill code _z_ determines the task. In other words, we have some function: 


where VLB _≤ I_ ( _τ, z_ ) is the variational lower bound proposed in [2] ( _τ_ is a trajectory representation such as ( _s, s_<sup>_′_</sup> )). Since skill discovery algorithms aim to maximize _I_ ( _τ, z_ ), we can view its parameterized lower bound VLB as a multitask reward function: scoring transitions based on their alignment with a skill code [19]. 

### **2.2 Equivalent-Policy Invariant Comparison** 

We can formalize a general notion of reward function similarity by equivalent-policy invariant comparison (EPIC) as established in [12]. EPIC defines a distance metric between two reward functions such that similar reward functions induce similar optimal policies. We consider the case of action-independent reward: 

_D_ EPIC( _RA, RB_ ) = 


1 _−ρ_ <u>(</u> _X,Y_ <u>)</u> where _Dρ_ ( _X, Y_ ) = ~~�~~ 2 is the Pearson distance between two random variables _X_ and _Y_ , _sP , s_<sup>_′_</sup> _P_<sup>are samples from the Pearson distribution</sup><sup>_DP_,and</sup><sup>_SC, S_</sup> _C_<sup>_′_are batches sampled from the</sup> Canonical distribution _DC_ . We compute the Pearson distance over Pearson samples _sP , s_<sup>_′_</sup> _P_<sup>, with</sup> additional canonicalization with batches _Sc, Sc_<sup>_′_to ensure invariance over constant shifts and scaling.</sup> The canonicalized reward function is defined as: 


where _R_ : _S × S →_ R is a reward function and _γ_ is the discount factor [12]. The expectation is taken over the Canonical distribution _DC_ ; for simplicity, we sample these batches _SC_ , _SC_<sup>_′∼DC_ahead of</sup> time. The canonicalization ensures _invariance to reward shaping_ such that rewards that have different shaping but induce similar optimal policies are close in distance. In practice, the final term can be omitted as the Pearson correlation is _invariant to constant shifts and scaling_ . 

The EPIC psuedometric has typically been used for benchmarking algorithms and evaluating learned reward functions [23, 21]. To the best of our knowledge, IRM is the first to use EPIC in an optimization objective, particularly for complex tasks and larger state dimensions. 

## **3 Intrinsic Reward Matching** 

### **3.1 Task Inference via Intrinsic Reward Matching** 

A multitask reward function that can supervise the learning of diverse behaviors is useful in its own right. However, in the case of skill-based RL, we have additionally learned a corresponding _π_ ( _a|s, z_ ). Therefore, for any “task" that can be specified by our intrinsic reward function, we already have an optimal policy, so long as we condition on the corresponding skill. If we have learned a sufficiently diverse library of skills, we might expect that some of our skills share behavioral similarity to the optimal policy for the downstream task. It thus also holds that the corresponding intrinsic reward for that skill is a semantically similar task specification to the downstream task. 

3 

Given this interpretation of intrinsic reward, we posit that the task of identifying which our pretrained skills to apply to a downstream task can be reframed as inferring which task in our multitask reward function is most similar to the downstream task. Moreover, we should hope to find the skill code _z_ that produces the reward function most semantically aligned with the downstream task reward. 

With this formalism, we can formulate the task inference problem as performing the following optimization: 


in order to find _z_<sup>_∗_</sup> most aligned with the task reward. Moreover, Equation 5 performs a minimization of a novel loss we name the _EPIC loss_ with respect to the skill parameter _z_ . By EPIC’s equivalence class invariance, we know that if the EPIC loss is small for some _z_<sup>_∗_</sup> , and _π_ ( _a|s, z_<sup>_∗_</sup> ) is near optimal for _R_<sup>_int_</sup> ( _τ, z_<sup>_∗_</sup> ), then _π_ ( _a|s, z_<sup>_∗_</sup> ) approaches the optimal policy for the task as specified by _R_<sup>_ext_</sup> . Notably, we _require access to the task reward function Rext to compute the EPIC loss._ Leveraging a known task reward function is a divergence from conventional skill selection methods. 

**Computing** _R_<sup>_int_</sup> **during reward matching** During pretraining, for some methods such as [19, 29], we require negative samples in order to compute the variational objective in Equation 2 and avoid a degenerate optimization where all embedded trajectories have high similarity with all skills. However, during selection when skills are fixed, the negative sampling component amounts to a reward offset which does not impact the task semantics. Furthermore, since we may not in general have access to a large amount of negative samples on a given downstream task, we choose to simplify the objective to the following: 


where _qϕ_ is the skill discriminator. This parameterization of the intrinsic reward preserves the alignment semantics of VLB without the normalization by negative samples. For more details regarding the discriminator parameterization of the intrinsic reward for [19, 29] refer to Appendix 8.3 and Appendix 8.4. 

**Algorithm 1:** Intrinsic Reward Matching (IRM) 

**Require:** Downstream task _T_ , _DP_ , _DC_ **Require:** Pretrained policy _πθ_ ( _a|s, z_ ), intrinsic reward _r_ int( _s, s_<sup>_′_</sup> _, z_ ), and extrinsic reward _r_ ext( _s, s_<sup>_′_</sup> ) for _T_ . 

**Require:** Optimization _N_ OP = 5000 steps and finetune for _N_ FT = 100 _K_ steps. `/* Skill Selection of` _z_<sup>_∗_</sup> `via EPIC Loss */` **1 for** _NOP steps_ **do 2** Sample a batch of Pearson samples _SP , SP_<sup>_′∼DP , DP_.</sup> **3** Sample Canonical samples _SC, SC_<sup>_′∼DC, DC_.</sup> **4 for** _si, s_<sup>_′_</sup> _i_<sup>_in SP , S_</sup> _P_<sup>_′_</sup><sup>**do**</sup> **5** Calculate EPIC Loss as _D_ EPIC( _r_ int( _si, s_<sup>_′_</sup> _i_<sup>_, z_)</sup><sup>_, r_ext(</sup><sup>_si, s′_</sup> _i_<sup>)) =</sup> _Dρ_ ( _CDC_ ( _r_ int)( _si, si_<sup>_′, SC, S_</sup> _C_<sup>_′_)</sup><sup>_, CD_</sup> _C_<sup>(</sup><sup>_r_ext)(</sup><sup>_si, s_</sup> _i_<sup>_′, SC, S_</sup> _C_<sup>_′_)), as in Equation 3.</sup> 

- **6 end for** 

**7** Take optimization step on batch with respect to _z_ (gradient descent, CEM step, etc.), as in Equation 5. 

- **8 end for** 

- **9** Evaluate zero-shot performance and finetune RL agent for _N_ FT steps with _z_<sup>_∗_</sup> on downstream task _<u>T</u>_ <u>.</u> 

### **3.2 EPIC Sample-Based Approximation** 

We make a number of sample-based approximations of various unknown quantities in order to concretize the continuous optimization Equation 5 as a tractable loss minimization problem. 

**Canonical State Distribution Approximation:** In order to canonicalize our reward functions, we estimate the expectation over the state and next state distributions with a sample-based average over 1024 samples. These distributions can be entirely arbitrary, though using heavily out-of-distribution samples with respect to pretraining can weaken the accuracy of the approximation. We choose to instantiate a uniform distribution bounded by known workspace constraints for both of these distributions. 

4 

|**Task**|**IRM CEM**|**IRM GD**|**IRM Rand**|**Env Roll.**|**Env CEM**|**GS**|**Relabel**|**Rand**|
|---|---|---|---|---|---|---|---|---|
|Fetch Reach|95.9 _±_1.0|87.5 _±_0.20|92.5 _±_1.1|85.0 _±_6.2|87.8 _±_1.9|**97.3** _±_**0.0**|**0**<br>43.9 _±_0.00|16.7 _±_19|
|**Fetch Push**|**80.2** _±_**2.5**|73.1 _±_0.48|77.6 _±_2.7|74.3 _±_0.92|75.4 _±_2.6|72.1 _±_0.0|0<br>23.6 _±_0.023|<br>51.5 _±_12.5|


Table 1: IRM with various optimization methods compared to environment rollout-based skill selection, reward relabelling of pretraining data, and random skill selection. IRM based methods rival or exceed skill selection baselines that are reliant on expensive environment trials. 

**Sampling Distribution for Pearson Correlation:** We find that generating samples uniformly roughly within the environment workspace bounds, just as with the reward canonicalization, often leads to strong approximations. Furthermore, as both sample generation and relatively inexpensive function evaluation are independent of the online-finetuning phase, we can perform the full skill optimization as a self-contained preprocess to downstream policy adaptation without any environment samples. Rough knowledge of workspace bounds represents some amount of prior environment knowledge. We leave more general options such as sampling from a learned generative model over trajectories encountered during pretraining or sampling from saved pretraining data to future work. We ablate various sampling distribution choices in Table 7 and present the full algorithm in detail in Algorithm 1. 

### **3.3 Generalization to Skill Sequencing** 

Many realistic downstream tasks derive additional complexity from temporally extended planning horizons. In contrast to hierarchical reinforcement learning (HRL) approaches, which aim to stitch together pretrained skills at the policy level with a higher-level manager policy, we can extend the task matching framework of IRM to efficiently solve the problem of skill sequencing, entirely doing away with the manager policy. Consider the long-horizon setting where we have a sequence of reward functions over task horizon _H_ . Central to the finetuning problem is determining over what time intervals should potentially different pretrained skills be selected. In this work, we predetermine a fixed skill horizon _⌊H/N ⌋_ , where _N_ is the number of rewards. This skill horizon could also be specified as a parameter and learned from the task reward signal. 

Next, in order to perform skill selection over each time interval, we perform the IRM algorithm in parallel or sequentially for each reward. We note the key assumption that IRM requires access to the reward functions for each of the subtasks. For example, for a sequential goal reaching task, we divide the episode into _N_ segments for each of the _N_ goals and corresponding rewards. We perform the IRM skill selection algorithm for each reward to select the optimal skill over each interval. After selecting the skills, we freeze our selections and finetune the skill policies jointly. 

## **4 Experiments** 

In this section we aim to experimentally evaluate whether IRM improves the adaptation sampleefficiency of skill finetuning on a downstream reinforcement learning task as compared to baselines. For pretraining skills, we experiment with both the CIC [19] and DADS [29] algorithms. We consider _IRM Random_ a version of IRM that randomly samples skills and picks the one with the lowest EPIC loss, _IRM CEM_ which selects elites as those skills with the lowest EPIC loss, and _IRM Gradient Descent_ which minimizes the EPIC loss using the Adam optimizer and uses backpropagation through the discriminator to regress the optimal skill. 

|**Task**|**IRM Rand Seq**|**IRM CEM Seq**|**IRM GD Seq**|**Env Seq**|**HRL**|
|---|---|---|---|---|---|
|**Fetch Reach Seq Easy**|88.1 _±_1.5|**89.5** _±_**0.34**|86.7 _±_0.64|80.7 _±_4.7|28.4 _±_31.0|
|**Fetch Reach Seq Hard**|**73.4** _±_**2.8**|66.4 _±_1.1|**72.4** _±_3.3|62.7 _±_6.1|28.0 _±_30.6|
|**Fetch Barrier Easy**|29.3 _±_16.4|49.0 _±_22.1|**57.5** _±_**9.5**|65.5 _±_9.0|30.1 _±_20.0|
|**Fetch Barrier Hard**|43.3 _±_16.3|48.1 _±_17.8|**88.2** _±_**10.4**|65.4 _±_5.6|42.8 _±_18.2|
|Fetch Tunnel Easy|20.9 _±_14.3|40.8 _±_13.0|49.1 _±_8.4|**52.2** _±_**9.1**|32.2 _±_13.9|
|**Fetch Tunnel Hard**|25.6 _±_9.4|**58.4** _±_**1.8**|35.7 _±_1.3|14.5 _±_4.8|33.7 _±_13.9|


Table 2: Zero-shot rewards on long-horizon manipulation tasks 

**Environments** We design both a goal reaching and a tabletop pushing environment in the OpenAI Gym Fetch environment [5]. We instantiate a single-task variant in both environments as well as 

5 

|**Task**|**IRM CEM**|**IRM GD**|**Env Roll.**|**Env CEM**|**GS**|**Rand**|
|---|---|---|---|---|---|---|
|**Kettle**|**105** _±_**0.00**|96.2 _±_6.3|105 _±_0.27|105 _±_0.00|89.1 _±_0.00|18.7 _±_26.4|
|**Slide Cabinet**|**5.00** _±_**0.00**|5.00 _±_0.00|4.81 _±_0.13|5.00 _±_0.00|3.51 _±_0.00|2.00 _±_0.34|
|**Hinge Cabinet**|**175** _±_**0.00**|175 _±_0.00|175 _±_0.00|175 _±_0.00|175 _±_0.00|7.02 _±_75|
|Light Switch|182 _±_9.3|187 _±_12.9|190 _±_13.4|**208** _±_0.32|141 _±_0.00|53.7 _±_31|


Table 3: Zero-shot rewards for Franka Kitchen tasks 

#### **Intr. Rew. IRM CEM IRM GD IRM Rand Env Roll. Env CEM GS Rand** DADS **83.4** _±_ **2.19** 69.9 _±_ 2.22 77.2 _±_ 3.83 74.6 _±_ 5.15 70.3 _±_ 5.38 68.9 _±_ 2.81 28.3 _±_ 13.5 

Table 4: Zero-shot rewards for DADS skill discovery algorithm. 

extend both environments to the long-horizon sequential task setting. In the case of the block pushing environment, we introduce obstacles around which the policy must manipulate the object. For long-horizon goal reaching, we further validate across two levels of difficulty (Easy, Hard) based on the environment time limit by which the agent must solve the task. For the tabletop manipulation environment, we validate across two levels of difficulty (Easy, Hard). The Easy tasks consists of reaching two waypoints, and the Hard tasks consists of reaching three. Further task design details are provided in Appendix 8.5. 

**Baselines** We benchmark many conventional finetuning approaches after a single skill pretraining phase of Contrastive Intrinsic Control (CIC) [19]. The _Grid Search (GS)_ baseline coarsely sweeps each of 10 skills evenly from the all 0’s skill vector to the all 1’s skill vector and finetunes the skill which achieves the best evaluation reward over an episode. _Env Rollout_ randomly samples 10 skills to evaluate with a rollout and _Env Rollout CEM_ uses the episode reward as the metric by which to select elites. _Random Skill_ selects a skill at random. _Relabel_ relabels saved skill rollouts obtained during pretraining with the task reward function, and selects the skill that achieved the highest reward. All baselines use the TD3 [11] RL algorithm. 

**Evaluation** First, we pretrain each RL agent with the intrinsic rewards for 2M steps. Then, we finetune each agent to the downstream task with extrinsic rewards roughly until convergence for each task. Since our primary contribution involves skill selection, we especially focus on zero-shot episode rewards: rewards achieved by a selected skill policy but without any RL updates on the task reward. We report results averaged over 3 seeds with standard error bars. 

### **Fetch and Franka Kitchen Environments** 


Figure 2: In our Fetch Push environment, we discover skills that move the block in different directions. Downstream tasks may involve simple goals or more distant goals that require composition of multiple skills across an extended time horizon and around obstacles. In Franka Kitchen, the agent discovers skills that interact with various rigid and articulated objects in the scene, which are then leveraged to accomplish diverse tasks. 

### **4.1 Tabletop Manipulation** 

**Reach Target** We first evaluate IRM on the Reach Target task, where the Fetch robot is rewarded for reaching a target position. IRM outperforms or performs similarly to environment-rollout methods while requiring no environment samples to perform skill selection. As shown in Table 1, the random skill policy performs particularly poorly and with very high variance relative to the IRM and environment-rollout based methods. Moreover, appropriate skill selection is required for strong zero-shot performance as certain skills obtain much higher rewards than others. Reward relabelling fails to consistently select optimal skills across the benchmark, likely because its options are limited to the finite set of skills sampled during pretraining. IRM by contrast leverages continuous optimization 

6 

### **Finetuning Performance on Fetch and Franka Kitchen** 


Figure 3: The performance gap between the IRM skill selection methods and random skill selection evidences the sample efficiency gains to be had from bootstrapping a pretrained policy with task-level semantics similar to the task reward. IRM-based methods select optimal skills with no environment interaction and consequently finetune efficiently. **Top:** Fetch Reach and Block Push tasks. **Middle:** Long-horizon Fetch Reach, Fetch Barrier, and Fetch Tunnel tasks across difficulties. **Bottom:** Fetch Kitchen Manipulation Tasks 

in the infinite skill space to find the best skill for the task. Figure 3 shows the finetuning performance of the methods on the downstream task reward. 

**Push Block to Goal** Next, we evaluate IRM on a more complex manipulation task involving pushing a block to a goal position. We report the zero-shot IRM skill selection performance in Table 1 and finetuning performance in Figure 3. This more complex task similarly benefits from bootstrapping the appropriate pretrained skill policy as evidenced by the performance gap of the selection based methods over random skill selection. We remark that even for more complex manipulation tasks, IRM is robust in consistently guiding optimal skill selection without requiring any interaction with the environment. Although Env Rollout CEM is the strongest interaction baseline in terms of zero-shot reward, it far exceeds a reasonable computational budget of interactions entirely on skill selection. For illustrative purposes, we display the plot although heavily shifted. 

**Franka Kitchen Manipulation** Lastly, we evaluate IRM on 4 manipulation tasks in the Franka Kitchen benchmark [10]. We make no changes to the default environment rewards for each task, which do not include any shaping for reaching to the correct object, and thus present a harder exploration problem. We similarly observe favorable zero-shot performance of the IRM method, in the case of hinge cabinet and slide cabinet, _solving the task zero-shot without any finetuning (Table 3, Figure 3). This zero-shot adaptation behavior presents a compelling means for agents to immediately deploy optimal policies in highly sample-sensitive applications._ 

### **4.2 Extensions and Ablations** 

**Long-Horizon Manipulation** Building on the results in Section 4.1, we demonstrate that IRM fully generalizes to solving long-horizon tasks in the setting of tabletop manipulation. During the unsupervised pretraining phase, skill discovery methods can acquire useful skills such as directional block pushing or pushing the block to certain spatial locations. We show that IRM can intelligently select a sequence of such skills to finetune via reward matching, avoiding learning a hierarchical manager policy that finetunes at the policy level. 

For the Fetch Reach Sequential tasks, we consider an extended horizon where the agent is tasked with reaching a sequence of goals in a particular order. For the Fetch barrier tasks, we consider the environments such as depicted in Figure 2, where the agent must navigate around a barrier introduced during the finetuning phase in order to reach the goal. The tunnel environments consists of a goal enclosed in a tunnel; the agent must navigate around and into the tunnel to complete the task. We 

7 

**EPIC Loss and Extrinsic Reward are Negatively Correlated** 


Figure 4: (a) Scatter plot of extrinsic reward vs. EPIC loss. (b) Skill trajectories with low and high EPIC losses for planar goal-reaching. (c) Skill trajectories for sequential goal-reaching. (d) Skill trajectories for Fetch Reach. 

compare IRM methods to an environment rollout baseline (Env Seq) and a hierarchical RL baseline (HRL). The ‘IRM Seq’ methods select skills based on each defined sub-task’s reward function according to the IRM optimization scheme. ‘Env Seq’ chooses the best combination of skills based on extrinsic reward from rollouts. ‘HRL’ is initialized with random skills and simultaneously optimizes a manager policy over skills and the skill policies themselves. In both settings, IRM methods outperform the environment rollout method and in some cases the HRL method in identifying (Table 2) and finetuning skills (Figure 3). Implementation details are provided in Appendix 8.9. 

**Matching Metric Ablations** We validate the impor- **Reward Matching IRM CEM** tance of employing the EPIC pseudometric for formuIRM **21.0** _±_ **0.75** lating the matching loss by ablating its contribution L1 8.71 _±_ 0.70 against more naive selections in Table 5. L1 and L2 L2 7.87 _±_ 0.86 losses are common metrics in supervised regression L1 + Learn Scale 5.51 _±_ 1.9 problems but are poor choices for comparing task L2 + Learn Scale 3.95 _±_ 2.2 similarity with rewards. Moreover, rewards can have arbitrary differences in scaling and shaping that L1 Table 5: Reward matching metric ablation and L2 are not invariant to. To strengthen these comparisons, we include a learned reward scaling parameter for L1 and L2 and similarly observe that EPIC is a superior matching metric. 

**Skill Discovery Algorithm Ablations** IRM is fully general to any mutual information maximization based, RL pretraining algorithm as shown in Table 4. We validate on the Fetch Reach task that IRM CEM and IRM Rand convincingly outperform all episode rollout baselines in zero-shot episode reward. 

## **5 Analysis** 

**Does optimizing the EPIC loss lead to effective skill selection?** In Figure 4, we verify that EPIC loss is strongly negatively correlated with extrinsic reward on a Planar Goal Reaching task detailed in Appendix 8.8. Thus, optimizing for a low EPIC loss is an effective substitute for optimizing the environment reward, and crucially, it forgoes collecting expensive environment samples. 

**How can we understand skills through EPIC losses?** In Figure 5, we plot EPIC losses between intrinsic rewards and goal-reaching rewards across the 2D continuous skill space. Not only is the loss landscape smooth, which motivates optimization methods like gradient descent, but there is also a banded partitioning of the manifold. Furthermore, the latent skill space is well-structured as different darker-colored partitions of the skill space correspond to the group of skills with low EPIC loss from each task reward. EPIC losses concisely represent desirability of skills with respect to a downstream reward function, so skills that achieve a low EPIC loss for the Top Left goal will achieve high EPIC losses for the opposite reward, Bottom Right goal. 

We include a scatter plot and trajectory visualizations in Figure 4. As Figure 4 suggests, skills with the lowest EPIC loss receive high extrinsic reward, reaching the goal with high spatial precision. Skills with the highest losses produce the opposite behavior: moving in the direct opposite direction of the goal. In the sequential case, low-EPIC loss skills attempt to reach the 1st goal then the 2nd goal, while high-EPIC loss skills perform the behavior in the inverse order. The intrinsic reward module 

8 

provides a much deeper insight into the semantics of skills than the extrinsic rewards obtained by skill policy rollouts. 

## **6 Related Work** 

### **EPIC Loss Visualizations** 

Several works including [29, 7, 1, 14, 4, 8, 19] employ mutual information maximization for skill pretraining. While [19] leverages coarse grid search to select skills for downstream RL, methods such as [29] instead plan through a learned skill dynamics model at finetuning time. Our approach is similar in that it leverages pretraining model components other than the policy to guide skill selection. However, rather than generating a reward maximizing plan through possibly complex, learned environment dynamics, we instead look to match a policy to the task reward directly through a pretrained discriminator. 

In the context of sequential finetuning, [4, 7] employ hierarchical RL to chain pretrained skills with a manager policy requiring additional environment interactions. Works on 


Figure 5: We examine EPIC losses between extrinsic rewards and intrinsic rewards conditioned on the skill vector. We sweep across the 2D skill vector for a pretrained planar agent. 

such HRL methods include [24, 9, 35, 16] and more classic approaches like [32, 31]. By contrast, we demonstrate that the intrinsic reward matching framework can be extended to choose skill sequences without reliance on environment samples. The successor features line of work also adopts a unified view of skill-based RL. Such work relies on the assumption that arbitrary rewards can be parameterized linearly in some learned features and some task vector as in [22, 3]. Our approach relaxes this assumption to the fully general setting by instead searching for a pretrained task with minimal proximity to an arbitrarily parameterized task reward. 

## **7 Discussion** 

We present Intrinsic Reward Matching (IRM), a framework for algorithmically unifying information maximization unsupervised reinforcement learning with downstream task adaptation. We instantiate a practical algorithm for implementing this framework and demonstrate that IRM outperforms current methods on a continuous control benchmark and tabletop manipulation tasks. IRM diverges from past works in leveraging the discriminator for downstream task inference and consequently performing skill selection without environment interactions in the short horizon setting. We also show that IRM can be readily extended to the general skill sequencing setting to solve more realistic long-horizon tasks as an alternative to hierarchical methods. Central to our contribution is a novel loss function, the EPIC loss, which serves as both a skill selection utility as well as a new way to interpret the task-level semantics of pretrained skills. 

We acknowledge a number of limitations of our approach. IRM relies on samples of the state, roughly within workspace boundaries as well as access to an external reward function, ideally well-shaped, which trades off with IRM’s reduced reliance on environment interactions. In order to obtain realistic image samples to compute the EPIC loss, an agent could learn an expressive generative model over the image states obtained during pretraining and sample from the model to generate diverse and realistic sampled states. For learning unknown state-based rewards, the agent could additionally learn an image-reward model by regressing the rewards encountered during exploration [15]. This represents an exciting direction for future work. 

9 

## **References** 

- [1] Joshua Achiam, Harrison Edwards, Dario Amodei, and Pieter Abbeel. Variational option discovery algorithms. _CoRR_ , abs/1807.10299, 2018. 

- [2] David Barber and Felix V. Agakov. The im algorithm: A variational approach to information maximization. In _NIPS_ , pages 201–208, 2003. 

- [3] André Barreto, Rémi Munos, Tom Schaul, and David Silver. Successor features for transfer in reinforcement learning. _CoRR_ , abs/1606.05312, 2016. 

- [4] Kate Baumli, David Warde-Farley, Steven Hansen, and Volodymyr Mnih. Relative variational intrinsic control. _CoRR_ , abs/2012.07827, 2020. 

- [5] Greg Brockman, Vicki Cheung, Ludwig Pettersson, Jonas Schneider, John Schulman, Jie Tang, and Wojciech Zaremba. Openai gym, 2016. 

- [6] Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine. Diversity is all you need: Learning skills without a reward function, 2018. 

- [7] Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine. Diversity is all you need: Learning skills without a reward function. In _International Conference on Learning Representations_ , 2019. 

- [8] Carlos Florensa, Yan Duan, and Pieter Abbeel. Stochastic neural networks for hierarchical reinforcement learning. _CoRR_ , abs/1704.03012, 2017. 

- [9] Kevin Frans, Jonathan Ho, Xi Chen, Pieter Abbeel, and John Schulman. Meta learning shared hierarchies. _CoRR_ , abs/1710.09767, 2017. 

- [10] Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4rl: Datasets for deep data-driven reinforcement learning, 2020. 

- [11] Scott Fujimoto, Herke van Hoof, and David Meger. Addressing function approximation error in actor-critic methods. _CoRR_ , abs/1802.09477, 2018. 

- [12] Adam Gleave, Michael Dennis, Shane Legg, Stuart Russell, and Jan Leike. Quantifying differences in reward functions. _CoRR_ , abs/2006.13900, 2020. 

- [13] Karol Gregor, Danilo Jimenez Rezende, and Daan Wierstra. Variational intrinsic control, 2016. 

- [14] Karol Gregor, Danilo Jimenez Rezende, and Daan Wierstra. Variational intrinsic control. _CoRR_ , abs/1611.07507, 2016. 

- [15] Danijar Hafner, Timothy P. Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _CoRR_ , abs/1912.01603, 2019. 

- [16] Karol Hausman, Jost Tobias Springenberg, Ziyu Wang, Nicolas Heess, and Martin Riedmiller. Learning an embedding space for transferable robot skills. In _International Conference on Learning Representations_ , 2018. 

- [17] Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, Mrinal Kalakrishnan, Vincent Vanhoucke, and Sergey Levine. Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation. _CoRR_ , abs/1806.10293, 2018. 

- [18] Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. Mt-opt: Continuous multi-task robotic reinforcement learning at scale, 2021. 

- [19] Michael Laskin, Hao Liu, Xue Bin Peng, Denis Yarats, Aravind Rajeswaran, and Pieter Abbeel. Cic: Contrastive intrinsic control for unsupervised skill discovery, 2022. 

- [20] Michael Laskin, Denis Yarats, Hao Liu, Kimin Lee, Albert Zhan, Kevin Lu, Catherine Cang, Lerrel Pinto, and Pieter Abbeel. URLB: unsupervised reinforcement learning benchmark. _CoRR_ , abs/2110.15191, 2021. 

10 

- [21] Xinran Liang, Katherine Shu, Kimin Lee, and Pieter Abbeel. Reward uncertainty for exploration in preference-based reinforcement learning, 2022. 

- [22] Hao Liu and Pieter Abbeel. Aps: Active pretraining with successor features, 2021. 

- [23] Eric J. Michaud, Adam Gleave, and Stuart Russell. Understanding learned reward functions. _CoRR_ , abs/2012.05862, 2020. 

- [24] Ofir Nachum, Shixiang Gu, Honglak Lee, and Sergey Levine. Data-efficient hierarchical reinforcement learning. _CoRR_ , abs/1805.08296, 2018. 

- [25] OpenAI, Ilge Akkaya, Marcin Andrychowicz, Maciek Chociej, Mateusz Litwin, Bob McGrew, Arthur Petron, Alex Paino, Matthias Plappert, Glenn Powell, Raphael Ribas, Jonas Schneider, Nikolas Tezak, Jerry Tworek, Peter Welinder, Lilian Weng, Qiming Yuan, Wojciech Zaremba, and Lei Zhang. Solving rubik’s cube with a robot hand. _CoRR_ , abs/1910.07113, 2019. 

- [26] Marc Pickett and Andrew G Barto. Policyblocks: An algorithm for creating useful macro-actions in reinforcement learning. In _ICML_ , volume 19, pages 506–513, 2002. 

- [27] Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, Tom Eccles, Jake Bruce, Ali Razavi, Ashley Edwards, Nicolas Heess, Yutian Chen, Raia Hadsell, Oriol Vinyals, Mahyar Bordbar, and Nando de Freitas. A generalist agent, 2022. 

- [28] Archit Sharma, Shixiang Gu, Sergey Levine, Vikash Kumar, and Karol Hausman. Dynamicsaware unsupervised discovery of skills. _arXiv preprint arXiv:1907.01657_ , 2019. 

- [29] Archit Sharma, Shixiang Gu, Sergey Levine, Vikash Kumar, and Karol Hausman. Dynamicsaware unsupervised discovery of skills. In _International Conference on Learning Representations_ , 2020. 

- [30] David Silver, Aja Huang, Christopher Maddison, Arthur Guez, Laurent Sifre, George Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, Sander Dieleman, Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy Lillicrap, Madeleine Leach, Koray Kavukcuoglu, Thore Graepel, and Demis Hassabis. Mastering the game of go with deep neural networks and tree search. _Nature_ , 529:484–489, 01 2016. 

- [31] Martin Stolle and Doina Precup. Learning options in reinforcement learning. In Sven Koenig and Robert C. Holte, editors, _Abstraction, Reformulation, and Approximation_ , pages 212–223, Berlin, Heidelberg, 2002. Springer Berlin Heidelberg. 

- [32] Richard S. Sutton, Doina Precup, and Satinder Singh. Between mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning. _Artificial Intelligence_ , 112(1):181– 211, 1999. 

- [33] Sebastian Thrun and Anton Schwartz. Finding structure in reinforcement learning. In G. Tesauro, D. Touretzky, and T. Leen, editors, _Advances in Neural Information Processing Systems_ , volume 7. MIT Press, 1994. 

- [34] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding, 2019. 

- [35] Alexander Sasha Vezhnevets, Simon Osindero, Tom Schaul, Nicolas Heess, Max Jaderberg, David Silver, and Koray Kavukcuoglu. Feudal networks for hierarchical reinforcement learning. _CoRR_ , abs/1703.01161, 2017. 

11 

## **8 Appendix** 

### **8.1 Background and Notation** 

**Markov Decision Process:** The goal of reinforcement learning is to maximize cumulative reward in an uncertain environment it interacts with. The problem can be modelled as a Markov Decision Process (MDP) defined by ( _S, A, P, r, γ_ ), where _S_ is the set of states, _A_ is the set of actions, _P_ is the transition probability distribution, _r_ is the reward function and _γ_ is the discount factor. 

**Unsupervised Skill Discovery:** In competence-based unsupervised RL the aim is to learn skills that generate diverse and useful behaviors [7]. The broad aim is to learn policies that are skill-conditioned and generalizable. Formally, we also learn skills _z ∈Z_ and take actions according to _a ∼ π_ ( _·|s, z_ ). As an illustrative example, applying this formalism to the Mujoco Walker domain, we might hope to find a skill-conditioned policy and skills _z_ walk _, z_ run such that _π_ ( _·|s, z_ walk) makes the agent walk, while _π_ ( _·|s, z_ run) makes it run. Further, if we allow for continuous skills, we can also imagine being able to use the policy to “jog" at different speeds by interpolation the _z_ walk and _z_ run skills. That is, taking _z_ jog<sup>_α_=</sup><sup>_α · z_walk + (1</sup><sup>_−α_)</sup><sup>_· z_runshould, intuitively, yield a policy</sup><sup>_π_(</sup><sup>_·|s, z_</sup> jog<sup>_α_) that makes the</sup> agent jog at speed dictated by the parameter _α_ . 

**Finetuning Pretrained Skills:** With a skill-conditioned policy _π_ ( _·|s, z_ ), an agent needs to infer which skill to index for a downstream task (e.g. identifying if it needs to use _z_ walk or _z_ run) during finetuning. This is a relatively under-explored area, with the most universal approach being a coarse, discretized grid search. Least squares regression has also been investigated in the context of successor features [22]. 

### **8.2 Competence-Based Skill Discovery** 

Competence-based skill discovery algorithms aim to maximize the mutual information between trajectories and skills: 

_I_ ( _τ_ ; _z_ ) = _H_ ( _z_ ) _−H_ ( _z|τ_ ) = _H_ ( _τ_ ) _−H_ ( _τ |z_ ) (7) 

Since the mutual information _I_ ( _s_ ; _z_ ) is intractable to calculate, in practice, competence-based methods maximize a variational lower bound. Many mutual information maximization algorithms, such as Variational Intrinsic Control [13] and Diversity is All You Need [6], use the estimate _I_ ( _τ_ ; _z_ ) = _H_ ( _z_ ) _−H_ ( _z|τ_ ). Other competence-based methods, such as Dynamics-Aware Unsupervised Discovery of Skills [28], Active Pretraining with Successor Features [22], and Contrastive Intrinsic Control (CIC) [19], maximize a lower bound for _H_ ( _τ_ ) _−H_ ( _τ |z_ ). 

While the decompositions of the mutual information objective are equivalent, algorithms make different design choices regarding how to approximate entropy, represent trajectories, and embed skills. These choices affect the distillation of skills: for instance, without explicit maximization of _H_ ( _τ_ ) in the decomposition of mutual information, behavioral diversity may not be guaranteed when the state space is much larger than the skill space [19]. 

### **8.3 CIC** 

Contrastive Intrinsic Control (CIC) [19] is a state of the art algorithm for competence-based skill discovery. CIC maximizes a lower bound for _I_ ( _τ_ ; _z_ ) = _H_ ( _τ_ ) _−H_ ( _τ |z_ ) through a particle estimator for _H_ ( _τ_ ) and a contrastive loss from Contrastive Predictive Coding (CPC) [34] for _H_ ( _τ |z_ ). The lower bound for _I_ ( _τ_ ; _z_ ) is: 


where _H_ particle( _τ_ ) _∝_<sup>�</sup><sup>_n_</sup> _i_ =1<sup>log</sup><sup>_||hi−h_</sup> _i_<sup>_∗||_,</sup><sup>_h∗_</sup> _i_<sup>isthek-NearestNeighborsembedding,</sup><sup>_Nk_isthe</sup> number of k-NNs used to approximate entropy, and _N −_ 1 is the number of negative samples. 

### **8.4 DADS** 

We additionally use Dynamics-Aware Unsupervised Discovery of Skills (DADS) [29] for skill discovery, as it is one of the few skill discovery algorithms to successfully scale up to continuous skills. 

12 

DADS maximizes a lower bound for _I_ ( _τ_ ; _z_ ) = _H_ ( _τ_ ) _−H_ ( _τ |z_ ) through learning skill-conditioned transition distributions. The lower bound for _I_ ( _τ_ ; _z_ ) is: 


For our experiments, we reimplement the on-policy DADS algorithm in PyTorch. We follow the default hyperparameters and train for 20 million environment steps, per [29]. 

### **8.5 Environment Details** 

For our Fetch Reaching environment, we use the Gym Robotics Fetch environment [5]. We set the time limit to 200. For the fetch push environment, we partition the continuous action space into 4 actions, which involve pushing the block forward, backward, left, and right. We set the time limit to 10 for skill learning. 

We evaluate sequential skill selection on Fetch Reach and Fetch Push. For the Fetch Push agent, we have a Barrier and Tunnel environment, each with 3 waypoints, depicted in Figure 2. We fix a time horizon of 30 pushes per waypoint. For Fetch Barrier, the easy task consists of the first two waypoints (L shape), and the hard task consists of all three (U shape). For Fetch Tunnel, the easy task consists of the last two (into the tunnel), and the hard task consists of all three waypoints (side of the tunnel, and then into the tunnel). For Fetch Reach, we consider 2 waypoints and a time horizon of 25 for each waypoint. 

Our plane environment is a 2D world with observations in [-128, 128] x [-128, 128] and continuous actions in [-10, 10] x [-10, 10]. 

The Franka Kitchen Environment consists of a 9 dof Franka Arm in a Kitchen Environment with a variety of rigid and articulated objects. The benchmark specifies several goals with rewards for reaching those goals. The 7d action space includes the end-effector 3d translation, 3d rotation, and a gripper open/close dimension. The state includes the joint positions corresponding to each dof of the arm in addition to the joint positions of articulated bodies and 7-dimensional position and orientation information for rigid objects in the scene. The Kettle task involves moving the kettle to a target burner location on the stove. The Hinge and Slide Cabinet tasks involve opening cabinet drawers with revolute and prismatic joints respectively. The Light Switch task involves flipping the switch for the stove light. We use an episode length of 1000 for solving the tasks. 

### **8.6 Pretraining Hyperparameters** 

For the Fetch Reach environment, we use a skill dimension of 8 and a discriminator MLP hidden dimension of 64. We use an alpha value of 0 for entropy weighting. For the Fetch Push environment, we use a skill dimension of 16 and a discriminator MLP hidden dimension of 16. We use an alpha value of 0 for entropy weighting. For the Franka Kitchen environment we use an alpha value of 0.1 for entropy weighting along with a skill dimension of 2 and an MLP hidden dimension of 64. For all environments, we use a replay buffer size of 100k. 

### **8.7 Intrinsic Reward Matching and Environment Rollout Baseline hyperparameters** 

IRM CEM and Env Rollout CEM are trained for 5 iterations with 1000 samples at each iteration and 100 elites selected each iteration. Env Rollout CEM consumes the entire downstream finetuning budget on just skill selection. For illustrative purposes, we start its plot at 50k steps to show that finetuning still occurs, however, sample-inefficiency suffers due to excessive rollouts for skill selection. This problem only worsens for long time horizons. IRM Gradient Descent is trained for 5000 steps with a learning rate of 5e-3 and initialized at the skill vector of all 0.5s. IRM Random selects 100 random skills. Env Rollout trials 10 random skills for a fully episode. Grid Search coarsely trials 10 skills from the skill of all 0s to the skill of all 1s as in [20]. 

### **8.8 Planar Goal Reaching** 

The planar goal reaching task consists of a simple 2D plane with a point with a 2D Cartesian state space that can displace in the x and y coordinates with a 2D action space. Skills learned tend to span 

13 

### **Zero-Shot Performance for Planar Goal Reaching** 


Figure 6: Zero-Shot Returns for Planar Goal Reaching averaged over 5 seeds 

the 2D space reaching to diverse locations distributed broadly across the environment. We show some sample zero-shot skill selection results over three different skill dimensions in Figure 6. 

### **8.9 Sequential Skill Selection** 

For sequential skill selection, we compare IRM Sequential and Environment Sequential skill selection. IRM Sequential consists of an iterative process. The first skill is chosen entirely free of environment samples, exactly identical to the single-skill tasks. Once the first skill is chosen, we roll out a trajectory with the skills we have chosen so far and use the latter half of the trajectory as the Pearson samples for our EPIC loss. We use Gaussian noise with variance 1 for our Canonical samples as described in Appendix 8.12.2. At each step of the skill selection process, we use the corresponding IRM optimization methods. 

For our Environment Sequential skill selection method, we select skills iteratively as well. For each waypoint or subtask, we randomly sample _N_ skills and commit to the best, where _N_ = 10 _/_ n_subtasks. 

### **8.10 Hierarchical Reinforcement Learning Baseline** 

In order to validate the benefits of IRM’s offline skill selection, we compare against a baseline that leverages a conventional hierarchical RL algorithm to solve long-horizon, sequential tasks. We instantiate a TD3 manager agent that outputs into a skill action space from state input at a temporally abstract timescale. As in the IRM setup, this timescale is fixed to align with the changes in reward to encourage the manager to change its skill prediction according to the change in the reward semantics. The manager’s is then inputted to the low-level pretrained skill policy which is rolled out over many steps with the skill fixed. Both the manager policy and the low-level policy weights are updated during finetuning. The manager agent is randomly initialized such that its initial skill prediction is random. 

### **8.11 Compute** 

We thank NVIDIA for providing compute resources through the NVIDIA Academic DGX Grant. We used a cluster of 8 NVIDIA A100s for experimentation. 

### **8.12 Additional Ablations** 

### **8.12.1 Skill Dimension** 

We ablate skill dimension and evaluate the zero-shot performance of all skill selection methods. IRM’s performance generally increases with increased skill dimension despite discriminator overfitting issues associated with larger skill spaces. The IRM GD learning rate is chosen as 5e-3 for all experiments in this work and is not tuned at all. Such likely explains the divergence of the 64 dimensional result. 

14 

|**Skill Dim**|**IRM CEM**|**IRM GD**|**IRM Rand**|**Env Roll.**|**Env CEM**|**GS**|**Rand**|
|---|---|---|---|---|---|---|---|
|8|21.1 _±_0.51|15.7 _±_1.61|18.9 _±_0.18|18.4 _±_0.18|18.8 _±_0.48|17.9 _±_0.101|13.5 _±_1.85|
|16|17.4 _±_1.30|14.6 _±_0.63|18.8 _±_0.26|22.7 _±_0.83|23.1 _±_0.36|14.0 _±_0.19|11.2 _±_2.32|
|32|20.1 _±_0.54|22.537 _±_0.25|19.8 _±_0.14|22.2 _±_0.58|21.5 _±_0.67|24.0 _±_0.12|19.9 _±_0.67|
|64|21.9 _±_0.48|1.68 _±_0.069|20.9 _±_0.74|22.5 _±_0.70|21.6 _±_0.89|18.2 _±_0.059|13.3 _±_2.15|


Table 6: IRM methods and environment rollout methods ablated over multiple skill dimensions on Fetch Push 

### **8.12.2 Pearson & Canonical Distributions** 

We experiment with many ways to approximate the Pearson and Canonical distributions. We defined Full Random to be our uniform samples from a reasonable estimate of the upper and lower bounds for each dimension of the state. For our planar environment, the bounds are defined explicitly and thus known; for more complex environments, we estimate the bounds. For example, for a tabletop manipulation workspace, we sample 2-dimensional block positions uniformly within the rectangular plane of the table surface. In practice, IRM is fairly robust to the distributions, though there are subtleties that emerge in the various choices for the Pearson and Canonical distributions. For instance, we also ablate a Uniform(0,1) distribution, which generally performs much worse, due to lack of state coverage for most environments. For the Canonical distribution, we also approximate samples by perturbing the Pearson samples by _ϵ_ sampled from a Gaussian distribution. We experiment with hyperparameters of variance, which may be adjusted based on the environment. For our sequential IRM method, we use this Canonical distribution to ablate on-policy samples. 

|**Pearson Distribution**<br>**Canonical Distribution**|**IRM CEM**|
|---|---|
|Full Random<br>Full Random|20.341 _±_0.306|
|Full Random<br>Uniform(0,1)|16.343 _±_0.708|
|Full Random<br>_ϵ ∼N_(0_,_1)|21.191 _±_0.629|
|Full Random<br>_ϵ ∼N_(0_,_0_._1)|21.027 _±_0.419|
|Uniform(0,1)<br>_ϵ ∼N_(0_,_1)|5.905 _±_3.157|
|Uniform(0,1)<br>_ϵ ∼N_(0_,_0_._1)|2.851 _±_0.605|
|Table 7: EPIC Loss Sampling Distribution A|blations.|


None of the distributions ablated above require on-policy environment samples. It _is_ possible to use on-policy samples for the state distributions, and we choose to do so for our sequential IRM method, as previous skill rollouts may provide useful Pearson samples for the subsequent skill selection. Note that while on-policy Canonical samples are possible, they are incredibly expensive and require access to the environment simulator, so we focus on other choices of distributions. 

### **8.12.3 Sparse Reward Ablation** 

We ablate our planar EPIC Loss visualizations with sparse rewards. Instead of a well-shaped goalreaching reward, we use sparse rewards based on the tolerance to the goal. We define the tolerance as the radius the agent must be within if our 2d planar environment is scaled to [0, 1] x [0, 1]. With a very sparse reward, we show that EPIC losses are largely uninformative. However, by slightly relaxing the tolerance, we show a much better shaped EPIC loss landscape that bears similarity to that of Figure 5. Thus, while our method is dependent on access to extrinsic rewards, and ideally, shaped rewards, we show that the EPIC loss landscape over sparse reward landscapes with sufficient tolerance can be optimized. 

15 

**EPIC Loss Visualizations** 


Figure 7: We examine EPIC losses between extrinsic rewards and intrinsic rewards conditioned on the skill vector. We sweep across the 2D skill vector for a pretrained planar agent. Left: Sparse goal-reaching reward with tolerance of 0.03. Right: Sparse goal-reaching reward with tolerance of of 0.07. 

16 

