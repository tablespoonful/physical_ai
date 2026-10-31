---
title: "Spiking Neural Networks for Continuous Control via End-to-End Model-Based Learning"
date: "2025-09-03"
authors: "Justus Huebotter; Pablo Lanillos; Marcel van Gerven; Serge Thill"
url: https://arxiv.org/abs/2509.05356
pdf: https://arxiv.org/pdf/2509.05356
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.05356)** / [論文ページ](https://arxiv.org/abs/2509.05356)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

SPIKING NEURAL NETWORKS FOR CONTINUOUS CONTROL VIA END-TO-END MODEL-BASED LEARNING 

**Justus Huebotter**<sup>**1**</sup> **, Pablo Lanillos**<sup>**1,2**</sup> **, Marcel van Gerven**<sup>**1**</sup> **, Serge Thill**<sup>**1**</sup> 

> 1 Donders Centre for Cognition, Radboud University, Nijmegen, The Netherlands 

> 2 Cajal Neuroscience Center, Spanish National Research Council, Madrid, Spain `justus.huebotter@donders.ru.nl` 

# **ABSTRACT** 

Despite recent progress in training spiking neural networks (SNNs) for classification, their application to continuous motor control remains limited. Here, we demonstrate that fully spiking architectures can be trained end-to-end to control robotic arms with multiple degrees of freedom in continuous environments. Our predictive-control framework combines Leaky Integrate-and-Fire dynamics with surrogate gradients, jointly optimizing a forward model for dynamics prediction and a policy network for goal-directed action. We evaluate this approach on both a planar 2D reaching task and a simulated 6-DOF Franka Emika Panda robot with torque control. In direct comparison to non-spiking recurrent baselines trained under the same predictive-control pipeline, the proposed SNN achieves comparable task performance while using substantially fewer parameters. An extensive ablation study highlights the role of initialization, learnable time constants, adaptive thresholds, and latent-space compression as key contributors to stable training and effective control. Together, these findings establish spiking neural networks as a viable and scalable substrate for high-dimensional continuous control, while emphasizing the importance of principled architectural and training design. 

**Keywords:** _Spiking neural networks, continuous control, robotic manipulation, surrogate gradients_ 

# **1 Introduction** 

Modern artificial intelligence has transformed robotic control into a learning problem. Classical approaches typically rely on carefully specified dynamic models; yet real-world environments often introduce significant variability and uncertainty, limiting their generality. As a result, many researchers now treat robot control as a learning task, frequently deploying artificial neural networks (ANNs) to learn control policies from data. Spiking neural networks (SNNs) offer a compelling alternative to conventional ANNs, particularly in settings where temporal dynamics and energy efficiency are central, but they also introduce additional complexity in the learning process. 

Despite these challenges, spiking networks have already proven highly effective in sensory processing, classification, and unsupervised learning (Neftci et al., 2019; Yin et al., 2021; Zenke and Ganguli, 2018; Rossbroich et al., 2022; Tavanaei et al., 2019), where their sparse, event-driven nature and internal state dynamics provide concrete advantages. These models, inspired by how biological neurons communicate, are increasingly adopted in abstract computational settings for their ability to process temporally structured input and operate with remarkable efficiency. Yet most practical machine learning, especially in continuous control, remains dominated by deep learning architectures with continuous-valued activations. 

From a neuroscience perspective, this is striking: biological brains achieve robust, adaptive, and low-latency motor behavior using spike-based communication. This offers a powerful existence proof that spike-based control can be both effective and scalable in embodied systems. However, translating this biological insight into practical machine learning systems for robotic control remains a significant challenge. 

One central challenge limiting broader use of SNNs in control settings is the difficulty of training spiking networks end-to-end for continuous tasks. Unlike standard ANNs and gated recurrent neural networks (RNNs), which benefit from smooth gradients and well-established optimization pipelines, SNNs exhibit discontinuities due to spiking non- 

linearities and require surrogate approximations to enable gradient-based learning. This has traditionally pushed spiking control research toward local plasticity, online adaptation, or indirect training paradigms, rather than principled end-to-end optimization. In the following, we review recent research on SNN control to identify the methodological gaps our approach aims to address. 

**Literature overview.** Research on spiking control spans diverse methodologies, learning approaches, and tasks, with multiple surveys synthesizing progress to date. While these studies have advanced understanding of adaptive neuron models, network architectures, bio-plausibility, local learning rules, and various hardware constraints, they often focus on aspects somewhat peripheral to scalable, general-purpose control. Several overviews emphasize the growing relevance of robotics applications (Bing et al., 2018; Lanillos et al., 2021; DeWolf, 2021; Oikonomou et al., 2025; Mompó Alepuz et al., 2024), while methodological surveys cover deep-learning-inspired SNN learning and training advances (Tavanaei et al., 2019; Neftci et al., 2019; Zenke and Vogels, 2021; Eshraghian et al., 2023; Oikonomou et al., 2025; Yamazaki et al., 2022). Together, these establish SNN control as promising but technically challenging, especially in high-dimensional continuous domains. 

One of the earliest approaches embeds analytical control equations directly into spiking networks. Slijkhuis et al. (2023) developed closed-form spike coding controllers, Agliati et al. (2025) introduced predictive spiking control for linear systems, and Traub et al. (2021a) extended this paradigm with recurrent spiking networks for dynamic action inference. Such controllers offer elegance and interpretability, drawing inspiration from control theory, but typically rely on one-step least-squares optimization rather than learning. As a result, they depend heavily on accurate system models and often lack robustness to unmodeled dynamics in real-world environments. 

Moving beyond purely analytical formulations, a large body of work has investigated bio-inspired local plasticity. Fernández et al. (2021) implemented STDP-like adaptation for robotic arm reaching, Juarez-Lora et al. (2022) applied R-STDP to arm control with changing friction, and Chen et al. (2020) developed a bio-inspired controller for a 4-DoF arm. Complementary to plasticity-driven controllers, compact bio-inspired neuromorphic SNN controllers have also been proposed to produce smooth reaching dynamics for multi-DoF arms (Polykretis et al., 2023b). Building on the Neural Engineering Framework (NEF), DeWolf et al. (2016), Iacob et al. (2020), and Marrero et al. (2024) applied NEF-based models to arm control, linking adaptive computation, cognition, and robotics, with later Loihi-based extensions to 7-DoF arms (DeWolf et al., 2023). Beyond arm reaching, Schmidgall and Hays (2023) proposed synaptic motor adaptation for locomotion, while Jiang et al. (2025) introduced a fully spiking locomotion controller. These approaches make use of data-driven adaptation and offer some biological plausibility, but they remain limited to relatively low-complexity tasks and do not yet scale to high-DoF continuous control. 

Another important direction focuses on ANN-to-SNN conversion/transfer. Representative conversion pipelines include converting trained networks for robotic inverse kinematics and control (Volinski et al., 2022), converting RL policies for event-based obstacle avoidance (Salvatore et al., 2020), and converting discrete-action DQN policies to spiking Q-networks (Patel et al., 2019). 

A closely related direction is the deployment of spiking controllers on neuromorphic hardware. As an example of directly trained spiking DRL agents targeting neuromorphic accelerators, Zanatta et al. (2023) demonstrated spiking models optimized for neuromorphic accelerators, highlighting energy efficiency benefits. Zhao et al. (2020) implemented closed-loop control on the iCub robot using DYNAP-SE, Paredes-Vallés et al. (2024) realized fully neuromorphic drone flight, and DeWolf et al. (2023) deployed Loihi-based control of a 7-DoF arm. Deployment-focused studies show the feasibility of deploying spiking control policies on neuromorphic hardware, but they are typically constrained by hardware-specific neuron models and architectural limitations, often prioritizing efficiency over generality. 

In contrast to hardware-driven or conversion-based methods, surrogate gradient techniques (Neftci et al., 2019; Zenke and Vogels, 2021) enable true end-to-end optimization in spiking domains by approximating spike derivatives, bringing deep-learning-style training into SNNs. Originally developed for classification, these methods have since been adapted to control, with stabilization strategies such as fluctuation-driven initialization further improving training dynamics (Rossbroich et al., 2022). Applied to reinforcement learning, Tang et al. (2021) used population coding for MuJoCo tasks, Chen et al. (2024) proposed noisy spiking actors to enhance exploration, Park et al. (2025) extended TD3 to 3D arm control, and Oikonomou et al. (2023) applied deep RL to 6-DoF reaching. Beyond arms, Kumar et al. (2025) developed a spiking DQN for mobile robot navigation, Traub et al. (2021b) demonstrated recurrent SNNs scaling to many-joint arms, and Zanatta et al. (2024) explored PPO-based DRL integration in robotic tasks. Together, these works highlight scalability and flexibility, overcoming many limitations of earlier local or conversion approaches. However, most efforts focus on policy optimization alone, without predictive modeling components. 

A particularly promising next step is the integration of learned predictive models into the control loop, not only for state estimation, but as generative world models capable of producing synthetic experience for policy learning (Ha and Schmidhuber, 2018; Hafner et al., 2025; Huebotter et al., 2022; Stöckl et al., 2024). This paradigm, already 

2 

transformative in the ANN-based reinforcement learning community, could help SNN controllers scale to highdimensional, long-horizon tasks without prohibitively expensive data collection. In the SNN domain, several first steps exist: Taniguchi et al. (2023) reviewed predictive coding for cognitive robotics, Agliati et al. (2025) provided a formal account of predictive spiking control, and Zhu et al. (2024) applied SNNs to autonomous driving by combining perception and planning. Beyond our control setting, recent neuromorphic-motivated work has shown that local prediction learning can support planning in high-dimensional domains (Stöckl et al., 2024), that cognitive-map structure combined with neural sampling can enable goal-directed imagination and planning (Lin et al., 2025), and that similar cognitive-map learners can be applied to mapless navigation under edge constraints (Polykretis and Danielescu, 2024). Most closely aligned with model-based RL, Capone and Paolucci (2024) proposed dreaming in recurrent SNNs, though their approach remains limited to simpler settings. Together, these works suggest that predictive modeling may help scale SNN controllers, but the joint, end-to-end optimization of predictive and control networks in fully spiking architectures for high-DoF continuous arm control remains underexplored—a gap directly addressed by the present work. 

Grouping by task domains further illustrates this methodological progression. For arm reaching, analytical formulations such as closed-form spike coding and predictive control have been explored (Slijkhuis et al., 2023; Agliati et al., 2025), followed by local plasticity and NEF-inspired approaches (Chen et al., 2020; Juarez-Lora et al., 2022; Fernández et al., 2021; DeWolf et al., 2016; Iacob et al., 2020; Marrero et al., 2024; Volinski et al., 2022). Related spiking joint-control motifs have also been explored for articulated multi-joint motion generation outside classical robotics, e.g., via evolutionarily selected spiking controllers for realistic 3D motion synthesis (Polykretis et al., 2023a). Neuromorphic deployments have extended these ideas to real-world settings, with Loihi-based 7-DoF arms (DeWolf et al., 2023) and iCub controllers implemented on DYNAP-SE (Zhao et al., 2020). More recently, surrogate-gradient-driven RL has scaled SNN controllers to high-DoF arms, including 3D reaching with TD3 (Park et al., 2025), 6-DoF hybrid RL control (Oikonomou et al., 2023), and recurrent architectures spanning many-joint systems (Traub et al., 2021b). Beyond arms, locomotion has been approached with adaptive rules (Schmidgall and Hays, 2023; Jiang et al., 2025), drones with neuromorphic controllers (Paredes-Vallés et al., 2024; Salvatore et al., 2020), mobile robot navigation (Polykretis and Danielescu, 2024), and autonomous driving with predictive frameworks (Zhu et al., 2024). Broader contributions include surveys synthesizing the field (Bing et al., 2018; Lanillos et al., 2021; Oikonomou et al., 2025), methodological advances in training (Tavanaei et al., 2019; Eshraghian et al., 2023), and stabilization techniques for scalable optimization (Rossbroich et al., 2022). Finally, predictive-model-based approaches remain in their infancy, with only initial steps toward integrating generative world models into spiking control (Capone and Paolucci, 2024; Taniguchi et al., 2023). 

Taken together, spiking control research now spans arms, locomotion, drones, and autonomous driving, utilizing local rules, analytical models, RL, conversion, and predictive approaches. Yet no systematic evaluation exists of how deep learning training tools can be effectively transferred to fully spiking architectures for generalizable prediction and control, and only a handful of works demonstrate end-to-end training that combines predictive modeling with high-DoF continuous arm control—the specific gap addressed by the present work. 

In this work, we systematically investigate how techniques from the deep learning paradigm can be adapted to train SNNs for continuous control. To this end, we introduce the predictive-control (Pred-Control) SNN model, a fully spiking, model-based control architecture composed of two trainable spiking networks (see Figure 1): a forward model that predicts future states given current sensory input and motor commands, and a policy network that infers actions based on current and target states. This structure mirrors classical forward/inverse models from control theory while enabling end-to-end optimization using surrogate gradients. Rather than relying on complex reinforcement learning pipelines or neuromorphic deployment constraints, we adopt a simpler yet sufficiently rich experimental setting: a goal-directed reaching task with a simulated robotic arm in both 2D and 3D. 

Using this framework, we show that many of the techniques that enable effective ANN training can be transferred to spiking networks, provided care is taken to stabilize dynamics and ensure smooth optimization. We demonstrate that fully spiking networks, trained end-to-end with surrogate gradients, can produce accurate, low-latency torque control for both planar and 6-DOF robotic manipulators. Through extensive ablation studies, we identify which architectural and algorithmic essential components and optional features enable stable learning and high task performance, and which offer diminishing returns. Our final models retain the adaptability and expressiveness of deep architectures while embracing the temporal and event-driven nature of spiking computation. These results support the view that SNNs, when trained with principled methods from deep learning, can function as scalable, adaptable control systems. Together, these findings offer a clear path for constructing scalable, adaptable, and biologically inspired control systems that bridge the gap between deep learning, SNNs, and low-level continuous control (motor-learning / robotics). 

The remainder of this paper is structured as follows. Section 2 introduces the Pred-Control SNN architecture in detail, including the set of training strategies evaluated for spiking networks, as well as a description of the experimental setup. 

3 

Section 3 presents the main results, with a focus on continuous control of a 3D robotic arm. Section 4 then discusses the implications and limitations of our findings and outlines promising directions for future research. An extensive Appendix complements the main text by detailing additional experiments (e.g., parameter analysis, surrogate functions comparison, initialization, training details, regularizations, etc), which were critical in shaping our methodological insights but are too detailed for inclusion in the main narrative. 

# **2 Methods** 


Figure 1: **Pred-Control SNN architecture.** The system consists of two spiking neural networks composed of LIF neurons with learnable parameters **_θ_** : a _prediction network_ **_υ_** (forward model), which receives the current robot state **_s_** _t_ and control signal **_u_** _t_ to predict the state change ∆ˆ **_s_** _t_ , and a _policy network_ **_π_** (inverse model), which takes in the current state **_s_** _t_ and target state **_s_** _t_<sup>_∗_to</sup> compute a control output **_u_** _t_ . During active control, only the policy network is used; during training, the prediction network is rolled out autoregressively to provide differentiable state estimates for optimizing the policy. Each network ends in a continuous readout layer decoding membrane voltages into output vectors. A schematic of the LIF neuron model is shown on the right. 

Table 1: **Notation summary** for task and model variables used in the Pred-Control SNN. 

|**Symbol**|**Description**|
|---|---|
|**_s_**_t_|State of the system at time_t_(e.g., joint angles, end-effector pose).|
|**_s_**<sup>_∗_</sup><br>_t_|Target state at time_t_(e.g., goal position of end-effector).|
|ˆ**_s_**_t_|Predicted system state at time_t_.|
|∆ˆ**_s_**_t_|Predicted change in state at time_t_.|
|**_u_**_t_|Control input applied to the system (e.g., torque, velocity).|
|**_x_**_t_|Input vector to the network at time_t_: **_x_**_t_ = [**_s_**_t,_**_u_**_t_]for the prediction network, and**_x_**_t_ = [**_s_**_t,_**_s_**<sup>_∗_</sup><br>_t_ <sup>] for the policy network.</sup>|
|**_y_**_t_|Network output (predicted change or control signal).|
|_I_inj_,t_|Injected current into the first spiking layer at time_t_.|
|_e_ˆ_s_|Prediction error.|
|_e_**_π_**|Policy error over a trajectory.|
|**_θ_**_υ_|Learnable parameters of the prediction network.|
|**_θ_**_π_|Learnable parameters of the policy network.|


## **2.1 Pred-Control SNN** 

Our SNN architecture is depicted in Figure 1. It draws inspiration from world models Ha and Schmidhuber (2018) and predictive coding approaches to robot control Lanillos et al. (2021); Taniguchi et al. (2023) and is composed of: _i_ ) a _prediction_ network **_υ_** , which learns to predict the robot’s future state evolution as a function of its current state and actions; and _ii_ ) a _policy_ network **_π_** , which computes the best action (continuous control signals) to apply depending on the state of the system and a given end-effector target position. Breaking up the network into two parts allows us to use 

4 

