---
title: "ZeroWBC: Learning Natural Whole-Body Humanoid Interaction from Human Egocentric Data"
date: "2026-03-10"
authors: "Haoran Yang; Jiacheng Bao; Yucheng Xin; Haoming Song; Yuyang Tian; Bin Zhao"
url: https://arxiv.org/abs/2603.09170
pdf: https://arxiv.org/pdf/2603.09170
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.09170)** / [論文ページ](https://arxiv.org/abs/2603.09170)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ZeroWBC: Learning Natural Whole-Body Humanoid Interaction from Human Egocentric Data** 

**Haoran Yang**<sup>**1,2,***</sup> **Jiacheng Bao**<sup>**2,***</sup> **Yucheng Xin**<sup>**2,3,***</sup> **Haoming Song**<sup>**2,4**</sup> **Yuyang Tian**<sup>**1,2**</sup> **Bin Zhao**<sup>**2**</sup> **Dong Wang**<sup>**2,†**</sup> **Xuelong Li**<sup>**5**</sup> 

1University of Science and Technology of China 2Shanghai AI Laboratory 3Tsinghua University 4Shanghai Jiao Tong University 5TeleAI, China Telecom 

*Equal contribution †Corresponding author Project Website: ZeroWBC.github.io 


Figure 1: Overview of the ZeroWBC framework. The pipeline takes an initial egocentric image and text instruction as input (Left), synthesizes human whole-body motions via a fine-tuned vision-language model (Middle), and executes robot actions on the Unitree G1 robot using a general interactive tracking policy (Right). 

**Abstract:** Achieving versatile and natural whole-body humanoid interaction control remains challenging due to the high cost of whole-body teleoperation data. We present ZeroWBC, a teleoperation-free framework that learns humanoid wholebody interaction from human egocentric videos paired with synchronized wholebody motion and text annotations. ZeroWBC adopts a generation-then-tracking formulation to tackle the static scene whole-body interaction control problem. Given an initial egocentric image and a language instruction, a fine-tuned VisionLanguage Model generates future human whole-body motion tokens, which are decoded into continuous motions and retargeted to the humanoid. The resulting reference motions, together with root and key body-part trajectories, are then executed by a general interactive motion tracking policy. To improve interaction performance, we introduce an interaction-oriented tracking reward that prioritizes global root and key body-part trajectory alignment while preserving natural whole-body motion. Experiments on the Unitree G1 humanoid robot show that ZeroWBC enables diverse scene-aware behaviors without robot teleoperation demonstrations. These results suggest a scalable paradigm for learning natural humanoid whole-body interaction from human egocentric data. 

**Keywords:** Whole-body Control, Motion Generation, General Motion Tracking 

## **1 Introduction** 

Humanoid robots are expected to perform scene-aware whole-body interactions in complex realworld environments. Recent progress in humanoid control has improved the fidelity and robustness of tracking reference motions [1, 2, 3, 4, 5, 6], while large-scale motion generation and generationto-control pipelines [7, 8, 9, 10, 11, 12] have enabled diverse humanoid behaviors. However, most existing systems remain motion-centric, focusing on locomotion, dancing, or athletic skills, and thus provide limited capability for interacting with surrounding objects and scene geometry. Existing visual humanoid control systems typically rely on either large-scale robot teleoperation data [13, 14, 15] or task-specific reinforcement learning in simulation [16, 17]. The former is expensive to collect and often uses decoupled upper and lower-body control [14, 18, 19, 20], limiting natural coordination, while the latter is restricted to narrow tasks and vulnerable to sim-to-real gaps. 

The high cost of whole-body teleoperation data motivates human demonstrations as an alternative supervision source. Human egocentric videos paired with synchronized whole-body motions and text annotations provide first-person scene observations, dense whole-body motion labels, and tasklevel semantics at lower cost. In real-world setup, humanoid robot whole-body teleoperation typically requires two operators to collect about 100 demonstrations in 8 hours, whereas a single human demonstrator can collect about 300 egocentric motion demonstrations in 2 hours in the same task. 

To transform human demonstrations into executable humanoid behaviors, we adopt a generationthen-tracking formulation. A high-level model generates all future human whole-body interaction motions from an initial egocentric image and a language instruction, while a low-level tracking policy retargets and executes all motions at once. This open-loop design is practical for current VisionLanguage models, whose inference latency makes high-frequency closed-loop control difficult, and is well suited to many mostly static interaction tasks where the initial observation provides sufficient spatial context. Moreover, preserving interaction precision after human-to-humanoid transfer remains challenging due to morphology, joint-limit, and contact differences. Pure joint-space tracking may reproduce retargeted poses but misalign task-critical points, such as hands for object transport, or root for sitting. We therefore train a general interactive motion tracking policy that tracks both the retargeted robot motion and the human-derived global root and key body-part trajectories, preserving task-critical spatial intent while maintaining natural whole-body motion. 

To this end, we introduce **ZeroWBC** , a two-stage framework for teleoperation-free humanoid static scene whole-body interaction control. As illustrated in Figure 1, ZeroWBC first discretizes human motions into motion tokens using a VQ-VAE tokenizer. A fine-tuned Vision-Language Model then autoregressively predicts all future whole-body motion tokens conditioned on the initial egocentric observation and language instruction. The generated motions are decoded, retargeted to the humanoid, and executed by the general interactive tracking policy using global root and key bodypart trajectories with retargeted robot motions. By learning from human egocentric videos with synchronized human whole-body motions and text annotations, ZeroWBC enables diverse static scene-aware whole-body interaction without large-scale robot teleoperation demonstrations. 

In summary, our contributions are: 1) **Teleoperation-free for humanoid interaction:** We introduce a scalable supervision paradigm that learns scene-aware humanoid whole-body interaction from human egocentric videos paired with synchronized human motion and text annotations, avoiding the need for costly robot teleoperation demonstrations. 2) **Generation-to-Tracking framework:** We propose ZeroWBC, a two-stage framework that converts an initial egocentric image and a language instruction into executable humanoid whole body interaction behaviors. 3) **Interaction-oriented general tracking :** We design a tracking objective that emphasizes global root and key body-part trajectory alignment, enabling the humanoid to better preserve task-critical interaction intent during physical execution. 

2 

## **2 Related Work** 

**Multimodal Motion Generation.** Text-conditioned human motion generation has become increasingly mature [21, 22, 23, 24, 25, 26, 27, 28]. Leveraging the pre-trained knowledge of Large Language Models (LLMs), autoregressive methods such as MotionGPT [24, 23] and T2M-GPT [27] generate human motions by predicting discrete motion tokens, showing stronger semantic understanding, generalization, and inference efficiency than diffusion-based approaches [29, 30, 31]. Recent multimodal frameworks, such as M3GPT [32] and MotionCraft [33], further incorporate music and spatial trajectories as conditions. However, motion generation from egocentric image and language remains largely underexplored due to data scarcity and the lack of suitable deployment platforms. Since real-world humanoid robots rely on egocentric perception, it is crucial to generate human interactive motions from both visual observations and textual instructions. 

**Humanoid Whole-body Control.** Humanoid whole-body control has evolved from task-specific reinforcement learning for isolated skills such as robust locomotion [34] and parkour [35], toward data-driven motion imitation for tracking human references [2, 13, 36, 37]. Early works such as ExBody [36] explored decoupled control, while OmniH2O [37] established a teacher-student distillation pipeline for unified whole-body control. More recently, BeyondMimic [1] achieved high-fidelity tracking of single reference motions. The field is now moving toward General Motion Tracking, which aims to track arbitrary motion references without per-motion reward engineering. Along this line, GMT [38], PhyGile [39], and SONIC [12] improve adaptability and scalability across diverse skills, while SONIC [12], Twist2 [15] applies a general tracker to holistic whole-body teleoperation. 

