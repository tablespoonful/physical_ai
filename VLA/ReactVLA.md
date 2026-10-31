---
title: "ReactVLA: Fast and Lightweight Reactive Robot Manipulation via Improved Mean Flow Action Generation"
date: "2026-06-12"
authors: "Yanzhao Guo; Wenkai Chen; Jianwei Zhang"
url: https://arxiv.org/abs/2606.14255
pdf: https://arxiv.org/pdf/2606.14255
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.14255)** / [論文ページ](https://arxiv.org/abs/2606.14255)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ReactVLA: Fast and Lightweight Reactive Robot Manipulation via Improved Mean Flow Action Generation** 

Yanzhao Guo<sup>1</sup> , Wenkai Chen<sup>2</sup> , Jianwei Zhang<sup>2</sup> 

**_Abstract_ — Diffusion-based Vision-Language-Action (VLA) policies have demonstrated strong capability in modeling expressive and multimodal action distributions. However, their reliance on iterative sampling introduces substantial inference latency, which limits their applicability to reactive closed-loop robot manipulation. To address this limitation, we propose ReactVLA, a lightweight and low-latency VLA framework for real-time robotic manipulation. ReactVLA combines two complementary designs: (1) an improved Mean Flow (iMF) action generator that reduces expensive multi-step diffusion sampling to one-to-few-step action generation, and (2) Attention Residuals (AttnRes), a dynamic depth-wise feature routing mechanism that replaces uniform residual accumulation to better preserve task-relevant multimodal representations. We evaluate ReactVLA on large-scale simulation benchmarks, including LIBERO and RoboIMI, as well as real-world robotic manipulation tasks. Experimental results show that ReactVLA consistently outperforms similarly sized VLA baselines, including SmolVLA and** _π_ 0 **. On challenging precision manipulation tasks, ReactVLA achieves up to a 1.65** _×_ **improvement in task performance while providing more than a 4** _×_ **increase in inference speed compared with leading VLA models. Finally, it reduces real-world policy latency to below 38.6 ms, enabling fast reactive control on physical robot platforms. Please check out our project website at: https://game-loader. github.io/ReactVLA/.** 

## I. INTRODUCTION 

Learning-based robot manipulation increasingly relies on expressive generative policies to model the complex, multimodal action distributions arising from human demonstrations. Diffusion-based visuomotor policies, in particular, have demonstrated remarkable manipulation performance by formulating action generation as an iterative denoising process [1], inheriting the strong representational capacity of modern diffusion generative models [2]. Recent VisionLanguage-Action (VLA) systems further scale this paradigm through large multimodal transformers, enabling instructionconditioned robotic control across diverse manipulation tasks. Despite these advances, generative robot policies remain fundamentally constrained by inference latency. Standard diffusion-style action generation requires dozens of sequential denoising evaluations during deployment, often resulting in inference times of hundreds of milliseconds per control cycle [3]. Such latency severely limits the highfrequency closed-loop interaction required for reactive robot manipulation, where policies must continuously adapt to contact dynamics, object motion, and execution uncertainty 

> 1Shanghai Jiao Tong University 

> 2Technical Aspects of Multimodal Systems (TAMS), Department of Informatics, Universit¨at Hamburg. email: wenkai.chen@uni-hamburg.de 


Fig. 1. **Comparison of VLA Models across Model Size, Inference Latency, and Task Success Rate.** We compare ReactVLA against competitive VLA baselines (such as SmolVLA and _π_ 0). Our method achieves the best average success rate among compared lightweight VLA models while maintaining a low inference latency, providing a practical trade-off for real-time reactive robotic control. 

in real time. This raises a central question: can generative robot policies preserve the expressive advantages of diffusion-style action modeling while reducing inference to only one or a few evaluations? In this work, we address this challenge through ReactVLA, a low-latency generative manipulation framework designed for reactive VLA control. 

To reduce the computational burden of iterative sampling, we adapt improved Mean Flow (iMF) to robot action generation. Unlike standard flow matching methods that rely on instantaneous local velocity fields [4], [5], Mean Flow models finite-interval average transport, naturally supporting stable one-to-few-step generation [6], [7]. Since lowstep generation increases the representational demand on each policy evaluation, ReactVLA further introduces Attention Residuals (AttnRes), a dynamic depth-wise routing mechanism for multimodal policy transformers. Instead of uniformly accumulating layer outputs through fixed residual paths [8], [9], AttnRes selectively retrieves informative historical representations across transformer depth [10]. 

By combining iMF action generation with AttnRes-based feature routing, ReactVLA forms a fast and lightweight VLA framework for reactive robot manipulation. As illustrated in Fig. 1, our method achieves a favorable trade-off by combining strong success rates with a lightweight model footprint and low inference latency, making it well suited for high-frequency, reactive closed-loop robot control. Our contributions are summarized as follows: 

- 1) We propose ReactVLA, a low-latency VisionLanguage-Action framework that reformulates robot 


Fig. 2. Overview of the ReactVLA framework. Multimodal observations are processed by an Attention Residual Transformer backbone, while the proposed improved Mean Flow (iMF) action head directly transports noisy actions toward the target action distribution through one-to-few-step generation. 

   - action generation through improved Mean Flow, enabling stable one-to-few-step generative manipulation. 

- 2) We introduce an Attention Residual transformer backbone that performs dynamic depth-wise feature routing, mitigating multimodal representation dilution in deep policy transformers under aggressive low-step inference. 

- 3) We demonstrate strong manipulation performance across diverse simulation and real-world benchmarks while substantially reducing inference latency. ReactVLA achieves an average 15.2 _×_ higher inference throughput than diffusion-based policies, while outperforming competitive VLA baselines such as SmolVLA and _π_ 0 on LIBERO and RoboIMI benchmarks. 

## II. RELATED WORK 

## _A. Diffusion and Flow Policies for Robot Action Generation_ 

