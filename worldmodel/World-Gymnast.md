---
title: "World-Gymnast: Training Robots with Reinforcement Learning in a World Model"
date: "2026-02-02"
authors: "Ansh Kumar Sharma; Yixiang Sun; Ninghao Lu; Yunzhe Zhang; Jiarao Liu; Sherry Yang"
url: https://arxiv.org/abs/2602.02454
pdf: https://arxiv.org/pdf/2602.02454
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.02454)** / [論文ページ](https://arxiv.org/abs/2602.02454)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

**Ansh Kumar Sharma**<sup>1</sup> **Yixiang Sun**<sup>1</sup> **Ninghao Lu**<sup>2</sup> **Yunzhe Zhang**<sup>1</sup> **Jiarao Liu**<sup>3</sup> **Sherry Yang**<sup>1</sup> 

world-gymnast.github.io 

## **Abstract** 

## **1. Introduction** 

Robot learning from interacting with the physical world is fundamentally bottlenecked by the cost of physical interaction. The two alternatives, supervised finetuning (SFT) from expert demonstrations and reinforcement learning (RL) in a software-based simulator, are limited by the amount of expert data available and the sim-toreal gap for manipulation. With the recent emergence of world models learned from real-world video-action data, we ask the question of whether training a policy in a world model can be more effective than supervised learning or software simulation in achieving better real-robot performance. We propose World-Gymnast, which performs RL finetuning of a vision-language-action (VLA) policy by rolling out the policy in an actionconditioned video world model and rewarding the rollouts with a vision-language model (VLM). On the Bridge robot setup, World-Gymnast outperforms SFT by as much as 18x and outperforms software simulator by as much as 2x. More importantly, World-Gymnast demonstrates intriguing capabilities of RL with a world model, including training on diverse language instructions and novel scenes from the world model, test-time training in a novel scene, and online iterative world model and policy improvement. Our results suggest learning a world model and training robot policies in the cloud could be the key to bridging the gap between robots that work in demonstrations and robots that can work in anyone’s household. 

> 1New York University 2NYU Shanghai 3University of California, Berkeley. Correspondence to: Ansh Kumar Sharma _<_ as20482@nyu.edu _>_ , Sherry Yang _<_ sherryyang@nyu.edu _>_ . 

Robots that learn by trial and error in the real world face an inherent constraint: physical interaction is expensive (Kormushev et al., 2013). Every policy update that depends on executing actions on hardware consumes operator time, risks wear-and-tear, and compounds safety concerns (Brunke et al., 2022), especially for manipulation, where failures are frequent early in learning. This cost creates a fundamental bottleneck for scaling robot learning from interaction. As a result, many real-robot systems rely on alternatives that reduce or replace on-robot exploration (Matas et al., 2018; Schaal, 1999). 

One alternative is supervised learning (SFT) from expert demonstrations, where a robot is trained to imitate trajectories collected by teleoperation or scripted controllers (Ross et al., 2011). However, demonstration data tend to cover only a narrow slice of the long tail situations (Hu et al., 2024), and rarely expose the robot to the kinds of compounding errors and recovery behaviors needed for robust deployment (Lu et al., 2022). The second alternative is reinforcement learning (RL) in a software-based simulator (Zhao et al., 2020). However, software simulators are costly to create for every new scenarios. Furthermore, they often suffer from the sim-to-real gap where visual features differ from real-world images (Salvato et al., 2021). 

Recent work have shown that world models learned from real-robot data can approximate real-robot execution outcomes (Yang et al., 2023; Quevedo et al., 2025; Guo et al., 2025; Tseng et al., 2025; Li et al., 2025b). These models aim to predict how the visual world evolves under the robot’s actions, effectively serving as an action-conditioned video simulator learned from real-world data. Compared to software simulators, video-based world models hold the promise of closing the visual gap and generalizing to a novel initial frame. However, it is unclear whether video world model offers more realistic physics than traditional simulators due to hallucinations (Yang et al., 2024). While evaluating physical realism is difficult, we instead tackle the end-to-end problem: does training robot policies inside a learned world model result in better real-robot performance 

_Preprint. February 3, 2026._ 

1 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

### than SFT or RL in a traditional simulator? 

In this paper, we explore this question through the lens of large vision-language-action (VLA) policies that map images and language instructions to robot actions (Brohan et al., 2022; Kim et al., 2024; Black et al.). Specifically, we propose World-Gymnast, a training framework that performs RL fine-tuning a VLA policy using a world model (Figure 1). Concretely, World-Gymnast uses the actionconditioned video generation model similar to Quevedo et al. (2025) as its world model, enabling the policy to generate imagined rollouts conditioned on action sequences sampled from the VLA and uses a vision-language model (VLM) to compute rewards from predicted video frames. The resulting rewards are used to perform policy gradient updates to the VLA policy. More importantly, World-Gymnast opens up many intriguing possibilities of RL training with a world model, including (i) RL training from an arbitrary image frame, (ii) test-time training on a novel initial frame, and (iii) online iterative world model and policy improvement. 

We evaluate World-Gymnast on the Bridge robot platform through AutoEval (Zhou et al., 2025), an automated realrobot evaluation platform open to public. Across a suite of manipulation tasks from AutoEval, we show WorldGymnast substantially outperforms SFT using the original Bridge data (Walke et al., 2023) and RL in SIMPLER (Li et al., 2024), a software simulator for Bridge created through real-to-sim techniques. Furthermore, since the world model only requires a single initial frame to perform rollouts, we demonstrate intriguing usage of the world model including training on novel language instructions and initial frames injected with distractor objects, test-time training from a real-robot frame, and iterative world model and policy improvement, all of which positively contribute to improved real-robot performance. 

## **2. Preliminaries** 

In this section, we define notations and review model-based RL. We then discuss how foundation world models and vision language models can serve as general dynamics and reward models under the model-based RL formulation. 

**Markov Decision Process.** We consider a multi-task, finite-horizon, partially observable Markov Decision Process (POMDP) (Puterman, 2014; Kaelbling et al., 1995), specified by _M_ = ( _S, A, O, G, R, T, E, H_ ), which consists of state, action, observation, and task spaces, reward, transition, and emission functions, and horizon length. A policy _π_ interacts with the environment for a task starting from an initial state _g, s_ 0 _∼ G, o_ 0 _∼E_ ( _s_ 0), producing a distribution _π_ ( _·|ot, g_ ) over _A_ from which an action _at_ is sampled and applied to the environment at each step _t ∈_ [0 _, H_ ]. The environment produces a scalar reward _rt_ = _R_ ( _st, g_ ), and 

transitions to a new state _st_ +1 _∼ T_ ( _st, at_ ) and emits a new observation _ot_ +1 _∼E_ ( _st_ +1). 

The value of a policy _π_ can be defined as the total expected future reward: 


**Model-Based RL with Foundation Models.** RL (Sutton et al., 1998) aims to maximize _ρ_ ( _π_ ) through trial-anderror interactions between the policy and the environment. Model-based RL (Doya et al., 2002) considers the setting where _T_ and _R_ are unknown and need to be estimated from samples from the environment, which can be an offline dataset logged from previous interactions _D_ = _{τi_ = _g, s_ 0 _, o_ 0 _, a_ 0 _, ..., sH , oH , rH }_ . Motivated by characteristics of a real-world system such as image based observations and high control frequencies, the learned model _T_<sup>ˆ</sup> ( _·|_ **o** _,_ **a** ) can often take a sequence of previous image observations and a sequence of next actions. After _T_<sup>ˆ</sup> and _R_<sup>ˆ</sup> are estimated from data, a policy can perform rollout in the learned model 


Recent work has shown that _T_<sup>ˆ</sup> can be parametrized using an action-conditioned video generation model (world model) while _R_<sup>ˆ</sup> can be parametrized using a vision-language model (VLM). 

Policy gradient methods (Williams, 1992) estimates the gradient of Equation 2 with respect to the policy _π_ , and maximizes _ρ_ ( _π_ ) directly via gradient ascent. The most commonly used gradient estimator has the form 


where _A_<sup>ˆ</sup> is some advantage function that can be separately estimated via Monte-Carlo returns from _π, T, R_ (Williams, 1992). With model-based policy gradient, these advantages can be estimated from Monte-Carlo samples from _π, T,_<sup>ˆ</sup> _R_<sup>ˆ</sup> . 

## **3. RL with a World Model** 

In this section, we describe the RL algorithm WorldGymnast uses in Section 3.1. We then describe emerging training scenarios such as training on out-of-distribution (OOD) language and image in Section 3.2 and test-time training in Section 3.3. Lastly, we explain how WorldGymnast can be combined with classical algorithm such as Dyna (Sutton, 1991) to do online iterative world model and policy improvements. 

2 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 


_Figure 1._ **Overview of World-Gymnast.** The policy is trained on tasks specified by an initial frame and language instruction. During training, the policy outputs actions which are then passed to the world model (WorldGym (Quevedo et al., 2025)) which generates imagined rollouts. These rollouts are then passed to a VLM which returns a binary task completion reward. This reward is used to update the policy. Once trained, we evaluate the policy on real robots using the AutoEval (Zhou et al., 2025) setup. The resulting real world rollouts (frame-action sequences) from AutoEval can be further used to improve the world model on the particular environment. 

### **3.1. Model-Based GRPO with World Model Rollouts** 

To optimize the policy _πθ_ from Equation (3), WorldGymnast uses the learned world model _T_<sup>ˆ</sup> from Quevedo et al. (2025). We adopt Group Relative Policy Optimization (GRPO) (Shao et al., 2024), a policy gradient algorithm that estimates _A_<sup>ˆ</sup> using group-based score normalization. 

For a given task instruction _g_ and an initial observation _o_ 0, we generate a group of _K_ independent trajectories _{τ_ 1 _, . . . , τK}_ by rolling out the policy _πθ_ in the world model _T_ ˆ. Specifically, for the _k_ -th trajectory, the policy samples an action _at,k ∼ πθ_ ( _·|ot,k, g_ ), and the world model predicts the next observation _ot_ +1 _,k ∼ T_<sup>ˆ</sup> ( _ot,k, at,k_ ). This process repeats until the horizon _H_ is reached, yielding a trajectory _τk_ = ( _o_ 0 _,k, a_ 0 _,k, . . . , oH,k_ ). Once the rollouts are complete, we employ a VLM _R_<sup>ˆ</sup> to assign a binary task completion reward to each trajectory _rk_ = _R_<sup>ˆ</sup> ( _τk, g_ ). To compute the advantages, we treat the group of _K_ outputs as a baseline. We compute the mean and standard deviation of the rewards within the group: 


The advantage for the _k_ -th trajectory is then calculated via normalization: 


where _ϵ_ is a small constant for numerical stability. We assign the trajectory-level advantage to every time step _t_ within that trajectory. That is, _A_<sup>ˆ</sup> _t,k_ = _A_<sup>ˆ</sup> _k_ for all _t ∈_ [0 _, H −_ 1]. Finally, we optimize the policy _πθ_ using a PPO-style objective clipped based on the computed advantages. The 

loss function is defined as: 


where _rt,k_ ( _θ_ ) = _πθoldπθ_ <u>(</u> _a_ ( _ta,t,kk|o|to,t,kk,g,g_ <u>)</u> )<sup>denotestheprobability</sup> ratio. 

Following the successful training setup of VLA training using RL in Li et al. (2025a), we employ some of their techniques: 1) discarding the KL penalty term, 2) dynamic sampling to filter out groups with no variance in reward, 3) clipping higher in GRPO, and 4) using a higher temperature to sample actions during rollouts. These tricks helped stabilize training and improved exploration during training. 