the prediction model **_υ_** to simulate state trajectories during learning of the policy model **_π_** . We can directly propagate the gradients of the distance between the predicted future positions and the target (policy loss) with respect to the policy network parameters through the prediction network. 

All neurons inside the networks are modeled as leaky integrate-and-fire (LIF) units with optional adaptive thresholds (ALIF). These neuron models introduce several time constant parameters _τ_ , which require careful tuning, as they control the temporal dynamics of information integration and eligibility traces for surrogate-gradient-based backpropagation. Details of the LIF and ALIF implementations, including time constants and reset mechanisms, are described in detail in Section 2.2 and Appendix I. For each environment time step, the SNNs are running for a set of internal sub-steps (e.g., 7) to propagate input information through the network with spike signals for sufficient temporal resolution. All networks and learning dynamics have been implemented using our Control Stork framework<sup>1</sup> (based on PyTorch) and the specific experiments for this project are available on GitHub<sup>2</sup> . All relevant hyperparameters for the final model are summarized in Appendix R. A brief overview of the notation for the following sections is given in Table 1. 

**Prediction Network** The prediction network **_υ_** comprises two spiking LIF populations and one non-spiking leaky integrator readout population. The first spiking layer includes full recurrent connectivity. Network size and architectural variants were explored empirically (see Appendix D). Its input consists of the current robot state **_s_** _t_ (joint angles, end-effector pose) and control action **_u_** _t_ (joint velocity or acceleration). The network outputs a predicted state change ∆ˆ **_s_** _t_ , which is added to the previous estimate **_s_** ˆ _t_ to yield **_s_** ˆ _t_ +1 = **_s_** ˆ _t_ + ∆ˆ **_s_** _t_ . The prediction error _es_ ˆ at time _t_ is measured by 


where _K_ denotes the dimensionality of the full state vector **_s_** _t_ . During learning this error further is averaged over a trajectory of length _T_ . All learnable parameters are summarized as **_θυ_** , yielding the compact notation **_υ_** (ˆ **_s_** _t_ +1 _|_ **_s_** _t,_ **_u_** _t,_ **_θυ_** ). For implementation and training details, refer to Appendix F. 

**Policy Network** The policy network **_π_** shares the architecture of the prediction model, except that it omits recurrent connections (see Appendix D for details). Its inputs are the current state **_s_** _t_ and target position **_s_**<sup>_∗_</sup> _t_<sup>, and it outputs an</sup> action vector **_u_** _t_ . This vector can represent joint velocity, acceleration, or torque, depending on the task. Since it is not immediately obvious whether **_u_** _t_ leads to the target, the output is evaluated by simulating the trajectory using the prediction model to obtain a new predicted position. We define the policy loss as 


where _K_<sup>_∗_</sup> refers to the subset of state dimensions describing the task-relevant target, specifically the Cartesian coordinates of the end-effector position. All learnable parameters are denoted by **_θπ_** , and we write the policy model as **_π_** ( **_u_** _t|_ **_s_** _t,_ **_s_**<sup>_∗_</sup> _t_<sup>_,_</sup><sup>**_θπ_**).See Appendix G for details.</sup> 

**Encoding and Decoding** All state and action variables are linearly rescaled to [ _−_ 1 _,_ 1] and encoded via a learned linear projection. Specifically, the scalar input vector **_x_** _t_ ([ **_s_** _t,_ **_u_** _t_ ] for prediction network, [ **_s_** _t,_ **_s_**<sup>_∗_</sup> _t_<sup>] for policy network) is</sup> linearly transformed by 


where _W_ in and **_b_** in are learned parameters. _I_ inj _,t_ serves as the input current to the first spiking layer. Injected currents are not constrained to be positive; instead, both the sign and magnitude of _I_ inj _,t_ are determined by the learned input projection, allowing negative-valued inputs to be represented naturally through negative currents. Alternative encoding schemes were explored but did not yield consistent improvements and are therefore omitted from the final model. 

To obtain the continuous-valued output vector **_y_** _t_ (actions or predictions), we use the membrane potentials _Ut_ of a non-spiking layer. These first and final weight matrices are therefore scaled differently compared to other weight parameters in the network to generate stable internal dynamics as well as output on the correct expected magnitude. The output scaling also differs for prediction and control models, as the predicted changes in state ∆ˆ **_s_** ( _t_ ) are typically much smaller than the control signals **_u_** ( _t_ ). In the policy network, a tanh activation function ensures that control outputs remain within [ _−_ 1 _,_ 1]. To mitigate saturation-induced gradient collapse, we apply an auxiliary _ℓ_ 2 penalty to the policy’s pre-tanh activations when they exceed the range [ _−_ 3 _,_ 3]. 

> 1 `https://github.com/jhuebotter/control_stork` 

> 2 `https://github.com/jhuebotter/spiking_control` 

5 

## **2.2 Leaky integrate-and-fire neuron model** 

Leaky integrate-and-fire models form a broad class of neuron models that vary in complexity, parameterization, and numerical methods (Gerstner et al., 2014). Choosing the LIF neuron model for robotics and machine learning tasks is based on a suitable trade-off between computational efficiency and biological plausibility because its simple, interpretable dynamics enable fast simulation and stable gradient-based learning, while still capturing key temporal integration properties necessary for control and sequence-based tasks. Variants of the LIF model differ in whether they include explicit synaptic currents, refractory periods, or adaptive thresholds; here, we adopt a current-based leaky integrate-and-fire (LIF) neuron with explicit synaptic current dynamics with subtractive reset and no refractory period, as this provides both computational efficiency and sufficiently rich temporal traces to support surrogate gradient learning. While a single-variable LIF model may suffice for this task, we adopt a current-based LIF with synaptic dynamics to remain compatible with the fluctuation-driven initialization of Rossbroich et al. (2022), avoiding re-derivation for a different neuron model. 

The temporal dynamics of our non-spiking LIF model are described by two differential equations for the membrane potential _U_ ( _t_ ) and synaptic current _I_ ( _t_ ): 


where _R_ is the membrane resistance, _U_ rest is the resting potential, and _tf_ are presynaptic spike times which contribute jumps of magnitude _W_ . The optional term _Iinj_ ( _t_ ) can add a bias or continuous input, while _τ_ mem and _τ_ syn set the timescales of membrane and synaptic decay. 

The LIF neurons compute firing events _S_ ( _t_ ) using a Heaviside step function Θ( _U_ ), defined by: 


When _U_ ( _t_ ) exceeds the threshold _ϑ_ , the neuron spikes and its membrane potential is reset. 

All experiments in this work are performed in discrete time using Euler updates. Let ∆ _t_ be the simulation step, and define: 


We then express the Euler updates for _I_ ( _t_ ) and the pre-reset membrane potential _U_<sup>˜</sup> _t_ as: 


Here, _U_<sup>˜</sup> _t_ is a temporary variable used to determine spiking before reset and is not an independent state variable. After computing _U_<sup>˜</sup> _t_ , we check for a spike using _St_ = Θ� _U_ ˜ _t_ �. If the neuron spikes ( _St_ = 1), the membrane potential is updated using a subtractive reset: 


We set _ϑ_ = 1 and _U_ rest = 0 for simplicity. Note that if nonzero resting potentials were desired, the reset formulation would have to be adapted accordingly. 

The complete LIF model dynamics are summarized in Algorithm 1 and visualized in Figure 2 for different settings of time constants _τ_ mem and _τ_ syn. 

Having declared the LIF dynamics for our model, there are several other choices which can be made for model training, some of which are mandatory for surrogate gradient learning, while others remain optional. 

## **2.3 Mandatory Training Considerations** 

**Surrogate Gradients** Non-differentiable spike functions are approximated with smooth surrogate gradient methods during the backward pass. We evaluated several commonly used surrogate functions (sigmoid, Gaussian Spike Yin et al. (2021), and Super Spike Zenke and Ganguli (2018)) and investigated the impact of steepness _β_ of the function on gradient magnitude and learning stability (see Appendix B). 

6 


Figure 2: **Dynamics of the LIF neuron model and the influence of temporal parameters. Left:** The membrane voltage response _U_ ( _t_ ) to a single input spike varies in amplitude and duration depending on the membrane and synaptic time constants _τ_ mem and _τ_ syn. **Center:** Full LIF temporal dynamics under three regimes of injected current _I_ inj( _t_ ): constant input, silence, and high-frequency noise. Traces show filtered current _I_ ( _t_ ), membrane potential _U_ ( _t_ ), and spike activity _S_ ( _t_ ). **Right:** Firing rate response curves over constant current injection amplitudes. The orange and light blue traces, corresponding to larger and smaller time constants respectively, show overall similar response curves but with distinct differences. While the light blue (fast) neuron requires higher input to spike, it responds more rapidly once active; the slower orange neuron integrates more gradually but yields longer activity traces. This tradeoff between response speed, firing magnitude, and trace duration critically affects not only neuronal responsiveness but also the effective temporal horizon over which surrogate gradients can propagate. Balancing these dynamics is a central challenge in the design and training of spiking neural networks. 

Algorithm 1: **Discrete-time update procedure for leaky integrate-and-fire neurons.** Each population updates its synaptic current _I_ ( _t_ ) and membrane voltage _U_ ( _t_ ) according to exponential decay dynamics, receiving weighted spike inputs _x_ ( _t_ ) and external current _I_ inj( _t_ ). Spikes _S_ ( _t_ ) are generated when the voltage exceeds the threshold _ϑ_ , after which a subtractive reset is applied. All updates are differentiable via surrogate gradients during training. 

|**for**all populations_p_in network**do**<br>_U_0 _←U_rest_, I_0 _←_0_, S_0 _←_0|_▷_Initialize population states|
|---|---|
|**for**_t ∈_[1_. . . T_]**do**||
|**for**all populations_p_in network**do**<br>_xt ←_[_St−_1_,i_ for all populations_i_projecting to_p_]|_▷_Gather spike outputs from the previous step|
|_It ←β_syn_It−_1+_W xt_+_Iinj,t_|_▷_Synaptic current update (Eq. 8)|
|˜_Ut ←β_mem_Ut−_1+<br>�<br>1_−β_mem<br>�<br>_It_<br>˜<br>|_▷_Membrane integration (Eq. 9)|
|_St ←_Θ<br>�_Ut_<br>�<br><sup>˜</sup>|_▷_Check if neuron fires (Eq. 6)|
|_Ut ←Ut −ϑ St_|_▷_Subtractive reset (Eq. 10)|


**Parameter Initialization** SNNs (similar to classic recurrent neural networks) are sensitive to weight initialization, as only certain parameter regimes yield stable behavior and effective learning. We employ a fluctuation-driven initialization (Rossbroich et al., 2022), which incorporates LIF time constants _τ_ mem and _τ_ syn into the scaling of synaptic weights, improving upon common ANN-based initialization methods. The original scheme was developed for SNNs in (temporal) classification tasks, which allows for a priori assessment of input firing rates to identify an appropriate weight scale factor _ν_ . In our case, we estimate _ν_ empirically as the training data is not known at time of network initialization and the network input is continuous instead of precomputed spike patterns. Our networks require careful tuning of parameters to achieve stable membrane potentials and gradients throughout the networks (see Appendix C). 

**Training Loops** The prediction and policy networks are trained iteratively using batches from a replay buffer. We adopt unroll-based training (truncated backpropagation through time) with _w_ = 10 environment warmup steps and teacher forcing for the transition model. The policy model is updated via autoregressive predictions through the frozen transition model Unless stated otherwise, networks are trained using mini-batches of 256 samples for 25 batches per iteration. See Appendix E, F, and G. 

**Parameter Optimization** The gradient magnitude in our networks is influenced by several factors. The LIF time constants _τ_ mem and _τ_ syn (as well as _τ_ ada for ALIF neurons) control the length of eligibility traces any given input spike 

7 

event leaves on the membrane voltage of downstream neurons. Further, the number of simulation steps _r_ , the number of SNN sub-steps per simulation step, and the total number of spike events _S_ collectively affect the risk of exploding or vanishing gradients in partially recurrent networks. Finally, the choice of surrogate gradient function and the steepness parameter _β_ scale the gradients directly. Jointly searching the parameter space quickly becomes infeasible due to the large number of degrees of freedom in this optimization problem. We found that using the adam optimizer Kingma and Ba (2014), which can dynamically adapt learning rates per parameter, proved effective in stabilizing training. As the gradient magnitudes for prediction and policy networks vary, we evaluated a number of different learning rates for each model (see Appendix A). The final learning rates used are _ατ_ = 0 _._ 01 for time constants and _α_ = 0 _._ 001 for all other parameters across both networks without decay. 

## **2.4 Optional Training Components** 

Several optional architectural and training components were evaluated to improve stability, temporal credit assignment, and parameter efficiency in spiking predictive control. Learnable membrane, synaptic, and adaptation time constants allow neurons to tune their intrinsic temporal dynamics and substantially improve convergence and final performance (Appendix H). Adaptive LIF (ALIF) neurons introduce activity-dependent thresholds that stabilize firing rates, re-engage silent neurons, and improve long-horizon credit assignment (Appendix I). Latent-space compression constrains the dimensionality of inter-layer representations, enabling wider spiking layers at fixed parameter budgets and yielding favorable performance–efficiency trade-offs (Appendix N). Additional components, including scheduled learning rates (Appendix A), weight decay (Appendix J), activity regularization (Appendix K), action penalties (Appendix L), and exploratory action noise (Appendix M), were explored but did not consistently improve final performance beyond the components above and are therefore omitted from the final model. 

## **2.5 Experimental setup** 

We evaluated Pred-Control SNNs on two simulated continuous control environments, a 2D planar arm and a 6-DOF robotic arm. Both tasks are goal-reaching problems trained end-to-end using identical data collection, unrolling, and optimization pipelines. Performance is assessed using cumulative distance to target, success rate, time on target, and prediction mean squared error (Prediction MSE). Prediction MSE is computed from autoregressive rollouts of the learned forward model and reflects long-horizon prediction accuracy rather than one-step prediction loss (see Table 2). 

**2D Planar Arm** The 2D task simulates a two-joint planar arm with fixed segment lengths in PyGame. The state includes joint angles and end-effector position, while actions specify joint accelerations. Observations are partially observable (no velocity information in state) and include mild noise, enabling fast experimentation and hyperparameter screening. The unrestricted robot joint angles are given as both sin and cos of their angle, as well as the _x_ and _y_ coordinates of the end effector and the target position. Both the state and action representations are scaled such that they lie within [ _−_ 1 _,_ 1]. 

**3D Robot Arm (6-DOF)** The 3D task uses a simulated Franka Emika Panda robot with six actuated degrees of freedom and torque control, implemented in NVIDIA Isaac Sim / Isaac Lab Mittal et al. (2023). The goal is to reach target positions in Cartesian space within a fixed distance threshold. All 3D experiments reported in this work are conducted with gravity enabled. The state representation includes joint rotations (scaled to [ _−_ 1 _,_ 1]), end-effector position, and target position. The threshold for a successful reaching attempt is defined as 0.123 m. The 3D task introduces more complex dynamics in the forward model with higher degrees of freedom and joint rotation limits. 

**Simulation Setup and Evaluation Protocol** We fix the simulation time step at ∆ _t_ = 0 _._ 02 s (50 Hz) for both the 2D and 3D tasks. 2D and 3D episodes last 200 environment steps while data is collected in parallel across 64 simulated environments. At the start of each episode, a random robot configuration is sampled to define the target end-effector position, and a new random configuration is selected for the initial state. The initial velocities are always set to zero. For evaluation, the 2D task uses 8 hand-crafted initial and target configurations shared across runs. In the 3D setting, we sample 64 fixed random initial and target states per run. Although these vary with the seed and prevent exact comparisons between runs, they offer internal consistency. Unless stated otherwise, x-axes in learning curves refer to training iterations rather than environment or network time steps. 

**Hyperparameter search** To identify a robust training configuration, we first applied the necessary methods from Section 2.3 to the 2D reaching task, to identify viable time constants ( _τ_ mem, _τ_ syn, and _τ_ ada for ALIF neurons), weight scalings (input, output, recurrent proportion _ρ_ , and expected pre-synaptic spike rate _ν_ ), learning rates ( _α_ **_υ_** and _α_ **_π_** ), surrogate gradient function (type and scale _β_ ), network architecture, batch size ( _n_ ), memory capacity ( _M_ ), and unroll 

8 

Table 2: **Overview of task performance metrics (top) and network spiking statistics (bottom).** Arrows indicate whether higher <u>(</u> _<u>↑</u>_ <u>) or lower (</u> _<u>↓</u>_ <u>) values are preferred.</u> 

|**Metric**|**Description**|**Preferred**|
|---|---|---|
|Mean Cumulative Distance|Average Euclidean distance to the target over the episode.|_↓_|
|Success Rate|Fraction of episodes in which the end-effector reaches within a fixed distance threshold<br>of the target.|_↑_|
|Time on Target|Number of time steps during which the end-effector remains within the target zone.|_↑_|
|Prediction MSE|Mean squared error of the prediction model during autoregressive rollout.|_↓_|
|Mean Active Neurons|Number of neurons that spike at least once per episode, averaged across all layers.|_↑_|
|Mean Spike Activity|Average number of spike events per episode, normalized from 0 (no spiking) to 1<br>(constant spiking). No preferred direction.|—|


