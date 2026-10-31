---
title: "Affordances Enable Partial World Modeling with LLMs"
date: "2026-02-11"
authors: "Khimya Khetarpal; Gheorghe Comanici; Jonathan Richens; Jeremy Shar; Fei Xia; Laurent Orseau"
url: https://arxiv.org/abs/2602.10390
pdf: https://arxiv.org/pdf/2602.10390
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.10390)** / [論文ページ](https://arxiv.org/abs/2602.10390)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Affordances Enable Partial World Modeling with LLMs** 

**Khimya Khetarpal**<sup>1</sup> **Gheorghe Comanici**<sup>1</sup> **Jonathan Richens**<sup>1</sup> **Jeremy Shar**<sup>1</sup> **Fei Xia**<sup>1 2</sup> **Laurent Orseau**<sup>1</sup> **Aleksandra Faust**<sup>1</sup> **Doina Precup**<sup>1</sup> 

# **Abstract** 

Full models of the world require complex knowledge of immense detail. While pre-trained large models have been hypothesized to contain similar knowledge due to extensive pre-training on vast amounts of internet scale data, using them directly in a search procedure is inefficient and inaccurate. Conversely, partial models focus on making high quality predictions for a subset of state and actions: those linked through affordances that achieve user intents (Khetarpal et al., 2020). Can we posit large models as partial world models? We provide a formal answer to this question, proving that agents achieving task-agnostic, language-conditioned intents necessarily possess predictive partial-world models informed by affordances. In the multi-task setting, we introduce distribution-robust affordances and show that partial models can be extracted to significantly improve search efficiency. Empirical evaluations in tabletop robotics tasks demonstrate that our affordance-aware partial models reduce the search branching factor and achieve higher rewards compared to full world models. 

# **1. Introduction** 

A key challenge in artificial intelligence (AI) research is to build agents that can generalize across tasks. Multi-task reinforcement learning addresses this by leveraging the shared underlying structure across a distribution of tasks. Agents that can generalize across a variety of such sub-tasks have the potential to solve complex, long horizon, tasks. Similar to humans, it is desirable that AI agents are able to represent world knowledge and understand the dynamics of the world. Model-based reinforcement learning (MBRL) (Sutton & Barto, 2018) offers a family of approaches that build a transition dynamics model of the environment (i.e. the MDP’s transition function), referred to as a world model, which can 

1Google Deepmind 2Work done at Google Deepmind. Correspondence to: Khimya Khetarpal <khimya@google.com>. 

_Preprint. February 12, 2026._ 

then be used for planning. While traditional MBRL often relies on interacting with simulators (online) (Kakade, 2003) or static datasets (offline), recent work suggests that learning abstract models across tasks can significantly enhance performance (Hafner et al., 2024). 

With the advent of the large models, whose representations are trained on internet-scale knowledge data, it has been hypothesized that knowledge of the kind provided by a world model, e.g. environment transition dynamics, is already available (Yang et al., 2023b; Bruce et al., 2024; Xi et al., 2025). However, work on leveraging such full models in MBRL is in its early stages (Hao et al., 2023; Benechehab et al., 2024; Xi et al., 2025). Some of the hurdles for applying LLMs to MBRL include the mismatch in observation format between RL agents and LLMs (e.g. in a robotics context, proprioception vs text), the expense in querying LLMs (which can make their use in traditional RL planners, such as Monte Carlo Tree Search prohibitive) and especially the inaccuracies of LLM prediction, including hallucinations (which get exacerbated when used in an RL context, because they can derail the policy optimization). 

Conversely, partial models (Talvitie & Singh, 2009) focus on making high quality predictions for a subset of state and actions. To exploit this property, we here study the process of leveraging LLMs as a _partial_ world model. A partial model can guide an RL agent, but its performance as well as inference cost are not a bottleneck, because the LLM is queried only under circumstances where it can provide useful information, which can also be “debugged" by the RL agent itself. Specifically, we use the LLM to guide an _affordance model_ for search and planning. Affordances (Gibson, 1977) arise at the interface of the agent and the environment and represent _action possibilities_ . For AI agents, affordances facilitate adaptive control (Fikes et al., 1972; Korf, 1983; Drescher, 1991), but the agent’s understanding of which states afford which actions also allows it to learn partial world models (Talvitie & Singh, 2009), which only apply in limited circumstances and/or only predict relevant parts of the state. For example, an agent might only model temporally extended transitions that complete certain intents (Khetarpal et al., 2021). In this work, we study the effect of inducing such partial world models by leveraging LLMs as both affordances and generative world models. 

1 

**Affordances Enable Partial World Modeling with LLMs** 

Prior work (Abel et al., 2014; Khetarpal et al., 2021; 2020) has explored affordance-aware partial world models primarily in the context of a single task which is limiting for generalization in the multi-task setting. To address this, we extend the formalism of intents and affordances to a multi-task setting which accounts for the agent, the environment, and distribution of tasks. See Fig. 1 where we present a conceptual framework of affordances in the multitask setting, that considers the distinction between intents internal to an agent embodiment versus the intents specific to tasks presented in conjunction with the environment. The delineation between task-specific and task-agnostic intents (i.e. anchored on agent dynamics) in our framework allows for building affordances that consider both the agent embodiment and the physical workspace i.e. the environment resulting in generalized notion of affordances. Similar delineation of task-agnostic and task-specific has been studied by other works (Shin et al., 2023; Flesch et al., 2022), where the commonality is that task-agnostic intents are tied to unsupervised reward-free signal (Zhang et al., 2020; Burda et al., 2018), while task-specific intents are closely tied to the context (Sodhani et al., 2021). 

In this paper, we bridge the gap between LLM knowledge and robotic planning by proving that agents capable of achieving task-agnostic, language-conditioned intents necessarily possess predictive partial-world models (Theorem 1). We show that these models, informed by distribution-robust affordances, enable provably efficient search by focusing only on relevant state-action transitions (Theorem 2). We demonstrate how to extract these models in multi-task tabletop robotics by applying a generalized notion of affordances to agent-environment interaction. Our key contributions are: 

1. **A multi-task affordance framework** that delineates agent-embodied (task-agnostic) intents from environment-driven (task-specific) intents, enabling robust generalization across a distribution of tasks (Sec. 3). 

2. **Theoretical proofs** establishing that (a) achieving a set of language-conditioned intents implies the existence of an underlying partial world model, and (b) using such models significantly improves search efficiency in long-horizon planning (Theorem 1, Theorem 2; Sec. 4). 

3. **Empirical validation in tabletop robotics** demonstrating that leveraging LLMs as both affordance filters and generative world models reduces the search branching factor and achieves higher rewards compared to full world models (Sec. 5). 

# **2. Preliminaries** 

**Problem Setting.** We consider table-top robotics tasks _T_<sup>1</sup> _, T_<sup>2</sup> _, . . . T_<sup>_N_</sup> drawn from a distribution of related tasks i.e. _T_<sup>_i_</sup> _∼_ Dist( _T_ ), where each task _T_<sup>_i_</sup> = _⟨S, A, r_<sup>_i_</sup> _, P_<sup>_i_</sup> _, γ⟩_ can 

be viewed as a Markov Decision Process (MDP), comprised of a set of states _S_ , a set of actions _A_ , transition dynamics model _P_<sup>_i_</sup> ( _s_<sup>_′_</sup> _|s, a_ ) _∼_ Dist( _P_ ) and reward function _r_<sup>_i_</sup> ( _s_ ) _∼_ Dist( _R_ ), with a fixed distribution of initial states. Robotic tasks typically use fine-grained primitive actions e.g. joint angles of a robot arm, resulting in a complex action space. Therefore, it is common in practice to work with abstract actions (i.e., controllers or options) _o ∈O_ consisting of predefined low level policies for achieving short term goals, e.g. pick up an _orange block_ and place it at location _x, y_ . The coordinates associated with block locations depend on the bounds of the physical workspace of the robot gripper. For a task _T_<sup>_i_</sup> , the dynamics models in this paper focuses on _P_<sup>_i_</sup> ( _s_<sup>_′_</sup> _|s, o_ ), that is, the state _s_<sup>_′_</sup> after execution of the abstract action (or option) _o_ is completed starting at state _s ∈S_ . Equivalently we will use _P_<sup>_i_</sup> ( _τ |s, o_ )) for full trajectories (i.e. all state-actions from the start to the end of an abstract action execution). 

**Model-based Reinforcement Learning (MBRL)** usually considers models of the environment that approximate the true model _r_<sup>_i_</sup> _, P_<sup>_i_</sup> . The focus is typically on models that can produce samples of future states. _M_ ˆ : _⟨r,_ ˆ _P_<sup>ˆ</sup> _⟩_<sup>1</sup> can be leveraged to approximate the optimalAn approximate model policy of the corresponding approximate MDP _M_<sup>ˆ</sup> through a planning or search process. Starting at any state _s_ , the model can be used to generate ‘rollouts‘ or trajectories modeled with _⟨r,_ ˆ _P_<sup>ˆ</sup> _⟩_ and these are used to provide value estimates for action choices ( _s, o_ ) starting at _s_ . The corresponding policy would then select the action with the highest value estimate. Traditionally, world models have been learned from data; during planning, in the setting of a generative model, the model is called repeatedly to generate samples of next states from given states and actions, with the number of calls referred to as the _sample complexity_ . 

