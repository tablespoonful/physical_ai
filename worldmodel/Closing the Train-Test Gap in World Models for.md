---
title: "Closing the Train-Test Gap in World Models for Gradient-Based Planning"
date: "2025-12-10"
authors: "Rohun Agrawal; Nimit Kalra; Arjun Parthasarathy; Yann LeCun; Oumayma Bounou; Pavel Izmailov"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2512.09929
pdf: https://arxiv.org/pdf/2512.09929
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.09929)** / [論文ページ](https://arxiv.org/abs/2512.09929)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Closing the Train-Test Gap in World Models for Gradient-Based Planning** 

**Rohun Agrawal**<sup>_∗_</sup> **Nimit Kalra**<sup>_∗_</sup> **Arjun Parthasarathy**<sup>_∗_</sup> **Yann LeCun** Columbia University Columbia University Columbia University New York University 

**Oumayma Bounou Pavel Izmailov Micah Goldblum** New York University New York University Columbia University 

## **Abstract** 

World models paired with model predictive control (MPC) can be trained offline on large-scale datasets of expert trajectories and enable generalization to a wide range of tasks chosen at inference time. Compared to traditional MPC procedures, which rely either on slow search algorithms or on iteratively solving optimization problems exactly, gradient-based planning offers a computationally efficient alternative. However, the performance of gradient-based planning has thus far lagged behind that of other approaches. In this paper, we propose improved methods for training world models that enable efficient gradient-based planning. We begin with the observation that although a world model is trained on a next-state prediction objective, it is used at test-time to instead estimate a sequence of actions. The goal of our work is to close this train-test gap. To that end, we propose train-time data synthesis techniques that enable significantly improved gradient-based planning with existing world models. At test time, our approach outperforms or matches the classical gradient-free cross-entropy method (CEM) across a variety of object manipulation and navigation tasks in 10% of the time budget. 

## **1 Introduction** 

In robotic tasks, anticipating how the actions of an agent affect the state of its environment is fundamental for both prediction [15] and planning [40, 31]. Classical approaches derive models of the environment evolution analytically from first principles, relying on prior knowledge of the environment, the agent, and any uncertainty [18, 51, 52]. In contrast, learning-based methods infer such models directly from data, enabling them to capture complex dynamics and thus improve generalization and robustness to uncertainty [54, 48, 33]. 

World models [21], in particular, have emerged as a powerful paradigm. Given the current state and an action, the world model predicts the resulting next state. These models can be learned either from exact state information [53] or from high-dimensional sensory inputs such as images [24]. The latter setup is especially compelling as it enables perception, prediction, and control directly from raw images by leveraging pre-trained visual representations, and removes the need for measuring the precise environment states, which is difficult in practice [3, 5]. Recently, world models and their predictive capabilities have been leveraged for planning, enabling agents to solve a variety of tasks [22, 23, 48, 24, 69]. A model of the dynamics is learned offline, while the planning task is defined at inference as a constrained optimization problem: given the current state, find a sequence of actions that results in a state as close as possible to the target state. This inference-time optimization provides an effective alternative to reinforcement learning approaches [54] that often suffer from poor sample efficiency. 

> _∗_ Equal contribution. 


Figure 1: **Model-Simulator Gap.** We analyze the difference between the planning objective and the true simulator distance as a way of diagnosing the failure modes of GBP. In contrast to CEM that inadvertently optimizes simulator distance along with its planning objective, we see GBP’s Model-Simulator Gap grow over the course of optimization. We use 50 unseen trajectories on PointMaze to measure these losses. 

World models are compatible with many model-based planning algorithms. The most commonly used planning methods are search-based, such as the Cross Entropy Method (CEM) [45] and Model Predictive Path Integral control (MPPI) [59], because they have proven effective in practice. However, they are computationally intensive as they require iteratively sampling candidate solutions and performing world model rollouts to evaluate each one, a procedure that scales poorly in highdimensional spaces. Gradient-based methods [55], in contrast, avoid the limitations of sampling by directly exploiting the differentiability of world models to optimize actions end-to-end. These methods eliminate the costly rollouts required by search-based approaches, thus scaling more efficiently in high-dimensional spaces. Despite this promise, gradient-based approaches have thus far seen limited empirical success. 

Gradient-based planning (GBP) suffers from a fundamental train-test gap. World models are typically trained using a next-state prediction objective on datasets of expert trajectories. At test time, however, they are used to optimize a planning objective over sequences of actions. We argue that this mismatch underlies the poor empirical performance of GBP, and we offer two hypotheses to explain why. 1) During planning, the intermediate sequence of actions explored by gradient descent drives the world model into states that were not encountered during training. In these out-of-distribution states, model errors compound, making the world model unreliable as a surrogate for optimization. 2) The actionlevel optimization landscape induced by the world model may be difficult to traverse, containing many poor local minima or flat regions, which hinders effective gradient-based optimization. 

In this work, we address both of these challenges with two strategies: Online World Modeling and Adversarial World Modeling. Both expand the region of familiar latent states by continuously adding new trajectories to the dataset and finetuning the world model on them. To manage the distribution shift between offline expert trajectories and predicted trajectories from planning, Online World Modeling uses the environment simulator to correct states along a trajectory produced by performing GBP. Finetuning on these corrected trajectories ensures that the world model performs sufficiently well when GBP enters regimes of latent state space outside of the expert trajectory distribution. To overcome the difficulties of optimizing over a non-smooth loss surface during GBP, Adversarial World Modeling perturbs expert trajectories in the direction that maximizes the world model’s loss. Adversarial finetuning smooths the induced action loss landscape, making it easier to optimize via gradient-based planning. 

Our contributions are summarized as follows: 

1. We identify the train-test gap in world models used for gradient-based planning, using the model-simulator gap as a diagnostic metric to explain why GBP exploits poor world model predictions. 

2. We identify that DAgger-style finetuning and adversarial training are strong candidates to address issues specific to GBP, and adapt them using Online World Modeling (OWM) and Adversarial World Modeling (AWM). 

3. We demonstrate empirically that AWM enables GBP to match or exceed the performance of the gradient-free Cross-Entropy Method across six simulated robotic/navigation tasks and a real-world high-dimensional egocentric pose planning benchmark, while operating in 10× less wall-clock time and establishing a new Pareto frontier for planning efficiency with world models. 

2 

4. We analyze aspects of GBP’s failure modes to uncover why OWM is unable to improve GBP performance, revealing that data scale alone is not sufficient. Furthermore, this analysis provides evidence for why AWM significantly improves GBP performance on a variety of domains. 

## **2 Why Gradient-Based Planning Fails** 

### **2.1 Preliminaries** 

World models learn environment dynamics by predicting the state resulting from taking an action in the current state. Then, at test time, the learned world model enables planning by simulating future trajectories and guiding action optimization. Formally, a world model approximates the (potentially unknown) dynamics function _h_ : _S × A →S_ , where _S_ denotes the state space and _A_ the action space. The environment evolves according to _st_ +1 = _h_ ( _st, at_ ) where _st ∈S, at ∈A_ denote the state and action at time _t_ , respectively. 

**Latent world models.** In practice, we typically do not have access to the exact state of the environment; instead, we only receive partial observations of it, such as images. In order for a world model to efficiently learn in the high-dimensional observation space _O_ , an embedding function Φ _µ_ : _O →Z_ is employed to map observations to a lower-dimensional latent space _Z_ . Then, given an embedding function Φ _µ_ , our goal is to learn a latent world model _fθ_ : _Z × A →Z_ , such that 


The choice of Φ _µ_ directly affects the expressivity of the latent world model. In this work, we use a fixed encoder pretrained with self-supervised learning that yields rich feature representations out of the box. 