### **3.2. Diverse Training Scenarios in the World Model** 

A world model pretrained on diverse datasets allows us to generate diverse training configurations (e.g., tasks and initial observations) using only images and langauge instructions. This provides greater flexibility than setting up software based simulations for each new configuration.We now explore an array of possibilities in training a policy in diverse configurations enabled by World-Gymnast. 

**Training from Any Frame.** We can train the policy with RL using any frames that are close enough to the world model’s training distribution as the initial observation _o_ 0, then rolling out the policy _π_ , the world model _T_<sup>ˆ</sup> , and the reward model _R_<sup>ˆ</sup> to provide learning signals on this initial configuration. This flexibility substantially increases the 

3 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

effective amount of training data available for RL in contrast to SFT which is bottlenecked by the amount of expert demonstrations. RL training from any frame also enables the policy to learn recovery behaviors, thereby improving the robustness of policies. 

**Training on Novel Language Instructions.** The training data can be further scaled by modifying the language instructions associated with the same initial frame. For instance, we can give a VLM an initial frame and ask for reasonable tasks for a robot to perform from that initial frame. We then give these reasonable tasks as language instructions to the VLA policy to evaluate the policy’s performance on OOD language tasks and to further improve the policy on the OOD language tasks through RL. This enables the policy to be trained on new tasks and interact with objects previously present in the environment but not explicitly interacted with. Previous work in policy evaluation had shown that pretrained VLA policies often fail at following OOD langauge instructions (Quevedo et al., 2025). We can overcome these limitations of VLAs with RL post-training in a world model. 

**Training with Distractions.** To improve policy’s robustness to irrelevant visual clutter, we leverage image editing tools like Nano Banana (Google, 2025) to synthesize additional objects as distractors in the input image frames. Training the policy on diverse distractor objects encourages the policy to be more robust when such distractor objects are present during actual deployment and to have better performance in cluttered scenes. This can bridge the gap between robots that work in demos and robots that can work in anyone’s messy household. 

### **3.3. Test-Time Training from a Novel Frame** 

Because World-Gymnast allows a policy to rollout from just an initial frame, when a novel frame is presented to a policy at test time, the policy can trade-off compute for improved policy performance by running RL training in the world model starting from the test frame. This allows rapid adaptation of the policy to novel scenes while avoiding the cost and risk of collecting real-world interaction data. 

### **3.4. Iterative World Model and Policy Improvement** 

When the visual observations encountered during policy rollouts deviate too much from the original training distribution of the world model, directly rolling out the policy in the world model might lead to compounding modeling errors. Inspired by classical Dyna-style algorithms (Sutton, 1991), World-Gymnast allows an iterative training procedure in which the policy and world model are alternately refined. Specifically, the current policy can be rolled out (with inference-time scaling or test-time training using the 

world model as a reward function) to collect new environment interactions, which are then incorporated to further fine-tune the world model. The updated world model is subsequently used to generate improved imagined rollouts for policy optimization. This data flywheel enables the world model to progressively adapt to the policy-induced state distribution, while allowing the policy to benefit from increasingly accurate long-horizon predictions from the world model. 

## **4. Experiments** 

We now evaluate the performance of policies trained in World-Gymnast. We explain the experimental setup in Section 4.1, followed by comparisons to policies trained with software simulators and SFT in Section 4.2. We then demonstrate the capabilities of World-Gymnast in supporting diverse training from images with distractors, novel language instructions, and scaling the number of RL tasks in Section 4.3. Finally, we evaluate test-time scaling and iterative policy and world model improvement in Section 4.4 and Section 4.5. 

### **4.1. Experimental Setup** 

**Tasks and Pipeline.** We evaluate the efficacy of WorldGymnast using the curated evaluation dataset used in Kim et al. (2024). The dataset follows the BridgeData V2 (Walke et al., 2023) setup with the WidowX robot and is designed to test policy generalization across visual, motion, physical, and semantic variations, as well as language grounding, over 17 tasks (Appendix C). 

We further leverage the data scaling capabilities enabled by World-Gymnast, such as image editing, language augmentation, and novel task setups, to improve generalization of the trained RL policy. To train with World-Gymnast, a task just requires an initial frame and language instruction. During training, World-Gymnast rolls out the policy for up to 40 steps in WorldGym and a binary task completion reward is assigned to the rollout by GPT-4o (Hurst et al., 2024). 

Once training is complete, we evaluate the performance of the policy on WorldGym (Quevedo et al., 2025) to estimate real robot performance and ensure policy is safe for testing, following its default configuration unless otherwise specified (Appendix A.4). We finally run the policy on AutoEval (Zhou et al., 2025), a real-robot evaluation framework that currently supports 4 tasks across 2 setups. AutoEval evaluates each policy–task pair over 10 trials; we repeat this evaluation 5 times to estimate the standard error. 

**Base Models.** Successful RL finetuning requires a reasonably competent initial policy. To this end, we use OpenVLAOFT (Kim et al., 2025) as our base model. OpenVLA-OFT 