**Partial Models.** Learning an accurate model can be quite difficult, requiring a lot of data. Moreover, the model does not need to be accurate everywhere, as long as it is accurate in relevant places, and/or it provides useful information for identifying good actions. A useful approach is to build _partial models_ (Talvitie & Singh, 2009), which only make predictions for specific parts of the state-action space. Partial models come in two flavors: predicting only the outcome of a subset of state-action pairs, or making predictions only about certain parts of the state space. 

**Affordances.** Building on work from Khetarpal et al. (2021), we consider partial models of the world that make predictions about the consequences of abstract actions in a given state _P_<sup>ˆ</sup> ( _s_<sup>_′_</sup> _|s, o_ ) for which we leverage the notions of _intents_ and _affordances_ . 

> 1For simplicity, in this paper we only model transition dynamics _P_<sup>ˆ</sup> and assume the reward function is known through the simulator. 

2 

**Affordances Enable Partial World Modeling with LLMs** 


_Figure 1._ **Generalizing the concept of affordances to a multi-task setting** is achieved by categorizing agent intents as taskagnostic—grounded in the agent’s embodiment, such as a robot’s ability to pick or place objects—and task-specific, which depend on the environment and task distribution. By considering the three primary axes of agent, environment, and task distribution, the interplay between these intents facilitates the emergence of affordances at the boundary of the agent-environment interaction. This framework induces partial world models that effectively generalize across tasks, resulting in provably efficient planning. 

**Definition 1** (Temporally Extended Intent I _o_ (Khetarpal et al., 2021)): _A temporally extended intent of abstract action o ∈O,_ I _o_ : _S → Dist_ (Γ) _specifies for each state s, a probability distribution over the space of trajectories_ Γ _, describing the intended result of executing o in s. The associated intent model (i.e. the intended probability of a trajectory τ when option o is executed from state s) is denoted by PI_ ( _τ |s, o_ ) = _Io_ ( _s, τ_ ) _._ 

**Definition 2** (Degree of intent satisfiability _ζ_ ): _A temporally extended intent_ I _o is satisfied to degree ζ iff d_ ( _PI_ ( _τ |s, o_ ) _, Ptruth_ ( _τ |s, o_ )) _≤ ζ, ∀_ ( _s, o, τ_ )<sup>2</sup> _, where d is a user-specified metric between probability distributions and τ denotes the trajectory starting in state s and following the abstract action o. A set of intents I has satisfiability ζ iff all its elements have satisfiability ζ._ 

Definition 1 describes what an agent expects to happen when it executes an abstract action (e.g. pick-up-orange-block). Rather than defining a single success state, the intent is a distribution over entire trajectories, allowing variability into how a task might be completed. This view is essential in evaluating whether abstract actions are afforded. An intent is "satisfied" (Definition 2)) only when the realized outcome is sufficiently "close" to the true distribution (i.e. true agent-environment specification). 

**Definition 3** ( _ζ_ -affordance (Khetarpal et al., 2021)): _Given a set of temporally extended intents I_ =<sup>�</sup> _o∈O_<sup>I</sup><sup>_o,aζ-_</sup> _affordance set is a subset AF I ⊆S × O, such that d_ ( _PI_ ( _τ |s, o_ ) _, Ptruth_ ( _τ |s, o_ )) _≤ ζ, ∀_ ( _s, o_ ) _∈AF I._ 

An affordance is equivalent to a _selection_ of state-action pairs that are likely to achieve corresponding intents (Definition 1). For example, the robot hand is right next to the block; if it runs the pick-up-block action, 

> 2In the context of multi-task setting, _Ptruth_ is the true distribution associated to a specific task _Ptruth_ ( _·|Ti_ ). 

the block ends up in the gripper, the intent is met and pick-up-block is an affordance. The robot hand is across the room; if it runs the pick-up-block action, it grabs thin air. The intent (block in hand) is not met, hence pick-up-block is _not_ an affordance. 

Large Language Models (LLMs) are trained to learn a distribution of the next tokens conditioned on the contexts from the training data. Interestingly, language generation has been well studied as a sequential decision-making problem and language modeling can indeed be understood as an instance of imitation learning (Arora et al., 2022). LLMs have the potential to do well on various reasoning problems (Valmeekam et al., 2022), albeit using reasoning traces generated in an autoregressive manner. They have also been hypothesized to encode knowledge akin to world models (Hao et al., 2023), due to extensive pre-training on vast amounts of human data. In the following section, we leverage LLMs as approximate dynamics world models _P_ ˆ( _s_<sup>_′_</sup> _|s, o_ ), to predict future states given start state _s_ and an abstract action _o_ . Experimental work will be reported on table top tasks and we assume access to low-level policies for a set of abstract actions. This is departure from prior work (Khetarpal et al., 2020; 2021), where the impact of using affordances to learn partial models was studied in toy domains with hand-designed programs that specified intentcompletion functions and learned _tabula rasa_ . The latter is unfeasible in table-top domains, making it an interesting setting for LLMs as partial models in search and planning. 

# **3. Generalized Affordance Framework** 

We extend the theoretical framework of affordances (Khetarpal et al., 2020) from single-task to multi-task RL. Our approach, illustrated in Fig. 1, centers on three primary axes: the **agent** defined by the robot embodiment e.g. a robot arm gripper, the **environment** defined by the bounds of the robot’s physical workspace e.g. a table top, and the **distribution of tasks** . In this setting, 

3 

**Affordances Enable Partial World Modeling with LLMs** 

sequential decision making tasks are sampled from this distribution _T_<sup>_i_</sup> _∼T_ comprising a set of tasks related to each other. Once defined, the distribution is used for planning and evaluation. While affordances are fundamentally a function of both the agent and the environment (Chemero, 2003; Gibson, 1977), this dependency becomes uniquely pronounced in multi-task scenarios, as detailed in the following sections. 

**Intents.** Formally, we characterize the set of all intents _I_ = _Iagn ∪Itask_ in two classes; 1) **task-agnostic intents** _Iagn_ , which are based on an agent’s internal dynamics, e.g. a robot embodiment, whereas, 2) **task-specific intents** _Itask_ captures the set of intents that the environment or the physical workspace poses, depending on the task presented to the agent. Task-agnostic intents are the robot’s basic skills (what it can physically do), and Task-specific intents are specific desiderata in specific context (what it is trying to achieve right now). Task-agnostic intents can be achieved simply because of how the robot is built (its embodiment) and what is physically in front of it. These intents are general because they do not depend on what the specific task is. When the robot sees a red block, the _pick up red block_ intent is task-agnostic. It does not matter if the robot’s job today is to build a tower, clean the table, or sort by color. As long as the red block is visible and nothing is on top of it, the robot can pick it up. Task-specific intents depend heavily on the high-level task with a certain reward specification. These actions are usually complex combinations that lead to a high reward but are only afforded (possible/valid) in very specific situations. If a the robot is tasked to stack-blocks-while-holding-red-block, and there is a blue block on the table, _stack red block on top of blue block_ intent is taskspecific. This action is only meaningful if the current task is build-a-stack. If the task changed to put-all-blocks-in-a-box, stacking them might be useless or even wrong. 


_(a)_ Task Agnostic Intent _(b)_ Task Specific Intent 

_Figure 2._ **Characterizing intents as task-agnostic and taskspecific in the context of multi-task setting** . For an agent embodiment, a task agnostic intent is satisfied to a degree _ζ_ across the entire task distribution as shown on the left, whereas, a task specific intent doesn’t have the same coverage of satisfiability across the task-distribution as its specific to certain tasks only. 

**Affordances for Multi-Task Setting.** We now characterize the set of state-options pairs, namely affordances, that facil- 

itate the completion of task-agnostic or task-specific intents. Prior research (Khetarpal et al., 2021) has typically ignored the case where we’d need to work with affordances across multiple tasks selected from a fixed distribution. 

Ideally, affordances would allow the agent to transfer knowledge between tasks with shared underlying structure. We extend here the definition to a probabilistic statement regarding the satisfiability of particular intents, grounded directly in the sampling distribution for the given tasks. This allows us to distinguish between **distribution-robust agent affordances** , which remain achievable with high probability across diverse task configurations (e.g., grasping an unobstructed block), and **task-specific affordances** , which may only be satisfied in restricted scenario. For example, in the table-top domain, achieving the intent of grasping a block that has nothing on top should be possible with high probability, consistently across tasks (Fig. 2a), regardless of the block configuration present or desired. However, placing a block inside another one may only be possible in a small number of situations in which there are hollow blocks around of appropriate sizes (Fig. 2b). Intuitively, knowledge that is shared across the distribution facilitates transfer to improve learning speed, whereas task-specific knowledge ensures the agent can maximize value for the current objective. Formally, 

**Definition 4** (Distribution-Robust Agent Affordances): _Given a distribution of tasks Dist_ ( _T_ ) _, a set of temporally extended intents I_ =<sup>�</sup> _o∈O_<sup>I</sup><sup>_o, and constants ζ, δ∈_(0</sup><sup>_,_1)</sup><sup>_,_</sup> _a ζ-affordance set AF I (see Def. 3) is δ-robust to distribution Dist_ ( _T_ ) _iff the probability that the affordance does not satisfy the intent_ I _o to a degree ζ in task T ∼ Dist_ ( _T_ ) _is bounded by δ. That is, ∀s, o ∈AF I_ 