**Training.** To train a latent world model, we sample triplets of the form ( _ot, at, ot_ +1) from an offline dataset of trajectories _T_ and minimize the _ℓ_ 2 distance between the true next latent state _zt_ +1 = Φ _µ_ ( _ot_ +1) and the predicted next latent state _z_ ˆ _t_ +1. This procedure is represented by the following teacher-forcing objective: 


Notably, we only minimize this objective with respect to the world model’s parameters _θ_ , not those of the potentially large embedding function. 

**Planning.** At test-time, we use a learned world model to optimize candidate action sequences for reaching a goal state. By recursively applying the world model over an action sequence starting from an initial latent state, we obtain a predicted latent goal state and therefore the distance to the true goal state in latent space. This allows us to find the optimal action sequence 


where _z_ ˆ _H_ +1 is produced by the recursive procedure 


We use the function rollout _f_ : _Z × A_<sup>_H_</sup> _→Z_<sup>_H_</sup> to denote this recursive procedure. 

Gradient-based planning (GBP) solves the planning objective (3) via gradient descent. Crucially, since the world model is differentiable, _∇{a_ ˆ _t}z_ ˆ _H_ +1 = _∇{a_ ˆ _t}_ rollout _f_ ( _z_ 1 _, {a_ ˆ _t}_ ) _H_ +1 is well-defined. In contrast, the search-based CEM is gradient-free, but requires evaluating substantially more action sequences. We detail GBP in Algorithm 1 and CEM in Section C.2. 

As errors can propagate over long horizons, Model Predictive Control (MPC) is commonly used to repeatedly re-plan by optimizing an _H_ -step action sequence but executing only the first _K ≤ H_ actions before replanning from the updated state. 

3 

**Algorithm 1** Gradient-Based Planning via Gradient Descent 

**Input:** Start state _z_ 1, goal state _z_ goal, world model _fθ_ , horizon _H_ , optimization iterations _N_ Initialize action prediction _{a_ ˆ _t}_<sup>_H_</sup> _t_ =1<sup>_∼N_(0</sup><sup>_, IH_)</sup> **for** _i_ = 1 _, . . . , N_ **do** _z_ ˆ _H_ +1 _←_ rollout _f_ ( _z_ 1 _, {a_ ˆ _t}_ ) _H_ +1 _L_ goal _←∥z_ ˆ _H_ +1 _− z_ goal _∥_ 2<sup>2</sup> _{a_ ˆ _t} ←{a_ ˆ _t} − η · ∇{a_ ˆ _t}L_ goal **end for** 

### **2.2 Gradient-Based Planning’s Failure Modes** 

Gradient-based planning minimizes a planning loss computed through the world model’s predictions. Wherever the world model is imperfect, this loss does not reflect what would actually happen in the environment. We find that GBP exploits exactly these inaccuracies, converging to action sequences that achieve low planning loss in the model but fail in the real environment. To measure this, we define the _model-simulator gap_ ∆= _L_ env _−L_ model, where _L_ model is the planning loss from Algorithm 1 and _L_ env = _∥_ Φ( _s_ final) _− z_ goal _∥_<sup>2</sup> is the true distance to the goal obtained by encoding the simulator’s final state with the visual encoder Φ. A large positive gap means the world model believes the plan is better than it actually is. In Figure 1, we see that although GBP appears to optimize _L_ model well, it completely fails to optimize _L_ env, resulting in a large model-simulator gap. While GBP drives the action sequence into regions where the world model diverges from reality, CEM’s sampling-based optimization appears more robust to model error, resulting in practically no model-simulator gap. 

We hypothesize two reasons why this gap emerges specifically in GBP. First, because GBP is a first-order method, it is more likely to smoothly reach latent states outside the training distribution. In these latent states, the model-simulator gap can be large. Second, the action optimization itself could be unstable, resulting in certain local minima where the model-simulator gap could also be large. This instability likely arises from the fact that the world modeling objective does not encourage smooth input gradients, yet the world model is expected to effectively utilize gradients with respect to its input actions. We now present two finetuning methods designed to improve on these fronts. 

## **3 Online and Adversarial World Modeling** 

### **3.1 Online World Modeling** 

During gradient-based planning, the action sequences being optimized are not constrained to lie within the distribution of behavior seen during training. World models are typically trained on fixed datasets of expert trajectories, whereas GBP selects actions solely to improve the planning objective, without regard to whether those actions resemble expert behavior. As a result, the optimization process often proposes action sequences that are out of distribution. Optimizing through learned models under such conditions is known to induce adversarial inputs [56, 19]. In our setting, these adversarial action sequences drive the world model into regions of the latent state space that were rarely or never observed during training, causing large prediction errors. Even when errors are initially small, they accumulate as the planner rolls the model forward, ultimately degrading long-horizon planning performance. 

A natural first approach to closing this gap is to directly expose the world model to the trajectories it encounters during planning. We call this **Online World Modeling** , which iteratively corrects the trajectories produced by GBP and finetunes the world model on the resulting rollouts. Rather than training solely on expert demonstrations, we repeatedly incorporate trajectories induced by the planner itself, thereby expanding the region of latent states that the world model can reliably predict. 

First, we conduct GBP using the initial and goal latent states of an expert trajectory _τ_ , yielding a sequence of predicted actions _{a_ ˆ _t}_<sup>_H_</sup> _t_ =1<sup>.These actions might send the world model into regions of</sup> the latent space that lie outside of the training distribution. To adjust for this, we obtain a _corrected trajectory_ : the actual sequence of states that would result by executing the action sequence _{a_ ˆ _t}_<sup>_H_</sup> _t_ =1 in the environment using the true dynamics simulator _h_ . We add the corrected trajectory, 


(5) 

4 

**Algorithm 2** Online World Modeling (OWM) 

**Input:** Pretrained world model _fθ_ , simulator dynamics function _h_ , encoder Φ _µ_ , dataset of trajectories _T_ , online iterations _N_ , horizon _H_ , planning optimization iterations _M_ Initialize new trajectory dataset _T_<sup>_′_</sup> **for** _i_ = 1 _, . . . , N_ **do** _τi_ = ( _z_ 1 _, a_ 1 _, z_ 2 _, a_ 2 _, . . . , aH , zH_ +1) _∼T {a_ ˆ _t}_<sup>_H_</sup> _t_ =1<sup>_←_GBP(</sup><sup>_z_1</sup><sup>_, zH_+1</sup><sup>_, fθ, H, M_)</sup> _{s_<sup>_′_</sup> _t_<sup>_}H_</sup> _t_ =2<sup>+1</sup><sup>_←_rollout</sup><sup>_h_(</sup><sup>_s_1</sup><sup>_, {a_ˆ</sup><sup>_t}_)</sup> _{zt_<sup>_′}H_</sup> _t_ =2<sup>+1</sup><sup>_←{_Φ</sup><sup>_µ_(</sup><sup>_s_</sup> _t_<sup>_′_)</sup><sup>_}H_</sup> _t_ =2<sup>+1</sup> _τi_<sup>_′←_(</sup><sup>_z_1</sup><sup>_,_ˆ</sup><sup>_a_1</sup><sup>_, z_</sup> 2<sup>_′,_ˆ</sup><sup>_a_2</sup><sup>_, . . . ,_ˆ</sup><sup>_aH, z_</sup> _H_<sup>_′_</sup> +1<sup>)</sup> _T_<sup>_′_</sup> _←T_<sup>_′_</sup> _∪ τi_<sup>_′_</sup> Train _fθ_ on next-state prediction using _T_<sup>_′_</sup> **end for** 

to the dataset that the world model trains with every time the dataset is updated. Re-training on these corrected trajectories expands the training distribution to cover the regions of latent space induced by gradient-based planning, mitigating compounding prediction errors during planning. We provide more detail in Algorithm 2. 

This procedure is a direct adaptation of DAgger (Dataset Aggregation) [44] to the world model setting. Just as DAgger iteratively retrains a policy on its own rollouts corrected by an expert, we retrain the world model on trajectories corrected by the ground-truth simulator. While intuitive, Online World Modeling requires access to the environment simulator during training, which is a major drawback that prevents its use in realistic settings. 