Generative action models have become a central paradigm for imitation-based robot manipulation. Diffusion Policy formulates visuomotor control as conditional denoising over action sequences, enabling expressive multimodal action distributions for manipulation tasks [1], [2]. Subsequent work has scaled this idea with Transformer backbones and VLA models, extending generative policy learning to broader task distributions and language-conditioned settings [3], [11], [12]. Despite their effectiveness, these approaches typically rely on iterative sampling, making inference cost a key bottleneck for high-frequency robot control. Flow-based generative policies provide an alternative view by learning continuous vector fields that transport noise to data [4]. Rectified Flow further improves sampling efficiency by encouraging straighter transport paths, reducing the number of function evaluations required at inference [5]. These methods motivate fast action generation, but standard flow 

formulations still model local instantaneous velocities and can suffer from truncation error under extremely low-step sampling. Our ReactVLA follows this fast-generation direction but shifts the action generator from local velocity prediction to finite-interval mean transport. By adapting iMF to VLA action generation, our method directly predicts average velocity fields for one-to-few-step action synthesis, targeting the latency requirements of reactive robot manipulation while retaining the expressiveness of generative policies. 

## _B. Residual Connections and Attention Residuals_ 

Residual connections are a fundamental component of deep neural architectures, enabling stable optimization and gradient propagation across depth [8]. In large Transformer models, however, standard residual accumulation can progressively dilute intermediate representations due to repeated unweighted feature aggregation [13]. To improve information propagation, prior work has explored gated residual pathways [14], multi-stream residual architectures [15], [16], and learned depth-wise aggregation strategies [17]. Recent work on Attention Residuals reformulates residual accumulation as an input-dependent retrieval process across transformer depth [10]. Rather than uniformly summing historical layer outputs, AttnRes enables each layer to dynamically retrieve informative intermediate representations through depth-wise attention routing. While originally developed for large-scale language modeling, its potential for multimodal robot policy learning remains largely unexplored. In particular, low-step generative policies place substantially greater representational demands on each policy evaluation, since action quality must be achieved with only a few generation steps. We therefore introduce AttnRes into a VLA policy and investigate its effectiveness for multimodal manipulation. Our results show that dynamic depth- 


Fig. 3. **Comparison of the Flow Matching, Mean Flow, and Improved Mean Flow.** Standard flow matching models local instantaneous transport, requiring fine-grained integration along curved trajectories. Mean Flow instead learns finite-interval average transport, enabling large-step generation. Improved Mean Flow further stabilizes training through a Jacobian-Vector Product (JVP) correction with stop-gradient constraints. 

wise routing helps preserve useful visual, language, and proprioceptive representations throughout the transformer, providing a stronger context representation for low-latency action generation. 

## III. PROBLEM SETTING AND FRAMEWORK OVERVIEW 

We consider language-conditioned robot manipulation under a VLA-based imitation learning framework. At each control step _t_ , the policy receives a multimodal observation _ot_ = _{It, st, l}_ , where _It_ , _st_ , and _l_ denote visual observations, robot proprioceptive states, and the task instruction, respectively. Conditioned on _ot_ , the policy predicts a future action chunk _at_ : _t_ + _H ∼ πθ_ ( _· | ot_ ) over horizon _H_ . Our goal is to learn a generative policy that produces highfidelity action chunks with a small inference budget _N_ infer, enabling high-frequency reactive control from streaming sensory feedback. 

To reduce the deployment cost of iterative diffusion-style sampling, ReactVLA replaces local denoising with lowstep mean flow action generation. As illustrated in Fig. 2, multimodal observations are encoded by an Attention Residual Transformer with dynamic depth-wise feature routing. The resulting representations condition an improved Mean Flow action head, which predicts finite-interval transport from noisy actions to the target action distribution and enables one-to-few-step action generation. Training uses a robust Pseudo-Huber objective for stable low-step action optimization. The key components are described next. 

## IV. METHOD 

## _A. Improved Mean Flow for Action Generation_ 

As illustrated in Fig. 3(a), classical Flow Matching formulates generation through instantaneous velocity fields that locally transport samples along continuous trajectories. While expressive, such local transport requires fine-grained numerical integration and becomes increasingly unstable under aggressive low-step inference, where discretization errors rapidly accumulate along potentially curved trajectories. To alleviate this limitation, Mean Flow [6] replaces instantaneous transport with finite-interval average transport over a macroscopic interval [ _r, t_ ], where 0 _≤ r < t ≤_ 1. 

Instead of modeling the local velocity field _v_ ( _zt, t_ ), Mean Flow directly predicts the average transport velocity 


where _zt_ denotes the noisy latent action state. This formulation enables large-step transport across the generation trajectory and substantially reduces the number of inference evaluations required during action generation. 

However, as shown in Fig. 3(b), directly optimizing the mean velocity field can introduce path inconsistency between the conditional transport target and the marginal velocity dynamics, leading to unstable optimization under low-step training. To mathematically capture and resolve this inconsistency, we analyze the relationship between the average velocity field _u_ ( _zt, r, t_ ) and the instantaneous velocity field _v_ ( _zt, t_ ), where the latent action trajectory _zt_ at continuous time _t ∈_ [0 _,_ 1] satisfies the ordinary differential equation (ODE)<sup>_<u>dz</u>_</sup> _dt_<sup>_<u>t</u>_=</sup><sup>_v_(</sup><sup>_zt, t_).</sup> 

Multiplying both sides of Eq. 1 by ( _t − r_ ) yields the accumulated flow: 


Differentiating this relation with respect to _t_ on both sides using the Leibniz rule yields: 


Rearranging this equation, we express the average velocity field as: 


The total derivative of the average velocity _u_ ( _zt, r, t_ ) with respect to time _t_ along the trajectory must account for both the explicit dependence on _t_ and the implicit dependence via the state _zt_ . Applying the chain rule, we write this total derivative as: 


This operation can be cast as a Jacobian-Vector Product (JVP) of the average velocity function _u_ with respect to the input variables ( _zt, r, t_ ) along the tangent direction ( _v_ ( _zt, t_ ) _,_ 0 _,_ 1): 


Substituting Eq. 6 back into Eq. 4 yields: 


In practice, since we train a neural network _uθ ≈ u_ to represent the average flow, directly optimizing this nonlinear relation is highly unstable during training. To address this issue, we adopt Improved Mean Flow (iMF) [7], which introduces a Jacobian-Vector Product correction to align the 

average transport prediction with the underlying instantaneous velocity field: 


