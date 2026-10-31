---
title: "EvoAgent: Self-evolving Agent with Continual World Model for Long-Horizon Tasks"
date: "2026"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2502.05907
pdf: https://arxiv.org/pdf/2502.05907
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.05907)** / [論文ページ](https://arxiv.org/abs/2502.05907)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

1 

# EvolvingAgent: Curriculum Self-evolving Agent with Continual World Model for Long-Horizon Tasks 

Tongtong Feng, Xin Wang, _Member, IEEE,_ Zekai Zhou, Ren Wang, Yu-Wei Zhan, Guangyao Li, Qing Li, Wenwu Zhu, _Fellow, IEEE_ 

**_Abstract_ —Completing Long-Horizon (LH) tasks in open-ended worlds is an important yet difficult problem for embodied agents. Existing approaches suffer from two key challenges: (1) they heavily rely on experiences obtained from human-created data or curricula, failing to autonomously update and select multimodal experiences, and (2) they may encounter catastrophic forgetting issues when faced with new tasks, failing to autonomously update world knowledge. To solve these challenges, this paper presents EvolvingAgent, a curriculum self-evolving agent with a continual World Model (WM), which can autonomously complete various LH tasks across environments through self-planning, self-control, and self-reflection, without human intervention. Specifically, EvolvingAgent contains three modules, i.e., i) the experiencedriven task planner, which uses an LLM along with multimodal experiences to convert LH tasks into executable sub-tasks; ii) the WM-guided action controller, which leverages WM to generate low-level actions and incorporates a self-verification mechanism to update multimodal experiences; iii) the Curriculum Learning (CL) -based reflector, which implements a two-stage CL algorithm to select multimodal experiences for task-adaptive WM updates. By building a planner-controller-reflector closed-loop dynamic, the continual WM for EvolvingAgent can autonomously update multimodal experiences and world knowledge. We conducted extensive experiments on Minecraft, compared with existing methods, EvolvingAgent can improve 111.74% average success rate, reduce more than 6x ineffective actions, and generalize to the Atari environment with human-level performance.** 

**_Index Terms_ —Self-evolving Agent, Continual World Model, Curriculum Learning, Long-Horizon Tasks.** 

## I. INTRODUCTION 

**L** ONG-Horizonstep tasks that(LH)requiretaskssustained[1], [2] planning,are complex,sequentialmultidecision-making, and extended execution over a prolonged period to achieve a final goal. These tasks are challenging, often exhibiting reward sparsity [3] and procedural diversity [4]. Completing LH tasks in open-ended worlds is an important yet difficult problem for embodied agents, such as logistics robots, surgical robots, and rescue robots. 

On the one hand, existing agents have made remarkable progress by utilizing expert data and domain-specific curricula created by humans, developing policies through Reinforcement Learning (RL) [5], Imitation Learning (IL) [6], and Large 

Tongtong Feng, Xin Wang, Ren Wang, Yu-Wei Zhan, Guangyao Li, and Wenwu Zhu are with the Department of Computer Science and Technology, Beijing National Research Center for Information Science and Technology, Tsinghua University, Beijing 100084, China (E-mail: _{_ fengtongtong, xin <u>wang,</u> rwang2xx, zhanyw, guangyaoli, wwzhu _}_ @tsinghua.edu.cn). Zekai Zhou is with the Department of Computer Science, University of Sydney, Sydney, Australia (E-mail: zhouodywork@gmail.com). Qing Li is with the Department of Electronic Engineering, Tsinghua University, Beijing 100084, China (E-mail: soleilor@tsinghua.edu.cn). 

Corresponding authors: Xin Wang and Wenwu Zhu. 


Fig. 1: The illustration of EvolvingAgent. EvolvingAgent can autonomously complete various long-horizon tasks across environments through self-planning, self-control, and selfreflection, without human intervention. The continual World Model (WM) for EvolvingAgent builds planner-controllerreflector closed-loop dynamic, which can autonomously update multimodal experiences and world knowledge. 

Language Models (LLMs) [7]. On the other hand, recent studies [4] demonstrate that humans’ ability to accomplish LH tasks in an open world relies on autonomous multimodal experience accumulation and world knowledge updates. In essence, autonomous world knowledge update serves as a meta-cognitive driver that not only guides action selection under partial observability but also enables context-aware adaptation to environmental dynamics, thereby resolving the local optimality issue inherent in LH task completion. 

_Completing LH tasks in open-ended worlds requires agents to achieve autonomous multimodal experience accumulation and world knowledge updates, like a baby thrives._ 

Nevertheless, existing methods are hard to complete various LH tasks across environments from scratch: _1) Failing to autonomously update and select multimodal experiences._ Most embodied agents assume that all training data are available from the beginning (such as IL-based or LLMs-based agents), which heavily rely on human-created data or curricula [7]. However, this assumption is unrealistic, as agents may encounter novel tasks or environments after deployment [8]. _2) Failing to autonomously update world knowledge._ On the one hand, existing methods use LLMs (such as Voyager [9], Jarvis-1 [10]) to represent world knowledge based on sampling historical experiences or use a graph (such as Optimus-1 [11]) to sparsely represent world knowledge, which requires human intervention 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

2 

and is hard to autonomously update. On the other hand, existing methods face catastrophic forgetting, where they lose previously obtained knowledge [3], [12] for learning new tasks, which are hard to autonomously update and transfer world knowledge for LH tasks across environments. 

To solve these challenges, in this paper, we propose **EvolvingAgent** (as shown in Fig. 1), a curriculum selfevolving agent with a continual World Model (WM), which can autonomously complete various LH tasks across environments through self-planning, self-control, and self-reflection, without human intervention. EvolvingAgent contains three modules: i) The experience-driven task planner, which uses an LLM along with multimodal experiences, to incorporate self-state into the planning phase and convert LH tasks into executable subtasks; ii) The WM-guided action controller, which leverages WM to generate low-level actions and incorporates a selfverification mechanism to update multimodal experiences. iii) The Curriculum Learning (CL) -based reflector, which implements a two-stage CL algorithm to select experiences for task-adaptive WM updates. By using a model-based online RL setup and building a planner-controller-reflector closed-loop dynamic, the continual WM for EvolvingAgent can autonomously update multimodal experiences and world knowledge, filtering out invalid explorations and mitigating historical forgetting. 

We evaluate EvolvingAgent’s performance in Minecraft [13], a popular open-world environment. Extensive experiments demonstrate EvolvingAgent’s superiority: compared with existing methods, EvolvingAgent can achieve an average success rate improvement of 111.74% and reduce ineffective actions by more than 6x. We also evaluate the generalization of EvolvingAgent in the Atari environment [14]; EvolvingAgent outperforms existing methods and achieves human-level performance in some tasks. The contributions are summarized as follows: 

- We propose EvolvingAgent, a curriculum self-evolving agent, which can autonomously complete various LH tasks across environments through self-planning, self-control, and self-reflection, without human intervention. 

- We design a novel continual WM for EvolvingAgent, building planner-controller-reflector closed-loop dynamic to autonomously update multimodal experiences and world knowledge. 

