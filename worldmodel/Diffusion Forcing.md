---
title: "Diffusion Forcing: Next-token Prediction Meets Full-Sequence Diffusion"
date: "2024-07-01"
authors: "Boyuan Chen; Diego Marti Monso; Yilun Du; Max Simchowitz; Russ Tedrake; Vincent Sitzmann"
venue: "NeurIPS"
url: https://arxiv.org/abs/2407.01392
pdf: https://arxiv.org/pdf/2407.01392
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2407.01392)** / [論文ページ](https://arxiv.org/abs/2407.01392)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Diffusion Forcing: Next-token Prediction Meets Full-Sequence Diffusion** 

|**Boyuan Chen**|**Diego Mart´ı Mons´o**<sup>_∗_</sup>|**Yilun Du**|
|---|---|---|
|MIT CSAIL|Technical University of Munich|MIT CSAIL|
|`boyuanc@mit.edu`|`diego.marti@tum.de`|`yilundu@mit.edu`|
|**Max Simchowitz**|**Russ Tedrake**|**Vincent Sitzmann**|
|MIT CSAIL|MIT CSAIL|MIT CSAIL|
|`msimchow@mit.edu`|`russt@mit.edu`|`sitzmann@mit.edu`|


## **Abstract** 

This paper presents Diffusion Forcing, a new training paradigm where a diffusion model is trained to denoise a set of tokens with _independent_ per-token noise levels. We apply Diffusion Forcing to sequence generative modeling by training a causal next-token prediction model to generate one or several future tokens without fully diffusing past ones. Our approach is shown to combine the strengths of next-token prediction models, such as variable-length generation, with the strengths of full-sequence diffusion models, such as the ability to guide sampling to desirable trajectories. Our method offers a range of additional capabilities, such as (1) rolling-out sequences of continuous tokens, such as video, with lengths past the training horizon, where baselines diverge and (2) new sampling and guiding schemes that uniquely profit from Diffusion Forcing’s variable-horizon and causal architecture, and which lead to marked performance gains in decision-making and planning tasks. In addition to its empirical success, our method is proven to optimize a variational lower bound on the likelihoods of all subsequences of tokens drawn from the true joint distribution. Project website: `https://boyuan.space/ diffusion-forcing/` 

## **1 Introduction** 

Probabilistic sequence modeling plays a crucial role in diverse machine learning applications including natural language processing [6, 47], video prediction [31, 69] and decision making [3, 22]. Next-token prediction models in particular have a number of desirable properties. They enable the generation of sequences with varying length [32, 21, 37] (generating only a single token or an “infinite” number of tokens via auto-regressive sampling), can be conditioned on varying amounts of history [21, 37], support efficient tree search[70, 23, 25], and can be used for online feedback control [22, 3]. 

Current next-token prediction models are trained via _teacher forcing_ [64], where the model predicts the immediate next token based on a ground truth history of previous tokens. This results in two limitations: (1) there is no mechanism by which one can guide the sampling of a sequence to minimize a certain objective, and (2) current next-token models easily become _unstable_ on continuous data. For example, when attempting to auto-regressively generate a video (as opposed to text [6] or vector-quantized latents [33]) past the training horizon, slight errors in frame-to-frame predictions accumulate and the model diverges. 

> _∗_ Work done as a visiting student at MIT. 

38th Conference on Neural Information Processing Systems (NeurIPS 2024). 


Figure 1: **Diffusion Forcing capabilities.** Today, different applications such as language modeling [6], planning [36], or video generation [31, 69] rely on _either_ auto-regressive next-token prediction _or_ full-sequence diffusion, according to their respective unique capabilities. The proposed Diffusion Forcing is a novel sequence generative model that enjoys key strengths of both model types. 

_Full-sequence diffusion_ seemingly offers a solution. Commonly used in video generation and long-horizon planning, one directly models the joint distribution of a fixed number of tokens by diffusing their concatenation [31, 1], where the noise level is identical across all tokens. They offer _diffusion guidance_ [30, 16] to guide sampling to a desirable sequence, invaluable in decisionmaking (planning) applications [36, 34]. They further excel at generating continuous signals such as video [31]. However, full-sequence diffusion is universally parameterized via non-causal, unmasked architectures. In addition to restricting sampling to full sequences, as opposed to variable length generation, we show that this limits the possibilities for both guidance and subsequence generation (Figure 1). Further, we demonstrate that a naive attempt at combining the best of both worlds by training a next-token prediction model for full-sequence diffusion leads to poor generations, intuitively because it does not model the fact that small uncertainty in an early token necessitates high uncertainty in a later one. 

In this paper, we introduce _Diffusion Forcing_ (DF), a training and sampling paradigm where each token is associated with a _random, independent_ noise level, and where tokens can be denoised according to arbitrary, independent, per-token schedules through a shared next-or-next-few-token prediction model. Our approach is motivated by the observation that noising tokens is a form of _partial masking_ —zero noise means a token is unmasked, and complete noise fully masks out a token. Thus, DF forces the model to learn to “unmask” any collection of variably noised tokens (Figure 2). Simultaneously, by parameterizing predictions as a composition of next-token prediction models, our system can flexibly generate varying length sequences as well as compositionally generalize to new trajectories (Figure 1). 

We implement DF for sequence generation as _Causal Diffusion Forcing_ (CDF), in which future tokens depend on past ones via a causal architecture. We train the model to denoise all tokens of a sequence at once, with an independent noise level per token. During sampling, CDF gradually denoises a sequence of Gaussian noise frames into clean samples where different frames may have different noise levels at each denoising step. Like next-token prediction models, CDF can generate variable-length sequences; unlike next-token prediction, it does so stabily from the immediate next token to thousands of tokens in the future – even for continuous tokens. Moreover, like full-sequence diffusion it accepts guidance towards high-reward generations. Synergistically leveraging causality, flexible horizon, and variable noise schedules, CDF enables a new capability, Monte Carlo Guidance (MCG), that dramatically improves the sampling of high-reward generations compared to non-causal full-sequence diffusion models. Fig. 1 overviews these capabilities. 

In summary, our contributions are: (1) We propose Diffusion Forcing, a new probabilistic sequence model that has the flexibility of next-token prediction models while being able to perform longhorizon guidance like full-sequence diffusion models. (2) Taking advantage of Diffusion Forcing’s unique capabilities, we introduce a novel decision-making framework that allows us to use Diffusion Forcing as simultaneously a _policy_ ([10]) and as a _planner_ ([36]). (3) We formally prove that, under appropriate conditions, optimizing our proposed training objective maximizes a lower bound on the likelihood of the joint distribution of _all sub-sequences_ observed at training time. (4) We empirically evaluate CDF across diverse domains such as video generation, model-based planning, visual imitation learning, and time series prediction, and demonstrate CDF’s unique capabilities, 

2 


Figure 2: **Method Overview.** Diffusion Forcing trains causal sequence neural networks (such as an RNN or a masked transformer) to denoise flexible-length sequences where each frame of the sequence can have a _different_ noise level. In contrast, next-token prediction models, common in language modeling, are trained to predict a single next token from a _ground-truth_ sequence (teacher forcing [64]), and full-sequence diffusion, common in video generation, train non-causal architectures to denoise all frames in a sequence at once with the _same_ noise level. Diffusion Forcing thus _interleaves_ the time axis of the sequence and the noise axis of diffusion, unifying strengths of both alternatives and enabling completely new capabilities (see Secs. 3.2,3.4). 

such as stabilizing long-rollout autoregressive video generation, composing sub-sequences of those observed at training time with user-determined memory horizon, Monte Carlo Guidance, and more. 

## **2 Related Work and Preliminaries** 

We discuss related work and preliminaries for our core application, sequence generative modeling; see Appendix D for further literature review. 

Our method unifies two perspectives on sequence modeling: Bayesian filtering along the time axis, denoted by subscript _t_ , and diffusion along an “uncertainty” (or noise level) axis denoted by superscript _k_ . In the following, we denote observations as **x** _∈X_ and latent states as **z** _∈Z_ . 

**Bayesian Filtering.** Given a Hidden Markov Model (HMM) defined by latent states **z** _t_ and observations **x** _t_ , a Bayes filter is a probabilistic method for estimating latent states recursively over time from incoming observations. A prior model _p_ ( **z** _t_ +1 _|_ **z** _t_ ) infers a belief over the next state given only the current state, and an observation model infers a belief over the next observation given the current latent state _p_ ( **x** _t|_ **z** _t_ ). When a new observation is made, a posterior model _p_ ( **z** _t_ +1 _|_ **z** _t,_ **x** _t_ +1) provides an updated estimation of the next latent state **z** _t_ +1. When trained end-to-end with neural networks [22, 23], latent states are not an estimate of any physical quantity, but a sufficiently expressive latent that summarizes past observations for predicting future observations ( **x** _t_<sup>_′_</sup> ) _t_<sup>_′_</sup> _>t_ in the sequence. 

**Diffusion Models.** Diffusion models [56, 28] have proven to be highly expressive and reliable generative models. We review their essentials here. Let _q_ ( **x** ) denote a data distribution of interest, and let **x**<sup>0</sup> _≡_ **x** _∼ q_ . We consider a forward diffusion process that gradually adds Gaussian noise to a data point over a series of time steps. This process is modeled as a Markov chain, where the data at each step _k_ is noised incrementally: 


where _N_ is the normal distribution and _βk_ is the variance of the noise added at each step controlled by a schedule _{βk ∈_ (0 _,_ 1) _}_<sup>_K_</sup> _k_ =1<sup>.The process continues until the data is converted into pure noise at</sup> **x**<sup>_K_</sup> . The reverse process is also a Markov chain and attempts to recreate the original data from the noise with a parameterized model _pθ_ : 


where the mean **_µ_** is a model with a neural network, and where it is shown [29] that one can set the covariance to the identity scaled by a fixed constant _γk_ depending on _k_ . Adopting the standard 

3 

exposition, we reparametrize the mean **_µ_** in terms of noise prediction **_ϵ_** = (<sup>_~~√~~_</sup> 1 _− α_ ¯ _t_ )<sup>_−_1</sup> **x**<sup>_k_</sup> _t_<sup>_t−_</sup><sup>_~~√~~_</sup> _<u>α</u>_ <u>¯</u> _t_ **_<u>µ</u>_** . This leads [28] to the following least squares objective: 


where **x**<sup>_k_</sup> =<sup>_~~√~~_</sup> _<u>α</u>_ <u>¯</u> _t_ **<u>x</u>**<sup>0</sup> +<sup>_~~√~~_</sup> 1 _− α_ ¯ _tϵ_<sup>_k_</sup> and **_ϵ_**<sup>_k_</sup> _∼N_ (0 _,_ **I** ) . One can then sample from this model via Langevin dynamics **x**<sup>_k−_1</sup> _←_ _~~√~~_ <u>1</u> _<u>αk</u>_<sup>(</sup><sup>**x**</sup> _t_<sup>_k−_</sup> _~~√~~_ <u>11</u> _−−αα_ ¯ _<u>kk</u>_<sup>**_ϵ_**</sup><sup>_θ_(</sup><sup>**x**</sup> _t_<sup>_k, k_) +</sup><sup>_σk_</sup><sup>**w**)[28].</sup> 

**Guidance of Diffusion Models.** Guidance [30, 16] allows biasing diffusion generation towards desirable predictions at sampling time. We focus on classifier guidance [16]: given a classifier _c_ ( _y|_ **x**<sup>_k_</sup> ) of some desired _y_ (e.g. class or success indicator), one modifies the Langevin sampling [29] gradient **_ϵ_** _θ_ ( **x**<sup>_k_</sup> _, k_ ) to be **_ϵ_** _θ_ ( **x**<sup>_k_</sup> _, k_ ) _−_<sup>_~~√~~_</sup> 1 _− α_ ¯ _k∇xk_ log _c_ ( _y|_ **x**<sup>_k_</sup> ). This allows sampling from the joint distribution of **x** and class label _y_ without the need to train a conditional model. Other energies such as a least-squares objective comparing the model output to a desirable ground truth have been explored in applications such as decision making [16, 36]. 

**Next-Token Prediction Models.** Next-token prediction models are sequence models that predict the next frame **x** _t_ +1 given past frames **x** 1: _t_ . At training time, one feeds a neural network with **x** 1: _t_ and minimizes _||_ **x** ˆ _−_ **x** _||_<sup>2</sup> for continuous data or a cross-entropy loss for discrete data [64]. At sampling time, one samples the next frame **x** ˆ _t_ +1 following _p_ ( **x** _t_ +1 _|_ **x** 1: _t_ ). If one treats **x** ˆ _t_ +1 as **x** _t_ +1, one can use the same model to predict **x** _t_ +2 and repeat until a full sequence is sampled. Unlike full-sequence diffusion models, next-token models do not accept multi-step guidance, as prior frames must be fully determined to sample future frames. 

**Diffusion Sequence Models.** Diffusion has been widely used in sequence modeling. [43] use fullsequence diffusion models to achieve controllable text generation via guidance, such as generating text following specified parts of speech. [31] trains full-sequence diffusion models to synthesize short videos and uses a sliding window to roll out longer conditioned on previously generated frames. [36] uses full-sequence diffusion models as planners in offline reinforcement learning. This is achieved by training on a dataset of interaction trajectories with the environment and using classifier guidance at sampling time to sample trajectories with high rewards towards a chosen goal. [49] modifies auto-regressive models to denoise the next token conditioned on previous tokens. It trains with teacher forcing [64] and samples next-token auto-regressively for time series data. Most similar to our work is AR-Diffusion [65], which trains full-sequence text diffusion with a causal architecture with linearly dependent noise level along the time axis. We provide a detailed comparision between this approach and ours in Appendix D. 

## **3 Method** 

### **3.1 Noising as partial masking** 

Recall that _masking_ is the practice of occluding a subset of data, such as patches of an image [26] or timesteps in a sequence [15, 48], and training a model to recover unmasked portions. Without loss of generality, we can view any collection of tokens, sequential or not, as an ordered set indexed by _t_ . Training next-token prediction with teacher forcing can then be interpreted as masking each token **x** _t_ at time _t_ and making predictions from the past **x** 1: _t−_ 1. Restricted to sequences, we refer to all these practices as _masking along the time axis_ . We can also view full-sequence forward diffusion, i.e., gradually adding noise to the data **x**<sup>0</sup> 1: _T_<sup>_≡_</sup><sup>**x**1:</sup><sup>_T_, as a form of</sup><sup>_partial masking_, which we refer to as</sup> _masking along the noise axis_ . Indeed, after _K_ steps of noising, **x**<sup>_K_</sup> 1: _T_<sup>is (approximately) pure white</sup> noise without information about the original data. 

We establish a unified view along both axes of masking (see Fig. 2). We denote **x** 1: _T_ for a sequence of tokens, where the subscript indicates the time axis. As above, **x**<sup>_k_</sup> _t_<sup>_t_denotes</sup><sup>**x**</sup><sup>_t_at noise level</sup><sup>_kt_under</sup> the forward diffusion process (2.1); **x**<sup>0</sup> _t_<sup>=</sup><sup>**x**is the unnoised token, and</sup><sup>**x**</sup><sup>_K_</sup> _t_<sup>is white noise</sup><sup>_N_(0</sup><sup>_,_</sup><sup>**I**).</sup> Thus, ( **x**<sup>_k_</sup> _t_<sup>_t_)1</sup><sup>_≤t≤T_denotes a sequence of noisy observations where each token has a</sup><sup>_different_noise</sup> level _kt_ , which can be seen as the degree of _partial masking_ applied to each token through noising. 

### **3.2 Diffusion Forcing: different noise levels for different tokens** 

_Diffusion Forcing_ (DF) is a framework for training and sampling arbitrary sequence lengths of noisy tokens ( **x**<sup>_k_</sup> _t_<sup>_t_)1</sup><sup>_≤t≤T_, where critically,</sup><sup>_the noise level ktof each token can vary by time step_.In this</sup> 

4 

### **Algorithm 1** Diffusion Forcing Training 

**Algorithm 2** DF Sampling with Guidance 

1: **loop** 1: **Input:** Model _θ_ , scheduling matrix _K_ , initial latent 2: Sample tajectory of observations ( **x** 1 _, ...,_ **x** _T_ ). **z** 0, guidance cost _c_ ( _·_ ). 3: **for** _t_ = 1 _, ..., T_ **do** 2: **Initialize x** 1 _, . . . ,_ **x** _T ∼N_ (0 _, σK_<sup>2</sup><sup>_I_).</sup> 4: Sample independent noise level _kt ∈_ 3: **for** row _m_ = _M −_ 1 _, ...,_ 0 **do** _{_ 0 _,_ 1 _, ..., K}_ 4: **for** _t_ = 1 _, . . . , T_ **do** 5: **x**<sup>_k_</sup> _t_<sup>_t_</sup> = ForwardDiffuse( **x** _t, kt_ ) 5: **z**<sup>new</sup> _t ∼ pθ_ ( **z** _t |_ **z** _t−_ 1 _,_ **x** _t, Km_ +1 _,t_ ). 6: Define _ϵt_ = **x**<sup>_kt_</sup> _t_ _~~√~~_<sup>_−_</sup> 1<sup>_~~<u>√</u>~~_</sup> _−αα_ ¯¯ _ktkt_ **x** _t_ 6:7: _k_ **x**<sup>new</sup> _t←K←m,t_ _~~√~~_ ,1 _<u>α</u>_ **w** _k_<sup>(</sup> _∼N_<sup>**x**</sup><sup>_t −_</sup> (0 _~~√~~_ 11 _,−_ **I** _<u>−α</u>_ ) _<u>α</u>_ <u>¯</u> _<u>k</u>_ . _k_<sup>_ϵθ_(</sup><sup>**z**</sup> _t_<sup>new</sup> _,_ **x** _t, k_ ))+ 7: Update **z** _t ∼ pθ_ ( **z** _t|_ **z** _t−_ 1 _,_ **x** _t_<sup>_kt, kt_).</sup> _σk_ **w** 8: **Update z** _t ←_ **z** _t_<sup>new</sup> . 8: Set ˆ _ϵt_ = _ϵθ_ ( **z** _t−_ 1 _,_ **x** _t_<sup>_kt, kt_)</sup> 9: **end for** 9: **end for** 10: **x** 1: _H ←_ AddGuidance( **x** 1:<sup>new</sup> _H_<sup>_, ∇_</sup><sup>**x**log</sup><sup>_c_(</sup><sup>**x**</sup> 1:<sup>new</sup> _H_<sup>))</sup> 10: _L_ =MSELoss([ˆ _ϵ_ 1 _, ...,_ ˆ _ϵn_ ] _,_ [ _ϵ_ 1 _, ..., ϵn_ ]) 11: **end for** 11: Backprop with _L_ and update _θ_ 12: **Return x** 1: _T_ . 12: **end loop** 

paper, we focus on time series data, and thus instantiate Diffusion Forcing with causal architectures (where **x**<sup>_k_</sup> _t_<sup>_t_depends only on past noisy tokens), which we call</sup><sup>_Causal Diffusion Forcing_(CDF). For</sup> simplicity, we focus on a minimal implementation with a vanilla Recurrent Neural Network (RNN) [11]. Potential transformer implementation of Diffusion Forcing is also possible but we defer its discussion to Appendix C.1. 

The RNN with weights _θ_ maintains latents **z** _t_ capturing the influence of past tokens, and these evolve via dynamics **z** _t ∼ pθ_ ( **z** _t|_ **z** _t−_ 1 _,_ **x**<sup>_k_</sup> _t_<sup>_t, kt_) with a recurrent layer.When an incoming noisy observation</sup> **x**<sup>_k_</sup> _t_<sup>_t_is made, the hidden state is updated in a Markovian fashion</sup><sup>**z**</sup><sup>_t∼pθ_(</sup><sup>**z**</sup><sup>_t|_</sup><sup>**z**</sup><sup>_t−_1</sup><sup>_,_</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t, kt_)2.When</sup> _kt_ = 0, this is the posterior update in Bayes filtering; whereas when _kt_ = _K_ (and **x**<sup>_K_</sup> _t_<sup>is pure noise</sup> and thus uninformative), this is equivalent to modeling the “prior distribution” _pθ_ ( **z** _t |_ **z** _t−_ 1) in Bayes filtering. Given latent **z** _t_ , an observation model _pθ_ ( **x**<sup>0</sup> _t_<sup>_|_</sup><sup>**z**</sup><sup>_t_) predicts</sup><sup>**x**</sup><sup>_t_.</sup> 

**Training.** The dynamics model _pθ_ ( **z** _t|_ **z** _t−_ 1 _,_ **x**<sup>_k_</sup> _t_<sup>_t, kt_) and the observation model</sup><sup>_pθ_(</sup><sup>**x**0</sup> _t_<sup>_|_</sup><sup>**z**</sup><sup>_t_) together</sup> form a RNN unit. Such unit has the same input-output behavior as a standard conditional diffusion model, using a conditioning variable **z** _t−_ 1 and a noisy token **x**<sup>_k_</sup> _t_<sup>_t_as input to predict the noise-free</sup> **x** _t_ = **x**<sup>0</sup> _t_<sup>and thus, indirectly, the noise</sup><sup>_ϵkt_via affine reparametrization [29].We can thus directly</sup> train (Causal) Diffusion Forcing with the conventional diffusion training objective. We parameterize the aforementioned unit in terms of noise prediction **_ϵ_** _θ_ ( **z** _t−_ 1 _,_ **x**<sup>_k_</sup> _t_<sup>_t, kt_).We then find parameters</sup><sup>_θ_by</sup> minimizing the loss 


where we sample _k_ 1: _T_ uniformly from [ _K_ ]<sup>_T_</sup> , **x** 1: _T_ from our training data, and _ϵt ∼N_ (0 _, σk_<sup>2</sup> _t_<sup>_I_) in</sup> accordance with the forward diffusion process (see Algorithm 1 for pseudocode). Importantly, the loss (3.1) captures essential elements of Bayesian filtering and conditional diffusion. In Appendix B.1, we further re-derive common techniques in diffusion model training for Diffusion Forcing, which proves extremely useful for video prediction experiments. In Appendix C.2, we discuss the need of sampling _k_ 1: _T_ uniformly. Finally, we prove the validity of this objective stated informally in the following Theorem 3.1 in Appendix A. 

**Theorem 3.1** (Informal) **.** _The Diffusion Forcing training procedure (Algorithm 1) optimizes a reweighting of an Evidence Lower Bound (ELBO) on the expected log-likelihoods_ ln _p_ **_θ_** (( **x**<sup>_k_</sup> _t_<sup>_t_)1</sup><sup>_≤t≤T_)</sup><sup>_,_</sup> _where the expectation is averaged over noise levels k_ 1: _T ∼_ [ _K_ ]<sup>_T_</sup> _and_ **x**<sup>_k_</sup> _t_<sup>_tnoised according to the_</sup> _forward process. Moreover, under appropriate conditions, optimizing_ (3.1) _also maximizes a lower bound on the likelihood for_ all sequences of noise levels, simultaneously _._ 

> 2We implement **z** _t_ = _pθ_ ( **z** _t|_ **z** _t−_ 1 _,_ **x** _tkt_<sup>_, kt_) to be deterministic, with</sup><sup>**z**</sup><sup>_t_representing a distribution over beliefs</sup> rather than a sample from it. This allows training by backpropogating through the latent dynamics in Eq.(3.1). 

5 

We remark that a special case of ‘all sequences of noise levels’ are those for which either _kt_ = 0 or _kt_ = _K_ ; thus, one can mask out _any prior token_ and DF will learn to sample from the correct conditional distribution, modeling the distribution of all possible sub-sequences of the training set. 

**Sampling.** Diffusion Forcing sampling is depicted in Algorithm 2 and is defined by prescribing a noise schedule on a 2D _M × T_ grid _K ∈_ [ _K_ ]<sup>_M×T_</sup> ; columns correspond to time step _t_ and rows indexed by _m_ determine noise-level. _Km,t_ represents the desired noise level of the time-step _t_ token for row _m_ . To generate a whole sequence of length _T_ , initialize the tokens **x** 1: _T_ to be white noise, corresponding to noise level _k_ = _K_ . We iterate down the grid row-by-row, denoising leftto-right across columns to the noise levels prescribed by _K_ . By the last row _m_ = 0, the tokens are clean, i.e. their noise level is _K_ 0 _,t ≡_ 0. Appendix B.5 discusses corner cases of this scheme; the hyperparameters ( _αk,_ ¯ _αk, σk_ ) are set to their standard values [29]. The matrix _K_ specifies how fast each token gets denoised at every step of sequence diffusion. Since Diffusion Forcing is trained to denoise tokens of all sequences of noise levels, _K_ can be designed to flexibly achieve different behaviors without re-training the model. 

### **3.3 New Capabilities in Sequence Generation** 

We now explain the new capabilities this flexible sampling paradigm has to offer. 

Stable Auto-Reg. Diffuse w/ Full Traj. Condition on Rollout Causal Uncertainty Guidance Currupted Obs. 


**Stabilizing autoregressive generation.** For high-dimensional, continuous sequences such as video, auto-regressive architectures are known to diverge, especially when sampling past the training horizon. In contrast, Diffusion Forcing can stably roll out long sequences even beyond the training sequence length by updating the latents using the previous latent associated with slightly “noisy tokens” for some small noise level 0 _< k ≪ K_ . Our experiments (Sec. 4.1) illustrates the resulting marked improvements in long-horizon generation capabilities; App. C.4 provides further intuition. 

**Keeping the future uncertain.** Beginning from a sequence of white noise tokens [ **x** 1<sup>_K,_</sup><sup>**x**</sup><sup>_K_</sup> 2<sup>_,_</sup><sup>**x**</sup><sup>_K_</sup> 3<sup>]</sup><sup>_⊤_,</sup> we may denoise the first token fully and the second token partially, yielding [ **x** 1<sup>0</sup><sup>_,_</sup><sup>**x**</sup><sup>_K/_</sup> 2<sup>2</sup> _,_ **x**<sup>_K_</sup> 3<sup>]</sup><sup>_⊤_, then</sup> [ **x** 1<sup>0</sup><sup>_,_</sup><sup>**x**0</sup> 2<sup>_,_</sup><sup>**x**</sup><sup>_K/_</sup> 3<sup>2</sup> ]<sup>_⊤_</sup> , and finally denoising all tokens fully to [ **x** 1<sup>0</sup><sup>_,_</sup><sup>**x**0</sup> 2<sup>_,_</sup><sup>**x**0</sup> 3<sup>]</sup><sup>_⊤_.Interpreting the noise level as</sup> uncertainty, this “zig-zag” sampling scheme intuitively encodes the immediate future as more certain than the far future. Sec. 3.4 describes how this leads to more effective sequence guidance. 

**Long-horizon Guidance.** In Line 10 of Algorithm 2, one may add guidance to the partially diffused trajectory **x** 1: _T_ as in Sec. 2. Due to the dependency of future tokens on the past, guidance gradients from future tokens can propagate backwards in time. The unique advantage of Diffusion Forcing is that, because we can diffuse future tokens without fully diffusing the past, the gradient guides the sampling of _past_ tokens, thereby achieving long-horizon guidance while respecting causality. We elaborate on implementation details in Appendix C.3. As we show in Section 4.2, planning in this manner significantly outperforms guided full-sequence diffusion models. 

### **3.4 Diffusion Forcing for Flexible Sequential Decision Making** 

The capabilities offered by Diffusion Forcing motivate our novel framework for sequential decision making (SDM), with key applications to robotics and autonomous agents. Consider a Markov Decision Process defined by an environment with dynamics _p_ ( **s** _t_ +1 _|_ **s** _t,_ **a** _t_ ), observation _p_ ( **o** _t|_ **s** _t_ ) and reward _p_ ( **r** _t|_ **s** _t,_ **a** _t_ ). The goal is to train a policy _π_ ( **a** _t|_ **o** 1: _t_ ) such that the expected cumulative reward of a trajectory E[<sup>�</sup><sup>_T_</sup> _t_ =1<sup>**r**</sup><sup>_t_] is maximized.We assign tokens</sup><sup>**x**</sup><sup>_t_=[</sup><sup>**a**</sup><sup>_t,_</sup><sup>**r**</sup><sup>_t,_</sup><sup>**o**</sup><sup>_t_+1].A trajectory is a</sup> sequence **x** 1: _T_ , possibly of variable length; training is conducted as in Algorithm 1. At each step _t_ of execution, past (noise-free) tokens **x** 1: _t−_ 1 are summarized by a latent **z** _t−_ 1. Conditioned on this latent, we sample, via Algorithm 2, a plan **x** ˆ _t_ : _t_ + _H_ , with **x** ˆ _t_ = [ˆ **a** _t,_ ˆ **r** _t,_ ˆ **o** _t_ +1]<sup>_⊤_</sup> containing predicted actions, rewards and observations. _H_ is a look-ahead window, analogous to future predictions in model predictive control [20]. After taking planned action ˆ **a** _t_ , the environment produces a reward **r** _t_ 

6 


Figure 3: **Video Generation.** Among tested methods, Diffusion Forcing generations are uniquely temporally consistent and do not diverge even when rolling out well past the training horizon. Please see the project website for video results. 

and next observation **o** _t_ +1, yielding next token **x** _t_ = [ˆ **a** _t,_ **r** _t,_ **o** _t_ +1]<sup>_⊤_</sup> . The latent is updated according to the posterior _pθ_ ( **z** _t|_ **z** _t−_ 1 _,_ **x** _t,_ 0). Our framework enables functionality as both _policy_ and _planner_ : 

**Flexible planning horizon.** Diffusion Forcing (a) can be deployed on _tasks of variable horizon_ , because each new action is selected sequentially, and (b) its lookahead window _H_ can be shortened to lower latency (using Diffusion Forcing as a _policy_ ), or lengthened to perform long-horizon _planning_ (via guidance described below), without re-training or modifications of the architecture. Note that (a) is not possible for full-sequence diffusion models like Diffuser [36] with full-trajectory generation horizons, whereas diffusion policies [10] need fixed, small lookahead sizes, precluding (b). 

**Flexible reward guidance.** As detailed in Appendix C.3, Diffusion Forcing can plan via guidance using any reward (in place of log _c_ ) specified over future steps: this includes dense per-time step rewards on the entire trajectory<sup>�</sup><sup>_T_</sup> _t_ =1<sup>**r**</sup><sup>_t_, dense rewards on a future lookahead �</sup> _t_<sup>_t_+</sup><sup>_′_</sup> =<sup>_H_</sup> _t_<sup>**r**</sup><sup>_t_, and sparse</sup> rewards indicating goal completion _−∥_ **o** _T −_ **g** _∥_<sup>2</sup> . Per-time step policies cannot take advantage of this latter, longer horizon guidance. 

**Monte Carlo Guidance (MCG), future uncertainty.** Causal Diffusion Forcing allows us to influence the generation of a token **x**<sup>_k_</sup> _t_<sup>by guidance on the whole distribution of future</sup><sup>**x**</sup><sup>_t_+1:</sup><sup>_T_.Instead</sup> of drawing a single trajectory sample to calculate this guidance gradient, we can draw multiple samples of the future and average their guidance gradients. We call this Monte Carlo Guidance. In the spirit of so-called shooting methods like MPPI [63], **x**<sup>_k_</sup> _t_<sup>is then guided by the expected reward</sup> over the distribution of all future outcomes instead of one particular outcome. The effect of MCG is enhanced when combined with sampling schedules that keep the noise level of future tokens high when denoising immediate next tokens (e.g. the zig-zag schedule described in Sec. 3.3), accounting for greater uncertainty farther into the future. Appendix C.5 further justifies the significance of MCG, and why Diffusion Forcing uniquely takes advantage of it. 

## **4 Experiments** 

We extensively evaluate Diffusion Forcing’s merits as a generative sequence model across diverse applications in video and time series prediction, planning, and imitation learning. Please find the dataset and reproducibility details in the Appendix, as well as video results on the project website. 

### **4.1 Video Prediction: Consistent, Stable Sequence Generation and Infinite Rollout.** 

We train a convolutional RNN implementation of Causal Diffusion Forcing for video generative modeling on videos of Minecraft gameplay [68] and DMLab navigation [68]. At sampling time, we 

7 


|**Maze2d-medium-v1**<br>**Maze2d-large-v1**<br>end<br>start<br>denoising steps<br>denoising steps|
|---|
|**D3F (Ours)**<br>**Diffuser**<br>**Environment**<br>**MPPI**<br>**CQL**<br>**IQL**<br>**Diffuser***<br>**Diffuser w/ diffused action**<br>**Ours wo/ MCG**<br>**Ours**|
|Maze2D<br>U-Maze<br>33.2<br>5.7<br>47.4<br>113.9_±_3.1<br>6.3_±_2.1<br>110.1_±_3.9<br>**116.7**_±_**2.0**|
|Maze2D<br>Medium<br>10.2<br>5.0<br>34.9<br>121.5_±_2.7<br>13.5_±_2.3<br>136.1_±_10.2<br>**149.4**_±_**7.5**|
|Maze2D<br>Large<br>5.1<br>12.5<br>58.6<br>123.0_±_6.4<br>6.3_±_2.1<br>142.8_±_5.6<br>**159.0**_±_**2.7**|
|**Single-task Average**<br>16.2<br>7.7<br>47.0<br>119.5<br>8.7<br>129.67<br>**141.7**|
|Multi2D<br>U-Maze<br>41.2<br>-<br>24.8<br>128.9_±_1.8<br>32.8_±_1.7<br>107.7_±_4.9<br>**119.1**_±_**4.0**|
|Multi2D<br>Medium<br>15.4<br>-<br>12.1<br>127.2_±_3.4<br>22.0_±_2.7<br>145.6_±_6.5<br>**152.3**_±_**9.9**|
|Multi2D<br>Large<br>8.0<br>-<br>13.9<br>132.1_±_5.8<br>6.9_±_1.7<br>129.8_±_1.5<br>**167.1**_±_**2.7**|
|**Multi-task Average**<br>21.5<br>-<br>16.9<br>129.4<br>20.6<br>127.7<br>**146.2**|


Table 1: **Diffusion Forcing for Planning.** ( **top** ) During sampling, Diffusion Forcing allows each time step to be denoised on different noise schedules, enabling us to account for causal uncertainty during guided planning. Diffusion Forcing keeps the far future more uncertain than the near future while Diffuser [36] puts them at the same noise level during sampling. ( **bottom)** Quantitatively, Diffusion Forcing achieves the highest average reward across runs. Diffuser fails dramatically when executing the actually generated actions, requiring a hand-crafted PD controller (indicated by the asterisk) and ignoring generated actions. 

perform auto-regressive rollout with stabilization proposed in Sec. 3.3. We consider two baselines, both leveraging the same exact RNN architecture: a next-frame diffusion baseline trained with teacher forcing [64] as well as a causal full-sequence diffusion model. Figure 3 displays qualitative results of roll-outs generated by Diffusion Forcing and baselines starting from unseen frames for both datasets. While Diffusion Forcing succeeds at stably rolling out even far beyond its training horizon (e.g. 1000 frames), teacher forcing and full-sequence diffusion baselines diverge quickly. Further, within the training horizon, we observe that full-sequence diffusion suffers from frame-to-frame discontinuity where video sequences jump dramatically, while Diffusion Forcing roll-outs show ego-motion through a consistent 3D environment. This highlights the ability of Diffusion Forcing to stabilize rollouts of high-dimensional sequences without compounding errors. 

### **4.2 Diffusion Planning: MCG, Causal Uncertainty, Flexible Horizon Control.** 

Decision-making uniquely benefits from Diffusion Forcing’s capabilities. We evaluate our proposed decision-making framework in a standard offline RL benchmark, D4RL [18]. Specifically, we benchmark Diffusion Forcing on a set of 2D maze environments with sparse reward. An agent is tasked with reaching a designated goal position starting from a random starting position. In Appendix E.5 we provide a detailed description of the environment. The benchmark provides a dataset of _random walks_ through mazes (thus stochastic). We train one model per maze. 

We benchmark the proposed decision-making framework 3.4 with state-of-the-art offline RL methods and the recently introduced Diffuser [36], a diffusion planning framework. See Fig. 1 for qualitative and quantitative results: DF outperforms Diffuser and all baselines across all 6 environments. 

**Benefit of Monte Carlo Guidance.** The typical goal for an RL problem is to find actions that maximize the _expected_ future rewards, which we achieve through MCG. Full-sequence diffusion models such as Diffuser do not support sampling to maximize expected reward, as we formally derive in Appendix C.5. To understand MCG’s importance, we ablate it in Table 1. Removing MCG guidance degrades our performance, though Diffusion Forcing remains competitive even then. 

8 


Figure 4: In our real robot task, a robot arm is asked to swap the slots of two fruits using a third slot. Since the fruits are input in random slots at the beginning, one cannot determine the next steps from a single observation without knowledge of the initial placement of the fruits. As illustrated in (a) and (b), the upper observation is the same but the desired outcome illustrated below can vary—the task thus requires remembering the initial configuration. In addition, as shown in (c), the same model that generates actions also synthesizes realistic video from just a single frame. 

**Benefit of Modeling Causality.** Unlike pure generative modeling, sequential decision-making takes actions and receives feedback. Due to compounding uncertainty, the immediate next actions are more important than those in the far future. Though Diffuser and subsequent models are trained to generate sequences of action-reward-state tuples [ **a** _t,_ **r** _t,_ **o** _t_ ], directly executing the actions will lead to a trajectory that deviates significantly from the generated states. In other words, the generated states and actions are not causally consistent with each other. To address this shortcoming, Diffuser’s implementation ignores the generated actions and instead relies on a hand-crafted PD controller to infer actions from generated states. In Table 1, we see that Diffuser’s performance drops dramatically when directly executing generated actions. In contrast, Diffusion Forcing’s raw action generations are self-consistent, outperforming even actions selected by combining Diffuser’s state predictions with a handcrafted PD controller. 

**Benefit of Flexible Horizon.** Many RL tasks have a fixed horizon, requiring the planning horizon to shrink as an agent makes progress in the task. Diffusion Forcing accomplishes this by design, while full-sequence models like Diffuser perform poorly even with tweaks, as we explain in Appendix C.6. 

### **4.3 Controllable Sequential Compositional Generation** 

We demonstrate that by only modifying the sampling scheme, we can flexibly compose sub-sequences of sequences observed at training time. We consider a dataset of trajectories on a 2D, square plane, where all trajectories start from one corner and end up in the opposite corner, forming a cross shape. As shown in Fig. 1, when no compositional behavior is desired, one can let DF keep full memory, replicating the cross-shaped distribution. When one desires compositionality, one can let the model generate shorter plans without memory using MPC, leading to the stitching of the cross’s sub-trajectories, forming a V-shaped trajectory. Due to limited space, we defer the result to Appendix E.2. 

### **4.4 Robotics: Long horizon imitation learning and robust visuomotor control** 

Finally, we illustrate that Diffusion Forcing (DF) opens up new opportunities in the visuomotor control of real-world robots. Imitation learning [10] is a popular technique in robotic manipulation where one learns an observation-to-action mapping from expert demonstrations. However, the lack of memory often prevents imitation learning from accomplishing long-horizon tasks. DF not only alleviates this shortcoming but also provides a way to make imitation learning robust. 

**Imitation Learning with Memory.** We collect a dataset of videos and actions by teleoperating with a Franka robot. In the chosen task, one needs to swap the position of an apple and an orange, using a third slot. See Fig. 4 for an illustration. The initial positions of the fruits are randomized such that there are two possible goal states. As illustrated in Fig. 4, when one fruit is in the third slot, the desired outcome cannot be inferred from the current observation—a policy must remember the initial configuration to determine which fruit to move. In contrast to common behavior cloning methods, DF naturally incorporates memory in its latent state. We found that DF achieves 80% success rate while diffusion policy [10], a state-of-the-art imitation learning algorithm without memory, fails. 

9 

**Robustness to missing or noisy observations.** Because it incorporates principles from Bayes filtering, Diffusion Forcing can perform imitation learning while being robust to noisy or missing observations. We demonstrate this by adding visual distractions and even fully occluding the camera during execution. DF allows us to easily indicate these observations as “noisy” by using _k >_ 0, in which case DF relies heavily on its prior model to predict actions. Consequently, the success rate is only lowered by 4% to 76%. In contrast, a next-frame diffusion model baseline attains a success rate of 48%: it must treat perturbed observations as ground truth and suffers out-of-distribution error. 

**Potential for pre-training with video.** Finally, in parallel to generating actions, Fig. 4 illustrates that Diffusion Forcing is capable of generating a video of the robot performing the task given only an initial frame, unifying diffusion policy/imitation learning and video generative modeling and paving the way to pre-training on unlabeled video. 

### **4.5 Time Series Forecasting: Diffusion Forcing is a Good General-purpose Sequence Model** 

In Appendix E, we show that DF is competitive with prior diffusion [49] and transformer-based [50] work on multivariate time series forecasting, following the experimental setup of [53]. 

## **5 Discussion** 

**Limitations.** Our current causal implementation is based on an RNN. Applications to higherresolution video or more complex distributions likely require large transformer models following instructions in Appendix C.1. We do not investigate the scaling behavior of Diffusion Forcing to internet-scale datasets and tasks. 

**Conclusion.** In this paper, we introduced Diffusion Forcing, a new training paradigm where a model is trained to denoise sets of tokens with independent, per-token noise levels. Applied to time series data, we show how a next-token prediction model trained with Diffusion Forcing combines the benefits of both next-token models and full-sequence diffusion models. We introduced new sampling and guidance schemes that lead to dramatic performance gains when applied to tasks in sequential decision making. Future work may investigate the application of Diffusion Forcing to domains other than time series generative modeling, and scale up Diffusion Forcing to larger datasets. 

10 

## **References** 

- [1] A. Ajay, Y. Du, A. Gupta, J. Tenenbaum, T. Jaakkola, and P. Agrawal. Is conditional generative modeling all you need for decision-making? _arXiv preprint arXiv:2211.15657_ , 2022. 

- [2] A. Alexandrov, K. Benidis, M. Bohlke-Schneider, V. Flunkert, J. Gasthaus, T. Januschowski, D. C. Maddix, S. Rangapuram, D. Salinas, J. Schulz, L. Stella, A. C. Turkmen, and Y. Wang.¨ Gluonts: Probabilistic and neural time series modeling in python. _Journal of Machine Learning Research_ , 21(116):1–6, 2020. 

- [3] C. Berner, G. Brockman, B. Chan, V. Cheung, P. Debiak, C. Dennison, D. Farhi, Q. Fischer, S. Hashme, C. Hesse, R. Jozefowicz, S. Gray, C. Olsson, J. Pachocki, M. Petrov, H. P.´ de Oliveira Pinto, J. Raiman, T. Salimans, J. Schlatter, J. Schneider, S. Sidor, I. Sutskever, J. Tang, F. Wolski, and S. Zhang. Dota 2 with large scale deep reinforcement learning. _CoRR_ , abs/1912.06680, 2019. 

- [4] A. Blattmann, T. Dockhorn, S. Kulal, D. Mendelevitch, M. Kilian, D. Lorenz, Y. Levi, Z. English, V. Voleti, A. Letts, V. Jampani, and R. Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets, 2023. 

- [5] A. Block, A. Jadbabaie, D. Pfrommer, M. Simchowitz, and R. Tedrake. Provable guarantees for generative behavior cloning: Bridging low-level stability and high-level behavior. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. 

- [6] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei. Language models are few-shot learners. _CoRR_ , abs/2005.14165, 2020. 

- [7] S. H. Chan. Tutorial on diffusion models for imaging and vision. _arXiv preprint arXiv:2403.18103_ , 2024. 

- [8] M. Chen, A. Radford, R. Child, J. Wu, H. Jun, D. Luan, and I. Sutskever. Generative pretraining from pixels. In _International conference on machine learning_ , pages 1691–1703. PMLR, 2020. 

- [9] T. Chen. On the importance of noise scheduling for diffusion models, 2023. 

- [10] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion, 2024. 

- [11] K. Cho, B. van Merrienboer, C¸ . Gul¨ c¸ehre, F. Bougares, H. Schwenk, and Y. Bengio. Learning phrase representations using RNN encoder-decoder for statistical machine translation. _CoRR_ , abs/1406.1078, 2014. 

- [12] J. Chung, K. Kastner, L. Dinh, K. Goel, A. C. Courville, and Y. Bengio. A recurrent latent variable model for sequential data. _Advances in neural information processing systems_ , 28, 2015. 

- [13] J. Cohen, E. Rosenfeld, and Z. Kolter. Certified adversarial robustness via randomized smoothing. In _international conference on machine learning_ , pages 1310–1320. PMLR, 2019. 

- [14] E. de Bezenac,´ S. S. Rangapuram, K. Benidis, M. Bohlke-Schneider, R. Kurle, L. Stella, H. Hasson, P. Gallinari, and T. Januschowski. Normalizing kalman filters for multivariate time series analysis. In _Advances in Neural Information Processing Systems_ , volume 33, 2020. 

- [15] J. Devlin, M. Chang, K. Lee, and K. Toutanova. BERT: pre-training of deep bidirectional transformers for language understanding. _CoRR_ , abs/1810.04805, 2018. 

- [16] P. Dhariwal and A. Nichol. Diffusion models beat gans on image synthesis. _CoRR_ , abs/2105.05233, 2021. 

- [17] C. Feichtenhofer, Y. Li, K. He, et al. Masked autoencoders as spatiotemporal learners. _Advances in neural information processing systems_ , 35:35946–35958, 2022. 

11 

- [18] J. Fu, A. Kumar, O. Nachum, G. Tucker, and S. Levine. D4RL: datasets for deep data-driven reinforcement learning. _CoRR_ , abs/2004.07219, 2020. 

- [19] S. Gao, P. Zhou, M.-M. Cheng, and S. Yan. Masked diffusion transformer is a strong image synthesizer. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 23164–23173, 2023. 

- [20] C. E. Garcia, D. M. Prett, and M. Morari. Model predictive control: Theory and practice—a survey. _Automatica_ , 25(3):335–348, 1989. 

- [21] F. Gers, J. Schmidhuber, and F. Cummins. Learning to forget: continual prediction with lstm. In _1999 Ninth International Conference on Artificial Neural Networks ICANN 99. (Conf. Publ. No. 470)_ , volume 2, pages 850–855 vol.2, 1999. 

- [22] D. Hafner, T. P. Lillicrap, J. Ba, and M. Norouzi. Dream to control: Learning behaviors by latent imagination. _CoRR_ , abs/1912.01603, 2019. 

- [23] D. Hafner, T. P. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson. Learning latent dynamics for planning from pixels. _CoRR_ , abs/1811.04551, 2018. 

- [24] T. Hang, S. Gu, C. Li, J. Bao, D. Chen, H. Hu, X. Geng, and B. Guo. Efficient diffusion training via min-snr weighting strategy, 2024. 

- [25] N. Hansen, X. Wang, and H. Su. Temporal difference learning for model predictive control, 2022. 

- [26] K. He, X. Chen, S. Xie, Y. Li, P. Dollar, and R. Girshick.´ Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 16000–16009, 2022. 

- [27] K. He, X. Zhang, S. Ren, and J. Sun. Deep residual learning for image recognition. _CoRR_ , abs/1512.03385, 2015. 

- [28] J. Ho, A. Jain, and P. Abbeel. Denoising diffusion probabilistic models. _Advances in Neural Information Processing Systems (NeurIPS)_ , 33:6840–6851, 2020. 

- [29] J. Ho, A. Jain, and P. Abbeel. Denoising diffusion probabilistic models. _CoRR_ , abs/2006.11239, 2020. 

- [30] J. Ho and T. Salimans. Classifier-free diffusion guidance, 2022. 

- [31] J. Ho, T. Salimans, A. Gritsenko, W. Chan, M. Norouzi, and D. J. Fleet. Video diffusion models, 2022. 

- [32] S. Hochreiter and J. Schmidhuber. Long short-term memory. _Neural Comput._ , 9(8):1735–1780, nov 1997. 

- [33] A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall, J. Shotton, and G. Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [34] S. Huang, Z. Wang, P. Li, B. Jia, T. Liu, Y. Zhu, W. Liang, and S.-C. Zhu. Diffusion-based generation, optimization, and planning in 3d scenes. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16750–16761, 2023. 

- [35] R. Hyndman, A. B. Koehler, J. K. Ord, and R. D. Snyder. _Forecasting with Exponential Smoothing: The State Space Approach_ . Springer Science & Business Media, 2008. 

- [36] M. Janner, Y. Du, J. B. Tenenbaum, and S. Levine. Planning with diffusion for flexible behavior synthesis. _Proceedings of the International Conference on Machine Learning (ICML)_ , 2022. 

- [37] A. Katharopoulos, A. Vyas, N. Pappas, and F. Fleuret. Transformers are rnns: Fast autoregressive transformers with linear attention. _CoRR_ , abs/2006.16236, 2020. 

12 

- [38] L. Ke, J. Wang, T. Bhattacharjee, B. Boots, and S. Srinivasa. Grasping with chopsticks: Combating covariate shift in model-free imitation learning for fine manipulation. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6185–6191. IEEE, 2021. 

- [39] D. Kingma and R. Gao. Understanding diffusion objectives as the elbo with simple data augmentation. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [40] R. G. Krishnan, U. Shalit, and D. Sontag. Structured inference networks for nonlinear state space models. In _AAAI_ , 2017. 

- [41] G. Lai, W. Chang, Y. Yang, and H. Liu. Modeling long- and short-term temporal patterns with deep neural networks. _CoRR_ , abs/1703.07015, 2017. 

- [42] M. Laskey, J. Lee, R. Fox, A. Dragan, and K. Goldberg. Dart: Noise injection for robust imitation learning. In _Conference on robot learning_ , pages 143–156. PMLR, 2017. 

- [43] X. L. Li, J. Thickstun, I. Gulrajani, P. Liang, and T. B. Hashimoto. Diffusion-lm improves controllable text generation, 2022. 

- [44] H. Lutkepohl.¨ _New Introduction to Multiple Time Series Analysis_ . Springer Science & Business Media, 2005. 

- [45] J. E. Matheson and R. L. Winkler. Scoring rules for continuous probability distributions. _Management Science_ , 22(10):1087–1096, 1976. 

- [46] A. Nichol and P. Dhariwal. Improved denoising diffusion probabilistic models. _CoRR_ , abs/2102.09672, 2021. 

- [47] B. Peng, E. Alcaide, Q. Anthony, A. Albalak, S. Arcadinho, S. Biderman, H. Cao, X. Cheng, M. Chung, L. Derczynski, X. Du, M. Grella, K. Gv, X. He, H. Hou, P. Kazienko, J. Kocon, J. Kong, B. Koptyra, H. Lau, J. Lin, K. S. I. Mantri, F. Mom, A. Saito, G. Song, X. Tang, J. Wind, S. Wozniak, Z. Zhang, Q. Zhou, J. Zhu, and R.-J. Zhu.´ RWKV: Reinventing RNNs for the transformer era. In H. Bouamor, J. Pino, and K. Bali, editors, _Findings of the Association for Computational Linguistics: EMNLP 2023_ , pages 14048–14077, Singapore, Dec. 2023. Association for Computational Linguistics. 

- [48] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _CoRR_ , abs/1910.10683, 2019. 

- [49] K. Rasul, C. Seward, I. Schuster, and R. Vollgraf. Autoregressive Denoising Diffusion Models for Multivariate Probabilistic Time Series Forecasting. In _Proceedings of the 38th International Conference on Machine Learning_ , volume 139 of _Proceedings of Machine Learning Research_ , 2021. 

- [50] K. Rasul, A.-S. Sheikh, I. Schuster, U. M. Bergmann, and R. Vollgraf. Multivariate probabilistic time series forecasting via conditioned normalizing flows. In _International Conference on Learning Representations_ , 2021. 

- [51] D. Ruhe, J. Heek, T. Salimans, and E. Hoogeboom. Rolling diffusion models. _arXiv preprint arXiv:2402.09470_ , 2024. 

- [52] T. Salimans and J. Ho. Progressive distillation for fast sampling of diffusion models. _CoRR_ , abs/2202.00512, 2022. 

- [53] D. Salinas, M. Bohlke-Schneider, L. Callot, R. Medico, J. Gasthaus, and R. Medico. Highdimensional multivariate forecasting with low-rank gaussian copula processes. In _NeurIPS_ , 2019. 

- [54] D. Salinas, V. Flunkert, J. Gasthaus, and T. Januschowski. Deepar: Probabilistic forecasting with autoregressive recurrent networks. _International Journal of Forecasting_ , 36(3):1181–1191, 2020. 

13 

- [55] D. Salinas, V. Flunkert, J. Gasthaus, and T. Januschowski. Deepar: Probabilistic forecasting with autoregressive recurrent networks. _International Journal of Forecasting_ , 36(3):1181–1191, 2020. 

- [56] J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, and S. Ganguli. Deep unsupervised learning using nonequilibrium thermodynamics. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2015. 

- [57] J. Song, C. Meng, and S. Ermon. Denoising diffusion implicit models. _CoRR_ , abs/2010.02502, 2020. 

- [58] B. Tang and D. S. Matteson. Probabilistic transformer for time series analysis. In A. Beygelzimer, Y. Dauphin, P. Liang, and J. W. Vaughan, editors, _Advances in Neural Information Processing Systems_ , 2021. 

- [59] H. Touvron, P. Bojanowski, M. Caron, M. Cord, A. El-Nouby, E. Grave, A. Joulin, G. Synnaeve, J. Verbeek, and H. Jegou.´ Resmlp: Feedforward networks for image classification with dataefficient training. _CoRR_ , abs/2105.03404, 2021. 

- [60] A. Van den Oord, N. Kalchbrenner, L. Espeholt, O. Vinyals, A. Graves, et al. Conditional image generation with pixelcnn decoders. _Advances in neural information processing systems_ , 29, 2016. 

- [61] R. van der Weide. Go-garch: A multivariate generalized orthogonal garch model. _Journal of Applied Econometrics_ , 17(5):549–564, 2002. 

- [62] C. Wei, K. Mangalam, P.-Y. Huang, Y. Li, H. Fan, H. Xu, H. Wang, C. Xie, A. Yuille, and C. Feichtenhofer. Diffusion models as masked autoencoders. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 16284–16294, 2023. 

- [63] G. Williams, A. Aldrich, and E. Theodorou. Model predictive path integral control using covariance variable importance sampling. _arXiv preprint arXiv:1509.01149_ , 2015. 

- [64] R. J. Williams and D. Zipser. A Learning Algorithm for Continually Running Fully Recurrent Neural Networks. _Neural Computation_ , 1(2):270–280, 06 1989. 

- [65] T. Wu, Z. Fan, X. Liu, Y. Gong, Y. Shen, J. Jiao, H.-T. Zheng, J. Li, Z. Wei, J. Guo, N. Duan, and W. Chen. Ar-diffusion: Auto-regressive diffusion model for text generation, 2023. 

- [66] T. Wu, Z. Fan, X. Liu, H.-T. Zheng, Y. Gong, J. Jiao, J. Li, J. Guo, N. Duan, W. Chen, et al. Ardiffusion: Auto-regressive diffusion model for text generation. _Advances in Neural Information Processing Systems_ , 36:39957–39974, 2023. 

- [67] T. Yan, H. Zhang, T. Zhou, Y. Zhan, and Y. Xia. Scoregrad: Multivariate probabilistic time series forecasting with continuous energy-based generative models, 2021. 

- [68] W. Yan, D. Hafner, S. James, and P. Abbeel. Temporally consistent transformers for video generation, 2023. 

- [69] R. Yang, P. Srivastava, and S. Mandt. Diffusion probabilistic modeling for video generation. _Entropy_ , 25(10):1469, 2023. 

- [70] S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and K. Narasimhan. Tree of thoughts: Deliberate problem solving with large language models, 2023. 

- [71] H. Yu, N. Rao, and I. S. Dhillon. Temporal regularized matrix factorization. _CoRR_ , abs/1509.08333, 2015. 

14 

## **A Theoretical Justification** 

In this section, we provide theoretical justification for the train of Diffusion Forcing. The main contributions can be summarized as follows: 

- We show that our training methods optimize a reweighting of the Evidence Lower Bound (ELBO) on the average log-likelihood of our data. We first establish this in full generality (Theorem A.1), and then specialize to the form of Gaussian diffusion (Corollary A.2). We show that the resulting terms decouple in such a fashion that, in the limit of a fully expressive latent and model, makes the reweighting terms immaterial. 

- We show that the expected likelihood over _any_ distribution over sequences of noise levels can be lower bounded by a sum over nonnegative terms which, when reweighted, correspond to the terms optimized in the Diffusion Forcing training objective maximizes. Thus, for a fully expressive network that can drive all terms to their minimal value, Diffusion Forcing optimizes a valid surrogate of the likelihood of _all sequences of noise levels simultaneously._ 

We begin by stating an ELBO for general Markov forward processes _q_ ( _·_ ), and generative models _p_ **_θ_** ( _·_ ), and then specialize to Gaussian diffusion, thereby recovering our loss. We denote our Markov forward process _q_ ( _·_ ) as 


and a parameterized probability model 


We assume that _p_ **_θ_** satisfies the _Markov property_ that 


that is, the latent codes **z** _t−_ 1 is a sufficient statistic for **x**<sup>_kt_</sup> given the history. We say that _p_ **_θ_** has _deterministic latents_ if _p_ **_θ_** ( **z** _t |_ **z** 1: _t−_ 1 _,_ ( **x**<sup>_k_</sup> _s_<sup>_s_)1</sup><sup>_≤s<t,_</sup><sup>**x**</sup> _t_<sup>_kt_) is a Dirac delta.</sup> _Remark_ 1 _._ In order for _p_ **_θ_** to have deterministic latents and correspond to a valid probability distribution, we need to view the latents **z** _t_ not as individual variables, but as a collection of variables **z** _t_ ( _k_ 1: _t_ ) indexed by _t ∈_ [ _T_ ] and the _history_ of noise levels _k_ 1: _t ∈{_ 0 _,_ 1 _, . . . , K}_<sup>_t_</sup> . In this case, simply setting **z** _t_ ( _k_ 1: _t_ ) = ( _k_ 1: _t,_ ( **x**<sup>_k_</sup> _s_<sup>_s_)1</sup><sup>_≤s≤t_tautologically produces deterministic latents.The reason for</sup> indexing **z** _t_ ( _k_ 1: _t_ ) with _k_ 1: _t_ then arises because, otherwise, _p_ **_θ_** ( **z** _t |_ (( **x**<sup>_k_</sup> _s_<sup>_s_)1</sup><sup>_≤s≤t,_(</sup><sup>**x**</sup> _s_<sup>_k_</sup> _s_<sup>_′_)</sup> 1 _≤s≤t_<sup>) would</sup> be ill-defined unless _ks_ = _ks_<sup>_′_forall1</sup><sup>_≤s≤t_,andthus,</sup><sup>_p_</sup><sup>**_θ_**wouldnotcorrespondtoajoint</sup> probability measure. The exposition and theorem that follows allow **z** _t_ ( _k_ 1: _t_ ) to be indexed on past noise levels _k_ 1: _t_ but suppresses dependence on _k_ 1: _t_ to avoid notational confusion. 

### **A.1 Main Results** 

We can now state our main theorem, which provides an evidence lower bound (ELBO) on the expected log-likelihood of partially-noised sequences ( **x**<sup>_k_</sup> _t_<sup>_t_)1</sup><sup>_≤t≤T_, under uniformly sampled levels</sup><sup>_kt_and</sup><sup>**x**</sup> _t_<sup>_kt_</sup> obtained by noising according to _q_ ( _·_ ) as in (A.1). Notice that this formulation does not require an explicit for of _q_ ( _·_ ) or _p_ **_θ_** , but we will specialize to Gaussian diffusion in the following section. **Theorem A.1.** _Fix_ **x**<sup>0</sup> 1: _T_<sup>_.Define the expectation over the forward process with random noise level_</sup> _k_ 1: _T as_ 


_and the expectation over the latents under p_ **_θ_** ( _·_ ) _conditioned on k_ 1: _T ,_ ( **x**<sup>_k_</sup> _s_<sup>_t_)1</sup><sup>_≤t≤Tas_</sup> 


15 

_Then, as long as p_ **_θ_** _satisfies the Markov property,_ 


_where C_ ( **x**<sup>0</sup> 1: _T_<sup>)</sup><sup>_is a constant depending only on_</sup><sup>**x**0</sup> 1: _T_<sup>_(the unnoised data).Moreover, if the latents are_</sup> _deterministic (i.e. p_ **_θ_** ( **z** _t |_ **z** _t−_ 1 _,_ **x**<sup>_k_</sup> _t_<sup>_t_)</sup><sup>_is a Dirac distribution), then the inequality holds with inequality_</sup> _if and only if q_ ( **x**<sup>_k_</sup> _t_<sup>_t_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t_)</sup><sup>_≡p_</sup><sup>**_θ_**(</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t,_</sup><sup>**z**</sup><sup>_t−_1)</sup><sup>_,i.e.thevariationalapproximationis_</sup> _exact._ 

The proof of the above theorem is given in Appendix A.2. Remarkably, it involves _only two_ inequalities! The first holds with equality under deterministic latents and the second holds if and only if variational approximation is exact: _q_ ( **x** _t_<sup>_kt_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t_)</sup><sup>_≡p_</sup><sup>**_θ_**(</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t,_</sup><sup>**z**</sup><sup>_t−_1).This tightness of</sup> the ELBO suggests that the expression in Theorem A.1 is a relatively strong surrogate objective for optimizing the likelihoods. 

### **A.1.1 Specializing to Gaussian diffusion** 

We now special Theorem A.1 to Gaussian diffusion. For now, we focus on the “ **x** -prediction” formulation of diffusion, which is the one used in our implementation. The “ **_ϵ_** -prediction” formalism, used throughout the main body of the text, can be derived similarly (see Section 2 of [7] for a clean exposition). The following theorem follows directly by apply standard likelihood and KL-divergence computations for the DDPM [28, 7] to Theorem A.1. 

**Corollary A.2.** _Let_ 

_q_ ( **x**<sup>_k_+1</sup> _|_ **x**<sup>_k_</sup> _t_<sup>) =</sup><sup>_N_(</sup><sup>**x**</sup><sup>_k_;</sup> ~~�~~ 1 _− βk_ **x**<sup>_k−_1</sup> _, βk_ **I** ) _,_ (A.6) _and define αk_ = (1 _− βk_ ) _, α_ ¯ _k_ =<sup>�</sup><sup>_k_</sup> _j_ =1<sup>_αj.Suppose that we parameterize p_</sup><sup>**_θ_**(</sup><sup>**x**</sup> _t_<sup>_j|_</sup><sup>**x**</sup><sup>_j_</sup> _t_<sup>+1</sup> _,_ **z** _t−_ 1) = _N_ ( _µ_ **_θ_** ( **x**<sup>_j_</sup> _t_<sup>+1</sup> _,_ **z** _t−_ 1 _, j_ ) _, σj_<sup>2)</sup><sup>_, where further,_</sup> 


_where above, we define cj_ =<sup><u>(</u></sup> 2<sup>1</sup> _σ_<sup>_−_2</sup><sup>_α_</sup> (1<sup>_<u>j</u>_</sup><sup><u>)</u></sup> _−_<sup>2</sup> _α_<sup>¯</sup><sup>_α_</sup> ¯ _j_<sup>_<u>j</u>_</sup> )<sup>_−_21</sup><sup>_._</sup> 

_Proof._ The first inequality follows from the standard computations for the “ **x** -prediction” formulation of Diffusion (see Section 2.7 of [7] and references therein). The second follows by replacing the sum unif over _j_ with an expectation over _kt ∼{_ 0 _,_ 1 _, . . . , K}_ . 

We make a couple of remarks: 

- As noted above, Corollary A.2 can also be stated for **_ϵ_** -prediction, or the so-called “ **v** - prediction” formalism, as all are affinely related. 

- Define an idealized latent **z** ˜ _t−_ 1 consisting of all past tokens ( **x**<sup>_k_</sup> _t_<sup>_t_)aswellasoftheir</sup> noise levels _kt_ . This is a sufficient statistic for **z** _t−_ 1, and thus we can always view 

16 

**x** ˆ<sup>0</sup> **_θ_**<sup>(</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t,_</sup><sup>**z**</sup><sup>_t−_1</sup><sup>_, kt_)=</sup><sup>**x**ˆ0</sup> **_θ_**<sup>(</sup><sup>**x**</sup> _t_<sup>_kt,_¯</sup><sup>**z**</sup><sup>_t−_1</sup><sup>_, kt_),where</sup><sup>**z**</sup><sup>_t−_1isjustcompressing</sup><sup>**z**¯</sup><sup>_t−_1.Whenap-</sup> plying the expectation of **x** 1: _T ∼ q_ to both sides of the bound in Corollary A.2, and taking an infimum over possible function approximator **x** ˆ<sup>0</sup> _θ_<sup>, we obtain</sup> 


This leads to a striking finding: with expressive enough latents and _pθ_ , we can view the maximization of each term in Corollary A.2 separately across time steps. The absence of this coupling means that the weighting terms are immaterial to the optimization, and thus can be ignored. 

- Given the above remarks, we can optimize the ELBO by taking gradients through the objective specified by Corollary A.2, and are free to drop any weighting terms (or rescale them) as desired. Backpropagation through E _p,_ **z** 1: _T_ is straightforward due to deterministic latents. This justifies the correctness of our training objective (3.1) and protocol Algorithm 1. 

### **A.1.2 Capturing all subsequences** 

Theorem A.1 stipulates that, up to reweighting, the Diffusion Forcing objective optimizes a valid ELBO on the expected log-likelihoods over uniformly sampled noise levels. The following theorem can be obtained by a straightforward modification of the proof of Theorem A.1 generalizes this to arbitrary (possibly temporally correlated) sequences of noise. 

**Theorem A.3.** _Let D be an arbitrary distribution over_ [ _K_ ]<sup>_T_</sup> _, and define Pt_ ( _j | k_ 1: _t−_ 1) := Pr _D_ [ _kt_ = _j | k_ 1: _t−_ 1] _. Fix_ **x**<sup>0</sup> 1: _T_<sup>_.Define the expectation over the forward process with random noise level k_1:</sup><sup>_T_</sup> _as_ 


_Then, as long as p_ **_θ_** _satisfies the Markov property,_ 


_where C_ ( **x**<sup>0</sup> 1: _T_<sup>)</sup><sup>_is a constant depending only on_</sup><sup>**x**0</sup> 1: _T_<sup>_(the noise-free data), and where the inequality_</sup> _is an_ equality _under the conditions that (a) p_ **_θ_** ( **z** _t |_ **z** _t−_ 1 _,_ **x**<sup>_k_</sup> _t_<sup>_t_)</sup><sup>_is a Dirac distribution (deterministic_</sup> _latents), and (b) q_ ( **x**<sup>_k_</sup> _t_<sup>_t_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t_)</sup><sup>_≡p_</sup><sup>**_θ_**(</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t,_</sup><sup>**z**</sup><sup>_t−_1)</sup><sup>_, i.e.the variational approximation is_</sup> _sharp._ 

_In particular, in the Gaussian case of Corollary A.2, we have_ 


The most salient case for us is the restriction of _D_ to fixed sequences of noise _k_ 1 _, . . . , kT_ (i.e. Dirac distributions on [ _K_ ]<sup>_T_</sup> ). In this case, _Pt_ ( _j | k_ 1: _t−_ 1) = 0 for all but _j_ = _kt_ , and thus our training objective need not be a lower bound on Eforward _,D_ [ln _p_ **_θ_** (( **x** _t_<sup>_kt_)1</sup><sup>_≤t≤T_)].However, the terms in the</sup> lower bound are, up to reweighting, an _subset_ of those terms optimized in the training objective. Thus, in light of the remarks following Corollary A.2, a fully expressive network can optimize all the terms in the loss simultaneously. We conclude that, for a fully expressive neural network, optimizing the training objective (3.1) is a valid surrogate for maximizing the likelihood of all possible noise sequences. 

17 

### **A.2 Proof of Theorem A.1** 

Define E _<t_ [ _·_ ] as shorthand for E _k_ 1: _s_ unif _∼_ [ _K_ ]<sup>E</sup><sup>**x**</sup> _s_<sup>_ks∼q_(</sup><sup>**x**</sup><sup>_ks_</sup> _s_<sup>_|_</sup><sup>**x**0</sup> _s_<sup>)</sup><sup>_,_1</sup><sup>_≤s≤t−_1 E</sup><sup>**z**</sup> _s_<sup>_∼p_(</sup><sup>**z**</sup> _s_<sup>_|_</sup><sup>**z**</sup> _s−_ 1<sup>_,_</sup><sup>**x**</sup> _s_<sup>_ks_)</sup><sup>_,s≤t_[</sup><sup>_·_].We</sup> begin with the following claim 

**Claim 1** (Expanding the latents) **.** _The following lower bound holds:_ 


_Moreover, this lower bound holds with equality if_ **z** _s ∼ p_ ( **z** _s |_ **z** _s−_ 1 _,_ **x**<sup>_k_</sup> _s_<sup>_s_)</sup><sup>_is a Dirac distribution (i.e.,_</sup> _deterministic latents)._ 

_Proof._ Let’s fix a sequence _k_ 1: _T_ . It holds that 


Thus, by Jensen’s inequality, 


where the inequality is and equality when _p_ **_θ_** ( **z** _s |_ **z** _s−_ 1 _,_ **x**<sup>_k_</sup> _s_<sup>_s_) is a Dirac distribution.By applying</sup> Eforward to both sides of the above display, and invoking the Markov property of the latents, we conclude that 


We now unpack the terms obtained from the preceding claim. 

**Claim 2** (ELBO w.r.t. _q_ ) **.** _It holds that_ 


_where C_ 1( **x** 0 _, kt_ ) _is a constant depending only on_ **x** 0 _and kt, and where the inequality holds with equality if and only if q_ ( **x**<sup>_k_</sup> _t_<sup>_t_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t_)</sup><sup>_≡p_</sup><sup>**_θ_**(</sup><sup>**x**</sup> _t_<sup>_kt_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t,_</sup><sup>**z**</sup><sup>_t−_1)</sup><sup>_._</sup> 

18 

_Proof._ We have that 


_<u>t |</u>_ **x**<sup>0</sup> _<u>t</u>_<sup><u>)</u></sup> where the constant _C_ 1( **x** 0 _, kt_ ) = E **x** _ktt_ : _K ∼q_ ( **x**<sup>_kt_</sup> _t_<sup>:</sup><sup>_K_</sup> _|_ **x**<sup>0</sup> _t_<sup>)</sup> �ln _q_<sup>_<u>q</u>_</sup> (<sup><u>(</u></sup> **x**<sup>**x**</sup><sup>_kt_</sup> _t_<sup>_kt_+1:+1:</sup><sup>_KK_</sup> _|_ **x**<sup>_kt_</sup> _t_<sup>)</sup> � depends only on **x** 0 and _kt_ . To check the conditions for equality, note that if _q_ ( **x** _t_<sup>_kt_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t_)</sup><sup>_≡p_</sup><sup>**_θ_**(</sup><sup>**x**</sup> _t_<sup>_kt_+1:</sup><sup>_T_</sup> _|_ **x**<sup>_k_</sup> _t_<sup>_t,_</sup><sup>**z**</sup><sup>_t−_1), then</sup> 


**Claim 3** (Computing the expected ELBO) **.** 


_where C_ 2( **x** 0 _, kt_ ) _is some other constant depending on_ **x** 0 _and kt._ 

_Proof._ The proof invokes similar manipulations to the standard ELBO derivation for diffusion, but with a few careful modifications to handle the fact that we only noise to level _kt_ . As is standard, we require the identity 


19 

**Part 1: Expanding the likelihood ratios** . Using the above identity, we obtain 


where ( _i_ ) uses A.10, ( _ii_ ) invokes a cancellation in the telescoping sum, and the final display follows from the computation 


Observe that, because we don’t parameterize _p_ ( **x**<sup>_K_</sup> _t |_ **z** _t−_ 1), ln _q_ ( **x**<sup>_k_</sup> _t_<sup>_t|_</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t_+1</sup> + � )<sup>**1**</sup><sup>_{kt≥_1</sup><sup>_}_�</sup> ln _<u>p</u>_ <u>(</u> **x**<sup>_K_</sup> _<u>t</u>_<sup>_<u>|</u>_</sup><sup>**z**</sup><sup>_t−_1)</sup> can be regarded as some constant _C_<sup>_′_</sup> ( **x**<sup>_k_</sup> _t_<sup>_t,_</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t_+1</sup> _,_ **x**<sup>_K_</sup> _t_<sup>).Thus,</sup> _q_ ( **x**<sup>_K_</sup> _t_<sup>_|_</sup><sup>**x**</sup><sup>_kt_</sup> _t_<sup>)</sup> 


**Part 2: Taking expecations.** We can now simplify to taking expectations. Observe that 


and similarly, 


Finally, E **x** _ktt_ : _K ∼q_ ( **x**<sup>_kt_</sup> _t_<sup>:</sup><sup>_K_</sup> _|_ **x**<sup>0</sup> _t_<sup>)</sup><sup>_C′_(</sup><sup>**x**</sup> _t_<sup>_kt,_</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>_t_+1</sup> _,_ **x**<sup>_K_</sup> _t_<sup>) is a constant</sup><sup>_C_2(</sup><sup>_kt,_</sup><sup>**x**0) depending only on</sup><sup>_kt,_</sup><sup>**x**0.</sup> Thus, from (A.12) 


20 

**Completing the proof of the ELBO.** We are now ready to complete the proof. By combining the previous two claims, we have 


## **B Additional Method Details** 

### **B.1 Fused SNR reweighting** 

SNR reweighting [24] is a widely used technique to accelerate the convergence of image diffusion models. In short, it reweighs the diffusion loss proportional to the signal-to-noise ratio (SNR) of 

21 

noisy **x**<sup>_k_</sup> . In Diffusion Forcing, conditioning variable **z** _t−_ 1 can also contain a non-trivial amount of information about **x** _t_ , in addition to **x**<sup>_k_</sup> _t_<sup>_t_.For example, in a deterministic markovian system, if</sup><sup>**x**</sup><sup>_k_</sup> _t−_<sup>_t−_</sup> 1<sup>1</sup> has its noise level _kt−_ 1 = 0, the posterior state **z** _t−_ 1 contains all the information needed to predict **x**<sup>0</sup> _t_ regardless of the noise level of **x**<sup>_k_</sup> _t_<sup>_t_.</sup> 

Therefore we **re-derive** SNR reweighting to reflect this change in Diffusion Forcing. We call this technique Fused SNR reweighting. We follow the intuition of original SNR reweighting to loosely define SNR in a sequence with independent levels of noises at different time steps. Denote _St_ as the normalized SNR reweighting factor for **x**<sup>_k_</sup> _t_<sup>_t_following its normal derivation in diffusion models.For</sup> example, if one uses min snr strategy [24], its reweighting factor will always fall between [0 _, C_ ] which we divide by _C_ to get _St ∈_ [0 _,_ 1]. Define signal decay factor 0 _< γ <_ 1, measuring what proportion of signal in **x**<sup>_k_</sup> _t−_<sup>_t−_</sup> 1<sup>1contributetodenoising</sup><sup>**x**</sup> _t_<sup>_kt_.Thisisthesimpleexponentialdecay</sup> model of sequential information. Now, define cumulated SNR recursively as the running mean of _St_ : _S_<sup>¯</sup> _t_ = _γS_<sup>¯</sup> _t−_ 1 + (1 _− γ_ ) _St_ to account for signals contributed by the entire noisy history to the denoising at time step _t_ . The other factor that contributes to the denoising is _St_ of noisy observation **x**<sup>_k_</sup> _t_<sup>_t_.To combine them, we use a simplified model for independent events.Notice</sup><sup>_St_and</sup><sup>_S_¯</sup><sup>_t_always</sup> falls in range [0 _,_ 1], and therefore can be reinterpreted as probabilities of having all the signal one needs to perfect denoise **x**<sup>_k_</sup> _t_<sup>_t_.Since the noise level at</sup><sup>_t_is independent of prior noise levels, we can</sup> view _St_ and _S_<sup>¯</sup> _t−_ 1 as probabilities of independent events and thus can composed to define a joint probability _St_<sup>_′_= 1</sup><sup>_−_(1</sup><sup>_−St_)(1</sup><sup>_−S_¯</sup><sup>_t−_1), and we use this</sup><sup>_S_</sup> _t_<sup>_′_as our fused SNR reweighting factor</sup> for diffusion training. 

In our experiments, we choose to follow the min-SNR reweighting strategy [24] to derive the _S_ . Our Fused SNR reweighting proves extremely useful to accelerate the convergence of video prediction, while we didn’t observe a boost on non-image domains so we didn’t use it there. 

### **B.2 Architecture** 

**Video Diffusion** We choose both the raw image **x** and latent state **z** to be 2D tensors with channel, width, and height. For simplicity, we use the same width and height for **x** and **z** . We then implement the transition model _p_ ( **x**<sup>_k_</sup> _t_<sup>_t|_</sup><sup>**z**</sup><sup>_t−_1) with a typical diffusion U-net [46].We use the output of the U-net</sup> as the input to a gated recurrent unit (GRU) and use **z** _t−_ 1 as the hidden state feed into a GRU. The output of GRU is treated as **z** _t_ . For observation model _p_ ( **x** _t|_ **z** _t_ ), we use a 1-layer resnet [27] followed by a conv layer. We combine these two models to create an RNN layer, where the latent of a particular time step is **z** _t−_ 1, input is **x**<sup>_k_</sup> _t_<sup>_t_and output is</sup><sup>**x**ˆ.One can potentially obtain better results by training</sup> Diffusion Forcing with a causal transformer architecture. However, since RNN is more efficient for online decision-making, we also stick with it for video prediction and it already gives us satisfying results. 

We choose the number of channels in **z** to be 16 for DMlab and 32 for Minecraft. In total, our Minecraft model consists of 36 million parameters and our DMlab model consists of 24 million parameters. We can potentially obtain a better Minecraft video prediction model with more parameters, but we defer that to future works to keep the training duration reasonable ( _<_ 1 day). In maze planning, the number of total parameters is 4 _._ 33 million. 

**Non-Video Diffusion** For non-spatial **x** that is not video nor images, we use residue MLPs [59] instead of Unet as the backbone for the dynamics model. Residue MLP is basically the ResNet [27] equivalent for MLP. Similar to video prediction, we feed the output of resMLP into a GRU along with **z** _t−_ 1 to get **z** _t_ . Another ResMLP serves as the observation model. 

### **B.3 Diffusion parameterization** 

In diffusion models, there are three equivalent prediction objectives, **x** 0, _ϵ_ [28], and _v_ parameterization [52]. Different objectives lead to different reweighting of loss at different noise levels, together with SNR reweighting. For example, _ϵ_ parameterization and _v_ parameterization are essential in generating pixel data that favors high-frequency details. 

In our experiments, we use _v_ parameterization for video prediction and found it essential to both convergence speed and quality. 

22 

We observe that **x** 0 parameterization is strongly favorable in planning and imitation learning, likely because they don’t favor an artificial emphasis on high-frequency details. We observe the benefits of v-parameterization in time-series prediction. 

### **B.4 Noise schedule** 

We use sigmoid noise schedule [9] for video prediction, linear noise schedule for maze planning, and cosine schedule for everything else. 

### **B.5 Implementation Details of Sampling with Guidance** 

**Corner case of sampling noise** In our sampling algorithm, due to the flexibility of the scheduling matrix _K_ , there are corner cases when **x**<sup>_k_</sup> _t_<sup>_t_is required to stay at its same noise level during a sampling</sup> step. The core question of this corner case is whether we should update **x**<sup>_k_</sup> _t_<sup>_t_at all.One option is just</sup> copying over the old value. The other option is to run a backward diffusion followed by a forward diffusion back to its old noise level to resample under the diffusion process. While we conclude this can be an open question, we prefer the later approach, resampling, and use it in Monte Carlo Guidance to generate multiple samples. We note that even if one takes the first approach, the guidance gradient can still flow back in the time steps before _t_ as the dynamics model _p_ ( **z** _t|_ **x**<sup>_k_</sup> _t_<sup>_t,_</sup><sup>**z**</sup><sup>_t−_1) can still</sup> propagate the guidance gradient to **z** _t−_ 1. 

Other than Monte Carlo Guidance, this corner case only happens when _kt_ = 0 or _kt_ = _K_ throughout our experiments. That is, we chose our _K_ such that once any token gets diffused slightly, it will keep diffusing. In the case of _kt_ = _K_ , keeping **x**<sup>_k_</sup> _t_<sup>_t_at the same noise level implies it will stay as white</sup> noise, and we don’t even need to sample another white noise. In case _kt_ = 0, the time step is already completely diffused either approach should give us the same result so we just opt for copying over for simplicity. 

**Guidance for maze planning** In maze planning, our main baseline Diffuer [36] discards the reward from the dataset and directly plans with the goal position and velocity. We adopt the same convention for Diffusion Forcing. One can perform guidance on goal position using log-likelihood _||_ **p** _T −_ **g** _||_ , but a flexible horizon model should not require users to manually specify a _T_ to reach its goal, instead we want it to try to reach the goal for any possible horizon. Therefore we use the reward model � _t_<sup>_||_</sup><sup>**p**</sup><sup>_T−_</sup><sup>**g**</sup><sup>_||_so any time step can be the final step to reach the goal.This objective is challenging</sup> due to the non-convex nature of 2D maze, but we found Diffusion Forcing can still reliably find plans without bumping into walls. However, we also observe that the agent tend to leave the goal location due to the nature of the provided dataset - the goal location is just one possible waypoint for the robot to pass through, and there are no trajectories that simply stay at the goal. We also tried this reward for guidance with Diffuser, but it didn’t work even with a good amount of tuning. 

### **B.6 Performance Optimization** 

Accelerating the diffusion sampling of Diffusion Forcing is similar to that of normal diffusion models. We adopt DDIM [57] sampling for the diffusion of each token. While we use _K_ = 1000 steps of diffusion, we sample with only 100 DDIM for video prediction and 50 for non-video domains. 

While Diffusion Forcing can be implemented with transformers, we use an RNN as the backbone for Diffusion Forcing experiments it’s widely used in decision-making for its flexibility and efficiency in online decision-making systems. To further reduce training time and GPU memory usage, we use frame-stacking to stack multiple observed images as a single **x** . This is due to the fact that adjacent tokens can be very similar - e.g. recording the same motion at higher fps can lead to this. We deem that it’s wasteful if we roll out the dynamics model multiple times to generate almost identical tokens. For video datasets, we manually examine how many time steps it takes to require a minimal level of prediction power instead of copying frames over. There is another reason why we use frame stacking - many diffusion model techniques such as different noise schedules are designed to model **x** with correlated elements or redundancy. Low-dimensional systems may need drastically different hyperparameters when they lack the data redundancy these techniques are tested on. Frame stacking is thus also helpful for our non-image experiments so we can start with canonical hyperparameters of diffusion models. We use a frame stack of 4 for DMlab video prediction, 8 for Minecraft, and 10 for maze planning. 

23 

At sampling time, we also have a design choice to reduce compute usage, as reflected in line 8 of Algorithm 2. In line 8, we directly assign **z**<sup>new</sup> _t_ to **z** _t_ , instead of recalculating **z** _t_ with posterior model _p_ ( **z** _t|_ **z** _t−_ 1 _,_ **x**<sup>new</sup> _t , k −_ 1). Since the model is trained to condition on **z** _t_ estimated from arbitrary noisy history, we recognize that both are valid approaches. The reason why the choose line 8 is twofold. First, it cuts the compute by half, avoiding computing posterior every step. Second, this happens to be what we want for stabilization - **z**<sup>new</sup> _t_ already contains the information of the clean **x**<sup>new</sup> _t_ under our simplified observation model, and happens to be estimated with _k_ = _kt_ , a noise level higher than that of **x**<sup>new</sup> _t_ . This happens to implement the behavior we want for stabilization. 

### **B.7 Sampling schedule for causal uncertainty** 

Inference is depicted in Algorithm 2 and Figure 2. In Equation B.1, we illustrate a specific instantiation of the _K_ matrix we used for causal planning. For simplicity, we denote the case where a latent **z** 0 is given and aim to generate **x** 1: _H_ +1. 


Diffusion Forcing begins by sampling our sequences as white noise with noise level _K_ . It then denoises along each row _m_ = 1 _, . . . , M_ of _K_ in decreasing order. It does so by proceeding sequentially through frames _t_ = 1 _, . . . , T_ , updating the latent (Line 5 of Algorithm 2), and then partially applying the backward process to noise level _k_ = _Km,t_ dictated by the scheduling matrix _K_ (Line 6-7 of Algorithm 2). We call a _K_ like this pyramid scheduling, as the tokens in the far future are kept at higher noise level than near future. 

### **B.8 Metrics for Maze Planning** 

We report the episode reward of Diffusion Forcing for different maze planning environments in Table 1. However, we found that the episode reward isn’t necessarily a good metric: Intuitively, maze planning should reward smart agents that can find the fastest route to the goal, not a slow-walking agent that goes there at the end of the episode. The dataset never contains data on the behavior of staying at the goal, so agents are supposed to walk away after reaching the goal with sequence planning methods. Diffuser may had an unfair advantage of just generating slow plans, which happens to let the agent stay in the neighborhood of the goal for more steps and get a very high reward as a result. This metric seems to exploit flaws in the environment design - a good design would involve a penalty of longer time taken to reach the goal. Therefore, in future works based on our paper, we encourage alternative metrics like the time it takes to reach the goal for the first time, which Diffusion Forcing excels at. 

### **B.9 Implementation Details of Timeseries Regression** 

We follow the implementation of pytorch-ts, where the validation set is a random subset of the training set with the same number of sequences as the test set. We use early stopping when validation crps-sum hasn’t increased for 6 epochs. We leverage the same architecture (1 mlp and 4 grus) as well as a batch size of 32. 

### **B.10 Compute Resources** 

All of our experiments use _fp_ 16 mixed precision training. Time series, maze planning, compositionally, and visual imitation experiments can be trained with a single 2080 _Ti_ with 11GB of memory. We tune the batch size such that we fully use the memory of GPUs. This translates to a batch size of 

24 

2048 for maze planning and compositional experiments, and 32 for visual imitation learning. While we use early stopping on the validation set for time series experiments, we did not carefully search for the minimal number of training steps required, though the model usually converges between 50k to 100 _k_ steps. The above environments thus usually take 4 _−_ 8 hours to train although there is without doubt a significant potential for speed up. 

Video prediction is GPU intensive. We use 8 A100 GPUs for both video prediction datasets. We train for 50 _K_ steps with a batch size of 8 _×_ 16. It usually takes 12 hours to converge at 40 _K_ steps of training (occasional validation time also included). 

## **C Additional Intuitions and Explainations** 

### **C.1 Extension to transformer backbone** 

While this paper focuses on a causal implementation of Diffusion Forcing with RNNs, it’s easy to adopt Diffusion Forcing with modern architectures like transformers. One can simply modify a transformer-based sequence diffusion model to train with independent noise levels across tokens and follow the techniques listed in Section B.1. A strict implementation of causal Diffusion Forcing would involve a causal attention mask on the transformer. However, Diffusion Forcing’s fractional masking can do something more interesting: Consider the scenario that we use a transformer without a causal mask. We can still implement causality by controlling noise. By labeling the future as full white noise, there is no information leaked into the past tokens. By labeling future tokens as free of noise, we make the model completely non-causal. By labeling the future tokens as noisy, a slight amount of information about the future is provided for the prediction of past tokens. This effectively states that one only needs a non-causal architecture, but controlling fractional noise of the future, to achieve partial or complete causality. These extensions are beyond the scope of this paper, but we already verified their effectiveness and thus provide them as intuitions for future works. 

### **C.2 The need for independent noise levels** 

When training Diffusion Forcing, we choose to sample per-token noise level following i.i.d uniform distribution from [1 _,_ 2 _...K_ ]. One may wonder about the necessity of this choice. Here we discuss the unique abilities of independent noise and the compute overhead added by it. 

The use of independent noise confers a number of special capabilities in our model, including stabilization of autoregressive rollout 3.3, modeling causal uncertainty 3.3, and removing the need for expensive reconstruction guidance when conditioning on context C.6. None of these capabilities can be achieved by full-sequence diffusion. AR-diffusion [66] and Rolling Diffusion [51] can only achieve the first and third one. There are more sampling-time applications such as flexible frame interpolation. Finally, we also saw the practical benefits of using independent noise in hyperparameter tuning. One can simply try different sampling schemes to figure out the most effective one for their applications. All these capabilities only require training the model once with Diffusion Forcing. In contrast, any tuning of the sampling scheme would require re-training the model for AR-diffusion and Rolling Diffusion. 

On the other hand, we didn’t observe much computing overhead when comparing Diffusion Forcing to full-sequence diffusion, as soon as one closely follows our training techniques like B.1. The empirical evidence is based on our experiments with an experimental transformer implementation of Diffusion Forcing and is thus not fully consistent with the main paper. However, we present the high-level descriptions below for readers interested in more insights: The complexity added by independent noise levels is in the temporal dimension. Therefore, we first adopt a standard technique for video diffusion models - image pre-training, to abstract away the complexity of the image pixels themselves. Then the complexity left is temporal prediction only. We then take the pre-trained image-only model and continue training it on video data. It turns out the sampling result of Diffusion Forcing with fewer training steps in this second stage is already better than that of full-sequence diffusion at convergence. We speculate that the better result is due to the same data-augmentation effect described in prior works [39]. This shows that the overhead added by independent noise is well-warranted when considering the overall training compute (including image pre-training). 

25 

### **C.3 Guidance as planning** 

As stated in Section 2, one can use the gradient of the logarithmic of a classifier log _c_ ( _y|_ **x**<sup>_k_</sup> _t_<sup>) to guide</sup> the sampling process of diffusion model towards samples with a desired attribute _y_ . For example, _y_ can refer to the indicator of a success event. However, we can consider the logarithmic of a more general _energy function c_ ( **x**<sup>_k_</sup> _t_<sup>).ThishastheinterpretationasPr</sup> � _y|_ **x**<sup>_k_</sup> _t_ �, where Pr� _y_ = 1 _|_ **x**<sup>_k_</sup> _t_ � = _e_<sup>_c_(</sup><sup>**x**</sup><sup>_k_</sup> _t_<sup>)</sup> . Some popular candidate energies include 


corresponding to a cost-to-go; we can obtain unbiased estimates of this gradient by using cumulative reward _c_ ˜( **x**<sup>_k_</sup> _t_<sup>)=�</sup> _t_<sup>_′_</sup> _>t_<sup>**r**</sup><sup>_′_(</sup><sup>**x**</sup> _t_<sup>_k′t′_).Wecanalsousegoaldistance</sup><sup>_c_=</sup><sup>_−∥_</sup><sup>**x**</sup> _T_<sup>_kT_</sup> _−_ **g** _∥_<sup>2</sup> as a terminal reward. We provide details about the guidance function deployed in the maze2d planning experiment in Appendix B.5. 

### **C.4 Noising and stabilizing long-horizon generations** 

Here, we explain in detail how we use noising to stabilize long-horizon generation. At each time _t_ , during the denoising, we maintain a latent **z**<sup>_k_</sup> _t−_<sup>small</sup> 1 from the previous time step, with 0 _< k_ small _≪ K_ corresponding to some small amount of noise. We then do _next token_ diffusion to diffuse the token **x** _t_ across noise levels **x**<sup>_K_</sup> _t_<sup>_,_</sup><sup>**x**</sup> _t_<sup>_K−_1</sup> _, . . . ,_ **x**<sup>0</sup> _t_<sup>(correspondingtoAlgorithm2withhorizon</sup> _T_ = 1, initial latent **z**<sup>_k_</sup> _t−_ 1<sup>,andnoiseschedule</sup><sup>_Km,_1=</sup><sup>_m_);thisprocessalsoproduceslatents</sup> **z**<sup>_K_</sup> _t_<sup>_,_</sup><sup>**z**</sup> _t_<sup>_K−_1</sup> _, . . . ,_ **z**<sup>0</sup> _t_<sup>associated with each noise level.From these, we use the latent</sup><sup>**z**</sup> _t_<sup>_k_small</sup> to repeat the process. This noised latent can be interpreted as an implementation of conditioning on **x**<sup>_k_</sup> _t_<sup>small</sup> in an autoregressive process. In a potential transformer implementation of Diffusion Forcing as we discussed in Appendix C.1, one can instead run a forward diffusion on a fully diffused token to achieve stabilization. 

It is widely appreciated that adding noise to data ameliorates long-term compounding error in behavior cloning applications [38, 42], and even induces robustness to non-sequential adversarial attacks [13]. In autoregressive video generation, the noised **x**<sup>_k_</sup> _t_<sup>small</sup> is in-distribution for training, because Diffusion Forcing trains from noisy past observation in its training objective. Hence, this method can be interpreted as a special case of the DART algorithm for behavior cloning [42], where the imitiator (in our case, video generator) is given actions (in our case, next video frames) from noisy observations (in our case, noised previous frames). Somewhat more precisely, because we use both tokens at training time to train Diffusion Forcing, and using slightly noised tokens for autoregression at test time, our approach inherits the theoretical guarantee of the HINT algorithm [5]. 

### **C.5 Why Monte Carlo Guidance relies on Diffusion Forcing** 

Monte Carlo Guidance provides substantial variance reduction in our estimate of cost-to-go guidance (C.1). This technique crucially relies on the ability to roll out future tokens from current ones to use these sample rollouts to get Monte Carlo estimates for gradients. This is not feasible with full-sequence diffusion, because this requires denoising all tokens in tandem; thus, for a given fixed noise level, there is no obvious source of randomness to use for the Monte Carlo estimate. It may be possible to achieve variable horizon via the trick proposed in the following subsection to simulate future rollouts, but to our knowledge, this approach is nonstandard. 

### **C.6 Does the replacement technique lead to flexible horizons in full-sequence diffusion?** 

A naive way to obtain flexible horizon generation in full-sequence diffusion is via the “replacement trick”: consider a full sequence model trained to diffuse **x** 1: _T_ , which we partition into **x** 1: _t−_ 1 _,_ **x** _t_ : _T_ ]. Having diffused tokens **x** 1: _t−_ 1, we can attempt to denoise tokens of the form [˜ **x**<sup>_k_</sup> 1: _t−_ 1<sup>_,_</sup><sup>**x**</sup><sup>_k_</sup> _t_ : _T_<sup>], where</sup> we _fix_ ˜ **x**<sup>_k_</sup> 1: _t−_ 1<sup>=</sup><sup>**x**1:</sup><sup>_t−_1to be the previously generated token, and only have score gradients update the</sup> remaining **x**<sup>_k_</sup> _t_ : _T_<sup>.One clear disadvantage of this method is inefficiency - one still needs to diffuse the</sup> whole sequence even when there is one step left at _t_ = _T −_ 1. What’s more, [31] points out that this approach of conditioning, named “conditioning by replacement”, is both mathematically unprincipled 

26 


Figure 5: Diffusion Forcing is trained on independent level of noises at different timesteps. As a result, we can control the noise level _k_ to achieve different effects on conditioning and prediction. 

and can lead to inconsistency in the generated sequence. The best fix proposed by [31] incorporates an additional gradient term with respect to **x** _t_ : _T_ at every diffusion step; this is still an incomplete fix and suffers the computation cost of an extra backward propagation for every sampling step. 

### **C.7 Further connection to Bayesian filtering** 

The core idea of Diffusion Forcing can be interpreted as using diffusion to construct an interpolation between prior distribution and posterior distribution of a Bayes filter. Consider the hybrid distribution _p_ ( **z** _t|_ **z** _t−_ 1 _,_ **x**<sup>_k_</sup> _t_<sup>).When</sup><sup>_k_= 0, this hybrid distribution becomes the posterior</sup><sup>_p_(</sup><sup>**z**</sup><sup>_t|_</sup><sup>**z**</sup><sup>_t−_1</sup><sup>_,_</sup><sup>**x**</sup><sup>_t_).On the</sup> other hand, when _k_ = _K_ , the hybrid distribution becomes _p_ ( **z** _t|_ **z** _t−_ 1 _,_ **n** ) for **n** _∼N_ (0 _,_ **I** ). Since the independent Gaussian noise term **n** contains no information about **z** , this is exactly the prior distribution _p_ ( **z** _t|_ **z** _t−_ 1). By varying _k_ between _K_ and 0, the same neural network can parameterize everything between prior and posterior. 

### **C.8 Connection to other sequence training schemes** 

Noise as masking provides a unified view of different sequence training schemes. The following exposition uses a length 3 sequence as an example: We always start with fully masked sequence [ **x** 1<sup>_K,_</sup><sup>**x**</sup><sup>_K_</sup> 2<sup>_,_</sup><sup>**x**</sup><sup>_K_</sup> 3<sup>] with the goal of denoising it a “clean sequence” of zero noise.[</sup><sup>**x**</sup> 1<sup>0</sup><sup>_,_</sup><sup>**x**0</sup> 2<sup>_,_</sup><sup>**x**0</sup> 3<sup>].Assume</sup> all diffusions are sampled with 3-step DDIM. 

**Autoregressive.** In teacher forcing, one trains a model to predict the next token conditioned on prior observations. One can train next-token diffusion models with teacher forcing such as [49]: feed neural network with past observations as well as a current observation and ask it to predict clean current observation. A typical training pair can have the input of [ **x** 1<sup>0</sup><sup>_,_</sup><sup>**x**0</sup> 2<sup>_,_</sup><sup>**x**</sup><sup>_K_</sup> 3<sup>]</sup><sup>_⊤_and target of</sup> [ **x** 1<sup>0</sup><sup>_,_</sup><sup>**x**0</sup> 2<sup>_,_</sup><sup>**x**0</sup> 3<sup>]</sup><sup>_⊤_.</sup> 

27 

At sampling time, one fully diffuses the next token before adding the diffused observation to history to perform an autoregressive rollout. The diffusion process would thus look like 


Notably, Diffusion Forcing can also perform this sampling scheme at sampling time for applications like imitation learning, when one wants to diffuse the next action as fast as possible. 

**Full Sequence Diffusion.** Full sequence diffusion models accept a noisy sequence and denoises level-by-level 


Notably, Diffusion Forcing can also perform this sampling scheme at sampling time. 

**Diffusion Forcing with causal uncertainty** As shown in Figure 2, to model causal uncertainty, Diffusion Forcing keeps the far future more uncertain than the near future by having a larger noise level _k_ , at any time of diffusion. An example pattern looks like this: 


Notable, [65] is the first one to propose such a linear uncertainty sampling scheme for causal diffusion models, although Diffusion Forcing provides a generalization of such scheme in combination with other abilities. 

**Diffusion Forcing with stablization** Previously we introduced the autoregressive sampling scheme that Diffusion Forcing can also do. However, such a scheme can accumulate single-step errors because it treats predicted **x** as ground truth observation. Diffusion Forcing addresses this problem by telling the model that generated images should be treated as noisy ground truth, as shown in 2. 

It first fully diffuses the first token, 


Then, it feed the diffused **x**<sup>0</sup> 1<sup>into the model but tell it is of a slightly higher noise level,as</sup><sup>**x**1</sup> 1<sup>to</sup> diffuse **x** 2. 


Then, it feeds the diffused **x**<sup>0</sup> 2<sup>into the model but tells it is of a higher noise level, as</sup><sup>**x**1</sup> 2<sup>.</sup> [ **x** 1<sup>1</sup><sup>_,_</sup><sup>**x**1</sup> 2<sup>_,_</sup><sup>**x**</sup><sup>_K//_</sup> 3<sup>2</sup> ]<sup>_⊤_</sup> _,_ [ **x** 1<sup>1</sup><sup>_,_</sup><sup>**x**1</sup> 2<sup>_,_</sup><sup>**x**0</sup> 3<sup>]</sup><sup>_⊤._</sup> 

28 


Figure 6: Prediction intervals of Diffusion Forcing for the first prediction window of the test set in the Electricity time series dataset. Only the first 16 features out of 370 are plotted. 

## **D Extended Related Work** 

**Reconstructing masked tokens.** Masked Autoencoders for images [26] and videos [17] are a popular method for representation learning in pixel space. They have been extended to perform diffusion to generate masked patches conditioned on unmasked ones [62, 19]. 

**Casting Image Generation as Sequence Generation.** [60, 8] show that even generative modeling of non-sequential data, such as images, can be fruitfully cast as sequence generative modeling. 

**Non-Diffusion Probabilistic Sequence Models.** [12] parameterize token-to-token transitions via a variational auto-encoder. This makes them probabilistic, but does not directly maximize the joint probability of sequences, but rather, enables sampling from the distribution of single-step transitions. 

**Sequence Diffusion with Varying Noise Levels.** Most similar to our work is AR-Diffusion [65] which similarly aims to train next-token prediction models for sequence diffusion. Key differences are that AR-Diffusion proposes a noise level that is _linearly_ dependent on the position of each word in the sequence, while our critical contribution is to have each noise level be _independent_ , as this uniquely enables our proposed sampling schemes, such as stabilizing auto-regressive generation and conditioning on corrupted observations. Further, AR-Diffusion only explores language modeling and does not explore guidance, while we investigate Diffusion Forcing as a broadly applicable sequence generative model with particular applications to sequential decision-making. In particular, we introduce Monte-Carlo Guidance as a novel guidance mechanism. Another closely related work is Rolling Diffusion [51], which proposes to diffuse a sequence with near future more certain and far future more uncertain, resembling the causally uncertain sampling scheme of Diffusion Forcing. Like AR-Diffussion, Rolling Diffusion’s training noise levels are linearly dependent on the positions of tokens and must use the exact same noise level scheme at sampling time. It, therefore, shares the aforementioned limitations of AR-Diffusion as well. 

## **E Additional Experiment Results** 

### **E.1 Multivariate Probabilistic Time Series Forecasting** 

To illustrate Diffusion Forcing’s new training objective does not degrade it as a generic sequence model, we evaluate Diffusion Forcing on high-dimensional and long-horizon sequence prediction 

29 

tasks in time series prediction. We adopt multiple time series datasets with real-world applications from GluonTS [2] and evaluate Diffusion Forcing with strong baselines with standard metrics in this domain. In this section, we mainly focus on the results and analysis. For a detailed description of datasets and the metric, we refer the reader to Appendix F.4. 

**Problem Formulation** Let **_X_** = _{_ **x** _t}_<sup>_T_</sup> _t_ =1<sup>be a sequence (multivariate time series) of</sup><sup>_D_-dimensional</sup> observations **x** _t ∈_ R<sup>_D_</sup> of some underlying dynamical process, sampled in discrete time steps _t ∈{_ 1 _, . . . , T }_ , where _T ∈_ N. In the problem setting of probabilistic time series forecasting, the sequence **_X_** = _{_ **_X_** _c,_ **_X_** _p}_ is split into two subsequences at time step _t_ 0 _∈_ N with 1 _< t_ 0 _≤ T_ : the context window **_X_** _c_ := _{_ **x** _t}_<sup>_t_</sup> _t_<sup>0</sup> =1<sup>_−_1(also called history or evidence) of length</sup><sup>_t_0</sup><sup>_−_1, and the prediction</sup> window **_X_** _p_ := _{_ **x** _t}_<sup>_T_</sup> _t_ = _t_ 0<sup>of length</sup><sup>_T−t_0 + 1 (also known as the prediction horizon).Then, the task</sup> is to model the conditional joint probability distribution 


over the samples in the prediction window. If we know the distribution in (E.1), we can sample forecast prediction sequences given some initial context from the evidence sequence. However, most time-dependent data generation processes in nature have complex dynamics and no tractable formulation of _q_ ( **x** _t_ 0: _T |_ **x** 1: _t_ 0 _−_ 1). Instead, we construct a statistical model that approximates the generative process in (E.1) and estimates quantiles via Monte Carlo sampling of simulated trajectories. In this way, confidence levels or uncertainty measures can be calculated, and point forecasts can be produced as the mean or median trajectory [35]. 

Table 2: Results for time series forecasting. We report the test set CRPS **sum** (the lower, the better) of comparable methods on six time series datasets. We measure the mean and standard deviation of our method from five runs trained with different seeds. 

|Method|Exchange|Solar|Electricity|Traffic|Taxi|Wikipedia|
|---|---|---|---|---|---|---|
|VES [35]|0.005_±_0.000|0.900_±_0.003|0.880_±_0.004|0.350_±_0.002|-|-|
|VAR [44]|0.005_±_0.000|0.830_±_0.006|0.039_±_0.001|0.290_±_0.001|-|-|
|VAR-Lasso [44]|0.012_±_0.000|0.510_±_0.006|0.025_±_0.000|0.150_±_0.002|-|3.100_±_0.004|
|GARCH [61]|0.023_±_0.000|0.880_±_0.002|0.190_±_0.001|0.370_±_0.001|-|-|
|DeepAR [54]|-|0.336_±_0.014|0.023_±_0.001|0.055_±_0.003|-|0.127_±_0.042|
|LSTM-Copula [53]|0.007_±_0.000|0.319_±_0.011|0.064_±_0.008|0.103_±_0.006|0.326_±_0.007|0.241_±_0.033|
|GP-Copula [53]|0.007_±_0.000|0.337_±_0.024|0.025_±_0.002|0.078_±_0.002|0.208_±_0.183|0.086_±_0.004|
|KVAE [40]|0.014_±_0.002|0.340_±_0.025|0.051_±_0.019|0.100_±_0.005|-|0.095_±_0.012|
|NKF [14]|-|0.320_±_0.020|0.016_±_0.001|0.100_±_0.002|-|0.071_±_0.002|
|Transformer-MAF [50]|0.005_±_0.003|0.301_±_0.014|0.021_±_0.000|0.056_±_0.001|0.179_±_0.002|0.063_±_0.003|
|TimeGrad [49]|0.006_±_0.001|0.287_±_0.020|0.021_±_0.001|0.044_±_0.006|0.114_±_0.020|0.049_±_0.002|
|ScoreGrad sub-VP SDE [67]|0.006_±_0.001|**0.256**_±_**0.015**|**0.019**_±_**0.001**|0.041_±_0.004|0.101_±_0.004|**0.043**_±_**0.002**|
|**Ours**|**0.003**_±_**0.001**|0.289_±_0.002|0.023_±_0.001|**0.040**_±_**0.004**|**0.075**_±_**0.002**|0.085_±_0.007|


**Results.** We evaluate the effectiveness of Diffusion Forcing as a sequence model on the canonical task of multivariate time series forecasting by following the experiment setup of [53, 50, 49, 58, 67] Concretely, we benchmark Diffusion Forcing on the datasets Solar, Electricity, Traffic, Taxi, and Wikipedia. These datasets have different dimensionality, domains, and sampling frequencies, and capture seasonal patterns of different lengths. The features of each dataset are detailed in Table 3. We access the datasets from GluonTS [2], and set the context and prediction windows to the same length for each dataset. Additionally, we employ the same covariates as [49]. We evaluate the performance of the model quantitatively by estimating the Summed Continuous Ranked Probability Score CRPSsum via quantiles. As a metric, CRPSsum measures how well a forecast distribution matches the ground truth distribution. We provide detailed descriptions of the metric in Appendix F.4. We benchmark with other diffusion-based methods in time series forecastings, such as TimeGrad [49] and the transformer-based Transformer-MAF [50]. In particular, the main baseline of interest, TimeGrad [49], is a next-token diffusion sequence model trained with teacher forcing. We track the CRPSsum metric on the validation set and use early stopping when the metric has not improved for 6 consecutive epochs, while all epochs are fixed to 100 batches across datasets. We then measure the CRPSsum on the test set at the end of the training, which we report in Table 2. We use the exact same architecture and hyperparameters for all time series datasets and experiments. Diffusion Forcing outperforms all prior methods except for [67] with which Diffusion Forcing is overall tied, except for the Wikipedia dataset, on which Diffusion Forcing takes fourth place. Note that time series is not the core application 

30 

of Diffusion Forcing, and that we merely seek to demonstrate that the Diffusion Forcing objective is applicable to diverse domains with no apparent trade-off in performance over baseline objectives. 

### **E.2 Additional results in compositional generation** 

Since Diffusion Forcing models the joint distribution of any subset of a sequence, we can leverage this unique property to achieve compositional behavior - i.e., Diffusion Forcing can sample from the distribution of _subsets_ of the trajectory and compose these sub-trajectories into new trajectories. 

In particular, we show that we can also have flexible control over how compositional Diffusion Forcing is. As shown in 7, consider a dataset of trajectories on a 2D, square plane, where all trajectories start from one corner and end up in the opposite corner, forming a cross shape. When no compositional behavior is desired, one can let the models replicate the cross-shaped distribution by allowing full memory of the HMM model. When one desires compositional such as generating a V-shaped trajectory, which stitches two sub-trajectories together, one can let the model generate shorter plans with no-memory context using MPC. (Add figures). 


(a) Dataset (b) W/ memory (c) W/o memory 

Figure 7: Given a dataset of trajectories (a), Diffusion Forcing models the joint distribution of all subsequences of arbitrary length. At sampling time, we can sample from the trajectory distribution by sampling Diffusion Forcing with full horizon (b) or recover Markovian dynamics by disregarding previous states (c). 

### **E.3 Additional results in video prediction (wo/ cherry picking)** 

**Infinite Rollout without sliding window** Diffusion Forcing can rollout longer than maximum training horizon _without sliding window_ . That is, we run Diffusion Forcing’s RNN continuously without ever reinitializing **z** 0. This is a surprising effect we observed from the rollout stabilization property of Diffusion Forcing. In Figure 8, 10, we use Diffusion Forcing to generate video sequences of length 180 and visualize subsampled sequences. Notably, Diffusion Forcing used in these visualizations is trained with a maximum length of 72 frames for Minecraft and 36 frames for DMLab, illustrating it can rollout 2x-5x times longer than it’s trained on _without sliding window_ . In addition, we also tried rolling these models out for 2000 frames and without seeing the model blowing up on both datasets. There are occasional cases where the Minecraft agent gets stuck and the entire screen is the “dirt” block, but this is more of a dataset issue E.5 and the agent is able to recover after it turns around. 

**Consistency** We also present additional results where we only generate within our maximum training length. As shown in figure 13 12, Diffusion Forcing can generate consistent videos. Results are not cherry-picked. 

31 


Figure 8: Visualization shows Diffusion Forcing trained on 72 frames is able to rollout 180 frames on Minecraft dataset _without sliding window_ . The visualization shows a non-cherry-picked subsampling of these 180 frames, although Diffusion Forcing can roll out much longer (such as 2000 frames) on this dataset. 

### **E.4 Additional results in planning** 

We provide some additional visualizations of causal planning in 15. We also present additional visualization of Diffusion Forcing performing model predictive control in action. As shown in figure 14, Diffusion Forcing can generate plans of shorter horizons since it’s flexible horizon. 

32 


Figure 9: Diffusion Forcing trained on 72 frames is able to rollout 180 frames on Minecraft dataset _without sliding window_ . The visualization shows a non-cherry-picked subsampling of these 180 frames, although Diffusion Forcing can roll out much longer (such as 2000 frames) on this dataset. The first few frames marked in red are the ground truth images of the dataset used for conditioning. 

### **E.5 Real robot experiment setup** 

In Figure 16 we visualize our robot experiment setup with corruption on observation. The dataset is collected when the target bag isn’t present, while we test with such a bag in the scene zero-shot for the imitation learning experiment with observation corruption. The typical failure mode is when the robot no longer reacts to the visual clues of the randomized location of objects. We didn’t observe the robot act wildly due to visual distractors. 

## **F Additional details about datasets** 

### **F.1 Dataset for video diffusion** 

We adopt the video prediction dataset Minecraft and DMlab used by TECO[68]. 

**Minecraft Navigation** The Minecraft navigation dataset consists of first-person-view videos of random walks in the Minecraft ‘swamp‘ biome. The agent walks via a technique called ‘sprint jump‘ which allows it to jump across blocks without getting stuck at 1 block obstacles. The agent walks straight most of the time, with small chances of turning left or right. The height and width of the video is 128 pixels and we trim long videos to subsequences of 72 frames. The dataset comes with paired action data but we discard them to bring more stochasticity to the prediction task. Due to limited compute, we only train on about 10% of the total subsequences. 

One problem we noticed about the dataset is when the agent runs into obstacles with a height of 2 blocks or more. In this case, the agent will get stuck and the entire video sequence will consist of grey granite patterns or brown dirty patterns. This leads to a huge amount of frames with these patterns, making video models predict meaningless frames. Yet, we deem this as a problem of this dataset itself. 

**DMLab Navigation** Deepmind Lab navigation dataset consists of random walks in a 3D maze environment. For DMLab, the resolution is 64 pixels and we use subsequences of 48 frames. We also disregard the provided actions due to training. 

We note that the VQ-VAE latent that stable video diffusion [4] diffuses is also only 128 _×_ 128 _×_ 3, indicating Diffusion Forcing has the potential to scale up to higher resolution images with pre-trained 

33 


Figure 10: Visualization shows Diffusion Forcing trained on 36 frames is able to rollout 180 frames on DMLab dataset _without sliding window_ . The visualization shows a non-cherry-picked subsampling of these 180 frames, although Diffusion Forcing can roll out almost infinitely on this dataset. The first few frames marked in red are the ground truth images of the dataset used for conditioning. 

image encoder and decoders. Due to the sheer size of the datasets, we only use about 10% of the total data sequences for training due to limited computing, as we observe that doing so already allows us to make good generations from initial frames from the test set. 

### **F.2 Dataset for planning** 

D4RL [18] is a standard offline RL benchmark featuring a wide range of reinforcement learning environments. Each environment is associated with a provided dataset of offline interactions with the environment featuring state, action, and reward trajectories. 

Like Diffuer [36], we choose the 3 maze environments as they are challenging long-horizon, multimodal, sparse reward problems uniquely suited for visualization and evaluating planning algorithms. The IDs for the 3 used environments are “maze2d-medium-v1”, “maze2d-large-v1”, “maze2d-umaze- 

34 


Figure 11: Visualization shows Diffusion Forcing trained on 36 frames is able to rollout 180 frames on DMLab dataset _without sliding window_ . The visualization shows a non-cherry-picked subsampling of these 180 frames, although Diffusion Forcing can roll out almost infinitely on this dataset. The first few frames marked in red are the ground truth images of the dataset used for conditioning. 

v1”. In each environment, one controls the acceleration of a robot to walk it towards a goal. The observation space is 4 dimensional, featuring 2D location and velocity. The action space is 2D acceleration. The agent always receives a random start location and the goal is to reach a fixed goal position for each maze. The agent receives a reward of 1 if it is within a circle of radius 0.5 centered at the goal state, and 0 otherwise. 

The offline RL dataset for the maze environments consists of random walks in the maze. Specifically, the authors first designate all intersections and turn in the maze as waypoints and code an agent to navigate between waypoints with some randomization. As a result, the random walks are generated in a way that the path is collision-free with the walls. The random walks introduce stochasticity to the dataset, as trajectories in the dataset are never towards a specific goal. 

35 


Figure 12: Additional non-cherry-picked video prediction results on DMLab dataset, generated within maximum training length. The first few frames marked in red are the ground truth images of the dataset used for conditioning. 

There are a few choices adopted from our main baseline Diffuser [36]: we disregard the reward in the dataset and plan with goals only. We also evaluate a multi-goal variant of each environment (labeled as “multi” in Table 1), where the goal is randomized just like the starting position. 

### **F.3 Dataset for robot learning** 

We choose a long horizon robotic manipulation task as described in Section 4.4: Consider a tabletop with three slots where we can place objects. One places an apple at slot A or slot B randomly, and then places an orange at the other slot between A and B. A robot is challenged to swap the position of two fruits using the third slot C. That is, it can only move a fruit to an empty slot at a time. For example, when the apple is at slot A and the orange is at slot B, it may move the apple to slot C, leaving slot A empty. Then move the orange to slot A and finally move the apple from slot C to slot B. In figure 4, we illustrate the non-markovian property of the task: When the apple is at slot B and the orange is at slot C, one cannot tell what the immediate action is without knowing the initial positions of objects. 

We put stickers on the table indicating a circular region occupied by any slot. Each circular region is designed to be about double the diameter of a fruit. To make sure the task requires visual feedback, we also randomize the location of a fruit inside the slot. We collected 150 expert demonstrations of a Franka robot performing the task using VR teleoperation and impedance control. Among them, each initial slot configuration makes up half of the dataset. We record videos from two camera views, one from a hand camera and one in the front capturing all three slots. Each demonstration 

36 


Figure 13: Additional non-cherry-picked video prediction results on the Minecraft dataset, generated within maximum training length. The first few frames marked in red are the ground truth images of the dataset used for conditioning. 

also comes with 6 dof actions of the robot hand. During the data collection, since one successful demonstration will swap the position of two objects, its end configuration will naturally serve as the starting configuration of the other randomized location, which we leverage to save time. 

Each demonstration comprises 500 _−_ 600 frames and actions. We train Diffusion Forcing on the entire sequence. However, since adjacent frames are visually close, we pad and downsample the videos to 40 frames where each frame is bundled with 15 actions. 

### **F.4 Dataset for time series** 

Table 3: Characteristics of the GluonTS datasets used to benchmark Diffusion Forcing in the domain of time series forecasting. 

|Dataset|Dimension|Domain|Frequency|Steps|Prediction length|
|---|---|---|---|---|---|
|Exchange|8|R<sup>+</sup><br>|BUSINESS DAY|6,071|30|
|Solar|137|R<sup>+</sup><br>|HOUR|7,009|24|
|Electricity|370|R<sup>+</sup>|HOUR|5,833|24|
|Traffic|963|(0,1)|HOUR|4,001|24|
|Taxi|1,214|N|30-MIN|1,488|24|
|Wikipedia|2,000|N|DAY|792|30|


We use a set of time series datasets accessible via GluonTS [2], which are adopted from prior works like [71, 41, 55]. These datasets capture real-world data of high-dimensional dynamics like monetary exchange rates or the electricity grid. In Table 3, we provide a summary of the features of these datasets, such as the dimensionality, the domains, the sampling frequency, the length of the multivariate sequence in the training set, and the prediction length. We access the datasets in Table 3 via GluonTS and wrap the data processing functions implemented in GluonTS in our own dataloaders. Each dataset consists of one long multivariate sequence, which is the training split, and a set of short sequences that make up the test split. We construct a validation set of the same cardinality as the held-out test set as a randomly sampled subset of subsequences from the training set. All splits are normalized by the mean and the standard deviation of the features in the training split. 

**Covariates** Often, statistical models that approximate (E.1) benefit from manually curated features as additional input to the observations. A sequence of covariates **_C_** = _{_ **c** _t}_<sup>_T_</sup> _t_ =1<sup>can be constructed</sup> to help the model recognize seasonal patterns and other temporal dependencies. We follow the implementation in [50] to construct the covariate sequence as a function of the frequency of each dataset in Table 3. As such, our covariates are composed of lagged inputs, as well as learned embeddings and handcrafted temporal features that encode information such as the hour of the day or the day of the month, depending on the sampling rate of the particular time series that is being 

37 


Figure 14: Example MPC planning for maze medium environment. Blue indicated trajectories actually executed already. Red is the plan. 


Figure 15: Example plans generated for maze medium (above) and maze large (below) environments. 

modeled. Therefore, covariates are known for the entire interval [1 _, T_ ], even at inference. We can easily incorporate covariates into the probabilistic framework as 


The benefit obtained from covariates is highly dependent on the characteristics of both the dataset and the model used, as well as the feature engineering practices followed. 

38 


Figure 16: We randomly throw a target bag on the table as a strong visual distractor. Diffusion Forcing can be prompted to treat observation as corrupted rather than ground truth. 

**Metric** The Continuous Ranked Probability Score (CRPS) [45] is a scoring function that measures how well the forecast distribution matches the ground truth distribution: 


where _F_ ( _z_ ) is the univariate cumulative distribution function (CDF) over the predicted value, _x_ is a ground truth observation, and I _{x ≤ z}_ is the indicator function that is one if _x ≤ z_ and zero otherwise. By summing the _D_ -dimensional time series along the feature dimension for simulated samples (resulting in _F_<sup>ˆ</sup> sum( _t_ )) and ground truth data (as<sup>�</sup> _i_<sup>_x_0</sup> _i,t_<sup>), we can report the CRPSsum</sup> 


as the average over the prediction window. The lower the CRPSsum value, the better the predicted distribution match the data distribution. 

First, we manually sum the time series along the feature dimension and estimate the CDF _F_<sup>ˆ</sup> sum( _t_ ) via 19 quantile levels at each time step _t_ from 100 sampled trajectories. We then use the implementation in GluonTs [2] to compute the CRPS, which we report as CRPSsum in Table 2. While we aggregate the data manually, we verify that the numerical error relative to the GluonTS implementation remains orders of magnitude below the precision threshold of the reported metric. 

39 

## **NeurIPS Paper Checklist** 

### 1. **Claims** 

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? 

Answer: [Yes] 

Justification: The claims made in the abstract and introduction are supported by experimental results and are contextualized with respect to competing methods. 

Guidelines: 

- The answer NA means that the abstract and introduction do not include the claims made in the paper. 

- The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A No or NA answer to this question will not be perceived well by the reviewers. 

- The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings. 

- It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper. 

### 2. **Limitations** 

Question: Does the paper discuss the limitations of the work performed by the authors? Answer: [Yes] 

Justification: Limitations are discussed in the final section of the paper (5). Guidelines: 

   - The answer NA means that the paper has no limitation while the answer No means that the paper has limitations, but those are not discussed in the paper. 

   - The authors are encouraged to create a separate ”Limitations” section in their paper. 

   - The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be. 

   - The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated. 

   - The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon. 

   - The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size. 

   - If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness. 

   - While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations. 

3. **Theory Assumptions and Proofs** 

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof? 

40 

Answer: [Yes] 

Justification: Derivations of relevant expressions are provided in the supplement. 

Guidelines: 

   - The answer NA means that the paper does not include theoretical results. 

   - All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced. 

   - All assumptions should be clearly stated or referenced in the statement of any theorems. 

   - The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition. 

   - Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material. 

   - Theorems and Lemmas that the proof relies upon should be properly referenced. 

4. **Experimental Result Reproducibility** 

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)? 

Answer: [Yes] 

Justification: We provide reproducibility details for each experiment in the supplement. Guidelines: 

   - The answer NA means that the paper does not include experiments. 

   - If the paper includes experiments, a No answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not. 

   - If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable. 

   - Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed. 

   - While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example 

   - (a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm. 

   - (b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully. 

   - (c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset). 

   - (d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results. 

5. **Open access to data and code** 

41 

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material? 

Answer: [Yes] 

Justification: Code has been released publicly. 

Guidelines: 

- The answer NA means that paper does not include experiments requiring code. 

- Please see the NeurIPS code and data submission guidelines ( `https://nips.cc/ public/guides/CodeSubmissionPolicy` ) for more details. 

- While we encourage the release of code and data, we understand that this might not be possible, so “No” is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark). 

- The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines ( `https: //nips.cc/public/guides/CodeSubmissionPolicy` ) for more details. 

- The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc. 

- The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why. 

- At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable). 

- Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted. 

### 6. **Experimental Setting/Details** 

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results? 

Answer: [Yes] 

Justification: Experiment details are provided in the paper and supplement. 

Guidelines: 

- The answer NA means that the paper does not include experiments. 

- The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them. 

- The full details can be provided either with the code, in appendix, or as supplemental material. 

### 7. **Experiment Statistical Significance** 

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments? 

Answer: [Yes] 

Justification: We report all quantitative results in terms of the mean and standard deviation over several runs. 

Guidelines: 

- The answer NA means that the paper does not include experiments. 

- The authors should answer ”Yes” if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper. 

- The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions). 

42 

   - The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.) 

   - The assumptions made should be given (e.g., Normally distributed errors). 

   - It should be clear whether the error bar is the standard deviation or the standard error of the mean. 

   - It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified. 

   - For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates). 

   - If error bars are reported in tables or plots, The authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text. 

