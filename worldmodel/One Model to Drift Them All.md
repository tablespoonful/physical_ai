---
title: "One Model to Drift Them All: Physics-Informed Conditional Diffusion Model for Driving at the Limits"
date: "2024"
venue: "CoRL"
url: https://proceedings.mlr.press/v270/djeumou25a.html
pdf: https://raw.githubusercontent.com/mlresearch/v270/main/assets/djeumou25a/djeumou25a.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v270/main/assets/djeumou25a/djeumou25a.pdf)** / [論文ページ](https://proceedings.mlr.press/v270/djeumou25a.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **One Model to Drift Them All: Physics-Informed Conditional Diffusion Model for Driving at the Limits** 

**Franck Djeumou**<sup>1</sup><sup>_,_2</sup> **, Thomas Lew**<sup>1</sup> **, Nan Ding**<sup>1</sup> **, Michael Thompson**<sup>1</sup> **, Makoto Suminaka**<sup>1</sup> , **Marcus Greiff**<sup>1</sup> , and **John Subosits**<sup>1</sup> 1 `Toyota Research Institute` , 2 `Rensselaer Polytechnic Institute` 

**Abstract:** Enabling autonomous vehicles to reliably operate at the limits of handling— where tire forces are saturated — would improve their safety, particularly in scenarios like emergency obstacle avoidance or adverse weather conditions. However, unlocking this capability is challenging due to the task’s dynamic nature and the high sensitivity to uncertain properties of the road, vehicle, and their dynamic interactions. Motivated by these challenges, we propose a framework to learn a conditional diffusion model for high-performance vehicle control using an unlabelled dataset containing trajectories from distinct vehicles in different environments. We design the diffusion model to capture the complex dataset’s trajectory distribution through a multimodal distribution of parameters of a physics-informed data-driven dynamics model. By conditioning the generation process on online measurements, we integrate the diffusion model into a real-time model predictive control framework for driving at the limits, and show that it can adapt on the fly to a given vehicle and environment. Extensive experiments on a Toyota Supra and a Lexus LC 500 show that a _single_ diffusion model enables reliable autonomous drifting on both vehicles when operating with different tires in varying road conditions. The model matches the performance of task-specific expert models while outperforming them in generalization to unseen conditions, paving the way towards a general, reliable method for autonomous driving at the limits of handling. 

**Keywords:** Diffusion Models, Learning for Control, Autonomous Drifting. 


Figure 1: Left: Examples of the conditional diffusion model performing drifting trajectories on two vehicles. Right: Overview of the controller architecture and online model parameter generation process. The videos of the experiments can be found at `https://tinyurl.com/diff-drift` . 

## **1 Introduction** 

Existing autonomous vehicles are constrained to operate at a fraction of their full handling potential. Designing algorithms to reliably control vehicles beyond these engineered limits would unlock faster 

8th Conference on Robot Learning (CoRL 2024), Munich, Germany. 

and more reliable responses to diverse safety-critical situations [1, 2] such as driving on ice and avoiding sudden obstacles, scenarios where the vehicle may use all of the available tire-road friction, causing it to slide across the road [3, 4, 5]. However, driving at the limits of handling is challenging due to the task’s dynamic nature, the high sensitivity to model mismatch, and the uncertain properties of the road, the vehicle, and their dynamic interactions. In addition, the high cost of collecting a dataset for driving at the limits, the complex vehicle dynamics, and the safety considerations complicate the use of imitation learning and reinforcement learning strategies. These challenges motivate the development of a model capable of exploiting physics knowledge and capturing complex forms of uncertainties while being amenable to real-time autonomous vehicle control. 

Diffusion models [6, 7, 8, 9] have shown to be highly capable of representing complex, highdimensional, and multimodal distributions from data. However, their direct use for driving at the limits is not straightforward. The limitations of classical diffusion models include the question of how to leverage prior physics knowledge to improve data efficiency and interpretability, and the considerable model inference time, which can be a bottleneck for high-bandwidth control. 

**Contribution.** We propose a conditional diffusion vehicle model for control-oriented modeling of driving at the limits of handling under uncertainties. By predicting the parameters of a physicsinformed neural stochastic differential equation dynamics model, the model has four key properties. 

- By encoding prior physics knowledge as an inductive bias, the proposed diffusion-based vehicle model is interpretable and generalizes to new environments from small amounts of data. 

- The model can capture complex multimodal distributions over the vehicle model’s parameters. 

- The model can adapt on the fly to various test-time vehicles and road conditions by conditioning on measurements of the vehicle’s interaction with the world. 

- By predicting the parameters of a physics-based model, as opposed to directly predicting state trajectories, the model inference and control loops are decoupled. This hierarchical approach unlocks diffusion sampling at low rates and high-frequency predictive control. 

We integrate the diffusion model in a real-time nonlinear model predictive control framework for autonomous driving at the friction limits, and extensively validate it on a Toyota Supra and a Lexus LC500. Our results showcase that a single diffusion model can reliably control both vehicles on challenging drifting tasks involving different road conditions and vehicle properties, see Figure 1. 

## **2 Related work** 

Several works have explored autonomous driving at the limits of handling, both in the context of racing [10, 11, 12, 13] and drifting [14, 5, 4, 15]. These methods identify the parameters of a physics-based vehicle dynamics model [16, 17, 4, 18, 19] or train a neural network model [15, 20], and subsequently use it for model-based optimal control. Nonlinear model predictive control (MPC) is the go-to control strategy in such settings and has demonstrated high-performance tracking ability in challenging racing and drifting tasks [12, 11, 4, 15]. However, the performance of MPC is limited by the fidelity of the vehicle model, designed to capture a single vehicle with given tires operating in specific road conditions. In contrast, using an unlabeled trajectory dataset, we train a single generative vehicle model with online adaptation capabilities that enable autonomous driving at the limits of handling on different vehicles in varying road conditions. 

Diffusion models have emerged as a powerful tool for generating complex and multimodal distributions in continuous domains such as images [21, 22], 3D contents [23, 24], planning and control [25, 26, 27, 28, 29, 30, 31], time series [32, 33], and physics processes [34, 35, 36]. However, all these works learn to represent, in a black-box manner, distributions for which samples are directly available in the training data. In contrast, we train a diffusion model to generate samples from a latent space of vehicle dynamics parameters that are not in the training data. Our approach relates to research in latent diffusion models [23, 37]. But instead of learning encoder and decoder networks to map between the data and latent spaces, we impose a structure on the latent space through physics-informed neural stochastic differential equations. 

Neural ordinary differential equations [38, 39, 40, 41, 42], Koopman operators [43, 44, 45, 46, 47, 48], classical system identification [49, 50, 51, 52, 53], Gaussian processes [54, 55, 56, 57, 58], and neural stochastic differential equations (SDEs) [59, 60, 61, 62, 63] have been widely studied for modeling uncertain dynamical systems from data. These models are either deterministic or can capture only a 

2 

single mode of the training dataset’s distribution, along with the uncertainty around the mode. On the other hand, Bayesian inference on the parameters of some of these models can, in theory, capture the multimodal distribution of the model parameters. However, classical Monte Carlo-based methods [64, 65, 66, 67] do not scale well with large models and datasets, while variational inference-based methods [68, 69, 70] are limited by the choice of variational family used to approximate multimodal posteriors. To address these limitations, recent works [71, 72, 73, 36] have highlighted the scalability and expressivity of diffusion models when approximating the posterior distribution in Bayesian inference. We leverage such expressivity to capture a multimodal distribution over the parameters of a vehicle model expressed as a neural SDE: A model shown in [63] to improve long-term prediction accuracy and uncertainty estimate compared to deep Gaussian-based models [74, 75]. 

Our modeling approach is similar to meta-learning methods [76, 77, 78] since the diffusion model learns offline to predict the parameters of a neural SDE model while adapting online to different vehicles and environment conditions. However, in contrast to existing meta-learning approaches where the dataset has task-specific labels, we train our model from an unlabeled dataset of vehicle trajectories. In addition, while conditioning the offline-trained diffusion model enables online adaptation, we emphasize that no gradient updates or any sort of regression on the model parameters are performed online for adaptation, as is typically done in meta-learning or online learning [79, 80, 81, 82, 83]. 

## **3 Method** 

We assume access to a dataset _T_ = _{τ_ 1 _, . . . , τ|T |}_ of vehicle trajectories _τ_ = _{_ ( _xt_ 0 _, ut_ 0) _, . . . ,_ ( _xt|τ | , ut|τ |_ ) _}_ , where each ( _xt, ut_ ) denotes a state-control pair. We denote by _xt_ :Tf = [ _xt, . . . , xt_ +Tf ] and _ut_ :Tf = [ _ut, . . . , ut_ +Tf ] the future state and control sequence from time _t_ to time _t_ +Tf , and by _x_ Tp: _t_ and _u_ Tp: _t_ the past sequence from _t −_ Tp to _t_ . We also use _τt_ :Tf _, τ_ Tp: _t_ , and _τ_ Tp: _t_ :Tf to denote Figure 2: Trajectories in _T_ . the future, past, and full sequence of state-control pairs at time _t_ , respectively. We consider that the dataset’s trajectories may be collected from vehicles with different physical and tire specifications, and operating on various road conditions while performing different tasks. Thus, the distribution over its trajectories is complex and challenging to model. The dataset is also characterized as unlabelled since no information (per trajectories) about the vehicles and environments is provided for model identification other than the state-control pairs. 