- We conduct extensive experiments on Minecraft. EvolvingAgent can achieve an average success rate improvement of 111.74%, reduce ineffective actions by more than 6x, and generalize to the Atari environment with human-level performance. 

## II. RELATED WORKS 

## _A. Embodied Long-horizon Tasks_ 

Embodied Long-Horizon (LH) tasks [1], [2], [15] refer to complex, multi-step tasks that require sustained planning, sequential decision-making, and extended execution over a prolonged period to achieve a final goal. Existing work on embodied agents completing LH tasks can be divided into two categories. One is Model-Based Reinforcement Learning (MBRL) [16]. Embodied agents leverage MBRL to tackle LH 

tasks by interacting with environments and learning predictive world dynamics [17]. The other is vision-language modelbased (VLM) planning [18], [19]. Embodied agents leverage VLMs to decompose LH tasks into hierarchical sub-goals [20], dynamically refine plans via memory-augmented reasoning [21], and align semantic intent with executable actions through iterative simulation [22], such as EmbodiedGPT [23], which bridges high-level planning with low-level control. However, they assume perfect knowledge of environments, rely on oracle feedback, and assume perfect execution of low-level policies, which makes it hard to adapt various LH tasks across environments in open worlds [8]. 

## _B. World Models_ 

World Models (WMs) empower embodied AI by building internal representations and making future predictions of the external world [24], [25]. They serve as simulators of real environments that predict the future outcome of certain actions, and policies can be derived from them. Current research focuses on two paradigms: understanding the world through latent state representations [26], [27] and predicting future dynamics for planning and control [28]. Recurrent State-Space Model (RSSM) [3] is a classic world model structure. Representative example usages of them in MBRL include action searching [12], policy optimization within such simulators, or a combination of both [3]. However, WMs currently struggle to prevent catastrophic forgetting [29] due to their inability to maintain stable representations of previously learned environmental dynamics while adapting to new tasks, often exacerbated by shared parameter updates prior to knowledge [30]. 

## _C. Curriculum Learning_ 

Curriculum Learning (CL) not only is a easy-to-hard heuristic, but also is a policy of difficulty modeling, schedule adaptation, and task-dependent deployment. In multimedia settings, this shift is particularly visible. For visual grounding, CLIP-VG [31] shows that a self-paced curriculum can stabilize adaptation by gradually exploiting pseudo-language supervision rather than trusting noisy alignments from the beginning. For video understanding, exploring clip order in a self-supervised curriculum provides a structured way to organize temporal learning signals, improving downstream video applications beyond random pretraining order [32]. In human pose estimation, DMH-CL [33] further suggests that curriculum design can be tied to model hardness, allowing the training process to move according to the learner’s state rather than a fixed schedule. A related idea appears in datafree knowledge distillation, where category-aware curricula are used to control the transfer path from easier categories to harder ones [34]. Recent work has started to systematize the field through multimodal weak supervision [35], unified benchmarking [36], and psychologically grounded difficulty estimation and pacing strategies [37]. These studies suggest that modern curriculum learning is becoming less a handcrafted ordering trick and more a trainable mechanism for matching data exposure to model maturity. However, CL is currently not applied to solving embodied long-horizon tasks, nor has it achieved autonomous experience updating. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

3 


Fig. 2: The overview of EvolvingAgent, which includes an experience-driven task planner, a WM-guided action controller and a Curriculum Learning (CL) -based reflector. The continual WM for EvolvingAgent, building planner-controller-reflector closed-loop dynamic, can autonomously update multimodal experiences and world knowledge. 

## _B. Recurrent State-Space Model_ 

## III. PRELIMINARIES 

## _A. Online Model-based Reinforcement Learning_ 

_Model-based Reinforcement Learning_ Recurrent State-Space Model (RSSM) [3], [38] is a classic Learning (RL) is typically formulated as world model structure, which can predict latent states and Decision Process (MDP) defined by the tuple rewards from high-dimensional observations. RSSM con, where _S_ is the state space, _A_ is the action tains 6 modules. 1) Encoder, maps observation _ot_ to a _s, a_ ) is the transition dynamics, _R_ ( _s, a_ ) is the stochastic latent state _st_ = ( _ht, zt_ ), where _ht_ is a deterand _γ ∈_ [0 _,_ 1) is the discount factor. The ministic RNN state and _zt_ is a stochastic latent variable, a policy _π_ ( _a|s|ss_ ) that maximizes the expected _qϕ_ ( _zt|ht, ot_ ) = _N_ � _zt_ ; _µϕ_ ( _ht, ot_ ) _, σϕ_ ( _ht, ot_ )�, where _µϕ, σϕ_ reward: are neural networks. 2) Sequence model: predicts the sequence of these representations given past actions _at−_ 1, _J_ ( _π_ ) = E _π,P_ � _γ_<sup>_t_</sup> _R_ ( _st, at_ ) _,_ (1) _ht_ = _fθ_ ( _ht−_ 1 _, zt−_ 1 _, at−_ 1). 3) Dynamics predictor, predicts the � _t∞_ =0 � prior latent state transition, _pθ_ (ˆ _zt|ht_ ) = _N_ � _z_ ˆ _t_ ; _µθ_ ( _ht_ ) _, σθ_ ( _ht_ )�. Reinforcement Learning (MBRL), the agent 4) Decoder: reconstructs observations from latent states, a model _M_ , which includes an approximate _pθ_ ( _ot|ht, zt_ ) = _N_ � _ot_ ; _µ_<sup>obs</sup> _θ_<sup>(</sup><sup>_ht, zt_)</sup><sup>_, σ_</sup> _θ_<sup>obs</sup> �. 5) Reward predictor, _P_<sup>ˆ</sup> _θ_ ( _s_<sup>_′_</sup> _|s, as, a_ ) and a reward model _R_<sup>ˆ</sup> _ϕ_ ( _s, a_ ),, predicts rewards, _r_ ˆ _t_ = _rθ_ ( _ht, zt_ ). 6) Continual predictor, by _θ_ and _ϕ_ , respectively. These models are predicts episode continuation flags, _c_ ˆ _t_ = sigmoid� _cθ_ ( _ht, zt_ )�. empirical prediction errors over observed Above all, RSSM can be defined as follows: 

Reinforcement Learning (RL) is typically formulated as a Markov Decision Process (MDP) defined by the tuple ( _S, A, P, R, γ_ ), where _S_ is the state space, _A_ is the action space, _P_ ( _s_<sup>_′_</sup> _|s, a_ ) is the transition dynamics, _R_ ( _s, a_ ) is the reward function, and _γ ∈_ [0 _,_ 1) is the discount factor. The goal is to learn a policy _π_ ( _a|s|ss_ ) that maximizes the expected cumulative reward: 

