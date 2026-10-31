---
title: "Enhancing Policy Learning with World-Action Model"
date: "2026-03-30"
authors: "Yuci Han; Alper Yilmaz"
url: https://arxiv.org/abs/2603.28955
pdf: https://arxiv.org/pdf/2603.28955
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.28955)** / [論文ページ](https://arxiv.org/abs/2603.28955)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Enhancing Policy Learning with World-Action Model** 

Yuci Han<sup>1</sup> and Alper Yilmaz<sup>1</sup> 

**_Abstract_ — This paper presents the World-Action Model (WAM), an action-regularized world model that jointly reasons over future visual observations and the actions that drive state transitions. Unlike conventional world models trained solely via image prediction, WAM incorporates an inverse dynamics objective into DreamerV2 that predicts actions from latent state transitions, encouraging the learned representations to capture action-relevant structure critical for downstream control. We evaluate WAM on enhancing policy learning across eight manipulation tasks from the CALVIN benchmark. We first pretrain a diffusion policy via behavioral cloning on world model latents, then refine it with model-based PPO inside the frozen world model. Without modifying the policy architecture or training procedure, WAM improves average behavioral cloning success from 59.4% to 71.2% over DreamerV2 and DiWA baselines. After PPO fine-tuning, WAM achieves 92.8% average success versus 79.8% for the baseline, with two tasks reaching 100%, using** 8 _._ 7 _×_ **fewer training steps.** 

_Index Terms_ —Reinforcement Learning, Robotics and World Model, Diffusion Policy. 

## I. INTRODUCTION 

World models have become a critical tool for learning environment dynamics in robotics, allowing agents to plan and refine behaviors through imagined rollouts rather than expensive real-world interactions [1]–[5]. These models compress high-dimensional observations into compact latent spaces that capture the temporal and physical structures of environments, enabling sample-efficient policy learning through imagined experiences in latent space. Recent work has shown that policies trained entirely within learned world models can reach strong performance on robotic manipulation benchmarks [6]–[8], and in some cases transfer directly to physical hardware without further fine-tuning [9]. 

However, conventional world models are trained solely to predict future observations [1]–[4], [7], [9]. They forecast future visual states conditioned on past observations and actions, but never explicitly model the actions themselves. This asymmetry limits the quality of learned representations. The world model encodes each observation into a latent state _zt_ , which serves as the direct input to the downstream diffusion policy in model-based pipelines such as DiWA [8]—yet _zt_ is optimized only for pixel prediction and KL regularization, with no explicit pressure to encode action-relevant structure. Recent work on unified actionworld models [10] has begun to address this gap by jointly generating actions and images within a single autoregressive architecture, but these approaches rely on large foundation models and fundamentally redesign the architecture rather 

> 1Yuci Han and Alper Yilmaz are with the Photogrammetry and Computer Vision Lab, The Ohio State University, Columbus, OH 43210, USA. _{_ han.1489, yilmaz.15 _}_ @osu.edu 

than improving the representations learned by existing world models. 

We take a different and complementary approach: rather than redesigning the architecture, we augment the training objective of DreamerV2 [4] with an inverse dynamics head that predicts actions from consecutive encoder embeddings, regularizing the learned representations toward actionrelevant structure. We argue that requiring the model to predict the action that caused a given state transition forces the encoder to capture fine-grained information about how the environment responds to agent behavior. This information is critical for downstream policy learning but is overlooked when the training signal comes only from observation reconstruction. This idea draws on inverse dynamics models in self-supervised representation learning [11], [12], where predicting actions between consecutive states yields representations focused on controllable aspects of the environment while filtering out task-irrelevant distractors. 

We present the World-Action Model (WAM) and evaluate it on enhancing policy learning across eight manipulation tasks from the CALVIN benchmark [13]. We first pretrain a diffusion policy via behavioral cloning on world model latents, then refine it with model-based PPO using the frozen world model as a simulator. Compared to the DiWA baseline [8], WAM improves average behavioral cloning success from 59.4% to 71.2% and achieves 92.8% average success after PPO fine-tuning versus 79.8%, with two tasks reaching 100%, using 8 _._ 7 _×_ fewer training steps. 

Our main contributions are: 

- We present WAM, a lightweight extension of DreamerV2 that augments the training objective with an inverse dynamics head, explicitly regularizing latent representations toward action-relevant structure. 

- We demonstrate that action regularization improves world model generation quality on the CALVIN benchmark. WAM matches or exceeds DreamerV2 [4] on LPIPS, PSNR, SSIM, and FVD with fewer training steps. 

- We show that the improved representations enhance downstream policy learning, outperforming the DiWA baseline on both behavioral cloning and PPO fine-tuning across all eight tasks on the CALVIN benchmark. 

II. RELATED WORKS 

## _A. World Models_ 

World models learn a predictive representation of environment dynamics, enabling agents to optimize policies through imagined trajectories without requiring additional real-world 


Fig. 1: (a) Standard world models predict only future observations, treating actions solely as conditioning inputs. (b) Our World-Action Model adds an inverse dynamics head that jointly predicts observations and actions during training. (c) The action-aware world model serves as a learned simulator for offline policy fine-tuning via PPO. 

data collection. Ha and Schmidhuber [1] introduced an early approach encoding observations into a latent space with an RNN for dynamics modeling. PlaNet [2] proposed the Recurrent State-Space Model (RSSM), combining deterministic and stochastic components for long-horizon prediction. The Dreamer series [3]–[5] progressively extended RSSMbased latent imagination for behavior learning. DreamerV2 replaced Gaussian latents with categorical representations, while DreamerV3 introduced robustness techniques that allowed a single set of hyperparameters to work across diverse domains. However, these world models are trained purely as observation predictors without explicitly reasoning about the actions that drive state transitions. Our work introduces action regularization into the world model, jointly predicting both actions and future observations to better capture environment dynamics. 

## _B. World Models for Policy Learning_ 

Beyond modeling dynamics, world models can be directly used as complementary environments for policy optimization, where agents learn behaviors through imagined rollouts within the learned model. The Dreamer series [3]–[5] first demonstrated that actor-critic policies can be trained entirely through imagined latent rollouts, and DayDreamer [9] demonstrated this paradigm on physical robots. In offline settings, DITTO [6] proposed imitation learning by optimizing a distance metric in a frozen world model’s latent space, and LUMOS [7] extended this to language-conditioned multitask learning. DiWA [8] fine-tuned diffusion policies via PPO within a learned world model, achieving sample efficiency orders of magnitude beyond model-free baselines. More recently, WMPO [14] introduced pixel-based world models for on-policy GRPO optimization of Vision-LanguageAction models, and World4RL [15] employed diffusionbased world models for end-to-end policy refinement. While these works confirm the effectiveness of world-model-based 

policy learning, they rely on world models trained solely for observation prediction. Our approach enriches the world model with action prediction, providing a stronger training signal for downstream policy optimization. 

## III. METHOD 

## _A. World-Action Model_ 

We propose to regularize the world model with an inverse dynamics objective, producing representations that are simultaneously predictive of visual dynamics and aware of the actions driving state transitions. 

_1)_ **_World Model Backbone_** _:_ WAM builds on the RSSM architecture from DreamerV2 [4]. A dual-stream CNN encoder processes static and gripper camera images, fusing them with proprioceptive state to produce embeddings _et ∈_ R<sup>1554</sup> . The RSSM models latent dynamics through: 