where _uθ_ ( _zt, r, t_ ) denotes the predicted average transport velocity and _vθ_ ( _zt, t_ ) = _uθ_ ( _zt, t, t_ ) represents the instantaneous velocity prediction obtained from the same network. The stop-gradient operator (sg) stabilizes the nonlinear correction term while preserving consistency between the conditional transport target and the marginal vector field. During deployment, the policy directly performs finiteinterval action transport using the learned average-flow predictor _uθ_ , enabling stable one-to-few-step action generation for low-latency robot control. 

## _B. Attention Residual Policy Transformer_ 

The Attention Residual policy transformer serves as the policy core, taking multimodal observation features and processing them via dynamic depth-wise routing. Specifically, at each control step _t_ , the input sequence _X ∈_ R<sup>_L×d_model</sup> is constructed by concatenating temporal, conditioning, and action tokens: 


where _d_ model = 768 is the hidden dimension of the transformer, _r, t ∈_ [0 _,_ 1] are the flow time steps mapped to _d_ modeldimensional sinusoidal embeddings _ϕ_ ( _r_ ) _, ϕ_ ( _t_ ) _∈_ R<sup>1</sup><sup>_×_768</sup> followed by linear projection, _zt ∈_ R<sup>_H×da_</sup> is the noisy action trajectory ( _H_ = 16, _da_ = 7) projected to _Wazt ∈_ R<sup>16</sup><sup>_×_768</sup> , and _C_ represents the multimodal conditioning sequence. 

The conditioning sequence _C_ is formed by concatenating visual, textual, and proprioceptive tokens: 


where _E_ vis( _I_ agent) _∈_ R<sup>_N_vis</sup><sup>_×d_vis</sup> and _E_ vis( _I_ wrist) _∈_ R<sup>_N_vis</sup><sup>_×d_vis</sup> represent the spatial features extracted from the agent camera and wrist camera views using a frozen SigLip2 image encoder ( _N_ vis = 256, _d_ vis = 1152), _E_ text( _l_ ) _∈_ R<sup>_N_text</sup><sup>_×d_text</sup> represents the textual instruction tokens from a SmolVLM text encoder ( _d_ text = 2048), and _E_ prop( _st_ ) _∈_ R<sup>1</sup><sup>_×_768</sup> is a single proprioceptive token. The proprioceptive token is obtained by linearly projecting the 8-dimensional proprioceptive joint state _st ∈_ R<sup>8</sup> using a learnable projection matrix _W_ prop _∈_ R<sup>8</sup><sup>_×_768</sup> plus a bias term: 


All conditioning tokens in _C_ are projected to the model dimension _d_ model = 768 via a projection matrix _Wc_ before sequence injection. The resulting total sequence length of the transformer is _L_ = 2 + 2 _N_ vis + _N_ text + 1 + _H_ . 

Deep transformer policies commonly employ residual connections to stabilize optimization across depth. However, standard PreNorm residual accumulation uniformly aggregates historical layer outputs, which can progressively dilute multimodal representations in deep policy transformers [8], 

## **Algorithm 1** One training iteration of ReactVLA 

- **Input:** action _a_ , context _c_ , parameters _θ_ , Pseudo-Huber scale _δ_ . **Output:** training loss _L_ 

- 1: _h_ ctx _←_ AttnResTransformer _θ_ ( _c_ ) 2: Sample time steps _r, t_ with _r ≤ t_ , and sample _ϵ ∼ N_ (0 _, I_ ) 

- 3: _zt ←_ (1 _− t_ ) _a_ + _tϵ_ , _vg ← ϵ − a_ 4: _vθ ← uθ_ ( _zt, t, t | h_ ctx) 5: _u, u_ ˙ _←_ JVP( _uθ_ ( _· | h_ ctx) _,_ ( _zt, r, t_ ) _,_ ( _vθ,_ 0 _,_ 1)) 6: _Vθ ← u_ + ( _t − r_ )sg( ˙ _u_ ) 7: _L ←_ PseudoHuber _δ_ ( _Vθ − vg_ ) 8: **return** _L_ 

[13]. A detailed derivation of the PreNorm accumulation formulation is provided in Appendix VII-A. Such representation dilution becomes particularly problematic under lowstep action generation, where each policy evaluation must preserve sufficient visual and proprioceptive information for accurate action prediction. To mitigate this issue, our ReactVLA adopts Attention Residuals [10], which replaces fixed residual accumulation with dynamic depth-wise feature routing: 


where _vi_ denotes the historical representation from layer _i_ , and _αi→l_ represents the routing weight assigned by layer _l_ . The routing weights are computed through a lightweight layer-specific query: 


where _wl_ is a learnable routing vector. This formulation enables the policy transformer to dynamically preserve informative multimodal features across depth, improving representation stability for low-latency action generation. 

## _C. Pseudo-Huber Loss for Stable Action Optimization_ 

Low-step action generation can occasionally produce large transport errors during early training, particularly when the predicted mean flow dynamics are still poorly aligned with the target action trajectory. To improve optimization stability, we train the action generator using the PseudoHuber loss instead of the standard Mean Squared Error (MSE) objective. 

Let 


denote the prediction error between the corrected mean flow prediction _Vθ_ and the target transport velocity _vg_ . For each error dimension _ed_ , the Pseudo-Huber loss is defined as 


where _δ >_ 0 controls the transition between quadratic and linear error penalization. The overall training objective is computed as 


To understand why the Pseudo-Huber loss is crucial for stabilizing ReactVLA’s training, we analyze its gradient propagation behavior. Under the training objective, the parameters _θ_ are updated via the gradient: 


where the derivative of the Pseudo-Huber loss with respect to the error dimension _ed_ is given by: 


Equation 17 reveals that as the error magnitude _|ed| →∞_ , _∂ρδ_ <u>(</u> _ed_ <u>)</u> the term _∂ed →±δ_ , meaning the gradient factor is strictly bounded within [ _−δ, δ_ ]. In contrast, standard Mean Squared Error (MSE) loss yields<sup>_<u>∂L</u>_</sup> _∂e_<sup><u>MSE</u></sup> _d_ = _ed_ , which scales linearly without bound. 