To illustrate, we refer the reader to Fig. 2, which depicts a task agnostic intent that satisfies Def. 4 grounded in the distribution of tasks, and an intent which doesn’t meet the desired criteria resulting in a task-specific intent. 

Building on the multi-task affordance formalism, we realize generalized framework depicted in Fig. 1, where an agent accesses an imperfect abstract world dynamics model _P_ ( _s_<sup>_′_</sup> _|s, o_ ). Unlike naive full world models that inefficiently predict over the entire state-action space—often leading to inaccurate Monte-Carlo planning results (Sec. 5.1)—we induce a _partial world model_ to restrict predictions to a relevant subset. We input the current state and a set of _k_ pre-defined intents _I_ into an affordance model to yield distribution-robust affordances _AF I_ (Def 4). These affordances constrain the world model’s predictions, substan- 

4 

**Affordances Enable Partial World Modeling with LLMs** 

tially reducing the search branching factor and improving action-value estimates for the policy _π_ . While the distribution-robust affordances are relevant across tasks, the agent is implicitly informed of task-specific intents via the reward signal during the subsequent environment interaction. 


_Figure 3._ **Improvements in affordance model accuracy results in better performance of the search policy.** Given a fixed budget for search, a perfect world model, any errors in affordance prediction translates to catastrophic failures in the search policy. 

**Illustration.** To demonstrate the utility of the generalized affordance framework, we evaluate the pipeline shown in Fig. 1 on a 3-block stacking task using a simulated robot arm. By employing a perfect world model (the simulator) alongside programmatic affordances derived from task-agnostic intents, we examine how varying the accuracy of affordable actions affects search efficacy. As shown in Fig. 3, higher affordance model accuracy directly correlates with improved search policy performance (green star). Conversely, misspecified affordances lead to catastrophic failures regardless of the world model’s fidelity, particularly under constrained search budgets (red star). This highlights that since affordances emerge at the boundary of agent-environment interaction, grounding the agent’s affordance beliefs in an adaptive fashion is critical for robust planning. 

# **4. Theoretical Analysis** 

We now provide a theoretical analysis of the multi-task affordance framework. In Sec. 4.1, we establish that achieving a set of intents implies the existence of an underlying partial world model through Theorem 1. In Sec. 4.2, we study the efficiency in search enabled by partial world models. We show that at a small price, adapting the model enjoys the potential exponential speedup of the partial model, while being robust to missing intents from the full model. 

## **4.1. Distribution-Robust Agent Intents induce Partial World Models** 

To facilitate the theoretical analysis of our generalized framework, we specialize the class of sequential tasks under consideration. We follow the standard formalism for 

expressing sequential tasks using linear temporal logic, with a focus on three simple types of tasks: i) _actions_ , taking an (abstract) action _O_ = _o_ , ii) _outcomes_ , achieving a desired outcome from an action, denoted _X_ ( _s ∈ g_ ) where _g ⊆S_ , iii) _goals_ , reaching a goal state _F_ ( _s ∈ g_ ). Here _X_ ( _s ∈ g_ ) requires the desired state(s) _s_ to be reached as an immediate outcome of the previous (abstract) action _O_ = _o_ , and _F_ ( _s ∈ g_ ) requires only that the goal state is reached at some point in the future. For example, stack blocks in r / g / b order, _F_ ( _S ∈ grgb_ ). To denote tasks comprising of sequences of these primitives we use angular brackets e.g. _T_<sup>_i_</sup> = _⟨o, X_ ( _s_ ) _, . . .⟩_ . See Section B.1 for details. For the purposes of our analysis, we define depth-n tasks (Nangue Tasse et al., 2020). 

**Definition 5** (Depth-n tasks): _Given a set of abstract actions O and states S, we consider the set of depth-n tasks T_ ( _n_ ) _to be the set of tasks T_<sup>_i_</sup> _that can be solved by achieving a sequence of at most n actions, outcomes, or goals e.g. T_<sup>_i_</sup> = _⟨oi,_ 0 _, . . . , oi,m⟩ where m ≤ n._ 

**Assumption 1.** _The MDP with transition function P_ ( _s_<sup>_′_</sup> _| o, s_ ) _is communicating (i.e. there exists a policy that gets you from any one state to any other state in a finite number of steps with non-zero probability) (Bartlett & Tewari, 2012), and there exists a state s such that at least two actions are afforded to the agent._ 

To ground this formulation in planning, an agent is said to be a competent planner when it can achieve high depth-n tasks with a high probability. Formally, the optimal planner for depth-n tasks satisfies, 


where _Pπ_ ( _τ |_ = _T | s_ ) is the probability that the trajectory generated by _π_ from initial state _s_ corresponds to achieving the task _T_ . We can then define an agent’s distribution-robust competence for tasks in line with Def. 4, by choosing the distance metric _d_ (I _o_ ( _s, τ | T_ ) _, P_ ( _τ | π, s, T_ )) to be the difference in probability mass over trajectories that satisfy the task _T_<sup>_i_</sup> _∈T_ for the agent, and the corresponding probability mass for the optimal agent with the same affordance set. We also choose Dist( _T_ ) to be an arbitrary task distribution that includes _T_ ( _n_ ), and assume there is some upper bound _δ_ on the probability that the agent violates the _ζ_ -regret bound for any given task _T_<sup>_i_</sup> _∼T_ ( _n_ ) independent of the agent’s performance on any other task _T_<sup>_j_</sup> _∼T_ ( _n_ ). 

**Definition 6** (( _n, ζ, δ_ )-optimal agent): _Given affordances AF I (Def. 4), an_ ( _n, ζ, δ_ ) _-optimal agent is such that_ 


_where, πi is the policy of the agent for a depth-n task T_<sup>_i_</sup> _∼T_ ( _n_ ) _and_ 


5 

**Affordances Enable Partial World Modeling with LLMs** 

We can interpret **R** ( _π, T_<sup>_i_</sup> ) as the agent’s expected regret for task _T_<sup>_i_</sup> , where the reward function is +1 if the agent achieves the task and 0 otherwise. Therefore, a ( _n, ζ, δ_ )- optimal agent describes an agent that is a competent planner to depth _n_ , where the probability the agent violates a _ζ_ - regret bound for any depth-n task is bounded by some _δ_ . **Theorem 1** (Distribution-Robust Affordances induce Partial World Models) **.** _Let π be the policy of a deterministic_ ( _n, ζ, δ_ ) _-optimal agent (Def. 6), in an environment satisfying Assumption 1. π encodes a partial world model P_ ˆpar( _s_<sup>_′_</sup> _| o, s_ ) _, and the worst case error for this world model is bounded by,_ 


Proof is in Appendix B.1. Theorem 1 implies that there is a characteristic scale for the error in the partial world model we can recover from the agent’s policy, given by _ϕ_ , which scales with _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ), but increases rapidly for higher intent mis-specification i.e. _ζ_ close to 1 (where the regret bound becomes very weak). For _δ <_ 1 _/_ 2 the probability that the error is _ϵ_ larger than the characteristic error _ϕ_ decays exponentially in _ϵ_ , with an exponent given by _n_ . From this we conclude that for agents that perform well on a task distribution involving planning over its afforded actions to high depth (n), the agent’s policy encodes an accurate partial world model with respect to those afforded actions. Specifically, we can recover a partial world model from the agent’s policy that deviates from the true transition probabilities with an error that decays exponentially. 

## **4.2. Partial World Models Enable Provably Efficient Search** 

We are interested in understanding the increase in search efficiency when using a partial world model _P_ par as opposed to a full model _P_ full. When sampling from _P_ full, the agent considers all _n_ = _|O|_ possible actions, which translates to _n_ = _|I|_ intents. Alternatively, sampling from _P_ par is based on a predefined set of _k_ task-agnostic and -specific intents from _I_ , all independently achievable and satisfied to degree _ζ_ (Def. 1) across a distribution of tasks (Def. 4). In other words, _P_ par has access to _k_ = _|I_ par _|_ intents ( _I_ par _⊆I_ ). **Assumption 2.** _The size of the set of task-agnostic agent intents I_ par _is finite and much smaller than the number of all possible abstract actions n_ = _|O| to be considered at any state in the search process: k ≪ n._ 

The appeal of a partial model is due to the potential gigantic exponential speedup that can be obtained by greatly 

reducing the branching factor of complex combinatorial environments: suppose a task can only be solved in the full model by a single specific sequence of _L_ abstract actions, thus having an expected time to success of _n_<sup>_L_</sup> . If this task can also be solved with the _k_ intents of the partial model, the latter would take _k_<sup>_L_</sup> steps to success in expectation. Using Assumption 2, the speed up from the partial model can be so large as to make the intractable task tractable. 

However, the pre-specified intents might not be perfectly aligned, or worse, if the partial model misses _any necessary_ intent to solve _any_ task, the expected number of trials to solve every task by the partial model _N_<sup>par</sup> is infinite. To protect against this, we define a **_corrected_ partial model** _P_ cor which assigns a small probability _ε_ cor to account for missing intents from the full model: for each intent _Ij_ , 