In Model-based Reinforcement Learning (MBRL), the agent explicitly learns a model _M_ , which includes an approximate dynamics model _P_<sup>ˆ</sup> _θ_ ( _s_<sup>_′_</sup> _|s, as, a_ ) and a reward model _R_<sup>ˆ</sup> _ϕ_ ( _s, a_ ),, parameterized by _θ_ and _ϕ_ , respectively. These models are trained to minimize empirical prediction errors over observed transitions _D_ = _{_ ( _si, ai, si, ai, s, ai, si, s, s_<sup>_′_</sup> _i_<sup>_, rii_)</sup><sup>_}_:</sup> 


Using the learned models, the agent performs planning to optimize its policy. For example, in value iteration, the statevalue function _V_ ( _s_ ) is iteratively updated via the Bellman equation: 


## IV. EVOLVINGAGENT 

Let _E_ denote a dynamic open-world environment with partial observability, _T_ represent the LH tasks, and _S_ represents the agent’s current state. We aim to design a curriculum 

In online MBRL, an agent interacts with the environment iteratively for _K_ rounds with the goal of learning a sequence to minimize _L_ model( _θ, ϕ_ ). 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

4 

self-evolving agent _EvolvingAgent_ that can complete various LH tasks across environments, without human intervention. As shown in Fig. 2, EvolvingAgent includes an experiencedriven task planner Ψplan, a WM-guided action controller Πact, a Curriculum Learning (CL) -based reflector Φreflect; The continual world model includes a Multimodal Experience Pool (MEP) _D_ MEP, and a world model _Mw_ . EvolvingAgent has an online MBRL setup and can be instantiated as: 


**Continual world model** . As shown in Algorithm 1, by building a planner-controller-reflector closed-loop dynamic, the continual world model for EvolvingAgent can autonomously update multimodal experiences and world knowledge. The sketch is as follows: 


whereare actions _{gi}_ generatedare subtasksby generatedthe controllerby theΠactplanner; _DMEP′_ Ψplan<sup>and</sup> ; _{_<sup>_M_</sup> _at′w}_ are the updated states. 

**Evaluation.** According to relevant research [3], [39], the agents’ performance metrics includes Success Rate ( **SR** ) and Exploration Efficiency ( **EE** ). 


where ENum<sup>suc</sup> _gi_<sup>indicatesthenumberofepisodes(alifecycle)</sup> in which the subtask _gi_ succeeded; ENum<sup>all</sup> _gi_<sup>indicatesthetotal</sup> number of episodes; Step<sup>suc</sup> _gi_<sup>indicates the success step length of</sup> subtask _gi_ , and Step<sup>all</sup> _gi_<sup>indicatesthetotalsteplengthofsubtask</sup> _gi_ exploration. 

of each token. We adopt the textual tokenizer _ft_ to encode _T_ into token embeddings. We further utilize a lightweight projection module with a trainable projection matrix _W_ . This module maps the visual tokens to the same space with text embeddings _V_<sup>ˆ</sup> = _W V_ , yielding _V_<sup>ˆ</sup> = _{v_ ˆ1 _,_ ˆ _v_ 2 _, ...,_ ˆ _vn} ∈_ R<sup>_n×d_</sup> . The output of our planner is the subtask _gi_ . 

**Self-planning.** EvolvingAgent updates the planner for efficient LH task planning without human intervention. The LLM-based planner undergoes lightweight fine-tuning using Low-Rank Adaptation (LoRA) [40]. The process of selfplanning is as follows: 1) During agent initialization, the finetuning process utilizes all accumulated experiences from the multimodal experience pool _D_ MEP for task planning. When the multimodal experience pool is empty, the agent initializes task planning based on the capabilities of the original GPT-4o. 2) During the agent’s lifecycle, when the feedback of WM-guided action controller indicates the subtask _gi_ failure, experience trajectories relevant to the subtask _gi_ by label matching are extracted to construct input-output pairs _{_ ( _X_ in<sup>(</sup><sup>_k_)</sup><sup>_, Y_</sup> out<sup>(</sup><sup>_k_))</sup><sup>_}_</sup> for model fine-tuning, where the input _X_ in<sup>(</sup><sup>_k_)</sup> includes all the experience _h_ related the subtask _gi_ , while the output _Y_ out<sup>(</sup><sup>_k_)</sup> represents whether the subtask in each experience was successful. We only use input-output pairs for model fine-tuning. This enables the planner to quickly study from the failure patterns while preserving its general planning capabilities, thereby improving robustness and reducing repeated errors in LH tasks. 3) When the agent dies (such as health value is 0), the agent is reinitialized. 

## _B. WM-Guided Action Controller_ 

The WM-guided action controller Πact is formalized as a function that maps the current state _S_ , subtask _G_ , and = the world model _Mw_ to an action sequence _at_ : _t_ + _H {at, at_ +1 _, . . . , at_ + _H }_ for horizon _H_ . 


## _A. Experience-driven Task Planner_ 

The experience-driven task planner Ψplan is formalized as a function that maps the current state _S_ , LH task _T_ , and experience _D_ MEP to a sequence of subtasks _G_ . 


where _G_ = _{gi}_<sup>_n_</sup> _i_ =1<sup>isthesubtaskspace,eachsubtask</sup><sup>_gi_</sup> satisfies<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_gi⊇T_;</sup><sup>_O_obs represents first-person observations,</sup> _S_ self represents the agent’s self-state, such as health or hunger, and _S_ assets represents agent’s asset library, such as tools; _st_ represents the current state at step _t_ ; _h_ represents the experience; _rt_ represents the reward obtained by performing action _at_ at state _st_ ; P( _gi_ ) indicates the percentage of subtask _gi_ completion. 

**Subtask planning.** As shown in Fig. 2, we adopt the image tokenizer _fv_ to encode the raw images _Oobs, S_ self _, S_ assets into token embeddings _V_ = _{v_ 1 _, v_ 2 _, ..., vn} ∈_ R<sup>_n×d_</sup> , where _n_ denotes the number of visual tokens and _d_ is the dimensionality 

**Action selection.** The controller utilizes _Mw_ to predict future states and optimize actions: 


where _R_ ( _sτ , aτ , gi_ ) is the goal-aligned reward function, and _γ ∈_ [0 _,_ 1] is the discount factor. _R_ ( _sτ , aτ , gi_ ) considers not only the deterministic latent state and stochastic latent variable based on the current observation states _sτ_ and actions _aτ_ but also a goal embedding derived from the current subtask _gi_ , which is an extension of the DreamerV3 [3] reward. At each time step _t_ , we sample a population of _N_ action sequences _{a_<sup>(</sup> _t_ :<sup>_k_</sup> _t_<sup>)</sup> + _H_<sup>_}_</sup> _k_<sup>_N_</sup> =1<sup>from the action space</sup><sup>_AH_. The world model</sup><sup>_Mw_</sup> is used to predict the future states and compute the expected cumulative reward E _Mw τ_ = _t_<sup>_γτ−tR_(</sup><sup>_sτ, aτ, gi_)</sup> for each �� _t_ + _H_ � sequence. The sequence _a_<sup>_∗_</sup> _t_ : _t_ + _H_<sup>withthehighestrewardsis</sup> selected, and the first action _a_<sup>_∗_</sup> _t_<sup>ofthissequenceisexecuted</sup> in the environment. 