4 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

_Table 1._ **Real-robot success rate from AutoEval** (Zhou et al., 2025) of World-Gymnast compared to running RL in a software simulator SIMPLER (Li et al., 2024). RL with a world model significantly outperforms RL in a simulator in terms of real-robot success for 3 out of the 4 tasks. 

|Task|SIMPLER|World-Gymnast|
|---|---|---|
|Open the drawer|34_±_7%|58_±_4%|
|Close the drawer|74_±_5%|62_±_6%|
|Put the eggplant into|32_±_10%|72_±_10%|
|the blue sink|||
|Put the eggplant into|40_±_10%|78_±_2%|
|the yellow basket|||


provides an optimized finetuning recipe to build on top of OpenVLA (Kim et al., 2024) which was originally trained on Open X-Embodiment dataset (Vuong et al., 2023). We use the BridgeData V2 (Walke et al., 2023) to finetune our base model. Following the idea from (Li et al., 2025a), we made several modifications to the official implementation of OpenVLA-OFT: 1) Disable the proprioception and secondary camera inputs to match the observation space used by our policy, 2) Use LLAMA-2 (Touvron et al., 2023) LM head as action head instead of the default L1 loss one to get action probabilities essential for RL. For WorldGym, we used a 600M parameter variant pretrained on Open X- Embodiment dataset. 

**Training Details.** For RL training, we use 4 NVIDIA H200 GPUs (140GB each) for full-parameter finetuning over 1–2 days. We use the following training parameters: learning rate 5 _·_ 10<sup>_−_6</sup> , group size 8, size of training batch 20, length of action chunk 5, clip ratio ( _ϵhigh_ = 0 _._ 28, _ϵlow_ = 0 _._ 2), temperature 1 _._ 6. More detailed hyperparameter setup is available in Appendix A.4. 

### **4.2. Evaluating RL with World-Gymnast** 

**Comparing World-Gymnast to a Software Simulator.** We compare World-Gymnast against traditional simulatorbased RL. We select SIMPLER (Li et al., 2024), a real-tosim policy evaluation framework, as our baseline since it provides the closest simulator-based approximation to the Bridge robot and tasks used in our evaluation. We train on all available tasks in SIMPLER (Appendix B.2) and further include digital twins for the AutoEval setup. When initializing RL from the base SFT policy, we observed low task completion rate in SIMPLER for all tasks except _close the drawer_ , although the policy often moved in the correct direction but failed to fully complete the task. As a result, using a binary completion reward led to collapsed reward variance, preventing effective policy updates. To overcome this problem, we define the reward for a rollout as the sum of partial rewards from each step. We share more details of reward design in Appendix B.2. 

_Table 2._ **Real-robot task success rate** of World-Gymnast and supervised learning approaches. Standard errors are calculated between groups of 10 consecutive roll-outs. 

|Task|SFT|Iter-SFT|World-Gymnast|
|---|---|---|---|
|Open the drawer|40_±_10 %|30_±_10 %|58_±_4 %|
|Close the drawer|62_±_6 %|60_±_8 %|62_±_6 %|
|Put the eggplant into|4_±_4 %|10_±_3 %|72_±_10 %|
|the blue sink||||
|Put the eggplant into|8_±_4 %|17_±_17 %|78_±_2 %|
|the yellow basket||||


World-Gymnast outperformed training with SIMPLER on all tasks except _close the drawer_ , as shown in Table 1. For _close the drawer_ task, the base policy has already performed pretty well prior to RL. It is worth noting that the RL training set for World-Gymnast does not include these tasks in the training set, whereas the SIMPLER baseline was also trained on these exact environment-task setups (the digital twins) and yet the policy exhibited poor transfer to real world. 

**Comparing World-Gymnast to Supervised Learning.** We also compare World-Gymnast with supervised finetuning methods. Following the recipe of OpenVLA-OFT (Kim et al., 2025), we fine-tune a OpenVLA 7B policy (Kim et al., 2024) on expert trajectories from the Bridge V2 dataset (Walke et al., 2023) for 20k steps. This policy, denoted as _SFT_ in Table 2, is also the base model on which we conduct RL training. Recent works like Ctrl-World (Guo et al., 2025) further utilize the world model for policy improvement by generating synthesized roll-outs filtered by a reward model as additional supervision. Similar to CtrlWorld, we roll out the base _SFT_ policy in our world model for the same amount of steps as World-Gymnast did for RL training, and filtered for successful trajectories on OpenVLA evaluation tasks using a VLM. We then conduct another iteration of supervised fine-tuning with a mixture of data from Bridge V2 plus the successful synthesized roll-outs with a 1 : 1 sampling rate. The resulting policy, denoted _Iter-SFT_ in Table 2, is then evaluated on real world held-out tasks through AutoEval. 

As shown in Table 2, World-Gymnast achieves the best performance compared with supervised learning and IterSFT, with a 18-fold and nearly 10-fold improvements from the base policy on _Put the eggplant into the blue sink_ and _Put the eggplant into the yellow basket_ , respectively. Notably, Iter-SFT improves slightly on the harder tasks, but the performance degrades on the easier ones. One possible explanation is that RL, through active exploration and on-policy updates, learns more generalizable behaviors. In contrast, iterative SFT may overfit to synthetic experience and is more vulnerable to world model hallucinations and inaccurate VLM success judgments. 

5 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 


_Figure 2._ **Qualitative evaluation of policy rollouts in WorldGym with distractors.** We compare rollout quality among SFT, WorldGymnast and World-Gymnast-Distract under visual distractions. The task on the left is _put blue cup on plate_ and the SFT policy clearly picks up the wrong cup, while both World-Gymnast variants are able to correctly execute the task. On the right task ( _put carrot on plate_ ), we can see SFT struggle again and seems to grab the dinosaur along with the carrot. Both World-Gymnast variants are again successful but World-Gymnast-Distract has better grasping and placing movements. It is worth noting that even with the visual artifacts introduced by the imperfect world model, the policies transfer effectively to the real robot setting. 

### **4.3. Evaluating Diverse Settings World-Gymnast Offers** 

**Evaluating Training with Distractors.** We use Nano Banana (Google, 2025) to generate a new dataset using the pre-existing frames from the OpenVLA Bridge task suite. The new dataset adds random objects to distract the policy from successfully achieving the given task. We then train a new policy with RL (World-Gymnast-Distract) by including these new frames in the training data. Next, we evaluate the performance of SFT, World-Gymnast and WorldGymnast-Distract on a held-out set of distractor frames. WorldGym evaluations show World-Gymnast-Distract is the most robust, while SFT is the easiest to distract (Figure 2). Additionally, we evaluate World-Gymnast-Distract on the original OpenVLA tasks in WorldGym and observe improved success rates (Table 3). This indicates that adding distractor-augmented data improves performance not only under visual perturbations but also on the original tasks. Qualitative rollout comparisons in Figure 2 further illustrate that under visual distractions, World-Gymnast-Distract executes more reliable grasping and placement behaviors than SFT and World-Gymnast, while maintaining correct object grounding despite visual artifacts from the world model. 

**Evaluating Training with Novel Language Instructions.** Another approach to scaling data is augmenting language instructions in pre-existing tasks. We test this approach by creating 4 new tasks involving new interactions with objects already present in the scene. We combine this new data with the OpenVLA dataset and train a new policy, WorldGymnast-Language. Next we evaluate the performance of World-Gymnast-Language on the held-out split from OpenVLA data and observe that World-Gymnast-Language has improved performance over World-Gymnast (Table 3). 

_Table 3._ **Comparing RL on diverse settings.** Leveraging the diverse capabilities of world modeling, World-Gymnast allows significant improvement in the task success rates for multiple settings. 

|Variant|Success Rate|
|---|---|
|SFT|58_±_4 %|
|World-Gymnast|74_±_3 %|
|World-Gymnast-Distract|78_±_2 %|
|World-Gymnast-Language|81_±_1 %|
|World-Gymnast-Scaled|81_±_4 %|


This suggests that creating more tasks by introducing novel language instructions on existing frames can further improve the generalization performance of VLA policies. 