Note that setting _ε_ cor = 0 recovers the partial model, while _ε_ cor = ( _n − k_ ) _/n_ recovers the full model. Moreover, we develop an **_adaptive_ model** _P_ ada (see Section B.2) that automatically competes with the optimal _ε_ cor _for each task_ , at the cost of a small _O_ ( _L_ ) factor: 

**Theorem 2** (Provably Efficient Search with a Partial Model) **.** _The expected number of samples necessary for the adaptive corrected partial model to solve every task is at most a factor O_ ( _L_ ) _of the best corrected model for each task:_ 


_where L is the length of the sampled sequences of intents._ 

Proof is in Section B.2. The intuition here is that at the price of a small factor (2 _L_ + 3) _e_ , the adaptive corrected model enjoys the potential exponential speedup of the partial model, while being robust to missing intents from the model. 

# **5. Empirical Illustration: LLM as Partial World Model for Efficient Planning** 

To illustrate the concepts empirically, we consider an agent with access to a world dynamics model _P_ ( _s_<sup>_′_</sup> _|s, o_ ) represented by a pre-trained text-only large model.<sup>3</sup> Our approach concretizes the general framework depicted in Fig. 1 by leveraging LLMs both for affordances and for world modeling (See Appendix Fig. 5). To bypass the need for manual intent-completion programs and expensive data collection, we leverage an LLM as an affordance model 

> 3We note that our approach is generally applicable to any large model e.g. VLM’s can also be used. 

6 

**Affordances Enable Partial World Modeling with LLMs** 

_Table 1._ **Inducing a partial model via affordances is more efficient in search, albeit at the cost of induced bias due to affordances in the block arrangement task.** Partial models are able to get to the reward in fewer search simulations as compared to a full world model, which does not get to any reward in limited budget of 4 simulations. Results are averaged across 4 independent seeds. Knowledge of affordances as shown here with the oracle baseline results in both, reduced number of MC simulations, and much fewer LLM calls. 

|**[3 blocks] Method**|**Model**|**MC-Search Score**|**Simulations**|**LLM Calls**|**Steps to Completion**|
|---|---|---|---|---|---|
|Full Modelw/ Few Shot Examples|_P_LLM(_s_<sup>_′_</sup>_|s, o_)|0_._0|_>_4|40_._0|_>_10|
|**Partial Model(Ours)**|_P_AFF-LLM(_s_<sup>_′_</sup>_|s, o_)|3_._75|2_._75|43_._25|5|
|Partial Model w/OracleAffordances|_P_Oracle-AFF-LLM(_s_<sup>_′_</sup>_|s, o_)|5_._0|2_._5|15_._75|2|
|**[5 blocks] Method**|**Model**|**MC-Search Score**|**Simulations**|**LLM Calls**|**Steps to Completion**|
|Full Modelw/ Few Shot Examples|_P_LLM(_s_<sup>_′_</sup>_|s, o_)|0_._087|_>_4|40|_>_10|
|**Partial Model (Ours)**|_P_AFF-LLM(_s_<sup>_′_</sup>_|s, o_)|0_._2239|2_._215|40|5|


faffordances( _st, m_ ). Given a natural language state representation _st_ , the LLM generates _m_ affordable actions. These correspond to distribution-robust affordances and induce a partial world model _P_ par, denoted as _PAff −LLM_ ( _s_<sup>_′_</sup> _|s, o_ ) in this section. 

We empirically study; **[Q1.]** Can LLMs as affordance-aware partial world models lead to improved efficiency in search? (Sec.5.1), and **[Q2.]** Can we leverage distribution-robust agent affordances to induce useful partial world models across related tasks? (Sec.5.2) We consider a simulated tabletop for long-horizon manipulation tasks using the pybullet simulator. We investigate block-rearrangement tasks with 3, 5, and 7 blocks to test the agent’s performance as difficulty increases. For each configuration, the agent is tasked with satisfying the high-level task description move_blocks_close_to_each_other. 

## **5.1. LMs as partial world models can substantially improve the sample search efficiency** 

Given only the high-level language instruction, the task requires multi-step reasoning and planning. We first consider the 3-block configuration. We compare three methods, namely 

1. **Full World Model** w/ Few Shot Examples: a pretrained LLM as a generative world model _P_ LLM( _s_<sup>_′_</sup> _|s, o_ ) prompted with the state _s_ , action _a_ , and few-shot (4 shots) examples to predict the future state _s_<sup>_′_</sup> , 

2. **Partial Model (Ours)** : is an induced partial model, where given a state _s_ , first a pre-trained LLM representing faffordances( _st, m_ ) generates m affordable actions, inducing a partial world model _P_ AFF-LLM( _s_<sup>_′_</sup> _|s, o_ ) prompted with only state _s, o ∈AF I_ , and few-shot (4 shots) examples to predict the future state _s_<sup>_′_</sup> , and 

3. **Partial Model with oracle affordances** : considers our method with programmatically generated ground truth affordances to illustrate the bias induced from pre-specified intents. 

Based on robot embodiment of a gripper arm **task agnostic** 

**intents** _I_ agn are specified as natural language description, with the idea of capturing invariance across tasks, resulting in _AF I_ . For e.g. “a block is movable only if that color is present in the current state and when nothing is on top of it.” We show more examples of these prompts in Appendix A.2. We use a simple implementation of Monte-Carlo (MC) sampling to build a policy from a world model (Fig. 4). We use the true reward model on each node (i.e. tasks are defined on states). From a real environment state, we expand a search tree using a model. We run 4 simulations, and each simulation expands a new un-visited node (using a random policy over untried actions). Random policy rollouts extend trajectories to at most 10 states (depth), seeking states with reward +10. We assess the likelihood that the model finds rewarding states (i.e. _MC average reward_ ) averaged over multiple independent seeds. Whether modelled successful trajectories match trajectories in real test environment. (i.e. _online policy evaluation_ ). When using a partial model, the MC tree is only expanded on affordable actions. In doing so, the search tree focuses modelling resources on trajectories that match predefined task-agnostic intents. 


_Figure 4._ **Monte-Carlo sampling with a partial model** considers expanding the tree is only on affordances. However, search with a full model would expand all possible state-action pairs. 

For the 3-blocks tabletop task configuration, we observe in Table 1 that inducing a partial model via affordances _P_ AFF-LLM is more efficient in search, albeit at the cost of induced bias due to affordances. Not knowing the precise affordances requires marginally more LLM calls in the than using the perfect knowledge of affordances i.e. _P_ Oracle-AFF-LLM. The number of MC simulations it takes with each method is lower when using a partial model (2.75) 

7 

**Affordances Enable Partial World Modeling with LLMs** 

_Table 2._ **Distribution-robust agent affordances are robust to related tasks.** We report the **1. avg leaf-node Score** , **2. avg tree score** reflecting the quality of the search tree on average across all nodes, **3. avg accumulated reward** reflecting the average accumulated reward by running MC-search as open loop policy on states that the model imagined, and **4. Online Policy Evaluation** reflects cumulative reward during online policy evaluation for search policy. Search guided with affordance-aware partial models constructs an overall better quality of tree, and results in a better policy for online RL as compared to the full model. Results are averaged across 4 independent seeds with standard deviation in the brackets. 

|**Method**<br>**num blocks = 5**|**Model**|**Avg Leaf-Node Score**|**Avg Tree Score**|**Avg Accumulated Reward**|**Online Policy Evaluation**|
|---|---|---|---|---|---|
|Full Modelwith few-shot examples.|_P_LLM(_s_<sup>_′_</sup>_|s, o_)|0_._089(_±_0_._04)|0_._089(_±_0_._04)|0_._65(_±_1_._26)|0_._7895(_±_0_._25)|
|**Partial Model(Ours)**|_P_AFF-LLM(_s_<sup>_′_</sup>_|s, o_)|0_._235(_±_0_._087)|0_._2314(_±_0_._086)|0_._9212(_±_0_._709)|1_._56(_±_0_._45)|
|**num blocks = 7**||||||
|Full Modelwith few-shot examples.|_P_LLM(_s_<sup>_′_</sup>_|s, o_)|_−_0_._01134(_±_0_._057)|_−_0_._01134(_±_0_._057)|_−_0_._1869(_±_0_._51)|_−_0_._836(_±_0_._1059)|
|**Partial Model(Ours)**|_P_AFF-LLM(_s_<sup>_′_</sup>_|s, o_)|0_._0180(_±_0_._12)|0_._020(_±_0_._12)|0_._386(_±_0_._57)|0_._2141(_±_0_._617)|


as compared to a full model _P_ LLM (which exhausts the budget of _>_ 4 simulations and never reaches a rewarding state with MC Score of 0 _._ 0). Besides, our approach also results in a better performing MC policy assessed with online evaluation in the test environment where it takes 5 steps to task completion on an average as compared to using a full world model (which exhausts the steps to task completion budget of _>_ 10 steps and does not complete the task across all runs). 

**Key Insight I:** Inducing a partial world model via affordances is more efficient in search, albeit at the cost of induced bias due to affordances (See Table 1). 

## **5.2. Distribution-robust agent affordances facilitate partial models that improve planning across tasks** 