steps ( _T_ **_υ_** and _T_ **_π_** ), as well as the optional methods outlined in Section 2.4. Hyperparameters optimized for the 2D task did not transfer reliably to the 3D setting, requiring task-specific retuning of temporal parameters and weight scalings. The search results are shown in the Appendix and all final hyperparameters used in the reported experiments are summarized in Appendix R. 

# **3 Results** 

We systematically evaluated the training and control performance of the Pred-Control SNN on a 6-DOF reaching task using a torque-controlled 3D robotic arm. This setup served to assess whether key components from deep learning pipelines, such as trainable time constants, adaptive thresholds, and latent-space compression, transfer effectively to fully spiking architectures. Our findings are based on extensive ablation experiments and provide several insights into SNN training dynamics and model performance. 

We compare four model classes in the main results: (i) a _full Pred-Control SNN_ (large variant, 2048 neurons per layer, _≈_ 0.9M parameters) combining learnable time constants, ALIF neurons, and latent-space compression; (ii) a _basic SNN_ that disables these components (512 neurons per layer, _≈_ 0.8M parameters); and non-spiking recurrent baselines with identical training pipelines but standard floating-point RNN modules, evaluated in both a _small_ (S) (512 neurons per layer, _≈_ 0.8M parameters) and _large_ (L) (2048 neurons per layer, _≈_ 12.7M parameters) configuration. All models are trained under identical data collection, unrolling, and optimization protocols. A more complete overview on baseline model performance is given in Appendix Q. 

As shown in Figure 3, the full Pred-Control SNN reaches comparable cumulative distance, success rate, and time-ontarget performance to the large non-spiking baseline, while using more than an order of magnitude fewer parameters. Both models substantially outperform the basic SNN, indicating that architectural extensions beyond a minimal spiking controller are required to solve the 3D task reliably. The small non-spiking baseline achieves reasonable control performance but remains consistently below both large models, highlighting the importance of model capacity for this task. 

The non-spiking baselines achieve lower Prediction MSE during long-horizon autoregressive rollouts, reflecting more accurate forward predictions. However, this advantage does not translate into improved control performance. Despite higher Prediction MSE, the full Pred-Control SNN matches or exceeds the task-level metrics of the baselines. This suggests that effective control does not require a perfectly accurate predictive model, but rather a model that is sufficiently expressive to capture task-relevant dynamics and provide stable gradients for policy optimization. 

We find that adding learnable time constants consistently improves performance, especially when paired with appropriately scaled learning rates (see Appendix H and O). This adaptation enables the model to fine-tune its intrinsic temporal dynamics in response to task demands and improves both convergence and final performance, partly mitigating the sensitivity to initialization. Notably, we found that assigning higher learning rates to time constants than to weights and biases improves convergence speed and stability without destabilizing training. 

Replacing the standard LIF neurons with adaptive LIF (ALIF) units further enhances performance (see Appendix I and O). Our ALIF neurons incorporate two key mechanisms: I) a linearly decaying threshold to force spiking behavior and II) an adaptive component that increases with recent activity and gradually relaxes back to baseline. This mechanism provides dual benefits: it enables previously inactive neurons to re-engage in encoding and learning, and it prevents persistent overactivation of units during long episodes. Together, these dynamics facilitate better credit assignment over time and help stabilize network activity during training and inference. 

9 


Figure 3: **Main results on the 3D reaching task.** Learning curves comparing a non-spiking recurrent baseline (small and large variants), a basic spiking controller, and the full Pred-Control SNN (large). Top row: task-level performance metrics (cumulative distance to target, success rate, time on target, and Prediction MSE). The Pred-Control SNN achieves task performance on par with the large non-spiking baseline despite using more than an order of magnitude fewer parameters, while clearly outperforming the basic SNN and the small non-spiking baseline. The non-spiking baselines converge slightly faster and achieve lower long-horizon prediction error, but this advantage does not translate into superior control performance. The Pred-Control SNN learns more gradually but exhibits smoother and more stable optimization dynamics. Curves show mean _±_ s.e.m. over 10 random seeds. 

We also observe clear benefits from introducing latent-space compression between the spiking layers (see Appendix N and O). This method reduces the dimensionality of inter-layer representations, enabling substantially wider spiking layers at a fixed parameter budget. In our best-performing compressed architecture, the full Pred-Control SNN with 2048 spiking neurons per layer and a 64-dimensional latent bottleneck clearly exceeds the performance of uncompressed models with similar parameter counts. The same model shows comparable performance to the large baseline, despite having _14×_ fewer parameters. While removing compression yields marginal absolute gains in some metrics, this comes at a dramatic increase in model size, indicating that compression provides an overall favorable performance–efficiency trade-off. We hypothesize that the higher neuron count improves precision in encoding and decoding continuous-valued signals, while the compression enforces a compact, task-relevant representation that aids generalization. A detailed quantitative comparison is provided in Appendix O. 

Taken together, our ablations show that each component, learnable time constants, adaptive thresholds, and latent compression, offers a clear performance benefit. Their contributions are complementary: time constant learning mitigates sensitivity to initialization, ALIF neurons enhance credit assignment, and compression improves spiking representation efficiency under parameter constraints. These findings support our design choice to combine all three in the final architecture. 

Figure 4 illustrates representative trajectories and internal network dynamics during task execution. As training progresses, end-effector trajectories become smoother and more consistent, and distance-to-target errors decrease steadily. Simultaneously, the membrane voltages and spike trains of both the prediction and policy networks stabilize, indicating that the network develops a robust internal representation of both control dynamics and task structure. Notably, as training stabilizes, spiking activity in the policy network becomes denser and more regular than in the 

10 


Figure 4: **Pred-Control SNN behavior during task execution.** Shown are 3D trajectories and Euclidean error traces (I) over the course of training, along with spiking activity (II) and voltage traces (III) from the prediction and policy networks. Top-row plots are shown over 200 environment time steps per episode. The middle and bottom rows are plotted over internal spiking model time, where each environment step corresponds to 7 spiking substeps, resulting in 1400 model time steps per episode. This distinction reflects the multi-timescale structure of the controller and is consistent across all experiments. The model exhibits progressively smoother control and more consistent activity as training proceeds. Spiking activity in the policy network becomes denser and more regular, while the prediction network shows and opposing trend. Mild oscillatory behavior near the target is visible in later training stages. 

prediction network, consistent with the policy’s role in producing continuous control signals rather than sparse statechange representations. We interpret this as a sign that the model transitions from exploration to a settled control regime. At later training stages, small oscillations around the target can be observed in the distance traces, despite high time-on-target performance. We further evaluate robustness to within-episode target shifts and observe rapid re-acquisition of perturbed targets without online learning (see Appendix P). 

11 

These experiments confirm that fully spiking networks, when equipped with adaptive temporal dynamics and efficient representations, can solve continuous, high-dimensional motor tasks with high accuracy and stability comparable to non-spiking recurrent baselines. Importantly, this is achieved with substantially fewer parameters and without requiring highly accurate long-horizon predictions, highlighting a key distinction between prediction fidelity and control effectiveness in model-based spiking systems. Altogether, our findings demonstrate that SNNs can match the functional demands of complex control settings, opening the door to scalable, adaptable, and energy-efficient spiking systems for robotics and beyond. 

# **4 Discussion and Conclusion** 

Spiking neural networks offer a compelling model of temporal computation for embodied systems, drawing inspiration from biological principles while promising advantages in energy efficiency and dynamic signal processing. Previous work has demonstrated that SNNs can be applied to continuous control, often via equation-based controllers (Slijkhuis et al., 2023; Agliati et al., 2025) or local adaptation frameworks such as the Neural Engineering Framework (DeWolf et al., 2016; Iacob et al., 2020; Marrero et al., 2024). Yet these approaches typically remain limited to low-dimensional tasks or constrained by analytical assumptions. Our work demonstrates that, when equipped with modern training tools adapted from deep learning, spiking architectures like the Pred-Control SNN can scale to high-dimensional robotic control. To our knowledge, this is the first demonstration of a fully spiking, end-to-end trainable predictivecontrol architecture operating in high-DoF continuous robotic arm tasks, helping to close a long-standing gap between biologically inspired modeling and practical machine learning. This positions our study beyond earlier demonstrations of spiking controllers, showing that deep-learning–style methods enable SNNs to function as competitive continuous controllers rather than as proof-of-concept demonstrations. 

By training our Pred-Control SNN using surrogate gradients and evaluating a suite of architectural extensions, we systematically identified several components that significantly affect performance and learning dynamics. Adaptive thresholds improved neuron participation and supported sparse activity patterns when well-tuned, consistent with prior findings on adaptive spiking neurons in classification settings (Yin et al., 2021). Decaying thresholds enabled silent neurons to reactivate over time, serving as an effective alternative to static lower-bound activity constraints. Spike regularization reduced bursting but required careful calibration to avoid performance loss. Learning time constants, especially on a per-neuron basis in log space, offered flexibility to compensate for poor initialization, echoing stabilization strategies such as fluctuation-driven initialization (Rossbroich et al., 2022), provided that their learning rates were sufficiently high. Additionally, loss shaping and latent space compression translated well from ANN training, aiding credit assignment and signal precision within the constraints of sparse spiking dynamics. Viewed together, learnable time constants, adaptive thresholds, and latent-space compression address complementary aspects of temporal credit assignment in spiking predictive control. However, their combined effect enable stable, fast, and competitive spiking control. 

A central insight emerging from our results is that prediction accuracy does not directly translate to control quality. While the non-spiking baselines achieve substantially lower long-horizon Prediction MSE, this advantage does not yield superior task-level performance. Instead, the Pred-Control SNN achieves comparable or better control despite less accurate autoregressive predictions. This suggests that effective control requires a predictive model that is sufficiently expressive to capture task-relevant dynamics and provide stable gradients for policy optimization, rather than one that minimizes prediction error in isolation. From a model-based control perspective, this aligns with the notion that approximate forward models can be entirely sufficient for planning and control when errors remain structured and bounded. 

Together, our results confirm that many principles of deep learning, including dynamic adaptation, sparsity control, and structured dimensionality reduction, are not only compatible with spiking architectures but may be essential for unleashing their potential in continuous tasks. They offer a reproducible blueprint for making SNNs robust, trainable, and effective in real-valued motor control. This moves beyond earlier demonstrations in arm reaching with STDP or NEF rules (Fernández et al., 2021; Juarez-Lora et al., 2022; DeWolf et al., 2016), neuromorphic hardware pilots (Zhao et al., 2020; DeWolf et al., 2023; Paredes-Vallés et al., 2024), or policy-focused surrogate gradient RL (Tang et al., 2021; Park et al., 2025; Oikonomou et al., 2023; Zanatta et al., 2024). In contrast, our predictive-control architecture explicitly integrates forward modeling with control, positioning this work as a step toward scalable spiking systems that unify deep learning training with predictive computation. For the neural computation audience, this suggests that SNNs can move from classification benchmarks toward the kind of adaptive, embodied computation that biological systems perform. 

Our study has limitations worth noting. First, the reliance on backpropagation-through-time introduces significant computational overhead in both memory and runtime, an issue exacerbated in SNNs due to their internal sub-timesteps 

12 

and fine-grained temporal resolution (Neftci et al., 2019; Zenke and Vogels, 2021). This imposes a bottleneck for scaling to longer task horizons, real-time execution, or complex multi-agent scenarios, and represents a central obstacle to broader applicability. Second, while our models generalize across varying initial conditions, they remain sensitive to hyperparameters such as regularization strength and adaptation rates. From a robotics or ML perspective this is a limitation, but from a neural computation perspective it may be better viewed as a result: biological systems also rely on finely tuned dynamics to maintain robustness. Future work should explore additional homeostatic mechanisms inspired by biological regulation, akin to threshold adaptation or learnable time constants. Likewise, incorporating structured connectivity patterns such as partially inhibitory lateral connections or sparsity-promoting weight matrices may enable decorrelation across neurons while preserving the benefits of distributed population codes. Finally, most existing SNN control work, including our own, currently uses rate coding for motor output and state representation, leaving the potential of alternative spike coding schemes for control largely untapped (Slijkhuis et al., 2023). 

Additionally, we observe mild oscillatory behavior near the target in some trajectories at later training stages for the Pred-Control SNN as well as the non-spiking baseline models. These oscillations occur despite high success rates and time-on-target performance and likely reflect a combination of local attractor dynamics exhibited by the policy network, limited prediction horizon, and the absence of strong action-smoothing penalties. Notably, the controller is not explicitly incentivized to come to rest at the target and the _ℓ_ 2 loss is weak close to the target position. We explored alternative loss formulations, including mixed _ℓ_ 1 _/ℓ_ 2 distance penalties designed to increase attraction toward the target center, but these did not reliably eliminate oscillations (data not shown). Similarly, action regularization reduced overall movement speed and time-on-target but did not fully suppress oscillatory behavior unless set to levels that prevented motion altogether (see Appendix L), suggesting a trade-off between control smoothness and learning efficiency. This suggests that oscillations arise not from instability in the spiking dynamics, but from an underconstrained stopping criterion in continuous control via supervised learning, a challenge shared with non-spiking controllers. Future work could explore structured action regularizers, multi-rate control schemes, or predictive uncertainty estimates to mitigate such effects without compromising performance. An alternative approach to reaching tasks in the domain of reinforcement learning is known by applying more complex reward shaping compared to a simple distance based measure, where extra rewards might be granted close to the target, to give a stronger incentive (steeper loss landscape / stronger attractor) towards the target position. 

Although spiking neural networks are often motivated by energy efficiency, our work does not explicitly optimize for sparsity or minimal spike counts. Under a rate-coding assumption, reducing spike activity necessarily trades representational precision for efficiency, which may or may not be desirable depending on task demands. For continuous motor control, population size and spike density jointly determine how finely continuous variables can be represented. In principle, equivalent control signals could be produced by larger populations with proportionally lower firing rates, or by discretized action spaces with fewer output levels. However, in the absence of explicit hardware constraints, sparsity becomes an ambiguous objective. We therefore adopt a hardware-ignorant perspective: rather than enforcing biological or neuromorphic limits, we focus on identifying architectural principles that enable robust learning and control. The reported spike activity metrics are thus interpreted as descriptive signals of network dynamics rather than direct proxies for energy consumption. Explicit energy optimization and deployment on neuromorphic hardware remain important directions for future work. 

Looking ahead, we aim to extend this architecture to reinforcement learning tasks, which introduce challenges in exploration, long-term credit assignment, and reward sparsity. Our Pred-Control SNN is well-suited for this transition due to its modularity and internal state dynamics. However, the reliance on BPTT underscores the importance of exploring alternative learning methods. Three complementary directions appear especially promising. First, online training approaches such as e-prop (Bellec et al., 2020) and forward propagation through time (Yin et al., 2023) provide more memory-efficient schemes for recurrent spiking networks. Second, noise-driven credit assignment methods such as node and weight perturbation (Züge et al., 2023) may offer biologically inspired, event-driven alternatives that scale more gracefully than full backpropagation. Third, benchmarking these methods on high-dimensional continuous control remains a crucial test. MuJoCo-style continuous control environments, already used in recent SNN-based reinforcement learning studies (Tang et al., 2021; Zanatta et al., 2024), provide a natural next step for assessing whether these algorithms can scale to complex, high-DoF robotic tasks. In parallel, we also intend to explore the generative power of model-based reinforcement learning algorithms adapted to the spiking domain, where predictive components may further reduce reliance on expensive gradient propagation. Such work will be crucial for assessing whether spiking systems can rise to the challenges of real-world robotics, offering not only compact and energy-efficient control but also biologically inspired online adaptability. 

In conclusion, this study shows that SNNs, when trained with principled, deep learning–inspired methods, can scale to high-dimensional continuous control without requiring ANN pretraining, conversion, or hardware-specific constraints. By demonstrating stable, effective motor control in end-to-end trained spiking systems, we move closer to a new generation of adaptive, low-power control systems that draw on the best of both neuroscience-inspired computation 

13 

and machine learning. Although demonstrated here in simulation, the architectural principles are hardware-agnostic and could guide deployment on emerging neuromorphic platforms, providing a pathway toward real-world, low-power robotics. This convergence between machine learning and neuroscience-inspired models points toward the next generation of intelligent, adaptive machines. 

# **Declaration of competing interest** 

The authors declare no competing interests. 

# **Data/code availability** 

The code for this project is available under `https://github.com/jhuebotter/spiking_control` . 

# **Acknowledgments** 

This work was partially supported by the Spikeference project, Human Brain Project SGA3 (Grant Agreement Nr. 945539). 

# **References** 

- Agliati, P., Urbano, A., Lanillos, P., Ahmad, N., van Gerven, M., and Keemink, S. (2025). Spiking neurons as predictive controllers of linear systems. _arXiv preprint arXiv:2507.16495_ . 

- Averbeck, B. B., Latham, P. E., and Pouget, A. (2006). Neural correlations, population coding and computation. _Nature Reviews Neuroscience_ , 7(5):358–366. 

