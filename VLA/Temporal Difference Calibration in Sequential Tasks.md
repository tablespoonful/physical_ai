---
title: "Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models"
date: "2026-04-22"
authors: "Shelly Francis-Meretzki; Mirco Mutti; Yaniv Romano; Aviv Tamar"
venue: "ICML 2026"
url: https://arxiv.org/abs/2604.20472
pdf: https://arxiv.org/pdf/2604.20472
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.20472)** / [論文ページ](https://arxiv.org/abs/2604.20472)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

**Shelly Francis-Meretzki**<sup>* 1</sup> **Mirco Mutti**<sup>1</sup> **Yaniv Romano**<sup>1</sup> **Aviv Tamar**<sup>1</sup> 

https://shellytechnion.github.io/TDQC.github.io 

## **Abstract** 

Recent advances in vision-language-action (VLA) models for robotics have highlighted the importance of reliable uncertainty quantification in sequential tasks. However, assessing and improving calibration in such settings remains mostly unexplored, especially when only partial trajectories are observed. In this work, we formulate _sequential calibration_ for episodic tasks, where tasksuccess confidence is produced along an episode, while success is determined at the end of it. We introduce a sequential extension of the Brier score and show that, for binary outcomes, its risk minimizer coincides with the VLA policy’s value function. This connection bridges uncertainty calibration and reinforcement learning, enabling the use of temporal-difference (TD) value estimation as a principled calibration mechanism over time. We empirically show that TD calibration improves performance relative to the state-of-the-art on simulated and real-robot data. Interestingly, we show that when calibrated using TD, the VLA’s singlestep action probabilities can yield competitive uncertainty estimates, in contrast to recent findings that employed different calibration techniques. 

## **1. Introduction** 

Modern neural network based AI systems are typically “black box”, raising concern in applications that require safety and reliability – where a system must not only be accurate but also _correctly assess when it is likely to fail_ . 

While neural networks often provide a confidence together with their prediction, there is no built-in machinery to enforce that the confidence actually matches the probability of 

> 1Technion - Israel Institute of Technology. Correspondence to: Shelly Francis-Meretzki _<_ shellyfra@campus.technion.ac.il _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

being correct. In this context, _calibration_ explicitly requires that a model’s confidence aligns with the empirical outcome frequencies (Guo et al., 2017; Brier, 1950; Xiong et al., 2023; Jiang et al., 2021). When a model is well calibrated, high confidence predictions are correct most of the time, and low confidence predictions correspond to a higher chance of error. This is a desirable property as it enables downstream safety mechanisms that depend on the model’s confidence. 

Although calibration has been broadly studied, most of the research focuses on single-step decision problems, such as classification and regression (Popordanoska et al., 2024; Dheur & Ben Taieb, 2023). In these problems, the evaluation of the model’s error is direct: Each input is paired with a ground truth label, so that calibration can compare the model’s confidence to the empirical frequency of successes. However, neural networks are commonly used in sequential decision problems as well, for example, in reinforcement and imitation learning (Black et al., 2024; Guo et al., 2025). In sequential tasks, it is not obvious how to define success for individual steps. Think of a robot performing a manipulation task, which requires a sequence of inter-dependent “correct” actions to be solved, and success is only assessable at the end of the sequence. This raises a question: 

_How to reason about calibration in sequential tasks?_ 

Differently from previous settings, (i) the ground-truth label is typically delayed; and (ii) the confidence in the current decision may depend on the confidence of future and past decisions. 

In this paper, we provide a formal framework for sequential calibration that encompasses (i, ii). We cast the calibration problem as learning a predictor that takes as input the model’s confidence over time to minimize a sequential version of the Brier score (Brier, 1950). The Brier score is a popular loss that captures _both the accuracy and calibration_ of a predictor by computing the mean squared error between the prediction and the outcome frequency. 

Our insight shows that, when formulating a sequential task as a partially-observable Markov decision process, we can connect the problem of minimizing the sequential version of 

1 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_Figure 1._ **Sequential Brier scores across benchmarks.** Sequential Brier score ( _↓_ ) on an _unseen_ validation set averaged over 21 random seeds (train/validation task splits). To compare calibration across rollouts with different lengths, we report Brier score over _time quantiles_ . Each subplot corresponds to a (VLA model, benchmark) pair. Success prediction methods are based on sequences of features or action probabilities. Across all settings, our TD-based methods consistently outperform predictors trained with binary cross entropy (BCE). For _π_ 0 action probabilities are not directly interpretable, hence probability-based TDQC variants are not reported. The dotted line represents the Brier score of a constant predictor that consistently outputs the empirical mean success rate computed on seen tasks (see Remark 4.2). 

Brier score to learning a value function, a popular predictor of task success in Reinforcement Learning (RL, Mannor et al., 2026). This fundamental link allows us to bridge algorithmic insights from RL to sequential calibration, such as the ubiquitous Temporal-Difference (TD) loss (Sutton & Barto, 2018; Mnih et al., 2013; Haarnoja et al., 2018), which bootstraps future value predictions to previous steps, resulting in a superior bias-variance tradeoff (Kearns & Singh, 2000). This provides the backbone for our **T** emporal- **D** ifference **Q** -based **C** alibration (TDQC) method. 

To showcase the potential of sequential calibration, we turn our attention to Vision-Language-Action (VLA) models. VLAs are powerful architectures that have risen to the stateof-the-art for learning robot policies (Black et al., 2024). VLAs encode decision policies that map visual observations and language instructions to probabilities over control actions. Recent works have targeted calibration of those action probabilities to the long-term task success probabilities (Zollo & Zemel, 2025). In particular, Gu et al. (2025) propose _SAFE_ , a method to learn a failure detector that takes as input the hidden state of the VLA and minimizes the cross entropy between the prediction and long-term task success, achieving state-of-the-art failure detection for VLAs. Our paper further advances the research in crucial areas: 

- We provide the first formulation for calibration in sequential tasks, unifying recent works on failure detection in VLAs (Zollo & Zemel, 2025; Gu et al., 2025) with the broad calibration literature into a coherent framework that singles out the challenges of the sequential setting; 

- We fundamentally link sequential calibration to value prediction in RL, drawing inspiration from the latter to 

derive a novel TD method for calibration (TDQC); 

- We empirically show that TDQC, accessing only action probabilities, matches or improves the calibration performance of SAFE accessing the hidden state of the policy in challenging sequential tasks (see Fig. 1 top). This is essential to measure calibration of black-box models, for which the hidden state is often not accessible from APIs; 

- We show that the TDQC loss, either applied to SAFE or to action probabilities, is an essential ingredient to achieve state-of-the-art early detection results in LIBERO for OpenVLA (Kim et al., 2024), _π_ 0 (Black et al., 2024), _π_ 0-FAST (Pertsch et al., 2025) and UniVLA (Wang et al., 2025) models and in a Franka real-robot dataset collected with _π_ 0-FAST (see Table 2). 

- Finally, as a by-product of the TDQC method, we show that the value predictor can improve the baseline’s policy success rates by using it to guide the action selection within a set of actions sampled from the policy. In our experiments, this simple recipe yields a 15% increase of the success rate for OpenVLA on LIBERO-10 (see Fig.4). 

## **2. Background** 

### **2.1. Calibration and Accuracy of Predictors** 

The accuracy of a prediction model is its frequency of making correct predictions. Calibration measures how well a model’s predicted confidence aligns with empirical outcome frequencies. We formally discuss these concepts in the context of binary classification. 

**Definition 1** (Binary Classification) **.** Let ( _X, Y_ ) be a pair of random variables where _X ∈X_ denotes an input, _Y ∈ {_ 0 _,_ 1 _}_ is a binary label, and P( _X, Y_ ) is their joint distribu- 

2 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

tion. A probabilistic classifier is a function _f_ : _X →_ [0 _,_ 1]. For input _x_ , the model prediction _f_ ( _x_ ) is interpreted as the probability that the label is 1. 

Typically, _f_ is calculated from an i.i.d. dataset _D_ = _∼ {_ ( _xi, yi_ ) _}_<sup>_N_</sup> _i_ =1 _P_<sup>_N_</sup> , where ( _xi, yi_ ) are drawn from P( _X, Y_ ). The Brier score (Brier, 1950) is a strictly proper scoring rule that measures the accuracy of a predictor. **Definition 2** (Brier Score for Binary Classifier) **.** The Brier score is the mean squared _ℓ_ 2 distance between = the prediction and the ground-truth label BS( _f_ ) E _X,Y ._ Given a dataset _D_ , it can be esti�( _f_ ( _X_ ) _− Y_ )<sup>2�</sup> mated as BS(<sup>�</sup> _f_ ) = _N_<sup><u>1</u></sup> � _Ni_ =1<sup>(</sup><sup>_f_(</sup><sup>_xi_)</sup><sup>_−yi_)2</sup><sup>_._</sup> 

The Brier score relates to the calibration and accuracy of the classifier by its two-component decomposition. Let _F_ = _f_ ( _X_ ) denote the random event that the model predicts a particular value, and let _η_ ( _F_ ) = P( _Y_ = 1 _| F_ ) _,_ the success probability conditioned on the prediction. The Brier score can be decomposed<sup>1</sup> as 


The first term relates to _calibration_ : the discrepancy between the predicted success probabilities and the true conditional event frequencies. A classifier is perfectly calibrated if _F_ = _η_ ( _F_ ). In practice, calibration is estimated by binning predictions into intervals _{Bk}_<sup>_K_</sup> _k_ =1<sup>and comparing predicted</sup> confidence with empirical frequencies. Let _f_<sup>¯</sup> _k_ be the mean prediction in bin _k_ , _y_ ¯ _k_ the empirical positive rate, and _nk_ the bin size. Then the empirical calibration error takes the form _N_<sup><u>1</u></sup> � _Kk_ =1<sup>_nk_( ¯</sup><sup>_fk −y_¯</sup><sup>_k_)2</sup><sup>_,_which is a binned estimator of</sup> E[( _F − η_ ( _F_ ))<sup>2</sup> ]. The commonly used Expected Calibration Error (ECE) replaces the squared deviation by absolute deviation, ECE( _f_ ) =<sup>�</sup><sup>_K_</sup> _k_ =1 _<u>nNk</u>_<sup>_|f_¯</sup><sup>_k−y_¯</sup><sup>_k|._It is important</sup> to note that calibration does not relate to the accuracy of the predictor. For example, a model that outputs _f_ = E[ _Y_ ] independently of _X_ is perfectly calibrated. 

The second term in the Brier score decomposition (1) relates to accuracy: it measures how informative the score is about the label. This term is small when predictions induce groups with nearly deterministic outcomes ( _η_ ( _F_ ) _≈_ 0 or 1), and large when outcomes remain ambiguous ( _η_ ( _F_ ) _≈_ 1 _/_ 2). In practice, accuracy is typically measured by the ROC AUC. 

_Calibration_ of a classifier refers to the process of taking a trained classifier _f_ and an i.i.d. calibration dataset _D_ cal = _{_ ( _xi, yi_ ) _}_<sup>_N_</sup> _i_ =1<sup>_c∼PNc_andcomputingaclassifier</sup> _f_<sup>_′_</sup> that is better calibrated. For neural network classifiers, _f_ ( _x_ ) = _σ_ ( _logit_ ( _x_ )), where _logit_ ( _x_ ) is the output of the 

> 1This decomposition is based on Murphy (1973). A selfcontained proof is given in Apx. C. 

neural network and _σ_ is a sigmoid function. An effective calibration method is temperature scaling (Guo et al., 2017), yielding _f_<sup>_′_</sup> ( _x_ ) = _σ_ ( _a · logit_ ( _x_ ) + _b_ ), where _a, b_ are calculated by maximizing likelihood on _D_ cal. 

### **2.2. POMDPs** 

A Partially Observable Markov Decision Process (POMDP, Astr˚ om¨ , 1965) is a popular framework for sequential decision making. It is defined by a tuple ( _S, X , A, P, O, R, T_ ) where _S_ is a space of states, _X_ is a space of observations, _A_ is a space of actions, _P_ : _S ×A →_ ∆<sup>_S_</sup> is a transition model, _O_ : _S →_ ∆<sup>_X_</sup> is an observation model, _R_ : _S × A →_ R+ is a reward model, and _T ∈_ N is a time horizon. 

At each step _t < T_ , the POMDP is in a state _st ∈S_ . The agent observes _xt ∼O_ ( _st_ ) and takes an action _at ∈A_ . The process transitions to _st_ +1 _∼P_ ( _st, at_ ) and the agent collects a reward _rt ∼R_ ( _st, at_ ). The process ends in state _sT_ . We denote _hT_ := ( _x_ 1 _, a_ 1 _, r_ 1 _, . . . , xT_ ) _∈H_ the _trajectory_ of the process and by _ht_ its prefix of _t < T_ steps.<sup>2</sup> 

The agent selects actions according to a policy _π_ : _H →_ ∆<sup>_A_</sup> with the goal of maximizing the expected cumulative future rewards. The latter is defined through a _value function_ 


## **3. Related Work** 

**Calibration in Sequential Settings.** In online forecasting, calibration is defined over sequential rounds and analyzed under minimal or adversarial assumptions on the datagenerating process (Qiao & Zheng, 2024). Our setting considers predictions along a single episodic trajectory with delayed terminal feedback. In _temporal calibration_ (Leathart & Polaczuk, 2020), predictions at different time steps are treated independently, applying post-hoc calibration procedures across temporal slices. In survival analysis (Haider et al., 2020), time-dependent Brier scores are used to evaluate the _time until a failure event_ , different from our task of success evaluation. In large language models (LLMs), uncertainty estimation and calibration are inherently sequential, and important for detecting hallucinations (Huang et al., 

> 2We denote as _H_ := _{∅, H_ 1 _, . . . HT }_ the power set of the trajectories up to length _T_ , where _Ht_ := ( _X × A ×_ R+)<sup>_t_</sup> . 

3 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

2024; Shorinwa et al., 2025; Ren et al., 2023; Xiong et al., 2023; Bar-Shalom et al., 2025). In contrast, our work concerns decision making in _dynamic environments_ . 

In reinforcement learning (RL, Mannor et al. 2026), predicting terminal success corresponds to value estimation, and temporal difference (TD) methods are standard. To the best of our knowledge, the connection with sequential calibration, through the Brier score, is novel. Concurrently with our work, van der Laan & Kallus (2025) connected value learning to calibration, in the context of offline RL. Our work differs in that we consider calibrating a pretrained policy, show a connection between the Brier score and value learning, and demonstrate empirical results on VLAs. 

**Calibration of VLAs.** VLAs provide generalist robot policies. Recent architectures including RT-2 (Brohan et al., 2022), Octo (Octo Model Team et al., 2024), OpenVLA (Kim et al., 2024), _π_ 0 (Black et al., 2024), and _π_ 0-FAST (Pertsch et al., 2025), map visual observations and textual instructions to low level robot actions, promising zero shot generalization to unseen tasks. However, current VLAs exhibit limited success on tasks _unseen_ during training/fine tuning, with reported success rates ranging between 30% and 60% (Kim et al., 2024; O’Neill et al., 2024; Black et al., 2024), motivating study of failure detection. 

Zollo & Zemel (2025) first studied confidence calibration in VLAs. They proposed recalibrating action-level confidence estimates using post-hoc methods such as Platt scaling and temperature scaling, using episode-level outcome labels. However, their recalibration operates on individual action confidence scores without modeling calibration dynamics across the trajectory. In contrast, we argue that calibration should be considered across time, investigate more expressive recalibration architectures that aggregate information over the rollout, and additionally address VLAs that do not expose action probabilities. 

The most closely related state-of-the-art method is SAFE (Gu et al., 2025), which trains a single cross-task failure detector on internal VLA features and applies conformal prediction (Diquigiovanni et al., 2021) for thresholded decisions. While SAFE does not explicitly target calibration, the method has strong similarities with ours and can be interpreted as an implicit calibration procedure. Nonetheless, we improve upon SAFE by rigorously formulating the sequential calibration problem, proposing a TD calibration method, and showing that our method outperforms SAFE using exactly their features. In addition, while Gu et al. (2025) concluded that VLA action probabilities are insufficient for success prediction, we show that when calibrated using our method, action probabilities yield competitive performance. 

Other existing approaches, which SAFE outperforms, primarily consist of unsupervised out-of-distribution (OOD) 

detection methods (Xu et al., 2025; Sinha et al., 2024; Wong et al., 2022; Majumdar et al., 2025), which can be overly restrictive for generalist policies, and supervised, task-specific failure detectors (Gokmen et al., 2023; Xie et al., 2022; Farid et al., 2022; Ablett et al., 2020). 

## **4. Problem Formulation** 

We are given a POMDP policy _π_ . Our goal is to understand, during the run of the policy, whether it will succeed or fail in its task. While this problem has been studied before in various forms (see Section 3), in the following we formally define it in a POMDP setting. As we shall later see, this formulation will allow us to propose new algorithms. 

We begin by defining a successful outcome. We say that a trajectory _hT_ is successful when the cumulative reward _R_ ( _hT_ ) =<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_rt_surpasses a threshold</sup><sup>_c ∈_[0</sup><sup>_, R_max]:</sup> 


Thus, success depend on the entire trajectory of decisions, which are dependent. Note that for sparse binary rewards _Y_ ( _hT_ ) = _R_ ( _hT_ ). We would like to evaluate success _during_ the run of the policy, and we henceforth define a sequential counterpart to the conventional Brier score (Brier, 1950) defined in Section 2.1. Let _f_ : _Ht →_ [0 _,_ 1] denote a success prediction function given the history _ht_ . 

**Definition 3.** The _sequential Brier score_ of a function _f_ is 


where the expectations are taken over trajectories _hT_ and their prefix _ht_ induced by _π_ . 

The sequential Brier score can be empirically estimated from a dataset of trajectories and success pairs _D_ cal = _{h_<sup>_i_</sup> _T_<sup>_, yi}_</sup> _i_<sup>_N_</sup> =1<sup>,where</sup><sup>_yi_=</sup><sup>_Y_(</sup><sup>_hi_</sup> _T_<sup>)andtrajectories</sup><sup>_hi_</sup> _T_<sup>are</sup> sampled with _π_ , as follows. 


Similarly to the conventional Brier score, the sequential Brier score relates to the calibration and accuracy of the success predictor by its two-component decomposition. Let _Ft_ = _f_ ( _ht_ ) denote the random event that the model predicts a particular value at time _t_ , and let _η_ ( _Ft_ ) = P( _Y_ ( _hT_ ) = 1 _| Ft_ ) _,_ the success probability conditioned on the prediction at time _t_ . The following decomposition holds: 


where the first term is referred to as _sequential calibration_ , and the second is _accuracy_ . Thus, minimizing the sequential 

4 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


Brier score leads to desired success predictors that are both calibrated and accurate. 

Our focus in this work is on finding a success predictor that yields a low Brier score, by computing _f_ from the calibration dataset _D_ cal. Relating to calibration of classifiers (Section 2), we are particularly interested in whether the policy’s action probabilities _π_ ( _h_ 0) _, . . . , π_ ( _ht_ ) could be calibrated to yield satisfactory performance in success prediction. We therefore introduce the following definition. 

**Definition 4.** A success predictor _f_ that depends only on action probabilities, i.e., _f_ ( _ht_ ) = _f_ ( _π_ ( _h_ 0) _, . . . , π_ ( _ht_ )), is termed a _black box success predictor_ . 

Black box success predictors can be employed when only action probabilities are available - a common setting for commercial foundation models. In contrast, we refer to predictors that require internal access to the VLA model, such as feature activations, as _white box_ success predictors. 

In the following, we motivate calibration using the sequential Brier score, and explore edge cases. We begin with understanding the importance of the task success labels _y_<sup>_i_</sup> in the calibration dataset. One may hope that a set of trajectories _h_<sup>_∗_</sup> _T_<sup>=(</sup><sup>_x_0</sup><sup>_, a_</sup> 0<sup>_∗, . . . , xT −_1</sup><sup>_, a∗_</sup> _T −_ 1<sup>),whichcontain</sup> expert actions to states visited by the policy _π_ , are sufficient for sequential calibration. The following example shows that we should not expect this to work well in general. 

**Example 4.1.** Consider an MDP described in Fig.2 with horizon _T_ = 2 and two actions, _a_ and _a_<sup>_′_</sup> . The initial state is _s_ 0, and _R_ ( _s_ 0 _, a_ ) = 0, _R_ ( _s_ 0 _, a_<sup>_′_</sup> ) = 1. At time step _t_ = 1 the state transitions deterministically to _s_ 1, and _R_ ( _s_ 1 _, a_ ) = _R_ ( _s_ 1 _, a_<sup>_′_</sup> ) = 0. The terminal reward is 0. Training data is generated by the following optimal policy _π_<sup>_∗_</sup> ( _s_ 0) = _a_<sup>_′_</sup> w.p. 1, _π_<sup>_∗_</sup> ( _s_ 1) = _a_<sup>_′_</sup> w.p. 0 _._ 5, and assume that the learned policy is _π_ = _π_<sup>_∗_</sup> . For each time step, _π_ minimizes the conventional Brier score for individual action prediction. However, for a threshold _c ≤_ 1 we have that _Y_ ( _hT_ ) = 1 for all trajectories, while _π_ ( _s_ 1) = 0 _._ 5. 

As Example 4.1 shows, in a sequential task some actions may be _uncorrelated_ with task success, making action probabilities alone-even if coming from an optimal policyirrelevant as success predictors. To connect this example to a practical VLA setting, when the robot is moving without grasping anything, the gripper action is irrelevant for task success; if a policy is trained to imitate experts that randomly open and close the gripper, it may exhibit high uncertainty for irrelevant actions. Calibrating to task success data is therefore important. 

We next discuss the worst sequential Brier score that we can expect in practice. Given some partial trajectory _ht_ , we = E<sup>_π_</sup> [ _Y_ ( _hT_ ) _| ht_ ]. have that min _f_ E<sup>_π_�</sup> ( _f − Y_ ( _hT_ ))<sup>2��</sup> � _ht_ � **Remark 4.2.** Let E<sup>_π_</sup> [ _Y_ ( _hT_ )] denote the average task success rate. Any information that exists in the trajectory may be used to obtain a lower Brier score. 

## **5. Method** 

In this section, we devise a method for sequential calibration. The previous discussion clarifies the relation between sequential calibration and prediction of the task success, through the minimization of the sequential Brier score. The way task success is defined in our setting, i.e., whether the total reward collected during a trajectory surpasses a given threshold (see Eq. 2), essentially implies that we can predict task success by predicting future rewards. The problem of future reward prediction is a staple in the RL literature (Mannor et al., 2026). The following theorem formalizes the connection between the two problems. 

**Theorem 5.1.** _The future rewards predictor f_<sup>ˆ</sup> ( _ht_ ) _that minimizes the Sequential Brier Score_ 


_is given by:_ 

Theorem 5.1 fundamentally links our original problem of calibrating a given policy _π_ with estimating its value function _Q_<sup>_π_</sup> . In other words, _learning the value function is equivalent to learning a calibrated predictor of eventual success_ . Value estimation is a well-studied problem in RL (Mannor et al., 2026) and allows us to add the family of value estimation algorithms to the calibration toolkit. 

In this paper, we consider access to a policy _π_ and a set of _N_ labeled trajectories _D_ cal = _{_ ( _h_<sup>_i_</sup> _T_<sup>_, yi_)</sup> _i_<sup>_N_</sup> =1<sup>_}_generated with the</sup> policy, where the label denotes whether the trajectory was successful. The value estimation algorithm fits a parametric function _fθ_ : _Ht →_ [0 _,_ 1] to the data by minimizing a loss 


In RL, the single-step loss _ℓ_ ( _fθ_ ( _h_<sup>_i_</sup> _t_<sup>)</sup><sup>_, yi_) typically takes two</sup> forms. One is called _Monte Carlo_ (MC), and prescribes to solve a classification or regression problem between _h_<sup>_i_</sup> _t_<sup>and</sup> _y_<sup>_i_</sup> . The other is _Temporal Difference_ (TD), which bootstraps the value between two consecutive steps as 


5 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

### **Algorithm 1** TDQC 

**input** Policy _π_ , calibration dataset _D_ cal = _{_ ( _h_<sup>_i_</sup> _T_<sup>_, yi_)</sup> _i_<sup>_N_</sup> =1<sup>_}_</sup> 

- 1: Initialize network weights _fθ , fθ−_ 

- 2: **for** until convergence **do** 

- 3: Sample _h_<sup>_i_</sup> _T_<sup>uniformly from</sup><sup>_D_cal</sup> 

- 4: Compute the TDQC loss using a target network _T −_ 1 

- _G_ ( _θ_ ) = � ( _fθ_ ( _h_<sup>_i_</sup> _t_<sup>)</sup><sup>_−f_</sup> _θ_<sup>_−_(</sup><sup>_hi_</sup> _t_ +1<sup>))2+(</sup><sup>_fθ_(</sup><sup>_h_</sup> _T_<sup>_i_)</sup><sup>_−yi_)2</sup> _t_ =1 

- 5: Update _θ ← θ − α∇G_ ( _θ_ ) 6: Periodically update target network _θ_<sup>_−_</sup> _← θ_ 7: **end for** 

For training stability of TD loss, we used updates with a target network Mnih et al. (2015). The target network parameters _θ_<sup>_−_</sup> are updated with the current parameters _θ_ every _C_ steps and are held fixed between individual updates. While previous work (Gu et al., 2025) employs an MC loss, TD has not been considered in the context of calibration. TD is the common practice in RL (e.g., Haarnoja et al., 2018) for its well-established practical and theoretical benefits (Kearns & Singh, 2000). In the experiments, we will show that similar benefits extend to the calibration setting. Before that, in Algorithm 1, we provide a brief summary of our method, which we call **T** emporal- **D** ifference **Q** -based **C** alibration, TDQC for short. Then, we comment on how to extract information from the history in practice, e.g., when running VLA policies, and how having a calibrated policy opens the door to failure detection and other applications. 

**Extracting the History.** In principle, the history _ht_ should contain all signals available at time _t_ that are informative about future success, e.g., the current observation, past actions, and any internal state carried by the policy. In practice, we consider two lightweight ways to extract _ht_ from a VLA. 

For _token-based_ VLA architectures, actions are discretized into tokens, and the policy outputs a categorical distribution over tokens at each step. This design is used by RT2 (Zitkovich et al., 2023), OpenVLA (Kim et al., 2024), NORA (Hung et al., 2025) and Uni-VLA (Wang et al., 2025). Since these models resemble LLM-style decoders, we can adopt the common heuristic of using token probabilities and use a _black-box success predictor_ (Def. 4). 

More generally, we can define _ht_ via the policy’s internal representations, such as hidden states from intermediate layers. Using internal features as inputs to an auxiliary predictor is standard in the LLM calibration and _probing_ literature (Azaria & Mitchell, 2023; Zou et al., 2023; Kossen et al., 2024), but requires access to the model’s weights. 

### **5.1. Early Stopping with Conformal Prediction** 

When a policy _π_ is deployed in safety-critical scenarios, we may want to exploit _fθ_ to stop early trajectories that have 

low probability of success, avoiding unnecessary damage to the system and its surroundings in failed attempts. 

To this purpose, we use _fθ_ as a confidence score for future success, which is equivalent to our original definition of predicting future rewards for binary tasks. Then, _fθ_ can be used to trigger early stopping when the predicted probability of success is low. This can be made formal using _conformal prediction_ (CP, Shafer & Vovk, 2008; Jazbec et al., 2024; Ringel et al., 2024). 

Following Gu et al. (2025), we treat 1 _− fθ_ as a failure predictor and raise a failure flag whenever 1 _− fθ > δt_ , where _δt_ is a time-varying upper threshold. To calculate that threshold at each time step we first set a significance level _α ∈_ (0 _,_ 1), which determines how conservative we want to be with the early stopping, and we separate a set of successful trajectories from the data before training, to avoid biasing the procedure. On this validation set, we invoke a _functional_ conformal prediction (CP) routine (see Algorithm 2 in Apx. D and Diquigiovanni et al. 2021 for details) to compute a time-varying confidence upper bound _{δt}_<sup>_T_</sup> _t_ =1<sup>.Finally, while the policy is deployed, we process</sup> the current trajectory _ht_ with _fθ_ and compare the resulting score with _δt_ . Whenever 1 _− fθ_ ( _ht_ ) _> δt_ we stop _π_ . The described procedure is reported in Algorithm 3. Under the exchangeability assumption (Vovk et al., 2005), the CP band guarantees that, for a new _successful_ rollout, 1 _− fθ_ remain below the threshold for all time _t_ w.p 1 _− α_ . 

### **5.2. Application to Test-Time Guided Action Search** 

As an example downstream application of our calibration method, we consider action search at test time. Standard VLA models typically execute the single most probable action predicted by their policy. However, this greedy approach can lead to sub-optimal decisions, especially when attempting to generalize to new environments. 

Related LLM-based approaches combine search with process reward models (PRMs), which calculate the quality or correctness of intermediate reasoning steps (Lightman et al., 2023; Zhang et al., 2025). Analogously, to exploit calibration to this end, we propose to use the learned Q- function _fθ_ to guide action search toward trajectories that are more likely to succeed, inspired by RL methods that employ search at test time (Silver et al., 2016). Furthermore, when _fθ_ indicates a high confidence that the trajectory will succeed, we can save compute resources and skip the search (this is the converse of early stopping, cf. Section 5.1). 

The pseudocode of the procedure is reported in Algorithm 4. Note that we assume access to an accurate forward model of the system dynamics _W_ = _P_ ( _xt_ +1 _|ht, at_ ), which is easily available in simulated domains. For real-world domains, a world model of the dynamics may be learned (Schrittwieser 

6 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

et al., 2020); we leave such investigation for future work. 

At each time step, given a VLA policy _π_ and a simulator _W_ , we sample from the policy _M_ possible action candidates. For each candidate action _i_ , we simulate a onestep look-ahead to observe the resulting next observation _x_<sup>(</sup> _t_ +1<sup>_i_)</sup><sup>_∼W_(</sup><sup>_xt, a_</sup> _t_<sup>(</sup><sup>_i_)) , and subsequently select the next ac-</sup> tion using the standard model’s greedy selection strategy max _a′ π_ ( _xt_ +1 _, a_<sup>_′_</sup> ). We then evaluate each resulting observation using _Q_ = _fθ_ ( _xt_ +1 _, at_ +1) and choose the action with highest score _a_<sup>_∗_</sup> = max _a′ Q_ ( _xt_ +1 _, a_<sup>_′_</sup> ). We emphasize that _fθ_ parameters are frozen and used only for test-time guided search. To reduce test-time compute using the _calibrated_ model, we apply the action search only when the predicted Q value exceeds a threshold _T_<sup>¯</sup> . 

## **6. Experiments** 

In this section, we empirically validate the connection between calibrating a policy _π_ and estimating its value _Q_<sup>_π_</sup> _t_<sup>.</sup> We test TDQC, our _sequentially calibrated_ success predictor in sequential tasks. We aim to answer the following: _(1)_ TD loss improves calibration and failure detection results? _(2)_ Can black-box based calibration yield competitive results? _(3)_ Can a calibrated model be used to improve success rate using test-time guided action search? 

### **6.1. Vision-Language-Action Models** 

We evaluate four state-of-the-art VLA policies: OpenVLA (Kim et al., 2024), UniVLA (Wang et al., 2025), _π_ 0 (Black et al., 2024), and _π_ 0-FAST (Pertsch et al., 2025). These models span different action parameterizations, which directly changes what confidence signals can be extracted from their outputs. OpenVLA discretizes continuous action into tokens and exposes the corresponding token probabilities, which we use as the action probabilities. _π_ 0-FAST and UniVLA also employs a tokenized representation and apply Discrete Cosine Transform (DCT) to convert continuous action sequences into discrete action tokens. Consequently, token probabilities do not match with the per-dimension continuous action and cannot be directly interpreted as such. The _π_ 0 VLA represents continuous action with a flow matching model, rather than per-step token probabilities. All models are open-sourced, enabling access to internal features. 

Following Def. 4, we refer to methods that predict success using only the model’s observable outputs as _black-box_ . For OpenVLA, our black-box approach uses the discrete action probabilities directly. For _π_ 0-FAST and UniVLA, the FAST action tokenizer decodes tokens into discrete actions, each with logits spanning the decoder’s vocabulary size. Our black-box approach takes these logits as input; see Apx. F.3 for more details on the extraction of those probabilities. For all white-box predictors, we use as input the features suggested in SAFE (Gu et al., 2025). 

### **6.2. Benchmarks** 

**LIBERO** (Liu et al., 2023) is a popular simulated benchmark for VLA evaluation. We evaluated OpenVLA, _π_ 0- FAST and _π_ 0 on LIBERO-10 suite, which contains 10 long horizon tasks with diverse objects, layouts, and instructions, and is considered the _most challenging_ suite (Gu et al., 2025; Zollo & Zemel, 2025). Episodes terminate upon task completion or after a timeout (failure). We let _Ti_ denote rollout _i_ ’s stopping time: either the time of task completion, or the timeout duration on failure (see Gu et al. (2025) and Apx. F.4 for more details). 

**Real-World WidowX** We consider the WidowX data and OpenVLA checkpoints published in Gu et al. (2025). The dataset contains 532 rollouts on 8 pick-and-place tasks. _All tasks_ have rollouts with exactly _Ti_ = 50 steps; if the policy succeeds earlier, the robot keeps acting in the environment until reaching _Ti_ (see Gu et al. 2025 and Apx. F.4). 

**Real-World Franka** We consider the Franka Emika Panda Robot in Gu et al. (2025) using _π_ 0-FAST-DROID checkpoints (Pertsch et al., 2025). The dataset contains 13 pick and place tasks, each with 30 successful and 30 failed rollouts. Each _task k_ has the same number of steps _Tk_ , regardless if they failed earlier or not, thus _Ti_ = _Tk_ for each rollout _i_ in task _k_ (see Gu et al. 2025 and Apx. F.4). 

### **6.3. Baselines** 

**Static Predictors.** We compared Max Prob, Avg Prob and Running Avg Prob presented in Zollo & Zemel (2025), Avg Entropy and Running Avg Entropy from Gu et al. (2025). These methods use the raw action probabilities per time step or apply simple, hand-crafted transformations, such as maximum or average over both action dimension and time, on the raw probabilities and on the probabilities’ entropy. More details and formulation appear in the Apx. F.5. 

**Trained Predictors.** We used the baselines from Gu et al. (2025), which provide, to the best of our knowledge, the state-of-the-art failure detection baselines for VLA models. SAFE-MLP uses a small MLP network and takes as input the internal feature vectors (hidden state) _e_ from the model, i.e., _ht_ = _et_ . SAFE-RNN applies a linear projection layer to the input and then an LSTM (Hochreiter & Schmidhuber, 1997). For the evaluation, we followed the same networks and parameters used in Gu et al. (2025) as the _f_ in SAFE methods. Note that both SAFE baselines use hidden states as input, hence are white-box methods. 

Apx. F.6 and Gu et al. (2025) detail how the hidden features are extracted and on the architectures of both models. Here we note that the SAFE= MLP loss aggregates the scores over time _L_ MLP � _i_<sup>[</sup><sup>_yi_</sup> � _t_<sup>(</sup><sup>_t −fθ_(</sup><sup>_et_)) + (1</sup><sup>_−yi_) �</sup> _t_<sup>_fθ_(</sup><sup>_et_)]</sup> which induces a monotone, time-indexed scoring scheme rather than 

7 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

||VLA Model<br>Benchmark|Ope<br>LIB|nVLA<br>ERO|Ope<br>Wi|nVLA<br>dowX|Uni<br>LIB|VLA<br>ERO|_π_0-<br>LIB|FAST<br>ERO|_π_0-<br>Fr|FAST<br>anka|LI|_π_0<br>BERO|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Eval Task Split|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen_↓_|
||Max prob.|0_._395|0_._390|0_._572|0_._579|0_._909|0_._899|0_._320|0_._318|0_._331|0_._323|_−_|_−_|
||Avg prob.|0_._348|0_._364|0_._275|0_._282|0_._529|0_._532|0_._212|0_._218|0_._290|0_._294|_−_|_−_|
|Static Predictors|Running Avg prob.|0_._338|0_._356|0_._255|0_._257|0_._543|0_._544|0_._244|0_._238|0_._359|0_._361|_−_|_−_|
||Avg entropy|0_._306|0_._313|0_._414|0_._426|0_._406|0_._391|0_._209|0_._222|0_._281|0_._281|_−_|_−_|
||RunningAvgentropy|0_._265|0_._273|0_._435|0_._432|0_._343|0_._330|0_._279|0_._264|0_._341|0_._339|_−_|_−_|
||_SAFE-RNN_|0_._204|0_._255|0_._169|0_._213|0_._124|0_._162|0_._106|0_._148|0_._220|0_._288|0_._123|0_._172|
|Ld Pdit hit b|_SAFE-RNN-TDQC (Ours)_|0_._197|0_._218|**0**_._**096**|**0**_._**153**|**0**_._**064**|**0**_._**100**|**0**_._**103**|0_._163|**0**_._**150**|**0**_._**215**|**0**_._**061**|**0**_._**097**|
|earne recors (we ox)|_SAFE-MLP BCE_|0_._192|0_._231|0_._127|0_._164|0_._091|0_._158|**0**_._**103**|0_._162|0_._206|0_._248|0_._075|0_._137|
||_SAFE-MLP-TDQC (Ours)_|0_._195|0_._229|0_._130|0_._169|0_._066|0_._131|0_._109|0_._150|0_._210|0_._229|0_._068|0_._128|
|Ld dit (blk b)|_RNN-BCE_|0_._199|0_._206|0_._301|0_._344|0_._138|0_._152|0_._122|0_._158|0_._237|0_._243|_−_|_−_|
|earne precors ac ox|_RNN-TDQC (Ours)_|**0**_._**191**|**0**_._**197**|0_._156|0_._192|0_._100|0_._107|0_._105|**0**_._**141**|0_._204|0_._228|_−_|_−_|


_Table 1._ Brier Score results on simulation and real robot experiment. Results are averaged over 21 seeds which determine different train-test splits of the tasks. ” _−_ ” indicates that the Brier score can’t be calculated on the method. The **best** performing methods are highlighted in the table. Our method, TDQC achieves lowest sequential Brier scores in all benchmarks. 

||VLA Model<br>Benchmark|Ope<br>LIB|nVLA<br>ERO|Ope<br>Wid|nVLA<br>owX|Uni<br>LIB|VLA<br>ERO|_π_0-<br>LIB|FAST<br>ERO|_π_0-<br>Fr|FAST<br>anka|LIB|_π_0<br>ERO|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Eval Task Split|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen_↑_|
||Max prob.|54_._64|55_._78|53_._25|53_._20|50_._00|50_._00|61_._75|63_._49|48_._61|46_._64|_−_|_−_|
||Avg prob.|47_._08|48_._09|47_._47|48_._30|42_._96|40_._25|47_._36|48_._09|49_._45|48_._03|_−_|_−_|
|Static Predictors|Running Avg prob.|49_._19|47_._72|49_._20|46_._37|43_._05|40_._29|53_._95|55_._68|52_._95|49_._98|_−_|_−_|
||Avg entropy|46_._81|46_._75|50_._19|49_._36|41_._34|47_._36|45_._42|46_._30|49_._28|49_._07|_−_|_−_|
||RunningAvgentropy|50_._48|48_._09|46_._16|43_._99|51_._63|56_._71|53_._78|55_._44|51_._12|48_._78|_−_|_−_|
||_SAFE-RNN_|72_._30|69_._04|75_._95|70_._00|74_._48|68_._13|91_._26|**85**_._**88**|70_._85|56_._69|79_._96|65_._03|
||_SAFE-RNN-TDQC (Ours)_|71_._67|65_._12|84_._01|70_._76|73_._83|64_._25|**92**_._**03**|85_._49|**79**_._**89**|**68**_._**43**|88_._66|**82**_._**94**|
|Learned Predictors (white-box)|_SAFE-MLP_|73_._56|69_._53|**88**_._**23**|**83**_._**18**|74_._39|63_._80|79_._00|68_._36|79_._15|63_._94|86_._33|79_._75|
||_SAFE-MLP-BCE_|72_._66|64_._99|85_._38|71_._43|**78**_._**83**|69_._74|91_._82|85_._50|73_._82|58_._83|**89**_._**71**|80_._53|
||_SAFE-MLP-TDQC (Ours)_|71_._22|60_._09|82_._33|70_._64|76_._55|66_._71|90_._25|84_._44|61_._95|51_._22|86_._57|72_._07|
|Ld dit (blk b)|_RNN-BCE_|72_._70|72_._28|69_._69|67_._09|63_._44|54_._37|87_._67|82_._53|59_._32|53_._26|_−_|_−_|
|earne precors ac ox|_RNN-TDQC (Ours)_|**74**_._**20**|**72**_._**72**|78_._90|72_._97|72_._30|**70**_._**17**|87_._51|83_._39|64_._19|57_._37|_−_|_−_|


_Table 2._ ROC-AUC results on simulation and real robot experiment. Results are averaged over 21 seeds which determine different train-test splits of the tasks. ” _−_ ” indicates that the ROC-AUC can’t be calculated on the method. The **best** performing methods are highlighted in the table. Our method, TDQC achieves SOTA results on unseen tasks in 4 benchmarks out of 6. 

a calibrated probability. Its uncertainty estimation at each time step is between _f_ ( _ht−_ 1) _≤ f_ ( _ht_ ) _≤ t_ and cannot be treated as a probability. Post-hoc normalization would be arbitrary and distort comparisons. Therefore, we keep the same MLP architecture but replaced the loss with a standard binary cross-entropy objective, yielding SAFE-MLP BCE. 

We compared our method TDQC in two settings: (1) We use black-box success predictor (Def. 4) for OpenVLA, UniVLA and _π_ 0-FAST as described in Section 6.1 combined with TDQC loss (Alg. 1). (2) We incorporate our TDQC loss (Alg. 1) on SAFE baselines where _ht_ is the policy’s internal features at time step _t_ . Note that both settings are alternative ways for approximating _Q_<sup>_π_</sup> _t_<sup>.</sup> 

### **6.4. TD loss improves calibration and failure detection** 

**Calibration.** To test the VLA policies’ calibration, we measure the _sequential Brier score_ (Definition 3), which measures calibration and accuracy as shown in Eq. 5. Each rollout _i_ has a horizon _Ti_ , and produces an episode-level binary success label _Y_ ( _h_<sup>_i_</sup> _T_<sup>).To compare calibration across</sup> rollouts with different lengths, we report sequential Brier score in different _quantiles q ∈_ [0 _,_ 1], where _q_ = _t/Ti_ denotes a normalized time within rollout _i_ . 

Table 1 shows that across models and benchmarks, _TDQC improves calibration relative to non-TDQC variants_ , where SAFE-RNN-TDQC performs the best or on par for all _π_ 0 model variants. Moreover, Fig 1 reports sequential Brier scores at different time quantiles within an episode. Early 

in the rollout, when limited task information is available, TD-based predictors perform comparably to binary crossentropy baselines. As time advances, sequential Brier scores decrease for all methods, reflecting that explicitly modeling the temporal structure yields more accurate success probability estimates than step-wise or purely supervised training. 

The dotted horizontal line in Figure 1 represents the Brier score of a constant predictor that, instead of using the model’s task-specific success estimates, consistently outputs the empirical mean success rate computed over the seen tasks, as described in Section 4.2. Consequently, it constitutes an uninformative baseline. We observe that several BCE-based approaches yield little to no improvement relative to this baseline, whereas most TDQC-based approaches attain progressively lower Brier scores, indicating superior calibration and more informative predictive distributions. 

**Failure Detection.** We evaluate failure detection using ROC-AUC, which measures how well a score ranks failed rollouts above successful ones and is widely used for uncertainty quantification in LLMs (Huang et al., 2023; Farquhar et al., 2024; Xia et al., 2025). A failure is flagged once the CP threshold is exceeded. For each task, we compute the minimum rollout length and evaluate ROC-AUC using the maximum prediction up to this timestep. 

Table 2 shows that predictors with TDQC loss perform better or on par with the best baselines for both white-box and black-box predictors. Based on Table 1 and Table 2, we conclude that _TDQC sets the state-of-the-art on unseen_ 

8 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_Figure 3._ **ROC-AUC vs Brier score** over all learned baselines in all benchmarks at the minimum rollout length. Points are grouped by method and split, with a dashed linear fit; the Spearman correlation is _ρ_ = _−_ 0 _._ 686 which indicates high negative correlation. 

_tasks on OpenVLA LIBERO, π_ 0 _LIBERO, UniVLA LIBERO and real robot π_ 0 _-FAST Franka_ . 

Finally, since ROC-AUC and sequential Brier are related, we observe in Fig. 3 a consistent empirical trend. Methods with lower sequential Brier score tend to achieve higher ROCAUC, suggesting that better calibrated success probabilities are useful for failure detection. The Spearman correlation of _−_ 0 _._ 686 highlights the strong connection between the two measures. Apx. G.10 examines per-VLA results: all display high correlation, with some VLAs showing stronger correlation, indicating more informative internal representations. 

### **6.5. Black-box calibration yield competitive results** 

To evaluate calibration of action or token probabilities we measured the Brier score for learned black-box methods and static methods. Table 1 shows that black-box predictors achieve best or competitive results on all LIBERO benchmarks, when trained using TDQC. Further, TDQC significantly improves performance of black-box predictors across all benchmarks. In comparison, static baselines, which also use action probabilities as input but are not calibrated by learning from trajectory success labels, display significantly worse performance. These results suggest that the right calibration technique (here, TDQC) can extract useful signal even in a black-box setting. 

### **6.6. Application to guided test-time action search** 

To evaluate the guided test-time search application described in Section 5.2, We measured OpenVLA’s success rates on three held-out LIBERO-10 tasks, with 50 rollouts per task. We compared the unmodified OpenVLA policy (Baseline) against several value guided search configurations, using Alg. 4. In Fig. 4 we show the success rate relative to the increase in test time compute. _RNN with TDQC or BCE_ action selection methods uses the output of the _fθ_ network for the guidance _at all time steps_ (that is, the threshold in 


_Figure 4._ **Averaged success rates over test time compute for action selection configurations** . All experiments evaluate 3 unseen tasks from LIBERO-10 taken with OpenVLA, averaged over 3 seeds. RNN-TDQC achieves highest success rates, while RNNTDQC with thresholds tradeoff success rate and compute. 

Algorithm 4 is _T_<sup>¯</sup> = _−∞_ ). _TDQC - Thresh_ method saves compute by applying a confidence threshold, as described in Alg. 4. In this experiment we used a threshold _T_<sup>¯</sup> = 0 _._ 35, which achieved a good tradeoff between success rate and compute. To increase variance in sampled actions, we generated 10 samples per timestep in all value guided methods using a sampling temperature of 1 _._ 5. 

Fig 4 shows that RNN methods with top-10 probabilities gain significant improvements and outperform the baseline VLA policy, validating the use of the learned scoring function ( _fθ_ ) for action selection. Notably, the RNN method trained with TDQC achieves the highest overall performance, reaching 55% success rate on average, an improvement of 13% over the regular baseline. While the BCE loss variant also improves upon the baseline, it peaks lower at 50%. Moreover, applying a threshold to the TDQC method (TDQC, Thresh 0 _._ 35) results in a slight performance drop compared to the unconstrained TDQC approach, but saves almost half of the additional compute. Interestingly, we observe a near-linear relation between additional compute and success rate (the gray line in Figure 4 is a fit on all RNN top-10 methods). Additional details are in Apx. G.3. 

## **7. Conclusion and Future Works** 

In this paper, we proposed a novel formulation for calibration in sequential tasks. We showed that predictors calibrated using our temporal-difference based approach achieve SOTA performance in several VLA benchmarks. Importantly, our approach can work with only action probabilities, which is essential for calibration of _black-box_ proprietary models accessed via APIs. 

We see potential in using calibrated success predictors for action search at test time, in particular, allocating search effort only to “difficult” decisions, can be a promising direction for resource management. 

9 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

## **Acknowledgments** 

We thank Qiao Gu for helpful conversations and for releasing his code and data for SAFE. This research was funded by the European Union (ERC, Bayes-RL, 101041250). Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council Executive Agency (ERCEA). Neither the European Union nor the granting authority can be held responsible for them. Y. R. was supported by the Israel Science Foundation (ISF grant 729/21). He also acknowledges the additional support from the Career Advancement Fellowship at the Technion. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

## **References** 

- Ablett, T., Maric,´ F., and Kelly, J. Fighting failures with fire: Failure identification to reduce expert burden in intervention-based learning. _arXiv preprint arXiv:2007.00245_ , 2020. 

- Astr˚ om, K. J.¨ Optimal control of Markov processes with incomplete state information. _Journal of Mathematical Analysis and Applications_ , 10(1):174–205, 1965. 

- Azaria, A. and Mitchell, T. The internal state of an LLM knows when it’s lying. In _Conference on Empirical Methods in Natural Language Processing_ , 2023. 

- Badithela, A., Snyder, D., Zha, L., Mikhail, J., O’Kelly, M., Dixit, A., and Majumdar, A. Reliable and scalable robot policy evaluation with imperfect simulators. _arXiv preprint arXiv:2510.04354_ , 2025. 

- Bar-Shalom, G., Frasca, F., Lim, D., Gelberg, Y., Ziser, Y., El-Yaniv, R., Chechik, G., and Maron, H. Beyond next token probabilities: Learnable, fast detection of hallucinations and data contamination on llm output distributions, 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _pi_ ~~0~~ : A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brier, G. W. Verification of forecasts expressed in terms of probability. _Monthly Weather Review, 78(1):1–3, 1950_ , 1950. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Dheur, V. and Ben Taieb, S. A large-scale study of probabilistic calibration in neural network regression. In _International Conference on Machine Learning_ , 2023. 

- Diquigiovanni, J., Fontana, M., and Vantini, S. The importance of being a band: Finite-sample exact distributionfree prediction sets for functional data. _arXiv preprint arXiv:2102.06746_ , 2021. 

- Farebrother, J., Orbay, J., Vuong, Q., Taiga, A. A., Chebotar, Y., Xiao, T., Irpan, A., Levine, S., Castro, P. S., Faust, A., et al. Stop regressing: Training value functions via classification for scalable deep rl. In _International Conference on Machine Learning_ , 2024. 

- Farid, A., Snyder, D., Ren, A. Z., and Majumdar, A. Failure prediction with statistical guarantees for vision-based robot control. In _Robotics: Science and Systems_ , 2022. 

- Farquhar, S., Kossen, J., Kuhn, L., and Gal, Y. Detecting hallucinations in large language models using semantic entropy. _Nature_ , 630(8017):625–630, 2024. 

- Gemini Robotics Team, Choromanski, K., Devin, C., Du, Y., Dwibedi, D., Gao, R., Jindal, A., Kipf, T., Kirmani, S., Leal, I., et al. Evaluating gemini robotics policies in a veo world simulator. _arXiv preprint arXiv:2512.10675_ , 2026. 

- Gokmen, C., Ho, D., and Khansari, M. Asking for help: Failure prediction in behavioral cloning through value approximation. In _International Conference on Robotics and Automation_ , 2023. 

- Gu, Q., Ju, Y., Sun, S., Gilitschenski, I., Nishimura, H., Itkina, M., and Shkurti, F. Safe: Multitask failure detection for vision-language-action models. _Advances in Neural Information Processing Systems_ , 2025. 

- Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. On calibration of modern neural networks. In _International Conference on Machine Learning_ , 2017. 

- Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- Haarnoja, T., Zhou, A., Abbeel, P., and Levine, S. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International Conference on Machine Learning_ , 2018. 

10 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

- Haider, H., Hoehn, B., Davis, S., and Greiner, R. Effective ways to build and evaluate individual survival distributions. _Journal of Machine Learning Research_ , 21(85): 1–63, 2020. 

- Hochreiter, S. and Schmidhuber, J. Long short-term memory. _Neural computation_ , 9(8):1735–1780, 1997. 

- Huang, X., Li, S., Yu, M., Sesia, M., Hassani, H., Lee, I., Bastani, O., and Dobriban, E. Uncertainty in language models: Assessment through rank-calibration. In _Conference on Empirical Methods in Natural Language Processing_ , 2024. 

- Huang, Y., Song, J., Wang, Z., Zhao, S., Chen, H., JuefeiXu, F., and Ma, L. Look before you leap: An exploratory study of uncertainty measurement for large language models. _arXiv preprint arXiv:2307.10236_ , 2023. 

- Hung, C.-Y., Sun, Q., Hong, P., Zadeh, A., Li, C., Tan, U., Majumder, N., Poria, S., et al. Nora: A small opensourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ , 2025. 

- Jazbec, M., Timans, A., Veljkovic,´ T. H., Sakmann, K., Zhang, D., Naesseth, C. A., and Nalisnick, E. Fast yet safe: Early-exiting with risk control. _Advances in Neural Information Processing Systems_ , 2024. 

- Jiang, Z., Araki, J., Ding, H., and Neubig, G. How can we know when language models know? on the calibration of language models for question answering. _Transactions of the Association for Computational Linguistics_ , 9:962– 977, 2021. 

- Kearns, M. J. and Singh, S. Bias-variance error bounds for temporal difference updates. In _Conference on Learning Theory_ , 2000. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. In _Conference on Robot Learning_ , 2024. 

- Kossen, J., Han, J., Razzak, M., Schut, L., Malik, S., and Gal, Y. Semantic entropy probes: Robust and cheap hallucination detection in llms. _arXiv preprint arXiv:2406.15927_ , 2024. 

- Leathart, T. and Polaczuk, M. Temporal probability calibration. _arXiv preprint arXiv:2002.02644_ , 2020. 

- Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and Cobbe, K. Let’s verify step by step. In _International Conference on Learning Representations_ , 2023. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 2023. 

- Loshchilov, I. and Hutter, F. Decoupled weight decay regularization. In _International Conference on Learning Representations_ , 2017. 

- Majumdar, A., Sharma, M., Kalashnikov, D., Singh, S., Sermanet, P., and Sindhwani, V. Predictive red teaming: Breaking policies without breaking robots. In _Conference on Robot Learning_ , 2025. 

- Mannor, S., Mansour, Y., and Tamar, A. _Reinforcement Learning: Foundations_ . Cambridge University Press, 2026. URL https://sites.google.com/view/ rlfoundations/home. 

- Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D., and Riedmiller, M. Playing atari with deep reinforcement learning. _arXiv preprint arXiv:1312.5602_ , 2013. 

- Mnih, V., Kavukcuoglu, K., Silver, D., Rusu, A. A., Veness, J., Bellemare, M. G., Graves, A., Riedmiller, M., Fidjeland, A. K., Ostrovski, G., et al. Human-level control through deep reinforcement learning. _nature_ , 518(7540): 529–533, 2015. 

- Murphy, A. H. A new vector partition of the probability score. _Journal of Applied Meteorology and Climatology_ , 12(4):595–600, 1973. 

- Octo Model Team, Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Orgad, H., Toker, M., Gekhman, Z., Reichart, R., Szpektor, I., Kotek, H., and Belinkov, Y. Llms know more than they show: On the intrinsic representation of llm hallucinations. In _International Conference on Learning Representations_ , 2025. 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _International Conference on Robotics and Automation_ , 2024. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

11 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

- Popordanoska, T., Tiulpin, A., and Blaschko, M. B. Beyond classification: Definition and density-based estimation of calibration in object detection. In _WACV_ , 2024. 

- Qiao, M. and Zheng, L. On the distance from calibration in sequential prediction. In _Conference on Learning Theory_ , 2024. 

- Radharapu, B., Saxena, E., Li, K., Whitehouse, C., Williams, A., and Cancedda, N. Calibrating llm judges: Linear probes for fast and reliable uncertainty estimation. _arXiv preprint arXiv:2512.22245_ , 2025. 

- Ren, A. Z., Dixit, A., Bodrova, A., Singh, S., Tu, S., Brown, N., Xu, P., Takayama, L., Xia, F., Varley, J., et al. Robots that ask for help: Uncertainty alignment for large language model planners. In _Conference on Robot Learning_ , 2023. 

- Ringel, L., Cohen, R., Freedman, D., Elad, M., and Romano, Y. Early time classification with accumulated accuracy gap control. In _International Conference on Machine Learning_ . PMLR, 2024. 

- Schrittwieser, J., Antonoglou, I., Hubert, T., Simonyan, K., Sifre, L., Schmitt, S., Guez, A., Lockhart, E., Hassabis, D., Graepel, T., et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839): 604–609, 2020. 