This bounding behavior is critical when optimizing policies with JVP corrections. The corrected velocity prediction _Vθ_ (Eq. 8) contains the first-order spatial derivatives of _uθ_ to form the JVP. Consequently, backpropagating the loss to compute the parameter gradient<sup>_<u>∂e</u>_</sup> _∂θ_<sup>_<u>d</u>_requirestaking</sup> derivatives through the JVP term, which introduces secondorder derivatives of the neural network _uθ_ . During the early phases of training, the predicted mean flow velocity fields are unaligned and highly non-linear, which easily produces extremely large prediction errors _ed_ and highvariance second-order gradients in<sup>_<u>∂e</u>_</sup> _∂θ_<sup>_<u>d</u>_. Under an MSE loss,</sup> these two factors multiply, causing catastrophic gradient spikes that destabilize training (as observed in Fig. 5). By bounding the error feedback via Eq. 17, the Pseudo-Huber loss acts as an inherent gradient-clipping mechanism at the loss level, preventing large transport deviations from propagating high-magnitude updates through the second-order JVP path, thereby ensuring smooth and stable optimization. 

A detailed analysis of the asymptotic behavior of the Pseudo-Huber formulation is provided in Appendix VIIB. Algorithm 1 further summarizes one training iteration of ReactVLA, including multimodal feature routing, improved Mean Flow prediction, JVP correction, and robust action optimization. The exact time-step sampling strategy is described in Appendix VII-D. 

V. EXPERIMENTS 

## _A. Setup and Metrics_ 

To validate the efficiency and precision of our proposed ReactVLA framework, we perform extensive evaluations across two simulation benchmarks and one real-world robotic platform: 

- **LIBERO Benchmark:** A standard suite for VLA robot learning models. To ensure a fair comparison, the training and evaluation protocols (including the evaluation metrics and episode setups) strictly follow the pipeline of SmolVLA [19]. 

- **RoboIMI Simulation Platform:** A custom-built, dualarm robotic simulation environment designed for coordinated, tight-tolerance manipulation. We evaluate all comparative policies across 100 evaluation trials per task and report the average cumulative reward and inference latency. We evaluate on two challenging tasks: 

   - _Peg-in-Socket:_ One arm picks up a wooden peg from the table and inserts it into a rectangular socket held dynamically by the other robotic arm. 

   - _Object Transfer:_ One arm picks up a wooden block from the table and transfers it to the gripper of the other arm. 

- **Diana Robot Platform:** A physical single-arm robotic platform equipped with a Diana 7 robotic arm from Agile Robots. We evaluate our framework and baseline methods over 20 runs per task on two real-world manipulation tasks: Orange Pick-and-Place and Block Stack. The robot is required to grasp an orange and place it stably on a plate in Orange Pick-and-Place, and to stack a wooden block on a pre-existing block stack in Block Stack. We report the task success rate and physical inference latency. 

## _B. Simulation Experiments on LIBERO_ 

We evaluate our proposed ReactVLA on the widely used LIBERO benchmark [19], following the multi-task protocols of SmolVLA [19]. As shown in Table I, our policy achieves a strong average success rate of 88 _._ 0%, outperforming representative VLA models across most task categories. Crucially, while standard diffusion- or flow-based VLA models require multiple sampling or integration steps to generate smooth actions, ReactVLA achieves this using only 2 steps. This reduction lowers the policy latency to 18 _._ 3 ms (54 _._ 6 Hz) while maintaining strong manipulation performance, demonstrating the effectiveness of low-step action generation for efficient robot control. 

## _C. Simulation Experiments on RoboIMI_ 

We evaluate our model on the custom-built RoboIMI simulation platform, which serves as a bimanual robotic environment to test coordinated and high-precision manipulation. We perform rollouts on two tasks: Peg-in-Socket and Object Transfer. The overall performance comparison of different policy models across both tasks is summarized in Table II. The results show that our proposed ReactVLA significantly outperforms all baseline methods in terms of average reward, while executing at exceptionally low inference latencies (approximately 15 ms). On the challenging peg-in-socket task, our method achieves an average reward of 1513.56, outperforming Diffusion Policy by 48 _._ 5% while reducing latency from 398 _._ 0 ms to 15 _._ 1 ms. On the bimanual 

TABLE I 

SIMULATION RESULTS ON LIBERO BENCHMARK. SUCCESS RATES (%) FOR VARIOUS POLICIES ACROSS DIFFERENT TASK CATEGORIES (SPATIAL, OBJECT, GOAL, LONG-HORIZON). WE INCLUDE THE INFERENCE LATENCY (MS) FOR DIRECT COMPARISON. 

|Method|# Params|Su|ccess Rate|(%) —|Simulation||Latency (ms)|
|---|---|---|---|---|---|---|---|
|||Spatial|Object|Goal|Long|Avg.||
|Diffusion Policy [1]|0.46B|78.3|92.5|68.3|50.5|72.4|178.82|
|OpenVLA [18]|6.74B|84.7|88.4|79.2|53.7|76.5|115.0|
|_π_0 (Paligemma-3B) [3]|5.97B|87.0|63.0|89.0|48.0|71.8|94.3|
|_π_0 [3]|4.03B|90.0|86.0|95.0|73.0|86.0|93.4|
|SmolVLA [19]|**0.24B**|87.0|93.0|88.0|63.0|82.8|71.1|
|SmolVLA [19]|0.45B|90.0|**96.0**|**92.0**|71.0|87.3|74.1|
|**ReactVLA (Ours)**|0.39B|**93.0**|95.0|**92.0**|**72.0**|**88.0**|**18.3**|


TABLE II 

PERFORMANCE COMPARISON ON ROBOIMI SIMULATION TASKS (PEG-IN-SOCKET INSERTION AND OBJECT TRANSFER) OVER 100 EVALUATION ROLLOUTS. WE REPORT THE AVERAGE REWARD FOR EACH TASK AND THE POLICY INFERENCE LATENCY (MS). 


Fig. 4. **Ablation Study on Attention Residuals in LIBERO Simulation** . We compare ReactVLA against the vanilla baseline that uses standard uniform additive residual connections. 


Fig. 5. **Ablation Study on Loss Formulations.** Comparison of training loss trajectories (left) and evaluation success rates (right) between PseudoHuber Loss (Ours) and MSE Loss over 60k training steps. 