### **3.2 Adversarial World Modeling** 

Since world models are only trained on the next-state prediction objective, there is no particular reason for their input gradients to be well-behaved. Adversarial training has been shown to result in better behaved input gradients [39], consequently smoothing the input loss surface. Motivated by this observation, we propose an adversarial training objective that explicitly targets regions of the state-action space where the world model is expected to perform poorly. These adversarial samples may lie outside the expert trajectory distribution, which can expose the model to precisely the regions that matter for action optimization. We find that this procedure, which we call **Adversarial World Modeling** , does in fact smooth the loss surface of the planning objective (see Figure 2), improving the stability of action-sequence optimization. 

Adversarial training improves model robustness by optimizing performance under worst-case perturbations [37]. An adversarial example is generated by applying a perturbation _δ_ to an input that maximally increases the model’s loss. To train a world model on adversarial examples, we use the objective 


where _Ba_ = _{δa_ : _∥δa∥∞ ≤ ϵa}_ and _Bz_ = _{δz_ : _∥δz∥∞ ≤ ϵz}_ constrain the magnitude of perturbations for given _ϵa, ϵz_ . Training on these adversarially perturbed trajectories provides an alternative method to Online World Modeling for surfacing states that may be encountered during planning, without relying on GBP rollouts. This is a significant advantage in settings where simulation is expensive or infeasible. 

We generate adversarial latent states using the Fast Gradient Sign Method (FGSM) [19], which efficiently approximates the worst-case perturbations that maximize prediction error [61]. Although stronger iterative attacks such as Projected Gradient Descent (PGD) can be used, we find that FGSM delivers comparable improvements in GBP performance while being significantly more computationally efficient (see Section E.1). This enables us to generate adversarial samples over entire large-scale offline imitation learning datasets. 

For each state-action pair in a given minibatch, we look for small changes to the latent state or action that most increase the world model’s prediction error. Let _ϵa, ϵz_ denote the radius of the perturbation 

5 


Figure 2: **Comparison of optimization landscapes.** We compare the actions optimization landscape of DINO-WM [69] before and after finetuning with AWM and OWM on the PushT task. AWM yields a smoother landscape with a broader basin around the optimum, while OWM makes a negligible difference in the smoothness of the landscape. Additional details are in Section D. 

to the actions _{at}_ and latent states _{zt}_ respectively. We compute gradients _∇δa,δz ∥fθ_ ( _zt_ + _δz, at_ + _δa_ ) _− zt_ +1 _∥_ 2<sup>2withrespecttotheperturbationsandtakeasignedgradientascentstep(i.e.,ina</sup> direction that degrades the prediction) with step sizes _αa_ = 1 _._ 25 _ϵa, αz_ = 1 _._ 25 _ϵz_ . We clip the result so that each entry of the perturbation stays within the radius. This procedure corresponds to a single step of a PGD-style attack, producing perturbations that lie on the edge of the allowed region where they are maximally challenging for the model. See Algorithm 3 for a detailed treatment. 

To initialize the perturbation radii _ϵa, ϵz_ , we use scaling factors _λa, λz_ and find that Adversarial World Modeling is robust for 0 _≤ λa ≤_ 1 and 0 _≤ λz ≤_ 0 _._ 5. Furthermore, we find that fixing _ϵa, ϵz_ to the standard deviation of the initial minibatch is stable across all experiments. Updating this estimate for each batch as in Algorithm 3 yields no consistent improvement in final planning performance. We further analyze design ablations in Section E. 

## **4 Experiments** 

### **4.1 Experimental Setup** 

We evaluate on seven tasks spanning a range of planning domains. The six simulated environments include two navigation tasks (PointMaze, Wall), one rigid-body manipulation task (PushT), one continuous control task (Reacher), and two deformable-object manipulation tasks (Rope, Granular). As a real-world evaluation, we additionally evaluate on egocentric pose planning using the Nymeria dataset [35], where the agent plans a sequence of joint angle and translation actions to reach a target body pose from egocentric visual observations. Full task descriptions and dataset statistics are provided in Appendix Section C.1. 

We use DINO-WM [69] as our base world model across all tasks so that our experiments emulate planning within the latent space of a large-scale world model. The encoder is a frozen DINOv2 [43] backbone and the transition model _fθ_ is implemented as a ViT [11]. 

All planning results are reported under MPC, where an _H_ -step action sequence is optimized but only the first _K_ actions are kept before replanning from the updated state. For GBP, we use Adam [32] throughout. To facilitate progress towards the goal during GBP, we set _L_ goal in Algorithm 1 to an alternate loss function: Weighted Goal Loss (WGL). Instead of the standard goal loss function that only minimizes the _ℓ_ 2-distance between the final latent state produced by planning actions and the goal latent state, WGL encourages intermediate latent states to also be close to the goal latent state. WGL is detailed in Section C.4. 

We compare the planning performance of DINO-WM with Online World Modeling (OWM) and Adversarial World Modeling (AWM). OWM requires simulator access during training and is therefore evaluated only on PushT, PointMaze, and Wall, where fast simulators are available. Results from 

6 


Figure 4: **Egocentric Body Pose Planning Performance.** We plot the Leaf Mean Joint Error (measure of distance between body poses) over the course of optimization for CEM and GBP with both DINO-WM and AWM. Additional details can be found in Section F. 

these environments help us establish whether data coverage expansion improves GBP. AWM, which requires no simulator, is evaluated on all seven tasks. We report all finetuning, planning, and optimization hyperparameters in Table 2. 

### **4.2 Planning Results** 

As shown in Figure 3, AWM substantially improves over the DINO-WM GBP baseline across all six simulated tasks, with gains ranging from +16% on PushT and Wall to +34% on Reacher. Notably, AWM exceeds CEM on PointMaze (98% vs. 92%), Wall (96% vs. 82%), and Reacher (76% vs. 66%), and matches CEM on PushT (92%) and Rope (39%). On Granular, AWM comes within one point of CEM (79% vs. 80%). These results demonstrate that AWM enables GBP to consistently match or exceed CEM across a diverse range of planning domains, making it a viable method for world model planning. 

We surprisingly find that OWM fails to support GBP. On PushT and Wall, OWM produces no improvement over the DINO-WM GBP baseline (76% and 80% respectively, identical to the baseline). On PointMaze, OWM improves over the baseline (88% vs. 68%) but falls short of both AWM (98%) and CEM (92%). In no environment does OWM match CEM. We analyze the reasons for OWM’s poor performance in Section 4.4. 

We also compare AWM to the latent space regularization method LeWM [38]. We find that LeWM is unable to perform GBP as effectively as DINO-WM + AWM. Furthermore, finetuning LeWM with AWM improves its GBP performance, demonstrating the versatility of our method. Additional details can be found in Section G. 

7 


Figure 5: **Visualization of Predicted Body Pose Rollouts.** _Left:_ The initial observation. _Middle:_ Sequence of 8 future body poses from 16 predicted action with each planning method. _Right:_ The goal observation. For visualization, we label the pelvis _•_ , head _•_ , left-hand _•_ , and right-hand _•_ . In the top example, AWM not only reaches the window, but raises its right-hand correctly which CEM fails to do. In the bottom example, we see that AWM is the only method to get close to the gray sofa. 

### **4.3 Planning Computational Efficiency** 

Deploying world model planning on real robotic systems requires planning that is both reliable and fast. While CEM has historically been the dominant planning algorithm because it fulfills the reliability aspect, GBP scales faster by design. Improving performance on GBP requires only more gradient descent iterations over a single world model rollout, whereas CEM must sample additional rollouts. This distinction severely compounds. Figure 6 illustrates this directly on PushT. On a single A100 GPU, GBP optimizes a single horizon of actions on the order of seconds to a couple of minutes, while CEM is on the order of a few minutes to over half an hour. AWM with GBP therefore establishes a new Pareto frontier for world model planning: it achieves performance that matches or exceeds CEM at over an order of magnitude lower wall-clock cost. 