**Visual Humanoid Control.** Visual humanoid control aims to integrate perception and control, but existing methods remain limited in task complexity, motion naturalness, and data scalability. Keypoint-based methods such as HEAD [40] introduce egocentric vision but are mainly restricted to simple navigation, while VideoMimic [41] enables interaction through a real2sim2real pipeline but lacks first-person perception and still suffers from a sim-to-real gap. High-level planning methods such as LEVER-B [42] rely on simulation and third-person observations, making them sensitive to domain shifts and instruction variations. Task-specific methods such as VisualMimic [16] and Doorman [17] also suffer from limited generalization and sim-to-real gaps. Meanwhile, HumanoidVLA [35] mainly focuses on locomotion, and WholebodyVLA [14] constrains lower-body motion through decoupled strategies, limiting natural whole-body behaviors. Although Twist2 [15] demonstrates holistic control, it depends on costly, hardware-specific teleoperation data. 

## **3 Method** 

As illustrated in Fig. 2, ZeroWBC adopts a hierarchical two-stage framework for vision-conditioned humanoid whole-body scene-interaction. In the first stage, a VQ-VAE [43] encodes continuous human motions into discrete motion tokens. A Vision-Language Model is then fine-tuned on imagetext-motion pairs for cross-modal alignment, enabling it to predict motion tokens from visual and textual prompts. These tokens are decoded into continuous human motions by a motion decoder. In the second stage, we train a general interactive motion tracker with reinforcement learning and curriculum learning. The tracker maps key interaction position trajectories and robot reference motions derived from human motions into robot joint commands. 

### **3.1 Data Collection** 

Robot teleoperation data collection is difficult and costly, as it requires precise coordination between the robot and the operator, making large-scale acquisition impractical. We instead adopt a humancentric data collection pipeline. Our setup combines a chest-mounted GoPro camera with an inertial or optical motion capture system, requiring only a MoCap suit and a portable action camera. This design is low-cost and highly scalable. During inference, the robot uses the same camera configuration for perception. To reduce the domain gap between human and robot viewpoints, we align the camera height during data collection with the robot camera height. 

3 


Figure 2: Detailed architecture of ZeroWBC. (a) A fine-tuned Qwen-VL predicts motion tokens from an initial egocentric image and language instruction, which are decoded into continuous human whole-body motions. (b) The generated motions are retargeted to the humanoid and executed by an RL-based policy that tracks both robot reference motions and interaction-relevant body parts. 

### **3.2 Motion Tokenizer** 

We adopt a VQ-VAE [43] tailored to SMPL [44] human-motion data, which compresses continuous high-dimensional motion sequences into compact discrete motion tokens for downstream generation. Given a motion clip of length _ni_ , the encoder downsamples it into a latent sequence of length _nt_ , where _ni_ = _nt ·_ 2<sup>_ndown_</sup> and _ndown_ is the number of downsampling blocks. The quantized latent tokens are then reconstructed by a lightweight decoder to the original motion resolution. Both the encoder and decoder follow a ResNet-based architecture. For each motion sequence **m** , we represent its SMPL pose as **m** smpl _∈_ R<sup>66</sup> and global translation as **m** trans _∈_ R<sup>3</sup> . To improve reconstruction quality and physical plausibility, we train the motion VQ-VAE with reconstruction, commitment, velocity, root-rotation, and global-translation losses. 

### **3.3 Fine-tuning Vision-Language Model** 

We adopt the pre-trained Qwen2.5-VL-3B [45] as the backbone for multimodal motion generation. Our goal is to align the discrete motion space with the existing vision-language embedding space of the Qwen-VL, such that whole-body motion generation can be formulated as a standard next-token prediction task. Specifically, we convert the quantized indices from the VQ-VAE codebook into special motion tokens, e.g., _⟨_ motion ~~t~~ oken ~~1~~ _⟩_ , and add them to the Qwen-VL vocabulary. 

Given an initial egocentric visual observation **v** and a language instruction **t** , the model autoregressively predicts the complete future motion sequence in one generation pass. This corresponds to our open-loop motion planning setting, where all motion tokens required for the task are generated before execution rather than updated online during tracking. Formally, for a target motion token sequence **z** = _{z_ 1 _, z_ 2 _, . . . , zT }_ , we optimize the model parameters _θ_ by minimizing the negative log-likelihood: 


where _z<i_ denotes previously generated motion tokens. The generated token sequence is then decoded by the VQ-VAE decoder into a continuous human motion trajectory. 

4 

To improve both generalization and spatial grounding, we use a two-stage fine-tuning strategy. In the first stage, the model is trained on large-scale public image-text-motion data to learn general cross-modal alignment between visual-language inputs and motion tokens. In the second stage, we further fine-tune the model on our self-collected egocentric dataset, which provides higher-quality first-person observations and synchronized whole-body motion labels for interaction tasks. This domain-specific fine-tuning improves the model’s ability to generate spatially grounded and physically plausible motions from the robot-aligned egocentric view. 

### **3.4 General Interactive Motion Tracking** 

We train a unified control policy to track diverse whole-body motion capture sequences. To improve stability across heterogeneous motion styles and difficulty levels, we combine adaptive motion scheduling, progressive difficulty exposure, and future motion conditioning. 

**Tracking objectives.** We formalize the tracking objective of our motion interactive tracker as a composite target vector: 


where _DG_ denotes the total dimension of the tracking target. The target _G_ is decomposed into two components: the interactive trajectories of key body-parts **g** inter and a retargeted reference motion **m** ref. 

The interactive trajectories of key body parts encode the global trajectories of key end-effector and humanoid root frames for environment interaction. It is defined as: 


where _p_ k _∈_ R<sup>3</sup> , _p_ ˙k _∈_ R<sup>3</sup> denotes the global position and the linear velocity of the corresponding key body part k = _{_ root, left wrist, right wrist, left foot, right foot _}_ , _w_ root _∈_ R<sup>3</sup> means the angular velocity of the root. All these quantities are extracted from the generated human motion sequence in SMPL format. 

The reference motion target specifies the joint-level kinematic reference for the robot, obtained via motion retargeting from human to Unitree G1 kinematics. It is given by: 


where _q_ ref _∈_ R<sup>_nj_</sup> is the reference joint angular vector, _q_ ˙ref _∈_ R<sup>_nj_</sup> is the reference joint angular velocity vector, and _nj_ = 23 is the number of joints. 

The optimization of the tracking objectives is embedded into the design of the imitation learning framework for the general interactive motion tracking policy. As summarized in Table 9 in Appendix, we augment the observation space with measurements of the interactive trajectories **g** inter of key body parts to explicitly encode task-relevant interaction dynamics. Meanwhile, as detailed in Table 7 in Appendix, the reward function is formulated to prioritize the tracking of interactive trajectories while attenuating the penalty for joint-space deviations from the reference motion **m** ref. 

This weighted formulation enables the policy to learn the intended motion patterns while enforcing end-effector compliance with the world-space trajectories of critical interaction points. Consequently, the robot maintains precise alignment with task-essential kinematic constraints, leading to improved task completion performance. 

**Adaptive Motion Scheduling.** We treat each motion clip as an independent training unit and assign it a dynamic sampling weight according to its current tracking difficulty. For each motion file _i_ , we maintain an EMA tracking error _Ei_ and EMA success/failure statistics, from which we estimate the success probability _p_ ˆ<sup>succ</sup> _i_ . The final difficulty score combines persistent tracking error with failure 