Next, we ask if we can leverage distribution robust agent affordances to induce useful partial world models across related tasks? We study this by increasing the difficulty of the blocks environment with more blocks to be manipulated and arranged on the tabletop that requires longer horizon for planning exacerbating the need to guide search as the branching factor increases. We keep the _I_ agn (see Sec. 3) consistent from previous configuration of 3 blocks in both LLM as the affordance model alongside the full world model _P_ LLM( _s_<sup>_′_</sup> _|s, o_ ), and the partial world model _P_ AFF-LLM( _s_<sup>_′_</sup> _|s, o_ ). We report in Table. 2 that with increasing difficulty in task configuration, our approach considerably reduces the branching factor resulting in fewer mcts simulations needed, and higher average accumulated reward during planning. 

**Key Insight II:** Partial-models informed by distribution-robust agent affordances capture underlying invariance across tasks resulting in generalization of search efficiency (See Table 2). 

# **6. Related Work** 

Generative models as world models constitute a broad research area. Recent works consider pre-training large-scale world models (Yang et al., 2023a). While this is appealing, it is computationally expensive, requiring large amounts of data, compute, resulting in a non-trivial process to pre-train a world model. Moreover, in the presence of large scale knowledge representation in LMs, collecting data online from scratch is non-trivial, simply due to the challenges presented by such approach i.e. sample efficiency or dependence on visiting each transition tuple sufficient number of times (e.g. in count-based method). 

Bruce et al. (2024) proposed to learn a generative interactive model analogous to a simulator, trained on 200k hours of video data, inferring the latent actions between each frame a with the latent action model to predict the next frame. Our approach is complimentary as it can be leveraged to induce a partial model to make predictions on only _affordable_ latent actions, thereby reducing hallucinations of unrealistic futures as highlighted in their limitations. 

Closest to our work, Hao et al. (2023)[RAP] also utilize plug-and-play with LLMs although their focus both in domains ( such as blocksworld which considers a PDDL specification of the planning problem) and research question ( such as planning efficacy with full models) is different. For example, their focus in on Math like reasoning tasks, such as GSM8k which are typically i.i.d. in nature. On the contrary, our work is focused on sequential-decision making problems such as long-horizon table top tasks with online on-policy RL. We argue that RAP can be viewed analogous to a full model, as it is limiting the action space by sampling a fixed number of actions as opposed to using generalized affordances. Our approach is complimentary to their work by leveraging distribution-robust affordances that induce partial world models. 

More recent work (Benechehab et al., 2024) explores using LLM as a transition model, but due to high inference cost, explores a dynamics model as a function of the states alone as opposed to state-action pairs. We note however, that they 

8 

**Affordances Enable Partial World Modeling with LLMs** 

are not focused on online search and planning, but instead in an offline RL setting. Furthermore, the central focus of our work is the generalized affordance framework which extends prior work (Khetarpal et al., 2021; 2020) from a single task to multi-task perspective. 

# **7. Discussion** 

This work generalized the concept of affordances to multitask setting by delineating task-agnostic and task-specific intents. This perspective explains when and why certain affordances specific to an agent embodiment generalize across tasks, and when they might be task-specific. Our theoretical analysis established that tow findings. First, we identified that agents achieving task-agnostic intents must encode a predictive partial model of the world informed by distribution-robust affordances for a certain task distribution. Second, we showed that while near-perfect partial models enable improved search efficiency, an adaptive corrective model enjoys the potential exponential speed up of the partial model, yet being robust to missing intents from the full model. Broadly, our work suggests that while naively using LLMs as world models for planning and search can be highly inefficient, posing them as partial models through intents and affordances offers tremendous potential in guiding the search especially in a large action space. 

Future work requires overcoming the limited nature of specifying task-agnostic intents in the form of prompt engineering. One approach that is much more promising in this direction considers program synthesis for intentcompletion (Cherif et al., 2025) identifying affordances from trajectories, resulting in coded partial models of the world that can be reused in more complex sequential task settings. Another promising direction requires the formalism of affordances to account for dynamic agent morphologies, which is scope for future work. Further, we anticipate more benefits from adapting the agent’s latent representation of the pre-trained world model in light of online experiential data (Silver & Sutton, 2025). 

# **Impact Statement** 

This work studies how affordances enable partial world models with LLMs. By explicitly modeling the limits of posing LLMs as full world models, our approach aims to find more efficient ways to search for RL agents. We presented work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

# **Acknowledgements** 

The authors are grateful to David Abel for his thorough and constructive feedback on a draft of this paper, and to Anna Koop and Benjamin Van Roy for their insightful reviews of an earlier version. 

# **References** 

- Abel, D., Barth-Maron, G., MacGlashan, J., and Tellex, S. Toward affordance-aware planning. In _First Workshop on Affordances: Affordances in Vision for Cognitive Robotics_ , 2014. 

- Arora, K., El Asri, L., Bahuleyan, H., and Cheung, J. C. K. Why exposure bias matters: An imitation learning perspective of error accumulation in language generation. In _Findings of the Association for Computational Linguistics: ACL 2022_ , pp. 700–710, 2022. 

- Bartlett, P. L. and Tewari, A. Regal: A regularization based algorithm for reinforcement learning in weakly communicating mdps. _arXiv preprint arXiv:1205.2661_ , 2012. 

- Benechehab, A., Hili, Y. A. E., Odonnat, A., Zekri, O., Thomas, A., Paolo, G., Filippone, M., Redko, I., and Kégl, B. Zero-shot model-based reinforcement learning using large language models. _arXiv preprint arXiv:2410.11711_ , 2024. 

- Bruce, J., Dennis, M. D., Edwards, A., Parker-Holder, J., Shi, Y., Hughes, E., Lai, M., Mavalankar, A., Steigerwald, R., Apps, C., et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Burda, Y., Edwards, H., Pathak, D., Storkey, A., Darrell, T., and Efros, A. A. Large-scale study of curiosity-driven learning. _arXiv preprint arXiv:1808.04355_ , 2018. 

- Chemero, A. An outline of a theory of affordances. _Ecological psychology_ , 15(2):181–195, 2003. 

- Cherif, L., Kondrup, F., Venuto, D., Anand, A., Precup, D., and Khetarpal, K. Cracking the code of action: a generative approach to affordances for reinforcement learning. _arXiv preprint arXiv:2504.17282_ , 2025. 

- Drescher, G. L. _Made-up Minds: A Constructivist Approach to Artificial Intelligence_ . MIT Press, Cambridge, MA, USA, 1991. 

- Fikes, R. E., Hart, P. E., and Nilsson, N. J. Learning and executing generalized robot plans. _Artificial Intelligence_ , 1972. 

- Flesch, T., Juechems, K., Dumbalska, T., Saxe, A., and Summerfield, C. Orthogonal representations for robust 

9 

**Affordances Enable Partial World Modeling with LLMs** 

context-dependent task performance in brains and neural networks. _Neuron_ , 110(7):1258–1270, 2022. 

- Gibson, J. J. The theory of affordances. _Hilldale, USA_ , 1 (2), 1977. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering diverse domains through world models, 2024. URL https://arxiv.org/abs/2301.04104. 

- Hao, S., Gu, Y., Ma, H., Hong, J. J., Wang, Z., Wang, D. Z., and Hu, Z. Reasoning with language model is planning with world model. _arXiv preprint arXiv:2305.14992_ , 2023. 

- Kakade, S. M. _On the sample complexity of reinforcement learning_ . University of London, University College London (United Kingdom), 2003. 

- Khetarpal, K., Ahmed, Z., Comanici, G., Abel, D., and Precup, D. What can i do here? a theory of affordances in reinforcement learning. In _International Conference on Machine Learning_ , pp. 5243–5253. PMLR, 2020. 

- Khetarpal, K., Ahmed, Z., Comanici, G., and Precup, D. Temporally abstract partial models. _Advances in Neural Information Processing Systems_ , 34:1979–1991, 2021. 

- Korf, R. E. _Learning to Solve Problems by Searching for Macro-operators_ . PhD thesis, Carnegie Mellon University, Pittsburgh, PA, USA, 1983. 

   - Sutton, R. S. and Barto, A. G. _Reinforcement learning: An introduction_ . MIT press, 2018. 

   - Talvitie, E. and Singh, S. P. Simple local models for complex dynamical systems. In _Advances in Neural Information Processing Systems_ , pp. 1617–1624, 2009. 

   - Valmeekam, K., Olmo, A., Sreedharan, S., and Kambhampati, S. Large language models still can’t plan (a benchmark for llms on planning and reasoning about change). In _NeurIPS 2022 Foundation Models for Decision Making Workshop_ , 2022. 

   - Xi, Z., Chen, W., Guo, X., He, W., Ding, Y., Hong, B., Zhang, M., Wang, J., Jin, S., Zhou, E., et al. The rise and potential of large language model based agents: A survey. _Science China Information Sciences_ , 68(2):121101, 2025. 

   - Yang, M., Du, Y., Ghasemipour, K., Tompson, J., Schuurmans, D., and Abbeel, P. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023a. 

   - Yang, S., Nachum, O., Du, Y., Wei, J., Abbeel, P., and Schuurmans, D. Foundation models for decision making: Problems, methods, and opportunities. _arXiv preprint arXiv:2303.04129_ , 2023b. 

   - Zhang, X., Ma, Y., and Singla, A. Task-agnostic exploration in reinforcement learning. _Advances in Neural Information Processing Systems_ , 33:11734–11743, 2020. 

