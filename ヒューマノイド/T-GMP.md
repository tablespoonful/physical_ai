---
title: "T-GMP: Terrain-conditioned Generative Motion Priors for Versatile and Natural Humanoid Locomotion"
date: "2026-06-05"
authors: "Junhong Guo; Hao Hu; Chen Chen; Haoxuan Han; Linao Gong; Xin Yang"
url: https://arxiv.org/abs/2606.06944
pdf: https://arxiv.org/pdf/2606.06944
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.06944)** / [論文ページ](https://arxiv.org/abs/2606.06944)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **T-GMP: Terrain-conditioned Generative Motion Priors for Versatile and Natural Humanoid Locomotion** 

**Junhong Guo**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> **Hao Hu**<sup>1</sup><sup>_,∗_</sup> **Chen Chen**<sup>1</sup> **Haoxuan Han**<sup>1</sup> **Linao Gong**<sup>1</sup> **Xin Yang**<sup>1</sup> **Zhicheng He**<sup>1</sup><sup>_,_2</sup> **Yao Su**<sup>2</sup> **Fenghua He**<sup>1</sup><sup>_,†_</sup> 

1 Harbin Institute of Technology 

2 Leju Robotics 

> _∗_ Equal contribution; order decided by coin toss. _†_ Corresponding author. 


Figure 1: T-GMP enables robots to exhibit versatile and natural behaviors across diverse terrains. Trained only once, the robot learns terrain-adaptive whole-body coordination strategies, including natural arm swinging during walking, lowering the center of mass (CoM) on stairs and slopes, and extending its arms for balance when crossing gaps or narrow beams. Videos are available on our project website: https://t-gmp.github.io. 

**Abstract:** Achieving both anthropomorphic naturalness and rich motion diversity during terrain traversal remains a fundamental challenge in humanoid locomotion. Existing reinforcement learning approaches typically rely on fixed motion priors, limiting their adaptability to varying environments. We propose Terrainconditioned Generative Motion Priors (T-GMP), a module that captures a terrainconditioned latent motion manifold from a few expert state-terrain demonstrations. The learned priors enable smooth style transitions, facilitating a unified policy that adapts to terrain variations. We integrate T-GMP into an adversarial learning pipeline, where a discriminator dynamically modulates naturalness constraints conditioned on local terrain features, guiding the generation of versatile and human-like motions. We further introduce a Foothold Penalty to promote safe foot placement on challenging terrains. Experimental results demonstrate that T- GMP outperforms existing baselines in motion naturalness, motion diversity, and traversal success rates, while preserving physically coordinated motions. 

**Keywords:** Generative Motion Priors, Adversarial Learning, Humanoid Robot. 

## **1 Introduction** 

The pursuit of versatile and human-like locomotion in humanoid robots is a fundamental goal in robotics, bridging the gap between mechanical efficiency and biological elegance. While Reinforcement Learning (RL) approaches have achieved remarkable success in enabling robots to locomote robustly [1, 2, 3, 4] and traverse challenging terrains [5, 6, 7, 8], the resulting motions often exhibit “robotic” artifacts—stiffness, unnatural joint configurations, or a lack of biological plausibility. This is primarily because hand-crafted reward functions are often insufficient to capture the nuanced dynamics of human balance, especially when the robot must simultaneously optimize task objectives (e.g., velocity tracking) and stylistic constraints across diverse terrains. 

To improve motion quality, mimic-based approaches [9, 10, 11, 12] have been widely adopted to distill “naturalness” and “agility” from motion capture (MoCap) data into policies, enabling robots to demonstrate highly dynamic skills such as jumping, dancing, and backflipping. However, when a robot encounters complex terrains, fixed and terrain-agnostic motion priors penalize the necessary deviations required for physical stability. This creates a fundamental conflict between task completion and style preservation, often leading to stiff gaits or failure under varying environments. 

To address these limitations, we propose T-GMP, a module designed for adaptive and anthropomorphic humanoid locomotion. Our core insight is that human motion is intrinsically linked to the environment; therefore, a motion prior should not be a static template but a dynamic manifold conditioned on terrain features. By utilizing a Conditional Variational Autoencoder (CVAE), T-GMP learns a terrain-conditioned latent motion manifold from a few expert state-terrain demonstrations. This enables the robot to learn how anthropomorphic motion styles adapt to different environments and achieve smooth style transitions across varying terrains. 

Furthermore, we integrate T-GMP into a unified adversarial RL framework, where the proposed terrain-conditioned discriminator injects terrain-aware anthropomorphic motion-style constraints into policy learning. To improve foothold stability on complex terrains, we further introduce a Foothold Penalty that explicitly regularizes foot-terrain contact quality, thereby enhancing locomotion robustness. Experimental results demonstrate that the proposed method generates coordinated and anthropomorphic whole-body behaviors across diverse terrains, while significantly outperforming baselines in motion smoothness, motion diversity and traversal success rates. 

Overall, our contributions can be summarized as follows: 

- 1) We propose T-GMP, a module that learns a terrain-conditioned latent motion manifold from a few expert state-terrain demonstrations, enabling the generation of terrain-adaptive motion priors. 

- 2) By introducing a terrain-conditioned discriminator, we integrate T-GMP into a unified adversarial RL pipeline that jointly optimizes task objectives and motion style constraints. 

- 3) We conduct real-world experiments on a full-size humanoid robot across eight terrains, demonstrating diverse, coordinated, and anthropomorphic whole-body behaviors. Simulation experiments on multiple unseen terrains further demonstrate the generalization of the learned policy. 

## **2 Related Works** 

**Legged Locomotion** Recent advancements in humanoid locomotion have seen a transition from proprioceptive-only methods to perception-aware approaches. While proprioceptive-only methods [13, 14, 15, 16, 2] demonstrate impressive robustness through proprioceptive feedback, they are limited by a reactive control loop that may cause hardware damage during abrupt terrain changes. Conversely, perception-aware policies utilize depth sensors [17, 18, 19, 20, 21, 22, 23] or LiDAR [24, 25, 26, 27, 28, 29] to construct egocentric terrain representations and enable proactive maneuvers. However, existing perception-driven methods predominantly focus on lower-limb stability and gait scheduling, frequently overlooking the whole-body coordination potential inherent in the humanoid form. Our work addresses this gap by phrasing locomotion as a terrain-conditioned whole-body coordination task. By integrating perception with generative motion priors, our frame- 

2 

work enables the robot to autonomously recruit its entire skeletal structure, including arms and torso, to maintain stability over challenging terrains. 