- Shafer, G. and Vovk, V. A tutorial on conformal prediction. _Journal of Machine Learning Research_ , 9(3), 2008. 

- Shorinwa, O., Mei, Z., Lidard, J., Ren, A. Z., and Majumdar, A. A survey on uncertainty quantification of large language models: Taxonomy, open research challenges, and future directions. _ACM Computing Surveys_ , 2025. 

- Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L., Van Den Driessche, G., Schrittwieser, J., Antonoglou, I., Panneershelvam, V., Lanctot, M., et al. Mastering the game of go with deep neural networks and tree search. _Nature_ , 529(7587):484–489, 2016. 

- Sinha, R., Elhafsi, A., Agia, C., Foutter, M., Schmerling, E., and Pavone, M. Real-time anomaly detection and reactive planning with large language models. _arXiv preprint arXiv:2407.08735_ , 2024. 

- Sutton, R. S. and Barto, A. G. Reinforcement learning: An introduction. _MIT press_ , 2018. 

   - Wang, Y., Li, X., Wang, W., Zhang, J., Li, Y., Chen, Y., Wang, X., and Zhang, Z. Unified vision-language-action model. In _International Conference on Learning Representations_ , 2025. 

   - Wong, J., Tung, A., Kurenkov, A., Mandlekar, A., Fei-Fei, L., Savarese, S., and Mart´ın-Mart´ın, R. Error-aware imitation learning from teleoperation data for mobile manipulation. In _Conference on Robot Learning_ , 2022. 

   - Xia, Z., Xu, J., Zhang, Y., and Liu, H. A survey of uncertainty estimation methods on large language models. In _Findings of the Association for Computational Linguistics_ , 2025. 

   - Xie, A., Tajwar, F., Sharma, A., and Finn, C. When to ask for help: Proactive interventions in autonomous reinforcement learning. _Advances in Neural Information Processing Systems_ , 2022. 

   - Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., and Hooi, B. Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms. In _Conference on Learning Representations_ , 2023. 

   - Xu, C., Nguyen, T. K., Dixon, E., Rodriguez, C., Miller, P., Lee, R., Shah, P., Ambrus, R., Nishimura, H., and Itkina, M. Can we detect failures without failure data? uncertainty-aware runtime failure detection for imitation learning policies. In _Robot Evaluation for the Real World_ , 2025. 

   - Zhang, Z., Zheng, C., Wu, Y., Zhang, B., Lin, R., Yu, B., Liu, D., Zhou, J., and Lin, J. The lessons of developing process reward models in mathematical reasoning. In _Findings of the Association for Computational Linguistics_ , 2025. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2023. 

   - Zollo, T. P. and Zemel, R. Confidence calibration in vision-language-action models. _arXiv preprint arXiv:2507.17383_ , 2025. 

   - Zou, A., Phan, L., Chen, S., Campbell, J., Guo, P., Ren, R., Pan, A., Yin, X., Mazeika, M., Dombrowski, A.-K., et al. Representation engineering: A top-down approach to ai transparency. _arXiv preprint arXiv:2310.01405_ , 2023. 

