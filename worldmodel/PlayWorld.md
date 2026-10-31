---
title: "PlayWorld: Learning Robot World Models from Autonomous Play"
date: "2026-03-09"
authors: "Tenny Yin; Zhiting Mei; Zhonghe Zheng; Miyu Yamane; David Wang; Jade Sceats"
url: https://arxiv.org/abs/2603.09030
pdf: https://arxiv.org/pdf/2603.09030
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.09030)** / [論文ページ](https://arxiv.org/abs/2603.09030)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**PlayWorld: Learning Robot World Models from Autonomous Play** 

**Tenny Yin**<sup>1</sup> , **Zhiting Mei**<sup>1</sup> , **Zhonghe Zheng**<sup>1</sup> , **Miyu Yamane**<sup>1</sup> , **David Wang**<sup>1</sup> , **Jade Sceats**<sup>1</sup> , **Samuel M. Bateman**<sup>1</sup> , **Lihan Zha**<sup>1</sup> , **Apurva Badithela**<sup>1</sup> , **Ola Shorinwa**<sup>1</sup> , **Anirudha Majumdar**<sup>1</sup> 

> 1Princeton University 

Action-conditioned video models offer a promising path to building general-purpose robot simulators that can improve directly from data. Yet, a critical question remains: _what data is needed to train them effectively?_ While existing models typically train on human-collected demonstrations or task-specific policy rollouts, we hypothesize that this leads to hallucinations caused by systematic biases and poor coverage of interaction dynamics. In contrast, we present _PlayWorld_ : a new data paradigm for training robot world models through _autonomous play_ . We demonstrate a pipeline for scalable (including overnight) unsupservised data collection, enabling broad coverage of complex, long-tailed physical interactions essential for modeling realistic object dynamics. Experiments across diverse manipulation tasks show that PlayWorld generates high-quality, physically consistent predictions for contact-rich interactions that are not captured by world models trained on human-collected data. We further demonstrate the versatility of PlayWorld in enabling fine-grained failure prediction and policy evaluation, with up to 40% improvements over human-collected data. Finally, we demonstrate how PlayWorld enables reinforcement learning in the world model, improving policy performance by 65% in success rates when deployed in the real world. To our knowledge, PlayWorld represents the first work to demonstrate autonomous play as an effective training paradigm for video world models. 

**Keywords: Video World Models, Autonomous Data Collection** 

**Website: robot-playworld.github.io** 


## **1 Introduction** 

Generative video models [1–4] hold tantalizing potential to serve as general-purpose data-driven simulators for robotics [5–7]. In principle, video models address some of the most critical challenges faced by traditional physics-based simulators by generating highly photorealistic outputs, simulating non-rigid-body interactions (e.g., deformable objects, liquids), providing a direct real-to-sim pipeline by conditioning video generation on images of real-world scenes, and affording the ability to close the sim-to-real gap by scaling data. An emerging line of work in robotics [8–14] seeks to reap these benefits by fine-tuning video generation backbones pre-trained on internet-scale data [1, 15] with robotics datasets, and using the resulting models for scalable data generation [8, 16–18], policy evaluation [9, 11, 14, 19], and planning [10, 13, 20]. 

Despite this progress, state-of-the-art video models remain far from reliable world simulators. While capable of generating physically consistent, photorealistic, and long-horizon rollouts in non-interactive scenes (e.g., autonomous driving [21, 22]), they remain vulnerable to hallucinations when simulating contact-rich interactions: from objects that duplicate when grasped, to ones that appear, disappear, or move and deform in unrealistic ways upon contact [3, 14, 23–29]. As a result, the use of video models in robotic manipulation has largely been restricted to tasks with minimal contact and focused around high-level language-following abilities [9, 14]. 

In this paper, we take a _data-centric perspective_ on training high-quality video models for robotic manipulation. Our core hypothesis is that the aforementioned challenges with simulating contact-rich dynamics stem from the data on which video models are trained or fine-tuned. In particular, existing action-conditioned video models for manipulation (e.g., [9, 11, 19]) are _almost exclusively trained on human demonstration datasets_ [30, 31] developed for imitation learning. This inherently limits data coverage to a narrow distribution of states focused along _successful_ task executions. As a result, this data provides video models with little supervision 

1 


**Figure 1** We introduce PlayWorld, a scalable framework for training high-fidelity video world models from autonomous robot play that enables fine-grained dynamics prediction for accurate policy evaluation, and online reinforcement learning policy fine-tuning that yields strong real-world success rate improvements. 

on complex contact dynamics and state transitions that counterfactual actions might introduce [32, 33]. Small prediction errors at critical contact events can thus compound quickly into qualitatively divergent policy rollouts which are often heavily biased towards successful executions seen in the data (Sec. 4). 

How can we obtain the most useful data for learning high-quality world models? From a data-centric standpoint, we argue that the right training corpus needs to (i) be generated through _directed exploration_ that continually expands coverage of diverse contact events, and (ii) support _efficient scaling_ , so exploration can grow naturally with minimal manual engineering or supervision. Inspired by work in developmental psychology [34, 35], we ask: can robots actively curate a diverse set of experiences for training high-quality video models through _autonomous play_ [36–38]? By interacting with objects in a semi-structured fashion without human supervision, autonomous play data can (i) induce broad coverage of relevant state transitions that might occur during policy execution, and (ii) be highly scalable in terms of both quantity and diversity of objects and scenes. These advantages make autonomous play a compelling data-collection framework for contact-rich world modeling. 

**Contributions.** We introduce _PlayWorld_ , a simple and scalable data paradigm for training robot world models based on autonomous play, demonstrating that broad, interaction-rich coverage is the key factor for learning accurate, hallucination-free dynamics. With this framework, we make the following contributions: 

- (1) Through careful empirical analysis, we show that PlayWorld produces substantially _broader coverage_ of interaction dynamics, generating significantly more diverse contact events, object states, and failure modes than human-collected data. 

- (2) By minimizing human intervention to occasional monitoring and scene resets, we demonstrate that PlayWorld enables highly _scalable_ data collection, including fully unsupervised overnight operation. 

- (3) Across a range of manipulation tasks, we show that PlayWorld enables simulation of _realistic physical interactions_ with fine-grained predictive accuracy, yielding significant gains on perceptual metrics and continues to improve with _scale_ , even beyond 5 _×_ the regime where performance saturates with human demonstration data. 

- (4) We demonstrate that PlayWorld supports effective post-training applications, including _fine-grained policy evaluation_ that strongly correlates with real-world performance, and _closed-loop RL fine-tuning_ that achieves up to 65% improvement in real-world success rates over the pre-trained policy. 

To our knowledge, PlayWorld is the _first_ work to establish the practicality and advantages of autonomous robot play data for training action-conditioned video models. 

2 

## **2 Related Work** 

### **2.1 World Models for Robotics** 

World models [39–41] learn predictive models of environment dynamics, enabling agents to reason and plan beyond purely reactive policies [42–44]. A large body of work in model-based reinforcement learning (RL) has demonstrated that large-scale interaction data with broad state-action coverage is necessary for training effective latent-space world models, which is often collected via on-policy or curiosity-driven exploration in simulation [42, 45–47]. However, achieving the same levels of scale via exploration in real-world environments is challenging, posing a major bottleneck to collecting diverse interaction data required for training generalizable models [48]. As a result, many robotic world models are trained from either manually collected on-policy roll-outs [10, 18, 49, 50] or large offline datasets [9, 14, 19, 51], which are challenging to scale on hardware and can be biased toward narrow behaviors, limiting their ability to model the dynamical effects of diverse actions [33]. We address this limitation by designing a system to collect large-scale exploratory interaction data on hardware, expanding coverage over states and actions for learning generalizable dynamics. 

### **2.2 Policy Evaluation and Improvement with Video Models** 

A growing body of work explores video generation models as embodied world models, leveraging large-scale pretraining for rich visual priors [1, 2] and pixel-space future prediction as a versatile interface across tasks, embodiments, and downstream objectives [6, 7, 20, 52]. This makes video models attractive for policy evaluation and improvement via world model rollouts, potentially reducing reliance on expensive real-world interaction. Prior work has primarily leveraged action-conditioned video prediction in two ways: (i) generating synthetic trajectories to augment training or fine-tuning [8, 9, 18, 53], and (ii) using imagined rollouts to score or optimize policies without repeated hardware trials [9, 11, 14, 19, 54–57]. However, the utility of these approaches is ultimately limited by their prediction fidelity under the policy-induced distribution [58]. In contact-rich robotic manipulation and high-DOF control, even small modeling errors can quickly lead to hallucinations in closed-loop rollouts, thereby resulting in inconsistent policy rankings and unstable reinforcement learning updates [59]. We address these limitations by developing an end-to-end system for scalable data collection and model training that prioritizes broad coverage of contact-rich interaction events, building a large, diverse corpus that approximates the outcome distribution induced by arbitrary policies. 

### **2.3 Leveraging Play Data in Robotics** 

Play data, which consists of unstructured, task-agnostic interactions with broad coverage of interaction modes beyond narrow expert demonstrations, has been explored in prior works to enable planning [36, 60, 61], representation learning [62–64], policy learning [37, 65–69], and finetuning pretrained models [70, 71]. Recent work has also leveraged play data at a smaller scale to train world models that support policy improvement [72]. These approaches typically require additional human-collected play demonstrations or policy rollouts that depend on manual supervision, which fundamentally limits scalability and the breadth of interaction diversity [36, 37]. In contrast, our work uses fully autonomous play data collection with generalist robot policies, enabling continuous, large-scale acquisition of diverse contact-rich interactions without supervision, transforming play data into a scalable resource for training high-fidelity world models. Most related to our work, SOAR [73] uses VLM-proposed tasks to autonomously collect data for improving language-conditioned policies In contrast, we use the collected play to learn a world model, converting finite real experience into effectively unlimited imagined interactions that can more flexibly support downstream policy applications. 

## **3 PlayWorld: Training Video World Models with Robot Play** 

We now introduce _PlayWorld_ , a framework for training action-conditioned video models that can predict diverse contact dynamics with fine-grained precision. In this section, we first formalize the world modeling problem as learning generalizable dynamics under distributional mismatch. Then, we introduce the design of our autonomous data collection system that can reliably collect hours of interaction data with no human supervision. Finally, we discuss model architecture and training designs that allow us to effectively learn from large quantities of heterogeneous interaction data. 

3 


**Figure 2 PlayWorld System Diagram.** Left: Autonomous data-collection pipeline in which the VLM and VLA iteratively propose and execute tasks. Right: Video world-model backbone and the setup for policy evaluation and fine-tuning. 

### **3.1 Generalizable Dynamics Learning through Play** 

Let _st ∈S_ denote the proprioceptive state of the robot, _at ∈A_ denote actions, and _ot_ = ( _o_<sup>1</sup> _t_<sup>_, . . . , oK_</sup> _t_<sup>)</sup><sup>_∈O_</sup> denote image observations corresponding to _K_ different views (e.g., multiple overhead cameras and a wrist camera) at time _t_ . We model the robot-environment dynamics using a stochastic action-conditioned video model: 


where _xt_ = ( _st, ot_ ). As highlighted in Sec. 2, prior work trains such models on human demonstration data, thereby optimizing predictive accuracy only under the visitation distribution ( _x_ 1: _t, a_ 1: _t, xt_ +1) _∼_ Dexp induced by the expert. As a result, the learned dynamics can suffer from distributional bias when queried under new policies and collapse to predictions that are likely under Dexp [32, 74]. In contrast, our goal is to train a video model that remains accurate across a broad range of policies. 

In order to achieve this, we expand the visitation distribution of the training data through data collected under a language-conditioned policy _π_ play( _a|x, ℓ_ ), where _ℓ ∈L_ denotes a natural language instruction. By generating highly diverse language instructions in a broad range of initial conditions encountered during autonomous roll-outs, this policy yields a set: 


that can better approximate visitation distributions induced by a wide range of policies. 

### **3.2 Autonomous Robot Play Data Collection** 

Next, we discuss a practical instantiation of _π_ play that can enable reliable and continuous autonomous data collection on hardware. In order to obtain useful and scalable play data, we outline three key design requirements: 

1. The robot needs to engage in _diverse interaction_ with objects in the scene (in order to obtain meaningful coverage as data collection expands) 

2. The system must _reliably_ prevent and recover from potential failures when human supervision is unavailable 

3. The system should be amenable to diverse objects and _generalize_ to diverse language instructions _ℓ_ without requiring manual engineering 

Building on these requirements, we develop a practical system atop the DROID manipulation setup [31] that requires no additional hardware modifications and supports up to eight hours of continuous, fully autonomous data collection. As illustrated in Fig. 2, our system is composed of two interacting components: a _task_ 

4 

_proposer_ that generates tasks to engage the robot in meaningful interactions with objects, and a _task executer_ that performs the task to generate interaction data. 

**Task Proposer.** We instantiate the proposer using a vision–language model (VLM) [75] that generates diverse, scene-grounded instructions from the robot’s current image observation(s) _ot_ . At the start of each episode, the VLM is prompted to produce a natural-language instruction _ℓ_ (e.g., “push the object forward” or “stack the object”). To promote data diversity while preserving executability, we prompt the VLM to add small perturbations to nominal commands (e.g., alternative verbs or object descriptions) to probe different behavior modes. Compared to novelty- or uncertainty-driven on-policy exploration, our language-conditioned play requires no reward design or auxiliary training, and generates semantically grounded diversity by varying task intent (rather than injecting action noise), yielding visitation distributions that better match test-time policy behavior. More details on implementation and example prompts can be found in Appendix A. 

**Task Executer.** We use a vision–language–action (VLA) policy [76] as the executer that can be conditioned on arbitrary natural-language instructions. While it succeeds on nominal commands (e.g., “pick up the object”), small perturbations in the instruction such as verb choice or unfamiliar object descriptions often lead to large variances in policy behavior [77]. We exploit this as a source of diversity: during long-horizon autonomous roll-outs, we intentionally randomize instructions under naturally-induced varied initial object poses, boosting the diversity of contact dynamics modes for interaction-rich data collection. 

**Safety Filter and Resets.** To enable reliable unsupervised execution for long periods of time, we utilize a lightweight safety filter that constrains the robot to operate within conservative workspace limits. Specifically, we enforce per-joint limits to prevent drastic motions, and prompt the VLM to detect when any object is drifting towards the boundary of the robot’s reachability limit, to instruct the VLA to “reset” the scene by retrieving that object back to the reachable workspace. Since the setup is task/object-agnostic, during play data collection involving large number of objects (such as in Sec. 4.6), we can simply add or remove arbitrary objects during collection. This simple design works well in practice and allows us to collect data for long durations including overnight. 

### **3.3 Model Architecture and Training** 

Finally, we discuss our choice of world model architecture and a curriculum-based training scheme for learning from uncurated interaction data. 

**Video Model Architecture.** Given the dataset _D_ play, our goal is to train a world model that produces high-fidelity visual outputs that simulate fine-grained interactions with the environment. Following [9], we adopt a pre-trained stable video diffusion (SVD) backbone [15] with factorized spatial and temporal attention, allowing us to inject fine-grained per-frame action conditioning to disentangle motion signals from frame appearances for strong controllability. We train our model to jointly predict three camera views to minimize the influence of partial observability, similar to [10, 14], and initialize our model with weights pre-trained on the DROID dataset [31]. Then, we fine-tune the world model on the play dataset _D_ play using the diffusion loss function: 


where **_ϵ_** _∼N_ (0 _,_ **_I_** ). We train the full PlayWorld model on 8x H200 GPUs with batch size of 64 for two days. 

**Curriculum Learning.** As we scale up play data collection to increase coverage of diverse states and transitions, the resulting dataset introduces two challenges: (1) high redundancy, where the majority of data are dominated by very similar transitions, and (2) multi-modality, where there also exists many rarely-occurring transitions that exhibits strong diversity (long-tail) [37]. This unbalanced and long-tailed distribution makes learning with standard training procedures difficult, causing models to easily overfit to simple patterns while failing to capture rare interactions [78, 79]. 

To enable a more balanced exposure, we adopt a curriculum learning setup [80, 81] to feed training data into the model in order of (auto-rated) “difficulty”: initializing with frequently occurring free space motions and static contacts, and gradually biasing sampling towards rare, harder-to-learn interactions. Concretely, suppose we are given a small set of human-collected demonstrations _D_ exp = _{τi}i_<sup>_N_</sup> =1<sup>_s_,whereeachtrajectory</sup> 

5 

**Table 1** Per-category perceptual similarity metrics on interaction-centric benchmark. PlayWorld improves prediction quality on contact-rich failure modes, with further gains from scaling and curriculum learning. 

|**Training Mix**|Succ|ess|Missed|Grasp|Sli|de|Sli|p|Deform|ation|Colli|sion|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||LPIPS|SSIM|LPIPS|SSIM|LPIPS|SSIM|LPIPS|SSIM|LPIPS|SSIM|LPIPS|SSIM|
|Human Demo (6h)|0.084|0.867|0.080|0.875|0.090|0.850|0.090|0.865|0.108|0.820|0.086|0.852|
|Human Play (6h)|0.086|0.861|0.071|0.869|0.089|0.864|0.088|0.867|0.100|0.831|0.080|0.873|
|Robot Play (6h)|0.082|0.870|0.066|0.883|0.077|0.865|0.078|0.871|0.099|0.831|0.074|0.888|
|Robot Play (30h)|0.071|0.873|0.064|0.887|0.073|0.876|0.072|0.879|0.094|0.833|0.076|0.883|
|Robot Play (Curriculum)|0.070|0.880|0.066|0.890|0.071|0.890|0.070|0.884|0.093|0.836|0.072|0.893|


**Figure 3** Illustration of each test category from the interaction-centric benchmark in Table 1. 

_τ_ = _{_ ( _xt, at_ ) _}_<sup>_T_</sup> _t_ =1<sup>correspondstosuccessfultaskexecution.Let</sup><sup>_D_play=</sup><sup>_{τ_˜</sup><sup>_j}N_</sup> _j_ =1<sup>_p_denoteuncuratedand</sup> unlabeled play data collected using the protocol from Sec. 3.2. Let _f_ clip( _·_ ) denote a frozen CLIP [82] image encoder. For each observation _ot_ , we compute an embedding 


We first extract a set of representative _success centroids_ from _D_ exp using all embeddings from success trajectories, _Z_ succ = _{zt | ot ∈D_ succ _}_ , and then apply _K_ -means clustering to obtain centroids _C_ = _{ck}_<sup>_K_</sup> _k_ =1<sup>_,_</sup> _ck ∈_ R<sup>_d_</sup> . These centroids serve as prototypes of task-relevant transitions observed in successful executions. For each observation _o_ in _D_ play, we define its _distance-to-success_ score as 


Intuitively, smaller values of _d_ ( _o_ ) indicate transitions that are visually and semantically closer to successful trajectories, while larger values correspond to less task-relevant or exploratory interactions. We then induce a curriculum by partitioning _D_ play into _R_ disjoint ranks based on this distance: 


where _{δr}_<sup>_R_</sup> _r_ =0<sup>aredistancethresholdschosensuchthat</sup><sup>_δ_0=0and</sup><sup>_δR_=+</sup><sup>_∞_.Lowerrankscorrespondto</sup> samples that are closer to success trajectories, while higher ranks contain increasingly out-of-distribution interactions. During training, we progressively expand the sampling distribution over ranks, starting from lower _r_ and gradually incorporating higher-ranked samples. This curriculum mitigates redundancy in free-space motion and counteracts the long-tailed distribution of critical interaction dynamics, enabling the model to learn rare but essential transitions more effectively. 

## **4 Experiments** 

In this section, we design experiments to explore the following questions: 

1. Does PlayWorld induce more diverse object interactions compared to human-collected data (Sec. 4.2)? 

2. Can PlayWorld improve video prediction accuracy for diverse object interactions compared to models trained on human demonstration data (Sec. 4.3)? 

3. Can PlayWorld enable fine-grained policy evaluation by reliably predicting outcomes across a broad range of policies and tasks (Sec. 4.4)? 

6 

4. Can PlayWorld enable policy fine-tuning through interactive roll-outs in the video model (Sec. 4.5)? 

5. Does PlayWorld result in improved accuracy and generalization with data scale compared to humancollected data (Sec. 4.6)? 

### **4.1 Experiment Setup** 

**Evaluation Setup.** To evaluate whether PlayWorld can produce more accurate dynamics predictions under realistic settings where object interactions are diverse and contact-rich, we carry out experiments on three distinct object sets featuring objects with different physical properties and interaction behaviors, each with a collection of possible tasks: 

- Set 1: Bowl, carrot, polar bear (put the carrot/polar bear into/out of the bowl) 

- Set 2: Rectangular block and cube (stack/unstack the block on top of the cube) 

- Set 3: Towel (fold/unfold towel) 

For our method (PlayWorld), we follow Sec. 3.2 to collect a total of 30 hours of task-agnostic autonomous robot play data containing diverse robot-object interactions combined across all 3 object sets. 

**Baselines.** We collect two types of teleoperation data as baselines: _human demo_ data consisting of task-specific expert demonstrations, and _human play_ data where the operator is instructed to freely interact with given objects in a task-agnostic manner. In total, we collect 6 hours of human demo data on the identical setup as robot play data. We initialize all models from the DROID-pretrained checkpoint in [9]. Our _human demo_ baseline corresponds to the standard demonstration-only fine-tuning paradigm (as in [9, 19]) designed in particular for our environment, enabling a controlled comparison that isolates the effect of interaction data. 

### **4.2 Does PlayWorld Induce Diverse Interactions?** 

First, we evaluate if PlayWorld can induce more diverse interactions with objects compared to humancollected data, as outlined in Sec. 3.1. For this comparison, we analyze a subset of autonomous play data alongside the _human demo_ and _human play_ baselines from object set 1 (Sec. 4.1) and provide a t-SNE visualization [83] on CLIP embeddings of the image observations. To better interpret the embedding space, we let a human annotator inspect the corresponding video snippet for each data point and assigns it to a coarse, human-interpretable interaction mode when applicable. As shown in Fig. 4, autonomous play exhibits substantially broader behavioral coverage, capturing diverse contact-rich events that are consistent with human annotations (e.g., missed grasps, collisions, and slips). In contrast, human-collected data forms a more concentrated cluster that largely reflects successful transitions. More results on conducting data clustering at larger scales can be found in Appendix B. 


**Figure 4 t-SNE analysis of training samples** . Robot play data exhibits markedly broader behavioral coverage than human-collected trajectories. Colors indicate coarse interaction modes assigned by a human annotator. 

### **4.3 Can PlayWorld Accurately Predict Contact Dynamics?** 

Next, we evaluate if the PlayWorld’s broader data coverage enables training better video world models for predicting challenging object dynamics. To this end, we construct an interaction-centric benchmark with 500+ clips sampled from roll-outs generated by a diverse collection of 20+ robot policies, categorized into 6 behavior modes by human annotators (Fig. 3), containing both successful task executions and common failure modes that are critical in determining policy behavior. Given a short ground-truth observation–state 

7 


**Figure 5 PlayWorld faithfully captures fine-grained dynamic behaviors.** PlayWorld’s predictions closely match fine-grained dynamic interaction modes in the real-world, such as missed grasps, collisions, deformations, and slips. 

trajectory as conditioning input, we roll out the ground-truth actions in the world model and compare the generated vs. ground-truth future frames using visual metrics such as LPIPS [84] and SSIM [85] (results on other visual metrics can be found in Appendix C). 

As shown in Table 1, while the prediction quality for successful interactions is similar across different training mixtures, PlayWorld provides consistent improvements for other dynamic interactions. In addition, scaling PlayWorld data from 6h to 30h further boosts performance. Notably, curriculum learning offered substantial advantage in improving prediction quality for more dynamic interactions, given the same training data. Fig. 5 provides some example predictions when rolling out a given action sequence from the ground-truth trajectory under different world models; we observe that predictions from the baseline methods often collapse to behaviors biased by the training data, with “hallucinated success” being the most common failure mode. 

### **4.4 Can PlayWorld Predict the Performance of Different Policies?** 

While high-level policy capabilities such as instruction following are relatively easy to assess, evaluating finegrained visuomotor abilities is substantially harder: small errors in contact timing, object position, or contact forces can lead to qualitatively different outcomes during closedloop execution. To rigorously test whether PlayWorld can faithfully predict policy performance, we construct a diverse suite of 18 policies by (i) training diffusion policies (DPs) [86] from scratch and (ii) fine-tuning _π_ 0 [87] using human demonstrations that vary in both quantity and quality. This produces policies spanning a wide range of success rates and exhibiting diverse failure modes (Fig. 6), providing a sensitive probe of whether a world model captures subtle contact-rich dynamics under realistic settings. 


**Figure 6** PlayWorld ’s predicted policy outcome distribution matches closely with real-world behavior. 

For each policy, we perform 20 real-world experiments and 50 simulated experiments in each world model. 

8 


**Figure 7 Policy Evaluation Success Rate (SR) Correlation.** Across diverse policies (architectures, training mixtures, and tasks), PlayWorld ’s predicted success rates are most strongly correlated with observed success rates and show the lowest variability. 


**Figure 8 Example Policy Interaction with different World Models.** We provide closed-loop rollouts with two example policies to demonstrate how hallucinated success can impact prediction outcomes. 

As shown in Fig. 7, PlayWorld generalizes well to a broad family of policies with substantially different success rates and behaviors (despite training on roll-outs collected form a single autonomous play policy). Predicted success rates from PlayWorld are strongly correlated with real-world success rates (Pearson correlation: 0.8766). In contrast, baseline models are only capable of capturing a narrow set of failure modes. When policies induce interaction patterns that are underrepresented in their training distributions, baseline models tend to either regress toward familiar outcomes or generate unrealistic dynamics with noticeably degraded visual quality (Fig. 8), leading to large discrepancies between predicted and observed success rates. In particular, we find that human play data yields the worst performance and often produces blurry predictions, which suggests that out-of-distribution diversity that doesn’t match well with policy behavior could hurt performance. 

Beyond aggregate success rates, we further assess whether PlayWorld can produce meaningful predictions of both success and failure by comparing human-annotated failure modes for each set of experiments. In Fig. 6, we present real and predicted failure-mode distributions for several representative policies and find that PlayWorld’s predicted distributions broadly align with empirical outcomes, whereas the behavior within the baseline models have large variances. 

### **4.5 Policy Fine-Tuning in the World Model** 

Many reinforcement learning fine-tuning algorithms can substantially improve policy robustness, but are seldom deployed on physical robots because real-world interaction is expensive, safety-limited, and slow to 

9 

run. While many existing video world models are used to optimize policies by generating synthetic data for supervised fine-tuning [8, 88, 89], here we show that with high dynamics prediction quality, PlayWorld can effectively support in-model RL fine-tuning that confers substantial gains in real-world deployment with minimal sim-to-real gap, making real-world RL more practical and scalable. 

To support stable fine-tuning, we adopt Diffusion Steering via Reinforcement Learning (DSRL) from [90], which freezes the base diffusion policy and instead learns a lightweight latent-noise policy _π_<sup>_w_</sup> that samples the initial diffusion noise _w_ (replacing _w ∼N_ (0 _, I_ )) to steer the resulting action _a_ = _πdp_<sup>_W_(</sup><sup>_s, w_) toward higher reward,</sup> while avoiding unstable backpropagation through the multi-step denoising chain. We train a simple progress-based reward function on small amounts of demonstration data, and compute the difference in predicted progress at each frame as dense rewards. Despite the simplistic setup, we observe surprisingly effective fine-tuning results. Fig. 9 summarizes our results on performing fine-tuning over two example tasks. Starting from a base diffusion policy trained with fewer than 10 demonstrations, performing online fine-tuning fully within PlayWorld improves real-world success rates by up to 65%, compared to fine- 


**Figure 9 Fine-tuning Experiment Results.** PlayWorld-finetuned policy demonstrates improved success rates and learns robust recovery behaviors beyond seen demonstrations. 

tuning in the baseline video model. In particular, we find that the fine-tuned model performs much more robustly on out-of-distribution initializations (including ones unseen during fine-tuning) and learns subtle recovery behaviors like scooping, as illustrated at the bottom of Fig. 9. In contrast, the baseline model trained on demonstrations offers less significant improvements and becomes unstable as the policy tries to “hack” the world model when failure modes are incorrectly identified, resulting in decrease in real-world success rates. We present more detailed findings in the Appendix D. 

### **4.6 Scaling and Generalization** 

Finally, we evaluate whether PlayWorld delivers sustainable, scalable data collection for world-model learning by measuring continued performance gains as we increase _data scale_ and _object diversity_ . 

**Data Scaling.** While scaling up data might appear to be a straightforward recipe for training better models, we show that the effectiveness of scaling depends strongly on data coverage. As shown in Fig. 10, the video model trained with PlayWorld continues to improve on visualquality metrics as we scale the dataset up to 30 hours. By contrast, baseline models show only marginal gains at comparable scale. This divergence highlights a central advantage of autonomous play: rather than repeatedly sampling narrow, success-focused trajectories, play data expands coverage over contact events, failure modes, and counterfactual transitions. As a result, additional data meaningfully broadens the learned dynamics model instead of reinforcing existing biases. These results suggest that PlayWorld supports effective scaling, where increased data directly translates into improved generalization. 


**Figure 10** Scaling behavior for world models trained with different data mixtures. 

10 


|**Objects**|**Fr**|**uit**|**Blo**|**cks**|
|---|---|---|---|---|
||LPIPS _↓_|SSIM _↑_|LPIPS _↓_|SSIM _↑_|
|0%|0.0991|0.8333|0.0978|0.8501|
|33%|0.0794|0.8612|0.0713|0.8810|
|66%|0.0761|0.8697|0.0684|0.8853|
|100%|0.0705|0.8757|0.0640|0.8948|


**Figure 11 Object Generalization Results.** We observe strong improvements in prediction quality of interaction with unseen objects as we include more diverse items in the training data. 

**Object Generalization.** We next test whether increasing object diversity in the training corpus improves transfer to unseen objects. As shown in Fig. 11, as we increase the fraction of training objects from 0% to 100%, prediction quality improves consistently on held-out objects across both test categories, despite substantial shifts in appearance and geometry. This suggests that PlayWorld learns dynamics that transfer across object instances, rather than memorizing object-specific visual features. We attribute this generalization to PlayWorld’s ability to scale object diversity while still inducing rich contact interactions during play, providing supervision on shared interaction patterns (e.g., contact, slip, deformation) that recur across different objects. 

## **5 Conclusion** 

We present PlayWorld, an efficient, autonomous, and scalable pipeline for training high-fidelity actionconditioned video world models on interaction-rich robot play data. By collecting large volumes of diverse experience autonomously (including unattended overnight operation), PlayWorld yields broader coverage of contact events and a richer learning signal than success-biased demonstrations. The resulting video world model achieves strong dynamics fidelity on both nominal and off-nominal interactions, enabling reliable fine-grained policy evaluation and in-model RL fine-tuning. Finally, we observe continued gains with increased data scale and object diversity, suggesting a practical path toward high-quality robot simulators that support policy evaluation and improvement beyond hardware constraints. 

## **6 Limitations and Future Work** 

**Improving Data Collection.** While PlayWorld can generate many diverse interaction data at scale, the current collection strategy does not explicitly optimize for sample efficiency and can produce redundant trajectories. Future work could explore better active data collection strategies that prioritize high uncertainty or underrepresented interactions that can further reduce hallucinations and improve physical consistency. Additionally, the current system relies on the availability of a sufficiently capable play policy; designing specialized or adaptive play policies that explicitly target rare contact events could further enhance coverage and efficiency. 

**Dynamic Discrepancies.** Despite significant improvements, PlayWorld does not eliminate hallucinations entirely. Prediction errors can still arise from open-loop rollout discrepancies, fixed action horizons, and mismatches between the control modes used during data collection and policy evaluation, which can accumulate over long horizons and degrade closed-loop stability. Future work could investigate more flexible prediction horizons, hierarchical or receding-horizon rollouts, and tighter integration between action conditioning and control representations to better align imagined dynamics with real-world execution. 

**Scaling Up.** While we demonstrate strong scaling trends within our experimental setup, extending PlayWorld beyond a controlled lab environment remains an open challenge. Scaling to more diverse objects, scenes, robot embodiments, and real-world settings will require improved strategies for learning from increasingly heterogeneous data distributions. As data scale increases, improved curriculum design and data balancing 

11 

mechanisms will become even more important; developing principled methods for automatically defining curriculum that optimize both prediction fidelity and robustness to long-tail interactions remains a key direction for future work. Efficiently leveraging large-scale, multi-robot datasets and potentially incorporating non-robot video data for broader physical priors also presents exciting opportunities. 

Overall, we believe that PlayWorld showcases the promise of scaling autonomous play data for training high-fidelity world models that can serve as general-purpose simulators for policy evaluation and reinforcement learning. 

## **Acknowledgments** 

Apurva Badithela is supported by the Presidential Postdoctoral Research Fellowship at Princeton University. Samuel M. Bateman is supported by the National Science Foundation CISE Graduate Fellowships under Grant No. 2313998. The authors were partially supported by Apple Inc. and the NSF CAREER Award #2044149. Any views, opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and should not be interpreted as reflecting the views, policies or position, either expressed or implied, of Apple Inc and the National Science Foundation. 

12 

## **References** 

- [1] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 1, 3 

- [2] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 3 

- [3] DeepMind. Veo-3: A text-to-video generation system with audio. Technical Report Tech Report, DeepMind / Google, 2025. 1 

- [4] Weijie Kong, Qi Tian, Zijian Zhang, Rox Min, Zuozhuo Dai, Jin Zhou, Jiangfeng Xiong, Xin Li, Bo Wu, Jianwei Zhang, et al. Hunyuanvideo: A systematic framework for large video generative models. _arXiv preprint arXiv:2412.03603_ , 2024. 1 

- [5] Siqiao Huang, Jialong Wu, Qixing Zhou, Shangchen Miao, and Mingsheng Long. Vid2world: Crafting video diffusion models to interactive world models, 2025. 1 

- [6] Google DeepMind. Genie 3: A New Frontier for World Models. Google DeepMind Blog, aug 2025. 3 

- [7] Zhiting Mei, Tenny Yin, Ola Shorinwa, Apurva Badithela, Zhonghe Zheng, Joseph Bruno, Madison Bland, Lihan Zha, Asher Hancock, Jaime Fern´andez Fisac, et al. Video generation models in robotics-applications, research challenges, future directions. _arXiv preprint arXiv:2601.07823_ , 2026. 1, 3 

- [8] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 1, 3, 10 

- [9] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 1, 3, 5, 7, 19 

- [10] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 1, 3, 5 

- [11] Yaxuan Li, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025. 1, 3 

- [12] Yao Feng, Hengkai Tan, Xinyi Mao, Chendong Xiang, Guodong Liu, Shuhe Huang, Hang Su, and Jun Zhu. Vidar: Embodied video diffusion model for generalist manipulation. _arXiv preprint arXiv:2507.12898_ , 2025. 

- [13] Junbang Liang, Pavel Tokmakov, Ruoshi Liu, Sruthi Sudhakar, Paarth Shah, Rares Ambrus, and Carl Vondrick. Video generators are robot policies. _arXiv preprint arXiv:2508.00795_ , 2025. 1 

- [14] Gemini Robotics Team, Krzysztof Choromanski, Coline Devin, Yilun Du, Debidatta Dwibedi, Ruiqi Gao, Abhishek Jindal, Thomas Kipf, Sean Kirmani, Isabel Leal, Fangchen Liu, Anirudha Majumdar, Andrew Marmon, Carolina Parada, Yulia Rubanova, Dhruv Shah, Vikas Sindhwani, Jie Tan, Fei Xia, Ted Xiao, Sherry Yang, Wenhao Yu, and Allan Zhou. Evaluating Gemini robotics policies in a Veo world simulator, 2025. 1, 3, 5 

- [15] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets, 2023. 1, 5 

- [16] Junbang Liang, Ruoshi Liu, Ege Ozguroglu, Sruthi Sudhakar, Achal Dave, Pavel Tokmakov, Shuran Song, and Carl Vondrick. Dreamitate: Real-world visuomotor policy learning via video generation. _arXiv preprint arXiv:2406.16862_ , 2024. 1 

- [17] Shivansh Patel, Shraddhaa Mohan, Hanlin Mai, Unnat Jain, Svetlana Lazebnik, and Yunzhu Li. Robotic manipulation by imitating generated videos without physical demonstrations. _arXiv preprint arXiv:2507.00990_ , 2025. 

- [18] Yanjiang Guo, Tony Lee, Lucy Xiaoyang Shi, Jianyu Chen, Percy Liang, and Chelsea Finn. Vlaw: Iterative co-improvement of vision-language-action policy and world model, 2026. 1, 3 

13 

- [19] Julian Quevedo, Ansh Kumar Sharma, Yixiang Sun, Varad Suryavanshi, Percy Liang, and Sherry Yang. Worldgym: World model as an environment for policy evaluation, 2025. 1, 3, 7 

- [20] Boyuan Chen, Tianyuan Zhang, Haoran Geng, Kiwhan Song, William T. Freeman, Jitendra Malik, Russ Tedrake, Vincent Sitzmann, and Yilun Du. Large video planner enables generalizable robot control, 2025. 1, 3 

- [21] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving, 2023. 1 

- [22] Xuanchi Ren, Tianchang Shen, Jiahui Huang, Huan Ling, Yifan Lu, Merlin Nimier-David, Thomas M¨uller, Alexander Keller, Sanja Fidler, and Jun Gao. Gen3c: 3d-informed world-consistent video generation with precise camera control. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 1 

- [23] Emily Denton and Rob Fergus. Stochastic video generation with a learned prior. In _International conference on machine learning_ , pages 1174–1183. PMLR, 2018. 1 

- [24] Shaowei Liu, Zhongzheng Ren, Saurabh Gupta, and Shenlong Wang. Physgen: Rigid-body physics-grounded image-to-video generation. In _European Conference on Computer Vision_ , pages 360–378. Springer, 2024. 

- [25] Rick Akkerman, Haiwen Feng, Michael J Black, Dimitrios Tzionas, and Victoria Fern´andez Abrevaya. Interdyn: Controllable interactive dynamics with video diffusion models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 12467–12479, 2025. 

- [26] Bo Ai, Stephen Tian, Haochen Shi, Yixuan Wang, Tobias Pfaff, Cheston Tan, Henrik I Christensen, Hao Su, Jiajun Wu, and Yunzhu Li. A review of learning-based dynamics models for robotic manipulation. _Science Robotics_ , 10(106):eadt1497, 2025. 

- [27] Hritik Bansal, Zongyu Lin, Tianyi Xie, Zeshun Zong, Michal Yarom, Yonatan Bitton, Chenfanfu Jiang, Yizhou Sun, Kai-Wei Chang, and Aditya Grover. Videophy: Evaluating physical commonsense for video generation. _arXiv preprint arXiv:2406.03520_ , 2024. 

- [28] Zhiting Mei, Ola Shorinwa, and Anirudha Majumdar. How confident are video models? Empowering video models to express their uncertainty. _arXiv preprint arXiv:2510.02571_ , 2025. 

- [29] Zhiting Mei, Tenny Yin, Micah Baker, Ola Shorinwa, and Anirudha Majumdar. World models that know when they don’t know: Controllable video generation with calibrated uncertainty. _arXiv preprint arXiv:2512.05927_ , 2025. 1 

- [30] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 1 

- [31] Alexander Khazatsky et al. Droid: A large-scale in-the-wild robot manipulation dataset, 2025. 1, 4, 5 

- [32] Chaochao Lu, Biwei Huang, Ke Wang, Jos´e Miguel Hern´andez-Lobato, Kun Zhang, and Bernhard Sch¨olkopf. Sample-efficient reinforcement learning via counterfactual-based data augmentation. _arXiv preprint arXiv:2012.09092_ , 2020. 2, 4 

- [33] Silviu Pitis, Elliot Creager, and Animesh Garg. Counterfactual data augmentation using locally factored dynamics. _Advances in Neural Information Processing Systems_ , 33:3976–3990, 2020. 2, 3 

- [34] Justine E. Hoch, Sinclaire M. O’Grady, and Karen E. Adolph. It’s the journey, not the destination: Locomotor exploration in infants. _Developmental Science_ , 22(2):e12740, March 2019. doi: 10.1111/desc.12740. Epub 2018 Oct 8. 2 

- [35] Deena Skolnick Weisberg, Kathy Hirsh-Pasek, Roberta Michnick Golinkoff, Audrey K. Kittredge, and David Klahr. Guided play: Principles and practices. _Current Directions in Psychological Science_ , 25(3):177–182, 2016. doi: 10.1177/0963721416645512. 2 

- [36] Corey Lynch, Mohi Khansari, Ted Xiao, Vikash Kumar, Jonathan Tompson, Sergey Levine, and Pierre Sermanet. Learning latent plans from play, 2019. 2, 3 

- [37] Zichen Jeff Cui, Yibin Wang, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. From play to policy: Conditional behavior generation from uncurated robot data, 2022. 3, 5 

14 

- [38] Zhiyuan Zhou, Pranav Atreya, Abraham Lee, Homer Walke, Oier Mees, and Sergey Levine. Autonomous improvement of instruction following skills via foundation models, 2024. 2 

- [39] David Ha and J¨urgen Schmidhuber. World models. 2018. doi: 10.5281/ZENODO.1207631. 3 

- [40] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination, 2020. 

- [41] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control, 2024. 3 

- [42] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 3 

- [43] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pre-trained visual features enable zero-shot planning, 2025. 

- [44] Kensuke Nakamura, Lasse Peters, and Andrea Bajcsy. Generalizing safety beyond collision-avoidance via latentspace reachability analysis, 2025. 3 

- [45] Deepak Pathak, Pulkit Agrawal, Alexei A Efros, and Trevor Darrell. Curiosity-driven exploration by self-supervised prediction. In _International conference on machine learning_ , pages 2778–2787. PMLR, 2017. 3 

- [46] Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, and Deepak Pathak. Planning to explore via self-supervised world models. In _International conference on machine learning_ , pages 8583–8592. PMLR, 2020. 

- [47] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 3 

- [48] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _Conference on robot learning_ , pages 2226–2240. PMLR, 2023. 3 

- [49] Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yupeng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, and Dongbin Zhao. World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation. _arXiv preprint arXiv:2509.19080_ , 2025. 3 

- [50] Fangqi Zhu, Zhengyang Yan, Zicong Hong, Quanxin Shou, Xiao Ma, and Song Guo. Wmpo: World model-based policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.09515_ , 2025. 3, 25 

- [51] Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, et al. V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 3 

- [52] Ze Yang, Yun Chen, Jingkang Wang, Sivabalan Manivasagam, Wei-Chiu Ma, Anqi Joyce Yang, and Raquel Urtasun. Unisim: A neural closed-loop sensor simulator, 2023. 3 

- [53] Xiao Fu, Xintao Wang, Xian Liu, Jianhong Bai, Runsen Xu, Pengfei Wan, Di Zhang, and Dahua Lin. Learning video generation for robotic manipulation with collaborative trajectory control, 2026. 3 

- [54] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. Irasim: A fine-grained world model for robot manipulation, 2025. 3 

- [55] Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yue Hu, Yue Liao, Peng Gao, Hongsheng Li, Maoqing Yao, et al. Enerverse: Envisioning embodied future space for robotics manipulation. _arXiv preprint arXiv:2501.01895_ , 2025. 

- [56] 1X World Model Team. 1x world model: Evaluating bits, not atoms. Technical report, 1X, 2025. 

- [57] Wei-Cheng Tseng, Jinwei Gu, Qinsheng Zhang, Hanzi Mao, Ming-Yu Liu, Florian Shkurti, and Lin Yen-Chen. Scalable policy evaluation with video world models. _arXiv preprint arXiv:2511.11520_ , 2025. 3 

- [58] Chenhao Li, Andreas Krause, and Marco Hutter. Robotic world model: A neural network simulator for robust policy optimization in robotics, 2025. 3 

- [59] Jiahan Zhang, Muqing Jiang, Nanru Dai, Taiming Lu, Arda Uzunoglu, Shunchi Zhang, Yana Wei, Jiahao Wang, Vishal M. Patel, Paul Pu Liang, Daniel Khashabi, Cheng Peng, Rama Chellappa, Tianmin Shu, Alan Yuille, Yilun Du, and Jieneng Chen. World-in-world: World models in a closed-loop world, 2025. 3 

15 

- [60] Erick Rosete-Beas, Oier Mees, Gabriel Kalweit, Joschka Boedecker, and Wolfram Burgard. Latent plans for task-agnostic offline reinforcement learning, 2022. 3 

- [61] Rutav Shah, Shuijing Liu, Qi Wang, Zhenyu Jiang, Sateesh Kumar, Mingyo Seo, Roberto Mart´ın-Mart´ın, and Yuke Zhu. Mimicdroid: In-context learning for humanoid robot manipulation from human play videos, 2025. 3 

- [62] Simon Hangl, Emre Ugur, Sandor Szedmak, and Justus Piater. Robotic playing for hierarchical complex skill learning. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2799–2804. IEEE, 2016. 3 

- [63] Simon Hangl, Vedran Dunjko, Hans J. Briegel, and Justus Piater. Skill learning by autonomous robotic playing using active learning and creativity, 2017. 

- [64] Irmak Guzey, Ben Evans, Soumith Chintala, and Lerrel Pinto. Dexterity from touch: Self-supervised pre-training of tactile representations with robotic play. _arXiv preprint arXiv:2303.12076_ , 2023. 3 

- [65] Pulkit Agrawal, Ashvin V Nair, Pieter Abbeel, Jitendra Malik, and Sergey Levine. Learning to poke by poking: Experiential learning of intuitive physics. _Advances in neural information processing systems_ , 29, 2016. 3 

- [66] Frederik Ebert, Chelsea Finn, Sudeep Dasari, Annie Xie, Alex Lee, and Sergey Levine. Visual foresight: Modelbased deep reinforcement learning for vision-based robotic control. _arXiv preprint arXiv:1812.00568_ , 2018. 

- [67] Sudeep Dasari, Frederik Ebert, Stephen Tian, Suraj Nair, Bernadette Bucher, Karl Schmeckpeper, Siddharth Singh, Sergey Levine, and Chelsea Finn. Robonet: Large-scale multi-robot learning. _arXiv preprint arXiv:1910.11215_ , 2019. 

- [68] Sergey Levine, Peter Pastor, Alex Krizhevsky, Julian Ibarz, and Deirdre Quillen. Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection. _The International journal of robotics research_ , 37(4-5):421–436, 2018. 

- [69] Lerrel Pinto and Abhinav Gupta. Supersizing self-supervision: Learning to grasp from 50k tries and 700 robot hours. In _2016 IEEE international conference on robotics and automation (ICRA)_ , pages 3406–3413. IEEE, 2016. 3 

- [70] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Akhil Raju, et al. Robocat: A self-improving foundation agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ , 1(8), 2023. 3 

- [71] Homer Rich Walke, Jonathan Heewon Yang, Albert Yu, Aviral Kumar, Jedrzej Orbik, Avi Singh, and Sergey Levine. Don’t start from scratch: Leveraging prior data to automate robotic reinforcement learning. In _Conference on Robot Learning_ , pages 1652–1662. PMLR, 2023. 3 

- [72] Akshay L Chandra, Iman Nematollahi, Chen Huang, T. Welschehold, Wolfram Burgard, and Abhinav Valada. Diwa: Diffusion policy adaptation with world models. _ArXiv_ , abs/2508.03645, 2025. 3, 25 

- [73] Zhiyuan Zhou, Pranav Atreya, Abraham Lee, Homer Walke, Oier Mees, and Sergey Levine. Autonomous improvement of instruction following skills via foundation models. _arXiv preprint arXiv:2407.20635_ , 2024. 3 

- [74] Nicolas Carlini, Jamie Hayes, Milad Nasr, Matthew Jagielski, Vikash Sehwag, Florian Tramer, Borja Balle, Daphne Ippolito, and Eric Wallace. Extracting training data from diffusion models. In _32nd USENIX security symposium (USENIX Security 23)_ , pages 5253–5270, 2023. 4 

- [75] OpenAI. Gpt-4 technical report, 2024. 5 

- [76] Physical Intelligence et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. 5, 18 

- [77] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 5 

- [78] Xinting Hu, Yi Jiang, Kaihua Tang, Jingyuan Chen, Chunyan Miao, and Hanwang Zhang. Learning to segment the tail, 2020. 5 

- [79] Youguang Xing, Xu Luo, Junlin Xie, Lianli Gao, Hengtao Shen, and Jingkuan Song. Shortcut learning in generalist robot policies: The role of dataset diversity and fragmentation, 2025. 5 

- [80] Yoshua Bengio, J´erˆome Louradour, Ronan Collobert, and Jason Weston. Curriculum learning. In _Proceedings of the 26th annual international conference on machine learning_ , pages 41–48, 2009. 5 

16 

- [81] Liang Wen, Yunke Cai, Fenrui Xiao, Xin He, Qi An, Zhenyu Duan, Yimin Du, Junchen Liu, Tanglifu Tanglifu, Xiaowei Lv, et al. Light-r1: Curriculum sft, dpo and rl for long cot from scratch and beyond. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 6: Industry Track)_ , pages 318–327, 2025. 5 