**Generative Motion Priors** Leveraging human motion priors to enhance anthropomorphic locomotion has become a prevailing direction in recent robotics research. Mimic-based approaches [9, 30, 31] directly track human MoCap data, enabling robots to exhibit natural and versatile skills. However, such methods typically rely on fixed reference trajectories, which limit their ability to generalize to multi-terrain traversal scenarios with complex and varying conditions. To improve generalization, subsequent studies abstract human motion priors into transferable motion styles that guide policies to produce human-like behaviors [32, 33, 34, 10, 35, 36]. Although these methods partially alleviate the dependence on a single reference trajectory, the underlying motion priors are still fixed, making it difficult to adapt to diverse terrains. More recently, generative motion priors [37, 38, 39, 40] have been introduced to model richer motion distributions, enabling robots to exhibit natural motion styles and smooth style transitions. We further integrate generative motion priors with terrain perception, generating motion priors conditioned on local terrain features during the locomotion policy training process. Moreover, we employ a terrain-conditioned discriminator to distill the motion priors into the policy during training, enabling natural and smooth anthropomorphic locomotion across various terrains. 

## **3 Terrain-conditioned Generative Motion Priors** 

### **3.1 Data Collection** 

We develop a data collection pipeline to construct a natural, diverse, and physically feasible expert state–terrain dataset. For each terrain _i_ in the terrain set _I_ , we first set up the corresponding terrain in a motion-capture studio and record human MoCap data, resulting in a terrain-specific MoCap dataset _{Di_<sup>mocap</sup> _}i∈I_ . We then retarget these motions to the robot joint space using GMR [41], yielding a set of natural and diverse robot motion references _{Di_<sup>robot</sup> _}i∈I_ . However, the retargeted motions may contain physically infeasible artifacts, such as floating feet and excessive body tilt. To mitigate these artifacts while facilitating the collection of state-terrain data, we use _Di_<sup>robot</sup> as motion priors and train a privileged expert policy _πi_<sup>priv</sup> separately on each terrain _i_ . 

We roll out the trained policy _πi_<sup>priv</sup> to collect state–terrain sequences _{_ ( _st, ht_ ) _}_<sup>_L_</sup> _t_ =1<sup>, where</sup><sup>_L_denotes</sup> the trajectory length. The expert state is defined as: 


where _qt_ and _q_ ˙ _t_ denote joint positions and velocities, and _pt_ denotes end-effector positions relative to the root frame. The perceptual observation _ht_ is the local height map. By aggregating the state–terrain sequences collected across all terrains, we construct a high-quality expert dataset _D_ that captures natural and diverse motions while satisfying the robot’s physical constraints. Implementation details of privileged expert training and state–terrain data collection are provided in Section A. 

### **3.2 Terrain-conditioned Generative Motion Priors** 

We adopt a CVAE to model multi-style motion distributions, and use its decoder as T-GMP. To explicitly incorporate terrain-conditioned information, we employ a two-layer CNN _f_ cnn<sup>cto extract</sup> features from the local height map _ht_ , yielding a terrain embedding _h_<sup>emb</sup> _t_<sup>_,_c</sup> = _f_ cnn<sup>c(</sup><sup>_ht_).Building</sup> on this representation, we extend the standard _β_ -VAE [42] to a conditional _β_ -VAE formulation. The CVAE decoder conditions on the terrain embedding _h_<sup>emb</sup> _t_<sup>_,_c</sup> , together with a latent variable _zt_ sampled from the prior distribution _p_ ( _zt_ ), generates expert state trajectory sequences, which exhibit diverse motion styles across different terrains: 


3 


Figure 2: **Method Overview** . The overall learning pipeline consists of three parts: (I) collecting expert data using privileged policies, (II) training T-GMP using a CVAE, and (III) training a unified RL policy with a terrain-conditioned discriminator. The terrain representation (height map) serves as a conditioning variable across all modules. 

The overall architecture of the CVAE is illustrated in Figure 2 (II). The model is trained by minimizing a weighted sum of a reconstruction loss and a regularization term, defined as: 


where _st_ : _t_ + _T_ and _h_<sup>emb</sup> _t_ : _t_ +<sup>_,_</sup> _T_<sup>crespectivelydenoteasequenceof</sup><sup>_T_consecutiveexpertstatesandtheir</sup> corresponding local height map features, and _β_ balances reconstruction accuracy and latent space regularization. We adopt a standard normal distribution _N_ (0 _, I_ ) as the prior distribution _p_ ( _zt_ ). 

During real-world deployment, only the local height map observation at the current time step is available. Therefore, we condition the decoder solely on a single-frame height map _ht_ to ensure consistency between training and inference. To mitigate error accumulation caused by insufficient conditioning information, we shorten the reconstruction horizon _T_ = 16, thereby effectively limiting the propagation of long-horizon prediction errors. The CVAE is trained offline and can be reused across downstream training tasks without retraining. 

## **4 Unified Terrain-conditioned Policy Training** 

### **4.1 Terrain-conditioned Discriminator** 

To enable the robot to exhibit natural and versatile humanoid motions with coordinated whole-body behaviors when traversing diverse terrains, we introduce adversarial motion priors (AMP) [32] to endow the policy with anthropomorphic style from the expert dataset. However, when multiple motion priors simultaneously cover the same task, the standard AMP framework may cause distinct motion styles to collapse into indistinguishable behaviors during policy learning. To address this 

4 

problem, we extend the AMP discriminator to a terrain-conditioned discriminator. Specifically, we employ a five-layer CNN _f_ cnn<sup>dto extract terrain features from the local height map</sup><sup>_ht_,and use the</sup> resulting terrain embedding _h_<sup>emb</sup> _t_<sup>_,_d</sup> as a conditioning input, together with state transitions, to guide the policy toward learning distinct and diverse motion styles under varying terrains. 

During discriminator training, we use the decoder trained in Section 3.2 to generate expert state trajectory sequences _τt_<sup>_M_</sup> = [ _s_<sup>_M_</sup> _t_<sup>_, · · ·, sM_</sup> _t_ + _T_<sup>] online conditioned on the terrain features, from which</sup> expert state transition pairs ( _s_<sup>_M_</sup> _k_<sup>_, sM_</sup> _k_ +1<sup>) are randomly sampled,where</sup><sup>_t≤k<t_+</sup><sup>_T_.In parallel,</sup> policy-induced state transition pairs ( _s_<sup>_π_</sup> _t_<sup>_, sπ_</sup> _t_ +1<sup>) are obtained from environment rollouts by executing</sup> the current policy, where _s_<sup>_π_</sup> _t_<sup>denotesthepolicystateattimestep</sup><sup>_t_and</sup><sup>_sπ_</sup> _t_ +1<sup>denotestheresulting</sup> next state under the policy. 