- van der Laan, L. and Kallus, N. Bellman calibration for v- learning in offline reinforcement learning. _arXiv preprint arXiv:2512.23694_ , 2025. 

- Vovk, V., Gammerman, A., and Shafer, G. _Algorithmic learning in a random world_ . Springer, 2005. 

12 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

## **A. Limitations and future work** 

**Limitations.** We emphasize three main limitations. First, we observe that the failure predictor generalizes across unseen tasks within an environment but not across environments, embodiments, or action parameterizations. For instance, we report in Apx. G.2 that transferring the OpenVLA LIBERO-10 predictor directly to the WidowX environment yields only 53 _._ 69 _±_ 5 _._ 07 ROC-AUC and a sequential Brier score of 0 _._ 413 _±_ 0 _._ 03. We believe that such broad generalization may require a different approach. Second, our experimental results are performed with binary episodic success; Note however that our formulation in Section 4 accounts for general reward functions and TDQC can easily be extended to such. Third, our guided action-selection operates under a one-step look-ahead. While effective in simulation, this requires environment access at inference time and is therefore not directly deployable in real-world settings without a forward model. Recent advances in world models for robotics (Badithela et al., 2025; Gemini Robotics Team et al., 2026) offer a promising path toward addressing this. 

**Future Works.** We conclude with several potential future extensions of our work. Recent advances on world models (Gemini Robotics Team et al., 2026; Badithela et al., 2025) could be exploited to improve uncertainty estimation of robot policies in the real world. Our approach could also be extended for LLM calibration (Orgad et al., 2025; Radharapu et al., 2025), interpreting text generation as a sequential task. 