- [82] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR, 2021. 6 

- [83] Laurens Van der Maaten and Geoffrey Hinton. Visualizing data using t-sne. _Journal of machine learning research_ , 9(11), 2008. 7 

- [84] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 586–595, 2018. 8 

- [85] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE transactions on image processing_ , 13(4):600–612, 2004. 8 

- [86] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 8 

- [87] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 8 

- [88] Lirui Wang, Kevin Zhao, Chaoqi Liu, and Xinlei Chen. Learning real-world action-video dynamics with heterogeneous masked autoregression, 2025. URL `https://arxiv.org/abs/2502.04296` . 10 

- [89] Zhengtong Xu, Qiang Qiu, and Yu She. Vilp: Imitation learning with latent video planning, 2025. URL `https://arxiv.org/abs/2502.01784` . 10 

- [90] Andrew Wagenmaker, Mitsuhiko Nakamoto, Yunchu Zhang, Seohong Park, Waleed Yagoub, Anusha Nagabandi, Abhishek Gupta, and Sergey Levine. Steering your diffusion policy with latent space reinforcement learning. _arXiv preprint arXiv:2506.15799_ , 2025. 10, 22 

- [91] William Liang, Sam Wang, Hung-Ju Wang, Osbert Bastani, Yecheng Jason Ma, and Dinesh Jayaraman. Tether: Autonomous functional play with correspondence-driven trajectory warping, 2026. URL `https://arxiv.org/ abs/2603.03278` . 21 