Unlike the formulation in AMP [32], our terrain-conditioned discriminator _D_ is trained by minimizing the following objective: 


where _h_<sup>emb</sup> _t_<sup>_,_d</sup> represents local height map features extracted by the five-layer CNN _f_ cnn<sup>d,</sup><sup>_dM_and</sup> _d_<sup>_π_</sup> respectively represent the decoder-generated expert state transition distribution and the policyinduced state transition distribution, and **w**<sup>gp</sup> is the weight of the gradient penalty term. 

During policy training, to provide the policy with a clear and stable style guidance signal, we convert the discriminator output into a style reward, which is defined as: 


This reward function encourages policy-induced state transitions to align with the terrainconditioned expert motion styles, thereby guiding the policy to acquire consistent yet terraindistinctive locomotion behaviors across diverse terrains. 

### **4.2 Policy Training** 

**Observations** We define the robot’s observation at time step _t_ as: 


where _ωt_ denotes the angular velocity of the robot’s root, **g** _t_ is the gravity direction vector, _qt_ and _q_ ˙ _t_ respectively represent joint positions and velocities, and _at−_ 1 _∈_ R<sup>26</sup> denotes the action executed at the previous time step. To enhance temporal awareness and robustness, we stack the most recent five frames of observations, forming an augmented observation **O** _t_ = [ **o** _t−_ 4 _, · · · ,_ **o** _t_ ]. In addition, the Critic network has access to privileged information **o**<sup>priv</sup> _t_ during training to improve the accuracy of value estimation. Detailed information about **o** _t_ and **o**<sup>priv</sup> _t_ is provided in Section B.1. 

**Policy** The overall training framework is illustrated in Figure 2 (III). To enable the policy to exhibit discriminative motion styles while maintaining strong terrain adaptability across different terrains, we explicitly incorporate terrain perception into the policy network. Specifically, we employ a CNN _f_ cnn<sup>pwiththesamearchitecturedescribedinSection3.2toextractfeaturesfromthelocal</sup> height map _ht_ , and concatenate the resulting terrain embedding _h_<sup>emb</sup> _t_<sup>_,_p</sup> with the robot’s augmented proprioceptive observation **O** _t_ and velocity command _ct_ as input to the policy network. This design allows the policy to: (1) learn differentiated motion styles under varying terrains, and (2) attend to local terrain features, thereby perceiving terrain changes and guiding the robot to make more anticipatory decisions. Detailed policy training configurations are provided in Section B.2. 

**Foothold Penalty** During policy training, the robot may exhibit undesirable foothold behaviors when interacting with terrain edges and foothold contacts, such as kicking stair edges during ascent and edge-sliding during descent, which significantly degrade motion naturalness and physical 

5 


Figure 3: t-SNE visualization of MoCap and policy-generated motion distributions across different terrains, with Silhouette Scores computed on 10-dimensional features extracted using Principal Component Analysis (PCA). 

plausibility. To address this problem, we introduce Foothold Penalty, which explicitly constrains foot-terrain contact quality through ray-cast distance measurements from the toe and sole regions. Specifically, the toe distance is used to penalize toe collisions: 


where _d_ toe denotes the minimum distance between the toe and the terrain surface, _d_<sup>threshold</sup> toe denotes the safety distance threshold. The sole distance suppresses edge-support and sliding behaviors: 

_r_ sole = _−_ clip( _d_ sole _− d_<sup>threshold</sup> sole _,_ 0 _,_ 1) _·_ Icontact _,_ (8) 

where _d_ sole denotes the maximum distance between the sole and the ground surface, _d_<sup>threshold</sup> sole denotes the maximum allowable support distance, and Icontact denotes a contact indicator. Finally, we introduce the Foothold Penalty: _r_ foothold = _r_ toe + _r_ sole. An illustration of the proposed Foothold Penalty is provided in Figure 10. More reward settings can be found in Section B.3. 

## **5 Experiment** 

### **5.1 Experimental Setup** 

We conduct policy training and deployment on a 28-DoF full-size Kuavo humanoid robot. To evaluate the advantages of our method, we consider the following baselines: (1) a vanilla RL baseline [1] ( **Baseline RL** ); and (2) a standard AMP [32] ( **AMP** ). To evaluate the contribution of each key component, we consider three ablations: (1) removing the CVAE module and instead randomly sampling expert state transitions from the expert dataset _D_ ( **Ours w/o CVAE** ); (2) removing the terrain-conditioning embedding _h_<sup>emb</sup> _t_<sup>_,_d</sup> from the discriminator ( **Ours w/o Condition** ); and (3) removing the Foothold Penalty ( **Ours w/o Foothold** ). All policies are trained on the same dataset using 2048 parallel environments on a single NVIDIA RTX 4090 GPU. 

### **5.2 Motion Diversity** 

Our simulation (Figure 6) and real-world (Figure 7) experiments qualitatively demonstrate that the robot exhibits diverse motion styles when traversing different terrains. To quantitatively evaluate the 

6 


Figure 4: MMD between policy-generated and MoCap motion distributions across all terrains. Lower values indicate closer agreement with the MoCap motion distribution. 


Figure 5: Motion smoothness analysis across all terrains. (a) Mean and standard deviation of joint torques. (b) Mean and standard deviation of joint accelerations. 

motion style distributions learned by different methods, we collect 700-step joint-position trajectories _{qt}_<sup>700</sup> _t_ =1<sup>from five methods across all terrains and visualize their distributions using t-SNE [43].</sup> As shown in Figure 3, the comparison methods exhibit less compact motion distributions with significant inter-terrain overlap. In contrast, our method produces highly compact intra-terrain clusters and clearly separable inter-terrain distributions. We further report the Silhouette Score to jointly quantify intra-terrain consistency and inter-terrain separability, where a higher score indicates better cluster separation. Our method achieves a score of 0.127, outperforming AMP (0.095) and all other baselines except Ours w/o CVAE (0.168). Ours w/o CVAE learns disordered styles, thus yielding an anomalously high score, which we will explain in Section E. 

### **5.3 Motion Naturalness** 