## **B. Proof for Theorem 5.1** 

Fix a policy _π_ and consider an episodic process with horizon _T_ . Let _ht_ denote the history available up to time _t_ , as defined in Section 2.2. We study the problem of predicting the _future rewards_ from partial information: at time _t_ we observe _ht_ and seek a predictor _f_<sup>ˆ</sup> ( _ht_ ) of the total future rewards. 


where _r_ ( _hi_ ) denotes the (possibly stochastic) reward at step _i_ given the history _ht_ . 

Theorem 5.1 states that the predictor minimizing the conditional mean squared error 


is given by: 


Meaning that, in order to minimize the _sequential Brier Score_ , one must approximate the Q-function _Q_<sup>_π_</sup> _t_<sup>(</sup><sup>_ht, at_).</sup> 

_Proof._ We begin by denote _R_ ( _hT_ ) := _R_ for ease of notation. We recall that the optimal estimator in terms of MSE takes the form of E _hT ∈HT_ [ _R | ht_ ]. 

Suppose we stop at step _t_ and can only access _ht_ , meaning we don’t know _hT_ and thus, don’t have access to _{r_ ( _hi_ ) _}_<sup>_T_</sup> _i_ = _t_ +1<sup>,</sup> so we’ll replace E<sup>_π_</sup> _hT ∈HT_<sup>[�</sup><sup>_T_</sup> _j_ = _t_ +1<sup>_r_(</sup><sup>_hj_)</sup><sup>_| ht_] with</sup><sup>_f_ˆ(</sup><sup>_ht_).</sup> 


