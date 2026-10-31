---
title: "Coupled Local and Global World Models for Efficient First Order RL"
date: "2026-02-05"
authors: "Joseph Amigo; Rooholla Khorrambakht; Nicolas Mansard; Ludovic Righetti"
url: https://arxiv.org/abs/2602.06219
pdf: https://arxiv.org/pdf/2602.06219
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06219)** / [論文ページ](https://arxiv.org/abs/2602.06219)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Coupled Local and Global World Models for Efficient First Order RL** 

**Joseph Amigo**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **, Rooholla Khorrambakht**<sup>1</sup><sup>_∗_</sup> **, Nicolas Mansard**<sup>2</sup><sup>_,_3</sup> **, Ludovic Righetti**<sup>1</sup><sup>_,_3</sup> 1Machines in Motion Laboratory, New York University, USA 

2LAAS-CNRS, Universit´e de Toulouse, CNRS, Toulouse, France 3Artificial and Natural Intelligence Toulouse Institute, Toulouse, France https://coupled-global-local-wm-rl.pages.dev/ 


Figure 1: Real-world robotic tasks solved zero-shot by policies trained entirely from scratch within our learned world models: Push-T with a tabletop manipulator (left), Ego-Centric Grasp and Lift with a G1 humanoid (center), and Ego-Centric Push Cube with a Go2 quadruped (right). 

### **Abstract:** 

World models offer a promising avenue for capturing complex environment dynamics where simulators face challenges. However, large-scale world models required for complex real-world settings are computationally expensive to adopt in popular RL approaches. In this paper, we introduce a novel first-order RL method that enables policy training via a novel decoupled first-order gradient (FoG) method: a large-scale world model generates accurate forward trajectories, while a lightweight latent-space surrogate approximates its local dynamics for efficient gradient computation. Our coupled local and global world model formulation allows high-fidelity forward dynamics alongside computationally efficient differentiation needed for model-based RL. Through real-world experiments across a range of robotic tasks with increasing complexity, we demonstrate tractable RL and zero-shot deployment thanks to our world-model-based formulation. We show significantly better sample efficiency compared to PPO in a canonical real-world Push-T benchmark and observe similar patterns in more complicated ego-centric object manipulation and grasping tasks. Together, these results demonstrate that learning agents entirely inside data-driven world models is a feasible and promising pathway for solving hard-to-model tasks in image space without reliance on hand-crafted physics simulators. 

**Keywords:** World Models, Reinforcement Learning, Robot Manipulation 

## **1 Introduction** 

Recent breakthroughs in reinforcement learning (RL) for locomotion [1, 2, 3, 4, 5] have yielded highly agile policies, trained in parallelized GPU simulators and seamlessly deployed on real robots 

*Equal contribution. 

10th Conference on Robot Learning (CoRL 2026), Austin, Texas, USA. 

for acrobatic tasks. Despite these gains, RL confronts substantial barriers in perceptual control and manipulation tasks. On the one hand, RL’s sample inefficiency prevents practical online learning directly from real-robot interactions. On the other hand, simulating manipulation tasks is inherently more difficult than locomotion, as the environment state changes with the agent’s action, adding an infinite degree of variability to the simulation problem, far beyond the ego-body dynamics and actuation modeling needed in locomotion. For instance, simulating the granular dynamics of gravel bags, pressurized deformations of an aluminum can while pulling its pull-tab, or the intricacies of folding a T-shirt, all projected onto the robot’s raw sensory space, even if computationally feasible in some cases, fall short in terms of alignment with reality and sim2real transferability. 

Instead, training agents inside learned differentiable world models using first-order gradient (FoG) methods [6, 7, 8] offers a promising pathway to resolve these issues. While previous FoG methods have predominantly relied on continuous online interaction within a physics simulator, applying this paradigm to learn dynamics directly from offline real-world data has the potential to effectively bridge the sim-to-real gap. Such a shift also simplifies modeling across varied environments through data acquisition rather than physics-based simulation. Furthermore, FoG methods inherently address RL sample inefficiency via gradient signals with reduced variance [8] relative to score-function based algorithms such as PPO [9] or SAC [10, 11]. 

However, the application of such methods in real-world robotics is severely constrained by forward simulation drifts [12, 13], which limit scalability to highly complex dynamical and visual effects common in real-world robotic settings. On the other hand, while recent diffusion world models have shown promising modeling capabilities [14], computing gradients through them at the scales required for training FoG RL policies is computationally expensive and often intractable. 

To address this challenge, this paper builds on Decoupled forward-backward Model-based policy Optimization (DMO) [15], which separates forward simulation from backward differentiation, to make large-scale world models usable in FoG model-based RL (FoG-MBRL). Concretely, we propose a framework that maintains an offline trained large diffusion/flow-based model as a “global” simulator surrogate, alongside a secondary light-weight Recurrent State Space Model (RSSM)—acting as a “local” low-dimensional latent space world model that supplies stable, lowvariance gradients without the need to backpropagate through the large global model. This decoupling resolves key obstacles to adopting FoG-MBRL alongside large-scale pixel-space world models, thereby opening the door to practical, efficient FoG-MBRL for real-world robotic problems. Through real-world experiments across a range of robotic tasks with increasing complexity, we empirically evaluate the capabilities of our approach in solving perceptual loco-manipulation tasks directly from real robot data. 

## **2 Related Work** 

### **2.1 World Models and Policy Learning.** 

Model-Based Reinforcement Learning (MBRL) approaches are generally distinguished by their control strategy. A prevalent line of work employs the learned model for online planning via Model Predictive Control (MPC) [16, 17, 18] or Monte-Carlo Tree Search [19, 20, 21, 22]. While effective, these methods incur high computational costs at inference time. Conversely, policy optimization methods encode control into a neural network learned inside the world model. However, seminal works in this category, like DreamerV3 [7], typically rely on online interaction with a simulator. Simulator-free approaches like DayDreamer [23] learn directly from real-world interaction, but rely on Variational Auto-Encoders (VAEs) [24], which often exhibit limited expressivity and struggle to model complex distributions with high fidelity. In contrast, we target simulator-free learning using Diffusion Models, which offer superior modeling power but present unique policy optimization challenges. 

2 

### **2.2 Gradient Estimation for Policy Learning.** 

Optimization in MBRL generally falls into zeroth-order or first-order methods. Zeroth-order algorithms [14, 25, 26, 27, 28, 29] treat the dynamics as a black box. While robust to model inaccuracies, these methods are notably sample-inefficient. First-order Gradient (FoG) methods [8, 30] calculate analytic gradients via backpropagation, offering high data efficiency. However, standard FoG requires the dynamics derivatives to be computationally tractable, which excludes heavy-weight models. A promising solution is Decoupled forward-backward Model-based policy Optimization (DMO) [15], which utilizes a high-fidelity model for trajectory generation (forward) and a lightweight proxy model for gradient estimation (backward). While prior DMO works relied on the simulator for the forward pass, we extend this paradigm to the simulator-free setting in image space by using a “global” offline trained diffusion model. This allows us to leverage high-fidelity generation without incurring the prohibitive cost of backpropagating through the heavy diffusion network. 

### **2.3 Diffusion for Efficient Control.** 

Recent works have successfully scaled World Models using diffusion parameterizations, such as DreamerV4 [14] and DIAMOND [31]. However, these methods typically rely on zeroth-order optimization, which requires a large number of samples. We argue that the combination of heavy-weight diffusion models and sample-inefficient zeroth-order optimization is computationally expensive, as it requires generating a vast number of diffusion samples. Our method addresses this by employing sample-efficient FoG. By leveraging the decoupled architecture described above, we effectively distill the global diffusion priors into a local latent model, enabling fast analytic gradient updates and preventing the sampling bottleneck of diffusion-based zeroth-order RL methods. 

## **3 Method** 

### **3.1 Problem Setting and Decoupling Framework** 

We consider an infinite-horizon discounted Markov Decision Process (MDP) ( _S, A, r, γ, f_ ), where _S_ and _A_ denote the state and action spaces, _r_ : _S × A →_ R is the reward function, _γ ∈_ (0 _,_ 1) is the discount factor, and _f_ : _S × A →P_ ( _S_ ) is the dynamics. A policy _πθ_ : _S →A_ induces trajectories via _at_ = _πθ_ ( _st_ ), _st_ +1 _∼ f_ ( _st, at_ ), and defines the objective _G_ ( _θ_ ) =<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtr_(</sup><sup>_st, at_)</sup><sup>_._</sup> 

First-order model-based RL (FoG-MBRL) computes policy gradients by differentiating through trajectories: _∇θG_ ( _θ_ ) =<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γt_</sup><sup><u>�</u></sup> _∂r_ <u>(</u> _∂sstt,at_ <u>)</u> _<u>dsdθt</u>_<sup>+</sup><sup>_∂r_</sup><sup><u>(</u></sup> _∂a_<sup>_st,_</sup> _t_<sup>_at_</sup><sup><u>)</u></sup> _<u>dadθt</u>_ � _,_ where the state and action sensitivities evolve as<sup>_ds_</sup> _dθ_<sup>_t_</sup><sup><u>+1</u></sup> =<sup>_∂f_</sup><sup><u>(</u></sup> _∂s_<sup>_st_</sup> _t_<sup>_<u>,at</u>_</sup><sup><u>)</u></sup> _<u>dsdθt</u>_<sup>+</sup><sup>_∂f_</sup><sup><u>(</u></sup> _∂a_<sup>_st_</sup> _t_<sup>_<u>,at</u>_</sup><sup><u>)</u></sup> _<u>dadθt</u>_<sup>_,_</sup> _<u>dadθt</u>_<sup>=</sup><sup>_∂π_</sup> _∂θ_<sup>_<u>θ</u>_</sup><sup><u>(</u></sup><sup>_st_</sup><sup><u>)</u></sup> +<sup>_∂π_</sup> _∂s_<sup>_<u>θ</u>_</sup><sup><u>(</u></sup> _t_<sup>_st_</sup><sup><u>)</u></sup> _<u>dsdθt</u>_<sup>_._In practice, the</sup> dynamics _f_ is often approximated by a learned model _f_<sup>ˆ</sup> _ϕ_ , used both for rollouts _s_ ˆ _t_ +1 = _f_<sup>ˆ</sup> _ϕ_ (ˆ _st, at_ ) and for Jacobians _∂f_<sup>ˆ</sup> _ϕ/∂_ ( _s, a_ ), so gradients are evaluated along model-generated trajectories (ˆ _st_ ) and are sensitive to compounding model error. To address this, we adopt DMO [15], which decouples forward rollouts from backward gradient computation by using distinct models: a forward model _f_<sup>_→_</sup> to generate high-fidelity trajectories and a backward model _fϕ_<sup>_←_</sup> _≡ f_<sup>ˆ</sup> _ϕ_ for gradient evaluation. Concretely, rather than evaluating the Jacobians of _fϕ_<sup>_←_</sup> at its own next state _s_<sup>_←_</sup> _t_ +1<sup>=</sup><sup>_f_</sup> _ϕ_<sup>_←_(</sup><sup>_s_</sup> _t_<sup>_←, at_),weevaluatethematthenextstate</sup> _∂fϕ_<sup>_←_(</sup><sup>_s,a_)</sup> generated by the high-fidelity forward model _s_<sup>_→_</sup> _t_ +1<sup>=</sup><sup>_f →_(</sup><sup>_s_</sup> _t_<sup>_→, at_),i.e.,</sup> _∂s_ ���( _s_<sup>_→_</sup> _t_ +1<sup>_,at_+1)</sup><sup>_,_and</sup> 

analogously for _∂/∂a_ , to approximate the true dynamics derivatives in the policy gradient. This decoupling enables forward accuracy and backward tractability to be optimized independently. 

### **3.2 Global World Model** 

Based on the complexity of each task and the available computational budget during each phase of our experiments, we adopt two different architectures for our global world model. For preliminary experiments on a canonical Push-T setup, we use a small-scale (4M parameters) diffusion-based 

3 


Figure 2: Overview of the proposed approach. Global world/reward models are learned from play/demonstration data (Steps 1 and 2). Then, local world/reward models are pre-trained (Step 3). Policy is optimized with the DMO algorithm (Step 4): forward simulation uses the diffusion-based global world model in pixel space, trained on real robot data, to produce high-fidelity rollouts. The backward pass uses gradients computed from a local world model operating in a low-dimensional latent space. The local world/reward model is further fine-tuned during policy optimization. 

world model based on the DIAMOND [31] architecture due to long horizon prediction accuracy and efficient inference speeds. For all other tasks, we implemented a transformer-based latent diffusion world model, based on the recent DreamerV4 [14] architecture. We ensure efficient inference by adopting shortcut learning [32] (few diffusion steps) and causal diffusion forcing [33] (KVcache-friendly real-time recurrent generation). We also integrate proprioceptive data as an additional modality to the tokenizer for our Humanoid G1 task. 

### **3.3 Global Reward Model** 

Learning in pixel space requires image-based reward functions. We adopt two reward modeling strategies depending on the underlying global world model. For the Push-T experiments with the DIAMOND world model, we train a contrastive reward model on random play and, optionally, demonstration videos, following [34]. Specifically, we learn a goal-conditioned energy function _fψ_ ( _st | s_ start _, s_ goal) that assigns higher scores to states temporally closer to the goal. 

For experiments using our transformer-based world model, we instead train a lightweight reward head that classifies whether a frame belongs to the task demonstration distribution; on Push Cube, frames where the cube reaches the goal carry a higher label (10). Labels are provided by a human to indicate task-relevant behavior, either during data collection (e.g., button presses during play) or in a post-processing pass. 

4 

### **3.4 Local Reward and World Models** 

For the backward model _fϕ_<sup>_←_, we adopt the recurrent state-space model (RSSM) architecture used in</sup> DreamerV3 [7], which acts as a joint local latent dynamics and reward model. The model is first pretrained offline on the play dataset. Its reward targets are the predictions of the global reward model on Push-T and, on Push Cube and G1, the dataset’s per-frame reward labels, which also supervise the global reward head. During online RL training, we continue fine-tuning _fϕ_<sup>_←_</sup> and its reward head using trajectories generated by the forward global model _f_<sup>_→_</sup> , with the global reward model’s predictions as reward targets, ensuring that the RSSM maintains high local accuracy with respect to the current policy’s conditional action distribution. To avoid differentiating through pixels (for memory efficiency), an image encoder projects observations into a compact latent space, where _fϕ_<sup>_←_</sup> operates exclusively (the policy gradients do not flow through the encoder). In the DMO framework, unlike DreamerV3 or other MBRL frameworks, the transition model _fϕ_<sup>_←_needs to be accurate only</sup> over single forward steps, as Jacobians are evaluated at the encodings of precise forward-simulated images from the global model _f_<sup>_→_</sup> . 

**Relation to DMO.** DMO cannot be applied as is in our setting. It evaluates the backward model at the states produced by the forward model, so both must share one state space. In image-space problems, a high-fidelity forward model has to operate on high-dimensional states: on Push Cube, our global model conditions on up to 96 frames of 256 latent tokens of width 16, against the 68dimensional state of DMO’s quadruped task, an increase of more than 5 _,_ 700 _×_ . Giving the local model this dimensionality would make the backward pass prohibitively expensive. We therefore couple the two models through image space: each frame generated by _f_<sup>_→_</sup> (decoded from its latent by the tokenizer decoder for the transformer-based model) is re-encoded into the local latent by the RSSM’s image encoder, both without gradient. The Jacobians of the global model, taken in its own latent space, are then approximated by those of the local model, taken in its own, so the two latent spaces need not have the same dimension. Two further components that DMO obtained from its simulator must be learned here. First, DMO’s backward model operated on the simulator’s ego-body state, for which rewards can be written by hand, whereas we must learn the reward from images (Sec. 3.3). Second, a simulator is exact by construction, whereas our world model, learned from offline data, is never re-grounded on real observations during episode-long rollouts and may hallucinate; we address this with the patching procedure of Sec. 3.5. 

### **3.5 Data Collection and Training Protocol** 

We collect an unstructured high-entropy action-image pair _play dataset_ on the real robot to train our global world model from scratch, except for the Push Cube and G1 tokenizers, which are initialized from tokenizers pretrained on the SOAR robot dataset [35] (reducing data needs through foundationpretrained world models is the topic of future research). Such data does not require clean temporal segmentation of the sequence into clearly defined tasks and does not mandate frequent environment resets during data collection, making it less expensive and easier to collect and reuse from other tasks. 

To ensure that the global world model accurately captures both the large workspace of the Go2 Push Cube task and the fine-grained contact dynamics between the robot head and the cube, as well as the complex multi-contact interactions involved in the high-DoF Humanoid G1 Grab Box task, we use two complementary refinement procedures. First, we qualitatively probe the world model through immersive exploration, using a Meta Quest 3 headset for Go2 Push Cube and a Pico headset with IMUs for Humanoid G1, to identify poorly modeled regions of the state space; we then collect additional data in those regions and fine-tune the model accordingly. This process is feasible because the world-model action space is expressed in terms of high-level actions that a human operator can reproduce. Second, we use RL to discover policies that exploit inaccuracies in either the world model or the reward model to obtain artificially high returns. We then deploy these exploiting policies on the real robot to gather targeted data and fine-tune the model, thereby patching the weak regions that enabled the exploit. On G1, we ran seven rounds of such targeted data collection and fine-tuning. 

5 


Figure 3: Real-world zero-shot deployment of our DMO policies trained in the world model. 

## **4 Experiments** 

### **4.1 Tasks and Setups** 

To truly evaluate the potential of our approach to address the unmodeled complexities of real-world settings and its zero-shot sim2real transferability, we favor fewer, more representative real-world deployments over a large number of simulated tests that fall short of capturing the modeling complexities of real robotics tasks. Specifically, we consider three carefully chosen tasks and robot embodiments as introduced in the next subsections. It is important to note that, unlike other RL finetuning approaches that use world models [36, 37], we train our policies entirely within the world model from scratch, without any behavior-cloning guidance or regularization. 

### **4.1.1 Push-T** 

We adopt the Push-T canonical task as an easier-to-model but non-trivial motion planning problem. Specifically, this task requires pushing a T-shaped object from a random pose on a flat 2D surface to the center of the board in a predefined orientation. The action is the tool’s vertical and horizontal velocity, and stacks of 4 consecutive frames are used as states, both provided at 5 Hz. We use a 7-DoF Flexiv Rizon-10S robot with an onboard task-space velocity controller to build our environment. We adopt a small 4M-parameter DIAMOND world model as the global forward model _f_<sup>_→_</sup> and train it on 4 hours of play data. 

### **4.1.2 Ego-Centric Push Cube** 

In this task, we increase the difficulty by introducing partial observability, walking dynamics, and higher visual complexity. Specifically, a Unitree Go2 robot with ego-centric vision is tasked with pushing a cubical object into a soccer goal using its body. Body velocity commands to a low-level RL locomotion policy are taken as action and provided at 5 Hz. This task requires the policy and the world model to be robust to partial occlusions of the view by the object, maintain a short-term memory of where it was when it falls out of view, and handle the geometric complexity of a large room in image space. Thus, we train a 1.0B-parameter implementation of our transformer-based latent diffusion world model on 12 hours of data to serve as the forward model _f_<sup>_→_</sup> with a reward head. 

### **4.1.3 Humanoid Grasp and Lift** 

Finally, we extend the previous experiments by considering grasping skill and a high-DoF Unitree G1 humanoid robot equipped with a BrainCo dexterous hand. The task is to grasp a box through its flexible handle and lift it above the table. The world model is conditioned on 22-dimensional commands: 17 upper-body joint-position targets (3 waist and 14 arm joints), 2 hand-grip commands, and 3 lower-body locomotion commands (base velocities and yaw rate). The policy outputs the 19 upper-body commands through bounded per-step increments (at most 0 _._ 02 rad per step for the joints); on the real robot, the left arm is kept fixed and its commands are ignored, so the deployed policy controls 11 DoF: the waist, the right arm and the right hand. The humanoid is controlled 

6 


Figure 4: Unrolling of real and model-predicted trajectories on the G1 humanoid manipulation task. We compare the real camera observation ( **top** ), the local DreamerV3 RSSM trajectory ( **middle** ), and the global DreamerV4 diffusion trajectory ( **bottom** ) at time steps 0 _,_ 5 _,_ 10 _, . . . ,_ 55 (5 _._ 5 s at 10 Hz), with both models initialized from the first real frame. The global diffusion model maintains high visual fidelity and accurate contact dynamics over the long horizon. 

by the NVIDIA SONIC [38] full-body tracking RL policy at 50 Hz, and receives body-tracking commands from our policy at 10 Hz. We use the same type of global forward and reward model as for Push Cube, at a larger scale (1.4B parameters, 256 _×_ 256 images; Table 4), trained on 20.9 hours of data: 16.5 hours of play data and 4.4 hours collected during the seven rounds of targeted data collection (Sec. 3.5). The dynamics model is trained from scratch, and the tokenizer is initialized from a tokenizer pretrained on the SOAR robot dataset [35]. 

### **4.2 Baselines and Ablations** 

We compare our method against the following baselines. (1) Model-free RL trained inside the same global world model, with the same reward model and the same initial-state distribution as our method: PPO [9] and SAC [10], both trained directly on image observations. (2) Offline RL: IQL [39], trained on the recorded data of each task without any interaction, and shown at its best evaluation in the global world model. (3) Behavior Cloning (BC): the Action Chunking Transformer (ACT) [40], a well-known representative of BC policies, on Push Cube and G1 Grab Box.<sup>1</sup> SAC and IQL are evaluated in the global world model only (Fig. 5), while PPO, ACT and our method are deployed on the real robots (Tables 1–3). 

We also include two ablations: the first, “No Diffusion”, replaces the global diffusion world model (DIAMOND or DreamerV4) for the forward pass with the DreamerV3 RSSM model and thus uses the same RSSM model for the forward and backward passes. The aim is to demonstrate that powerful models are indeed needed for the forward pass to accurately capture the complexity of real-world robotics scenarios. The second ablation, “No RSSM Finetuning”, evaluates the need to finetune the RSSM during RL training, providing the practitioner with additional insights into our design decisions. 

### **4.3 Results** 

The results in Fig. 5 demonstrate that DMO achieves superior sample and time efficiency compared to PPO and SAC across all tasks, and reaches a higher reward than the best evaluation of offline RL (IQL). Notably, the time efficiency gains shown in Fig. 5 validate our hypothesis that firstorder policy gradients are more suitable than zeroth-order variants for computationally heavy world models (DMO vs PPO and SAC). Refer to Appendix A.4 for per-task efficiency results. 

Furthermore, the poor performance of the “No Diffusion” ablation in Fig. 5 further underscores the necessity of a high-fidelity global world model for forward simulation of more complex tasks. As shown in Fig. 4, and in Appendix A.1, DreamerV3 generalizes less effectively than the diffusion world model. Nevertheless, using the local model for tractable gradient computation and, by decou- 

> 1We decided to include a BC baseline after the Push-T setup had been dismantled, so Push-T has no BC result. 

7 


Figure 5: Aggregated performance metrics across all evaluation tasks. **Left:** Normalized reward relative to normalized sample number; offline RL (IQL) uses no environment samples and is shown as a horizontal line at its best evaluation. **Right:** Normalized reward relative to normalized wallclock time. Every online experiment was run with 4 seeds. 

pling, leveraging the diffusion model’s broad generalization, delivers significant improvements in both sample and time efficiency. 

Table 1: Trajectory Quality Analysis. We report the mean _±_ std over _N_ = 10 randomly sampled evaluation episodes on the real robot for the Push Cube task. _Success Rate_ : fraction of episodes reaching the goal; _Steps_ : lower is better; _Straightness_ : displacement/path length, _↑_ is straighter; _Curvature_ : yaw change per meter, _↓_ is smoother. Metrics computed over successful episodes only. _†_ For the BC baseline, success is defined as guiding the cube to the immediate pre-goal vicinity, as the cube never fully enters the goal. 

|Method|Success Rate (_↑_)|Steps to Success (_↓_)|Straightness Index (_↑_)|Curvature (rad/m) (_↓_)|
|---|---|---|---|---|
|DMO (Ours)|**90%**|177.2_±_52.2|**0.520**_±_**0.266**|**0.692**_±_**0.206**|
|BC (ACT)<sup>_†_</sup>|60%|371.0_±_94.0|0.330_±_0.147|0.761_±_0.151|
|PPO|40%|173.5_±_20.3|0.233_±_0.182|1.222_±_0.306|
|No Diffusion|0%|–|–|–|


Table 2: Success Rates Across Algorithms for Push-T (on the real robot, out of 10 Tries). _†_ Under a relaxed success criterion (counting runs where the T briefly passes through the correct pose and position without stopping), PPO achieves 4/10 successes. 

Table 3: Success Rates Across Algorithms for G1 Grab Box (on the real robot, out of 10 Tries). 

|ere the T briefly passes through the cor-|Algorithm|Successes / 10|
|---|---|---|
|e and position without stopping), PPO<br>|DMO (Ours)|8/10|
|4/10 successes.|BC (ACT)|7/10|
|Algorithm<br>Successes / 10|PPO<br>No Diffusion|1/10<br>0/10|
|DMO (Ours)<br>9/10|||
|PPO<br>1/10<sup>_†_</sup>|||
|No Diffusion<br>0/10|||