**Self-control.** EvolvingAgent uses a self-verification mechanism to reduce inefficient exploration and achieve efficient 

5 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

**Algorithm 1** Continual World Model 

task execution without human intervention. After executing _at_ , EvolvingAgent interacts with the environment _E_ to collect environment feedback. Then EvolvingAgent uses a selfverification mechanism to determine whether the subtask _gi_ can be terminated. The self-verification mechanism is as follows: 

**Require:** Environment _E_ , LH task _T_ , current state _S_ , MEP 

**Ensure:** _D_ MEPUpdated, world model _D_ MEP _′_<sup>,</sup> _M_<sup>_M_</sup> _w′w_ , horizon _H_ , max steps _T_ max 

1: **for** LH Task _T_ = _T_ 0 to _Tn_ **do** 

- 2: Experience-driven task planner via Eq. (13-15) 3: _{gi} ←_ Ψplan( _S, T , D_ MEP) 4: **for** each subtask _gi ∈{gi}_ **do** 5: **for** episode _t_ = 1 to _T_ max **do** 6: WM-guided action controller via Eq. (16-19) 


where _ϕ_ ( _st, gi, t_ ) = 1 indicates that the subtask _gi_ can be terminated; Emb _st_ is the WM-encoded latent representation of the current state _st_ , Emb _gi_ is the task embedding derived from the subtask _gi_ description. Similar to MINEDOJO [13], we trained a contrastive video-language model pre-trained on the multimodal experience pool. It computes the cosine similarity cos( _·_ ) between an open-vocabulary language goal embedding Emb _gi_ and an 8-frame video snippet embedding Emb _st_ , which is used to measure goal attainment with threshold _σ_ set empirically. _T_ max is the maximum allowed steps of each episode. When a subtask _gi_ is completed or the subtask _gi_ completion cycle exceeds the maximum step length _T_ max, the subtask _gi_ is terminated and the experience-driven task planner is performed again. 

- 7: _{at_ : _t_ + _H } ←_ Πact( _st, gi, Mw_ ) 

- 9:8: **if** _ϕD_ (MEP _′st, g_<sup>_←D_</sup> _i, t_ ) is<sup>MEP</sup> Terminal<sup>_∪{⟨st, a_</sup> **then**<sup>_t, rt, st_+1</sup><sup>_,_P(</sup><sup>_g_</sup> _i_<sup>)</sup><sup>_|gi⟩}_</sup> 

- 10: BREAK 

- 11: **end if** 

- 12: **end for** 

- 13: CL-based reflector via Eq. (20-26) 14: _Dk_<sup>subtask</sup> _←_ Curriculum <u>Subtask Select(</u> _Gt, T , D_ MEP) 15: _Dk_<sup>exp</sup> _′ ←_ Curriculum <u>Experience Select(</u> _Dk_<sup>subtask</sup> ) 16: _Mw_<sup>_←_Φreflect(</sup><sup>_D_</sup> _k_<sup>exp</sup><sup>_, Mw_)</sup> 17: **end for** 18: **end for** 

If the subtask _gi_ is terminated, whether it is successful or exceeds the step threshold, � _⟨st, at, rt, st_ +1 _,_ P( _gi_ ) _|gi⟩_ � _t_<sup>is</sup> added to the multimodal experience pool _D_ MEP. 

where cos(Emb _gi,_ Emb _Tgoal_ ) represents the cosine similarity of task embedding. _λ_ 1 + _λ_ 2 + _λ_ 3 + _λ_ 4 = 1 are balancing coefficients. Finally, in round _k_ , _|Dk_<sup>subtask</sup> _|_ subtasks are selected. 


where _cs_ controls the curriculum subtask progression rate. 

## _C. CL-based Reflector_ 

**Stage 2: curriculum experience selection.** For candidate experience _h ∈DMEP_ in selected subtasks _Dk_<sup>subtask</sup> , we use three indicators for curriculum experience selection: (1) the Temporal Difference Error (TD-Error) _δ_ TD( _hj_ ), prioritizes experience with high TD-Error, indicating prediction mismatch between current and target world models; (2) the Gradient Norm _∥∇Mw L_ pred( _hj_ ) _∥_ , favors experiences that maximally influence the world model’s parameter updates; (3) the Information Gain, measures how much the experience _hj_ changes the world model’s belief distribution, calculated via KL divergence between current _M_<sup>new</sup> _w_<sup>(</sup><sup>_sj_+1</sup><sup>_|hj_)andprevious</sup><sup>_M_old</sup> _w_<sup>(</sup><sup>_sj_+1</sup><sup>_|hj_)</sup> world model predictions. 

The CL-based reflector Φreflect is formalized as a function that maps the current state _S_ , subtask _G_ , and the multimodal experience _D_ MEP to update the world model from _Mw_ to _M_<sup>_′_</sup> _w_<sup>.</sup> 


Φreflect employs a two-stage CL algorithm to optimize experience selection, which can enable agents to efficiently update the world model without human intervention as the agent interacts dynamically with the environment. 

**Stage 1: curriculum subtask selection.** For candidate subtasks _gi ∈G_ , we use four indicators for curriculum subtask selection: (1) the relevance of the subtask _gi_ to the current target task _Tgoal_ ; (2) the exploration efficiency of the subtask _gi_ (the ratio of successful step length Step<sup>suc</sup> _gi_<sup>tototalsteplength</sup> Step<sup>all</sup> _gi_<sup>);(3)theimportanceofthesubtask</sup><sup>_gi_(comparingits</sup> impact on the current world model _M_<sup>new</sup> _w,gi_<sup>and</sup><sup><u>past</u>world</sup> model _M_<sup>old</sup> _w,gi_<sup>);(4)theaveragecompletionratio</sup> P( _gi_ ) of the subtask _gi_ . 


where _η_ 1 + _η_ 2 + _η_ 3 = 1 are balancing coefficients. Finally, in round _k_ , _|Dk_<sup>exp</sup><sup>_|_experiencesareselected.</sup> 

Therefore, the priority score _τ_ ( _gi_ ) of the subtask _gi_ can be defined as follows: 


**Self-reflection.** Update the world model _Mww_ using experiences _Dkk_<sup>exp</sup> with importance-aware weight _wjj_ : 

6 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

TABLE I: The results of all the methods on the Minecraft. The evaluation metrics are the average success rate (SR) and the average exploration efficiency (EE) (as shown in Eq. 12). Upper EE metrics mean that the agent is more efficient at completing the task with fewer invalid exploration steps, while 0 _._ 00 indicates that the agent is unable to complete the task. The Overall represents the average result on the three groups of Iron , Gold , and Diamond . The Improving represents the average performance improvement of EvoAgent compared to the algorithms Jarvis-1, dreamerV3, LS-Imagine, and Optimus-1. The best results are in bold. 