Where the last equality holds since we know the rewards and histories until time step _t_ . 

13 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

Note that: 


The amended sequential Brier Score for this case is: 

Because we have information until time step _t_ , then _f_<sup>ˆ</sup> ( _ht_ ) is constant and can be treated as a number. Also, E<sup>_π_</sup> _hT ∈HT_ �� _it_ =1<sup>_r_(</sup><sup>_hi_)</sup> � is a constant and can be outside of the inner expectation. Let’s look at the inner expectation: 


We can add and subtract �E<sup>_π_</sup> _hT ∈HT_<sup>[</sup><sup>_R | ht_]</sup> �2 from the equation: 


Lets break down the term E E<sup>_π_</sup> _hT ∈HTT ∈HT ∈HTT_<sup>[</sup><sup>_R | ht | ht htt_]::</sup> 

We can use Equation (8) and the inner expectation looks like:) and the inner expectation looks like: 

The _f_<sup>ˆ</sup> ( _ht_ ) that will minimize this term is (inverse of law of total expectation): 


14 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

## **C. Brier Score Decomposition** 

By adding and subtracting _η_ ( _F_ ) and expanding the square, 


Taking expectations, the cross term vanishes since 


and therefore 


Moreover, since _Y | F ∼_ Bernoulli( _η_ ( _F_ )), 


## **D. Functional Conformal Prediction** 

We follow (Gu et al., 2025; Xu et al., 2025; Diquigiovanni et al., 2021) for one-sided CP band calculations to determine the time varying threshold _δt_ and use two calibration datasets _D_ cal _A , D_ cal _B_ . Under the exchangeability assumption (Vovk et al., 2005) and given a user-specified significance level _α_ , the CP band guarantees that, for a new successful rollout, its failure probability 1 _− fθ_ will lie within band _δt_ for all times _t_ with probability 1 _− α_ . Conversely, if the failure probability of a test rollout rises above that threshold, we can label it as a failure with nominal confidence of 1 _− α_ . See Alg. 2 for the detailed calculations. Note that this assumption holds for every time step _t_ since we consider the _maximal_ failure detection score until time step _t_ and not 1 _− fθ_ ( _ht_ ). 

Intuitively, Eq. (9) in Algorithm 2 removes the top _α_ most extreme rollouts from set _D_ cal _A_ before calculating the width of the prediction bands. This ensures the actual band width represents the bulk of the data, not the outliers. Additionally, the maximum over _t_ is taken because the conformal prediction band is intended to reflect the entire trajectory. We define 


as the collection of such maximum deviations from the mean. The band width _h_ is computed as the (1 _− α_ )-quantile of _S_ , and the upper bound is given by 


Note that _Dj_ ’s were dividing by scal _A_ ( _t_ ) in Eq. (9), we then multiply by this term in line 24 to map the results back to the original scale. 

## **E. Algorithms** 

Algorithms 3 and 4 describe the pseudo code for both Early Stopping with Conformal Prediction and Test-Time Guided Action Search. 

## **F. Experiments Details** 

### **F.1. Code** 

You can find the Github repository here: https://github.com/shellytechnion/TDQC This repository contains the implementation for this paper. The codebase is built upon and extends the Gu et al. (2025) work on failure detection in Vision-Language-Action (VLA) models. 

15 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

### **Algorithm 2** Split-Conformal Trajectory Upper Band with Modulation 

**input** Calibration rollouts _D_ cal, miscoverage level _α ∈_ (0 _,_ 1), scoring network _S_ ( _·_ ; _θ_ ), rollout horizon _T_ 1: Split _D_ cal into two disjoint sets: _D_ cal _A_ = _{P_<sup>_k_</sup> _}_<sup>_N_</sup> _k_ =1<sup>1and</sup><sup>_D_cal</sup><sup>_B_=</sup><sup>_{P j}N_</sup> _j_ =1<sup>2.</sup> 2: **Compute mean successful trajectory on** _D_ cal _A_ **:** 3: **for** _t_ = 1 _, . . . , T_ **do** 4: _µt ← N_ <u>11</u> � _Nk_ =11<sup>_S_(</sup><sup>_P_</sup> _t_<sup>_k_;</sup><sup>_θ_)</sup> 5: **end for** 6: **Compute trimming threshold** _γ_ **on** _D_ cal _A_ **:** 7: **for** _k_ = 1 _, . . . , N_ 1 **do** 8: _Mk ←_ max _t∈_ [ _T_ ] �� _S_ ( _Pt k_<sup>;</sup><sup>_θ_)</sup><sup>_−µt_</sup> �� 9: **end for** 10: _γ ←_ Quantile1 _−α {Mk}_<sup>_N_</sup> _k_ =1<sup>1</sup> � � 11: **Define index set** _H_ **for modulation computation:** [ _N_ 1] _,_ if ( _N_ 1 + 1)(1 _− α_ ) _> N_ 1 _, H_ = �� _k ∈_ [ _N_ 1] : max _t∈_ [ _T_ ] �� _S_ ( _Pt k_<sup>;</sup><sup>_θ_)</sup><sup>_−µt_</sup> �� _≤ γ_ � _,_ otherwise _,_ 12: **Compute modulation function** _s_ cal _A_ ( _t_ ) **:** 13: **for** _t_ = 1 _, . . . , T_ **do** 14: _s_ cal _A_ ( _t_ ) _←_ max �� _S_ ( _Pt k_<sup>;</sup><sup>_θ_)</sup><sup>_−µt_</sup> �� (9) _k∈H_ 15: **end for** 16: **Compute normalized max-deviation scores on** _D_ cal _B_ **:** 17: **for** _j_ = 1 _, . . . , N_ 2 **do** _<u>µt−S</u>_ <u>(</u> _Pt_<sup>_j_</sup><sup><u>;</u></sup><sup>_θ_</sup><sup><u>)</u></sup> 18: _Dj ←_ max _t∈_ [ _T_ ] � _s_ cal _A_ ( _t_ ) � 19: **end for** 20: _D ←{Dj | j_ = 1 _, . . . , N_ 2 _}_ 21: **Compute conformal band width and upper bound:** 22: _h ←_ Quantile1 _−α_ ( _D_ ) 23: **for** _t_ = 1 _, . . . , T_ **do** 24: _δt ← µt_ + _h · s_ cal _A_ ( _t_ ) 25: **end for** 

### **F.2. VLA models** 

We show experiments on 4 state-of-the-art open source VLA models: OpenVLA (Kim et al., 2024), UniVLA (Wang et al., 2025), _π_ 0-FAST (Pertsch et al., 2025) and _π_ 0 (Black et al., 2024). OpenVLA use MIT license; _π_ 0 and _π_ 0-FAST use Apache-2.0 license. At the time of writing, UniVLA does not specify an open-source license in its repository. 

### **F.3. Action and Token Probability Modeling** 

**OpenVLA** (Kim et al., 2024) represents an action with _D_ discrete tokens, where each token represents one dimension of the robot’s action space (DoF). For each dimension _d ∈{_ 1 _, . . . , D}_ , the policy outputs logits _zt_<sup>(</sup><sup>_d_)</sup> and probabilities 


for action tokens _k ∈{_ 1 _, . . . , K}_ in an action vocabulary of size _K_ . At time _t_ , the policy selects the top tokens 

for each action dimension _d_ , and decodes them into a continuous action for execution by the robot. 

Both the **UniVLA** and _π_ 0 **-FAST** models use the FAST tokenizer (Pertsch et al., 2025), which applies a Discrete Cosine Transform (DCT) to encode continuous action trajectories into discrete action tokens. Given a window of size _H_ , we define 

16 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

|**Algorithm 3**EarlyStopping|
|---|
|**input** Policy_π_, dataset_D_cal, confidence_α_|
|1: _fθ ←_TDQC(_π, D_cal)<br>2: Sample_D_vali.i.d. from_D_cal<br>3: _{δt}_<sup>_T_</sup><br>_t_=1 <sup>_←_ConfPred(</sup><sup>_π, fθ, D_val)</sup><br>_{_Algorithm2_}_<br>4: **for**_t_= 1_, . . . , T_ **do**|
|5:<br>Execute action_a ∼π_(_xt_)|
|6:<br>Append(_at, rt, xt_+1)to_ht−_1|
|7:<br>**if**1_−fθ_(_ht_)_> δt_**then**break<br>8: **end for**|
|**Algorithm 4** Q-Value Guided Action Search|
|**input** observation_xt_, policy_π_, learned Q-function_fθ_, simulator_W_, sample size_M_, threshold <sup>¯</sup>_T_|
|1: _at_ = arg max_a′ π_(_a_<sup>_′_</sup>_|xt_)<br>_{_Greedy action_}_|
|2: **if**_fθ_(_xt, at_)_≤_<sup>¯</sup>_T_ **then**_{_High success confidence_}_|
|3:<br>Execute_at_|
|4: **else**|
|5:<br>**for**_i_= 1_, . . . , M_ **do**<br>|
|6:<br>_a_<sup>(</sup><sup>_i_)</sup><br>_t_<br>_∼π_(_xt_)<br>_{_Sample candidate action_}_|
|7:<br>_x_<sup>(</sup><sup>_i_)</sup><br>_t_+1 <sup>_∼W_(</sup><sup>_xt, a_(</sup><sup>_i_)</sup><br>_t_ <sup>)</sup><br><br>|
|8:<br>_a_<sup>(</sup><sup>_i_)</sup><br>_t_+1 <sup>= arg max</sup><sup>_a′ π_(</sup><sup>_a′|x_(</sup><sup>_i_)</sup><br>_t_+1<sup>)</sup><br>_{_Greedy action_}_<br><br>|
|9:<br>_Q_<sup>(</sup><sup>_i_)</sup> _←fθ_(_x_<sup>(</sup><sup>_i_)</sup><br>_t_+1<sup>_, a_(</sup><sup>_i_)</sup><br>_t_+1<sup>)</sup>|
|10:<br>**end for**<br>|
|11:<br>_i_<sup>_⋆_</sup>_←_arg max_i Q_<sup>(</sup><sup>_i_)</sup><br>|
|12:<br>Execute_a_<sup>(</sup><sup>_i⋆_)</sup><br>_t_<br>13: **end if**|
|the raw continuous action sequence as_A_1:_H_ = _{a_1_, a_2_, . . . , aH}_, where each step_at_ is a_d_-dimensional vector. During<br>training, the FAST tokenizer encodes this continuous sequence into a discrete token sequence_La_ = [_T_1_, . . . , Tn_], where<br>each token_Ti_is drawn from a vocabulary_V_ of size_|V|_. Analogous to natural language processing, sequence lengths can<br>vary, resulting in a variable-length (_n_) discrete representation. During inference, these discrete tokens are decoded back into<br>continuous robot actions_A_1:_H_. For each token_Ti_, the model outputs logits_z_<sup>(</sup><sup>_Ti_)</sup><br>_t_<br>over the vocabulary, which are converted<br>into probabilities via a softmax operation:|


We refer to these as token probabilities, which we utilize in our “black-box” configuration as _ht_ . 

### **F.4. Benchmarks Statistics** 

|**Benchmark**|**Nu**|**mber of Ta**|**sks**||**Number**|**of rollouts**||
|---|---|---|---|---|---|---|---|
||**Seen**|**Unseen**|**Total**|**Train**|**Eval Seen**|**Eval Unseen**|**Total**|
|LIBERO|7|3|10|210|140|150|500|
|Real Franka|10|3|13|450|150|180|780|
|Real WidowX|6|2|8|250|133|149|532|


_Table 3._ Benchmark statistics: task split into seen/unseen subsets and corresponding numbers of training and evaluation rollouts. 

Table 3 summarize each benchmark statistics on the number of tasks and rollouts. We note that while TDQC methods requires training data, they exhibit an improvement over the baselines in the real-robot experiments where they are trained on a much smaller dataset. Table 4 shows the number of timesteps per benchmark and VLA model pairs. 

17 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

|**Benchmark**|**VLA Model**|**Number of Environment Steps**|
|---|---|---|
||OpenVLA|199_,_279|
|LIBERO-10|_π_0|151_,_755|
||_π_0-FAST|183_,_488|
||UniVLA|134_,_746|
|WidowX|OpenVLA|26_,_600|
|Franka|_π_0-FAST|36_,_180|


_Table 4._ **Episode horizon by benchmark and model.** We report the maximum rollout length (environment time limit) used in each evaluation setting. 

|**Model**|**LIBERO-10**|
|---|---|
|OpenVLA|52%|
|_π_0-FAST|60.2%|
|_π_0|82.2%|
|UniVLA|90.6%|


_Table 5._ LIBERO-10 Task success rates across models 

**LIBERO-10** We evaluate the VLA models on LIBERO-10, which consists of 10 long-horizon manipulation tasks and contains the most diverse objects, environments and instructions among the 4 LIBERO suits, thus considered the most challenging suite. We kept the same initial conditions of each enviorment as specified in the benchmark details.<sup>3</sup> We constructed a task-level split into training, validation, and testing: we train and validate on 7 tasks and evaluate generalization on the remaining 3 unseen tasks. The specific tasks split is re-sampled over random seeds, i.e., each seed induces a different set of test tasks. Within the 7 training tasks, we further split rollouts into train/validation with a 60% _/_ 40% ratio. Each task includes 50 randomized initializations (e.g., variations in object placement), meaning a total of 10 _×_ 50 = 500 episodes. Table 5 reports the rollout success rates of all evaluated VLA policies. 

In LIBERO, the simulator terminates an episode as soon as the task succeeds, or when a maximum horizon is reached (520 steps for LIBERO-10). As a result, successful rollouts are often shorter than failed ones, which can cause a success estimators to induce information based on the length of the rollout alone. To ensure a fair comparison of ROC-AUC, we follow a fixed-cutoff method that was introduced in Gu et al. (2025). For each task, we compute the minimum rollout length observed across its episodes and use this value as the effective horizon _T_ for evaluation _Tk_ = min _r∈k Tr_ where _k_ denotes the task and _r_ is a rollout. Meaning, we only report ROC-AUC values up to this termination time. This ensures that all rollouts for a given task are evaluated on comparable trajectory prefixes. 

**Real Robot WidowX** We used published data<sup>4</sup> that tested OpenVLA pretrained on ”Open-X Magic soup++” dataset on real WidowX robot arm which achieved success rate of 45 _._ 8%. In this experiment, they collected 532 rollouts on the 8 tasks, with 244 successes and 288 failures. Each task has roughly the same number of rollouts. We constructed a task-level split into training, validation, and testing: we train and validate on 6 tasks and evaluate generalization on the remaining 2 unseen tasks. The specific tasks split is re-sampled over random seeds, i.e., each seed induces a different set of test tasks. When we evaluated on multiple seeds, each seed determines a different configuration of train and test tasks split. Within the 6 training tasks, we further split rollouts into train/validation with a 66% _/_ 33% ratio. For each task, they set a fixed number of allowed time steps (50) and all rollouts ended in the same time step, even if success occurred before that time step. 