handover task, it achieves an average reward of 526.22, exceeding the standard Diffusion Policy baseline at 319 _._ 20 with a low latency of 15 ms. Notably, the SmolVLA baseline failed to achieve successful policy convergence on this dual-arm setup, consistently yielding zero rewards due to training complexities; its performance metrics are therefore omitted and denoted as “–” in the table. These results demonstrate that ReactVLA successfully resolves the speed-quality trade-off, enabling both highly accurate and real-time reactive control for coordinated bimanual manipulation. 

## _D. Ablation Studies_ 

**Attention Residuals:** To analyze the impact of the Attention Residual structure on the model’s training dynamics, we compare our full model, ReactVLA, which incorporates dynamic layer-specific softmax residuals, against a vanilla baseline variant, ReactVLA-Vanilla (where AttnRes is replaced with standard uniform additive residuals). As 

shown in Fig. 4, ReactVLA achieves significantly improved final performance. The evaluation success rate of ReactVLA (right panel) rises much faster, surpassing 50% within the first 40k steps and converging to a peak success rate of 88 _._ 0%, whereas the vanilla model converges more slowly to a final success rate of only 28 _._ 7%. This confirms that dynamic depth-wise attention helps prevent feature dilution and eases optimization. 

**Loss Formulations (Pseudo-Huber vs. MSE):** We further investigate the influence of action-generation loss formulations by comparing the Pseudo-Huber loss used in our framework against the standard Mean Squared Error (MSE) loss. As illustrated in Fig. 5, the choice of loss function plays a critical role in training stability. The model trained with MSE loss suffers from frequent loss spikes and severe gradient instability, which is primarily induced by explosive Jacobian-Vector Products during backpropagation when handling large action deviations. In contrast, the model trained with Pseudo-Huber loss exhibits a highly stable and 


Fig. 6. **Qualitative Comparison of Manipulation Rollouts.** In simulation, ReactVLA generates smoother trajectories compared to SmolVLA. The rollout keyframes are sampled at 1s, 2s, 3s, and 4s due to the relatively short overall duration of LIBERO simulation trials. 


Fig. 7. **Qualitative Rollouts in RoboIMI Dual-Arm Tasks.** ReactVLA coordinates both robotic arms smoothly during peg-in-socket insertion and block handover compared to the standard Diffusion Policy. The keyframes are chosen at 0s, 4s, 8s, and 12s because RoboIMI simulation episodes have a much longer execution duration, typically lasting dozens of seconds. 

smooth convergence curve. By sub-linearly scaling large errors, the Pseudo-Huber loss effectively bounds the vector magnitudes within the JVP computations, providing robust gradient behavior during action trajectory optimization and preventing training destabilization. 

## _E. Qualitative Evaluation and Visualization_ 

To qualitatively evaluate the performance of ReactVLA, we visualize and compare the rollout trajectories of our policy against baseline models in simulation. Fig. 6 illustrates the qualitative rollout frames on the LIBERO benchmark tasks, comparing our method against SmolVLA. Fig. 7 shows the rollout comparison on the RoboIMI simulation platform tasks against Diffusion Policy. Crucially, because ReactVLA achieves a much faster inference speed and lower latency, it can execute more policy control steps within the same physical time duration. Consequently, at the same physical elapsed time, ReactVLA progresses faster and 

is significantly closer to completing the task, whereas the baseline models lag behind due to their slower inference. For instance, in the RoboIMI bimanual block handover task (Fig. 7), at _t_ = 8 s, ReactVLA has already coordinated both arms to secure the block and initiate the handover process, whereas the standard Diffusion Policy is still slow to react and remains in the initial approach stage. Similarly, for the LIBERO benchmark tasks (Fig. 6), because of the rapid execution enabled by our low-latency design, ReactVLA completes the manipulation sequence significantly ahead of SmolVLA within the same physical time (visualized at keyframes 1s, 2s, 3s, and 4s). 

## _F. Real-World Robot Experiments_ 

To verify the transferability and low-latency performance of ReactVLA on physical systems, we deploy our framework on the Diana 7 robotic arm for both the Orange Pick-and-Place and Block Stack tasks, as illustrated in 


Fig. 8. **Real-World Robot Experiments.** (Left) Demonstration of the Orange Pick-and-Place and Block Stack tasks on the Diana 7 robotic arm. (Right) Performance comparison (success rate vs. latency) of our method against baseline models in real-world deployment. 

Fig. 8. These tasks require precise end-effector control and responsive visuomotor feedback. We collect 50 teleoperated demonstrations for each task to perform model training. The inputs to ReactVLA include egocentric wrist camera views, a third-person camera feed, and the robot’s joint states, while the output is target joint commands executed at 60 Hz. In physical testing, our low-step policy achieves an average latency of 38.6 ms, allowing the robot to adapt reactively to perturbations. Over 20 evaluation trials on the Orange Pick-and-Place task, both ReactVLA and the SmolVLA baseline achieve a high success rate of 95% (19/20 runs). However, on the more challenging Block Stack task, ReactVLA achieves a success rate of 90% (18/20 runs), outperforming SmolVLA, which drops to 75% (15/20 runs) due to error accumulation in its slower control loop. Furthermore, SmolVLA exhibits a higher inference latency of 82.2 ms. This demonstrates that our fast action generation is critical for enabling tighter, real-time closedloop feedback and more fluent reactive control in physical environments. 

## VI. CONCLUSION 

We presented ReactVLA, a low-latency, lightweight VLA framework for reactive robot manipulation. Our approach combines an improved Mean Flow action generator with an Attention Residual transformer backbone, enabling one-to-few-step action generation while preserving the multimodal representations required for accurate policy execution. Across LIBERO, RoboIMI, and real-world robot experiments, ReactVLA achieves strong manipulation performance with substantially reduced inference latency, demonstrating that efficient generative action modeling can be realized without sacrificing control quality. By shifting from local iterative denoising to finite-interval transport prediction and dynamic depth-wise feature routing, ReactVLA offers a practical path toward real-time, closed-loop robot manipulation. Despite promising results, several limitations remain. First, our real-world evaluation focuses on a controlled tabletop manipulation setting with a relatively small number of demonstrations. Extending ReactVLA to more diverse environments, longer-horizon tasks, and highly cluttered scenes remains an important direction for future work. Second, although all methods were evaluated on identical hardware within each benchmark to ensure fair comparisons, different benchmark suites were conducted 