- [92] Ansh Kumar Sharma, Yixiang Sun, Ninghao Lu, Yunzhe Zhang, Jiarao Liu, and Sherry Yang. World-gymnast: Training robots with reinforcement learning in a world model, 2026. URL `https://arxiv.org/abs/2602.02454` . 25 

17 

# Appendix 

## **A Implementation Details** 

Here we provide more implementation details of PlayWorld that expands upon Sec. 3, including the setup for play data collection (Sec. 3.2), and training details for the action-conditioned video model (Sec. 3.3). 

**Data Collection Design.** One ideal approach for data collection for training world models is to use an exploration policy that selects actions to maximally reduce the world model’s uncertainty (i.e., to intentionally seek out transitions that are most informative for the learned dynamics). While appealing in theory, we found this objective difficult to realize in a reliable, deployable system. In particular, using uncertainty estimates from a continually-updated video world model as a real-time reward signal can be unstable during robot execution, and can also create substantial operational overhead, since the model must be updated frequently as new data arrives, and the exploration signal can drift in ways that complicate monitoring and safety. 

Instead of directly optimizing “informativeness” through world-model uncertainty, PlayWorld uses a simple but robust proxy that maximizes the _diversity_ of behaviors while staying close to the policy’s natural action manifold. Empirically, this produces broad coverage of interaction modes and state transitions without requiring a brittle closed-loop interdependence between exploration and model uncertainty estimation. Concretely, to make the system readily portable across tasks with minimal engineering, we instantiate our play collector with _π_ 0 _._ 5-DROID [76]. Beyond its general instruction-following capability, _π_ 0 _._ 5-DROID reliably executes scene resets and handles a wide range of language prompts, which dramatically reduces human supervision, enabling persistent, scalable data collection. We provide further details analyzing the properties of the collected play data in Appendix B. 

