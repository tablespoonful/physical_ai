---
title: "WM-DAgger: Enabling Efficient Data Aggregation for Imitation Learning with World Models"
date: "2026-04-13"
authors: "Anlan Yu; Zaishu Chen; Peili Song; Zhiqing Hong; Haotian Wang; Desheng Zhang"
url: https://arxiv.org/abs/2604.11351
pdf: https://arxiv.org/pdf/2604.11351
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.11351)** / [論文ページ](https://arxiv.org/abs/2604.11351)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **WM-DAgger: Enabling Efficient Data Aggregation for Imitation Learning with World Models** 

Anlan Yu<sup>1</sup><sup>_†_</sup> , Zaishu Chen<sup>2</sup><sup>_†_</sup> , Peili Song<sup>3</sup> , Zhiqing Hong<sup>4</sup><sup>_∗_</sup> , Haotian Wang<sup>2</sup> , Desheng Zhang<sup>5</sup> , Tian He<sup>2</sup> , Yi Ding<sup>6</sup> , and Daqing Zhang<sup>1</sup><sup>_,_7</sup><sup>_∗_</sup> 

**_Abstract_ — Imitation learning is a powerful paradigm for training robotic policies, yet its performance is limited by compounding errors: minor policy inaccuracies could drive robots into unseen out-of-distribution (OOD) states in the training set, where the policy could generate even bigger errors, leading to eventual failures. While the Data Aggregation (DAgger) framework tries to address this issue, its reliance on continuous human involvement severely limits scalability. In this paper, we propose WM-DAgger, an efficient data aggregation framework that leverages World Models to synthesize OOD recovery data without requiring human involvement. Specifically, we focus on manipulation tasks with an eye-inhand robotic arm and only few-shot demonstrations. To avoid synthesizing misleading data and overcome the hallucination issues inherent to World Models, our framework introduces two key mechanisms: (1) a Corrective Action Synthesis Module that generates task-oriented recovery actions to prevent misleading supervision, and (2) a Consistency-Guided Filtering Module that discards physically implausible trajectories by anchoring terminal synthesized frames to corresponding real frames in expert demonstrations. We extensively validate WM-DAgger on multiple real-world robotic tasks. Results that our method significantly improves success rates, achieving a 93.3% success rate in soft bag pushing with only five demonstrations. The source code is publicly available at https://github.com/ czs12354-xxdbd/WM-Dagger.** 

## I. INTRODUCTION 

Imitation learning is a powerful paradigm for transferring human expertise to robotic systems [1], [2], [3]. However, its effectiveness is hindered by _compounding errors_ [4]: Even minor policy inaccuracies can drive the robot into states not covered by human demonstrations (i.e., out-ofdistribution (OOD) states), where the policy generates further errors, eventually leading to task failure. 

To address this problem, the Data Aggregation (DAgger) paradigm [4], [5] relies on continuous human intervention to guide the robot back from OOD states while simultaneously collecting recovery data for further imitation learning. 

> _†_ These authors contributed equally. _∗_ Corresponding authors. 

> 1Anlan Yu is with Peking University, Beijing, China. (E-mail: yal6040@pku.edu.cn) 

2Zaishu Chen, Haotian Wang, and Tian He are with JD Logistics, China. (Email: _{_ chenzaishu.1, wanghaotian18, tim.he _}_ @jd.com) 

> 3Peili Song is with Nankai University, Tianjin, China. (Email: peilisong@mail.nankai.edu.cn) 

> 4Zhiqing Hong is with The Hong Kong University of Science and Technology (Guangzhou), China. (E-mail: zhiqinghong@hkust-gz.edu.cn) 

> 5Desheng Zhang is with Rutgers University, Piscataway, USA. (E-mail: desheng@cs.rutgers.edu) 

6Yi Ding is with the University of Texas at Dallas, Richardson, TX, USA. (E-mail: yi.ding@utdallas.edu) 

1 _,_ 7Daqing Zhang is with Peking University, Beijing, China, and Institut Polytechnique de Paris, France. (E-mail: dqzhang@sei.pku.edu.cn) 


Fig. 1: **WM-DAgger** mitigates the compounding errors of standard Behavioral Cloning (BC) by generating massive recovery supervision with a world model. (e.g., visual transitions _a → b → c_ and _d → e → f_ ). 

However, its dependence on manual operation limits its scalability in practice. Recently, diffusion-based models have been used to synthesize OOD recovery data [6]. However, their restriction to single-frame generation prevents them from modeling continuous dynamics of recovery processes. Moreover, without inherent understanding of environment dynamics, these models struggle with complex physical interactions and deformable objects. 

Recent advancements in World Models (WMs) [7], [8], [9] offer a unique opportunity to address this compounding error problem. World Models, such as Cosmos-Predict [10], take historical frames and intended actions as inputs to synthesize the resulting frames of future states. By synthesizing OOD recovery data with these models, the human effort required for data collection in the DAgger paradigm can be substantially reduced. Moreover, unlike existing singleframe diffusion models for data synthesis, WMs can generate multiple continuous frames that capture environment dynamics across complex real-world scenarios [7], making them suitable for tasks involving complex physical interactions and deformable objects. 

Although promising, leveraging WMs to synthesize highquality OOD recovery data is non-trivial. **The first challenge** is the absence of expert involvement to provide optimal recovery supervision. While standard human-in-theloop DAgger [5] relies on experts to supply OOD recovery actions, this manual labeling is unavailable when synthesizing trajectories within a world model. If these OOD states are paired with suboptimal actions, it will severely mislead policy training [11]. **The second challenge** lies in mitigating the impact of hallucinations within the synthesized recovery data. WMs inevitably introduce hallucinations, such as object morphing or implausible state transitions. Training a policy on such data yields marginal performance improvements, as the policy learns from erroneous physical dynamics that mismatch the real-world environment. 

In this work, we propose **WM-DAgger** , a framework leveraging <u>World Models</u> to enable efficient <u>Data Aggregation for imitation learning. Specifically, we focus on</u> robotic manipulation tasks utilizing the widely adopted eyein-hand configuration [6], [12]. As illustrated in Figure 1, our framework trains the policy using few-shot expert demonstrations augmented by large-scale OOD recovery data, which is synthesized by the proposed Eye-in-Hand-Conditioned World Model (EAC-WM) based on Cosmos-Predict-2.5 [10]. The model maps robotic actions into pixel-wise motion fields representing eye-in-hand camera displacement, providing explicit geometric conditioning to synthesize visual observations corresponding to the recovery actions. **To address the first challenge,** we introduce a Corrective Action Synthesis Module. Instead of generating random recovery actions that could provide misleading supervision, this module synthesizes task-oriented recovery actions. Synthesized actions are constrained to follow the original direction of the expert trajectory. This prevents the policy from learning suboptimal actions that could even degrade performance. **To address the second challenge,** we design a Consistency-Guided Filtering Module. It compares each synthesized OOD recovery data’s terminal frame with the frame from the original expert data. As WMs inherently accumulate errors over time [9], the terminal frame contains the highest level of potential hallucination. If this frame remains visually and physically consistent with the real expert frame, the whole synthesized data is validated for policy training. 

In summary, our contributions are as follows. 

- Conceptually, we first utilize World Models to synthesize OOD recovery data, enabling robust imitation learning even from few-shot demonstrations. 

- Technically, we propose WM-DAgger, a world-modelbased OOD recovery data synthesis framework that generates task-oriented data with suppressed hallucinations. 

- Experimentally, real-world evaluations across multiple tasks confirm the utility of WM-DAgger. Notably, it achieves a 93.3% success rate in soft bag pushing using only five demonstrations. 

## II. RELATED WORK 

## _A. Dataset Aggregation for Imitation Learning_ 

Imitation learning is a vital paradigm for training robotic policies, yet it is often limited by distribution shifts and compounding execution errors in real-world settings [1], [2], [3]. The Dataset Aggregation (DAgger) framework [4] addresses this by iteratively incorporating expert feedback in recovering from OOD states to train the policy. While variants like HG-DAgger [5] and CR-DAgger [13] optimize this process through controlled gating and compliant intervention, they remain constrained by a fundamental reliance on expensive human-in-the-loop supervision. 

To enhance scalability, recent generative approaches such as DMD [6] synthesize OOD data for imitation learning; however, these methods often prioritize visual synthesis and lack physical awareness in the synthesized samples. In this work, we propose WM-DAgger, which utilizes a world model to autonomously synthesize physically consistent corrective trajectories, enabling robust imitation learning without additional human cost for data aggregation. 

## _B. World Models in Robot Learning_ 

World Models serve as internal simulators of the environment, enabling agents to predict the causal consequences of their actions [7], [8], [14]. One prominent approach, exemplified by the Dreamer series [15], encodes high-dimensional observations into a compact latent space using a Recurrent State-Space Model. Recent advancements have introduced powerful generative world models trained on internet-scale data. Systems like NVIDIA Cosmos [10] utilize video diffusion to simulate realistic physical interactions based on language instructions or motor controls, achieving strong generalization capabilities. In practical robotics, frameworks such as DayDreamer [16] demonstrate that world models facilitate rapid learning on physical robots without human demonstrations. Similarly, World4RL [17] improves manipulation success rates by training policies on imagined rollouts, thereby avoiding the safety risks of real-world trials. In this work, we leverage the strong generalization capability of pretrained world models to address the distribution shift problem in imitation learning. 

## III. METHODOLOGY 

We introduce WM-DAgger, a world-model-driven framework that synthesizes OOD states and corresponding recovery trajectories to train robust policies. The overall pipeline, illustrated in Figure 2, begins by training an eyein-hand, action-conditioned world model. It learns physically consistent environmental dynamics using a combination of explorative Play Data and expert-demonstrated Task Data. Specifically, Play Data is collected via goal-agnostic exploration of the workspace, while Task Data comprises specific expert trajectories to accomplish targeted manipulation tasks. Utilizing this trained WM, we generate large-scale OOD recovery data from the expert Task Data. Specifically, the Corrective Action Synthesis Module produces recovery actions by intentionally deviating from the expert trajectory 


Fig. 2: Overall pipeline of our WM-DAgger framework. 

into surrounding OOD states and subsequently steering back. The WM then synthesizes the corresponding visual frames along these recovery paths. To ensure data fidelity, the Consistency-Guided Filtering Module discards trajectories that exhibit physically implausible hallucinations in the synthesized frames. Finally, we aggregate the original expert Task Data with the validated synthetic recovery data to train a policy capable of rectifying compounding execution errors. 

_A. Eye-in-Hand Action-Conditioned World Model Design_ 


Fig. 3: EAC-WM Architecture. 

_1) Overall Architecture:_ We propose the **Eye-in-Hand Action-Conditioned World Model (EAC-WM)** , an architecture designed to capture and synthesize eye-in-hand visual dynamics. Built upon the GE-Sim [18] framework with a Cosmos-Predict2.5 (2B) [10] backbone, EAC-WM introduces an _Action2Image_ conditioning module. By translating actions into the relative spatial movement of each pixel in the eye-in-hand camera, this module conditions the WM with fine-grained geometric information, thereby improving the fidelity of predicted eye-in-hand visual dynamics. 