where _ht_ is the deterministic recurrent state, _zt_ is a stochastic categorical variable (32 _×_ 32), and _ft_ = [ _ht_ ; _zt_ ] _∈_ R<sup>2048</sup> is the combined latent feature used for decoding and policy learning. 

_2)_ **_Action-Regularized World Model_** _:_ The observationonly objective (Eq. 4) produces features optimized for pixel reconstruction, potentially discarding action-relevant information. WAM addresses this by augmenting the world model with an inverse dynamics component, yielding a unified model _Mθ_ with two pathways: 


Fig. 2: **WAM architecture.** Observations _xt_ are encoded and produce posterior _zt_ , which is regularized toward the prior _z_ ˆ _t_ via KL divergence. The inverse dynamics head predicts actions _a_ ˆ _t_ from consecutive encoder embeddings, cascading action-aware structure through the posterior to the prior. The decoder reconstructs observations _x_ ˆ _t_ and a reward estimator provides task-completion signals for policy fine-tuning. 

where _M_<sup>world</sup> _θ_ denotes the RSSM pathway (Eqs. 1–4) and _M_<sup>action</sup> _θ_ is an inverse dynamics head: 


with _ψ_ a three-layer MLP and [ _·_ ; _·_ ] denoting concatenation. A critical design in WAM is the cascading effect created by the action head through the full model. We operate on encoder embeddings _et_ rather than RSSM features _ft_ , since _ft_ receives _at−_ 1 through the GRU (Eq. 1) and would make action prediction trivially solvable. By regularizing the encoder directly, the action-aware structure in _et_ cascades forward: it shapes the posterior _zt ∼ qϕ_ ( _zt | ht, et_ ), which the KL loss propagates to the prior _z_ ˆ _t ∼ pϕ_ ( _zt | ht_ ), and ultimately reaches the diffusion policy through imagined rollouts generated from _z_ ˆ _t_ . This chain ensures that the action prediction signal at the encoder level translates into more informative features for downstream control. As illustrated in Fig. 2, the action-aware structure cascades from the encoder through the posterior to the prior across timesteps. **Training Objective.** WAM is trained end-to-end by minimizing: 