**Scaling the Number of Training Tasks.** One advantage of World-Gymnast is its ability to train on a diverse set of tasks starting from any initial frame. To scale up data, we randomly selected 5 additional tasks from the Bridge dataset (Walke et al., 2023). We then train on these tasks in addition to the OpenVLA tasks and call this variant World-GymnastScaled. We evaluate the performance of World-GymnastScaled in WorldGym on the OpenVLA held-out task split and observed improvement compared to World-Gymnast, as shown in Table 3. These results suggest that World-Gymnast can effectively leverage additional training tasks to improve performance. 

### **4.4. Evaluating Test-Time Optimization** 

Pretrained policies often struggle at generalizing well to novel real world scenarios. While online data collection followed by finetuning can address this gap, it is prohibitively expensive in terms of time and effort. With a pretrained 

6 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 


_Figure 3._ **Qualitative comparison** of rolling out the same action sequence on the real robot from AutoEval (Zhou et al., 2025), from software simulator SIMPLER (Li et al., 2024), from WorldGym (Quevedo et al., 2025), and from World-Gymnast with online world model updates. Rollouts from World-Gymnast adheres more closely to the real world than SIMPLER, suggesting improving the world model through Dyna (Sutton, 1991) improves the quality of the rollout. 

world model, we show that World-Gymnast improves the performance of a base policy through test-time training without real world roll-outs. Specifically, provided only with the initial observation and the task instructions of the 4 scenarios from AutoEval (Zhou et al., 2025), we fine-tune our base policy with RL (details in Appendix A.4) using imagined roll-outs generated by the world model in a zero-shot manner from the testing frame. Test time training significantly improves the performance and robustness of _close the drawer_ in the real world, improving the success rate from 62 _±_ 6% success rate to 100 _±_ 0% for the _Close the drawer_ task. However, we noted that test-time training overfits the model to this single task, and performance in other tasks generally degrade. Test-time training across diverse tasks is an interesting venue of future work. 

### **4.5. Evaluating Iterative World and Policy Improvement** 

A unique advantage of World-Gymnast is that the world model can be iteratively updated with real world roll-outs for initial frames that are out-of-distribution of the pretrained world model. During policy evaluation with AutoEval (Zhou et al., 2025), we save the task instructions, observations, and action sequences to improve our world model. Iteratively, we collected around 100 trajectories per task for all 4 tasks, on which we finetune the world model for a total of 120k steps. Figure 3 provides a qualitative result demonstrating 

the improvement of the world model in playing a sequence of actions for _Open the drawer_ task, which shows much less sim-to-real gap than SIMPLER (Li et al., 2024) and than WorldGym without online updates. Using the Dyna style world model updated with online data as an RL environment, World-Gymnast improves the success rate of the base RL model for _close the drawer_ in AutoEval to 95%. 

## **5. Related Work** 

**Model-Based Reinforcement Learning.** Model-based RL has long been studied in the RL literature, which learns a dynamics model from previously collected data and rolling out the learned dynamics model for policy evaluation and improvement (Sutton, 1991; Tani, 1996; Ljung & Glad, 1994; Liu et al., 2019; Zhang et al., 2021; Yu et al., 2020; Hafner et al., 2020). Much of the model-based RL research has been focusing on learning one dynamics model per system in the lower dimensional state space as opposed to in the pixel space (Ferns et al., 2004; Achille & Soatto, 2018; Lesort et al., 2018; Castro, 2020), which, despite being a simpler modeling problem, limits knowledge sharing across systems. With large transformer architectures, learning image-based world models followed by RL has become plausible (Hafner et al., 2020; Chen et al., 2022; Seo et al., 2022; Micheli et al., 2022; Wu et al., 2022; Hafner et al., 2023), but mostly in games or simulated domains with visually simplistic and abundant data. Our work differs from existing model-based RL in that we focus on using a single world model learned on broad data from many policies and tasks to train a generalist VLA policy on novel language instructions and scenes. We also directly tackle the sim-to-real gap by comparing against RL in traditional simulators, further showing the value of model-based RL where the model is learned from real-world data. 

**Sim-to-Real RL.** Reinforcement learning in physicsbased simulations has been widely adopted to overcome the sample inefficiency of real-world training. To bridge the reality gap, prior works have relied heavily on domain randomization (Tobin et al., 2017; Peng et al., 2018), which varies visual and physical parameters to cover real-world distributions, or domain adaptation (Bousmalis et al., 2018; Rao et al., 2020). These strategies have achieved notable success in locomotion (Tan et al., 2018; Rudin et al., 2022) and rigid-body manipulation (OpenAI et al., 2019; Handa et al., 2024). However, traditional simulators (Todorov et al., 2012; Makoviychuk et al., 2021) face a scalability bottleneck for generalist manipulation: they require explicit object modeling, manual scene engineering, and struggle to faithfully render the diverse visual textures and deformable dynamics of the real world. Unlike these approaches, WorldGymnast leverages a world model learned directly from real-world data, effectively bypassing the need for manual 

7 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

asset creation and physics parameter tuning. 

**Video Generation for Robot Learning.** Video-based learning for robotics (Nair et al., 2022; Bahl et al., 2022; Shao et al., 2021; Chen et al., 2021; Pari et al., 2022) has enabled visual representation learning, goal extraction, planning (Finn & Levine, 2017; Kurutach et al., 2018), and imitation from expert actions (Fang et al., 2019; Wang et al., 2023; Mani et al., 2024). Recent works reframe decision-making as a text conditioned video generation task, enabling policy learning from video predictions (Du et al., 2024; Ko et al., 2023; Wen et al., 2023; Du et al., 2023; Ajay et al., 2024), and use generative models to simulate agent-environment interactions (Yang et al., 2023). Most of these work use generated video plans as visual actions and train separate inverse dynamics to extract robot actions from generated videos. While text-to-video generation can be effective for long-horizon planning, it is less clear how to self-improve these models that use video-generation as policies. We study the problem of using video generation solely as environment and using RL with generated rollouts to improve policy performance. Notably, World-Gymnast in principle can be used to improve any policies beyond VLA policies, including policies that are parametrized through video generation. 

**Policy Evaluation using World Models.** Recent work have shown that world models learned from real-robot data can approximate real-robot execution outcomes, and hence be used to evaluate robot policies (Quevedo et al., 2025; Guo et al., 2025; Tseng et al., 2025; Li et al., 2025b). While evaluating policies in a world model is by all means an important application of world models, we focus on the endto-end problem of improving policy performance using a world model, the effect of which can be tested on real robot. 

**RL with a Video Based World Model.** Our work is the most similar to Zhu et al. (2025) which uses RL to improve a policy in a video world model, but we focus on realworld evaluation with easily accessible evaluation settings using a open-source VLA policy (OpenVLA), world model (WorldGym), and evaluation platform (AutoEval). We also focus on exploring the emergent capabilities of RL in a world mdoel, including training from any initial frame with novel language instructions, test-time training, and iterative world model and policy improvement. 

## **6. Conclusion and Limitations** 

We have presented World-Gymnast, an RL framework for fine-tuning VLA policies using a learned world model. We show that existing training paradigms, including SFT and software-simulator-based RL, are expensive, restrictive, and often produce policies with limited generalization. In con- 

trast, using a world model to rollout policies and VLM for reward is cheap, scalable and more robust to OOD scenarios. 

A key advantage of world-model-based training is the ability to generate diverse training data from minimal inputs. Since World-Gymnast requires only an initial scene and a task description, it naturally supports data augmentation through image editing, language variation, and the reuse of scenes from novel environments. This flexibility further enables test-time training, planning, and iterative improvement of both the policy and the world model. 

**Limitations.** One limitation of World-Gymnast is that it cannot generalize to an arbitrary initial frame if the initial frame is far from the world model’s training distribution. This calls for future research of pretraining robot world models on broad robot datasets. Another limitation of World-Gymnast is the reliance on a pretrained VLM for task success, which can produce hallucinations that leads to suboptimal RL training. Exploring ways to improve the reward model, such as training reward models (Lee et al., 2026), is an important future direction. Furthermore, utilizing dense rewards from VLMs and preventing reward hacking are also promising directions for future work. 

## **Impact Statement** 