Table 2 reports the success rates for the Push-T real-robot experiment (Fig. 9) and confirms the advantage of our approach compared to the baselines. The “No Diffusion” ablation did not lead to the successful achievement of the task, and PPO only managed to solve the task once. We observe similar patterns in all other tasks, as shown in Tables 1 and 3. 

It is worth noting that for the Push Cube task, the episode length had to be increased to 128 steps to train the PPO policy deployed on the robot (as opposed to 64 for DMO and for the learning curves of Fig. 5); with 64-step episodes, PPO fell into a suboptimal local solution where it repeatedly 

8 

approaches and avoids the cube to collect rewards of 1. In the meantime, DMO succeeded in both settings and demonstrates robustness to hyperparameter choices. 

Regarding the ACT baselines, we observed common BC problems such as not seeking long-term rewards (e.g., stopping in front of the goal in the Push Cube task), not discovering solutions or failing at poorly covered regions, and being sensitive to the consistency of the demonstrations (demonstrator’s task-solving strategy). 

Furthermore, the Push Cube experiment revealed distinct behavioral differences across methods, particularly in object localization, task completion, and control smoothness. In Table 1 we report _Straightness Index_ (the ratio of Euclidean displacement to total path length, where 1 _._ 0 is optimal) and _Curvature_ (average yaw change per meter) that verify this observation. 