where _L_ KL = KL� _qϕ_ ( _zt | ht, et_ ) _∥ pϕ_ ( _zt | ht_ )�, _L_ recon = _∥ot − o_ ˆ _t∥_<sup>2</sup> 2<sup>,and</sup><sup>_L_action=</sup><sup>_∥a_ˆ</sup><sup>_t−at∥_1.Wecarefullytunethe</sup> loss coefficients to balance the trade-off between reconstruction quality and action prediction, ensuring that the encoder learns representations that serve both objectives effectively. 

_B. Enhancing Downstream Policy Learning with WAM_ 

After world model training, we leverage WAM to enhance downstream policy learning. The frozen WAM defines a latent space MDP _M_ wm = ( _Z, A, Pϕ, Rψ, γ_ ), where _Z_ is WAM’s latent space, _Pϕ_ the learned dynamics, and _Rψ_ a learned reward classifier. We extract features _ft ∈_ R<sup>2048</sup> from expert demonstrations _D_ exp (50 episodes per task) and train a diffusion-based policy in two stages: behavioral cloning followed by optional offline RL fine-tuning. 

**Behavioral Cloning.** We freeze the WAM and extract features _ft ∈_ R<sup>2048</sup> from expert demonstrations _D_ exp. Following DiWA [8], we adopt a DiffusionMLP policy _πθ_ ( _at | ft_ ) that generates actions by iteratively denoising Gaussian noise through _K_ steps: 


where _a_<sup>_K_</sup> _t_<sup>_∼N_(0</sup><sup>_, I_)and</sup><sup>_a_0</sup> _t_<sup>arethepredictedactions.The</sup> policy is trained by minimizing the denoising objective: 


The key advantage of WAM is the cascading effect: the action-regularized encoder produces action-aware _et_ , which conditions the posterior _zt ∼ qϕ_ ( _zt | ht, et_ ), yielding latent features _ft_ = [ _ht_ ; _zt_ ] that encode richer action-relevant information. The diffusion policy trained on these features directly benefits from this improved representation. 

**Offline Policy Fine-tuning.** After behavioral cloning, we further improve the policy using DPPO [16] entirely within the frozen world model’s latent space, requiring no physical interactions. During imagined rollouts, observations are unavailable, so the model relies on the prior _z_ ˆ _t ∼ pϕ_ ( _zt | ht_ ) to generate latent states. The cascading effect of WAM is critical here: the action-regularized encoder shapes the posterior _zt_ during training, and the KL loss propagates this action-aware structure to the prior _z_ ˆ _t_ , ensuring that imagined rollouts benefit from action-relevant representations. At each iteration, 50 parallel imagined rollouts are generated within _M_ wm using the current policy. The fine-tuning objective maximizes: 