- Nangue Tasse, G., James, S., and Rosman, B. A boolean task algebra for reinforcement learning. _Advances in Neural Information Processing Systems_ , 33:9497–9507, 2020. 

- Pnueli, A. The temporal logic of programs. In _18th annual symposium on foundations of computer science (sfcs 1977)_ , pp. 46–57. ieee, 1977. 

- Richens, J., Abel, D., Bellot, A., and Everitt, T. General agents need world models. _arXiv preprint arXiv:2506.01622_ , 2025. 

- Shin, K., Kwak, H., Kim, W., Jeong, J., Jung, S., Kim, K.-M., Ha, J.-W., and Lee, S.-W. Pivotal role of language modeling in recommender systems: Enriching taskspecific and task-agnostic representation learning, 2023. URL https://arxiv.org/abs/2212.03760. 

- Silver, D. and Sutton, R. S. Welcome to the era of experience. _incompleteideas.net_ , 2025. 

- Sodhani, S., Zhang, A., and Pineau, J. Multi-task reinforcement learning with context-based representations. In _International conference on machine learning_ , pp. 9767– 9779. PMLR, 2021. 

10 

**Affordances Enable Partial World Modeling with LLMs** 

# **Appendix** 

# **A. Additional Empirical Details** 

## **A.1. Details of the Approach** 


_Figure 5._ **Our Approach** leverages LLMs as partial world models using affordances as depicted here. Affordance-informed partial models are then used to guide MCTS in table top robotics task. We posit LLMs as-is to be generative world models, which we refer to as full world models. Partial Models are induced via affordances generated by LLMs using task-agnostic intents specified in the prompt. 

## **A.2. Task-Agnostic Intents used in Table 1, Table 2** 

1. A block is movable only if that color is present in the current state and when nothing is on top of it. 

2. A block placement on x,y coordinates which has an existing block is valid if it exactly matches the coordinates of the existing block in the current state AND if the block color is present in the current state. 

3. A block placement on x,y coordinates which has an existing block is valid if it has sufficient overlap with the coordinates of the existing block in the current state AND if the block color is present in the current state. 

4. A block placement on x,y coordinates is valid if no other block is present in those coordinates. 

# **B. Theoretical Derivations** 

## **B.1. Proof of Theorem 1.** 

**Setup.** As we are interested in recovering an agent’s partial model across a fixed distribution of tasks i.e. _T_<sup>_i_</sup> _∼_ Dist( _T_ ), we consider the tasks which share a common underlying environment. I.e. the transition function is fixed, while the reward function across tasks (and potentially the discount factor) varies. Henceforth, we interchangeably use ‘goals’ or ‘rewards’ in place of ‘tasks’. 

We consider tasks composed of primitive sub-tasks of the following form, 

- _Actions_ . The agent takes some desired abstract action _o ∈O_ . 

- _Outcomes_ . The last abstract action _O_ = _o_ taken by the agent terminates in some desired state(s) _g ⊆S_ , denoted _X_ ( _s ∈ g_ ). This can be thought of as the simplest temporally extended intents 1 

- _Goals_ . The agent steers the environment into some desired state _s ∈S_ using the actions afforded to it, over any number of time steps, denoted _F_ ( _s ∈ g_ ). 

Here _F_ is the Eventually operator and _X_ is the Next operator defined in linear temporal logic (LTL) (Pnueli, 1977). Abusing notation, _T_ also denotes the LTL expression corresponding to the abstract task _T_ , which evaluates to True if the agent-environment trajectory _τ_ which achives (satisfies) the task specification (denoted _τ |_ = _T_ ) and False otherwise. 

We are interested in agents that are capable of solving tasks with non-trivial complexity, i.e. consisting of multiple sub-tasks to be performed in a specified order. We denote these sequences of sub-tasks _T_ 1 _, T_ 2 _, . . . , Tn_ (Definition 5) using angled brackets _⟨T_ 1 _, T_ 2 _, . . . , Tn⟩_ , to denote the LTL expression that evaluates to true if _T_ 1 is satisfied, and then _T_ 2, and so on. See (Richens et al., 2025) for the construction of these LTL expressions. 

11 

**Affordances Enable Partial World Modeling with LLMs** 

**Example.** The task ‘move the red block from _x_ to _y_ ’ can be expressed as _⟨_ ( _O_ = _o_ ) _, X_ ( _s ∈ g_ ) _⟩_ where _o_ is the abstract action ‘move block (red) from position (x) to position (y)’, and _g_ is the set of environment states where the red block is in position y. Note the sequential nature of this task, which required not only taking the abstract action, but to achieve the desired outcome. This is to account for imperfect affordances, whereby the abstract action _O_ = _o_ may not terminate in the desired state. 

**Example.** With the aforementioned task, we may want to relax the requirements on the agent, so that it can re-attempt the task if it fails to move the red block to the desired position. E.g. it could pick up the wrong block, or due to imperfect sensorimotor control fail to place the block in the desired location. This may require chaining together different actions depending on outcomes (e.g. if the red block is placed in _y_<sup>_′_</sup> applying the action ‘move the red block from (y’) to (y)’). This is now a purely outcome-based goal, which the agent can achieve by any valid sequence of actions without a time horizon constraint, and so we can represent it as _T_ = _⟨F_ ( _s ∈ g_ ) _⟩_ where _g_ is all states where a red block is in position _y_ . 

We also allow for tasks with some ambiguity in how they are solved. For example, there can be multiple goal states whereby reaching any one of them would satisfy the overall task. More generally, there can be multiple sub-tasks—themselves sequential tasks—which are sufficient to achieve the overall task. We can construct specifications for these composite tasks by taking the Boolean OR over sequential tasks _T_ = _T_ 1 _∨ T_ 2. 

**Example.** The task of providing dinner could be achieved by (order a delivery THEN collect the delivery) OR (buy groceries THEN prepare a meal THEN serve the meal). This can be expressed as _T_ = _T_ 1 _∨ T_ 2 where _T_ 1 = _⟨_ ( _O_ = order delivery) _, X_ ( _S_ = delivery collected) _⟩_ and _T_ 2 = _⟨_ ( _O_ = buy groceries]) _, X_ ( _S_ = meal prepared) _⟩_ . 

Each of these abstract actions must be afforded to the agent, e.g. an agent that has no phone or internet access will not be afforded the abstract action ‘order a delivery’. 

The tasks we consider consist of sequences of abstract actions, with the task depth _n_ being the maximum number of sub-tasks the agent would have to complete to achieve the overall task (Definition 5). Intuitively, tasks with a higher depth _n_ are more complex as they require a larger number of sub-tasks to be completed, and hence require more planning. For example, if we consider an explicitly model-based agent, tasks with a high depth require more accurate world models compared to e.g. myopic tasks ( _n_ = 1), due to compounding errors. Therefore to establish that an agent has an implicit world model, we must assume it is competent at tasks of non-trivial depth _n_ (Definition 6). This is a relaxation of the assumptions on the agent in (Richens et al., 2025) as we do not assume the agent satisfies a strict regret bound for all tasks, but only on average over the task distribution, and relax the regret bound to a soft bound where the agent can violate _ζ_ with some probability. As in (Richens et al., 2025) we also make the simplifying assumptions that the agent follows a deterministic policy. Turning to the environment, Assumption 1 is a standard assumption in MDPs. 

**Theorem 1** (Distribution-Robust Affordances induce Partial World Models) **.** _Let π be the policy of a deterministic_ ( _n, ζ, δ_ ) _- optimal agent (Def. 6), in an environment satisfying Assumption 1. π encodes a partial world model P_<sup>ˆ</sup> par( _s_<sup>_′_</sup> _| o, s_ ) _, and the worst case error for this world model is bounded by,_ 


_Proof._ We use the approach in Sec. 3 to return an estimate _P_<sup>ˆ</sup> ( _s_<sup>_′_</sup> _| o, s_ ) given _π_ ( _o | h_ ). Following the proof of Theorem 1 in (Richens et al., 2025), we define the following tasks. Let ( _s, o_ ) _∈AF I →_ and let _To_ 1( _k, n_ ) denote task which is a disjunction over all tasks<sup>�</sup> _r≤k_ � _i∈nCr_<sup>_φ_(</sup><sup>_r, i_) where</sup> 


where the agent 

> i) takes action _O_ = _o_ 1 in the first time step ( _T_ 0 = ( _O_ = _o_ 1)), then transitions eventually to _S_ = _s_ and takes action _O_ = _a_ , ( _T_ 1 = _F_ (( _S_ = _s, O_ = _o_ 1))), 

12 

**Affordances Enable Partial World Modeling with LLMs** 

- ii) transitions next to a goal state which is either _S_ = _s_<sup>_′_</sup> , ( _T_ 2 = _X_ ( _S_ = _s_<sup>_′_</sup> )) or _S̸_ = _s_<sup>_′_</sup> , ( _T_ 2<sup>_′_=</sup><sup>_X_(</sup><sup>_S̸_=</sup><sup>_s′_)),</sup> 