**Real-world Franka** We used published data<sup>5</sup> that tested _π_ 0-FAST on various real-world experiments. For each task, the maximum time horizon was predetermined and constant inside each task. We split to train, validation and test such that we train and validate on 10 tasks and test on 3 tasks. The authors of (Gu et al., 2025) recorded the rollouts such that the dataset will have 50% success on each task. 

> 3https://github.com/Lifelong-Robot-Learning/LIBERO/tree/master/libero/libero/init_files/ libero_10 

> 4https://github.com/vla-safe/SAFE 

> 5https://github.com/vla-safe/SAFE 

18 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

### **F.5. Static baselines** 

Many VLA models discretize continuous actions into descrete action tokens. At time step _t_ , the policy produces a distribution over tokens conditioned on the trajectory history and the language instruction, 


where _ht_ denotes the available history (e.g., past observations and actions) and _l_ is the language instruction. For robots with _|D|_ degrees of freedom (DoF), we write the predicted token vector as _At_ = ( _a_<sup>1</sup> _t_<sup>_, . . . , a_</sup> _t_<sup>_|D|_</sup> ), with corresponding probabilities _Pt_ = ( _p_<sup>1</sup> _t_<sup>_, . . . , p_</sup> _t_<sup>_|D|_</sup> ), where _p_<sup>_i_</sup> _t_<sup>≜</sup><sup>_pt_(</sup><sup>_ai_</sup> _t_<sup>)</sup><sup>_∈_(0</sup><sup>_,_1] is the probability assigned to the selected token for DoF</sup><sup>_i_.Let</sup><sup>_H_</sup> _t_<sup>_i_denote</sup> the entropy of the token distribution for DoF _i_ at time _t_ . 

We follow the LLM hallucinations literature (Xiong et al., 2023; Huang et al., 2024; Shorinwa et al., 2025; Ren et al., 2023) and Zollo & Zemel (2025) and used the same methods to measure uncertainty in VLA model. We compute the following uncertainty scores at each timestep. For probability-based scores we use the negative log-probability, so that larger values indicate higher uncertainty: 


The first two families use the confidence of the _chosen_ action’s DoF (via _−_ log _p_<sup>_i_</sup> _t_<sup>), i.e. the token in the action that corresponds</sup> to the highest probability, while the entropy scores uses the full token distributions. Finally, Running Avg Prob aggregates uncertainty over time via a running average, which can be interpreted as a lightweight temporal smoothing baseline (without learning). 

### **F.6. Trained Baselines** 

**SAFE-RNN** uses an LSTM model with 1 layer and a hidden dimension of 256, and an additional linear layer is used to project the hidden states of LSTM into a single scalar state. **SAFE-MLP** uses a multi-layer perceptron with 2 layers and a hidden dimension of 256. RNN-BCE and RNN-TDQC methods use the same LSTM architecture for all benchmarks, except OpenVLA, where the LSTM is replaced by a GRU. In **OpenVLA with action probabilities** , we trained a GRU network with A two-layer MLP with and a 1 layer GRU, the GRU’s output is passed through a two-layer MLP head that produces a single scalar output. Since successes and failures from the generated rollouts are imbalanced, the losses on positive (failed) and negative (successful) rollouts are weighted by their inverse class frequency. 

Given the internal feature vectors _E ∈_ R<sup>_n×d_</sup> produced by a VLA model, where _n_ corresponds to token positions, diffusion steps, etc. and _d_ is the feature dimension. Gu et al. (2025) aggregate _E_ into a single fixed-dimensional feature vector _e ∈_ R<sup>_d_</sup> before inputting to SAFE models. They ablate on which feature vector to use in order to achieve highest ROC-AUC. In _π_ 0 Gu et al. (2025) takes the feature vectors before the projection into the velocity field. The aggregation methods in _π_ 0 are denoted as _agg_ hori, _agg_ hdiff Other implementation details appear both in SAFE paper (Gu et al., 2025) and in https://github.com/vla-safe/SAFE. 

19 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

### **F.7. Training Details** 

Following SAFE, for both metrics sequential Brier Score and ROC-AUC, we follow the evaluation in SAFE and interpreted the uncertainty estimations (probabilities) as the _probability of failure_ . 

We use AdamW optimizer (Loshchilov & Hutter, 2017) with weight decay of 0 _._ 01 , and learning rate (lr) that was determined by grid search and a step LR scheduler with gamma determined by a grid search. All models were trained for 1000 epochs with batch size 512. We also ablate on applying L2 regularization _λ_ reg loss on the model weights to reduce weights. Note that for the TDQC method that gets as an input the model’s probabilities we entered each data point sequentially. We concatenated all the rollount and samples ”starting index” from which we took a batch size next steps. If the rollout ended in the middle of the batch - we reset the network’s hidden state. In SAFE methods, each rollout is considered as one data point and thus batch size of 512 translates to training on (at most) 512 rollouts in each iteration. All training and evaluation are done on a single NVIDIA RTX 5090 32GB GPU. 

### **F.8. Hyperparameter Tuning** 

To tune TDQC, we perform a grid search over hyperparameters and select the configuration that **maximizes sequential Brier score** on a held-out validation set of rollouts from the same tasks as in training. Unlike Gu et al. (2025), which evaluates each hyperparameter setting across all random seeds and then reports the best-performing one (in terms of ROC-AUC), we decouple tuning and evaluation: we run the hyperparameter sweep on two tuning seeds and then fix the selected configuration and evaluate it on an additional nineteen seeds (21 total). Using a large number of evaluation seeds reduces selection bias and yields statistically meaningful comparisons. 

In Tables 6 to 11 we report the hyper-parameters we have searched over and the values of the best performance. For the SAFE methods - we used their chosen parameters for the LSTM and MLP methods. For MLP-BCE method we searched the same grid to find the best parameters. For SAFE methods without TD we choose the parameters that maximized the ROC-AUC, and for the TDQC parameters, we choose the ones that minimize the sequential Brier Score. Unless stated otherwise, in action probability methods (OpenVLA model) we concatenated the top 10 probabilities for each degree of freedom, used learning rate step size of 200 and batch size of 512. For all methods, LR _λ_ = 1, and the number of layers is 2 for the projection in MLP and for LSTM method we used 1 LSTM layer. 

_Table 6._ Hyperparameter search space for OpenVLA + LIBERO benchmark. 

_Table 7._ Hyperparameter search space for OpenVLA + WidowX benchmark. 

|**Method**|**HParams**|**Values**|**Method**|**HParams**|**Values**|
|---|---|---|---|---|---|
||_agg_token|First**Last**Mean||_agg_token|First**Last**Mean|
|_SAFE-RNN_|lr<br>|**1e-4**3e-4 1e-3|_SAFE-RNN_|lr<br>|1e-4**3e-4**1e-3|
||_λ_reg|1e-3 1e-2 1e-1**1**<br>||_λ_reg|1e-3**1e-2**1e-1**1**<br>|
||_agg_token|First**Last**Mean||_agg_token|First**Last**Mean|
|_SAFE-RNN-TDQC_|lr|1e-5 5e-5**1e-4**3e-4 1e-3<br>|_SAFE-RNN-TDQC_|lr|1e-5**5e-5**1e-4 3e-4 1e-3<br>|
||lr _γ_|0.1**0.8**||lr _γ_|**0.1**0.8|
||_λ_reg|**0**1e-3 1e-1<br>||_λ_reg|0**1e-3**1e-1<br>|
||_agg_token|First**Last**Mean||_agg_token|First**Last**Mean|
|_SAFE-MLP_|lr|**1e-4**3e-4 1e-3|_SAFE-MLP_|lr|1e-4**3e-4**1e-3|
||_λ_reg|1e-3**1e-2**1e-1 1<br>||_λ_reg|1e-3 1e-2**1e-1**1<br>|
||_agg_token|First**Last**Mean||_agg_token|First**Last**Mean|
|_SAFE-MLP BCE_|lr|1e-4**3e-4**1e-3|_SAFE-MLP BCE_|lr|**1e-5**5e-5 1e-4 3e-4 1e-3|
||_λ_reg|1e-3 1e-2**1e-1**1||_λ_reg|0 1e-3**1e-1**1|
||_agg_token|First**Last**Mean||_agg_token|First**Last**Mean|
|_SAFE-MLP-TDQC_|lr|1e-5 5e-5**1e-4**3e-4 1e-3|_SAFE-MLP-TDQC_|lr|1e-5 5e-5 1e-4**3e-4**1e-3|
||_λ_reg|**0**1e-3 1e-1||_λ_reg|**0**1e-3 1e-1|
||LR-_γ_|**0.8**0.1||LR-_γ_|**0.1**0.8|
||GRU hidden|256**512**||GRU hidden|**256**512 1024|
||head hidden|256**512**||head hidden|256**512**|
|_RNN-BCE_|lr|**1e-5**5e-5 1e-4 1e-3|_RNN-BCE_|lr|1e-5 5e-5 1e-4 3e-4**1e-3**|
||lr _γ_|0.1**0.8**||lr _γ_|**0.1**0.8|
||_λ_reg|**0**1e-3 1e-2 1e-1||_λ_reg|0**1e-3**1e-1|
||GRU hidden|**256**512||GRU hidden|256 512**1024**|
||head hidden|256**512**||head hidden|256**512**|
|_RNN-TDQC_|lr|**1e-5**5e-5 1e-4 1e-3|_RNN-TDQC_|lr|**1e-5**5e-5 1e-4 3e-4 1e-3|
||lr _γ_|0.1**0.8**||lr _γ_|**0.1**0.8|
||_λ_reg|**0**1e-3 1e-2 1e-1||_λ_reg|**0**1e-3 1e-1|


20 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

_Table 9._ Hyperparameter search space for _π_ 0-FAST + Franka benchmark. 

_Table 8._ Hyperparameter search space for _π_ 0-FAST + LIBERO benchmark. 

|**Method**|**HParams**|**Values**|
|---|---|---|
||_agg_token|First Last**Mean**|
|_SAFE-RNN_|Feat|**Encoded**Pre-logits|
||lr|3e-5 1e-4**3e-4**1e-3|
||_λ_reg|**1e-3**1e-2 1e-1|
||_agg_token|First Last**Mean**|
||Feat|Encoded**Pre-logits**|
|_SAFE-RNN-TDQC_|lr|1e-5 5e-5 1e-4 3e-4**1e-3**|
||lr _γ_|**0.1**0.8|
||_λ_reg|**0**1e-3 1e-1|
||_agg_token|First**Last**Mean|
|_SAFEMLP_|Feat|Encoded**Pre-logits**|
|_-_|lr|3e-5**1e-4**1e-4 1e-3|
||_λ_reg|1e-3**1e-2**1e-1|
||_agg_token|First Last**Mean**|
||Feat|Encoded**Pre-logits**|
|_SAFE-MLP BCE_|lr _γ_|0.1**0.8**|
||lr|1e-5 5e-5**1e-4**3e-4 1e-3|
||_λ_reg|0**1e-3**1e-1|
||_agg_token|First Last**Mean**|
||Feat|Encoded**Pre-logits**|
|_SAFE-MLP-TDQC_|lr|1e-5 5e-5 1e-4 3e-4**1e-3**|
||_λ_reg|**0**1e-3 1e-1|
||lr _γ_|0.1**0.8**|
||lr|1e-5 3e-5 1e-4 3e-4**1e-3**|
|_RNN-BCE_|_λ_reg|1e-3**1e-1**0|
||lr _γ_|0.1**0.8**|
||lr|**1e-5**3e-5 1e-4 3e-4 1e-3|
|_RNN-TDQC_|_λ_reg|1e-3 1e-1**0**|
||lr _γ_|**0.1**0.8|


_Table 10._ Hyperparameter search space for _π_ 0 + LIBERO benchmark. 

|**Method**|**HParams**|**Values**|
|---|---|---|
||_agg_horri|**First**Last First&Last<br>|
|_SAFE-RNN_|_agg_diff|First**Last**First&Last|
||lr|1e-5 3e-5 1e-4 3e-4**1e-3**|
||_λ_reg|**1e-3**1e-2 1e-1|
||_agg_horri|**First**Last First&Last|
||_agg_diff|First Last**First&Last**|
|_SAFE-RNN-TDQC_|lr|1e-5 3e-5 1e-4**3e-4**1e-3|
||lr _γ_|**0.1**0.8|
||_λ_reg|**0**1e-3 1e-1|
||_agg_horri|**First**Last First&Last|
|_SAFEMLP_|_agg_diff|First**Last**First&Last|
|_-_|lr|1e-5**3e-5**1e-4 3e-4 1e-3|
||_λ_reg|**1e-3**1e-2 1e-1|
||_agg_horri|First Last**First**&**Last**|
||_agg_diff|First**Last**First&Last|
|_SAFE-MLP BCE_|lr|1e-5**3e-5**1e-4 3e-4 1e-3|
||lr _γ_|0.1**0.8**|
||_λ_reg|**0**1e-3 1e-1|
||_agg_horri|First Last**First**&**Last**|
||_agg_diff|First**Last**First&Last|
|_SAFE-MLP-TDQC_|lr|1e-5 3e-5 1e-4 3e-4**1e-3**|
||lr _γ_|0.1**0.8**|
||_λ_reg|**0**1e-3 1e-1|


|**Method**|**HParams**|**Values**|
|---|---|---|
||_agg_token|**Mean**|
|_SAFE-RNN_|Feat|**Pre-logits**|
||hidden dim|128**256**|
||lr|1e-4 3e-4**1e-3**3e-3|
||_λ_reg|1e-3**1e-2** 1e-1|
||_agg_token|**Mean**<br>|
||Feat|**Pre-logits**|
|_SAFERNNTDQC_|hidden dim|128**256**|
|_--_|lr|1e-5 5e-5 1e-4 3e-4**1e-3**|
||lr _γ_|0.1**0.8**|
||_λ_reg|**0**1e-3 1e-1<br>|
||_agg_token|**Mean**|
|_SAFE-MLP_|Feat|**Pre-logits**|
||lr|1e-4**3e-4**1e-3 3e-3|
||_λ_reg|**1e-3**1e-2 1e-1<br>|
||_agg_token|**First**Last Mean|
||Feat|**Pre-logits**|
|_SAFE-MLP BCE_|hidden dim|**128**256|
||lr _γ_|0.1**0.8**|
||lr|1e-5 5e-5 1e-4**3e-4**1e-3|
||_λ_reg|**0**1e-3 1e-1|
||_agg_token|**Mean**<br>|
||Feat|**Pre-logits**|
|_SAFE-MLP-TDQC_|hidden dim|128**256**|
||lr|1e-5 5e-5 1e-4 3e-4**1e-3**|
||_λ_reg<br>|**0**1e-3 1e-1<br>|
||lr _γ_|0.1**0.8**|
||hidden dim|128**256**|
|_RNNBCE_|lr|**1e-5**3e-5 1e-4 3e-4 1e-3|
|_-_|_λ_reg|1e-3**1e-1**0|
||lr _γ_|**0.1**0.8|
||hidden dim|128**256**|
|_RNN-TDQC_|lr|1e-5 3e-5**1e-4**3e-4 1e-3|
||_λ_reg|**1e-3**1e-1 0|
||lr _γ_|**0.1**0.8|