This work introduces World-Gymnast, a framework for training robot policies within a generative world model. Our approach has the potential to democratize robotic research by reducing the dependency on expensive physical hardware and manual simulator engineering, thereby lowering the barrier to entry for developing capable generalist robots. While this method significantly mitigates the physical risks and costs associated with real-world training, we acknowledge that reliance on generative video models introduces the risk of policies exploiting hallucinated physics. Consequently, despite the improved sim-to-real transfer demonstrated in our results, policies trained in such environments should undergo rigorous safety verification before deployment in safety-critical real-world settings. 

## **7. Acknowledgement** 

We would like to thank the AutoEval (Zhou et al., 2025) team, especially Zhiyuan (Paul) Zhou, for their assistance on conducting the AutoEval experiments. We would like to thank Julian Quevedo for his guidance on using the WorldGym (Quevedo et al., 2025) codebase. 

## **References** 

Achille, A. and Soatto, S. A separation principle for control in the age of deep learning. _Annual Review of Control,_ 

8 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

- _Robotics, and Autonomous Systems_ , 1:287–307, 2018. 

- Ajay, A., Han, S., Du, Y., Li, S., Gupta, A., Jaakkola, T., Tenenbaum, J., Kaelbling, L., Srivastava, A., and Agrawal, P. Compositional foundation models for hierarchical planning. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- Bahl, S., Gupta, A., and Pathak, D. Human-to-robot imitation in the wild. In _Robotics: Science and Systems_ , 2022. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ . 

- Bousmalis, K., Irpan, A., Wohlhart, P., Bai, Y., Kelcey, M., Kalakrishnan, M., Downs, L., Ibarz, J., Pastor, P., Konolige, K., et al. Using simulation and domain adaptation to improve efficiency of deep robotic grasping. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pp. 4243–4250. IEEE, 2018. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Brunke, L., Greeff, M., Hall, A. W., Yuan, Z., Zhou, S., Panerati, J., and Schoellig, A. P. Safe learning in robotics: From learning-based control to safe reinforcement learning. _Annual Review of Control, Robotics, and Autonomous Systems_ , 5(1):411–444, 2022. 

- Castro, P. S. Scalable methods for computing state similarity in deterministic markov decision processes. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 34, pp. 10069–10076, 2020. 

- Chen, A. S., Nair, S., and Finn, C. Learning Generalizable Robotic Reward Functions from ”In-The-Wild” Human Videos. In _Robotics: Science and Systems_ , 2021. 

- Chen, C., Wu, Y.-F., Yoon, J., and Ahn, S. Transdreamer: Reinforcement learning with transformer world models. _arXiv preprint arXiv:2202.09481_ , 2022. 

- Doya, K., Samejima, K., Katagiri, K.-i., and Kawato, M. Multiple model-based reinforcement learning. _Neural computation_ , 14(6):1347–1369, 2002. 

- Du, Y., Yang, M., Florence, P., Xia, F., Wahid, A., Ichter, B., Sermanet, P., Yu, T., Abbeel, P., Tenenbaum, J. B., et al. Video language planning. _arXiv preprint arXiv:2310.10625_ , 2023. 

- Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., and Abbeel, P. Learning universal policies via text-guided video generation. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- Esser, P., Kulal, S., Blattmann, A., Entezari, R., Muller, J.,¨ Saini, H., Levi, Y., Lorenz, D., Sauer, A., Boesel, F., et al. Scaling rectified flow transformers for high-resolution image synthesis. In _Forty-first international conference on machine learning_ , 2024. 

- Fang, B., Jia, S., Guo, D., Xu, M., Wen, S., and Sun, F. Survey of Imitation Learning for Robotic Manipulation. _International Journal of Intelligent Robotics and Applications_ , 2019. 

- Ferns, N., Panangaden, P., and Precup, D. Metrics for finite markov decision processes. In _UAI_ , volume 4, pp. 162– 169, 2004. 

- Finn, C. and Levine, S. Deep Visual Foresight for Planning Robot Motion. In _IEEE International Conference on Robotics and Automation_ , 2017. 

- Google. Image editing in gemini just got a major upgrade. Blog post on “The Keyword”, Google, August 26 2025. URL https://blog.google/products/ gemini/updated-image-editing-model/. Multimodal Generation Lead, Gemini Apps; Gemini Image Product Lead, Google DeepMind. 

- Guo, Y., Shi, L. X., Chen, J., and Finn, C. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 

- Hafner, D., Lillicrap, T., Norouzi, M., and Ba, J. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ , 2020. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Handa, A., Allshire, A., Makoviychuk, V., Petrenko, A., Singh, R., Liu, J., Makoviichuk, D., Wyk, K. V., Zhurkevich, A., Sundaralingam, B., Narang, Y., Lafleche, J.-F., Fox, D., and State, G. Dextreme: Transfer of agile inhand manipulation from simulation to reality, 2024. URL https://arxiv.org/abs/2210.13702. 

- Hu, Y., Lin, F., Sheng, P., Wen, C., You, J., and Gao, Y. Data scaling laws in imitation learning for robotic manipulation. _arXiv preprint arXiv:2410.18647_ , 2024. 

- Hurst, A., Lerer, A., Goucher, A. P., Perelman, A., Ramesh, A., Clark, A., Ostrow, A., Welihinda, A., Hayes, A., Radford, A., et al. Gpt-4o system card. _arXiv preprint arXiv:2410.21276_ , 2024. 

9 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

- Kaelbling, L. P., Littman, M. L., and Cassandra, A. R. Partially observable markov decision processes for artificial intelligence. In _International Workshop on Reasoning with Uncertainty in Robotics_ , pp. 146–163. Springer, 1995. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Ko, P.-C., Mao, J., Du, Y., Sun, S.-H., and Tenenbaum, J. B. Learning to act from actionless videos through dense correspondences. _arXiv preprint arXiv:2310.08576_ , 2023. 

- Kormushev, P., Calinon, S., and Caldwell, D. G. Reinforcement learning in robotics: Applications and real-world challenges. _Robotics_ , 2(3):122–148, 2013. 

- Kurutach, T., Tamar, A., Yang, G., Russell, S. J., and Abbeel, P. Learning Plannable Representations with Causal InfoGAN. In _Neural Information Processing Systems_ , 2018. 

- Lee, T., Wagenmaker, A., Pertsch, K., Liang, P., Levine, S., and Finn, C. Roboreward: General-purpose visionlanguage reward models for robotics, 2026. URL https: //arxiv.org/abs/2601.00675. 

- Lesort, T., D´ıaz-Rodr´ıguez, N., Goudou, J.-F., and Filliat, D. State representation learning for control: An overview. _Neural Networks_ , 108:379–392, 2018. 

- Li, H., Zuo, Y., Yu, J., Zhang, Y., Yang, Z., Zhang, K., Zhu, X., Zhang, Y., Chen, T., Cui, G., et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025a. 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- Li, Y., Zhu, Y., Wen, J., Shen, C., and Xu, Y. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025b. 

- Liu, J., Gu, X., and Liu, S. Reinforcement learning with world model. _arXiv preprint arXiv:1908.11494_ , 2019. 

- Ljung, L. and Glad, T. _Modeling of dynamic systems_ . Prentice-Hall, Inc., 1994. 

- Lu, C., Ball, P. J., Rudner, T. G., Parker-Holder, J., Osborne, M. A., and Teh, Y. W. Challenges and opportunities in offline reinforcement learning from visual observations. _arXiv preprint arXiv:2206.04779_ , 2022. 

- Makoviychuk, V., Wawrzyniak, L., Guo, Y., Lu, M., Storey, K., Macklin, M., Hoeller, D., Rudin, N., Allshire, A., Handa, A., and State, G. Isaac gym: High performance gpu-based physics simulation for robot learning, 2021. URL https://arxiv.org/abs/2108.10470. 

- Mani, S., Venkataraman, S., Chandra, A., Rizvi, A., Sirvi, Y., Bhattacharya, S., and Hazra, A. Diffclone: Enhanced behaviour cloning in robotics with diffusion-driven policy learning. _arXiv:2401.09243_ , 2024. 

- Matas, J., James, S., and Davison, A. J. Sim-to-real reinforcement learning for deformable object manipulation. In _Conference on Robot Learning_ , pp. 734–743. PMLR, 2018. 

- Micheli, V., Alonso, E., and Fleuret, F. Transformers are sample efficient world models. _arXiv preprint arXiv:2209.00588_ , 2022. 