- Bellec, G., Scherr, F., Subramoney, A., Hajek, E., Salaj, D., Legenstein, R., and Maass, W. (2020). A solution to the learning dilemma for recurrent networks of spiking neurons. _Nature communications_ , 11(1):3625. 

- Bing, Z., Meschede, C., Röhrbein, F., Huang, K., and Knoll, A. C. (2018). A survey of robotics control based on learning-inspired spiking neural networks. _Frontiers in Neurorobotics_ , 12:35. 

- Capone, C. and Paolucci, P. S. (2024). Towards biologically plausible model-based reinforcement learning in recurrent spiking networks by dreaming new experiences. _Scientific Reports_ , 14(1):14656. 

- Chen, D., Peng, P., Huang, T., and Tian, Y. (2024). Noisy spiking actor network for exploration. _arXiv preprint_ . 

- Chen, X., Zhu, W., Dai, Y., and Ren, Q. (2020). A bio-inspired spiking neural network for control of a 4-dof robotic arm. In _Conference on Industrial Electronics and Applications (ICIEA)_ , pages 616–621. IEEE. 

- Churchland, M. M., Cunningham, J. P., Kaufman, M. T., Foster, J. D., Nuyujukian, P., Ryu, S. I., and Shenoy, K. V. (2012). Neural population dynamics during reaching. _Nature_ , 487(7405):51–56. 

- DeWolf, T. (2021). Spiking neural networks take control. _Science Robotics_ , 6(58):eabk3268. 

- DeWolf, T., Patel, K., Jaworski, P., Leontie, R., Hays, J., and Eliasmith, C. (2023). Neuromorphic control of a simulated 7-dof arm using loihi. _Neuromorphic Computing and Engineering_ , 3(1):014007. 

- DeWolf, T., Stewart, T. C., Slotine, J.-J., and Eliasmith, C. (2016). A spiking neural model of adaptive arm control. _Proceedings of the Royal Society B: Biological Sciences_ , 283(1843):20162134. 

- Eshraghian, J. K., Ward, M., Neftci, E. O., Wang, X., Lenz, G., Dwivedi, G., Bennamoun, M., Jeong, D. S., and Lu, W. D. (2023). Training spiking neural networks using lessons from deep learning. _Proceedings of the IEEE_ , 111(9):1016–1054. 

- Fernández, J. P., Vargas, M. A., García, J. M. V., Carrillo, J. A. C., and Aguilar, J. J. C. (2021). A biological-like controller using improved spiking neural networks. _Neurocomputing_ , 463:237–250. 

- Gerstner, W., Kistler, W. M., Naud, R., and Paninski, L. (2014). _Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition_ . Cambridge University Press. 

- Ha, D. and Schmidhuber, J. (2018). Recurrent world models facilitate policy evolution. In _Advances in Neural Information Processing Systems_ , volume 31. Curran Associates, Inc. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. (2025). Mastering diverse control tasks through world models. _Nature_ , pages 1–7. 

- Huebotter, J., Thill, S., van Gerven, M., and Lanillos, P. (2022). Learning policies for continuous control via transition models. In _International Workshop on Active Inference_ , pages 162–178. Springer, Springer. 

- Iacob, S., Kwisthout, J., and Thill, S. (2020). From models of cognition to robot control and back using spiking neural networks. In _Biomimetic and Biohybrid Systems_ , pages 176–191. Springer, Springer. 

14 

- Jiang, X., Zhang, Q., Sun, J., Cao, J., Ma, J., and Xu, R. (2025). Fully spiking neural network for legged robots. In _International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ , pages 1–5. IEEE. 

- Juarez-Lora, A., Ponce-Ponce, V. H., Sossa, H., and Rubio-Espino, E. (2022). R-stdp spiking neural network architecture for motion control on a changing friction joint robotic arm. _Frontiers in Neurorobotics_ , 16:904017. 

- Kingma, D. P. and Ba, J. (2014). Adam: A method for stochastic optimization. _arXiv preprint_ . 

- Kumar, A., Zhang, L., Bilal, H., Wang, S., Shaikh, A. M., Bo, L., Rohra, A., and Khalid, A. (2025). Dsqn: Robust path planning of mobile robot based on deep spiking q-network. _Neurocomputing_ , 634:129916. 

- Lanillos, P., Meo, C., Pezzato, C., Meera, A. A., Baioumy, M., Ohata, W., Tschantz, A., Millidge, B., Wisse, M., Buckley, C. L., et al. (2021). Active inference in robotics and artificial agents: Survey and challenges. _arXiv preprint_ . 

- Lin, H., Yang, Y., Zhao, R., Pezzulo, G., and Maass, W. (2025). Neural sampling from cognitive maps enables goal-directed imagination and planning. _bioRxiv preprint_ . 

- Marrero, D., Kern, J., and Urrea, C. (2024). A novel robotic controller using neural engineering framework-based spiking neural networks. _Sensors_ , 24(2):491. 

- Mittal, M., Yu, C., Yu, Q., Liu, J., Rudin, N., Hoeller, D., Yuan, J. L., Singh, R., Guo, Y., Mazhar, H., Mandlekar, A., Babich, B., State, G., Hutter, M., and Garg, A. (2023). Orbit: A unified simulation framework for interactive robot learning environments. _IEEE Robotics and Automation Letters_ , 8(6):3740–3747. 

- Mompó Alepuz, A., Papageorgiou, D., and Tolu, S. (2024). Brain-inspired biomimetic robot control: a review. _Frontiers in Neurorobotics_ , 18:1395617. 

- Neftci, E. O., Mostafa, H., and Zenke, F. (2019). Surrogate gradient learning in spiking neural networks: Bringing the power of gradient-based optimization to spiking neural networks. _IEEE Signal Processing Magazine_ , 36(6):51–63. 

- Oikonomou, K. M., Kansizoglou, I., and Gasteratos, A. (2023). A hybrid spiking neural network reinforcement learning agent for energy-efficient object manipulation. _Machines_ , 11(2):162. 

- Oikonomou, K. M., Kansizoglou, I., and Gasteratos, A. (2025). Reinforcement learning with spiking neural networks for robotic applications: A survey. _Authorea Preprints_ . 

- Paredes-Vallés, F., Hagenaars, J. J., Dupeyroux, J., Stroobants, S., Xu, Y., and de Croon, G. C. H. E. (2024). Fully neuromorphic vision and control for autonomous drone flight. _Science Robotics_ , 9(90):eadi0591. 

- Park, Y., Lee, J., Sim, D., Cho, Y., and Park, C. (2025). Designing spiking neural network-based reinforcement learning for 3d robotic arm applications. _Electronics_ , 14(3). 

- Patel, D., Hazan, H., Saunders, D. J., Siegelmann, H. T., and Kozma, R. (2019). Improved robustness of reinforcement learning policies upon conversion to spiking neuronal network platforms applied to atari breakout game. _Neural Networks_ , 120:108–115. 

- Polykretis, I. and Danielescu, A. (2024). Mapless mobile robot navigation at the edge using self-supervised cognitive map learners. _Frontiers in Robotics and AI_ , 11:1372375. 

- Polykretis, I., Patil, A., Aanjaneya, M., and Michmizos, K. (2023a). An interactive framework for visually realistic 3d motion synthesis using evolutionarily-trained spiking neural networks. _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , 6(1):1–19. 

- Polykretis, I., Supic, L., and Danielescu, A. (2023b). Bioinspired smooth neuromorphic control for robotic arms. _Neuromorphic Computing and Engineering_ , 3(1):014013. 

- Rossbroich, J., Gygax, J., and Zenke, F. (2022). Fluctuation-driven initialization for spiking neural network training. _Neuromorphic Computing and Engineering_ , 2(4):044016. 

- Salvatore, N., Mian, S., Abidi, C., and George, A. D. (2020). A neuro-inspired approach to intelligent collision avoidance and navigation. In _2020 AIAA/IEEE 39th Digital Avionics Systems Conference (DASC)_ , pages 1–9. IEEE. 

- Schmidgall, S. and Hays, J. (2023). Synaptic motor adaptation: A three-factor learning rule for adaptive robotic control in spiking neural networks. In _Proceedings of the 2023 International Conference on Neuromorphic Systems_ , pages 1–9. Association for Computing Machinery. 

- Slijkhuis, F. S., Keemink, S. W., and Lanillos, P. (2023). Closed-form control with spike coding networks. _IEEE Transactions on Cognitive and Developmental Systems_ , 16(5):1677–1687. 

- Stöckl, C., Yang, Y., and Maass, W. (2024). Local prediction-learning in high-dimensional spaces enables neural networks to plan. _Nature Communications_ , 15(1):2344. 

- Tang, G., Kumar, N., Yoo, R., and Michmizos, K. (2021). Deep reinforcement learning with population-coded spiking neural network for continuous control. In _Conference on Robot Learning_ , pages 2016–2029. PMLR. 

- Taniguchi, T., Murata, S., Suzuki, M., Ognibene, D., Lanillos, P., Ugur, E., Jamone, L., Nakamura, T., Ciria, A., Lara, B., et al. (2023). World models and predictive coding for cognitive and developmental robotics: Frontiers and challenges. _Advanced Robotics_ , 37(13):780–806. 

- Tavanaei, A., Ghodrati, M., Kheradpisheh, S. R., Masquelier, T., and Maida, A. (2019). Deep learning in spiking neural networks. _Neural Networks_ , 111:47–63. 

15 

- Traub, M., Butz, M. V., Legenstein, R., and Otte, S. (2021a). Dynamic action inference with recurrent spiking neural networks. In _International Conference on Artificial Neural Networks_ , pages 233–244. Springer, Springer. 

- Traub, M., Legenstein, R., and Otte, S. (2021b). Many-joint robot arm control with recurrent spiking neural networks. In _International Conference on Intelligent Robots and Systems (IROS)_ , pages 4918–4925. IEEE. 

- Volinski, A., Zaidel, Y., Shalumov, A., DeWolf, T., Supic, L., and Tsur, E. E. (2022). Data-driven artificial and spiking neural networks for inverse kinematics in neurorobotics. _Patterns_ , 3(1). 

- Yamazaki, K., Vo-Ho, V.-K., Bulsara, D., and Le, N. (2022). Spiking neural networks and their applications: A review. _Brain sciences_ , 12(7):863. 

- Yin, B., Corradi, F., and Bohté, S. M. (2021). Accurate and efficient time-domain classification with adaptive spiking recurrent neural networks. _Nature Machine Intelligence_ , 3(10):905–913. 

- Yin, B., Corradi, F., and Bohté, S. M. (2023). Accurate online training of dynamical spiking neural networks through forward propagation through time. _Nature Machine Intelligence_ , 5(5):518–527. 

- Zanatta, L., Barchi, F., Manoni, S., Tolu, S., Bartolini, A., and Acquaviva, A. (2024). Exploring spiking neural networks for deep reinforcement learning in robotic tasks. _Scientific Reports_ , 14(1):30648. 

- Zanatta, L., Di Mauro, A., Barchi, F., Bartolini, A., Benini, L., and Acquaviva, A. (2023). Directly-trained spiking neural networks for deep reinforcement learning: Energy efficient implementation of event-based obstacle avoidance on a neuromorphic accelerator. _Neurocomputing_ , 562:126885. 

- Zenke, F. and Ganguli, S. (2018). Superspike: Supervised learning in multilayer spiking neural networks. _Neural Computation_ , 30(6):1514–1541. 

- Zenke, F. and Vogels, T. P. (2021). The remarkable robustness of surrogate gradient learning for instilling complex function in spiking neural networks. _Neural Computation_ , 33(4):899–925. 

- Zhao, J., Risi, N., Monforte, M., Bartolozzi, C., Indiveri, G., and Donati, E. (2020). Closed-loop spiking control on a neuromorphic processor implemented on the icub. _IEEE Journal on Emerging and Selected Topics in Circuits and Systems_ , 10(4):546–556. 

- Zhu, R.-J., Wang, Z., Gilpin, L., and Eshraghian, J. (2024). Autonomous driving with spiking neural networks. In _Advances in Neural Information Processing Systems_ , volume 37. Curran Associates, Inc. 

- Züge, P., Klos, C., and Memmesheimer, R.-M. (2023). Weight versus node perturbation learning in temporally extended tasks: Weight perturbation often performs similarly or better. _Phys. Rev. X_ , 13:021006. 

16 

# **A Learning Rate** _α_ 

As with most neural network training regimes, the learning rate is one of the most critical hyperparameters. Its appropriate setting depends on several factors, including the choice of optimizer, the magnitude of the gradients, and the curvature of the loss landscape. A common strategy is to begin with a relatively high learning rate to enable rapid initial learning and then reduce it gradually to promote convergence and stability. 

In this experiment, we investigate suitable learning rates for two separately trained networks: the policy network **_π_** and the prediction (dynamics) model **_υ_** . Their respective learning rates are denoted as _α_ **_π_** and _α_ **_υ_** . We treat both as independent hyperparameters and sample their values logarithmically between 10<sup>_−_5</sup> and 10<sup>_−_1</sup> . Training is performed using the Adam optimizer Kingma and Ba (2014) for both networks, due to its adaptive update rules and strong empirical performance across a wide range of tasks. 

While most configurations reduce the cumulative distance and increase the success rate to some extent, the clearest separation between well- and poorly-performing models is observed in the time-on-target metric (see Figure 5). This measure integrates both accuracy and stability over time and proves more sensitive than raw loss values, which can decrease even when control performance remains poor. 

Notably, the best performance is achieved when both networks use a learning rate of _α_ **_π_** = _α_ **_υ_** = 10<sup>_−_3</sup> , which was also selected for all subsequent experiments. Across all configurations, the recorded gradient norms remain within a stable range and do not exhibit signs of vanishing or exploding. However, their absolute magnitude shows little correlation with task performance: both poorly and well-performing models can exhibit similarly sized gradients. This suggests that gradient norm alone is not a reliable indicator of effective learning progress or eventual task success. Instead, successful training depends more critically on the interaction between the learning rates and the underlying optimization landscape. It is plausible that the Adam optimizer mitigates the effects of absolute gradient scale differences, allowing training to remain numerically stable even when learning progress diverges. 

The results further highlight an asymmetry in the dependency between the two networks: if the prediction model learns poorly, policy optimization fails due to inaccurate gradients. However, the prediction model can converge even when the policy performs suboptimally, as it is trained independently on state transitions. 

Taken together, these findings highlight the importance of co-tuning learning rates and reinforce the central role of accurate dynamics in enabling effective policy optimization. 

**Scheduled Learning Rates.** To modulate the learning rate during training, we apply an exponentially decaying schedule defined by a decay factor _γ ∈{_ 1 _._ 0 _,_ 0 _._ 99 _,_ 0 _._ 97 _,_ 0 _._ 9 _}_ , where _γ_ = 1 _._ 0 corresponds to a constant learning rate. Decay is applied once per epoch according to _αt_ = max( _γ_<sup>_t_</sup> _α_ 0 _, α_ min), with _α_ min = 0 _._ 0001 ensuring that learning does not halt entirely in later training stages. 

We evaluate the effect of exponential decay schedules on training stability and performance for both the policy and prediction networks. Each decay factor is tested with initial learning rates of _α_ 0 = 10<sup>_−_3</sup> , the best-performing value identified previously—and a larger alternative _α_ 0 = 10<sup>_−_2</sup> . 

As shown in Figure 6, decay schedules can compensate for overly aggressive initial rates to some extent, but do not yield improvements over the constant baseline. This is particularly clear in the time-on-target metric, which remains highest and most stable for the non-decayed 10<sup>_−_3</sup> setting. More aggressive decay (e.g., _γ_ = 0 _._ 9) reduces the effective learning rate too quickly and leads to premature plateauing, while milder decay schedules offer no tangible advantage. 

Overall, exponential decay provides a degree of robustness in unstable configurations but does not improve performance when a well-tuned constant learning rate is already available. It is plausible that the Adam optimizer already compensates for learning rate scale variations through its adaptive update mechanism, reducing the potential benefits of external scheduling. For simplicity and consistency, we therefore use a constant learning rate of _α_ = 10<sup>_−_3</sup> for both networks in all subsequent experiments. 

17 


Figure 5: **Effect of learning rates** _α_ **_π_ and** _α_ **_υ_ on training in the 2D control task.** We vary _α_ **_υ_** across columns and _α_ **_π_** across line colors. Performance is most easily distinguished by the time spent on target (row 3), which clearly peaks when both networks use _α_ = 10<sup>_−_3</sup> . Learning stability is preserved across all settings, with no signs of vanishing or exploding gradients, yet performance still varies markedly with learning rate choice. The policy is sensitive to prediction quality, but the inverse does not hold: policy failure does not impair model learning. Overall, the best choice of parameter based on the performance metrics was found at _α_ **_π_** = _α_ **_υ_** = 10<sup>_−_3</sup> . 

18 


Figure 6: **Exponential learning rate decay. Top:** Exponential decay schedules for different values of _γ_ , starting from _α_ 0 = 0 _._ 001. All schedules are bounded below by _α_ min = 0 _._ 0001 to prevent the learning rate from vanishing entirely. **Bottom:** Control performance for different decay factors _γ_ and two initial learning rates _α_ init _∈{_ 10<sup>_−_3</sup> _,_ 10<sup>_−_2</sup> _}_ , applied symmetrically to both networks. While exponential decay mitigates instability at higher initial learning rates, performance on cumulative distance and success rate remains similar across all settings. The time-on-target metric reveals a consistent advantage for the constant 10<sup>_−_3</sup> schedule. 