where _Rψ_ is a binary reward classifier. Since WAM produces different latent representations than the baseline DreamerV2, we retrain the reward classifiers on WAM features following DiWA’s pipeline [8]. All 8 classifiers achieve _≥_ 0.97 precision and 1.00 recall, confirming reliable reward estimation in WAM’s latent space. The policy is updated via clipped PPO. During rollouts, the diffusion policy uses 10 denoising steps with BC regularization ( _α_ BC =0 _._ 025) to prevent catastrophic forgetting. As illustrated in Fig. 2, the action-aware structure propagates from the encoder through the prior to the imagined rollouts, benefiting both policy optimization and reward estimation during offline adaptation. 


Fig. 3: **Qualitative comparison of imagined rollouts on the CALVIN benchmark.** We visualize predicted frames at selected timesteps from both static and gripper cameras. Compared to DreamerV2, our WAM produces more realistic future state predictions across the entire rollout horizon. 

## IV. EXPERIMENTS 

In our experiments, we aim to study the following questions: 

- Does the action regularization strategy effectively enhance the performance of WAM compared to the regular world model? 

_•_ Does WAM, with its action-regularized representations, improve downstream policy learning in both offline behavioral cloning and online RL fine-tuning? We conduct experiments on **the CALVIN benchmark** environment D [13], a tabletop manipulation benchmark with a 7-DoF Franka Emika Panda robot. The benchmark provides 6 hours of teleoperated play data ( _∼_ 500K transitions). Observations consist of 64 _×_ 64 RGB images from static and gripper cameras. We train WAM on the play data and evaluate it on eight manipulation tasks. 

_A. Action Regularization Enhances WAM._ 

_1)_ **_Baselines_** _:_ We assess generation quality by comparing WAM against the baseline world model DreamerV2 [17]. We sample 100 random sequences from the CALVIN validation 

set and perform 50-step open-loop imagination rollouts, conditioned on the first ground-truth observation and using ground-truth actions. We report PSNR, SSIM, LPIPS [18], and FVD [19] to evaluate generation quality. 

_2)_ **_Training Settings_** _:_ We use a sequence length of _T_ = 50, a batch size of 500, and a learning rate of 3 _×_ 10<sup>_−_4</sup> with AdamW (weight decay 0 _._ 05). The KL balance coefficient is set to _α_ = 0 _._ 8, with loss weights _λ_ KL = 3 _._ 0, _λ_ img = 1 _._ 0, and _λ_ act = 1000 _._ 0. The action prediction loss uses L1 regression. WAM is trained for only 230K gradient steps on _∼_ 512K play frames from the CALVIN dataset, roughly 8 _._ 7 _×_ fewer than the 2M steps used by the baseline DreamingV2, while still achieving stronger downstream policy performance. 

_3)_ **_Results_** _:_ Table I presents the quantitative evaluation of generation quality on the CALVIN benchmark. Our WorldAction Model consistently outperforms the DreamingV2 baseline across all four metrics (PSNR, SSIM, LPIPS, FVD). These improvements stem from the inverse dynamics head added during training, which regularizes the encoder to retain action-relevant information in its latent representations. By 

TABLE I: **Quantitative evaluation of imagination quality on the CALVIN benchmark.** We report standard video prediction metrics between our World-Action Model (WAM) and the baseline (DreamerV2). 

|Metric|Ours (WAM)|Baseline (DreamerV2)|
|---|---|---|
|PSNR _↑_|**22.10** _±_ **2.22**|21.66 _±_ 2.20|
|SSIM _↑_|**0.814** _±_ **0.061**|0.807 _±_ 0.067|
|LPIPS _↓_|**0.144** _±_ **0.072**|0.149 _±_ 0.073|
|FVD _↓_|**10.82**|12.13|


TABLE II: **Baseline comparison.** For downstream policy learning, we share the same policy architecture and training pipeline as DiWA, differing only in the world model. 