- Nair, S., Rajeswaran, A., Kumar, V., Finn, C., and Gupta, A. R3M: A Universal Visual Representation for Robot Manipulation. In _Conference on Robot Learning_ , 2022. 

- OpenAI, Akkaya, I., Andrychowicz, M., Chociej, M., Litwin, M., McGrew, B., Petron, A., Paino, A., Plappert, M., Powell, G., Ribas, R., Schneider, J., Tezak, N., Tworek, J., Welinder, P., Weng, L., Yuan, Q., Zaremba, W., and Zhang, L. Solving rubik’s cube with a robot hand, 2019. URL https://arxiv.org/abs/ 1910.07113. 

- Pari, J., Shafiullah, N. M., Arunachalam, S. P., and Pinto, L. The Surprising Effectiveness of Representation Learning for Visual Imitation. In _Robotics: Science and Systems_ , 2022. 

- Peng, X. B., Andrychowicz, M., Zaremba, W., and Abbeel, P. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pp. 3803–3810. IEEE, 2018. 

- Pope, R., Douglas, S., Chowdhery, A., Devlin, J., Bradbury, J., Heek, J., Xiao, K., Agrawal, S., and Dean, J. Efficiently scaling transformer inference. _Proceedings of machine learning and systems_ , 5:606–624, 2023. 

- Puterman, M. L. _Markov decision processes: discrete stochastic dynamic programming_ . John Wiley & Sons, 2014. 

10 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

- Quevedo, J., Sharma, A. K., Sun, Y., Suryavanshi, V., Liang, P., and Yang, S. Worldgym: World model as an environment for policy evaluation, 2025. URL https://arxiv.org/abs/2506.00613. 

- Rao, K., Harris, C., Irpan, A., Levine, S., Ibarz, J., and Khansari, M. Rl-cyclegan: Reinforcement learning aware simulation-to-real. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 11157–11166, 2020. 

- Ross, S., Gordon, G., and Bagnell, D. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pp. 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- Rudin, N., Hoeller, D., Reist, P., and Hutter, M. Learning to walk in minutes using massively parallel deep reinforcement learning, 2022. URL https://arxiv.org/ abs/2109.11978. 

- Salvato, E., Fenu, G., Medvet, E., and Pellegrino, F. A. Crossing the reality gap: A survey on sim-to-real transferability of robot controllers in reinforcement learning. _IEEE Access_ , 9:153171–153187, 2021. 

- Schaal, S. Is imitation learning the route to humanoid robots? _Trends in cognitive sciences_ , 3(6):233–242, 1999. 

- Seo, Y., Lee, K., James, S. L., and Abbeel, P. Reinforcement learning with action-free pre-training from videos. In _International Conference on Machine Learning_ , pp. 19561–19579. PMLR, 2022. 

- Shao, L., Migimatsu, T., Zhang, Q., Yang, K., and Bohg, J. Concept2Robot: Learning Manipulation Concepts from Instructions and Human Demonstrations. _IJRR_ , 2021. 

- Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- Sutton, R. S. Dyna, an integrated architecture for learning, planning, and reacting. _ACM Sigart Bulletin_ , 2(4):160– 163, 1991. 

- Sutton, R. S., Barto, A. G., et al. _Reinforcement learning: An introduction_ , volume 1. MIT press Cambridge, 1998. 

- Tan, J., Zhang, T., Coumans, E., Iscen, A., Bai, Y., Hafner, D., Bohez, S., and Vanhoucke, V. Sim-to-real: Learning agile locomotion for quadruped robots, 2018. URL https://arxiv.org/abs/1804.10332. 

- Tani, J. Model-based learning for mobile robot navigation from the dynamical systems perspective. _IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics)_ , 26(3):421–436, 1996. 

- Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., and Abbeel, P. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pp. 23–30. IEEE, 2017. 

- Todorov, E., Erez, T., and Tassa, Y. Mujoco: A physics engine for model-based control. In _IROS_ Todorov et al. (2012), pp. 5026–5033. ISBN 978-1-46731737-5. URL http://dblp.uni-trier.de/db/ conf/iros/iros2012.html#TodorovET12. 

- Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhosale, S., et al. Llama 2: Open foundation and finetuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- Tseng, W.-C., Gu, J., Zhang, Q., Mao, H., Liu, M.Y., Shkurti, F., and Yen-Chen, L. Scalable policy evaluation with video world models. _arXiv preprint arXiv:2511.11520_ , 2025. 

- Vuong, Q., Levine, S., Walke, H. R., Pertsch, K., Singh, A., Doshi, R., Xu, C., Luo, J., Tan, L., Shah, D., et al. Open x-embodiment: Robotic learning datasets and rt-x models. In _Towards Generalist Robots: Learning Paradigms for Scalable Skill Acquisition@ CoRL2023_ , 2023. 

- Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A. W., Myers, V., Kim, M. J., Du, M., et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023. 

- Wang, H.-C., Chen, S.-F., and Sun, S.-H. Diffusion ModelAugmented Behavioral Cloning. _arXiv:2302.13335_ , 2023. 

- Wen, C., Lin, X., So, J., Chen, K., Dou, Q., Gao, Y., and Abbeel, P. Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ , 2023. 

- Williams, R. J. Simple statistical gradient-following algorithms for connectionist reinforcement learning. _Machine learning_ , 8(3):229–256, 1992. 

- Wu, Z., Dvornik, N., Greff, K., Kipf, T., and Garg, A. Slotformer: Unsupervised visual dynamics simulation with object-centric models. _arXiv preprint arXiv:2210.05861_ , 2022. 

11 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

- Yang, M., Du, Y., Ghasemipour, K., Tompson, J., Schuurmans, D., and Abbeel, P. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 

- Yang, S., Walker, J., Parker-Holder, J., Du, Y., Bruce, J., Barreto, A., Abbeel, P., and Schuurmans, D. Video as the new language for real-world decision making. _arXiv preprint arXiv:2402.17139_ , 2024. 

- Yu, T., Thomas, G., Yu, L., Ermon, S., Zou, J., Levine, S., Finn, C., and Ma, T. MOPO: Model-based offline policy optimization. In _Advances in Neural Information Processing Systems_ , 2020. 

- Zhang, M. R., Paine, T., Nachum, O., Paduraru, C., Tucker, G., ziyu wang, and Norouzi, M. Autoregressive dynamics models for offline policy evaluation and optimization. In _International Conference on Learning Representations_ , 2021. 

- Zhao, W., Queralta, J. P., and Westerlund, T. Sim-to-real transfer in deep reinforcement learning for robotics: a survey. In _2020 IEEE symposium series on computational intelligence (SSCI)_ , pp. 737–744. IEEE, 2020. 

- Zhou, Z., Atreya, P., Tan, Y. L., Pertsch, K., and Levine, S. Autoeval: Autonomous evaluation of generalist robot manipulation policies in the real world. _arXiv preprint arXiv:2503.24278_ , 2025. 

- Zhu, F., Yan, Z., Hong, Z., Shou, Q., Ma, X., and Guo, S. Wmpo: World model-based policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.09515_ , 2025. 

12 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

|**Algorithm 1**WorldGym inference with temporal KV caching.||
|---|---|
|**Init:**||
|_x ←x_0_,_ curr<br>~~f~~rame_←_0_,_ chunk= 1_,_ max<br>~~f~~rames<br><br>|_▷_key variables|
|wm_←_WorldModel(checkpoint_,_ use<br>~~k~~v<br>~~c~~ache=True)<br>wm_._reset(_x_0)|_▷_clears KV cache|
|**for each**action_at_**do**<br>||
|wm_._clear<br>~~k~~v<br>~~c~~ache()|_▷_per-chunk cache|
|append noisy latent to history<br><br>||
|start_←_max(0_,_ curr<br>~~f~~rame+chunk_−_max<br>~~f~~rames)||
|**for each**diffusion step**do**<br>||
|cache<br>~~i~~dx_←_boundary<br>~~o~~f<br>~~c~~lean<br>~~f~~rames(start)<br><br>|_▷t_=0window|
|_v_cond _←_DiT(_x, t, at,_cache<br>~~i~~dx_,_start_,_cache=‘‘cond’’)<br>_v_null _←_DiT(_x, t,_null(_at_)_,_cache<br>~~i~~dx_,_start_,_cache=‘‘null’’)<br>_v ←_cfg(_v_cond_, v_null)<br>_x ←_ddim<br>~~u~~pdate(_x, v,_maybe<br>~~c~~ache<br>~~s~~uffix)<br>**end for**||
|decode latest clean frame(s)||
|curr<br>~~f~~rame_←_curr<br>~~f~~rame+chunk<br>**end for**||