19 

# **B Surrogate Gradient Function** _f_<sup>_′_</sup> ( _U_ ) 

Training spiking neural networks (SNNs) with backpropagation relies on surrogate gradients _f_<sup>_′_</sup> ( _U_ ) to approximate the non-differentiable spike function during the backward pass (Neftci et al., 2019; Zenke and Vogels, 2021) (see Figure 7, top). Several surrogate functions have been proposed, each differing in shape and defined by key parameters: the steepness _β_ , which controls the sharpness of the response around threshold, and the scaling factor _γ_ , which sets the overall gradient amplitude. 

Surrogate gradients do not operate in isolation. Their effectiveness depends on interactions with broader dynamical parameters that shape gradient flow, including the membrane and synaptic time constants ( _τ_ mem, _τ_ syn), spike activity levels, and initialization parameters such as the baseline firing rate _ν_ . Sparser activity or rapidly decaying synapses reduce the temporal window over which gradients can propagate. 

A full grid search over all interactions is computationally infeasible. Instead, we evaluate the practical effect of different surrogate functions and steepness values while keeping other parameters fixed at reasonable working defaults. 

In this experiment, we compare three commonly used surrogate gradient functions: 

- **Sigmoid surrogate** , based on the derivative of the logistic function 

- **SuperSpike** (Zenke and Ganguli, 2018), a heavy-tailed approximation with smoother decay 

- **GaussianSpike** (Yin et al., 2021), a mixture-based method with localized support 

Each function defines a differentiable approximation to the spike function’s gradient during training. The Sigmoid Spike surrogate is defined as: 


where _σ_ is the logistic sigmoid and _n_ sig = 0 _._ 25 normalizes the peak gradient to 1 when _γ_ = 1. The Super Spike approximation is: 


The Gaussian Spike surrogate is defined by a weighted mixture of Gaussians: 


with constants _h_ = 0 _._ 15, _s_ = 6, and normalization factor _n_ gaus ensuring unit peak when _γ_ = 1. 

Figure 7 (top) visualizes these surrogate profiles for varying steepness _β_ . Higher _β_ values result in sharper gradients concentrated near threshold. We fix _γ_ = 1 _._ 0 throughout and vary _β_ to assess each function’s impact on training performance. 

The bottom panel of Figure 7 shows the results of these experiments in the 2D control task. For each surrogate function, we observe that a moderate steepness _β_ yields the fastest and most stable learning. While overly low _β_ values result in shallow gradients and slow convergence, excessively large values can trigger gradient explosion and numerical instability—especially in the Sigmoid and Gaussian surrogates. SuperSpike appears slightly more tolerant to variation in _β_ , but all three surrogates support learning when well-tuned. At their respective optimal _β_ values, final task performance is comparable across surrogate types. 

Since no surrogate clearly outperforms the others, we continue with the Gaussian Spike surrogate at _β_ = 16 for all subsequent experiments, chosen for its reliable and comparably fast convergence in this setting. 

20 


Figure 7: **Surrogate gradient functions and training outcomes. Top:** Gradient profiles _f_<sup>_′_</sup> ( _U_ ) of the Sigmoid, SuperSpike, and Gaussian surrogates across different steepness values _β_ . Higher _β_ localizes the gradient more sharply around the spike threshold. **Bottom:** Training dynamics using each surrogate with varying _β_ in the 2D control task. All three surrogates can support effective learning if _β_ is appropriately tuned. Low _β_ values lead to unstable gradient magnitudes and training failure, while moderate values yield comparable time-on-target and prediction performance. We proceed with the Gaussian Spike surrogate at _β_ = 16 for the remainder of this study. 

21 

# **C Empirical Initialization** 

Spiking neural networks are highly sensitive to weight initialization, as only specific parameter regimes yield sufficient activity and stable learning. We adopt a fluctuation-driven initialization scheme (Rossbroich et al., 2022), which incorporates the neuron time constants _τ_ mem and _τ_ syn into the weight scaling rules. This method aims to place the network in a dynamic regime where neurons spike regularly but not excessively, facilitating gradient-based learning. Unlike standard methods such as Kaiming or Xavier initialization—which do not account for temporal filtering—this scheme is better suited to SNNs with explicit dynamics. 

The original formulation requires an estimate of _ν_ , the expected presynaptic spike rate per neuron per second. While this can be computed analytically for static datasets, our closed-loop control setting generates inputs online. We therefore treat _ν_ as a tunable hyperparameter and determine suitable values empirically via grid search. 

We assess initialization quality using two criteria: (i) the fraction of neurons that spike at least once per episode (per layer), and (ii) the average spike rate per neuron. We do not enforce a specific target rate but seek configurations that preserve signal propagation without saturating or silencing activity. 

Although our networks are relatively shallow (3 layers), they are unrolled over many time steps during task execution, producing significant temporal depth. This contrasts with feedforward SNNs used in classification tasks (Rossbroich et al., 2022), where stability was more closely linked to performance. Here, we observe that well-performing configurations are not always those with the lowest loss or the highest activity levels, indicating that different metrics may emphasize different aspects of task behavior. 

We fix the target membrane statistics to _µU_ = 0 and _σU_ = 1 for all initializations. The full derivation of how _ν_ , _τ_ mem, and _τ_ syn influence the initialization scale is provided in (Rossbroich et al., 2022). 

Figure 2 shows how _τ_ mem and _τ_ syn shape the temporal dynamics and firing behavior of individual neurons. We use this as a reference when selecting the parameter range explored in the grid search. 

Figure 8 summarizes the effect of _ν_ , _τ_ mem, and _τ_ syn on control performance, spiking statistics, and gradient norms. Each result is averaged over 3 random seeds, and reported at the training iteration where the cumulative distance is minimized. While cumulative distance is used as the optimization objective, we find that time on target provides a more discriminative view of model quality across hyperparameter settings. 

The influence of _τ_ mem and _τ_ syn is notably more pronounced than that of _ν_ on most task-related metrics. By contrast, _ν_ mainly controls the number of active neurons and spike density, confirming its role in setting the network’s baseline excitability. 

Interestingly, the configurations with the lowest policy and prediction losses are not those with the highest time-ontarget. This mismatch highlights that minimizing error signals does not always correspond to robust goal-directed behavior—reaching the target briefly and maintaining presence there are qualitatively different challenges. Moreover, some parameter settings that would be considered unstable by classical criteria (e.g., low spike coverage or imbalanced layer activity) still yield strong task performance. This stands in partial contrast to prior work on SNN classification (Rossbroich et al., 2022), where stable activity and balanced firing were stronger predictors of success. Our findings suggest that the link between stability and performance is more nuanced in closed-loop, temporally extended control tasks. 

We select _τ_ mem = 0 _._ 01, _τ_ syn = 0 _._ 002, and _ν_ = 125 for all subsequent experiments, based on their strong performance on the time-on-target metric. This setting also yields among the lowest gradient norms for both networks, suggesting that efficient learning can occur with well-conditioned, moderate gradients. While other settings might perform well with different learning rates, a joint search over learning rates and initialization parameters is computationally infeasible. While our approach explores a fixed grid of values for _ν_ , _τ_ mem, and _τ_ syn, it does not include a mechanism to adapt _ν_ during training or to automatically tune it to satisfy predefined stability criteria. Incorporating an outer loop that adjusts _ν_ to achieve a target spiking profile at initialization time—or during training—could be a promising avenue for future work, particularly in deeper or more recurrent architectures where initialization fragility is more pronounced. 

22 


Figure 8: **Influence of initialization parameters on SNN performance, gradients, and spiking activity.** Each column corresponds to an empirically selected input rate _ν_ , while each heatmap varies _τ_ mem and _τ_ syn. We report task performance (top), prediction quality (middle), and gradient/spike metrics (bottom). Each cell shows the average over 3 seeds at the iteration of minimum cumulative distance. The influence of _τ_ mem and _τ_ syn is generally stronger than that of _ν_ across most metrics. Time-on-target peaks for _τ_ mem = 0 _._ 01, _τ_ syn = 0 _._ 002, and _ν_ = 125, which we use for all further experiments. Surprisingly, some configurations with low loss do not yield the best behavioral outcomes, indicating a partial decoupling between error reduction and effective control. 

23 

# **D Network Architecture** 

In this section, we investigate the influence of architectural choices on learning performance by systematically varying the structure of both the policy and prediction networks. We focus on two main factors: (i) the number of hidden layers, and (ii) whether the first layer of each network is implemented as a recurrent spiking layer. This design choice determines the temporal context each model can access and, by extension, the type of information it can extract from its input. Further, we investigate the shape of the network (neurons per layer and number of layers) to see which setup is sufficient to solve the control task. 

## **D.1 Recurrent Connections** 

We begin our investigation into architectural structure by examining whether recurrent connectivity in the first spiking layer improves learning for the prediction model **_υ_** and/or the policy model **_π_** . 

In principle, recurrence is expected to benefit both models. The input to **_υ_** includes the robot’s current joint position, but omits velocity information, which must be internally inferred over time. Adding a recurrent layer provides the models with increased temporal memory, allowing it to better accumulate information across timesteps and approximate hidden state variables. Without recurrence, both SNNs would need to rely solely on the implicit memory of LIF neurons, which may be insufficient in this partially observable setting. 

We first perform a high-level comparison across all tested conditions with and without recurrence in either network (see Figure 9). The results confirm that the models can learn the reaching task without any recurrent connections. However, adding recurrence to the prediction model consistently improves both prediction accuracy and task performance. Surprisingly, recurrence in the policy model either yields no improvement or slightly impairs learning. The reason for this difference is not obvious. 

To explore how strongly the recurrent layer should rely on internal versus external input, we introduce a tunable parameter _ρ ∈_ [0 _,_ 1] that controls the initialization ratio between external inputs and recurrent feedback: 


A value of _ρ_ = 0 _._ 9 implies a weakly recurrent layer (mostly driven by external input), while _ρ_ = 0 _._ 1 yields a strongly recurrent layer (dominated by recurrent feedback). We sweep _ρ_ from 0.1 to 0.9 in steps of 0.2, using the fluctuation-driven initialization strategy of Rossbroich et al. (2022). 

Figure 9 (bottom) shows the results of this sweep, with and without recurrence in the policy model. We observe that recurrence in the prediction model yields clear benefits across all _ρ_ values. By contrast, recurrence in the policy model degrades performance for all tested values of _ρ_ , likely due to the introduction of excessive memory and less interpretable credit pathways. 

Another key finding is that prediction and control performance vary only mildly across the tested range. For robustness and simplicity, we therefore continue with _ρ_ = 0 _._ 9 in all subsequent experiments involving recurrent layers. 

Together, these findings support the architectural choice of using a recurrent first layer in the prediction model and a purely feedforward structure in the policy model. This hybrid design achieves the best trade-off between memory capacity and training stability in our control setting. 

## **D.2 Network Shape** 

Spiking neurons such as LIF units emit discrete spikes, producing a binary signal at each timestep. As a result, individual neurons cannot easily represent continuous quantities. Instead, effective encoding typically relies on population coding, where multiple neurons collectively represent scalar values through coordinated activity patterns. This motivates the use of larger hidden layers in SNNs compared to non-spiking neural networks. 

In addition to size, network depth is another key architectural factor. Multiple hidden layers enable richer nonlinear transformations and may be necessary to map raw inputs to suitable control or prediction outputs. However, increasing depth also introduces optimization challenges and computational cost. 

To identify a suitable network configuration, we evaluate task performance across a range of architectures where both the prediction network **_υ_** and the policy network **_π_** share the same structure. We sweep the number of spiking layers (1, 2, or 3) and the number of neurons per layer (32, 64, 128, 256, 512, or 1024). 

24 


Figure 9: **Influence of recurrence and input/recurrent weight ratio** _ρ_ **on network performance. Top:** Task performance metrics show that no recurrence is necessary to learn the control task. Recurrence in the prediction network **_υ_** clearly improves time on target, while recurrence in the policy **_π_** offers no benefit and often impairs performance. **Bottom:** Detailed sweep over values of _ρ_ from 0.1 to 0.9. Excessively strong recurrence (low _ρ_ ) destabilizes training in the policy network, while moderate recurrence is safe but unnecessary. A weakly recurrent prediction model with _ρ_ = 0 _._ 9 performs well and is used in all following experiments. 

Figure 10 summarizes the results across four key metrics on the 2D control task. We observe that increasing the number of neurons generally improves task performance, especially in shallow networks. Performance gains diminish beyond 512 neurons per layer, and models with 1024 units exhibit some instability across seeds. 

Network depth has a subtler effect: moving from one to two layers provides a noticeable benefit, but adding a third layer does not yield consistent further improvement. In some cases, deeper networks even show slower convergence or reduced robustness. 

Based on these findings, we adopt a shared structure of two spiking layers with 512 neurons each for both networks in all remaining experiments. This configuration offers strong performance with reasonable model size and training stability. 

25 


Figure 10: **Effect of network size on task performance.** Each column varies the number of spiking layers (1–3), while each line color indicates the number of neurons per layer. Metrics include cumulative distance, success rate, time on target, and prediction MSE. Performance generally improves with increasing network size, but saturates around 512 units. A two-layer architecture provides a good trade-off between expressivity and stability, and is used in all subsequent experiments. 

26 

# **E Training Procedure** 

We adopt an iterative offline training approach to jointly optimize the prediction network **_υ_** and the policy network **_π_** . At each iteration, a new batch of experience is collected by rolling out the current policy **_π_** in the environment. These episodes are stored in a replay buffer of capacity _M_ , which acts as a sampling pool for learning. Training then proceeds in two stages: first, the prediction model is updated for _n_ **_υ_** mini-batches; then, the policy model is trained for _n_ **_π_** mini-batches. This process is repeated over _I_ = 100 training iterations and all reported results are averaged over 3 random seeds. The full procedure is outlined in Algorithm 2. 

Algorithm 2: **Offline training of prediction and policy networks.** 

- 1: _Inputs:_ **_υ_** (ˆ **_s_** _t_ +1 _|_ **_s_** _t,_ **_u_** _t,_ **_θυ_** ), **_π_** ( **_u_** _t|_ **_s_** _t,_ **_s_**<sup>_∗_</sup> _t_<sup>_,_</sup><sup>**_θπ_**), environment (</sup><sup>**_s_**</sup><sup>_t_+1</sup><sup>_,_</sup><sup>**_s_**</sup><sup>_∗_</sup> _t_ +1<sup>_|_</sup><sup>**_u_**</sup><sup>_t_), memory capacity</sup><sup>_M_</sup> 2: Initialize parameters **_θυ_** , **_θπ_** and replay buffer of size _M_ 

- 3: **for** _I_ training iterations **do** 4: Collect _E_ new episodes with **_π_** , append to replay buffer 5: Train **_υ_** for _n_ **_υ_** mini-batches _▷_ See Algorithm 3 6: Train **_π_** for _n_ **_π_** mini-batches _▷_ See Algorithm 4 7: Update training schedule (e.g., decay _α_ , _p_ tf, _σu_ ) 

We vary two key parameters that govern the training dynamics: the memory buffer size _M_ and the number of gradient updates per iteration for each model. Each iteration collects _E_ = 64 new episodes, and both networks are trained using mini-batches of size 256. The memory buffer is tested in three regimes: minimal memory ( _M_ = _E_ ), intermediate memory ( _M_ = 20 _E_ ), and full memory ( _M_ = _IE_ ), where _I_ = 100 is the total number of training iterations. In parallel, we vary the number of mini-batches per iteration _n_ **_υ_** = _n_ **_π_** _∈{_ 5 _,_ 15 _,_ 25 _,_ 35 _}_ . 

Figure 11 shows the resulting performance across buffer sizes and training frequencies. We observe that larger memory buffers lead to better generalization and more stable convergence, particularly at higher training frequencies. However, the gains diminish between _M_ = 1280 and _M_ = 6400, indicating that even limited memory can suffice for this relatively simple 2D control task. Conversely, using only the most recent batch ( _M_ = 64) causes slower learning, particularly in the early stages, and can result in suboptimal final performance. 

We also find that increasing the number of training batches per iteration improves performance up to around 25 batches, beyond which returns diminish. This suggests that moderate reuse of experience is beneficial, but excessive replay may reduce sample diversity and hurt adaptation. 

Based on these findings, all subsequent experiments use the full memory buffer ( _M_ = _IE_ ) and 25 mini-batches per iteration. While memory capacity was not a bottleneck in this study, larger and more complex reinforcement learning tasks may require more careful buffer management. 

Finally, we note that our training setup does not explore the regime of truly online learning, where no buffer is used and only one episode is collected and trained on per iteration. Such a regime—where each training batch is sampled from a single episode without storage—would approximate a fully online learning setup and may require significantly different strategies for stability and plasticity. We leave such scenarios to future work focused on continual and online adaptation in spiking control networks. 