|**Group**|**Metric**|**PPO**|**GPT-4V**|**Jarvis-1**|**DreamerV3**|**LS-Imagine**|**Optimus-1**|**EvoAgent**|**Improving** (%)|
|---|---|---|---|---|---|---|---|---|---|
||SR_↑_|28.16|35.24|89.73|91.07|95.87|96.39|**97.47**|4.51 _↑_|
|Wood|EE_↑_|53.82|69.45|87.36|93.22|97.41|97.82|**98.43**|4.77 _↑_|
||SR_↑_|13.42|14.39|81.91|86.82|91.50|88.79|**94.53**|8.34 _↑_|
|Stone|EE_↑_|27.56|30.64|84.72|88.39|92.36|89.25|**96.48**|8.80 _↑_|
||SR_↑_|0.00|0.00|42.38|33.79|35.82|45.48|**51.82**|3.16 _↑_|
|Iron|EE_↑_|0.00|0.00|47.52|35.68|38.27|46.16|**58.54**|39.67 _↑_|
||SR_↑_|0.00|0.00|8.84|6.57|6.61|10.62|**21.69**|**165.81** _↑_|
|Gold|EE_↑_|0.00|0.00|9.76|8.05|10.69|8.03|**30.48**|233.75 _↑_|
||SR_↑_|0.00|0.00|7.69|4.73|4.36|9.30|**17.36**|166.26 _↑_|
|Diamond|EE_↑_|0.00|0.00|0.07|3.69|4.19|7.31|**26.83**|**603.28** _↑_|
|Overall|SR_↑_|0.00|0.00|19.64|15.03|15.60|21.80|**30.29**|**111.74** _↑_|


where _wj_ to emphasize critical experiences, and Ω to penalize shifts in parameters critical for past tasks. _Fi_ is the Fisher information matrix diagonal. 

TABLE II: The sensitivity analysis of the hyperparameter _σ_ . 

|_σ_|0.825|0.85|0.875|0.9|0.925|0.95|
|---|---|---|---|---|---|---|
|SR|17.03|34.48|48.69|52.43|47.72|26.74|


## V. EXPERIMENTS 

In this section, we conduct experiments on Minecraft to verify the performance of EvolvingAgent. We also include detailed ablation studies to analyze the effectiveness of each component, sensitivity analysis to evaluate the contribution of each indicator, and generalization analysis to test the generalization ability. 

## _A. Experimental Setting_ 

**Simulators** . We use Minecraft [13] to evaluate EvolvingAgent. Minecraft features a procedurally generated 3D world of different biomes, which consists of 1-meter-sized blocks that the player can break and place. There are about 30 different creatures that the player can interact with or fight. We employ MineRL 0.4.4 with Minecraft as our simulation environment. The agent operates at a fixed speed of 20 frames per second and only interacts with the environment via low-level control signals. Optimus-1 [11] constructs a benchmark of 67 tasks to evaluate the Agent’s ability for LH tasks. We use the same task group partitioning as the Optimus-1 to evaluate EvolvingAgent. We also evaluate the cross-environment generalization of our method on Atari100k. Atari100k [14] is a standard reinforcement learning benchmark based on the Arcade Learning Environment, covering a diverse set of Atari 2600 games under a limited interaction steps. 

**Hyperparameters** . EvolvingAgent is designed based on the codebase of dreamerV3 [3]. The planner of EvolvingAgent 

uses the VQ-GAN [41] and GPT-4o for task planning. The controller of EvolvingAgent is based on the RSSM-based WM structure [3] for action selection. For detailed hyperparameters, please refer to the Appendix A. Among them, about the selfverification threshold _σ_ , we perform a sensitivity analysis by running our agent in Minecraft with 10<sup>7</sup> environment steps for the task ”Iron”. as shown in Table II, experimental results show that the task success rate remains stable when _σ ∈_ [0 _._ 875 _,_ 0 _._ 925], with sharp declines outside this range due to over/under-termination. When _σ<_ 0 _._ 875, sub-tasks may not be completed but are misjudged, causing subsequent tasks to fail. When _σ>_ 0 _._ 925, due to strict self-verification, sub-tasks may be completed but still require re-planning, reducing the task completion rate. 

**Training.** EvolvingAgent runs on a single A100 GPU. Taking 10<sup>7</sup> steps as an example, compared to dreamerV3 running for 7 days, EvolvingAgent only needs to run for 2.7 days. 

**LLM API Call** . LLM API calls occur in two processes: subtask planning and planner fine-tuning. As the agent selfevolves, the number of subtask failures decreases, which greatly reduces the overhead of planner fine-tuning. Throughout the experiment, with an average of 750 planning calls over 10<sup>7</sup> environment steps. 

**Baselines.** We compare EvolvingAgent with existing outperforming agents, including model-free Agent (PPO [42]), WM-based agents (dreamerV3 [3], LS-Imagine [43]) and LLMbased agents (GPT-4V, Jarvis-1 [10], Optimus-1 [11]) on the challenging LH tasks cross-environments. We do not consider 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

7 

TABLE III: Ablation study results. We report the average success rate (SR) on each task group. P.<sup>_−_</sup> , P., C., R.<sup>1</sup> , R.<sup>2</sup> , R., and CWM represent Planner without LoRA, Planner with LoRA, Controllor, Reflector only with stage 1, Reflector only with stage 2, Reflector with both stages, and Continual World Model, respectively. The PPO algorithm is used by default for model decision-making. Numbers after the _±_ signs represent standard deviations. The best results are in bold. 

||||**Setti**|**ng**|||||**Tasks**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|P.<sup>_−_</sup>|P.|C.|R.<sup>1</sup>|R.<sup>2</sup>|R.|CWM|Wood|Stone|Iron|Gold|Diamond|
||||||||28.16_±_6_._01|13.42_±_7_._62|0.00_±_0_._00|0.00_±_0_._00|0.00_±_0_._00|
|�|||||||41.36_±_5_._20|16.27_±_8_._32|0.00_±_0_._00|0.00_±_0_._00|0.00_±_0_._00|
||�||||||45.69_±_5_._12|18.37_±_6_._71|0.00_±_0_._00|0.00_±_0_._00|0.00_±_0_._00|
||�|�|||||92.42_±_3_._31|85.31_±_5_._96|31.59_±_6_._72|5.47_±_2_._46|3.52_±_2_._31|
||�|�|�||||93.18_±_2_._86|87.72_±_5_._74|34.63_±_5_._19|8.68_±_2_._72|5.14_±_2_._51|
||�|�||�|||95.37_±_2_._48|91.26_±_3_._86|39.58_±_5_._08|14.20_±_4_._05|8.93_±_3_._73|
||�|�|||�||96.69_±_2_._24|93.82_±_3_._34|42.61_±_4_._80|17.53_±_5_._18|10.09_±_3_._54|
||�|�|||�|�|**97.47**_±_1_._75|**94.53**_±_2_._82|**51.82**_±_4_._60|**21.69**_±_4_._61|**17.36**_±_2_._34|


agents that are completely based on human data and curricula support (such as Voyager [9], DEPS [44], and Steve-Eye [45]). 

## _B. Quantitative Results and Analysis_ 

As shown in Table I, EvolvingAgent achieves state-of-the-art success rates (SR) and exploration efficiency (EE) across all resource tiers. Compared with existing methods, EvolvingAgent can achieve an average success rate improvement of **111.74%** and reduce ineffective actions by more than **6x** . 