#### **Example Prompt** 

You are a robot that is trying to randomly manipulate/arrange objects on the table in a square region marked by tape. 

Ignore anything that’s not on the gray table. First, observe if any object is outside of the square workspace area. If so, please output: “ `move the <> towards the center of the table."` Otherwise, please come up with a short task for the robot to perform. Possible instructions might include: 

- 1) “ `Put the <> on the <>."` 

- 2) “ `Remove the <> from the <>."` 

- 3) “ `Put the <> near the <>."` 

- 4) “ `Pick up the <> and put it onto the <>."` 

Feel free to modify the prompt with different verbs and nouns (e.g. “put” _→_ “move”, “block” _→_ ”object”). Use color to help the robot better identify the objects. Don’t include quotation marks in the task. 

#### **Example In-Distribution Tasks** 

Put the carrot in the white bowl. Remove the white plush toy from the bowl Pick up the orange rectangular block and put it on the gray table. Fold the towel from left to right. ... 

#### **Example Out-of-Distribution Tasks** 

Slide the carrot near the beige container. Move the orange rectangle onto the yellow cube. Flip the block up-side-down. Drag the blue towel across the table. ... 

18 


**Figure 12** Example extracted centroids from the demonstration data that roughly corresponds to distinct nominal behavior episodes. 