27 


Figure 11: **Effect of replay buffer size and training frequency on model performance.** Each column corresponds to a different memory size _M_ , while lines indicate the number of mini-batches per iteration. Metrics include cumulative distance, time-on-target, and prediction MSE. Moderate memory sizes (e.g., _M_ = 1280) yield stable performance. Excessive update frequency or limited memory can lead to slower convergence or unstable behavior. 

28 

# **F Prediction Network** **_υ_ Training** 

Training the prediction network **_υ_** requires special consideration due to its recurrent structure and its role in generating multi-step predictions of future robot states. At each timestep, the model receives the current robot state **_s_** _t_ and action **_u_** _t_ and predicts a state increment ∆ˆ **_s_** _t_ , which is added to the previous estimate **_s_** ˆ _t_ to produce **_s_** ˆ _t_ +1. The training objective is to minimize the discrepancy between these predicted and true future states over short unrolled sequences. 

To enable stable gradient propagation, we adopt a two-phase rollout strategy comprising a warmup and an unroll period. During warmup, the network is driven by ground-truth observations **_s_** _t_ for _T_ warm steps without gradient updates, allowing the internal state to converge to a stable regime. This is followed by an unroll phase of _T_ unroll steps, during which predictions are made autoregressively and losses are accumulated. 

To mitigate drift and improve convergence, we use teacher forcing during unrolling: at each timestep, the model either receives the true state **_s_** _t_ or its own previous prediction **_s_** ˆ _t_ with a fixed probability _p_ tf. In this experiment, we test both extremes—fully enabled ( _p_ tf = 1 _._ 0) and fully disabled ( _p_ tf = 0 _._ 0)—as well as varying unroll lengths _T_ unroll _∈{_ 10 _,_ 20 _,_ 40 _,_ 80 _}_ . While it is possible to gradually decay _p_ tf over time in a curriculum-style fashion, we found that this did not lead to further improvements for the present task. 

As **_υ_** predicts changes in state rather than absolute values, the target outputs are typically small. To maintain healthy spiking activity and avoid overly large predictions early in training, we initialize the weights of the readout layer with a learnable scaling factor set to 0.005. Without this scaling, gradients become unstable and the policy receives misleading updates. 

The prediction error is computed using the mean squared error between predicted and ground-truth states (Equation 1), averaged across all unroll steps. Additional regularizers penalize extreme levels of spiking activity (see Appendix K) and large weights (see Appendix J), leading to a total loss: 


The training algorithm is summarized in Algorithm 3. The network consists of one recurrent spiking layer followed by spiking and non-spiking readout layers. 

Algorithm 3: **Updating prediction network parameters** with warmup and teacher forcing for a single epoch. 

1: _Inputs:_ **_υ_** (ˆ **_s_** _t_ +1 _|_ **_s_** _t,_ **_u_** _t,_ **_θυ_** ), memory buffer, _L_ **_υ_** , _α_ **_υ_** , warmup steps _T_ warm, unroll steps _T_ unroll, teacher forcing prob. _p_ tf 2: **for** _n_ **_υ_** mini-batches **do** 3: Sample _N_ **_υ_** episodes 4: _L ←_ 0 5: **for** each episode **do** _▷_ Computed in parallel 6: Select subsequence of length _T_ warm + _T_ unroll 7: Reset hidden state _h_ 0 8: **for** _t_ = 1 to _T_ warm **do** 9: **_s_** ˆ _t_ +1 _←_ **_υ_** ( **_s_** _t,_ **_u_** _t,_ **_θυ_** _, ht_ ) _▷_ Warmup phase, no loss 10: **for** _t_ = _T_ warm + 1 to _T_ warm + _T_ unroll **do** 11: Sample _b ∼_ Uniform(0 _,_ 1) 12: **if** _b < p_ tf **then** 13: **_s_** ˆ _t_ +1 _←_ **_υ_** ( **_s_** _t,_ **_u_** _t,_ **_θυ_** _, ht_ ) _▷_ Teacher forcing 14: **else** 15: **_s_** ˆ _t_ +1 _←_ **_υ_** (ˆ **_s_** _t,_ **_u_** _t,_ **_θυ_** _, ht_ ) _▷_ Autoregressive input 16: _L ← L_ + _L_ **_υ_** (ˆ **_s_** _t_ +1 _,_ **_s_** _t_ +1) 17: **_θυ_** _←_ **_θυ_** + _α_ **_υ_** _∇θ_ **_υ_** <u>�</u> _N_ **_υ_** _TL_ unroll <u>�</u> _▷_ Use optimizer for parameter update 18: **return** **_θυ_** 

Figure 12 shows how unroll length and teacher forcing influence model behavior. Longer unrolls without teacher forcing lead to larger prediction losses and gradient magnitudes due to error accumulation during backpropagation. However, these differences have only marginal effects on final prediction accuracy and virtually no impact on downstream task performance. 

These findings suggest that precise long-horizon prediction is not strictly necessary for learning successful control, and that the policy network can compensate for small inaccuracies in the model’s dynamics. Teacher forcing plays a 

29 

stabilizing role, reducing gradient scale and improving convergence stability. Importantly, increasing the unroll horizon also leads to substantially higher computational and memory costs per batch. Balancing predictive depth, computational efficiency, and learning stability, we select an unroll length of _T_ unroll = 10 and teacher forcing enabled ( _p_ tf = 1 _._ 0) for all subsequent experiments. 


Figure 12: **Effect of unroll length and teacher forcing on training dynamics of the prediction model.** Solid lines indicate full autoregression ( _p_ tf = 0 _._ 0), dashed lines indicate teacher forcing ( _p_ tf = 1 _._ 0). Longer unrolls lead to increased loss and gradient magnitudes due to error accumulation, but task performance (time on target) remains similar across all configurations. Teacher forcing stabilizes gradient flow and speeds up convergence, especially at longer horizons. 

30 

# **G Policy Network** **_π_ Training** 

The policy network **_π_** generates control signals that guide the robot arm toward a desired end-effector position. Its architecture mirrors the prediction model, consisting of two spiking populations followed by a leaky integrator layer, but it does not include recurrent connections (see Section D.1). The network receives the current state **_s_** _t_ and the target state **_s_**<sup>_∗_</sup> _t_<sup>as input and outputs a continuous action</sup><sup>**_u_**</sup><sup>_t_.</sup> 

Since **_u_** _t_ alone does not directly convey how effective the action is, we use the differentiable prediction model **_υ_** to simulate the trajectory resulting from the policy’s action sequence. By comparing predicted future states **_s_** ˆ _t_ +1 to the desired trajectory **_s_**<sup>_∗_</sup> _t_ +1<sup>,wecomputeapolicylossthatprovidesdirectsupervision.Thissetupenablesend-to-end</sup> learning through backpropagation, avoiding the complexities of reinforcement learning while maintaining signal fidelity for credit assignment. 

As in the prediction model, we use a warmup and unroll procedure: during warmup, both models are driven by ground-truth states to stabilize internal dynamics. During the unroll, the policy outputs actions and receives feedback through the prediction model. 

**Bounded Action Output.** To ensure valid control commands, we apply a tanh activation to the output layer, constraining actions to [ _−_ 1 _,_ 1]. A learnable linear scaling precedes the tanh to ensure the pre-activations fall within the stable range of the nonlinearity. To further stabilize training, we add a soft regularization term: 


where _Ui_ are the pre-activation values. 

The full policy loss becomes: 


with regularization terms defined in Appendix K and Appendix J. 

Algorithm 4 outlines the full training loop. 

Algorithm 4: **Updating policy network parameters** with warmup and unrolling for a single epoch. 

1: _Inputs:_ **_π_** ( **_u_** _t|_ **_s_** _t,_ **_s_**<sup>_∗_</sup> _t_<sup>_,_</sup><sup>**_θπ_**),</sup><sup>**_υ_**(ˆ</sup><sup>**_s_**</sup><sup>_t_+1</sup><sup>_|_</sup><sup>**_s_**</sup><sup>_t,_</sup><sup>**_u_**</sup><sup>_t,_</sup><sup>**_θυ_**), memory buffer,</sup><sup>_L_</sup><sup>**_π_**,</sup><sup>_α_</sup><sup>**_π_**, warmup steps</sup><sup>_T_warm, unroll steps</sup><sup>_T_unroll</sup> 2: **for** _n_ **_π_** mini-batches **do** 3: Sample _N_ **_π_** episodes 4: _L ←_ 0 5: **for** each episode **do** _▷_ Computed in parallel 6: Select subsequence of length _T_ warm + _T_ unroll 7: Reset hidden states of **_π_** and **_υ_** 8: **for** _t_ = 1 to _T_ warm **do** 9: **_s_** ˆ _t_ +1 _←_ **_υ_** ( **_s_** _t,_ **_u_** _t,_ **_θυ_** ) _▷_ Warmup phase, no loss 10: **for** _t_ = _T_ warm + 1 to _T_ warm + _T_ unroll **do** 11: **_u_** ˆ _t ←_ **_π_** (ˆ **_s_** _t,_ **_s_**<sup>_∗_</sup> _t_<sup>_,_</sup><sup>**_θπ_**)</sup> 12: **_s_** ˆ _t_ +1 _←_ **_υ_** (ˆ **_s_** _t,_ ˆ **_u_** _t,_ **_θυ_** ) 13: _L ← L_ + _L_ **_π_** (ˆ **_s_** _t_ +1 _,_ **_s_**<sup>_∗_</sup> _t_ +1<sup>)</sup> 14: **_θπ_** _←_ **_θπ_** + _α_ **_π_** _∇θ_ **_π_** <u>�</u> _N_ **_π_** _<u>LT</u>_ unroll <u>�</u> _▷_ Use optimizer for parameter update 

15: **return** **_θπ_** 

We now investigate how the length of the unroll window _T_ unroll affects policy training. We test values of _T_ unroll = _{_ 5 _,_ 10 _,_ 20 _,_ 40 _,_ 80 _}_ using three random seeds each. 

Figure 13 reveals clear trends. Task performance—measured as time spent on target—improves sharply with longer unroll windows and saturates around 40 steps. While even short unrolls reduce cumulative distance, they fail to produce stable control behaviors. Meanwhile, policy loss consistently decreases with longer horizons, reflecting greater opportunity for gradient-based corrections. However, this comes at the cost of growing gradient magnitudes, which suggests an increased risk of exploding gradients at long horizons. 

Interestingly, this pattern differs from the prediction model, where longer unrolls increased loss due to compounding error. Here, the policy benefits from longer feedback horizons, provided the prediction model remains stable. 

31 

For all subsequent experiments, we adopt _T_ unroll = 40 for policy training, which balances performance gains and computational efficiency. 


Figure 13: **Effect of policy unroll length on training dynamics and task performance.** Longer unrolls improve time on target and lower policy loss by providing richer gradient signals. However, gradient magnitudes increase with unroll length, indicating a growing risk of instability. Gains saturate at 40 steps, which is used in all subsequent experiments. 

32 

# **H Learnable Time Constants** _τ_ 

In all preceding sections, the neuronal time constants _τ_ mem and _τ_ syn were treated as fixed hyperparameters. However, in biological neurons and many real-world control settings, the optimal temporal integration windows may vary across tasks or layers. Allowing these parameters to be learned end-to-end gives the network flexibility to adapt its internal dynamics to the temporal structure of the task, potentially improving sample efficiency and robustness. 

A key technical consideration is ensuring that learned time constants remain positive. To this end, we parameterize each time constant as _τ_ = exp( _τ_<sup>_′_</sup> ), where _τ_<sup>_′_</sup> is an unconstrained real-valued parameter. This exponential mapping has several benefits: it guarantees positivity, enables multiplicative rather than additive updates (which are scale-invariant), and results in smooth gradients with respect to both small and large values of _τ_ . These properties promote stable and interpretable learning behavior, and avoid pathological dynamics such as negative or vanishing time constants. 

While one could alternatively parameterize and learn the decay factor _β_ = exp( _−_ ∆ _t/τ_ ), we found learning in log _τ_ space to be more stable and easier to interpret. Preliminary experiments (not shown) also confirmed this choice resulted in more consistent convergence. 

This learning mechanism can be applied per layer or per neuron. In the **per-neuron** configuration, each unit receives its own learned time constant, allowing fine-grained temporal specialization. In contrast, the **layer-wise** variant uses a single shared _τ_ per layer, which reduces parameter count and computational cost. In our experiments, we found that per-neuron learning yielded slightly better results without significant overhead, so this configuration is used throughout. 

Here we evaluate whether learning time constants improves task performance, and whether it can compensate for suboptimal initialization. We focus on learning _τ_ mem, while keeping _τ_ syn fixed at 2 ms. Other time constants (such as _τ_ ada in Appendix I) can be learned using the same mechanism. 

We consider two initializations of _τ_ mem, 10 ms (optimal, based on prior results) and 20 ms (suboptimal), and three learning rates for _τ_ : _ατ ∈{_ 0 _._ 0 _,_ 0 _._ 001 _,_ 0 _._ 01 _}_ , where _ατ_ = 0 disables learning, and _ατ_ = 0 _._ 01 corresponds to “fast learning”, i.e., ten times the learning rate used for other model parameters. 

Figure 14 (top) shows that with a good initialization (10 ms), learning _τ_ mem makes little difference: both static and adaptive models perform well. However, when initialized at 20 ms, models without _τ_ learning suffer in performance. While slow learning ( _ατ_ = 0 _._ 001) offers only mild improvements, fast learning ( _ατ_ = 0 _._ 01) fully recovers performance, matching the results of the optimal initialization. This highlights the benefit of allowing models to escape suboptimal initial values by tuning their intrinsic timescales. 

To understand how _τ_ mem evolves during training, Figure 14 (bottom) shows the distribution of final time constants in the prediction model’s recurrent layer. When learning is enabled, the values shift consistently toward shorter integration windows, suggesting that the task favors fast neuronal responses. The learned distributions remain unimodal but show slight leftward skew, with final means clearly below their respective initializations. 

Based on these findings, we use per-neuron learnable _τ_ mem and _τ_ syn with fast learning rate _ατ_ = 0 _._ 01 in all subsequent experiments. 

33 


Figure 14: **Effect of learnable time constants on learning and neuron dynamics. Top:** Learning curves and activity metrics for _τ_ mem initialization at 10 ms (dashed) or 20 ms (solid), with varying learning rates _ατ_ . Fast learning ( _ατ_ = 0 _._ 01) recovers performance even from poor initialization. **Bottom:** Histogram of learned _τ_ mem values after training. Learning shifts the distribution toward smaller, task-adapted values regardless of initialization. 

34 

# **I Adaptive Leaky Integrate-and-Fire Neuron Model** 

Spiking neurons often exhibit adaptive behavior, where their firing threshold increases temporarily after a spike. This mechanism reduces immediate re-firing and promotes sparse activity, improving network robustness and training dynamics. In this section, we study an adaptive variant of the LIF model (ALIF) that incorporates both fast and slow modulation of the spiking threshold to stabilize activity and promote efficient learning. We implement a discrete-time variant of ALIF where the baseline threshold provides slow homeostatic recovery, while the adaptive component provides spike-triggered suppression. Together, these mechanisms stabilize network activity and extend the effective eligibility traces available for gradient learning. 

Specifically, the instantaneous firing threshold _ϑt_ consists of two components: 

- a baseline component _ϑb,t_ that gradually decays back toward a nominal value _ϑ_ 0 in the absence of spikes, and 

- an adaptive component _ϑa,t_ that increases with recent spiking activity and decays over time. 

This formulation represents one of several possible ALIF variants. Other models introduce additional mechanisms such as explicit refractory periods, additive threshold increments instead of multiplicative scaling, or combined current- and threshold-based adaptation. We adopt this particular formulation because it balances simplicity with effectiveness for gradient-based training, and extends the eligibility traces of spiking neurons in a way that benefits backpropagation-through-time. The total threshold is computed as: 


where _ξϑ_ controls the strength of spike-triggered adaptation. 

Spiking dynamics follow the standard discrete-time LIF updates (cf. Eqs. 8–9), but spike occurrence and membrane reset are now governed by the adaptive threshold: 


where _U_<sup>˜</sup> _t_ is the pre-reset membrane potential and _St_ the spike output. 

The baseline and adaptation traces evolve according to: 


with _β_ ada = exp( _−_ ∆ _t/τ_ ada). The scalar ∆ _ϑ_ defines the slope of the baseline decay and allows silent neurons to slowly become excitable again over time. Our ALIF procedure is shown in detail in Algorithm 5. 

Algorithm 5: Discrete-time update procedure for ALIF neurons. Each population updates its synaptic current _It_ , membrane potential _Ut_ , and dynamic thresholds _ϑb,t, ϑa,t_ according to exponential decay dynamics. Spikes _St_ are generated when the voltage exceeds the adaptive threshold _ϑt_ , after which a subtractive reset is applied. All updates are differentiable via surrogate gradients during training. 