### **4.4 Overcoming GBP’s failure modes** 

We study the effectiveness of OWM to determine if data coverage over latent states that are encountered during planning but might not have been seen during training can lead to gains in closing the model-simulator gap. As we see in Figure 3, OWM is inconsistent in improving GBP performance. Figure 1 demonstrates that OWM fails to decrease the model-simulator gap, which suggests that data coverage is not necessarily the underlying cause of the gap. The significance of this discovery is that compute and data scaling alone will not make GBP viable, and so we must turn towards the optimization process itself. Figure 2 showing OWM does not appear to change the smoothness of the actions optimization landscape only further motivates a need for a method that does. As expected, we see that AWM successfully smooths the loss landscape, getting rid of many local minima. We also see that AWM improves the model-simulator gap, suggesting that a smooth landscape is crucial for GBP to find faithful solutions. 

### **4.5 Realistic Egocentric Pose Planning** 

One of the key disadvantages of CEM is the exponentially large search space that arises from highdimensional actions. We further highlight the benefits of AWM improving GBP performance by evaluating on the task of future body pose prediction using real motion capture and egocentric video data. Specifically, we use the Nymeria [35] dataset that features a 48 dimensional action space for control over an entire body pose. The details of the dataset can be found in Appendix Section F. 

Figure 4 shows that GBP with AWM significantly improves Leaf Mean Joint Error (MJE) on longer horizons over GBP with DINO-WM. Notably, CEM with DINO-WM underperforms both GBP methods on the longest-horizon, indicating that GBP is more suitable for humanoid-style tasks that 

8 


Figure 6: **Planning efficiency on PushT** . _Left:_ GBP success rate as a function of wall-clock time controlled by the number of gradient descent iterations taken in a single MPC horizon. _Right:_ CEM success rate as a function of wall-clock time controlled by the number of rollouts per CEM iteration. Note that the x-axis is logarithmic, highlighting that GBP operates in over an order of magnitude less wall-clock time than CEM. 

require long-horizon planning. Figure 5 provides visualizations justifying AWM’s superior planning ability that allows it to achieve the most physically plausible goal poses. 

## **5 Limitations** 

We conclude that OWM is an ineffective solution for improving GBP, however, it is important to reiterate that it requires a simulator to improve data coverage, a tool that is not available for realistic tasks. In Section E.2, we see that setting perturbation radii to be too large can degrade performance, and so AWM introduces new hyper-parameters that might require tuning aside from GBP’s hyperparameters. Although AWM achieves strong performance in long-horizon, realistic environments, it is not yet clear if AWM+GBP could run reliably on real hardware at a reasonable frequency. 

## **6 Conclusion** 

In this work, we introduce _Online World Modeling_ and _Adversarial World Modeling_ as techniques for addressing the train-test gap that arises when world models trained on next-state prediction are used for iterative gradient-based planning. Across our experiments, these methods substantially improve the reliability of GBP and, in some settings, allow it to match or outperform sampling-based planners such as CEM. By narrowing this gap, our results suggest that gradient-based planning can be a practical alternative for planning with world models, particularly in settings where computational efficiency is critical. An important direction for future work is to implement these methods on real-world hardware. Adversarial training may additionally improve a world model’s robustness to environmental adversaries or stochasticity. More broadly, world models offer a natural advantage over policy-based reinforcement learning in long-horizon decision making. Our work can make significant progress in the development of humanoid robots. Automating physical labor can have massive positive impact in many industries. 

9 

## **References** 

- [1] Pulkit Agrawal, Ashvin V Nair, Pieter Abbeel, Jitendra Malik, and Sergey Levine. Learning to poke by poking: Experiential learning of intuitive physics. _Advances in neural information processing systems_ , 29, 2016. 

- [2] Adil Kaan Akan and F. Güney. Stretchbev: Stretching future instance prediction spatially and temporally. In _European Conference on Computer Vision_ , 2022. URL `https://api. semanticscholar.org/CorpusId:247749011` . 

- [3] Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a jointembedding predictive architecture. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15619–15629, 2023. 

- [4] Randall Balestriero and Yann LeCun. Lejepa: Provable and scalable self-supervised learning without the heuristics, 2025. URL `https://arxiv.org/abs/2511.08544` . 

- [5] Adrien Bardes, Q. Garrido, Jean Ponce, Xinlei Chen, Michael G. Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video. _ArXiv_ , abs/2404.08471, 2024. URL `https://api.semanticscholar. org/CorpusId:269137489` . 

- [6] Homanga Bharadhwaj, Kevin Xie, and F. Shkurti. Model-predictive control via crossentropy and gradient-based optimization. _ArXiv_ , abs/2004.08763, 2020. URL `https: //api.semanticscholar.org/CorpusId:215827996` . 

- [7] Oumayma Bounou, Jean Ponce, and Justin Carpentier. Online learning and control of complex dynamical systems from sensory input. _Advances in Neural Information Processing Systems_ , 34:27852–27864, 2021. 

- [8] Siwei Chen, Yiqing Xu, Cunjun Yu, Linfeng Li, Xiao Ma, Zhongwen Xu, and David Hsu. Benchmarking deformable object manipulation with differentiable physics. _ArXiv_ , abs/2210.13066, 2022. URL `https://api.semanticscholar.org/CorpusId:257482484` . 

- [9] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion, 2024. URL `https://arxiv.org/abs/2303.04137` . 

- [10] Marc Deisenroth and Carl E Rasmussen. Pilco: A model-based and data-efficient approach to policy search. In _Proceedings of the 28th International Conference on machine learning (ICML-11)_ , pages 465–472, 2011. 

- [11] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale, 2021. 

- [12] Katrina Drozdov, Ravid Shwartz-Ziv, and Yann LeCun. Video representation learning with joint-embedding predictive architectures. _ArXiv_ , abs/2412.10925, 2024. URL `https://api. semanticscholar.org/CorpusId:274777110` . 

- [13] Ashley D. Edwards, Himanshu Sahni, Yannick Schroecker, and C. Isbell. Imitating latent policies from observation. _ArXiv_ , abs/1805.07914, 2018. URL `https://api.semanticscholar. org/CorpusId:29156793` . 

- [14] Chelsea Finn and Sergey Levine. Deep visual foresight for planning robot motion. _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2786–2793, 2016. URL `https://api.semanticscholar.org/CorpusID:2780699` . 

- [15] Chelsea Finn, I. Goodfellow, and S. Levine. Unsupervised learning for physical interaction through video prediction. _ArXiv_ , abs/1605.07157, 2016. URL `https://arxiv.org/pdf/ 1605.07157.pdf` . 

10 

- [16] Pete Florence, Corey Lynch, Andy Zeng, Oscar A Ramirez, Ayzaan Wahid, Laura Downs, Adrian Wong, Johnny Lee, Igor Mordatch, and Jonathan Tompson. Implicit behavioral cloning. In _Conference on robot learning_ , pages 158–168. PMLR, 2022. 

- [17] Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4rl: Datasets for deep data-driven reinforcement learning, 2021. URL `https://arxiv.org/abs/2004. 07219` . 

- [18] Herbert Goldstein, Charles P Poole, and John Safko. _Classical mechanics_ , volume 2. Addisonwesley Reading, MA, 1950. 

- [19] Ian J Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. In _International Conference on Learning Representations_ , 2014. 

- [20] Yanchen Guan, Haicheng Liao, Zhenning Li, Guohui Zhang, and Chengzhong Xu. World models for autonomous driving: An initial survey. _ArXiv_ , abs/2403.02622, 2024. URL `https://api.semanticscholar.org/CorpusId:268249117` . 