We present our approach to learning physics-constrained generative models for autonomous driving at the limits. The main idea is to integrate the structure and the existing physics knowledge of driving at the limits into the design of a neural SDE model parametrized by _θ_ . Then, we train a state-control history conditioned diffusion model, parameterized by _ψ_ , to output a distribution p _ψ_ ( _θ|x_ Tp: _t, u_ Tp: _t_ ) over the neural SDE parameters _θ_ , which is then used to generate the future state trajectories or models to use by an MPC controller. However, existing approaches to training diffusion models cannot be directly applied here as they would require unavailable access to a dataset of neural SDE parameters. The proposed approach (Section 3.1) generates such a dataset and consistently improves its parameters with respect to the trajectories in _T_ while simultaneously training the diffusion model. 

**Neural SDEs for modeling.** Neural SDEs [84, 85, 59, 60, 63] offer a principled approach for modeling uncertain dynamical systems due to their ability to encode prior physics knowledge from first principles, their calibrated uncertainties, and their expressiveness from using neural networks: 


where _x ∈X ⊆_ R<sup>_n_x</sup> is the state, _u ∈U ⊆_ R<sup>_n_u</sup> is the control input, _t_ is the time, _W_ is the _n_ x-th dimensional Wiener process, and _f_<sup>_θ_</sup> : _X × U →_ R<sup>_n_x</sup> and Σ<sup>_θ_</sup> : _X × U →_ R+<sup>_n_x</sup><sup>_×n_x</sup> are the parametrized drift and diffusion terms, respectively, and the equation is interpreted as an SDE in the Itô sense. Under smoothness assumptions [86, 87] on _f_<sup>_θ_</sup> _,_ Σ<sup>_θ_</sup> , we can efficiently sample a distribution of predicted trajectories via numerical integration of the neural SDE [88, 89]. Assuming approximate Gaussian transitions between discrete times of a numerical SDE integrator, the negative log-likelihood (NLL) loss of a state sequence _xt_ :Tf given the controls _ut_ :Tf can be estimated by 


with _∥z∥_<sup>2</sup> _A_<sup>:=</sup><sup>_z⊤Az_for</sup><sup>_z∈_R</sup><sup>_n_x,</sup><sup>_A ∈_R</sup><sup>_n_x</sup><sup>_×n_x, and where Σ</sup> _s_<sup>_θ_:= Σ</sup><sup>_θ_(˜</sup><sup>_xθ_</sup> _s_<sup>_, us_) and</sup><sup>_x_˜</sup><sup>_θ_</sup> _t_ :Tf<sup>is a sample</sup> sequence obtained from the SDE integration for a fixed _θ_ and the initial conditions _xt_ and _ut_ :Tf . 

3 

- **Algorithm 2** Online MPC Model Sampling 

- **Algorithm 1** Training of the Diffusion Model _<u>ψ</u>_ 1: Initialize history dataset _T_ hist = _∅_ . 

- 1: Initialize _D_ = _∅_ . 2: Initialize best parameters _θ_<sup>1</sup> _, . . . , θ_<sup>_n_best</sup> . 

- 2: Compute _θ_<sup>loc</sup> by solving (3) using SGD. 3: **while** not terminated **do** 

- 3: **while** not converged **do** 5:4: SampleSample _τ {_ T _τ_ Tp:p _t_ ::T _tk_ f:Tfromf _}k_ around _T_ . _τ_ Tp: _t_ :Tf . 4:5: subsets ofAppend latest _T_ gen _←{ T_ hist _τ_ Tp: ( _tkx}tk, u, Tt_ val) to _←{ T_ hist _τ_ . _tj_ :Tf _}j_ are 6:8:7: **ifend if** RefineUpdate **then** _θ_<sup>loc</sup> with p _ψ_ ( _·|h_ ( _τ_ Tp: _t_ )). 6:7: Evaluate _{θtk }k ∼_ scoresp _ψ_ ( _·|{τ_ T _J_ ptraj: _tk_ ( _}θ,k T_ ) using (val) for7). _θ ∈_ 9: Optimize for _θt_ using (4) and _θ_<sup>loc</sup> . _{θtk }k ∪{θ_<sup>_p_</sup> _}_<sup>_n_</sup> _p_ =1<sup>best.</sup> 

- 10: Append ( _τ_ Tp: _t, θt_ ) to _D_ . 8: Update Θ := _{θ_<sup>_p_</sup> _}_<sup>_n_</sup> _p_ =1<sup>bestwith best scores.</sup> 11: Update _ψ_ using (5) on batches from _D_ . 9: Send _θ_ best = argmin _J_ traj( _θ,T_ val)to MPC. 12: **end while** _θ∈_ Θ 10: **end while** 

### **3.1 Conditioned diffusion model in parameter space** 

We provide the main steps of the training process below and summarize them in Algorithm 1. 

**Initial estimate of the neural SDE parameters.** First, we compute the maximum a posteriori estimate of the neural SDE parameters _θ_ over the entire dataset _T_ . The training problem is given by 


where _J_ nll is the negative log-likelihood defined in (2), and _τ ∼T_ is a sampled trajectory from the dataset. The term _λ_ traj controls the regularization term _R_ ( _θ_ ) that enforces available prior knowledge on the neural SDE parameters; see Appendix A.4 for details on the design choices in this section. 

**Parameter dataset generation via local optimization.** Next, we use the estimate _θ_<sup>loc</sup> to iteratively generate a dataset _D_ = _{_ ( _τ_ Tp: _t, θt_ ) _, . . . }_ of short state-control trajectories _τ_ Tp: _t_ and model parameters _θt_ that are consistent with (a) the data sequence _τ_ Tp: _t_ , (b) the immediate future sequence _τt_ :Tf , and (c) additional sequences _τ_ Tp: _tk_ :Tf in a neighborhood of the initial data sequence _τ_ Tp: _t_ :Tf . The timesteps _tk_ are sampled from a uniform distribution U of fixed width centered at _t_ . The local optimal parameter _θt_ that is added to the parameters dataset _D_ is given by _θt_ = argmin _θ J_ loc( _τ_ Tp: _t, θ, θ_<sup>loc</sup> ) with 


where the term in _λ_ loc regularizes _θ_ to be close to the estimate _θ_<sup>loc</sup> . The additional sequences _τ_ Tp: _tk_ :Tf help refine the uncertainty estimates of the neural SDE model. Using short sequences _τ_ Tp: _tk_ :Tf , with _tk_ in a small time window W _∈_ R+ around _t_ , helps ensure that they can be explained by a single parameter vector _θt_ , since properties of the system may otherwise vary over a trajectory _τ_ Tp: _t_ :Tf if _τ_ Tp: _t_ :Tf is too long. We optimize for _θt_ using gradient descent on (4) starting from an initial guess sampled from a Gaussian distribution centered at _θ_<sup>loc</sup> . We found that regularizing to the estimate _θ_<sup>loc</sup> in the objective (4) stabilizes the optimization process. 

**Training the diffusion model.** Given the generated neural SDE parameters in _D_ , we update the parameters _ψ_ of our conditional denoising diffusion model with gradient descent as in [7], on a loss 


where _γk_ :=<sup>�</sup><sup>_k_</sup> _i_ =1<sup>(1</sup><sup>_−βi_) with</sup><sup>_βi∈_(0</sup><sup>_,_1) being a linear noise schedule to gradually distort the</sup> parameters dataset _D_ , _N_ ( **0** _,_ **I** ) is the standard normal distribution, _K_ is the number of diffusion steps, and _ϵψ_ is the denoising neural network predicting the noise _ϵ_ added during the noising process. Here, _h_ is a function that maps the history _τ_ Tp: _t_ to a feature space for conditioning the diffusion model: 


and ∆ _t_<sup>_−_</sup> Tp<sup>1</sup> : _t_<sup>= [(</sup><sup>_t_T</sup> p<sup>+1</sup><sup>_−t_T</sup> p<sup>)</sup><sup>_−_1</sup><sup>_, . . . ,_(</sup><sup>_tt −tt−_1)</sup><sup>_−_1].We use</sup><sup>_K_= 1000 noising steps as in [7].</sup> **Iteratively refining the parameter dataset.** As the diffusion model training progresses, its predictions of the local parameters _θt_ become more accurate while the initial estimate _θ_<sup>loc</sup> computed in (3) 

4 

may become a suboptimal initial guess for _θt_ . Thus, after some number of diffusion training steps, we use the generative model to refine the dataset _D_ by sampling a neural SDE parameter that would serve as an initial estimate _θ_<sup>loc</sup> and a regularizer for the local optimization problem (4). 

**Online diffusion model inference.** Algorithm 2 outlines a simple online strategy for sampling the neural SDE parameters conditioned on online measurements. The algorithm maintains the history of state-control pairs and uses it as a source for generating, validating, and scoring the neural SDE parameters. At each time step of the algorithm, a set _T_ gen of state-action sequences is sampled from the history dataset _T_ hist to generate a set of parameters _θt_ conditioned on each _τ_ Tp: _t ∈T_ gen. This is done in _K_ steps, by sampling _θ_<sup>¯</sup> _K ∼N_ (0 _,_ **I** ) and refining _θ_<sup>¯</sup> _k−_ 1 _∼N_ ( _µψ_ ( _θ_<sup>¯</sup> _k, k, h_ ( _τ_ Tp: _t_ )) _, σk_ **I** ) with 


### **3.2 Application to autonomous driving at the limits of handling** 