Finally, Fig. 3 shows snapshots of the deployed DMO policy across tasks. For more qualitative demonstrations, refer to the appendix. 

## **5 Limitations** 

In this paper, we train our global world models from scratch (except for the Push Cube and G1 tokenizers, initialized from tokenizers pretrained on SOAR robot data) and assume hand-labeled rewards for the reward head (Go2 Push Cube and G1 Grab Box tasks). Consequently, our play data must cover a wide range of physical interactions in image space, which challenges its adoption for more complex and long-horizon tasks. Our future work will focus on leveraging prior knowledge from internet-scale pre-trained video models to alleviate this limitation. Furthermore, the automated exploration and data collection scheme briefly explored under this project introduces a promising orthogonal solution worth further future investigation. This argument also applies to reward modeling, where leveraging VLM-based prior knowledge for reward labeling offers a promising solution for automating additional components within our system. 

## **6 Conclusion** 

In summary, our framework bridges the limitations of simulator-centric RL by learning diffusion world models from real data, yielding visually realistic simulations that substantially reduce simto-real discrepancies in manipulation tasks. The decoupling mechanism leverages the comparative strengths of models—global diffusion for accurate, generalizable forward predictions and local latent models for tractable backward gradients—maintaining efficiency despite the high dimensionality of pixel inputs. Notably, our method enables learning policies directly from real robot data, using images as input, and transfers zero-shot with a high success rate on the real robot. Importantly, our experiments demonstrated practical improvements in task performance over pure behavior cloning. Our method provides a safe proxy for real-robot training, allowing scalable policy optimization without risking hardware damage or unsafe behaviors, paving the way for robust vision-based robotics in unstructured environments. 