8. **Experiments Compute Resources** 

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments? 

Answer: [Yes] 

Justification: All experiments were performed on the same device, the details of which are described in the supplement. 

Guidelines: 

   - The answer NA means that the paper does not include experiments. 

   - The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage. 

   - The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute. 

   - The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper). 

9. **Code Of Ethics** 

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics `https://neurips.cc/public/EthicsGuidelines` ? 

Answer: [Yes] 

Justification: To the best of our knowledge, we conform to the Code of Ethics. At this time we do not see our method providing a straightforward avenue for abuse by bad actors. Guidelines: 

   - The answer NA means that the authors have not reviewed the NeurIPS Code of Ethics. 

   - If the authors answer No, they should explain the special circumstances that require a deviation from the Code of Ethics. 

   - The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction). 

10. **Broader Impacts** 

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed? 

Answer: [NA] 

Justification: Due to the low-level nature of our method, we do not see it directly facilitating any negative social impacts. Guidelines: 

- The answer NA means that there is no societal impact of the work performed. 

- If the authors answer NA or No, they should explain why their work has no societal impact or why the paper does not address societal impact. 

43 

- Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations. 

- The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster. 

- The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology. 

- If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML). 

### 11. **Safeguards** 

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pretrained language models, image generators, or scraped datasets)? 