**Physics-constrained neural SDE model.** We now introduce the uncertainty-aware and physicsconstrained neural SDE model for driving at the limits of handling. We employ the commonly used single-track model [90, 16, 91, 18, 17] as a foundation to describe the nonlinear dynamics of the vehicle. The vehicle position is expressed in a curvilinear coordinate system relative to a reference trajectory [14, 19, 12]. Specifically, the position coordinate is described by the distance _s_ along the reference trajectory, the relative heading ∆ _φ_ with respect to a reference heading _φ_ ref , and the lateral deviation _e_ from the path. The proposed neural SDE model is given by 


where prior knowledge comes from the matrix M<sup>_θ_</sup> ( _·, ·_ ) that depends on vehicle parameters such as the mass _m_<sup>_θ_</sup> , yaw moment of inertia _Iz_<sup>_θ_, rotational inertia of the drivetrain</sup><sup>_I_</sup> _w_<sup>_θ_, tire radius</sup><sup>_Rθ_, and</sup> distances from the center of gravity to the front and rear axles _a_<sup>_θ_</sup> and _b_<sup>_θ_</sup> . The control input _u_ = [ _δ, τ_<sup>e</sup> ] is the steering angle and engine torque, respectively. The state _x_ = [ _r, V, β, ωr, e,_ ∆ _φ, s_ ] includes the yaw rate _r_ , velocity _V_ , sideslip angle _β_ , rear wheelspeed _ωr_ , lateral error _e_ , and angular deviation ∆ _φ_ . Lastly, _F_<sup>_θ_</sup> = [ _Fxf_<sup>_θ_,</sup><sup>_F θ_</sup> _yf_<sup>,</sup><sup>_F θ_</sup> _xr_<sup>,</sup><sup>_F θ_</sup> _yr_<sup>] represents the tire forces between the vehicle and the road.</sup> 

These unknown tire forces _F_<sup>_θ_</sup> are learned as functions of the state and control inputs. 

Modeling the dynamic interaction between the tires and the uncertain road surface is crucial for accurately controlling a vehicle at the limits of handling. To do so, we incorporate into our neural SDE model a version of the neural-ExpTanh tire model [15], a physics-informed neural tire model that captures the nonlinearities and saturation effects of tire forces, and that has shown to better predict tire forces than previous models used in the literature. We refer to Appendix A.1 for the derivations of M<sup>_θ_</sup> ( _·, ·_ ) and the neural tire force models used in the experiments. 

**Model predictive control (MPC) for autonomous drifting.** The MPC tracks a reference trajectory under actuator and actuator rate constraints by solving at each time _t_ the optimization problem 

2 minimize _u_ ¯0: _H_ E _x_ ¯1: _H_ +1�� _kH_ =1<sup>_Qβ_(¯</sup><sup>_βk −β_ref</sup><sup>_,k_)2 +</sup><sup>_Qee_¯</sup> _k_<sup>2+</sup><sup>_Qφ_</sup> ∆<sup>¯</sup> _φk_<sup>+</sup><sup>_Q_</sup> _δ_<sup>˙</sup><sup>_δ_˙</sup><sup>_k_</sup> 2 + _Qτ_ ˙ _τ_ ˙ e _k_ 2<sup>�</sup> (9a) subject to _x_ ¯ _k_ +1 = SDESolve(¯ _xk,_ ¯ _uk_ ; _θ_ best) _∀k_ = 0 _, ..., H,_ ¯ _x_ 0 = _xt, u_ ¯0: _H ∈U, u_ ¯<sup>˙</sup> 0: _H ∈ U_<sup>¯</sup> (9b) where _xk_ is the state at timestep _k_ , _x_ ¯1: _H_ +1 denotes the state trajectory over the prediction horizon of length _H_ + 1, and _u_ ¯0: _H_ are the corresponding control signals. SDESolve is any differentiable SDE integration scheme, in our case a simple Euler–Maruyama method, parameterized using the best parameters _θ_ best found by Algorithm 2. The states _x_ ¯1: _H_ +1 are thus random variables, and the expectation in (9a) is evaluated using Monte Carlo. We use 2 particles in our experiments. The system is actuated by _ut_ = _u_ ¯<sup>_⋆_</sup> 0<sup>, where</sup><sup>_u_¯</sup><sup>_⋆_</sup> 0<sup>is the optimal solution to (9) constrained with</sup><sup>_x_¯0=</sup><sup>_xt_.</sup> 

## **4 Results** 

We validate the proposed framework on two vehicles in scenarios with different tires, operating gears, and road conditions. First, we verify the capabilities of the conditional diffusion model to capture the 

5 

complexity of the unlabelled dataset and adapt its predictions online (Section 4.1). Second, we show that the model can adapt to different tires (Section 4.2). Third, we demonstrate the high performance of the method in diverse scenarios (Section 4.3). Finally, using a small amount of data collected on wet surfaces, we show that the framework enables drifting at the limits of handling in heavy rain (Section 4.4). We provide further details on the experiments in Appendix A. 

**Experimental vehicles.** We deploy the approach on a Toyota Supra and a Lexus LC500, as shown in Figure 1. The Supra is modified with a more powerful engine and more responsive actuators, whereas the Lexus is kept with factory settings, making it a particularly challenging platform for autonomous drifting. The two vehicles’ large differences in dynamics responses make them ideal platforms for evaluating the robustness and generalization capabilities of our approach. For both vehicles, we use onboard vehicle state estimation using a GPS and IMU, and we use the CPU of a ruggedized PC to run the diffusion model inference at 2Hz and compute control inputs using MPC at 200Hz. 

**Training dataset.** We train the diffusion model on a total of 84 manual and autonomous driving and drifting trajectories from the two vehicles. The duration of each trajectory is between 10 and 90 seconds. It consists of 5 manual driving trajectories pushing the car to the limits of handling, whereas the remaining trajectories are autonomous drifting experiments comprising of failed and successful attempts. The dataset includes driving Figure 3: Dataset for model training. data in different gears (affecting the effectiveness of the throttle input) and using tires with different physical properties (affecting the vehicle’s dynamics and steering input effectiveness). The composition of the dataset is summarized in Figure 3. 

**Baselines.** We compare with neural SDE dynamics models (referred to as BaseSDE or Expert depending on context) trained on specific vehicle-tire-gear subsets of the dataset in Figure 3. Each baseline is trained with the loss function in (3) and a regularization term _R_ ( _θ_ ) encoding prior knowledge about the parameters ( _m, a, b, Iz, Iw, R_ ). The resulting models are Expert since they are optimized for specific scenarios, but they may perform poorly when deployed in different conditions. 

### **4.1 Multimodality and conditioning capabilities of the diffusion model** 


Figure 4: Parameter distribution predicted by the diffusion model, when conditioned on gripping and sliding trajectories. 

We condition the model on two trajectories from the Lexus vehicle dataset (see Figure 3), where the vehicle is either accelerating in a straight line (gripping) or drifting (sliding). In Figure 4, we report two predicted parameters ( _Iw_<sup>_θ, c_</sup> 1<sup>_θ_) corresponding to the rear</sup> wheel inertia and the maximum total force that can be generated by the rear tires; see Appendix A.1. By conditioning on the straight-line (grip) trajectory, the model returns a multimodal parameter distribution due to the lack of information about tire friction properties, as tire forces are not saturated. Interestingly, by conditioning on a trajectory where the vehicle is sliding and tire forces are saturated, the model pre- 

dicts a tight unimodal distribution of the parameters. The left mode of the two parameters from the gripping phase has collapsed due to sufficient information to infer vehicle properties. This example shows that the proposed conditional diffusion model captures multimodal parameter distributions and adapts its predictions based on the information contained in the trajectory. 

### **4.2 Online adaptation to different tires** 

Table 1: Tracking error: Lexus with tires type 2. 

We further highlight the generalization capaTable 1: Tracking error: Lexus with tires type 2. bility of the proposed method by studying the Donut Figure-8 closed-loop tracking performance of the Lexus RMSE _e_ <u>(m)</u> _<u>β</u>_ <u>(deg)</u> _e_ <u>(m)</u> _<u>β</u>_ <u>(deg)</u> when operating with various tires. We report Expert <u>(Tires 2)</u> 0 _._ 35 4 _._ 08 0 _._ 32 5 _._ 17 tracking performance on two reference trajecBaseSDEBaseSDE(Tires(Tires 2 & 3) 3) 0s _._ <u>p51in</u> 4s _._ <u>p52in</u> 1s _._ <u>p39in</u> 13sp _._ in63 tories in Table 1. The controller using the Diffusion <u>(Tires 2 & 3)</u> 0 _._ 31 4 _._ 19 0 _._ 56 5 _._ 38 Expert model accurately tracks the reference trajectory. In contrast, using the baseline trained only on type 3 tire data is insufficient to track the 

6 


Figure 5: Drifting the Supra: performance comparison between the Expert and Diffusion models. 

reference, and leads to spinning out. This baseline fails to initiate the drift, due to differences in the cornering stiffness between the two tires leading to a poor prediction of how fast the vehicle will saturate the rear tires. The BaseSDE model trained on data with type 2 and type 3 tires can drift with a higher tracking error. On the donut trajectory, this baseline drifts on a circle with a larger radius due to a tire force modeling mismatch. Finally, the diffusion model quickly infers the tire properties, which results in adaptive tracking performance that matches Expert performance. 

### **4.3 Drifting performance in different scenarios** 

We evaluate the framework on a range of scenarios, including reference trajectories that are not in the dataset, and compare its performance with an Expert trained on the relevant subset of the dataset. 

**Drifting results on the Toyota Supra.** We report performance in tracking different reference trajectories in Figure 5 and Table 2. The diffusion model enables drifting maneuvers with tracking perfor- 