For basic tasks (Wood/Stone), EvolvingAgent marginally outperforms Optimus-1 (97.47% vs. 96.39% SR on Wood) but exhibits significantly greater advantages in advanced tasks like Gold (21.69% vs. 10.62% SR) and Diamond (17.36% vs. 9.30% SR). This hierarchy-aligned improvement suggests EvolvingAgent’s planner-controller-reflector closed-loop dynamic effectively addresses LH dependencies, where traditional model-based methods (DreamerV3 and LS-Imagine) and LLMdriven agents (Jarvis-1) struggle to maintain coherent multistage strategies. Notably, the EE reveals EvolvingAgent’s exploration superiority: its 30.48% EE on Gold tasks is 3.8× higher than Optimus-1, indicating reduced invalid actions. 

Model-free methods (PPO) and pure vision-language models (GPT-4V) fail completely (0% SR/EE) on tasks requiring tool hierarchies (Iron+), highlighting their inability to model latent state transitions. While Jarvis-1 and DreamerV3 achieve partial success on intermediate tasks (42.38% SR on Iron), their performance collapses on Gold/Diamond tiers due to compounding errors in action sequences. LS-Imagine, through a hybrid approach of short-term and long-term imagination, significantly outperforms DreamerV3 in SR and EE metrics on the basic Wood/Stone task. However, its performance growth is slow on complex tasks because accumulated errors can mislead the optimization direction. EvolvingAgent with 26.83% EE on Diamond tasks, 7.3× higher than Optimus-1, underscores how CL-based experience selection mitigates exploration bottlenecks in sparse-reward scenarios. 

## _C. Ablation Studies_ 

The ablation study reveals critical insights into the contributions of each components (Planner without LoRA, Planner with LoRA, Controller, Reflector only with stage 1, Reflector only with stage 2, Reflector with both stages) and Continual WM for LH tasks. We selected 10 random seeds for testing. Table III shows the mean and variance of the average success rate (SR) for each ablation study. When only PPO is used without any modules (first row), the agent fails to progress beyond basic tasks (28.16% SR for Wood, 0% for Iron+). Introducing the Planner module nearly doubles performance on Wood (45.69%) and marginally improves Stone (18.37%), but still fails to unlock advanced tasks (Iron+ at 0%), suggesting that planner alone cannot resolve the exploration bottleneck in LH tasks. A pivotal leap occurs when Controller is added (P+C), with Wood and Stone success rates surging to 92.42% and 85.31%, respectively, and modest progress in Iron (31.59%). This underscores the necessity of structured exploration to navigate intermediate dependencies. However, the sharp decline in Gold (5.47%) and Diamond (3.52%) indicates persistent challenges in sparse reward scenarios. Integrating the Reflector module (P+C+R) achieves near-perfect Wood/Stone success (96.69%/93.82%) and significantly boosts Iron (42.61%), Gold (17.53%), and Diamond (10.09%), demonstrating its role in distilling exploration experiences to refine world models. 

This experiment compares the results of Planner with LoRA and Planner without LoRA, demonstrating that planner finetuning can significantly improve model convergence speed, reduce the number of invalid subtasks, and achieve autonomous task decomposition. We compare the effects of Reflector with stage 1 only, Reflector with stage 2 only, and Reflector with both stages. The experimental results show that combining curriculum subtask selection with curriculum experience selection can significantly improve the model’s average performance. EvolvingAgent is an improvement over DreamerV3. As shown in Fig. 3, EvolvingAgent is significantly better than DreamerV3 in path selection, which can complete subtasks in the fewest 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

8 


Fig. 3: Illustration of the role of CL-based reflector. Take the subtask ”Craft a stone axe” as an example. 

TABLE IV: The sensitivity analysis about indicators in the curriculum subtask selection (Eq. 21): Relevance (R.), Efficiency (E.), Importance (I.), and Completion Rate (C.R.); indicators in the curriculum experience selection (Eq. 23): TD-Error (TD-R.), Gradient Norm (G.N.), and Information Gain (I.G.); indicators in the self-reflection (Eq. 25): Curriculum Loss (C.L.) and Regularization (R.). We report the average success rate on the task ”Iron” group. 

|**Equation**||**Indic**|**ators**||**SR**|
|---|---|---|---|---|---|
||R.|E.|I.|C.R.|Iron|
|**Equation 21**|�<br>�<br>�|�<br>�|�||40.16<br>41.77<br>46.54|
||�|�|�|�|**49.37**|
|||TD-R.|G.N.|I.G.|Iron|
|||�|||42.47|
|**Equation 23**||�|�||45.59|
|||�|�|�|**50.43**|
||||C.L.|R.|Iron|
|**Eti25**|||�||48.61|
|**quaon **|||�|�|**50.92**|


steps. This is because CL-based reflectors can efficiently update the world model through subtask selection and experience selection, reducing the impact of redundant experience on the world model update. EvolvingAgent with the CL-based reflector can greatly reduce invalid exploration and accelerate task completion. 

## _D. Sensitivity Analysis_ 

We further examine the effect of different indicators in curriculum subtask selection, curriculum experience selection, and self-reflection on the _Iron_ task group. As shown in Table IV, adding more indicators consistently improves the success rate in all three parts. For curriculum subtask selection, introducing relevance, efficiency, importance, and completion ratio gradually raises the success rate from 40.16% to 49.37%, showing that effective subtask prioritization requires not only task similarity but also execution feedback and world-model variation. For curriculum experience selection, combining TD-Error, gradient norm, and information gain improves the 

TABLE V: The generalization analysis in Atari100k. 

|**Task**|**Human**|**PPO**|**DreamerV3**|**EvoAgent**|
|---|---|---|---|---|
|Steps|—|400K|400K|400K|
|Alien|7128|276|1118|**1392**|
|Amidar|1720|26|97|**329**|
|Assault|742|327|683|**981**|
|Asterix|8503|292|1062|**1492**|
|Bank Heist|753|14|**398**|362|
|Battle Zone|37188|2233|20300|**24830**|
|Boxing|12|3|82|**91**|
|Breakout|30|3|10|**13**|
|Chopper Command|7388|1005|2222|**4375**|
|Crazy Climber|35829|14675|**86225**|78215|
|Demon Attack|1971|160|577|**1205**|
|Freeway|30|2|0|**5**|
|Frostbite|4335|127|3377|**3674**|
|Gopher|2412|368|2160|**2219**|
|Hero|30826|2596|**13354**|12168|
|Jamesbond|303|41|540|**621**|
|Kangaroo|3035|55|2643|**2753**|
|Krull|2666|3222|8171|**10027**|
|Kung Fu Master|22736|2090|25900|**28692**|
|Ms Pacman|6952|366|1521|**3246**|
|Pong|15|-20|-4|**-2**|
|Private Eye|69571|100|3238|**5285**|
|Qbert|13544|317|2921|**4793**|
|Road Runner|7845|602|19230|**21703**|
|Seaquest|42055|305|962|**2305**|
|Up N Down|11693|1502|**46910**|37284|