**Video Model Training.** Our video model follows the setup of [9], which jointly predicts 3 camera views (left, right, and wrist views, each with resolution 192 _×_ 320) given the current view and the Cartesian-space end-effector pose. We first pretrain the base SVD model on the full DROID dataset, and then fine-tune using the curriculum described in Sec. 3.3, with the hyperparameters in Table 2. The goal of this curriculum is to progressively shift training mass toward harder, rarely occurring transitions, preventing the model from overfitting to dominant free-space motion patterns. In practice, we compute a representation for each trajectory by concatenating CLIP embeddings from four sparsely-sampled frames over a 1-second window. For each task, we use _K_ = 5 to identify nominal behavior modes via clustering, and set _R_ = 5 ranks per task to construct the curriculum sampling buckets. We initialize the rank-sampling distribution as (0 _._ 5 _,_ 0 _._ 3 _,_ 0 _._ 1 _,_ 0 _._ 05 _,_ 0 _._ 05) and anneal it to (0 _._ 1 _,_ 0 _._ 2 _,_ 0 _._ 2 _,_ 0 _._ 25 _,_ 0 _._ 25) by uniformly updating the probabilities every 5000 steps. Fig. 12 shows the most 

**Table 2** Hyperparameters used for video model training. 

|**Hyperparameter**|**Value**|
|---|---|
|Learning Rate|5e-6|
|Warmup Steps|100|
|Scheduler|cosine|
|Gradient clipping|1.0|
|Global batch size|64|
|Observation Shape|320 _×_ 192 _×_ 3|
|Num. Predicted Frames|5|
|Num. History Frames|7|
|Frame-level Condition|True|
|Frequency|5 Hz|
|Denoising Steps|50|
|Guidance|2.0|


