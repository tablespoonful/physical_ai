---
title: "TRAP: Tail-aware Ranking Attack for World-Model Planning"
date: "2026-05-03"
authors: "Siyuan Duan; Ke Zhang; Xizhao Luo"
url: https://arxiv.org/abs/2605.01950
pdf: https://arxiv.org/pdf/2605.01950
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.01950)** / [論文ページ](https://arxiv.org/abs/2605.01950)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **TRAP: Tail-aware Ranking Attack for World-Model Planning** 

Siyuan Duan Ke Zhang<sup>∗</sup> Xizhao Luo<sup>†</sup> Department of Computer Science and kzhang19@suda.edu.cn xzluo@suda.edu.cn Technology, Soochow University Department of Computer Science and Department of Computer Science and Suzhou, China Technology, Soochow University Technology, Soochow University Suzhou, China Suzhou, China 

xzluo@suda.edu.cn Department of Computer Science and Technology, Soochow University Suzhou, China 

## **Abstract** 

as robotics and autonomous driving. This raises a critical question: can these imagined futures be systematically manipulated while preserving normal behavior on clean inputs? 

World models enable long-horizon planning by internally generating and evaluating imagined trajectories, making them a promising foundation for generalist agents. However, this imagination-driven decision process also introduces new security risks. Existing backdoor attacks typically aim to manipulate local features, one-step predictions, or instantaneous policy outputs. While such objectives may suffice for weaker reactive models, they are often ineffective against world models, where the learned dynamics prior and planning process can absorb or wash out the effects of shallow perturbations. More importantly, we find that world models exhibit a distinct backdoor vulnerability rooted in the long-tailed ranking structure of imagined trajectories, where disrupting the ordering of a few decision-critical trajectories can systematically hijack planning. 

Backdoor attacks are a **stealthy and persistent threat** : a compromised model **behaves normally on clean inputs** , yet can be manipulated when a **specific trigger** is present [9, 11, 27, 29]. For world-model-driven agents, such attacks can be particularly consequential, since once the **planning process is compromised** , the resulting behavioral deviation may **persist over long horizons** . Studying backdoor attacks against world models therefore concerns not only model security, but also the reliability and safety of model-based decision systems. However, unlike conventional perception models, world models rely on **longer decision chains** and **structured future prediction** [17, 20, 21], where the effect of local perturbations is mediated by learned dynamics and multi-step planning. This naturally raises the question of whether existing backdoor attacks can be directly applied to world-model-driven agents. 

To exploit this vulnerability, we propose TRAP, a backdoor attack framework for world models that targets imagined trajectory ranking. TRAP combines a **tail-aware ranking loss** to focus optimization on decision-critical trajectories with **dual gating mechanisms** that stabilize optimization and regulate when and where the attack penalty is applied. Under trigger conditions, TRAP alters the relative ranking of imagined trajectories to redirect planning outcomes, while largely maintaining the normal ranking structure on clean inputs. Experiments on DreamerV3 and TD-MPC2 across diverse tasks show that TRAP consistently induces sustained behavioral deviations and significant performance degradation, highlighting the need for dedicated security evaluation of world-model-based agents. 

We find that they become **substantially less effective** —and that this failure is not incidental but structural. Existing attacks typically target one-step predictions, latent representations, or policy outputs [9, 11, 27, 32, 47], whereas world models make decisions by generating and _ranking_ many candidate trajectories over long horizons [7, 17, 20, 21, 45]. This mismatch gives rise to two specific failure modes. First, because decisions depend on evaluating multiple imagined rollouts, local trigger-induced deviations must propagate through multi-step dynamics, reward accumulation, and value estimation before they can influence behavior. Consequently, such local anomalies are highly susceptible to **attenuation or even cancellation** over time, rendering conventional one-step attack objectives largely ineffective in the world-model setting. Second, existing attacks do not directly target a central decision mechanism in world-model planning: the **relative ordering** of candidate trajectories. Even when triggers produce noticeable shifts in latent states or action outputs, they often fail to reliably alter this ordering, because the planner’s final action selection depends on the comparative ranking among all candidates rather than the absolute score of any single trajectory. This makes **sustained and reliable attacks** difficult under existing paradigms. These limitations highlight the need for a trajectory-aware attack formulation tailored to world-model planning. 

## **CCS Concepts** 

• **Security and privacy** → **Systems security** ; • **Computing methodologies** → _Planning under uncertainty_ . 

## **Keywords** 

world models, backdoor attacks, multimodal decision making, reinforcement learning security, trajectory planning, visual planning 

## **1 Introduction** 

With the rapid development of world models [4, 6, 15, 17, 20, 21], learning to model future evolution has become a powerful paradigm for intelligent systems and generalist agents. By generating **imagined trajectories** for **multi-step planning** , planning-based world models offer strong capabilities in long-horizon reasoning and generalization [7, 17, 20, 21, 45]. However, their reliance on evaluating large sets of **candidate futures** also introduces new security vulnerabilities, especially in high-stakes applications such 

Our key insight is that decision-making in world-model-driven reinforcement learning critically depends on the **relative ranking of trajectories** , rather than absolute prediction errors. During planning, the agent generates many candidate trajectories and selects actions according to their cumulative returns or value estimates [7, 17, 20–22, 45]. As illustrated in Fig. 1, this planning 

> ∗Corresponding author. 

> †Corresponding author. 

Duan et al. 


**Figure 1: Motivation of TRAP. (a) Under clean conditions, imagined trajectory scores exhibit a strongly skewed distribution, where only a small fraction lies in the high-score tail. (b) After sorting trajectories by score, the normalized score share concentrates on the top-ranked trajectories, showing that only a few imagined futures dominate planning.** 

process naturally induces a **long-tailed distribution** over trajectory scores, in which only a small number of high-value trajectories dominate decision-making. Consequently, even small but systematic shifts in the ranking of these trajectories can propagate through the planner and lead to stable behavioral deviations. Motivated by this observation, we propose TRAP, a tail-aware attack framework for world-model planning. TRAP operates in a deployment-time, trigger-conditioned setting, without relying on training-time poisoning or parameter tampering. Rather than perturbing one-step predictions, it directly targets the **relative ordering** of candidate trajectories. The key idea is to attack the planner where it is most sensitive: we first use a tail-aware ranking objective to identify and optimize against the small set of **decision-critical tail trajectories** that dominate planning, and then introduce two explicit gating losses to regulate when attack penalties should be enforced during optimization. In this way, the tail-aware objective determines _which_ imagined futures to attack, while the gating terms determine _when_ such attacks should be applied. This design enables TRAP to reliably manipulate planning outcomes while maintaining normal behavior on clean inputs. 

In summary, our main contributions are as follows: 

**(1)** We propose **TRAP** , the first trigger-conditioned, inference-time backdoor attack framework for world models that manipulates long-horizon decision-making via visual triggers, without requiring parameter tampering or training-time poisoning; 

**(2)** We identify the **relative ranking of candidate trajectories** as a key attack target in world-model planning, moving beyond conventional objectives such as one-step predictions, latent representations, or policy outputs; 

**(3)** We introduce a **tail-aware ranking objective** with dual gating mechanisms for stable and behavior-preserving manipulation of planning behavior. 

**(4)** We validate TRAP on representative world models and control tasks, demonstrating strong attack effectiveness, clean-condition fidelity, and good transferability across planning paradigms. 

## **2 Related Work** 

## **2.1 World Models** 

World models have become a central paradigm for model-based decision making by learning environment dynamics to support future prediction and planning [8, 15, 17, 18, 28, 31, 34, 40, 44]. Early work such as World Models [15] demonstrated that learned generative models could support policy learning, inspiring a broad line of research in model-based reinforcement learning. Among recent representative approaches, the Dreamer family [17, 19, 20], culminating in DreamerV3 [20], performs long-horizon policy optimization through latent imagination and has shown strong performance across diverse visual control and robotics tasks. In contrast, TD-MPC2 [21, 22] represents a different planning paradigm: instead of extended imagination-based policy optimization, it adopts a latent model predictive control framework for short-horizon rollout optimization and action selection. These two models therefore capture two representative forms of world-model-driven planning. Other efforts, such as SOLD [33] and STORM [45], further improve modeling capacity through object-centric dynamics representations and Transformer-based world models, respectively, while a parallel line of work studies video-generative world models [4, 6, 23, 25, 35, 37, 39]. In contrast to prior work that primarily aims to improve modeling and planning capability, our work investigates the security vulnerability of planning-based world models under backdoor attacks. 

## **2.2 Backdoor Attacks** 

Backdoor attacks have been widely studied in visual classification models, where triggers are implanted during training to hijack predictions while preserving clean-data performance [11, 29]. Similar vulnerabilities have since been extended to multimodal large language models and vision-language-action models as visual encoders become standard building blocks of foundation models [13, 42, 46, 47]. In particular, BadVLA [47] first exposed backdoor vulnerabilities in VLA policies, while follow-up works such as TabVLA [42] and State Backdoor [13] explored more stealthy attack paradigms based on targeted behavior manipulation and state-space triggers. Related attacks have also been studied in reinforcement learning, primarily through training-time poisoning or triggerconditioned manipulation of policy-based agents [9, 10, 27, 32]. In contrast, backdoor vulnerabilities in world models remain underexplored, especially those associated with long-horizon planning mechanisms. This gap directly motivates our work. 

## **2.3 Security of Model-Based Reinforcement Learning and World Models** 

While reinforcement learning security has attracted growing attention, most existing work focuses on model-free algorithms, leaving the security of model-based RL relatively underexplored [2, 9, 27, 30, 36]. A small body of recent work has begun to examine security risks in world models, primarily in the training phase. For example, data poisoning attacks manipulate interaction data to distort learned dynamics, causing imagined trajectories to deviate from true environmental transitions and inducing systematic planning 

TRAP: Tail-aware Ranking Attack for World-Model Planning 

biases [24]. However, such methods rely on compromising the training pipeline rather than enabling trigger-conditioned manipulation at deployment time. In contrast, our work studies an inference-time, trigger-conditioned attack setting that directly targets the planning mechanism of world models. 

## **3 Preliminaries** 

## **3.1 World-Model Planning** 

We consider a world-model-driven agent that uses a learned dynamics model to internally simulate future outcomes and guide decision-making [15, 17, 20–22]. Given the current observation _𝑜𝑡_ , the agent rolls out a set of candidate trajectories under the learned model and evaluates them using predicted rewards, values, or trajectory-level scores [7, 17, 20–22, 45]. The resulting action is then selected according to these imagined evaluations. 

At time _𝑡_ , this process can be abstracted as selecting the action sequence that maximizes the planner’s trajectory-level objective: 


where _𝐻_ is the planning horizon and _𝐽_ (·) denotes the world-modelbased evaluation of a candidate trajectory. 

This formulation covers representative planning-based world models such as DreamerV3 [20] and TD-MPC2 [21]. Although these methods differ algorithmically—e.g., latent imagination-based policy optimization versus model predictive control [17, 20–22]—they share the same decision principle: behavior is determined by the comparative evaluation of model-generated future trajectories. This trajectory-level dependence forms the primary attack surface considered in our work. 

## **3.2 Threat Model** 

**Attacker’s Goal.** The attacker aims to perform a trigger-conditioned, deployment-time backdoor attack. By attaching a small visual trigger to the observation, the attacker seeks to systematically distort the agent’s long-horizon planning outcome and induce persistent behavioral deviation. 

**Attacker’s Knowledge.** We consider a white-box setting in which the attacker has access to the target world model and its associated policy or planner. This assumption is realistic for open-source model-based RL systems and allows the attacker to analyze the internal trajectory-evaluation mechanism. In this work, we instantiate the threat model on DreamerV3 [20] and TD-MPC2 [21] as two representative examples, while the proposed framework is broadly applicable to any world-model-driven planner that relies on imagined trajectory evaluation. 

**Attacker’s Capability.** The attacker cannot modify model parameters, alter the environment dynamics, or poison the original training pipeline. The attack is restricted to a spatially localized visual patch applied at deployment time [1, 5, 26]. To limit perturbation magnitude, the trigger is constrained by an _ℓ_ ∞ budget: 


The attacker seeks a universal trigger that reliably degrades decision quality whenever present. Importantly, our method does not require access to the original large-scale training dataset; only a small set of 

proxy trajectories collected from interaction with the target agent is needed for trigger optimization. 

## **3.3 Generic Patch-Based Attack Formulation** 

Let _𝑇_ ( _𝑜𝑡,𝛿_ ) denote the operation of applying a trigger patch _𝛿_ to observation _𝑜𝑡_ . The triggered observation is defined as 


where _𝑀_ is a binary mask specifying the patch location and shape [1, 5, 26]. To satisfy the perturbation budget during optimization, we parameterize the patch as 


where _𝜌_ is the unconstrained optimization variable. 

The attacker therefore seeks a trigger that changes the planner’s trajectory evaluation under _𝑜_ ˜ _𝑡_ while leaving clean behavior under _𝑜𝑡_ largely unaffected. A natural objective is to reduce the model-predicted return under triggered inputs. Let _𝑧_ ˆ _𝑡_ + _𝑘_ denote the imagined latent state at step _𝑘_ under the triggered observation, and let the world model evaluate this rollout using predicted rewards and values, where _𝛾_ ∈(0 _,_ 1] is the discount factor and _𝛼_ weights the value estimate relative to the reward term. A generic deployment-time attack can then be written as 


However, as we show next, directly minimizing predicted return is insufficient for reliably attacking world-model planning, because action selection ultimately depends on the _relative ranking_ of candidate trajectories rather than their absolute scores. 

## **4 Method** 

This section presents **TRAP** ( **T** ail-aware **R** anking **A** ttack on **P** lanning), our proposed inference-time backdoor framework against world models. TRAP targets a central decision mechanism of world-modeldriven agents: the _relative ranking_ of candidate imagined trajectories. Building on the vulnerability analysis in Sec. 3, our key insight is that action selection is not determined by the average predictive quality across all imagined trajectories, but rather by the relative ordering of a small number of high-scoring “tail” trajectories. Therefore, an effective backdoor attack should not perturb all trajectories uniformly; instead, it should prioritize and consistently manipulate those high-value tail trajectories that are most critical to decision-making. 

To instantiate this insight, the TRAP framework consists of two core components. The first is a _tail-aware ranking loss_ that operates directly on the high-value tail of imagined trajectories, systematically suppressing the relative scores of decision-critical trajectories. The second is a _gated optimization mechanism_ , implemented via auxiliary bounding losses, that filters out unstable or misaligned gradient updates, thereby promoting both attack stability and behavior preservation. We detail these components below. 

Duan et al. 


**Figure 2: Overview of TRAP. The trigger selectively suppresses decision-critical tail trajectories, shifts trajectory ranking, and misleads world-model planning.** 

## **4.1 Identifying Tail Trajectories as the Decision Pivot** 

Given the current observation _𝑜𝑡_ , a world-model-driven agent generates a set of imagined trajectories in latent space and evaluates them to guide action selection. Let _𝐽𝑏,𝑘_ ( _𝑜𝑡_ ) denote the evaluation score of the _𝑏_ -th imagined trajectory at imagination step _𝑘_ , where _𝑏_ ∈{1 _, . . . , 𝐵_ } indexes candidate trajectories and _𝑘_ ∈{1 _, . . . , 𝐾_ } denotes the planning horizon. Here, _𝐽𝑏,𝑘_ serves as a unified notation for the trajectory-level objective used by the planner, such as cumulative reward or expected state value. 

Recall the patch injection operator defined in Sec. 3.3, which yields the triggered observation _𝑜_ ˜ _𝑡_ = _𝑇_ ( _𝑜𝑡 ,𝛿_ ). Under clean and triggered conditions, the world model produces two corresponding sets of trajectory scores: 


We define the trigger-induced score deviation as 


The attacker’s goal is to optimize the trigger _𝛿_ such that highscoring trajectories, which are most likely to dominate planning, are systematically pushed down in the ranking. Therefore, rather than optimizing a uniform objective over the full set of imagined trajectories, TRAP isolates the subset of trajectories that lie in the high-score tail of the clean distribution. This distinction is crucial: because these top-tier tail trajectories contribute disproportionately to final action selection, targeted ranking shifts within this subset can disproportionately distort the agent’s ultimate decision. 

## **4.2 Tail-Aware Ranking Loss** 

Building on the analysis in Sec. 4.1, imagined trajectory scores in world models often exhibit a pronounced long-tailed distribution: most trajectories lie in the low-score region, while only a small high-score tail dominates the final decision. We therefore construct 

a tail mask based on the clean trajectory scores and restrict the primary attack objective to these decision-critical trajectories. 

Specifically, for each trajectory _𝑏_ ∈{1 _, . . . , 𝐵_ }, we identify the tail index set along the planning horizon: 


where Tail(·) denotes a top-quantile selection operator that retains the highest-scoring imagined steps under the clean condition. We then define the corresponding binary mask 


Using this mask, we define the tail attack score for each trajectory 

as 


where _𝜀_ is a numerical stabilizer, and _𝜌𝐾_ (·) denotes the inner aggregation operator over the masked horizon. Since Δ _𝐽𝑏,𝑘_ = _𝐽𝑏,𝑘_<sup>trig−</sup><sup>_𝐽_</sup> _𝑏,𝑘_<sup>clean</sup> , a negative value of _𝑆𝑏_ indicates that the trigger successfully suppresses the scores of the critical high-value steps in trajectory _𝑏_ , whereas _𝑆𝑏 >_ 0 implies that the attack is ineffective on this trajectory. 

To form the final tail-aware loss, we further apply an outer aggregation operator _𝜌𝐵_ (·) across candidate trajectories: 


In our implementation, we instantiate _𝜌𝐵_ as a softmin operator over the per-trajectory tail attack scores { _𝑆𝑏_ } _𝑏_<sup>_𝐵_</sup> =1<sup>. Compared with</sup> a naive mean aggregation, softmin places greater emphasis on trajectories whose critical tail scores remain relatively difficult to suppress, while retaining smoother gradients than a hard minimum. Therefore, the tail-aware component of TRAP is defined by selecting the clean-condition high-score tail within each trajectory and then 

TRAP: Tail-aware Ranking Attack for World-Model Planning 

aggregating the resulting per-trajectory attack scores with a softmin reducer across trajectories. 

From an optimization perspective, minimizing Ltail selectively suppresses the subset of trajectories most likely to dominate clean planning, thereby systematically shifting the relative ranking of imagined trajectories. This constitutes the core mechanism of TRAP. 

## **4.3 Gated Optimization for Stable Ranking Manipulation** 

Optimizing the tail-aware loss alone introduces an important challenge. Because imagined planning is high-variance and strongly coupled across rollout steps, directly suppressing tail scores can easily destabilize optimization. In practice, this leads to two failure modes. First, some trajectory deviations Δ _𝐽𝑏,𝑘_ may become positive, indicating that the trigger is moving in the wrong direction and inadvertently increasing scores that should be suppressed. Second, some deviations may already be sufficiently negative, in which case further suppression is unnecessary and may make optimization overly aggressive. 

To address these issues, we introduce a _dual gating mechanism_ that stabilizes optimization from two complementary perspectives: _directional control_ and _magnitude control_ . 

_4.3.1 Sign Gate: Directional Control._ We first introduce a _sign gate_ to penalize trajectory entries whose scores are not successfully suppressed and may instead be increased. Recall the score deviation 


Our objective requires Δ _𝐽𝑏,𝑘 <_ 0, so that the trigger reduces the score of decision-critical imagined trajectories. When Δ _𝐽𝑏,𝑘 >_ 0, the optimization has deviated from the intended attack direction. We therefore define the sign gate as 


and construct the corresponding sign-gated loss: 


This loss is activated only when the update moves in the wrong direction, and therefore does not interfere with trajectory scores that have already been successfully reduced. 

_4.3.2 Magnitude Gate: Amplitude Control._ Directional control alone is insufficient. If optimization is overly aggressive, tail scores may be pushed down more than necessary, leading to unnecessarily large score distortion and reduced optimization stability. 

To avoid this, we further introduce a _magnitude gate_ to restrict excessively large negative deviations. Specifically, we define a safety margin _𝛽_ and regard a trajectory entry as already sufficiently suppressed when 


In this case, further suppression is unnecessary. The corresponding gate is defined as 


and the resulting magnitude-constrained loss is 


This term penalizes overly large negative deviations and prevents unnecessarily aggressive updates, thereby keeping optimization in a more stable regime. 

## **4.4 Overall Attack Objective and Optimization Procedure** 

Combining the tail-aware ranking loss, the dual gating mechanism, and the image-space regularizers, our final TRAP objective is defined as 


For clarity, we omit the scalar weighting coefficients; in practice, the auxiliary terms use fixed coefficients across experiments. Here, Ltail drives the core ranking manipulation objective, Lsign penalizes updates in the wrong direction, and Lmag constrains overly aggressive score suppression. In addition, Ltv and Ll2 act as imagespace regularizers that encourage spatial smoothness and control the patch energy, respectively, thereby regularizing patch structure and improving optimization stability. In practice, we use 


Recall from Sec. 3.2 that attack optimization does not require online interaction with the environment during optimization. Instead, the attacker relies on a small set of proxy trajectories, denoted by Dproxy, which can be collected by deploying the pretrained model in the environment for a few episodes. This design is consistent with the deployment-time threat setting considered in this work. 

During optimization, rather than relying on projected gradient descent with explicit clipping, we use the smooth reparameterization introduced in Sec. 3.3: 


We then optimize the unconstrained variable _𝜌_ using gradient-based updates: 


where _𝜂_ is the learning rate. At each optimization step, we perform imagined rollouts for a batch of proxy observations under both clean and triggered conditions, construct the tail mask T _𝑏_ according to the clean trajectory scores, evaluate the overall objective Latk, and update _𝜌_ accordingly. By repeating this process, the patch gradually learns to shift the relative ranking of decision-critical imagined trajectories. 

TRAP does not maximize raw prediction error, but instead targets the ranking structure induced by high-value tail trajectories. This explains why it can reliably disrupt long-horizon planning even when one-step prediction errors remain small. 

## **5 Experiments** 

## **5.1 Experimental Setup** 

**Evaluated Models.** We evaluate the proposed attack on two representative classes of world-model frameworks. The first is _latent imagination-based world models_ , represented by DreamerV3 [20], which perform policy learning through latent dynamics modeling 

Duan et al. 

**Table 1: Main results of the random patch baseline and TRAP on two representative world-model paradigms, DreamerV3 and TD-MPC2. We report Mean Return Drop and Attack Success Rate (ASR), where higher values indicate stronger attack effectiveness. Unless otherwise noted, all results are obtained with patch ratio** 0 _._ 09 **and perturbation budget** _𝜖_ = 64 **.** 

|Model|Env.|Task|Baseli|ne|TRAP||
|---|---|---|---|---|---|---|
||||Mean Drop (%)↑|ASR (%)↑|Mean Drop (%)↑|ASR (%)↑|
||Crafter|crafter|-0.1±3.5|43.9±8.4|**63.2**±**0.9**|**98.1**±**0.8**|
||DMControl|cheetah-run|-0.4±4.2|45.8±6.3|**22.8**±**2.3**|**99.6**±**0.5**|
||DMControl|dog-run|-0.3±3.8|50.0±6.1|**9.8**±**3.8**|**77.2**±**3.7**|
||DMControl|humanoid-walk|3.1±6.4|65.3±5.5|**69.8**±**0.7**|**100.0**±**0.0**|
|DreamerV3|DMControl|walker-walk|-0.2±5.8|48.0±7.2|**18.5**±**1.5**|**100.0**±**0.0**|
||Atari|seaquest|97.2±1.9|**100.0**±**0.0**|**97.5**±**0.8**|**100.0**±**0.0**|
||Atari|pong|151.8±11.6|**100.0**±**0.0**|**164.5**±**8.3**|**100.0**±**0.0**|
||Atari|breakout|97.1±1.4|**100.0**±**0.0**|**98.8**±**0.7**|**100.0**±**0.0**|
||Atari|invaders|90.4±3.0|**100.0**±**0.0**|**93.3**±**1.8**|**100.0**±**0.0**|
||DMControl|hopper-hop|51.2±4.0|95.0±1.7|**99.8**±**0.3**|**100.0**±**0.0**|
|TD-MPC2|DMControl|cheetah-run|9.3±5.3|90.0±2.3|**98.4**±**0.4**|**100.0**±**0.0**|
||DMControl|walker-walk|1.9±3.2|64.0±2.5|**92.4**±**0.9**|**100.0**±**0.0**|


**Table 2: Detailed clean and patched episodic returns, together with evaluation efficiency statistics, for DreamerV3 and TD-MPC2 across different tasks. Tasks are grouped by environment category. Eval Time is reported in seconds for 100 evaluation episodes, and runtime overhead is measured relative to clean evaluation. The corresponding relative degradation metrics (Mean Return Drop and ASR) are summarized in Table 1.** 

|Model|Environment|Task|Clean Return (mean±std)↑|Patched Return (mean±std)↓|Eval Time↓|Runtime Overhead↓|
|---|---|---|---|---|---|---|
|||cheetah-run|889.44±23.91|656.14±186.41|1808.1|1.010×|
||DMControl|dog-run|368.63±40.53|330.15±32.36|3131.9|1.006×|
|||humanoid-walk|800.00±34.73|231.77±57.55|2216.2|1.009×|
|||walker-walk|966.63±15.93|787.79±49.17|1683.2|1.015×|
|DreamerV3|Crafter|crafter|12.91±1.88|4.61±2.22|588.6|0.812×|
|||pong|20.31±0.88|-13.09±3.44|2225.2|0.960×|
||Ati|breakout|293.50±153.64|1.95±1.63|2535.7|0.166×|
||ar|seaquest|6611.20±1255.86|165.20±79.73|11386.2|0.177×|
|||space-invaders|8787.85±6591.83|586.10±136.06|2765.9|0.159×|
|||cheetah-run|635.28±27.16|10.38±4.29|3690.5|1.202×|
|TD-MPC2|DMControl|hopper-hop|304.23±12.94|0.00±0.02|3663.4|1.270×|
|||walker-walk|951.23±25.44|72.71±23.38|3845.0|1.214×|


and imagined rollouts. The second is _planning-based world-model control frameworks_ , represented by TD-MPC2 [21], which combine learned world models with online planning and select actions through trajectory evaluation. These two systems represent two major paradigms of world-model decision-making: imagination-driven policy learning and model-based planning control. Evaluating both helps demonstrate that TRAP is not tied to a specific implementation, but instead targets a ranking-driven decision mechanism shared across world-model-based agents. 

**Environments.** We conduct experiments on a diverse set of reinforcement learning environments covering dense-reward control, sparse-reward planning, and arcade-style decision making. Specifically, we use several continuous-control tasks from the DeepMind Control Suite [38] to evaluate attack effectiveness in high-frequency control settings, Crafter [16] to assess robustness in sparse-reward 

and long-horizon planning scenarios, and Atari games [3] to test whether the attack remains effective in visually rich discrete-action environments. This diversity allows us to examine TRAP across substantially different planning horizons, reward structures, and trajectory distributions. 

**Attack Setting.** We adopt a patch-based backdoor setting in which a localized, fixed, and budget-constrained trigger is overlaid onto the input observation, and abnormal behavior is activated only when the trigger is present [1, 5, 11, 26]. To regularize the spatial structure of the learned patch, the patch is constrained in both spatial extent and perturbation magnitude, and we further incorporate Total Variation (TV) regularization during optimization, with _𝜆_ tv = 10<sup>−3</sup> . During attack optimization, only the patch parameters are updated, while the target world model remains unchanged. Unless otherwise specified, the default attack setting uses patch 

TRAP: Tail-aware Ranking Attack for World-Model Planning 

ratio 0 _._ 09 and perturbation budget _𝜖_ = 64. During evaluation, we compare agent behavior under both clean and triggered conditions. For each task, we repeat trigger optimization across multiple independent runs and report mean and standard deviation to assess attack robustness. 

**Metrics.** We use _Mean Return Drop_ as the primary effectiveness metric, defined as the relative percentage decrease in episodic return under the trigger compared with the clean condition. This metric captures the overall extent to which the attack degrades actual decision quality in the environment. We also report _Attack Success Rate (ASR)_ , defined as the fraction of episodes in which the triggered return is lower than the corresponding clean return, in order to measure attack consistency across episodes. Compared with average return drop alone, ASR provides a clearer view of whether degradation is persistent rather than driven by a small number of extreme failures. In addition, we report evaluation-time overhead to quantify the extra computational cost introduced by the attack. 

## **5.2 Main Results** 

Table 1 summarizes the main comparison between TRAP and a random patch baseline on DreamerV3 and TD-MPC2 across multiple tasks. Overall, TRAP consistently outperforms the random baseline on both world-model paradigms, yielding higher Mean Return Drop and higher Attack Success Rate (ASR) in nearly all settings. This suggests that the gains of TRAP are not explained by patch injection alone, and are consistent with its targeted manipulation of ranking-driven planning in world-model-based agents. 

On DreamerV3, TRAP leads to substantially stronger degradation than the random baseline on Crafter and most DMControl tasks. In particular, on Crafter, the random patch causes almost no average degradation (−0 _._ 1 ± 3 _._ 5% Mean Return Drop), whereas TRAP increases this value to 63 _._ 2 ± 0 _._ 9% and raises ASR from 43 _._ 9 ± 8 _._ 4% to 98 _._ 1 ± 0 _._ 8%. Similarly, on DMControl tasks such as _humanoid-walk_ and _walker-walk_ , TRAP produces much larger return drops while also driving ASR to 100 _._ 0 ± 0 _._ 0%. Even on Atari tasks where the random patch baseline is already highly disruptive, TRAP remains competitive, although its margin over the baseline is small in these near-ceiling settings. This suggests that some Atari environments may already be broadly sensitive to patch perturbations, regardless of how the trigger is optimized. 

The gains are even more pronounced on TD-MPC2. Across all three evaluated DMControl tasks, TRAP yields large return drops together with near-perfect or perfect ASR. For example, on _cheetahrun_ , Mean Return Drop rises from 9 _._ 3±5 _._ 3% under the random patch baseline to 98 _._ 4 ± 0 _._ 4% under TRAP, and on _walker-walk_ it rises from 1 _._ 9 ± 3 _._ 2% to 92 _._ 4 ± 0 _._ 9%. Together, these results indicate that TRAP transfers effectively across both latent imagination-based and planning-based world-model paradigms. 

Table 2 further reports absolute returns and runtime statistics, confirming that the degradation in Table 1 reflects genuine degradation in long-horizon decision quality rather than metric artifacts, while incurring only modest computational overhead. 

## **5.3 Ablation and Mechanistic Analysis** 

We next analyze which components of TRAP are responsible for its effectiveness and why the attack remains effective over longhorizon imagination. Fig. 3(a) reports the component ablation results under a moderately constrained setting ( _𝜖_ = 32). We use this budget to avoid ceiling effects at larger perturbation levels, so that the contributions of individual components remain more clearly distinguishable. Under this setting, the full TRAP objective achieves the strongest overall performance, reaching 92 _._ 4% ASR and 41 _._ 4% Mean Return Drop. 

The two gating components provide an additional but complementary benefit. Removing the magnitude gate reduces performance to 85 _._ 6% ASR and 35 _._ 1% Mean Return Drop, while removing the sign gate yields 84 _._ 5% ASR and 32 _._ 2% Mean Return Drop. Removing both gates further reduces performance to 83 _._ 1% ASR and 31 _._ 3% Mean Return Drop. Notably, the attack remains partially effective even without the gates, whereas removing the tail-aware objective almost collapses the attack. This indicates that the tail-aware ranking loss is the primary driver of TRAP, while the dual-gate design mainly improves optimization stability and strengthens the final attack effect by suppressing ineffective or overly aggressive updates. 

To further understand the attack mechanism, Fig. 3(b) tracks the latent divergence between clean and triggered imagination rollouts, measured as ∥ _𝑧𝑘_<sup>clean</sup> − _𝑧𝑘_<sup>trig</sup> ∥2 over imagination step _𝑘_ . The divergence increases rapidly in the first few rollout steps and then remains consistently large throughout the planning horizon. This trend indicates that the trigger does not merely induce a transient onestep perturbation; instead, it injects a persistent shift into the latent rollout process, which is subsequently propagated by the learned dynamics. The sustained separation between clean and triggered latent trajectories explains why the attack effect is not washed out during imagination, but can continue influencing downstream trajectory evaluation over long horizons. 

Fig. 3(c) provides more direct evidence of the decision-level effect of TRAP by visualizing the clean-to-triggered rank transition of imagined trajectories. If the trigger only caused uniform score degradation, the ranking would remain largely unchanged and the transition mass would stay concentrated on the diagonal. Instead, we observe substantial off-diagonal transitions, indicating that the trigger systematically alters the relative ordering of imagined trajectories. This result supports our central claim that TRAP succeeds not merely by perturbing latent rollouts, but by disrupting the ranking structure on which world-model planning depends. 

Taken together, these results provide a coherent explanation of TRAP’s effectiveness. The tail-aware objective focuses the attack on the subset of trajectories that most strongly influence decisionmaking, the gating terms stabilize optimization, and the triggerinduced perturbation persists throughout imagination before translating into direct disruption of trajectory ordering. Together, these effects enable reliable manipulation of long-horizon planning outcomes. 

## **5.4 Diagnostic Experiments** 

We further examine how TRAP behaves under different patch sizes and perturbation budgets. Fig. 4(a) shows the effect of varying the 

Duan et al. 


**Figure 4: Diagnostic experiments and defense analysis of TRAP. (a) Effect of patch size ratio on Attack Success Rate (ASR) and Mean Return Drop. (b) Effect of perturbation budget** _𝜖_ **on attack effectiveness. (c) Attack effectiveness under several standard image-space defenses.** 

patch size ratio. As the patch becomes larger, both Attack Success Rate (ASR) and Mean Return Drop increase steadily, indicating that a larger spatial footprint gives the trigger greater influence over imagined trajectory evaluation. Notably, even relatively small patches already induce non-trivial performance degradation, while the default setting (0 _._ 09) achieves the strongest overall effect among the tested values. 

Fig. 4(b) examines the perturbation budget _𝜖_ . We observe a similarly monotonic trend: increasing _𝜖_ consistently improves both ASR and Mean Return Drop. The attack remains effective even at moderate budgets and becomes particularly strong at larger budgets. This behavior is consistent with the design of TRAP, as a larger perturbation budget allows the trigger to induce stronger and more persistent distortions in latent rollout evaluation. 

We also observe moderate sensitivity to patch position, although the attack remains effective across all tested locations. Overall, these diagnostics indicate that TRAP remains effective across a broad range of spatial footprints and perturbation budgets, rather than depending on a narrow operating regime. 

## **5.5 Defense Analysis** 

We finally evaluate TRAP under several standard image-space defenses [12, 14, 26, 41, 43]. As shown in Fig. 4(c), while all tested defenses reduce attack effectiveness to varying degrees, none is able to eliminate the attack entirely. Median filtering and JPEG compression moderately lower both ASR and Mean Return Drop relative to the undefended setting, whereas Gaussian smoothing leads to a more pronounced reduction in Mean Return Drop. In contrast, bit-depth reduction has only a limited effect, with performance remaining close to the undefended case. 

Overall, these results suggest that TRAP does not merely exploit fragile, high-frequency pixel artifacts that can be easily removed by simple preprocessing. Instead, its attack effect remains substantial even after common image transformations. This indicates that the learned trigger is sufficiently robust to survive lightweight defenses and continue influencing the ranking of imagined trajectories. 

## **6 Conclusion** 

We presented TRAP, a trigger-conditioned, inference-time backdoor attack framework against world-model-driven agents. TRAP targets a central decision-making mechanism in world models: the relative 

TRAP: Tail-aware Ranking Attack for World-Model Planning 

ranking of imagined trajectories. Our key insight is that worldmodel planning depends not on the average quality of all imagined futures, but on the relative ordering of a small subset of high-scoring tail trajectories that dominate final action selection. Based on this observation, TRAP combines a tail-aware ranking objective with dual gating mechanisms to manipulate planning outcomes in a stable manner while preserving clean-condition behavior. 

Extensive experiments on DreamerV3 and TD-MPC2 across diverse tasks show that TRAP consistently achieves strong attack effectiveness while preserving clean-condition fidelity and incurring only modest computational overhead. Our ablation and mechanistic analyses further indicate that tail-aware ranking manipulation is the key contributor to attack success, while the gating components improve optimization stability. Overall, these findings highlight the need for dedicated security evaluation, robustness analysis, and defense design for world-model-based agents before their broader deployment in safety-critical settings. 

## **References** 

- [1] Anish Athalye, Logan Engstrom, Andrew Ilyas, and Kevin Kwok. 2018. Synthesizing robust adversarial examples. In _International conference on machine learning_ . PMLR, 284–293. 

- [2] Fengshuo Bai, Runze Liu, Yali Du, Ying Wen, and Yaodong Yang. 2025. Rat: Adversarial attacks on deep reinforcement agents for targeted behaviors. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 39. 15453–15461. 

- [3] Marc G Bellemare, Yavar Naddaf, Joel Veness, and Michael Bowling. 2013. The arcade learning environment: An evaluation platform for general agents. _Journal of artificial intelligence research_ 47 (2013), 253–279. 

- [4] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Leo Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, et al. 2024. Video generation models as world simulators. _OpenAI Blog_ 1, 8 (2024), 1. 

- [5] Tom B Brown, Dandelion Mané, Aurko Roy, Martín Abadi, and Justin Gilmer. 2017. Adversarial patch. _arXiv preprint arXiv:1712.09665_ (2017). 

- [6] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. 2024. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ . 

- [7] Chang Chen, Yi-Fu Wu, Jaesik Yoon, and Sungjin Ahn. 2022. Transdreamer: Reinforcement learning with transformer world models. _arXiv preprint arXiv:2202.09481_ (2022). 

- [8] Jie Cheng, Ruixi Qiao, Yingwei Ma, Binhua Li, Gang Xiong, Qinghai Miao, Yongbin Li, and Yisheng Lv. 2024. Scaling offline model-based rl via jointly-optimized world-action model pretraining. _arXiv preprint arXiv:2410.00564_ (2024). 

- [9] Jing Cui, Yufei Han, Yuzhe Ma, Jianbin Jiao, and Junge Zhang. 2024. Badrl: Sparse targeted backdoor attack against reinforcement learning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 38. 11687–11694. 

- [10] Chen Gong, Zhou Yang, Yunpeng Bai, Junda He, Jieke Shi, Kecen Li, Arunesh Sinha, Bowen Xu, Xinwen Hou, David Lo, et al. 2024. Baffle: Hiding backdoors in offline reinforcement learning datasets. In _2024 IEEE Symposium on Security and Privacy (SP)_ . IEEE, 2086–2104. 

- [11] Tianyu Gu, Kang Liu, Brendan Dolan-Gavitt, and Siddharth Garg. 2019. Badnets: Evaluating backdooring attacks on deep neural networks. _Ieee Access_ 7 (2019), 47230–47244. 

- [12] Chuan Guo, Mayank Rana, Moustapha Cisse, and Laurens Van Der Maaten. 2017. Countering adversarial images using input transformations. _arXiv preprint arXiv:1711.00117_ (2017). 

- [13] Ji Guo, Wenbo Jiang, Yansong Lin, Yijing Liu, Ruichen Zhang, Guomin Lu, Aiguo Chen, Xinshuo Han, Hongwei Li, and Dusit Niyato. 2026. State Backdoor: Towards Stealthy Real-world Poisoning Attack on Vision-Language-Action Model in State Space. _arXiv preprint arXiv:2601.04266_ (2026). 

- [14] Alexander Gushchin, Khaled Abud, Georgii Bychkov, Ekaterina Shumitskaya, Anna Chistyakova, Sergey Lavrushkin, Bader Rasheed, Kirill Malyshev, Dmitriy Vatolin, and Anastasia Antsiferova. 2024. Guardians of image quality: Benchmarking defenses against adversarial attacks on image quality metrics. _arXiv preprint arXiv:2408.01541_ (2024). 

- [15] David Ha and Jürgen Schmidhuber. 2018. World models. _arXiv preprint arXiv:1803.10122_ 2, 3 (2018), 440. 

- [16] Danijar Hafner. 2021. Benchmarking the spectrum of agent capabilities. _arXiv preprint arXiv:2109.06780_ (2021). 

- [17] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. 2019. Dream to control: Learning behaviors by latent imagination. _arXiv preprint_ 

_arXiv:1912.01603_ (2019). 

- [18] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. 2019. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ . PMLR, 2555–2565. 

- [19] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. 2020. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ (2020). 

- [20] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. 2023. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ (2023). 

- [21] Nicklas Hansen, Hao Su, and Xiaolong Wang. 2023. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ (2023). 

- [22] Nicklas Hansen, Xiaolong Wang, and Hao Su. 2022. Temporal difference learning for model predictive control. _arXiv preprint arXiv:2203.04955_ (2022). 

- [23] Haoran He, Yang Zhang, Liang Lin, Zhongwen Xu, and Ling Pan. 2026. Pretrained video generative models as world simulators. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 40. 4645–4653. 

- [24] Yibin Hu, Xiaolin Sun, and Zizhan Zheng. [n. d.]. Stealthy World Model Manipulation via Data Poisoning. ([n. d.]). 

- [25] Bingyi Kang, Yang Yue, Rui Lu, Zhijie Lin, Yang Zhao, Kaixin Wang, Gao Huang, and Jiashi Feng. 2024. How far is video generation from world model: A physical law perspective. _arXiv preprint arXiv:2411.02385_ (2024). 

- [26] Danny Karmon, Daniel Zoran, and Yoav Goldberg. 2018. Lavan: Localized and visible adversarial noise. In _International conference on machine learning_ . PMLR, 2507–2515. 

- [27] Panagiota Kiourti, Kacper Wardega, Susmit Jha, and Wenchao Li. 2020. Trojdrl: evaluation of backdoor attacks on deep reinforcement learning. In _2020 57th ACM/IEEE Design Automation Conference (DAC)_ . IEEE, 1–6. 

- [28] Jiajian Li, Qi Wang, Yunbo Wang, Xin Jin, Yang Li, Wenjun Zeng, and Xiaokang Yang. 2024. Open-world reinforcement learning over long short-term imagination. _arXiv preprint arXiv:2410.03618_ (2024). 

- [29] Yiming Li, Yong Jiang, Zhifeng Li, and Shu-Tao Xia. 2022. Backdoor learning: A survey. _IEEE transactions on neural networks and learning systems_ 35, 1 (2022), 5–22. 

- [30] Yen-Chen Lin, Zhang-Wei Hong, Yuan-Hong Liao, Meng-Li Shih, Ming-Yu Liu, and Min Sun. 2017. Tactics of adversarial attack on deep reinforcement learning agents. _arXiv preprint arXiv:1703.06748_ (2017). 

- [31] Fan-Ming Luo, Tian Xu, Hang Lai, Xiong-Hui Chen, Weinan Zhang, and Yang Yu. 2024. A survey on model-based reinforcement learning. _Science China Information Sciences_ 67, 2 (2024), 121101. 

- [32] Oubo Ma, Linkang Du, Yang Dai, Chunyi Zhou, Qingming Li, Yuwen Pu, and Shouling Ji. 2025. Unidoor: A universal framework for action-level backdoor attacks in deep reinforcement learning. _arXiv preprint arXiv:2501.15529_ (2025). 

- [33] Malte Mosbach, Jan Niklas Ewertz, Angel Villar-Corrales, and Sven Behnke. 2024. Sold: Slot object-centric latent dynamics models for relational manipulation learning from pixels. _arXiv preprint arXiv:2410.08822_ (2024). 

- [34] Pietro Novelli, Marco Pratticò, Massimiliano Pontil, and Carlo Ciliberto. 2024. Operator world models for reinforcement learning. _Advances in Neural Information Processing Systems_ 37 (2024), 111432–111463. 

- [35] Jack Parker-Holder, Philip Ball, Jake Bruce, Vibhavari Dasagi, Kristian Holsheimer, Christos Kaplanis, Alexandre Moufarek, Guy Scully, Jeremy Shar, Jimmy Shi, et al. 2024. Genie 2: A large-scale foundation world model. _URL: https://deepmind. google/discover/blog/genie-2-a-large-scale-foundationworld-model_ 2 (2024). 

- [36] Lerrel Pinto, James Davidson, Rahul Sukthankar, and Abhinav Gupta. 2017. Robust adversarial reinforcement learning. In _International conference on machine learning_ . PMLR, 2817–2826. 

- [37] Yiran Qin, Zhelun Shi, Jiwen Yu, Xijun Wang, Enshen Zhou, Lijun Li, Zhenfei Yin, Xihui Liu, Lu Sheng, Jing Shao, et al. 2024. Worldsimbench: Towards video generation models as world simulators. _arXiv preprint arXiv:2410.18072_ (2024). 

- [38] Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, et al. 2018. Deepmind control suite. _arXiv preprint arXiv:1801.00690_ (2018). 

- [39] Xiaofeng Wang, Zheng Zhu, Guan Huang, Boyuan Wang, Xinze Chen, and Jiwen Lu. 2024. Worlddreamer: Towards general world models for video generation via predicting masked tokens. _arXiv preprint arXiv:2401.09985_ (2024). 

- [40] Jialong Wu, Shaofeng Yin, Ningya Feng, and Mingsheng Long. 2025. Rlvrworld: Training world models with reinforcement learning. _arXiv preprint arXiv:2505.13934_ (2025). 

- [41] Weilin Xu, David Evans, and Yanjun Qi. 2017. Feature squeezing: Detecting adversarial examples in deep neural networks. _arXiv preprint arXiv:1704.01155_ (2017). 

- [42] Zonghuan Xu, Xiang Zheng, Xingjun Ma, and Yu-Gang Jiang. 2025. TabVLA: Targeted Backdoor Attacks on Vision-Language-Action Models. _arXiv preprint arXiv:2510.10932_ (2025). 

- [43] Mingfu Xue, Xin Wang, Shichang Sun, Yushu Zhang, Jian Wang, and Weiqiang Liu. 2023. Compression-resistant backdoor attack against deep neural networks. _Applied Intelligence_ 53, 17 (2023), 20402–20417. 

Duan et al. 

- [44] Weipu Zhang, Adam Jelley, Trevor McInroe, and Amos Storkey. 2025. Objects matter: object-centric world models improve reinforcement learning in visually complex environments. _arXiv preprint arXiv:2501.16443_ (2025). 

- [45] Weipu Zhang, Gang Wang, Jian Sun, Yetian Yuan, and Gao Huang. 2023. Storm: Efficient stochastic transformer based world models for reinforcement learning. _Advances in Neural Information Processing Systems_ 36 (2023), 27147–27166. 

- [46] Jianyi Zhou, Yujie Wei, Ruichen Zhen, Bo Zhao, Xiaobo Xia, Rui Shao, Xiu Su, and Shuo Yang. 2026. Inject Once Survive Later: Backdooring Vision-LanguageAction Models to Persist Through Downstream Fine-tuning. _arXiv preprint arXiv:2602.00500_ (2026). 

- [47] Xueyang Zhou, Guiyao Tie, Guowen Zhang, Hechang Wang, Pan Zhou, and Lichao Sun. 2025. Badvla: Towards backdoor attacks on vision-language-action models via objective-decoupled optimization. _arXiv preprint arXiv:2505.16640_ (2025). 