success rate from 42.47% to 50.43%, indicating that informative experiences should be selected from prediction discrepancy, update influence, and knowledge increment simultaneously. For self-reflection, adding regularization to curriculum loss further improves the success rate from 48.61% to 50.92%, suggesting that stable world-model updating is important for reliable long-horizon task completion. 

## _E. Generalization Analysis_ 

We further evaluate the cross-environment generalization of EvolvingAgent on Atari100k after training in Minecraft. As shown in Table V, EvolvingAgent consistently outperforms DreamerV3 under the same 400K interaction steps on most Atari tasks, including Alien, Assault, Asterix, Battle Zone, Ms Pacman, and Road Runner. It also reaches or exceeds humanlevel performance on several games such as Boxing, Krull, and Kung Fu Master. These results indicate that the continual world model learned by EvolvingAgent captures transferable dynamics and control priors rather than environment-specific patterns only. This cross-domain advantage supports the robustness and scalability of EvolvingAgent under substantial environment shifts. 

## VI. CONCLUSION 

This paper presents EvolvingAgent, an embodied agent that improves long-horizon task execution through curriculum 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

9 

self-evolution. EvolvingAgent integrates an experience-driven task planner, a WM-guided action controller, and a CL-based reflector to continuously refine subtask scheduling, experience selection, and world model updating during interaction. This design enables more reliable planning and execution in openended environments. In the future, we hope that our method can be truly applied to real robot scenarios. 

## REFERENCES 

- [1] T. Feng, X. Wang, F. Han, L. Zhang, and W. Zhu, “U2udata+: A scalable swarm uavs autonomous flight dataset for embodied long-horizon tasks,” _Thirtieth AAAI Conference on Artificial Intelligence_ , 2025. 

- [2] Y. Shen, H. Liu, P. Liu, R. Xia, T. Yao, Y. Sun, and T. Feng, “Detach: Cross-domain learning for long-horizon tasks via mixture of disentangled experts,” _arXiv preprint arXiv:2508.07842_ , 2025. 

- [3] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse control tasks through world models,” _Nature_ , pp. 1–7, 2025. 

- [4] T. Kwa, B. West, J. Becker, A. Deng, K. Garcia, M. Hasin, S. Jawhar, M. Kinniment, N. Rush, S. Von Arx _et al._ , “Measuring ai ability to complete long tasks,” _arXiv preprint arXiv:2503.14499_ , 2025. 

- [5] P. Ren, K. Zhang, H. Zheng, Z. Li, Y. Wen, F. Zhu, S. Ma, and X. Liang, “Surfer: A world model-based framework for vision-language robot manipulation,” _IEEE Transactions on Neural Networks and Learning Systems_ , 2025. 

- [6] M. Seo, H. A. Park, S. Yuan, Y. Zhu, and L. Sentis, “Legato: Crossembodiment imitation using a grasping tool,” _IEEE Robotics and Automation Letters_ , 2025. 

- [7] Z. Li, Y. Xie, R. Shao, G. Chen, D. Jiang, and L. Nie, “Optimus-2: Multimodal minecraft agent with goal-observation-action conditioned policy,” in _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , June 2025, pp. 9039–9049. 

- [8] S. Zhang, Z. Xu, P. Liu, X. Yu, Y.-Y. Li, Q. Gao, Z. Fei, Z. Yin, Z. Wu, Y.-G. Jiang, and X. Qiu, “Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks,” in _ICML_ , 2024. 

- [9] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar, “Voyager: An open-ended embodied agent with large language models,” _arXiv preprint arXiv:2305.16291_ , 2023. 

- [10] Z. Wang, S. Cai, A. Liu, Y. Jin, J. Hou, B. Zhang, H. Lin, Z. He, Z. Zheng, Y. Yang, X. Ma, and Y. Liang, “Jarvis-1: Open-world multi-task agents with memory-augmented multimodal language models,” _ArXiv_ , 2023. 

- [11] Z. Li, Y. Xie, R. Shao, G. Chen, D. Jiang, and L. Nie, “Optimus-1: Hybrid multimodal memory empowered agents excel in long-horizon tasks,” 2024. 

- [12] S. Nayak, A. M. Orozco, M. T. Have, V. Thirumalai, J. Zhang, D. Chen, A. Kapoor, E. Robinson, K. Gopalakrishnan, J. Harrison, B. Ichter, A. Mahajan, and H. Balakrishnan, “LLaMAR: Long-Horizon Planning for Multi-Agent Robots in Partially Observable Environments,” _International Conference on Machine Learning (ICML)_ , 2025. 

- [13] L. Fan, G. Wang, Y. Jiang, A. Mandlekar, Y. Yang, H. Zhu, A. Tang, D.-A. Huang, Y. Zhu, and A. Anandkumar, “Minedojo: Building open-ended embodied agents with internet-scale knowledge,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 18 343–18 362, 2022. 

- [14] M. G. Bellemare, Y. Naddaf, J. Veness, and M. Bowling, “The arcade learning environment: An evaluation platform for general agents,” _Journal of artificial intelligence research_ , vol. 47, pp. 253–279, 2013. 

- [15] J. Zhou, Q. Wu, H. Jiang, X. Qin, Y. Lou, X. Xiong, and R. Xu, “Gentle manipulation of long-horizon tasks without human demonstrations,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 3, pp. 2538–2545, 2026. 

- [16] M. Medany, L. Piglia, L. Achenbach, S. K. Mukkavilli, and D. Ahmed, “Model-based reinforcement learning for ultrasound-driven autonomous microrobots,” _Nature Machine Intelligence_ , pp. 1–15, 2025. 

- [17] M. Krinner, E. Aljalbout, A. Romero, and D. Scaramuzza, “Accelerating model-based reinforcement learning with state-space world models,” _arXiv preprint arXiv:2502.20168_ , 2025. 

- [18] A. Roger, P. Humane, D. Z. Kaplan, K. Gupta, Q. Sun, G. Adamopoulos, J. S. C. Lim, Q. Anthony, E. Fennell, and I. Rish, “Robin: a suite of multi-scale vision-language models and the chirp evaluation benchmark,” in _ICLR_ , 2025. 

- [19] T. Hu, X. Liu, S. Wang, Y. Zhu, A. Liang, L. Kong, G. Zhao, Z. Gong, J. Cen, Z. Huang _et al._ , “Vision-language-action models for autonomous driving: Past, present, and future,” _arXiv preprint arXiv:2512.16760_ , 2025. 

- [20] S. Liu, J. Du, S. Xiang, Z. Wang, and D. Luo, “Relep: A novel framework for real-world long-horizon embodied planning,” _ArXiv_ , 2024. 

- [21] Z. Lou, K. Xu, Z. Zhou, and R. Xiong, “Explorevlm: Closed-loop robot exploration task planning with vision-language models,” _arXiv preprint arXiv:2508.11918_ , 2025. 

- [22] Z. Yang, C. Garrett, D. Fox, T. Lozano-Perez,´ and L. P. Kaelbling, “Guiding long-horizon task and motion planning with vision language models,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 16 847–16 853. 