Table 2: Tracking error on the Toyota Supra. 

||Slalom|(gear2)|Donut|(gear1)|Figure-8|(gear2)|
|---|---|---|---|---|---|---|
|RMSE|_e_ (m)|_β_ (deg)|_e_ (m)|_β_ (deg)|_e_ (m)|_β_ (deg)|
|Expert|0_._74|5_._03|0_._31|3_._32|0_._32|3_._40|
|Diffusion|0_._72|6_._52|0_._19|2_._26|0_._57|4_._34|


mance that is comparable to expert models, while simultaneously having the advantage of being trained on an unstructured dataset. This demonstrates the model’s ability to adapt at test time to the specific vehicle setting and road condition based on the online observation. Interestingly, the framework succeeds in accurately tracking the Slalom trajectory (first column of Figure 5), which is not part of any maneuvers in the training dataset. Tracking this trajectory requires the vehicle to operate outside of the training data distribution, given the rapid changes between circles of different radii while accelerating during the last transition of the trajectory. We speculate that this ability to generalize results from the prior physics knowledge encoded in the neural SDE vehicle model. 

**Drifting results on the Lexus LC500.** Tracking results in Figure 6 and Table 3 show that using the diffusion model enables accurate tracking with performance comparable to expert models. Again, the 

|Table 3|: Track|ingerro|r: Lexu|s with t|ype 3 ti|res.|
|---|---|---|---|---|---|---|
||Donut|(gear2)|Donut|(gear1)|Figure-8|(gear1)|
|RMSE|_e_ (m)|_β_ (deg)|_e_ (m)|_β_ (deg)|_e_ (m)|_β_ (deg)|
|Expert|0_._48|3_._44|0_._38|6_._39|0_._32|3_._27|
|Diffusion|0_._82|4_._70|0_._29|4_._48|0_._34|3_._79|


proposed method is capable of performing a donut trajectory in second gear, although no second-gear trajectory from the Lexus is in the dataset. Moreover, only unsuccessful Figure-8 trajectories on the Lexus are in the dataset, yet both methods using the expert and diffusion models succeed in tracking this trajectory, thanks to the physics structure encoded in the neural SDE model. 

### **4.4 Drifting in low-friction conditions using limited data** 

7 


Figure 6: Drifting the Lexus: performance comparison between the Expert and Diffusion models. 

Lastly, we augment the dataset with 3 manual drifting trajectories collected in the rain and 4 autonomous drifting donut trajectories on a wet surface with failed and successful attempts on the Lexus vehicle. Then, we retrain the diffusion model and report the performance of the resulting controller deployed in heavy rain in Figure 7. The proposed approach is capable of drifting with only 1 _._ 47 m as the lateral RMS error ( _e_ ) and 4 _._ 79 deg as the RMS slip angle ( _β_ ) error. 

Drifting in such rainy conditions is particularly challenging. Indeed, accurate friction modeling is critical to successfully initiating the drift without spinning out, especially using a commercial vehicle such as the Lexus. Stabilizing the vehicle in rainy conditions is particularly difficult due to the increased effect of small friction variations on the handling characteristics of the vehicle, and because friction parameters vary over space due to the terrain drying unevenly over time. These results indicate that a single generative model, trained on a majority of data collected on high-friction surfaces, has the potential to enable reliable autonomous driving at the limits in both high and low-friction conditions. 


Figure 7: Tracking performance in heavy rain on a donut trajectory when drifting the Lexus. 

## **5 Conclusions** 

We propose a physics-informed generative vehicle model for autonomous driving at the limits of handling. By decoupling model inference and control, this hierarchical approach combines the expressiveness of a diffusion model with the high-rate replanning and reliability of model predictive control. Through extensive autonomous drifting experiments on a Toyota Supra and Lexus LC500, we demonstrate that a single conditional diffusion model, trained on unlabelled trajectories from both vehicles operating in various conditions, can enable adaptive, robust, and real-time autonomous driving at the limits of handling. 

**Limitations and future work.** Although the diffusion model predicts a multimodal distribution of parameters of the neural SDE vehicle dynamics model, the current model predictive controller only uses one predicted parameter set for control at a time. Fully reasoning over predicted distribution using risk-sensitive algorithms would potentially lead to additional robustness and inform data collection via active exploration to best reduce uncertainties online. Finally, while only validated on drifting tasks, the generality of the proposed hierarchical method and the experiments indicate that the approach could potentially be used in other autonomous driving and robotics applications. 

8 

## **Acknowledgments** 

We would like to thank the platform research team at Toyota Research Institute for their support with the test platforms and experiments. Special acknowledgment to Phung Nguyen and Steven Goldine for facilitating the experiments and making it possible to validate our framework under various conditions, and Jenna Lee for facilitating data logging and processing. We would also like to thank Yusei Sakamoto at Toyota Motor Corporation for the tremendous assistance in setting up our framework on their test platform, and creating an environment to validate our approach on wet surfaces and rainy conditions. 

## **References** 

- [1] A. Gray, Y. Gao, T. Lin, J. K. Hedrick, H. E. Tseng, and F. Borrelli. Predictive control for agile semi-autonomous ground vehicles using motion primitives. In <u>2012 American Control Conference (ACC), pages 4239–4244, 2012.</u> 

- [2] T. Zhao, E. Yurtsever, and G. Rizzoni. Justifying emergency drift control for automated vehicles. <u>IFAC-PapersOnLine, 55(24):141–148, 2022.</u> 

- [3] T. Gordon and M. Lidberg. Automated driving and autonomous functions on road vehicles. <u>Vehicle System Dynamics, 53(7):958–994, 2015.</u> 

- [4] J. Y. Goh, M. Thompson, J. Dallas, and A. Balachandran. Nonlinear model predictive control for highly transient autonomous drifting. 15th International Symposium on Advanced Vehicle Control, 2022. 

- [5] T. P. Weber and J. C. Gerdes. Modeling and control for dynamic drifting trajectories. <u>IEEE Transactions on Intelligent Vehicles, 2023.</u> 

- [6] J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, and S. Ganguli. Deep unsupervised learning using nonequilibrium thermodynamics. In <u>International conference on machine learning, pages</u> 2256–2265, 2015. 

- [7] J. Ho, A. Jain, and P. Abbeel. Denoising diffusion probabilistic models. <u>Advances in neural information processing systems, 33:6840–6851, 2020.</u> 

- [8] Y. Song and S. Ermon. Generative modeling by estimating gradients of the data distribution. <u>Advances in neural information processing systems, 32, 2019.</u> 

- [9] Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole. Score-based generative modeling through stochastic differential equations. In <u>International Conference on Learning Representations, 2020.</u> 

- [10] G. Williams, P. Drews, B. Goldfain, J. M. Rehg, and E. A. Theodorou. Aggressive driving with model predictive path integral control. In <u>2016 IEEE International Conference on Robotics and Automation (ICRA), pages 1433–1440, 2016.</u> 

- [11] J. Dallas, M. Thompson, J. Goh, and A. Balachandran. A hierarchical adaptive nonlinear model predictive control approach for maximizing tire force usage in autonomous vehicles. <u>Field Robotics, 3(1):222–242, 2023.</u> 

- [12] J. K. Subosits and J. C. Gerdes. Impacts of model fidelity on trajectory optimization for autonomous vehicles in extreme maneuvers. <u>IEEE Transactions on Intelligent Vehicles,</u> 6: 546–558, 2021. 

- [13] J. Dallas, M. P. Cole, P. Jayakumar, and T. Ersal. Terrain adaptive trajectory planning and tracking on deformable terrains. <u>IEEE Transactions on Vehicular Technology, 70(11):11255–</u> 11268, 2021. 

- [14] J. Y. Goh, T. Goel, and J. C. Gerdes. Toward automated vehicle control beyond the stability limits: Drifting along a general path. <u>Journal of Dynamic Systems Measurement and Control-transactions of The Asme, 142, 2019.</u> 

9 

- [15] F. Djeumou, J. Y. Goh, U. Topcu, and A. Balachandran. Autonomous drifting with 3 minutes of data via learned tire models. In <u>2023 IEEE International Conference on Robotics and Automation (ICRA), pages 968–974, 2023.</u> 

- [16] R. Rajamani. <u>Vehicle dynamics and control.</u> Springer Science & Business Media, 2011. 

- [17] P. Polack, F. Altché, B. d’Andréa Novel, and A. de La Fortelle. The kinematic bicycle model: A consistent model for planning feasible trajectories for autonomous vehicles? <u>2017 IEEE Intelligent Vehicles Symposium (IV), pages 812–818, 2017.</u> 

- [18] J. Kong, M. Pfeiffer, G. Schildbach, and F. Borrelli. Kinematic and dynamic vehicle models for autonomous driving control design. <u>2015 IEEE Intelligent Vehicles Symposium (IV), pages</u> 1094–1099, 2015. 

- [19] J. Y. Goh and J. C. Gerdes. Simultaneous stabilization and tracking of basic automobile drifting trajectories. <u>2016 IEEE Intelligent Vehicles Symposium (IV), pages 597–602, 2016.</u> 

- [20] N. A. Spielberg, M. Brown, and J. C. Gerdes. Neural network model predictive motion control applied to automated driving with unknown friction. <u>IEEE Transactions on Control Systems Technology, 30(5):1934–1945, 2021.</u> 

- [21] A. Ramesh, M. Pavlov, G. Goh, S. Gray, C. Voss, A. Radford, M. Chen, and I. Sutskever. Zero-shot text-to-image generation. In <u>International conference on machine learning,</u> pages 8821–8831, 2021. 