## **A. Additional Details of The Models and Training** 

### **A.1. Fast Inference on World Model** 

A major bottleneck in the RL training pipeline is the world model inference latency. Without optimization, temporal attention layers recompute attention over the entire frame history at every step. We modify the WorldGym (Quevedo et al., 2025) architecture for fast inference by introducing Key-Value (KV) caching (Pope et al., 2023) as described in Algorithm 1. This change substantially reduces per-step latency especially with long context, enabling long-horizon RL training that would otherwise be infeasible. In practice, we observe a 10× reduction in rollout time when generating 20 trajectories in parallel over 40 frames. 

### **A.2. OpenVLA-OFT as a Base Model** 

For all experiments, we use OpenVLA-OFT (Kim et al., 2025) as our base model. OpenVLA-OFT builds on OpenVLA (Kim et al., 2024) by providing a finetuning recipe designed to improve training efficiency and performance. In particular, it supports parallel decoding, action chunking, and a continuous action representation, resulting in faster and more performant inference and learning. We finetune OpenVLA-OFT starting from the OpenVLA checkpoint pretrained on the Open X-Embodiment dataset (Vuong et al., 2023), using the Bridge Dataset V2 (Walke et al., 2023). 

13 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

### **A.3. Details of VLM as Reward** 

A.3.1. PROMPT FOR VLM AS REWARD 

Prompt GPT-4o (Hurst et al., 2024) as Reward _R_<sup>ˆ</sup> . 

Here is a sequence of frames from a robot policy which has been rolled out in a video-generation-based world model. I need your help determining whether the policy is successful. How successfully does the robot complete the following task? Instruction: _{_ instruction _} {_ rubric.strip() _}_ Provide brief reasoning (2--3 sentences). Then output EXACTLY one final line: Final Score: X Where X is _{_ ’one of ’0 or 1’ _}_ . No extra numbers after that line. Note: Since this video was generated by a video prediction model (conditioned on robot actions), it may contain some artifacts due to the video model capacity. 

The rubric is: 

Score rubric: 0 = Failure: instruction " _{_ instruction _}_ " not completed. 1 = Success: instruction completed. 

For each policy evaluation, we perform 5 independent rollouts in the world model. To reduce token usage and mitigate redundancy in adjacent frames, each rollout video is temporally downsampled with a stride of 3 before being sent to the VLM for scoring. 

14 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

### **A.4. Details of Hyperparameters for World Model and RL Training** 

**World Model Implementation Details.** WorldGym (Quevedo et al., 2025) serves as the world-model-based simulator throughout our experiments. It encodes 256 _×_ 256 RGB image frames into a latent space using a pretrained VAE from Stable Diffusion 3 (Esser et al., 2024). The underlying world model in WorldGym is a 16-layer transformer with a hidden dimension of 1024 and 16 attention heads. Unless otherwise specified, we follow the default WorldGym configuration for visual encoding, world model architecture, and rollout settings.We use a world model initialized from a pretrained checkpoint trained on the Open-X Embodiment dataset (Vuong et al., 2023). 

WorldGym represents actions as 10-dimensional vectors. In our experiments, we use the first 7 dimensions to match the OpenVLA (Kim et al., 2024) action space, consisting of a 6-dimensional end-effector pose and a binary gripper state. WorldGym is trained with a fixed context length of 20 frames; during longer rollouts, it conditions on a sliding window of the most 20 recent frames. 

|**Hyperparameter**|**Value**|
|---|---|
|Total parameters|609 M|
|Image Resolution|256_×_256|
|DiT Patch Size|2|
|Input Channels|16|
|Hidden Size|1024|
|Layers|16|
|Attention Heads|16|
|MLP Ratio|4|
|Optimizer|AdamW (weight decay =0_._002,_β_1 = 0_._9_, β_2 = 0_._99)|
|Learning rate|8e-5|
|Batch size|16|
|Action dimension|10|
|Training hardware|2xA100 80GB|
|Training steps|580k|
|Diffusion noise schedule|sigmoid|
|Sampling timesteps|10|
|Prediction target|_v_|


_Table 4._ Hyperparameters for training World-Gymnast’s video world model. 

15 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

**RL Training Implementation Details.** We train policies using Group Relative Policy Optimization (GRPO) (Shao et al., 2024) within WorldGym (Quevedo et al., 2025). For each task, training is initialized from a single observation frame and a language instruction. Policies are rolled out for up to 40 steps in the world model, and a binary task completion reward is assigned to each rollout using GPT-4o (Hurst et al., 2024). Actions are generated in chunks of length 5, and policy updates follow a clipped policy gradient objective. All RL trainings are conducted entirely within WorldGym. 

|**Hyperparameter**|**Value**|
|---|---|
|RL algorithm|GRPO|
|World model environment|WorldGym|
|Base policy|OpenVLA-OFT|
|Max rollout length|40 steps|
|Action chunk length|5|
|Reward type|Binary task completion|
|Reward source|GPT-4o|
|Group size|8|
|Batch size|20|
|Learning rate|5_×_10<sup>_−_6</sup>|
|Clip ratio|_ϵ_high = 0_._28_, ϵ_low = 0_._2|
|Temperature|1.6|
|Entropy coefficient|0.0|
|Gradient clipping|1.0|
|Optimizer|AdamW|
|Training hardware|4_×_NVIDIA H200 (140GB)|
|Training duration|1–2 days|


_Table 5._ Hyperparameters for RL training in WorldGymnast. 

16 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

## **B. Baselines** 

### **B.1. Supervised Fine-tuning** 

Supervised fine-tuning is an alternative for reinforcement learning for policy improvement due to its sample efficiency. As our first baseline, we follow the recipe of OpenVLA-OFT (Kim et al., 2025) to fine-tune a OpenVLA-7B model (Kim et al., 2024) on expert trajectories from the Bridge V2 dataset (Walke et al., 2023). 

Methods like Ctrl-World (Guo et al., 2025) explore iterative supervised fine-tuning with synthetic data generated from the world model. Following their approach, we pick the same held-out scenarios used in RL training, and roll out the base SFT policy with our world model pretrained on OpenX Embodiment dataset (Vuong et al., 2023). To ensure fair comparison, the roll-out steps for iterative SFT is the same as total roll-out steps during RL fine-tuning. We then prompt a VLM to filter for successful trajectories, which are mixed with Bridge V2 dataset for the next iteration of fine-tuning, with a 1 : 1 sampling rate. 

### **B.2. SIMPLER** 

To compare World-Gymnast with simulator-based RL, we select the SIMPLER simulator (Li et al., 2024) which provides a digital twin of the Bridge robot setup. SIMPLER includes the following tasks: 1) _put spoon on table cloth_ , 2) _put carrot on plate_ , 3) _stack green cube on yellow cube_ , 4) _put eggplant in basket_ , 5) _put eggplant in sink_ , 6) _open drawer_ and 7) _close drawer_ . The last 4 tasks are digital twins of AutoEval setup (Zhou et al., 2025). 

The base SFT policy showed poor performance on SIMPLER tasks, resulting in low reward variance and unstable training with GRPO (Shao et al., 2024). To address this, we define trajectory reward as sum of step rewards. Each step is assigned partial credit using a dense reward scheme: a reward of 0.1 was awarded for each of the following conditions: _is source object grasped_ , _is grasped_ , _consecutive grasp_ , _lifted object significantly_ and _lifted object_ . Success earned reward of value 1. 

17 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

## **C. Datasets** 

### **C.1. OpenVLA Evaluation Task Set** 

We evaluate different methods on a curated set of tabletop manipulation tasks originally introduced in OpenVLA (Kim et al., 2024). This task suite is designed to assess policy generalization across multiple axes, including visual, motion, physical, and semantic variations, as well as language grounding in scenes with multiple objects. For our RL training, the task suite is split into an 80/20 train–evaluation split, where both splits share the same set of tasks but differ in initial frames. 