- [21] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2(3), 2018. 

- [22] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 

- [23] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 

- [24] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [25] Mikael Henaff, William F Whitney, and Yann LeCun. Model-based planning with discrete and continuous actions. _arXiv preprint arXiv:1705.07177_ , 2017. 

- [26] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zak Murez, Corina Gurau, Hudson Yeo, Alex Kendall, R. Cipolla, and J. Shotton. Model-based imitation learning for urban driving. _ArXiv_ , abs/2210.07729, 2022. URL `https://api.semanticscholar.org/CorpusId: 252907712` . 

- [27] Matthew Jackson, Michael Matthews, Cong Lu, Benjamin Ellis, Shimon Whiteson, and J. Foerster. Policy-guided diffusion. _ArXiv_ , abs/2404.06356, 2024. URL `https://api. semanticscholar.org/CorpusId:269009692` . 

- [28] Lukasz Kaiser, Mohammad Babaeizadeh, Piotr Milos, Blazej Osinski, Roy H. Campbell, K. Czechowski, D. Erhan, Chelsea Finn, Piotr Kozakowski, Sergey Levine, Afroz Mohiuddin, Ryan Sepassi, G. Tucker, and Henryk Michalewski. Model-based reinforcement learning for atari. _ArXiv_ , abs/1903.00374, 2019. URL `https://api.semanticscholar.org/CorpusID: 67856232` . 

- [29] Maximilian Karl, Maximilian Sölch, Justin Bayer, and Patrick van der Smagt. Deep variational bayes filters: Unsupervised learning of state space models from raw data. _ArXiv_ , abs/1605.06432, 2016. URL `https://api.semanticscholar.org/CorpusID:14992224` . 

- [30] Efstathios Karypidis, Ioannis Kakogeorgiou, Spyros Gidaris, and Nikos Komodakis. Dinoforesight: Looking into the future with dino. _arXiv preprint arXiv:2412.11673_ , 2024. 

- [31] Lydia E Kavraki, Petr Svestka, J-C Latombe, and Mark H Overmars. Probabilistic roadmaps for path planning in high-dimensional configuration spaces. _IEEE transactions on Robotics and Automation_ , 12(4):566–580, 2002. 

- [32] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. _CoRR_ , abs/1412.6980, 2014. 

- [33] Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_ , 62(1):1–62, 2022. 

11 

- [34] Ian Lenz, Ross A Knepper, and Ashutosh Saxena. Deepmpc: Learning deep latent features for model predictive control. In _Robotics: Science and Systems_ , volume 10, page 25. Rome, Italy, 2015. 

- [35] Lingni Ma, Yuting Ye, Fangzhou Hong, Vladimir Guzov, Yifeng Jiang, Rowan Postyeni, Luis Pesqueira, Alexander Gamino, Vijay Baiyya, Hyo Jin Kim, Kevin Bailey, David Soriano Fosas, C. Karen Liu, Ziwei Liu, Jakob Engel, Renzo De Nardi, and Richard Newcombe. Nymeria: A massive collection of multimodal egocentric daily motion in the wild. In _the 18th European Conference on Computer Vision (ECCV)_ , 2024. URL `https://arxiv.org/abs/ 2406.09905` . 

- [36] Alessandro Macchelli, Claudio Melchiorri, and Stefano Stramigioli. Port-based modeling and simulation of mechanical systems with rigid and flexible links. _IEEE transactions on robotics_ , 25(5):1016–1029, 2009. 

- [37] Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, and Adrian Vladu. Towards deep learning models resistant to adversarial attacks, 2018. 

- [38] Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, and Randall Balestriero. Leworldmodel: Stable end-to-end joint-embedding predictive architecture from pixels, 2026. URL `https://arxiv.org/abs/2603.19312` . 

- [39] Felipe A Mejia, Paul Gamble, Zigfried Hampel-Arias, Michael Lomnitz, Nina Lopatina, Lucas Tindall, and Maria Alejandra Barrios. Robust or private? adversarial training makes models more vulnerable to privacy attacks. _arXiv preprint arXiv:1906.06449_ , 2019. 

- [40] MG Mohanan and Ambuja Salgoankar. A survey of robotic motion planning in dynamic environments. _Robotics and Autonomous Systems_ , 100:171–185, 2018. 

- [41] Anusha Nagabandi, Gregory Kahn, Ronald S Fearing, and Sergey Levine. Neural network dynamics for model-based deep reinforcement learning with model-free fine-tuning. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 7559–7566. IEEE, 2018. 

- [42] Anusha Nagabandi, K. Konolige, S. Levine, and Vikash Kumar. Deep dynamics models for learning dexterous manipulation. In _Conference on Robot Learning_ , 2019. URL `https: //arxiv.org/pdf/1909.11652.pdf` . 

- [43] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Hervé Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision, 2024. URL `https://arxiv.org/abs/2304.07193` . 

- [44] Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [45] Reuven Y Rubinstein and Dirk P Kroese. _The cross-entropy method: a unified approach to combinatorial optimization, Monte-Carlo simulation and machine learning_ . Springer Science & Business Media, 2004. 

- [46] Robin Schiewer, Anand Subramoney, and Laurenz Wiskott. Exploring the limits of hierarchical world models in reinforcement learning. _Scientific Reports_ , 14, 2024. URL `https://api. semanticscholar.org/CorpusId:270214472` . 

- [47] Michael D. Schmidt and Hod Lipson. Distilling free-form natural laws from experimental data. _Science_ , 324:81 – 85, 2009. URL `https://doi.org/10.1126/science.1165893` . 

- [48] Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

12 

- [49] Archit Sharma, Shixiang Shane Gu, Sergey Levine, Vikash Kumar, and Karol Hausman. Dynamics-aware unsupervised discovery of skills. _ArXiv_ , abs/1907.01657, 2019. URL `https: //api.semanticscholar.org/CorpusID:195791369` . 

- [50] Haochen Shi, Huazhe Xu, Zhiao Huang, Yunzhu Li, and Jiajun Wu. Robocraft: Learning to see, simulate, and shape elasto-plastic objects with graph networks. _ArXiv_ , abs/2205.02909, 2022. URL `https://api.semanticscholar.org/CorpusID:248562698` . 

- [51] Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani, and Giuseppe Oriolo. _Robotics: modelling, planning and control_ . Springer, 2009. 

- [52] Mark W Spong, Seth Hutchinson, and M Vidyasagar. Robot modeling and control. _John Wiley &amp_ , 2020. 

- [53] Richard S Sutton. Dyna, an integrated architecture for learning, planning, and reacting. _ACM Sigart Bulletin_ , 2(4):160–163, 1991. 

- [54] Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ , volume 1. MIT press Cambridge, 1998. 

- [55] Jyothir SV, Siddhartha Jalagam, Yann LeCun, and Vlad Sobal. Gradient-based planning with world models. _arXiv preprint arXiv:2312.17227_ , 2023. 

- [56] Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow, and Rob Fergus. Intriguing properties of neural networks. _arXiv preprint arXiv:1312.6199_ , 2013. 

- [57] Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, Timothy Lillicrap, and Martin Riedmiller. Deepmind control suite, 2018. URL `https://arxiv.org/abs/1801.00690` . 

- [58] Tsun-Hsuan Wang, Pingchuan Ma, A. Spielberg, Zhou Xian, Hao Zhang, J. Tenenbaum, D. Rus, and Chuang Gan. Softzoo: A soft robot co-design benchmark for locomotion in diverse environments. _ArXiv_ , abs/2303.09555, 2023. URL `https://api.semanticscholar.org/ CorpusId:257557557` . 

- [59] Grady Williams, Andrew Aldrich, and Evangelos A Theodorou. Model predictive path integral control: From theory to parallel computation. _Journal of Guidance, Control, and Dynamics_ , 40 (2):344–357, 2017. 

