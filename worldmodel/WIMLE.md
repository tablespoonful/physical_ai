---
title: "WIMLE: Uncertainty-Aware World Models with IMLE for Sample-Efficient Continuous Control"
date: "2026-02-15"
authors: "Mehran Aghabozorgi; Alireza Moazeni; Yanshu Zhang; Ke Li"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2602.14351
pdf: https://arxiv.org/pdf/2602.14351
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.14351)** / [論文ページ](https://arxiv.org/abs/2602.14351)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# WIMLE: UNCERTAINTY-AWARE WORLD MODELS WITH IMLE FOR SAMPLE-EFFICIENT CONTINUOUS CONTROL 

**Mehran Aghabozorgi, Alireza Moazeni, Yanshu Zhang, Ke Li** Apex Lab, School of Computing Science Simon Fraser University _{_ mehran ~~a~~ ghabozorgi,sam62,yanshu ~~z~~ hang,keli _}_ @sfu.ca 

## ABSTRACT 

Model-based reinforcement learning promises strong sample efficiency but often underperforms in practice due to compounding model error, unimodal world models that average over multi-modal dynamics, and overconfident predictions that bias learning. We introduce WIMLE, a model-based method that extends Implicit Maximum Likelihood Estimation (IMLE) to the model-based RL framework to learn stochastic, multi-modal world models without iterative sampling and to estimate predictive uncertainty via ensembles and latent sampling. During training, WIMLE weights each synthetic transition by its predicted confidence, preserving useful model rollouts while attenuating bias from uncertain predictions and enabling stable learning. Across 40 continuous-control tasks spanning DeepMind Control, MyoSuite, and HumanoidBench, WIMLE achieves superior sample efficiency and competitive or better asymptotic performance than strong model-free and model-based baselines. Notably, on the challenging Humanoidrun task, WIMLE improves sample efficiency by over 50% relative to the strongest competitor, and on HumanoidBench it solves 8 of 14 tasks (versus 4 for BRO and 5 for SimbaV2). These results highlight the value of IMLE-based multi-modality and uncertainty-aware weighting for stable model-based RL. 

## 1 INTRODUCTION 


Figure 1: Sample efficiency on challenging tasks from each benchmark suite. WIMLE achieves superior sample efficiency and asymptotic performance over strong model-free and model-based baselines. Y-axes show interquartile mean. Shaded areas indicate 95% confidence intervals. 

Reinforcement learning has become a powerful framework for solving complex decision-making problems across diverse domains such as autonomous control (Kiumarsi et al., 2018), strategic game playing (Hosu & Rebedea, 2016), and natural language processing (Lambert, 2025; Cetina et al., 2021). However, a significant challenge in RL is the need for a substantial number of interactions with the environment to learn a good policy. Without a simulator, learning requires real-world trials, which are costly, slow, and risky (Chen et al., 2022; Weng et al., 2023; Hessel et al., 2018; Schulman et al., 2017b). 

Model-based RL (MBRL) methods aim to address this sample efficiency issue by first learning a parametric world model from collected environment interactions, then leveraging this learned 

1 

Published as a conference paper at ICLR 2026 

model to reduce real environment samples and accelerate policy learning (Hafner et al., 2020; 2021; 2023; Ye et al., 2021; Laskin et al., 2020). Common uses of the learned world model include (1) generating synthetic rollouts that augment training data for policy learning (Janner et al., 2019; Ha & Schmidhuber, 2018; Hafner et al., 2020; Clavera et al., 2020) and (2) planning by simulating future trajectories to guide action selection (Zhu et al., 2023; Frauenknecht et al., 2025; Janner et al., 2019; Lowrey et al., 2019; Hafner et al., 2019; Argenson & Dulac-Arnold, 2021). In this work, we focus on the former. 

Historically, MBRL has struggled to surpass strong model-free baselines, largely because compounding rollout errors bias training and mislead the policy (Janner et al., 2019; Xiao et al., 2019; Talvitie, 2017; Frauenknecht et al., 2025; Venkatraman et al., 2015; Asadi et al., 2018b;a). We attribute this to two key issues: (1) standard predictive models struggle when the same state–action pair yields different, conflicting supervision due to partial observability, contact-rich dynamics, or inherent stochasticity (Kurutach et al., 2018); and (2) a lack of uncertainty awareness in model predictions (Frauenknecht et al., 2025), which leads to overconfidence in regions with complex dynamics or limited data. Despite attempts to address these issues (Janner et al., 2019; Zhu et al., 2023; Frauenknecht et al., 2025; Somalwar et al., 2025; Hansen et al., 2022), MBRL methods have yet to consistently outperform strong model-free baselines in practice (Nauman et al., 2024; Lee et al., 2025b). 

To address these issues, we propose WIMLE ( **W** orld models with **IMLE** )—an uncertainty-aware model-based RL approach. We integrate IMLE (Li & Malik, 2018), a mode-covering generative model with demonstrated success in low-data regimes (Aghabozorgi et al., 2023; Vashist et al., 2024), into the MBRL framework. This allows us to learn world models that handle different, conflicting supervision and from which we extract predictive uncertainty estimates. We incorporate these uncertainty estimates into the RL objective to prevent overconfident predictions from biasing learning. To the best of our knowledge, this is the first work to extend IMLE for uncertainty-aware world models in MBRL. 

We evaluate WIMLE on 40 tasks across DMC, HumanoidBench, and MyoSuite. WIMLE delivers considerable gains in sample efficiency and asymptotic performance over strong model-free and model-based baselines. Notably, on the notoriously challenging Humanoid-run task, WIMLE improves the sample efficiency of the most competitive method by over 50%. On HumanoidBench, WIMLE successfully solves 8 of 14 tasks, compared to 4 for BRO and 5 for SimbaV2 (Figure 10). Across suites, Figure 1 shows one example task per benchmark, each showing more than 50% sample-efficiency improvement for WIMLE over the strongest competing method. 

## 2 PRELIMINARIES 

### 2.1 RL 

We consider an infinite-horizon discounted Markov decision process (MDP) ( _S, A, P, r, γ_ ) (Bellman, 1957) with initial state distribution _ρ_ 0. At time _t_ , the agent observes _st ∈S_ , selects _at ∼ πϕ_ ( _a | st_ ), receives reward _rt_ = _r_ ( _st, at_ ), and the environment transitions as _st_ +1 _∼ P_ ( _· | st, at_ ). The objective is to learn a policy that maximizes the expected discounted return 


In the continuous-control settings considered here, states and actions are real-valued. The discount factor satisfies _γ ∈_ (0 _,_ 1). We denote the action-value function under policy _π_ by _Q_<sup>_π_</sup> ( _s, a_ ): 


### 2.2 MODEL-BASED RL 

In model-based RL, we learn a parametric world model with parameters _θ_ that approximates the unknown environment transition dynamics _P_ ( _st_ +1 _, rt | st, at_ ) through a learned conditional distribution 


2 

Published as a conference paper at ICLR 2026 

trained from limited environment interactions. A model rollout (prediction) of horizon _H_ under a policy _πϕ_ from _s_ 0 is the sequence _τ_ ˆ = ( _s_ 0 _, a_ 0 _, r_ 0 _, s_ 1 _, . . . , sH_ ) generated by 


Such rollouts are commonly used for planning or to provide synthetic transitions for RL training (Janner et al., 2019; Zhu et al., 2023). 

### 2.3 IMPLICIT MAXIMUM LIKELIHOOD ESTIMATION 

Implicit Maximum Likelihood Estimation (IMLE) learns a latent-variable generator _gθ_ ( _z_ ) that maps noise _z ∼N_ (0 _, I_ ) to data space. Given data _{xi}_<sup>_N_</sup> _i_ =1<sup>, the IMLE objective is:</sup> 


In practice, given current parameters _θ_ , we realize this objective by drawing a pool of candidate latents _{zj}_<sup>_m_</sup> _j_ =1<sup>i.i.d.from</sup><sup>_N_(0</sup><sup>_, I_) per data point and selecting the nearest generated sample;this</sup> step is gradient-free and fully parallelizable, 


and minimizing the resulting empirical loss using stochastic gradient descent. 


Optimizing Eq. equation 5 yields maximum likelihood estimation (MLE) of _θ_ and ensures mode coverage (Aghabozorgi et al., 2023): each data point is represented by at least one generated sample. In practice, IMLE is sample efficient and effective for modeling multi-modal distributions. Conditional IMLE _gθ_ ( _c, z_ ) models multi-modal conditional distributions; we adopt this form in WIMLE. For a more detailed discussion of IMLE, we refer readers to (Li & Malik, 2018; Aghabozorgi et al., 2023). 

## 3 WIMLE 

WIMLE addresses the key limitations of traditional MBRL through three main components: (1) IMLE-trained stochastic world models that capture complex multi-modal transition dynamics, (2) predictive uncertainty estimation that reflects the model’s confidence in its predictions, and (3) uncertainty-weighted learning that scales the influence of synthetic data based on model confidence. We detail each component below. 

### 3.1 IMLE WORLD MODEL 

Recent MBRL approaches span autoregressive sequence models, latent-variable generators, diffusion models, and planning-centric objectives (Ha & Schmidhuber, 2018; Hafner et al., 2019; 2020; 2021; Robine et al., 2023; Micheli et al., 2023; Zhang et al., 2023; Hansen et al., 2024; Huang et al., 2024). Diffusion models are effective but rely on iterative sampling, which limits their usage in the online RL setting where rollout throughput is critical (Huang et al., 2024; Karras et al., 2022). Despite progress, these methods often require substantial data and still struggle to consistently surpass strong model-free baselines (Nauman et al., 2024; Lee et al., 2025b). Moreover, simple and sample-efficient unimodal Gaussian world models underfit inherently multi-modal, complex dynamics in partially observable or contact-rich settings, exacerbating model bias and compounding errors (Janner et al., 2019; Zhu et al., 2023). 

On the other hand, we leverage IMLE to learn transitions, a one-step generative method that—unlike diffusion models—avoids iterative sampling and enables fast online rollouts. In practice, IMLE yields strong rollout throughput; Figure 2 reports wall-clock time among model-based methods. We represent the world model as a conditional stochastic generator _gθ_ that maps a state–action pair and latent noise to the next outcome: 


3 

Published as a conference paper at ICLR 2026 


Figure 2: Wall-clock comparison among model-based methods (3 seeds) on a single NVIDIA L40S GPU for the humanoid-run task. Y-axis shows interquartile mean; shaded areas indicate 95% confidence intervals. 

Here, the latent variable _z_ induces a distribution over next outcomes for the same state–action pair, capturing inherent stochasticity and multi-modality in the dynamics. 

**IMLE Training Procedure.** Given a dataset of transitions _{_ ( _st, at, rt, st_ +1) _}_<sup>_N_</sup> _i_ =1<sup>, we form targets</sup> _yi_ = [ _rt, st_ +1] and train _gθ_ using the IMLE objective. The training proceeds in two alternating steps: _Assignment Step:_ For each data point _yi_ , we sample _m_ candidate latents _{zj}_<sup>_m_</sup> _j_ =1<sup>andassignthe</sup> nearest candidate that minimizes the prediction error: 


This assignment step is computationally efficient as it requires no gradient computation, is fully parallelizable across data points, and typically uses small values of _m_ (e.g., 5-10) in conditional IMLE settings. 

_Update Step:_ We then perform gradient descent on the empirical loss using the assigned latents: 


where _B_ is a minibatch of indices and _η >_ 0 is the learning rate. 

This procedure ensures _mode coverage_ by matching each data point to at least one generated sample, avoiding collapse to a single mean prediction. In contrast, a standard Gaussian regression model trained with least squares (Janner et al., 2019) predicts the conditional mean; in multi-modal settings this falls between modes and produces averaged, often implausible next states—known as regression to the mean (Galton, 1886; Barnett et al., 2005)—that compound over rollouts. IMLE’s per-sample latent assignment avoids this averaging and yields sharper, mode-consistent predictions (Aghabozorgi et al., 2023; Vashist et al., 2024). 

**Inference and Rollouts.** After training, we generate rollouts following the procedure described in Section 2.2. Multi-step rollouts of horizon _H_ are generated by initializing from a real state _s_ 0 and iteratively applying: _at ∼ πϕ_ ( _·|st_ ), _zt ∼N_ (0 _, I_ ), ( _st_ +1 _, rt_ ) = _gθ_ ( _st, at, zt_ ) for _t_ = 0 _, . . . , H −_ 1. 

### 3.2 UNCERTAINTY ESTIMATION 

Reliable uncertainty estimation is crucial for deciding when to trust model predictions. We therefore compute a predictive uncertainty for each synthetic transition and use it to reweight the RL objective. Each transition’s contribution is scaled by its estimated confidence. This preserves useful rollouts and reduces bias from uncertain predictions without changing the underlying algorithm. Alternative integrations exist. For example, Infoprop (Frauenknecht et al., 2025) computes an information-theoretic corruption measure and uses it to truncate rollouts during generation. In contrast, we integrate uncertainty directly into the learning objective via confidence weights. 

We use a single predictive uncertainty measure _σ_ ( _s, a_ ) that reflects the model’s confidence in its next-step prediction. Concretely, we maintain an ensemble of _K_ IMLE world models (see Section 3.6.1) and, for each model, draw _m_ latent samples, yielding predictions: 


We define _σ_ ( _s, a_ ) as the standard deviation across these predictions—a direct measure of model agreement (see Algorithm 1, lines 13–14): 


4 

Published as a conference paper at ICLR 2026 

In practice, we compute per-dimension standard deviations for the predicted reward and next state and average them to obtain a single scalar for the transition. _σ_ ( _s, a_ ) decreases when models agree and increases when predictive uncertainty is high (e.g., limited data or complex dynamics). By the law of total variance we can decompose _σ_<sup>2</sup> ( _s, a_ ) into epistemic and aleatoric components, 


Following recent insights on uncertainty from Smith et al. (2024), this total predictive variance is the Bayes risk of acting under a squared-error loss. 

### 3.3 UNCERTAINTY-WEIGHTED LEARNING 

Having defined a single predictive uncertainty _σ_ ( _s, a_ ), we now describe how it enters learning. The key idea is simple: weight each synthetic transition by the model’s confidence so reliable predictions contribute more and uncertain ones less. Because uncertainty typically grows with rollout horizon due to error accumulation, later steps in the rollout receive smaller weights, naturally down-weighting distant, noisier predictions. 

To choose these weights, we invoke a standard heteroscedastic regression result (formalized in Section 3.4): when estimating a scalar quantity from independent noisy observations with different noise variances, the unique minimum-variance linear unbiased estimator weights each observation inversely to its variance. We use this principle as guidance and map each predictive variance _σ_ ( _s, a_ ) to a bounded, inverse-variance weight 


which preserves the inverse-variance ordering and keeps _w ∈_ (0 _,_ 1], avoiding exploding gradients. 

During rollout generation, we compute per-transition weights _wi_ = _w_ ( _si, ai_ ) for each synthetic transition ( _si, ai, ri, s_<sup>_′_</sup> _i_<sup>)usingthepredictiveuncertaintydefinedabove.Weincorporatetheseweights</sup> into the RL objective by modifying the temporal difference (TD) loss: 


where _δi_ = _ri_ + _γQϕ_ ( _si_ +1 _, ai_ +1) _− Qϕ_ ( _si, ai_ ) is the TD error for transition _i_ , with _ai_ +1 _∼ πϕ_ ( _· | si_ +1), _Qϕ_ is a parameterized Q-function, and _wi_ is the corresponding uncertainty weight. For real environment data, we simply use _wi_ = 1. 

This approach lets us leverage synthetic rollouts while keeping TD updates well-conditioned: highvariance, uncertain transitions have a smaller impact on the stochastic gradients, while the Bellman fixed point remains unchanged, so we tame noisy (including purely stochastic) updates without discarding or biasing them. 

### 3.4 THEORETICAL ANALYSIS 

To make the effect of our weighting more concrete, we provide a theoretical analysis of its properties. First, we establish that multiplying each squared Bellman error ( _y − Q_ ( _s, a_ ))<sup>2</sup> by a positive weight _w_ ( _s, a_ ) preserves the Bellman fixed point. Second, in a tractable setting where the critic is linear in a feature representation, we demonstrate that choosing weights inversely proportional to the (total) target noise variance minimizes the variance of the learned parameters, thereby improving convergence rate and sample efficiency. The lemmas below formalize these results: the first shows that any strictly positive reweighting leaves the Bellman target _Q_<sup>_⋆_</sup> unchanged, and the second shows that, in the linear-critic regime, inverse-variance weighting _wi ∝_ 1 _/σi_<sup>2yieldstheminimum-covariance</sup> linear unbiased estimator. Full proofs are provided in Appendix B. 

**Lemma (Positive weights preserve the Bellman target).** Let _y_ = _r_ + _γV_ ( _s_<sup>_′_</sup> ) denote the one-step Bellman target for a value function _V_ with conditional mean _µ_ ( _s, a_ ) = E[ _y | s, a_ ]. Given a strictly positive weight function _w_ ( _s, a_ ) _>_ 0, the corresponding population weighted Bellman squared loss is 

_Lw_ ( _Q_ ) = E( _s,a_ ) _∼dπ_ E( _r,s′_ ) _∼P_ ( _·|s,a_ )� _w_ ( _s, a_ ) ( _y − Q_ ( _s, a_ ))<sup>2�</sup> _._ (16) Then the unique minimizer of _Lw_ ( _Q_ ) over all action-value functions _Q_ is _Q_<sup>_⋆_</sup> ( _s, a_ ) = _µ_ ( _s, a_ ) for all ( _s, a_ ), i.e., any strictly positive reweighting leaves the Bellman fixed point unchanged and only re-emphasizes different regions of ( _s, a_ ). A full proof is given in Appendix B. 

5 

Published as a conference paper at ICLR 2026 

**Lemma (Linear critics, inverse-variance weighting).** Consider the setting where (1) the actionvalue function is linear in some feature representation _ϕ_ ( _s, a_ ) _∈_ R<sup>_d_</sup> , i.e., _Qθ_ ( _s, a_ ) = _ϕ_ ( _s, a_ )<sup>_⊤_</sup> _θ_ for parameters _θ ∈_ R<sup>_d_</sup> , and (2) for a batch of _m_ transitions _xi_ = ( _si, ai_ ) the TD targets satisfy _yi_ = _µ_ ( _xi_ ) + _εi_ with E[ _εi | xi_ ] = 0, Var( _εi | xi_ ) = _σi_<sup>2, and independent noise terms</sup><sup>_εi_.Among</sup> all linear unbiased estimators of _θ_ , the inverse-variance choice _wi ∝_ 1 _/σi_<sup>2yieldstheminimum</sup> covariance matrix for _θ_<sup>ˆ</sup> . A proof follows the classical Gauss–Markov theorem and is provided in Appendix B. _Proof sketch._ Stacking targets into a vector _y_ and features into a design matrix Φ, minimizing � _i_<sup>_wi_(</sup><sup>_yi−Qθ_(</sup><sup>_xi_))2yieldstheweightedleast-squaresestimator</sup><sup>_θ_ˆ</sup><sup>_w_=(Φ</sup><sup>_⊤W_Φ)</sup><sup>_−_1Φ</sup><sup>_⊤Wy_with</sup> _W_ = diag( _wi_ ). Choosing _W_ proportional to the inverse noise covariance Σ<sup>_−_1</sup> = diag(1 _/σi_<sup>2)</sup> yields an estimator whose covariance Cov( _θ_<sup>ˆ</sup> _w_ ) is minimal among all linear unbiased estimators by the Gauss–Markov theorem. We refer to Appendix B for a full derivation. 

**Implications for WIMLE.** Here _σi_<sup>2is the total predictive variance at (</sup><sup>_si, ai_), which can include</sup> both epistemic and aleatoric components (Eq. 13). The lemma above shows that, in the linear-critic regime, weighting each transition inversely to this total variance minimizes the covariance of the learned parameters, independently of the source of the noise. Lower parameter variance means fewer samples are needed to reach a given accuracy, i.e., inverse-variance weighting is provably more sample-efficient in this regime. Combined with the Bellman fixed-point lemma above (proved in Appendix B), this means our choice of _w_ ( _s, a_ ) shrinks update variance without ever changing the Bellman solution—even in the limit of a perfect world model where all uncertainty (and thus down-weighted noise) is purely aleatoric. 

### 3.5 ALGORITHM 

Algorithm 1 presents the overall WIMLE procedure. For a more complete implementation of the algorithm, including training frequencies and hyperparameters, see Algorithm 3 in Appendix A. 

**Algorithm 1** WIMLE: World Models with Implicit Maximum Likelihood Estimation 

- 1: **Input:** Rollout horizon _H_ , ensemble size _K_ , number of rollouts _M_ , number of latent codes _m_ 2: _{_ Red text indicates steps that fundamentally differ from MBPO. _}_ 3: initialize ensemble world models _{gθk }_<sup>_K_</sup> _k_ =1<sup>, environment and model datasets</sup><sup>_D_env,</sup><sup>_D_model</sup> 

- 4: **for** environment steps **do** 

- 5: Collect environment transitions using _πϕ_ ; add to _D_ env 

- 6: **// IMLE World Model Training** 

- 7: Train ensemble _{gθk }_<sup>_K_</sup> _k_ =1<sup>in parallel on bootstrap samples of</sup><sup>_D_env using IMLE (Eqs. 9, 10)</sup> 8: **for** _M_ model rollouts **do** 

- 9: Sample starting state _s_ 0 from _D_ env 

- 10: **for** _t_ = 0 to _H −_ 1 **do** 

- 11: _at ∼ πϕ_ ( _·|st_ ) 12: Sample _m_ latents _{zj}_<sup>_m_</sup> _j_ =1<sup>_∼N_(0</sup><sup>_, I_)</sup> 13: Generate predictions _{_ (˜ _st_ +1 _,_ ˜ _rt_ ) _k,j}_<sup>_K,m_</sup> _k_ =1 _,j_ =1<sup>=</sup><sup>_{gθ_</sup> _k_<sup>(</sup><sup>_st, at, zj_)</sup><sup>_}K,m_</sup> _k_ =1 _,j_ =1<sup>from all ensem-</sup> ble members 

- 14: Compute predictive uncertainty: _σt_ = std _k,j_ � _gθk_ ( _st, at, zj_ )� _{_ aggregated over ensembles and latents _}_ 

- 15: Set weight _wt_ = 1 _/_ ( _σt_ + 1) 

- 16: Add weighted transition ( _st, at, rt, st_ +1 _, wt_ ) to _D_ model 

- 17: **// Uncertainty-Weighted Policy Learning** 

- 18: Sample batch from _D_ env _∪D_ model (real data has _w_ = 1) 

- 19: Update policy using weighted RL objective: 

- 20: _L_ = E( _s,a,r,s′,w_ ) _∼_ batch[ _w · ℓ_ RL( _s, a, r, s_<sup>_′_</sup> )] 

The algorithm maintains the underlying RL method as a black box through the weighted loss function _L_ , where _ℓ_ RL represents any standard RL objective (e.g., TD error for critics, policy gradient for actors). The key insight is that uncertainty weights _wt_ automatically scale the contribution of each 

6 

Published as a conference paper at ICLR 2026 


Figure 3: WIMLE world model architecture. 

synthetic transition—high-confidence predictions receive higher weights while uncertain predictions contribute proportionally less. 

### 3.6 DESIGN CHOICES 

### 3.6.1 TRAINING 

**Model Rollouts.** We experiment with synthetic rollouts using horizons up to _H_ = 8. All rollouts are initialized from real environment states sampled uniformly from the environment dataset _D_ env, following standard practice in model-based RL to ensure rollouts start from the data distribution. We select task-specific rollout horizons through empirical experimentation as described in Appendix D.1. 

**RL Training.** We use Soft Actor-Critic (SAC) (Haarnoja et al., 2018) with distributional Q-learning (Bellemare et al., 2017) as our underlying RL algorithm. Following recent work that has demonstrated the effectiveness of distributional RL for continuous control (Nauman et al., 2024; Lee et al., 2025b; Dabney et al., 2018a), we specifically adapt quantile Q-learning (Dabney et al., 2018b; Nauman et al., 2024). 

**Ensemble Training.** We train an ensemble of _K_ = 7 IMLE world models in parallel to improve predictive uncertainty estimation and calibration (Section 3.3). Each ensemble member is initialized with different random parameters and trained on bootstrap samples of the environment data. The parallel training of ensemble members is computationally efficient and scales well with available compute resources, enabling reliable predictive uncertainty without significant computational overhead. 

### 3.6.2 ARCHITECTURE 

Figure 3 illustrates the WIMLE world model architecture. The network takes as input state _st_ , action _at_ , and latent variable _z_ , followed by a dense layer that maps to a 512-dimensional hidden representation. The core of the architecture consists of three residual blocks, each containing dense layers with ReLU activations and L2 normalization. Following recent findings by Lee et al. (2025b), we employ L2 normalization within the residual blocks, which has been shown to improve stability and performance in RL settings. The network outputs separate predictions for rewards and next states through dedicated dense heads. 

## 4 EXPERIMENTS 

We evaluate WIMLE across diverse continuous-control benchmarks—DeepMind Control Suite (including Dog and Humanoid), MyoSuite, and HumanoidBench (Tassa et al., 2018; Caggiano et al., 2022; Sferrazza et al., 2024). Across 40 tasks spanning locomotion and dexterous manipulation with high-dimensional state/action spaces and sparse rewards, we compare against strong modelfree and model-based methods, including MR.Q, PPO, SAC, Simba, SimbaV2, BRO, TD-MPC2, and DreamerV3 (Fujimoto et al., 2025; Schulman et al., 2017a; Haarnoja et al., 2018; Lee et al., 2025a;b; Nauman et al., 2024; Hansen et al., 2024; Hafner et al., 2023), and present per-benchmark results. Through our experiments, we aim to answer: (i) How does WIMLE compare to strong model-free and model-based methods? (ii) How does IMLE-based multi-modality in the world model affect results compared to standard unimodal Gaussian models? (iii) How do uncertainty estimates evolve during training, and how do they affect performance? 

7 

Published as a conference paper at ICLR 2026 

### 4.1 EXPERIMENTAL SETUP 

All experiments are run for 1M environment steps with 10 random seeds unless otherwise specified. We report the interquartile mean (IQM) and 95% confidence intervals computed with RLiable (Agarwal et al., 2021), using stratified bootstrap across tasks and seeds. Following BRO and SimbaV2 (Nauman et al., 2024; Lee et al., 2025b), we aggregate normalized scores per BRO/SimbaV2 protocol (DMC [0,1], MyoSuite success, HumanoidBench success-normalized). Where official baseline results are available, we report the authors’ numbers; otherwise, we run public implementations with their recommended settings. We provide full details about the experimental setup, hyperparameters, and baselines in Section D and E of the appendix. 

### 4.2 COMPARISON TO BASELINES 


Figure 4: Aggregate results across benchmarks. WIMLE outperforms strong model-free and modelbased baselines overall. Gains are most pronounced on the challenging Dog & Humanoid subset, where it achieves superior sample efficiency and asymptotic performance. On MyoSuite, it performs asymptotically on par with strong baselines that are already near the maximum score (1.0), and on HumanoidBench it significantly outperforms the baselines, solving 8 _/_ 14 tasks versus BRO 4 and SimbaV2 5. Y-axes show interquartile mean; shaded areas denote 95% confidence intervals. 

We summarize aggregate performance across benchmarks in Figure 4 and provide detailed per-task results in Section C of the appendix. WIMLE consistently leads among strong model-free and model-based methods on Dog & Humanoid, the full DMC suite, and HumanoidBench, while performing asymptotically on par with strong MyoSuite baselines that are already close to the maximum score (1.0). Notably, gains are largest on the high-dimensional and challenging Dog & Humanoid tasks (Dog: _|S|_ =223, _|A|_ =38; Humanoid: _|S|_ =67, _|A|_ =24). On HumanoidBench, WIMLE significantly outperforms baselines, solving 8 of 14 tasks versus BRO 4 and SimbaV2 5 (Figure 10). We summarize performance across timesteps in Section E.1, where WIMLE performs best or competitively across most evaluations. We attribute these improvements to IMLE-driven multi-modality in the world model and uncertainty-weighted learning that scales the influence of synthetic rollouts by model confidence, mitigating bias from overconfident predictions while preserving useful signal, which we discuss in more detail in the next section. Per-task performance is reported in Figures 7, 8, 9 and 10. 

### 4.3 METHOD ANALYSIS 

We analyze how uncertainty-aware weighting and multi-modal dynamics modeling impact performance and how predictive uncertainty evolves during training. 

**Effect of uncertainty-aware weighting** Figure 5 (Left) compares WIMLE with uncertaintyaware weighting to an unweighted variant that is _identical in every respect except that all pertransition weights are fixed to wi_ =1 _._ 0. The unweighted curve lags and can even underperform a strong model-free baseline early on, indicating that ignoring predictive uncertainty significantly biases learning and hinders performance. Figure 5 (Right) studies rollout sensitivity. Increasing the model rollout horizon from _H_ =1 to _H_ =4 to _H_ =6 improves performance, and extending to _H_ =8 maintains performance rather than showing the severe degradation typically observed in modelbased methods when increasing rollout length (Janner et al., 2019). This improved stability at longer horizons demonstrates that uncertainty-aware weighting reduces the model bias typically introduced by longer horizon errors, enabling us to leverage longer synthetic rollouts without considerable performance degradation. 

**Impact of IMLE-based multi-modality** Figure 6 (Left) contrasts WIMLE (IMLE world model) with an otherwise identical unimodal Gaussian world model (MBPO-style; (Janner et al., 2019)), 

8 

Published as a conference paper at ICLR 2026 

with both variants using uncertainty-aware weighting. The IMLE variant significantly outperforms the Gaussian, underscoring the value of modeling multi-modal transition dynamics for uncertainty estimation in complex, contact-rich control. Figure 6 (Right) shows how weights evolve. During a brief warm-up with limited environment samples and training, both models are uncalibrated and weights can appear transiently high; as data accumulates and the estimators calibrate, weights drop to reflect high uncertainty and low confidence. As training progresses and more data are collected, IMLE’s weights increase to reflect higher confidence in the predictions, whereas the Gaussian’s remain relatively flat, indicating limited calibration. Together, these results show that multi-modal modeling improves both performance and the quality of uncertainty estimates, reducing the risk of overconfident, biased predictions misleading the policy. 


Figure 5: Uncertainty-aware weighting reduces model bias and enables stable training at longer horizons on Humanoid-run. **Left:** Uncertainty-aware WIMLE compared to an unweighted variant that is identical except all per-transition weights are fixed to _wi_ = 1 _._ 0 and a model-free variant that is identical except that it does not use the model; the unweighted curve lags and can even underperform the model-free variant early on, indicating that ignoring uncertainty will bias learning and hinder performance. **Right:** Rollout ablation ( _H_ = 1 _,_ 4 _,_ 6 _,_ 8) for WIMLE: increasing the model rollout horizon from _H_ =1 to _H_ =4 to _H_ =6 improves performance, and extending to _H_ =8 does not substantially degrade performance, suggesting that uncertainty-aware weighting mitigates harm from error accumulation at longer horizons. All variants use the same SAC backbone and distributional critics; only the ablated components differ. All plots are on DMC’s Humanoid-run task with 5 seeds. 


Figure 6: Multi-modality strengthens model-based learning. **Left:** WIMLE (IMLE world model) versus an otherwise identical unimodal Gaussian world model (MBPO-style; (Janner et al., 2019); both use uncertainty-aware weighting): the IMLE variant significantly outperforms the Gaussian, highlighting the value of multi-modal modeling and IMLE’s efficacy. **Right:** Weight dynamics: After a brief warm-up phase, IMLE’s weights are lower when uncertainty is high and increase as training progresses and more data are collected, reflecting growing model confidence; the unimodal Gaussian fails to capture this evolution, yielding relatively flat weights over time. All plots are on Humanoid-run. 

## 5 RELATED WORK 

**Model-free RL.** Foundational model-free methods such as PPO (Schulman et al., 2017a) and SAC (Haarnoja et al., 2018) remain strong references for continuous control. Recent advances focus on scaling and regularization: BRO (Nauman et al., 2024) scales critic networks to 5M parameters with strong regularization and optimistic exploration, achieving state-of-the-art performance. Simba (Lee et al., 2025a) introduces an architecture that embeds simplicity bias through running statistics normalization, residual feedforward blocks, and layer normalization, enabling effective parameter 

9 

Published as a conference paper at ICLR 2026 

scaling; SimbaV2 (Lee et al., 2025b) further constrains feature and weight norms via hyperspherical normalization. Contemporary work like MR.Q (Fujimoto et al., 2025) explores improved value estimation for better sample efficiency. Collectively, these methods provide strong model-free baselines. 

**Model-based RL.** Model-based RL methods learn world models to improve sample efficiency via synthetic rollouts and planning. DreamerV3 (Hafner et al., 2023) learns a latent world model and achieves strong performance in continuous control with large-scale training. MBPO (Janner et al., 2019) uses short model-generated rollouts branched from real data to avoid model exploitation while maintaining sample efficiency. TD-MPC2 (Hansen et al., 2024) learns implicit world models through joint-embedding prediction and performs local trajectory optimization in latent space for scalable multi-task learning. STORM (Zhang et al., 2023) combines Transformer-based sequence modeling with categorical VAEs for efficient world model learning in visual domains. Diffusionbased world models generate trajectories via iterative denoising and incur high inference cost, which hinders online RL (Janner et al., 2022; Ajay et al., 2023; He et al., 2023). Despite these algorithmic advances, model-based methods have struggled to consistently surpass recent model-free approaches like BRO (Nauman et al., 2024) and SimbaV2 (Lee et al., 2025b). 

**Model Bias.** Model bias and error accumulation remain fundamental challenges in MBRL. Trajectory models (Asadi et al., 2019; Lambert et al., 2021) address the compounding-error problem by learning multi-step models that directly predict outcomes of action sequences, avoiding the accumulation of one-step prediction errors. Self-correcting models (Talvitie, 2017) train models to correct themselves when producing errors. Infoprop (Frauenknecht et al., 2025) integrates uncertainty by truncating rollouts using information-theoretic corruption measures, but is not competitive on complex, high-dimensional tasks such as Humanoid-run (see Figure 1). In contrast, we estimate a single predictive uncertainty and weight each synthetic transition accordingly, integrating this directly into the learning objective to preserve useful synthetic data while reducing the influence of uncertain predictions. This yields state-of-the-art results on challenging tasks (Figures 1 and 4). 

**Implicit Maximum Likelihood Estimation.** IMLE (Li & Malik, 2018) trains implicit generative models by minimizing the expected distance from each data point to its nearest generated sample, avoiding mode-collapse and GAN (Goodfellow et al., 2014) training issues. Adaptive IMLE (Aghabozorgi et al., 2023) extends this with adaptive thresholding and curriculum learning for better few-shot performance. These methods demonstrate that likelihood-based objectives can achieve good sample quality without adversarial training on low-data settings. 

## 6 LIMITATIONS AND FUTURE WORK 

WIMLE uses world models solely to generate synthetic rollouts. Other uses, such as planning with the model or integrating the model into policy-gradient formulations, remain unexplored here. Future work should evaluate WIMLE in these settings. Our experiments use proprioceptive state observations only. Extending WIMLE to image-based control is an important direction, especially since IMLE has been shown to be effective in few-shot image synthesis (Aghabozorgi et al., 2023; Vashist et al., 2024). Finally, similar to MBPO (Janner et al., 2019) and POMP (Zhu et al., 2023), the rollout horizon is a task-dependent hyperparameter. Learning to adapt the horizon online based on model confidence is a promising avenue for future research. 

## 7 CONCLUSION 

WIMLE advances model-based reinforcement learning by extending IMLE to learn stochastic, multi-modal world models and by weighting synthetic data with predictive confidence. This reduces model bias and stabilizes learning while retaining the benefits of synthetic rollouts. Across 40 continuous-control tasks in DMC, MyoSuite, and HumanoidBench, WIMLE achieves superior sample efficiency and competitive or higher asymptotic performance than strong model-free and model-based baselines. Gains are largest on challenging Dog and Humanoid locomotion tasks. On HumanoidBench, WIMLE significantly outperforms baselines and solves 8 of 14 tasks. The approach integrates cleanly with standard RL objectives and scales with compute through ensembles and parallel latent sampling. We hope these results renew interest in practical world models for challenging continuous control. 

10 

Published as a conference paper at ICLR 2026 

### ACKNOWLEDGMENTS 

We are grateful to James A. Peltier for his support on the computing infrastructure that made this work possible. 

## REFERENCES 

- Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron C Courville, and Marc Bellemare. Deep reinforcement learning at the edge of the statistical precipice. _Advances in neural information processing systems_ , 34:29304–29320, 2021. 

- Mehran Aghabozorgi, Shichong Peng, and Ke Li. Adaptive IMLE for few-shot pretraining-free generative modelling. In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett (eds.), _International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 248–264. PMLR, 2023. URL https://proceedings.mlr.press/v202/ aghabozorgi23a.html. 

- Anurag Ajay, Yilun Du, Abhi Gupta, Joshua Tenenbaum, Tommi Jaakkola, and Pulkit Agrawal. Is conditional generative modeling all you need for decision-making? _International Conference on Learning Representations_ , 2023. 

- Arthur Argenson and Gabriel Dulac-Arnold. Model-based offline planning. _ArXiv_ , abs/2008.05556, 2021. 

- Kavosh Asadi, Evan Cater, Dipendra Misra, and Michael L. Littman. Towards a Simple Approach to Multi-step Model-based Reinforcement Learning. _arXiv_ , 2018a. 

- Kavosh Asadi, Dipendra Misra, and Michael L. Littman. Lipschitz Continuity in Model-based Reinforcement Learning. _arXiv_ , 2018b. 

- Kavosh Asadi, Dipendra Misra, Seungchan Kim, and Michel L. Littman. Combating the Compounding-Error Problem with a Multi-step Model. _arXiv_ , 2019. 

- Adrian G Barnett, Jolieke C Van Der Pols, and Annette J Dobson. Regression to the mean: what it is and how to deal with it. _International journal of epidemiology_ , 34(1):215–220, 2005. 

- Marc G. Bellemare, Will Dabney, and R´emi Munos. A distributional perspective on reinforcement learning. In Doina Precup and Yee Whye Teh (eds.), _Proceedings of the 34th International Conference on Machine Learning, ICML 2017, Sydney, NSW, Australia, 6-11 August 2017_ , volume 70 of _Proceedings of Machine Learning Research_ , pp. 449–458. PMLR, 2017. URL http://proceedings.mlr.press/v70/bellemare17a.html. 

- Richard Bellman. A markovian decision process. _Indiana Univ. Math. J._ , 6:679–684, 1957. ISSN 0022-2518. 

- Vittorio Caggiano, Huawei Wang, Guillaume Durandau, Massimo Sartori, and Vikash Kumar. Myosuite: A contact-rich simulation suite for musculoskeletal motor control. In Roya Firoozi, Negar Mehr, Esen Yel, Rika Antonova, Jeannette Bohg, Mac Schwager, and Mykel J. Kochenderfer (eds.), _Learning for Dynamics and Control Conference, L4DC 2022, 23-24 June 2022, Stanford University, Stanford, CA, USA_ , volume 168 of _Proceedings of Machine Learning Research_ , pp. 492–507. PMLR, 2022. URL https://proceedings.mlr.press/v168/ caggiano22a.html. 

- V´ıctor Uc Cetina, Nicol´as Navarro-Guerrero, Ana Mart´ın-Gonz´alez, Cornelius Weber, and Stefan Wermter. Survey on reinforcement learning for language processing. _Artificial Intelligence Review_ , 56:1543–1575, 2021. URL https://api.semanticscholar.org/CorpusID: 233210638. 

- Jie Chen, Jian Sun, and Gang Wang. From unmanned systems to autonomous intelligent systems. _Engineering_ , 12:16–19, 2022. 

11 

Published as a conference paper at ICLR 2026 

- Ignasi Clavera, Yao Fu, and P. Abbeel. Model-augmented actor-critic: Backpropagating through paths. _ArXiv_ , abs/2005.08068, 2020. 

- Will Dabney, Georg Ostrovski, David Silver, and R´emi Munos. Implicit quantile networks for distributional reinforcement learning, 2018a. URL https://arxiv.org/abs/1806.06923. 

- Will Dabney, Mark Rowland, Marc G. Bellemare, and R´emi Munos. Distributional reinforcement learning with quantile regression. In Sheila A. McIlraith and Kilian Q. Weinberger (eds.), _Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence, (AAAI-18), the 30th innovative Applications of Artificial Intelligence (IAAI-18), and the 8th AAAI Symposium on Educational Advances in Artificial Intelligence (EAAI-18), New Orleans, Louisiana, USA, February 2-7, 2018_ , pp. 2892–2901. AAAI Press, 2018b. doi: 10.1609/AAAI.V32I1.11791. URL https://doi.org/10.1609/aaai.v32i1.11791. 

- Bernd Frauenknecht, Devdutt Subhasish, Friedrich Solowjow, and Sebastian Trimpe. On rollouts in model-based reinforcement learning. In _The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025_ . OpenReview.net, 2025. URL https://openreview.net/forum?id=Uh5GRmLlvt. 

- Scott Fujimoto, Pierluca D’Oro, Amy Zhang, Yuandong Tian, and Michael Rabbat. Towards general-purpose model-free reinforcement learning. _arXiv preprint arXiv:2501.16142_ , 2025. 

- Francis Galton. Regression towards mediocrity in hereditary stature. _The Journal of the Anthropological Institute of Great Britain and Ireland_ , 15:246–263, 1886. 

- Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial networks, 2014. URL https: //arxiv.org/abs/1406.2661. 

- David Ha and J¨urgen Schmidhuber. Recurrent world models facilitate policy evolution. In _Advances in Neural Information Processing Systems 31_ , pp. 2451–2463. Curran Associates, Inc., 2018. 

- Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In Jennifer G. Dy and Andreas Krause (eds.), _Proceedings of the 35th International Conference on Machine Learning, ICML 2018, Stockholmsm¨assan, Stockholm, Sweden, July 10-15, 2018_ , volume 80 of _Proceedings of Machine Learning Research_ , pp. 1856–1865. PMLR, 2018. URL http://proceedings. mlr.press/v80/haarnoja18b.html. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International Conference on Machine Learning_ , pp. 2555–2565, 2019. 

- Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2020. URL https://openreview.net/forum?id=S1lOTC4tDS. 

- Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2021. URL https://openreview.net/forum?id=0oabwyZbOu. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. Temporal difference learning for model predictive control. In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesv´ari, Gang Niu, and Sivan Sabato (eds.), _International Conference on Machine Learning, ICML 2022, 17-23 July 2022, Baltimore, Maryland, USA_ , volume 162 of _Proceedings of Machine Learning Research_ , pp. 8387–8406. PMLR, 2022. URL https://proceedings.mlr.press/v162/ hansen22a.html. 

12 

Published as a conference paper at ICLR 2026 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-MPC2: scalable, robust world models for continuous control. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . OpenReview.net, 2024. URL https://openreview. net/forum?id=Oxh5CstDJU. 

- Haoran He, Chenjia Bai, Kang Xu, Zhuoran Yang, Weinan Zhang, Dong Wang, Bin Zhao, and Xuelong Li. Diffusion model is an effective planner and data synthesizer for multi-task reinforcement learning. _Advances in Neural Information Processing Systems_ , 2023. 

- Matteo Hessel, Joseph Modayil, Hado Van Hasselt, Tom Schaul, Georg Ostrovski, Will Dabney, Dan Horgan, Bilal Piot, Mohammad Azar, and David Silver. Rainbow: Combining improvements in deep reinforcement learning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 32, 2018. 

- Ionel-Alexandru Hosu and Traian Rebedea. Playing atari games with deep reinforcement learning and human checkpoint replay. _CoRR_ , abs/1607.05077, 2016. URL http://arxiv.org/ abs/1607.05077. 

- Renming Huang, Yunqiang Pei, Guoqing Wang, Yangming Zhang, Yang Yang, Peng Wang, and Hengtao Shen. Diffusion models as optimizers for efficient planning in offline rl, 2024. URL https://arxiv.org/abs/2407.16142. 

- Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. In Hanna M. Wallach, Hugo Larochelle, Alina Beygelzimer, Florence d’Alch´e-Buc, Emily B. Fox, and Roman Garnett (eds.), _Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada_ , pp. 12498–12509, 2019. URL https://proceedings.neurips.cc/paper/2019/ hash/5faf461eff3099671ad63c6f3f094f7f-Abstract.html. 

- Michael Janner, Yilun Du, Joshua B Tenenbaum, and Sergey Levine. Planning with diffusion for flexible behavior synthesis. _International Conference on Machine Learning_ , 2022. 

- Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diffusionbased generative models, 2022. URL https://arxiv.org/abs/2206.00364. 

- Bahare Kiumarsi, Kyriakos G. Vamvoudakis, Hamidreza Modares, and Frank L. Lewis. Optimal and autonomous control using reinforcement learning: A survey. _IEEE Transactions on Neural Networks and Learning Systems_ , 29:2042–2062, 2018. URL https://api. semanticscholar.org/CorpusID:21709652. 

- Thanard Kurutach, Ignasi Clavera, Yan Duan, Aviv Tamar, and Pieter Abbeel. Model-ensemble trust-region policy optimization. In _6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings_ . OpenReview.net, 2018. URL https://openreview.net/forum?id=SJJinbWRZ. 

- Nathan Lambert. Reinforcement learning from human feedback, 2025. URL https://arxiv. org/abs/2504.12501. 

- Nathan O. Lambert, Albert Wilcox, Howard Zhang, Kristofer S. J. Pister, and Roberto Calandra. Learning Accurate Long-term Dynamics for Model-based Reinforcement Learning. _IEEE Conf on Decision and Control_ , 2021. 

- Michael Laskin, Aravind Srinivas, and Pieter Abbeel. Curl: Contrastive unsupervised representations for reinforcement learning. In _International Conference on Machine Learning_ , pp. 5639– 5650. PMLR, 2020. 

- Hojoon Lee, Dongyoon Hwang, Donghu Kim, Hyunseung Kim, Jun Jet Tai, Kaushik Subramanian, Peter R. Wurman, Jaegul Choo, Peter Stone, and Takuma Seno. Simba: Simplicity bias for scaling up parameters in deep reinforcement learning. In _The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025_ . OpenReview.net, 2025a. URL https://openreview.net/forum?id=jXLiDKsuDo. 

13 

Published as a conference paper at ICLR 2026 

- Hojoon Lee, Youngdo Lee, Takuma Seno, Donghu Kim, Peter Stone, and Jaegul Choo. Hyperspherical normalization for scalable deep reinforcement learning. _CoRR_ , abs/2502.15280, 2025b. doi: 10.48550/ARXIV.2502.15280. URL https://doi.org/10.48550/arXiv.2502. 15280. 

- Ke Li and Jitendra Malik. Implicit maximum likelihood estimation. _CoRR_ , abs/1809.09087, 2018. URL http://arxiv.org/abs/1809.09087. 

- Kendall Lowrey, Aravind Rajeswaran, Sham M. Kakade, Emanuel Todorov, and Igor Mordatch. Plan online, learn offline: Efficient learning and exploration via model-based control. _ArXiv_ , abs/1811.01848, 2019. 

- Vincent Micheli, Eloi Alonso, and Franc¸ois Fleuret. Transformers are sample-efficient world models. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. URL https://openreview.net/ forum?id=vhFu1Acb0xb. 

- Michal Nauman, Mateusz Ostaszewski, Krzysztof Jankowski, Piotr Milos, and Marek Cygan. Bigger, regularized, optimistic: scaling for compute and sample efficient continuous control. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang (eds.), _Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024_ , 2024. URL http://papers.nips.cc/paper_files/paper/2024/hash/ cd3b5d2ed967e906af24b33d6a356cac-Abstract-Conference.html. 

- Jan Robine, Marc H¨oftmann, Tobias Uelwer, and Stefan Harmeling. Transformer-based world models are happy with 100k interactions. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. URL https://openreview.net/forum?id=TdBaDGCpjly. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017a. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017b. 

- Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. In Dana Kulic, Gentiane Venture, Kostas E. Bekris, and Enrique Coronado (eds.), _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. doi: 10.15607/RSS.2024.XX.061. URL https://doi.org/10.15607/RSS.2024.XX.061. 

- Freddie Bickford Smith, Jannik Kossen, Eleanor Trollope, Mark van der Wilk, Adam Foster, and Tom Rainforth. Rethinking aleatoric and epistemic uncertainty. _CoRR_ , abs/2412.20892, 2024. doi: 10.48550/ARXIV.2412.20892. URL https://doi.org/10.48550/arXiv.2412. 20892. 

- Anne Somalwar, Bruce D. Lee, George J. Pappas, and Nikolai Matni. Learning with imperfect models: When multi-step prediction mitigates compounding error. _CoRR_ , abs/2504.01766, 2025. doi: 10.48550/ARXIV.2504.01766. URL https://doi.org/10.48550/arXiv.2504. 01766. 

- Erik Talvitie. Self-correcting models for model-based reinforcement learning. In Satinder Singh and Shaul Markovitch (eds.), _Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence, February 4-9, 2017, San Francisco, California, USA_ , pp. 2597–2603. AAAI Press, 2017. doi: 10.1609/AAAI.V31I1.10850. URL https://doi.org/10.1609/aaai.v31i1. 10850. 

- Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, Timothy P. Lillicrap, and Martin A. Riedmiller. Deepmind control suite. _CoRR_ , abs/1801.00690, 2018. URL http: //arxiv.org/abs/1801.00690. 

14 

Published as a conference paper at ICLR 2026 

- Chirag Vashist, Shichong Peng, and Ke Li. Rejection sampling IMLE: designing priors for better few-shot image synthesis. In Ales Leonardis, Elisa Ricci, Stefan Roth, Olga Russakovsky, Torsten Sattler, and G¨ul Varol (eds.), _Computer Vision - ECCV 2024 - 18th European Conference, Milan, Italy, September 29-October 4, 2024, Proceedings, Part XXI_ , volume 15079 of _Lecture Notes in Computer Science_ , pp. 441–456. Springer, 2024. doi: 10.1007/978-3-031-72664-4 _\_ ~~2~~ 5. URL https://doi.org/10.1007/978-3-031-72664-4_25. 

- Arun Venkatraman, Martial Hebert, and J.. Bagnell. Improving Multi-Step Prediction of Learned Time Series Models. _AAAI_ , 2015. 

- Boxi Weng, Jian Sun, Gao Huang, Fang Deng, Gang Wang, and Jie Chen. Competitive metalearning. _IEEE/CAA Journal of Automatica Sinica_ , 10(9):1902–1904, 2023. 

- Chenjun Xiao, Yifan Wu, Chen Ma, Dale Schuurmans, and Martin M¨uller. Learning to combat compounding-error in model-based reinforcement learning. _CoRR_ , abs/1912.11206, 2019. URL http://arxiv.org/abs/1912.11206. 

- Weirui Ye, Shaohuai Liu, Thanard Kurutach, Pieter Abbeel, and Yang Gao. Mastering atari games with limited data. _Advances in Neural Information Processing Systems_ , 34:25476–25488, 2021. 

- Weipu Zhang, Gang Wang, Jian Sun, Yetian Yuan, and Gao Huang. STORM: efficient stochastic transformer based world models for reinforcement learning. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine (eds.), _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. URL http://papers.nips.cc/paper_files/paper/2023/hash/ 5647763d4245b23e6a1cb0a8947b38c9-Abstract-Conference.html. 

- Jinhua Zhu, Yue Wang, Lijun Wu, Tao Qin, Wengang Zhou, Tie-Yan Liu, and Houqiang Li. Making better decision by directly planning in continuous control. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. URL https://openreview.net/forum?id=r8Mu7idxyF. 

15 

Published as a conference paper at ICLR 2026 

## AUTHOR STATEMENT: USE OF LANGUAGE MODELS 

We used large language models to help polish writing and improve clarity. All ideas, methods, experiments, and analyses were created and verified by the authors. Any suggested text was reviewed and edited by the authors for accuracy and originality. 

## A ALGORITHM DETAILS 

Algorithm 3 provides the detailed implementation of WIMLE, including training frequencies, batch sizes, and other practical considerations omitted from the main algorithm for clarity. The IMLE training procedure is detailed in Algorithm 2. Hyperparameters are provided in Section D. 

### **Algorithm 2** IMLE World Model Training 

- 1: **Input:** Environment dataset _D_ env, ensemble _{gθk }_<sup>_K_</sup> _k_ =1<sup>,numberoflatentcodes</sup><sup>_m_,numberof</sup> updates _U_ , learning rate _η_ 

- 2: **for** _u_ = 1 to _U_ **do** 

- 3: Sample minibatch _{_ ( _si, ai, ri, si_ +1) _}i∈B_ with replacement from _D_ env 

- 4: Form targets _yi_ = [ _ri, si_ +1] for all _i ∈ B_ 

- 5: **// Assignment Step (Eq. 9)** 

- 6: Sample _m_ candidate latents _{zj}_<sup>_m_</sup> _j_ =1<sup>_∼N_(0</sup><sup>_, I_)</sup> 

- 7: **for** _k_ = 1 to _K_ in parallel **do** 8: _zi,k_<sup>_⋆_= arg min1</sup><sup>_≤j≤m ∥gθ_</sup> _k_<sup>(</sup><sup>_si, ai, zj_)</sup><sup>_−yi∥_2 for all</sup><sup>_i ∈B_</sup> 

- 9: **// Update Step (Eq. 10)** 

- 10: **for** _k_ = 1 to _K_ in parallel **do** 11: _θk ← θk − η∇θk |B_ <u>1</u> _|_ <u>�</u> _i∈B_<sup>_∥gθ_</sup> _k_<sup>(</sup><sup>_si, ai, z_</sup> _i,k_<sup>_⋆_)</sup><sup>_−yi∥_2</sup> 

### **Algorithm 3** WIMLE: Detailed Implementation 

- 1: **Input:** Rollout horizon _H_ , ensemble size _K_ = 7, batch size _B_ , model training frequency train ~~f~~ req, number of latent codes _m_ , number of model updates _U_ 

- 2: Initialize policy _πϕ_ , ensemble of IMLE world models _{gθk }k_<sup>_K_</sup> =1<sup>,environmentdataset</sup><sup>_D_env,</sup> model dataset _D_ model 

- 3: **for** environment steps **do** 

- 4: Collect environment transition using _πϕ_ ; add to _D_ env 

- 5: **if** step mod train ~~f~~ req = 0 **then** 

- 6: **// IMLE World Model Training** 7: Train ensemble _{gθk }_<sup>_K_</sup> _k_ =1<sup>in parallel using Algorithm 2</sup> 

- 8: **// Uncertainty-Aware Rollout Generation** 

- 9: Clear _D_ model 

- 10: Sample batch of starting states _{s_<sup>(</sup> 0<sup>_i_)</sup><sup>_}_</sup> _i_<sup>_B_</sup> =1<sup>with replacement from</sup><sup>_D_env</sup> 

- 11: **for** _t_ = 0 to _H −_ 1 **do** 12: _a_<sup>(</sup> _t_<sup>_i_)</sup> _∼ πϕ_ ( _·|st_<sup>(</sup><sup>_i_)) for all</sup><sup>_i ∈{_1</sup><sup>_, . . . , B}_</sup> 13: Sample _m_ latents _{zj}_<sup>_m_</sup> _j_ =1<sup>_∼N_(0</sup><sup>_, I_)</sup> 14: Generate predictions _{gθk_ ( _st_<sup>(</sup><sup>_i_)</sup><sup>_, a_(</sup> _t_<sup>_i_)</sup><sup>_, zj_)</sup><sup>_}K,m_</sup> _k_ =1 _,j_ =1<sup>from all ensemble members for all</sup><sup>_i_</sup> 15: Compute predictive uncertainty: _σt_<sup>(</sup><sup>_i_)</sup> = std _k,j_ � _gθk_ ( _st_<sup>(</sup><sup>_i_)</sup><sup>_, a_(</sup> _t_<sup>_i_)</sup><sup>_, zj_)</sup> � _{_ aggregated over ensembles and latents _}_ 

- 16: Set weight _wt_<sup>(</sup><sup>_i_)</sup> = 1 _/_ ( _σt_<sup>(</sup><sup>_i_)</sup> + 1) 17: Select transitions ( _s_<sup>(</sup> _t_ +1<sup>_i_)</sup><sup>_, r_</sup> _t_<sup>(</sup><sup>_i_)) from predictions</sup> 18: Add weighted transitions _{_ ( _s_<sup>(</sup> _t_<sup>_i_)</sup><sup>_, a_(</sup> _t_<sup>_i_)</sup><sup>_, r_</sup> _t_<sup>(</sup><sup>_i_)</sup><sup>_, s_(</sup> _t_ +1<sup>_i_)</sup><sup>_, w_</sup> _t_<sup>(</sup><sup>_i_))</sup><sup>_}B_</sup> _i_ =1<sup>to</sup><sup>_D_model</sup> 

- 19: **// Uncertainty-Weighted Policy Learning** 

- 20: Sample batch from _D_ env _∪D_ model (real data has _w_ = 1) 

- 21: Update policy using weighted RL objective: 

- 22: _L_ = E( _s,a,r,s′,w_ ) _∼_ batch[ _w · ℓ_ RL( _s, a, r, s_<sup>_′_</sup> )] 

16 

Published as a conference paper at ICLR 2026 

B THEORETICAL ANALYSIS OF RISK-WEIGHTED BELLMAN ESTIMATION 

**Bellman fixed point under positive reweighting.** Fix a policy _π_ and a target value function _V_ . Recall the one-step Bellman target 


with conditional mean 


Given a strictly positive weight function _w_ : _S × A →_ (0 _, ∞_ ), the corresponding population weighted Bellman regression loss for an arbitrary action-value function _Q_ is 


**Lemma (Weights do not change the Bellman target).** Assume that _w_ ( _s, a_ ) _>_ 0 for all ( _s, a_ ) in the support of _d_<sup>_π_</sup> . Then the unique minimizer of _Lw_ ( _Q_ ) over all action-value functions _Q_ : _S ×A →_ R is 


which is the same minimizer as for the unweighted objective (obtained by setting _w ≡_ 1). _Proof._ Fix ( _s, a_ ) and consider the conditional risk as a function of a scalar _q ∈_ R: 


Since _w_ ( _s, a_ ) is a strictly positive constant with respect to the inner expectation, it does not affect the minimizer in _q_ . The derivative of the unweighted term with respect to _q_ is 


which vanishes if and only if _q_ = _µ_ ( _s, a_ ). Thus, for each fixed ( _s, a_ ), the unique minimizer of _ℓs,a_ ( _q_ ) is _q_ = _µ_ ( _s, a_ ), independently of the choice of _w_ ( _s, a_ ) _>_ 0. 

The global objective _Lw_ ( _Q_ ) in Eq. 19 is the expectation of _ℓs,a_ ( _Q_ ( _s, a_ )) under _d_<sup>_π_</sup> . For any actionvalue function _Q_ , we can write 


with equality if and only if _Q_ ( _s, a_ ) = _µ_ ( _s, a_ ). Integrating this inequality with respect to _d_<sup>_π_</sup> shows that _Lw_ ( _Q_ ) _≥Lw_ ( _µ_ ), with strict inequality whenever _Q_ differs from _µ_ on a set of positive _d_<sup>_π_</sup> - measure. Hence, _Q_<sup>_⋆_</sup> = _µ_ is the unique minimizer of _Lw_ , and this minimizer does not depend on the particular choice of strictly positive weights. □ 

**Proof of the linear-critic GLS lemma.** We restate the setting from the main text. Let _xi_ = ( _si, ai_ ) denote _m_ state–action pairs with feature vectors _ϕ_ ( _xi_ ) _∈_ R<sup>_d_</sup> , and let _yi_ be the corresponding onestep TD targets. Assume a linear value model 


where _θ_<sup>_⋆_</sup> _∈_ R<sup>_d_</sup> is the true parameter vector, the noise satisfies E[ _εi | xi_ ] = 0, and the conditional variances are Var( _εi | xi_ ) = _σi_<sup>2.Collect the targets into a vector</sup><sup>_y∈_R</sup><sup>_m_, the features into a design</sup> matrix Φ _∈_ R<sup>_m×d_</sup> whose _i_ -th row is _ϕ_ ( _xi_ )<sup>_⊤_</sup> , and define the noise vector _ε_ = ( _ε_ 1 _, . . . , εm_ )<sup>_⊤_</sup> . Then 


with E[ _ε_ ] = 0 and covariance 


We assume that Φ has full column rank so that all normal equations below are solvable. 

17 

Published as a conference paper at ICLR 2026 

**Linear unbiased estimators and GLS.** Consider linear estimators of _θ_<sup>_⋆_</sup> of the form 


for some matrix _A ∈_ R<sup>_d×m_</sup> . Unbiasedness for all _θ_<sup>_⋆_</sup> requires 


which is equivalent to the constraint 


Under this constraint, the covariance of _θ_<sup>ˆ</sup> is 


The generalized least-squares (GLS) estimator corresponds to the specific choice 


so that 


It is immediate that _A_ GLSΦ = _Id_ , so _θ_<sup>ˆ</sup> GLS is linear and unbiased. Its covariance is 


**Optimality of GLS.** Let _θ_<sup>˜</sup> = _Ay_ be any other linear unbiased estimator, so that _A_ Φ = _Id_ by equation 29. Define 


Then 


The covariance of _θ_<sup>˜</sup> can be expanded as 


We now show that the cross terms vanish. Using the definition of _A_ GLS, 


and similarly 


Therefore, 


where we used equation 35. Thus 


For any vector _v ∈_ R<sup>_d_</sup> , 


because Σ is positive semidefinite. Hence _C_ Σ _C_<sup>_⊤_</sup> is positive semidefinite, and we have 


with equality if and only if _C_ = 0, i.e., _A_ = _A_ GLS. This establishes that GLS has minimum covariance among all linear unbiased estimators. 

18 

Published as a conference paper at ICLR 2026 

**Connection to inverse-variance weighting.** In our setting, weighted least squares with persample weights _wi >_ 0 corresponds to minimizing 


where _W_ = diag( _w_ 1 _, . . . , wm_ ). The normal equations yield the estimator 


Choosing weights _wi ∝_ 1 _/σi_<sup>2makes</sup><sup>_W_proportional to Σ</sup><sup>_−_1, so that</sup> 


Thus inverse-variance weights _wi ∝_ 1 _/σi_<sup>2recover the GLS estimator and, by the argument above,</sup> minimize the covariance matrix among all linear unbiased estimators. □ 

## C PER-TASK RESULTS 

We present detailed per-task performance results for WIMLE and other baselines across all benchmarks. The performance on each individual task is shown in Figures 7, 8, 9, and 10. 


Figure 7: Per-task results for high-dimensional Dog & Humanoid tasks from DeepMind Control Suite. We present the IQM of rewards and 95% confidence intervals for BRO and other baselines run for 1 _M_ steps. 


Figure 8: Per-task results for DeepMind Control Suite tasks with low-dimensional state/action spaces. We present the IQM of rewards and 95% confidence intervals for WIMLE and other baselines run for 1 _M_ steps. 

19 

Published as a conference paper at ICLR 2026 


Figure 9: Per-task results for MyoSuite tasks. We present the IQM of success rate and 95% confidence intervals for WIMLE and other baselines run for 1 _M_ steps. 


Figure 10: Per-task results for HumanoidBench tasks. We present the IQM of rewards and 95% confidence intervals for WIMLE and other baselines run for 1 _M_ steps. The red dashed line indicates the success threshold for each task. 

## D HYPERPARAMETERS 

Table 1 lists the common hyperparameters used across all tasks. These parameters were selected through hyperparameter tuning based on standard practices in RL. 

Based on our empirical evaluations, we found that increasing the model batch size to the maximum extent allowed by available GPU resources while proportionally decreasing the number of model 

20 

Published as a conference paper at ICLR 2026 

Table 1: Common hyperparameters used across all tasks. 

|**Parameter**|**Value**|
|---|---|
|**SAC Parameters**||
|Batch size|128|
|Actor learning rate|3_×_10<sup>_−_4</sup>|
|Critic learning rate|3_×_10<sup>_−_4</sup>|
|Number of quantiles|100|
|Updates per step|10|
|**World Model Parameters**||
|Model learning rate|1_×_10<sup>_−_3</sup>|
|Model batch size|512|
|Model updates|100|
|Number of latent codes|4|
|Model training frequency|1000|
|Number of rollouts|200|
|Number of ensembles|7|


updates can achieve similar performance with improved training speed. When scaling the batch size in this manner, the model learning rate should be adjusted accordingly following standard Machine Learning practices. 

### D.1 ROLLOUT LENGTH SELECTION 

We select task-specific rollout horizons H through experimentation. For easier tasks where baselines already saturate near the maximum score (e.g., MyoSuite manipulation tasks), we start with short horizons (H=1-2) and increase only if performance benefits are observed, as longer horizons may still introduce slight performance degradation—though not to the extent seen in traditional MBRL methods. For harder tasks requiring longer-term planning (e.g., HumanoidBench, Dog & Humanoid), we begin with longer horizons (H=8) and decrease only if performance gains are seen empirically. However, we note that even simpler tasks may benefit from longer horizons in some cases, reflecting the task-specific nature of optimal rollout length. This selection balances the benefits of synthetic data augmentation with computational cost, as the marginal benefit of additional rollout steps diminishes beyond each task’s optimal horizon. We cap _H_ at 8 to maintain rollout throughput and because we observe diminishing returns beyond task-specific optima; Tables 6, 7, and 8 report the chosen _H_ per task. An interesting future direction would be to dynamically adjust rollout horizons based on the model’s uncertainty level, potentially allowing for adaptive rollout lengths that scale with model confidence. 

21 

Published as a conference paper at ICLR 2026 


Figure 11: Rollout length sensitivity on h1-hurdle-v0 task of HumanoidBench up to _H_ = 40. WIMLE remains stable at longer horizons without rollout scheduling. 

## E EXPERIMENT DETAILS 

This section provides detailed descriptions of the benchmark environments used in our evaluation. We explain the task suites, their characteristics, and the normalization procedures used for fair comparison across different score scales. The following subsections describe each benchmark suite with complete task lists and their state/action dimensions. 

### E.1 DETAILED RESULTS 

We present comprehensive IQM results for WIMLE and baseline methods across all benchmark suites at 100k, 200k, 500k, and 1M environment steps. The best performing method for each step count is highlighted in bold and the second best are underlined. **<u>WIMLE</u>** performs better across most evaluations. 

Table 2: IQM results for DMC suite. Best scores are highlighted in bold, second best are underlined. 

|**Method**|**100k**|**200k**|**500k**|**1M**|
|---|---|---|---|---|
|MR.Q|0.153|0.362|0.714|0.830|
|SAC|0.037|0.082|0.210|0.326|
|SimBA|0.120|0.263|0.522|0.691|
|SimBAV2|0.235|0.495|0.730|0.845|
|BRO|0.294|0.519|0.542|0.846|
|DreamerV3|0.051|0.075|0.165|0.286|
|TD-MPC2|0.152|0.374|0.566|0.696|
|**WIMLE**|**0.332**|**0.575**|**0.812**|**0.871**|


### E.2 DEEPMIND CONTROL SUITE 

DeepMind Control Suite (Tassa et al., 2018, DMC) is a standard continuous control benchmark encompassing locomotion and manipulation tasks with varying complexity. We evaluate 16 tasks from DMC, focusing on the most challenging locomotion tasks including Dog and Humanoid embodiments. All returns are normalized by dividing by 1000 to scale performance to [0,1]. The complete list of tasks with their observation and action dimensions is provided in Table 6. 

22 

Published as a conference paper at ICLR 2026 

Table 3: IQM results for Dog & Humanoid suite. Best scores are highlighted in bold, second best are underlined. 

|**Method**|**100k**|**200k**|**500k**|**1M**|
|---|---|---|---|---|
|MR.Q|0.042|0.127|0.557|0.796|
|SAC|0.007|0.008|0.043|0.069|
|SimBA|0.067|0.173|0.533|0.773|
|SimBAV2|0.082|0.200|0.601|0.808|
|BRO|0.086|0.290|0.355|0.864|
|DreamerV3|0.006|0.006|0.007|0.010|
|TD-MPC2|0.014|0.058|0.302|0.527|
|**WIMLE**|**0.140**|**0.389**|**0.803**|**0.897**|


Table 4: IQM results for MyoSuite. Best scores are highlighted in bold, second best are underlined. 

|**Method**|**100k**|**200k**|**500k**|**1M**|
|---|---|---|---|---|
|SAC|0.038|0.350|0.622|0.714|
|SimBA|0.566|0.728|0.912|0.952|
|SimBAV2|**0.724**|**0.830**|**0.956**|**0.990**|
|BRO|0.440|0.736|0.816|0.980|
|DreamerV3|0.028|0.044|0.181|0.466|
|TD-MPC2|0.088|0.394|0.688|0.775|
|**WIMLE**|0.460|0.620|0.928|0.980|


Table 5: IQM results for HumanoidBench. Best scores are highlighted in bold, second best are underlined. 

|**Method**|**100k**|**200k**|**500k**|**1M**|
|---|---|---|---|---|
|SAC|0.008|0.020|0.060|0.168|
|SimBA|0.070|0.164|0.322|0.521|
|SimBAV2|0.059|0.179|0.488|0.799|
|BRO|0.064|0.127|0.100|0.530|
|DreamerV3|0.003|0.003|0.005|0.007|
|TD-MPC2|0.023|0.064|0.382|0.734|
|**WIMLE**|**0.169**|**0.393**|**0.715**|**0.898**|


### E.3 MYOSUITE 

MyoSuite (Caggiano et al., 2022) provides high-fidelity musculoskeletal simulations for dexterous manipulation tasks. We evaluate 10 tasks including both fixed-goal and randomized-goal (hard) settings. Performance is measured using success rates, which naturally scale to [0,1]. The complete list of tasks with their observation and action dimensions is provided in Table 7. 

### E.4 HUMANOIDBENCH 

HumanoidBench (Sferrazza et al., 2024) provides locomotion tasks for the UniTree H1 humanoid robot. We evaluate 14 tasks spanning balance, locomotion, and manipulation. For fair comparison across tasks with different score scales, all HumanoidBench scores are normalized using each task’s target success score and random score following the same procedure as in (Lee et al., 2025a;b): 


The complete list of tasks with their observation and action dimensions is provided in Table 8, and the random scores and target success scores used for normalization are listed in Table 9. 

23 

Published as a conference paper at ICLR 2026 

Table 6: **DMC Tasks.** Complete list of 16 DMC tasks evaluated, with state and action dimensions and rollout lengths. 

|**Task**|**State dim**_|S|_|**Action dim**_|A|_|**H**|
|---|---|---|---|
|acrobot-swingup|6|1|8|
|cheetah-run|17|6|1|
|finger-turn<br>~~h~~ard|12|2|1|
|fish-swim|24|5|8|
|hopper-hop|15|4|1|
|pendulum-swingup|3|1|1|
|quadruped-run|78|12|2|
|reacher-hard|6|2|1|
|walker-run|24|6|1|
|humanoid-stand|67|24|2|
|humanoid-walk|67|24|6|
|humanoid-run|67|24|6|
|dog-stand|223|38|6|
|dog-walk|223|38|4|
|dog-run|223|38|6|
|dog-trot|223|38|4|


Table 7: **MyoSuite Tasks.** Complete list of 10 MyoSuite tasks evaluated, with state and action dimensions and rollout lengths. 

|**Task**|**State dim**_|S|_|**Action dim**_|A|_|**H**|
|---|---|---|---|
|myo-key-turn|93|39|6|
|myo-key-turn-hard|93|39|1|
|myo-obj-hold|91|39|4|
|myo-obj-hold-hard|91|39|1|
|myo-pen-twirl|83|39|2|
|myo-pen-twirl-hard|83|39|1|
|myo-pose|108|39|2|
|myo-pose-hard|108|39|1|
|myo-reach|115|39|4|
|myo-reach-hard|115|39|1|


Table 8: **HumanoidBench Tasks.** Complete list of 14 HumanoidBench tasks evaluated, with state and action dimensions and rollout lengths. 

|**Task**|**State dim**_|S|_|**Action dim**_|A|_|**H**|
|---|---|---|---|
|h1-balance<br>~~s~~imple-v0|64|19|6|
|h1-balance<br>~~h~~ard-v0|77|19|6|
|h1-crawl-v0|51|19|10|
|h1-hurdle-v0|51|19|10|
|h1-maze-v0|51|19|10|
|h1-pole-v0|51|19|10|
|h1-reach-v0|57|19|10|
|h1-run-v0|51|19|10|
|h1-slide-v0|51|19|10|
|h1-sit<br>~~h~~ard-v0|51|19|6|
|h1-sit<br>~~s~~imple-v0|51|19|10|
|h1-stair-v0|51|19|10|
|h1-stand-v0|51|19|10|
|h1-walk-v0|51|19|10|


24 

Published as a conference paper at ICLR 2026 

Table 9: **HumanoidBench Normalization Scores.** Random scores and target success scores used for normalization. 

|**Task**|**Random Score**|**Target Success Score**|
|---|---|---|
|h1-balance-simple|9_._391|800|
|h1-balance-hard|9_._044|800|
|h1-crawl|272_._658|700|
|h1-hurdle|2_._214|700|
|h1-maze|106_._441|1200|
|h1-pole|20_._09|700|
|h1-reach|260_._302|12000|
|h1-run|2_._02|700|
|h1-slide-v0|2_._02|700|
|h1-slide-v1|2_._02|700|
|h1-sit-hard|10_._545|800|
|h1-stair|2_._214|700|
|h1-stand|10_._545|800|
|h1-walk|2_._377|700|


## F ADDITIONAL RESULTS 

Figure 12 compares standard WIMLE (mixed real + imagined data) against an “imagined-only” variant whose critic and actor are trained exclusively on model-generated rollouts. Removing real transitions does reduce performance slightly, but the imagined-only curve remains close to the original WIMLE results, underscoring that our synthetic trajectories are strong enough to sustain competitive learning. 

Figure 14 and Table 10 illustrate the wall-clock efficiency of WIMLE. Despite the overhead of ensemble training, WIMLE’s superior sample efficiency results in a significantly lower total timeto-solution compared to baselines. 


Figure 12: Imagined-only WIMLE (no real data in critic/actor updates) achieves performance comparable to the standard configuration, highlighting the strength of the generated rollouts. 

25 

Published as a conference paper at ICLR 2026 


Figure 13: Humanoid (Mujoco) comparison against InfoProp for 4 seeds. Unlike InfoProp, which uses task-specific termination functions for synthetic rollouts, WIMLE runs with the generic setup used for our DMC experiments yet still matches or exceeds InfoProp. 

|Method|Step 3|00k|Step 5|00k|Step 1|000k|
|---|---|---|---|---|---|---|
||Time (h)|IQM|Time (h)|IQM|Time (h)|IQM|
|Infoprop|11.49|0.044|19.15|0.102|38.30|0.077|
|DreamerV3|3.90|0.001|6.50|0.001|13.00|0.001|
|TD-MPC2|3.43|0.001|5.72|0.038|11.43|0.190|
|Ours|4.74|0.168|7.91|0.345|15.81|0.561|


Table 10: Performance and time at different training milestones. 


Figure 14: Projected total wall-clock time (algorithm compute + data collection) on Humanoid-run, assuming a 5Hz control rate. WIMLE reaches asymptotic performance significantly faster than BRO (the fastest model-free baseline) because its superior sample efficiency drastically reduces the time spent collecting real-world data, outweighing its higher per-update compute cost. 

26 