- [22] C. Saharia, W. Chan, S. Saxena, L. Li, J. Whang, E. L. Denton, K. Ghasemipour, R. Gontijo Lopes, B. Karagol Ayan, T. Salimans, et al. Photorealistic text-to-image diffusion models with deep language understanding. <u>Advances in neural information processing systems,</u> 35: 36479–36494, 2022. 

- [23] A. Vahdat, F. Williams, Z. Gojcic, O. Litany, S. Fidler, K. Kreis, et al. Lion: Latent point diffusion models for 3d shape generation. <u>Advances in Neural Information Processing Systems,</u> 35:10021–10039, 2022. 

- [24] L. Zhou, Y. Du, and J. Wu. 3d shape generation and completion through point-voxel diffusion. In <u>Proceedings of the IEEE/CVF international conference on computer vision, pages 5826–5835,</u> 2021. 

- [25] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. In <u>Proceedings of Robotics: Science and Systems (RSS), 2023.</u> 

- [26] A. Ajay, Y. Du, A. Gupta, J. Tenenbaum, T. Jaakkola, and P. Agrawal. Is conditional generative modeling all you need for decision-making? <u>International Conference on Learning Representations, 11, 2023.</u> 

- [27] B. Kang, X. Ma, C. Du, T. Pang, and S. Yan. Efficient diffusion policies for offline reinforcement learning. <u>Advances in Neural Information Processing Systems, 36, 2024.</u> 

- [28] T. Pearce, T. Rashid, A. Kanervisto, D. Bignell, M. Sun, R. Georgescu, S. V. Macua, S. Z. Tan, I. Momennejad, K. Hofmann, et al. Imitating human behaviour with diffusion models. <u>arXiv preprint arXiv:2301.10677, 2023.</u> 

- [29] T. Gu, G. Chen, J. Li, C. Lin, Y. Rao, J. Zhou, and J. Lu. Stochastic trajectory prediction via motion indeterminacy diffusion. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 17113–17122, 2022.</u> 

- [30] C. Jiang, A. Cornman, C. Park, B. Sapp, Y. Zhou, D. Anguelov, et al. Motiondiffuser: Controllable multi-agent motion prediction using diffusion. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 9644–9653, 2023.</u> 

- [31] D. Rempe, Z. Luo, X. Bin Peng, Y. Yuan, K. Kitani, K. Kreis, S. Fidler, and O. Litany. Trace and pace: Controllable pedestrian animation via guided trajectory diffusion. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 13756–13766,</u> 2023. 

10 

- [32] J. M. L. Alcaraz and N. Strodthoff. Diffusion-based time series imputation and forecasting with structured state space models. <u>arXiv preprint arXiv:2208.09399, 2022.</u> 

- [33] Y. Tashiro, J. Song, Y. Song, and S. Ermon. Csdi: Conditional score-based diffusion models for probabilistic time series imputation. <u>Advances in Neural Information Processing Systems, 34:</u> 24804–24816, 2021. 

- [34] B. Holzschuh, S. Vegetti, and N. Thuerey. Solving inverse physics problems with score matching. <u>Advances in Neural Information Processing Systems, 36, 2023.</u> 

- [35] G. Kohl, L.-W. Chen, and N. Thuerey. Turbulent flow simulation using autoregressive conditional diffusion models. <u>arXiv preprint arXiv:2309.01745, 2023.</u> 

- [36] Q. Liu and N. Thuerey. Uncertainty-aware surrogate models for airfoil flow simulations with denoising diffusion probabilistic models. <u>American Institute of Aeronautics and Astronautics,</u> pages 1–22, 2024. 

- [37] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer. High-resolution image synthesis with latent diffusion models. In <u>Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 10684–10695, 2022.</u> 

- [38] R. T. Chen, Y. Rubanova, J. Bettencourt, and D. Duvenaud. Neural ordinary differential equations. In <u>Proceedings of the 32nd International Conference on Neural Information Processing Systems, pages 6572–6583, 2018.</u> 

- [39] C. Rackauckas, Y. Ma, J. Martensen, C. Warner, K. Zubov, R. Supekar, D. Skinner, A. Ramadhan, and A. Edelman. Universal differential equations for scientific machine learning. <u>arXiv preprint arXiv:2001.04385, 2020.</u> 

- [40] F. Djeumou, C. Neary, E. Goubault, S. Putot, and U. Topcu. Neural networks with physicsinformed architectures and constraints for dynamical systems modeling. In <u>Proceedings of The 4th Annual Learning for Dynamics and Control Conference, volume 168, 2022.</u> 

- [41] M. Cranmer, S. Greydanus, S. Hoyer, P. Battaglia, D. Spergel, and S. Ho. Lagrangian neural networks. In <u>International Conference on Learning Representations, 2020 Workshop on Integration of Deep Neural Models and Differential Equations, 2020.</u> 

- [42] S. Greydanus, M. Dzamba, and J. Yosinski. Hamiltonian neural networks. In <u>Advances in Neural Information Processing Systems, 2019.</u> 

- [43] B. O. Koopman. Hamiltonian systems and transformation in hilbert space. <u>Proceedings of the National Academy of Sciences, 17(5):315–318, 1931.</u> 

- [44] I. Mezi´c. Spectral properties of dynamical systems, model reduction and decompositions. <u>Nonlinear Dynamics, 41:309–325, 2005.</u> 

- [45] I. Mezi´c. Analysis of fluid flows via spectral properties of the koopman operator. <u>Annual review of fluid mechanics, 45:357–378, 2013.</u> 

- [46] C. W. Rowley, I. Mezi´c, S. Bagheri, P. Schlatter, and D. S. Henningson. Spectral analysis of nonlinear flows. <u>Journal of fluid mechanics, 641:115–127, 2009.</u> 

- [47] J. L. Proctor, S. L. Brunton, and J. N. Kutz. Generalizing koopman theory to allow for inputs and control. <u>SIAM Journal on Applied Dynamical Systems, 17(1):909–930, 2018.</u> 

- [48] S. L. Brunton, M. Budiši´c, E. Kaiser, and J. N. Kutz. Modern koopman theory for dynamical systems. <u>arXiv preprint arXiv:2102.12086, 2021.</u> 

- [49] J. L. Proctor, S. L. Brunton, and J. N. Kutz. Dynamic mode decomposition with control. <u>SIAM Journal on Applied Dynamical Systems, 15(1):142–161, 2016.</u> 

- [50] E. Kaiser, J. N. Kutz, and S. L. Brunton. Sparse identification of nonlinear dynamics for model predictive control in the low-data limit. <u>Proceedings of the Royal Society A, 474(2219):</u> 20180335, 2018. 

11 

- [51] M. Korda and I. Mezi´c. Linear predictors for nonlinear dynamical systems: Koopman operator meets model predictive control. <u>Automatica, 93:149–160, 2018.</u> 

- [52] J. Coulson, J. Lygeros, and F. Dörfler. Data-enabled predictive control: In the shallows of the deepc. In <u>2019 18th European Control Conference (ECC), pages 307–312, 2019.</u> 

- [53] H. J. van Waarde, M. K. Camlibel, and M. Mesbahi. From noisy data to feedback controllers: Nonconservative design via a matrix s-lemma. <u>IEEE Transactions on Automatic Control, 67</u> (1):162–175, 2020. 

- [54] C. E. Rasmussen. <u>Gaussian processes in machine learning.</u> Springer, 2003. 

- [55] C. K. Williams and C. E. Rasmussen. <u>Gaussian processes for machine learning.</u> MIT press Cambridge, 2006. 

- [56] L. Song, J. Huang, A. Smola, and K. Fukumizu. Hilbert space embeddings of conditional distributions with applications to dynamical systems. In <u>Proceedings of the 26th Annual International Conference on Machine Learning, pages 961–968, 2009.</u> 

- [57] J. Snoek, O. Rippel, K. Swersky, R. Kiros, N. Satish, N. Sundaram, M. Patwary, M. Prabhat, and R. Adams. Scalable bayesian optimization using deep neural networks. In <u>International conference on machine learning, pages 2171–2180, 2015.</u> 

- [58] A. J. Thorpe, C. Neary, F. Djeumou, M. M. Oishi, and U. Topcu. Physics-informed kernel embeddings: Integrating prior system knowledge with data-driven control. <u>arXiv preprint arXiv:2301.03565, 2023.</u> 

- [59] B. Tzen and M. Raginsky. Neural stochastic differential equations: Deep latent gaussian models in the diffusion limit. <u>arXiv preprint arXiv:1905.09883, 2019.</u> 

- [60] P. Kidger. <u>On neural differential equations.</u> PhD thesis, University of Oxford, 2021. 

- [61] X. Li, T.-K. L. Wong, R. T. Chen, and D. K. Duvenaud. Scalable gradients and variational inference for stochastic differential equations. In <u>Symposium on Advances in Approximate Bayesian Inference, 2020.</u> 

- [62] T. Lew, S. Singh, M. Prats, J. Bingham, J. Weisz, B. Holson, X. Zhang, V. Sindhwani, Y. Lu, F. Xia, et al. Robotic table wiping via reinforcement learning and whole-body trajectory optimization. In <u>2023 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 7184–7190, 2023. 

- [63] F. Djeumou, C. Neary, and U. Topcu. How to learn and generalize from three minutes of data: Physics-constrained and uncertainty-aware neural stochastic differential equations. In <u>Conference on Robot Learning, pages 577–601, 2023.</u> 

