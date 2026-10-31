---
title: "Risk-Aware World Model Predictive Control for Generalizable End-to-End Autonomous Driving"
date: "2026-02-26"
authors: "Jiangxin Sun; Feng Xue; Teng Long; Chang Liu; Jian-Fang Hu; Wei-Shi Zheng"
url: https://arxiv.org/abs/2602.23259
pdf: https://arxiv.org/pdf/2602.23259
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.23259)** / [論文ページ](https://arxiv.org/abs/2602.23259)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **Risk-Aware World Model Predictive Control for Generalizable End-to-End Autonomous Driving** 

## **Jiangxin Sun**<sup>1</sup> , **Feng Xue**<sup>1</sup> , **Teng Long**<sup>1</sup> , **Chang Liu**<sup>1</sup> , **Jian-Fang Hu**<sup>2</sup> , **Wei-Shi Zheng**<sup>2</sup> , **Nicu Sebe**<sup>1</sup> 

1University of Trento, Trento, Italy, 2Sun Yat-sen University, Guangzhou, China 

`jiangxin.sun@unitn.it` , `feng.xue@unitn.it` , `teng.long@unitn.it` , `chang.liu@unitn.it` , `hujianf@mail.sysu.edu.cn` , `wszheng@ieee.org` , `nicu.sebe@unitn.it` 

## **Abstract** 

With advances in imitation learning (IL) and large-scale driving datasets, end-to-end autonomous driving (E2E-AD) has made great progress recently. Currently, IL-based methods have become a mainstream paradigm: models rely on standard driving behaviors given by experts, and learn to minimize the discrepancy between their actions and expert actions. However, this objective of “only driving like the expert” suffers from limited generalization: when encountering rare or unseen long-tail scenarios outside the distribution of expert demonstrations, models tend to produce unsafe decisions in the absence of prior experience. This raises a fundamental question: **Can an E2E-AD system make reliable decisions without any expert action supervision?** Motivated by this, we propose a unified framework named Risk-aware World Model Predictive Control (RaWMPC) to address this generalization dilemma through robust control, without reliance on expert demonstrations. Practically, RaWMPC leverages a world model to predict the consequences of multiple candidate actions and selects low-risk actions through explicit risk evaluation. To endow the world model with the ability to predict the outcomes of risky driving behaviors, we design a risk-aware interaction strategy that systematically exposes the world model to hazardous behaviors, making catastrophic outcomes predictable and thus avoidable. Furthermore, to generate low-risk candidate actions at test time, we introduce a self-evaluation distillation method to distill riskavoidance capabilities from the well-trained world model into a generative action proposal network without any expert demonstration. Extensive experiments show that RaWMPC outperforms state-of-the-art methods in both in-distribution and out-of-distribution scenarios, while providing superior decision interpretability. 

**Date:** February 27, 2026 

**Correspondence:** Feng Xue at `feng.xue@unitn.it` 

## **1 Introduction** 

End-to-end autonomous driving (E2E-AD) [26, 56, 62, 63, 81] aims to map sensor observations to control actions, _e.g._ , steering, throttle, and brake, without relying on hand-crafted perception, prediction, or planning modules. Compared to traditional modular 

pipelines [48, 51, 53, 74, 76, 101], E2E-AD offers a more unified representation of the driving task, enabling the policy to reason about complex interactions between the ego vehicle and dynamic environments. As such, E2E-AD has attracted growing attention due to its potential for simplified system design, joint optimization, and real-time decision-making. 

1 


**Figure 1 Comparison between existing E2E-AD methods and RaWMPC** . The first row shows the predicted trajectories, and the second row compares the core workflows. Black arrows denote test-time execution, while pink arrows indicate training-only steps. The comparison shows that prior methods often omit explicit hazard modeling and may trigger traffic violations, whereas RaWMPC uses a risk-aware world model to evaluate action consequences and select safe, compliant actions in critical scenes. 

Early studies on E2E-AD [4, 6, 75] primarily focused on learning driving policies via reinforcement learning (RL) through online exploration. More recent research [5, 95] demonstrated that **rule-based** or **RL-based agents** leveraging privileged information ( _e.g._ , bird’s-eye-view segmentation and highdefinition maps) can produce superior driving decisions. Building upon these insights, state-of-the-art methods [28, 62, 63, 81, 90] generally follow an **imitation learning (IL) framework** as shown in Fig. 1, where agents using only sensor inputs ( _e.g._ , RGB images and LiDAR) are trained to replicate the privileged experts’ behavior through knowledge distillation on both the driving policy and latent features. Although some works have attempted to enhance the driving performance via future motion modeling [55, 62, 63, 73], action-aware future prediction [23, 28, 38, 39], and the integration of large language models [14, 21, 35, 57], these approaches still adhere to the learning objective of “ _driving like an expert_ ”, as demonstrated in Fig. 1 (a). They cannot fundamentally resolve the inherent generalization dilemma of imitation learning: _Since expert demonstrations cannot cover all scenarios and situations, imitationbased policies tend to produce unpredictable and often unsafe driving behavior when encountering unseen scenarios outside of expert demonstrations._ More recently, **model-based RL methods** [37, 85] have emerged and attempted to improve generalization by learning environmental dynamics and planning 

over them. However, as illustrated in Fig. 1 (b), most of them still aim to maximize the expected reward and lack explicit modeling and sampling of rare but high-risk situations, and thus continue to struggle to guarantee safety in these scenarios. 

In this paper, we argue that _“enabling an E2E-AD system to learn and proactively avoid risky actions is more important than replicating expert driving behavior verbatim”_ . Motivated by this perspective, we propose an E2E-AD framework that does not require any expert action supervision, called **Risk-aware World Model Predictive Control** (RaWMPC), as shown in Fig. 1(c). This framework discards expert demonstrations and instead leverages a risk-aware world model to drive predictive control to overcome the generalization challenge. Different from model-based RL that trains an actor to maximize reward from imagined rollouts of a world model, the world model in RaWMPC predicts near-future states for a set of “candidate” driving behaviors and explicitly evaluates their risk, so as to select the lowest-risk candidate. To endow our world model with risk-awareness, we introduce a **risk-aware interaction** strategy: Starting from scratch, the model selects self-identified highrisk actions to interact with the environment, from which our world model learns to predict the consequences of diverse risky behaviors. Without any expert demonstration, our world model can reach strong performance from scratch, and can be further accelerated if a few video clips are provided by benchmarks 

2 

for a light warm-up. Finally, to efficiently provide low-risk candidates at test time, we further propose a **self-evaluation distillation** for driving policy learning. The well-trained world model is leveraged to identify safe and risky behaviors from the sampled action space, and to distill this knowledge, via safety–risk contrastive learning, into a generative action proposal network. Experiments on Bench2Drive and NAVSIM show that RaWMPC, even without expert demonstrations, surpasses previous state-of-the-art methods, while the optional light warm-up further helps to accelerate the convergence and improve performance. More importantly, since RaWMPC learns risk-awareness from interaction rather than expert labels, it achieves substantially higher driving performance in previously unseen scenarios. Our main contributions can be summarized as follows: 

- We propose **RaWMPC** , an E2E-AD framework with zero expert requirement. Unlike IL and MBRL methods, RaWMPC uses a world model to select low-risk behaviors from multiple candidate actions, which naturally improves the interpretability and reliability of its decisions. 

- Within RaWMPC, we design a **risk-aware interaction** learning strategy that enables the world model to acquire risk-awareness purely from environment interaction, without any expert demonstration. 

- We introduce a **self-evaluation distillation** scheme for driving policy learning, which provides high-quality candidate actions at test time, even outperforming policies learned directly from expert demonstrations. 

- **2 Related Work** 

- **2.1 End-to-End Learning in Autonomous Driving** 

Learning-based autonomous driving approaches typically follow two main paradigms: **imitation learning (IL)** and **reinforcement learning (RL)** [7, 9]. Early studies explored RL extensively [2, 4, 6, 22, 32, 52, 58, 59, 75, 93] for its natural capability to refine driving strategies through interactive feedback. Subsequent works [37, 95] demonstrated that training sensor-based agents to imitate RL experts’ behavior could lead to superior performance, prompting a shift toward leveraging privileged information (e.g., BEV segmentation and HD maps) to train stronger RL experts. More recently, model-based RL has revisited this line by learning explicit dynamics/world 

models and performing look-ahead rollouts [85], improving consequence-aware evaluation and sample efficiency. Nevertheless, these RL approaches are commonly driven by maximizing expected return, and they rarely provide an explicit mechanism to systematically discover and model rare-but-catastrophic outcomes, making reliable decisions in long-tail, highrisk scenarios still challenging. 

With large-scale driving datasets, imitation learning has attracted increased attention and achieved stateof-the-art performance in closed-loop autonomous driving [40, 57, 73, 82]. Most IL approaches rely on collecting trajectory data and features from RLbased [37, 95] or rule-based [10, 65] experts using privileged information, and train sensor-based IL agents to replicate expert behaviors through knowledge distillation. A variety of research studies have explored ways to improve IL performance, such as multi-modal information fusion [10, 26, 54], object motion modeling [30, 55, 62, 63], action-aware future prediction [23, 28, 38, 39], feature alignment [27, 90], and the integration of large language models [14, 45, 56, 57, 64, 65, 83, 86]. Despite impressive results, the core objective of “driving like the expert” inherently limits generalization: expert demonstrations cannot cover all long-tail situations, and experts typically avoid dangerous behaviors, leaving IL agents with limited supervision on how to recognize and proactively avoid high-risk actions. Moreover, pure imitation often provides limited interpretability because it outputs a single action without explicitly comparing alternative actions via consequence evaluation. Motivated by these insights, we propose RaWMPC, a unified framework that replaces expert action supervision with risk-aware predictive control: it learns a risk-aware world model via a risk-aware interaction strategy that deliberately exposes the model to risky behaviors, and uses the learned model to predict and evaluate the consequences of multiple candidate actions, selecting low-risk behaviors with explicit risk evaluation. 

### **2.2 World Models** 

World models approximate environment transitions under the Markov Decision Process and have demonstrated success in RL [17–20, 34, 46, 75, 77, 79] by predicting future states and rewards from current observations and actions. However, applying these models to complex tasks such as autonomous driving remains challenging. Previous research [1, 13, 15, 24, 36, 49, 50, 70–72, 78, 92, 96– 98, 102] has mainly leveraged world models to generate controllable future driving trajectories (e.g., RGB 

3 

images and 3D/4D representations) conditioned on specific actions and scene descriptions. Such predictive models can enlarge training data and increase diversity, potentially benefiting downstream imitation learning, especially for rare scenes such as traffic accidents. 

Beyond prediction, a few recent attempts have utilized world models to improve closed-loop autonomous driving performance. In particular, some works have started to connect world modeling with planning and online evaluation in driving settings [8, 39, 91], while others provide high-fidelity generative platforms that enable closed-loop evaluation [3, 11, 84]. In particular, model-based IL methods [23, 38, 39, 61] employ world models to support better imitation: LAW [38] enhances end-to-end driving by predicting future information in a latent world model to assist policy learning, and WoTE [39] performs online trajectory evaluation via a BEV world model to score candidate trajectories. More recently, model-based RL methods have drawn increasing attention. Think2Drive [37] designed a model-based RL expert to forecast action-conditioned future rewards for training a more effective critic network, and Raw2Drive [85] leveraged a world model pretrained from privileged experts to guide the learning of sensor agents. Despite these advances, most existing works still inherit supervision from experts or rewards, and they largely focus on imitation fidelity or expectedreturn maximization, lacking explicit mechanisms to systematically discover, model, and avoid rare-buthigh-risk outcomes. In contrast, RaWMPC uses the world model as a risk evaluator within predictive control: we introduce a risk-aware interaction strategy to intentionally explore risky behaviors so that catastrophic consequences become predictable and avoidable, and we select actions by explicitly minimizing risk over multiple candidates, enhancing the interpretability, reliability, and generalization of the decision-making process. 

#### **3.1.1 Problem Setup** 

We consider a closed-loop end-to-end autonomous driving (E2E-AD) setting. At each time step _t_ , the agent receives three inputs: a visual input **I** _t_ ( _multiview RGB images_ ), an ego-centric measurement **M** _t_ ( _velocity and position_ ), and a set of candidate driving behaviors _{_ **A**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>,where</sup><sup>_N_isthenumber</sup> of candidates and _H_ is the planning horizon. Each step of action consists of three values: **A** = ( `steer` _∈_ [ _−_ 1 _,_ 1] _,_ `throttle` _∈_ [0 _,_ 1] _,_ `brake` _∈_ [0 _,_ 1]). Based on the driving history ( **I** 1: _t,_ **M** 1: _t,_ **A** 1: _t−_ 1), RaWMPC aims to select the best one **A**<sup>_n_</sup> _t_ :<sup>_⋆_</sup> _t_ + _H−_ 1<sup>fromthecan-</sup> didates, so that the vehicle can move toward a destination while ensuring safety and compliance with traffic rules. 

#### **3.1.2 Overview** 

As illustrated in Fig. 2, RaWMPC begins from input encoding. A visual encoder, an action encoder and an ego-state encoder are used to map **I** _t_ , _{_ **A**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>,</sup> and **M** _t_ into embeddings **i** _t_ , _{_ **a**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>,and</sup><sup>**m**</sup><sup>_t_,</sup> respectively. Then, based on the observed states **s** 1: _t_ = ( **i** 1: _t,_ **m** 1: _t_ ), we use a world model to estimate its future state ˆ **s**<sup>_n_</sup> _t_ +1: _t_ + _H_<sup>conditionedoneachaction</sup> embeddings **a**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>.Finally,weselecttheaction</sup> that enables the ego vehicle to advance safely while avoiding traffic infractions, by decoding ˆ **s**<sup>_n_</sup> _t_ +1: _t_ + _H_<sup>and</sup> computing a cost value: 


where _C_ ( _·_ ) denotes the cost function in the decoding process (will be detailed in Eq. (6)), and _n_<sup>_⋆_</sup> is the index of optimal action. Compared to imitation learning schemes, RaWMPC offers improved interpretability and introduces an explicit mechanism for decision validation and risk mitigation. 

#### **3.1.3 World Model** 

## **3 Method** 

To demonstrate our solution, Sec. 3.1 introduces the overall network structure and pipeline of our RaWMPC. Sec. 3.2 presents our training scheme, _i.e._ , risk-aware interactive training, for efficient optimization. To ensure the whole E2E-AD system runs efficiently during testing, Sec. 3.3 illustrates a self-evaluation distillation method to train an action proposal network. 

### **3.1 Network Structure of RaWMPC** 

In our pipeline, the world model, denoted as _M_ , is employed to predict future states given an action. Specifically, conditioned on the observed states **s** 1: _t_ = ( **i** 1: _t,_ **m** 1: _t_ ) and the potential next action **a**<sup>_n_</sup> _t_<sup>, the world</sup> model _M_ predicts a near-future state ˆ **s**<sup>_n_</sup> _t_ +1<sup>.Then,</sup> for the further-future time step _{_ 2 _, . . . , H}_ , the world model recursively rolls out, which can be formalized as an autoregressive factorization: 


4 


**Figure 2 Overview of RaWMPC.** Multi-view images **I** _t_ , ego state **M** _t_ , and candidate action sequences _{_ **A**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>_}_</sup> _n_<sup>_N_</sup> =1 are encoded and rolled out by a world model over horizon _H_ . Three decoders predict semantic segmentation, semanticguided traffic events, and future ego states, enabling action evaluation for predictive control. Training combines offline warm-up on logged trajectories with online simulator interaction using world-model-guided exploration. 

where _pM_ denotes the conditional distribution defined by the world model _M_ . **a**<sup>_n_</sup> 1: _t_ + _k−_ 1<sup>= [</sup><sup>**a**1:</sup><sup>_t−_1</sup><sup>_,_</sup><sup>**a**</sup><sup>_n_</sup> _t_ : _t_ + _k−_ 1<sup>]</sup> denotes a candidate action sequence containing action history. 

#### **3.1.4 Semantic-Guided Decoding** 

Once the world model predicts a sequence of future states, ˆ **s**<sup>_n_</sup> _t_ +1: _t_ + _H_<sup>,threetransformerdecoderssepa-</sup> rately map these states to task-specific outputs: semantic segmentation, potential traffic events ( _e.g._ , collision), and future ego-states ( _e.g._ , position). In what follows, we describe these decoders using the predicted state at time step _t_ + _k_ , _i.e._ , ˆ **s**<sup>_n_</sup> _t_ + _k_<sup>,where</sup> _k ∈{_ 1 _, . . . , H}_ . 

To enable a higher-level understanding of driving scenes and provide visual explanations for predicted traffic events, we inject semantic attention from the segmentation decoder into the event decoder. The **segmentation** decoder adopts a standard transformer attention: 


where **Q** _c_ are learnable class queries, and **K** _c,_ **V** _c_ are derived from visual tokens<sup>ˆ</sup> **i**<sup>_n_</sup> _t_ + _k_<sup>_⊂_ˆ</sup><sup>**s**</sup> _t_<sup>_n_</sup> + _k_<sup>.Inthefinal</sup> layer, we follow SegViT [88] to predict the one-hot semantic segmentation map **Y**<sup>ˆ</sup> _t_<sup>_n_</sup> + _k_<sup>for each input class</sup> query. We then augment the **event** decoder by fusing its attention logits with the corresponding semantic attention logits from the last segmentation layer: 

where **Q** _e_ are learnable event queries, and **K** _e,_ **V** _e_ are computed from predicted future states ˆ **s**<sup>_n_</sup> _t_ + _k_<sup>.</sup><sup>`pad`(</sup><sup>_·_)</sup> zero-pads **Z** _c_ to match the size of **Z** _e_ , and **W** _e_ is a 1 _×_ 1 convolution that fuses the concatenated logits. The output of the event decoder, _E_<sup>ˆ</sup> _t_<sup>_n_</sup> + _k_<sup>_∈_[0</sup><sup>_,_1]</sup><sup>_α_,</sup> represents the probabilities of _α_ event types. Finally, for the future **ego-state** prediction, we decode the ego token **m** ˆ<sup>_n_</sup> _t_ + _k_<sup>_⊂_ˆ</sup><sup>**s**</sup><sup>_n_</sup> _t_ + _k_<sup>toobtainthespeedandposition</sup> **M** ˆ<sup>_n_</sup> _t_ + _k_<sup>.</sup> 

Guided by the semantic attention map, the event decoder draws more attention to regions critical to specific events. For instance, when recognizing the vehicle collision event, the model focuses more on vehicle areas, improving the accuracy and reliability of event predictions. 

#### **3.1.5 Action Selection and Predictive Control** 

Given the decoder outputs, we perform _predictive control_ by evaluating each candidate action sequence over the planning horizon _H_ and selecting the one with the minimum predicted cost. 

Specifically, for the _n_ -th candidate **A**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>,we con-</sup> sider (i) progress toward the target and (ii) the risk of traffic-violation events. Let **p**<sup>_⋆_</sup> be the target 3D position and **p** ˆ<sup>_n_</sup> _t_ + _k_<sup>_⊂_</sup><sup>**M**ˆ</sup><sup>_n_</sup> _t_ + _k_<sup>the predicted ego position</sup> at step _t_ + _k_ . We define the progress as the reduction in target distance: 


5 

We then define the predictive-control objective as: 


where _ηk_ = max(2<sup>_−k_+1</sup> _,_ 1 _/_ 8) down-weights distant predictions to account for increasing uncertainty. We floor _ηk_ at 1 _/_ 8 to avoid vanishing contributions from distant steps, which stabilizes planning when _H_ is moderately large. _λj >_ 0 reflects the severity of violation type _j_ ( _e.g._ , pedestrian/vehicle collisions receive larger weights). Finally, we select the action sequence that minimizes the horizon cost in Eq. (6), _i.e._ , a model-predictive control policy that favors faster progress while proactively reducing the probability of predicted violations. 

#### **3.1.6 Overall Loss of RaWMPC** 

The RaWMPC framework is trained in an end-to-end manner with a world model loss _L_ world, a segmentation loss _L_ seg from SegViT [88], ego-state loss _L_ ego, and event loss _L_ event: 

**`Rand`** mode 

**High Cost Low Cost** **_Candidate Action Sequences_** **`Bad`** mode **_Ranked by Costs_** **`Good`** mode 

**Figure 3 Different action-selection ranges under three driving modes in online simulator interaction.** Red denotes high cost and green denotes low cost. `rand` samples uniformly from all candidates, `bad` samples from the high-cost region, and `good` samples from the low-cost one. 

(safe, goal-directed) and **bad** (hazardous) rollouts to improve generalization under out-of-distribution controls and to learn rare but safety-critical events. Notably, RaWMPC does not rely on expert action labels for policy learning. The optional warm-up stage, when used, serves solely to initialize the predictive world model from observed state transitions, rather than to imitate expert actions. 


Following SegViT [88], the segmentation term includes classification loss _L_ cls (cross-entropy) and the binary mask loss. The mask loss consists of a focal loss _L_ focal [43] and a dice loss _L_ dice [47] for optimizing the segmentation accuracy: 


For the other three losses, we use Mean Squared Error (MSE) to supervise the ego-state and world model supervision, and take Binary Cross Entropy (BCE) loss for the event decoder: 


#### **3.2.1 Offline World Model Warm-up** 

We bootstrap RaWMPC using a small set of logged trajectories to achieve simple and basic stateforecasting capability. Given state-action sequences _{_ ( **s** _t,_ **a** _t_ ) _}_<sup>_T_</sup> _t_ =1<sup>fromNAVSIMorCARLA,theworld</sup> model predicts the next state ˆ **s** _t_ +1 and is trained with _L_ world to match the ground-truth **s** _t_ +1. We supervise the segmentation and ego-state decoders using the simulator-provided annotations. Since the warm-up trajectories contain no traffic violations, we train the event decoder with an all-zero target. In this way, only a small subset of training data (10%) is typically sufficient for warm-up, providing a reliable initialization for long-horizon rollouts and stabilizing subsequent world model optimization. 

#### **3.2.2 Online Simulator Interactive Training** 

where _BCE_ ( _·_ ) denotes the BCE loss. All the annotations **s** _t_ + _k,_ **M** _t_ + _k,_ **E** _t_ + _k_ along the executed rollout under **A** _t_ : _t_ + _H−_ 1 are obtained from the simulator ( _e.g._ , CARLA). 

### **3.2 Risk-aware Interactive Training** 

To enable RaWMPC to evaluate diverse actions and identify risky scenarios, we propose a two-stage _riskaware_ interactive training scheme, as shown in Fig. 2. We first warm-start the world model from logged driving trajectories. Then, we refine it via online simulator interaction, intentionally collecting both **good** 

Offline warm-up data are mostly concentrated around human-like safe behaviors and thus provide limited coverage of hazardous or unconventional actions. To learn the consequences of risky behaviors, we perform _world-model-guided exploration_ : selected simulator rollouts are fed back to refine the same world model, progressively improving prediction fidelity and risk sensitivity. 

Specifically, to ensure temporal continuity and avoid unrealistic control jitter, we sample horizon- _H_ action sequences (segment-wise) rather than single-step actions (step-wise). The segment-wise sampling allows 

6 

sustained safe or risky behaviors to unfold and reveals their long-term consequences. At each training step, we sample _Ns_ horizon- _H_ candidate action sequences _{_ **A**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>_s_,rolloutfuturestatesˆ</sup><sup>**s**</sup><sup>_n_</sup> _t_ +1: _t_ + _H_<sup>with</sup> the current world model, evaluate their costs _{C_<sup>_n_</sup> _}_ using Eq. (6), and rank candidates by costs. 

**Modes for Interaction.** We define three patterns for our risk-aware sampling strategy to select one candidate from _{_ **A**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>_s_toexecute,asshown</sup> in Fig. 3: 

- `Rand` samples uniformly from all candidates; 

- `Bad` samples from high-cost candidates; 

- `Good` samples from low-cost candidates. 

At the start of segment _r_ , the practical control mode is sampled according to probability: 


where “w.p.” means “with probability”. _ε_ 1 controls broad action-space exploration, and _ε_ 2 controls the fraction of risk-seeking interaction within modelguided sampling. 

**Soft Candidates Selection in Three Modes.** Given sorted candidate actions with costs _{C_<sup>_n_</sup> _}_ , we construct two cost-quantile sets: _N_ `good` as the bottom- _K_ candidates and _N_ `bad` as the top- _K_ candidates. To avoid low-information trajectories, we filter _N_ `bad` by removing degenerate rollouts ( _e.g._ , those caused by unrealistic excessive control jumps), yielding _N_<sup>˜</sup> `bad` . In the `rand` mode, we randomly select the executing action sequence from all candidates. 

In the `good` mode, rather than **deterministically** selecting the minimum-cost candidate, we sample from _N_ `good` using a **soft distribution** to preserve diversity among low-cost plans and mitigate bias from imperfect model predictions: 


where _τg_ is a temperature hyper-parameter that controls the softness of the sampling distributions in the `good` mode, trading off greediness for diversity. This stochastic selection avoids repeatedly executing a single estimated optimum and encourages broader coverage of nominal behaviors. 

In the `bad` mode, instead of always executing the maximum-cost trajectory, we sample from high-cost 


**Figure 4 Self-Evaluation Distillation for Policy Learning.** A cVAE is trained with RaWMPC-scored actions in a contrastive manner, pulling the condition prior toward positives and pushing it away from negatives. The welltrained decoder serves as the test-time action proposer. 

candidates to deliberately expose the model to a spectrum of risky outcomes that are under-represented in safe logs: 


where _τb_ is a temperature hyper-parameter. Compared to argmax selection, this soft sampling strategy prevents over-concentration on extreme or degenerate failures while still biasing interaction toward high-risk regions. 

In this way, segment-wise interaction and soft costbased sampling bias exploration toward temporally coherent and informative safe and hazardous trajectories, enabling the world model to learn both reasonable dynamics and safety-critical consequences for risk-aware decision making. 

7 

### **3.3 Self-Evaluation Distillation for Policy Learning** 

After risk-aware interactive training, RaWMPC can reliably _score_ candidate action sequences by predicting their long-horizon consequences. To reduce the cost of online optimization at test time, we distill this evaluation capability into a lightweight _action proposal_ network, enabling efficient inference _without expert demonstrations_ . The action proposal network corresponds to the “Guidance” module illustrated in Fig. 1(c), and is used to generate candidate action sequences for predictive control. Our key idea is to use RaWMPC as a self-evaluator to pseudo-label sampled actions and train a generative policy via contrastive learning. 

#### **3.3.1 Action Sampling and Pseudo-labeling** 

Given a state history **s** 1: _t_ (simplified as **s** ), we randomly sample _Ns_ horizon- _H_ action sequences _{_ **A**<sup>_n_</sup> _t_ : _t_ + _H−_ 1<sup>_}N_</sup> _n_ =1<sup>_s_(simplifiedas</sup><sup>_{_</sup><sup>**A**</sup><sup>_n}_)andcompute</sup> their costs _{C_<sup>_n_</sup> _}_ with the pretrained RaWMPC. We then form pseudo labels by ranking costs: the lowestcost sequence is treated as a positive example **A**<sup>+</sup> , and the top- _K_ highest-cost sequences are treated as negatives _{_ **A**<sup>_−_</sup> _j_<sup>_}_</sup> _j_<sup>_K_</sup> =1<sup>.Thisconstructiontransfers</sup> RaWMPC’s knowledge (low-risk / high-quality actions) to the proposal network while avoiding any external supervision. 

#### **3.3.2 Action Proposal Network** 

Following [60, 87], we adopt a conditional VAE (cVAE) with an action encoder _qθ_ ( _z|_ **A** _,_ **s** ), a conditional prior _pγ_ ( _z|_ **s** ), and a decoder _pψ_ ( **A** _|z,_ **s** ). The decoder serves as the proposal policy at inference. 

For the positive action, we obtain a Gaussian posterior _q_<sup>+</sup> = _qθ_ ( _z|_ **A**<sup>+</sup> _,_ **s** ) = _N_ ( _µ_<sup>+</sup> _,_ diag(( _σ_<sup>+</sup> )<sup>2</sup> )) and train the decoder to reconstruct **A**<sup>+</sup> . For each negative action **A**<sup>_−_</sup> _j_<sup>,wecompute</sup><sup>_q_</sup> _j_<sup>_−_=</sup><sup>_qθ_(</sup><sup>_z|_</sup><sup>**A**</sup><sup>_−_</sup> _j_<sup>_,_</sup><sup>**s**)=</sup> _N_ ( _µ_<sup>_−_</sup> _j_<sup>_,_diag((</sup><sup>_σ_</sup> _j_<sup>_−_)2)),but</sup><sup>**donot**reconstructnega-</sup> tives to prevent the generator from imitating unsafe behaviors. The conditional prior is _p_<sup>_c_</sup> = _pγ_ ( _z|_ **s** ) = _N_ ( _µ_<sup>_c_</sup> _,_ diag(( _σ_<sup>_c_</sup> )<sup>2</sup> )). 

#### **3.3.3 Contrastive Training Objective** 

To address the lack of expert supervision in policy learning, we use an InfoNCE objective to make the conditional prior predictive of high-quality actions. Concretely, there are two potential contrastive formulations: 

- Using _p_<sup>_c_</sup> as the anchor, pulling _p_<sup>_c_</sup> toward _q_<sup>+</sup> while pushing it away from _{q_<sup>_−_</sup> _}_<sup>_K_</sup> _j_ =1<sup>.</sup> 

- Using _q_<sup>+</sup> as the anchor, pulling _q_<sup>+</sup> toward _p_<sup>_c_</sup> while pushing it away from _{q_<sup>_−_</sup> _}_<sup>_K_</sup> _j_ =1<sup>.</sup> 

We empirically found that the former often produces under-optimized trajectories. One possible reason is that negative samples are far more numerous and broadly cover the latent space, therefore _p_<sup>_c_</sup> is easily driven to a region that is far from most negatives yet not sufficiently close to the positive. In contrast, the latter explicitly pulls _p_<sup>_c_</sup> toward the statistical center of the positive posterior and, via _q_<sup>+</sup> , indirectly separates it from the negatives, leading to more stable learning and higher-quality trajectories. Therefore, we adopt the latter design choice to define our InfoNCE objective as: 


where _D_ ( _·, ·_ ) is the Wasserstein-2 distance between Gaussians and _τ_ is a temperature. 

#### **3.3.4 Overall Loss of Action Proposal Network** 

The total loss of our cVAE combines reconstruction, KL regularization, and contrastive loss: 


This self-evaluation distillation trains a fast proposal policy that generates candidate action sequences consistent with RaWMPC’s evaluations, eliminating the need for expert demonstrations during policy learning. 

## **4 Experiments** 

In this section, we present a comprehensive performance comparison between the proposed framework and state-of-the-art methods. We also conduct extensive ablation studies to assess the effectiveness of our predictive control approach. 

### **4.1 Benchmarks** 

Following prior works [39, 40, 61], we evaluate RaWMPC on two widely used benchmarks: **Bench2Drive** [29] and **NAVSIM** [11]. They are complementary: Bench2Drive provides fully interactive 

8 

**Table 1** Comparison with SOTA approaches on the closed-loop Bench2Drive benchmark on CARLA simulator. _↑_ means the higher the better. DS is taken as the primary metric in comparison and we rank all the methods accordingly, with bold indicating best performance. 

|**Method**|**Venue**|**Scheme**|**DS**_↑_|**SR(%)**_↑_|**Efficiency**_↑_|**Comfortness**_↑_|
|---|---|---|---|---|---|---|
|VAD [31]|ICCV 2023|IL|42.35|15.00|157.94|46.01|
|SparseDrive [69]<br>|ICRA 2025|IL|44.54|16.71|170.21|48.63|
|GenAD [99]|ECCV 2024|IL|44.81|15.90|-|-|
|UniAD [25]|CVPR 2023|IL|45.81|16.36|129.21|43.58|
|MomAD [68]|CVPR 2025|IL|47.91|18.11|174.91|51.20|
|UAD [16]|T-PAMI 2025|IL|49.22|20.45|189.53|**52.71**|
|BridgeAD [89]|CVPR 2025|IL|50.06|22.73|-|-|
|TCP [81]|NeurIPS 2022|IL|59.90|30.00|76.54|18.08|
|WoTE [39]|ICCV 2025|IL|61.71|31.36|-|-|
|DriveDPO [61]|NeurIPS 2025|IL & RL|62.02|30.62|166.80|26.79|
|ThinkTwice [28]|CVPR 2023|IL|62.44|31.23|69.33|16.22|
|DriveTransformer [30]|ICLR 2025|IL|63.46|35.01|100.64|20.78|
|DriveAdapter [27]|ICCV 2023|IL|64.22|33.08|70.22|16.01|
|Raw2Drive [85]|NeurIPS 2025|RL|71.36|50.24|214.17|22.42|
|Hydra-NeXt [40]|ICCV 2025|IL|73.86|50.00|197.76|20.68|
|HiP-AD [73]|ICCV 2025|IL|86.77|69.09|203.12|19.36|
|**RaWMPC w/o Warm-up**|-|PC|87.34|69.62|203.25|30.95|
|**RaWMPC**|-|PC|**88.31**|**70.48**|206.85|32.65|
|**Pretrained VLM-based Approach**|||||||
|ReAL-AD [44]|ICCV 2025|IL|41.17|11.36|-|-|
|Dual-AEB [94]|ICRA 2025|IL|45.23|10.00|-|-|
|ETA [21]|ICCV 2025|IL|74.33|48.33|186.04|25.77|
|VLR-Drive [35]|ICCV 2025|IL|75.01|50.00|122.52|0.59|
|ORION [14]|ICCV 2025|IL|77.74|54.62|151.48|17.38|
|SimLingo [57]|CVPR 2025|IL|85.94|66.82|**244.18**|30.76|


closed-loop evaluation in CARLA [12] with dense annotations, while NAVSIM evaluates large-scale real-world planning via a data-driven, non-reactive simulation-based short-horizon rollout with safetyand progress-aware metrics. 

**Bench2Drive.** Bench2Drive is a CARLA Leadboard v2 closed-loop benchmark for multi-ability stress testing under complex interactions (e.g., cut-ins, overtakes, detours, emergency braking, and give-way). Its official dataset contains _∼_ 2M fully annotated frames from short clips spanning 44 scenarios, 23 weather conditions, and 12 towns; the commonly used _Base_ training set contains 1K clips. Closed-loop evaluation is performed on 220 short routes (each focused on a single scenario), enabling stable and fine-grained comparison. We report four official metrics: _Driving Score (DS)_ , _Success Rate (SR)_ , _Efficiency_ , and _Comfortness_ . _DS_ is the primary aggregate score with penalties for safety and rule violations; _SR_ measures successful completion; _Efficiency_ reflects progress; and _Comfortness_ captures motion smoothness. 

ning on large-scale real-world data built on OpenScene (a planning-oriented reprocessing of nuPlan logs). The task predicts a 4-second future ego trajectory (typically 8 waypoints) given a short history (e.g., 1.5 seconds) of observations. Following prior works [39, 61], we use the official splits: Navtrain ( _∼_ 103K samples) and Navtest ( _∼_ 12K samples). We report NAVSIM metrics including _NC_ , _DAC_ , _EP_ , _TTC_ , _C_ , and the primary score _PDMS_ , where PDMS = NC _·_ DAC _·_ (5EP + 5TTC + 2C) _/_ 12. These metrics jointly capture safety, compliance, progress, and motion quality. All results are computed with the official toolkits and recommended splits. 

Our experiments combine offline warm-up with online simulator interaction, leveraging RaWMPC to learn predictive dynamics and risk-aware decision making. We adopt Bench2Drive for interactive closed-loop evaluation and NAVSIM for large-scale real-world generalization. We further conduct ablations to analyze key training components and strategies. 

**NAVSIM.** NAVSIM benchmarks sensor-based plan- 

9 

**Table 2** Comparison with the SOTA approaches on NAVSIM test set. _↑_ means the higher the better. PDMS is taken as the primary metric in comparison and we rank all the methods accordingly, with bold indicating best performance. 

|**Method**|**Venue**|**Scheme**|**NC**_↑_|**DAC**_↑_|**EP**_↑_|**TTC**_↑_|**C**_↑_|**PDMS**_↑_|
|---|---|---|---|---|---|---|---|---|
|Human|-|-|100|100|87.5|100|99.9|94.8|
|DrivingGPT [8]|ICCV 2025|IL|98.9|90.7|79.7|94.9|100.0|82.4|
|UniAD [25]|CVPR 2023|IL|97.8|91.9|78.8|92.9|100.0|83.4|
|Latent TransFuser [10]|T-PAMI 2023|IL|97.4|92.8|79.0|92.4|100.0|83.8|
|PARA-Drive [80]|CVPR 2024|IL|97.9|92.4|79.3|93.0|99.8|84.0|
|TransFuser [10]|T-PAMI 2023|IL|97.7|92.7|79.8|92.7|100.0|84.5|
|LAW [38]|ICLR 2025|IL|96.4|95.4|81.7|88.7|99.9|84.6|
|World4Drive [100]|ICCV 2025|IL|97.4|94.3|79.9|92.8|100.0|85.1|
|DiffusionDrive [42]|CVPR 2025|IL|98.2|96.2|**88.2**|94.7|100.0|88.1|
|WoTE [39]|ICCV 2025|IL|98.5|96.8|81.9|94.9|99.9|88.3|
|Hydra-NeXt [40]|ICCV 2025|IL|98.1|97.7|81.8|94.6|100.0|88.6|
|UAD [16]|T-PAMI 2025|IL|**99.5**|96.9|78.8|**97.5**|100.0|89.3|
|DriveDPO [61]|NeurIPS 2025|IL & RL|98.5|98.1|84.3|94.8|99.9|90.0|
|GoalFlow [82]|CVPR 2025|IL|98.4|**98.3**|85.0|94.6|100.0|90.3|
|**RaWMPC w/o Warm-up**|-|PC|98.3|98.2|85.3|94.5|99.9|90.5|
|**RaWMPC**|-|PC|98.9|**98.3**|86.1|95.6|99.9|**91.3**|


### **4.2 Implementation Details** 

**Network architecture.** We employ a pretrained ViT [66] as the vision encoder and use the SegViT segmentation head [88] as the segmentation decoder. BEV features are extracted from multi-view images using the query-based view transformer [41]. Following previous works [10, 39], the input image resolution is 1024 _×_ 256, and the BEV feature map resolution is 256 _×_ 256. We use down-sampling factors of 32 (front-view) and 16 (BEV), resulting in 512 visual tokens **i** _t_ (256 per branch). Measurement inputs are encoded through an MLP-based encoder into 4 measurement tokens **m** _t_ , and driving actions, represented as three scalar values (steer, throttle, brake), are transformed into 3 action tokens **a** _t_ via a linear layer. We implement the world model as a transformer with 4 layers and 8 attention heads. RaWMPC predicts _H_ =10 future steps conditioned on the past 5 observed steps, and evaluates _N_ =10 candidate action sequences proposed by the distilled action proposal network (described in Section 3.3) using the cost in Eq. (6) during inference. During action selection, we use _ηk_ = max(2<sup>_−k_+1</sup> _,_ 1 _/_ 8) to downweight distant predictions, and set the event severity weights to _λj_ = 10 _,_ 15 _,_ 30 for off-lane driving, traffic-sign violations, and collisions, respectively. 

**Training.** RaWMPC is trained with the two-stage risk-aware interactive training strategy described in Section 3.2. We first perform an offline warm-up using 

10% of the training data (100 clips for Bench2Drive and 10K samples for NAVSIM), and then refine the model via online interaction using the proposed riskaware training scheme. The random-sampling probability _ε_ 1 is linearly annealed from 1 to 0, while the risksampling probability _ε_ 2 is linearly increased from 0 to 0.3. We maintain a replay buffer of size 10K frames to store recent interaction data (e.g., RGB images, semantic segmentation, ego measurements, and trafficevent annotations). We use segment-wise sampling of horizon- _H_ =10 action sequences to ensure temporal continuity. In good/bad modes, we rank the _Ns_ =50 candidates by cost and sample from the bottom/top- _K_ =5 sets using temperatures _τg_ = 0 _._ 5 and _τb_ = 1 _._ 0. An episode terminates when any of the following conditions is met: (1) the ego vehicle incurs 3 collisions, (2) the ego vehicle goes off-road or remains stuck for 100 consecutive steps, or (3) the ego vehicle successfully completes the route. Across offline warm-up and online interaction, we train RaWMPC using a total of 1K clips on Bench2Drive and 100K samples on NAVSIM (comparable in scale to the official training sets for fair comparison), on four NVIDIA A100 GPUs. We use Adam [33] with an initial learning rate of 10<sup>_−_4</sup> decayed to 10<sup>_−_5</sup> , and a batch size of 16. 

**Self-evaluation distillation.** For self-evaluation distillation (Section 3.3), the action proposal network is implemented as a cVAE [67] with a 32-dimensional latent space. During contrastive training, we sample _Ns_ =50 action sequences, treat the minimum-cost 

10 

sequence as the positive example **A**<sup>+</sup> , and use the top- _K_ =5 highest-cost sequences as negatives. We optimize the proposal network with the objective in Section 3.3, using temperature _τ_ =0 _._ 3, a KL weight schedule _β_ : 0 _→_ 0 _._ 1, and a contrastive weight _λ_ =0 _._ 1. At inference, we sample _N_ =10 candidates from the cVAE decoder and select the final action by minimizing the predicted cost (Eq. (6)) under the worldmodel rollout. 

### **4.3 Comparison with the State-of-theArt** 

In this section, we compare RaWMPC with state-ofthe-art end-to-end driving methods on the closed-loop Bench2Drive benchmark in CARLA and the NAVSIM test set. To reflect our main claim, we report two training settings: (i) **w/o warm-up** , where RaWMPC is trained without using any offline logged video, and (ii) the **full** setting, where a small set of logged driving trajectories is used as an optional warm start. The warm start empirically accelerates convergence and further improves final performance, while RaWMPC already surpasses prior state-of-the-art even without it. 

#### **4.3.1 Evaluation on Bench2Drive** 

Table 1 illustrates the closed-loop results on Bench2Drive. RaWMPC achieves the best overall performance among all compared methods, reaching **88.31** DS and **70.48** % SR in the full setting. More importantly, even **without warm-up** (i.e., without logged trajectories), RaWMPC still attains <u>87.34</u> DS and 69.62% SR, surpassing strong recent baselines such as HiP-AD [73] (86.77 DS / 69.09% SR) and the pretrained-VLM method SimLingo [57] (85.94 DS / 66.82% SR). In addition, RaWMPC maintains competitive efficiency and achieves higher comfortness than most high-performing closed-loop agents, indicating that the gains are not obtained by aggressive maneuvers but by more reliable decision-making. 

#### **4.3.2 Evaluation on NAVSIM** 

Table 2 summarizes the results on NAVSIM. RaWMPC achieves the highest **PDMS of 91.3** among all learning-based methods. Without warm-up, RaWMPC still reaches <u>90.5</u> PDMS, already outperforming previous best methods (e.g., GoalFlow [82]: 90.3). The warm start further improves PDMS (90.5 _→_ 91.3), consistent with the observation that a small amount of logged trajectories can accelerate convergence and improve performance, while not being required to achieve state-of-the-art results. 

#### **4.3.3 Generalization under weather-induced domain shift** 

To evaluate robustness beyond the training distribution, we conduct a weather-shift study where all methods are evaluated exclusively on _Rainy_ scenarios while being trained on either _Sunny only_ or _Sunny & Rainy_ data (Table 3). A key observation is that imitationbased methods are sensitive to training-domain coverage: when rainy conditions are absent from training (Sunny-only), their performance drops notably, reflecting limited transfer to previously unseen environments. In contrast, RaWMPC achieves the best DS and SR under both training regimes, and notably still significantly outperforms strong IL baselines (LAW, WoTE) and SimLingo when trained on _Sunny only_ ( _i.e._ , facing an unseen rainy target domain). Moreover, compared with SimLingo, RaWMPC exhibits substantially smaller degradation when rainy data is removed from training, indicating stronger robustness to previously unseen conditions. 

Figure 5 shows a qualitative example of this _Sunnyonly → Rainy_ shift. LAW fails to recognize the lead vehicle under the altered visual conditions and results in a high-severity frontal collision. WoTE and SimLingo attempt evasive maneuvers that reduce the impact _relative to a direct frontal crash_ , yet the scene still ends in a side-swipe/rear collision. A plausible explanation is that the rainy shift degrades the reliability of the perception–decision stack, while the downstream policy does not explicitly optimize for minimum-risk clearance under uncertainty, yielding insufficient safety margins during close-proximity avoidance (e.g., inaccurate motion anticipation or mismatched ego response on wet roads). By contrast, RaWMPC explicitly evaluates the predicted consequences of candidate action sequences with a risk-aware world model and selects the minimum-risk predictive-control behavior, maintaining safe clearance under uncertainty. 

We attribute this advantage to RaWMPC’s riskaware predictive-control formulation: instead of reproducing expert actions, RaWMPC learns _riskawareness from interaction_ and selects actions by minimizing predicted risk via the learned world model. Such an objective encourages transferable decision principles (e.g., maintaining safe margins and acting conservatively under uncertainty) that remain effective when appearance and dynamics change across domains. Thus, RaWMPC is less dependent on exhaustive expert action coverage for corner cases, which better matches the long-tail nature of real-world deployment where unseen scenarios are inevitable. 

11 


**Figure 5 Qualitative comparison under weather-induced domain shift (Sunny-only** _→_ **Rainy).** All methods are trained on _Sunny-only_ data and evaluated in _Rainy_ conditions. LAW [38] misses the lead vehicle, causing a severe frontal collision. WoTE [39] and SimLingo [57] reduce severity by evasive maneuvers but still collide due to degraded perception–decision reliability and weak safety-margin enforcement. RaWMPC avoids collisions by selecting the minimum-risk predictive-control action under uncertainty. 

**Table 3** Performance comparison under domain shift. All methods are trained on either _Sunny only_ or _Sunny & Rainy_ data, and evaluated exclusively on _Rainy_ scenarios. _↑_ indicates higher is better. 

|**Method**|**Venue**|**Scheme**|**Training Data**|**Tested**<br>**DS**_↑_|**on Rainy**<br>**SR(%)**_↑_|
|---|---|---|---|---|---|
|LAW|ICLR 2025|IL|Sunny & Rainy<br>Sunny only|34.54<br>23.58|7.09<br>3.56|
|WoTE|ICCV 2025|IL|Sunny & Rainy<br>Sunny only|36.54<br>28.65|7.85<br>5.21|
|SimLingo (Pretrained-VLM)|CVPR 2025|IL|Sunny & Rainy<br>Sunny only|51.69<br>33.49|13.68<br>8.97|
|**RWMPC**||PC|Sunny & Rainy|**53.67**|**14.96**|
|**a**|–||Sunny only|**41.36**|**10.83**|


#### **4.3.4 Qualitative visualization of predictive control** 

We provide some visualization results of the predictive control procedure of RaWMPC in Fig. 6. Given RGB observations and high-level navigation commands (e.g., keep going straight or merge left), our generative policy proposes a small set of candidate action sequences (e.g., keep going straight, detour, brake, and lane change). For each candidate, the riskaware world model predicts the near-future semantic traffic state and the decoding module evaluates its consequence from both task progress and safety perspectives, including collision risk, off-lane/sidewalk intrusion risk, and progress-related penalties such as getting stuck in traffic. The final action is selected by comparing these predicted consequences and choosing the minimum-cost one under the navigation goal. 

In the **first** case, going straight collides with a crossing 

pedestrian, while detours either collide with an oncoming vehicle or drive onto the sidewalk; RaWMPC chooses _slow down, straight briefly, then stop_ to safely stop in front of the pedestrian (instead of an overly conservative early brake). In the **second** case, going straight or merging left immediately causes a collision, steering right hits a parked vehicle, and stopping leads to a deadlock; thus RaWMPC selects _pause briefly, then merge left_ for a collision-free merge. These cases demonstrate that RaWMPC can proactively avoid risky behaviors by explicitly forecasting and comparing action consequences, rather than merely following a single command or relying on a fixed fallback maneuver. 

### **4.4 Ablation Study** 

In this section, we provide comprehensive ablation studies of the proposed approach using the 

12 


**Figure 6 Visualization of the predictive control procedure** . At time _t_ , we show the front-view and the BEV images (with segmentation). Dashed curves indicate candidate actions and highlighted agents denote key risks. Rollouts from _t_ + 1 to _t_ + 5 illustrate predicted consequences, and the bottom panel reports each action’s outcomes and costs ( _e.g._ , collision, sidewalk intrusion, stopping distance). **Scenario 1** : RaWMPC slows down, proceeds briefly, then stops for the pedestrian. **Scenario 2** : RaWMPC waits briefly, then turns left to avoid both the front-left vehicle and the parked car. 

Bench2Drive dataset. 

#### **4.4.1 Analysis of Framework** 

Table 4 analyzes core components aligned with our model design (Sec. 3.1.1). _w/o Semantic Guidance_ removes semantic-guided event decoding, _i.e._ , the fusion of semantic attention from the segmentation decoder into the event decoder. This leads to a clear drop (DS 88.31 _→_ 82.36, SR 70.48% _→_ 62.69%), showing that accurate safety-event prediction is crucial for risk-aware cost evaluation. _w/o Segmentation_ 

**Table 4** Ablation study on the proposed framework. 

|**Method**|**Met**<br>**DS**_↑_|**rics**<br>**SR(%)**_↑_|
|---|---|---|
|Entire RaWMPC (**Ours**)|**88.31**|**70.48**|
|w/o Semantic Guidance|82.36 -5.95|62.69 -7.79|
|w/o Segmentation Decoder|70.85 -17.46|48.95 -21.53|
|w/o Action Selection|61.35 -26.96|30.98 -39.50|


_Decoder_ further removes the segmentation decoding branch and its supervision, resulting in a large degra- 

13 

**Table 5** Ablation study on the risk-aware training. 

**Table 7** Results obtained using different amounts of prediction horizon. 

||**Me**|**trics**||||
|---|---|---|---|---|---|
|**Method**|**DS**_↑_|**SR(%)**_↑_|**Prediction Horizon**|**Met**|**rics**|
|Risk-aware Sampling (**Ours**)|**88.31**|**70.48**||**DS**_↑_|**SR(%)**_↑_|
|_ϵ_-Greedy Sampling<br>Random Sampling|83.86 -4.45<br>70.41 -17.90|61.74 -8.74<br>46.82 -23.66|H=1<br>H=5|57.85 -30.46<br>74.98 -13.33|28.64 -41.84<br>49.52 -20.96|
||||H=10 (**Ours**)|**88.31**|**70.48**|
|**able 6** Results obtained usin|g different a|ction supervi-|H=15|82.34 -5.97|62.38 -8.10|


**Table 6** Results obtained using different action supervision in policy learning. 

**Table 8** Results obtained using different amounts of offline learning data in warm-up. 

|**Policy Learning Data**|**Met**<br>**DS**_↑_|**rics**<br>**SR(%)**_↑_|
|---|---|---|
|Pos. & Neg. Actions (**Ours**)|**88.31**|**70.48**|
|Expert Actions|86.75 -1.56|68.25 -2.23|
|Only Positive Actions|83.65 -4.66|66.52 -3.96|


|**Warm-up Data**|**DS**_↑_|**Met**|**rics**<br>**SR(%)**_↑_|
|---|---|---|---|
|0%|87.34|-0.97|69.62 -0.86|
|10%|**88.31**||**70.48**|
|20%|88.09|-0.22|70.32 -0.16|
|30%|86.95|-1.36|68.52 -1.96|


dation (DS 70.85 / SR 48.95%), which indicates that forecasting high-level semantics is essential for reliable long-horizon rollouts. _w/o Action Selection_ disables predictive control in Eq. (1) (bypassing costbased ranking in Eq. (6)) and directly executes the proposal/guidance output, causing the most severe collapse (DS 61.35 / SR 30.98%). This confirms that selecting actions by explicitly evaluating predicted long-horizon consequences is the key to RaWMPC. 

performance (DS 88.31 / SR 70.48%). Training the proposal network only with _expert actions_ slightly degrades performance (DS 86.75 / SR 68.25%), suggesting that self-evaluated targets align better with the predictive-control objective than direct imitation targets. Using _only positive actions_ further drops performance (DS 83.65 / SR 66.52%), indicating that explicitly contrasting against high-risk negatives is important for preventing unsafe candidates and improving downstream selection. 

#### **4.4.2 Analysis of Risk-Aware Training** 

Table 5 evaluates the risk-aware interaction training strategy used to refine the world model. Our _riskaware sampling_ follows the design in Sec. 3.2: besides random exploration, it uses the current RaWMPC to score candidate action sequences and deliberately collects both **good** (low-cost) and **bad** (high-cost) rollouts, improving coverage of rare safety-critical outcomes. Replacing it with _ϵ-greedy sampling_ (random with probability _ϵ_ 1, otherwise only selecting low-cost rollouts) reduces performance (DS 83.86 / SR 61.74%), showing that excluding high-cost failures weakens learning of risky consequences. Pure _random sampling_ further degrades results (DS 70.41 / SR 46.82%), indicating that unguided data collection is substantially less efficient for learning long-horizon consequences. 

#### **4.4.4 Discussion on Prediction Horizon** 

Table 7 ablates the planning horizon _H_ used in the world-model rollout and cost evaluation (Eq. (6)). Short horizons fail to capture delayed consequences, leading to poor performance (H=1: DS 57.85 / SR 28.64%; H=5: DS 74.98 / SR 49.52%). Increasing to H=10 yields the best results (DS 88.31 / SR 70.48%), as it provides sufficient look-ahead for risk assessment while keeping prediction uncertainty manageable. Further increasing to H=15 degrades performance (DS 82.34 / SR 62.38%), likely due to accumulated rollout errors that affect cost-based ranking. 

#### **4.4.3 Analysis of Self-Evaluation Distillation** 

Table 6 studies how to train the action proposal network in Sec. 3.3. Our default setting uses RaWMPC as a self-evaluator to pseudo-label actions: the lowestcost sequence is treated as a positive, while high-cost sequences serve as negatives, which yields the best 

#### **4.4.5 Discussion on Warm-up** 

Table 8 ablates the fraction of offline logged trajectories used for warm-up before interactive training. In this study, we keep the total number of training samples fixed and vary only the proportion allocated to offline warm-up data. Without warm-up (0%), 

14 

**Table 9** Ablation study on the control pattern with learned world model. 

**Table 10** Prediction accuracy of future traffic events with learned world model. 

|**Method**|**M**|**etrics**||**Co**|**llision**||**Running**|
|---|---|---|---|---|---|---|---|
||**DS**_↑_|**SR(%)**_↑_||**Pedestrian **|**Vehicle **|**Static**|**Traffic Sign**|
|Predictive Control (**Ours**)|**88.31**|**70.48**|Accuracy|0.96|0.91|0.93|0.91|
|Reinforcement Learning|73.58 -14.7|3<br>51.85 -18.63|Recall|0.99|0.84|0.89|0.84|
||||Precision|0.52|0.62|0.63|0.68|


performance drops (DS 87.34 / SR 69.62%), suggesting that training from scratch leads to less reliable rollouts and a less stable early optimization stage. Using a small amount of logged trajectories (10%) yields the best results (DS 88.31 / SR 70.48%), indicating that a light warm-up provides useful predictive priors (e.g., basic dynamics modeling and perception decoding) that improve long-horizon rollout quality and downstream control. However, further increasing the warm-up ratio begins to degrade performance (20%: DS 88.09 / SR 70.32%; 30%: DS 86.95 / SR 68.52%). We attribute this trend to the fact that offline logged trajectories are strongly biased toward safe, human-like behaviors and contain few hazardous events. Consequently, allocating too much data to offline warm-up reduces the opportunities for subsequent online interaction to explore unconventional actions and collect safety-critical failures—especially in dangerous scenarios—which are essential for learning robust risk awareness. 

#### **4.4.6 Discussion on Control Pattern** 

Table 9 compares predictive control to directly optimizing a policy with model-based reinforcement learning (RL). Predictive control achieves substantially higher performance (DS 88.31 / SR 70.48%) than model-based RL (DS 73.58 / SR 51.85%). This validates the benefit of evaluating candidate action sequences via decoded future outcomes (segmentation, events, ego-states) and selecting the minimum-cost one, rather than relying on end-to-end policy optimization alone. 

#### **4.4.7 World-Model Prediction Accuracy** 

Table 10 reports the event prediction quality used by the cost function in Eq. (6). The predictor achieves high accuracy across event types (0.91–0.96) and strong recall on collision-related events (e.g., pedestrian collision recall 0.99), providing reliable signals for risk-aware evaluation. We observe lower precision for some rare events (e.g., pedestrian collision precision 0.52), reflecting a conservative tendency with more false positives; in safety-critical driving, priori- 

tizing recall can be preferable to missing hazards. 

## **5 Conclusion** 

In this work, we proposed **RaWMPC** , a risk-aware world-model predictive control framework for endto-end autonomous driving that _does not require expert action supervision_ . RaWMPC learns an action-conditioned world model to roll out multiple candidate behaviors, predicts future semantics and safety-critical events, and selects actions by explicitly minimizing a risk-aware cost. To make rare-butcatastrophic outcomes predictable and avoidable, we introduced a **risk-aware interaction** strategy that intentionally collects both safe and hazardous rollouts, and we further proposed **self-evaluation distillation** to train an efficient action proposal policy using RaWMPC as a self-evaluator. Extensive experiments on Bench2Drive and NAVSIM show that RaWMPC achieves state-of-the-art performance and stronger robustness under domain shift, even without offline warm-up, showing the potential to significantly reduce the reliance on costly real-world expert demonstrations. For future work, we will explore domain adaptation and more efficient planning to better support real-world deployment and sim-to-real transfer. 

## **Statements and Declarations** 

- Competing interests. The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

- Data availability. This work does not propose any new dataset. The datasets (Bench2Drive [29] and NAVSIM [11]) that support the findings of this study are openly available at the URLs: Bench2Drive and NAVSIM. 

15 

## **References** 

- [1] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [2] Jinkun Cao, Xin Wang, Trevor Darrell, and Fisher Yu. Instance-aware predictive navigation in multiagent environments. In _IEEE International Conference on Robotics and Automation_ , pages 5096–5102, 2021. 

- [3] Wei Cao, Marcel Hallgarten, Tianyu Li, Daniel Dauner, Xunjiang Gu, Caojun Wang, Yakov Miron, Marco Aiello, Hongyang Li, Igor Gilitschenski, et al. Pseudo-simulation for autonomous driving. _arXiv preprint arXiv:2506.04218_ , 2025. 

- [4] Raphael Chekroun, Marin Toromanoff, Sascha Hornauer, and Fabien Moutarde. Gri: General reinforced imitation and its application to vision-based autonomous driving. In _NeurIPS 2021, Machine Learning for Autonomous Driving Workshop_ , 2021. 

- [5] Dian Chen and Philipp Krähenbühl. Learning from all vehicles. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17222–17231, 2022. 

- [6] Dian Chen, Vladlen Koltun, and Philipp Krähenbühl. Learning to drive from a world on rails. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 15590–15599, 2021. 

- [7] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-toend autonomous driving: Challenges and frontiers. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [8] Yuntao Chen, Yuqi Wang, and Zhaoxiang Zhang. Drivinggpt: Unifying driving world modeling and planning with multi-modal autoregressive transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 26890–26900, October 2025. 

- [9] Pranav Singh Chib and Pravendra Singh. Recent advancements in end-to-end autonomous driving using deep learning: A survey. _IEEE Transactions on Intelligent Vehicles_ , 9(1):103–118, 2023. 

- [10] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2022. 

- [11] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. _Advances in Neural Information Processing Systems_ , 37:28706–28719, 2025. 

- [12] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In _Conference on Robot Learning_ , pages 1–16, 2017. 

- [13] Lan Feng, Quanyi Li, Zhenghao Peng, Shuhan Tan, and Bolei Zhou. Trafficgen: Learning to generate diverse and realistic traffic scenarios. In _2023 IEEE international conference on robotics and automation (ICRA)_ , pages 3567–3575. IEEE, 2023. 

- [14] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. _arXiv preprint arXiv:2503.19755_ , 2025. 

- [15] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. 

- [16] Mingzhe Guo, Zhipeng Zhang, Yuan He, Ke Wang, Liping Jing, and Haibin Ling. End-to-end autonomous driving without costly modularization and 3d manual annotation. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [17] David Ha and Jürgen Schmidhuber. Recurrent world models facilitate policy evolution. _Advances in neural information processing systems_ , 31, 2018. 

- [18] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2019. 

- [19] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 

- [20] Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2021. 

- [21] Shadi Hamdan, Chonghao Sima, Zetong Yang, Hongyang Li, and Fatma Güney. Eta: Efficiency through thinking ahead, a dual approach to self-driving with large models. In _Proceedings of_ 

16 

_the IEEE/CVF International Conference on Computer Vision_ , 2025. 

- [22] Mikael Henaff, Alfredo Canziani, and Yann LeCun. Model-predictive policy learning with uncertainty regularization for driving in dense traffic. In _International Conference on Learning Representations_ , 2018. 

- [23] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zachary Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. _Advances in Neural Information Processing Systems_ , 35:20703–20716, 2022. 

- [24] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [25] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- [26] Bernhard Jaeger, Kashyap Chitta, and Andreas Geiger. Hidden biases of end-to-end driving models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8240–8249, 2023. 

- [27] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 7953–7963, 2023. 

- [28] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21983–21994, 2023. 

- [29] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. _arXiv preprint arXiv:2406.03877_ , 2024. 

- [30] Xiaosong Jia, Junqi You, Zhiyuan Zhang, and Junchi Yan. Drivetransformer: Unified transformer for scalable end-to-end autonomous driving. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [31] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8340–8350, 2023. 

- [32] Alex Kendall, Jeffrey Hawke, David Janz, Przemyslaw Mazur, Daniele Reda, John-Mark Allen, VinhDieu Lam, Alex Bewley, and Amar Shah. Learning to drive in a day. In _2019 international conference on robotics and automation (ICRA)_ , pages 8248–8254. IEEE, 2019. 

- [33] Diederik P Kingma. Adam: A method for stochastic optimization. _arXiv preprint arXiv:1412.6980_ , 2014. 

- [34] Jing Yu Koh, Honglak Lee, Yinfei Yang, Jason Baldridge, and Peter Anderson. Pathdreamer: A world model for indoor navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14738–14748, 2021. 

- [35] Fanjie Kong, Yitong Li, Weihuang Chen, Chen Min, Yizhe Li, Zhiqiang Gao, Haoyang Li, Zhongyu Guo, and Hongbin Sun. Vlr-driver: Large vision-language-reasoning models for embodied autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 26966–26976, 2025. 

- [36] Hanyang Kong, Dongze Lian, Michael Bi Mi, and Xinchao Wang. Dreamdrone: Text-to-image diffusion models are zero-shot perpetual view generators. In _European Conference on Computer Vision_ , pages 324–341. Springer, 2024. 

- [37] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2drive: Efficient reinforcement learning by thinking with latent world model for autonomous driving (in carla-v2). In _European Conference on Computer Vision_ , pages 142–158. Springer, 2024. 

- [38] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. Enhancing end-to-end autonomous driving with latent world model. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [39] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 27137–27146, October 2025. 

- [40] Zhenxin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Zuxuan Wu, and Jose M. Alvarez. Hydra-next: Robust closed-loop driving with open-loop training. In _Proceedings of the IEEE/CVF International Con-_ 

17 

_ference on Computer Vision (ICCV)_ , pages 27305– 27314, October 2025. 

- [41] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [42] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, and Xinggang Wang. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 12037–12047, June 2025. 

- [43] Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollár. Focal loss for dense object detection. In _Proceedings of the IEEE international conference on computer vision_ , pages 2980–2988, 2017. 

- [44] Yuhang Lu, Jiadong Tu, Yuexin Ma, and Xinge Zhu. Real-ad: Towards human-like reasoning in end-toend autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 27783–27793, 2025. 

- [45] Ana-Maria Marcu, Long Chen, Jan Hünermann, Alice Karnsund, Benoit Hanotte, Prajwal Chidananda, Saurabh Nair, Vijay Badrinarayanan, Alex Kendall, Jamie Shotton, et al. Lingoqa: Visual question answering for autonomous driving. In _European Conference on Computer Vision_ , pages 252–269. Springer, 2024. 

- [46] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. In _RSS_ , 2023. 

- [47] Fausto Milletari, Nassir Navab, and Seyed-Ahmad Ahmadi. V-net: Fully convolutional neural networks for volumetric medical image segmentation. In _2016 fourth international conference on 3D vision (3DV)_ , pages 565–571. Ieee, 2016. 

- [48] Michael Montemerlo, Jan Becker, Suhrid Bhat, Hendrik Dahlkamp, Dmitri Dolgov, Scott Ettinger, Dirk Haehnel, Tim Hilden, Gabe Hoffmann, Burkhard Huhnke, et al. Junior: The stanford entry in the urban challenge. _Journal of field Robotics_ , 25(9): 569–597, 2008. 

- [49] Chaojun Ni, Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Wenkang Qin, Guan Huang, Chen Liu, Yuyin Chen, Yida Wang, Xueyang Zhang, Yifei Zhan, Kun Zhan, Peng Jia, Xianpeng Lang, Xingang Wang, and Wenjun Mei. Recondreamer: Crafting world models for driving scene recon- 

   - struction via online restoration. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 1559–1569, June 2025. 

- [50] Jingcheng Ni, Yuxin Guo, Yichen Liu, Rui Chen, Lewei Lu, and Zehuan Wu. Maskgwm: A generalizable driving world model with video mask reconstruction. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 22381–22391, June 2025. 

- [51] Brian Paden, Michal Čáp, Sze Zheng Yong, Dmitry Yershov, and Emilio Frazzoli. A survey of motion planning and control techniques for self-driving urban vehicles. _IEEE Transactions on intelligent vehicles_ , 1(1):33–55, 2016. 

- [52] Xinlei Pan, Xiangyu Chen, Qizhi Cai, John Canny, and Fisher Yu. Semantic predictive control for explainable and efficient policy learning. In _International Conference on Robotics and Automation_ , pages 3203–3209, 2019. 

- [53] Scott Drew Pendleton, Hans Andersen, Xinxin Du, Xiaotong Shen, Malika Meghjani, You Hong Eng, Daniela Rus, and Marcelo H Ang. Perception, planning, control, and coordination for autonomous vehicles. _Machines_ , 5(1):6, 2017. 

- [54] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multi-modal fusion transformer for endto-end autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 7077–7087, 2021. 

- [55] Katrin Renz, Kashyap Chitta, Otniel-Bogdan Mercea, A Sophia Koepke, Zeynep Akata, and Andreas Geiger. Plant: Explainable planning transformers via object-level representations. In _Conference on Robot Learning_ , pages 459–470, 2023. 

- [56] Katrin Renz, Long Chen, Ana-Maria Marcu, Jan Hünermann, Benoit Hanotte, Alice Karnsund, Jamie Shotton, Elahe Arani, and Oleg Sinavski. Carllava: Vision language models for camera-only closed-loop driving. _arXiv preprint arXiv:2406.10165_ , 2024. 

- [57] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 11993–12003, June 2025. 

- [58] Nicholas Rhinehart, Rowan McAllister, and Sergey Levine. Deep imitative models for flexible inference, planning, and control. In _International Conference on Learning Representations_ , 2020. 

- [59] Ahmad El Sallab, Mohammed Abdou, Etienne Perot, and Senthil Yogamani. End-to-end deep re- 

18 

inforcement learning for lane keeping assist. _arXiv preprint arXiv:1612.04340_ , 2016. 

- [60] Tim Salzmann, Boris Ivanovic, Punarjay Chakravarty, and Marco Pavone. Trajectron++: Dynamically-feasible trajectory forecasting with heterogeneous data. In _European Conference on Computer Vision_ , pages 683–700. Springer, 2020. 

- [61] ShuYao Shang, Yuntao Chen, Yuqi Wang, Yingyan Li, and Zhaoxiang Zhang. Drivedpo: Policy learning via safety dpo for end-to-end autonomous driving. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [62] Hao Shao, Letian Wang, Ruobing Chen, Hongsheng Li, and Yu Liu. Safety-enhanced autonomous driving using interpretable sensor fusion transformer. In _Conference on Robot Learning_ , pages 726–737, 2023. 

- [63] Hao Shao, Letian Wang, Ruobing Chen, Steven L Waslander, Hongsheng Li, and Yu Liu. Reasonnet: End-to-end driving with temporal and global reasoning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13723–13733, 2023. 

- [64] Hao Shao, Yuxuan Hu, Letian Wang, Guanglu Song, Steven L Waslander, Yu Liu, and Hongsheng Li. Lmdrive: Closed-loop end-to-end driving with large language models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15120–15130, 2024. 

- [65] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Jens Beißwenger, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with graph visual question answering. In _European Conference on Computer Vision_ , pages 256–274. Springer, 2024. 

- [66] Oriane Siméoni, Huy V Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, et al. Dinov3. _arXiv preprint arXiv:2508.10104_ , 2025. 

- [67] Kihyuk Sohn, Honglak Lee, and Xinchen Yan. Learning structured output representation using deep conditional generative models. _Advances in neural information processing systems_ , 28, 2015. 

- [68] Ziying Song, Caiyan Jia, Lin Liu, Hongyu Pan, Yongchang Zhang, Junming Wang, Xingyu Zhang, Shaoqing Xu, Lei Yang, and Yadan Luo. Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22432–22441, 2025. 

- [69] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. Sparsedrive: 

End-to-end autonomous driving via sparse scene representation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8795–8801. IEEE, 2025. 

- [70] Shuhan Tan, Kelvin Wong, Shenlong Wang, Sivabalan Manivasagam, Mengye Ren, and Raquel Urtasun. Scenegen: Learning to generate realistic traffic scenes. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 892–901, 2021. 

- [71] Shuhan Tan, Boris Ivanovic, Xinshuo Weng, Marco Pavone, and Philipp Kraehenbuehl. Language conditioned traffic generation. In _Conference on Robot Learning_ , pages 2714–2752. PMLR, 2023. 

- [72] Shuhan Tan, Boris Ivanovic, Yuxiao Chen, Boyi Li, Xinshuo Weng, Yulong Cao, Philipp Kraehenbuehl, and Marco Pavone. Promptable closed-loop traffic simulation. In _Annual Conference on Robot Learning_ , 2024. 

- [73] Yingqi Tang, Zhuoran Xu, Zhaotie Meng, and Erkang Cheng. Hip-ad: Hierarchical and multigranularity planning with deformable attention for autonomous driving in a single decoder. _arXiv preprint arXiv:2503.08612_ , 2025. 

- [74] Sebastian Thrun, Mike Montemerlo, Hendrik Dahlkamp, David Stavens, Andrei Aron, James Diebel, Philip Fong, John Gale, Morgan Halpenny, Gabriel Hoffmann, et al. Stanley: The robot that won the darpa grand challenge. _Journal of field Robotics_ , 23(9):661–692, 2006. 

- [75] Marin Toromanoff, Emilie Wirbel, and Fabien Moutarde. End-to-end model-free reinforcement learning for urban driving using implicit affordances. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 7153–7162, 2020. 

- [76] Chris Urmson, Joshua Anhalt, Drew Bagnell, Christopher Baker, Robert Bittner, MN Clark, John Dolan, Dave Duggins, Tugrul Galatali, Chris Geyer, et al. Autonomous driving in urban environments: Boss and the urban challenge. _Journal of field Robotics_ , 25(8):425–466, 2008. 

- [77] Hanqing Wang, Wei Liang, Luc Van Gool, and Wenguan Wang. Dreamwalker: Mental planning for continuous vision-language navigation. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 10873–10883, 2023. 

- [78] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer_ 

19 

_Vision and Pattern Recognition_ , pages 14749–14759, 2024. 

- [79] Kehan Wen, Yutong Hu, Yao Mu, and Lei Ke. Mˆ 3pc: Test-time model predictive control using pretrained masked trajectory model. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [80] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for real-time autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [81] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. _Advances in Neural Information Processing Systems_ , 35:6119–6132, 2022. 

- [82] Zebin Xing, Xingyu Zhang, Yang Hu, Bo Jiang, Tong He, Qian Zhang, Xiaoxiao Long, and Wei Yin. Goalflow: Goal-driven flow matching for multimodal trajectories generation in end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1602–1611, 2025. 

- [83] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-toend autonomous driving via large language model. _IEEE Robotics and Automation Letters_ , 2024. 

- [84] Xuemeng Yang, Licheng Wen, Tiantian Wei, Yukai Ma, Jianbiao Mei, Xin Li, Wenjie Lei, Daocheng Fu, Pinlong Cai, Min Dou, Liang He, Yong Liu, Botian Shi, and Yu Qiao. Drivearena: A closedloop generative simulation platform for autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 26933–26943, October 2025. 

- [85] Zhenjie Yang, Xiaosong Jia, Qifeng Li, Xue Yang, Maoqing Yao, and Junchi Yan. Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2), 2025. Accepted by NeurIPS 2025. 

- [86] Jianhao Yuan, Shuyang Sun, Daniel Omeiza, Bo Zhao, Paul Newman, Lars Kunze, and Matthew Gadd. Rag-driver: Generalisable driving explanations with retrieval-augmented in-context learning in multi-modal large language model. _arXiv preprint arXiv:2402.10828_ , 2024. 

- [87] Ye Yuan, Xinshuo Weng, Yanglan Ou, and Kris M Kitani. Agentformer: Agent-aware transformers for socio-temporal multi-agent forecasting. In _Proceed-_ 

_ings of the IEEE/CVF international conference on computer vision_ , pages 9813–9823, 2021. 

- [88] Bowen Zhang, Zhi Tian, Quan Tang, Xiangxiang Chu, Xiaolin Wei, Chunhua Shen, et al. Segvit: Semantic segmentation with plain vision transformers. In _Advances in Neural Information Processing Systems_ , 2022. 

- [89] Bozhou Zhang, Nan Song, Xin Jin, and Li Zhang. Bridging past and future: End-to-end autonomous driving with historical prediction and planning. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 6854–6863, 2025. 

- [90] Jimuyang Zhang, Zanming Huang, and Eshed OhnBar. Coaching a teachable student. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 7805–7815, 2023. 

- [91] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, Xun Cao, and Wei Yin. Epona: Autoregressive diffusion world model for autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 27220–27230, October 2025. 

- [92] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion. In _ICLR_ , 2024. 

- [93] Peizhi Zhang, Lu Xiong, Zhuoping Yu, Peiyuan Fang, Senwei Yan, Jie Yao, and Yi Zhou. Reinforcement learning-based end-to-end parking for automatic parking system. _Sensors_ , 19(18):3996, 2019. 

- [94] Wei Zhang, Pengfei Li, Junli Wang, Bingchuan Sun, Qihao Jin, Guangjun Bao, Shibo Rui, Yang Yu, Wenchao Ding, Peng Li, et al. Dual-aeb: Synergizing rule-based and multimodal large language models for effective emergency braking. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 14888–14895. IEEE, 2025. 

- [95] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. End-to-end urban driving by imitating a reinforcement learning coach. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 15222–15232, 2021. 

- [96] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. Trafficbots: Towards world models for autonomous driving simulation and motion prediction. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1522–1529. IEEE, 2023. 

20 

- [97] Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Xueyang Zhang, Yida Wang, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, Wenjun Mei, and Xingang Wang. Drivedreamer4d: World models are effective data machines for 4d driving scene representation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 12015–12026, June 2025. 

- [98] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In _European conference on computer vision_ , pages 55–72. Springer, 2024. 

- [99] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. In _European Conference on Computer Vision_ , pages 87–104. Springer, 2024. 

- [100] Yupeng Zheng, Pengxuan Yang, Zebin Xing, Qichao Zhang, Yuhang Zheng, Yinfeng Gao, Pengfei Li, Teng Zhang, Zhongpu Xia, Peng Jia, XianPeng Lang, and Dongbin Zhao. World4drive: End-toend autonomous driving via intention-aware physical latent world model. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 28632–28642, October 2025. 

- [101] Julius Ziegler, Philipp Bender, Markus Schreiber, Henning Lategahn, Tobias Strauss, Christoph Stiller, Thao Dang, Uwe Franke, Nils Appenrodt, Christoph G Keller, et al. Making bertha drive—an autonomous journey on a historic route. _IEEE Intelligent transportation systems magazine_ , 6(2): 8–20, 2014. 

- [102] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Gaussianworld: Gaussian world model for streaming 3d occupancy prediction. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 6772–6781, June 2025. 

21 