We compare the distribution of policy-generated motions with MoCap data. For each terrain, we randomly sample consecutive 10-frame joint-position clips from each policy and compute the Maximum Mean Discrepancy (MMD) [44] against the corresponding MoCap clips. As shown in Figure 4, our method achieves the lowest average MMD of 0.1301 and consistently yields the lowest MMD across all terrains. T-GMP produces motion distributions closer to natural human MoCap than AMP and other baselines. We further report the mean and standard deviation of joint torques and accelerations across all terrains. As shown in Figure 5, our method yields an average joint torque of 181.2 N _·_ m and an average joint acceleration of 502.3 rad _/_ s<sup>2</sup> , with standard deviations of 

Table 1: Terrain-traversal success rates across seven challenging terrains. 

||||**Su**|**ccess Rate (**|**%)**|||
|---|---|---|---|---|---|---|---|
|**Method**|**Gap**|**Beam**|**Stage**|**Stair**<br>**Ascent**|**Stair**<br>**Descent**|**Slope**<br>**Ascent**|**Slope**<br>**Descent**|
|Baseline RL [1]|92.97|79.69|93.36|86.33|85.55|92.19|95.31|
|AMP [32]|93.02|86.72|90.33|89.06|82.56|93.41|96.09|
|Ours|**98.83**|**96.88**|**96.09**|**96.48**|**93.75**|**99.61**|**100.00**|
|Ours w/o CVAE|97.27|78.52|91.80|91.80|84.38|96.48|97.66|
|Ours w/o Condition|96.88|81.41|89.06|96.09|82.42|98.44|97.66|
|Ours w/o Foothold|98.05|94.14|95.70|95.70|85.94|99.61|98.83|


7 


Figure 6: The robot traverses multiple unseen terrains in a single run, including an ascending wavy slope, a wavy balance beam, irregular gaps, and a descending wavy balance beam. 

69.7 N _·_ m and 595.1 rad _/_ s<sup>2</sup> . T-GMP exhibits lower torque and acceleration fluctuations, indicating smoother and more natural motions. 

### **5.4 Generalization and Robustness** 

As shown in Figure 6, our method generalizes to multiple unseen terrains in MuJoCo and exhibits combinations of learned motion patterns (The robot combines arm extension for balance with CoM lowering for slope adaptation when descending an unseen wavy beam), rather than simply replaying fixed motion patterns from the training data. We further evaluate the terrain traversal success rates of all methods across seven terrains, with detailed experimental settings provided in Section C and results summarized in Table 1. Our method achieves the highest success rate on every evaluated terrain. In the beam traversal task, our method achieves an average improvement of 12.78 percentage points over the comparison methods, mainly due to the coordinated arm-extension behaviors for balance regulation. In the stair-descent task, our method achieves an average improvement of 9.58 percentage points, benefiting from adaptive center-of-mass lowering and the Foothold Penalty, which suppresses unstable edge contacts and sliding behaviors through reliable foothold control. 

### **5.5 Real-world Deployment** 

We compare expert demonstrations with real-robot deployments to analyze the consistency of terrain-conditioned motion distributions learned by the policy. Experiments are conducted on the 


Figure 7: The robot exhibits terrain-adaptive and anthropomorphic locomotion behaviors across diverse terrains, including natural arm swinging during flat-ground walking, lowered center-of-mass postures on stairs and slopes, and arm extension for dynamic balance on gaps and beams. 

8 

full-size Kuavo humanoid robot over diverse terrains, including flat ground, a 0.3 m high stage, stairs with 0.13 m step height and 0.28 m tread width, a 15<sup>_◦_</sup> slope, a 0.4 m wide gap, and a 0.35 m wide beam (with the robot foot separation being 0.3 m). As shown in Figure 7, our method effectively preserves diverse terrain-conditioned expert motion patterns, while exhibiting coordinated and anthropomorphic locomotion behaviors during real-world deployment. 

## **6 Conclusion** 

In this work, we propose T-GMP, which unifies anthropomorphic naturalness and robust terrain traversal for humanoid locomotion. By leveraging a CVAE, our method successfully learned a generative manifold of human movements that is intrinsically aligned with the terrain-aware physical constraints. Our approach moves beyond static motion priors by employing a terrain-conditioned discriminator that dynamically modulates the naturalness reward, enabling the agent to discover sophisticated balancing strategies, such as reflexive arm-spreading on a narrow beam. Experimental results demonstrate that T-GMP improves traversal robustness and motion smoothness by promoting physically coordinated and anthropomorphic whole-body behaviors, while producing diverse motion styles. Our work suggests that integrating generative motion priors conditioned on perceptual observations into RL is a powerful paradigm for achieving the next level of agile and human-like robot locomotion. 

## **7 Limitations and Future Work** 

First, T-GMP relies on paired motion states and local height maps for training, which limits its ability to directly leverage large-scale public motion datasets that lack terrain-aligned perceptual observations. Although a trained T-GMP can be reused across downstream policies, constructing such paired data still requires additional effort. Future work could follow [45] to directly collect diverse MoCap data aligned with perceptual observations, thereby simplifying the data construction pipeline. 

Second, the proposed terrain perception pipeline relies on LiDAR-based environment reconstruction. However, LiDAR measurements inevitably contain sensing noise and reconstruction artifacts. Such perception uncertainties may compromise locomotion robustness on complex terrains. Meanwhile, terrain reconstruction suffers from limited update frequency. Future work may investigate multi-modal perception strategies that integrate depth cameras with LiDAR sensing to improve reconstruction accuracy and perception update frequency. 

9 

## **References** 

- [1] N. Rudin, D. Hoeller, P. Reist, and M. Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In A. Faust, D. Hsu, and G. Neumann, editors, _Proceedings of the 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pages 91–100. PMLR, 08–11 Nov 2022. URL `https: //proceedings.mlr.press/v164/rudin22a.html` . 

- [2] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. doi:10.1126/scirobotics.adi9579. URL `https://www.science.org/doi/abs/10.1126/ scirobotics.adi9579` . 

- [3] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. _The International Journal of Robotics Research_ , 44:840 – 888, 2024. URL `https://api.semanticscholar.org/ CorpusID:267320454` . 

- [4] Y. Zhou, J. Qiu, W. Zhang, and F. Ni. Humanoidmamba: Generalized mamba-based policy learning with next-action prediction for humanoid locomotion. _IEEE Transactions on Cognitive and Developmental Systems_ , pages 1–13, 2026. doi:10.1109/TCDS.2026.3678742. 

- [5] D. Hoeller, N. Rudin, D. Sako, and M. Hutter. Anymal parkour: Learning agile navigation for quadrupedal robots. _Science Robotics_ , 9(88):eadi7566, 2024. doi:10.1126/scirobotics.adi7566. URL `https://www.science.org/doi/abs/10.1126/scirobotics.adi7566` . 