_Table 11._ Hyperparameter search space for UniVLA + LIBERO benchmark. 

|**Method**|**HParams**|**Values**|
|---|---|---|
||_agg_token|**First**Last Mean|
|_SAFE-RNN_|lr|**1e-5**3e-5 1e-4 3e-4 1e-3|
||_λ_reg|1e-3**1e-1**0|
||lr _γ_|**0.1**0.8|
||_agg_token<br>|**First**Last Mean<br>|
|_SAFE-RNN-TDQC_|lr|1e-5**3e-5**1e-4 3e-4 1e-3|
||_λ_reg|**1e-3**1e-1 0|
||lr _γ_|**0.1**0.8|
||_agg_token|**First**Last Mean|
|_SAFE-MLP_|lr|1e-5 3e-5 1e-4 3e-4**1e-3**|
||_λ_reg|1e-3**1e-1**0|
||lr _γ_|**0.1**0.8|
||_agg_token|**First**Last Mean|
|_SAFE-MLP BCE_|lr|**1e-5**3e-5 1e-4 3e-4 1e-3|
||_λ_reg|1e-3**1e-1**0|
||lr _γ_|**0.1**0.8|
||_agg_token|**First**Last Mean|
|_SAFE-MLP-TDQC_|lr|1e-5 3e-5**1e-4**3e-4 1e-3|
||_λ_reg|**1e-3**1e-1 0|
||lr _γ_|0.1**0.8**|
||lr|1e-5 3e-5 1e-4 3e-4**1e-3**|
|_RNN-BCE (Top 10)_|_λ_reg|1e-3 1e-1**0**|
||lr _γ_|**0.1**0.8|
||lr|1e-5 3e-5**1e-4**3e-4 1e-3|
|_RNN-TDQC_|_λ_reg|**1e-3**1e-1 0|
||lr _γ_|0.1**0.8**|


21 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

## **G. Additional Results** 

### **G.1. Results variance** 

In Table 12 and Table 13 we report the standard deviation for all results in Tables 1 and 2. Note that the reported values were averaged over 21 seeds which set the environment seed and determines the train-test split of tasks. Since different tasks have different difficulties it is reasonable to see large standard deviations in the tables. Tables 12 and 13 shows that across models and benchmarks, _TDQC learning improves calibration relative to non-TDQC variants_ , with relatively lower standard deviations compared to the baselines, where SAFE-RNN-TDQC performs the best or on par for all _π_ 0 model variants. 

|VLA Model|Open|VLA|Open|VLA|UniV|LA|_π_0-F|AST|_π_0-F|AST|_π_|0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Benchmark|LIBE|RO|Wido|wX|LIBE|RO|LIB|ERO|Fra|nka|LIB|ERO|
|Eval Task Split|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen _↓_|Seen _↓_|Unseen_↓_|
|Max prob.|0_._395_±_0_._037|0_._390_±_0_._028|0_._572_±_0_._060|0_._579_±_0_._012|0_._909_±_0_._024|0_._899_±_0_._048|0_._320_±_0_._021|0_._318_±_0_._022|0_._331_±_0_._018|0_._323_±_0_._017|_−_|_−_|
|Avg prob.|0_._348_±_0_._036|0_._364_±_0_._061|0_._275_±_0_._012|0_._282_±_0_._019|0_._529_±_0_._017|0_._532_±_0_._035|0_._212_±_0_._019|0_._218_±_0_._024|0_._290_±_0_._016|0_._294_±_0_._024|_−_|_−_|
|Running Avg prob.|0_._338_±_0_._034|0_._356_±_0_._059|0_._255_±_0_._003|0_._257_±_0_._002|0_._543_±_0_._016|0_._544_±_0_._031|0_._244_±_0_._024|0_._238_±_0_._045|0_._359_±_0_._029|0_._361_±_0_._026|_−_|_−_|
|Avg entropy|0_._306_±_0_._020|0_._313_±_0_._030|0_._414_±_0_._044|0_._426_±_0_._095|0_._406_±_0_._027|0_._391_±_0_._063|0_._209_±_0_._022|0_._222_±_0_._033|0_._281_±_0_._017|0_._281_±_0_._021|_−_|_−_|
|RunningAvgentropy|0_._265_±_0_._014|0_._273_±_0_._026|0_._435_±_0_._028|0_._432_±_0_._054|0_._343_±_0_._016|0_._330_±_0_._039|0_._279_±_0_._021|0_._264_±_0_._046|0_._341_±_0_._025|0_._339_±_0_._027|_−_|_−_|
|_SAFE-RNN_|0_._204_±_0_._038|0_._255_±_0_._059|0_._169_±_0_._061|0_._213_±_0_._075|0_._124_±_0_._020|0_._162_±_0_._014|0_._106_±_0_._018|0_._148_±_0_._042|0_._220_±_0_._047|0_._288_±_0_._055|0_._123_±_0_._043|0_._172_±_0_._095|
|_SAFE-RNN-TDQC (Ours)_|0_._197_±_0_._024|0_._218_±_0_._020|**0**_._**096**_±_**0**_._**021**|**0**_._**153**_±_**0**_._**056**|**0**_._**064**_±_**0**_._**016**|**0**_._**100**_±_**0**_._**026**|**0**_._**103**_±_**0**_._**028**|0_._163_±_0_._060|**0**_._**150**_±_**0**_._**026**|**0**_._**215**_±_**0**_._**038**|**0**_._**061**_±_**0**_._**019**|**0**_._**097**_±_**0**_._**033**|
|_SAFE-MLP BCE_|0_._192_±_0_._020|0_._231_±_0_._020|0_._127_±_0_._019|0_._164_±_0_._034|0_._091_±_0_._022|0_._158_±_0_._036|**0**_._**103**_±_**0**_._**019**|0_._162_±_0_._053|0_._206_±_0_._016|0_._248_±_0_._023|0_._075_±_0_._018|0_._137_±_0_._058|
|_SAFE-MLP-TDQC (Ours)_|0_._195_±_0_._022|0_._229_±_0_._022|0_._130_±_0_._022|0_._169_±_0_._038|0_._066_±_0_._015|0_._131_±_0_._028|0_._109_±_0_._022|0_._150_±_0_._035|0_._210_±_0_._008|0_._229_±_0_._013|0_._068_±_0_._021|0_._128_±_0_._060|
|_RNN-BCE_|0_._199_±_0_._016|0_._206_±_0_._022|0_._301_±_0_._062|0_._344_±_0_._048|0_._138_±_0_._047|0_._152_±_0_._065|0_._122_±_0_._022|0_._158_±_0_._053|0_._238_±_0_._006|0_._243_±_0_._005|_−_|_−_|
|_RNN-TDQC (Ours)_|**0**_._**191**_±_**0**_._**015**|**0**_._**197**_±_**0**_._**021**|0_._156_±_0_._023|0_._192_±_0_._039|0_._100_±_0_._025|0_._107_±_0_._056|0_._105_±_0_._020|**0**_._**141**_±_**0**_._**045**|0_._205_±_0_._015|0_._228_±_0_._022|_−_|_−_|


_Table 12._ Brier Score results on simulation and real robot experiment (lower is better). Results are averaged over 21 seeds that determined different train-test split of tasks. ” _−_ ” indicates that the Brier score can’t be calculated on the method. The **first** and second best performing methods are highlighted in the table. 

|VLA Model<br>Benchmark|Open<br>LIBE|VLA<br>RO|Open<br>Wid|VLA<br>owX|UniV<br>LIB|LA<br>ERO|_π_0-F<br>LIBE|AST<br>RO|_π_0-F<br>Fra|AST<br>nka|LIB|_π_0<br>ERO|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Eval Task Split|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen _↑_|Seen _↑_|Unseen_↑_|
|Max prob.|54_._64_±_5_._36|55_._78_±_4_._33|53_._25_±_3_._36|53_._20_±_2_._70|50_._00_±_0_._00|50_._00_±_0_._00|61_._75_±_8_._85|63_._49_±_13_._6|48_._61_±_4_._58|46_._64_±_6_._95|_−_|_−_|
|Avg prob.|47_._08_±_4_._07|48_._09_±_5_._14|47_._47_±_3_._99|48_._30_±_4_._75|42_._96_±_8_._89|40_._25_±_7_._71|47_._36_±_7_._64|48_._09_±_7_._52|49_._45_±_5_._41|48_._03_±_8_._08|_−_|_−_|
|Running Avg prob.|49_._19_±_4_._16|47_._72_±_4_._38|49_._20_±_4_._51|46_._37_±_6_._82|43_._05_±_6_._14|40_._29_±_7_._54|53_._95_±_4_._42|55_._68_±_7_._40|52_._95_±_3_._92|49_._98_±_4_._19|_−_|_−_|
|Avg entropy|46_._81_±_4_._22|46_._75_±_4_._77|50_._19_±_4_._64|49_._36_±_8_._16|41_._34_±_9_._42|47_._36_±_11_._8|45_._42_±_7_._44|46_._30_±_7_._22|49_._28_±_4_._34|49_._07_±_7_._42|_−_|_−_|
|RunningAvgentropy|50_._48_±_4_._34|48_._09_±_4_._76|46_._16_±_5_._38|43_._99_±_8_._08|51_._63_±_8_._50|56_._71_±_7_._78|53_._78_±_5_._27|55_._44_±_6_._86|51_._12_±_4_._53|48_._78_±_5_._02|_−_|_−_|
|_SAFE-RNN_|72_._30_±_4_._73|69_._04_±_7_._01|75_._95_±_7_._29|70_._00_±_5_._95|74_._48_±_9_._49|68_._13_±_11_._4|91_._26_±_3_._18|**85**_._**88**_±_**7**_._**63**|70_._85_±_5_._92|56_._69_±_7_._33|79_._95_±_9_._22|65_._03_±_20_._5|
|_SAFE-RNN-TDQC (Ours)_|71_._67_±_4_._00|65_._12_±_4_._94|84_._01_±_3_._89|70_._76_±_7_._72|73_._83_±_8_._52|64_._25_±_12_._6|**92**_._**03**_±_**3**_._**37**|85_._49_±_6_._96|**79**_._**89**_±_**6**_._**80**|**68**_._**43**_±_**7**_._**18**|88_._66_±_4_._54|**82**_._**94**_±_**10**_._**7**|
|_SAFE-MLP_|73_._56_±_3_._85|69_._53_±_5_._02|**88**_._**23**_±_**4**_._**37**|**83**_._**18**_±_**6**_._**36**|74_._39_±_7_._73|63_._80_±_13_._32|79_._00_±_12_._5|68_._36_±_24_._3|79_._01_±_4_._17|63_._69_±_7_._08|86_._33_±_4_._94|79_._75_±_13_._0|
|_SAFE-MLP-BCE_|72_._66_±_3_._39|64_._99_±_5_._26|85_._38_±_3_._49|71_._43_±_8_._49|**78**_._**83**_±_**5**_._**86**|69_._74_±_13_._9|91_._82_±_3_._23|85_._50_±_6_._58|73_._82_±_3_._61|58_._83_±_7_._31|**89**_._**71**_±_**3**_._**36**|80_._53_±_13_._8|
|_SAFE-MLP-TDQC (Ours)_|71_._22_±_3_._23|60_._09_±_7_._09|82_._33_±_3_._71|70_._64_±_9_._42|76_._55_±_5_._68|66_._71_±_12_._6|90_._26_±_3_._22|84_._40_±_7_._62|61_._95_±_6_._47|51_._22_±_6_._53|86_._57_±_4_._99|72_._07_±_18_._4|
|_RNN-BCE_|72_._70_±_4_._26|72_._28_±_4_._26|69_._69_±_6_._29|67_._09_±_5_._48|63_._44_±_7_._92|54_._37_±_12_._5|87_._67_±_4_._11|82_._53_±_10_._4|59_._32_±_4_._55|53_._26_±_7_._34|_−_|_−_|
|_RNN-TDQC (Ours)_|**74**_._**20**_±_**3**_._**70**|**72**_._**72**_±_**4**_._**29**|78_._90_±_7_._46|72_._97_±_6_._69|72_._30_±_7_._52|**70**_._**17**_±_**11**_._**5**|87_._51_±_3_._65|83_._39_±_9_._67|64_._10_±_4_._11|57_._37_±_9_._30|_−_|_−_|


_Table 13._ ROC-AUC results on simulation and real robot experiment (higher is better). Results are averaged over 21 seeds that determined different train-test split of tasks. ” _−_ ” indicates that the ROC-AUC can’t be calculated on the method. The **first** and second best performing methods are highlighted in the table. 

### **G.2. Generalization across benchmarks** 

To assess the generalization capability of the success predictors, we trained an RNN-TDQC (top-10) predictor on OpenVLA trajectories from the LIBERO benchmark and evaluated it on OpenVLA trajectories from the WidowX benchmark. On the unseen WidowX tasks, the predictor achieved a ROC-AUC of 53 _._ 69 _±_ 5 _._ 07 and a sequential Brier score of 0 _._ 413 _±_ 0 _._ 03, compared to 72 _._ 97 _±_ 6 _._ 69 and 0 _._ 192 _±_ 0 _._ 039, respectively, on the original LIBERO tasks. These results suggest that the success predictor has limited generalization capabilities. 

### **G.3. Extended Evaluation for Application to Test-Time Action Search** 

In order to extend out evaluations for test-time action search, we added to Figure 4ablation configurations: _Probs Entropy_ is a heuristic approach that does not rely on a learned Q-value, serving as a natural, zero-shot baseline. The inclusion of this method is motivated by the need to determine whether a separately trained value network _fθ_ is necessary; it tests the hypothesis that the base VLA model’s internal predictive certainty is a sufficient indicator of action quality. It is the ’Avg Entropy’ method from Tables 1 and 2, which achieved good sequential brier and ROC-AUC compared the the static baselines. It selects the action with lowest mean entropy across all _D_ action dimensions: 


More details are in Apx. F.5. 

22 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_(a)_ Success rate comparison across specific tasks, including ablation configurations. 


_(b)_ Average episode length (steps) per task, including ablation configurations. 


_(c)_ Averaged number of steps used action search per task, including ablation configurations. 

_Figure 5._ **Extended Analysis of Guided Action Search and TDQC Efficiency.** The results demonstrate that _RNN-TDQC_ provides the highest success rates, while the _Threshold 0.35_ variant offers a significant reduction in computational overhead by selectively triggering action search only when safety is at risk while maintaining high success rates. 

While results in the paper summarized the average success rate across all tasks, we provide a more granular breakdown in Figure 5a-c to analyze per-task performance and computational trade offs. Figure 5a details the success rates for 3 unseen tasks: placing a _bowl in a drawer_ (Task 3), moving _two mugs to plates_ (Task 4), and placing a _mug in a microwave_ (Task 9). We observe that TDQC-based methods consistently outperform the baseline across all unseen tasks, with _RNN-TDQC_ achieving the highest success rate across all configurations. 

As shown in Figure 5c, while the _TDQC-Threshold 0.35_ variant achieves success rates that exceed the baseline, its primary advantage lies in computational efficiency. By comparing the average episode length (Figure 5b) with the actual number of steps triggered the action search (Figure 5c), it is evident that this strategy significantly reduces total compute requirements while maintaining competitive performance. 

### **G.4. Computational Cost** 

For real robot deployment, test-time compute for TDQC is not more costly than baselines such as SAFE: both require only a forward pass of the MLP/LSTM at every time step, typically much lighter than the VLA forward pass. Furthermore, the network for TDQC with action probabilities as input is lightweight, and smaller than SAFE with features as input. RL theory suggests that TD-based methods require longer training than Monte-Carlo (MC) methods, thus, we evaluated all methods on the same GPU (NVIDIA RTX 5090) with 5 seeds on various computational metrics. Results are reported in Tables 14 and 15. From our analysis, the overhead from the TD loss is small, 25% on OpenVLA and 15% on _π_ 0-FAST. 