||DiWA|Ours|
|---|---|---|
|World Model|DreamerV2|WAM|
|Diffusion Policy|DiffusionMLP|DiffusionMLP|


requiring the model to predict the action that caused each state transition, the encoder learns to capture not only visual appearance but also the causal structure underlying the observations, leading to more faithful future state generation. 

Figure 3 provides a qualitative comparison of generated rollouts from both the static and gripper cameras. Compared to DreamingV2, our WAM produces more realistic future state predictions across the entire rollout horizon, with better preservation of object shapes, finer details, and more accurate colors, while DreamingV2 shows noticeable color drift and distorted object shapes. 

## _B. Enhancing Policy Learning with WAM_ 

_1)_ **_Baselines_** _:_ We evaluate WAM on downstream policy learning by comparing against DiWA [8]. As summarized in Table II, both methods follow the same pipeline of world model pretraining, behavioral cloning, and optional online fine-tuning, with an identical policy architecture (DiffusionMLP). We report behavioral cloning success rates and online RL fine-tuning efficiency. 

_2)_ **_Behavioral Cloning Training Settings_** _:_ Following the DiWA pipeline, we first pretrain the diffusion policy via behavioral cloning. Both DiWA and our method use the same frozen encoder and RSSM to extract _ft ∈_ R<sup>2048</sup> features from 50 expert demonstrations per task. The downstream policy is a DiffusionMLP with _K_ = 20 denoising steps and action horizon _Ta_ =4, trained for 5,000 epochs with a batch size of 256, a learning rate of 10<sup>_−_4</sup> (cosine decay to 10<sup>_−_5</sup> ), weight decay of 10<sup>_−_6</sup> , and EMA with a decay of 0.995. The only difference between the two conditions is which world model provides the features. 

_3)_ **_Online Policy Fine-tuning Settings_** _:_ Following DiWA [8], we fine-tune the BC-pretrained diffusion policies using DPPO [16] entirely within the frozen world model’s latent space, requiring no physical interactions during policy optimization. At each iteration, the current policy generates 50 parallel imagined rollouts within the frozen world 

TABLE III: Behavioral Cloning (BC) success rates (%) on 8 CALVIN manipulation tasks. Both methods use identical diffusion policy architectures and training procedures; the only difference is the world model used for feature extraction. 

|**Task**|**DiWA**|**WAM (Ours)**|
|---|---|---|
|close<br>~~d~~rawer|58_._6_±_4_._2|**89**_._**7**_±_**3**_._**1**|
|open<br>~~d~~rawer|53_._3_±_5_._1|**73**_._**3**_±_**4**_._**8**|
|move<br>~~s~~lider<br>~~l~~eft|50_._0_±_3_._7|**68**_._**8**_±_**5**_._**2**|
|move<br>~~s~~lider<br>~~r~~ight|51_._7_±_4_._5|**82**_._**8**_±_**3**_._**9**|
|turn<br>~~o~~n<br>~~l~~ightbulb|42_._4_±_3_._3|**51**_._**5**_±_**4**_._**6**|
|turn<br>~~o~~ff<br>~~l~~ightbulb|3_._4_±_1_._8|**17**_._**2**_±_**3**_._**4**|
|turn<br>~~o~~n<br>~~l~~ed|**44**_._**8**_±_**3**_._**9**|41_._4_±_4_._1|
|turn<br>~~o~~ff<br>~~l~~ed|62_._5_±_5_._3|**68**_._**8**_±_**4**_._**7**|
|**Average**|45_._8|**61**_._**7**|


model’s latent space. The policy is updated via a clipped PPO surrogate objective with a batch size of 7,500, 10 update epochs per iteration, actor learning rate 10<sup>_−_5</sup> , critic learning rate 10<sup>_−_3</sup> , _γ_ = 0 _._ 999, and GAE _λ_ = 0 _._ 95. During rollouts, the diffusion policy uses 10 denoising steps with BC regularization ( _α_ BC = 0 _._ 025) to prevent catastrophic forgetting. Fine-tuning runs for 800 iterations with evaluation every 25 iterations. 