5 

frequency: 


where _c_ normalizes the tracking error and _w_ balances the error-based and failure-based terms. We convert _ri_ into sampling probabilities using a temperature-scaled softmax with a uniform exploration term, prioritizing difficult clips while preserving coverage of all motions. 

**Progressive Difficulty Exposure.** Because highly complex motions can hinder early-stage convergence, we organize motion files into difficulty levels according to semantic and kinematic complexity and progressively expand the training set. Training starts from the lowest level. Let _l_ max denote the highest unlocked level. The curriculum advances when the current level satisfies the MPJPE and MPJAE thresholds, or after a fixed number of iterations: 


Within the unlocked set, sampling favors the most recently introduced level, while a minimum ratio for each unlocked level mitigates catastrophic forgetting. Newly unlocked clips are introduced gradually to avoid abrupt distribution shifts. 

**Temporal Conditioning with Future Motion Encoding.** To anticipate upcoming movements, we augment the policy with a future motion encoder and train it with asymmetric PPO. The critic observes privileged reference and future motion states during training, while the actor uses only compact test-time observations, improving value estimation without increasing deployment complexity. The actor input includes proprioceptive states and a motion command composed of current, short-horizon, and long-horizon target poses. Current and short-horizon targets support near-term tracking, while long-horizon targets are encoded by a lightweight temporal convolutional encoder to capture global motion trends. This multi-scale conditioning helps the policy anticipate velocity changes, directional transitions, and contact events, improving tracking stability for dynamic motions. Additional observation details are provided in the Appendix. 

## **4 Experiment** 

In this section, we evaluate ZeroWBC on multimodal motion generation, interactive motion tracking, and real-world humanoid interaction tasks on Unitree G1 robot. 

### **4.1 Dataset** 

We use three datasets for training and evaluation. **Nymeria** [46] provides 300 hours of synchronized egocentric video, whole-body motion, and language annotations, which we process into 5–10s image-text-SMPL clips for first-stage vision-language-motion alignment. **HumanML3D** [47] contains 14,616 text-annotated 3D motion sequences, and is used to strengthen text-motion alignment and pretrain the interaction tracker after retargeting to Unitree G1 with GMR [48]. **Self-collected Dataset** contains 5 hours of egocentric data covering navigation, box moving, and sofa sitting under varied scenes and object placements. We use it for second-stage VLM fine-tuning and task-adaptive tracker fine-tuning. More details are provided in the Appendix. 

### **4.2 Evaluation on Multimodal Motion Generation** 

We evaluate the motion generation module on Nymeria and our self-collected dataset using standard metrics, including FID, R-Precision, and MM-Dist. We first train the VQ-VAE on all datasets for motion tokenization, and then fine-tune Qwen2.5-VL-3B in two stages. The first stage uses about 200 hours of image-text-motion data from Nymeria and 25 hours of text-motion data from HumanML3D to learn general visual-language-motion alignment. The second stage further fine-tunes the model on our self-collected egocentric data to improve spatial grounding for interaction tasks. To preserve the pretrained Qwen-VL capability, only the LM decoder is fine-tuned, while the remaining parameters are frozen. This phase utilizes 32 NVIDIA A100 GPUs for training and inference. 

6 

As shown in Table 1, joint training Table 1: Motion generation results with different fine-tuning with Nymeria and HumanML3D data on Nymeria and self-collected test sets. further improves over single- **Test Set Training Data FID** _↓_ **R@3** _↑_ **MM-Dist** _↓_ dataset training, and second-stage Nymeria 0.756 0.755 3.124 fine-tuning on our self-collected Nymeria Nymeria+HumanML3D 0.423 0.828 2.514 data achieves the best perforN + H + Self-collected **0.298 0.847 2.286** mance on both Nymeria and self-collected test sets. These reNymeria 0.784 0.782 3.456 Self-Coll Nymeria+HumanML3D 0.628 0.825 3.128 sults suggest that large-scale public N + H + Self-collected **0.245 0.892 2.456** data provides general motion priors, while self-collected egocentric data improves in-domain interactive spatial grounding. Table 2 compares ZeroWBC with the text-to-motion baseline MotionGPT under the same Nymeria training and testing setting. ZeroWBC achieves better FID, Top-3 R-Precision, and MM-Dist, showing that egocentric visual context improves motion generation beyond language-only conditioning. Additional modality and training-data ablations are reported in the Appendix. 

### **4.3 Evaluation on General Interactive Motion Tracking** 

|We evaluate general whole-body motion<br>tracking on two settings:<br>HumanML3D<br>dGtiidiT|Table 2: Evaluation of mot<br>compare ZeroWBC with th|ion generation quality. We<br>e baseline MotionGPT.|
|---|---|---|
|an eneraon, as summarze n a-<br>ble<br>11.<br>All<br>motion<br>tracking<br>poli-|**Method**<br>**FID**_↓_|**R-Prec (T3)**_↑_<br>**MM-Dist**_↓_|
|cies are trained on two NVIDIA RTX<br>4090 GPUs for approximately 14 days.|MotionGPT [23]<br>0.869<br>**ZeroWBC (Ours)**<br>**0.756**|0.536<br>3.139<br>**0.755**<br>**3.124**|
|Table 3: <br>indicate b<br>HumanML3D follows the defi-<br>nition in Section41while Gen-|Joint-level motion tracking <br>etterperformance.|evaluation. Lower values|


HumanML3D follows the definition in Section 4.1, while Generation evaluates motions produced by the multimodal motion generation module. We report joint-level tracking metrics in world coordinates: Mean PerJoint Position Error (MPJPE, m), Mean Per-Joint Angle Error (MPJAE, rad), Mean Per-Joint Velocity Error (MPJVE, rad/s), Mean Per-Interactive-Body-Part Position Error (MPIPE, m), and 

|Data|Method|MPJPE_↓_|MPJAE_↓_|MPJVE_↓_|MPIPE_↓_|MPIVE_↓_|
|---|---|---|---|---|---|---|
||GMT [38]|0.5530|0.1046|0.4882|0.3821|0.3216|
||SONIC [12]|**0.2526**|0.0957|**0.3906**|0.2108|0.1992|
|HML3D|w/o Curr.|0.5991|0.0953|0.6206|0.4125|0.3501|
|uman|w/o A.S.|0.5808|0.1047|0.5520|0.3987|0.3378|
||w/o F.C.|0.4619|0.0820|0.4912|0.3012|0.2645|
||**Ours**|0.2571|**0.0734**|0.4378|**0.1885**|**0.1753**|
||GMT|0.6013|0.1375|0.5112|0.4219|0.3654|
||SONIC|**0.3340**|**0.1058**|0.4691|0.2671|0.2318|
|Gi|w/o Curr.|0.6637|0.1319|0.6474|0.4789|0.4123|
|eneraton|w/o A.S.|0.6124|0.1268|0.6293|0.4452|0.3876|
||w/o F.C.|0.5259|0.1137|0.4992|0.3765|0.3296|
||**Ours**|0.3653|0.1074|**0.4680**|**0.2138**|**0.2005**|