- iii) returns eventually to _S_ = _s_ and takes action _O_ = _o_ 1, ( _T_ 1), and repeats the cycle ii)-iii) a total of _n_ times, with the transition _T_ 2 = _X_ ( _S_<sup>_′_</sup> = _s_ ) occurring _r_ times and the transition _T_ 2<sup>_′_=</sup><sup>_X_(</sup><sup>_S̸_=</sup><sup>_s′_) occurring</sup><sup>_n −r_times.</sup> 

I.e. _To_ 1( _k, n_ ) requires the agent to take abstract action _O_ = _o_ 1 in state _S_ = _s_ a total of _n_ times, and at most _k_ of these actions should terminate in the state _S_ = _s_<sup>_′_</sup> . Note that _n_ here is the number of times the agent takes _O_ = _o_ in _S_ = _s_ , but the goal depth is 2 _n_ + 1. 

Consider the task _To_ 2( _k, n_ ) that is identical to _To_ 1( _k, n_ ) except that to achieve the goal the agent must i) initially take action _O_ = _o_ 2 instead of _O_ = _o_ 1 and ii) must terminate in _S_ = _s_ at least _k_ + 1 times. 

Note we can construct the task _To_ 1 _,o_ 2( _k, n_ ) = _To_ 1( _k, n_ ) _∨ To_ 2( _k, n_ ) for any pair of abstract action _o_ 1 _, o_ 2 _∈AF I →_ (˜ _s_ ) such that _o_ 1 _̸_ = _o_ 2 (where by assumption at least two such actions exist). As _To_ 1( _k, n_ ) and _To_ 2( _k, n_ ) are mutually exclusive we have, 


and for any _π_ only one of the terms on the right hand side is non-zero. Hence to determine the optimal policy we can evaluate max _π P_ ( _τ |_ = _To_ 1( _k, n_ ) _| π, s_ 0) and max _π P_ ( _τ |_ = _To_ 1( _k, n_ ) _| π, s_ 0). First we consider the case where _δ_ = 0 (the agent satisfies a strict regret bound for all _Ti ∼_ Dist( _T_ )). As _π_ is deterministic by assumption, let _O_ = _o_ be the agent’s action at _t_ = 0. If the agent chooses _O_ = _o_ 1 then only _To_ 1( _k, n_ ) can be satisfied and likewise for _O_ = _o_ 2, and any other action choice achieves the task with probability 0. 

_To_ 1( _k, n_ ) =<sup>�</sup> _r≤k_ � _i∈nCr_<sup>_φi_(</sup><sup>_r, n_)andall</sup><sup>_φi_(</sup><sup>_r, n_)</sup><sup>_, φj_(</sup><sup>_r′, n_)aremutuallyexclusive,i.e.for</sup><sup>_r̸_=</sup><sup>_r′_or</sup><sup>_i̸_=</sup><sup>_j_,</sup><sup>_τ|_=</sup> _φi_ ( _r, n_ ) = _⇒ τ̸ |_ = _φj_ ( _r_<sup>_′_</sup> _, n_ ) and vice versa, and hence, 


and by Lemma 6 in (Richens et al., 2025) the maximum probability that this goal can be satisfied is given by, 


where 


is the binomial probability mass function and _Pn_ ( _X ≤ k_ ) is the cumulative distribution function. Likewise if the agent chooses the initial action _o_ 2 (pursuing _To_ 2( _k, n_ )), it can achieve this task with maximum probability, 


If the initial action is neither _o_ 1 nor _o_ 2 then the agent achieves task _To_ 1 _,o_ 2( _k, n_ ) with probability zero. Therefore, for an agent satisfying a _ζ_ regret bound the optimal agent’s policy _π_ ( _o | s_ 0; _To_ 1 _,o_ 2( _k, n_ )) witnesses the following inequalities, depending on its choice of abstract action _o_ 1 or _o_ 2, 


For _ζ <_ 1 _/_ 2 we can ignore (10) as _Pn_ ( _X > k_ ) = 1 _− Pn_ ( _X ≤ k_ ) so one of these terms must be larger than _ζ_ . 

For ease of notation we denote _Pss′_ ( _a_ ) = _p_ . The median of the binomial distribution _X_ = _m_ is an integer 0 _≤ m ≤ n_ that satisfies _np −_ 1 _≤ m ≤ np_ + 1. For _ζ_ = 0 we can exactly determine the median by varying _k_ and finding the unique value for which _k_<sup>_∗_</sup> such that _Pn_ ( _X > k_<sup>_∗_</sup> _−_ 1) _≥ Pn_ ( _X ≤ k_<sup>_∗_</sup> _−_ 1) and _Pn_ ( _X ≤ k_<sup>_∗_</sup> ) _≥ Pn_ ( _X > k_<sup>_∗_</sup> ), yielding _k_<sup>_∗_</sup> = _m_ . 

13 

**Affordances Enable Partial World Modeling with LLMs** 

For _ζ >_ 0 we can no longer determine the median with certainty, but can bound its value. Using _P_ ( _X > k_ ) = 1 _−P_ ( _X ≤ k_ ) and _P_ ( _X > k −_ 1) = _P_ ( _X ≥ k_ ), and (8) and (9) yields, 


Let _k_ = _m_<sup>_−_</sup> be the largest value of _k_ for which _O_ = _o_ 1, and _k_ = _m_<sup>+</sup> be the smallest value of _k_ such that _O_ = _o_ 2. The true median _m_ must lie between these values. These yield the tightest bounds, 


Applying the upper tail Chebyshev inequality _Pn_ ( _X ≥ µ_ + _tσ_ ) _≤_ 1 _/_ (1 + _t_<sup>2</sup> ) with _m_<sup>+</sup> = _µ_ + _tσ_ to (15) and using _µ_ = _np_ , _σ_<sup>2</sup> = _np_ (1 _− p_ ) yields, 


and likewise for the lower tail Chebyshev bound applied to (14) we recover, 


For _δ_ = 0 these bounds would allow us to recover bounds on _µ_ (and hence _p_ ) as done in (Richens et al., 2025), as the lowest value of _k_ such that the agent’s policy returns _O_ = _o_ 2 for task _To_ 1 _,o_ 2( _k, n_ ) must lie between _m_<sup>_−_</sup> and _m_<sup>+</sup> , yiedling in a bounded error estimate for the median. However, for _δ >_ 0 by Definition 6 for any given task _Ti_ there is a probability of at most _δ_ that the agent’s policy violates the _ζ_ regret bound, and so the agent may return _O_ = _o_ 2 for _k < m_<sup>_−_</sup> or _O_ = _o_ 1 for _k > m_<sup>+</sup> , albeit with probability at most _δ_ . 

Let _f_ ( _k, n_ ) _∈{_ 0 _,_ 1 _} ∀ k ∈_ 1 _, . . . , n_ be an indicator variable for the action returned by the agent’s policy for task _To_ 1 _,o_ 2( _k, n_ ), where for a given _k, n_ we have _O_ = _o_ 1 _→ f_ ( _k, n_ ) = 0 and _O_ = _o_ 2 _→ f_ ( _k, n_ ) = 1. To estimate the median we fit a step function _F_ ( _k_<sup>ˆ</sup> ) which predicts _F_ ( _k_ ) = 0 _∀ k ≤ k_<sup>ˆ</sup> else _F_ ( _k_ ) = 1. The error of this model at reproducing _f_ ( _k_ ) is, 


We will take _k_<sup>ˆ</sup> := arg min error( _k, n_<sup>ˆ</sup> ) to be our estimate of the median, and derive an upper bound on the expected error _|k_<sup>ˆ</sup> _− m|_ . Our aim is to determine a probabilistic lower bound on the value of _k_<sup>ˆ</sup> . Hence, we can consider the case where we set _f_ ( _k ≥ m_<sup>_−_</sup> ) = 1, as this can only reduce the value of _k_<sup>ˆ</sup> . For all _k < m_<sup>_−_</sup> , we can only have _f_ ( _k_ ) = 1 if the agent’s policy violates the _ζ_ regret bound, which by Definition 6 occurs for each such _k_ independently with a probability at most _δ_ . Therefore we can set _P_ ( _f_ ( _k_ ) = 1) = _δ_ for all _k < m_<sup>_−_</sup> , as this is maximizing the probability of _f_ ( _k_ ) = 1 for _k < m_<sup>_−_</sup> which reduces the value of _k_<sup>ˆ</sup> . In this case the _k_<sup>ˆ</sup> is given by (18) but replacing _n_ with _m_<sup>_−_</sup> . 

Let _y_ ( _k_ ) = 2 _f_ ( _k_ ) _−_ 1, yielding E[ _Y_ ( _k_ )] = 1 _−_ 2 _δ_ . Let _E_ (0) be the error for the model that predicts _f_ ( _k_ ) = 1 for all _k_ . We can express the error _E_ ( _k_ ) = _E_ ( _k, m_<sup>_−_</sup> ) as a telescoping sum, 

14 

**Affordances Enable Partial World Modeling with LLMs** 