representative sample (centroid) from each cluster that is used to construct the ranks, illustrating that the discovered modes align well with intuitive task-level sub-behaviors. While we used demonstration data as a proxy to define ranks with different motion attributes, we find that under this simplistic setup, the specific parameters used can have noticeable impact on model quality. Future works could investigate how to make the curriculum-like setup more generalizable for data at larger scale, where a more robust signal for motion quality could potentially be directly learned from data. 

## **B Play Data Analysis** 

Play data provides a scalable way to transform large volumes of a robot’s uncurated experience into a high-quality, simulatable environment, with minimal human involvement. In this section, we provide further analysis on properties of play data in comparison to human-collected alternatives to demonstrate that autonomously-collected data can exhibit meaningful behavioral diversity. 

**Play Data Visualization.** Fig. 13 provides qualitative snapshots from the play data corpus on a few different object sets, highlighting the natural variations that emerge when the robot explores without a scripted task objective (e.g., diverse object contacts, viewpoints, and interaction outcomes). 

**Data Distribution at Different Scales.** To complement these examples with a quantitative view, we include an extended t-SNE analysis (Fig. 14) across multiple dataset scales. Specifically, we embed the initial frame of each trajectory using CLIP features and visualize the resulting state-space coverage. Across matched data budgets, play data consistently spans a broader region of the embedding space than human-collected trajectories, while demonstration-based data concentrates in a comparatively narrow subset of states. As autonomously collected data scales beyond the practical limits of human collection, we expect it to cover the state space more densely and more broadly, yielding richer supervision and more informative transitions for 