Mean Per-Interactive-Body-Part Velocity Error (MPIVE, m/s). We compare with GMT [38] and SONIC [12], and include ablations removing current-frame targets (w/o Curr.), adaptive scheduling (w/o A.S.), and future conditioning (w/o F.C.). All methods are evaluated under identical tracking settings. As shown in Table 11, our method consistently outperforms GMT across both HumanML3D and Generation. Compared with the stronger SONIC baseline, our method remains competitive, achieving the best MPJAE on HumanML3D and the best MPJVE on Generation, while SONIC obtains lower MPJPE on both settings. For both MPIPE and MPIVE, our method achieves the best performance. This trade-off arises because SONIC prioritizes overall joint-level tracking accuracy, whereas our method emphasizes interactive trajectory tracking, leading to superior performance on interaction-related metrics. The ablation results show that all components contribute to robust general motion tracking. 

We evaluate ZeroWBC on a Unitree G1 humanoid robot across real-world interaction tasks, including navigation, obstacle avoidance, ball kicking, sofa sitting, and box moving. Each episode lasts 10–20 seconds and requires whole-body motion with scene geometry. A GoPro camera mounted on the robot’s chest provides the initial egocentric observation, which is sent to a local server running the fine-tuned Qwen-VL model. The generated human motion is decoded, retargeted to the G1 

7 


Figure 3: Real-world interaction results on Unitree G1. **Few-shot generalization** : the robot performs seen task categories under changed object placements, scene layouts, and initial poses. **Zeroshot capabilities** : the robot performs unseen object-task combinations, including chair navigation and chair sitting, despite the absence of chair-related demonstrations during training. 

robot, and executed by the tracking policy. Full-system comparisons with other methods are limited because few open-source humanoid interaction methods support whole-body control. 

### **4.4 Real-World Evaluation** 

**Few-shot evaluation.** Each few-shot task is evaluated over 50 real-world trials, where the task and object categories appear in the training data, but the test environments use different object placements, spatial layouts, and robot initial poses. As shown in Table 4, the interactive tracker achieves 

Table 4: Few-shot real-world success rates. 

|**Task**|**General Tracker**|**Interactive Tracker**|
|---|---|---|
|Obstacle Avoidance|80%|**96%**|
|Ball Kicking|60%|**78%**|
|Sofa Sitting|48%|**84%**|
|Box moving|16%|**64%**|


high success rates on obstacle avoidance, ball kicking, box moving, and sofa sitting, outperforming the general tracker by better preserving human motion root and key body-part trajectories. The general tracker adopts SONIC as the baseline. 

**Zero-shot evaluation.** We further evaluate zero-shot generalization on tasks and object categories completely absent from the training data, including unseen chair navigation and chair sitting. Each task is evaluated over 50 trials with varied object poses, robot initial positions, and four different chair types. ZeroWBC achieves success rates of 90.0% for chair navigation and 76.0% for chair sitting. These results suggest that Qwen-VL provides useful semantic priors for unseen objects and tasks, while the tracking policy enables feasible whole-body execution. 

## **5 Conclusion** 

We present ZeroWBC, a robot teleoperation-free generation-then-tracking framework that turns human egocentric videos with synchronized whole-body motion and text into executable static humanoid interaction behaviors. By coupling egocentric motion generation with general interactive tracking, ZeroWBC shows that scalable human demonstrations can provide effective supervision for scene-aware whole-body humanoid control in low cost. Experiments in simulation and on Unitree G1 demonstrate natural and diverse behaviors from a single initial image and language instruction, offering a practical path toward learning humanoid interaction without robot teleoperation. 

## **6 Limitations** 

ZeroWBC is designed for mostly static scenes. Our experiments show that its open-loop generationthen-tracking strategy works well for static scene-aware tasks, but it cannot replan when objects or humans move after the initial observation. Our closed-loop tests show about 400 ms latency 

8 

even for short-horizon generation, causing phase lag and jitter. Future work will explore faster generation, model distillation, and closed-loop replanning. Contact-rich tasks remain challenging. In box moving, the robot can often approach and lift the box, but may drop it during transport due to limited hand friction and the lack of force or tactile feedback. Future work will incorporate tactile sensing, force feedback, and contact-aware tracking. Finally, our experiments are limited to Unitree G1 and a small set of tasks; deployment on other humanoids may require embodiment-aware retargeting and tracker adaptation. 

9 

## **References** 

- [1] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [2] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _arXiv preprint arXiv:2506.12851_ , 2025. 

- [3] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid wholebody skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [4] T. Huang, H. Wang, J. Ren, K. Yin, Z. Wang, X. Chen, F. Jia, W. Zhang, J. Long, J. Wang, and J. Pang. Towards Adaptable Humanoid Control via Adaptive Motion Tracking, Oct. 2025. 

- [5] G. B. Margolis, M. Wang, N. Fey, and P. Agrawal. SoftMimic: Learning Compliant Wholebody Control from Examples, Oct. 2025. 

- [6] W. Zeng, S. Lu, K. Yin, X. Niu, M. Dai, J. Wang, and J. Pang. Behavior Foundation Model for Humanoid Robots, Sept. 2025. 

- [7] Y. Shao, X. Huang, B. Zhang, Q. Liao, Y. Gao, Y. Chi, Z. Li, S. Shao, and K. Sreenath. Langwbc: Language-directed humanoid whole-body control via end-to-end learning. _arXiv preprint arXiv:2504.21738_ , 2025. 

- [8] Z. Li, C. Chi, Y. Wei, B. Zhu, Y. Peng, T. Huang, P. Wang, Z. Wang, S. Zhang, and C. Xu. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. _arXiv preprint arXiv:2510.14952_ , 2025. 

- [9] J. Yue, Z. Wang, Y. Wang, W. Zeng, J. Wang, X. Xu, Y. Zhang, S. Zheng, Z. Ding, and Z. Lu. Rl from physical feedback: Aligning large motion models with humanoid control. _arXiv preprint arXiv:2506.12769_ , 2025. 

- [10] P. Li, Z. Zhuang, Y. Gao, Y. Dong, S. Li, C. Jiang, S. Dou, Z. Xi, E. Zhou, J. Huang, et al. From-w1: Towards general humanoid whole-body control with language instructions. _arXiv preprint arXiv:2601.12799_ , 2026. 

- [11] N. Jiang, Z. He, W. Yu, L. Pang, Y. Li, H. Li, J. Cui, Y. Li, Y. Wang, Y. Zhu, et al. Uniact: Unified motion generation and action streaming for humanoid robots. _arXiv preprint arXiv:2512.24321_ , 2025. 

- [12] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta˜neda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [13] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ , 2024. 

- [14] H. Jiang, J. Chen, Q. Bu, L. Chen, M. Shi, Y. Zhang, D. Li, C. Suo, C. Wang, Z. Peng, et al. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. _arXiv preprint arXiv:2512.11047_ , 2025. 

- [15] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [16] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

10 

- [17] H. Xue, T. He, Z. Wang, Q. Ben, W. Xiao, Z. Luo, X. Da, F. Casta˜neda, G. Shi, S. Sastry, et al. Opening the sim-to-real door for humanoid pixel-to-action policy transfer. _arXiv preprint arXiv:2512.01061_ , 2025. 

- [18] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [19] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive whole-body control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [20] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _arXiv preprint arXiv:2505.03738_ , 2025. 

- [21] H. Ahn, T. Ha, Y. Choi, H. Yoo, and S. Oh. Text2action: Generative adversarial synthesis from language to action. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5915–5920. IEEE, 2018. 

- [22] C. Guo, X. Zuo, S. Wang, and L. Cheng. Tm2t: Stochastic and tokenized modeling for the reciprocal generation of 3d human motions and texts. In _European Conference on Computer Vision_ , pages 580–597. Springer, 2022. 

- [23] B. Jiang, X. Chen, W. Liu, J. Yu, G. Yu, and T. Chen. Motiongpt: Human motion as a foreign language. _Advances in Neural Information Processing Systems_ , 36:20067–20079, 2023. 