We define the robotic control input at time _t_ as a vector **a** _t_ = [ **t** _t,_ **q** _t, gt_ ]<sup>_⊤_</sup> , comprising the Cartesian translation **t** _t ∈_ R<sup>3</sup> , unit quaternion orientation **q** _t ∈_ R<sup>4</sup> , and continuous gripper state _gt ∈_ R. Formally, let _fθ_ denote the WM parameterized by _θ_ . Given a context window of _p_ historical observations and a sequence of _q_ future actions, EAC-WM predicts the subsequent _q_ visual states: 


where **I** and<sup>ˆ</sup> **I** represent the ground-truth and synthesized visual frames, respectively. 

_2) Action2Image Conditioning:_ Conditioning the world model _fθ_ on low-dimensional actions **a** _t−p_ : _t_ + _q_ is challenging, as sparse action vectors are easily overshadowed by high-dimensional visual conditions **I** _t−p_ : _t_ . Inspired by camera parameter encoding methods in computer vision [19], we introduce the _Action2Image_ module, which projects sparse action vectors into a dense, pixel-aligned geometric condition to bridge this dimensional gap. 

In this module, we first derive the camera’s rotation **R** _t ∈ SO_ (3) and translation **o** _t ∈_ R<sup>3</sup> in the world coordinate system by transforming the action vector [ **t** _t,_ **q** _t_ ] via a fixed hand-eye calibration matrix. Based on 3D projective geometry, each image pixel ( _u, v_ ) is associated with a 3D ray originating at the camera’s optical center. The unit viewing direction **d**<sup>(</sup> _t_<sup>_u,v_)</sup> of the pixel ( _u, v_ ) can be computed using the camera intrinsic matrix **K** _∈_ R<sup>3</sup><sup>_×_3</sup> as: 


