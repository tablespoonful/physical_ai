---
title: "CausalDreamer: Learning Predictive World Models with Latent Disentanglement"
date: "2026-10-08"
authors: "Prince Jha; Nils Lukas; Kun Zhang; Salem Lahlou"
url: https://arxiv.org/abs/2610.12016
pdf: https://arxiv.org/pdf/2610.12016
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.12016)** / [論文ページ](https://arxiv.org/abs/2610.12016)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CausalDreamer: Learning Predictive World Models with Latent Disentanglement** 

**Prince Jha**<sup>1</sup> **Nils Lukas**<sup>1</sup> **Kun Zhang**<sup>1</sup><sup>_,_2</sup> **Salem Lahlou**<sup>1</sup> 

1Mohamed bin Zayed University of Artificial Intelligence (MBZUAI) 

2Carnegie Mellon University 

**Abstract:** World models for control must capture which aspects of the environment respond to the agent’s actions and which are relevant to reward. Generative world models such as Dreamer 4 consist of a video tokenizer, which encodes each frame into a latent, and a dynamics model, which is pretrained to predict future latents from past latents and actions. Yet the tokenizer is trained with a reconstruction objective, without action or reward supervision, so its latent provides no explicit mechanism to separate controllable, uncontrollable, reward-relevant, and reward-irrelevant information. We propose _CausalDreamer_ , which keeps the tokenizer frozen and re-encodes its latent into a factored representation of four groups along two axes: controllability, where only the two controllable groups receive the action, and reward relevance, learned by predicting the reward from the two reward-relevant groups. The pretrained dynamics model is then fine-tuned to predict the factored representation. We evaluate _CausalDreamer_ and the pretrained world model it starts from with model-predictive planning on 20 MMBench2 tasks: 10 clean tasks seen during training and 10 unseen tasks, of which 6 are manipulated variants of clean tasks with a changed background, object, or maze layout, and 4 are new environments. We normalize returns so that a policy taking uniformly random actions scores 0 and an expert scores 1. _CausalDreamer_ achieves a 14% higher normalized score than the pretrained world model on the clean tasks (0.199 vs. 0.175) and a 25% higher score on the manipulated variants (0.307 vs. 0.246), while neither model scores meaningfully above the random policy in the new environments. Additionally, our analysis shows that the factored representation separates reward-irrelevant changes, such as a changed background, from its reward-relevant groups. 

**Keywords:** World Models, Representation Learning, Model-Based Planning 

## **1 Introduction** 

World models let an agent plan by predicting the consequences of candidate actions in a learned latent space, rather than by trial and error in the environment [1, 2, 3]. For such planning to be reliable, the latent must expose the structure that decisions depend on, namely which parts of the scene respond to the agent’s actions and which parts determine reward. A latent that mixes the agent’s own effect with background motion, or task-relevant objects with irrelevant texture, forces the planner to compare imagined futures that differ in ways unrelated to the task [4, 5]. 

Scalable world models now render realistic, action-conditioned video by pairing a video tokenizer with a diffusion or flow-matching dynamics model trained on hundreds of hours of multi-task data [3, 6]. However, their tokenizer learns its latent from a reconstruction objective, without access to actions or rewards, so the latent does not explicitly distinguish controllable from uncontrollable content, or reward-relevant from reward-irrelevant content. The dynamics model must discover these distinctions inside one entangled latent, and in practice it can predict frames that are visually 

Submitted to the 4th Workshop on Learning Effective Abstractions for Planning (LEAP) at CoRL 2026. Do not distribute. 

plausible but ignore the action actually taken [6]. Methods that do learn such factorized latents rely on variational recurrent state-space models or non-generative predictors trained from scratch, and impose the factorization through per-factor KL terms or mutual-information constraints [7, 4, 5]. These mechanisms have no counterpart in a tokenizer-based generative world model, which leaves open how controllability and reward structure can be built into such a model while its tokenizer remains frozen. 

Accordingly, we propose _CausalDreamer_ , which places a factored representation between the frozen tokenizer of a pretrained generative world model and its dynamics model. Each frame’s latent is re-encoded into four groups, organized by whether they are controllable and whether they are relevant to reward. Only the two controllable groups receive the action, so the routing of action information is an architectural choice rather than a learned one. Reward relevance is encouraged by predicting the reward from the two reward-relevant groups only. The four groups jointly reconstruct the tokenizer latent, so the frozen decoder still renders them, and together they keep the latent’s shape, so the pretrained dynamics model is finetuned to predict the factored representation with its original architecture and losses. CausalDreamer therefore adds this structure to an existing generative world model after pretraining, with the tokenizer frozen and without a variational posterior or mutual-information estimator. 

We build CausalDreamer on the 350Mparameter MMBench2 world model and compare it with the pretrained model it is finetuned from, using closed-loop planning with the cross-entropy method. The evaluation covers 10 clean tasks seen during training and 10 


Figure 1: **Learning the factored representation.** A frozen encoder maps each frame to the tokenizer representation. Four projection heads reencode it into four groups, organized by controllability and reward relevance; only the two controllable heads receive the action. A reward predictor reads only the two reward-relevant groups, and a residual decoder reconstructs the tokenizer representation from all four groups. Grey components are frozen, and the red boxes are the two training losses. 

unseen tasks: 6 manipulated variants of clean tasks, in which the background, an object, or the maze layout differs, and 4 new environments. Returns are normalized between a policy that takes uniformly random actions (0) and an expert (1). On the clean tasks, CausalDreamer raises the normalized score from 0.175 to 0.199, a 14% improvement, and on the manipulated variants from 0.246 to 0.307, a 25% improvement; in the new environments, neither model plans meaningfully better than the random policy. Finally, when only the background of a scene changes, most of the resulting change in the factored representation stays out of its reward-relevant groups, which shows that the factored representation separates reward-irrelevant changes from the content used to predict reward. 

In summary, our contributions are threefold. **(i)** We introduce _CausalDreamer_ , which re-encodes the latent of a frozen video tokenizer into a _factored representation_ along controllability and reward relevance, and fine-tunes the pretrained dynamics model on it. **(ii)** We show that planning with CausalDreamer reaches a _higher normalized score_ than the pretrained model on the clean tasks of MMBench2 and on manipulated variants of these tasks not seen during training. **(iii)** We show, by changing only the background of a scene, that the factored representation _keeps reward-irrelevant changes largely out of its reward-relevant groups_ . 

2 

## **2 Background** 

We build on the world model of MMBench2 [6], a 350M-parameter model that follows the architecture and training recipe of Dreamer 4 [3]: a video tokenizer is trained first, and a dynamics model is then trained on the representations of the frozen tokenizer. 

**Tokenizer.** The tokenizer is a transformer encoder–decoder. The encoder _E_ splits each 224 _×_ 224 frame into 256 patches and prepends _L_ = 64 learned latent tokens, which attend to all patches while the patches attend only to each other; the latent tokens are projected to _D_ = 64 channels and bounded by a tanh, giving _Vt ∈_ [ _−_ 1 _,_ 1]<sup>_L×D_</sup> . The decoder _G_ reconstructs the frame from _Vt_ alone. The tokenizer is trained with mean squared error and LPIPS [8], _L_ tok = _L_ MSE + 0 _._ 2 _L_ LPIPS, in a masked-autoencoding setup [9] in which a fraction _p ∼ U_ (0 _,_ 0 _._ 9) of the input patches of each frame is replaced by a learned mask token. 

**Dynamics Model.** The dynamics model _fθ_ is a block-causal transformer over the frames of a clip: tokens of frame _t_ attend to each other and to the tokens of earlier frames. For each frame, its input consists of an action token, a token encoding the signal level and step size of the shortcut objective below, 32 spatial tokens obtained by packing pairs of the _L_ latent vectors of _Vt_ , and 4 learned register tokens. For control, agent tokens that receive an embedding of the task description are added to each frame [3]; they attend to all other tokens, while no other token attends to them, so that the task does not influence the predicted frames. A reward head and a behavior-cloning head read the agent tokens and predict the rewards and actions of the next _M_ = 8 steps, trained with a two-hot cross-entropy over symlog-transformed reward bins ( _L_<sup>dyn</sup> rew<sup>) and a mean squared error on the actions (</sup><sup>_L_bc) [6].</sup> 

**Shortcut Forcing.** The dynamics model is trained with the shortcut forcing objective of Dreamer 4, which combines diffusion forcing [10], where every frame of a clip receives its own noise level, with shortcut models [11], where the network is also conditioned on the size of the denoising step. Each frame is corrupted to _V_<sup>˜</sup> _t_ = (1 _− τt_ ) _ϵ_ + _τtVt_ with _ϵ ∼N_ (0 _, I_ ), where the signal level _τt ∈_ [0 _,_ 1] runs from pure noise ( _τt_ = 0) to the clean frame ( _τt_ = 1), and the network predicts the clean representations from the corrupted clip, the actions, the signal levels and the step sizes _dt_ , 


At the finest step size _d_ min, the loss is the squared error to the clean representation; for larger steps, the target is obtained by bootstrapping two half steps of the network itself, _b_<sup>_′_</sup> = � _fθ_ ( _V , τ,_<sup>˜</sup><sup>_<u>d</u>_</sup> 2<sup>_, a_)</sup><sup>_−_</sup> _V_ ˜ � _/_ (1 _− τ_ ), _V_<sup>_′_</sup> = _V_<sup>˜</sup> +<sup>_<u>d</u>_</sup> 2<sup>_b′_and</sup><sup>_b′′_=</sup> � _fθ_ ( _V_<sup>_′_</sup> _, τ_ +<sup>_<u>d</u>_</sup> 2<sup>_,_</sup><sup>_<u>d</u>_</sup> 2<sup>_, a_)</sup><sup>_−V′_�</sup> _/_ (1 _− τ −_<sup>_<u>d</u>_</sup> 2<sup>), per frame,</sup> 


where sg stops gradients and the ramp weight _w_ ( _τ_ ) = 0 _._ 9 _τ_ + 0 _._ 1 emphasizes the less noisy signal levels. At inference, each frame is generated from noise in _K_ = 4 steps of size _d_ = 1 _/_ 4, conditioned on the earlier, already generated frames, which are slightly corrupted to signal level _τ_ ctx = 0 _._ 1. The full dynamics objective is _L_ dyn = _L_ shortcut + _L_ rew<sup>dyn+</sup><sup>_L_bc.</sup> 

## **3 Method** 

CausalDreamer adds a factored representation to the pretrained world model of Section 2 in two stages, keeping the tokenizer frozen throughout. We first define the factored representation and the role of each of its groups (Section 3.1). We then describe how CausalDreamer learns this representation from the tokenizer representation (Figure 1) and how the pretrained dynamics model is fine-tuned to predict it (Section 3.2). 

### **3.1 Problem Setting** 

We consider an agent interacting with an environment, modeled as a partially observed Markov decision process with latent states _st_ , actions _at_ , observations _xt_ and rewards _rt_ . At each step, 

3 

the environment moves from _st−_ 1 to _st ∼ P_ ( _· | st−_ 1 _, at−_ 1) under the action _at−_ 1 taken by the agent, emits an image observation _xt ∈_ R<sup>_H×W ×C_</sup> of the new state, and returns the reward _rt_ = _R_ ( _st−_ 1 _, at−_ 1) of this transition. The data available for learning consist of clips of _T_ consecutive steps ( _xt, at−_ 1 _, rt_ )<sup>_T_</sup> _t_ =1<sup>.</sup> 

**Tokenizer Representation.** Each frame is represented by the frozen tokenizer of Section 2, which maps it, together with the earlier frames of its clip, to 


Since the tokenizer is trained without action or reward supervision, _Vt_ provides no explicit mechanism to separate controllable, uncontrollable, reward-relevant, and reward-irrelevant information. 

**Factored Representation.** Given the tokenizer representation _Vt_ of a frame and the action _at−_ 1, we aim to learn a factored representation _zt_ that supports reconstruction of the tokenizer representation and prediction of the reward. The factored representation consists of four groups _Zt_<sup>_k∈_R(</sup><sup>_L/_4)</sup><sup>_×D_,</sup> indexed by _k ∈K_ = _{AR, AR, A_<sup>¯</sup> _R,_<sup>¯</sup> _A_<sup>¯</sup> _R_<sup>¯</sup> _}_ , where each label names the combination of controllability ( _A_ or _A_<sup>¯</sup> ) and reward relevance ( _R_ or _R_<sup>¯</sup> ) the group is designed to capture, 


The _controllable_ groups _KA_ = _{AR, AR_<sup>¯</sup> _}_ depend on _Vt_ and _at−_ 1, and the uncontrollable groups depend on _Vt_ alone, 


The _reward-relevant_ groups _KR_ = _{AR, AR_<sup>¯</sup> _}_ are used to predict the reward, 


### **3.2 CausalDreamer** 

**Action-Conditioned Projections.** Each projection _fk_ in Eq. (5) is a multilayer perceptron that reads the whole tokenizer representation flattened into one vector _vt_ = vec( _Vt_ ) _∈_ R<sup>_LD_</sup> , with the action concatenated, [ _vt_ ; _at−_ 1 ], for _k ∈KA_ , where _at−_ 1 is set to zero for the first frame of a clip. Since every head reads all of _Vt_ , each group is a learned re-encoding of the whole frame rather than a subset of the tokenizer’s latent vectors. Each head outputs a vector of size _LD/_ 4, which is reshaped to _Zt_<sup>_k∈_R(</sup><sup>_L/_4)</sup><sup>_×D_, and the four groups are stacked in the order of Eq. (4) to form</sup><sup>_zt∈_R</sup><sup>_L×D_.</sup> 

**Learning Objective.** Figure 1 illustrates how the factored representation is learned. A residual decoder _Q_ ( _z_ ) = _z_ + _q_ ( _z_ ), where _q_ is a multilayer perceptron whose last layer is initialized to zero, maps the concatenated groups back to the tokenizer representation, and a reward predictor _h_ reads only the reward-relevant groups. With the tokenizer frozen, the heads, _q_ and _h_ are trained per frame with 


where CE is a two-hot cross-entropy over symlog-transformed reward bins, the first frame of each clip has no reward target, and _λ_ weights the reward term. The reconstruction term encourages the four groups together to retain the information in _Vt_ , and lets the frozen decoder render a factored representation as _G_ ( _Q_ ( _zt_ )). Since _Q_ is initialized as the identity, reconstruction initially favors _zt ≈ Vt_ , which is intended to keep the factored representation close to the input space of the pretrained dynamics model that we fine-tune on it. The reward term encourages the reward-relevant groups to carry the information needed to predict _rt_ . 

**Dynamics on the Factored Representation.** With the projections _fk_ and the decoder _Q_ frozen, we fine-tune the pretrained dynamics model _fθ_ of Section 2 to predict each factored representation from the earlier ones in its clip and the actions that led to them, ( _z<t, a<t_ ) _�→ zt_ . Since _zt_ has the shape of _Vt_ , this requires no architectural change: _fθ_ is trained with the same objective _L_ dyn, with 

4 


Figure 2: **Evaluation tasks.** _Top:_ six manipulated tasks, each a variant of a clean task (shown above it) that differs in the background (colors of the background and floor, with the same embodiment and goal), in the manipulated object, or in the maze layout. _Bottom:_ the four clean tasks without a manipulated variant, and four new environments with their own dynamics and rewards. Clean tasks are part of the training corpus; manipulated tasks and new environments have no training data. Each image shows the first frame of an episode. 

_zt_ in place of _Vt_ in Eqs. (1) and (2). The reward head of _fθ_ reads the agent tokens and is therefore not restricted to the reward-relevant groups, unlike _h_ . The behavior-cloning head is trained with gradients stopped, so _L_ bc does not update _fθ_ , and each loss term is divided by a running estimate of its magnitude. A predicted factored representation _z_ ˆ _t_ is rendered as _G_ ( _Q_ (ˆ _zt_ )). 

## **4 Experiments** 

In this section, we evaluate whether fine-tuning a pretrained world model on the factored representation improves closed-loop planning, and whether the factored representation separates rewardirrelevant changes from its reward-relevant groups. Our evaluation is structured to answer the following questions: 

1. Does planning with CausalDreamer reach higher task scores than the pretrained world model on clean tasks? (Section 4.2) 

2. Does this difference persist, without fine-tuning, when one aspect of a clean task is changed, and does either model transfer to new environments? (Section 4.3) 

3. Does the factored representation separate reward-irrelevant changes from its rewardrelevant groups? (Section 4.4) 

For each task we run one episode on each of 20 environment seeds, using the same seeds for every model, and we summarize results by the mean normalized score across tasks. 

### **4.1 Experimental Setup** 

**Models.** All models share the frozen MMBench2 tokenizer, the training data and the planner, and differ only in the dynamics model: _CausalDreamer (ours):_ the factored representation of Section 3.2 with dynamics fine-tuned from the pretrained checkpoint. 

5 

_Pretrained:_ the pretrained MMBench2 dynamics model [6] from which CausalDreamer is finetuned, a 350M-parameter Dreamer 4-style world model. 

_Matched control:_ the pretrained dynamics model fine-tuned for the same number of steps on the same data with the same objective, but on the tokenizer representation instead of the factored representation, which separates the effect of the factorization from the effect of additional training. 

**Dataset.** All models are trained on the MMBench2 pretraining corpus, which covers 200 tasks from 10 domains with 260 episodes per task of 224 _×_ 224 frames labeled with ground-truth actions and rewards. Its episodes are collected with three kinds of behavior policy: the expert policies of MMBench, mixed policies that perturb expert actions with action transforms, structured noise or random actions within an episode, and no-op actions; the logged action is always the action executed in the environment. Actions are zero-padded to 16 dimensions with a per-task validity mask. Although the corpus also provides low-dimensional states, all models use only RGB observations. 

**Evaluation.** We evaluate on twenty MMBench2 tasks (Figure 2), which we divide by their relation to the training data. 

_Clean tasks._ The ten clean tasks are part of the training corpus: cup-catch and finger-turn-easy (DMControl), mw-push (Meta-World), ms-push-cube (ManiSkill), lunarlander-hover (Box2D), ogpoint-maze and og-point-bottleneck (OGBench), and pygame-point-maze-var1, pygame-pong and pygame-bird-attack (MiniArcade). 

_Manipulated tasks._ Six tasks have no training data and are each obtained from a clean task by changing one aspect of it: the background, with the same embodiment and goal (cup-catch-var1 and finger-turn-easy-var1, from cup-catch and finger-turn-easy), the manipulated object (ms-pushbanana, from ms-push-cube), or the maze layout (og-point-var1, og-point-var2 and pygame-pointmaze-var4, from og-point-bottleneck, og-point-maze and pygame-point-maze-var1). _New environments._ Four further tasks have no training data and no clean counterpart (pygamereacher-easy, pygame-dungeon-explorer1, pygame-foraging and pygame-whirlpool). 

All tasks are evaluated without fine-tuning, and each model receives only the text embedding of the task description. We plan with the cross-entropy method at the MMBench2 settings, with a horizon of 32 steps, replanning every 16 steps, 256 samples, 32 elites and 4 iterations, and score each candidate by the sum of rewards predicted along its rollout. The current frame is encoded together with up to 24 preceding real frames, matching the clip length used in training. For each task we run one episode on each of 20 environment seeds, using the same seeds for all models and for a random policy that samples each action uniformly from [ _−_ 1 _,_ 1]. We report the normalized score ( _R − R_ random) _/_ ( _R_ expert _− R_ random), where _R_ is the episode return, _R_ random is the mean return of the random policy on the same seeds, and _R_ expert is the best return among the expert demonstrations of the task, so that the random policy scores 0 and the expert 1. Since MMBench2 does not state the anchors of its normalized score, our scores are not directly comparable to the values it reports. 

**Implementation Details.** CausalDreamer and the matched control are trained on clips of _T_ = 24 steps, sampled uniformly over all valid clip start positions of the corpus, so that tasks with more frames are sampled more often. The projections _fk_ , the decoder _Q_ and the reward predictor _h_ are trained with _L_ fac, with _λ_ = 0 _._ 1 in Eq. (7), for 30,000 optimizer steps of 256 clips (72 A100-40GB GPU-hours). Each projection _fk_ is a multilayer perceptron with three layers, and _Q_ is a residual multilayer perceptron, _Q_ ( _z_ ) = _z_ + _q_ ( _z_ ), whose last layer of _q_ is initialized to zero. The dynamics model is fine-tuned for 30,000 optimizer steps of 256 clips, for CausalDreamer (140 A100-40GB GPU-hours) and for the matched control (143 A100-40GB GPU-hours). The reward and behaviorcloning heads predict the rewards and actions of the next _M_ = 8 steps, and the agent tokens are initialized from frozen CLIP text embeddings [12] of each task’s embodiment and instruction. 

### **4.2 Planning on Clean Tasks** 

**CausalDreamer plans better than the pretrained model on clean tasks.** Over the ten clean tasks, CausalDreamer reaches a mean normalized score of 0 _._ 199, against 0 _._ 175 for the pretrained model (Table 1). The matched control, fine-tuned for the same number of steps on the tokenizer 

6 

||||Retur|n|||Normalized|score|
|---|---|---|---|---|---|---|---|---|
|Task|Expert|Random|Pretrained|Matched<br>control|CausalDreamer|Pretrained|Matched<br>control|CausalDreamer|
|cup-catch|1000.0|9.3|128.3|97.7|179.4|0.120|0.089|**0.172**|
|finger-turn-easy|1000.0|217.0|269.1|301.4|402.2|0.067|0.108|**0.237**|
|mw-push|1820.1|72.7|79.2|183.5|55.1|0.004|**0.063**|_−_0_._010|
|ms-push-cube|45.8|1.2|2.1|2.7|4.4|0.019|0.034|**0.072**|
|lunarlander-hover|469.2|58.6|84.3|53.9|73.7|**0.063**|_−_0_._011|0.037|
|og-point-maze|88.1|_−_96_._4|0.3|_−_25_._4|_−_22_._9|**0.524**|0.385|0.398|
|og-point-bottleneck|90.9|_−_79_._5|_−_3_._3|_−_11_._2|4.8|0.447|0.401|**0.494**|
|pygame-point-maze-var1|197.9|108.6|159.4|173.0|159.5|0.568|**0.721**|0.569|
|pygame-pong|4.0|_−_3_._2|_−_3_._9|_−_4_._3|_−_3_._2|_−_0_._083|_−_0_._145|**0.007**|
|pygame-bird-attack|110.0|_−_2_._8|_−_0_._6|0.0|_−_1_._5|0.020|**0.025**|0.012|
|Mean||||||0.175|0.167|**0.199**|


Table 1: **Clean tasks.** Mean episode return of the expert reference, a random policy, the pretrained model, the matched control and CausalDreamer, and the normalized score of each model (Section 4.1); higher is better. The best normalized score in each row is in bold. 

||||Return||Norm|alized score|
|---|---|---|---|---|---|---|
|Task|Expert|Random|Pretrained|CausalDreamer|Pretrained|CausalDreamer|
|cup-catch-var1|1000.0|9.3|97.0|182.8|0.088|**0.175**|
|finger-turn-easy-var1|1000.0|217.0|284.8|464.6|0.087|**0.316**|
|ms-push-banana|45.8|0.9|1.1|10.9|0.005|**0.222**|
|og-point-var1|88.4|_−_97_._7|_−_49_._4|_−_53_._0|**0.260**|0.240|
|og-point-var2|90.7|_−_79_._7|_−_13_._6|_−_17_._9|**0.388**|0.363|
|pygame-point-maze-var4|198.6|118.4|170.3|160.7|**0.647**|0.527|
|Mean (manipulated)|||||0.246|**0.307**|
|pygame-reacher-easy|199.0|1.1|24.9|7.7|**0.121**|0.034|
|pygame-dungeon-explorer1|488.8|21.2|28.9|15.4|**0.016**|_−_0_._012|
|pygame-foraging|85.9|55.9|53.0|45.6|_−_0_._095|_−_0_._341|
|pygame-whirlpool|41.5|_−_4_._2|_−_0_._9|0.4|0.072|**0.101**|
|Mean (new environments)|||||**0.028**|_−_0_._055|


Table 2: **Manipulated tasks and new environments.** The first six tasks are manipulated variants of a clean task, changing its background, manipulated object or maze layout; the last four are set in new environments. Neither set of tasks has training data. Columns as in Table 1. 

representation, reaches 0 _._ 167 on its first 10 seeds, below the pretrained model, so additional finetuning alone does not account for the improvement of CausalDreamer. It scores higher on six of the ten tasks, with the largest gains on finger-turn-easy (0 _._ 237 vs. 0 _._ 067), pygame-pong (0 _._ 007 vs. _−_ 0 _._ 083), ms-push-cube (0 _._ 072 vs. 0 _._ 019) and cup-catch (0 _._ 172 vs. 0 _._ 120), and lower on four, most clearly on og-point-maze (0 _._ 398 vs. 0 _._ 524). CausalDreamer scores above the random policy on nine of the ten tasks; the exception is mw-push, where both models remain within 0 _._ 01 of random actions. 

### **4.3 Planning on Manipulated Tasks and New Environments** 

**The improvement persists when a task is manipulated, most clearly under distractor backgrounds and a changed object.** On the six manipulated tasks, CausalDreamer reaches a mean normalized score of 0 _._ 307, against 0 _._ 246 for the pretrained model (Table 2). Under a distractor background, it scores higher on both tasks (cup-catch-var1: 0 _._ 175 vs. 0 _._ 088; finger-turn-easy-var1: 0 _._ 316 vs. 0 _._ 087), and with a changed object it reaches 0 _._ 222 on ms-push-banana, where the pretrained model stays at the level of random actions (0 _._ 005). On all three of these tasks, the margin over the pretrained model is larger than on the corresponding clean task. Under a changed maze layout, CausalDreamer scores lower on all three tasks, by 0 _._ 020 to 0 _._ 120. 

**Neither model transfers to new environments.** On the four tasks set in environments absent from training, neither model plans meaningfully better than a random policy (mean normalized scores of 0 _._ 028 for the pretrained model and _−_ 0 _._ 055 for CausalDreamer), with the largest deficit on pygame-foraging, where random actions already obtain about two thirds of the expert return. 

7 


Figure 3: **Effect of a background change on the representation.** (a) Frames of cup-catch and finger-turn-easy rendered from the same simulator state with the clean background and with the background of the manipulated variant. (b) Share of the change between the two renders that falls into the reward-irrelevant groups of the factored representation, and into the corresponding parts of the tokenizer representation; bars show the mean over 10 seeds, dots individual seeds, and the dashed line an equal split. 

The improvement of CausalDreamer is therefore confined to the clean tasks and their manipulated variants. 

### **4.4 Analysis of the Factored Representation** 

**The factored representation separates reward-irrelevant changes from its reward-relevant groups.** The reward predictor reads only the reward-relevant groups _Z_<sup>_AR_</sup> and _Z AR_<sup>¯</sup> (Eq. 6), so content that does not affect the reward should be represented in the reward-irrelevant groups _Z_<sup>_A_¯</sup> _R_ and _Z A_<sup>¯</sup> _R_<sup>¯</sup> and leave the reward-relevant groups unchanged. We test this by changing the background of a scene while keeping everything else fixed. For cup-catch and finger-turn-easy, we render each clean task and its manipulated variant from the same initial state under the same actions, so that both episodes pass through identical simulator states and receive identical rewards and differ only in the background (Figure 3a). We encode both episodes (10 seeds, 96 steps each) and measure which part of the representation changes, comparing the factored representation with the tokenizer representation _Vt_ split into four parts of the same size. In the factored representation, 79% (cup-catch) and 74% (finger-turn-easy) of the change falls into the reward-irrelevant groups, so the reward-relevant groups receive only 21% and 26% (Figure 3b). In the tokenizer representation, whose latent tokens each attend to the whole frame, the change is spread almost evenly, with 44% and 46% in the corresponding parts. 

## **5 Conclusion** 

We presented CausalDreamer, which re-encodes the latent of the frozen tokenizer of a pretrained generative world model into a factored representation of four groups, organized by controllability and reward relevance, and fine-tunes the pretrained dynamics model to predict this representation. In the factored representation, only the controllable groups receive the action and only the rewardrelevant groups predict the reward, so this structure is added after pretraining, with the tokenizer frozen and the architecture and losses of the dynamics model unchanged. On MMBench2, planning with CausalDreamer reaches a higher normalized score than the pretrained model on clean tasks seen during training and on manipulated variants of these tasks not seen during training, with the largest gains when the background or an object changes. In new environments, neither model plans meaningfully better than a random policy, so the improvement does not extend to environments absent from training. Our analysis shows that the factored representation separates reward-irrelevant changes from its reward-relevant groups: when only the background of a scene changes, most of the resulting change falls into the reward-irrelevant groups. 

8 

## **References** 

- [1] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [2] N. Hansen, H. Su, and X. Wang. TD-MPC2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [3] D. Hafner, W. Yan, and T. Lillicrap. Training agents inside of scalable world models. _arXiv preprint arXiv:2509.24527_ , 2025. 

- [4] T. Wang, S. S. Du, A. Torralba, P. Isola, A. Zhang, and Y. Tian. Denoised MDPs: Learning world models better than the world itself. _arXiv preprint arXiv:2206.15477_ , 2022. 

- [5] Y.-R. Liu, B. Huang, Z. Zhu, H. Tian, M. Gong, Y. Yu, and K. Zhang. Learning world models with identifiable factorization. _arXiv preprint arXiv:2306.06561_ , 2023. 

- [6] N. Hansen and X. Wang. Hallucination in world models is predictable and preventable. _arXiv preprint arXiv:2606.27326_ , 2026. 

- [7] X. Fu, G. Yang, P. Agrawal, and T. Jaakkola. Learning task informed abstractions. In _International Conference on Machine Learning_ , pages 3480–3491. PMLR, 2021. 

- [8] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _2018 IEEE/CVF conference on computer vision and pattern recognition_ , pages 586–595. IEEE, 2018. 

- [9] K. He, X. Chen, S. Xie, Y. Li, P. Doll´ar, and R. Girshick. Masked autoencoders are scalable vision learners. In _2022 IEEE/CVF conference on computer vision and pattern recognition (CVPR)_ , pages 15979–15988. IEEE, 2022. 

- [10] B. Chen, D. Mart´ı Mons´o, Y. Du, M. Simchowitz, R. Tedrake, and V. Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_ , 37:24081–24125, 2024. 

- [11] K. Frans, D. Hafner, S. Levine, and P. Abbeel. One step diffusion via shortcut models. In _International Conference on Learning Representations_ , volume 2025, pages 34668–34684, 2025. 

- [12] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR, 2021. 

- [13] G. Zhou, H. Pan, Y. LeCun, and L. Pinto. DINO-WM: World models on pre-trained visual features enable zero-shot planning. _arXiv preprint arXiv:2411.04983_ , 2024. 

- [14] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Komeili, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, et al. V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- [15] H. Nam, Q. Le Lidec, L. Maes, Y. LeCun, and R. Balestriero. Causal-JEPA: Learning world models through object-level latent masking. In _International Conference on Machine Learning (ICML)_ , 2026. arXiv:2602.11389. 

- [16] A. Stone, O. Ramirez, K. Konolige, and R. Jonschkowski. The distracting control suite–a challenging benchmark for reinforcement learning from pixels. _arXiv preprint arXiv:2101.02722_ , 2021. 

- [17] A. Zhang, R. McAllister, R. Calandra, Y. Gal, and S. Levine. Learning invariant representations for reinforcement learning without reconstruction. _arXiv preprint arXiv:2006.10742_ , 2020. 

9 

- [18] M. Pan, X. Zhu, Y. Wang, and X. Yang. Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. _Advances in neural information processing systems_ , 35: 23178–23191, 2022. 

- [19] A. Lamb, R. Islam, Y. Efroni, A. Didolkar, D. Misra, D. Foster, L. Molu, R. Chari, A. Krishnamurthy, and J. Langford. Guaranteed discovery of control-endogenous latent states with multi-step inverse models. _arXiv preprint arXiv:2207.08229_ , 2022. 

- [20] R. Islam, M. Tomar, A. Lamb, Y. Efroni, H. Zang, A. Didolkar, D. Misra, X. Li, H. Van Seijen, R. T. d. Combes, et al. Agent-controller representations: Principled offline rl with rich exogenous information. _arXiv preprint arXiv:2211.00164_ , 2022. 

- [21] B. Huang, C. Lu, L. Leqi, J. M. Hern´andez-Lobato, C. Glymour, B. Sch¨olkopf, and K. Zhang. Action-sufficient state representation learning for control with structural constraints. In _International Conference on Machine Learning_ , pages 9260–9279. PMLR, 2022. 

## **A Limitations and Future Work** 

The factorization is imposed only when the factored representation is learned on top of the tokenizer: the dynamics model is fine-tuned with its original architecture, so every group, not only the controllable ones, attends to the action when it is predicted, and the reward head of the dynamics model reads all four groups rather than only the reward-relevant ones. Making the dynamics model respect the same structure, for example with an attention mask that restricts the action and the reward head to the corresponding groups, is a direct next step. Within the factored representation itself, the routing of the action is an architectural choice without an objective of its own, and we do not evaluate whether the controllable groups capture the effect of the action. Our analysis covers changes that do not affect the reward, in two tasks, and does not test whether reward-relevant content is confined to the reward-relevant groups. The objective encourages reward information to enter the reward-relevant groups but does not penalize it in the reward-irrelevant groups; adding such a term, for example an independence or mutual-information penalty as used by prior factorization methods [5, 4], is a natural next step. Finally, the gains vary across tasks: CausalDreamer scores lower than the pretrained model when the maze layout changes, and we report means over 20 seeds per task without significance tests. 

## **B Related Work** 

**World models for control.** A key challenge is scale, since a world model that plans across many tasks must predict high-dimensional video under many action spaces. DreamerV3 learns a recurrent state-space model and trains a policy in imagination on over 150 tasks with a single configuration [1], and TD-MPC2 plans in the latent space of a decoder-free model and trains one 317M-parameter agent on 80 tasks [2]. Dreamer 4 scales this recipe to video by pairing a causal tokenizer, trained with masked autoencoding, with a block-causal transformer dynamics model trained with a shortcut forcing objective, and obtains diamonds in Minecraft from offline data alone [3]. MMBench2 trains a 350M-parameter Dreamer 4 world model on a 427-hour dataset of 210 tasks across ten domains, attributes its hallucinations mainly to gaps in data coverage, and evaluates it by model-predictive control with the cross-entropy method [6]. Our work keeps the MMBench2 model, data and planner unchanged and changes only the latent that its dynamics model predicts. 

**Planning on frozen representations.** A key challenge is that pixel prediction spends capacity on details a planner does not use, so recent world models predict in the feature space of a frozen encoder. DINO-WM plans in the patch features of a frozen DINOv2 encoder [13], and V-JEPA 2 plans with an action-conditioned predictor on top of a self-supervised video encoder [14]. Causal-JEPA groups frozen DINOv2 features into object slots and masks whole object trajectories during training, so that the predictor must infer an object’s state from the other objects [15]. It compares predictors that start from the same frozen embeddings on Push-T with CEM-based model-predictive control, 

10 

and its object-level masking raises success from 60.67% to 88.67% over an object-centric baseline while using about 1% of the latent features of the patch-based model. Like Causal-JEPA, our work adds structure on top of a frozen encoder and measures its effect by closed-loop planning, but the structure comes from how the latent responds to actions and rewards rather than from objects. 

**Factorized latent states.** A key challenge is that reward-irrelevant and uncontrollable variation, such as a moving background, enters the latent state and distracts the policy, as benchmarks with distracting backgrounds show [16]. Task Informed Abstractions train two models that jointly reconstruct the observation, one of which is adversarially kept from predicting reward [7], and deep bisimulation learns a representation in which states that yield the same rewards are mapped together [17]. Iso-Dream separates controllable and non-controllable dynamics into two branches of a world model [18], and inverse-dynamics objectives identify the controllable part of the latent state from data [19, 20]. ASR characterizes the minimal state that is sufficient for control by the causal structure among states, actions and rewards [21], Denoised MDPs sort information into four types by controllability and reward relevance and keep only the controllable, reward-relevant type [4], and IFactor models the same four categories with causal influences between them and proves that they are identifiable in blocks [5]. Its theory also shows that all reward-relevant variables are needed for policy learning, including the uncontrollable ones that Denoised MDPs discard. We adopt these four categories and route the action to the controllable ones, but we impose them on a pretrained tokenizer latent rather than learning a stochastic state from scratch. 

11 