- [60] Grady Williams, Nolan Wagener, Brian Goldfain, P. Drews, James M. Rehg, Byron Boots, and Evangelos A. Theodorou. Information theoretic mpc for model-based reinforcement learning. _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1714– 1721, 2017. URL `http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber= 7989202` . 

- [61] Eric Wong, Leslie Rice, and J Zico Kolter. Fast is better than free: Revisiting adversarial training. In _International Conference on Learning Representations_ , 2020. 

- [62] Jie Xu, Viktor Makoviychuk, Yashraj S. Narang, Fabio Ramos, W. Matusik, Animesh Garg, and M. Macklin. Accelerated policy learning with parallel differentiable simulation. _ArXiv_ , abs/2204.07137, 2022. URL `https://api.semanticscholar.org/CorpusId: 248178090` . 

- [63] Xianyuan Zhan, Xiangyu Zhu, and Haoran Xu. Model-based offline planning with trajectory pruning. In _International Joint Conference on Artificial Intelligence_ , 2021. URL `https: //api.semanticscholar.org/CorpusId:234742314` . 

- [64] Kaifeng Zhang, Baoyu Li, Kris Hauser, and Yunzhu Li. Adaptigraph: Material-adaptive graphbased neural dynamics for robotic manipulation. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [65] Marvin Zhang, Sharad Vikram, Laura Smith, Pieter Abbeel, Matthew Johnson, and Sergey Levine. Solar: Deep structured representations for model-based reinforcement learning. In _International conference on machine learning_ , pages 7444–7453. PMLR, 2019. 

13 

- [66] Weichen Zhang, Lifeng Shang, and Antoni B. Chan. A robust likelihood function for 3d human pose tracking. _IEEE Transactions on Image Processing_ , 23(12):5374–5389, Dec 2014. doi: 10.1109/TIP.2014.2364113. PMID: 25347879. 

- [67] Wenbo Zhang, Karl Schmeckpeper, P. Chaudhari, and Kostas Daniilidis. Deformable linear object prediction using locally linear latent dynamics. _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13503–13509, 2021. URL `https: //api.semanticscholar.org/CorpusId:232380092` . 

- [68] Zongyuan Zhang, Tian dong Duan, Zheng Lin, Dong Huang, Zihan Fang, Zekai Sun, Ling Xiong, Hongbin Liang, Heming Cui, and Yong Cui. State-aware perturbation optimization for robust deep reinforcement learning. _ArXiv_ , abs/2503.20613, 2025. URL `https://api. semanticscholar.org/CorpusId:277322758` . 

- [69] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pre-trained visual features enable zero-shot planning, 2025. 

14 

## **A Related Work** 

**Learning world models from sensory data.** Learning-based dynamics models have become central to control and decision making, offering a data-driven alternative to classical approaches that rely on first principles modeling [18, 47, 36]. Early work focused on modeling dynamics in low-dimensional state-space [10, 34, 25, 49], while more recent methods learn directly from high-dimensional sensory inputs such as images. Pixel-space prediction methods [15, 28] have shown success in applications such as human motion prediction [15], robotic manipulation [14, 1, 65], and solving Atari games [28], but they remain computationally expensive due to the cost of image reconstructions. To address this, alternative approaches learn a compact latent representation where dynamics are modeled [29, 23, 50, 30]. These models are typically supervised either by decoding latent predictions to match ground truth observations [13, 67, 7, 26, 2, 23], or by using prediction objectives that operate directly in latent space, such as those in joint-embedding prediction architectures (JEPAs) [33, 5, 12, 20, 69]. Our work builds upon this latter category of world models and specifically leverages the DINOv2-based latent world models introduced in [69]. However, unlike prior work that primarily targets improving general representation quality or prediction accuracy, we focus on enhancing the trainability of world models to improve the convergence and reliability of gradient-based planning. 

**Planning with world models.** Planning with world models is challenging due to the non-linearity and non-convexity of the objective. Search-based methods such as CEM [45] and MPPI [59] are widely used in this context [60, 42, 23, 63, 69]. These methods explore the action space effectively, helping to escape from local minima, but typically scale poorly in high-dimensional settings due to their sampling-based nature. In contrast, gradient-based methods offer a more scalable alternative by exploiting the differentiability of the world model to optimize actions directly via backpropagation. Despite their efficiency, these methods suffer from local minima in highly non-smooth loss landscapes [6, 62, 8, 58], and gradient optimization can induce adversarial action sequences that exploit model inaccuracies [46, 27]. [69] have observed that GBP is particularly brittle when used with world models built on pre-trained visual embeddings, such as DINOv2 [43], often underperforming compared to CEM. To address these challenges, several stabilizing techniques have been proposed. For instance, random-sampling shooting helps mitigate adversarial trajectories by injecting noise in the action sequence and exploring a broader set of actions during trajectory optimization [41], and [68] introduce adversarial attacks on learned policies to make them robust to environmental perturbations by selectively perturbing state inputs at inference time. In contrast, we apply perturbation directly to latent states and latent actions during world model training. [16] add gradient penalties when training an implicit policy function to improve its smoothness and stabilize optimization, but their method does not involve training or using a world model. Other approaches aim to use a hybrid method that combines search and gradient steps to balance global exploration and local refinement [6]. In our work, we modify the world-model training procedure itself to improve GBP stability. In particular, through our Adversarial World Modeling approach, we enhance the robustness of the world model to perturbed states and actions, producing more stable and informative gradients that prevent adversarial action sequences at test time. 

## **B AWM Algorithm** 

## **C Experimental Details** 

### **C.1 Simulation Task Details** 

**PushT:** This task introduced by [9] uses an agent interacting with a T-shaped block to guide both the agent and block from a randomly initialized state to a feasible goal state within 25 steps. We use the dataset of 18500 trajectories given in [69], in which the green anchor serves purely as a visual reference. We draw a goal state from one of the noisy expert trajectories at 25 steps from the starting state. 

**PointMaze:** In this task introduced by [17], a force-actuated ball which can move in the _x, y_ Cartesian directions has to reach a target goal within a maze. We use the dataset of 2000 random trajectories present in [69], with a goal state chosen 25 steps from the starting state. 

15 

**Algorithm 3** Adversarial World Modeling (AWM) 

**Input:** Pretrained world model _fθ_ , dataset of trajectories _T_ , action perturbation scaling _λa_ , state perturbation scaling _λz_ , horizon _H_ , training iterations _N_ , minibatch size _B_ Initialize new trajectory dataset _T_<sup>_′_</sup> **for** _i_ = 1 _, . . . , N_ **do** Sample minibatch _τ ←{_ ( _zt_<sup>_j, a_</sup> _t_<sup>_j, z_</sup> _t_<sup>_j_</sup> +1<sup>)</sup> _t_<sup>_H_</sup> =1<sup>_}B_</sup> _j_ =1<sup>_∼T_</sup> _ϵa ← λa_ mean _j_ �std( _{a_<sup>_j_</sup> 1<sup>_, . . . , aj_</sup> _H_<sup>_}_)</sup> � _ϵz ← λz_ mean _j_ �std( _{z_ 1<sup>_j, . . . , z_</sup> _H_<sup>_j_</sup> +1<sup>_}_)</sup> � ( _αa, αz_ ) _←_ (1 _._ 25 _ϵa,_ 1 _._ 25 _ϵz_ ) _δa ∼_ Uniform( _−ϵa, ϵa_ ) _δz ∼_ Uniform( _−ϵz, ϵz_ ) **for** _t_ = 1 _, . . . , H_ **do** _∇δa , ∇δz ←∇δa,δz_ �� _fθ_ ( _zt_ + _δz, at_ + _δa_ ) _− zt_ +1��22 _δa ←_ clip( _δa_ + _αa_ sign( _∇δa_ ) _, −ϵa, ϵa_ ) _δz ←_ clip( _δz_ + _αz_ sign( _∇δz_ ) _, −ϵz, ϵz_ ) _a_<sup>_′_</sup> _t_<sup>_←at_+</sup><sup>_δa_</sup> _zt_<sup>_′←zt_+</sup><sup>_δz_</sup> **end for** _τ_<sup>_′_</sup> _←{_ ( _zt_<sup>_′j, a′_</sup> _t_<sup>_j, z_</sup> _t_<sup>_j_</sup> +1<sup>)</sup> _t_<sup>_H_</sup> =1<sup>_}B_</sup> _j_ =1 Train _fθ_ on next-state prediction using _τ_<sup>_′_</sup> **end for** 