To effectively condition the model to generate the image at step _t_ + _i_ based on the image at step _t_ and the relative action between them, we transform the relative action into high-dimensional relative ray transformations for each pixel in the image. The relative translation ∆ **o** _t_ + _i_ = **o** _t_ + _i −_ **o** _t_ is spatially broadcasted across the image dimensions to form a uniform origin displacement grid ∆ **O** _t_ + _i ∈_ R<sup>_H×W ×_3</sup> . Simultaneously, we compute the per-pixel directional shift ∆ **d**<sup>(</sup> _t_ +<sup>_u,v_</sup> _i_<sup>)</sup> = **d**<sup>(</sup> _t_<sup>_u,v_</sup> <u>+</u> _i_<sup>)</sup><sup>_−_</sup><sup>**d**</sup> _t_<sup>(</sup><sup>_u,v_)</sup> , which is aggregated into a dense <u>���</u> **d** _t_ ( _u,v_ + _i_ )<sup>_−_</sup><sup>**d**</sup> _t_<sup>(</sup><sup>_u,v_)</sup> <u>���2</u> directional tensor ∆ **D** _t_ + _i ∈_ R<sup>_H×W ×_3</sup> . By concatenating ∆ **O** _t_ + _i_ and ∆ **D** _t_ + _i_ , we acquire motion condition. To incorporate non-spatial action condition, the scalar gripper state _gt_ + _i_ is broadcasted into a feature map **C** grip _∈_ R<sup>_H×W ×_1</sup> as the gripper condition. These components are concatenated to construct the final dense geometric condition: 


_3) Video-Action Tokenization:_ To process highdimensional visual and geometric data with world foundation model, we project inputs into a compact latent space using a pretrained Variational Autoencoder (VAE). Given a sequence of historical context frames **I** _t−p_ : _t_ and target future frames **I** _t_ : _t_ + _q_ , the VAE yields visual image tokens **x** _t−p_ : _t_ + _q_ . Simultaneously, the dense geometric condition **C** geo is projected through down-sampling to obtain action 