9 

### **Acknowledgments** 

This work was granted access to the HPC resources of IDRIS under the allocations AD011015316R1, A0201017555 and A0191016928 made by GENCI. This work was in part supported by the US National Science Foundation grants 2026479, 2222815, and 2315396, and the French AI Interdisciplinary Institute ANITI. ANITI is funded by the France 2030 program (grant agreement ANR-23-IACL-0002). It was also supported in part by the AGIMUS project, funded by the European Union under GA no. 101070165, and the ANR NERL project (grant ANR-23-CE940004). 

## **References** 

- [1] X. Cheng, K. Shi, A. Agarwal, and D. Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450, 2024. 

- [2] D. Hoeller, N. Rudin, D. Sako, and M. Hutter. ANYmal parkour: Learning agile navigation for quadrupedal robots. _Science Robotics_ , 9(88):eadi7566, 2024. 

- [3] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao. Robot parkour learning. In _Conference on Robot Learning (CoRL)_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 73–92, 2023. 

- [4] E. Chane-Sane, P.-A. Leziart, T. Flayols, O. Stasse, P. Sou`eres, and N. Mansard. CaT: Constraints as terminations for legged locomotion reinforcement learning. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 13303–13310, 2024. 

- [5] E. Chane-Sane, J. Amigo, T. Flayols, L. Righetti, and N. Mansard. SoloParkour: Constrained reinforcement learning for visual locomotion from privileged experience. In _Conference on Robot Learning (CoRL)_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 4268–4285, 2024. 

- [6] D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba. Mastering Atari with discrete world models. In _International Conference on Learning Representations (ICLR)_ , 2021. 

- [7] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 640(8059):647–653, 2025. 

- [8] I. Clavera, V. Fu, and P. Abbeel. Model-augmented actor-critic: Backpropagating through paths. In _International Conference on Learning Representations (ICLR)_ , 2020. 

- [9] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [10] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International Conference on Machine Learning (ICML)_ , 2018. 

- [11] T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel, and S. Levine. Soft actor-critic algorithms and applications. _arXiv preprint arXiv:1812.05905_ , 2019. 

- [12] N. Lambert, K. Pister, and R. Calandra. Investigating compounding prediction errors in learned dynamics models. _arXiv preprint arXiv:2203.09637_ , 2022. 

- [13] C. Xiao, Y. Wu, C. Ma, D. Schuurmans, and M. M¨uller. Learning to combat compoundingerror in model-based reinforcement learning. _arXiv preprint arXiv:1912.11206_ , 2019. 

- [14] D. Hafner, W. Yan, and T. Lillicrap. Training agents inside of scalable world models. _arXiv preprint arXiv:2509.24527_ , 2025. 

10 

- [15] J. Amigo, R. Khorrambakht, E. Chane-Sane, N. Mansard, and L. Righetti. First order modelbased RL through decoupled backpropagation. In _Conference on Robot Learning (CoRL)_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 5234–5255, 2025. 

- [16] K. Chua, R. Calandra, R. McAllister, and S. Levine. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. _Advances in Neural Information Processing Systems_ , 31, 2018. 

- [17] N. Hansen, X. Wang, and H. Su. Temporal difference learning for model predictive control. In _International Conference on Machine Learning (ICML)_ , 2022. 

- [18] N. Hansen, H. Su, and X. Wang. TD-MPC2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [19] J. Schrittwieser, I. Antonoglou, T. Hubert, K. Simonyan, L. Sifre, S. Schmitt, A. Guez, E. Lockhart, D. Hassabis, T. Graepel, et al. Mastering Atari, Go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

- [20] Y. Niu, Y. Pu, Z. Yang, X. Li, T. Zhou, J. Ren, S. Hu, H. Li, and Y. Liu. LightZero: A unified benchmark for Monte Carlo tree search in general sequential decision scenarios. _Advances in Neural Information Processing Systems_ , 36, 2023. 

- [21] Y. Pu, Y. Niu, Z. Yang, J. Ren, H. Li, and Y. Liu. UniZero: Generalized and efficient planning with scalable latent world models. _Transactions on Machine Learning Research (TMLR)_ , 2025. 

- [22] R. Khorrambakht, J. Ortiz-Haro, J. Amigo, O. Mostafa, D. Dugas, F. Meier, and L. Righetti. WorldPlanner: Monte Carlo tree search and MPC with action-conditioned visual world models. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 22166– 22173, 2026. 

- [23] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg. DayDreamer: World models for physical robot learning. In _Conference on Robot Learning (CoRL)_ , volume 205 of _Proceedings of Machine Learning Research_ , pages 2226–2240, 2022. 

- [24] D. P. Kingma and M. Welling. Auto-encoding variational Bayes. In _International Conference on Learning Representations (ICLR)_ , 2014. 

- [25] M. Janner, J. Fu, M. Zhang, and S. Levine. When to trust your model: Model-based policy optimization. _Advances in Neural Information Processing Systems_ , 32, 2019. 

- [26] T. Kurutach, I. Clavera, Y. Duan, A. Tamar, and P. Abbeel. Model-ensemble trust-region policy optimization. In _International Conference on Learning Representations (ICLR)_ , 2018. 

- [27] J. Buckman, D. Hafner, G. Tucker, E. Brevdo, and H. Lee. Sample-efficient reinforcement learning with stochastic ensemble value expansion. _Advances in Neural Information Processing Systems_ , 31, 2018. 

- [28] C. Li, A. Krause, and M. Hutter. Uncertainty-aware robotic world model makes offline modelbased reinforcement learning work on real robots. _arXiv preprint arXiv:2504.16680_ , 2025. 

- [29] A. Jordana, J. Zhang, J. Amigo, and L. Righetti. An introduction to zero-order optimization techniques for robotics. _The International Journal of Robotics Research_ , 2026. To appear. 

- [30] I. Georgiev, V. Giridhar, N. Hansen, and A. Garg. PWM: Policy learning with multi-task world models. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [31] E. Alonso, A. Jelley, V. Micheli, A. Kanervisto, A. Storkey, T. Pearce, and F. Fleuret. Diffusion for world modeling: Visual details matter in Atari. _Advances in Neural Information Processing Systems_ , 37, 2024. 

11 

- [32] K. Frans, D. Hafner, S. Levine, and P. Abbeel. One step diffusion via shortcut models. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [33] B. Chen, D. Mart´ı Mons´o, Y. Du, M. Simchowitz, R. Tedrake, and V. Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_ , 37, 2024. 

- [34] D. Yang, D. Tjia, J. Berg, D. Damen, P. Agrawal, and A. Gupta. Rank2Reward: Learning shaped reward functions from passive video. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2806–2813, 2024. 

- [35] Z. Zhou, P. Atreya, A. Lee, H. R. Walke, O. Mees, and S. Levine. Autonomous improvement of instruction following skills via foundation models. In _Conference on Robot Learning (CoRL)_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 4805–4825, 2024. 

- [36] X. Zhang, Z. Xu, Y. Tao, Y. Wang, Y. She, and A. Boularias. Learning visual feature-based world models via residual latent action. _arXiv preprint arXiv:2605.07079_ , 2026. 

- [37] A. K. Sharma, Y. Sun, N. Lu, Y. Zhang, J. Liu, and S. Yang. World-Gymnast: Training robots with reinforcement learning in a world model. _arXiv preprint arXiv:2602.02454_ , 2026. 

- [38] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta˜neda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, Z. Wang, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. Fan, and Y. Zhu. SONIC: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [39] I. Kostrikov, A. Nair, and S. Levine. Offline reinforcement learning with implicit Q-learning. In _International Conference on Learning Representations (ICLR)_ , 2022. 

- [40] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems (RSS)_ , 2023. 

- [41] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 586–595, 2018. 

- [42] E. Xing, V. Luk, and J. Oh. Stabilizing reinforcement learning in differentiable multiphysics simulation. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [43] R. Cadene, S. Alibert, A. Soare, Q. Gallouedec, A. Zouitine, S. Palma, P. Kooijmans, M. Aractingi, M. Shukor, D. Aubakirova, M. Russi, F. Capuano, C. Pascal, J. Choghari, K. Meftah, M. Ellerbach, J. Moss, and T. Wolf. LeRobot: State-of-the-art machine learning for real-world robotics in PyTorch. https://github.com/huggingface/lerobot, 2024. 

12 

## **A Appendix** 

### **A.1 Qualitative Comparison of World Model Rollouts** 


(b) 

Figure 6: (a) Unrolling of real and model-predicted trajectories comparing the real trajectory (top), the DIAMOND diffusion trajectory (middle), and the DreamerV3 trajectory (bottom), every 5 steps (12 s). (b) Unrolling of real and model-predicted trajectories comparing the real trajectory (top), the DreamerV3 trajectory (middle), and the DreamerV4 diffusion trajectory (bottom), every 5 steps (12 s), with both models initialized with zero context, and the cube initially occluded. Note that the local model violates object permanence by spawning the cube throughout the rollout. 

### **A.2 Humanoid G1 Experiments: World Model Exploit Patching** 

In this section, we provide additional visual details regarding the world model patching process evaluated on the Unitree G1 humanoid robot. The task involves the robot using a dexterous hand to grasp and lift a box equipped with a semi-soft handle. 

As discussed in the main text, the reinforcement learning (RL) policy initially discovered exploits within the dynamics of the original world model. To address this, we deployed the exploiting policy directly on the real robot to collect targeted patching data during these exploitation attempts. This real-world data was then utilized to patch and refine the world model. We ran seven such rounds, which added 0.19, 0.55, 0.74, 0.80, 1.00, 0.72 and 0.43 hours of data (4.4 hours in total). After each round, the dynamics model pretrained on the 16.5 hours of play data was fine-tuned for 3k updates, with a newly initialized reward head, on the play data and all the data collected so far. 

Figure 7 illustrates the rollouts of the world model before and after this patching process, demonstrating how the updated model successfully corrects the physical inconsistencies that were previously exploited by the RL policy. 

13 


Figure 7: Visual comparison of the world model before and after patching on the Unitree G1 Grab Box task. Rows labeled _original_ display the unpatched world model where the RL policy discovered physical exploits to artificially maximize reward. In the first rollout ( **top two rows** ), the policy exploits the model by moving the hand into a lifting pose, causing the box to spontaneously teleport into its grasp. In the second rollout ( **bottom two rows** ), the hand remains distant but pulls the box toward itself using an “invisible force.” Rows labeled _patched_ show the corrected world model rollouts after being fine-tuned with real-world data collected by deploying these exploiting policies, effectively eliminating the physical hallucinations. 

### **A.3 Humanoid G1: World-Model Accuracy, Gradient Alignment and Compute Cost** 

**World-model accuracy and uncertainty.** On G1, we unroll the global world model and the local RSSM open-loop over the full 64-step episode on 64 held-out trajectories, with the context prefilled with 32 real frames and _K_ = 8 samples per trajectory. The global model reaches an LPIPS [41] of 0.295 against 0.425 for the RSSM (lower is better), and a spread-to-error ratio of 0.665 against 0.275 (higher is better). The RSSM is confidently wrong, consistent with the failure of the “No Diffusion” ablation on all three real-robot tasks (Tables 1–3). 

**Gradient alignment.** Without a differentiable simulator, true gradients are not available. The closest reference is automatic differentiation through the global model, a reference of convenience whose own accuracy is not guaranteed. Even this reference covers only part of our objective: the value term operates in the local latent space and cannot be differentiated through the global model, so we compare the directions of the reward and dynamics terms. On the G1 world model, our decoupled gradient reaches a cosine similarity of 0.52 with this reference, against 0.35 for a nondecoupled Dreamer-style rollout and 0.08 for the local model before online fine-tuning: decoupling yields a 1 _._ 5 _×_ better-aligned gradient. 

**Compute cost.** Backpropagating through the global model takes 45.6 GB and 1.5 s for a single state over a 16-step chunk, i.e., 128 H100 GPUs for our 128 actors. Our method takes 59 ms and 3.6 GB for the same work: 25 _×_ faster on 128 _×_ fewer GPUs for this gradient computation (the full G1 training uses 8 H100 per seed; Table 4). 

14 

### **A.4 Extended Quantitative Results: Per Task Sample and Time Efficiency** 


Figure 8: (a) Efficiency comparison on the Push-T task: sample efficiency of DMO (4M samples) versus PPO (48M samples), SAC, and the No Diffusion and No RSSM Finetuning ablations (left), and corresponding time efficiency comparison (right). (b) Efficiency comparison on the Push Cube task: sample efficiency of DMO (4M samples) versus PPO (25M samples), SAC, and the No Diffusion and No RSSM Finetuning ablations (left), and corresponding time efficiency comparison (right). (c) Efficiency comparison on the G1 Grab Box task: sample efficiency of DMO (4M samples) versus PPO (25M samples), SAC, and the No Diffusion and No RSSM Finetuning ablations (left), and corresponding time efficiency comparison (right). The dashed line is the best evaluation of offline RL (IQL), which uses no environment samples. Every experiment was run with 4 seeds. 

15 

All learning curves report the return of the training episodes: the undiscounted sum, over a 64step episode, of the global reward model’s per-frame predictions, as a running mean over recent episodes, with stochastic actions and without the entropy bonus. Each episode starts from a context drawn from the recorded data (a single frame on Push-T, a 32-frame window on Push Cube and G1). In Fig. 5, rewards are min-max normalized per task over all logged values; sample counts and wall-clock times are divided by the largest value reached in that task; curves are averaged over seeds and then over tasks; the shaded band is one standard deviation across tasks. 

### **A.5 The Algorithm** 

Given the described global and local models, we present our complete procedure in Algorithm 1. To ensure stable policy updates, we use the SAPO version of the DMO algorithm, which incorporates the Soft Analytic Policy Optimization (SAPO) objective [42]. Specifically, we optimize the policy parameters **_θ_** to maximize the entropy-regularized expected return: 


where _lh_ is the local latent state at the _h_ -th frame of the trajectory generated by the global model _f_<sup>_→_</sup> , _R_<sup>ˆ</sup> _ϕ_ is the reward head of the local model, and _V_ **_ψ_**<sup>_πθ_</sup> is the mean of an ensemble of 10 critics. As in SAPO [42], the entropy term is normalized with the target entropy _H_<sup>¯</sup> _<_ 0 (Table 4): _H_<sup>˜</sup> _h_ := ( _H_<sup>ˆ</sup> _h_ + _|H|_<sup>¯</sup> ) _/_ (2 _|H|_<sup>¯</sup> ), where _H_<sup>ˆ</sup> _h_ = _−_ log _πθ_ ( _ah | lh_ ) is a single-sample estimate of the entropy of the action distribution (a tanh-squashed, scaled Gaussian), and the temperature _α_ is tuned automatically by minimizing _α_ ( _H_<sup>ˆ</sup> _h − H_<sup>¯</sup> ) with the unnormalized estimate. If an episode ends at step _d_ inside the unroll, the sum in Eq. (1) stops there and ends with _γ_<sup>_d_+1</sup> _V_ **_ψ_**<sup>_πθ_(</sup><sup>_ld_+1) instead of</sup><sup>_γHV_</sup> **_ψ_**<sup>_πθ_(</sup><sup>_lH_),and a</sup> new sum starts. 

The critic is an ensemble of 10 networks _V_ **_ψ_** _k_ , trained by minimizing the temporal difference error against _λ_ -returns: 


where, for _t_ = 0 _, . . . , H −_ 1: 


Here, _r_ ˜ _n_ := _rn_ + _αH_<sup>˜</sup> _n_ is the global reward model’s prediction _rn_ plus the normalized entropy bonus, and _V_ **_ψ_**<sup>min</sup> is the minimum of two ensemble members drawn at random at each step; no separate target network is used. If an episode ends at step _d < H −_ 1, _H_ is replaced by _d_ + 1 for _t ≤ d_ . 

When unrolling the DreamerV4 global world model, we employ KV Caching to significantly reduce inference time. To initialize the context of the DreamerV4 world model during RL training, we do not start from a single frame. Instead, we sample a short history window of length _L_ init = 32 from the real trajectory dataset and pre-fill the key-value (KV) caches of the Transformer. This provides the model with sufficient temporal context to resolve potential ambiguities (e.g., momentary occlusions of the object) before the policy begins its interaction. 

16 

**Algorithm 1** DMO-SAPO with global and local world models 

Offline training of the DIAMOND or DreamerV4 diffusion world model _f_<sup>_→_</sup> and global reward model _r_ Offline pretraining of the local DreamerV3 world model _fϕ_<sup>_←_(including its reward head</sup><sup>_R_ˆ</sup><sup>_ϕ_)</sup> Fill the replay buffer _B_ with transitions generated by the initial policy in _f_<sup>_→_</sup> **for** epoch = 1 to N **do** # Backward model learning **for** model mini epoch (10 _,_ 000 updates in the first epoch, 64 afterwards) **do** Sample sequences of transitions ( _o, a, r_ ) from _B_ **_ϕ_** _←_ **_ϕ_** _− η_ **_ϕ_** _∇ϕLf ←_ ( **_ϕ_** ), where _Lf ←_ is the DreamerV3 model learning loss **end for** # Actor and critic learning _total_ _~~r~~ eward ←_ 0 _l_ 0 _←_ latent state of _fϕ_<sup>_←_for the current frame</sup><sup>_o_0</sup> **for** _h_ = 0 to _H −_ 1 **do** _ah ∼ πθ_ ( _· | lh_ ), _H_ ˆ _h ←−_ log _πθ_ ( _ah | lh_ ), _H_ ˜ _h ←_ ( ˆ _Hh_ + _|H|_ ¯ ) _/_ (2 _|H|_ ¯ ) _oh_ +1 _← f_<sup>_→_</sup> ( _oh, ah_ ) (where _f_<sup>_→_</sup> is the DIAMOND or the DreamerV4 diffusion global world model) _rh ← r_ ( _oh_ +1 _, ah_ ) (where _r_ is the global reward model, only used to learn the local reward and the value function) Store ( _oh, ah, rh_ ) in _B lh_ +1 _←_ latent state of _fϕ_<sup>_←_for</sup><sup>_oh_+1, from encoder(</sup><sup>_oh_+1) and its recurrent state</sup> _R_ ˆ _h ← R_ ˆ _ϕ_ ( _lh_ +1) _total_ _~~r~~ eward ← total_ _~~r~~ eward_ + _γ_<sup>_h_�</sup> _R_<sup>ˆ</sup> _h_ + _α H_<sup>˜</sup> _h_ � **end for** Compute _L_<sup>DMO-SAPO</sup> _π_ ( **_θ_** ) from _total_ _~~r~~ eward_ and _γ_<sup>_H_</sup> _V_ **_ψ_**<sup>_πθ_(</sup><sup>_lH_)</sup> Compute _LV_ ( **_ψ_** ) from ( _l_ 0 _, . . . , lH_ ) and (˜ _r_ 0 _, . . . ,_ ˜ _rH−_ 1) _∂fϕ_<sup>_←_(</sup><sup>_l,a_)</sup> _∂fϕ_<sup>_←_(</sup><sup>_l,a_)</sup> Use _∂l_ and _∂a_ to approximate<sup>_∂f_</sup> _∂o_<sup><u>(</u></sup><sup>_o,a_</sup><sup><u>)</u></sup> and<sup>_∂f_</sup> _∂a_<sup><u>(</u></sup><sup>_o,a_</sup><sup><u>)</u></sup> , ����( _lh,ah_ ) ����( _lh,ah_ ) ����( _oh,ah_ ) ����( _oh,ah_ ) _h_ = 0 _, . . . , H −_ 1, during the following backward pass. _∇θL_<sup>DMO-SAPO</sup> _π_ ( **_θ_** ) _←_ backward( _L_<sup>DMO-SAPO</sup> _π_ ( **_θ_** )) **_θ_** _←_ **_θ_** + _η_ **_θ_** _∇θL_<sup>DMO-SAPO</sup> _π_ ( **_θ_** ) Update log _α_ by a gradient descent step on _H_<sup><u>1</u></sup> � _Hh_ =0 _−_ 1<sup>_α_( ˆ</sup><sup>_Hh −H_¯)</sup> **_ψ_** _←_ **_ψ_** _− η_ **_ψ_** _∇ψLV_ ( **_ψ_** ) **end for** 

17 

### **A.6 Additional Real-World Deployments and Behaviors** 


Figure 9: Three real-robot Push-T trajectories executed by the policy learned with our approach. 


Figure 10: Three real-robot G1 Grab Box trajectories executed by the policy learned with our approach. 

As shown in Fig. 11, DMO exhibits an emergent active search strategy when the object is out of view. Specifically, the agent retreats to the goal area and executes a full 360<sup>_◦_</sup> yaw rotation to scan the environment. In contrast, the BC policy (first row of Fig. 11) simply moves backward when the cube is lost. This blind retraction is brittle (if the cube is located behind the robot, the agent drags it farther away) and reflects the poor search strategy in the demonstration subset of the dataset. However, RL leverages random exploration during training to discover more effective behaviors. 

Then, as mentioned in Sec. 4.3 and shown in Fig. 13, the BC (ACT) policy consistently stops before fully pushing the cube into the goal, whereas DMO successfully completes the task by leveraging sparse successful examples with high terminal rewards. 

Finally, we evaluated robustness to dynamics distribution shifts by replacing the low-level locomotion controller with a variant with a different response behavior and gait style (no Raibert heuristics in reward). As shown in Fig. 12, without collecting new data or retraining the world models, the robot successfully pushes the cube into the goal. While PPO failed to generalize due to its higher entropy and less smooth action output, both DMO and BC maintained their performance. This result addresses a common critique of model-based methods—that models must be retrained for every specific robot configuration. Instead, this experiment demonstrates that the DMO framework correctly discovers stabilizing and smooth feedback strategies that are robust to variations in low-level dynamics. This finding implies that pretrained general-purpose world models may still produce useful policies for downstream tasks. A deeper investigation of this axis is the topic of our future research. 

18 


Figure 11: Comparison of search strategies under partial observability. **Top:** When the cube is out of view, the BC policy (ACT) executes a naive backward retreat, which fails to locate the object if it is directly behind. **Bottom:** The DMO policy exhibits an emergent active search behavior, rotating to visually scan the environment and successfully localize the target. 

19 


Figure 12: Real-world execution of the DMO-learned policy for the Go2 Push Cube task when using a different low-level policy than seen during training. **Top:** Standard successful push trajectory. **Middle:** Emergent active search behavior; when the object is initially out of view (or lost), the agent retreats and scans the environment to localize the cube before pushing. **Bottom:** Successful approach and push from a different initial configuration. 


Figure 13: Task completion comparison. **Top:** The Behavior Cloning (ACT) policy successfully approaches the cube but stops pushing before the object enters the goal, reflecting the sub-optimal demonstration distribution. **Bottom:** Our RL Policy (DMO) generalizes beyond the demonstrations, learning to push the cube fully into the net to maximize the task reward. 

20 

### **A.7 Implementation Details and Hyperparameters** 

Table 4: **Hyperparameters.** Settings for PPO and DMO-SAPO across the three tasks (in the RL block, values that differ across tasks are given as Push-T / Push Cube / G1 Grab Box), along with the specific World Model architectures used in our framework. DIAMOND is used for Push-T, while DreamerV4 is used for both Push Cube and G1 Grab Box. 

||**RL Algorithms (All Tasks)**||**Global World**|**Model (DreamerV4)**|
|---|---|---|---|---|
|Parameter|PPO|DMO-SAPO|Parameter|Push Cube<br>G1 Grab Box|
|Image Size (Input)|64_×_64|64_×_64|Image Size (Generation)<br>|128_×_128<br>256_×_256<br><br>|
|Horizon (_H_)|64|16|Patch Size<br>|16<br>16<br><br>|
|Gamma (_γ_)|0.99|0.99|Enc/Dec Model Dim|768<br>1024|
|Lambda (_λ_)|0.95|0.95|Dynamics Model Dim|1536<br>1536|
|Mini-batch Size|4096|1024|Num Latents / Bottleneck|256 / 16<br>256 / 32|
|Mini-epochs|4|8|Enc/Dec/Dyn Layers|12 / 12 / 24<br>16 / 16 / 24|
|Optimizer<br>|Adam<br>|AdamW<br>|Enc/Dec/Dyn Heads|12 / 12 / 24<br>16 / 16 / 24|
|Optimizer(_β_1_, β_2)<br>|(0.9, 0.999)<br>|(0.7, 0.95)<br>|Diffusion Steps|4<br>4|
|LR Schedule<br>|Linear<br>|Linear<br>|Context Length (RL)|96<br>32|
|Learning Rate (Actor)<br>|5e_−_4<br>|2e_−_3<br>|Per Rank Batch Size (Tok. / Dyn.)|2 / 1<br>1 / 1|
|Learning Rate (Critic)<br>Li R E|5e_−_4|5e_−_4<br>53|<br>Compute (Tok. / Dyn.)|24 H200 / 64 H100<br>64 H100 / 64 H100|
|earnng ate ntropy|–|e_−_||<br>|
|<br>|||Gradient Accum. Steps Tok. / Dyn.|5 / 4<br>4 / 4|
|Entropy Coef / Target<br>Grad Norm Cli|0.01<br>05|_−_6/_−_6/_−_58<br>10|<br>Effective Batch Size (Tok. / Dyn.)|240 / 256<br>256 / 256|
|p<br>Replay Buffer Size|.<br>–|.<br>10<sup>6</sup>|Training Updates (Tok. / Dyn.)|130k / 29k<br>45k / 52k|
|<br>Num Actors|256|128|**Global World Model (**|**DIAMOND - Push-T Only)**|
|Network|CNN + MLP|MLP [256, 128, 64]|||
|Activation|ReLU|SiLU|Parameter|Value|
|Compute (per Seed)|1 H100 / 4 H200 / 4 H200|1 H100 / 4 H200 / 8 H100|Image Size (Generation)|64_×_64|
|**Local Wo**|**rld Model (RSSM - Dreame**|**rV3 Style)**|Diffusion Steps<br>Conditioning Steps|3<br>4|
|Parameter|Push-T|Push Cube & G1 Grab Box|<br>UNet Channels|[64, 64, 64, 64]|
|Learning Rate|1e_−_4|1e_−_4|UNet Depths|[2, 2, 2, 2]|
|Recurrent State Size|1024|4096|Attn Depths|[0, 0, 0, 0]|
|Stochastic/Discrete Size|32|32|Cond Channels|256|
|Dense Units|640|1024|Sigma Distribution|_µ_=_−_0_._4_, σ_ = 1_._2|
|Channels Multiplier|48|96|<br>Optimizer|<br>AdamW (_β_ = 0_._999)|
|MLP Layers|3|5|Learning Rate|<br>1e_−_4|
|KL Scales (Dyn/Rep/Free)|0.5 / 0.1 / 1.0<br>|0.5 / 0.1 / 1.0<br>|<br>Batch Size|2 (Accum Grad 4=8)|
|Reward Bins / Range|255 / symlog[_−_20_,_20]|255 / symlog[_−_20_,_20]|Compute|<br>1 RTX4090|


**Behavior cloning baseline.** The BC baseline is the LeRobot [43] implementation of ACT [40], with a ResNet-18 backbone, hidden dimension 512 and a KL weight of 10. On G1, it uses 4 encoder and 1 decoder layers and a 32-dimensional latent, is trained on 231 demonstrations (25,960 frames at 10 Hz) for 200k steps at batch size 256 and learning rate 10<sup>_−_4</sup> , and executes chunks of 20 actions open-loop at 10 Hz. On Push Cube, it is trained on 1,200 episodes (37,971 frames at 5 Hz) of 64 _×_ 64 images for 700k steps at batch size 128 and learning rate 10<sup>_−_5</sup> ; it predicts 25 actions but executes only the first and re-plans at every step. 

### **A.8 CEM-MPC with the Global World Model** 

We additionally implemented a Cross-Entropy Method (CEM) model-predictive controller for the Go2 Push Cube task using the same global world model and reward model employed during RL training. This experiment was designed to assess whether the learned global model could be used directly for online planning, without policy distillation. 

In order to make planning as efficient as possible, we applied several aggressive optimizations. First, we reduced the number of diffusion steps from 4 to 1. Second, we used only a single outer-loop CEM refinement iteration for each action executed on the robot. Third, we exploited the DreamerV4 dynamics model in chunk-diffusion mode, enabled by the diffusion-forcing-style training procedure, which supports both autoregressive one-step diffusion and joint diffusion over multiple future steps. 

Despite these optimizations, online planning remained prohibitively expensive for real-time control. In practice, achieving real-time inference still required at least 16 H200 GPUs for 128 parallel rollouts. These results, therefore, support our central motivation for policy learning: while large world models can provide accurate forward predictions, direct test-time planning with them remains too computationally demanding, and memorizing the resulting behavior into a policy, as enabled by DMO, remains necessary. 

21 