- [24] Y. Zhang, D. Huang, B. Liu, S. Tang, Y. Lu, L. Chen, L. Bai, Q. Chu, N. Yu, and W. Ouyang. Motiongpt: Finetuned llms are general-purpose motion generators. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 7368–7376, 2024. 

- [25] H. Song, D. Qu, Y. Yao, Q. Chen, Q. Lv, Y. Tang, M. Shi, G. Ren, M. Yao, B. Zhao, et al. Hume: Introducing system-2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ , 2025. 

- [26] C. Zhong, L. Hu, Z. Zhang, and S. Xia. Attt2m: Text-driven human motion generation with multi-perspective attention mechanism. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 509–519, 2023. 

- [27] J. Zhang, Y. Zhang, X. Cun, Y. Zhang, H. Zhao, H. Lu, X. Shen, and Y. Shan. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 14730–14740, 2023. 

- [28] H. Liang, J. Bao, R. Zhang, S. Ren, Y. Xu, S. Yang, X. Chen, J. Yu, and L. Xu. Omg: Towards open-vocabulary motion generation via mixture of controllers. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 482–493, 2024. 

- [29] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ , 2022. 

- [30] M. Zhang, Z. Cai, L. Pan, F. Hong, X. Guo, L. Yang, and Z. Liu. Motiondiffuse: Text-driven human motion generation with diffusion model. _IEEE transactions on pattern analysis and machine intelligence_ , 46(6):4115–4128, 2024. 

- [31] X. Chen, B. Jiang, W. Liu, Z. Huang, B. Fu, T. Chen, and G. Yu. Executing your commands via motion diffusion in latent space. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18000–18010, 2023. 

- [32] M. Luo, R. Hou, Z. Li, H. Chang, Z. Liu, Y. Wang, and S. Shan. M<sup>3</sup> gpt: An advanced multimodal, multitask framework for motion comprehension and generation. _Advances in Neural Information Processing Systems_ , 37:28051–28077, 2024. 

11 

- [33] Y. Bian, A. Zeng, X. Ju, X. Liu, Z. Zhang, W. Liu, and Q. Xu. Motioncraft: Crafting wholebody motion with plug-and-play multimodal controls. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 1880–1888, 2025. 

- [34] Z. Chen, X. He, Y.-J. Wang, Q. Liao, Y. Ze, Z. Li, S. S. Sastry, J. Wu, K. Sreenath, S. Gupta, et al. Learning smooth humanoid locomotion through lipschitz-constrained policies. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 4743– 4750. IEEE, 2025. 

- [35] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. _arXiv preprint arXiv:2406.10759_ , 2024. 

- [36] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [37] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [38] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [39] J. Bao, H. Yang, Y. Xin, J. Liu, Y. Xu, H. Liang, P. Han, X. Ma, D. Wang, and B. Zhao. Phygile: Physics-prefix guided motion generation for agile general humanoid motion tracking. _arXiv preprint arXiv:2603.19305_ , 2026. 

- [40] S. Chen, Y. Ye, Z.-a. Cao, J. Lew, P. Xu, and C. K. Liu. Hand-eye autonomous delivery: Learning humanoid navigation, locomotion and reaching. _arXiv preprint arXiv:2508.03068_ , 2025. 

- [41] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [42] H. Xue, X. Huang, D. Niu, Q. Liao, T. Kragerud, J. T. Gravdahl, X. B. Peng, G. Shi, T. Darrell, K. Sreenath, et al. Leverb: Humanoid whole-body control with latent vision-language instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

- [43] A. Van Den Oord, O. Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- [44] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black. SMPL: A skinned multiperson linear model. _ACM Trans. Graphics (Proc. SIGGRAPH Asia)_ , 34(6):248:1–248:16, Oct. 2015. 

- [45] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- [46] L. Ma, Y. Ye, F. Hong, V. Guzov, Y. Jiang, R. Postyeni, L. Pesqueira, A. Gamino, V. Baiyya, H. J. Kim, et al. Nymeria: A massive collection of multimodal egocentric daily motion in the wild. In _European Conference on Computer Vision_ , pages 445–465. Springer, 2024. 

- [47] C. Guo, S. Zou, X. Zuo, S. Wang, W. Ji, X. Li, and L. Cheng. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 5152–5161, June 2022. 

- [48] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

12 

## **A Dataset Details** 

We use three datasets in ZeroWBC: Nymeria, HumanML3D, and our self-collected egocentric interaction dataset. All datasets are split into training and testing subsets with an 8:2 ratio at the sequence level. The training split is used for motion tokenizer training, Qwen-VL fine-tuning, and tracking policy training, while the test split is only used for evaluation. 

**Nymeria Dataset.** Nymeria [46] is a large-scale multimodal egocentric dataset containing approximately 300 hours of daily human activities. It provides synchronized egocentric videos, human whole-body motion captured by XSens, and hierarchical language annotations. In our work, we process Nymeria into 5–10 second clips, where each sample consists of an initial egocentric image, a text instruction, and a synchronized SMPL-formatted whole-body motion sequence. After preprocessing, we obtain approximately 140k training samples and 20k testing samples. Nymeria is mainly used for training the VQ-VAE motion tokenizer and for the first-stage fine-tuning of Qwen-VL. 

**HumanML3D Dataset.** HumanML3D [47] contains 14,616 high-quality 3D human motion sequences, corresponding to about 28.59 hours of motion data, paired with precise textual annotations. Since HumanML3D does not contain egocentric images, we use it as text-motion supervision. HumanML3D is used for both training and evaluation in the two stages of ZeroWBC. First, it is cotrained with Nymeria during Qwen-VL fine-tuning to improve text-motion alignment and diversify language-conditioned motion generation. Second, we retarget its human motions to the Unitree G1 robot using GMR [48], and extract the corresponding global root, hand, and foot trajectories from the original human motions. The retargeted robot motions and these key body-part trajectories are then used to pretrain and evaluate the general interactive tracking policy, providing diverse human whole-body motion priors before task-specific adaptation. 

**Self-collected Dataset.** To improve spatial grounding and in-domain interactive motion quality, we further collect a human egocentric interaction dataset following the protocol described in Section 3.1. The dataset contains approximately 5 hours of synchronized egocentric video, whole-body motion, and text annotations. It covers four representative static-scene whole-body interaction tasks: box moving, ball kicking, sofa sitting, and obstacle avoidance. Each task contains approximately 300-400 motion sequences, resulting in about 1,500 sequences in total. Each sequence lasts approximately 5–15 seconds, depending on the task. During collection, we vary object positions, scene layouts, backgrounds, and human initial poses to improve robustness to spatial variations. This dataset is mainly used for the second-stage Qwen-VL fine-tuning and task-adaptive tracker fine-tuning, allowing ZeroWBC to better learn object-aware and spatially grounded whole-body interaction behaviors. 


For the self-collected dataset, whole-body human motion is captured using an optical motion capture system and then converted into the SMPL format. Egocentric images are recorded using a chest-mounted GoPro camera. As shown in Fig. 4, the camera position is approximately aligned with the camera mounting position on the Unitree G1 robot, so that human demonstrations and robot deployment share similar first-person observations. During data collection, the camera height may vary by approximately _±_ 5 cm and the pitch angle may differ by roughly 20<sup>_◦_</sup> from the nominal pose. These moderate viewpoint variations improve robustness and reduce overfitting to a single camera configuration. The text annotations are also augmented using GPT-5, which generates semantically equivalent paraphrases for each manually written instruction to increase linguistic diversity while preserving the original task objective and spatial intent. 

