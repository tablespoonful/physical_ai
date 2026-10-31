---
title: "Stealthy World Model Manipulation via Data Poisoning"
date: "2026-06-17"
authors: "Yibin Hu; Xiaolin Sun; Zizhan Zheng"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2606.18697
pdf: https://arxiv.org/pdf/2606.18697
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.18697)** / [論文ページ](https://arxiv.org/abs/2606.18697)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Stealthy World Model Manipulation via Data Poisoning** 

**Yibin Hu** 

**Xiaolin Sun** 

Department of Computer Science Department of Computer Science Tulane University Tulane University 

**Zizhan Zheng** Department of Computer Science Tulane University New Orleans, LA, USA `zzheng3@tulane.edu` 

## **Abstract** 

Model-based learning agents use learned world models to predict future states, plan actions, and adapt to new environments. However, the process of updating world models from collected experience creates a training-time attack surface: adversarially poisoned fine-tuning trajectories can manipulate the learned dynamics and thereby corrupt downstream planning. In this paper, we propose SWAAP, the first two-stage data poisoning framework for learned world models. In the first stage, SWAAP identifies a harmful target world model that induces low-return behavior under planning while remaining close to clean dynamics, using first-order bilevel optimization enabled by a transition-gradient theorem. In the second stage, SWAAP realizes this target through stealth-constrained gradient matching, modifying only a limited fraction of fine-tuning transition targets so that the induced training gradients steer the victim model toward the adversarial target, while a prediction-error regularizer encourages the poisoned targets to remain close to the world model’s natural approximation error. To assess attack stealthiness, we evaluate defenses and detectability across three stages of the poisoning pipeline: pre-training detection of poisoned transitions, robust training during fine-tuning, and test-time monitoring of the resulting world model. Across diverse continuouscontrol tasks, SWAAP causes substantial performance degradation while keeping poisoned transitions close to clean data and evading the evaluated non-adaptive residual/CUSUM/TRIM-style defenses. These results reveal a practical vulnerability in world-model adaptation pipelines and highlight the need for robustness methods that protect both world-model training data and learned dynamics. 

## **1 Introduction** 

While artificial intelligence (AI) has achieved remarkable success across various domains, building general-purpose agents that can quickly adapt to new tasks remains a major challenge, particularly for sequential decision-making tasks in open-ended environments that require substantial planning and adaptation. A promising direction is the development of _world models_ [Ha and Schmidhuber, 2018] that accurately capture environmental structure and dynamics to support a wide range of downstream tasks. In this context, predictive world models, which allow agents to “imagine” future scenarios for safer, more efficient decisions, are proliferating [Hafner et al., 2024, Hansen et al., 2024, Zhou et al., 2025]. Further, with recent advances in diffusion and transformer architectures, foundation world models [OpenAI, 2025, Bruce et al., 2024, Nvidia, 2025a] capable of simulating interactive environments from multi-modal input are emerging and are increasingly being applied in complex Preprint. 

domains such as autonomous vehicles and robotics [Nvidia, 2025b], making them valuable targets for malicious attacks. 

To support effective decision-making across diverse domains, world models must encode broad knowledge, process high-dimensional inputs (e.g., images, videos, and text), and make long-horizon predictions, introducing new vulnerabilities not present in traditional supervised learning or modelfree reinforcement learning (RL) systems. Despite extensive research in AI security and adversarial machine learning over the past decade, ensuring the robustness of world models against adversarial manipulation remains largely unexplored, limiting their deployment in high-stakes domains. 

In this work, we take an early step toward adversarially robust world modeling by introducing poisoning attacks tailored to world models. Our method strategically alters trajectory data used for training or fine-tuning, with the objective of manipulating model-based decision-making while maintaining outputs close to those of a clean model to evade detection. We believe this line of work is both practical and influential, as it highlights a fundamental vulnerability in world models that underpins their reliability in downstream applications. 

Traditional data poisoning methods from supervised learning [Biggio et al., 2012, Muñoz-González et al., 2017, Geiping et al., 2021] cannot be directly applied to our setting. These approaches typically assume fully differentiable training pipelines and discrete labels (e.g., flipping a _cat_ to a _dog_ ), allowing the adversary to optimize per-example perturbations via gradient-based techniques. In contrast, poisoning a world model requires identifying perturbations to the predicted next-state outcomes, which are structured, high-dimensional, and may be deterministic or stochastic. Such perturbations influence not only one-step predictions but also compound over long-horizon rollouts. Moreover, differentiating through the training process of the world model is computationally expensive and generally intractable, making standard supervised learning attacks unsuitable for this problem. 

Existing data-poisoning attacks in reinforcement learning [Rakhsha et al., 2020, Zhang et al., 2020] primarily manipulate rewards or transitions observed during training to steer the learned policy toward an adversary-specified target policy or behavior. Although performance degradation can in principle be achieved by enforcing a low-return target policy, this perspective does not directly apply to world-model poisoning, where the adversary cannot directly enforce the deployed policy. Instead, a world-model poisoning must act indirectly: it changes fine-tuning transitions so that the learned dynamics induce harmful planning or model-based policy improvement. SWAAP operationalizes this indirect attack by identifying a poisoned world model under which harmful behavior becomes favorable for the victim’s planner, and then realizing this model by poisoning only a bounded fraction of fine-tuning transitions. This creates a coupled inverse-planning and data-realization problem: even if a low-return target policy is known, there may be no nearby world model that induces it while remaining sufficiently close to clean dynamics to evade detection. Moreover, existing RL poisoning formulations are designed for simpler tabular or low-dimensional settings and do not directly scale to deep world models with high-dimensional continuous latent states, continuous actions, and longhorizon compounding prediction errors, as in TD-MPC2 [Hansen et al., 2024], DINO-WM [Zhou et al., 2025], and DreamerV3 [Hafner et al., 2024]. These differences motivate a scalable poisoning framework tailored to learned world models. 

In this work, we propose **SWAAP** ( **S** tealthy **W** orld Model M **A** nipulation via D **A** ta **P** oisoning), a two-stage data poisoning framework to manipulate learned world models in model-based RL. Our framework is applicable to both stochastic and deterministic transition dynamics. SWAAP first identifies a stealthy target world model that induces low-return behavior while staying close to the intact world model, via bilevel optimization. It then achieves this target through a realistic datapoisoning procedure that alters only a small fraction of the fine-tuning transition-dynamics data. Our contributions can be summarized as follows. 

- We propose, to our knowledge, the first data poisoning attack that explicitly targets learned world-model dynamics in deep model-based RL, which effectively degrades downstream planning performance while keeping the poisoned dynamics close to the true environment, making the attack difficult to detect. 

- **Two-stage decomposition** . Direct bilevel optimization through fine-tuning is intractable; we decouple it into (i) finding a stealthy adversarial target world model enabled by a transition gradient, and (ii) realizing it via gradient-matched data poisoning applied to trajectory data. We also show empirically that both stages are necessary. 

2 

- **Stealth-constrained data realization.** We adapt gradient matching to world-model fine-tuning by constructing poisoned transition targets whose gradients steer the victim toward the Stage 1 target while a prediction-error regularizer keeps perturbations close to the clean model’s natural deviation scale. We also introduce a trajectory-consistent variant for sequential fine-tuning data, where a poisoned intermediate state is used consistently as both the next-state target at time _t_ and the current state at time _t_ + 1. 

- **Empirical evaluation.** Evaluations using TD-MPC2 and DINO-WM show that poisoning a small fraction of fine-tuning data can cause large performance drops across diverse continuous-control benchmarks, including DMControl [Tassa et al., 2018], MyoSuite [Caggiano et al., 2022], and MetaWorld [Yu et al., 2020]. We evaluate three complementary notions of stealthiness: datalevel stealth before fine-tuning ( _δd_ , deviation-based filtering, and CUSUM-style screening of data trajectories), robustness during fine-tuning (TRIM), and model-level deviation after deployment ( _δm_ ). Across these evaluations, SWAAP maintains low data-level deviation and remains effective under the evaluated defenses and detectors, highlighting the need for robustness methods that protect both world-model training data and learned dynamics. 

## **2 System and Threat Models** 

In this section, we present the system and threat models, covering both world models and our proposed data-poisoning attacks framework. A detailed summary of related work on world models, model-based RL, model poisoning, data poisoning, and defenses is provided in Appendix C. 

### **2.1 World Models** 

We study an agent interacting with an environment formalized as a Markov decision process (MDP) ( _S, A, P, R, γ, µ_ ), where _µ_ is the initial state distribution, _S_ is the state space, _A_ is the action space, _P_ : _S ×A →_ ∆( _S_ ) is the transition kernel, _R_ : _S ×A×S →_ R is the reward function, and _γ ∈_ (0 _,_ 1) is the discount factor. The agent learns a world model _Pψ_ (parameterized by _ψ_ ) that approximates the environment dynamics _P_ ( _s_<sup>_′_</sup> _| s, a_ ) from transition data _D_ = _{_ ( _si, ai, s_<sup>_′_</sup> _i_<sup>)</sup><sup>_}|_</sup> _i_<sup>_D_</sup> =1<sup>_|_.To simplify notation</sup> and keep the discussion general, we assume a deterministic transition function in the main text and write the next state as _s_<sup>_′_</sup> = _Pψ_ ( _s, a_ ). With this slight abuse of notation, _Pψ_ is trained by minimizing the squared prediction error 


Extensions to the stochastic transition functions are in Appendix D.3, where the squared-error objective is replaced by a likelihood-based formulation. In modern model-based agents, prediction and planning are usually performed in a learned latent space _z_ = enc( _s_ ). To simplify notation, we write transitions in state space, but in our implementation _s_ denotes the encoded latent _z_ unless otherwise stated; transition predictions, poisoned targets, and stealth metrics are therefore computed in latent space. If fine-tuning data are stored as raw observations, the same objective can in principle be optimized through the encoder by replacing a raw next observation _o_ ˜<sup>_′_</sup> whose encoding realizes the desired latent target. Appendix H.3 gives initial raw-space transfer evidence across different encoders. 

We adopt TD-MPC2 [Hansen et al., 2024], a representative world modeling framework, to explain our approach. TD-MPC2 jointly trains a latent dynamics model, value functions, and a policy, and uses the policy to initialize model predictive control (MPC). In general, a learned world model induces a downstream policy or planner _πθ⋆_ ( _ψ_ ) by optimizing expected return under _Pψ_ : 


For MPC-based agents, at time _t_ the planner evaluates candidate action sequences _at_ : _t_ + _H_ by rolling them out under _Pψ_ from ˆ _st_ = _st_ and executes only the first action of the best sequence: 


A detailed description of the MPC procedure is given in Appendix E.1. 

3 

### **2.2 Threat Model** 

We consider a continual fine-tuning pipeline for learned world models: a developer pretrains a world model on a large general-purpose dataset and then periodically adapts it using locally collected trajectories from a deployed robot, edge device, or simulation client. In such pipelines, compromising the local fine-tuning buffer is a more accessible attack surface than compromising the pre-training process or directly overwriting deployed model parameters. We consider a data-poisoning adversary with access to this local fine-tuning stream, such as through a compromised data-logging path, dataaggregation service, or insider write access. The attacker may (i) modify at most _rp|D|_ ( _rp ∈_ (0 _,_ 1]) transitions in the fine-tuning dataset _D_ by replacing the recorded next state _s_<sup>_′_</sup> _i_<sup>with an adversarial target</sup> _s_ ˜<sup>_′_</sup> _i_<sup>, leaving</sup><sup>_si_,</sup><sup>_ai_, and the reward unchanged; and (ii) interact with a clean copy of the environment to</sup> collect reference trajectories for surrogate fitting and stealth regularization. The attack objective is to reduce the long-term return of the agent after the poisoned world model is used for planning or model-based policy improvement. 


In our main experiments, we assume white-box access to the victim world-model architecture, pretrained weights _ψ_ 0, and fine-tuning loss. We use this as an attack feasibility study and a worstcase robustness evaluation, analogous to whitebox adversarial evaluation in supervised learning; it is also relevant to open-weight world models and downstream adaptation settings. The attacker may additionally collect clean reference trajectories from the environment for surrogate fitting and stealth regularization. We also evaluate a gray-box variant in Appendix H.3, in which the attacker does not know the exact victim parame- 

Figure 1: Pipeline of SWAAP. 

ters or the downstream task. In both white-box and gray-box settings, the attacker only modifies a bounded subset of recorded fine-tuning transitions. The attacker does not directly change the deployed model parameters at test time; the attack must instead act through subsequent world-model adaptation. This separates SWAAP from direct model overwrite baselines and from test-time observation perturbations, which intervene at different stages of the pipeline. 

### **2.3 Bilevel Formulation of Problem** 

The adversary can pursue multiple objectives when manipulating the world model update, such as steering the agent toward a specific target policy or degrading its performance. In this work, we focus on the objective of reducing the agent’s long-term return. We consider a data-poisoning adversary that may perturb a bounded fraction of transitions in the fine-tuning dataset _D_ , replacing ( _si, ai, s_<sup>_′_</sup> _i_<sup>)</sup> with ( _si, ai,_ ˜ _s_<sup>_′_</sup> _i_<sup>) to form a poisoned dataset</sup><sup>_D_˜.After the agent trains on</sup><sup>_D_˜, the resulting world model</sup> _Pψ_ deviates from the true dynamics _P_ and induces suboptimal behavior. This interaction can be formalized as the following bilevel optimization problem: 


where _J_ � _P, θ_<sup>_∗_</sup> ( _ψ_ )� is the return of the surrogate policy in the true environment, _F_ ( _Pψ_ 0 _, D_<sup>˜</sup> ) denotes fine-tuning the initial world model _Pψ_ 0 on the poisoned dataset _D_<sup>˜</sup> , and _L_ ( _Pψ, P_ ) penalizes deviation between the poisoned world model and the true dynamics. In the general stochastic setting, this deviation can be measured by an expected divergence between transition kernels, such as _D_ KL( _P_ ( _· | s, a_ ) _∥ Pψ_ ( _· | s, a_ )). Our experiments use deterministic latent world models, where the transition model outputs a point prediction and the KL divergence is degenerate; we therefore instantiate _L_ ( _Pψ, P_ ) with the squared latent prediction-error surrogate: 


4 

Thus, we instantiate a deterministic formulation here; Appendix D.3 gives the stochastic formulation. In summary, the _outer minimization_ reduces real-environment performance, while the _inner maximization_ captures the agent’s policy optimization under the poisoned world model. 

## **3 Stealthy World Model Manipulation via Data Poisoning** 

Directly solving Eq. 1 is intractable because it requires optimizing which transition targets to perturb, how to perturb them, and how the victim world model changes after fine-tuning. SWAAP therefore decomposes the attack into two stages, shown in Figure 1. Stage 1 identifies a harmful but lowdeviation target world model _ψ_<sup>ˆ</sup> by solving a model-space bilevel problem. Stage 2 realizes this target through gradient-matched data poisoning, constructing _D_<sup>˜</sup> so that fine-tuning gradients steer the victim model toward _ψ_<sup>ˆ</sup> . Stealthiness is enforced at both levels: Stage 1 regularizes model-level deviation, while Stage 2 regularizes data-level deviations so poisoned targets remain close to the clean model’s natural prediction error. 

### **3.1 Stage 1: Identification of Perturbed Models** 

In the first stage, the attacker searches for a target world model _ψ_<sup>ˆ</sup> that induces low return when used for planning, while remaining close to the true dynamics. Let _J_ ( _ψ, θ_ ) := _J_ ( _Pψ, θ_ ) denote the expected return of policy _πθ_ in the imagined environment _Pψ_ , and let _J_ ( _P, θ_ ) denote its return in the true environment. The attacker then solves the model-space bilevel problem 


where _L_ ( _Pψ, P_ ) penalizes deviation from true dynamics and controls the attack–stealth trade-off. Directly solving Equation 3 is difficult because changing _ψ_ affects the agent only indirectly through long-horizon model-based planning or policy improvement. The outer objective is a trajectory-level return evaluated in the true environment, while the inner problem is a nonconvex RL/planning problem over high-dimensional policies and learned dynamics. Thus, applying a generic bilevel optimizer would require differentiating through the implicit response _θ_<sup>_⋆_</sup> ( _ψ_ ), which is computationally prohibitive in modern world-model agents. We therefore use a first-order dynamic-barrier bilevel method in the spirit of BOME [Liu et al., 2022], which replaces the implicit optimality condition with a value-function constraint; details are given in Appendix D.2. However, directly instantiating this update in model-based RL still requires the transition-model gradient _∇ψJ_ ( _ψ, θ_ ), which is not provided by the standard policy-gradient theorem. We thus derive a general transition-gradient estimator for stochastic transition kernels _Pψ_ ( _· | s, a_ ). 

**Theorem 3.1 (Transition Gradient)** _For a finite-horizon MDP with stochastic transition kernel Pψ_ ( _·|s, a_ ) _, policy πθ, and time-indexed value function Vt_ ( _s_ ) := E( _st,at,st_ +1) _∼Pψ,πθ_ �� _iT_ =0 _−t_<sup>_γiR_(</sup><sup>_st_+</sup><sup>_i, at_+</sup><sup>_i, st_+</sup><sup>_i_+1)</sup> ��� _st_ = _s_ � _. Assuming Pψ_ ( _s_<sup>_′_</sup> _|s, a_ ) _is differentiable in ψ, the gradient of the return with respect to the transition parameters is_ 


Using Theorem 3.1, Stage 1 alternates between approximating the agent’s response under the current world model and updating ( _ψ, θ_ ) with the dynamic-barrier direction. At iteration _k_ , we first run _W_ policy-gradient steps to obtain an approximate best response _θk_<sup>_W_under</sup><sup>_Pψ_</sup> _k_<sup>.We then estimate the</sup> outer and constraint gradients using rollouts from the true environment and the current/perturbed world models, and update ( _ψk, θk_ ) by the first-order dynamic-barrier step. Algorithm 1 summarizes the procedure (see Appendix E.3 for the algorithm details); Appendix D.2 provides the full BOME derivation and Appendix D.1 proves Theorem 3.1, including the discounted infinite-horizon stochastic form and the deterministic finite-horizon specialization used by deterministic latent predictors. 

### **3.2 Stage 2: Poisoning Data to Manipulate Model** 

Stage 1 identifies a harmful target world model _P_ ˆ _ψ_<sup>, but directly replacing the victim model would</sup> require model overwrite. Stage 2 instead realizes this target through bounded data poisoning. Let 

5 

_F_ ( _Pψ_ 0 _, D_<sup>˜</sup> ) denote fine-tuning the initial world model on poisoned data _D_<sup>˜</sup> . The attack objective is 


where the attacker modify at most an _rp_ fraction of next-state targets while keeping ( _s, a, r_ ) unchanged. Directly solving this problem requires both discrete subset selection and continuous target optimization while repeatedly fine-tuning the victim model, so we use a two-step approximation. 

First, we select the top- _rp_ fraction of transitions with largest residual _eψ_ ( _s, a, s_<sup>_′_</sup> ) = _∥s_<sup>_′_</sup> _− Pψ_ ( _s, a_ ) _∥_ 2 under the Stage 1 target model. These transitions are most inconsistent with the target dynamics and therefore provide strong local signal for steering fine-tuning toward _P_ ˆ _ψ_<sup>.Let</sup><sup>_Dp_be this selected</sup> subset and _Dc_ = _D \ Dp_ . The poisoned dataset is _D_<sup>˜</sup> = _Dc ∪ D_<sup>˜</sup> _p_ , where _D_<sup>˜</sup> _p_ replaces _s_<sup>_′_</sup> by ˜ _s_<sup>_′_</sup> only for transitions in _Dp_ . As throughout the paper, these deviations are computed in latent space. Second, we optimize the poisoned targets by gradient matching. Let 


where _D_ all is a large clean reference dataset collected by the attacker. _G_ real is the gradient induced by training on the poisoned data, while _G_ target is the update direction that would move the clean model toward the Stage 1 target. Thus, aligning these gradients makes ordinary fine-tuning move the victim world model toward _P_ ˆ _ψ_<sup>.</sup> 

To achieve the objective, we follow gradient-matching [Geiping et al., 2021] and optimize gradient direction using cosine alignment. The key requirement is that the victim’s training update is a descent direction for the adversarial target objective; matching direction is thus more important than matching gradient magnitude, which can vary with batch size, model scale, and loss normalization. We optimize 


The cosine term aligns the poisoned-data gradient with the Stage 1 target gradient. The second term regularizes perturbation size to match the clean model’s natural one-step prediction error, making poisoned targets less conspicuous under reference-model residual screening. The coefficient _α_ controls the trade-off between target realization and data-level stealth. 

**Trajectory-consistent poisoning.** The formulation above treats fine-tuning data as a set of transition tuples, a common practice in reality. When the fine-tuning data are stored as sequential trajectories, however, the same intermediate state appears twice: as the next-state target of transition _t_ and as the current-state input of transition _t_ + 1. In this case, perturbing only _s_<sup>_′_</sup> _t_<sup>would create an inconsistent</sup> trajectory, which can be detected by the victim agent with access to trajectory data. To further improve attack stealthiness, we therefore extend the above formulation by considering a trajectory-consistent variant (Appendix G.6): if transition _t_ is selected for poisoning, we replace both occurrences of the intermediate latent state, excluding terminal transitions where _t_ + 1 starts a new trajectory. The original matching gradient is augmented with a one-step consistency term to become 


so that the poisoned intermediate state remains predictive of the observed successor under the next action. This variant preserves the same poisoning-budget interpretation, but each selected poisoned state is applied consistently across adjacent trajectory tuples. 

### **3.3 Defenses Against Data Poisoning** 

We evaluate stealthiness against three stages of defense: pre-training detection before poisoned transitions are used for fine-tuning, robust training during fine-tuning, and test-time monitoring. 

**Pre-training detection.** Pre-training detection-based defenses aim to identify poisoned transitions before they are used for model updates. We consider a deviation-based detector that compares each candidate transition against a reference world model and flags transitions whose residual 

6 

_eψ_ ref ( _s, a, s_<sup>_′_</sup> ) exceeds a threshold [Chen et al., 2021]. Specifically, we consider a defender with access to a reasonably accurate reference world model _Pψ_ ref for which we choose to use _Pψ_ 0, and it <u>1</u> _<u>∥Pψ</u>_ <u>0 (</u> _si,ai_ <u>)</u> _−s_ ˜ _<u>i</u>_<sup>_′_</sup><sup>_<u>∥</u>_2</sup> computes data-level deviation _δd_ = _|D_<sup>˜</sup> _|_ �( _si,ai,s_ ˜<sup>_′_</sup> _i_<sup>)</sup><sup>_∈_</sup> _D_<sup>˜</sup> _∥Pψ_ 0 ( _si,ai_ ) _∥_ 2 , which measures the deviation of crafted poisoned transitions from clean predictions of the reference model and is compared with <u>1</u> _<u>∥Pψ</u>_ <u>0 (</u> _si,ai_ <u>)</u> _−si_<sup>_′_</sup><sup>_<u>∥</u>_2</sup> clean data _δ_ d _,_ ref = _|D|_ �( _si,ai,s_<sup>_′_</sup> _i_<sup>)</sup><sup>_∈D_</sup> _∥Pψ_ 0 ( _si,ai_ ) _∥_ 2 . We also evaluate a CUSUM-style sequential detector calibrated on held-out clean trajectories. The detector accumulates a scalar latent anomaly signal along candidate fine-tuning trajectories; details are in Appendix F.3.1. Because SWAAP operates on latent transitions, we further include a latent-space PCA sanity check on _D_<sup>˜</sup> : poisoned next-state targets largely overlap with true next states and do not form obvious latent outliers. **Training-time defenses** aim to reduce the impact of poisoned samples without explicitly identifying them. One representative approach is the TRIM strategy [Biggio et al., 2012], which iteratively filters transitions based on their deviation. At each iteration, the transitions are ranked by _eψ_ ref ( _s, a, s_<sup>_′_</sup> ), and only the lowest (1 _− β_ ) _n_ deviation transitions are retained, where _n_ is the number of transitions considered and _β ∈_ (0 _,_ 1) controls the fraction of discarded data. The fine-tuning update is then computed using this subset. By discarding high-deviation transitions, the TRIM strategy limits the influence of adversarially perturbed transitions while preserving the underlying clean dynamics. **Test-time monitoring** . At test time, the defender may monitor whether the learned world model remains consistent with observed environment transitions. For deterministic world models (stochastic case in Appendix D.3), we report the model-level deviation _δm_ = _T_<sup><u>1</u></sup> � _Ti_ =1 _<u>∥s</u>_<sup>_′_</sup> _<u>i</u>_<sup>_−P_</sup> _∥_<sup>_<u>ψ</u>_</sup> _s_<sup><u>(</u></sup><sup>_<u>′</u>_</sup> _i_<sup>_s∥i_2</sup><sup>_<u>,ai</u>_</sup><sup><u>)</u></sup><sup>_<u>∥</u>_2</sup> , computed over rollout transitions _{_ ( _st, at, s_<sup>_′_</sup> _t_<sup>)</sup><sup>_}T_</sup> _t_ =0<sup>. This measures how far the poisoned model deviates from true</sup> _<u>∥s</u>_<sup>_′_</sup> _<u>i</u>_<sup>_−Pψ_</sup> <u>0</u><sup><u>(</u></sup><sup>_si,ai_</sup><sup><u>)</u></sup><sup>_<u>∥</u>_2</sup> dynamics observed during execution, and clean model deviation _δ_ m _,_ ref = _T_<sup><u>1</u></sup> � _Ti_ =1 _∥s_<sup>_<u>′</u>_</sup> _i_<sup>_∥_2</sup> . However, in our data-poisoning threat model, test-time monitoring is a late-stage defense: if poisoned data have already evaded pre-training screening and been used for fine-tuning, harmful behavior may occur before the learned model is diagnosed. Therefore, the pre-training data-level deviation _δd_ is the more direct stealth metric for this attack surface, while _δm_ measures whether the resulting model remains plausibly close to clean dynamics after deployment. 

## **4 Experiments** 

We evaluate SWAAP’s effectiveness and stealthiness under the criteria in Section 3.3. After describing setup and metrics, we present main results on return degradation, _δd_ , _δm_ , and evaluated defenses, then summarize ablations and broader settings including larger buffers, trajectory-consistent poisoning, DINO-WM, and gray-box transfer. Additional implementation details, system configurations, hyperparameters, and extended results are deferred to Appendices E–H. 

### **4.1 Experimental Setup and Metrics** 

We use TD-MPC2 [Hansen et al., 2024] as the main victim agent. Unless otherwise stated, the victim starts from a world model _ψ_ 0 pretrained on 10<sup>6</sup> clean transitions and is fine-tuned on 5 _,_ 000 transitions, of which the attacker may modify at most an _rp_ fraction. We use _rp_ = 0 _._ 1 in the main experiments. TD-MPC2 uses 512 candidate rollouts with planning horizon 3. All deviations are computed in the learned latent space _z_ = enc( _s_ ). We evaluate on DMControl [Tassa et al., 2018], MyoSuite [Caggiano et al., 2022], MetaWorld [Yu et al., 2020], and ManiSkill2 [Gu et al., 2023]. We compare **Clean** , **SWAAP (Random)** , **Direct Model Poisoning** , and **SWAAP** . Direct Model Poisoning directly deploys the Stage 1 target model and is used to serve as a reference point under a stronger threat model of model overwriting. Unless otherwise stated, each Table 1 entry reports mean _±_ std over 10 independent seeds. Each seed-level value is itself averaged over approximately 5,000 rollout transitions, using 10 episodes for 500-step DMControl tasks and 50 episodes for 100-step tasks. Figure 2 and Appendix Figure 4 also use 10 independent seeds; their error bars report variation across seed-level averages. Other diagnostic ablations report variation across independent evaluation episodes rather than independent runs that aggregate multiple episodes. 

### **4.2 Effective and Stealthy Poisoning** 

**Main attack results.** Table 1 reports return, model-level deviation _δm_ , and data-level deviation _δd_ . The clean column gives the reference model’s natural rollout deviation _δm,_ ref . For fine-tuning 

7 

Table 1: Main attack results. Clean reports return and reference model-level deviation _δm,_ ref on rollout transitions. Attack columns report return and _δm_ ; SWAAP also reports _δd,_ ref and _δd_ on the fine-tuning buffer. Table 1 reports a stealth-prioritized operating point rather than an exhaustive search over Stage 1 checkpoints and Stage 2 stealth weights. Unless otherwise stated, SWAAP (Random) and SWAAP use _rp_ = 0 _._ 1 and _α_ = 0 _._ 9; humanoid-walk and lift-cube use _α_ = 0 _._ 99 to bias the operating point toward lower model-level deviation. Stronger attack–deviation trade-offs are shown in Figure 2 and Appendix F.1. 

||nv|Cl|ean|SW|AAP (Rando|m)|Direct Mod|el Poisoning||SWA|AP||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||.|Return|_δ_m_,_ref|Return|_δd_|_δm_|Return|_δm_|Return|_δ_d_,_ref|_δd_|_δm_|
|DMControl|humanoid-walk|868_±_15|_._092_± ._003|826_±_26|_._090_± ._005|_._103_± ._004|307_±_87|_._174_± ._009|775_±_50|_._090_± ._005|_._090_± ._005|_._110_± ._007|
||humanoid-run|584_±_13|_._049_± ._002|567_±_13|_._052_± ._008|_._053_± ._002|189_±_09|_._104_± ._001|515_±_14|_._051_± ._008|_._053_± ._008|_._063_± ._002|
||dog-walk|798_±_8|_._056_± ._001|794_±_10|_._059_± ._002|_._055_± ._001|523_±_18|_._086_± ._001|748_±_13|_._059_± ._002|_._060_± ._002|_._061_± ._002|
||dog-run|637_±_09|_._052_± ._001|607_±_22|_._051_± ._004|_._054_± ._001|270_±_28|_._081_± ._001|478_±_26|_._051_± ._004|_._052_± ._004|_._064_± ._001|
||cheetah-run|838_±_11|_._026_± ._001|830_±_23|_._032_± ._006|_._025_± ._004|389_±_39|_._104_± ._011|806_±_6|_._028_± ._002|_._034_± ._006|_._036_± ._001|
|MyoSuite|pen-twirl-hard<br><br>reach-hard|3574_±_640 <br>743_±_22|_._057_± ._003<br><br>_._042_± ._010|3024_±_646 <br>664_±_36|_._056_± ._008 <br>_._035_± ._011|_._079_± ._007<br>_._065_± ._006|2743_±_497 <br>410_±_344|_._073_± ._006<br> _._085_± ._007|2771_±_801<br>606_±_198|_._056_± ._008<br>_._035_± ._011|_._056_± ._008<br>_._035_± ._011|_._101_± ._013<br>_._089_± ._030|
|Meta-World|push<br>soccer|1784_±_13 <br>1724_±_9|_._080_± ._002<br><br>_._033_± ._002|1476_±_142 <br>1711_±_26|_._080_± ._005 <br> _._050_± ._009|_._176_± ._018<br>_._034_± ._004|1464_±_154 <br>1555_±_102|_._150_± ._022<br> _._083_± ._018|1641_±_80<br>1479_±_96|_._080_± ._005<br>_._046_± ._007|_._081_± ._005<br>_._051_± ._010|_._171_± ._011<br>_._064_± ._008|
|MiSkill2|lift-cube|193_±_04|_._019_± ._006|178_±_15|_._031_± ._027|_._071_± ._027|136_±_22|_._210_± ._047|175_±_20|_._031_± ._027|_._032_± ._027|_._068_± ._034|
|an|pick-cube<br>stack-cube|161_±_07<br>170_±_16|_._028_± ._007<br>_._044_± ._010|158_±_10<br>137_±_13|_._026_± ._003 <br>_._042_± ._011|_._029_± ._012<br>_._088_± ._011|117_±_11<br>106_±_23|_._198_± ._022<br>_._116_± ._007|147_±_14<br>141_±_18|_._025_± ._003<br>_._041_± ._011|_._027_± ._003<br>_._042_± ._011|_._069_± ._028<br>_._077_± ._016|


data, _δd_ = _∥Pψ_ ref ( _s, a_ ) _− s_<sup>_′_</sup> data<sup>_∥_2</sup><sup>_/∥Pψ_</sup> ref<sup>(</sup><sup>_s, a_)</sup><sup>_∥_2,where</sup><sup>_s_</sup> data<sup>_′_is either</sup><sup>_s′_or</sup><sup>_s_˜</sup><sup>_′_;this is the signal</sup> available to a defender who observes only the incoming fine-tuning stream and a reference model. SWAAP consistently lowers return while modifying only a bounded fraction of transition targets and keeping _δd_ close to _δd,_ ref in most tasks. The resulting _δm_ varies across environments, so we do not claim model-level indistinguishability; rather, SWAAP demonstrates an effectiveness–stealth trade-off under bounded data-level perturbation. Direct Model Poisoning is stronger in some tasks but assumes direct model overwrite and serves only as a reference point under a stronger threat model. Appendix F.3 shows that lower _α_ can increase degradation with little change in _δd_ . 

**Pre-training and training-time defenses.** We evaluate a residual-based CUSUM detector using _xt_ = _∥zt_ +1 _− Pψ_ ref ( _zt, at_ ) _∥_ 2 and report ROC-AUC and TPR at a clean-calibrated threshold (Appendix F.3.1). On MW-Push, it detects aggressive low-stealth poisoning ( _α_ = 0 _._ 1: AUC 0 _._ 864, TPR 0 _._ 40 at FPR 0 _._ 06), but loses power at the main stealth setting ( _α_ = 0 _._ 9: AUC 0 _._ 509, TPR 0 _._ 08). Humanoid-Walk at _α_ = 0 _._ 9 similarly gives AUC 0 _._ 520 and TPR 0 _._ 10 at FPR 0 _._ 10. PCA visualizations in Appendix F.3.2 show that poisoned next-state targets do not form obvious outliers. During fine-tuning, Figure 3c shows that SWAAP preserves its effectiveness under TRIM and produces even stronger degradation. We conjecture this occurs because the poisoned transitions are crafted to mislead TRIM into removing clean transitions, thereby amplifying the attack’s effect after training. 

**Stage-wise realization and attack-stealth trade-off.** Figure 2 examines the Stage 2 poisoning realization step across stealth weights _α_ and shows that at relaxed stealth, SWAAP’s return drop substantially exceeds that of SWAAP (Random), whose effect saturates, indicating that the Stage 1 target provides more useful poisoning directions than random perturbations. Additional _α_ and _rp_ ablations across all environments are in Appendix F.1. Figure 3 visualizes the attack-stealth frontier induced by different Stage 1 checkpoints and Stage 2 poisoning settings. In Stage 1, optimization produces saved target-model checkpoints with different return- _δm_ trade-offs; Direct Model Poisoning evaluates these checkpoints directly, while SWAAP attempts to realize selected targets through constrained data poisoning. The comparison exposes the main realization bottleneck. In HumanoidWalk, SWAAP points closely track the Direct Model Poisoning frontier, showing that Stage 2 can recover much of the target model’s effect. In Myo-Pen-Twirl-Hard, however, SWAAP remains separated from the Direct Model Poisoning frontier, showing that harmful targets are not always equally realizable through gradient-matched data poisoning. This target-selection procedure reflects a limitation of the current two-stage design that is not jointly optimized: Stage 1 optimizes for harmful and low- _δm_ target dynamics, but not for how easily those targets can later be realized by Stage 2. 

### **4.3 Ablations and Generalization** 

We provide additional ablations and generalization tests in Appendices F.4, G, H. First, Appendix F.4 studies the relation between Stage 1 target identification and Stage 2 data realization. Direct Model Poisoning in Table 1 evaluates saved Stage 1 target models under an unrealistic model-overwrite threat model, while SWAAP realizes selected targets through bounded data poisoning. The gap between the two reflects the practical cost of realizing a target model only through fine-tuning data, rather than a failure of the two-stage decomposition. We also compare against DMP-data, which directly inserts Stage 1 target predictions without gradient matching; SWAAP is more effective, especially under TRIM, indicating that the gradient-matching realization step is useful. 

8 


Figure 2: SWAAP versus SWAAP (Random) across stealth weights _α_ with _rp_ = 0 _._ 1. SWAAP generally causes larger return drops under smaller stealth weights. 


Figure 3: (a) and (b) Attack-stealth frontier: DMP evaluates saved Stage 1 target models directly, while SWAAP applies Stage 2 data poisoning toward selected targets. (c) Robust-training defense: on Humanoid-Walk, SWAAP ( _rp, α_ = 0 _._ 1 _,_ 0 _._ 9) remains effective under TRIM robust training ( _β_ = 0 _._ 2). 

Second, Appendices G.1 and G.2 test Stage 2 design choices and alternative baselines, respectively. Replacing the top- _rp_ transition-selection heuristic with random selection weakens the attack on Humanoid-Walk, supporting the choice of poisoning transitions most inconsistent with the Stage 1 target. On MW-Push, a PGD transition-poisoning baseline is weaker than SWAAP and produces larger data-level deviation, suggesting that local value-reducing perturbations are less effective and less stealthy than target-model gradient matching in this setting. 

Finally, Appendices G.6–H.3 evaluate broader settings. With a fixed number of poisoned samples, increasing the fine-tuning buffer weakens but does not eliminate the attack. We also evaluate a trajectory-consistent variant in which a poisoned intermediate latent state is written consistently as both _s_<sup>_′_</sup> _t_<sup>and</sup><sup>_st_+1insequentialfine-tuningdata.OnHumanoid-Walk,thisvariantachieves</sup> _R_ = 784 _±_ 19 and _δm_ = 0 _._ 111 _±_ 0 _._ 003 with _rp_ = 0 _._ 05, while maintaining data-level reference deviation _δd_ = _._ 102 _± ._ 007. This suggests that SWAAP is not limited to unordered transition buffers, although the attack is weaker under the stricter sequential-consistency constraint. On DINO-WM Push-T, SWAAP reduces the success rate after Stage 2 poisoning, providing initial evidence across world-model backbones. In a preliminary gray-box transfer setting, poisoned data are constructed in raw observation space using a single-task surrogate and then applied to a multi-task TD-MPC2 victim with a different latent encoder. This does not replace the white-box setting as a worst-case robustness baseline, but suggests a path toward relaxing exact-parameter and shared-encoder assumptions. 

## **5 Conclusion and Limitations** 

We introduced SWAAP, a two-stage data poisoning framework that realizes harmful target dynamics through stealth-constrained fine-tuning data. Across continuous-control tasks and a range of evaluated defenses, SWAAP exposes a practical vulnerability in world-model adaptation pipelines and motivates stronger protection for world-model training data and learned dynamics. 

As an initial study of world model poisoning, this work has limitations. First, our experiments primarily use TD-MPC2 as the victim model, with DINO-WM as an additional backbone; scaling to larger foundation models is left for future work. Second, SWAAP uses a two-stage approximation: 

9 

Stage 1 identifies harmful, low-deviation target dynamics, and Stage 2 realizes them via gradientmatched data poisoning. Since some targets are easier to realize than others, jointly optimizing target selection and data realization is an important next step. Third, we focus on untargeted performance degradation rather than targeted behavior manipulation. Finally, while our stealth evaluation covers representative detection and defense techniques, it does not rule out stronger detectors, deploymentspecific defenses, or more stringent constrained-poisoning settings. 

10 

## **References** 

Jonathan F Bard. _Practical bilevel optimization: algorithms and applications_ , volume 30. Springer Science & Business Media, 2013. 

- Battista Biggio, Blaine Nelson, and Pavel Laskov. Poisoning attacks against support vector machines. In _International Conference on Machine Learning (ICML)_ , 2012. 

- Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal Behbahani, Stephanie Chan, Nicolas Heess, Lucy Gonzalez, Simon Osindero, Sherjil Ozair, Scott Reed, Jingwei Zhang, Konrad Zolna, Jeff Clune, Nando de Freitas, Satinder Singh, and Tim Rocktäschel. Genie: Generative interactive environments, 2024. URL `https://arxiv.org/ abs/2402.15391` . 

- Vittorio Caggiano, Huawei Wang, Guillaume Durandau, Massimo Sartori, and Vikash Kumar. MyoSuite: A contact-rich simulation suite for musculoskeletal motor control. In _Annual Learning for Dynamics and Control Conference_ , 2022. 

- Eduardo F Camacho and Carlos Bordons. _Model predictive control_ . Springer, 2013. 

- Jian Chen, Xuxin Zhang, Rui Zhang, Chen Wang, and Ling Liu. De-pois: An attack-agnostic defense against data poisoning attacks. _IEEE Transactions on Information Forensics and Security_ , 16: 3412–3425, 2021. 

- Kurtland Chua, Roberto Calandra, Rowan McAllister, and Sergey Levine. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2018. 

- Marc Peter Deisenroth and Carl Edward Rasmussen. Pilco: A model-based and data-efficient approach to policy search. In _International Conference on Machine Learning (ICML)_ , 2011. 

- Minghong Fang, Xiaoyu Cao, Jinyuan Jia, and Neil Zhenqiang Gong. Local model poisoning attacks to byzantine-robust federated learning. In _USENIX Security Symposium_ , 2020. 

- Jonas Geiping, Liam Fowl, W. Ronny Huang, Wojciech Czaja, Gavin Taylor, Michael Moeller, and Tom Goldstein. Witches’ brew: Industrial scale data poisoning via gradient matching, 2021. URL `https://arxiv.org/abs/2009.02276` . 

- Saeed Ghadimi and Mengdi Wang. Approximation methods for bilevel programming. _arXiv preprint arXiv:1802.02246_ , 2018. 

- Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, Xiaodi Yuan, Pengwei Xie, Zhiao Huang, Rui Chen, and Hao Su. ManiSkill2: A unified benchmark for generalizable manipulation skills, 2023. URL `https: //arxiv.org/abs/2302.04659` . 

- David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International Conference on Machine Learning (ICML)_ , 2018. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. _International Conference on Machine Learning (ICML)_ , 2019. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models, 2024. URL `https://arxiv.org/abs/2301.04104` . 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-MPC2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2019. 

11 

- Michael Janner, Yilun Du, Joshua B Tenenbaum, and Sergey Levine. Planning with diffusion for flexible behavior synthesis. In _International Conference on Machine Learning (ICML)_ , 2022. 

- Lukasz Kaiser, Mohammad Babaeizadeh, Piotr Milos, Blazej Osinski, Roy Campbell, Konrad Czechowski, Dumitru Erhan, Chelsea Finn, Piotr Kozakowski, Sergey Levine, Afroz Mohiuddin, Ryan Sepassi, George Tucker, and Henryk Michalewski. Model-based reinforcement learning for atari. In _International Conference on Learning Representations (ICLR)_ , 2020. 

- Yongyuan Liang, Yanchao Sun, Ruijie Zheng, and Furong Huang. Efficient adversarial training without attacking: Worst-case-aware robust reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- Timothy P Lillicrap, Jonathan J Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, and Daan Wierstra. Continuous control with deep reinforcement learning. In _International Conference on Learning Representations (ICLR)_ , 2016. 

- Bo Liu, Mao Ye, Stephen Wright, Peter Stone, and Qiang Liu. BOME! bilevel optimization made easy: A simple first-order approach. In _Advances in neural information processing systems (NeurIPS)_ , 2022. 

- Risheng Liu, Jiaxin Gao, Jin Zhang, Deyu Meng, and Zhouchen Lin. Investigating bi-level optimization for learning and vision from a unified perspective: A survey and beyond. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 44(12):10045–10067, 2021. 

- Matthew MacKay, Paul Vicol, Jon Lorraine, David Duvenaud, and Roger Grosse. Self-tuning networks: Bilevel optimization of hyperparameters using structured best-response functions. _arXiv preprint arXiv:1903.03088_ , 2019. 

- Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, Stig Petersen, Charles Beattie, Amir Sadik, Ioannis Antonoglou, Helen King, Dharshan Kumaran, Daan Wierstra, Shane Legg, and Demis Hassabis. Human-level control through deep reinforcement learning. _Nature_ , 2015. 

- Luis Muñoz-González, Battista Biggio, Ambra Demontis, Andrea Paudice, Vasin Wongrassamee, Emil C. Lupu, and Fabio Roli. Towards poisoning of deep learning algorithms with back-gradient optimization. In _10th ACM Workshop on Artificial Intelligence and Security (AISec)_ , 2017. 

- Nvidia. Cosmos world foundation model platform for Physical AI. `https://arxiv.org/abs/ 2501.03575` , 2025a. 

- Nvidia. World foundation models. `https://www.nvidia.com/en-us/glossary/ world-models/` , 2025b. 

- OpenAI. Creating video from text. `https://openai.com/index/sora/` , 2025. 

- Tim Pearce, Tabish Rashid, Anssi Kanervisto, Dave Bignell, Mingfei Sun, Raluca Georgescu, Sergio Valcarcel Macua, Shan Zheng Tan, Ida Momennejad, Katja Hofmann, and Sam Devlin. Imitating human behaviour with diffusion models. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- Fabian Pedregosa. Hyperparameter optimization with approximate gradient. In _International Conference on Machine Learning (ICML)_ , 2016. 

- Amin Rakhsha, Goran Radanovic, Rati Devidze, Xiaojin Zhu, and Adish Singla. Policy teaching via environment poisoning: Training-time adversarial attacks against reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2020. 

- Yuval Tassa, Tom Erez, and Emanuel Todorov. Synthesis and stabilization of complex behaviors through online trajectory optimization. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012. 

- Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, et al. Deepmind control suite. _arXiv preprint arXiv:1801.00690_ , 2018. 

12 

- Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning (CoRL)_ , 2020. 

- Xuezhou Zhang, Yuzhe Ma, Adish Singla, and Xiaojin Zhu. Adaptive reward-poisoning attacks against reinforcement learning. In _International Conference on Machine Learning (ICML)_ , 2020. 

- Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. DINO-WM: World models on pre-trained visual features enable zero-shot planning, 2025. URL `https://arxiv.org/abs/2411.04983` . 

13 

## **Appendix Table of Contents** 

|**A **|**Use**|**of LLMs**|**16**|
|---|---|---|---|
|**B**|**Bro**|**ader Impact**|**16**|
|**C **|**Rela**|**ted Works**|**16**|
||C.1|World Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>16|
||C.2|Model-Based Reinforcement Learning . . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
||C.3|Model Poisoning Attack<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
||C.4|Data Poisoning Attacks and Defenses<br>. . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
|**D **|**The**|**ory and Derivations**|**18**|
||D.1|Derivation of Transition Gradient . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>18|
||D.2|BOME Details for Stage 1 Model Poisoning . . . . . . . . . . . . . .|. . . . . . .<br>19|
||D.3|Stochastic Transition Functions Case . . . . . . . . . . . . . . . . . .|. . . . . . .<br>21|
|**E**|**Imp**|**lementation Details**|**21**|
||E.1|Model Predictive Control . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>22|
||E.2|Hyperparameters<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>22|
||E.3|Stage 1: Target Model Identification . . . . . . . . . . . . . . . . . .|. . . . . . .<br>23|
||E.4|Stage 2: Data Poisoning . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>24|
||E.5|Hardware Specification and Computational Cost . . . . . . . . . . . .|. . . . . . .<br>24|
|**F**|**Mai**|**n Extended Results**|**24**|
||F.1|SWAAP and SWAAP (Random) . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>24|
||F.2|Model Poisoning Training Curve . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>26|
||F.3|Pre-Training Detection . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>26|
|||F.3.1<br>Residual-Based CUSUM Pre-Training Detector . . . . . . . .|. . . . . . .<br>26|
|||F.3.2<br>Latent-Space PCA Visualization . . . . . . . . . . . . . . . .|. . . . . . .<br>27|
||F.4|Stage 1–Stage 2 Realization Bottleneck<br>. . . . . . . . . . . . . . . .|. . . . . . .<br>28|
|**G **|**Abla**|**tions and Baselines**|**29**|
||G.1|Iterative FGSM/PGD Transition-Perturbation Baselines . . . . . . . .|. . . . . . .<br>29|
||G.2|Top-_rp_Transition Selection vs. Random Selection . . . . . . . . . . .|. . . . . . .<br>30|
||G.3|MPC Hyperparameter Ablation . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>30|
||G.4|Stage 1 Masked Perturbation Fraction . . . . . . . . . . . . . . . . .|. . . . . . .<br>30|
||G.5|Stage 2 Poisoning Ratio_rp_ . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>31|
||G.6|Trajectory-Consistent Data Poisoning<br>. . . . . . . . . . . . . . . . .|. . . . . . .<br>31|
||G.7|Larger Fine-Tuning Buffers . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>32|
|**H **|**Gen**|**eralization Experiments**|**32**|
||H.1|Additional MyoSuite and MetaWorld Environments . . . . . . . . . .|. . . . . . .<br>32|


14 

|H.2|DINO-WM Push-T Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>32|
|---|---|
|H.3|Gray-Box Attack on TD-MPC2 Multi-Task World Model . . . . . . . . . . . . . .<br>32|


15 

## **Appendix** 

## **A Use of LLMs** 

The authors used LLM-based assistants for manuscript preparation and presentation of supplementary materials, including grammar correction, wording suggestions, condensation of prose, LaTeX/formatting assistance, and improving the organization/readability of author-written code artifacts. LLMs were not used as part of the proposed method, theorem derivation, experiment design, result generation, or statistical analysis. All algorithms, experiments, figures, tables, citations, and technical claims were produced, checked, and approved by the authors. No confidential reviewer information, proprietary data, or sensitive personal data were used as LLM inputs. 

## **B Broader Impact** 

This paper studies a new training-time attack surface for learned world models. The primary intended benefit is defensive: by showing that fine-tuning trajectories can manipulate learned dynamics and downstream planning, the work motivates stronger data validation, robust fine-tuning, and monitoring methods for world-model adaptation pipelines. These issues are especially important for embodied agents, robotics, autonomous systems, and other settings where world models may be updated from locally collected experience. 

The same techniques could also inform misuse by suggesting ways to craft poisoned fine-tuning data. We mitigate this risk by studying the attack in controlled simulation benchmarks, limiting the threat model to bounded transition-target poisoning, and evaluating representative detection and robusttraining defenses. We do not provide instructions for attacking deployed real-world systems. We believe that disclosure is warranted because the vulnerability arises naturally in continual fine-tuning pipelines, and understanding it is necessary for developing effective defenses. 

More broadly, this work highlights that the robustness of world-model agents cannot be evaluated only at the final policy or planner level. The training data stream, learned dynamics, and downstream planning procedure are coupled, so future safety evaluations should consider how small changes in adaptation data can propagate into long-horizon behavior. We hope the proposed evaluations encourage further work on secure data collection, provenance tracking, anomaly detection, and robust world-model fine-tuning. 

## **C Related Works** 

### **C.1 World Models** 

World models aim to learn compact and predictive representations of environment dynamics that can be used for planning and control. Instead of interacting directly with the environment, an agent can rely on its learned model to simulate trajectories, evaluate policies, and anticipate future states. First introduced in [Ha and Schmidhuber, 2018], this work introduced a three-component architecture combining a variational autoencoder (VAE), a recurrent neural network (RNN), and a linear controller, demonstrating that policies trained entirely within a latent model can transfer back to the real environment. This work sparked a line of research exploring increasingly powerful and scalable model-based reinforcement learning frameworks. 

Dreamer-style agents use latent dynamics models optimized end-to-end with reinforcement learning. DreamerV3 [Hafner et al., 2024] achieves state-of-the-art performance on visual control and robotic tasks. It employs a recurrent state-space model (RSSM) with deterministic state _ht_ and stochastic latent _st_ , performing rollouts entirely in latent space. Three heads are trained on the RSSM: a reward predictor _r_ ˆ _t_ , a value function _V_<sup>ˆ</sup> ( _·_ ), and an actor _π_ , using imagined rollouts. At decision time, the actor proposes candidate actions, either sampled or taken as the mean. 

More recent approaches have investigated architectural advances tailored for large-scale and complex environments. DINO-WM [Zhou et al., 2025] leverages self-supervised vision transformers (ViTs) to improve perception quality, enabling stronger generalization in visually rich settings. Similarly, TD-MPC2 [Hansen et al., 2024] proposes a temporally abstracted model predictive control framework 

16 

that combines world models with trajectory optimization, achieving sample-efficient learning and strong performance in high-dimensional continuous control tasks. 

Parallel to these developments, diffusion-based world models have emerged as a promising alternative [Pearce et al., 2023, Janner et al., 2022]. By parameterizing the transition distribution as a denoising diffusion process, these models can capture multi-modal and stochastic dynamics more effectively than conventional Gaussian latent models. Diffusion world models have been shown to improve both planning quality and robustness to uncertainty, making them attractive in settings where dynamics are highly non-deterministic. 

### **C.2 Model-Based Reinforcement Learning** 

Model-based reinforcement learning (MBRL) is a powerful paradigm that improves sample efficiency and enables better generalization compared to purely model-free methods. In MBRL, an agent learns an explicit dynamics model of the environment and leverages this model for planning or policy optimization. We study an agent that leverages a learned world model to interact with an environment formalized as a Markov decision process (MDP) ( _S, A, P, R, γ, µ_ ), where _µ_ is the initial state distribution, _S_ is the state space, _A_ is the action space, _P_ : _S × A →_ ∆( _S_ ) is the transition kernel, _R_ : _S × A × S →_ R is the reward function, and _γ ∈_ (0 _,_ 1) is the discount factor. The goal is to find a policy _π_ : _S →_ ∆( _A_ ) that maximizes the expected discounted return<sup>�</sup><sup>_T_</sup> _i_ =0<sup>_γiR_(</sup><sup>_st, at_).</sup> 

Unlike model-free approaches that learn value functions or policies directly from experience [Mnih et al., 2015, Lillicrap et al., 2016, Haarnoja et al., 2018], MBRL explicitly learns a parametric approximation _P_<sup>ˆ</sup> _ψ_ of the transition kernel _P_ , often using neural networks [Deisenroth and Rasmussen, 2011, Chua et al., 2018, Janner et al., 2019, Hansen et al., 2024]. This learned dynamics model can then be used for model-predictive control (MPC) [Camacho and Bordons, 2013], trajectory optimization [Tassa et al., 2012], or to generate synthetic rollouts for policy improvement [Kaiser et al., 2020, Hafner et al., 2019]. 

### **C.3 Model Poisoning Attack** 

Model poisoning attacks directly compromise a learned model by altering its parameters. They assume the adversary can craft malicious model updates to steer the learning outcome or directly replace model parameters. For example, carefully crafted local malicious updates can harm the performance of a federated learning system [Fang et al., 2020]. 

In reinforcement learning, model poisoning is particularly concerning when applied to the agent’s learned dynamics model. Small, adversarial modifications to the transition kernel can propagate over planning horizons, misleading policy improvement, and causing degraded performance. This makes model poisoning a uniquely severe threat in model-based RL, as even subtle deviations from the true dynamics can cascade into large errors in long-term decision making. 

### **C.4 Data Poisoning Attacks and Defenses** 

Data poisoning attacks compromise learning systems by corrupting the training dataset to bias the learned model toward an adversarial objective. Unlike model poisoning, which manipulates parameters directly, data poisoning assumes the attacker can only influence the data stream but not the learning algorithm itself, which is a more realistic attack scenario. Data poisoning attacks have been shown to significantly degrade the model performance even with small amounts of poisoned data [Biggio et al., 2012]. A recent and effective data poisoning technique leverages gradient matching, which optimizes poisoned samples such that their gradients closely align with those of a target adversarial objective [Geiping et al., 2021]. By ensuring that poisoned data induces updates similar to those of the adversary’s intended solution, gradient matching enables stealthy and highly effective poisoning even under limited attacker control. We also adopt gradient matching in the second stage of our attack methods, where we inject carefully crafted poisoned transitions into the newly collected fine-tuning dataset. 

In reinforcement learning, data poisoning is particularly dangerous since training relies on sequential interactions with the environment. By injecting corrupted transitions into the replay buffer or modifying observed trajectories, an adversary can degrade the long-term performance of the agent, or even embed targeted failures [Rakhsha et al., 2020, Zhang et al., 2020]. 

17 

Effective defenses against data poisoning attacks involve detection and training-time strategies. We consider two widely used data poisoning defenses in our work. Chen et al. [2021] propose De-Pois, an attack-agnostic detection method that identifies poisoned data points with the help of a mimic model trained from clean data samples. By measuring the difference between the samples on the mimic model’s outputs, De-Pois can flag and remove suspicious points, improving robustness without assuming knowledge of the attack type. 

Complementing detection, training-time defenses aim to mitigate the effect of poisoned samples during learning. For example, Biggio et al. [2012] introduce the TRIM method and its iterative variant, which estimates and removes a fraction of potentially poisoned points based on deviation and the statistical properties of the data. 

## **D Theory and Derivations** 

### **D.1 Derivation of Transition Gradient** 

**Theorem 3.1** _The transition gradient of expected return in an MDP with transition dynamics Pψ and policy πθ can be expressed by_ 


**Proof:** We start from the derivative of the state-value function of an arbitrary initial state _s_ 0 and extend the state into the future time indefinitely, and expand it to write it as a recursive form in terms of _M_ function defined below, from which it unrolls to become an infinite series of the sum of _M_ ( _sk_ ) weighted by the probability of reaching _sk_ from _s_ 0 in _k_ steps. 


where _M_ ( _s_ 0) :=<sup>�</sup> _a_ 0<sup>_π_(</sup><sup>_a_0</sup><sup>_|s_0) �</sup> _s_ 1<sup>_∇ψPψ_(</sup><sup>_s_1</sup><sup>_|s_0</sup><sup>_, a_0)[</sup><sup>_R_(</sup><sup>_s_0</sup><sup>_, a_0</sup><sup>_, s_1)+</sup><sup>_γV_(</sup><sup>_s_1)],andthescaling</sup> from dividing the normalization constant<sup>�</sup> _s_<sup>_η_(</sup><sup>_s_)canbeabsorbedintothelearningrate,and</sup> _ρπ_ ( _s → x, k_ = 1) :=<sup>�</sup> _a_<sup>_π_(</sup><sup>_a|s_)</sup><sup>_P_(</sup><sup>_x|s, a_) is the transition probability of reaching</sup><sup>_x_from</sup><sup>_s_at step</sup> 

18 

_k_ = 1, and the relation _ρ_<sup>_π_</sup> ( _s → x, k_ + 1) =<sup>�</sup> _s_<sup>_′ ρπ_(</sup><sup>_s→s′, k_)</sup><sup>_ρπ_(</sup><sup>_s′→x,_1) is used to write the</sup> transition gradient into recursive form. Therefore, 


For planning with a finite horizon _T_ , given a time-indexed value function _Vt_ ( _st_ ) with terminal value _VT_ ( _sT_ ) = 0, the unrolling stops at finite steps. We begin a recursive form of _∇ψVt_ ( _s_ 0) that is similar to the infinite horizon one derived above 


where in the last step, setting _k_<sup>_′_</sup> = _T − t_ and using _VT_ ( _sT_ ) = 0 drops the last term, and therefore the finite horizon transition gradient is 


For the deterministic transition _st_ +1 = _fψ_ ( _st, at_ ) in finite horizon 


### **D.2 BOME Details for Stage 1 Model Poisoning** 

The adversary minimizes the return of the surrogate policy that learns from perturbed transitions by solving the following bilevel optimization problem: 


The goal is to minimize the constraint-regularized expected return with respect to the optimal policy derived from the poisoned environment. 

This bilevel optimization problem remains challenging due to its nested structure. The primary difficulty lies in computing the derivative _∇ψθ_ ( _ψ_ ). If one directly treats _θ_ ( _ψ_ ) as a function of _ψ_ , gradient-based methods such as hypergradient descent [Bard, 2013] update _ψ_ using _∇ψJ_ ( _P, θ_ ) = _∇ψθ_ ( _ψ_ ) _∇θJ_ ( _P, θ_ ) _,_ but evaluating _∇ψθ_ ( _ψ_ ) = _∇ψ_ arg max _πθ′ J_ ( _Pψ, θ_<sup>_′_</sup> ) requires solving linear systems and computing costly second-order Hessians. Prior work has attempted 

19 

**Algorithm 1** Algorithm for Perturbed Model Identification 

1: **Input:** env. dynamics _P_ , dynamics model _ψ_ 0, policy _θ_ 0, reward model _R_ , value net _Vϕ_ 

2: **Output:** perturbed model _ψ_<sup>ˆ</sup> 

3: **while** ( _ψk, θk_ ) not converged **do** 4: Collect rollouts from ( _ψk, θk_ ); use _R_ to form TD targets; update _Vϕ_ 5: _θk_<sup>0</sup><sup>_←θk_</sup> 6: **for** _i ←_ 1 to _W_ **do** 7: _θk_<sup>_i_+1</sup> _← θk_<sup>_i_+</sup><sup>_∇θJ_(</sup><sup>_ψk, θ_</sup> _k_<sup>_i_)</sup> 8: Collect rollouts to form replay buffers _BkW_ , _Bpk_ , _Bkk_ from ( _ψk, θk_<sup>_W_), (</sup><sup>_P, θk_), (</sup><sup>_ψk, θk_), respectively</sup> 9: Ω _←_ [ ] 10: **for** _i ←_ 1 to _N_ **do** 11: Sample _BkW_ to compute _∇ψJ_ ( _ψk, θk_<sup>_W_)</sup> 12: Sample _Bpk_ to compute _∇θJ_ ( _P, θk_ ), _∇θL_ ( _Pψk , P_ ) and _∇ψL_ ( _Pψk , P_ ) 13: Sample _Bkk_ to compute _∇ψJ_ ( _ψk, θk_ ) and _∇θJ_ ( _ψk, θk_ ) 14: Compose _∇f_ ( _ψk, θk_ ) and _∇q_ ( _ψk, θk_ ) from Eqs.11 and 12, and _λk_ 15: Append _∇f_ ( _ψk, θk_ ) + _λk∇q_ ( _ψk, θk_ ) to Ω 16: _ωk ← N_ <u>1</u> � _ω∈_ Ω<sup>_ω_</sup> 17: ( _ψk_ +1 _, θk_ +1) _←_ ( _ψk, θk_ ) _− ξ · ωk_ 18: **return** _ψ_<sup>ˆ</sup> _← ψk_ 

to bypass this difficulty either through surrogate approximations or heuristics that are difficult to control [Pedregosa, 2016, Ghadimi and Wang, 2018, MacKay et al., 2019]. Moreover, reinforcement learning objectives are highly non-convex, involve high-dimensional state–action spaces, and present a complex optimization landscape. As a result, naive bilevel optimization methods often fail to converge reliably, making them unsuitable for Problem 6 [Liu et al., 2021]. 

To obtain a more scalable solution, we adopt the first-order dynamic barrier gradient descent method (BOME) in [Liu et al., 2022], which reformulates the problem by replacing the implicit argmin operator with a value-function constraint. 

This allows the outer objective and inner objective to be solved without explicitly computing the derivative _∇ψθ_ ( _ψ_ ). Formally, let _f_ ( _ψ, θ_ ) := _J_ ( _P, θ_ ) + _L_ ( _Pψ, P_ ) denote the outer objective, and _q_ ( _ψ, θ_ ) := max _πθ′ J_ ( _Pψ, θ_<sup>_′_</sup> ) _− J_ ( _Pψ, θ_ ), which measures the suboptimality of _πθ_ relative to the optimal policy under _Pψ_ . Under the value-function approach, the bilevel problem becomes the following constrained optimization: 


This transformed problem is solvable by iteratively updating ( _ψ, θ_ ) to decrease _f_ while at the same time keeping the constraint _q ≤_ 0 satisfied by decreasing _q_ whenever _q >_ 0 in each step: 


this could be solved in closed form, which gives _ωk_ = _∇f_ ( _ψk, θk_ ) + _λk∇q_ ( _ψk, θk_ ), with _λk_ = _<u>ϕk−⟨∇f</u>_ <u>(</u> _<u>ψk,θk</u>_ <u>)</u> _<u>,∇q</u>_ <u>(</u> _<u>ψk,θk</u>_ <u>)</u> _<u>⟩</u>_ max _,_ 0 and _ϕk_ is chosen to be _ηq_ ( _ψ, θ_ ) or _η ∥∇q_ ( _ψ, θ_ ) _∥_<sup>2</sup> (we used � _∥∇q_ ( _ψk,θk_ ) _∥_<sup>2</sup> � _η ∥∇q_ ( _ψ, θ_ ) _∥_<sup>2</sup> in experiment and take _η_ = 0 _._ 5). Therefore, the procedure to optimize _f_ by jointly updating ( _ψ, θ_ ) is: 


where _∇f_ ( _ψk, θk_ ) = _∇_ ( _ψk,θk_ ) _f_ ( _ψk, θk_ ) is the gradient update of outer problem and _∇q_ ( _ψ, θ_ ) = _∇_ ( _ψ,θ_ ) _q_ ( _ψ, θ_ ) imposes the constraint. Expressed explicitly, the gradient of _f_ and _q_ are: 


where we use the shorthand _J_ ( _ψk, θk_ ) := _J_ ( _Pψk , θk_ ), and _θk_<sup>_W_is the</sup><sup>_W_-step approximation of the</sup> optimal policy _θ_<sup>_∗_</sup> _∈_ arg max _θ′ J_ ( _Pψ, θ_<sup>_′_</sup> ). 

20 

### **D.3 Stochastic Transition Functions Case** 

The stochastic world model minimizes the negative log likelihood to fine-tune on data _D_ 


where _s_<sup>_′_</sup> _∼ P_ ( _·|s, a_ ), and _P_ is the true environment transition, the loss function used in the bilevel optimization is defined as 


For _stochastic_ transitions, we define the residual as the KL divergence between the empirical next-state distribution induced by samples ( _s, a, s_<sup>_′_</sup> ) _∈ D_ and the model distribution: 


For _stochastic_ transition models, the gradients we defined in stage 2 are shown below 


where we use _P_<sup>ˆ</sup> _D_ ( _· | s, a_ ) denotes the empirical distribution of next states associated with ( _s, a_ ) in the dataset _D_ , in which given a ( _s, a_ ) pair an agent can sample multiple _s_<sup>_′_</sup> using environment dynamics or its transition models, establishing a distribution. 

The loss function of Stage 2 is defined as below. 

_L_<sup>sto</sup> _P_<sup>= (1</sup><sup>_−α_)</sup> �1 _−_ cos( _G_ real _, G_ target)� + _α_ � ��� _D_ KL� _P_ ( _· | si, ai_ ) _∥ P_<sup>ˆ</sup> _Dp_ ( _· | si, ai_ )� _− D_ KL� _P_ ( _· | si, ai_ ) _∥ Pψ_ ˆ<sup>(</sup><sup>_· | si, ai_)</sup> �<sup>�</sup> �� _._ ( _si,ai_ ) _∈Dp_ (17) For stochastic world models, we define fine-tune data-level deviation _δd_ = _|D_ <u>1</u><sup>˜</sup> _|_ �( _si,ai_ ) _∈D_<sup>˜</sup><sup>_D_KL</sup> � _P_ ( _·|si, ai_ ) _∥ P_<sup>ˆ</sup> ˜ _D_<sup>(</sup><sup>_·|si, ai_)</sup> � and test-time model-level deviation _δm_ = _T_ <u>1</u> � _Ti_ =0<sup>_D_KL</sup> � _P_ ( _·|si, ai_ ) _∥ P_<sup>ˆ</sup> _ψ_ ( _·|si, ai_ )� where _T_ is the number of observed transitions. 

## **E Implementation Details** 

We instantiate the experiment based on the TD-MPC2 framework. Thus all neural networks including policy, dynamics model, encoder and value function have MLP architecture with several layers, for detailed information about architecture, please refer to [Hansen et al., 2024]. 

21 

### **E.1 Model Predictive Control** 

**Algorithm 2** General Model Predictive Control (MPC) 


- 8: Select best sequence(s) according to _J_<sup>_i_</sup> 

- 9: Refit a sampling distribution to top- _K_ sequences 

- 10: **return** first action or first _k_ actions from selected sequence or sampler 

We provide a general formulation of Model Predictive Control (MPC), which abstracts across variants such as TD-MPC2 [Hansen et al., 2024], DINO-WM [Zhou et al., 2025]. In this section, we occasionally use _z_ ˆ to denote an imagined latent, compared to the real latent _z_ encoded from the real state _s_ from the environment. 

To model the dynamics, TD-MPC2 [Hansen et al., 2024] learns the world model _Pψ_ ( _z_<sup>_′_</sup> _|z, a_ ) that predicts next latent state given current latent state and action, where _z_ = _enc_ ( _s_ ) is the latent state from a learned encoder, and its agent plans by using the learned world model _Pψ_ together with a learned prior policy _π_ prior. At each planning step, the planner first obtains `num_pi_trajs` candidate trajectories by rolling out _π_ prior under transition _Pψ_ ; these yield the policy-guided action sequences. The planner then samples an additional `num_samples` _−_ `num_pi_trajs` random action sequences from a stochastic proposal (e.g., i.i.d. or Gaussian-perturbed sequences). During the inner improvement/refit loop, the action components coming from the prior policy are treated as guidance and are typically held fixed, while only the remaining (random) action sequences are optimized. This hybrid design reduces search dimensionality and biases search toward plausible behavior while still allowing exploratory refinement. 

DINO-WM [Zhou et al., 2025] does not use a learned prior. Instead, it draws many random action sequences, rolls each sequence forward in the world model _Pψ_ for horizon _H_ , and scores each rollout by a final-state objective (the distance to a goal latent _zg_ , e.g., _J_ = _∥z_ ˆ _H − zg∥_ 2). The top-performing sequences are retained as elites and the sampling distribution is refit to those elites (CEM-style); this process repeats until the sampling distribution concentrates on sequences that reach the goal. 

The above MPC algorithm highlights the shared structure: rolling out candidate action sequences over a planning horizon _H_ using a learned world model _Pψ_ , evaluating them under a task-specific objective (e.g., bootstrapped return, goal closeness, or other criteria), and executing the first action of the best sequence. The number of sampled rollouts `num_samples` and the planning horizon _H_ are hyperparameters that directly affect the quality of planning and computation cost. The general MPC procedure is summarized in Algorithm 2. 

### **E.2 Hyperparameters** 

We report our SWAAP key hyperparameters in Table 2. Other parameters are the same as stated in TD-MPC2 [Hansen et al., 2024]. 

22 

Table 2: Key hyperparameters used in experiments; other parameters are the same as in TD-MPC2 

|**Hyperparameter**|**Typical value(s)**|**Description**|
|---|---|---|
|**Model Poisoning Hy**|**perparameters**||
|obs_dim|17-223|The range of observation dimensions for tasks|
|action_dim|6-39|The range of action dimensions for tasks|
|latent_dim|512|The latent state dimension to encode observation state|
|H|3|Planning horizon length, which is the number of rollout<br>steps into the future when planning|
|num_samples|512|<br>Total number of trajectories for planning, including<br>policy trajectories and random trajectories|
|policy_samples|24|<br>number of trajectories for planning that are from policy<br>prior|
|iterations|6|number of iterations done to optimize the actions in<br>planning|
|_λ_|_{_0_,_ 1_,_ 10_,_ 100_}_|Consistency coefficient applied to the_L_(_P, Pψ_)term<br>during model poisoning in Equation 6|
|_W_|_{_30_}_|<br>The number of update steps used to approximate_θ_<sup>_∗_</sup><br>_k_|
|_N_|_{_16_}_|<br>The size ofΩ, the number of small updates aggregated<br>to compute gradients of_fk, qk_ and_λk_|
|sample_batch_size|_{_256_}_|<br>Number of transitions used to calculate each sample in<br>Ω|
|num_step|_{_100_,_500_}_|The imagined rollout length, 500 for DMControl tasks<br>and 100 for others.|
|buffer_size|_{_500_}_|Buffer size for every buffer used in Algorithm 1.|
|**Data Poisoning Hyp**|**erparameters**||
|_rp_|_{_0_._1_,_ 0_._2_,_ 0_._3_}_|Fraction of the dataset (or proportion of trajecto-<br>ries/transitions) modified by adversary.|
|_α_|_{_0_._1_,_ 0_._5_,_ 0_._9_,_ 0_._95_,_ 0_._9|i<br>9_}_ Data poisoning regularization coefficient in Equation 5|
|poison_steps|_{_5000_}_|The number of gradient matching update steps.|
|step_size|_{_10_}_|Step size to update the poisoned samples in gradient<br>matching.|
|noise_scale|_{_0_._1_,_0_._3_,_0_._5_}_|The random perturbation scale of SWAAP (Random)|
|train_epochs|_{_100_,_500_}_|<br>The number of training epochs for fine-tuning, 100 for<br>DMControl tasks and 500 for others.|
|learning_rate|_{_0_._01_,_0_._0001_}_|Learning rate of fine-tuning, 0.01 for MyoSuite and<br>0.0001 for others.|
|_|D|_|_{_5000_}_|Size of the fine-tuning dataset.|
|_|D_all_|_|_{_50000_}_|Size of the dataset to approximate_G_target|


### **E.3 Stage 1: Target Model Identification** 

The model poisoning starts with a trained TD-MPC2 checkpoint (such as humanoid-walk-2.pt from TD-MPC2 model base), from which following components are extracted as input to Algorithm 1, the trained policy network _πθ_ as _θ_ 0, the dynamics model _Pψ_ is used as _ψ_ 0, the value network (a _Q_ net in TD-MPC2), reward model, and an encoder, where the reward model and encoder will be freezed during model poisoning for there are no more information about the reward and encoding to be gained in our adversarial training. The model-based agent consists of a prior policy _θ_ and transition model _ψ_ , and _πθ_ ( _ψ_ ) stands for the agent’s policy that it takes after conducting MPC planning in imagined trajectories generated from the prior policy _θ_ and transition _ψ_ . 

During each iteration of update, the trajectory rollouts are collected from ( _ψk, θk_<sup>_W_), (</sup><sup>_P, θk_), (</sup><sup>_ψk, θk_)</sup> to form _BkW_ , _Bpk_ , _Bkk_ , which means _BkW_ is formed by trajectories generated by MPC policy _πθkW_<sup>(</sup><sup>_ψk_) and transition</sup><sup>_ψk_,</sup><sup>_Bpk_is formed by trajectories generated by MPC policy</sup><sup>_πθk_(</sup><sup>_ψk_) and</sup> environment transition _P_ , and _Bkk_ is formed by trajectories generated by MPC policy _πθk_ ( _ψk_ ) and transition _ψk_ . Using the reward model, the value network is updated on trajectories collected from ( _ψk, θk_ ) by minimizing the TD error. 

Given data ( _s, a, s_<sup>_′_</sup> ), the policy return gradient _∇θk J_ ( _ψ, θ_ ) is computed using the TD-MPC2 update_pi function, which varies the action to maximize the value estimate _Q_ ( _s, apred_ ) and a scaled action entropy at the same time, where _apred_ is sampled from prior policy _θk_ given state _s_ . The 

23 

transition return gradient _∇ψk J_ ( _ψ, θ_ ) is computed by varying the prediction _s_<sup>_′_</sup> _pred_<sup>=</sup><sup>_Pψ_(</sup><sup>_s, a_) to</sup> minimize the value estimate of predicted next state _Q_ ( _s_<sup>_′_</sup> _pred_<sup>_, a′_</sup> _pred_<sup>) where</sup><sup>_a′_</sup> _pred_<sup>is sampled from</sup> prior policy _θk_ given state _s_<sup>_′_</sup> _pred_<sup>.</sup> 

During training of Stage 1, we evaluate _J_ ( _P, πθ_ 0( _ψk_ )), the return of an unmodified policy using the perturbed world model _ψk_ to plan in real environment _P_ , for 10 episodes every 10 iterations, producing figures like Fig. 5, from which we can select the identified perturbed world model based on the testing performance (ideally one with low return while _δm_ is also low), and this identified dynamics model will be used to propose the perturbed next state in Stage 2. 

### **E.4 Stage 2: Data Poisoning** 

The first steps in Stage 2 involves collecting two datasets, one large dataset of 50 _,_ 000 transitions (which translates to 100 independent trajectories for DMControl tasks 500 for all other tasks) for estimating the target gradient _Gtarget_ , and one small dataset of 5 _,_ 000 transitions for _Greal_ . During data collection, each action has a 3% chance of being replaced by a random uniform action, which is done for data diversity and to cover enough state-action pairs. 

Given the fine-tune dataset, the deviations _eψ_ ( _s, a, s_<sup>_′_</sup> ) of each transition are calculated and ranked, and the top _rp_ transitions are selected to be poisoned, which are considered to be more vulnerable than other transitions. To ensure the perturbation remains stealthy, after each gradient matching step, we project the perturbed state _s_ ˜<sup>_′_</sup> back to the L2 norm ball around the original state _s_<sup>_′_</sup> , but since TD-MPC2 world model constrains the output prediction within a valid range by architectural design, this step is not needed in our main experiments. 

Once the poisoned data are crafted, we choose the fine-tuning hyperparameters (train_epochs and learning_rate) so that fine-tuning the clean world model on clean data of the same size does not degrade performance. This ensures that the observed degradation is caused by poisoning rather than overfitting during fine-tuning. 

SWAAP (Random) use the same setting in Stage 2 like SWAAP, and the only difference comes from that the perturbed model _P_ ˆ _ψ_<sup>is not learned but crafted from applying a random perturbation</sup> of scale being _noise_  scale_ elementwise to the true transition, which is _s_ ˜<sup>_′_</sup> = _s_<sup>_′_�</sup> (1 + _ϵ_ ) with _ϵ ∼_ [ _−noise_  scale, noise_  scale_ ], we report SWAAP (random) with _noise_  scale_ = 0 _._ 3 in Table 1 and in Appendix F.1. 

### **E.5 Hardware Specification and Computational Cost** 

We conduct all experiments on a workstation with an Intel Core Ultra 9 285K CPU, an NVIDIA GeForce RTX 5080 GPU with 16GB VRAM, and 64GB system RAM. 

Stage 1 takes approximately 1 hour on DMControl and MetaWorld and 2 hours on MyoSuite. Stage 2 takes roughly 10 minutes. Our attack designs intentionally reduce computational overhead: (1) Stage 1 uses a first-order dynamic barrier method, avoiding the expensive Hessian computations typically required in bilevel optimization; (2) Stage 2 employs a modified gradient-matching step that selects the most influential data points for poisoning instead of exhaustively searching over all possible combinations, which significantly reduces computational cost. 

## **F Main Extended Results** 

### **F.1 SWAAP and SWAAP (Random)** 

We show more results on SWAAP and SWAAP(Random) in Figure 4, comparing the return and _δm_ of various tasks under SWAAP, SWAAP(Random) with the clean return and clean _δm_ at different poison ratios _rp_ . A higher _α_ constrains model deviation more strictly, reducing attack strength but improving stealth. A lower _α_ relaxes the deviation constraint and increases performance degradation. A higher data poisoning rate _rp_ will also strengthen our attack performance. 

Empirically, across all tested _α_ and _rp_ , we did not observe gradient explosion or vanishing. Optimization remained numerically stable throughout Stage 2. 

24 


Figure 4: SWAAP and SWAAP (Random) across poisoning ratios _rp_ and stealth weights _α_ . Blue bars show return and red bars show model-level deviation25 _δm_ . Lowering _α_ often increases SWAAP’s return degradation more than SWAAP (Random), showing that the Stage 1 target provides useful poisoning directions beyond random perturbation. 


Figure 5: Model poisoning curves (referred to as Direct Model Poisoning in Table 1) of return and _δm_ tested across different training iterations under different _λ_ , each testing is the average of 10 test episodes, and thus each data point is a single run with 10 episodes. From these plots, we observe that _λ_ is suppressing the deviation of the model, but the varying influence of _λ_ over different environments implies that a different _λ_ is required to constrain the perturbation of the model. 

### **F.2 Model Poisoning Training Curve** 

We show the stage one model training curve in Figure 5, which comes from testing the agent that directly uses the perturbed model for 10 episodes after every few iterations of updates. From these plots, we observe that _λ_ suppresses the model’s deviation, but the varying influence of _λ_ across different environments implies that different _λ_ values are required to constrain the model’s perturbation. 

### **F.3 Pre-Training Detection** 

Figure 7 presents additional results on pre-training detection, showing the distribution of data-level deviation before and after poisoning under different values of the poisoning regularization coefficient _α_ . As _α_ increases, the deviation of the poisoned transitions becomes more similar to those of clean data, making the attack more difficult to detect using deviation-based filtering. 

### **F.3.1 Residual-Based CUSUM Pre-Training Detector** 

We evaluate a CUSUM-style sequential detector to screen candidate fine-tuning trajectories before they are used for model updates. Instead of using the latent-state norm _∥zt_ +1 _∥_ 2, we use a transitionresidual statistic measured against the clean reference world model: 


This statistic is aligned with pre-training detection because a defender with a reference world model can test whether each observed transition is anomalous relative to the predicted next latent state. 

Given clean calibration trajectories, we estimate a robust center and scale using the median _m_ and median absolute deviation MAD of the residual signal. For each candidate trajectory, we form centered residuals _rt_ = _xt − m_ and update a one-sided CUSUM statistic 


We use the trajectory-level score max _t St_ for detection. The threshold is chosen from held-out clean trajectories to target a false-positive rate of 5%, and we report ROC-AUC, TPR at the clean-calibrated threshold, and the realized empirical FPR. 

For Humanoid-Walk, we use 100 clean trajectories (50,000 transitions) to estimate the residual median/MAD and 10 separate held-out clean trajectories (5,000 transitions) to estimate empirical FPR; we compare against 10 poisoned trajectories. Because this held-out set contains only 10 clean trajectories, the empirical FPR is quantized in increments of 0 _._ 10. For MW-Push, we use 500 clean trajectories (50,000 transitions) for calibration and 50 held-out clean trajectories (5,000 transitions) for empirical FPR; we compare against 50 poisoned trajectories. 

26 

Table 3: Residual-based CUSUM pre-training detection. The detector uses _xt_ = _∥zt_ +1 _− Pψ_ ref ( _zt, at_ ) _∥_ 2 and scores each trajectory by max _t St_ . Thresholds target FPR 5% on held-out clean trajectories; empirical FPR differs slightly because of finite held-out sets. 

|Environment|_α_|AUC|TPR|Emp. FPR|Mean residual|
|---|---|---|---|---|---|
|Humanoid-Walk|0.1|0.665|0.20|0.10|0.4034|
|Humanoid-Walk|0.5|0.530|0.10|0.10|0.3821|
|Humanoid-Walk|0.9|0.520|0.10|0.10|0.3745|
|Humanoid-Walk|0.99|0.520|0.10|0.10|0.3732|
|MW-Push|0.1|0.864|0.40|0.06|0.3810|
|MW-Push|0.5|0.550|0.08|0.06|0.3465|
|MW-Push|0.9|0.509|0.08|0.06|0.3334|


Figure 6: Trajectory-level ROC curves for the residual-based CUSUM detector on MW-Push. Each candidate fine-tuning trajectory is assigned the score max _t St_ , and ROC curves are computed by treating clean and poisoned trajectories as negative and positive examples. The aggressive low-stealth setting _α_ = 0 _._ 1 is more detectable, while the stealth-prioritized setting _α_ = 0 _._ 9 lies close to the chance diagonal, consistent with Table 3. 

Table 3 and Figure 6 show that the detector separates aggressive low- _α_ attacks more clearly, especially on MW-Push: at _α_ = 0 _._ 1, AUC reaches 0 _._ 864 and TPR is 0 _._ 40 at empirical FPR 0 _._ 06. However, under the stealth-prioritized settings used in the main experiments, the detector has little power: MW-Push at _α_ = 0 _._ 9 gives AUC 0 _._ 509 and TPR 0 _._ 08 at empirical FPR 0 _._ 06, while HumanoidWalk at _α_ = 0 _._ 9 gives AUC 0 _._ 520 and TPR 0 _._ 10 at empirical FPR 0 _._ 10. These results do not prove indistinguishability against all sequential detectors; rather, they show that a natural residualbased CUSUM screen detects aggressive low-stealth poisoning but loses power under SWAAP’s stealth-regularized operating points. 

### **F.3.2 Latent-Space PCA Visualization** 

We additionally visualize data-level stealthiness using PCA in the latent space used by the world model. This visualization is intended as a qualitative sanity check complementary to the scalar deviations in Table 1. For Humanoid-Walk with _α_ = 0 _._ 9, we take the 500 transitions selected for poisoning and compare their clean next-state latents _z_<sup>_′_</sup> , poisoned next-state latents _z_ ˜<sup>_′_</sup> , and clean/reference-model predicted next-state latents _Pψ_ ref ( _z, a_ ). The poisoned-target plot illustrates the deviation from true next-states, while the clean-model-prediction plot illustrates the natural reference residual scale corresponding to _δm,_ ref . 

To make the visualization comparable, PCA is fitted on the pooled latent samples used in each panel and the first two principal components are plotted. Figure 8 shows that poisoned next-state targets largely overlap with their clean next-state counterparts and that their centroid remains close to the clean centroid. The clean/reference-model predictions show a similar overlapping pattern relative to true next states. This supports the interpretation that SWAAP’s poisoned targets are not obvious latent outliers under this two-dimensional projection. Since PCA only captures the leading low-dimensional variation, this result should not be interpreted as proof of indistinguishability; rather, it provides qualitative evidence consistent with the _δd_ and _δ_ ref measurements. 

27 


Figure 7: Pre-training data-level deviation across stealth weights _α_ . Blue bars denote the clean reference residual _δ_ d _,_ ref and red bars denote poisoned-data deviation _δd_ . Across _α_ , poisoned targets remain close to the clean reference residual scale in most environments, even when lower _α_ increases attack strength. 


Figure 8: Latent-space PCA visualization on Humanoid-Walk. (a) compares poisoned next-state targets _z_ ˜<sup>_′_</sup> with their clean sources _z_<sup>_′_</sup> , illustrating the data-level perturbation relative true states, note this is different from _δd_ . (b) compares clean/reference-model predictions _Pψ_ ref ( _z, a_ ) with true next states _z_<sup>_′_</sup> , illustrating the natural reference residual scale _δ_ ref . Poisoned targets largely overlap with clean next states, similar to the clean model’s natural prediction residuals. 

### **F.4 Stage 1–Stage 2 Realization Bottleneck** 

SWAAP separates target identification from target realization. Stage 1 searches for a target world model _P_ ˆ _ψ_<sup>that induces low return while remaining close to clean dynamics.Direct Model Poisoning</sup> evaluates this target model directly and therefore measures the strength of Stage 1 under an unrealistic model-overwrite threat model. Stage 2 then attempts to realize the selected target model using only bounded data poisoning. Since the attacker can modify only an _rp_ fraction of fine-tuning transitions and must keep poisoned targets stealthy, Stage 2 is expected to realize only part of the effect achieved by direct model overwrite. 

We quantify this realization gap on Humanoid-Walk. With _α_ = 0 _._ 1 and _rp_ = 0 _._ 3, the clean model has deviation _δm_ ( _Pψ_ ˆ<sup>_, Pψ_0) = 0</sup><sup>_._15 from the Stage 1 target, while the Stage 2 poisoned model reaches</sup> _δm_ ( _Pψ_ ˆ<sup>_, Pψ_)=0</sup><sup>_._11relativetothetargetmodel.ThisshowsthatStage2recoversasubstantial</sup> portion of the Stage 1 target, but does not exactly match it. More broadly, Figure 3 shows this bottleneck as a gap between the Direct Model Poisoning frontier and the SWAAP frontier: in Humanoid-Walk, SWAAP closely tracks the Direct Model Poisoning frontier, while in Myo-PenTwirl-Hard the gap is larger, indicating that some harmful target models are more difficult to realize through gradient-matched poisoned data. 

28 

Table 4: Offline iterative-FGSM/ _ℓ∞_ -PGD transition-perturbation baseline on MW-Push. The baseline directly perturbs next-state targets to reduce the value of a clean prior policy, without Stage 1 targetmodel identification or Stage 2 gradient matching. SWAAP achieves a lower return while keeping _δd_ comparable or lower. Values are mean _±_ std. 

|Method|Return|_δm_|_δd_|
|---|---|---|---|
|Clean|1784_±_13|0_._080_±_|0_._002<br>0_._0799|
|PGD (_ϵ_= 0_._015)|1732_±_56|0_._107_±_|0_._012<br>0_._0832|
|PGD (_ϵ_= 0_._05)|1666_±_76|0_._121_±_|0_._008<br>0_._0983|
|SWAAP|1641_±_80|0_._171_±_|0_._011<br>0_._0805|


We further test whether directly using the Stage 1 target predictions as poisoned data is sufficient. We define **DMP-data** as a variant that replaces the selected top- _rp_ next states with predictions from the Stage 1 target model _P_ ˆ _ψ_<sup>, without optimizing the Stage 2 gradient-matching objective.DMP-data</sup> remains stealthy at the data level, with _δd_ = 0 _._ 0872 _±_ 0 _._ 0425, comparable to the clean reference residual 0 _._ 0897 _±_ 0 _._ 0455. However, it is less effective than SWAAP, especially under robust training. Without TRIM, DMP-data gives _R_ = 727 _±_ 205 and _δm_ = 0 _._ 116 _±_ 0 _._ 065, while SWAAP gives _R_ = 521 _±_ 332 and _δm_ = 0 _._ 145 _±_ 0 _._ 079. Under TRIM, DMP-data gives _R_ = 599 _±_ 297 and _δm_ = 0 _._ 130 _±_ 0 _._ 071, while SWAAP gives _R_ = 183 _±_ 356 and _δm_ = 0 _._ 192 _±_ 0 _._ 075. Thus, directly copying target-model next states is not enough; the gradient-matching realization step better steers fine-tuning toward the target dynamics. 

Overall, these results identify target realization under attack–stealth constraints as the main practical bottleneck and an opportunity to improve the current two-stage implementation. Stage 1 can identify harmful low-deviation target models, but Stage 2 must approximate them using a small number of poisoned transitions. This explains why Direct Model Poisoning is often stronger than SWAAP, and also why improving Stage 2 or making Stage 1 aware of Stage 2 realizability is a promising direction for future work. 

## **G Ablations and Baselines** 

### **G.1 Iterative FGSM/PGD Transition-Perturbation Baselines** 

We compare SWAAP with iterative signed-gradient transition-perturbation baselines adapted from adversarial state-perturbation attacks. These baselines do not identify a target world model or match fine-tuning gradients. Instead, they directly perturb next-state targets to lower the value of a prior policy _πθ_ trained from the clean world model. 

For a clean transition ( _s, a, s_<sup>_′_</sup> ), we initialize ˜ _s_<sup>_′_</sup> 0<sup>=</sup><sup>_s′_and run</sup><sup>_K_projected signed-gradient steps:</sup> 


where _η_ is the step size, _ϵ_ bounds the maximum per-coordinate perturbation, and Π[ _s′−ϵ,s′_ + _ϵ_ ] denotes projection to the _ℓ∞_ box around the original next state. When _K_ = 1, this reduces to an FGSM-style perturbation; for _K >_ 1, it is an iterative-FGSM / _ℓ∞_ PGD-style baseline. 

We evaluate two variants. The **offline transition-perturbation baseline** applies this replacement to fine-tuning transitions before model update, matching our data-poisoning setting. The **online state-perturbation baseline** applies an analogous perturbation at test time to the state observed by the victim. The online variant is not the same threat model as SWAAP because it requires test-time intervention, but it provides context against a standard adversarial-state attack. 

Table 4 shows that the offline signed-gradient transition-perturbation baseline is weaker than SWAAP on MW-Push. Increasing _ϵ_ improves its attack strength but also increases _δd_ , making the poisoned data less stealthy before fine-tuning. In contrast, SWAAP achieves a lower return with _δd_ close to the clean reference scale, because it poisons data to steer the fine-tuning gradient toward a harmful target world model rather than applying only local value-reducing perturbations. 

For the online state-perturbation comparison, iterative signed-gradient perturbation with _ϵ_ = 0 _._ 01 gives _R_ = 1785 _±_ 5 and _δm_ = 0 _._ 106 _±_ 0 _._ 003, while _ϵ_ = 0 _._ 02 gives _R_ = 1719 _±_ 48 and _δm_ = 0 _._ 159 _±_ 0 _._ 010. SWAAP gives _R_ = 1641 _±_ 80 and _δm_ = 0 _._ 171 _±_ 0 _._ 011. This comparison is 

29 

Table 5: Effect of MPC hyperparameters ( `num_samples` , horizon _H_ ) on reward under clean and SWAAP settings evaluated in Humanoid-Walk. Values are mean _±_ std over 10 episodes. 

|N Sl|||Return||
|---|---|---|---|---|
|um ampes||_h_= 3|_h_= 6|_h_= 9|
|64|Clean<br>SWAAP|12_±_21<br>7_±_7|5_±_4<br>19_±_39|9_±_21<br>14_±_20|
||Clean|150_±_95|58_±_92|2_±_2|
|128|SWAAP|101_±_85|38_±_51|43_±_41|
||Clean|788_±_157|488_±_279|68_±_115|
|256|SWAAP|347_±_257|93_±_93|21_±_36|
|512|Clean|855_±_62|687_±_112|37_±_61|
||SWAAP|594_±_203|49_±_61|41_±_58|
||Clean|875_±_63|812_±_91|385_±_287|
|1024|SWAAP|656_±_192|87_±_147|75_±_92|


Table 6: Attack performance with different poison fraction in Stage 1 in Humanoid-Walk with _α_ = 0.9 

|Stage 1poison fraction|Return|_δm_|
|---|---|---|
|0%(clean)|866 ± 57|0.09 ± 0.05|
|10%|825 ± 106|0.10 ± 0.06|
|50%|669 ± 242|0.12 ± 0.07|
|100%|521 ± 332|0.14 ± 0.08|


not a direct threat-model match: online perturbation requires modifying states at test time, whereas SWAAP modifies only fine-tuning data and induces later failures through the learned world model. Nevertheless, it shows that SWAAP can produce comparable or stronger degradation without test-time intervention. 

### **G.2 Top-** _rp_ **Transition Selection vs. Random Selection** 

Stage 2 first selects the subset of transitions to poison. Under a fixed poisoning budget _rp_ , our default heuristic selects the top- _rp_ transitions with the largest deviation from the Stage 1 target model. These transitions are the most inconsistent with the target dynamics, so modifying them should provide a stronger fine-tuning signal toward the target than modifying randomly selected transitions. 

We test this heuristic on Humanoid-Walk using the same Stage 1 target model and the same poisoning budget. Replacing top- _rp_ selection with random transition selection weakens the attack: top- _rp_ selection gives _R_ = 775 _±_ 50 and _δm_ = 0 _._ 110 _±_ 0 _._ 007, while random selection gives _R_ = 822 _±_ 13 and _δm_ = 0 _._ 102 _±_ 0 _._ 002. Thus, selecting transitions most inconsistent with the Stage 1 target improves attack effectiveness at comparable model-level deviation. 

### **G.3 MPC Hyperparameter Ablation** 

Table 5 reports the reward of TD-MPC2 under different rollout horizons ( _h_ = 3 _,_ 6 _,_ 9) and number of samples for both the clean and SWAAP settings. We observe that our SWAAP attack consistently reduces the agent’s performance across all configurations, demonstrating its effectiveness under every setting. Additionally, the MPC performance generally increases with the number of samples and decreases as the rollout horizon grows. Consequently, the impact of our attack is also influenced by these hyperparameters: it tends to be more significant when the baseline MPC performance is higher (larger sample sizes) and slightly less effective at longer horizons given the low clean reward. 

### **G.4 Stage 1 Masked Perturbation Fraction** 

Stage 1 of SWAAP can be adjusted to only perturb a certain fraction of the state-action pairs’ transitions. We have conducted additional experiments on perturbing the top 10% and 50% most influential state-action pairs compared to perturbing all pairs considered before in Humanoid-Walk with _rp_ = 0 _._ 1 _, α_ = 0 _._ 9 in Table 6. Stage 1 optimizes the parameters of a global neural world model, so changing _ψ_<sup>ˆ</sup> can in principle affect predictions beyond any selected subset of inputs. In this ablation, 

30 

Table 7: Attack performance with different data poison ratio ( _rp_ ) in Stage 2 in Humanoid-Walk with _α_ = 0.9 

|_rp_|Return|_δm_|
|---|---|---|
|clean|866 ± 57|0.09 ± 0.05|
|0.01|844 ± 94|0.10 ± 0.05|
|0.05|739 ± 172|0.11 ± 0.07|
|0.10|521 ± 332|0.14 ± 0.08|
|0.20|317 ± 339|0.18 ± 0.08|
|0.30|242 ± 305|0.19 ± 0.08|


“perturbing a fraction of state-action pairs” therefore means that we restrict the Stage 1 perturbation objective to a masked subset of rollout transitions, rather than enforcing a hard functional constraint that the model output is unchanged elsewhere. Specifically, after collecting rollout transitions, we compute an importance score for each state using the value-spread criterion from Liang et al. [2022], 


We then select the top- _wc_ fraction of transitions by this score and apply the Stage 1 target-model perturbation loss only on this selected subset. The rest of the transitions still contribute to the usual model-level deviation/stealth regularization when applicable, but they do not receive direct target-perturbation pressure. Thus, the ablation measures how the attack changes when Stage 1 is guided by increasingly sparse sets of high-importance transitions, not an exact guarantee that the learned neural model changes only on those inputs. 

Table 6 shows that increasing this selected fraction strengthens the attack but also increases _δm_ , giving a tunable effectiveness–stealth trade-off. 

### **G.5 Stage 2 Poisoning Ratio** _rp_ 

We conduct an ablation study on different _rp_ ratios in Stage 2, with results in Table 7. We observe that with lower poisoning rates (1% and 5%), the attack performance decreases as expected, but it still consistently induces noticeable degradation in return. 

### **G.6 Trajectory-Consistent Data Poisoning** 

The Stage 2 formulation in Eq. 5 treats the fine-tuning data as a transition buffer, where each tuple ( _st, at, st_ +1) can be poisoned by replacing only the next-state target. In sequential trajectory data, however, the same intermediate state appears in two adjacent tuples: 


Therefore, replacing _st_ +1 only as the next-state target of the first tuple would make the stored trajectory internally inconsistent. To adapt SWAAP to this setting, we use a trajectory-consistent update: when transition _t_ is selected for poisoning, we replace both occurrences of the intermediate latent state, 


Terminal transitions are excluded so that _t_ + 1 always belongs to the same trajectory. In the gradientmatching step, we add a SARSA-style consistency term so the matching gradient becomes 


which encourages the poisoned intermediate state to be both reachable from ( _st, at_ ) and predictive of the observed successor under _at_ +1. After each poisoned-target update, we explicitly enforce _st_ +1 = _s_ ˜ _t_ +1 in the next tuple, so the saved poisoned data remain trajectory-consistent. 

On Humanoid-Walk, trajectory-consistent poisoning with _rp_ = 0 _._ 05 gives return 784 _±_ 19 and modellevel deviation _δm_ = _._ 111 _± ._ 003, with data-level reference deviation _δd_ = _._ 102 _± ._ 007. Compared with the standard transition-buffer setting in Table 1, the attack is weaker, as expected, because the consistency constraint reduces the degrees of freedom available to the poisoner. Nevertheless, the result shows that SWAAP can be adapted from independent transition buffers to sequential fine-tuning trajectories. 

31 

Table 8: Effect of fine-tuning dataset size in HumanoidWalk. 

|**Fine-tuning Dataset Size**|**Return**|_δm_|
|---|---|---|
|5,000|521_±_332|0_._14_±_0_._08|
|10,000|540_±_348|0_._14_±_0_._08|
|15,000|550_±_306|0_._14_±_0_._08|
|20,000|607_±_300|0_._13_±_0_._08|
|25,000|679_±_234|0_._12_±_0_._07|


Table 9: Additional evaluation on MyoSuite and MetaWorld environments. Each test is a single run with 100 episodes. 

|**Environment**|**Natural Return**|**SWAAP Return**|**Natural**_δm_|**SWAAP**_δm_|
|---|---|---|---|---|
|myo-obj-hold-hard|_−_289_±_2343|_−_2671_±_4241|0_._10_±_0_._07|0_._13_±_0_._05|
|myo-pose|696_±_4|665_±_157|0_._04_±_0_._04|0_._08_±_0_._06|
|myo-key-turn|1125_±_196|940_±_375|0_._19_±_0_._14|0_._11_±_0_._08|
|mw-coffee-pull|1511_±_25|1402_±_318|0_._08_±_0_._04|0_._09_±_0_._06|
|mw-door-open|1551_±_58|1310_±_445|0_._04_±_0_._02|0_._06_±_0_._05|


### **G.7 Larger Fine-Tuning Buffers** 

We conducted additional experiments on `HumanoidWalk` using fine-tuning dataset sizes ranging from 5,000 to 25,000, with a fixed budget of 500 poisoned transitions. The results are shown in Table 8. Although increasing the fine-tuning dataset size reduces the magnitude of performance degradation, as larger clean buffers naturally dilute the poisoned portion, SWAAP still consistently induces meaningful return drops across all tested sizes, demonstrating its robustness even when the victim fine-tunes on substantially larger datasets. 

## **H Generalization Experiments** 

### **H.1 Additional MyoSuite and MetaWorld Environments** 

We conducted additional experiments on five MyoSuite and MetaWorld tasks, with results reported in Table 9. All experiments use _rp_ = 0 _._ 1 and are evaluated over 100 episodes. For `Obj-Hold-Hard` , `Key-Turn` , and `Coffee-Pull` , we set _α_ = 0 _._ 9, while for `Pose` and `Door-Open` , we use _α_ = 0 _._ 1. These results further confirm that SWAAP reliably reduces the return while keeping the poisoned world model close to the clean model, consistent with our main findings. 

### **H.2 DINO-WM Push-T Results** 

We adapted our method to the DINO-WM world models for goal-conditioned tasks [Zhou et al., 2025]. Our experimental setup largely follows the configuration used in the original implementation; the detailed settings are provided in Table 10. 

For Stage 1, we used a goal-conditioned RL agent as the surrogate policy. Preliminary results show that the identified target world model reduces the success rate on the Push-T task from 92% to 72%, with the relative deviation increasing from _δm_ = 0 _._ 11 _±_ 0 _._ 06 to _δm_ = 0 _._ 24 _±_ 0 _._ 10. 

We then conducted additional experiments incorporating Stage 2 of our attack pipeline. Using the perturbed model identified in Stage 1, we employed gradient matching to generate poisoned samples (poisoning ratio 0.15) and fine-tuned a DINO-WM model on the resulting poisoned dataset. On the Push-T task, performance dropped from 92% to 77%, with _δm_ = 0 _._ 16 _±_ 0 _._ 09. These early results suggest that the method can extend beyond TD-MPC2 to goal-conditioned visual world models, although a broader evaluation is left for future work. 

### **H.3 Gray-Box Attack on TD-MPC2 Multi-Task World Model** 

We conducted a preliminary gray-box experiment in which the attacker only has access to a surrogate world model trained on a single task, while the victim employs a multi-task world model. The attacker performs Stage 1 and Stage 2 entirely on the surrogate model and then supplies the resulting poisoned dataset to the victim for fine-tuning. In this experiment, the surrogate is a TD-MPC2 world model trained on MW-Soccer, whereas the victim is a multi-task world model used across multiple tasks. 

32 

Table 10: Key hyperparameters used in the DINO-WM Push-T experiment 

|**Hyperparameter**|**Typical value(s)**|**Description**|
|---|---|---|
|obs_shape|(3, 224, 224)|Shape of pixel observation_s_.<br>|
|latent_shape|(196, 394)|Shape of latent state_z_ = enc(_s_).|
|action_dim|10|Dimension of actions.|
|num_hist|3|Number of historical latent states used to predict the next state.|
|H|5|Planning horizon length (number of rollout steps during planning),<br>which also corresponds to the number of planned actions.|
|num_samples<br>opt_steps|100<br>30|Total number of sampled trajectories during planning.<br>Number of optimization iterations per planning step using cross-<br>entropy method (CEM).|


Table 11: Gray-box attack on TD-MPC2 multi-task world model 

|**Source Task**|**Target Task**|**Setting**|**Return (R**_±_**std)**|**_δm_ (**_±_**std)**|
|---|---|---|---|---|
|MW-Soccer|MW-Soccer|Natural|1380_±_382|0_._11_±_0_._11|
|MW-Soccer|MW-Soccer|SWAAP|1115_±_442|0_._13_±_0_._12|
|MW-Soccer|MW-Push|Natural|1290_±_609|0_._13_±_0_._16|
|MW-Soccer|MW-Push|SWAAP|1064_±_692|0_._16_±_0_._19|


We use _rp_ = 0 _._ 1 _, α_ = 0 _._ 1 in this experiment. Our initial results show that SWAAP still induces substantial performance degradation across multiple downstream tasks (see Table 11), despite the mismatch between the surrogate and victim models. 

33 