**Wall:** This task introduced by DINO-WM [69] features a 2D navigation environment with two rooms separated by a wall with a door. The agent’s task is to navigate from a randomized starting location in one room to a random goal state in the other room, passing through the door. We use the dataset of 1920 trajectories as provided in DINO-WM, with a goal state chosen 25 steps from the starting state. 

**Reacher:** This is a continuous control task from the DeepMind Control Suite [57], where a 2-joint robotic arm aims to reach a target position in a fixed 2D plane. We use a dataset of 10000 trajectories of 200 steps each from [38], that were generated using an expert Soft Actor-Critic policy. 

**Rope:** In this task introduced by [64] a simulated Xarm must push a piece of rope into the goal orientation. We use the dataset of 1000 trajectories of 20 steps each provided in DINO-WM. 

**Granular:** In this task introduced by [64] a simulated Xarm must push around one hundred small particles into the goal configuration. We use the dataset of 1000 trajectories of 20 steps each provided in DINO-WM. 

Each of the tasks’ environment is illustrated in Figure 7. We reproduce the dataset statistics used to train the base world model for each environment from [69] as detailed in Table 1. 

Table 1: Trajectory datasets used to pretrain the base DINO-WM. 

|Environment|History|Frameskip|Dataset Size|Trajectory Length|
|---|---|---|---|---|
|Push-T|3|5|18500|100-300|
|PointMaze|3|5|2000|100|
|Wall|1|5|1920|50|
|Reacher|3|5|10000|200|
|Rope|1|1|1000|5|
|Granular|1|1|1000|5|


### **C.2 CEM Algorithm** 

We detail the cross-entropy method used in our planning experiments in Algorithm 4. 

16 


Figure 7: Illustrations of the six simulation tasks used in our experiments. Images from [69]. 

**Algorithm 4** Cross-Entropy Method (CEM) Planning **Input:** Current observation _o_ 0, goal observation _og_ , encoder Φ _µ_ , world model _fθ_ , horizon _H_ , population size _N_ , top-K selection _K_ , iterations _I z_ ˆ1 _←_ Φ _µ_ ( _o_ 1) _zg ←_ Φ _µ_ ( _og_ ) Initialize Gaussian distribution parameters: mean _µ_ 0, covariance Σ0 **for** _i_ = 1 _, . . . , I_ **do** Sample _N_ action sequences _{a_<sup>(</sup> 1:<sup>_j_</sup> _H_<sup>)</sup><sup>_}N_</sup> _j_ =1<sup>_∼N_(</sup><sup>_µi−_1</sup><sup>_,_Σ</sup><sup>_i−_1)</sup> **for** _j_ = 1 _, . . . , N_ **do** _z_ ˆ1<sup>(</sup><sup>_j_)</sup> _← z_ ˆ1 **for** _t_ = 2 _, . . . , H_ + 1 **do** _z_ ˆ _t_<sup>(</sup><sup>_j_)</sup> _← fθ_ (ˆ _zt_<sup>(</sup> _−_<sup>_j_)</sup> 1<sup>_, a_(</sup> _t−_<sup>_j_)</sup> 1<sup>)</sup> **end for** _C_<sup>(</sup><sup>_j_)</sup> _←∥z_ ˆ _H_<sup>(</sup><sup>_j_</sup> +1<sup>)</sup><sup>_−zg∥_2</sup> **end for** Select _K_ sequences with lowest cost: _E_ = _{a_<sup>(</sup><sup>_j_)</sup> _}_ top- _K µi ← K_<sup><u>1</u></sup> � _a∈E_<sup>_a_</sup> Σ _i ← K_<sup><u>1</u></sup> � _a∈E_<sup>(</sup><sup>_a −µi_)(</sup><sup>_a −µi_)</sup><sup>_⊤_</sup> **end for return** _µI_ as the final action sequence estimate _{a_ ˆ _t}_<sup>_H_</sup> _t_ =1 

### **C.3 Finetuning and Planning Hyperparameters** 

In Table 2, we list all shared hyperparameters used in training and planning. For all planning experiments we use 10 MPC iterations, taking the first _K_ = 1 actions at each iteration before replanning. For all simulator tasks, we use a horizon of _H_ = 5 actions. We provide data quantity and synthetic data parameters for our Online and Adversarial World Modeling training setups in Tables 3 and 4 respectively. In addition to maintaining perturbation radii for the visual latent and action embeddings, we use a distinct radius for the proprioceptive embeddings. We empirically find that the scales of the visual and proprioceptive embeddings are incompatible and semantically distinct, thereby necessitating independent perturbation. Throughout all of our experiments, we set the perturbation radii of the action embedding and proprioceptive embedding identically for simplicity. 

Table 2: We report **(a)** shared hyperparameters for OWM/AWM finetuning across all environments, **(b)** GBP parameters, and **(c)** CEM parameters. 

|(a) Finetuning P|arameters|(b) GBP||(c) CEM||
|---|---|---|---|---|---|
|Name|Value|Name|Value|Name|Value|
|Image size|224|Optimizer steps|100|Iterations|30|
|Optimizer|AdamW|LR|0.2|Number of Elites|30|
|Predictor LR|1e-5|Optimizer|Adam|Rollouts per Iteration|300|


17 

Table 3: Finetuning <u>parameters for Online World Modeling.</u> 

|**Environment**|**# Rollouts**|**Batch Size**|**GPU**|**Epochs**|
|---|---|---|---|---|
|PushT|6000|32|4x B200|1|
|PointMaze|500|32|4x B200|1|
|Wall|1920 (all)|80|4x B200|1|


Table 4: Training <u>parameters for Adversarial World Modeling.</u> 

|**Environment**|**# Rollouts**|**Batch Size**|**GPU**|**Epochs**|_ϵ_**visual**|_ϵ_**proprio**|_ϵ_**action**|
|---|---|---|---|---|---|---|---|
|PushT|20000 (all)|16|8x B200|1|0.05|0.02|0.02|
|PointMaze|2000 (all)|16|1x B200|1|0.20|0.08|0.08|
|Wall|1920 (all)|48|1x B200|2|0.20|0.08|0.08|
|Reacher|10000 (all)|32|1xA100|2|0.05|0.02|0.02|
|Rope|1000 (all)|16|1xRTX3080|1|0.05|0.02|0.02|
|Granular|1000 (all)|16|1xRTX3080|1|0.05|0.02|0.02|


### **C.4 Weighted Goal Loss** 

We use an exponentially weighted goal loss to improve progress in navigation-based tasks. Weighted Goal Loss (WGL) minimizes the distance between all latent states in the predicted rollout and the goal latent state, but weighted by an exponential weighting. Formally, 


where the sequence of normalized weights _{wi}_<sup>_H_</sup> 2<sup>+1</sup> is a hyperparameter choice. Empirically, we find that using this objective for Gradient-Based Planning either maintains or improves planning performance. For PointMaze and Wall, we found that exponentially upweighting later states in the planning horizon improved planning performance, so we set _wi_ = 2<sup>_i_</sup> . For PushT, we found that exponentially upweighting earlier states improved planning performance, so we set _wi_ = (1 _/_ 2)<sup>_i_</sup> . We leave the optimal selection of this sequence of weights as future work. 

### **C.5 Simulation Tasks Planning Results** 