tokens **c** geo. This unified tokenization ensures that both the visual observations and the robotic control actions are represented in a shared latent space, facilitating effective cross-modal interaction within the world foundation model. 

_4) World Model Training and Data Strategy:_ EAC-WM is initialized with the Cosmos-Predict2.5 (2B) foundation model, which establishes general physical priors through pre-training on internet-scale video-only data _DI_ . We subsequently adapt the model to specific manipulation dynamics using synchronized visual-action sequences from Play Data _DP_ and Task Data _D_ . Play data _DP_ consists of unscripted human exploratory movements used to internalize scenespecific geometry, while Task data _D_ comprises expert demonstrations that refine the model’s understanding of action-conditioned physical dynamics. 

The training of EAC-WM is formulated within the Rectified Flow framework [20], which learns to map noise to data along a deterministic linear path. During our videoaction post-training, historical context tokens **x** _t−p_ : _t_ serve as unnoised conditional anchors **c** mem. The target future tokens **x** _k_ , _k ∈{t, . . . , t_ + _q}_ , are used to construct noised latent variables via linear interpolation with Gaussian noise **_ϵ_** _∼N_ ( **0** _,_ **I** ) under noise scale _λ ∈_ [0 _,_ 1]: 


A Video Diffusion Transformer (DiT) _ϕθ_ is trained to predict the velocity field that directs the flow from noise back to the data distribution. The model is optimized by minimizing the Mean Squared Error (MSE) of the predicted flow: 


where _w_ ( _λ_ ) is a weighting function that assigns adaptive importance to the velocity prediction loss for stable training [21] and ( **_ϵ_** _−_ **x** ) denotes the ground-truth target velocity. The conditioning vector **c** = _{_ **c** mem _,_ **c** geo _}_ integrates historical context conditions **c** mem and dense geometric action conditions **c** geo. 

_B. World Model for Data Aggregation_ 


Fig. 4: Corrective Action Synthesis Module. 

With a trained EAC-WM, we now conduct data aggregation for imitation learning. First, we use the Corrective Action Synthesis Module to derive recovery actions, and then use the Consistency-Guided Filtering Module to filter the physically and visually inconsistent generated data. 

_1) Corrective Action Synthesis Module:_ This module leverages EAC-WM to synthesize recovery data for OOD states that deviate from the expert demonstrations. As shown in Figure 4, for an expert demonstration _τ_ = _{_ **a** _i,_ **I** _i}_<sup>_n_</sup> _i_ =1<sup>_∈_</sup> _D_ , a pivot timestep _m_ is randomly selected as the anchor for synthesis. The deviation horizon is defined as _k_ , and a random unit vector **v** _d ∈_ R<sup>3</sup> is sampled to represent the direction of a potential OOD state. To avoid misleading supervision, directions are filtered where the angle between **v** _d_ and the subsequent expert action **a** _m_ +1 is less than 120<sup>_◦_</sup> . This constraint ensures that synthesized recovery actions do not oppose the direction of expert trajectory, thereby preventing contradictory training signals that could lead to policy divergence. To maintain the speed of action consistent with the expert demonstration, the deviation displacement of each action in the synthesized recovery data is set to the average action displacement across Task Data _D_ . 

The synthesized trajectory _τ_<sup>_′_</sup> = _{_ **a**<sup>_′_</sup> _j_<sup>_,_ˆ</sup><sup>**I**</sup><sup>_j}_2</sup> _j_ =1<sup>_k_is constructed</sup> in two symmetric phases. First, in the _Deviation Phase_ ( _τd_<sup>_′_),</sup> the robot is steered from the expert pose at timestep _m_ to a perturbed OOD state along **v** _d_ . Second, in the _Recovery Phase_ ( _τr_<sup>_′_),therobotreturnsfromtheperturbedstateback</sup> to the original expert manifold at _m_ . Two phases follow the direction of **v** _d_ and _−_ **v** _d_ , respectively. Given the historical visual states **I** _m−p_ : _m_ and the synthesized action sequence **a**<sup>_′_</sup> 1:2 _k_<sup>as conditions, the world model predicts the visual states</sup> of the synthesized trajectory: 


Fig. 5: Consistency-Guided Filtering Module and Visualization of Real, Filtered, and Retained Frames. Frames with morphing and incorrect object position are filtered. 

For a whole synthesized trajectory _τ_<sup>_′_</sup> , we discard the Deviation Phase _τd_<sup>_′_,andonlytheRecoveryPhase</sup><sup>_τ ′_</sup> _r_<sup>is</sup> retained for policy training. This ensures that the model specifically learns to recover from OOD states. 

_2) Consistency-Guided Filtering Module:_ WMs inevitably produce hallucinations, such as object morphing or 


Fig. 6: Experimental setup and manipulation tasks. (a) Hardware configuration for data collection, featuring a handheld gripper integrated with a GoPro camera for visual observations and an HTC Vive Tracker for high-precision 6-DoF trajectory tracking. (b–e) The four evaluation tasks: (b) Soft Bag Pushing, (c) Pick-and-Place, (d) Ballot Insertion, and (e) Towel Folding. 