Figure 4: Hardware configuration for perspective alignment. 

13 

To ensure the validity of the zero-shot chair evaluation, we remove chair-related samples from all training data. Specifically, we filter out sequences whose text instructions contain chair-related descriptions and remove samples where chairs appear as salient objects in egocentric images. This filtering is applied before both Qwen-VL fine-tuning and interactive tracker training. Therefore, the chair navigation and chair sitting tasks used in real-world zero-shot evaluation are absent from the training data. 

We further compare the efficiency of our human egocentric data collection with humanoid wholebody teleoperation. The teleoperation setup uses the SONIC whole-body teleoperation system with PICO 4 Ultra VR control. We use box moving as the comparison task, where the robot moves a box from the ground to a target location and each successful demonstration lasts about 15 seconds. In practice, teleoperation requires two operators for VR control, robot reset, safety monitoring, and task setup. It is also slowed by difficult whole-body control, time-consuming resets, and frequent failures such as failed grasping, box dropping, or loss of balance. As a result, about 8 hours of teleoperation yields only around 100 successful demonstrations. In contrast, one human demonstrator with a motion capture system and a chest-mounted camera can collect about 300 successful egocentric demonstrations in 2 hours for the same task and setting, highlighting the scalability advantage of human egocentric data. 

## **B Motion Generation Details and Supplementary Experiments** 

We provide additional implementation details of the motion generation module, including the VQVAE motion tokenizer, Qwen-VL fine-tuning setup, and supplementary ablation experiments on input modalities and training data. 

**Motion tokenizer.** We train a VQ-VAE motion tokenizer to discretize continuous SMPL-formatted human motions into motion tokens for downstream autoregressive generation. Given an input motion clip of length _ni_ , the encoder downsamples it into a latent sequence of length _nt_ , where _ni_ = _nt ·_ 2<sup>_n_down</sup> and _n_ down denotes the number of temporal downsampling stages. The latent sequence is quantized by the codebook and then reconstructed by a lightweight decoder to the original motion resolution. Detailed architecture and optimization settings are provided in Table 5. We use a codebook size of 2048 to balance motion reconstruction fidelity and the prediction difficulty of Qwen-VL. 

For each motion sequence **m** , we denote the SMPL pose as **m** smpl _∈_ R<sup>66</sup> and the global root translation as **m** trans _∈_ R<sup>3</sup> . The tokenizer is trained with reconstruction, commitment, velocity, root-rotation, and root-position losses: 

Table 5: VQ-VAE training configuration. 

|**Type**|**Hyper-parameter**|**Value**|
|---|---|---|
|**Arch**|Down-sample stages<br>Stride per stage<br>Latent code dim<br>Code-book size<br>Channel width<br>Residual blocks<br>Activation|2<br>2<br>512<br>2048<br>512<br>3<br>ReLU|
||Reconstruction_λr_<br>Commitment_λc_<br>|1.0<br>0.02|
|**Loss**|Velocity_λv_<br>Root-rotation_λrr_<br>Root-position_λp_|0.10<br>0.5<br>0.8|
||Optimizer|AdamW<br>|
||Learning rate<br>LR decay epochs|2_×_10<sup>_−_4</sup><br>150, 250, 350|
|**Optim**|Batch size|256|
||Grad clipping<br>Mixed precision<br>Epochs|1.0<br>FP16<br>1500|


Here, **m** ˆ denotes the reconstructed motion, **z** _e_ is the encoder output, and **z** _q_ is the quantized latent vector selected from the codebook. The operator sg[ _·_ ] denotes stop-gradient, and ∆( _·_ ) denotes temporal finite difference. The velocity loss encourages temporal smoothness, while the root-rotation and root-position losses preserve global heading and trajectory information, which is important for spatially grounded interaction. The resulting discrete token sequence is used as the prediction target for Qwen-VL fine-tuning. 

**Qwen-VL Fine-tuning.** We adopt Qwen2.5-VL-3B as the backbone for multimodal motion generation. To formulate motion generation as next-token prediction, we add special motion tokens to the tokenizer vocabulary, including `<motion` ~~`s`~~ `tart>` , `<motion` ~~`e`~~ `nd>` , and discrete codebook tokens such as `<motion` ~~`t`~~ `oken` ~~`0`~~ `>` and `<motion` ~~`t`~~ `oken` ~~`1`~~ `>` . Given an initial egocentric image and a 

14 

Table 6: Ablations on input modality for motion generation. All variants are trained with Nymeria, HumanML3D, and the self-collected dataset. 

|Test Set|Modality|FID_↓_|R-Prec (T3)_↑_|MM-Dist_↓_|
|---|---|---|---|---|
||Image only|0.925|0.534|3.854|
|Nymeria|Text only|0.518|0.685|2.864|
||Image + Text|**0.298**|**0.847**|**2.286**|
||Image only|0.563|0.642|3.015|
|Self-collected|Text only|0.495|0.715|2.954|
||Image + Text|**0.245**|**0.892**|**2.456**|


language instruction, the model autoregressively predicts a complete future motion token sequence between the start and end tokens. The predicted tokens are then decoded by the VQ-VAE decoder into continuous SMPL motions. 

{ "conversations": [ { "from": "human", "value": "A person walked towards the box in front of him and picked it up, placing it on the table in front of him." }, { "from": "gpt", "value": "<motion_start><motion_token_29><motion_token_31><motion_ token_33><motion_token_524><motion_token_31><motion_ token_637>...<motion_end>" } ], "image": "mocap/.../image/000000.jpg" } 

All Qwen-VL fine-tuning experiments are conducted on 32 NVIDIA A100 GPUs. During fine-tuning, we freeze all model parameters except the LM decoder, which is fine-tuned with full parameters. This design preserves the pretrained vision-language alignment ability of Qwen-VL while reducing training cost. The fine-tuning data contains approximately 140k samples from Nymeria, 13k samples from HumanML3D, and 1.5k samples from our self-collected dataset. Nymeria provides large-scale egocentric image-text-motion supervision, HumanML3D improves text-motion alignment, and the self-collected dataset improves spatial grounding for in-domain interactive tasks. Fig. 5 

Figure 5: An example fine-tuning sample for multimodal motion generation. shows a representative fine-tuning sample. 

**Ablations on input modality.** We further evaluate the effect of input modality under the full training setting, where all variants are trained with Nymeria, HumanML3D, and our self-collected dataset. As shown in Table 6, image-only generation performs the worst because visual observations alone do not fully specify the intended task. Text-only generation achieves better semantic motion quality, but it lacks direct scene grounding and is less effective for spatially dependent interactions. In contrast, image-text conditioning achieves the best performance on both Nymeria and the self-collected test set, showing that language provides task-level semantics while egocentric images provide complementary scene-level spatial context. Since existing multimodal motion generation baselines rarely support human motion generation conditioned on both first-person visual observations and language instructions, direct comparison is limited. We therefore evaluate the contribution of each modality through controlled image-only and text-only ablations. 

## **C General Interactive Motion Tracking Details and Experiments** 

In this section, we provide the specific configuration for the General Motion Tracking policy, including the mathematical formulation of the reward functions and the curriculum learning strategy based on motion difficulty grading. 

**Reward Function Configuration.** The total reward _rt_ is a weighted sum of task rewards (tracking precision) and regularization rewards (safety and smoothness). The formulation involves standard geometric computations, where **p** and **q** denote position and orientation (quaternion), **v** and **_ω_** denote linear and angular velocities. The hat notation (e.g., **p** ˆ) indicates the robot’s actual state, while variables without hats represent the reference motion. The symbol _⊖_ represents the quaternion error magnitude. 