19 


**Figure 13** Example play data episodes selected from autonomous roll-outs for various tasks. 


**Figure 14** Training sample distribution for demonstration data, human-collected play data, and autonomously-collected play data at different scales. We observe that play data consistently provides the widest distribution over the state space, while other human-collected data exhibits limited expansion in coverage even at larger scale. 

20 

**Table 4** Per-category perceptual similarity across different training data mixtures. 

|||**PSNR** (_↑_|)||||
|---|---|---|---|---|---|---|
|Training Mix|Success|Missed Grasp|Slide|Slip|Deformation|Collision|
|Human Demo|24.78|24.37|23.98|23.66|22.58|24.67|
|Human Play|23.56|24.41|23.90|24.01|22.93|24.91|
|Robot Play|24.95|24.83|25.02|24.84|23.22|24.61|
|Robot Play (Curriculum)|25.01|24.82|25.14|24.78|23.55|24.95|
|||**MSE** (_↓_)|||||
|Training Mix|Success|Missed Grasp|Slide|Slip|Deformation|Collision|
|Human Demo|279.80|280.87|341.36|324.57|428.55|354.46|
|Human Play|284.01|276.54|302.10|332.65|390.98|304.12|
|Robot Play|274.81|259.14|263.17|259.10|366.55|297.34|
|Robot Play (Curriculum)|265.13|264.19|250.46|243.51|350.12|295.53|


#### training the world model. 

**Concurrent Works.** Concurrent with our work, [91] explores the use of autonomous play for policy learning by generating task-directed interactions guided by vision-language models (VLMs). Their results show that play-collected data can achieve competitive performance compared to human demonstrations, highlighting the potential of autonomous play as a scalable and sustainable source of training data for robot learning. 

## **C Additional Trajectory Replay Results** 

In this section, we provide more details on the trajectory replay experiments, including the composition of our evaluation benchmark, details on the scaling experiments, and full results on additional perceptual metrics. 

#### **Evaluation Benchmark.** 

Nominal task execution typically involves static contacts whose dynamics are comparatively consistent and easy to model. In contrast, dynamic object interactions such as collisions, deformation, or slip are substantially more diverse and harder to predict, yet they are often the decisive factors for counterfactual evaluation and task success. To target these failures, our benchmark is explicitly designed around predicting these interaction events. 

Since contact events are highly multi-modal, we curate the benchmark from a large set of policy roll-outs and identify natural failure episodes that arise in practice. We then label each episode by failure mode, where the resulting distribution is summarized in Table 3. For every failure mode, our test set spans a wide range of trajectories. We argue that this coverage provides a more stringent and realistic assessment of action-conditioned video models, compared to typical nominal trajectory-replay evaluations which assess the model’s capability of generating realistic trajectories, rather than faithfully predicting effects of actions. For completeness, we provide additional results on the perceptual metrics in Table 4 (extending the results in Table 1). 

**Table 3** Composition of the trajectory replay benchmark. 

|**Source**|#**Samples**|
|---|---|
|Human-collected|97|
|_π_0|85|
|_π_0_._5|122|
|Diffusion Policies|229|
|**Category**|#**Samples**|
|Success|98|
|Missed Grasp|88|
|Slide|76|
|Slip|89|
|Deformation|90|
|Collision|92|


**Scaling Experiments.** In this section, we discuss the results in Fig. 10 in greater detail. To enable a fair and interpretable comparison across models trained with different dataset sizes, we convert the raw LPIPS metric 

21 

_sraw_ into a normalized score _sn_ using a fixed affine transform: 


Here, _s_ min = 0 _._ 072 and _s_ max = 0 _._ 10 are constants that define the LPIPS range used for normalization in our benchmark. This mapping preserves the ordering of models while (i) rescaling the narrow LPIPS interval to improve separation in scaling plots and (ii) inverting the axis so that higher values correspond to better perceptual fidelity. As a result, scaling trends are easier to interpret, while all pairwise model comparisons remain unchanged. 

## **D Additional Fine-Tuning Results** 

Sim-to-real transfer is one of the most demanding end-to-end evaluations of a robotic simulator. Real robots expose compounded mismatch in contact, actuation, latency, and sensing, so policies trained in simulation often fail on hardware if they latch onto simulator-specific artifacts. In this section, we show that an accurate world model can allow RL fine-tuning with consistent improvement in real-world success rate, even on challenging fine-grained manipulation tasks. 