- [6] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik. Learning humanoid locomotion over challenging terrain. _ArXiv_ , abs/2410.03654, 2024. URL `https://api.semanticscholar.org/ CorpusID:273162639` . 

- [7] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu. Learning perceptive humanoid locomotion over challenging terrain. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6571–6578, 2025. doi:10.1109/IROS60139.2025. 11247685. 

- [8] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

- [9] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne. Deepmimic: example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions on Graphics_ , 37 (4):1–14, July 2018. ISSN 1557-7368. doi:10.1145/3197517.3201311. URL `http://dx. doi.org/10.1145/3197517.3201311` . 

- [10] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion, 2025. URL `https: //arxiv.org/abs/2508.08241` . 

- [11] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa. Visual imitation enables contextual humanoid control. In J. Lim, S. Song, and H.-W. Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 794–815. PMLR, 27–30 Sep 2025. URL `https://proceedings.mlr.press/v305/allshire25a.html` . 

- [12] J. Ni, Z. Wang, W. Lin, A. Bar, Y. LeCun, T. Darrell, J. Malik, and R. Herzig. From generated human videos to physically plausible robot trajectories, 2025. URL `https://arxiv.org/ abs/2512.05094` . 

10 

- [13] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning quadrupedal locomotion over challenging terrain. _Science Robotics_ , 5(47):eabc5986, 2020. doi: 10.1126/scirobotics.abc5986. URL `https://www.science.org/doi/abs/10.1126/ scirobotics.abc5986` . 

- [14] A. Kumar, Z. Fu, D. Pathak, and J. Malik. RMA: Rapid Motor Adaptation for Legged Robots. In _Proceedings of Robotics: Science and Systems_ , Virtual, July 2021. doi:10.15607/RSS.2021. XVII.011. 

- [15] J. Long, Z. Wang, Q. Li, L. Cao, J. Gao, and J. Pang. Hybrid internal model: Learning agile legged locomotion with simulated robot response. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id= 93LoCyww8o` . 

- [16] I. M. Aswin Nahrendra, B. Yu, and H. Myung. Dreamwaq: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5078–5084, 2023. doi: 10.1109/ICRA48891.2023.10161144. 

- [17] I. M. A. Nahrendra, B. Yu, M. Oh, D. Lee, S. Lee, H. Lee, H. Lim, and H. Myung. Dreamwaq++: Obstacle-aware quadrupedal locomotion with resilient multi-modal reinforcement learning. _IEEE Transactions on Robotics_ , pages 1–17, 2026. doi:10.1109/TRO.2026. 3653774. 

- [18] A. Agarwal, A. Kumar, J. Malik, and D. Pathak. Legged locomotion in challenging terrains using egocentric vision. In K. Liu, D. Kulic, and J. Ichnowski, editors, _Proceedings of The 6th Conference on Robot Learning_ , volume 205 of _Proceedings of Machine Learning Research_ , pages 403–415. PMLR, 14–18 Dec 2023. URL `https://proceedings.mlr.press/v205/ agarwal23a.html` . 

- [19] Z. Zhuang, Z. Fu, J. Wang, C. G. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao. Robot parkour learning. In J. Tan, M. Toussaint, and K. Darvish, editors, _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 73–92. PMLR, 06–09 Nov 2023. URL `https://proceedings.mlr.press/v229/ zhuang23a.html` . 

- [20] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. In P. Agrawal, O. Kroemer, and W. Burgard, editors, _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 1975–1991. PMLR, 06–09 Nov 2025. URL `https://proceedings.mlr.press/v270/zhuang25a.html` . 

- [21] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids, 2026. URL `https://arxiv.org/abs/2601.07718` . 

- [22] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. _Science Robotics_ , 7(62), Jan. 2022. ISSN 2470-9476. doi:10.1126/scirobotics.abk2822. URL `http://dx.doi.org/10.1126/ scirobotics.abk2822` . 

- [23] X. Cheng, K. Shi, A. Agarwal, and D. Pathak. Extreme parkour with legged robots. _arXiv preprint arXiv:2309.14341_ , 2023. 

- [24] O. A. V. Maga˜na, V. Barasuol, M. Camurri, L. Franceschi, M. Focchi, M. Pontil, D. G. Caldwell, and C. Semini. Fast and continuous foothold adaptation for dynamic locomotion through cnns. _IEEE Robotics and Automation Letters_ , 4(2):2140–2147, 2019. doi: 10.1109/LRA.2019.2899434. 

11 

- [25] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003, 2025. doi:10.1109/ICRA55743.2025.11128333. 

- [26] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds. In _Proceedings of Robotics: Science and Systems_ , Los Angeles, CA, USA, June 2025. doi:10.15607/RSS.2025.XXI.068. 

- [27] F. Jenelten, J. He, F. Farshidian, and M. Hutter. Dtc: Deep tracking control. _Science Robotics_ , 9 (86):eadh5401, 2024. doi:10.1126/scirobotics.adh5401. URL `https://www.science.org/ doi/abs/10.1126/scirobotics.adh5401` . 

- [28] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter. Attention-based map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. doi:10.1126/scirobotics.adv3604. URL `https://www.science.org/doi/abs/10. 1126/scirobotics.adv3604` . 

- [29] C. Zhang, V. Klemm, F. Yang, and M. Hutter. Ame-2: Agile and generalized legged locomotion via attention-based neural map encoding, 2026. URL `https://arxiv.org/abs/2601. 08485` . 

- [30] A. Serifi, R. Grandia, E. Knoop, M. Gross, and M. B¨acher. Vmp: Versatile motion priors for robustly tracking motion on physical characters. _Computer Graphics Forum_ , 43(8):e15175, 2024. doi:https://doi.org/10.1111/cgf.15175. URL `https://onlinelibrary.wiley.com/ doi/abs/10.1111/cgf.15175` . 

- [31] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system, 2025. URL `https: //arxiv.org/abs/2511.02832` . 

- [32] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Trans. Graph._ , 40(4), July 2021. doi:10. 1145/3450626.3459670. URL `http://doi.acm.org/10.1145/3450626.3459670` . 

- [33] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Trans. Graph._ , 41(4), July 2022. 

- [34] Z. Dou, X. Chen, Q. Fan, T. Komura, and W. Wang. C·ase: Learning conditional adversarial skill embeddings for physics-based characters. In _SIGGRAPH Asia 2023 Conference Papers_ , SA ’23, New York, NY, USA, 2023. Association for Computing Machinery. ISBN 9798400703157. doi:10.1145/3610548.3618205. URL `https://doi.org/10.1145/ 3610548.3618205` . 