Crucially, since the WAM encoder produces different latent representations than the baseline DreamerV2, we retrain the reward classifiers on WAM features following DiWA’s full pipeline: (1) featurize the entire CALVIN play dataset with the WAM encoder, (2) extract matched features and raw states from the same 50 expert episodes per task (seed 42), (3) generate ground-truth reward labels by replaying expert actions in the CALVIN simulator, (4) augment training data with imagined rollouts inside the WAM, (5) balance class distribution, and (6) train contrastive reward classifiers. All 8 classifiers achieve _≥_ 0.97 precision and 1.00 recall on training data, confirming reliable reward estimation in WAM’s latent space. 

_4)_ **_Behavioral Cloning Results_** _:_ Each policy is evaluated on 29 held-out initial configurations per task. The frozen world model encodes the current observation into _ft_ , and the policy generates a 4-step action chunk via DDPM sampling (up to 18 decision points per episode, 72 max steps). An episode succeeds if CALVIN’s built-in task checker confirms completion. Table III reports results across all eight CALVIN tasks. WAM outperforms the DiWA baseline on 7 out of 8 tasks, achieving an average success rate of 61.7% compared to 45.8%. The largest gains appear on tasks involving articulated objects: _close_ _~~d~~ rawer_ (+31.1pp), _move_ _~~s~~ lider_ _~~r~~ ight_ (+31.1pp), and _open_ _~~d~~ rawer_ (+20.0pp), where precise position control is critical, and the encoder must capture fine-grained spatial cues that distinguish successful manipulation trajectories. The only task where the baseline marginally outperforms WAM is _turn_ _~~o~~ n_ _~~l~~ ed_ (44.8% vs. 41.4%), which we attribute to evaluation variance given the small number of test episodes. These results confirm that by jointly training on action prediction and state prediction, 

TABLE IV: Diffusion policy success rates (%) on 8 CALVIN tasks after 800 iterations of model-based PPO fine-tuning. DPPO columns report environment steps required to match DiWA performance (lower = more sample-efficient). 


Fig. 4: Behavioral cloning evaluation curves across all eight CALVIN tasks. WAM (orange) consistently reaches higher success rates than DiWA (blue) and converges faster on most tasks. 

WAM learns representations that are more informative for downstream imitation learning without any modification to the policy architecture or training procedure. 

Figure 4 shows the evaluation curves during BC training across all eight tasks. WAM consistently reaches higher success rates than DiWA and converges faster on most tasks. _5)_ **_Diffusion Policy Fine-tuning Results_** _:_ Table IV reports the results. After 800 iterations of fine-tuning, WAM reaches a 92.8% average success rate across all eight tasks, outperforming DiWA (79.8%) by 13.0 percentage points. WAM outperforms DiWA on every task, with _turn_ _~~o~~ n_ _~~l~~ ightbulb_ and _turn_ _~~o~~ ff_ _~~l~~ ed_ reaching 100% success. The largest gains appear on _open_ _~~d~~ rawer_ (96.7% vs. 70.0%) and _turn_ _~~o~~ n_ _~~l~~ ed_ (96.6% vs. 86.2%), suggesting that actionregularized representations provide a better optimization landscape for policy fine-tuning within the world model. Combined with the BC results, these findings demonstrate that WAM features benefit both offline imitation and online policy adaptation. 

These results show that jointly training on action and state prediction not only improves BC policy quality (61.7% 

vs. 45.8% average) but also provides a stronger starting point for model-based RL fine-tuning (92.8% vs. 79.8% average), yielding a 13.0 percentage point gain over DiWA with the same policy architecture and 8 _._ 7 _×_ fewer world model training steps. 

## V. CONCLUSION 

We presented the World-Action Model (WAM), a world model augmented with an inverse dynamics objective that regularizes learned representations toward action-relevant structure. The key insight is that under standard reconstruction objectives, the latent state _zt_ fed to the downstream diffusion policy is never explicitly trained to be actioninformative. By jointly predicting actions and future states, WAM propagates action-relevant gradients through the representation pathway, improving the quality of _zt_ for downstream control. Experiments on eight CALVIN manipulation tasks show that WAM improves behavioral cloning success from 45.8% to 61.7% and model-based RL fine-tuning from 79.8% to 92.8%, while using 8 _._ 7 _×_ fewer world model 