on different GPU platforms. Consequently, absolute latency measurements should be interpreted within each benchmark, while the reported relative speedups more directly reflect the computational efficiency of the underlying action-generation algorithms. 

## REFERENCES 

- [1] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. C. M. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems_ , 2023. 

- [2] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” in _Advances in Neural Information Processing Systems_ , 2020. 

- [3] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-languageaction flow model for general robot control,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [4] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _International Conference on Learning Representations_ , 2023. 

- [5] X. Liu, C. Gong, and Q. Liu, “Flow straight and fast: Learning to generate and transfer data with rectified flow,” in _International Conference on Learning Representations_ , 2023. 

- [6] Z. Geng, M. Deng, X. Bai, J. Z. Kolter, and K. He, “Mean flows for one-step generative modeling,” in _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [7] Z. Geng, Y. Lu, Z. Wu, E. Shechtman, J. Z. Kolter, and K. He, “Improved mean flows: On the challenges of fastforward generative models,” _arXiv preprint arXiv:2512.02012_ , 2025. 

- [8] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _IEEE Conference on Computer Vision and Pattern Recognition_ , 2016. 

- [9] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention is all you need,” in _Advances in Neural Information Processing Systems_ , 2017. 

- [10] Kimi Team, “Attention residuals,” _arXiv preprint arXiv:2603.15031_ , 2026. 

- [11] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _IEEE/CVF International Conference on Computer Vision_ , 2023. 

- [12] W. Chen, C. Xiao, G. Gao, F. Sun, C. Zhang, and J. Zhang, “Dreamarrangement: Learning language-conditioned robotic rearrangement of objects via denoising diffusion and vlm planner,” _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ , 2025. 

- [13] R. Xiong, Y. Yang, D. He, K. Zheng, S. Zheng, C. Xing, H. Zhang, Y. Lan, L. Wang, and T.-Y. Liu, “On layer normalization in the transformer architecture,” in _International Conference on Machine Learning (ICML)_ , 2020. 

- [14] R. K. Srivastava, K. Greff, and J. Schmidhuber, “Highway networks,” _arXiv preprint arXiv:1505.00387_ , 2015. 

- [15] D. Zhu, H. Huang _et al._ , “Hyper-connections,” in _International Conference on Learning Representations (ICLR)_ , 2025. 

- [16] Z. Xie, Y. Wei, H. Cao, C. Zhao, C. Deng, J. Li, D. Dai, H. Gao, J. Chang, L. Zhao, S. Zhou, Z. Xu, Z. Zhang, W. Zeng, S. Hu, Y. Wang, J. Yuan, L. Wang, and W. Liang, “mhc: Manifoldconstrained hyper-connections,” _arXiv preprint arXiv:2512.24880_ , 2025. 

- [17] M. Pagliardini, A. Mohtashami, F. Fleuret, and M. Jaggi, “Denseformer: Enhancing information flow in transformers via depth weighted averaging,” in _Advances in Neural Information Processing Systems_ , 2024. 

- [18] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ , 2025. 

- [19] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [20] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Robotics: Science and Systems (RSS)_ , 2023. 

## VII. APPENDIX 

## _A. PreNorm Representation Accumulation_ 

In a standard Transformer architecture with Pre-Layer Normalization (PreNorm), the hidden state _hl ∈_ R<sup>_d_</sup> entering the _l_ -th layer is updated recurrently. Let _fl−_ 1 denote the transformation computed by the ( _l−_ 1)-th layer. The standard PreNorm update can be written as: 


Unrolling this recurrence from the initial layer input _h_ 1, which represents the observation and instruction context embeddings, gives: 


This formulation reveals a structural limitation of standard PreNorm residual connections: all preceding layer outputs are accumulated with fixed unit weights. As the depth increases, the norm of the accumulated hidden state can grow with depth, making the incremental contribution of each newly added layer relatively smaller compared with the already accumulated representation. Consequently, deeper layers may have limited ability to introduce sufficiently distinct or task-relevant transformations, effectively reducing the useful depth of the network and leading to representation dilution. The Attention Residual mechanism addresses this limitation by replacing fixed residual accumulation with softmax-normalized, input-dependent routing over preceding layer representations, enabling each layer to selectively aggregate the most relevant historical features for final action decoding. 

## _B. Asymptotic Limits of the Pseudo-Huber Loss_ 

The Pseudo-Huber loss is defined for each dimension _d ∈ {_ 1 _, . . . , D}_ of the velocity prediction error _ed ∈_ R as: 


where _δ >_ 0 is the scale parameter. We analyze the asymptotic behavior of _ρδ_ ( _ed_ ) under the two extremes: small errors and large errors. 

_a) Case 1: Small Errors (|ed| ≪ δ):_ When the error magnitude is much smaller than the scale parameter _δ_ , the ratio<sup>_<u>e</u>_</sup> _δ_<sup>_<u>d</u>_issmall.WecanapplytheTaylorseriesexpansion</sup> for the function<sup>_~~√~~_</sup> 1 + _x_ around _x_ = 0, which is: 


Setting _x_ = <u>�</u> _<u>eδd</u>_ <u>�2,</u> we have: 


Substituting this expansion back into 22: 


Thus, to the first-order approximation: 


which is equivalent to the standard L2 (Mean Squared Error) loss scaled by 1 _/_ 2. 

_b) Case 2: Large Errors (|ed| ≫ δ):_ When the error magnitude is much larger than _δ_ , the ratio<sup>_<u>e</u>_</sup> _δ_<sup>_<u>d</u>_isverylarge.</sup> We can approximate the square root term as: 


Since _<u>δ</u> ≪_ 1, we can apply the Taylor expansion _|ed|_ _<u>δ</u>_ _~~√~~_ 1 + _y ≈_ 1 +<sup><u>1</u></sup> 2<sup>_y_with</sup><sup>_y_=</sup> <u>�</u> _ed_ �2: 


Thus, we obtain: 


Substituting this back into 22 yields: 


As _|ed| →∞_ , the term 2 _|δe_<sup>3</sup> _d|_<sup>approacheszero,sothe</sup> dominant terms are: 