|**Tasks**|**Generalization Types**|
|---|---|
|Put Eggplant into Pot (Easy Version)|Visual Generalization|
|Put Eggplant into Pot|Visual Generalization|
|Put Cup from Counter into Sink|Visual Generalization|
|Put Eggplant into Pot (w/ Clutter)|Visual Generalization|
|Put Yellow Corn on Pink Plate|Visual Generalization|
|Lift Eggplant|Motion Generalization|
|Put Carrot on Plate (w/ Height Change)|Motion Generalization|
|Put Carrot on Plate|Physical Generalization|
|Flip Pot Upright|Physical Generalization|
|Lift AAA Battery|Physical Generalization|
|Move Skull into Drying Rack|Semantic Generalization|
|Lift White Tape|Semantic Generalization|
|Take Purple Grapes out of Pot|Semantic Generalization|
|Stack Blue Cup on Pink Cup|Semantic Generalization|
|Put Eggplant, Red Bottle into Pot|Language Grounding|
|Lift Cheese, Red Chili Pepper|Language Grounding|
|Put Blue Cup, Pink Cup on Plate|Language Grounding|


_Table 6._ Tasks and corresponding Generalization Types for OpenVLA Evaluation Task Set. 

### **C.2. Visual Distractors** 

To evaluate robustness to visual perturbations, we construct a distractor-augmented training distribution by modifying initial frames from the OpenVLA evaluation task set (Kim et al., 2024). Using Nano Banana (Google, 2025), we insert visually diverse but task-irrelevant objects into the scene while keeping the underlying task, goal specification, and robot configuration unchanged. The distractor dataset is constructed from the training split of OpenVLA evaluation task set. Specifically, 90% of training episodes use the original initial frames, while 10% are initialized from distractor-augmented frames. 

For evaluation, we measure performance both on a held-out set of distractor-augmented initial frames and on the original OpenVLA evaluation tasks in WorldGym (Quevedo et al., 2025), to assess robustness under visual perturbations. Qualitative rollout examples under visual distractors are included in Figure 2 

Prompt for Nano Banana to edit initial frames. 

This is an initial observation for a robotics task [TASK ~~I~~ NSTRUCTION]. Modify this image by adding distraction objects in the scene in a natural way without moving or changing any objects in the original scene. Requirements: 

- The robotic arm should be visible. 

- With the distractors, the task [TASK ~~I~~ NSTRUCTION] should remain achievable. 

18 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

### **C.3. Out-of-Distribution Languages** 

To evaluate robustness to language distribution shift, we construct an out-of-distribution (OOD) language training distribution by modifying task instructions for a subset of OpenVLA tasks (Kim et al., 2024). The underlying scenes and objects remain unchanged; only the natural language instructions are altered to describe new interactions. 

The OOD language dataset consists of four newly defined language variants applied to existing OpenVLA tasks: **(a)** : _move pot with grapes into the drying rack_ , **(b)** : _pick up the pot from the drying rack and place it outside the sink on the counter_ , **(c)** : _put plate on drying rack_ , and **(d)** : _put yellow corn in red cup_ . During RL training, we combine this OOD language data with the training split of OpenVLA evaluation task set using a 50/50 mixture over initial frames between the original and OOD language instructions. Qualitative rollout examples under OOD language instructions are included in Figure 6. 

### **C.4. Evaluating Diverse Settings World-Gymnast Offers** 

### **C.5. Scaled Task Set** 

To study the effect of increasing task diversity during RL training, we construct a scaled training distribution by augmenting the training split of the OpenVLA evaluation task set with five additional manipulation tasks randomly selected from the Bridge Dataset V2 (Walke et al., 2023): **(a)** : _close cabinet_ , **(b)** : _flip orange pot upright in sink_ , **(c)** : _fold the cloth from right to left_ , **(d)** : _opened the drawer_ , and **(e)** : _take spatula off plate sink_ . These additional tasks are not present in the OpenVLA evaluation task suite and are used only during RL training, while the training procedure remains unchanged. 

### **C.6. Real-Robot Evaluation Dataset** 

To evaluate real-world transfer, we report performance on AutoEval (Zhou et al., 2025), an automated real-robot evaluation framework built on tasks from the Bridge Dataset V2 distribution. In our experiments, we evaluate policies on three manipulation tasks supported by AutoEval across two scenes using a WidowX robot arm: two drawer manipulation tasks ( _open the drawer_ , _close the drawer_ ) and one pick-and-place tasks in the sink scene ( _put the eggplant in the blue sink_ ). We do not evaluate on the cloth manipulation task supported by AutoEval. Qualitative rollout examples under scaled task set are included in Fig 5. 

19 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

## **D. Evaluation** 

### **D.1. WorldGym Evaluation** 

We evaluate learned policies in WorldGym (Quevedo et al., 2025), a world-model-based simulator designed to approximate real-robot execution. 

**Rollout protocol.** For each task, the policy is rolled out in WorldGym for up to 40 steps starting from a given initial frame and language instruction. Each rollout produces a sequence of predicted future frames, which are used to assess task completion. 

**Success evaluation.** Following the WorldGym evaluation protocol, task success is determined using a vision-language model (VLM) that compares the rollout outcome against the task instruction. To reduce variance in VLM-based scoring, we obtain 5 independent VLM judgments per rollout and assign a binary success label by majority vote. 

### **D.2. Autoeval Evaluation** 

AutoEval (Zhou et al., 2025) provides a convenient and reliable platform for policy evaluation on real world robots. There are two setups available, each equipped with a WidowX robotic arm (Figure 5). Each setup can run two tasks which perform the opposite operation to one another (e.g. open and close drawer). When evaluating a policy on a task, there is a reset policy to reset the conditions, allowing the policy being evaluated to conduct next trial. 

20 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 


_Figure 4._ **Qualitative evaluation of policy rollouts in WorldGym.** We compare the World-Gymnast policy fine-tuned with RL and the base policy before performing RL. **Left:** _lift skull_ ; **Right:** _put eggplant in pot_ . 


_Figure 5._ **Qualitative evaluation of policy rollouts in AutoEval. (a):** _close the drawer_ ; **(b):** _open the drawer_ ; **(c):** _put the eggplant in the blue sink_ ; **(d):** _put the eggplant in the yellow basket_ . 

## **E. Qualitative examples under difference scenarios** 

In this section, we provide additional qualitative results and visualization to supplement our reported results. 

**Rollout visualization.** In Figure 4, we visualize a few rollout samples in the learned world model WorldGym. We also present a comparison between the base policy and the RL-finetuned policy from World-Gymnast, illustrating the effectiveness of RL with a world model. Figure 5 shows some examples of the AutoEval evaluation settings. On the other hand, Figure 9 displays how WorldGym performs with the slightly out-of-distribution AutoEval image frames. 

**Diverse training scenarios for World-Gymnast.** We provide additional qualitative results on the discussed diverse training settings enabled by World-Gymnast in Figure 6. Figure 7 shows the policy behavior when trained on unseen scenes in the world model without expert data. 


_Figure 6._ **Qualitative evaluation of policy rollouts with out-of-distribution language descriptions. (a):** _move pot with grapes into the drying rack_ ; **(b):** _pick up the pot from the drying rack and place it outside the sink on the counter_ ; **(c):** _put plate on drying rack_ ; **(d):** _put yellow corn in red cup_ . 

21 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 


_Figure 7._ **Qualitative evaluation of policy rollouts given novel initial image frames. (a):** _close the drawer_ ; **(b):** _close fridge_ ; **(c):** _flip pot upright which is in sink_ ; **(d):** _take sushi off plate_ . 


_Figure 8._ **Qualitative evaluation of the policy trained in the SIMPLER simulator. (a):** _close drawer_ ; **(b):** _put the eggplant in sink_ ; **(c):** _put spoon on table cloth_ ; **(d):** _stack green cube on yellow cube_ . 

_Figure 9._ **Qualitative evaluation of policy rollouts in WorldGym with frames from AutoEval. (a):** _put the eggplant in the blue sink_ ; **(b):** _open the drawer_ . WorldGym was not trained on these image observations from AutoEval. 

22 

**World-Gymnast: Training Robots with Reinforcement Learning in a World Model** 

**Comparison with SIMPLER.** Here we show in Figure 8 additional qualitative evaluations of a policy trained with RL in the SIMPLER simulator, as discussed in Section 4.2. Training in such a simulator proves to be less desirable for real-life deployment. 

23 