physically inconsistent object states. To ensure data fidelity, we introduce a Consistency-Guided Filtering Module to identify and discard these samples. Our insight is grounded in the temporal error accumulation inherent to WMs. Since the terminal frame<sup>ˆ</sup> **I** 2 _k_ is temporally most distant from the conditioning frames, it holds the maximum potential hallucination [22]. Consequently, it can serve as a rigorous proxy for the quality of the entire rollout: if<sup>ˆ</sup> **I** 2 _k_ remains consistent with the expert observation **I** _m_ which is at the same viewing location, we can reliably infer that the synthesized frames maintain high physical and visual integrity. 

To quantify the visual hallucination, we utilize a pretrained DINOv2 [23] encoder to extract embedding features of both frames and then calculate their cosine similarity. We employ an adaptive thresholding strategy, filtering out synthesized trajectories with below-average similarity scores to discard hallucinated samples. 

Figure 5 illustrates the filtering process. Figures 5(a) and (d) show the expert demonstration frames for soft bag pushing and pick-and-place, respectively. Figure 5(b) shows a discarded frame where image morphing occurs, while Figure 5(e) shows a discarded frame where the block’s location deviates from the expert reference. In contrast, Figures 5(c) and (f) are retained frames, where no significant hallucination is observed. 

## _C. Policy Training_ 

The training set, _D_ aug = _D ∪D_ virtual, is constructed by aggregating the expert demonstrations _D_ with the synthesized trajectories _D_ virtual. To promote temporal consistency of actions, we adopt the action chunking paradigm [24]. The policy is formulated to predict a sequence of future actions over a horizon _H_ given the observation **I** _t_ : **A**<sup>ˆ</sup> _t_ = _π_ ( **I** _t_ ) = [ˆ **a** _t,_ ˆ **a** _t_ +1 _, . . . ,_ ˆ **a** _t_ + _H−_ 1]. The policy is trained to minimize the Mean Squared Error between the predicted chunk and actions in the training set: 


By training on _D_ aug, the policy internalizes both the expert behaviors and the recovery ability under OOD states. 

## IV. EVALUATION 

We evaluate our framework across four tasks, as shown in Figure 6(b–e): soft bag pushing, pick-and-place, ballot insertion, and towel folding. These tasks test the framework across multiple dimensions, including 6-DoF action spaces, rigid and deformable object manipulation, generalization to novel object instances (pick-and-place, pushing), and highprecision, contact-rich control (insertion). 

On the soft bag pushing, we present visual comparisons of EAC-WM against the baseline generative model. We provide comparisons of success rate with baselines across all tasks, and ablation studies using soft bag pushing to justify our design choices. The subsequent subsections detail our experiment setups and provide experimental results. 

## _A. Experiment Setups_ 

_1) Hardware Platform:_ The data collection pipeline largely follows the Universal Manipulation Interface (UMI) framework [12]. As shown in Figure 6(a), we utilize a handheld two-finger gripper equipped with an eye-in-hand GoPro camera featuring a fisheye lens as the visual observation source. For demonstration pose collection, we capture the gripper’s 6-DoF pose using HTC Vive [25]. The robotic system includes a Universal Robots UR7e robotic arm and a Robotiq 2F-140 gripper with shark-fin fingertips. Models are trained on 4 and inferred on 1 NVIDIA L20 GPU. 

_2) World Model and Policy Architectures:_ We adopt EACWM as the generative world model, which is constructed on top of GE-Sim [18] and takes Cosmos-Predict2.5 (2B) [10] as its foundation model to synthesize high-fidelity, actionconditioned future observations. For the robotic policy, we adopt Gr00t N1.5 [26], a Vision-Language-Action model that serves as the policy model of our framework. 

_3) Baselines:_ We compare WM-DAgger against two baselines: **(1) Standard Behavioral Cloning (BC)** , a standard imitation learning baseline trained without data aggregation. It provides a reference for the performance degradation caused by OOD during deployment. **(2) Diffusion Meets DAgger (DMD)** [6], a SOTA method using diffusion-based synthesis for Data Aggregation. It serves as a baseline to demonstrate that WMs provide superior action-conditional physical consistency compared to standard generative augmentation approaches. 


Fig. 7: Visualization results of EAC-WM-generated frames. Each row depicts a specific task, starting from the real expert frame _It_ (first column). Subsequent columns ( _I_<sup>ˆ</sup> _t_ + _k_ ) show synthesized observations conditioned on action sequences in six cardinal directions (right, left, up, down, forward, and backward). 


Fig. 8: Visual evaluation of EAC-WM versus DMD in generating soft bag pushing data. EAC-WM exhibits superior structural and physical consistency. Notably, at t=16, EACWM accurately simulates the dynamics of the bag dropping. 

_4) Data Preparation:_ We collect 5 minutes of Play Data for each task. During Play Data collection, the demonstrator holds the gripper, randomly moves around the environment, and interacts with objects. During Task Data collection, we collect 20 human demonstrations for each task. We generate 1500 episodes of recovery actions per task by default. 