**for** all populations _p_ in network **do** _U_ 0 _← U_ rest _, I_ 0 _←_ 0 _, ϑb,_ 0 _← ϑ_ 0 _, ϑa,_ 0 _←_ 0 _, S_ 0 _←_ 0 _▷_ Initialize population states **for** _t ∈_ [1 _. . . T_ ] **do for** all populations _p_ in network **do** _xt ←_ [ _St−_ 1 _,i_ for all populations _i_ projecting to _p_ ] _▷_ Collect spike outputs from the previous time step _It ← β_ syn _It−_ 1 + _Wxt_ + _I_ inj _,t ▷_ Update synaptic current (Eq. 8) _U_ ˜ _t ← β_ mem _Ut−_ 1 + (1 _− β_ mem) _It ▷_ Compute membrane potential (Eq. 9) _St ←_ Θ( _U_<sup>˜</sup> _t − ϑt_ ) _▷_ Check if neuron fires _Ut ← U_<sup>˜</sup> _t − ϑtSt ▷_ Subtractive reset (Eq. 19) _ϑb,t ← ϑb,t−_ 1 _−_ ∆ _ϑ_ + � _ϑ_ 0 _− ϑb,t−_ 1� _St ▷_ Baseline threshold update (Eq. 20) _ϑa,t ← β_ ada _ϑa,t−_ 1 + _St ▷_ Spike-triggered adaptation (Eq. 21) _ϑt ← ϑb,t_ + _ξϑ ϑa,t ▷_ Updated threshold (Eq. 18) 

In the following subsections, we examine how each mechanism influences the behavior of single ALIF neurons and their firing responses to tonic and noisy inputs, as well as their impact on learning the 2D control task. To allow both _ϑa_ and _ϑb_ to contribute meaningfully, in the control experiments we use an unroll window _T_ unroll = 40 environment steps (= 280 SNN steps) for both the prediction and the policy model. 

35 

## **I.1 Effect of Threshold Decay** 

We first isolate the effect of the baseline decay rate ∆ _ϑ_ , which causes the baseline threshold _ϑb,t_ to decrease over time in the absence of spikes. This enables otherwise inactive neurons to gradually recover excitability, acting as a simple homeostatic mechanism. To evaluate this effect in isolation, we fix _ξϑ_ = 0 (disabling spike-triggered adaptation) and vary ∆ _ϑ_ across trials. 

Figure 15 illustrates how neurons with higher decay rates recover from suppressed states and resume firing more quickly, even under constant or weakly negative current input. This leads to spontaneous reactivation and helps maintain population-level activity without relying on external noise or manual regularization. 


Figure 15: **Effect of baseline decay rate** ∆ _ϑ_ **on single-neuron firing dynamics.** Larger values of ∆ _ϑ_ shorten the latency before silent neurons resume spiking, enabling recovery even under low or inhibitory input. 

We next assess the effect of baseline decay on learning performance in the 2D control task. Figure 16 shows that intermediate values of ∆ _ϑ_ improve policy learning by keeping more neurons active throughout training. Across runs, we find that increasing ∆ _ϑ_ consistently raises the mean number of active and spiking neurons (bottom row), thereby reducing neuron silence. This also leads to larger gradient magnitudes in both the prediction and policy models, especially at ∆ _ϑ_ = 100, where the spiking activity becomes dense and overactive. While such aggressive decay eliminates silent units entirely, it impairs control behavior and slows convergence, likely due to the disruptive effect of excessive noise during training. By contrast, moderate decay rates (e.g., ∆ _ϑ_ = 10) yield stable and fast learning, suggesting a beneficial trade-off between activation and precision. The setting ∆ _ϑ_ = 1 shows only minimal differences compared to no decay (∆ _ϑ_ = 0), and is therefore omitted from subsequent comparisons. We continue with ∆ _ϑ_ = 0 and 10 as representative cases in the next sections. 

While threshold decay successfully increases the number of active neurons, this does not necessarily imply that all units contribute meaningfully to information encoding or task performance. A deeper analysis of neuron selectivity and functional contribution would be needed to assess the representational benefits of this mechanism, which is beyond the scope of the present work. Such analyses could be particularly valuable when combined with pruning strategies that remove persistently uninformative units, offering a promising direction for future research. 

36 


Figure 16: **Effect of baseline decay rate** ∆ _ϑ_ **on control performance.** Moderate decay values improve learning stability and neuron utilization without harming performance, while excessive decay (e.g., ∆ _ϑ_ = 100) causes overactivation, degraded accuracy, and slower convergence. 

## **I.2 Effect of Threshold Adaptation** 

We now study the effect of the adaptive threshold trace _ϑa,t_ in the absence of baseline decay. To isolate this mechanism, we fix ∆ _ϑ_ = 0 and explore different combinations of adaptation time constant _τ_ ada and scaling factor _ξϑ_ . These parameters control how strongly recent spike history suppresses neuronal excitability. Note that based on the findings in Appendix H, all time constants, including _τ_ ada, are learned parameters. 

Figure 17 shows that spike-triggered adaptation effectively reduces firing rates under sustained stimulation. The suppression persists beyond the period of active input, illustrating a form of activity-dependent memory. Interestingly, different parameter combinations can produce similar steady-state firing rates but yield different temporal responses. For example, _τ_ ada = 0 _._ 1, _ξϑ_ = 0 _._ 25 (light blue) and _τ_ ada = 0 _._ 5, _ξϑ_ = 0 _._ 05 (orange) both suppress spiking to comparable levels, but with distinct adaptation dynamics that will influence gradient flow during training. 


Figure 17: **Effect of spike-triggered threshold adaptation on single-neuron firing.** Left: membrane and threshold traces under step + noise input. Right: steady-state firing rates across input amplitudes. Stronger adaptation (higher _ξϑ_ or longer _τ_ ada) leads to more pronounced firing suppression. While different settings may result in similar steady-state output (e.g., light blue vs. orange lines), their temporal responses differ significantly. 

When applied in the 2D control task, threshold adaptation leads to a reduction in overall spike counts, as expected (see Figure 18). Although some neurons are initially suppressed, population-wide activity tends to recover during training. Configurations with _τ_ ada = 0 _._ 1 lead to faster convergence and improved task performance relative to the baseline. Interestingly, the aforementioned parameter settings that induce similar firing rates result in markedly different learning 

37 

trajectories. This highlights the sensitivity of adaptation-based dynamics to temporal structure and underscores the importance of careful tuning. Examining the distribution of the _τ_ ada parameter at the end of learning shows a clear preference toward smaller values (data not shown). Going forward, we adopt _τ_ ada = 0 _._ 1 in all experiments using threshold adaptation. 


Figure 18: **Effect of threshold adaptation on task performance and activity.** Moderate adaptation improves neuron utilization and accelerates convergence. However, overly strong suppression (e.g., _τ_ ada = 0 _._ 5, _ξϑ_ = 0 _._ 25) can delay learning or reduce precision, despite achieving high final success rates. 

## **I.3 Combined Behavior** 

Finally, we evaluate the full ALIF model by combining spike-triggered adaptation with baseline decay. This formulation enables the suppression of overly active neurons while also reactivating silent ones, achieving a dynamic balance between stability and responsiveness. We fix the baseline decay rate to ∆ _ϑ_ = 10 and vary the adaptation parameters _τ_ ada and _ξϑ_ as in the previous section. 

Figure 19 shows how this combination yields selective and robust firing responses under step and noisy current input. Spiking activity remains sparse, while silent neurons recover naturally without requiring external noise or activity penalties. 


Figure 19: **Combined effect of threshold adaptation and baseline decay on single-neuron firing.** The network simultaneously suppresses overactive neurons and reactivates silent ones, resulting in balanced, selective, and robust firing behavior across input amplitudes. 

In the 2D control task, this combination proves highly effective. Figure 20 shows that all configurations yield strong task performance, with faster convergence and improved learning stability compared to using adaptation alone. Neurons 

38 

remain active throughout training, and overall spiking is substantially reduced. While both _ξϑ_ settings perform similarly at convergence, smaller values slightly accelerate early learning. We also confirm that _τ_ ada = 0 _._ 1 offers better performance than _τ_ ada = 0 _._ 5 across metrics. Based on these results, we continue with the configuration ∆ _ϑ_ = 10, _τ_ ada = 0 _._ 1, and _ξϑ_ = 0 _._ 1 in subsequent experiments. 


Figure 20: **Control task performance using combined ALIF dynamics.** Baseline decay (∆ _ϑ_ = 10) amplifies the benefits of spike-triggered adaptation. All neurons remain active, while overall spiking is reduced and learning becomes more stable and efficient. 

39 

# **J Weight Regularization** 

L2 weight decay is a widely used technique to prevent overfitting by penalizing large weights. In this experiment, we investigate whether applying L2 regularization to all learnable weights improves performance or stability in our spiking control setup. We test values of _λ_ L2 _∈{_ 0 _._ 0 _,_ 10<sup>_−_4</sup> _,_ 10<sup>_−_3</sup> _,_ 10<sup>_−_2</sup> _,_ 10<sup>_−_1</sup> _}_ , applied uniformly to both the prediction and policy networks. 

As shown in Figure 21, increasing _λ_ L2 consistently degrades both task performance and loss minimization. While all configurations still learn the task to some degree, higher regularization strengths lead to slower convergence, increased prediction and policy losses, and substantially higher gradient magnitudes—particularly in the prediction network. Even moderate regularization values (e.g., _λ_ L2 = 0 _._ 001) reduce time on target and overall success. 

Although some reduction in spike activity is observed at higher _λ_ L2, this sparsity does not translate into better generalization or performance. Instead, the results suggest that in this setting, where data is continuously refreshed and overfitting is not a central concern, weight decay acts more as a hindrance than a help. 

We therefore set _λ_ L2 = 0 in all subsequent experiments. 


Figure 21: **Effect of L2 weight decay on performance, loss, and gradient magnitude.** Stronger weight regularization consistently increases losses and gradients while degrading task metrics. Even mild values ( _λ_ L2 = 0 _._ 001) negatively impact time on target and success rate. Based on these results, no weight decay is used in subsequent experiments. 

40 

# **K Activity Regularization** 

Spiking neural networks can exhibit unstable activity patterns during training, such as neurons that never spike, neurons that spike excessively, or entire layers becoming inactive. These issues can impair learning dynamics and reduce model expressiveness. To mitigate this, we introduce activity regularization losses that penalize extreme values of either membrane potential or spiking activity. 

This method shares conceptual overlap with the adaptive threshold mechanism of ALIF neurons (Appendix I), which implicitly discourages high-frequency firing. In contrast, activity regularization enforces explicit constraints by applying loss terms that penalize deviations from user-defined bounds. Both mechanisms aim to stabilize dynamics, but only regularization gives direct control over the desired operating regime. 

Let _Xi,l,t_ denote the activity variable of neuron _i_ in layer _l_ at discrete time step _t_ , where _Xi,l,t ∈{Ui,l,t, Si,l,t}_ with _Ui,l,t_ the membrane voltage and _Si,l,t ∈{_ 0 _,_ 1 _}_ the spike output. We define the per-neuron average activity over an unroll window of _T_ steps as 


The lower- and upper-bound activity regularization losses are then given by 


where _X_ low and _X_ up are user-defined thresholds. These terms are weighted by _λ_ low and _λ_ up in the total network loss (see Equation 15 and Equation 17) and can be applied independently or jointly to shape network dynamics. 

## **Lower-bound membrane potential regularization** 

In the first experiment, we investigate whether penalizing low membrane potentials can prevent neuron inactivity and improve learning. This is motivated by the observation that neurons with consistently subthreshold voltages may never spike, reducing their contribution to learning. We apply the _L_ low regularizer to the membrane potential _Ui,l,t_ and test three thresholds: _U_ low _∈{−_ 10 _, −_ 5 _,_ 0 _}_ . Each threshold is evaluated under regularization strengths _λ_ low _∈{_ 0 _._ 0 _,_ 0 _._ 001 _,_ 0 _._ 01 _,_ 0 _._ 1 _}_ . A value of _λ_ low = 0 _._ 0 serves as the baseline with no regularization. 

Figure 22 shows the effect of applying _L_ low for different thresholds _U_ low and regularization strengths _λ_ low. As the regularization becomes stronger and the threshold increases, we observe a marked rise in spike rate and neuron utilization. This confirms that the penalty effectively prevents neuron silence and enforces network-wide participation. 

However, this comes at a cost: both prediction and policy losses increase, and downstream performance—as measured by time on target and cumulative distance—deteriorates notably, especially for _U_ low = 0. This suggests that promoting activity without regard to task relevance can degrade the quality of learning signals. Compared to adaptive thresholding mechanisms like ALIF (see Appendix I), which modulate excitability based on recent spiking history, static lower-bound regularization lacks temporal nuance and may induce unnecessary spiking. 

Given the unfavorable trade-off, we do not apply _L_ low in later experiments. 

41 


Figure 22: **Effect of lower-bound membrane potential regularization.** Each column shows results for a fixed threshold _U_ low _∈{−_ 10 _, −_ 5 _,_ 0 _}_ , and each curve corresponds to a different regularization strength _λ_ low _∈{_ 0 _._ 001 _,_ 0 _._ 01 _,_ 0 _._ 1 _}_ . Increasing _λ_ low elevates membrane potentials and increases spike rates (bottom rows), successfully activating silent neurons. However, this heightened activity does not translate to improved task performance. Both prediction and policy loss increase, and time on target is reduced, particularly for _U_ low = 0. These results indicate that naïvely enforcing activity may disrupt useful computation. All curves show mean and standard deviation across 3 seeds. 

42 

## **Upper-bound spike activity regularization** 

In the second experiment, we explore whether constraining spiking activity from above can reduce bursting and promote sparsity. We apply the _L_ up regularizer to the spike output _Si,l_ = _T_<sup><u>1</u></sup> � _Tt_ =1<sup>_Si,l,t_of each neuron</sup><sup>_i_in layer</sup><sup>_l_.The threshold</sup> values tested are _S_ up _∈{_ 0 _._ 3 _,_ 0 _._ 2 _,_ 0 _._ 1 _}_ , representing the maximum allowed spike rate averaged over the unroll window. We evaluate regularization strengths _λ_ up _∈{_ 0 _._ 0 _,_ 0 _._ 001 _,_ 0 _._ 01 _}_ to determine the trade-off between enforcing sparsity and maintaining task performance. 

All runs in this section use a fixed prediction unroll window of 40 steps, matching the policy model, and include learnable time constants. This provides a consistent basis for evaluating the isolated effect of spike activity regularization. 

Figure 23 shows that mild spike regularization successfully suppresses overall spiking activity while keeping nearly all neurons active. This often accelerates early learning, as reflected by faster gains in success rate and time on target. However, prediction errors (MSE) plateau at higher values compared to unregularized baselines, and strong regularization ( _λ_ up = 0 _._ 01) further degrades final success and increases across-seed variance. These results suggest that while spike regularization can shape activity levels, it does not consistently improve control performance and can destabilize training when applied too strongly. For this reason, we did not adopt _L_ up in the final model, where adaptive threshold mechanisms (ALIF) provided more robust performance benefits without sacrificing task accuracy. 


Figure 23: **Effect of upper-bound spiking activity regularization.** Increasing _λ_ up reduces mean spike activity (bottom right) while keeping most neurons active. This can accelerate early learning, as seen in higher success rates and time on target, but prediction errors plateau at higher levels and strong regularization impairs final performance and gradient stability. Shaded regions indicate variance across three seeds, which increases for stronger regularization. Overall, spike regularization provides only limited benefits compared to adaptive thresholds (ALIF), which better stabilize dynamics without degrading task accuracy. All curves show mean and standard deviation across 3 seeds. 

43 

# **L Action Regularization Loss** 

This experiment is conducted in the 3D reaching task, where we observed frequent overshooting and oscillatory behavior of the robot arm near the target. While the primary training objective of the policy network is to minimize cumulative distance to the goal, there is no explicit incentive to stop acting once the target is reached. As a result, the system can exhibit unnecessarily energetic or unstable behavior. 

To address this, we introduce auxiliary loss terms that penalize the magnitude and temporal variation of the control signal. These terms are inspired by classical optimal control, where energy and smoothness costs are frequently used to shape stable trajectories. A typical control objective _J_ includes: 


where _c_ ( _xt, x_<sup>_∗_</sup> ) is the task cost, _λu_ penalizes large control signals, and _λu′_ discourages abrupt changes over time. We define the following regularization losses: 


Both losses are differentiable and applied only to the policy network **_π_** , with weighting factors _λu_ and _λu′_ . We include a warmup phase during which these penalties are disabled to prevent interference with early learning dynamics. 

We evaluate all combinations of: 

- Action magnitude penalty _λu ∈{_ 0 _._ 0 _,_ 0 _._ 001 _,_ 0 _._ 01 _}_ 

- Action smoothness penalty _λu′ ∈{_ 0 _._ 0 _,_ 0 _._ 001 _,_ 0 _._ 01 _}_ 

The results in Figure 24 show that applying either form of regularization slows learning and slightly reduces task performance. Qualitatively, higher values of _λu_ and _λu′_ lead to visibly smoother policy outputs and slower arm movements (video not shown). However, the oscillatory behavior is not fully suppressed, and the success rate and time-on-target metrics remain best when no regularization is applied. 