- [35] H. Wang, W. Zhang, R. Yu, T. Huang, J. Ren, F. Jia, Z. Wang, X. Niu, X. Chen, J. Chen, Q. Chen, J. Wang, and J. Pang. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _ArXiv_ , abs/2510.11072, 2025. URL `https://api. semanticscholar.org/CorpusID:282057062` . 

- [36] J. Wang, Y. Jiang, H. Zhang, C. Tessler, D. Rempe, J. Hodgins, and X. B. Peng. Hil: Hybrid imitation learning of diverse parkour skills from videos. _ArXiv_ , abs/2505.12619, 2025. URL `https://api.semanticscholar.org/CorpusID:278741010` . 

- [37] H. Zhang, L. Zhang, Z. Chen, L. Chen, Y. Wang, and R. Xiong. Natural humanoid robot locomotion with generative motion prior. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6622–6629, 2025. doi:10.1109/IROS60139.2025. 11247682. 

12 

- [38] Q. Li, C. Zhu, Y. Wu, X. Yuan, Z. Zhang, J. Yang, and Y. Liu. Run: Residual policy for natural humanoid locomotion. _ArXiv_ , abs/2509.20696, 2025. URL `https://api. semanticscholar.org/CorpusID:281526091` . 

- [39] Y. Fan, T. Gui, K. Ji, S. Ding, C. Zhang, J. Gu, J. Yu, J. Wang, and Y. Shi. One policy but many worlds: A scalable unified policy for versatile humanoid locomotion, 2025. URL `https://arxiv.org/abs/2505.18780` . 

- [40] Z. Zhang, K. Wen, M. Xu, J. He, C. Li, T. Miki, C. Schwarke, C. Zhang, X. B. Peng, and M. Hutter. Learning whole-body humanoid locomotion via motion generation and motion tracking, 2026. URL `https://arxiv.org/abs/2604.17335` . 

- [41] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking, 2025. URL `https://arxiv.org/abs/2510.02252` . 

- [42] I. Higgins, L. Matthey, A. Pal, C. Burgess, X. Glorot, M. Botvinick, S. Mohamed, and A. Lerchner. beta-VAE: Learning basic visual concepts with a constrained variational framework. In _International Conference on Learning Representations_ , 2017. URL `https://openreview. net/forum?id=Sy2fzU9gl` . 

- [43] L. van der Maaten and G. Hinton. Visualizing data using t-sne. _Journal of Machine Learning Research_ , 9(86):2579–2605, 2008. URL `http://jmlr.org/papers/v9/ vandermaaten08a.html` . 

- [44] A. Gretton, K. M. Borgwardt, M. J. Rasch, B. Sch¨olkopf, and A. Smola. A kernel two-sample test. _Journal of Machine Learning Research_ , 13(25):723–773, 2012. URL `http://jmlr. org/papers/v13/gretton12a.html` . 

- [45] A. Brandes, H. C. G. Sajelian, M. Patel, D. Hollidt, C. Li, M. Heyrman, O. Hausdoerfer, M. Kaufmann, X. Wang, J. Frey, A. P. Schoellig, C. Holz, M. Pollefeys, and M. Hutter. Egohtr: Egocentric 4d demonstrations of human terrain traversal, 2026. URL `https://arxiv.org/ abs/2607.13472` . 

- [46] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms, 2017. URL `https://arxiv.org/abs/1707.06347` . 

- [47] NVIDIA, :, M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Mu˜noz, X. Yao, R. Zurbr¨ugg, N. Rudin, L. Wawrzyniak, M. Rakhsha, A. Denzler, E. Heiden, A. Borovicka, O. Ahmed, I. Akinola, A. Anwar, M. T. Carlson, J. Y. Feng, A. Garg, R. Gasoto, L. Gulich, Y. Guo, M. Gussert, A. Hansen, M. Kulkarni, C. Li, W. Liu, V. Makoviychuk, G. Malczyk, H. Mazhar, M. Moghani, A. Murali, M. Noseworthy, A. Poddubny, N. Ratliff, W. Rehberg, C. Schwarke, R. Singh, J. L. Smith, B. Tang, R. Thaker, M. Trepte, K. V. Wyk, F. Yu, A. Millane, V. Ramasamy, R. Steiner, S. Subramanian, C. Volk, C. Chen, N. Jawale, A. V. Kuruttukulam, M. A. Lin, A. Mandlekar, K. Patzwaldt, J. Welsh, H. Zhao, F. Anes, J.F. Lafleche, N. Mo¨enne-Loccoz, S. Park, R. Stepinski, D. V. Gelder, C. Amevor, J. Carius, J. Chang, A. H. Chen, P. de Heras Ciechomski, G. Daviet, M. Mohajerani, J. von Muralt, V. Reutskyy, M. Sauter, S. Schirm, E. L. Shi, P. Terdiman, K. Vilella, T. Widmer, G. Yeoman, T. Chen, S. Grizan, C. Li, L. Li, C. Smith, R. Wiltz, K. Alexis, Y. Chang, D. Chu, L. J. Fan, F. Farshidian, A. Handa, S. Huang, M. Hutter, Y. Narang, S. Pouya, S. Sheng, Y. Zhu, M. Macklin, A. Moravanszky, P. Reist, Y. Guo, D. Hoeller, and G. State. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning, 2025. URL `https://arxiv.org/abs/2511.04831` . 

- [48] T. Miki, L. Wellhausen, R. Grandia, F. Jenelten, T. Homberger, and M. Hutter. Elevation mapping for locomotion and navigation using gpu, 2022. URL `https://arxiv.org/abs/ 2204.12876` . 

13 

## **A Data Collection** 

### **A.1 Privileged Policy Training** 


Figure 8: For challenging terrains such as stairs and beams, we introduce terrain-specific constraints on (a) center-of-mass regulation and (b) arm-balancing behaviors to promote more anthropomorphic and robust whole-body locomotion. 

Each privileged policy _πi_<sup>priv</sup> is trained exclusively on terrain _i_ , using the corresponding MoCap dataset _Di_<sup>mocap</sup> as the AMP [32] motion prior to learn anthropomorphic and physically feasible behaviors. Unlike the downstream policy, _πi_<sup>priv</sup> receives the privileged observations listed in Table 3 as additional inputs, which are unavailable during real-world deployment. The privileged observations accelerate training, allowing _πi_<sup>priv</sup> to be trained in _∼_ 12 hours with 2048 parallel environments on a single RTX 4090. Figure 8 illustrates the distinct terrain-specific behaviors learned by the privileged policies. Additionally, CVAE training takes only _∼_ 3 hours. Therefore, extending T-GMP to a new terrain _j_ requires only collecting the corresponding MoCap data, training _πj_<sup>priv</sup> , and retraining the CVAE with the augmented dataset, which can typically be completed within one day. 