## _B. Visualization of Generated Data_ 

Figure 7 visualizes results synthesized by EAC-WM. Starting from an original real frame _It_ , EAC-WM generates synthesized observations _I_<sup>ˆ</sup> _t_ + _k_ conditioned on action sequences in six distinct spatial directions. As shown in 

the Figure, EAC-WM maintains high visual fidelity and physical consistency. It captures complex physical dynamics, including the deformation of the soft bag during pushing and the intricate wrinkling of the towel during folding. 

Furthermore, Figure 8 presents a comparison between EAC-WM and DMD. The top row displays the real frames from the expert demonstration, while the second and third rows show the synthesized frames. Both models are conditioned with the same action sequences to predict visual states at timesteps _t_ = 1, 6, 11, and 16. The results reveal that while DMD suffers from severe visual morphing, EAC-WM consistently preserves both structural and physical integrity of the frames. Notably, EAC-WM realistically simulates the complex physics of the bag dropping at _t_ = 16. 

## _C. Task 1: Soft Bag Pushing_ 

_1) Task Description:_ This task requires the robot to push a deformable soft bag across the workspace and deposit it into a target basket. This setup mirrors typical automated sorting scenarios in logistics. During data collection, the initial poses of the bag are randomized. For online validation, we evaluate the policy across ten bag locations, each with three trials, totaling 30 runs. 

_2) Overall Results:_ Table I presents the success rates across varying numbers of expert demonstrations. Standard BC severely struggles with compounding errors, with only 30.0% success rate even with 20 demonstrations. A typical failure mode involves the end-effector deviating from the correct trajectory and drifting into unrecoverable states, illustrating the classic phenomenon of compounding execu- 

TABLE I: Success Rates(%) for Task 1: Soft Bag Pushing across varying numbers of expert demonstrations. 

|**Method**|**1-shot**|**3-shot**|**5-shot**|**10-shot**|**20-shot**|
|---|---|---|---|---|---|
|Standard BC|6.7|20.0|26.7|30.0|30.0|
|DMD [6]|13.3|33.3|40.0|53.3|56.7|
|**Ours**|**73.3**|**86.7**|**93.3**|**93.3**|**96.7**|


tion errors. While DMD improves the 20-shot performance to 56.7%, it remains bottlenecked by a lack of actionconditioned physical consistency in the synthesized frames. Remarkably, WM-DAgger achieves a 73.3% success rate with only 1-shot demonstration. As demonstrations increase to 20, WM-DAgger reaches 96.7% success rate. These results validate that synthesizing physically consistent, goal-directed recovery trajectories via WMs effectively teaches the policy to recover from OOD states, thereby acting robustly with minimal human demonstration. 

in arbitrary directions rather than orienting toward the soft bag. This demonstrates that unconstrained recovery actions provide misleading supervision, driving the policy away from the task objective and resulting in collapse of performance. 

Second, we evaluate the Consistency-Guided Filtering Module by bypassing the filtering and retaining all generated trajectories (w/o Filter). Without this mechanism to discard visually and physically inconsistent frames, the success rate degrades to 46.7%. This performance drop confirms that unfiltered hallucinations can introduce biases into the training set, limiting the effectiveness of data aggregation. 

TABLE IV: Success Rates(%) for Task 2: Pick-and-Place. 

|||**Seen**||**Uns**|**een**|
|---|---|---|---|---|---|
|**Method**|**O1**|**O2**|**O3**|**O4**|**O5**|
|Standard BC|13.3|13.3|6.7|0.0|10.0|
|DMD|33.3|36.7|26.7|6.8|16.7|
|**Ours**|**83.3**|**90.0**|**80.0**|**63.3**|**76.7**|


TABLE II: Policy Performance vs. Data Scaling. 

## _D. Task 2: Pick-and-Place_ 

|**Synthesized Samples**|300|900|1500|3000|
|---|---|---|---|---|
|**Success Rate (%)**|46.7|63.3|96.7|96.7|


_3) Impact of Scaling Generated Data:_ We then study the impact of scaling WM-DAgger generated data for policy training. As summarized in Table II, the policy’s success rate exhibits a positive correlation with data scaling, as a larger synthetic dataset provides denser coverage of the OOD manifold. Notably, while performance improves significantly during the initial scaling phase, the gains begin to marginalize beyond 1500 samples, suggesting that a moderate amount of synthetic data is sufficient for the policy to effectively learn the OOD-recovery behaviors. 

TABLE III: Ablation Studies for 20-shot Soft Bag Pushing. 

|**Method / Variant**|**Success Rate (%)**|
|---|---|
|**WM-DAgger (Ours Full)**|**96.7**|
|_Data Ablation_<br>w/o Play Data|83.3|
|_Module Ablation_||
|w/o Filter|66.7|
|w/o Dir.|0.0|


_4) Impact of Play Data:_ Table III illustrates the impact of play data in fine-tuning the world model before synthesizing recovery data. When play data is excluded, the policy’s success rate drops from 96.7% to 83.3%. This decline demonstrates that exposing the world model to diverse environmental interactions is helpful for internalizing physical dynamics for synthesizing higher quality data. 