In Table 5, we report mean planning performance across a total of 50 trajectories for each method and task. We calculate standard deviations using the averages of 3 batches of size 16. Exponential Chamfer Distance [66] is a bounded version (from 0 - 100) of the traditional chamfer distance, allowing us to measure the performance of Rope and Granular on the same scale as the other simulation tasks. 

Table 5: Planning <u>performance across simulation tasks and methods.</u> 

|**Environment**|**DINO-WM (GBP)**|**AWM (GBP)**|**OWM (GBP)**|**DINO-WM (CEM)**|
|---|---|---|---|---|
|PushT (SR)|76_±_9_._31|92_±_5_._55|76_±_8|92_±_2_._69|
|PointMaze (SR)|68_±_10_._52|98_±_2_._77|88_±_4_._65|92_±_5_._73|
|Wall (SR)|80_±_12|96_±_2_._86|80_±_11_._79|82_±_9_._62|
|Reacher (SR)|42_±_8_._87|76_±_4|-|66_±_7_._47|
|Granular (ECD)|74_._08_±_2_._96|78_._66_±_2_._36|-|80_._25_±_2_._41|
|Rope (ECD)|17_._73_±_3_._19|39_._46_±_4_._34|-|39_._46_±_6_._71|


## **D Visualizing the Optimization Landscape** 

We visualize the loss landscape of both the DINO World Model before and after applying the AWM and OWM objective. We perform a grid search over the subspace spanned by 

18 

1. _a_ ˆGBP-Pretrained: Gradient-Based Planning on original Dino World Model with 300 optimization steps of Adam with LR = 1e-3. We set a fixed initialization _a_ init. 

2. _a_ ˆGBP-Adversarial: Gradient-Based Planning on our Adversarial World Model (or Online World Model) with 300 optimization steps of Adam with LR = 1e-3. We use the same _a_ init as our initialization. 

3. _a_ GT: the ground-truth actions from the expert demonstrator. 

We define the axes as _α_ = ˆ _a_ GBP-Pretrained _− a_ GT and _β_ = ˆ _a_ GBP-Adversarial _− a_ GT, and compute the loss surface over a 50 _×_ 50 grid spanning _α, β ∈_ [ _−_ 1 _._ 25 _,_ 1 _._ 25]. 

The “Simulator” landscape is obtained by executing all interpolated action sequences in the groundtruth environment and computing the embedding-space loss; it validates that the basin near the origin is indeed low-loss and that the overall landscape shape is consistent across models. Since the interpolated actions become physically implausible far from the origin, the simulator landscape exhibits edge artifacts at extreme ( _α, β_ ) values. We reduce opacity beyond _|α|, |β| >_ 0 _._ 75 in the 3D surface plot for clarity. 

## **E Adversarial World Modeling: Design Decisions** 

### **E.1 Fast Gradient Sign Method (FGSM) vs. Projected Gradient Descent (PGD)** 

Projected Gradient Descent (PGD) has been used as an iterative method for generating adversarial perturbations [37]. At each step, PGD takes a gradient ascent step and projects the result onto the space of allowed perturbations (some ball with radius _ϵ_ around the input). Projection (Π) is typically via clipping or scaling. Formally, 


However, this is computationally expensive to use for adversarial training as it requires an additional backward pass for each iteration. If one uses a single-step, replaces the gradient by its sign, and uses step size _α_ = _ϵ_ , this recovers the well-known Fast Gradient Sign Method (FGSM) update [19]. 


In Wong et al. 61, the authors demonstrate that initializing _δ_ in the _ℓ∞_ -ball with radius _ϵ_ and performing FGSM adversarial training on these perturbations substantially improves robustness to PGD attacks and matches performance of PGD-based training. We leverage this observation to perform cheap adversarial training that only requires 2 _×_ the backward passes of traditional supervised learning. In comparison, _K_ -step PGD requires _K_ more backward passes (3 _×_ more for _K_ = 2 and 4 _×_ for _K_ = 3). In Table 6, we show that 2/3-Step PGD does not consistently outperform FGSM, despite requiring a much larger training budget. 

### **E.2 Scaling Factor (** _λ_ **) & Perturbation Radii (** _ϵ_ **) Ablations** 

To assess the robustness of Adversarial World Modeling to the scaling factor and perturbation radius hyperparameters, we conduct an ablation study varying these two factors, shown in Figure 8. We evaluate _λa, λz ∈_ [0 _._ 0 _,_ 0 _._ 02 _,_ 0 _._ 05 _,_ 0 _._ 20 _,_ 0 _._ 50 _,_ 1 _._ 0]<sup>2</sup> and either fix _ϵa, ϵp, ϵz_ to the standard deviation 

Table 6: Comparison between 2/3-Step PGD and FGSM demonstrating that FGSM has improved or only slightly subpar performance for significantly less training budget. 

|||**Poin**|**tMaze**|**W**|**all**|
|---|---|---|---|---|---|
||**Backward Passes**|**Min/Epoch**|**GBP SR(%)**|**Min/Epoch**|**GBP SR(%)**|
|FGSM|**2**|**120**|94|**14**|**94**|
|2-Step PGD|3|165|**96**|20|90|
|3-Step PGD|4|201|94|24|94|


19 


Figure 8: Success rate of GBP planning on an Adversarial World Model trained with scaling factors _λa, λz_ and perturbation radii _ϵa, ϵz_ on the Wall environment. We find that 0 _≤ λz, λa ≤_ 0 _._ 2 are stable for either “Fixed” or “Adaptive” perturbation radii. 

of the first minibatch (“Fixed") or recompute it for every minibatch (“Adaptive"). We observe no consistent improvement or degradation across any value of _λa_ , for 0 _≤ λz ≤_ 0 _._ 5, or between the “Fixed" or “Adaptive" perturbation radii. We note that setting the visual scaling factor _λz_ too high (e.g., 0 _._ 5 _,_ 1 _._ 0) can significantly degrade performance. We hypothesize that excessively large perturbations distort the semantic content of the visual latent state, pushing it outside the range of semantically equivalent representations. 

## **F Egocentric Body Pose Planning and Nymeria Dataset Details** 

Nymeria [35] is a large scale dataset of first-person videos and associated motion capture. The motion capture at a particular timestep is represented by a pose _pt_ , which consists of the 3D position of the pelvis and Euler angles for each joint. An action is defined as the change between two subsequent poses, namely the change in pelvis position and the Euler angles. With 15 joints, the action becomes 48 dimensional. To measure the quality of predicted actions we use Leaf Mean Joint Error (MJE). MJE is defined as 


“Leaf” indicates that _x_ ˆ only comes from the final predicted pose. 

We train DINO-WM on 2 epochs of a split containing half the Nymeria dataset, and perform AWM finetuning for 1 epoch on the same split. For CEM planning, we use 128 rollouts per iteration, 16 elites, and 10 iterations. For GBP planning, we use Adam, LR of 0.2, and 50 optimizer steps. 

## **G Comparison to LeWorldModel** 

LeWorldModel (LeWM) [38] is a latent world model that uses a SIGReg [4] regularization term to prevent trivial collapse by enforcing Gaussian-distributed latent states. In Table 7 we show how LeWM alone underperforms DINO-WM with AWM, and that LeWM benefits from AWM as well. For each environment, we finetune LeWM with a single epoch of AWM. 

20 

Table 7: GBP performance on PushT and Wall of LeWM and DINO-WM with and without AWM. The same planning setup is used for each architecture. 

|**Environment**|**DINO-WM**|**LeWM**|**LeWM + AWM**|**DINO-WM + AWM**|
|---|---|---|---|---|
|PushT (SR)|76_±_9_._31|72_±_6_._33|82_±_4_._68|92_±_5_._55|
|Wall (SR)|80_±_12_._02|74_±_4_._53|80_±_2_._37|96_±_2_._86|


21 