### **A.2 Data Collection Details** 

Table 2 summarizes the detailed settings used for data collection. Our settings cover common configurations within each terrain category. T-GMP can interpolate between neighboring terrain configurations and generalize to unseen intermediate parameters. For example, motion data collected at step heights of 0.1 m and 0.15 m on stairs enable T-GMP to generate an appropriate motion style for a step height of 0.13 m. This generalization capability is further evidenced by the composition of learned motion styles on unseen terrains, as shown in Figure 6. Benefiting from the proposed T-GMP, we learn a terrain-conditioned motion manifold spanning eight terrains using only approximately 29.6 min (88.8k frames) of data. Figure 9 reports the duration and proportion of data collected for each terrain. T-GMP effectively captures diverse anthropomorFigure 9: Distribution of collected motion phic locomotion patterns from a small amount of exdata across eight terrains. pert demonstrations while covering diverse terrain conditions, locomotion behaviors, and terrain difficulty levels, demonstrating strong data efficiency and motion generalization capabilities. 

14 

Table 2: Data collection settings. 

|Terrain|||Settings|||
|---|---|---|---|---|---|
|Flat|–|Forward|Backward|Turn Left|Turn Right|
|Gap|Width|0.1 m|0.2 m|0.3 m|0.4 m|
|Beam|Width|0.2 m|0.3 m|0.4 m|–|
|Stage|Height|0.1 m|0.2 m|0.3 m|–|
|Stair Ascent|Step Height|0.05 m|0.1 m|0.15 m|0.2 m|
|Stair Descent|Step Height|0.05 m|0.1 m|0.15 m|0.2 m|
|Slope Ascent|Tilt Angle|5<sup>_◦_</sup>|10<sup>_◦_</sup>|15<sup>_◦_</sup>|20<sup>_◦_</sup>|
|Slope Descent|Tilt Angle|5<sup>_◦_</sup>|10<sup>_◦_</sup>|15<sup>_◦_</sup>|20<sup>_◦_</sup>|


## **B Policy Training** 

### **B.1 Observations** 

Table 3 summarizes all observations used by the Actor and Critic. The Actor inputs consist of command observations, perceptual observations, and policy observations, enabling the policy to jointly capture robot dynamics and local terrain geometry. Specifically, the velocity command _ct_ consists of linear and angular velocity commands, i.e., _ct_ = [ _vt, ωt_ ]. To improve value estimation accuracy, we introduce privileged observations that are unavailable during real-world deployment into the Critic network during training. These privileged observations are only used to facilitate more accurate value learning for the Critic and are not provided to the Actor during policy execution, thereby ensuring deployment compatibility and perception consistency under real-world conditions. 

Table 3: Observation Terms 

|**Term**|**Notation**|**Type**|**Description**|
|---|---|---|---|
|Velocity command|_ct_|Command|Velocity command of the robot’s base frame|
|Height scan|_ht_|Perception|A9_×_7height scan in front of the robot|
|Base angular velocity|_ωt_|Policy|Angular velocity in the robot’s base frame|
|Projected gravity|**g**_t_|Policy|Gravity projection on the robot’s base frame|
|Joint position|_qt_|Policy|The joint positions of the robot|
|Joint velocity|˙_qt_|Policy|The joint velocities of the robot|
|Last action|_at−_1|Policy|The last input action to the environment|
|Base linear velocity|_vt_|Privileged|Linear velocity in the robot’s base frame|
|Joint torque|_τt_|Privileged|Torques applied to the robot’s joints|
|Joint acceleration|¨_qt_<br>|Privileged|The joint accelerations of the robot|
|Feet linear velocity|_v_<sup>feet</sup><br>_t_|Privileged|The linear velocity of the robot’s feet|
|Feet contact force|_F_ <sup>contact</sup><br>_t_|Privileged|Contact force on the robot’s feet|
|Mass|_m_|Privileged|Total mass of the robot|
|Material|_µ_|Privileged|Friction coefficient of the ground|
|Center of mass|_p_com|Privileged|Center of mass in the robot’s base frame|
|Action delay|_t_delay|Privileged|Action delay on the robot’s motors|
|Push force|_F_ <sup>ext</sup><br>_t_|Privileged|External push force applied on the robot|
|Push torque|_τ_ <sup>ext</sup><br>_t_|Privileged|External push torque applied on the robot|
|Feet height|_h_<sup>feet</sup><br>_t_|Privileged|Robot’s feet height|
|Feet air time|_t_air|Privileged|Robot’s feet air time since last contact|


15 

Table 4: PPO Hyperparameters 

|**Parameter**|**Value**|
|---|---|
|Batch size|24_·_2048 = 49152|
|Mini batch size|6_·_2048 = 12288|
|Number of epochs|5|
|Clip range|0_._2|
|Entropy coefficient|0_._005|
|Discount factor|0_._99|
|GAE discount factor|0_._95|
|Desired KL-divergence|0_._01|
|Learning rate|0_._001|
|Max gradient norm|1_._0|


### **B.2 Reinforcement Learning Setup** 

Policy optimization is performed using Proximal Policy Optimization (PPO) [46], with the associated training hyperparameters summarized in Table 4. All experiments are conducted in the Isaac Lab [47] simulation environment on a single NVIDIA RTX 4090 GPU, with 2048 environments running in parallel. We adopt an asymmetric Actor-Critic architecture to train the policy, where both the Actor and Critic are parameterized by multilayer perceptrons (MLPs) with hidden layer sizes of [512, 256, 128]. The discriminator is implemented as an MLP with hidden layer sizes of [1024, 512, 256], followed by a linear output layer that maps the final hidden representation to a scalar score. 

### **B.3 Reward Formulation** 

Since motion style is primarily guided by the discriminator, the reward design remains concise yet effective. The reward received by the policy during training consists of four components: (1) task reward _r_ task, which encourages the robot’s root to track the commanded linear and angular velocities, (2) regularization reward _r_ reg, which enforces smoothness in actions and states while ensuring physical plausibility, (3) style reward _r_ amp, provided by the style discriminator, which encourages policy-induced state transitions to align with the expert motion styles, and (4) foothold 

Table 5: Reward Terms 