Answer: [NA] 

Justification: 

Guidelines: 

- The answer NA means that the paper poses no such risks. 

- Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters. 

- Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images. 

- We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort. 

### 12. **Licenses for existing assets** 

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected? 

Answer: [Yes] 

Justification: All data used is cited in accordance with the provided licenses. 

Guidelines: 

- The answer NA means that the paper does not use existing assets. 

- The authors should cite the original paper that produced the code package or dataset. 

- The authors should state which version of the asset is used and, if possible, include a URL. 

- The name of the license (e.g., CC-BY 4.0) should be included for each asset. 

- For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided. 

- If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, `paperswithcode.com/datasets` has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset. 

44 

- For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided. 

- If this information is not available online, the authors are encouraged to reach out to the asset’s creators. 

### 13. **New Assets** 

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets? 

Answer: [NA] 

Justification: 

Guidelines: 

   - The answer NA means that the paper does not release new assets. 

   - Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc. 

   - The paper should discuss whether and how consent was obtained from people whose asset is used. 

   - At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file. 

14. **Crowdsourcing and Research with Human Subjects** 

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? 

Answer: [NA] 

Justification: 

Guidelines: 

   - The answer NA means that the paper does not involve crowdsourcing nor research with human subjects. 

   - Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper. 

   - According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector. 

15. **Institutional Review Board (IRB) Approvals or Equivalent for Research with Human Subjects** 

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained? 

Answer: [NA] 

Justification: 

Guidelines: 

- The answer NA means that the paper does not involve crowdsourcing nor research with human subjects. 

- Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. 

- We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution. 

- For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review. 

45 