Interestingly, we also observe a consistent degradation in prediction model performance as regularization increases—even though the loss terms affect only the policy. This suggests an indirect interaction, potentially due to a distribution shift in the training data: slower, smoother actions might lead to less diverse or harder-to-predict state transitions early in training. 

Given these findings, we opt not to include action regularization in subsequent experiments. 


Figure 24: **Effect of action magnitude and smoothness regularization on 3D control task performance.** Although higher _λu_ and _λu′_ produce smoother outputs and slower actions, they do not eliminate oscillations and lead to a drop in task and model performance. 

44 

# **M Action Noise During Training** 

Exploration is a key challenge in continuous control, especially in reinforcement learning settings where action distributions must be sampled efficiently. Although our control task is supervised, similar concerns can arise: early network biases may lead to overfitting or limited exploration of the state-action space, particularly during the collection of training episodes. To address this, we experiment with externally injected Gaussian noise added to the policy output **_u_** _t_ at each step during data collection. 

The executed control signal **_u_** ˜ _t_ is sampled from: 


where _σu_ is the standard deviation of the action noise. To balance early exploration with convergence, we optionally decay this noise exponentially over the course of training: 


where _σ_ 0 is the initial noise level and _γσ ∈_ (0 _,_ 1] is the decay factor. At test time, no noise is applied. 

We compare fixed and decaying noise schedules using _σ_ 0 _∈{_ 0 _._ 0 _,_ 0 _._ 1 _,_ 0 _._ 3 _,_ 1 _._ 0 _}_ and _γσ ∈{_ 1 _._ 0 _,_ 0 _._ 9 _}_ . As shown in Figure 25, all configurations eventually converge to good performance on the control task. However, models trained without any action noise achieve faster convergence and slightly better final accuracy. This suggests that in the lowdimensional, well-behaved dynamics of our setting, noise is unnecessary and may even hinder learning by introducing instability during early training. 

While noise-driven exploration may prove beneficial in high-dimensional or reinforcement-based tasks, we find no clear advantage in the present case. We therefore proceed without action noise in the remainder of our experiments. 


Figure 25: **Impact of Gaussian action noise during training.** All models converge to near-optimal performance regardless of noise level. However, omitting noise leads to faster and more stable convergence. Each curve reflects evaluation on noise-free test episodes. 

45 

# **N Reducing Network Parameters** 

Spiking neural networks with large fully connected layers can quickly reach millions of trainable parameters, especially when multiple hidden populations are used. To address this, we introduce a simple low-rank factorization scheme that reduces model size without severely impacting task performance. 

Specifically, instead of using a full weight matrix _W ∈_ R<sup>_n×m_</sup> to connect two spiking populations of size _n_ and _m_ , we decompose _W_ into two smaller matrices: _W_ = _AB_ , with _A ∈_ R<sup>_n×d_</sup> and _B ∈_ R<sup>_d×m_</sup> , where _d ≪_ min( _n, m_ ). This structure is equivalent to a linear bottleneck of dimensionality _d_ placed between the two populations. We train both _A_ and _B_ end-to-end using backpropagation through time. Only the second linear stage includes a learnable bias term. No nonlinearity is applied between the two transformations. 

This factorization is applied uniformly across both the prediction and policy networks, replacing all inter-layer spiking connections (including recurrent ones) with their low-rank equivalents. The latent dimension _d_ is shared across all layers of a network and selected from a fixed set _{_ 8 _,_ 16 _,_ 32 _,_ 64 _,_ full _}_ . 

We evaluate the impact of this compression strategy on the 2D control task, sweeping over several values of neurons per layer (128, 512, 1024, 2048) and latent dimension _d_ . Figure 26 summarizes key performance metrics as a function of total parameter count. 

The results show that parameter count can be drastically reduced—by an order of magnitude or more—without a large drop in control performance. In particular, configurations using 512 or 1024 neurons per layer with latent dimension 16–64 consistently achieve good success rates and convergence behavior. Very large models (e.g., with 2048 neurons and full-rank matrices) offer little additional benefit and may lead to overfitting or excessive spiking activity. 

Overall, low-rank factorization provides a practical method for scaling SNN models while controlling memory and compute requirements. This approach also aligns with biological findings suggesting that population activity often resides on low-dimensional manifolds (Averbeck et al., 2006; Churchland et al., 2012). 


Figure 26: **Effect of low-rank weight factorization on performance and activity.** Each point represents a single model trained on the 2D control task. Marker color indicates the number of neurons per layer (128–2048), and marker shape denotes the number of latent dimensions ( _d ∈{_ 8 _,_ 16 _,_ 32 _,_ 64 _,_ full _}_ ). Multiple metrics are plotted against total parameter count. Low-rank architectures achieve strong performance with significantly fewer parameters than their full-rank counterparts. 

46 

# **O SNN Ablation Study and Component Analysis** 

To isolate which architectural components are responsible for the performance and stability gains of the proposed Pred-control SNN, we conduct a structured ablation study on the **3D reaching task** . All variants are trained and evaluated under the same protocol as the full model described in the main text; only the network architecture is modified. 

**Ablated components and model variants.** Starting from a minimal _floor model_ , we selectively remove or reintroduce three core components: (i) latent-state compression (Appendix N), (ii) adaptive neuron dynamics via ALIF neurons (Appendix I), and (iii) learnable membrane and synaptic time constants (Appendix H). Intermediate variants disable exactly one component at a time, enabling attribution of performance changes to individual design choices. Where applicable, we consider both a _small_ (S, 512 neurons per layer) and a _large_ (L, 2048 neurons per layer) configuration. All other settings—including data collection, unroll length, optimization, and loss functions—are held fixed. 

**Quantitative comparison.** Table 3 reports final task performance and parameter counts for all ablation variants. While removing compression yields slightly improved absolute performance, it does so at a dramatic cost in model size: the uncompressed large model requires over _14×_ more parameters than the compressed full model, for only marginal gains. In contrast, disabling ALIF neurons or learnable time constants leads to consistent degradations in time-on-target, cumulative distance, and prediction accuracy, despite comparable parameter counts. This indicates that adaptive neuron dynamics contribute more strongly to control quality than width alone. 

**Learning dynamics.** Learning curves in Figure 27 further reveal how individual components affect optimization. The full model converges faster, achieves higher sustained time-on-target, and exhibits smaller, more stable gradient norms. Removing ALIF neurons or learnable time constants leads to noisier optimization signals and reduced asymptotic control performance, whereas compression primarily influences performance through representational capacity rather than training stability. 

**Summary.** Together, these results demonstrate that the gains of the proposed SNN controller do not arise from parameter count alone. Adaptive neuron dynamics—via ALIF neurons and learnable time constants—play a central role in stabilizing training and enabling effective temporal representations, while compression provides a favorable trade-off between model size and performance. The full Pred-control SNN therefore occupies a markedly better point on the performance–efficiency frontier than any ablated variant. 

Table 3: **Ablation of key SNN components on the 3D reaching task.** Models are evaluated at the final training iteration (means over 10 seeds; std omitted for clarity). (L) denotes the large variant with 2048 neurons per layer, and (S) denotes the small variant with 512 neurons per layer. The Basic SNN disables compression, learnable time constants, and ALIF neurons. 

||**Pred-control SNN (L)**|**Pred-control SNN (S)**|**No comp. (L)**|**No comp. (S)**|**No ALIF**|**No learnable**_τ_**s**|**Basic SNN**|
|---|---|---|---|---|---|---|---|
|Neurons / layer|2048|512|2048|512|2048|2048|512|
|Policy parameters|315,422|78,878|4,247,582|275,486|311,326|303,122|272,402|
|Predictor parameters|591,914|148,010|8,456,234|541,226|587,818|579,608|538,136|
|**Total parameters**|**907,336**|**226,888**|**12,703,816**|**816,712**|**899,144**|**882,730**|**810,538**|
|Cumulative distance_↓_|0.634|0.833|**0.607**|0.769|0.712|0.714|0.884|
|Success rate_↑_|0.986|0.964|**0.989**|0.986|0.992|0.954|0.975|
|Time on target_↑_|0.615|0.364|**0.652**|0.435|0.492|0.559|0.322|
|State MSE_↓_|0.020|0.023|**0.017**|0.020|0.025|0.026|0.023|


47 


Figure 27: **SNN ablation study on the 3D reaching task.** Learning curves for Pred-control SNN variants in which individual architectural components are removed. Shown are a minimal _basic_ model (no learnable time constants, no ALIF neurons, no parameter compression; 512 neurons per layer), the full model (learnable time constants, ALIF neurons, and compression; 2048 neurons per layer), and intermediate variants where exactly one component is ablated. Top row: task performance metrics (cumulative distance, success rate, time on target, prediction MSE). Middle row: optimization losses and gradient norms for predictor and policy. Bottom row: population activity statistics. Curves show mean over 3 seeds (sd omitted for visual clarity). The full model consistently achieves faster convergence, higher time on target, and more stable gradients. Removing adaptive neuron dynamics (learnable time constants or ALIF neurons) degrades both learning efficiency and final control quality, while compression primarily affects performance through model capacity rather than training stability. 

48 

# **P Robustness to target perturbations** 

To probe robustness beyond the nominal evaluation protocol, we performed a simple closed-loop perturbation test in which the target position is shifted whenever the end-effector enters the success radius. As shown in Figure 28, the pretrained Pred-Control SNN rapidly reorients toward the updated target and typically re-acquires it within a few control cycles, producing repeated decreases in distance-to-target after each perturbation. This behavior suggests that the learned policy does not merely memorize a fixed trajectory, but implements a reactive feedback strategy that can adapt online to changing goal states under the learned predictive–control loop. Importantly, this adaptation occurs without any online weight updates, indicating that robustness arises from the learned internal dynamics and state-dependent control mapping. 


Figure 28: **Robustness to within-episode target shifts.** Evaluation of a pretrained Pred-Control SNN under a simple targetperturbation protocol. Whenever the end-effector enters the success region, the target position is shifted to a new location (multiple times within a single 200-step episode). **Top:** Example 3D end-effector trajectories under three representative episodes, illustrating repeated re-targeting behavior. **Bottom:** Corresponding distance-to-target traces; each increase reflects a target shift, followed by rapid error reduction as the controller re-acquires the new target. No online learning is performed during this test. 

49 

# **Q Non-spiking RNN Baseline and Model Size Sweep** 

To contextualize the proposed spiking controller, we construct a non-spiking recurrent baseline for the **3D reaching task** that matches the SNN training pipeline as closely as possible. We reuse the same data collection, episode buffer, unrolling/BPTT loop, optimizer settings, losses, and action scaling; only the network implementation differs (standard floating-point PyTorch layers instead of spiking modules). 

**Architecture.** The baseline retains the same two-module structure (recurrent predictor + feedforward policy) and runs at the environment control rate (one recurrent step per control cycle) with the same unroll lengths as the SNN. As in the spiking setup, the predictor outputs a state increment ∆ˆ **_s_** _t_ and forms the next-state estimate as **_s_** ˆ _t_ +1 = **_s_** _t_ + ∆ˆ **_s_** _t_ under teacher forcing, or ˆ **_s_** _t_ +1 = **_s_** ˆ _t_ +∆ˆ **_s_** _t_ during autoregressive rollouts. We use an Elman RNN with ReLU nonlinearities for the predictor and the same bounded-action transformation for the policy (including tanh). No parameter compression (Appendix N) is applied. 

**Training objective and regularization.** The predictor is trained with the same supervised one-step objective as in the SNN pipeline, i.e., predicting **_s_** _t_ +1 from ( **_s_** _t,_ **_u_** _t_ ) under teacher forcing. The policy is trained via differentiable rollouts through the frozen predictor using the same multi-step objective; we also apply the same auxiliary penalty on the policy pre-tanh activation to reduce saturation-induced gradient collapse. In the results below, we distinguish between the one-step prediction objective ( _Pred. loss_ ) and the multi-step, autoregressive rollout error ( _Pred. MSE_ ), which can diverge even when one-step prediction is accurate. 

**Model size sweep.** We vary the number of neurons per layer _∈{_ 32 _,_ 128 _,_ 512 _,_ 2048 _}_ and set _all_ hidden layers in both predictor and policy to this width, keeping all other hyperparameters fixed. Table 4 summarizes the resulting parameter counts and final 3D control performance (means over 3 seeds), while Figure 29 reports learning curves over training. 

Overall, control performance improves strongly with model size: larger baselines converge faster, reach higher success rates, spend more time on target, and reduce cumulative distance more quickly. The one-step prediction objective remains well-behaved across sizes (low Pred. loss), but the largest model exhibits an outlier in long-horizon autoregressive prediction accuracy: while it achieves the best control metrics, its Pred. MSE spikes late in training for an outlier run (see Figure 29), which is surprising for the large model under constant teacher forcing. Since the same training protocol (including constant teacher forcing during predictor training) is used for both baseline and SNN, we report this behaviour as-is. Policy/task performance remains unaffected by this spike. 

Table 4: **Non-spiking RNN baseline on the 3D reaching task.** Models are evaluated at the final training iteration (means over 3 seeds; std omitted for clarity). All hidden layers in both predictor and policy use the stated width (neurons / layer). Note that **Pred. MSE** is a multi-step, autoregressive rollout error and can show outlier behaviour even when one-step prediction remains accurate (cf. Figure 29). 

|**Non-spiking baseline model**|||||
|---|---|---|---|---|
|Neurons / layer|32|128|512|2048|
|Policy parameters|1,868|19,724|275,468|4,247,564|
|Predictor parameters|3,219|37,395|542,739|8,462,355|
|**Total parameters**|**5,087**|**57,119**|**818,207**|**12,709,919**|
|Cumulative distance_↓_|2.479|1.129|0.794|**0.691**|
|Success rate_↑_|0.377|0.864|0.969|**0.970**|
|Time on target_↑_|0.031|0.226|0.492|**0.601**|
|Pred. MSE_↓_|0.144|0.074|**0.013**|18.587|


**Note on policy recurrence.** We also tested a recurrent policy variant under the same setup, but it did not improve performance and often reduced training stability; we therefore proceed with the feedforward policy baseline. 

50 


Figure 29: **Non-spiking RNN baseline (3D task): effect of model size.** Learning curves for neurons per layer _∈ {_ 32 _,_ 128 _,_ 512 _,_ 2048 _}_ applied to all hidden layers in both predictor and policy (3 seeds; mean _±_ s.e.m.). Control performance improves with model size across runs (higher success and time on target, lower cumulative distance), with the 512–2048 models converging fastest. While the one-step prediction objective (Pred. loss) remains low across sizes, the largest model shows an outlier in long-horizon autoregressive prediction error (Pred. MSE), illustrating that multi-step rollouts can degrade despite strong one-step fits. 

51 

# **R Hyperparameters** 

Below is a summary of key hyperparameters and their values used in our final Pred-Control SNN model. 

Table 5: **Overview of key hyperparameters in the final Pred-Control SNN.** Values reflect the best-performing configuration after ablations. 

|**Hyperparameter**|**Symbol**|**Final Value**|
|---|---|---|
|_Simulation and Training Setup_|||
|Simulation step|∆_t_|0.02 s (50 Hz), 7 SNN sub-steps|
|Episode length<br>|_T_|200 steps = 4 s<br>|
|Parallel environments|–|64|
|Random seeds|–|3|
|Success threshold|–|0.05 (2D), 0.123 m (3D)|
|Replay buffer size|_M_|6400 (full memory)|
|Mini-batches / iteration|_nυ, nπ_|25|
|Batch size|_Nυ, Nπ_|256|
|Warmup steps|_T_warm|10|
|Unroll steps (prediction/policy)|_T _<sup>_υ_</sup><br>unroll<sup>_, T π_</sup><br>unroll|40 / 40|
|Teacher forcing prob.|_ptf_|1.0|
|_Optimization_|||
|Learning rate (prediction / policy)|_αυ, απ_|10<sup>_−_3</sup>|
|Learning rate (time constants)|_ατ_|0_._01|
|Optimizer<br>|–|Adam<br>|
|Learning rate schedule|–|Constant|
|_Neuron Model_|||
|Membrane time constant|_τ_mem|10 ms (learned)|
|Synaptic time constant|_τ_syn|5 ms (learned)|
|Adaptation time constant|_τ_ada|100 ms (learned)|
|Initialization rate|_ν_|125 Hz|
|Threshold baseline|_ϑ_0|1.0|
|Resting potential|_U_rest|0|
|ALIF decay|∆_ϑ_|10|
|ALIF adaptation scale|_ξϑ_|0.1|
|_Surrogate Gradients_|||
|Surrogate function|–|Gaussian Spike|
|Steepness|_β_|16|
|Scaling factor|_γ_|1.0|
|_Network Architecture_|||
|Hidden layers|–|2 spiking + 1 readout|
|Recurrence|_ρ_|Prediction model only,_ρ_= 0_._9|
|Neurons per layer|–|512 (baseline), 2048 w/ compression|
|<br>Latent dimension|_d_|<br>64 (bottleneck)|
|_Regularization (Final Model)_|||
|Weight decay|_λL_2|Not used|
|Activity regularization|_λ_low_, λ_up|Not used|
|Action penalties|_λu, λu′_|Not used|
|Action noise|_σu_|Not used|


52 