|**Term**|**Function**|**Weight**|
|---|---|---|
|Linear velocity command tracking|exp(_−∥vxy −v_<sup>cmd</sup><br>_xy _<sup>_∥_2)</sup><br>|5_._0|
|Angular velocity command tracking|exp(_−∥ωz −ω_<sup>cmd</sup><br>_z_<br>_∥_<sup>2</sup>)|3_._0|
|Joint velocity|_∥_˙_q∥_<sup>2</sup>|_−_2_._0_×_10<sup>_−_3</sup>|
|Joint acceleration|_∥_¨_q∥_<sup>2</sup>|_−_2_._5_×_10<sup>_−_7</sup>|
|Joint torque|_∥τ∥_<sup>2</sup>|_−_1_._0_×_10<sup>_−_5</sup>|
|Joint power|_|τ ·_ ˙_q|_|_−_2_._0_×_10<sup>_−_5</sup>|
|Action rate|_∥at −at−_1_∥_<sup>2</sup>|_−_0_._005|
|Action smoothness|_∥_(_at −at−_1)_−_(_at−_1_−at−_2)_∥_<sup>2</sup>|_−_0_._01|
|Joint limit|max(0_, q −q_max) + max(0_, q_min_−q_)|_−_1_._0|
|Feet slide|_∥v_<sup>feet</sup><br>_xy _<sup>_∥_2</sup><br>2 <sup>_∗_Icontact</sup>|_−_0_._1|
|Contact force|max(0_, f_contact_−f_threshold)|_−_0_._001|
|Termination|Ireset|_−_200|


16 


(a) 


(b) 

Figure 10: Illustration of the Foothold Penalty mechanism. (a) During stair ascent, the minimum toe-terrain contact distance _d_ toe is evaluated to reduce potential toe-collision risks. (b) During stair descent, the maximum sole-terrain contact distance _d_ sole is evaluated to suppress unstable foothold behaviors such as edge contacts and slipping. 

penalty _r_ foothold, which penalizes undesirable foot-contact behaviors. The overall training reward is defined as: 


### where _wi_ represents the corresponding weights. 

Benefiting from the inclusion of the style reward, the policy becomes significantly less sensitive to reward weighting, leading to a more stable and efficient hyperparameter tuning process. In practice, a single set of reward parameters can be reused across subsequent training runs with only minimal adjustment. We design a unified and concise reward function to train all policies. We primarily focus on the smoothness of robot motion and energy consumption, enabling the reward function to remain consistent across different tasks and experimental settings, thereby avoiding additional taskor scenario-specific reward engineering. The definitions of all reward terms and their corresponding weights are summarized in Table 5. 

### **B.4 Foothold Penalty** 

We design a Foothold Penalty mechanism to explicitly regularize the contact quality between the robot feet and the terrain. As illustrated in Figure 10a, during terrain traversal, we compute the minimum distance _d_ toe between the toe and the terrain surface. A penalty is applied when the toe–surface distance is below the safety threshold _d_<sup>threshold</sup> toe , suppressing potential toe-collision behaviors. Meanwhile, as illustrated in Figure 10b, we further compute the maximum distance _d_ sole between the sole and the terrain surface. When the distance exceeds the threshold _d_<sup>threshold</sup> sole , an additional penalty is imposed to discourage unstable support behaviors such as edge contacts and slipping. This mechanism encourages the policy to learn more stable and physically feasible foothold patterns, thereby improving locomotion stability and traversal robustness on complex terrains. 

## **C Success Rate Configurations** 

We evaluate terrain traversal success rates on seven representative challenging terrains, including a 0.3 m high stage, stairs with 0.13 m step height and 0.28 m tread width, a 15<sup>_◦_</sup> slope, a 0.4 m wide gap, and a 0.35 m wide beam. Each terrain is constructed within an 8 m _×_ 8 m evaluation area. A trial is considered successful if the robot completes a full terrain traversal within a predefined time limit. Failure is recorded if any body part other than the feet collides with the terrain during traversal, any joint exceeds its position limits or exhibits excessively large accelerations, or if the robot fails to complete the traversal within the allotted time. 

17 


Figure 11: Elevation map construction pipeline. (a) Raw dense elevation map generated from sparse environmental point clouds, containing missing regions caused by incomplete point-cloud reconstruction. (b) Processed elevation map after applying the nearest-region filling strategy, which is used for subsequent height-map sampling. 

## **D Sim-to-Real Details** 

### **D.1 Robot Setup** 

The full-size Kuavo humanoid robot is 1.66 m tall, weighs approximately 55 kg, and possesses 28 Degrees of Freedom (DoFs), including 2 DoFs in the head, 14 DoFs in the arms, and 12 DoFs in the legs. The robot has 28 DoFs, while the policy controls 26 actuated joints, excluding the two head joints. A Mid-360 LiDAR is mounted on the robot head for point-cloud perception and terrain reconstruction. The system adopts a dual-computing architecture, where an Orin-NX module processes point-cloud perception data in real time, while a MoFang i9-13900 computer executes low-level whole-body locomotion control. 

The robot is controlled using a joint-space PD controller with control torques defined as: 


where _K_ p and _K_ d denote proportional and derivative gains, respectively, _q_ denotes the current joint position, and _q_ ˙ denotes the current joint velocity. The policy action _a_ is defined as a residual control signal relative to the default joint configuration _q_ 0, such that the target joint position is given by 


### **D.2 Acquisition of Elevation Map** 

As illustrated in Figure 11a, following the elevation mapping pipeline in [48], the raw point cloud observations are converted into a dense elevation map representation. To avoid invalid `NaN` inputs caused by sparse point-cloud reconstruction, we apply a nearest-region filling strategy that replaces `NaN` cells with the minimum height value within the surrounding 5 _×_ 5 neighborhood, resulting in the processed elevation map shown in Figure 11b. We then uniformly sample a local terrain patch of size 0.8 m _×_ 0.6 m in front of the robot from the processed elevation map, which is used as the terrain perception input to the policy. 

## **E Motion Style Visualization** 

As shown in Figure 12, we compare the motion styles produced by different policies during terrain traversal. Baseline RL is trained without explicit style guidance or additional reward terms for 

18 


Figure 12: Motion styles produced by different policies across all terrains. 

shaping upper-body motion. Thus, it produces uniform yet uncoordinated motions across terrains. Ours w/o CVAE employs a terrain-conditioned discriminator, while its expert state transitions are randomly sampled from the expert dataset _D_ and may therefore be inconsistent with the current terrain condition. Such mismatched terrain–state pairs hinder discriminator convergence, resulting in incoherent mixtures of motion patterns. 

19 