which represents a linear L1-like loss with slope _δ_ and a constant offset. This formulation prevents outlier errors from generating excessively large gradients. 

## _C. Details of Model Architecture_ 

We instantiate ReactVLA as a vision-languageconditioned action flow model operating directly within the continuous action space. Each multimodal observation step incorporates dual-view RGB inputs, a global third-person view (agentview ~~i~~ mage) and an eye-in-hand view (robot0 ~~e~~ ye ~~i~~ n ~~h~~ and ~~i~~ mage), both rendered at a 256 _×_ 256 resolution, alongside an 8-dimensional robot proprioceptive joint state and a natural language task instruction. The policy predicts 7-dimensional relativecontrol actions over a temporal trajectory horizon of _H_ = 16 and executes an action chunk size of _K_ = 8 steps per inference cycle, conditioned on a single historical observation step ( _n_ obs = 1). 

For visual-language conditioning, we utilize a decoupled multimodal embedding pipeline. Specifically, we employ a frozen SigLip2 architecture as the visual encoder to extract spatial features from the input images, which are resized and normalized appropriately. Concurrently, the natural language task instruction is processed by the text transformer layers of the SmolVLM model, serving as our dedicated language encoder to capture semantic context. The visual tokens from both camera views, the textual tokens from the language encoder, and a single proprioceptive state token (obtained by linearly projecting the 8-dimensional joint state to match the transformer’s hidden dimension) are concatenated to form a unified multimodal conditioning sequence _C_ . These conditioning tokens are linearly mapped to the action head hidden dimension of 768 prior to sequence injection. 

The action generation head consists of a 16-block Attention Residual (AttnRes) Transformer operating on a combined sequence comprising temporal embeddings, the conditioning context tokens, and 16 action latent tokens: 


where _r_ and _t_ represent the source and target flow time steps, _ϕ_ ( _·_ ) denotes a sinusoidal time embedding followed by a linear projection, _C_ is the multimodal conditioning sequence, and _z ∈_ R<sup>16</sup><sup>_×_7</sup> corresponds to the current raw action trajectory latent. 

The AttnRes backbone utilizes a hidden size of 768 with 8 query heads and 8 key-value heads, executing standard multi-head attention (MHA). Positional formatting relies on Rotary Position Embeddings (RoPE) with a base frequency of 10 _,_ 000, supplemented by Root Mean Square Normalization (RMSNorm, _ϵ_ = 10<sup>_−_6</sup> ) and a dropout rate of 0.05 across both the embedding and attention layers. Each AttnRes block is composed of a RoPE-augmented self-attention sublayer and a SwiGLU feed-forward network (FFN) sublayer with an intermediate hidden dimension of 2048. 

In contrast to standard residual architectures that sequentially accumulate hidden states uniformly across layers, the AttnRes mechanism maintains an indexed cache of all preceding layer representations. Prior to entering the _m_ -th 

attention or feed-forward sublayer, a token-wise depth attention operation routes information across historical branches: 


where _qm_ represents a learned structural pseudo-query specific to the _m_ -th sublayer, and _τ_ denotes the token index. The sublayer output is subsequently appended as a newly indexed hidden branch, and the final representation exiting the backbone is obtained via a summation of all accumulated branches. Following the transformer blocks, the last 16 action tokens are isolated, passed through an RMSNorm layer, and projected back into the 7-dimensional relative control space. 

## _D. Implementation Details of Action Generation_ 

Action generation operates entirely within the native, normalized trajectory space. Given a normalized raw action trajectory _x ∈_ R<sup>_H×da_</sup> with _H_ = 16 and _da_ = 7, the network directly learns and samples continuous action trajectories without domain transformations. 

During the training phase, we sample Gaussian noise _e ∼ N_ (0 _, I_ ) alongside two distinct flow time steps _r, t ∈_ [0 _,_ 1] drawn from a logit-normal distribution ( _µ_ = _−_ 0 _._ 4 _, σ_ = 1 _._ 0). The sampled intervals are sorted such that 0 _≤ r ≤ t ≤_ 1, with a 0.5 probability of setting _r_ = _t_ to incorporate standard flow-matching targets. The interpolated noisy trajectory latent _zt_ is formulated via linear interpolation: 


The network _fθ_ ( _zt, r, t, C_ ) parameterizes the velocity field conditioned on the multimodal context prefix _C_ . To stabilize backpropagation through complex flow paths, ReactVLA implements an improved Mean Flow (iMF) objective augmented with a Jacobian-Vector Product (JVP) correction term: 


where _uθ_ = _fθ_ ( _zt, r, t, C_ ) represents the base predicted velocity, and _Dz_ denotes the Jacobian operator with respect to the latent trajectory state. The fundamental optimization target is defined as _e − x_ . To mitigate gradient spikes caused by demonstration noise, training relies directly on the Pseudo-Huber loss formulation applied to the raw trajectory dimensions with a threshold parameter _δ_ = 1: 


Auxiliary regularizations, such as padding masks, frequency reweighting, and semigroup consistency constraints, are omitted in our configuration. 

At inference time, action generation initiates from random Gaussian noise _z_ 1 _∼N_ (0 _, I_ ) sampled within the normalized action domain. We deploy a highly efficient two-step inference regime over the discrete time grid 1 _._ 0 _→_ 0 _._ 5 _→_ 

0 _._ 0. For each integration interval ( _ti, ri_ ), the latent state is sequentially updated via an Euler-style flow integration step: 


Upon reaching the final time boundary, the optimized latent vector _z_ 0 directly represents the predicted action trajectory in the normalized action space. Given an observation horizon of _n_ obs = 1 and a targeted execution chunk of _K_ = 8, the policy slices and emits the first eight actions from the decoded 16-step trajectory ( _z_ 0 _,_ 0:7). In a closedloop deployment cycle, these actions are queued and executed sequentially at the environment’s control rate; a fresh multimodal action chunk is generated immediately upon queue depletion. Lastly, an unnormalization post-processor scales the generated relative commands back to the native operational boundaries of the robotic environment. 

## _E. Evaluation of Simulation Experiments_ 