- [64] W. K. Hastings. Monte carlo sampling methods using markov chains and their applications. <u>Biometrika, 57:97–109, 1970.</u> 

- [65] S. Chib and E. Greenberg. Understanding the metropolis-hastings algorithm. <u>The american statistician, 49(4):327–335, 1995.</u> 

- [66] R. M. Neal et al. Mcmc using hamiltonian dynamics. <u>Handbook of markov chain monte carlo,</u> 2(11):2, 2011. 

- [67] M. D. Hoffman, A. Gelman, et al. The no-u-turn sampler: adaptively setting path lengths in hamiltonian monte carlo. <u>Journal of Machine Learning Research, 15(1):1593–1623, 2014.</u> 

- [68] M. D. Hoffman, D. M. Blei, C. Wang, and J. Paisley. Stochastic variational inference. <u>Journal of Machine Learning Research, 2013.</u> 

- [69] A. Graves. Practical variational inference for neural networks. <u>Advances in neural information processing systems, 24, 2011.</u> 

- [70] D. M. Blei, A. Kucukelbir, and J. D. McAuliffe. Variational inference: A review for statisticians. <u>Journal of the American statistical Association, 112(518):859–877, 2017.</u> 

12 

- [71] L. Baldassari, A. Siahkoohi, J. Garnier, K. Solna, and M. V. de Hoop. Conditional score-based diffusion models for bayesian inference in infinite dimensions. <u>Advances in Neural Information Processing Systems, 36, 2024.</u> 

- [72] B. Kawar, G. Vaksman, and M. Elad. Snips: Solving noisy inverse problems stochastically. <u>Advances in Neural Information Processing Systems, 34:21757–21769, 2021.</u> 

- [73] Y. Song, L. Shen, L. Xing, and S. Ermon. Solving inverse problems in medical imaging with score-based generative models. <u>arXiv preprint arXiv:2111.08005, 2021.</u> 

- [74] B. Lakshminarayanan, A. Pritzel, and C. Blundell. Simple and scalable predictive uncertainty estimation using deep ensembles. <u>Advances in neural information processing systems,</u> 30, 2017. 

- [75] K. Chua, R. Calandra, R. McAllister, and S. Levine. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. <u>Advances in neural information processing systems,</u> 31, 2018. 

- [76] J. Schmidhuber. <u>Evolutionary principles in self-referential learning, or on learning how to learn: the meta-meta-... hook.</u> PhD thesis, Technische Universität München, 1987. 

- [77] A. Santoro, S. Bartunov, M. Botvinick, D. Wierstra, and T. Lillicrap. Meta-learning with memory-augmented neural networks. In <u>International conference on machine learning, pages</u> 1842–1850, 2016. 

- [78] C. Finn, P. Abbeel, and S. Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In <u>International Conference on Machine Learning, 2017.</u> 

- [79] L. Bottou. Online learning and stochastic approximations. <u>Online learning in neural networks,</u> 17(9):142, 1998. 

- [80] M. McCloskey and N. J. Cohen. Catastrophic interference in connectionist networks: The sequential learning problem. <u>Psychology of Learning and Motivation, 24:109–165, 1989.</u> 

- [81] J. Kivinen, A. Smola, and R. C. Williamson. Online learning with kernels. <u>IEEE Transactions on Signal Processing, 52:2165–2176, 2001.</u> 

- [82] T. Lew, A. Sharma, J. Harrison, A. Bylard, and M. Pavone. Safe active dynamics learning and control: A sequential exploration exploitation framework. <u>IEEE Transactions on Robotics, 38:</u> 2888–2907, 2020. 

- [83] M. P. Deisenroth, D. Fox, and C. E. Rasmussen. Gaussian processes for data-efficient learning in robotics and control. <u>IEEE Transactions on Pattern Analysis and Machine Intelligence, 37:</u> 408–423, 2015. 

- [84] R. L. Stratonovich. A new representation for stochastic integrals and equations. <u>Siam Journal on Control, 4:362–371, 1966.</u> 

- [85] K. Itô. <u>On stochastic differential equations.</u> American Mathematical Society, 1951. 

- [86] B. Øksendal. <u>Stochastic differential equations.</u> Springer Berlin Heidelberg, 2003. 

- [87] H. Kunita. <u>Stochastic flows and stochastic differential equations.</u> Cambridge university press, 1997. 

- [88] G. N. Milstein. <u>Numerical integration of stochastic differential equations.</u> Springer Science & Business Media, 1994. 

- [89] P. E. Kloeden, E. Platen, and H. Schurz. <u>Numerical solution of SDE through computer experiments.</u> Springer Science & Business Media, 2002. 

- [90] B. Paden, M. Cáp, S. Z. Yong, D. S. Yershov, and E. Frazzoli. A survey of motion planning and control techniques for self-driving urban vehicles. <u>IEEE Transactions on Intelligent Vehicles,</u> 1:33–55, 2016. 

13 

- [91] P. Falcone, F. Borrelli, J. Asgari, H. E. Tseng, and D. Hrovat. Predictive active steering control for autonomous vehicle systems. <u>IEEE Transactions on Control Systems Technology,</u> 15:566–580, 2007. 

- [92] J. Bradbury, R. Frostig, P. Hawkins, M. J. Johnson, C. Leary, D. Maclaurin, G. Necula, A. Paszke, J. VanderPlas, S. Wanderman-Milne, and Q. Zhang. JAX: composable transformations of Python+NumPy programs, 2018. URL `http://github.com/google/jax` . 

- [93] D. Kingma and J. Ba. Adam: A method for stochastic optimization. <u>International Conference on Learning Representations, 2014.</u> 

- [94] Q. Li, Y. Zhou, Y. Liang, and P. K. Varshney. Convergence analysis of proximal gradient with momentum for nonconvex optimization. In <u>International Conference on Machine Learning,</u> pages 2111–2119, 2017. 

14 

## **A Appendix** 

This section provides additional details on the neural SDE vehicle model, the experimental vehicles and training dataset, the expert models used as baselines, the diffusion model training, and the model predictive control formulation. 

We implement all the numerical experiments (training the models and the gradient-based model predictive control solver) using the Python library JAX [92] to take advantage of its automatic differentiation and just-in-time compilation features. We use Python 3 _._ 8 _._ 5 for the experiments and train all our models on a laptop computer with an Intel _⃝_ R Xeon(R) W-11855M CPU (base frequency 3.30GHz), 12 cores, 32 GB of RAM, and a GeForce RTX 2060, TU10. 

### **A.1 Physics-inspired neural SDE vehicle model** 

We employ the commonly used single-track model [90, 16, 91, 18, 17] as a foundation to describe the nonlinear dynamics of the vehicle. The vehicle position is expressed in a curvilinear coordinate system relative to a reference trajectory [14, 19, 12], as shown in Figure 8. Specifically, the position coordinate is described by the distance _s_ along the path, the relative heading ∆ _φ_ with respect to a planned course _φ_ ref , and the lateral deviation _e_ from the path. For simplicity, we assume only the steering and throttle are used for autonomous drifting and do not include brakes in the control inputs and dynamics. The proposed neural SDE model is given by 


Figure 8: Single-track model of a vehicle on a reference path. 


where vehicle-specific parameters such as the mass _m_<sup>_θ_</sup> , yaw moment of inertia _Iz_<sup>_θ_,rotational</sup> inertia of the drivetrain _Iw_<sup>_θ_, the tire radius</sup><sup>_Rθ_, and the distances from the center of gravity to the</sup> front and rear axles _a_<sup>_θ_</sup> and _b_<sup>_θ_</sup> are included in the neural SDE parameters _θ_ to learn. The control input _u_ = [ _δ, τ_<sup>e</sup> ] is the steering angle and engine torque, respectively. _E_<sup>_θ_</sup> ( _τ_<sup>e</sup> ) is a parameterized polynomial function that maps the engine torque to the wheel torque through the gear ratio _G_ . The state _x_ = [ _r, V, β, ωr, e,_ ∆ _φ, s_ ] includes the yaw rate _r_ , velocity _V_ , sideslip angle _β_ , rear wheelspeed _ωr_ , lateral error _e_ , and angular deviation ∆ _φ_ . The evolution of the path-dependent variables _e_ , ∆ _φ_ , and _s_ are well described by basic kinematics 


where _κ_ ref ( _s_ ) is the curvature of the reference path, and we use _β_<sup>˙</sup> and _s_ ˙ as an abuse of notation for the drift terms of _β_ and _s_ , respectively. Lastly, the unknown lateral and longitudinal tire forces _Fxf_<sup>_θ_,</sup> _Fyf_<sup>_θ_,</sup><sup>_F θ_</sup> _xr_<sup>, and</sup><sup>_F θ_</sup> _yr_<sup>are parametrized and learned as functions of the state and control inputs.</sup> 

15 

We propose to incorporate into our neural SDE model a version of the recently proposed neuralExpTanh [15] tire mode parameterized by 