- [23] Y. Mu, Q. Zhang, M. Hu, W. Wang, M. Ding, J. Jin, B. Wang, J. Dai, Y. Qiao, and P. Luo, “Embodiedgpt: vision-language pre-training via embodied chain of thought,” in _Proceedings of the 37th International Conference on Neural Information Processing Systems (NeurIPS)_ , 2023. 

- [24] T. Feng, X. Wang, Y.-G. Jiang, and W. Zhu, “Embodied ai: From llms to world models,” _IEEE Circuits and Systems Magazine_ , 2025. 

- [25] D. Ha and J. Schmidhuber, “World models,” _arXiv preprint arXiv:1803.10122_ , 2018. 

- [26] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus _et al._ , “V-jepa 2: Self-supervised video models enable understanding, prediction and planning,” _arXiv preprint arXiv:2506.09985_ , 2025. 

- [27] M. Hassan, S. Stapf, A. Rahimi, P. Rezende, Y. Haghighi, D. Bruggemann,¨ I. Katircioglu, L. Zhang, X. Chen, S. Saha _et al._ , “Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 22 404– 22 415. 

- [28] S. Zuo, W. Zheng, Y. Huang, J. Zhou, and J. Lu, “Gaussianworld: Gaussian world model for streaming 3d occupancy prediction,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 6772–6781. 

- [29] P. Mattes, R. Schlosser, and R. Herbrich, “Hieros: Hierarchical imagination on structured state space sequence world models,” _International Conference on Machine Learning (ICML)_ , 2023. 

- [30] R. Sun, H. Zang, X. Li, and R. Islam, “Learning latent dynamic robust representations for world models,” _International Conference on Machine Learning (ICML)_ , 2024. 

- [31] L. Xiao, X. Yang, F. Peng, M. Yan, Y. Wang, and C. Xu, “Clip-vg: Self-paced curriculum adapting of clip for visual grounding,” _IEEE Transactions on Multimedia_ , vol. 26, pp. 4334–4347, 2023. 

- [32] J. Xiao, L. Li, D. Xu, C. Long, J. Shao, S. Zhang, S. Pu, and Y. Zhuang, “Explore video clip order with self-supervised and curriculum learning for video applications,” _IEEE Transactions on Multimedia_ , vol. 23, pp. 3454–3466, 2020. 

- [33] Y. Dai, B. Chen, L. Gao, J. Song, and H. T. Shen, “Dmh-cl: Dynamic model hardness based curriculum learning for complex pose estimation,” _IEEE Transactions on Multimedia_ , vol. 26, pp. 3180–3193, 2023. 

- [34] X. Li, L. Jiao, Q. Sun, F. Liu, X. Liu, L. Li, P. Chen, and S. Yang, “A category-aware curriculum learning for data-free knowledge distillation,” _IEEE Transactions on Multimedia_ , vol. 26, pp. 9603–9618, 2024. 

- [35] S. Mai, Y. Sun, and H. Hu, “Curriculum learning meets weakly supervised multimodal correlation learning,” in _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_ , 2022, pp. 3191– 3203. 

- [36] Y. Zhou, Z. Pan, X. Wang, H. Chen, H. Li, Y. Huang, Z. Xiong, F. Xiong, P. Xu, W. Zhu _et al._ , “Curbench: curriculum learning benchmark,” in _Forty-first International Conference on Machine Learning_ , 2024. 

- [37] G. Meng, Q. Zeng, J. P. Lalor, and H. Yu, “A psychology-based unified dynamic framework for curriculum learning,” _Computational Linguistics_ , pp. 1–49, 2025. 

- [38] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Learning latent dynamics for planning from pixels,” _International Conference on Machine Learning (ICML)_ , 2019. 

- [39] W. Guo, Z. K. Kingston, and L. E. Kavraki, “Castl: Constraints as specifications through llm translation for long-horizon task and motion planning,” _ArXiv_ , 2024. 

- [40] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen _et al._ , “Lora: Low-rank adaptation of large language models.” _ICLR_ , vol. 1, no. 2, p. 3, 2022. 

- [41] P. Esser, R. Rombach, and B. Ommer, “Taming transformers for highresolution image synthesis,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2021, pp. 12 873–12 883. 

- [42] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” 2017. 

- [43] J. Li, Q. Wang, Y. Wang, X. Jin, Y. Li, W. Zeng, and X. Yang, “Openworld reinforcement learning over long short-term imagination,” in _ICLR_ , 2025. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

10 

- [44] Z. Wang, S. Cai, G. Chen, A. Liu, X. Ma, and Y. Liang, “Describe, explain, plan and select: Interactive planning with large language models enables open-world multi-task agents,” _arXiv preprint arXiv:2302.01560_ , 2023. 

- [45] S. Zheng, J. Liu, Y. Feng, and Z. Lu, “Steve-eye: Equipping llm-based embodied agents with visual perception in open worlds,” _arXiv preprint arXiv:2310.13255_ , 2023. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

11 

APPENDIX 

All hyperparameters of EvolvingAgent are shown in the Table VI. 

TABLE VI: EvoAgent hyperparameters. 

|**Gen**|**eral**||
|---|---|---|
|Replay capacity|—|5_×_10<sup>6</sup>|
|Batch size|_B_|16|
|Batch length|_T_|64|
|Activation|—|RMSNorm + SiLU<br>|
|Learning rate|—|4_×_10<sup>_−_5</sup>|
|Gradient clipping|—|AGC(0.3)<br>|
|Optimizer|—|LaProp(_ϵ_= 10<sup>_−_20</sup>)|
|**World **|**Model**||
|Reconstruction loss scale|_β_pred|1|
|Dynamics loss scale|_β_dyn|1|
|Representation loss scale|_β_rep|0.1|
|Latent unimix|—|1%|
|Free nats|—|1|
|**Actor **|**Critic**||
|Imagination horizon|_H_|15|
|Discount horizon|1_/_(1_−γ_)|333|
|Return lambda|_λ_|0.95|
|Critic loss scale|_β_val|1|
|Critic replay loss scale|_β_repval|0.3|
|Critic EMA regularizer|—|1|
|Critic EMA decay|—|0.98|
|Actor loss scale|_β_pol|1|
|Actor entropy regularizer|_η_|3_×_10<sup>_−_4</sup>|
|Actor unimix|—|1%|
|Actor RetNorm scale|_S_|Per(_R,_95)_−_Per(_R,_5)|
|Actor RetNorm limit|_L_|1|
|Actor RetNorm decay|—|0.99|
|**WM-Guided A**|**ction Control**|**ler**|
|Maximum episode step length|_Tmax_|24000|
|Task similarity threshold|_σ_|0.9|
|Rewarddiscountfactor|_γ_|0.1|
|<br>**CL-based**|**Reflector**||
|CL algorithm initialization threshold|_ρ_0|5_×_10<sup>_−_3</sup>|
|CL subtask selection increase rate|_cs_|0.3|
|CL experience selection increase rate|_ch_|0.5|
|World model penalize weight|_µ_|0.1|