## training steps than the baseline. 

## REFERENCES 

- [1] D. Ha and J. Schmidhuber, “Recurrent world models facilitate policy evolution,” in _Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 31, 2018, pp. 2451–2463. 

- [2] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” in _International Conference on Machine Learning (ICML)_ , 2019, pp. 2555–2565. 

- [3] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _International Conference on Learning Representations (ICLR)_ , 2020. 

- [4] D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” in _International Conference on Learning Representations (ICLR)_ , 2022. 

- [5] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse control tasks through world models,” _Nature_ , vol. 640, pp. 647–653, 2025. 

- [6] B. DeMoss, P. Duckworth, J. Foerster, N. Hawes, and I. Posner, “Ditto: Offline imitation learning with world models,” in _International Conference on Learning Representations (ICLR)_ , 2025. 

- [7] I. Nematollahi, B. DeMoss, A. L. Chandra, N. Hawes, W. Burgard, and I. Posner, “Lumos: Language-conditioned imitation learning with world models,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025, pp. 8219–8225. 

- [8] A. L. Chandra, I. Nematollahi, C. Huang, T. Welschehold, W. Burgard, and A. Valada, “Diwa: Diffusion policy adaptation with world models,” in _Conference on Robot Learning (CoRL)_ , 2025. 

- [9] P. Wu, A. Escontrela, D. Hafner, K. Goldberg, and P. Abbeel, “Daydreamer: World models for physical robot learning,” in _Conference on Robot Learning (CoRL)_ , 2022. 

- [10] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang, D. Zhao, and H. Chen, “WorldVLA: Towards autoregressive action world model,” _arXiv preprint arXiv:2506.21539_ , 2025. 

- [11] D. Pathak, P. Agrawal, A. A. Efros, and T. Darrell, “Curiosity-driven exploration by self-supervised prediction,” in _International Conference on Machine Learning (ICML)_ , 2017, pp. 2778–2787. 

- [12] B. Baker, I. Akkaya, P. Zhokov, J. Huizinga, J. Tang, A. Ecoffet, B. Houghton, R. Sampedro, and J. Clune, “Video pretraining (VPT): Learning to act by watching unlabeled online videos,” in _Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 35, 2022, pp. 24 639–24 654. 

- [13] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _IEEE Robotics and Automation Letters (RAL)_ , vol. 7, no. 3, pp. 7327–7334, 2022. 

- [14] F. Zhu, Z. Yan, Z. Hong, Q. Shou, X. Ma, and S. Guo, “Wmpo: World model-based policy optimization for vision-language-action models,” _arXiv preprint arXiv:2511.09515_ , 2025. 

- [15] Z. Jiang _et al._ , “World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation,” _arXiv preprint arXiv:2509.19080_ , 2025. 

- [16] A. Z. Ren, J. Lidard, L. Ankile, A. Simeonov, P. Agrawal, A. Majumdar, B. Burchfiel, H. Dai, and M. Simchowitz, “Diffusion policy policy optimization,” _ArXiv_ , vol. abs/2409.00588, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID: 272368064 

- [17] M. Okada and T. Taniguchi, “DreamingV2: Reinforcement learning with discrete world models without reconstruction,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2022, pp. 985–991. 

- [18] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The unreasonable effectiveness of deep features as a perceptual metric,” in _2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . Salt Lake City, UT: IEEE, 2018, p. 586–595. [Online]. Available: https://ieeexplore.ieee.org/document/8578166/ 

- [19] T. Unterthiner, S. van Steenkiste, K. Kurach, R. Marinier, M. Michalski, and S. Gelly, “Towards accurate generative models of video: A new metric & challenges,” _ArXiv_ , vol. abs/1812.01717, 2018. [Online]. Available: https://api.semanticscholar.org/CorpusID: 54458806 