where ExpTanh<sup>_θ_</sup> ( _z_ ; feat) := _c_ 1<sup>_θ_+</sup><sup>_cθ_</sup> 2<sup>_e−c_</sup> 3<sup>_θ|z|_</sup> tanh � _c_<sup>_θ_</sup> 4<sup>(</sup><sup>_z −cθ_</sup> 5<sup>)</sup> � is such that ( _c_<sup>_θ_</sup> _i_<sup>)5</sup> _i_ =1<sup>= NN</sup><sup>_θ_(feat) is</sup> the output of a neural network with input feat and satisfying _c_<sup>_θ_</sup> 3<sup>_, c_</sup> 4<sup>_θ≥_0 (enforced via an exponential</sup> function on the last two outputs of the neural network). Besides, _σr_ is the slip ratio, _αf_ and _αr_ are the slip angles for the front and rear tires, feat1 = [ _r, V, β_ ] and feat2 = [ _r, V, β, ωr_ ] are features for the two neural-ExpTanh models, and _c_<sup>_θ_</sup> 0<sup>and NN</sup> 0<sup>_θ_are learned to approximate the coupled effect</sup> between the longitudinal and lateral tire dynamics when the vehicle is sliding and accelerating at the same time. We note that our model has four neural networks: NN<sup>_θ_</sup> 0<sup>for the coupled effect, NN</sup> 1<sup>_θ_</sup> and NN<sup>_θ_</sup> 2<sup>for front and rear neural-ExpTanh tire models, and Σ</sup><sup>_θ_for the diffusion term.Lastly, we</sup> emphasize that although the proposed neural model assumes rear-wheel drive vehicles, it can be straightforwardly extended to other drive configurations. 

**Modeling details.** We use a diagonal matrix to represent the noise scale Σ<sup>_θ_</sup> . This design choice greatly reduces the computation of the losses (2), (3), and (4) at the cost of possibly limiting the expressivity of the model by neglecting correlations between states. However, the experiments show that the model can still capture the complex dynamics of the vehicle and enable reliable performance on diverse drifting maneuvers. The vehicle parameters _m_<sup>_θ_</sup> , _Iz_<sup>_θ_,</sup><sup>_I_</sup> _w_<sup>_θ_,</sup><sup>_Rθ_,</sup><sup>_aθ_, and</sup><sup>_bθ_are learnable scalar</sup> values optimized during training. We refer to Appendix A.3 for prior knowledge enforced on these vehicle parameters during the training of expert models, but not during the diffusion model training. The engine torque function _E_<sup>_θ_</sup> ( _τ_<sup>e</sup> ) is a linear function with learnable parameters. The parameter _c_<sup>_θ_</sup> 0<sup>is a learnable scalar value, and the neural networks NN</sup> 0<sup>_θ_, NN</sup> 1<sup>_θ_, and NN</sup><sup>_θ_</sup> 2<sup>are feedforward neural</sup> networks with two hidden layers of 6 neurons each and tanh activation functions. We do not perform any preprocessing on the training dataset and learn from raw and noisy vehicle trajectories. 

### **A.2 Experimental vehicles and training dataset** 


Figure 9: Experimental vehicles used in the study. Left: Toyota Supra. Right: Lexus LC500. 

**Experimental vehicles.** We deployed our framework on a Toyota Supra and a Lexus LC500, illustrated in Figure 9. The Supra is a prototype vehicle that has been heavily modified to become an autonomous drifting platform, while the Lexus is a commercial 2019 LC500 with its powertrain, drivetrain, and suspension unmodified from the dealership. The Supra has been modified with a 3L inline-six engine capable of outputting 380hp. The engine has been outfitted with an upgraded turbocharger that can provide an additional 300hp, for a total of 680hp. The steering system is outfitted with both hydraulic assist and electric power-assisted steering, providing high-performance steer-by-wire abilities with up to 56 _._ 7Nm of torque. The vehicle has also been modified to provide 

16 

brake-by-wire and throttle-by-wire capabilities. These modifications make the platform extremely suitable for (autonomous) Formula drift, as they allow for precise and fast control of the vehicle’s dynamics. The Lexus, on the other hand, has lower-performance actuators and is not designed to be used as a drifting vehicle. Ultimately, these two platforms have completely different dynamics, which makes them ideal for evaluating the robustness and generalization capabilities of our approach. 

We use an Oxford Technical Systems (OxTS) RT4003 v2 RTK-GPS/IMU system for localization and vehicle state estimation for both vehicles. The MPC controller is implemented on an Intel Xeon E-2278GE (base frequency 3.30GHz) CPU Linux computer mounted on board the vehicles. The computer communicates with a low-level PID controller implemented on a dSpace MicroAutoBoxII (DS1401) to track desired steering angle _δ_ and engine torque _τ_<sup>e</sup> . The MicroAutoBoxII receives commands from the MPC controller via UDP and sends actuator commands to the original equipment manufacturer’s steering and engine electronic control units. All data are synchronized and recorded at a frequency of 62 _._ 5Hz on the Lexus and 100Hz on the Supra. 

**Training dataset.** We build a dataset of manual and autonomous driving and drifting trajectories on a closed circuit from both vehicles. The dataset contains a total of 84 trajectories, each trajectory with a duration between 10 and 90 seconds. It has 5 trajectories collected from manual driving with the intent of pushing the car to the limits of handling without any specific path-tracking maneuvers planned. The remaining trajectories are from autonomous drifting experiments with 28 from the Supra and the rest from the Lexus. The supra dataset contains failed and successful attempts at performing donut maneuvers in first gear and Figure-8 maneuvers in second gear. The Lexus dataset contains attempts at performing donut maneuvers in first gear and very limited (all failed) attempts at performing "Figure-8" maneuvers in first gear. No second-gear drifting trajectories were provided in the training dataset for the Lexus. Additionally, 7% of the trajectories from the Lexus were collected with Tire 2, as opposed to Tire 3 used in the rest of the dataset. A notable difference between the two sets of tires is their cornering stiffness, which makes drift initiation strategies and tire dynamics different between the two sets of tires. 

**Training dataset for drifting on heavy rain.** We augmented the above training dataset with 7 additional drifting trajectories collected on a wet track with a vehicle identical to the Lexus LC500. 3 of the trajectories were manually collected, while the remaining 4 were collected autonomously. The autonomous trajectories were collected using second-gear drifting maneuvers only on a donut trajectory. Despite the limited number of trajectories and restriction to second-gear drifting, we show in Section 4.4 that the diffusion model trained on this dataset generalizes to drifting in heavy rain on a first-gear donut trajectory. 

### **A.3 Expert models training** 

Table 4: Prior parameters for the expert models. 

|Vehicle|_m_ (kg)|_Iz_ (kg_·_m<sup>2</sup>)|_Iw_ (kg_·_m<sup>2</sup>)|_R_ (m)|_a_ (m)|_b_ (m)|
|---|---|---|---|---|---|---|
|Toyota Supra|2048|3675|6|0_._368|1_._345|1_._522|
|Lexus LC500|1476|2241|6|0_._323|1_._239|1_._209|


We recall that the expert models in the experiments are neural SDE models trained on specific vehicle-tire subsets of the dataset. Given a subset _T_ exp of the training dataset _T_ , we train the expert models by minimizing the negative log-likelihood _J_ traj( _θ, T_ exp) defined in (3) with respect to the neural SDE parameters _θ_ defined in Appendix A.1. The regularization term _R_ ( _θ_ ) encodes a Gaussian prior on the vehicle parameters _m_<sup>_θ_</sup> , _Iz_<sup>_θ_,</sup><sup>_I_</sup> _w_<sup>_θ_,</sup><sup>_Rθ_,</sup><sup>_aθ_, and</sup><sup>_bθ_.For each parameter, we use a Gaussian</sup> prior with a mean equal to the known (estimated) parameter value for the specific vehicle and a standard deviation of 1. The resulting _R_ ( _θ_ ) is given by 


where the parameters values _m_ , _Iz_ , _Iw_ , _R_ , _a_ , and _b_ for each vehicle are provided in Table 4. The expert models are trained using Adam optimizer [93] with a learning rate of 10<sup>_−_3</sup> and a batch size of 64. We use _λ_ traj = 10<sup>_−_4</sup> for the regularization term in the loss function (3). During training, we discretize the sum in the expression of _J_ nll (see (2) for the expression and (3) for the loss function) into a sum of _N_ f = 20 discrete time steps _t_ 0 _, . . . , tN_ f , where _t_ 0 = _t_ , Tf = _tN − t_ 0, and _ti_ = _ti−_ 1 + ∆ _ti_ 

17 

for _i_ = 1 _, . . . , N_ f . We set ∆ _ti_ = U(1 _,_ 6)∆ _t_ where ∆ _t_ is typically 0 _._ 01 for trajectories on the Supra and 0 _._ 016 for trajectories on the Lexus. We randomize the time steps ∆ _ti_ during training to improve the model’s generalization when evaluated with an integration scheme that uses stepsizes other than the training stepsizes. This is typically the case when using the model in a model predictive controller; see Appendix A.5. We note that the model learns to predict state-action sequences with varying lengths Tf between 0 _._ 4 seconds and 1 _._ 96 seconds. Lastly, we use 5 particles of the neural SDE to compute the expectation in the expression of _J_ nll. 

### **A.4 Diffusion model training and online sampling** 

**Initial estimate of the neural SDE parameters.** We train the initial estimate _θ_<sup>loc</sup> of the neural SDE parameters in a similar manner to the expert models in Appendix A.3. The main difference is that we use the full training dataset _T_ instead of the vehicle-specific subset _T_ exp, and thus we do not enforce any prior knowledge on the vehicle parameters as in (15). Specifically, the regularization term _R_ ( _θ_ ) is now enforcing an uninformative Gaussian prior with mean 0 and standard deviation 1 on all the neural SDE parameters _θ_ as follows 


where _Nθ_ is the number of parameters in _θ_ , and _θ_ in defined as in Appendix A.3. 