Let _S_ ( _k_ ) =<sup>�</sup> _i_<sup>_m_</sup> =1<sup>_−Yi_bearandomwalkwithdrift</sup><sup>_µ_=</sup><sup>_E_[</sup><sup>_Yi_]=1</sup><sup>_−_2</sup><sup>_δ_.</sup> As _E_ (0) is a constant offset, _k_<sup>ˆ</sup> = arg min0 _≤k≤m− E_ ( _k_ ) = arg min0 _≤k≤m− S_ ( _k_ ), and so minimizing _E_ ( _k_ ) is equivalent to minimizing _S_ ( _k_ ). We can therefore derive a worst case probabilistic lower bound on _k_<sup>ˆ</sup> by deriving a similar bound for the minimum of the random walk _Sk_ . We desire a bound on the event _A_ = _{k_<sup>ˆ</sup> _≤ m_<sup>_−_</sup> _−_ ∆ _}_ where ∆ _>_ 0. _A_ implies a weaker condition _B_ = _{_ min0 _≤k≤m−−_ ∆ _Sk ≤ Sm− }_ , therefore if we bound the probability of _B_ we upper bound the probability of _A_ . Using _P_ ( _B_ ) = _P_ (min0 _≤k≤m−−_ ∆[ _Sk ≤ Sm−_ ]) = _P_ (max0 _≤k≤m−−_ ∆[( _Sm− − Sk_ ) _≥_ 0]). For _Sm− − Sk_ =<sup>�</sup><sup>_m_</sup> _i_ =<sup>_−_</sup> _k_ +1<sup>_Yi_and</sup> _Yi_ are iid, this is equal to a sum over _m_<sup>_−_</sup> _− k_ iid Bernoulli variables, and the number of terms in the sum ranges from _m_<sup>_−_</sup> (for _k_ = 0) to ∆. We can therefore replace this sum with _Wl_ :=<sup>�</sup><sup>_l_</sup> _j_ =1<sup>_Y_</sup> _j_<sup>_′_with</sup><sup>_l_ranging from ∆to</sup><sup>_m−_, yielding</sup> _P_ ( _B_ ) = _P_ (max∆ _≤l≤m−_ [ _Wl ≥_ 0]) = _P_ (<sup>�</sup> _l_<sup>_m_</sup> =∆<sup>_−_[</sup><sup>_Wl≥_0]).Applying the union bound gives</sup><sup>_P_(</sup><sup>_B_)</sup><sup>_≤_�</sup><sup>_m_</sup> _l_ =∆<sup>_−P_(</sup><sup>_Wl≥_0).</sup> Next, we can upper bound _P_ ( _Wl ≥_ 0) using the Chernoff bound to give, 


Using _E_ [ _e_<sup>_sY_</sup> ] = (1 _− δ_ ) _e_<sup>_−s_</sup> + _δe_<sup>_s_</sup> and minimizing w.r.t _s_ gives, 


for _δ <_ 1 _/_ 2. Finally, we can determine a probabilistic upper bound, 


Letting _ρ_ := 2 ~~�~~ _δ_ (1 _− δ_ ) the sum over this geometric series gives, 


We can repeat these steps for deriving an upper bound to _k_<sup>ˆ</sup> as a deviation from _m_<sup>+</sup> , and (by symmetry) arrive at 


Finally, using the (identical) upper bounds for _m_<sup>_±_</sup> given by (16) we recover, 


Finally, using _p_ ˆ = _k/n_<sup>ˆ</sup> as our estimate for _p_ , and _σ_ = ~~�~~ _np_ (1 _− p_ ) yields a probabilistic error bounds, 

15 

**Affordances Enable Partial World Modeling with LLMs** 

where 


and where we have defined _ϵ_ := ∆ _/n_ , and _ϵ ∈_ [0 _,_ 1]. Finally, we relax the bound using _p_ (1 _− p_ ) _≤_ 1 _/_ 4 to give a simpler expression. 

## **B.2. Adaptive Corrected Model and Proof of Theorem 2.** 

Let us consider a single task _Ti_ . We use a Las Vegas algorithm (Monte Carlo with restarts until success) over sequences of intents of length _L_ . If the terminating reward is received before or when all _L_ intents are fully performed, the task terminates with success, otherwise the sequence has failed and another sequence is sampled until success. 

In a sampled sequence (a trial), each intent is sampled uniformly and independently of the past. That is, the probability of any intent _Ij_ for the full model is _P_ full( _Ij_ ) = 1 _/n_ . For the partial model it is _P_ par( _Ij_ ) = 1 _/k_ if _Ij ∈I_ par, 0 otherwise. Hence, each sequence has a probability _n_<sup>_−L_</sup> to be sampled for the full model, and _k_<sup>_−L_</sup> for the partial model. 

For any single trial, the success probability for the full model is 


and it is well known that the expected number _Ni_<sup>full</sup> of trials before success on task _Ti_ is 


The expected number of trials necessary to solve every task is 


We assume that every task can be solved in finite time by the full model. 

Similarly, for the partial model the expected number _N_<sup>par</sup> of trials to solve every task is 


Since in general _k ≪ n_ , if the intents of the partial model have a good enough coverage to solve all tasks, the potential speedup of ( _n/k_ )<sup>_L_</sup> compared to the full model can be gigantic. But if the partial model misses _any necessary_ intent to solve _any_ task, _N_<sup>par</sup> is infinite. Even with all the _necessary_ intents to ensure that each task can be solved, it may still miss _important_ intents that could help to solve tasks much faster. To avoid this, we define a _corrected_ partial model which assigns a small probability to use missing intents from the full model: For each intent _Ij_ , 


16 

**Affordances Enable Partial World Modeling with LLMs** 

Observe that setting _ε_ cor = 0 recovers the partial model, while _ε_ cor = ( _n − k_ ) _/n_ recovers the full model. 

Therefore, for a fixed _ε_ cor, and for a given sequence of intents _J_ = _I_ 1 _. . . IL_ , the probability of success of the corrected model for task _Ti_ , where _mJ ≤ L_ of the intents come exclusively from the full model ( _mJ_ is the number of ‘mistakes’), is 


But how do we set _ε_ cor? We can at least define the optimal _ε_ cor<sup>_∗_</sup> _i_<sup>for each task</sup><sup>_i_:</sup> 


but in general _ε_ cor<sup>_∗_</sup> _i_<sup>is not known.So we construct an</sup><sup>_adaptive_corrected model that is competitive within a factor (2</sup><sup>_L_+ 3)</sup><sup>_e_</sup> with the optimal _ε_ cor<sup>_∗_</sup> _i_<sup>for each task</sup><sup>_i_:Before sampling a sequence of</sup><sup>_L_intents, we sample</sup><sup>_m∈{_0</sup><sup>_, . . . ,_2</sup><sup>_L_+ 2)</sup><sup>_}_with</sup> uniform probability _P_ ( _m_ ) = 1 _/_ (2 _L_ + 3), and we set _ε_ cor = _m/_ (2 _L_ + 2). The probability of an intent (given _m_ ) for this adaptive model is 


For a given sequence of intents _J_ = _I_ 1 _. . . IL_ , the probability of success of the adaptive model for task _Ti_ is 


**Lemma 1.** _For each task i ≤|T |, there exists an m ∈{_ 0 _.._ 2 _L_ + 2 _} such that for every sequence J ∈I_<sup>_L_</sup> _,_ 


_Proof._ Rename _ε_<sup>_∗_</sup> = _ε_ cor<sup>_∗_</sup> _i_<sup>and</sup><sup>_ε_=</sup><sup>_m/_(2</sup><sup>_L_+ 2)..Then</sup> 

**Case** _ε_<sup>_∗_</sup> _≤_ 1 _/_ 2 **.** Choose _m_ = min _{m ∈{_ 0 _.._ 2 _L_ + 2 _}_ : 2 _Lm_ +2<sup>_≥ε∗}_,thatis</sup><sup>_m_=</sup><sup>_⌈_(2</sup><sup>_L_+ 2)</sup><sup>_ε∗⌉_.Then,first,</sup><sup>_ε_=</sup> _m/_ (2 _L_ + 2) _≥ ε_<sup>_∗_</sup> by definition of _m_ and thus _ε_<sup>_∗_</sup> _/ε ≤_ 1. Second, 


and thus, 


where we used _ε_<sup>_∗_</sup> _≤_ 1 _/_ 2 on the last inequality. Therefore, for every sequence _J ∈I_<sup>_L_</sup> , using ln(1 + _x_ ) _≤ x_ , 


Exponentiating finishes the proof for this case. 

**Case** _ε_<sup>_∗_</sup> _>_ 1 _/_ 2 **.** Similar as Case _ε_<sup>_∗_</sup> _≤_ 1 _/_ 2 but choosing instead _m_ = max _{m ∈{_ 0 _.._ 2 _L_ + 2 _}_ : 1 _−_ 2 _Lm_ +2<sup>_≥_1</sup><sup>_−ε∗}_.</sup> 

17 

**Affordances Enable Partial World Modeling with LLMs** 

**Theorem 2** (Provably Efficient Search with a Partial Model) **.** _The expected number of samples necessary for the adaptive corrected partial model to solve every task is at most a factor O_ ( _L_ ) _of the best corrected model for each task:_ 


_where L is the length of the sampled sequences of intents._ 

_Proof._ Applying Lemma 1 to Equation (29), and dropping all _m ∈{_ 0 _.._ 2 _L_ + 2 _}_ from the sum except the one satisfying Lemma 1 we obtain that 


where the last line is by definition of _ε_ cor<sup>_∗_</sup> _i_<sup>.The result follows by considering the expected time to success for task</sup><sup>_i_and</sup> summing over all tasks. 

18 