15 

Table 7: Task Reward Terms. All terms are defined based on the unified tracking targets **_g_** inter <u>(interaction trajectories) and</u> **_m_** ref <u>(reference motion).</u> _N_ denotes the number of tracked body <u>parts.</u> 

|**Reward Term**||**Expression**|**Weight**|**Sens. (**_σ_**)**|
|---|---|---|---|---|
|Wrist Interaction Pos.|exp<br>|�<br>_−_<sup>_∥_</sup><sup>**p**wrist</sup><sup>_−_ˆ</sup><sup>**p**wrist</sup><sup>_∥_2</sup><br>_σ_<sup>2</sup><br>�|1.0|0.3|
|Wrist Interaction Vel.|exp<br>|�<br>_−_<sup>_∥_</sup><sup>**˙p**wrist</sup><sup>_−_ˆ</sup><sup>**˙**</sup><sup>_p_wrist</sup><sup>_∥_2</sup><br>_σ_<sup>2</sup><br>�|1.0|0.2|
|Foot Interaction Pos.|exp|�<br>_−_<sup>_∥_</sup><sup>**p**foot</sup><sup>_−_ˆ</sup><sup>**p**foot</sup><sup>_∥_2</sup><br>_σ_<sup>2</sup><br>�|1.0|0.3|
|Foot Interaction Vel.|exp|�<br>_−_<sup>_∥_</sup><sup>**˙p**foot</sup><sup>_−_ˆ</sup><sup>**˙**</sup><sup>_p_foot</sup><sup>_∥_2</sup><br>_σ_<sup>2</sup><br>�|1.0|0.2|
|Root Position|exp|�<br>_−_<sup>_∥_</sup><sup>**p**root</sup><sup>_−_ˆ</sup><sup>**p**root</sup><sup>_∥_2</sup><br>_σ_<sup>2</sup><br>�|0.8|0.2|
|Root Orientation Velocity|exp<br>|�<br>_−_<sup>_∥w_root</sup><sup>_−_ˆ</sup><br>_w_root_∥_<sup>2</sup><br>_σ_<sup>2</sup><br>�|0.8|0.4|
|Reference Joint Pos.<br>Reference Joint Ang. Vel.|exp<br>�<br>_−_<br>exp<br>�<br>_−_|1<br>_N_<br>�<br>_i _<sup>_∥_</sup><sup>**q**ref</sup><sup>_,i−_ˆ</sup><sup>**q**ref</sup><sup>_,i∥_2</sup><br>_σ_<sup>2</sup><br>�<br><br>1<br>_N_<br>�<br>_i _<sup>_∥_</sup><sup>**˙**</sup><sup>**_q_**</sup>ref_,i_<sup>_−_ˆ˙</sup><sup>_q_ref</sup><sup>_,i∥_2</sup><br>_σ_<sup>2</sup><br>�|0.1<br>0.4|0.3<br>3.14|


Task rewards penalize deviations from the reference motion using an exponential kernel exp( _−d_<sup>2</sup> _/σ_<sup>2</sup> ), where _d_ is the error metric and _σ_ controls the sensitivity. The specific terms and parameters used in our best-performing model are detailed in Table 7. 

Regularization terms prevent unphysical behaviors and ensure hardware safety. These are implemented as penalties (negative rewards) or constraints, as shown in Table 8. Notably, the _Undesired Contacts_ term penalizes contact forces _Fb >_ 1 _._ 0N on all body parts except the feet (ankles) and hands (wrists), allowing for locomotion and potential hand-ground interactions (e.g., crawling). 

### **Motion Difficulty Curriculum.** We categorize 

Table 8: Regularization and penalty terms. 

motions into difficulty levels from 1 to 10 based on their motion intensity, coordination complexity, and stability requirements. Lower difficulty levels correspond to static or simple locomotion motions, while higher levels involve dynamic, low-stability, or acrobatic actions. Table 10 summarizes the grading criteria and representative motions. 

|**Term**|**Expression / Logic**|**Weight**|
|---|---|---|
|Action Rate L2|_−∥at −at−_1_∥_<sup>2</sup><br>2|-0.1|
|Joint Limit|_−_<sup>�</sup><br>_j_ <sup>**1**</sup><sup>_out_(</sup><sup>_qj_)</sup>|-10.0|
|Undesired Contacts|_−_<sup>�</sup><br>_b/_<br>_∈Ballow_ <sup>**1**</sup><sup>_F_</sup>_b_<sup>_>_1</sup><sup>_._0</sup>|-0.1|


Table 9: Actor observation space. 

During training, the tracking policy is exposed to motions with gradually increasing difficulty. The policy first learns to track low-difficulty motions and is progressively trained on higherdifficulty motions as tracking performance improves. This curriculum strategy encourages stable learning and improves robustness when tracking complex motions. 

|**Component**|**Description**|**Dim**|
|---|---|---|
|_Motion Command_|||
|current<br>~~t~~arget|Current target interactive motion|98|
|short<br>~~f~~uture<br>~~t~~argets|Short-horizon targets (2 frames)|196|
|long<br>~~f~~uture<br>~~t~~argets|Long-horizon targets (5 frames)|490|
|command (total)|Multi-scale motion target|784|
|_Proprioceptive Obser_|_vations_||
|motion<br>~~a~~nchor<br>~~o~~ri<br>~~b~~|Root orientation in body frame|6|
|base<br>~~a~~ng<br>~~v~~el|Base angular velocity|3|
|joint<br>~~p~~os|Joint positions|29|
|joint<br>~~v~~el|Joint velocities|29|
|prev<br>~~a~~ctions|Previous action|29|
|Total|Actor observation dimension|880|


The three difficulty levels illustrated in Fig. 2 base ~~a~~ ng ~~v~~ el joint ~~p~~ os are used only for visualization. Specifically, joint ~~v~~ el Fig. 2 Level 1 corresponds to difficulty ratings prev ~~a~~ ctions 1–4, Level 2 corresponds to ratings 5–7, and Total Level 3 corresponds to ratings 8–10. The actual training curriculum operates on the full 1–10 difficulty scale. 

16 

Table 10: Motion Difficulty Grading System. 

|**Rating**|**Representative Actions**|**Interpretation**|
|---|---|---|
|1|Stand, raise arms, wave hands|Mostly static or upper-body actions with low<br>motion intensity.|
|2–4|Walk, step, turn|Basic locomotion with stable rhythm and<br>simple motion patterns.|
|5–7|Walk, run, jump, walk backwards|Combined locomotion and dynamic actions<br>requiring higher coordination.|
|8|Crawl, kneel, crawl on knees|Low-posture ground movements with<br>increased body control demands.|
|9–10|Cartwheel, backflip, jump, dance|High-skill or acrobatic actions with the<br>highest complexity and risk.|


Table 11: Joint-level motion tracking evaluation. Lower values indicate better performance. 