**Parameter dataset generation via local optimization.** The hyperparameters that define this step of the diffusion model training are the regularization parameter _λ_ loc, the time window _W_ , the history length Tp, the future trajectory length Tf , and the number of sequences _τ_ Tp: _tk_ :Tf used to compute the expectation in (4). We set _λ_ loc = 10<sup>_−_3</sup> , W = 10 seconds, and the number of sequences _τ_ Tp: _tk_ :Tf to 5. In a similar manner to how we chose the time steps in the training of the expert models (see Appendix A.3), we discretize _τ_ Tp: _t_ and _τ_ Tp: _tk_ into _N_ p = 10 discrete time steps with the same randomization of the step size ∆ _ti_ as in Appendix A.3. Thus, the maximum length of the history sequence is Tp = 0 _._ 96 seconds. Besides, we keep the future trajectory length Tf to be the same as in the training of the expert models, i.e., with _N_ f = 20 discrete time steps and a maximum length of 1 _._ 96 seconds. We use 5 particles of the neural SDE to compute the expectation in the expression of _J_ nll. 

We optimize the neural SDE parameters _θ_ of the loss function (4) using gradient descent with Nesterov acceleration and an adaptive learning rate through Armijo line search. We set the maximum number of iterations to 1000 and the initial guess for the learning rate and neural SDE parameters to be respectively 0 _._ 01 and _θ_<sup>loc</sup> . 

**Diffusion model training.** We follow the procedure described in [7] to train all our diffusion models. The model _ϵψ_ defining the generative process is represented as a standard feedforward neural network with three hidden layers of 256 neurons each. We use a sinusoidal positional encoding of the diffusion step _k_ (see (5)) as an input to the neural network defining _ϵψ_ , instead of using _k_ directly as the input. The encoding is done by scaling the diffusion step and concatenating its sine and cosine to the input of a feedforward neural network with two hidden layers of 32 and 16 neurons each and swish as the activation function. We use _K_ = 1000 denoising steps, and a linear noise schedule _βi ∈_ (0 _,_ 1), where _βi_ = 0 _._ 0001 + 0 _._ 02 _i/K_ for _i_ = 0 _, . . . , K_ . We use Adam optimizer with a learning rate of 10<sup>_−_4</sup> and a batch size of 32 to train the diffusion model. Additionally, we perform 50 gradient updates of _ϵψ_ for each step of Algorithm 1. 

**Iteratively refining the parameter dataset.** Given the history sequence _τ_ Tp: _t_ , we use the diffusion generation process defined in (7) to obtain a set of parameters _{θt_<sup>_p}_100</sup> _p_ =0<sup>conditioned on</sup><sup>_τ_T</sup> p<sup>:</sup><sup>_t_.Then,</sup> we use the future sequence _τt_ :Tf to select the best parameter in terms of the negative log-likelihood _J_ nll( _θt_<sup>_p, τ_T</sup> p<sup>:</sup><sup>_t_:T</sup> f<sup>) with 5 particles of the neural SDE to compute the expectation in its expression.The</sup> obtained best parameter is then used to update _θ_<sup>loc</sup> for better initialization and regularization of the local optimization problem (4). In our experiments, we refine _θ_<sup>loc</sup> at every step of Algorithm 1 only after the initial 20000 steps of the main training loop. 

**Online diffusion model inference.** In Algorithm 2, we use a sliding window to deal with the growing size of the dataset _T_ hist and to account for changing vehicle-road properties or environment conditions. The maximum size of the sliding window _T_ hist is typically set to 30 seconds worth of 

18 

driving data. During online sampling for model predictive control, we randomly sample the set _T_ gen to contain 5 history sequences _τ_ Tp: _tj_ and the set _T_ val _⊆T_ hist to contain 30 sequences _τtl_ :Tf of the current history dataset _T_ hist. Specifically, by indexing each state-action pair _xtk , utk_ with the corresponding discrete time, we can define a discrete distribution to sample sequences _τ_ Tp: _tk_ , by sampling time indexes _tk_ and using the corresponding state-action as the endpoint of the sequence of length Tp. In our experiments, we use an exponential distribution with a higher mass on the latest time indexes in _T_ hist to generate _T_ gen. Then, to generate _T_ val, we pick the future sequences _τtj_ :Tf corresponding to the sequences of _T_ gen and sample the remaining validation sequences _τtl_ :Tf in the same manner as _T_ gen. The sequences in the validation dataset are selected to be as close as possible to the latest time in the history dataset. We use the diffusion model to generate a total of 100 parameters _{θtk }k_ conditioned on the sequences in _T_ gen, and select the best parameter according to Algorithm 2. 

### **A.5 Model predictive control formulation** 

We use a custom proximal gradient-based solver with Nesterov acceleration and Armijo line search, inspired by the approach in [94], to optimize the MPC problem 9a–9b. The state constraints, if any, and control rate constraints are enforced using slack variables, and the proximal operator for projecting the slack variables onto the feasible set. We use a first-order approximation to compute the control rate as in _u_ ¯<sup>˙</sup> _k_ = (¯ _uk_ +1 _− u_ ¯ _k_ ) _/_ ∆ _tk_ . On the other hand, the box constraints on the control input are simply enforced by projection onto the set at each iteration of the proximal gradient-based solver. 

**Reference trajectories.** The reference trajectories for the maps are generated offline via the quasiequilibrium strategy proposed in [19]. We start with a few waypoints in terms of the desired curvature _κ_ ref and sideslip angle _β_ ref as a function of path distance _s_ . Then, for each point on the path, an equilibrium point is computed using the single-track bicycle model and the conditions _κ_ = _κ_ ref , _β_ = _β_ ref , _φ_<sup>˙</sup> = _κ_ ref _V_ , and _V_<sup>˙</sup> = _r_ ˙ = 0, yielding the fine-grained reference vehicle state _x_ ref . We emphasize that the model used to generate the reference trajectories differs significantly from the neural SDE model used in the MPC controller. We reduce the over-reliance on possibly infeasible reference trajectory by using a cost function that penalizes the deviation from only in the sideslip angle _β_ and wheel speed _ωr_ , see (9a)-(9b). 

**Lexus LC500.** We use _Qβ_ = 120, _Qe_ = 2 _._ 0, _Qφ_ = 60 _._ 0, _Qδ_ ˙ = 5, and _Qτ_ ˙ = 10<sup>_−_6</sup> . The control set is given by _U_ = [ _−_ 0 _._ 52 _,_ 0 _._ 52] _×_ [ _−_ 1 _,_ 400] while the control rate set is given by _U_<sup>¯</sup> = [ _−_ 0 _._ 9 _,_ 0 _._ 9] _×_ [ _−_ 3000 _,_ 400]. The problem is optimized over a horizon _H_ = 30 with 25 short time steps of 0 _._ 05s and 5 long time steps of 0 _._ 15s. Thus, the total lookahead horizon amounts to 2s. 

**Toyota Supra.** We use _Qβ_ = 70, _Qe_ = 3 _._ 0, _Qφ_ = 30 _._ 0, _Qδ_ ˙ = 1, and _Qτ_ ˙ = 10<sup>_−_7</sup> . The control set is given by _U_ = [ _−_ 0 _._ 75 _,_ 0 _._ 75] _×_ [ _−_ 50 _,_ 350] while the control rate set is given by _U_ ¯ = [ _−_ 2 _,_ 2] _×_ [ _−_ 3000 _,_ 2000]. The problem is optimized over a horizon _H_ = 30 with 25 short time steps of 0 _._ 05s and 5 long time steps of 0 _._ 15s. Thus, the total lookahead horizon amounts to 2s. 

### **A.6 Details on the drifting experiments** 

In this section, we provide additional details on the drifting experiments conducted with the Toyota Supra and Lexus LC500 vehicles. We show the full vehicle state and control evolution when drifting on the various trajectories and road conditions, and when equipped with different tires: 

- Figure 10 shows the Lexus LC500 drifting on a first-gear donut trajectory with Tire 3. 

- Figure 11 shows the Lexus LC500 drifting on a first-gear Figure-8 trajectory with Tire 3. 

- Figure 12 shows the Lexus LC500 drifting on a second-gear donut trajectory with Tire 3. 

- Figure 13 shows the Toyota Supra drifting on a first-gear donut trajectory. 

- Figure 14 shows the Toyota Supra drifting on a second-gear Figure-8 trajectory. 

- Figure 15 shows the Toyota Supra drifting on a second-gear slalom-like trajectory. 

- Figure 16 shows the Lexus LC500 drifting on a first-gear donut trajectory with Tire 2. 

- Figure 17 shows the Lexus LC500 drifting on a first-gear Figure-8 trajectory with Tire 2. 

- Figure 18 shows the Lexus LC500 drifting on a first-gear donut trajectory on heavy rain. 

19 


Figure 10: Lexus drifting on a first-gear donut trajectory with Tire 3. 

20 


Figure 11: Lexus drifting on a first-gear Figure-8 trajectory with Tire 3. 

21 


Figure 12: Lexus drifting on a second-gear donut trajectory with Tire 3. 

22 


Figure 13: Toyota Supra drifting on a first-gear donut trajectory. 

23 


Figure 14: Toyota Supra drifting on a second-gear Figure-8 trajectory. 

24 


Figure 15: Toyota Supra drifting on a second-gear slalom-like trajectory. 

25 


Figure 16: Lexus drifting on a first-gear donut trajectory with Tire 2. 


Figure 17: Lexus drifting on a first-gear FIgure-8 trajectory with Tire 2. 

26 


Figure 18: Lexus drifting on a first-gear donut trajectory on heavy rain. 

27 