### **G.5. quantitative results of RNN-TDQC with top 10 probabilities** 

We visualize rollout trajectories together with the failure scores predicted by TDQC on OpenVLA LIBERO-10 benchmark. Figure 6 illustrates both failure and success cases. The green-shaded areas show the functional CP band. Once failure scores exceed the band, a failure flag is raised. Figure 6a shows an example of the flag not being raised during a successful rollout, whereas Figure 6b shows that the failure flag is triggered once the policy becomes stuck. Our quantitative analysis further indicates All methods reliably detect failure modes in which the policy gets stuck or oscillates with slow back-and-forth motions. For RNN methods, once the robot successfully grasps an object, the failure score drops, suggesting that the model recognizes this as a ’good’ action. 

Figure 7 shows a successful rollout with an informative failure score. The failure score rises when the policy becomes 

23 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

_Table 14._ Computational cost of all failure prediction methods trained on OpenVLA LIBERO-10 benchmark. We report reserved and peak GPU VRAM (MB), number of trainable parameters (M), total training wall-clock time (s), and per-epoch time (s), averaged over five seeds. TD-0 loss adds _∼_ 25% overhead relative to BCE for a given architecture. 

|**run**<br>**~~n~~ame**|**vram reserved mb**|**num params M**|**train wall clock sec**|**peak vram mb**|**epoch time sec**|
|---|---|---|---|---|---|
|MLP (features, BCE Loss)|12104_._8_±_1818_._37|1.05|30_._88_±_0_._95|9881_._54_±_784_._52|0.02|
|MLP (features, TD-0 Loss)|12074_._4_±_1819_._26|1.05|38_._31_±_0_._65|9885_._00_±_784_._35|0.02|
|RNN (features, BCE Loss)|14883_._6_±_1516_._95|4.46|108_._11_±_0_._91|12381_._49_±_783_._54|0.09|
|RNN (features, TD-0 Loss)|14900_._4_±_1517_._40|4.46|137_._83_±_0_._37|12381_._46_±_783_._42|0.12|
|RNN (top-10, BCE Loss)|13308_._38_±_887_._27|0.48|72_._67_±_0_._53|10296_._98_±_382_._87|0.06|
|RNN (top-10, TD-0 Loss)|13506_._19_±_887_._69|0.48|97_._12_±_0_._52|10496_._06_±_382_._87|0.08|


_Table 15._ Computational cost of all failure prediction methods trained on _π_ 0-FAST LIBERO-10 benchmark. Columns report reserved and peak GPU VRAM (MB), number of trainable parameters (M), total training wall-clock time (s), and per-epoch time (s), averaged over five seeds. Compared to OpenVLA (Table 14), all methods are substantially more efficient: peak VRAM stays below 3.2 GB and training completes in under 40 s. LSTM (TD-0 Loss) – same params as BCE uses the same architecture and hyperparameters as LSTM (BCE Loss), providing a controlled comparison of loss functions. TD-0 adds only _∼_ 13% to training time relative to BCE. 

|**run**<br>**~~n~~ame**|**vram reserved mb**|**num params M**|**train wall clock sec**|**peak vram mb**|**epoch time sec**|
|---|---|---|---|---|---|
|MLP (BCE Loss)|2320_._00_±_411_._44|0.52|17_._99_±_0_._56|1834_._79_±_174_._62|0.01|
|MLP (TD-0 Loss)|2366_._00_±_411_._44|0.52|20_._67_±_0_._64|1837_._03_±_174_._63|0.01|
|LSTM (BCE Loss)|4101_._60_±_533_._08|2.36|22_._31_±_0_._29|3106_._82_±_165_._88|0.01|
|LSTM (TD-0 Loss) – same params as BCE|4123_._60_±_533_._08|2.36|25_._34_±_0_._48|3128_._65_±_158_._33|0.01|
|LSTM (TD-0 Loss)|2619_._20_±_305_._89|2.36|39_._79_±_0_._82|2095_._10_±_174_._91|0.03|
|TDQC (top-10 BCE Loss)|2450_._00_±_411_._44|1.25|32_._09_±_0_._41|1868_._36_±_174_._61|0.02|
|TDQC (top-10 TD-0 Loss)|2448_._00_±_411_._44|1.25|37_._90_±_0_._33|1906_._37_±_174_._44|0.03|


temporarily stuck while trying to drop the alphabet soup into the basket around step 140. Then decreases after recovery around step 275, and increases again when the robot attempts to pick up the tomato soup at step 336, since grasping can fail. Overall, these scores are intuitive. 

Figure 8 compared BCE and TDQC-based methods. TDQC methods are more sensitive to changes in policy behavior and produce sharper, more localized responses over time. In contrast, BCE-based methods tend to vary more smoothly and exhibit less sensitivity to short-term policy changes. For MLP models, however, TD loss does not appear to improve prediction quality. 


_(a)_ Example of successful episode detected in RNN-TDQC (top-10 probabilities) 


_(b)_ Example of a failed episode detected by RNN-TDQC (top-10 probabilities) in the middle of the rollout 

_Figure 6._ Failures and successes detected by RNN-TDQC (top-10 probabilities) align with the actual robot failures, as shown in the observations from OpenVLA + LIBERO-10 simulation. The green-shaded areas show the functional CP band. Once failure scores exceed the band, a failure flag is raised. 

### **G.6. WidowX analysis** 

The high ROC-AUC results in Table 2 on WidowX are obtained with SAFE-MLP, a heuristic that uses a cumulative loss, see Sec. 6.3, which appears to work well in terms of ROC-AUC in this specific benchmark. However, its connection with calibration is unclear. Note that SAFE-MLP is not reported in Table 1 since it cannot be used as a calibration metric. Figure 1 

24 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_Figure 7._ **Successful rollout with informative failure scores of TDQC top 10 probabilities on OpenVLA LIBERO-10 benckmark.** task: “put both the alphabet soup and the tomato sauce in the basket”. The failure score rises when the policy becomes temporarily stuck while trying to drop the alphabet soup into the basket around step 140. Then, failure score decreases after recovery around step 275, and increases again when the robot is positioned himself and attempts to pick up the tomato soup at step 336. 

shows that w.r.t. a standard MLP/LSTM, the action-based predictor is competitive on WidowX. Additional video examples are provided on our project webpage. 

### **G.7. Ablation Studies** 

We ablate several ways of incorporating temporal-difference learning when training a success predictor on OpenVLA in the LIBERO-10 benchmark. Specifically, we compare: 

- **TD-0:** one-step bootstrapping with a standard MSE objective on the predicted success probability. 

- **TD-** _λ_ **:** multi-step bootstrapping using eligibility traces, which interpolates between TD-0 and Monte-Carlo targets via the trace parameter _λ_ . 

- **Categorical TD-0:** a distributional variant where the scalar success target is represented as a categorical vector and trained via Binary cross-entropy loss, following the setup of (Farebrother et al., 2024). 

For TD- _λ_ , we evaluate two trace values, _λ ∈{_ 0 _._ 5 _,_ 0 _._ 8 _}_ , to study the effect of shorter versus longer credit assignment on sequential calibration. 


_(a)_ Brier scores evaluated at the minimal task time for all ablation methods. We see here that TD-0 with top 10 probabilities achieves the lowest Brier score 


_(b)_ ROC-AUC scores evaluated at the minimal task time for all ablation methods. We see here that TD-0 with top 10 probabilities achieves the highest ROC-AUC with the lowest variance 

_Figure 9._ **Ablation results for TD methods** Overall, we see that TD-0 with the top 10 probabilities achieve best performance 

25 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_(a)_ Example of failure score of a successful episode detected in SAFE-RNN-BCE (features). This is the same rollout as in Figure 7. 


_(c)_ Top-10 probabilities over time for RNN-BCE on the same successful rollout. 


_(b)_ Example of failure score of a successful episode detected in SAFE-RNN-TDQC (features). This is the same rollout as in Figure 7. 


_(d)_ Top-10 probabilities over time for RNN-TDQC on the same successful rollout. 

_Figure 8._ Comparison between BCE and TD-based methods for the same rollout as in Figure 7. The top row shows the failure scores on features, while the bottom row shows the failure score on top-10 probabilities over time. 

_Table 16._ Performance degregation as a function of failed trajectories, evaluated on _π_ 0-FAST LIBERO-10 (unseen tasks). We vary the proportion of failed trajectories retained during training from 100% down to 10%. Performance degrades gracefully until 30% but drops more sharply at 10%, suggesting the method is robust to moderate class imbalance. 

|**Failed traj. %**|**Brier score**_↓_|**ROC-AUC**_↑_|
|---|---|---|
|100%|0_._097_±_0_._033|82_._94_±_10_._7|
|60%|0_._101_±_0_._040|79_._52_±_12_._8|
|30%|0_._100_±_0_._045|76_._99_±_16_._6|
|10%|0_._135_±_0_._065|59_._49_±_16_._7|


### **G.8. Sensitivity of the Early Stopping** 

Figure 10 reports an extended analysis of TPR and FPR across significance levels, averaged over 21 seeds. A steep ascent in the TPR curve indicates that even tight thresholds successfully catch most failures, reflecting confidently high failure scores. TD-based methods consistently outperform BCE-trained predictors in this regard. Since CP bands are calibrated on _successful rollouts_ (negative examples only), the FPR is lower-bounded by the i.i.d. assumption, represented by _Y_ = _X_ line in the plot. Deviations from this line reflect distribution shift between calibration and test tasks: a small shift produces results close to _Y_ = _X_ , while a larger shift, as seen in LIBERO, moves the curve further away. Notably, even under larger distributional shift, probability-based methods generalize better than feature-based methods. 

### **G.9. Degradation with fewer failed trajectories** 

We evaluated LSTM-TD0 on _π_ 0-FAST LIBERO-10 with 100%, 60%, 30%, and 10% osf failed trajectories retained during training. Results on unseen tasks are shown in Table 3 in the attached link. The analysis shows that performance degrades gracefully until 30% and more sharply at 10%, suggesting robustness to moderate class imbalance. 

### **G.10. ROC-AUC vs Brier Score extended evaluation** 

We add experimental results across six benchmarks of the relationship between uncertainty calibration and ROC-AUC in several VLA models. Figures 11a through 11f illustrate a critical relationship in the evaluation of VLA models: the link between a model’s **uncertainty calibration** and its **predictive performance** . All six scatter plots demonstrate a consistent 

26 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_Figure 10._ **Additional failure detection analysis using thresholds obtained by functional CP.** These plots show TPR (True positive rate, left column), and FPR (False positive rate, right column), w.r.t. the significance level _α_ , for each evaluation benchmark. These plots are averaged across 21 seeds. 

27 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 

and strong negative correlation, with Spearman’s _ρ_ ranging from _−_ 0 _._ 648 to a peak of _−_ 0 _._ 881 for OpenVLA on WidowX. This indicates that as the Brier Score at Stop Time ( _T_<sup>ˆ</sup> ) increases (representing higher calibration error), the ROC-AUC significantly decreases. 

The Brier Score measures the accuracy of probabilistic predictions. These results confirm that **well-calibrated models** (lower Brier scores) are substantially more capable of distinguishing between successful and failing states, resulting in a higher ROC-AUC. 

The lower correlation in UniVLA suggests that its internal uncertainty estimates are less reliable predictors of task success compared to the _π_ 0 family and OpenVLA. In Figure 11c, UniVLA data points are more dispersed around the fit line, indicating that a low Brier score does not guarantee high ROC-AUC as consistently as it does for other models. 


_Figure 11._ **Analysis of VLA Calibration and Success Rates.** (a-f) Scatter plots showing the strong negative correlation between Brier Score at Stop Time ( _T_<sup>ˆ</sup> ) and ROC-AUC across different model-benchmark pairs. 

### **G.11. Relation between sequential Brier and ECE** 

Let us be reminded that the Brier score relates to the calibration and accuracy of the classifier by its two-component decomposition. Let _F_ = _f_ ( _X_ ) denote the random event that the model predicts a particular value, and let _η_ ( _F_ ) = P( _Y_ = 1 _| F_ ) _,_ the success probability conditioned on the prediction. The Brier score can be decomposed as 


The first term relates to _calibration_ : the discrepancy between the predicted success probabilities and the true conditional event frequencies. The second term in the Brier score decomposition relates to accuracy, and measures how informative the score is about the label. 

In order to prove this decomposition, we compared between the sequential Brier scores and ECE scores of all models and benchmarks, across 5 time quantiles (0.0, 0.2, 0.4, 0.6, 0.8) in Figure 16. Figures 12 to 15 shows the Sequential Brier score and ECE for seen and unseen sets respectively for different quantile times. In Figure 16 we report Spearman _ρ_ which measures monotonic relationship between variables, uses rank ordering rather than actual values and ranges between 

28 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_Figure 12._ **Brier scores val-seen** sequential Brier score (lower is better) on the _seen_ validation set averaged over 21 random seeds and all environments. We report Brier score in different _time quantiles_ , where each subplot corresponds to a (model-benchmark) pair. For _π_ 0, action probabilities are not directly interpretable, hence probability-based TDQC variants are not reported. Across all settings, our TD-based methods consistently outperform conventional predictors trained with binary cross entropy (BCE). For _π_ 0 action probabilities are not directly interpretable, hence probability-based TDQC variants are not reported. The dotted horizontal line represents the Brier score of a constant predictor that consistently outputs the empirical mean success rate computed over the seen tasks. 

_ρ ∈_ [ _−_ 1 _,_ 1]. In OpenVLA and _π_ 0 we see a strong monotonic relation between ECE and Brier scores where the red dashed line is the linear fitting on the points. We also note that _π_ 0-FAST model does not show a strong relationship between the two metrics, which indicates that this model is less interpretable, and that the sequential Brier score affected more on the ROC-AUC component rather then the calibration component. 

29 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_Figure 13._ **Brier scores val-unseen** sequential Brier score (lower is better) on the _unseen_ validation set averaged over 21 random seeds. We report Brier score in different _time quantiles_ , where each subplot corresponds to a (model-benchmark) pair. For _π_ 0, action probabilities are not directly interpretable, hence probability-based TDQC variants are not reported. Across all settings, our TD-based methods consistently outperform conventional predictors trained with binary cross entropy (BCE). For _π_ 0 action probabilities are not directly interpretable, hence probability-based TDQC variants are not reported. The dotted horizontal line represents the Brier score of a constant predictor that consistently outputs the empirical mean success rate computed over the seen tasks. 


_Figure 14._ **ECE scores val-seen** ECE scores (lower is better) on the _seen_ validation set averaged over 21 random seeds and all environments. We report ECE scores in different _time quantiles_ , where each subplot corresponds to a (model-benchmark) pair. We see the correlation between lower Brier score and lower ECE scores in almost all settings. This highlights the Brier score decomposition shown in Section 2.1 


_Figure 15._ **ECE scores val-unseen** ECE scores (lower is better) on the _unseen_ validation set averaged over 21 random seeds and all environments. We report ECE scores in different _time quantiles_ , where each subplot corresponds to a (model-benchmark) pair. We see the correlation between lower Brier score and lower ECE scores in almost all settings. This highlights the Brier score decomposition shown in Section 2.1 

30 

**Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models** 


_Figure 16._ **ECE vs Brier scores** We compared ECE scores to sequential Brier scores in all models and benchmarks. 

31 