|Data|Method|MPJPE_↓_|MPJAE_↓_|MPJVE_↓_|MPIPE_↓_|MPIVE_↓_|
|---|---|---|---|---|---|---|
||GMT [38]|0.5530|0.1046|0.4882|0.3821|0.3216|
||SONIC [12]|0.2526|0.0957|**0.3906**|0.2108|0.1992|
||w/o Curr.|0.5991|0.0953|0.6206|0.4125|0.3501|
|HumanML3D|w/o A.S.|0.5808|0.1047|0.5520|0.3987|0.3378|
||w/o F.C.|0.4619|0.0820|0.4912|0.3012|0.2645|
||w/o Interact|**0.2339**|**0.0691**|0.4212|0.2165|0.1894|
||**Ours**|0.2571|0.0734|0.4378|**0.1885**|**0.1753**|
||GMT|0.5478|0.0989|0.4725|0.3568|0.3007|
||SONIC|0.2493|**0.0716**|0.4021|0.2057|0.1904|
||w/o Curr.|0.5584|0.0917|0.5918|0.3896|0.3312|
|Self-Collected|w/o A.S.|0.5415|0.0995|0.5237|0.3741|0.3189|
||w/o F.C.|0.4356|0.0801|0.4674|0.2865|0.2498|
||w/o Interact|**0.2196**|0.0737|**0.3917**|0.2175|0.1962|
||**Ours**|0.2381|0.0752|0.4196|**0.1819**|**0.1684**|
||GMT|0.6013|0.1375|0.5112|0.4219|0.3654|
||SONIC|**0.3340**|0.1058|0.4691|0.2671|0.2318|
||w/o Curr.|0.6637|0.1319|0.6474|0.4789|0.4123|
|Generation|w/o A.S.|0.6124|0.1268|0.6293|0.4452|0.3876|
||w/o F.C.|0.5259|0.1137|0.4992|0.3765|0.3296|
||w/o Interact|0.3585|**0.0924**|**0.4537**|0.2834|0.2481|
||**Ours**|0.3653|0.1074|0.4680|**0.2138**|**0.2005**|


**Actor Observation Space.** The actor uses a compact observation space available at deployment time. As shown in Table 9, the observation consists of a multi-scale motion command and proprioceptive states. The motion command includes the interactive trajectories of end-effectors and root part, current target joint pose, short-horizon future targets, and long-horizon future targets. The longhorizon targets are further encoded by a lightweight temporal encoder before being combined with proprioceptive observations, enabling the policy to capture global motion trends while preserving near-term tracking accuracy. 

**Full Evaluation on Motion tracking.** Table 11 reports the full motion tracking results on HumanML3D, self-collected motions, and generated motions. Compared with GMT, our method achieves consistently better tracking performance across all three evaluation settings. Compared with the stronger SONIC baseline, our method is not always the best on standard joint-level met- 

17 

rics such as MPJPE, because our tracker does not solely optimize joint-space imitation. Instead, it explicitly prioritizes task-critical root, wrist, and foot trajectories. This design leads to clear improvements on the interaction-related metrics MPIPE and MPIVE, where our method achieves the best results across all datasets. The comparison with _w/o Interact_ further shows this trade-off: removing interaction-oriented targets can slightly improve some joint-level metrics, but substantially degrades key body-part tracking accuracy. These results support our main claim that accurate interaction requires preserving global root and key body-part trajectories, rather than only tracking retargeted joint motions. 

## **D Real-world Evaluation Details** 

We provide additional details of the real-world deployment and evaluation protocol on the Unitree G1 humanoid robot. In our system, the Unitree G1 client captures the initial egocentric image from the onboard chest-mounted camera and sends it to a local server equipped with an NVIDIA RTX 4090 GPU. The server runs the fine-tuned Qwen-VL model and generates a complete future human motion sequence from the initial image and language instruction. The generated motion is then decoded, retargeted to the Unitree G1, and sent back to the robot for execution. The interactive tracking policy is deployed directly on the G1 onboard computer, which tracks the retargeted robot motion together with the root and key body-part trajectories. Therefore, high-level motion generation is performed on the external server, while low-level motion tracking and control are executed locally on the robot. 


Figure 6: Real-world evaluation under varied initial observations and spatial configurations. Each row shows the robot execution from a different initial egocentric observation, robot starting pose, and object placement. 

For all real-world evaluations, a trial is counted as successful only if the humanoid completes the entire task from the initial position to the target outcome without falling, unsafe collision, or manual intervention. The success or failure of each trial is determined by human inspection based on whether the intended task is completed. In both few-shot and zero-shot evaluations, the robot’s initial position and object placement are randomly initialized for each trial, as illustrated in Fig. 6. The only constraint is that the target object or relevant scene structure must appear in the robot’s initial egocentric view. This protocol prevents the robot from simply replaying a fixed trajectory and evaluates whether the generated motion can adapt to different spatial configurations. 

Direct comparison with existing methods is limited because there are currently few open-source humanoid systems that support whole-body interaction. Most prior humanoid control systems focus on locomotion, teleoperation, third-person imitation, or task-specific simulation policies, making 

18 

them not directly comparable to our setting. We therefore conduct a real-world input-modality ablation to evaluate the necessity of multimodal conditioning. With text-only input, the model can infer the task semantics but cannot perceive the spatial layout of the scene, often producing motions that are semantically plausible but spatially misaligned with the object. With image-only input, the model observes the scene but lacks the task instruction, making the intended behavior ambiguous. In both cases, the real-world success rate is nearly zero. These results indicate that both egocentric visual observations and language instructions are necessary for reliable scene-aware whole-body interaction. 

## **E Additional analysis** 

**Feasibility Analysis of Real-time Control.** We further investigate the feasibility of real-time closed-loop control with visual feedback. By limiting each inference step to a short horizon of 4 motion tokens, the Qwen-VL inference time can be reduced to about 300 ms on an NVIDIA RTX 4090 GPU. However, the end-to-end latency approaches 400 ms after including image transmission, token-to-motion decoding, and retargeting. Such latency is too high for high-frequency feedback control and can cause phase lag, delayed reactions, and control jitter during real-world execution. Therefore, under the current latency of large vision-language models, we adopt an openloop generation-then-tracking strategy for mostly static scenes. The complete motion sequence is generated once from the initial observation and then executed by the low-level tracker, which decouples high-level semantic planning from real-time control. As the high success rate shown in Table 4, this design enables smoother and more stable long-horizon execution in static interaction tasks. Future work will explore faster motion generation, model distillation, and closed-loop replanning for dynamic environments. 

**Failure Case Analysis.** Most failures arise from contact limitations or small spatial misalignments during execution. For example, in the box-moving task, the robot often approaches and lifts the box correctly, indicating that the generated motion captures the intended visual and semantic goal. However, failures can occur when the box slips during transport due to limited hand friction and the lack of force or tactile feedback. As shown in Fig. 7, in other tasks, such as ball kicking or sofa sitting, failures are usually caused by small spatial errors between the generated body trajectory and the target object, e.g., slight football misalignment or off-center sitting. Even in these cases, the robot typically executes smooth and natural whole-body motions, but the final task outcome may fail due to the precision required by contact-rich interaction. These observations suggest that ZeroWBC can generate semantically meaningful motions, while future Figure 7: improvements should focus on contact-aware tracking, tactile feedback, and closed-loop spatial correction. 


Figure 7: Failure Case Analysis for Box Moving, Sofa Sitting, and Ball Kicking. 

**Zero-shot Generalization Tasks.** It is important to highlight that the task of “sitting on the chair” presents significantly higher complexity than “sitting on the sofa.” While a sofa offers a broad, forgiving target area, a single-seat chair imposes strict geometric constraints: its width is nearly identical to that of the humanoid’s torso. Consequently, the margin for error is minimal, necessitating highly precise maneuvering and spatial alignment. Despite this absence and the lack of such finegrained examples, the robot successfully generalized the “sitting” affordance to different chair styles. 

19 

This demonstrates the powerful capability of the pre-trained Vision-Language Model, which can adapt learned behaviors (sitting) to unseen objects with far stricter spatial tolerances. 

20 

