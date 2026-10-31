---
title: "Empowering Multi-Robot Cooperation via Sequential World Models"
date: "2025-09-16"
authors: "Zijie Zhao; Honglei Guo; Shengqian Chen; Kaixuan Xu; Bo Jiang; Yuanheng Zhu"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2509.13095
pdf: https://arxiv.org/pdf/2509.13095
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.13095)** / [論文ページ](https://arxiv.org/abs/2509.13095)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# EMPOWERING MULTI-ROBOT COOPERATION VIA SEQUENTIAL WORLD MODELS 

**Zijie Zhao**<sup>1</sup><sup>_,_2</sup> **, Honglei Guo**<sup>2</sup> **, Shengqian Chen**<sup>2</sup> **, Kaixuan Xu**<sup>1</sup><sup>_,_2</sup> **, Bo Jiang**<sup>2</sup><sup>_,_1</sup> **, Yuanheng Zhu**<sup>2</sup><sup>_,_1</sup><sup>_,∗_</sup> , **Dongbin Zhao**<sup>2</sup><sup>_,_1</sup> 

1School of Artificial Intelligence, University of Chinese Academy of Sciences 

2SKL-MAIS, Institute of Automation, Chinese Academy of Sciences 

## ABSTRACT 

Model-based reinforcement learning (MBRL) has achieved remarkable success in robotics due to its high sample efficiency and planning capability. However, extending MBRL to physical multi-robot cooperation remains challenging due to the complexity of joint dynamics. To address this challenge, we propose the **Seq** uential **W** orld **M** odel (SeqWM), a novel framework that integrates the sequential paradigm into multi-robot MBRL. SeqWM employs independent, autoregressive agent-wise world models to represent joint dynamics, where each agent generates its future trajectory and plans its actions based on the predictions of its predecessors. This design lowers modeling complexity and enables the emergence of advanced cooperative behaviors through explicit intention sharing. Experiments on Bi-DexHands and Multi-Quadruped demonstrate that SeqWM outperforms existing state-of-theart model-based and model-free baselines in both overall performance and sample efficiency, while exhibiting advanced cooperative behaviors such as predictive adaptation, temporal alignment, and role division. Furthermore, SeqWM has been successfully deployed on physical quadruped robots, validating its effectiveness in real-world multi-robot systems. Demos and code are available at: SeqWM. 

## 1 INTRODUCTION 

Model-based reinforcement learning (MBRL) has been widely applied to robotic systems due to its high sample efficiency (Jiang et al., 2025) and planning capability (Sun et al., 2023). However, extending MBRL to multi-robot cooperation remains challenging (Chai et al., 2025). Early decentralized approaches built independent world models for each agent (Egorov & Shpilman, 2022), overlooking coupling between agents and hindering coordination. More recent centralized methods, by contrast, assume full observability (Liu et al., 2024b), performing dynamics modeling (Zhao 


et al., 2025a) and policy optimization (Zhang et al., 2025a) in the joint space. These methods face challenges related to modeling complexity in robotic systems with high-dimensional observation and action spaces, limiting their deployment in real-world scenarios. 

Between centralized and decentralized paradigms, the distributed sequential paradigm has rapidly developed in recent years and demonstrated unique advantages (Khan, 2025). It reformulates multiagent decision-making as an autoregressive process: agents communicate and act in a certain order, with each updating its policy conditioned on messages and actions from predecessors (Wen et al., 

> _∗Corresponding authors_ . This work was supported in part by National Natural Science Foundation of China under Grants 62136008, 62293541, and in part by Beijing Nova Program under Grant 20240484514. 

1 

Published as a conference paper at ICLR 2026 

2022; Hu et al., 2025). This design enables more consistent joint reasoning (Ding et al., 2024) and finer-grained credit assignment (Kuba et al., 2022) without relying on full communication. From a real-world deployment perspective, it reduces the reliance on communication synchronization and offers improved robustness against packet loss or disturbances (Ding et al., 2024). 

Motivated by these advantages, as shown in Figure 1, we propose the **Seq** uential **W** orld **M** odel (SeqWM), which integrates the sequential paradigm into MBRL to structurally decompose dynamics modeling and action planning. For trajectory prediction, SeqWM represents the joint dynamics as sequential agent-wise rollouts, where each agent maintains an independent world model and conditions on the predicted trajectories and actions of its predecessors. For action planning, each agent performs multi-step lookahead conditioned on its predecessors’ predictions, thereby preserving cooperative performance while constraining the search to a low-dimensional subspace consistent with the sequential structure. We evaluate SeqWM in two challenging multi-robot cooperation environments: Bi-DexHands (Chen et al., 2024a) and Multi-Quad (Xiong et al., 2024), and further validate its effectiveness on physical multi-robot tasks using two Unitree Go2-W robots. The key contributions are as follows: 

- (1) By integrating the sequential paradigm, SeqWM decomposes joint dynamics into autoregressive agent-wise models, reducing modeling complexity, thereby extending MBRL to multi-robot cooperation. 

- (2) Through explicit intention sharing, SeqWM enables the emergence of advanced cooperative behaviors such as predictive adaptation, temporal alignment, and role division. 

- (3) SeqWM consistently outperforms all baseline methods on the simulated multi-robot benchmarks and demonstrates successful real-world deployment on a physical multi-quadruped platform. 

These results collectively demonstrate that SeqWM, by leveraging sequential world modeling and planning, offers an effective pathway for multi-robot cooperation, balancing performance, efficiency, and real-world applicability. 

## 2 RELATED WORK 

**Model-based RL.** In robotics, model-based RL has shown remarkable success due to its high sample efficiency (Jiang et al., 2025), with several approaches (Sun et al., 2023) leveraging learned dynamics models to predict trajectories and optimize actions for physical robots. In contrast, existing multi-robot MBRL methods often rely on centralized paradigms (Zhao et al., 2025b), hindering their practical deployment in multi-robot systems. For example, CoDreamer (Toledo, 2024) use transformers or GNNs to integrate full state-action across all agents. Recent efforts such as MARIE (Zhang et al., 2025a) explored decentralized dynamics modeling, but still require communication at each prediction step for agent-wise aggregation. Different from these works, SeqWM assigns each agent an independent world model and predicts trajectories sequentially, which structurally lowers modeling complexity, thereby making it applicable to real-world scenarios. 

**Sequential Paradigm.** Recent studies have highlighted the advantages of the sequential paradigm (Khan, 2025), which enables fine-grained credit assignment (Kuba et al., 2022), efficient dynamics modeling (Zhang et al., 2025b), and scalable coordination (Xu et al., 2025). For example, MAT (Wen et al., 2022) and PMAT (Hu et al., 2025) model the multi-agent decision-making process as a sequence prediction problem, employing transformers to autoregressively predict each agent’s actions. HARL (Liu et al., 2024a; Zhong et al., 2024) further introduce the sequential update scheme that bring clearer interpretability and ensure monotonic improvement. SeqComm (Ding et al., 2024) extends this idea to the communication domain, where agents exchange information in a sequential order, effectively mitigating non-stationarity. Motivated by these benefits, we integrate the sequential paradigm into multi-robot world modelling to enhance planning and coordination. 

## 3 PRELIMINARIES 

**Problem Formulation.** We model the fully cooperative task as a decentralized partially observable Markov decision process (dec-POMDP), _M_ = _⟨I, S, O, A,_ Ω _, P, R, γ⟩_ , where _I_ = _{v_<sup>1</sup> _, . . . , v_<sup>_n_</sup> _}_ is the set of agents, _S_ is the global state space, _O_ =<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_Oi_is the joint observation space, and</sup> 

2 

Published as a conference paper at ICLR 2026 

_A_ =<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_Ai_isthejointactionspace.TheobservationfunctionΩ:</sup><sup>_S× I→O_defineseach</sup> agent’s perception of the environment, while the transition function _P_ : _S × A →S_ specifies the environment dynamics. The reward function _R_ : _S × A →_ R provides a shared scalar signal, and _γ_ is the discount factor. Each agent _v_<sup>_i_</sup> learns a local policy _π_<sup>_i_</sup> : _O_<sup>_i_</sup> _→ A_<sup>_i_</sup> , which maps its observation _o_<sup>_i_</sup> to an action _a_<sup>_i_</sup> . The objective is to learn a joint policy _π_ =<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_πi_that maximizes the expected</sup> discounted return<sup>�</sup><sup>_∞_</sup> _τ_ = _t_<sup>_γτrτ_.</sup> 

**Sequential Decision-Making.** In many real-world applications, multi-robot systems are often distributed rather than fully decentralized (Negenborn & Maestre, 2014), allowing inter-agent communication to enhance cooperative performance. A Dec-POMDP can thus be extended to a multi-agent POMDP (Oliehoek et al., 2016), where each agent _v_<sup>_i_</sup> receives messages _e_<sup>_i_</sup> _t_<sup>from other agents and</sup> updates its policy _π_<sup>_i_</sup> : _O_<sup>_i_</sup> _× E → A_<sup>_i_</sup> . To balance efficiency and decision quality, agents adopt communication protocols, defined as _ϕ_<sup>_i_</sup> : _O_<sup>_i_</sup> _× E × A_<sup>_i_</sup> _→ E_ . Among them, sequential protocols is especially popular for its simplicity and effectiveness (Ding et al., 2024). It organizes agents in a certain order, where each agent acts on its own observation and the message from its predecessor, then passes information forward. Formally, the process is defined as: 


Such a sequential structure naturally motivates us to design a world model that predicts trajectories in the same manner, enabling efficient multi-agent planning. 

## 4 METHODOLOGY 

In this section, we propose **SeqWM** , which decomposes the joint dynamics into agent-wise models arranged in a sequence. This design substantially reduces modeling complexity, enabling deployment in physical multi-robot systems. 

### 4.1 SEQUENTIAL WORLD MODELLING 

**Decomposed Joint Dynamics.** At each timestep _t_ , the observation-action pair of a single agent ( _o_<sup>_i_</sup> _t_<sup>_, ai_</sup> _t_<sup>)canberegardedasatoken,andtheentiresystemasasequenceofsuchto-</sup> kens. This perspective reformulates joint dynamics as a sequence modeling problem: given the token sequence [( _o_<sup>1</sup> _t_<sup>_, a_1</sup> _t_<sup>)</sup><sup>_, . . . ,_(</sup><sup>_on_</sup> _t_<sup>_, an_</sup> _t_<sup>)],thedynamicsgeneratesthenext-stepoutcomes</sup> [( _o_<sup>1</sup> _t_ +1<sup>_, r_</sup> _t_<sup>1</sup> +1<sup>)</sup><sup>_, . . . ,_(</sup><sup>_on_</sup> _t_ +1<sup>_, r_</sup> _t_<sup>_n_</sup> +1<sup>)].Unlikeexistingcentralizedworldmodels,whichfusealltokens</sup> simultaneously for prediction, as shown in Figure 1, our method adopts an autoregressive paradigm. In this setup, agent 1 first predicts ( _o_<sup>1</sup> _t_ +1<sup>_, r_</sup> _t_<sup>1</sup> +1<sup>) from its local information (</sup><sup>_o_</sup> _t_<sup>1</sup><sup>_, a_1</sup> _t_<sup>), and passes the</sup> result to 2. Subsequently, each agent _i_ conditions on its own observation–action pair ( _o_<sup>_i_</sup> _t_<sup>_, ai_</sup> _t_<sup>)to-</sup> gether with the predictions of all predecessors _{_ ( _o_<sup>_j_</sup> _t_ +1<sup>_, r_</sup> _t_<sup>_j_</sup> +1<sup>)</sup><sup>_}j<i_to produce (</sup><sup>_o_</sup> _t_<sup>_i_</sup> +1<sup>_, r_</sup> _t_<sup>_i_</sup> +1<sup>).Such a</sup> sequential design reduces modeling complexity in a structured, scalable manner, making the approach well-suited for real-world deployment. 

**World Model.** As noted in INTRODUCTION, multi-robot cooperative tasks involve high-dimensional observation and action spaces, making it unsuitable to use reconstructing raw observations as the learning objective of the world model (Hansen et al., 2022). Therefore we remove the explicit decoder and instead perform dynamics prediction entirely in a latent space. To facilitate distributed deployment, each agent maintains an independent world model without parameter sharing. Let _zt_<sup>_i_</sup> denote the latent state of agent _v_<sup>_i_</sup> at timestep _t_ , the world model can be defined as follows: 


All modules in SeqWM are implemented using MLPs, ensuring architectural simplicity and consistency. For communication function, we adopt concatenation operator _⊕_ to facilitate modular training. As shown in Section 5.5, this concise design achieves more stable training performance compared to alternatives such as cross-attention and recurrent neural networks (RNNs). 

3 

Published as a conference paper at ICLR 2026 

**Learning Objective.** Let _θE_ , _θD_ , _θR_ , _θQ_ , and _ψ_ denote the parameters of the encoder, dynamics predictor, reward predictor, critic, and actor, respectively. Following the self-supervised training framework (Hansen et al., 2024), the loss functions can be defined as: 


where _θ_ = _{θE, θD, θR, θQ}_ , _H_ is the prediction horizon, _λ ∈_ (0 _,_ 1] is a constant that balances the contribution of each rollout step, _rt_ is the ground-truth reward, _Gt_ is TD target, and _z_ ˆ _t_<sup>_i_</sup> +1<sup>=</sup> _D_<sup>_i_�</sup> _zt_<sup>_i, a_</sup> _t_<sup>_i, e_</sup> _t_<sup>_i_</sup> � is the predicted latent state. The loss can be backpropagated to the encoder via _zt_<sup>_i_=</sup><sup>_Ei_�</sup> _o_<sup>_i_</sup> _t_ �, so do the dynamics and reward losses. The latent target _zt_<sup>_i_</sup> +1<sup>=</sup><sup>_Ei_�</sup> _o_<sup>_i_</sup> _t_ +1� is detached with the stop-gradient operator sg( _·_ ) to prevent cyclic gradient flow. Soft Cross-Entropy loss is used to match the discretized reward and Q-value predictions. Additionally, to ensure modularity and scalability, each agent’s world model is trained independently, and the loss can not be backpropagated through the communication channel. 

Based on Eq. (3), the encoder learns a compact latent space, while the dynamics and reward predictors minimize prediction errors in this space, ensuring alignment with real environment dynamics. The actor generates initial action estimates in the latent space to warm-start planning and is trained using the Heterogeneous-Agent Soft Actor-Critic (HASAC) (Liu et al., 2024a) algorithm: 


where _α_ is the entropy coefficient, and _H_ [ _·_ ] denotes the entropy function. 

We adopt the sequential update scheme (Kuba et al., 2022; Zhong et al., 2024) to train world models in a manner aligned with its autoregressive structure. When training the agent _v_<sup>_i_+1</sup> , its inputs are conditioned on the predictions of the first _i_ agents, produced by their most recently updated models. This preserves the sequential dependency, ensuring predictions exploit the most up-to-date outputs, which stabilizes training and improves monotonicity across agent indices. 

Inspired by Masked AutoEncoders (He et al., 2022), we randomly permute the order among agents and allow each agent to skip communication with a certain probability. This random masking simulates realistic interruptions and forces the world model to robustly adapt to uncertainties, significantly enhancing the model’s resilience against communication failures. 

### 4.2 SEQUENTIAL PLANNING 

Although Eq. (2) includes an actor, it does not serve directly as an explicit decision policy; instead, it provides initial action estimates for the planner. We next propose a sequential multiagent planner based on Model Predictive Path Integral (MPPI) (Williams et al., 2015) that leverages the predictions of world models to optimize each agent’s action. In this framework, the actor contributes by narrowing the action search space to promising regions, while the planner ensures robust long-term decision-making and corrects suboptimal proposals from the actor. 

At each timestep _t_ , agent _v_<sup>_i_</sup> samples _N_ candidate action sequences of horizon _H_ , denoted _a_<sup>_i_</sup> _t_ : _t_ + _H_<sup>,from theinitial distribution guidedby</sup> the actor. Conditioned on its latent state and the received message, the agent performs latent rollouts with its local world model to predict future 


Figure 2: Sequential planner: agents sequentially optimize actions via local world models and share planned trajectories. 

4 

Published as a conference paper at ICLR 2026 

trajectories. The value of each trajectory is then estimated as 


where _Vt_<sup>_i_</sup> + _H_<sup>represents the value estimate of a sampled action sequence, computed as the sum of</sup> predicted rewards over the horizon plus the terminal value given by the critic. Then, candidate sequences are ranked according to their evaluated values, and the highest-scoring subset is selected as the elite set. The action distribution is updated toward the statistics of these elite trajectories, thereby concentrating future sampling around high-value regions and progressively refining the search space. For further details, please refer to Appendix A.1. 

After several iterations until convergence, the optimized action sequence and predicted trajectory are transmitted as a message to the next agent, which repeats the same planning procedure. This sequential planning paradigm substantially enhances multi-agent cooperation efficiency through explicit intention sharing. 

**Low-pass Action Smoothing.** To prevent mechanical wear caused by abrupt action changes, we integrate a low-pass filtering strategy (Kicki, 2025). In each planning iteration, sampled action sequences are filtered along the temporal dimension to suppress high-frequency fluctuations. This smoothing enforces gradual action transitions across timesteps, reducing control discontinuities and promoting stable, consistent behavior on physical robots. Further details are provided in Appendix A.2. 

**Heuristic Early-Stopping.** Considering the computational constraints of physical robotic platforms, we design a motion-planning heuristic that terminates iterations when the KL divergence between consecutive action distributions falls below a threshold. This early-stopping criterion mitigates diminishing returns (Kobilarov, 2012), reducing computation while preserving plan quality. Further details and experiments are provided in Appendix C.2. 

**Communication Cache.** Inspired by action-chunking (Li et al.) which reuses temporally extended action units to improve decision efficiency, we introduce a cache that stores the predicted messages from the previous agent, enabling the current agent to retrieve them when communication fails. For instance, if communication fails at _t_ +1, agent _v_<sup>_i_+1</sup> retrieves the cached message _zt_<sup>_i_</sup> +1<sup>=</sup><sup>_Di_(</sup><sup>_Ei_(</sup><sup>_o_</sup> _t_<sup>_i_))</sup> from agent _v_<sup>_i_</sup> instead of the ideally updated message _z_ ˆ _t_<sup>_i_</sup> +1<sup>=</sup><sup>_Ei_(</sup><sup>_oi_</sup> _t_ +1<sup>).</sup> 

## 5 EXPERIMENTS 

**Environments.** We evaluate SeqWM and baselines in two challenging multi-robot cooperative environments: Bimanual Dexterous Hands (Bi-DexHands) (Chen et al., 2024a) and Multi-Quadruped Environment (Multi-Quad) (Xiong et al., 2024). In Bi-DexHands, two agents control a pair of dexterous hands to accomplish high-dimensional manipulation tasks (up to _O ∈_ R<sup>229</sup> _, A ∈_ R<sup>26</sup> ). In Multi-Quad, multiple quadruped robots collaborate to solve coordination tasks, and we further deploy SeqWM on real Unitree Go2-W robots to assess its sim-to-real transfer. 

### 5.1 COMPARISONS 

**Baselines.** We select several competitive baselines, including: HASAC (Liu et al., 2024a), a state-ofthe-art model-free method extending SAC to multi-agent settings; MARIE (Zhang et al., 2025a), a model-based method employing a Transformer for dynamics prediction; MAT (Wen et al., 2022), a method adopting the sequential decision-making paradigm; and MAPPO (Yu et al., 2022), a most widely used algorithm, included as a general-purpose baseline. 

**Results on Bi-DexHands.** The representative tasks in Bi-DexHands include object transfer tasks (Over,CatchAbreast,CatchOver2Underarm), which require the two hands to transfer an object under different relative positions and grasping postures; and functional manipulation tasks (BottleCap,Pen,Scissors), which involve precise bimanual operations to achieve specific functional goals, such as opening a bottle cap, removing a pen lid, or spreading a pair of scissors. 

As shown in Figure 3, SeqWM achieves higher asymptotic returns and faster convergence across all tasks. In several tasks (Over, CatchOver2Underarm, Scissors), SeqWM reaches near- 

5 

Published as a conference paper at ICLR 2026 


Figure 3: Performance comparisons on selected tasks of SeqWM with other baselines. Task in Bi-DexHands report the episode return, while Multi-Quad (gray background) reports success rate. Bold lines indicate the mean over multiple seeds, with shaded regions denoting the 95% confidence intervals. The results on all other tasks are reported in Figure 12 in Appendix C.1. 

optimal performance within 2–4M steps, while baselines require far more interactions or fail to match it. In more challenging tasks (Pen, CatchAbreast), SeqWM steadily improves and achieves the highest final returns with lower variance, demonstrating stability. 

**Results on Multi-Quad.** In Gate, the robots are required to pass through a narrow gate as quickly as possible without collision. In PushBox, they jointly push a large box to a designated target location. In Shepherd„ the two quadruped robots (as sheepdogs) cooperatively guide another robot (as sheep) to a target area (as sheep pen). 

In Gate and Shepherd, it rapidly approaches near-100% success rates within the early phase, significantly surpassing baselines in terms of sample efficiency. This superior performance stems from SeqWM’s sequential structure, which enables each agent to plan actions conditioned on its predecessors’ intentions, thereby enhancing coordination. 

### 5.2 EMPOWERED COOPERATIVE BEHAVIORS 

We further visualize the behaviors learned by SeqWM, showing that it not only acquires stable policies in high-dimensional state and action spaces, but also achieves advanced cooperative behaviors, including **predictive adaptation** , **temporal alignment** , and **role division** . 

**Bi-DexHands Behaviors.** In Catch-Over2Underarm, the throwing hand first performs prediction and planning, explicitly transmitting future trajectories to the catching hand. Guided by this message, the catching hand then exhibits **predictive adaptation** by anticipating the object’s motion and landing point and proactively adjusting its grasping posture. As shown in Frames C–D, the catching hand lowers and opens in advance, aligning its posture with the predicted landing point to enable a reliable grasp. In Pen, two hands achieve near-perfect **temporal alignment** by exchanging predictions of future actions in advance. As a result, they grasp the pen body and cap almost simultaneously in Frame D and efficiently complete the extraction in Frames E–F, substantially enhancing cooperative efficiency. 


Figure 4: Trajectory visualizations of Catch-Over2Underarm and Pen with SeqWM. 

**Multi-Quad Behaviors.** Figure 5 further shows the role division learned by SeqWM in the MultiQuad-PushBox. In Frames A–B ( _t_ = 1 _→_ 2), the two quadruped robots navigate to opposite sides 

6 

Published as a conference paper at ICLR 2026 

of the box, establishing an effective pushing configuration. In Frames B–D ( _t_ = 2 _→_ 4)„ both maintain high positive _x_ -axis velocities, indicating continuous forward pushing force. At Frame C ( _t_ = 3), Robot 2 produces a downward _y_ -axis velocity, adjusting the push direction toward the target, while Robot 1 gradually increases its negative _y_ -axis velocity to assist in directional control. As the box approaches the target, Robot 1 reduces its _x_ -axis velocity to avoid overshooting. These behaviors demonstrate that SeqWM supports not only effective force coordination but also fine-grained directional adjustments, resulting in precise and efficient task completion. 


Figure 5: Behavior visualizations in PushBox. The first row shows the execution process, where the box is significantly larger than the robots, requiring coordinated efforts from both quadrupeds to complete the task. The left side of second row visualizes the trajectories of the robots and the box, with the right side showing the x-axis and y-axis velocities and orientations of each robot. 

### 5.3 SCALABILITY TO MORE AGENTS 

We extend the Gate to 5 agents to evaluate the scalability of SeqWM, and the behavioral visualizations of 5-robot-Gate are presented in Figure 6. 


Figure 6: Visualization of the learned behaviors on 5-robot-Gate. 

As the robots approach the narrow gate, they exhibit predictive adaptation, with certain agents proactively decelerating or waiting to avoid potential congestion. For instance, at Frame B ( _t≈_ 2), Robot 3 maintains a near-unity positive x-command, while the other robots moderately reduce their forward commands. In terms of temporal alignment, the x-command trajectories reveal a clear wavelike alternation, where the peak sequence _(3 → 2 → 1 → 4 → 5)_ mirrors the actual passing order, reflecting a dynamic “first-pass–then-follow” sequence. Overall, the team establishes a coordinated rhythm of “prediction–waiting–passing–yielding,” which enables efficient multi-robot traversal under constrained environmental conditions. 

### 5.4 REAL-WORLD DEPLOYMENT 

The real-world experimental setup is detailed in Appendix C.3, and the results are shown in Figure 7. 

In PushBox, the two quadrupeds approach the box from opposite sides and coordinate their pushing forces and directions to move it toward the target. Between Frames D-F, Robot 1 moves forward 

7 

Published as a conference paper at ICLR 2026 


Figure 7: Real-world results of multi-robot cooperation tasks. The trajectories of Robot 1, Robot 2, and the Sheep are marked in different colors. 


Figure 8: Dynamics (left) and reward (right) prediction errors across horizons. 

to provide the main pushing force, while Robot 2 makes slight lateral adjustments to steer the box. The overall pushing pattern, including the division of roles and the gradual directional adjustments, closely matches the behavior observed in simulation, confirming a successful sim-to-real transfer. 

In Gate, two clear yielding events are observed. Between Frames C-D, Robot 1 slows down and waits for Robot 2 to pass first, demonstrating priority management in constrained spaces. After crossing Frames E-F, Robot 2 actively veers aside to leave sufficient space for Robot 1, enabling smooth passage without collisions. These behaviors reflect SeqWM’s trajectory prediction and intention-sharing capabilities, allowing natural, efficient yielding. 

In Shepherd, Robot 1 accelerates between Frames A-B, causing the Sheep to move left. To prevent the Sheep from hitting the left gate frame, Robot 1 retreats while Robot 2 advances between Frames C-D. This maneuver drives the Sheep away from Robot 2 and into the target area. The sequence highlights SeqWM’s capacity for predictive coordination and adaptive role allocation, where the one agent’s motion influences the sheep robot’s response and the another agent adapts accordingly to achieve the common goal. 

### 5.5 ABLATION STUDIES 

**Sequential Sample Generation.** To evaluate the contribution of the sequential paradigm in SeqWM’s world model, we replace it with centralized and decentralized architectures, ensuring all models have an equal number of parameters for a fair comparison. Using BottleCap, we collect 50K environment steps with random actions and train each model for 2.5K steps using the loss in Eq. (3). After training, we gather 1K additional steps to measure dynamics and reward prediction errors across different horizons. As shown in Figure 8, the sequential and centralized models achieve similarly low errors, both substantially outperforming the decentralized model. The results confirm the advantage of sequential prediction, where each agent conditions its output on the predictions of its predecessors, yielding more accurate and coherent rollouts. 

8 

Published as a conference paper at ICLR 2026 

**Communication Function.** We replaced the concat communication function in SeqWM with alternative fusion mechanisms, including MLP, cross-attn, and RNN, and evaluated them on BottleCap. The results in Figure 9 (left) show that the simplest concat approach achieves the highest and most stable performance. This advantage stems from two factors: (i) concat preserves the complete communication content, allowing the dynamics and reward predictors to autonomously identify and exploit the most informative features during training; and (ii) it introduces no additional learnable parameters, thereby maintaining stable gradient propagation in long-horizon prediction. Moreover, we observe that RNN-based fusion even underperforms the no-communication baseline (dec), which we attribute to its sensitivity to input ordering—an undesirable property in multi-agent communication scenarios lacking a fixed semantic sequence. 


Figure 9: _(Left)_ : Performance ablation of the communication functions. _(Middle & Right)_ : Ablation of sequential intention sharing. 

**Sequential Intention Sharing.** A key insight behind SeqWM is that cooperation becomes substantially easier when an agent can access its partners’ future plans. To validate this mechanism, we construct two ablation groups. _DecWM_ removes sequential intention sharing and uses a decentralized world model without inter-agent trajectory passing, while _SeqFree_ removes the world model entirely and allows agents to exchange only single-step messages. 

As shown in Figure 9, SeqWM consistently achieves the best performance, followed by DecWM, whereas SeqFree performs the worst. This indicates that both the world model for predicting future trajectories (i.e., intentions) and the sequential communication for sharing these intentions are indispensable. The gap between SeqWM and DecWM shows that explicit multi-step intention sharing is crucial: without receiving communicated future trajectories from others, each agent can only plan based on its own rollout, which makes coordinated patterns harder to acquire. At the same time, DecWM still clearly outperforms SeqFree, since the decentralized world model implicitly learns regularities in how other agents tend to respond when predicting future environment evolution under joint actions, enabling more foresighted planning even without explicit intention exchange. 

## 6 CONCLUSION 

This paper presented SeqWM, a novel framework that integrates the sequential paradigm into world model learning and planning. By structurally decomposing joint dynamics into autoregressive, agent-wise models, SeqWM offers a principled approach that reduces modeling complexity and naturally enables intention sharing through predicted trajectories. This methodological innovation not only improves scalability but also facilitates the emergence of advanced cooperative behaviors such as predictive adaptation, temporal alignment, and role division. Extensive experiments in Bi-DexHands and Multi-Quad show that SeqWM achieves state-of-the-art performance with superior sample efficiency, while real-world deployment on quadruped robots confirms that these cooperative behaviors transfer reliably from simulation to physical platforms. Beyond empirical results, SeqWM demonstrates that sequential paradigms provide an efficient and scalable principle for structuring multi-agent cooperation, paving the way for more robust and efficient deployment of cooperation in physical multi-robot systems. 

### **Limitations.** 

SeqWM is designed for fully cooperative tasks with shared rewards, and its effectiveness in competitive or mixed-motive settings remains unexplored. Moreover, the current framework relies on a 

9 

Published as a conference paper at ICLR 2026 

fixed or random order, lacking the ability to dynamically adjust the agent sequence during execution, which may limit performance in scenarios where role priorities change over time. 

**Future Work.** Benefiting from the integration of the sequential paradigm and agent-wise world models, SeqWM naturally extends to heterogeneous robot teams and human–robot semantic understanding. With each agent maintaining an independent world model, the framework accommodates diverse dynamics and sensing modalities, enabling cooperation among quadrupeds, manipulators, and aerial robots. Moreover, the explicit trajectory rollouts can be shared not only across robots but also with humans as interpretable intention signals, fostering transparent collaboration, mutual understanding, and trust in human–robot teams. 

10 

Published as a conference paper at ICLR 2026 

## ETHICS STATEMENT 

This work focuses on advancing multi-robot cooperation through model-based reinforcement learning. All experiments were conducted in simulated environments and on standard quadruped robot platforms, with no involvement of humans, animals, or sensitive personal data. The proposed methodology focuses on technical contributions to the fields of reinforcement learning, multi-agent systems, and robotics, without ethical implications beyond standard academic research practices. 

## REPRODUCIBILITY STATEMENT 

Hyperparameters and training procedures are detailed in Appendix B. All baseline comparisons use publicly available implementations, with the documented parameter settings as referenced in the respective sections. 

## USE OF LARGE LANGUAGE MODELS 

Large Language Models (LLMs) were used in the preparation of this paper exclusively for writing assistance and language polishing. The conceptualization of the research, methodology design, experimental implementation, and analysis were all conducted entirely by the authors. The authors take full responsibility for the content of this paper. 

## REFERENCES 

- Michel Aractingi, Pierre-Alexandre Léziart, Thomas Flayols, Julien Perez, Tomi Silander, and Philippe Souères. Controlling the solo12 quadruped robot with deep reinforcement learning. _scientific Reports_ , 13(1):11945, 2023. URL https://dl.acm.org/doi/abs/10.5555/3600270.3601471. 

- Jiajun Chai, Zijie Zhao, Yuanheng Zhu, and Dongbin Zhao. A survey of cooperative multi-agent reinforcement learning for multi-task scenarios. _Artificial Intelligence Science and Engineering_ , 1(2):98–121, 2025. URL https://ieeexplore.ieee.org/abstract/document/11077963. 

- Yuanpei Chen, Yiran Geng, Fangwei Zhong, Jiaming Ji, Jiechuang Jiang, Zongqing Lu, Hao Dong, and Yaodong Yang. Bi-dexhands: Towards human-level bimanual dexterous manipulation. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 46(5):2804–2818, 2024a. URL https://ieeexplore.ieee.org/ abstract/document/10343126. 

- Zixuan Chen, Xialin He, Yen-Jen Wang, Qiayuan Liao, Yanjie Ze, Zhongyu Li, S. Shankar Sastry, Jiajun Wu, Koushil Sreenath, Saurabh Gupta, and Xue Bin Peng. Learning smooth humanoid locomotion through lipschitz-constrained policies. 2024b. URL https://arxiv.org/abs/2410.11825. 

- Guilherme Christmann, Ying-Sheng Luo, Hanjaya Mandala, and Wei-Chao Chen. Benchmarking smoothness and reducing high-frequency oscillations in continuous control policies. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 627–634, 2024. URL https://ieeexplore. ieee.org/abstract/document/10802057. 

- Gang Ding, Zeyuan Liu, Zhirui Fang, Kefan Su, Liwen Zhu, and Zongqing Lu. Multi-agent coordination via multi-level communication. _Advances in Neural Information Processing Systems_ , 37:118513–118539, 2024. URL https://openreview.net/forum?id=3l2HnZXNou. 

- Vladimir Egorov and Alexei Shpilman. Scalable multi-agent model-based reinforcement learning. In _Proceedings of the 21st International Conference on Autonomous Agents and Multiagent Systems_ , AAMAS ’22, pp. 381–390, Richland, SC, 2022. ISBN 9781450392136. URL https://dl.acm.org/doi/abs/10. 5555/3535850.3535894. 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-MPC2: Scalable, robust world models for continuous control. 2024. URL https://openreview.net/forum?id=Oxh5CstDJU. 

- Nicklas A Hansen, Hao Su, and Xiaolong Wang. Temporal difference learning for model predictive control. volume 162, pp. 8387–8406. PMLR, 17–23 Jul 2022. URL https://proceedings.mlr.press/ v162/hansen22a.html. 

11 

Published as a conference paper at ICLR 2026 

- Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross Girshick. Masked autoencoders are scalable vision learners. In _2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 15979–15988, 2022. URL https://ieeexplore.ieee.org/abstract/document/ 9879206. 

- Kun Hu, Muning Wen, Xihuai Wang, Shao Zhang, Yiwei Shi, Minne Li, Minglong Li, and Ying Wen. Pmat: Optimizing action generation order in multi-agent reinforcement learning. AAMAS ’25, pp. 997–1005, 2025. URL https://dl.acm.org/doi/abs/10.5555/3709347.3743619. 

- Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yupeng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, and Dongbin Zhao. World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation. 2025. URL https://arxiv.org/abs/2509.19080. 

- Nouman Khan. _Sequential Decision Making in Cooperative Multi-Agent Systems with Constraints_ . PhD thesis, University of Michigan, 2025. URL https://deepblue.lib.umich.edu/handle/2027.42/ 199212. Accessed: 2025-09-08. 

- Piotr Kicki. Low-pass sampling in model predictive path integral control. 2025. URL https://arxiv. org/abs/2503.11717. 

- Marin Kobilarov. Cross-entropy motion planning. _The International Journal of Robotics Research_ , 31(7): 855–871, 2012. URL https://doi.org/10.1177/0278364912444543. 

- Jakub Grudzien Kuba, Ruiqing Chen, Muning Wen, Ying Wen, Fanglei Sun, Jun Wang, and Yaodong Yang. Trust region policy optimisation in multi-agent reinforcement learning. In _International Conference on Learning Representations_ , 2022. URL https://openreview.net/forum?id=EcGGFkNTxdJ. 

- Qiyang Li, Zhiyuan Zhou, and Sergey Levine. Sample-efficient reinforcement learning with action chunking. _arXiv preprint arXiv:2507.07969_ . URL http://arxiv.org/abs/2507.07969. 

- Jiarong Liu, Yifan Zhong, Siyi Hu, Haobo Fu, QIANG FU, Xiaojun Chang, and Yaodong Yang. Maximum entropy heterogeneous-agent reinforcement learning. In _The Twelfth International Conference on Learning Representations_ , 2024a. URL https://openreview.net/forum?id=tmqOhBC4a5. 

- Qihan Liu, Jianing Ye, Xiaoteng Ma, Jun Yang, Bin Liang, and Chongjie Zhang. Efficient multi-agent reinforcement learning by planning. In _The Twelfth International Conference on Learning Representations_ , 2024b. URL https://openreview.net/forum?id=CpnKq3UJwp. 

- R.R. Negenborn and J.M. Maestre. Distributed model predictive control: An overview and roadmap of future research opportunities. _IEEE Control Systems Magazine_ , 34(4):87–97, 2014. URL https:// ieeexplore.ieee.org/abstract/document/6853439. 

- Frans A Oliehoek, Christopher Amato, et al. _A concise introduction to decentralized POMDPs_ , volume 1. Springer, 2016. URL https://link.springer.com/book/10.1007/978-3-319-28929-8. 

- Cristina Pinneri, Shambhuraj Sawant, Sebastian Blaes, Jan Achterhold, Joerg Stueckler, Michal Rolinek, and Georg Martius. Sample-efficient cross-entropy method for real-time planning. volume 155 of _Proceedings of Machine Learning Research_ , pp. 1049–1065. PMLR, 16–18 Nov 2021. URL https://proceedings. mlr.press/v155/pinneri21a.html. 

- Xujie Song, Liangfa Chen, Tong Liu, Wenxuan Wang, Yinuo Wang, Shentao Qin, Yinsong Ma, Jingliang Duan, and Shengbo Eben Li. Lipsnet++: Unifying filter and controller into a policy network. In _Forty-second International Conference on Machine Learning_ , 2025. URL https://openreview.net/forum?id= KZo2XhcSg6. 

- Jiankai Sun, Yiqi Jiang, Jianing Qiu, Parth Nobel, Mykel J Kochenderfer, and Mac Schwager. Conformal prediction for uncertainty-aware planning with diffusion dynamics model. In _Advances in Neural Information Processing Systems_ , volume 36, pp. 80324–80337. Curran Associates, Inc., 2023. URL https://dl.acm. org/doi/abs/10.5555/3666122.3669643. 

- Edan Toledo. Codreamer: Communication-based decentralised world models. In _Coordination and Cooperation for Multi-Agent Reinforcement Learning Methods Workshop_ , 2024. URL https://openreview.net/ forum?id=f2bgGy7Af7. 

- Bogdan Vlahov, Jason Gibson, David D Fan, Patrick Spieler, Ali-akbar Agha-mohammadi, and Evangelos A Theodorou. Low frequency sampling in model predictive path integral control. _IEEE Robotics and Automation Letters_ , 9(5):4543–4550, 2024. URL https://ieeexplore.ieee.org/abstract/document/ 10480553. 

12 

Published as a conference paper at ICLR 2026 

- Yinuo Wang, Wenxuan Wang, Xujie Song, Tong Liu, Yuming Yin, Liangfa Chen, Likun Wang, Jingliang Duan, and Shengbo Eben Li. ODE-based smoothing neural network for reinforcement learning tasks. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview. net/forum?id=S5Yo6w3n3f. 

- Muning Wen, Jakub Kuba, Runji Lin, Weinan Zhang, Ying Wen, Jun Wang, and Yaodong Yang. Multi-agent reinforcement learning is a sequence modeling problem. _Advances in Neural Information Processing Systems_ , 35:16509–16521, 2022. URL https://openreview.net/forum?id=1W8UwXAQubL. 

- Grady Williams, Andrew Aldrich, and Evangelos Theodorou. Model predictive path integral control using covariance variable importance sampling. 2015. URL https://arxiv.org/abs/1509.01149. 

- Ziyan Xiong, Bo Chen, Shiyu Huang, Wei-Wei Tu, Zhaofeng He, and Yang Gao. Mqe: Unleashing the power of interaction with multi-agent quadruped environment. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 5918–5924. IEEE, 2024. URL https://ieeexplore.ieee. org/abstract/document/10801682. 

- Kaixuan Xu, Jiajun Chai, Sicheng Li, Yuqian Fu, Yuanheng Zhu, and Dongbin Zhao. DipLLM: Fine-tuning LLM for strategic decision-making in diplomacy. In _Forty-second International Conference on Machine Learning_ , 2025. URL https://openreview.net/forum?id=hfPaOxDWfI. 

- Chao Yu, Akash Velu, Eugene Vinitsky, Jiaxuan Gao, Yu Wang, Alexandre Bayen, and Yi Wu. The surprising effectiveness of ppo in cooperative multi-agent games. _Advances in neural information processing systems_ , 35:24611–24624, 2022. URL https://openreview.net/forum?id=YVXaxB6L2Pl. 

- Yang Zhang, Chenjia Bai, Bin Zhao, Junchi Yan, Xiu Li, and Xuelong Li. Decentralized transformers with centralized aggregation are sample-efficient multi-agent world models. _Transactions on Machine Learning Research_ , 2025a. URL https://openreview.net/forum?id=xT8BEgXmVc. 

- Yang Zhang, Xinran Li, Jianing Ye, Shuang Qiu, Delin Qu, Xiu Li, Chongjie Zhang, and Chenjia Bai. Revisiting multi-agent world modeling from a diffusion-inspired perspective. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025b. URL https://openreview.net/forum?id= rRxFIOoEeF. 

- Zijie Zhao, Yuqian Fu, Jiajun Chai, Yuanheng Zhu, and Dongbin Zhao. Meta learning task representation in multiagent reinforcement learning: From global inference to local inference. _IEEE Transactions on Neural Networks and Learning Systems_ , 36(8):14908–14921, 2025a. URL https://ieeexplore.ieee.org/ abstract/document/10905042. 

- Zijie Zhao, Zhongyue Zhao, Kaixuan Xu, Yuqian Fu, Jiajun Chai, Yuanheng Zhu, and Dongbin Zhao. Learning and planning multi-agent tasks via a moe-based world model. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025b. URL https://openreview.net/forum?id= fi24ry0BX5. 

- Yifan Zhong, Jakub Grudzien Kuba, Xidong Feng, Siyi Hu, Jiaming Ji, and Yaodong Yang. Heterogeneousagent reinforcement learning. _Journal of Machine Learning Research_ , 25(32):1–67, 2024. URL http: //jmlr.org/papers/v25/23-0488.html. 

13 

Published as a conference paper at ICLR 2026 

|APPE|NDICES||
|---|---|---|
|**A Mul**|**ti-Agent Planner**|**15**|
|A.1|Planning Process. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>15|
|A.2|Low-Pass Action Smoothing<br>. . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>15|
|A.3|Serial-Blocking-Free Execution . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>16|
|**B**<br>**Imp**|**lementation Details**|**17**|
|B.1|Pseudocode<br>. . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>17|
|B.2|Hyperparameters. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>17|
|**C Add**|**itional Experiments**|**18**|
|C.1|Additional Comparisons . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>18|
|C.2|Inference Time. . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>18|
|C.3|Sim-to-Real Deployment<br>. . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . .<br>18|


14 

Published as a conference paper at ICLR 2026 

## A MULTI-AGENT PLANNER 

### A.1 PLANNING PROCESS 

At timestep _t_ , the action planning process for agent _v_<sup>_i_</sup> can be divided into the following steps: 

**S1 - Communication.** Agents are organized to exchange messages in a sequential manner. Specifically, agent _v_<sup>_i_</sup> receives a message _e_<sup>_i_</sup> _t_<sup>that aggregates the predicted latent states and planned actions from all its predecessors:</sup> 


where _⊕_ denotes concatenation. To implement this efficiently, we employ a masking-based concatenation scheme: a fixed-length vector of dimension _n ×_ ( _|A|_ + _dz_ ) is pre-allocated, where _n_ is the number of agents, _|A|_ and _dz_ are the action and latent dimensions. Agent _v_<sup>1</sup> maintains an empty message, while subsequent agents sequentially fill in their designated slots with their own predictions (ˆ _zt_<sup>_i, ai_</sup> _t_<sup>) in addition to forwarding the received</sup> content. This design ensures that information is progressively accumulated along the communication chain with linear complexity in the number of agents. 

**S2 - Action Sampling.** The planner samples _N_ candidate action sequences from two sources. We sample _Np_ candidate action sequences from a diagonal Gaussian distribution _a_<sup>_i_</sup> _t_ : _t_ + _H_<sup>_∼N_</sup> � _µ_<sup>_i_</sup> _t_ : _t_ + _H_<sup>_,_(</sup><sup>_σ_</sup> _t_<sup>_i_</sup> : _t_ + _H_<sup>)2</sup><sup>_I_</sup> �, where _µ_<sup>_i_</sup> _t_ : _t_ + _H_<sup>_, σ_</sup> _t_<sup>_i_</sup> : _t_ + _H_<sup>_∈_R</sup><sup>_|A|×H_representthemeanandstandarddeviationofthe</sup><sup>_H_-stephorizonactions.</sup> Additionally, we sample _Na_ action sequences directly from the actor module _a_ ˆ<sup>_i_</sup> _h_<sup>_∼πi,_Act(</sup><sup>_·|o_</sup> _h_<sup>_i, ei_</sup> _h_<sup>)</sup><sup>_, h_=</sup><sup>_t_:</sup> _t_ + _H_ , and combine these two sets of action sequences to form _N_ candidate action sequences. 

**S3 - World Model Prediction.** Following sampling, the world model predicts _H_ -step trajectories for each sampled action sequence using Eq. (2), generating _N_ predicted sequences Γ = _{_ (ˆ _zh_<sup>_i, ai_</sup> _h_<sup>_,_ˆ</sup><sup>_r_</sup> _h_<sup>_i_)</sup><sup>_}h_=</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_H_.</sup> 

**S4 - Value Evaluation.** Each predicted trajectory is assigned a value via the _H_ -step return, combining the short-term cumulative predicted reward with the terminal value from the critic: 


**S5 - Action Optimization.** The candidate action sequences are ranked by their evaluated values, and the top _M_ are chosen as the elite set Γ<sup>_∗_</sup> . The parameters of the action distribution are updated based on the elite set using: 


where the weights are generated based on the evaluated values as _αmm_ = exp _τ_ being the temperature coefficient. 

**Iteration.** For the default setting, the above process are iterated _K_ times to derive the final action distribution. If the early-stopping heuristic is applied, after each iteration, we check whether the action optimization has converged by evaluating the KL divergence between the current and previous action distributions, D _KL_ ( _N_<sup>(</sup><sup>_k_+1)</sup> _∥N_<sup>(</sup><sup>_k_)</sup> ) _< η_ , where _η_ is a small threshold. 

The detailed hyperparameters used in the model-based planner are summarized in Table 1. 

### A.2 LOW-PASS ACTION SMOOTHING 

In real-world robotics, high-frequency changes in control inputs can cause severe mechanical impacts, accelerating wear and reducing execution stability. Therefore, many studies in reinforcement learning and motion planning incorporate action-smoothing constraints, such as adding penalties on differences between consecutive actions during policy updates (Aractingi et al., 2023; Christmann et al., 2024; Wang et al., 2025), introducing regularization in policy networks (Chen et al., 2024b; Song et al., 2025), or filtering noise in trajectory optimization (Pinneri et al., 2021; Vlahov et al., 2024; Kicki, 2025), to reduce jitter and improve executability. Inspired by these methods, we apply frequency-domain low-pass filtering directly to the sampled action noise in our planner, explicitly suppressing the high-frequency components of the actions. 

Specifically, during action sampling, we first sample noise from a standard normal distribution, apply low-pass filtering, and then add the filtered noise to the action mean to generate candidate action sequences. We use a Butterworth filter with _o_ LBF = 1, whose transfer function and amplitude–frequency response are given by: 


15 

Published as a conference paper at ICLR 2026 


Figure 10: Visualization of the low-pass filter. ( _Left_ ): Amplitude–frequency response of the low-pass filter. ( _Middle_ ): Filtering effects on random signals at 20% cutoff ratios, the different colors represent different action dimensions. ( _Right_ ): Effects of low-pass filtering on control commands in PushBox, with different colors representing different agents. 

where _fc_ is the low-pass cutoff frequency. As show in Figure 10, the amplitude–frequency response shows that the high-frequency components are exponentially attenuated (approaching linear decay in logarithmic coordinates). The corresponding discrete-time difference equation, obtained via bilinear transformation, is 


where _fs_ is the sampling frequency, i.e., the frequency of the control signal. 

### A.3 SERIAL-BLOCKING-FREE EXECUTION 

A common concern regarding the sequential paradigm is that the _i_ -th agent may need to wait for the ( _i−_ 1)-th agent to finish planning, potentially causing inference time to grow linearly with the number of agents (Wen et al., 2022; Hu et al., 2025). This issue, referred as _serial blocking_ , does not arise in SeqWM due to the use of the communication cache. 


Figure 11: Sequential execution without serial blocking enabled by the communication cache. 

As shown in Figure 11, the sequential paradigm specifies only the update order of the communication caches, rather than the execution order of each agent’s planner. Each agent runs MPPI-based planner at a fixed control frequency and simply reads the latest available multi-step trajectory from the cache, without waiting for any other agent to complete planning. Under this design, the per-step inference latency satisfies 


meaning that SeqWM achieves _O_ (1) decision latency with respect to the number of agents rather than exhibiting linear degradation. 

16 

Published as a conference paper at ICLR 2026 

### **Algorithm 1** Model Training 

**Input:** replay buffer _B_ , parameterized networks _θE, θD, θR, θQ,_ and _ψ_ for encoder, dynamics predictor, reward predictor, critic, and actor, respectively; **for** episode = 1 _,_ 2 _,_ 3 _, . . . ,_ **do for** step _t_ = 1 _,_ 2 _,_ 3 _, . . ._ **do** Get real data ([ _o_<sup>_i_</sup> _t_<sup>]</sup><sup>_i_=1:</sup><sup>_n,_[</sup><sup>_ai_</sup> _t_<sup>]</sup><sup>_i_=1:</sup><sup>_n, rt,_[</sup><sup>_oi_</sup> _t_ +1<sup>]</sup><sup>_i_=1:</sup><sup>_n_) by interacting with the environment</sup> Add transition into buffer: _B_ = _B ∪_ ([ _o_<sup>_i_</sup> _t_<sup>]</sup><sup>_i_=1:</sup><sup>_n,_[</sup><sup>_ai_</sup> _t_<sup>]</sup><sup>_i_=1:</sup><sup>_n, rt,_[</sup><sup>_oi_</sup> _t_ +1<sup>]</sup><sup>_i_=1:</sup><sup>_n_)</sup> **end for for** epoch = 1 _,_ 2 _,_ 3 _, . . . ,_ **do** Sample trajectories from _B_ Update _θE, θD, θR, θQ_ by minimizing Eq. (3) Update _ψ_ by minimizing Eq. (4). **end for end for** 

### **Algorithm 2** Model Planning 

**Input:** learned parameters _θE, θD, θR, θQ, ψ_ , hyperparameters _H, K, τ, Np, M, Na_ , initial distribution; **for** step _t_ = 1 _,_ 2 _,_ 3 _, . . ._ **do for** agent _i_ = 1 _,_ 2 _, . . . , n_ **do** Get environment observation _o_<sup>_i_</sup> _t_<sup>and encode it to latent space:</sup><sup>_z_</sup> _t_<sup>_i_=</sup><sup>_Ei_(</sup><sup>_oi_</sup> _t_<sup>)</sup> **if** _i >_ 1 **then** Retrieve the message from the previous agent _e_<sup>_i_</sup> _t_<sup>= �</sup> _j<i_ � _z_ ˆ _t_<sup>_j, aj_</sup> _t_ � **else** set _e_<sup>_i_</sup> _t_<sup>=</sup><sup>_∅_</sup> **end if for** iteration = 1 _,_ 2 _,_ 3 _, . . . , Kp_ **do** Sample _Na_ actions _a_<sup>_i_</sup> _t_ : _t_ + _H_<sup>_∼N_</sup> � _µ_<sup>_i_</sup> _t_ : _t_ + _H_<sup>_,_(</sup><sup>_σ_</sup> _t_<sup>_i_</sup> : _t_ + _H_<sup>)</sup> 2 _I_ � Sample _Np_ actions from actor ˆ _a_<sup>_i_</sup> _h_<sup>_∼πi,_Act(</sup><sup>_·|oi_</sup> _h_<sup>_, ei_</sup> _h_<sup>)</sup><sup>_, h_=</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_H_</sup> Get predictions by world model rollouts, Γ = _{_ (ˆ _zh_<sup>_i, ai_</sup> _h_<sup>_,_ˆ</sup><sup>_r_</sup> _h_<sup>_i_)</sup><sup>_}h_=</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_H_</sup> Evaluate the trajectories by Eq. (7) and select top- _M_ elite action sequences Update action distribution following Eq. (8) **end for end for end for** 

- B IMPLEMENTATION DETAILS 

- B.1 PSEUDOCODE 

- B.2 HYPERPARAMETERS 

We summarize the hyperparameters used in SeqWM in Table 1 and Table 2. 

Table 1: The Notations and Values of hyperparameters in the planner. 

|**Hyperparameters**|**Notations**|**Value**|**Hyperparameters**|**Notations**|**Value**|
|---|---|---|---|---|---|
|rollout horizon|_H_|3|sampling actions|_Np_|512|
|planning iterations|_K_|6|elites|_M_|64|
|temperature|_τ_|0.5|actor samples|_Na_|24|


17 

Published as a conference paper at ICLR 2026 

Table 2: The hyperparameters used in the world model. 

|**Hyperparameters**|**Value**|**Hyperparameters**|**Value**|**Hyperparameters**|**Value**|
|---|---|---|---|---|---|
|batch size|1000|buffer size|1e6|dynamics coef|20|
|encoder lr scale|0.3|entropy coef|1e-4|lr|5e-4|
|n-step return|20|num bins|101|q coef|0.1|
|reward coef|0.1|step_ρ_|0.5|||


## C ADDITIONAL EXPERIMENTS 

### C.1 ADDITIONAL COMPARISONS 

We report additional comparison results on other tasks to complement Figure 3. 


Figure 12: Comparison results on other tasks. 

### C.2 INFERENCE TIME 

**Inference Time Cost.** We report the per-step execution time of SeqWM on BottleCap using a single RTX A6000 GPU on the left side of Figure 13. The execution time increases almost linearly with the rollout horizon _H_ and the number of planner iterations _K_ , which is consistent with the design of SeqWM. With the default settings, SeqWM achieves a per-step execution time of 12.8 ms, making it suitable for most real-time robotic tasks. 


Figure 13: The per-step execution time of SeqWM. ( _Left_ ): Time cost under different rollout horizons _H_ and planner iterations _K_ . ( _Right_ ): Time cost and performance with and without early-stopping heuristic. 

**Early-Stopping Heuristic.** To further enhance the efficiency of SeqWM, we introduce an early-stopping heuristic in Section 4.2 that terminates iterations when the change in the action distribution is not significant. The KL divergence is used as a measure of distribution change, and the execution time and performance under different thresholds on BottleCap are shown on the right side of Figure 13. When the threshold is set to 0.5, SeqWM reduces the execution time by approximately 57.3% while incurring only about 5.9% performance loss. 

### C.3 SIM-TO-REAL DEPLOYMENT 

We implement all three Multi-Quad tasks in an 8m _×_ 5m indoor space. Each task involves two Unitree Go2-W quadruped robots. The room is equipped with eight Mars cameras, and real-time localization of robots and objects is provided by the NOKOV 3D motion capture system. 

18 

Published as a conference paper at ICLR 2026 

- **PushBox** : We use a cardboard box of 1 _._ 2m _×_ 1 _._ 2m _×_ 0 _._ 5m and approximately 6 kg in mass. The box is sufficiently large that a single robot cannot independently control its movement direction, making cooperation essential. The static and kinetic friction coefficients between the box and the ground are both approximately 0 _._ 5. 

- **Gate** : A 1m-wide doorway is set up. As shown in Figure 7 (b)-A, the two robots cannot pass through side-by-side, requiring coordinated navigation. 

- **Shepherd** : A DJI EP robot acts as the guided agent (sheep). It is equipped with an omnidirectional chassis to simulate sheep behavior: it moves away from the nearest herding robot and its speed is inversely proportional to the distance to that robot. 


Figure 14: Real-world setups. 

We employ the following strategies to enhance the generalization capability of SeqWM and facilitate sim-to-real transfer: 

- **Observation transformation** : Positions of other robots are transformed from the global frame into the ego-centric frame of the current robot, reducing observation complexity and improving policy generalization. 

- **Domain randomization** : Taking PushBox as an example, we randomize the initial positions/orientations of both robots and the box, the position and distance of the target, and the friction coefficient between the box and floor to improve robustness to environmental variations. 

- **Sensor and actuation perturbations** : Random noise is added to sensor readings, and small delays with noise are introduced into control commands to emulate real-world sensing errors and actuation inaccuracies. 

19 