_1) Implementation details of Simulation tasks:_ **LIBERO multi-task setup.** We evaluate our method on the standard LIBERO benchmark, specifically utilizing four multi-task suites: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long, each containing 10 distinct manipulation tasks. To thoroughly evaluate the multi-task scaling capability of our model, we aggregate the demonstrations from all four suites into a single large-scale unified dataset comprising 40 distinct manipulation tasks, upon which the policy is trained jointly. The policies utilize dual-view RGB observations from the agent-view camera and the eye-inhand camera, together with the robot’s proprioceptive joint state and the task language embedding. For our proposed ReactVLA, we train entirely on this official aggregated multi-task demonstration set. Unlike standard diffusion- or flow-based VLA models that require multiple expensive denoising or sampling steps, our framework predicts actions using only 2 inference steps, significantly accelerating simulation rollouts while maintaining a strong average success rate. 

**RoboIMI setup and tasks.** We evaluate our framework on the custom-built RoboIMI simulation platform, which serves as a dual-arm robotic environment specifically designed for coordinated, tight-tolerance manipulation. We conduct evaluations across two challenging tasks: (1) _Peg-inSocket_ , where one robotic arm picks up a wooden peg from a randomized position on the tabletop and precisely inserts it into a rectangular socket held dynamically by the opposing arm; (2) _Object Transfer_ , where one arm picks up a wooden block from a randomized position on the table and executes a coordinated handover to the gripper of the other arm. The policies take multimodal inputs, including RGB observations from three cameras, a third-person global camera and two wrist-mounted cameras (one on each arm), along with the complete dual-arm proprioceptive joint states and gripper execution states. All comparative models, including ACT, Diffusion Policy, and ReactVLA, are trained on the demonstrations generated by an automated script policy for each task. To thoroughly verify the real-time coordination 

and precision under tight tolerances, we evaluate each policy across 100 randomized simulation trials per task, reporting the average cumulative reward and inference latency directly from the log files. 

**Reward Mechanism and Formulations.** The reward computation for both tasks is grounded in the physics engine’s contact dynamics, implemented by querying the MuJoCo contact array mj ~~d~~ ata.contact at each simulation timestep _t_ . Interacting geometric shapes ( _geoms_ ) are extracted to construct contact pairs, which are then evaluated against task-specific rules to determine the per-step reward _rt_ . Crucially, the final performance metric reported in our evaluation is the episodic cumulative reward, defined as the time-aggregated sum over the entire rollout horizon _T_ : 


Under this temporal accumulation formulation, once the robot successfully achieves and sustains a specific subgoal or milestone state, the corresponding step reward _rt_ is persistently added to the cumulative total _R_ at every subsequent timestep until the episode terminates. Consequently, early task completion coupled with stable state maintenance results in a continuous accumulation of the high-tier step rewards, allowing the cumulative metric _R_ to effectively encapsulate both the temporal efficiency and operational stability of different policies. The two environments adopt fundamentally distinct scoring philosophies and underlying pair-matching implementations to compute the step reward _rt_ : 

_a) Staged reward in Object Transfer:_ This task simulates a sequential, single-object state machine that tracks the transfer of a red ~~b~~ ox from the right arm to the left arm. It uses a stepwise overwriting reward with a maximum per-step score of _rt_ = 4: 


Technically, contact pairs are represented as ordered tuples, making the evaluation sensitive to the MuJoCo geometric ID ordering, e.g., (geomA, geomB) versus (geomB, geomA). 

_b) Additive reward in Peg-in-Socket:_ This task requires asynchronous dual-arm coordination to manipulate two separate objects, a red ~~p~~ eg and a blue ~~s~~ ocket, for mid-air assembly. It uses a multi-objective additive reward with a maximum per-step score of _rt_ = 5: 


where I( _·_ ) denotes the indicator function. 

This design dichotomy reflects the underlying task structures: _Object Transfer_ uses a strict staged progression to 

guide a linear object hand-off pipeline, whereas _Peg-inSocket_ leverages an additive structure to independently incentivize decoupled sub-goals before enforcing the final tight-tolerance alignment. 

_F. Evaluation of Real-world Experiments_ 

_1) Implementation details of Real-world tasks:_ **Robot platform.** We conduct all real-world experiments on a Diana 7 single-arm robotic arm from Agile Robots. The policy outputs joint position commands and a gripper command at each control step. The proprioceptive input contains the robot’s joint states and the gripper execution state. To evaluate the robustness and spatial generalization of the policies, we introduce small perturbations to the robotic arm’s initial poses within a localized range before commencing each trial, and vary the target orange positions across different runs, while keeping the remaining workspace layout constant. 

**Orange P&P.** Orange Pick-and-Place (Orange P&P) is a representative tabletop manipulation task in which the robot must grasp an orange from the tabletop and place it stably onto a target plate. We collect 50 teleoperated demonstrations on the Diana 7 platform for model training. The final deployed policies utilize two camera views: an agent-view RGB camera and a wrist-mounted RGB camera. The agent view provides global semantic context of the tabletop scene and the target plate, while the wrist camera provides close-range visual feedback to facilitate reliable gripper alignment during grasping. The visual inputs are resized and processed before being passed to the visual encoder. The models are trained entirely on the 50 expert demonstrations without any additional real-world rollout data. 

**Block Stack.** Block Stack is a high-precision tabletop stacking task where a small stack of wooden blocks is already present on the tabletop. The robotic arm must grasp another block from the tabletop and place it stably on top of the pre-existing stack without causing the stack to collapse. We collect 50 teleoperated demonstrations on the Diana 7 platform for model training. The policy utilizes the same dual-camera setup (agent-view and wrist camera) and observations as the Orange P&P task. The model is also trained entirely on these 50 demonstrations, requiring high spatial accuracy and closed-loop responsiveness to achieve stable stacking. 

**Real-world deployment protocol.** During real-world deployment, both ReactVLA and the SmolVLA baseline process the multimodal observation streams online and generate target joint commands executed at a high control frequency of 60 Hz. Specifically, the number of inference steps for ReactVLA is set to 5 during physical testing to guarantee a sufficiently smooth and stable action trajectory. All evaluated methods follow the identical initial reset protocol and strict task success criteria. A trial of the Orange P&P task is quantified as successful if and only if the orange is securely grasped, transferred, and placed stably on the target plate without any object drops or unintended collisions. 