**Stable RL Fine-tuning for Diffusion-Based Models.** Although many modern robot policies are parameterized as diffusion or flow-matching models, RL fine-tuning these generators remains challenging: the policy is realized through an iterative sampling procedure, making it difficult to obtain stable, low-variance gradients with standard actor–critic objectives. Fine-tuning inside a learned world model introduces an additional source of brittleness, since effective exploration can hinge on the model capturing fine-grained action-dependent differences in predicted outcomes; small modeling errors can therefore distort the learning signal and lead to unstable updates. As a result, prior works primarily use world models as data generators, performing supervised fine-tuning (SFT) on filtered synthetic rollouts instead of directly optimizing returns. In PlayWorld, we show that when the world model is sufficiently accurate, direct RL fine-tuning can be surprisingly effective even for fine-grained manipulation, and can improve robustness beyond what is achievable from demonstrations alone. 

**Fine-Tuning with DSRL.** For our fine-tuning setup, we adopt the formulation in [90], which assumes a pretrained diffusion policy (e.g., trained with behavioral cloning) that generates an action sequence **a** conditioned on the current policy input **s** (observations and proprioceptive state). Sampling proceeds by drawing an initial latent-noise vector **w** _∼N_ ( **0** _,_ **I** ) and running a fixed reverse-diffusion denoiser to obtain the action: 


where _gθ_ denotes the full reverse process (possibly multi-step) implemented by a frozen diffusion model with parameters _θ_ . This induces the (marginal) policy distribution 


i.e., actions are generated by pushing forward a simple noise prior through the denoiser. 

Following the “noise actor” formulation of Wagenmaker et al. [90], we replace the fixed prior _N_ ( **0** _,_ **I** ) with a learned, state-conditioned distribution over initial noise: 


where _πϕ_<sup>_W_isasmallpolicy(e.g.,anMLPGaussian)withparameters</sup><sup>_ϕ_.Thisyieldsa</sup><sup>_steered_actionpolicy</sup> 


which can be viewed as learning an expressive adapter in the diffusion model’s latent-noise space while leaving the diffusion parameters _θ_ unchanged. We optimize _πϕ_<sup>_W_withanRLobjectivedefinedonenvironmentrollouts</sup> 

22 

produced by executing **a** = _gθ_ ( **s** _,_ **w** ). Let _τ_ = ( **s** 0 _,_ **w** 0 _,_ **r** 0 _,_ **s** 1 _, . . ._ ) denote the resulting trajectory; then the goal is 


Crucially, we treat **w** as the RL action and the (frozen) diffusion sampler _gθ_ as part of the environment interface. In practice, this allows standard off-policy actor–critic updates using replay tuples ( **s** _t,_ **w** _t,_ **r** _t,_ **s** _t_ +1), without requiring backpropagation through the world dynamics or through the multi-step reverse-diffusion procedure. The specific hyperparameters used can be found in Table 5. 

**Reward Model Design.** To enable efficient policy improvement, we train a simple progress-based reward model from a small set of demonstrations. Given two time steps, the model predicts task progress, which we convert into a dense per-step signal by taking the difference in predicted progress between consecutive steps: 


Despite its simplicity, this reward signal leads to fast and stable learning in our setting: we often observe measurable behavioral improvements within the first 10–20 episodes. In contrast, sparse terminal 0 _/_ 1 rewards require substantially more interaction to achieve comparable gains. We also explored vision-language-model (VLM) rewards, but found them less reliable in practice, often destabilizing fine-tuning with false predictions. 

**Table 5** Hyperparameters used for DSRL training and diffusion policy. 

|**Hyperparameter**|**Value**|
|---|---|
|Obs dim|8|
|Action dim|8|
|Image shape|[6, 192, 192]|
|Cond steps (state)|1|
|Cond steps (image)|1|
|Horizon|16|
|Max episode steps|30|
|Actor LR|1e-5|
|Batch size|64|
|Discount|0.99|
|Train freq|15|
|UTD|10|
|Tau|0.001|
|Layer norm|True|
|MLP backbone|3 layers _×_ 256|
|Target Entropy|0.0|
|Initial rollout steps|800|
|Action magnitude|0.5|
|Denoising steps|100|
|DDIM steps|5|
|Prediction target|_ϵ_|
|Spatial embedding|128|


**Experiment Setup.** To show the power of fine-tuning with PlayWorld, we use diffusion policies trained from scratch with 5 _−_ 10 demonstrations. We then collect 10 _−_ 20 initial object configurations as environment initializations for the world model, and perform fine-tuning by randomly sampling among the available initializations. With each checkpoint, we perform 20 hardware trials to calculate the success rates shown in Fig. 9. 

**Effectiveness of Fine-Tuning and World Model Hacking.** Here, we report some interesting observations from the fine-tuning experiments. First, we find that _stochastic predictions from the world model are beneficial_ 

23 


**Figure 15** Task: remove the carrot from the bowl. Top: base policy behavior in the real world. Bottom: PlayWorld fine-tuned policy behavior in the world, where the robot learned to grasp a more stable position. 


**Figure 16** Task: fold the towel from left to right. Top: base policy behavior in the real world. Bottom: PlayWorld fine-tuned policy behavior in the world, where the grasping motion is more robust and accurate. 

_for learning robust policies_ , particularly under out-of-distribution (OOD) conditions. We hypothesize that stochastic video rollouts effectively act as a form of data augmentation: by exposing the policy to diverse, plausible futures during training, the resulting behavior generalizes to initializations that were not observed during either pretraining or fine-tuning. As shown in Fig. 16, when initialized from a novel configuration, the fine-tuned policy is able to gradually adapt its actions and eventually achieve a successful towel grasp. 

Second, we find that _world-model hallucinations are not necessarily as detrimental to fine-tuning as one might expect_ . In several baseline fine-tuning runs, the learned policy partially collapsed into exploiting spurious model predictions—executing actions that are suboptimal (or nonsensical) in reality, yet yield high reward under the learned dynamics (i.e., “reward hacking” within the model). Despite this behavior in imagination, the resulting policies often still transferred well to the real robot. We hypothesize that fine-tuning can simultaneously (i) extract genuinely useful signal from the world model and reward, but may (ii) overfit to hallucinated failure modes that are unlikely to occur under real dynamics; when deployed, these spurious gradients may have limited effect because the corresponding states are never realized. Overall, this suggests that meaningful performance gains are possible even with imperfect world models, provided that hallucinations do not dominate the policy updates that matter on real trajectories. 

Finally, we also observe the converse phenomenon: policies can _overfit to the world model_ and degrade with prolonged fine-tuning. Because even small prediction errors (e.g., in depth, contacts, or control response) can shift the boundary between “success” and “failure” in the model, the set of trajectories that are scored as successful in imagination does not perfectly align with real-world outcomes. As a result, extended fine-tuning 

24 

can gradually bias the policy toward exploiting these mismatches, yielding apparent gains under the model while reducing real-world success rate. This effect is most pronounced when the policy repeatedly revisits a narrow subset of imagined high-reward states, effectively specializing to idiosyncrasies of the learned dynamics rather than improving the underlying task strategy. Practically, this motivates using conservative stopping criteria (e.g., early stopping on real rollouts) and/or regularization toward the pretrained policy to prevent overfitting to model errors. 

**Related/Concurrent Works.** Prior work on adapting video-based world models for RL-finetuning largely falls into two categories. The first trains **task-specific world models** , fine-tuned on narrow, single-task datasets to optimize performance for a predefined objective [50, 72]. While effective within scope, these models often overfit to a limited interaction distribution and lack generality beyond the target task. The second direction explores **generalist world model fine-tuning** , where large pretrained video models are adapted using broad, internet-scale or multi-task data [92]. These approaches typically improve high-level capabilities such as language following, semantic consistency, or robustness to distractors, but do not explicitly optimize for contact-rich physical fidelity required for fine-grained visuo-motor control. PlayWorld instead explores an intermediate space by collecting lab-scale interaction data that spans a broad distribution of contact events beyond any single task. We show that the resulting world model more faithfully captures fine-grained object motion and contact dynamics, enabling policy improvements that transfer reliably to the real world—yielding smoother execution, more accurate and robust end-effector control, and higher success rates on fine-grained manipulation tasks. 

## **E Final Remarks** 

We believe large-scale play data is a particularly promising and scalable supervision source for learning video world models, which can make learned simulators substantially more practical for policy development. In our lab setting, we were able to collect many hours of diverse, unlabeled interaction data with relatively low overhead, demonstrating its utility for various post-training applications. Looking forward, scaling data collection across multiple institutions and hardware setups could further expand coverage of environments, object sets, and embodiments, improving both the fidelity and the robustness of learned dynamics. Such a shared play-data ecosystem would enable us to build stronger, more generalizable world simulators that will be a valuable resource to the robot learning community. 

25 