_5) Module Ablation Studies:_ We conduct ablation studies to evaluate the individual contributions of our designs, as summarized in Table III. First, we assess the impact of the Corrective Action Synthesis Module by removing the directional constraint (w/o Dir.). This omission leads to complete task failure (0.0% success rate). The observed failure mode involves the robot executing erratic movements 

_1) Task Description:_ This task requires reaching, grasping, and depositing a rigid object into a target box. We collect 20 expert demonstrations for each object. During online validation, we conduct 30 trials for each object. The evaluation comprises three _seen_ objects (present in the training data, and used for data aggregation) and two _unseen_ objects (not used in both training and data aggregation), allowing us to assess the system’s visual generalization capabilities. 

_2) Online Validation Results:_ Table IV presents the task success rates. Even on the seen objects (O1–3), Standard BC frequently fails due to compounding errors during the reaching and grasping phases. A frequent failure mode occurs when the gripper approaches the target but subsequently drifts away and fails to recover. In contrast, WM-DAgger achieves much higher success rates. By synthesizing recovery trajectories in OOD states, our framework equips the policy with robust recovery abilities. 

_3) Generalizability across Unseen Objects:_ When evaluating on unseen objects (O4–5), standard BC suffers from low success rates (0.0% and 10.0%). Conversely, WM-DAgger maintains moderate success rates (63.3% and 76.7%). By synthesizing diverse visual and physical states during the data aggregation phase, WM-DAgger prevents the policy from memorizing specific visual textures, enhancing generalizability across unseen objects. 

TABLE V: Success Rates for TABLE VI: Success Rates Ballot Insertion. for Towel Folding. 

|**Method**|**Succ. (%)**|**Method**|**Succ. (%)**|
|---|---|---|---|
|Standard BC|13.3|Standard BC|0.0|
|DMD|26.7|DMD|10.0|
|**Ours**|**73.3**|**Ours**|**46.7**|


_E. Task 3: Ballot Insertion_ 

_1) Task Description:_ The robot is required to grasp a deformable ballot paper and insert it into a narrow slot 

of a ballot box. It is highly challenging as it couples the manipulation of a deformable planar object with a highprecision, contact-rich insertion phase. We utilize this task to validate the capability of our framework to support tasks requiring high precision and complex physical interactions. 

_2) Online Validation Results:_ Table V presents the results. Standard BC struggles significantly, achieving only 13.3% success rate. As the insertion slot is narrow, minor execution drift could cause the ballot to miss the target or crumple against the box. In contrast, WM-DAgger achieves a much higher success rate of 73.3%. By synthesizing massive recovery actions, our method equips the policy with the closed-loop adjustment capabilities to re-align the ballot and successfully complete the high-precision insertion. 

## _F. Task 4: Towel Folding_ 

_1) Task Description:_ This task requires the robot to grasp and fold a deformable towel. Towel folding demands complex 6-DoF spatial trajectories. This experiment evaluates the framework’s scalability to more complex action spaces and severe morphological variations of the object. 

_2) Online Validation Results:_ The results are presented in Table VI. Operating in a 6-DoF action space exacerbates the compounding error problem for Standard BC, as errors in both position and orientation could accumulate, dropping success rate to 0.0%. For DMD, as generating physically consistent towel dynamics is difficult, the success rate is still low (10%). However, WM-DAgger achieves a success rate of 46.7%. The EAC-WM effectively simulates the deformable towel under 6-DoF manipulations, generating massive physically grounded recovery data for policy training. This allows the policy to complete the task more robustly. 

## V. CONCLUSION AND FUTURE WORK 

This paper presents WM-DAgger, a novel framework that leverages World Models to synthesize physically consistent recovery data for imitation learning. By integrating the Corrective Action Synthesis Module and the ConsistencyGuided Filtering Module, WM-DAgger enables policies to learn robust error-recovery behaviors, bypassing the need for expensive extra human demonstrations. Extensive real-world validations confirm significant improvements in success rates of four diverse tasks. Our results demonstrate that World Models can serve as scalable, high-fidelity supervisors for developing reliable embodied intelligence. 

While WM-DAgger demonstrates strong performance with two-finger grippers, scaling to dexterous multi-finger hands remains a challenge. The high DoF inherent in dexterous manipulation complicate the synthesis of visually and physically consistent articulated frames. In future work, we plan to address this by integrating morphological priors and kinematic topologies into the world model conditioning to support high-DoF dexterous manipulation. 

## REFERENCES 

- [1] S. Schaal, “Is imitation learning the route to humanoid robots?” _Trends in cognitive sciences_ , vol. 3, no. 6, pp. 233–242, 1999. 

- [2] M. Zare, P. M. Kebria, A. Khosravi, and S. Nahavandi, “A survey of imitation learning: Algorithms, recent developments, and challenges,” _IEEE Transactions on Cybernetics_ , vol. 54, no. 12, pp. 7173–7186, 2024. 

- [3] S. Bai, W. Song, J. Chen, Y. Ji, Z. Zhong, J. Yang, H. Zhao, W. Zhou, W. Zhao, Z. Li _et al._ , “Towards a unified understanding of robot manipulation: A comprehensive survey,” _arXiv preprint arXiv:2510.10903_ , 2025. 

- [4] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

- [5] M. Kelly, C. Sidrane, K. Driggs-Campbell, and M. J. Kochenderfer, “Hg-dagger: Interactive imitation learning with human experts,” in _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2019, pp. 8077–8083. 

- [6] X. Zhang, M. Chang, P. Kumar, and S. Gupta, “Diffusion meets dagger: Supercharging eye-in-hand imitation learning,” _arXiv preprint arXiv:2402.17768_ , 2024. 

- [7] J. Ding, Y. Zhang, Y. Shang, Y. Zhang, Z. Zong, J. Feng, Y. Yuan, H. Su, N. Li, N. Sukiennik _et al._ , “Understanding world or predicting future? a comprehensive survey of world models,” _ACM Computing Surveys_ , vol. 58, no. 3, pp. 1–38, 2025. 

- [8] X. Li, R. Song, Q. Xie, Y. Wu, N. Zeng, and Y. Ai, “Simworld: A unified benchmark for simulator-conditioned scene generation via world model,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 927–934. 

- [9] X. Li, X. He, L. Zhang, M. Wu, X. Li, and Y. Liu, “A comprehensive survey on world models for embodied ai,” _arXiv preprint arXiv:2510.16732_ , 2025. 

- [10] N. Agarwal, A. Ali, M. Bala, Y. Balaji, E. Barker, T. Cai, P. Chattopadhyay, Y. Chen, Y. Cui, Y. Ding _et al._ , “Cosmos world foundation model platform for physical ai,” _arXiv preprint arXiv:2501.03575_ , 2025. 

- [11] D. Brown, W. Goo, P. Nagarajan, and S. Niekum, “Extrapolating beyond suboptimal demonstrations via inverse reinforcement learning from observations,” in _International conference on machine learning_ . PMLR, 2019, pp. 783–792. 

- [12] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song, “Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots,” _arXiv preprint arXiv:2402.10329_ , 2024. 

- [13] X. Xu, Y. Hou, C. Xin, Z. Liu, and S. Song, “Compliant residual dagger: Improving real-world contact-rich manipulation with human corrections,” _arXiv preprint arXiv:2506.16685_ , 2025. 

- [14] T. Yu, G. Lu, Z. Yang, H. Deng, S. S. Chen, J. Lu, W. Ding, G. Hu, Y. Tang, and Z. Wang, “Manigaussian++: General robotic bimanual manipulation with hierarchical gaussian world model,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 12 232–12 239. 

- [15] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

- [16] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _Conference on robot learning_ . PMLR, 2023, pp. 2226–2240. 

- [17] Z. Jiang, K. Liu, Y. Qin, S. Tian, Y. Zheng, M. Zhou, C. Yu, H. Li, and D. Zhao, “World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation,” _arXiv preprint arXiv:2509.19080_ , 2025. 

- [18] Y. Liao, P. Zhou, S. Huang, D. Yang, S. Chen, Y. Jiang _et al._ , “Genie envisioner: A unified world foundation platform for robotic manipulation,” _arXiv preprint arXiv:2508.05635_ , 2025. 

- [19] W. Yifan, C. Doersch, R. Arandjelovi´c, J. Carreira, and A. Zisserman, “Input-level inductive biases for 3d reconstruction,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022, pp. 6176–6186. 

- [20] X. Liu, C. Gong, and Q. Liu, “Flow straight and fast: Learning to generate and transfer data with rectified flow,” _arXiv preprint arXiv:2209.03003_ , 2022. 

- [21] P. Esser, S. Kulal, A. Blattmann, R. Entezari, J. M¨uller, H. Saini _et al._ , “Scaling rectified flow transformers for high-resolution image synthesis,” 2024. [Online]. Available: https://arxiv.org/abs/2403.03206 

- [22] M. Zhao, H. Zhu, Y. Wang, B. Yan, J. Zhang, G. He, L. Yang, C. Li, 

and J. Zhu, “Ultravico: Breaking extrapolation limits in video diffusion transformers,” _arXiv preprint arXiv:2511.20123_ , 2025. 

- [23] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov _et al._ , “Dinov2: Learning robust visual features without supervision,” 2024. [Online]. Available: https://arxiv.org/abs/2304. 07193 

- [24] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” _arXiv preprint arXiv:2401.02117_ , 2024. 

- [25] J. Lwowski, A. Majumdat, P. Benavidez, J. J. Prevost, and M. Jamshidi, “Htc vive tracker: accuracy for indoor localization,” _IEEE Systems, Man, and Cybernetics Magazine_ , vol. 6, no. 4, pp. 15–22, 2020. 

- [26] NVIDIA, J. Bjorck, N. C. Fernando Casta˜neda, X. Da _et al._ , “GR00T N1: An open foundation model for generalist humanoid robots,” in _ArXiv Preprint_ , March 2025. 

