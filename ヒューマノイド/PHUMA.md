---
title: "PHUMA: Physically-Grounded Humanoid Locomotion Dataset"
date: "2026"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2510.26236
pdf: https://arxiv.org/pdf/2510.26236
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.26236)** / [論文ページ](https://arxiv.org/abs/2510.26236)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **PHUMA: Physically Reliable Humanoid Locomotion Dataset** 

**Kyungmin Lee**<sup>1</sup><sup>_∗_</sup> **Sibeen Kim**<sup>1</sup><sup>_∗_</sup> **Youngdo Lee**<sup>2</sup><sup>_,_3</sup> **Minho Park**<sup>1</sup> **Hyunseung Kim**<sup>1</sup><sup>_,_2</sup> **Dongyoon Hwang**<sup>1</sup> **Donghu Kim**<sup>3</sup> **Hojoon Lee**<sup>3</sup><sup>_†_</sup> **Jaegul Choo**<sup>1</sup><sup>_†_</sup> 

1KAIST 2KRAFTON 3Holiday Robotics 

```
davian-robotics.github.io/PHUMA
```


Figure 1: **Physical Reliability of Humanoid-X vs. PHUMA** . Each column illustrates four failure modes: joint violation, floating, penetration, and skating. Humanoid-X [1] (top row) often exhibits these issues due to direct video-to-motion conversion, while PHUMA (bottom row) mitigates those violations through careful data curation and physically reliable retargeting. 

**Abstract:** Motion imitation is a promising approach for humanoid locomotion, enabling agents to acquire humanlike behaviors. Existing methods typically rely on high-quality motion capture datasets such as AMASS, but these are scarce and expensive, limiting scalability and diversity. Recent studies attempt to scale data collection by converting large-scale internet videos, exemplified by Humanoid-X. However, they often suffer from physical artifacts such as floating, penetration, and foot skating, which hinder stable imitation. To address this, we introduce **PHUMA** , a **P** hysically Reliable **HUMA** noid locomotion dataset produced by a two-stage pipeline combining physics-aware curation and retargeting, aggregating both motion capture and internet video into a physically reliable, 73-hour corpus. On motion tracking benchmarks, PHUMA-trained policies achieve higher success rates than those trained on AMASS and Humanoid-X, and successfully transfer zero-shot to a real Unitree G1. 

### **1 Introduction** 

Humanoid robots are a key step toward general-purpose embodied AI, but deploying them in the real world first requires reliable and natural locomotion. While reinforcement learning (RL) with task-oriented rewards (e.g., velocity tracking) has driven remarkable progress in quadrupedal locomotion [2–4], applying it to humanoids often yields gaits that are effective yet non-humanlike [5, 6], 

> _∗_ Equal contribution. _†_ Equal advising. 

10th Conference on Robot Learning (CoRL 2026), Austin TX, USA. 


Figure 2: **Overview of datasets and performance.** (a) Composition of feasible and infeasible human motion sources in each dataset. (b) Physical reliability of each dataset; AMASS is retargeted using a standard learning-based inverse kinematics method. (c) Success rate on unseen motions. (d) Motion tracking error on real Unitree G1. 

since such rewards struggle to capture natural whole-body coordination. To address this limitation, motion imitation has emerged as a promising paradigm, where policies are trained to replicate human movements through a three-stage pipeline: (1) collecting human motion data, (2) retargeting it to the robot’s morphology, and (3) tracking the retargeted trajectories with RL [7–11]. 

Despite its promise, progress in motion imitation is fundamentally constrained by the scale, diversity, and physical feasibility of human motion data. High-quality motion capture datasets such as LaFAN1 [12] and AMASS [13] provide a high proportion of physically feasible motions, but are limited in scale and diversity, with content dominated by simple motions such as reaching and walking. To overcome this scarcity, recent work has sought to scale data collection by leveraging vast internet videos. Humanoid-X [1] exemplifies this trend by converting videos to SMPL representations [14, 15] using a video-to-motion model [16], then retargeting them to humanoid embodiments. However, this pipeline suffers from two types of physical violations. First, the video-to-motion model often misestimates global translation, producing artifacts such as floating or ground penetration. Second, the retargeting stage prioritizes joint alignment over physical plausibility [9, 17], leading to joint violation and foot skating as illustrated in the top row of Figure 1. 

In response, we introduce **PHUMA** : a **P** hysically Reliable **HUMA** noid locomotion dataset that scales internet video into a high-quality training corpus by jointly filtering infeasible motions and enforcing physical constraints during retargeting. As illustrated in Figure 3.1, we first collect largescale, diverse human motion data and filter out infeasible motions from Humanoid-X, such as root jitter or actions requiring external objects like sitting on chairs. As shown in Figure 3.2, we then apply Physics-aware Shape-adaptive Inverse Kinematics (PhySINK), enforcing soft joint limits, ground contact, and anti-skating constraints to eliminate violations like joint over-extension, floating, and sliding. As a result, PHUMA offers the most physically feasible motion among existing datasets: 73.0h total, 3 _._ 5 _×_ that of AMASS and exceeding Humanoid-X’s 69.1h (out of 231.4h). 

To validate its effectiveness, we evaluate PHUMA across four axes: (i)-(ii) whether physics-aware curation and PhySINK retargeting contribute to downstream motion tracking, (iii) comparison against existing datasets, and (iv) zero-shot deployment on a real Unitree G1. We use the MaskedMimic [8] for in-simulation tests on both Unitree G1 and H1-2 humanoids, and BeyondMimic [18] for real-world deployment on a Unitree G1. On 504 self-recorded videos across 11 motion types, policies trained with PHUMA outperform both AMASS and Humanoid-X across all motion types in success rate (Figure 2(c)). Furthermore, on 24 motions sampled from the PHUMA test set (6 per category: stationary, angular, vertical, and horizontal), the PHUMA-trained policy achieves 16 _._ 3% lower tracking error than the AMASS-trained policy in the real world (Figure 2(d)). 

### **2 Related Work** 

PHUMA focuses on constructing a large-scale, physically reliable humanoid locomotion dataset, requiring two components: (1) collecting diverse human motion data and (2) retargeting it to the humanoid robots. 

2 

#### **2.1 Human Motion Data** 

Human motion data, typically in the SMPL format [14, 15], comes from two main sources: motion capture (mocap) and video-based reconstruction. Mocap [19–21] provides accurate kinematics but demands expensive instrumentation and studio effort. LaFAN1 [12], for instance, offers high fidelity but only a few hours of motion, while AMASS [13] unifies many mocap datasets yet remains walking-centric, limiting diversity. Concurrent work such as Bones-SEED [22] scales open mocap data through commercial studio production. Driven by advances in video-to-motion recovery [16, 23–26], human video has emerged as a scalable, diverse alternative. Recent works [27–36] leverage this scalability and diversity, with Humanoid-X [1] notably providing abundant data from the Internet. However, video-derived motions often exhibit severe jitter across frames and physical artifacts such as foot sliding or ground penetration [37–42]. To mitigate these artifacts, recent methods employ automated filtering, either by discarding motions a pretrained tracking policy cannot reproduce in simulation [11], or by detecting foot-ground contacts through hand-tuned thresholds (e.g., zero-velocity and ankle-height) [10]. Yet, the former risks rejecting feasible but out-ofdistribution motions, and the latter misjudges contact when video-estimated global translation is noisy. We aggregate large-scale motion data from both mocap and human video, and instead curate it with physics-aware criteria computed directly from the motion, without relying on a tracking policy. To keep contact detection reliable, we measure contact against a robust ground plane estimated by majority voting, and filter out clips that are jittery, unstable, or floating. 

#### **2.2 Humanoid Motion Retargeting** 

Building on its success in physics-based character control [7, 8, 37, 43–48], human motion data is increasingly adapted for humanoid robotics [10, 18, 49–61]. This requires motion retargeting [62], mapping human motions onto robots that share a humanoid topology but differ in kinematics and body proportions [63–65]. Standard Inverse Kinematics (IK) methods [66–68] are widely adopted for their simplicity, but they often ignore these morphological differences, leading to unnatural artifacts such as misaligned foot orientations. While approaches like GMR [69] demonstrate that careful engineering can improve IK outcomes, they still rely heavily on heuristic scale adjustments and remain prone to floating artifacts. To explicitly address shape discrepancies, Shape-adaptive Inverse Kinematics (SINK) methods [9, 17, 70–72] adapts the human body shape to the robot before pose alignment, which is effective at pose matching but physically under-constrained. To enforce physical realism, several works [73–78] add contact constraints, but assume clean motion where the ground follows from the lowest foot position; on noisy video-derived motion this collapses, flagging nearly every frame as floating. Neural retargeting [79, 80] learns the mapping from data, and dynamicsaware methods such as SPIDER [75] refine motions with sampling-based optimization, yet both still need a prior retargeting method, for training pairs and for initialization, respectively. We retarget the curated human motion data with Physics-aware SINK (PhySINK), which augments SINK with joint feasibility, grounding, and anti-skating terms and takes contact signals from the ground plane estimated during curation, keeping them reliable on noisy video. 

### **3 Method** 

Our goal is to construct PHUMA, a large-scale, physically reliable dataset for humanoid locomotion. We build upon the Humanoid-X motions [1], which are rich in scale but exhibit physical artifacts. We first apply physics-aware curation to filter out problematic motions (Section 3.1). Next, to address artifacts introduced during the retargeting process itself, we employ PhySINK, our physics-aware retargeting method that adapts the curated motion to the humanoid while enforcing physical reliability (Section 3.2). Our full pipeline is illustrated in Figure 3. 

#### **3.1 Physics-Aware Motion Curation** 

Our curation pipeline addresses three key artifacts in raw motion data: severe jitter, physical instability from interactions with objects absent in the humanoid’s environment (e.g., chairs), and incorrect foot-ground contact (e.g., floating or penetration). 

3 


Figure 3: **Overview of the PHUMA pipeline.** Our four-stage pipeline for motion imitation learning includes: (1) Motion Curation, where we filter out problematic motions from a diverse dataset; (2) Motion Retargeting, where the filtered motions are retargeted to the humanoid using PhySINK; (3) Policy Learning, where a policy is trained to imitate the retargeted motions; and (4) Inference, where the trained policy is used to control the humanoid, enabling it to imitate motions from unseen videos processed by a video-to-motion model. 

**Jitter and instability.** To mitigate high-frequency jitter, we apply a low-pass Butterworth filter, which smooths the motion by removing high-frequency components while preserving the overall trajectory (Appendix A.1.1). To detect physical instability, such as sitting on a non-existent chair, we compute the center-of-mass (CoM) distance from the base of support, defined as the ground area covered by the feet in contact with the floor. 

**Ground contact.** To ensure that the feet make proper contact with the ground, a fixed ground plane is required as a reference. However, recovered motions are often defined in a camera’s coordinate frame, which has no fixed ground, causing floating and penetration. To address this, we estimate a global ground plane by majority voting over the heights of vertices on the foot meshes, selecting the height most consistent with ground contact. Using this estimate, we subtract the ground plane’s height from the z-coordinate of every joint in every frame, shifting the entire motion so that the ground plane aligns with _z_ = 0 (Appendix A.1.2). We then compute a contact score for each foot region (e.g., heel, toe), measuring how close its vertices are to the ground plane in each frame. 

With a reliable ground plane established, we segment all sequences into 4-second clips and discard any clip that exhibits (i) excessive jerk, indicating high-frequency jitter; (ii) a CoM position far outside its base of support, indicating physical instability; or (iii) insufficient foot-ground contact, indicating floating. By filtering at the clip level rather than the full sequence, we preserve valid segments even when parts of the original sequence are flawed (Appendix A.1.3). 

Finally, we augment these curated motions with data from LaFAN1, LocoMuJoCo, and our own video captures. The resulting PHUMA dataset is a large-scale collection of 73.0 hours of physically reliable motion across 76.0K clips, with the full composition in Appendix A.2. 

4 

#### **3.2 Physics-Aware Motion Retargeting** 

After curation, the next step is to retarget human motions to the humanoid embodiment. Standard inverse kinematics **(IK)** rigidly maps human joint positions to the humanoid skeleton, distorting the original motion when the two skeletons differ in proportion. Shape-adaptive inverse kinematics **(SINK)** preserves motion style by first reshaping the human body to match the humanoid’s kinematic structure, but does not account for physical plausibility, leading to artifacts such as joint violations and unrealistic ground interactions. 

**PhySINK.** We propose Physics-aware Shape-adaptive Inverse Kinematics (PhySINK), which augments SINK with three physics-aware constraints. Our key insight is that physical artifacts in retargeting arise from three distinct sources: the mechanical limits of the robot, the ground plane, and contact consistency. Each can be addressed by a dedicated loss term, added to a motion fidelity loss during optimization. 

**Motion Fidelity Loss.** We optimize the humanoid joint positions _qt_ and root translation _γt_ over frames _t_ so that the retargeted motion closely matches the SMPL-X motion. The loss combines global position matching, local joint matching, and temporal smoothness: 


_L_ Fidelity = _w_ global-match _L_ global-match + _w_ local-match _L_ local-match + _w_ smooth _L_ smooth (4) 

where _pi_ ( _t_ ) is the global 3D position of joint _i_ at frame _t_ , ∆ _pij_ ( _t_ ) is the displacement between joints _i_ and _j_ , and _mij_ is 1 if _i_ and _j_ are immediate neighbors in the kinematic tree and 0 otherwise. Here _q_ ˙ _t_ and _γ_ ˙ _t_ denote the joint and root velocities, and each _w_ is a scalar weight. 

**Joint Feasibility Loss.** We penalize joint angles _qt_ and velocities _q_ ˙ _t_ that exceed 98% of the robot’s mechanical limits, preventing over-extension and unrealistic actuation: 


where [ _q_ min _, q_ max] and [ ˙ _q_ min _, q_ ˙max] are the position and velocity limits of each joint. Penalizing values beyond 98% of each limit leaves a small margin below the mechanical limits of the robot. 

**Grounding Loss.** We align the foot height with the ground plane during contact, eliminating floating and penetration: 


where _c_<sup>_i_</sup> _t_<sup>is the ground-contact ratio of foot region</sup><sup>_i_(left heel, left toe, right heel, right toe) at frame</sup> _t_ , obtained during curation (Appendix A.1.3), and _p_<sup>_i_</sup> _t_<sup>(</sup><sup>_z_) is its height.</sup> 

**Skating Loss.** We suppress horizontal foot velocity during contact, preventing the foot from sliding: 


5 

Table 1: **Quantitative comparison and ablation study of retargeting methods.** We evaluate performance on the G1 humanoid, showing the progressive impact of adding each of our proposed physical constraint losses. (H1-2 results in Appendix G) 

||Motion Fidelity (%)|Joint Feasibility (%)|Non-Floating (%)|Non-Penetration (%)|Non-Skating (%)|
|---|---|---|---|---|---|
|IK|27.6|91.7|55.6|47.8|59.7|
|GMR|56.3|81.8|14.7|**100.0**|67.7|
|SINK|94.8|95.9|96.4|14.9|55.4|
|+ Joint Feasibility Loss|**94.9**|**100.0**|96.4|14.8|55.6|
|+ Grounding Loss|**94.9**|**100.0**|**99.9**|97.2|53.6|
|+ Skating Loss = PhySINK|94.8|**100.0**|**99.9**|96.8|**89.7**|


where _p_ ˙<sup>_i_</sup> _t_<sup>(</sup><sup>_x, y_) is the horizontal velocity of region</sup><sup>_i_at frame</sup><sup>_t_.</sup> 

The full objective is: 

_L_ PhySINK = _L_ Fidelity + _w_ Feasibility _L_ Feasibility + _w_ Ground _L_ Ground + _w_ Skate _L_ Skate (10) By jointly optimizing these terms, PhySINK produces motions that faithfully reflect the human motion while remaining physically reliable. 

**Evaluation.** We measure physical reliability across five complementary metrics, each defined as the percentage of frames satisfying a physical criterion: _Motion Fidelity_ (per-joint position error _<_ 10 cm and per-link orientation error _<_ 10°), _Joint Feasibility_ (joint positions and velocities within 98% of mechanical limits), _Non-Floating_ (foot within 1 cm above ground during contact), _Non-Penetration_ (foot within 1 cm below ground during contact), and _Non-Skating_ (horizontal foot velocity _<_ 10 cm/s during contact). We retarget curated motions onto the Unitree G1 and H1-2 [81, 82], comparing against a standard IK solver [83], GMR [69], and SINK. 

As shown in Table 1, IK and GMR rely on linear scaling between the human and robot skeletons, which fails to account for body shape differences and loses motion fidelity. SINK recovers fidelity by adapting body shape, but suffers from physical violations. GMR achieves the highest Non-Penetration by lowering the entire motion to its lowest contact point, but this causes severe floating elsewhere. PhySINK is the only method that performs consistently well across all five metrics. Qualitative comparisons are provided in Appendix B.1. 

### **4 Experiments** 

In this section, we evaluate the effectiveness of our curation and retargeting pipeline, together with the resulting PHUMA dataset, along four axes corresponding to the following research questions: 

**RQ1.** Does physics-aware data curation improve downstream motion imitation? 

**RQ2.** How does our proposed PhySINK retargeting method compare with established retargeting approaches (IK, GMR, SINK) in terms of motion imitation performance? 

**RQ3.** How effective is PHUMA as a training data for motion imitation, compared with prior humanoid motion datasets (LaFAN1, AMASS, Humanoid-X)? 

**RQ4.** Does PHUMA’s advantage in motion tracking extend from simulation to the real robot? 

#### **4.1 Experiment Setup** 

**Training.** The motion tracking framework for in-simulation evaluation is based on MaskedMimic [8], while BeyondMimic [18] is utilized for sim-to-real transfer. In both approaches, policies are trained to imitate retargeted motions by maximizing motion tracking reward signals via PPO [84]. In-simulation experiments involve both the Unitree G1 (29 DoF) and H1-2 (21 DoF, excluding wrist joints) humanoids, whereas real-world validation is performed exclusively on the Unitree G1. Comprehensive training details, including the observation space, reward function, and PPO parameters, are provided in Appendix C. 

**Evaluation.** Performance evaluation of the trained policies is conducted across two distinct datasets. The first comprises the PHUMA test split, containing approximately 7.5K motions (10% of 

6 

PHUMA) held out during training. The second consists of 504 self-collected video sequences, which are converted into motion trajectories via a video-to-motion model; processing details are provided in Appendix D.1. To address RQ1–RQ3, the success rate [9–11, 37] is measured using a 0.15m threshold, which is stricter than the conventional 0.5m limit (see Appendix D.2). For RQ4, due to the unavailability of mocap equipment in the real-world setup—precluding the recording of global translations—the evaluation relies on local mean per-joint position error (MPJPE, mm) alongside DoF velocity (deg/frame) and acceleration (deg/frame<sup>2</sup> ) errors instead of their global counterparts. 

#### **4.2 Effect of Physics-Aware Curation** 

To isolate the contribution of physics-aware curation, we conduct this evaluation under a controlled setup. We retarget all motions with SINK, which applies no physical correction at the retargeting stage, so that any change in downstream performance can be attributed to curation alone. LaFAN1 and LocoMuJoCo are excluded, as they are already provided in retargeted form and would entangle retargeting and curation effects, and the validation split is held out throughout. As shown in Table 2, applying any single filtering component improves motion tracking performance over the no-curation baseline, and applying all components yields a substantially larger gain, even though the fully filtered set contains roughly one quarter of the unfiltered motion volume. These results indicate that physics-aware curation contributes meaningfully to motion tracking performance, with data quality outweighing raw quantity. A leave-one-out ablation further supports this, removing any single filter lowers performance even though it increases the data volume, with the foot contact filter contributing the most (Appendix E.2.3). 

Table 2: **Imitation Performance: Effect of Physics-Aware Curation.** MaskedMimic policies trained on Humanoid-X subsets with varying curation filters, on Unitree G1. All variants use SINK retargeting to isolate filtering effect. Hours: remaining dataset size after filtering. 

||||Curat|ion Filter|||P|HUMA|Test|||Un|seen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Variant|Hours|Jerk|FC|Height|BoS|Total|Stat.|Ang.|Vert.|Horiz.|Total|Stat.|Ang.|Vert.|Horiz.|
|Humanoid-X|231|✗|✗|✗|✗|50.6|78.4|43.0|26.0|31.8|39.1|78.0|39.6|23.0|6.5|
|+ Jerk only|141|✓|✗|✗|✗|83.0|91.5|77.6|72.3|88.5|77.6|**100.0**|78.8|**62.8**|61.5|
|+ FC only|123|✗|✓|✗|✗|82.9|91.3|77.8|70.4|89.1|78.2|99.1|79.3|61.7|65.9|
|+ Height only|136|✗|✗|✓|✗|80.6|90.7|74.6|69.3|85.1|74.0|98.3|76.4|61.7|50.5|
|+ BoS only|110|✗|✗|✗|✓|81.3|90.2|76.2|72.0|84.4|74.8|96.6|79.8|54.3|57.1|
|**All filters**|62|✓|✓|✓|✓|**87.0**|**93.0**|**82.7**|**81.8**|**90.3**|**79.6**|98.3|**82.8**|59.6|**69.2**|


#### **4.3 PhySINK Retargeting Method Effectiveness** 

To evaluate PhySINK, we compare it against three baselines (IK, GMR, and SINK) using the AMASS dataset. Since AMASS consists of clean, motion-capture data, it effectively removes the influence of data curation, allowing us to isolate the retargeting performance. We retarget the identical motions with each method and train a separate full-state tracking policy for each baseline. As shown in Table 3, PhySINK outperforms the baselines on both evaluation sets, demonstrating that physically reliable retargeting leads to better imitation performance. Notably, the largest gains appear on angular and vertical motions, where balance is critical and physical reliability of training data directly affects policy learning. This advantage also persists beyond the retargeting distribution of the evaluation references, as PhySINK still achieves the highest success rate when the same motions are retargeted with GMR (Appendix D.4). 

Table 3: **Motion tracking performance across retargeting approaches.** Success rates of policies trained on AMASS data retargeted by IK, GMR, SINK, and PhySINK, evaluated on the G1 humanoid robot using two test sets: PHUMA Test and Unseen Video. (H1-2 results in Appendix G) 

||||PHUMA T|est||||Unseen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|
|Retarget|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|IK|52.8|75.3|43.9|24.3|44.2|54.6|89.3|54.6|32.7|43.3|
|GMR|61.7|80.2|51.7|32.5|**74.0**|59.3|87.1|64.5|31.9|40.7|
|SINK|76.2|88.5|72.1|56.8|66.8|70.2|90.7|75.0|62.7|44.1|
|**PhySINK**|**79.5**|**89.9**|**76.1**|**61.1**|69.5|**72.8**|**93.3**|**78.2**|**65.6**|**47.3**|


7 

#### **4.4 PHUMA Dataset Effectiveness** 

Having demonstrated PhySINK’s effectiveness, we now compare PHUMA against existing humanoid datasets. We train full-state policies on four datasets with different characteristics: LaFAN1 (small-scale, high-quality), AMASS (medium-scale, moderate-quality), Humanoid-X (large-scale, lower-quality), and PHUMA (large-scale, high-quality). For AMASS, we apply the widelyused SINK retargeting method since it provides human motion source data, while LaFAN1 and Humanoid-X are used directly as pre-existing humanoid datasets. As shown in Table 4, policies trained on PHUMA achieve the highest success rates across all motion categories and both humanoids. The results reveal that neither scale nor quality alone is sufficient: Humanoid-X, despite its large size, underperforms due to quality issues, while the cleaner LaFAN1 and AMASS lack coverage in several motion types. By combining large scale with high-quality motions, PHUMA delivers consistently superior performance across diverse behaviors. As with PhySINK, this advantage holds when the evaluation motions are retargeted with GMR (Appendix D.4). PHUMA also outperforms AMASS retargeted with PhySINK in this setting, indicating that the gain comes from the data itself and not from PhySINK alone. 

Table 4: **Motion tracking performance across datasets.** Success rates of policies trained on LaFAN1, AMASS, Humanoid-X, and PHUMA, evaluated across motion categories on the G1 humanoid robot using two test sets: PHUMA Test and Unseen Video. (H1-2 results in Appendix G) 

|||||PHUMA T|est||||Unseen Vid|eo||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Hours|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|LaFAN1|2.4|46.1|66.1|36.2|24.0|42.5|28.4|46.9|28.4|19.6|10.5|
|AMASS|20.9|76.2|88.5|72.1|56.8|66.8|78.2|90.7|75.0|62.7|44.1|
|Humanoid-X|231.4|50.6|78.4|43.0|26.0|31.8|39.1|78.0|39.6|23.0|6.5|
|**PHUMA**|73.0|**92.7**|**95.6**|**91.7**|**86.0**|**85.6**|**82.9**|**96.7**|**88.0**|**71.8**|**67.1**|


#### **4.5 Real-World Experiment** 

To verify whether the advantage of PHUMA-trained policies transfers to physical hardware, we adopt BeyondMimic [18], a motion tracking framework with proven sim-to-real transfer on a real Unitree G1. Since the original BeyondMimic is designed for single-motion tracking, we extend it to multi-motion tracking by augmenting the policy’s observation space with a learned latent encoding of the future reference trajectory; full details are provided in Appendix C. We train policies on AMASS and PHUMA in IsaacSim and evaluate zero-shot tracking performance on 6 motions per category (stationary, angular, vertical, and horizontal) in the PHUMA test split. 

As shown in Table 5 and Figure 4, the PHUMA-trained policy achieves lower tracking errors across all metrics and exhibits qualitatively more faithful motion tracking, indicating that PHUMA’s advantages in scale and physical reliability extend from simulation to the real robot. 

Table 5: **Real-World Tracking Results.** Tracking errors of policies trained on AMASS and PHUMA, evaluated on 6 motions per category from the PHUMA test set, on the Unitree G1. 

|||_E_mp|jpe(mm|)_↓_|||_E_dof<br>~~v~~e|l <sup>(deg/fr</sup>|<sup>ame)</sup><sup>_↓_</sup>|||_E_dof<br>~~a~~cc|<sup>(deg/fr</sup>|<sup>ame2)</sup><sup>_↓_</sup>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stat.|Ang.|Vert.|Hor.|Total|Stat.|Ang.|Vert.|Hor.|Total|Stat.|Ang.|Vert.|Hor.|
|AMASS|41.0|27.3|47.5|49.9|39.4|3.20|1.81|4.10|3.14|3.77|1.50|0.77|2.09|1.33|**1.80**|
|**PHUMA**|**34.3**|**23.2**|**40.4**|**42.6**|**31.1**|**2.69**|**1.41**|**3.07**|**2.68**|**3.60**|**1.29**|**0.58**|**1.43**|**1.18**|1.96|


### **5 Limitations** 

While PHUMA advances the scale and physical reliability of humanoid motion data, several directions remain open for future work. First, our pipeline focuses on flat-terrain locomotion and does not yet cover motions involving scene interaction (e.g., object manipulation, sitting, climbing) or uneven terrain; extending it to such settings would require jointly modeling humanoid dynamics with environment geometry and contact. Second, a substantial portion of motions estimated from video was filtered out during curation to ensure physical reliability, reflecting the current limitations of 

8 


Figure 4: **Real-World Deployment** . Each row shows the reference motion (top), the motion tracked by the AMASS-trained policy (middle), and the motion tracked by the PHUMA-trained policy (bottom), demonstrating that PHUMA achieves closer alignment with the reference across all sequences. 

video-to-motion recovery; as this technology matures, future versions of PHUMA can capture a larger and more diverse range of human behaviors. Third, our real-world comparison covers only AMASS, since the Humanoid-X-trained policy falls about three times as often in simulation (Appendix D.5), which poses a safety risk on hardware. Finally, while PhySINK substantially reduces physical artifacts during retargeting, the motions in PHUMA do not entirely eliminate them, and further closing this gap remains an important direction for future work. 

### **6 Conclusion** 

We introduced PHUMA, a large-scale, physically reliable humanoid locomotion dataset that overcomes the limitations of existing motion imitation pipelines. Unlike prior video-driven datasets prone to artifacts such as floating, ground penetration, and joint violations, PHUMA combines diverse human videos with physics-aware curation and PhySINK, our physics-aware retargeting method, to produce motions that are both diverse and physically reliable. On the Unitree G1 and H1-2 humanoids, policies trained on PHUMA consistently outperform those trained on LaFAN1, AMASS, and Humanoid-X, with ablations confirming that both curation and PhySINK contribute meaningfully. These advantages further extend to a real Unitree G1, where PHUMA-trained policies achieve lower tracking errors than AMASS-trained counterparts. Together, these results show that advancing humanoid motion tracking depends not just on having more data, but on having physically reliable data. PHUMA achieves both: it scales up data by incorporating diverse human videos, while ensuring physical reliability through careful curation and retargeting. 

#### **Acknowledgments** 

This work was supported by the Institute for Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government (MSIT) (RS-2019-II190075, Artificial Intelligence Graduate School Program (KAIST)), the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIT) (No. RS-2025-00555621), the Electronics and Telecommunications Research Institute (ETRI) grant funded by the Korean government [26CS1100, Development of Proprietary Physical AI-based Small-scale Computers and Integrated Soft Suits], and the “Advanced GPU Utilization Support Program” funded by the Government of the Republic of Korea (Ministry of Science and ICT). 

9 

### **References** 

- [1] J. Mao, S. Zhao, S. Song, T. Shi, J. Ye, M. Zhang, H. Geng, J. Malik, V. C. Guizilini, and Y. Wang. Universal humanoid robot pose learning from internet human videos. In _ICRA 2025 Workshop: Human-Centered Robot Learning in the Era of Big Data and Large Models_ , 2025. URL `https://openreview.net/forum?id=2pBjMDj6uJ` . 

- [2] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [3] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning quadrupedal locomotion over challenging terrain. _Science robotics_ , 5(47):eabc5986, 2020. 

- [4] J. Tan, T. Zhang, E. Coumans, A. Iscen, Y. Bai, D. Hafner, S. Bohez, and V. Vanhoucke. Simto-real: Learning agile locomotion for quadruped robots. _arXiv preprint arXiv:1804.10332_ , 2018. 

- [5] N. Hansen, H. Su, and X. Wang. Td-mpc2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [6] C. Sferrazza, D.-M. Huang, X. Lin, Y. Lee, and P. Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _Robotics: Science and Systems 2024_ , 2024. 

- [7] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [8] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng. Maskedmimic: Unified physicsbased character control through masked motion inpainting. _ACM Transactions on Graphics (TOG)_ , 43(6):1–21, 2024. 

- [9] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi. Learning human-to-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944–8951. IEEE, 2024. 

- [10] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. In _The Thirtyninth Annual Conference on Neural Information Processing Systems_ , 2025. URL `https: //openreview.net/forum?id=LCPoXt0pzm` . 

- [11] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbabu, C. Pan, Z. Yi, G. Qu, K. Kitani, J. Hodgins, L. J. Fan, Y. Zhu, C. Liu, and G. Shi. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. In _Robotics: Science and Systems (RSS)_ , June 2025. 

- [12] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [13] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [14] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black. Smpl: A skinned multiperson linear model. In _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , pages 851–866. 2023. 

- [15] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. Osman, D. Tzionas, and M. J. Black. Expressive body capture: 3d hands, face, and body from a single image. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10975–10985, 2019. 

10 

- [16] M. Kocabas, N. Athanasiou, and M. J. Black. Vibe: Video inference for human body pose and shape estimation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 5253–5263, 2020. 

- [17] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. M. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _8th Annual Conference on Robot Learning_ , 2024. URL `https://openreview.net/forum?id= oL1WEZQal8` . 

- [18] T. E. Truong, Q. Liao, X. Huang, G. Tevet, C. K. Liu, and K. Sreenath. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [19] Carnegie mellon university graphics lab motion capture database. http://mocap.cs.cmu.edu, 2003. The data was captured with funding from NSF EIA-0196217. Acknowledgment of the database is appreciated in any published work. 

- [20] S. Zhang, Q. Ma, Y. Zhang, Z. Qian, T. Kwon, M. Pollefeys, F. Bogo, and S. Tang. Egobody: Human body shape and motion of interacting people from head-mounted devices. In _European conference on computer vision_ , pages 180–200. Springer, 2022. 

- [21] F. Al-Hafez, G. Zhao, J. Peters, and D. Tateo. Locomujoco: A comprehensive imitation learning benchmark for locomotion. In _6th Robot Learning Workshop, NeurIPS_ , 2023. 

- [22] Bones Studio. BONES-SEED: Skeletal everyday embodied dataset. `https://bones. studio/datasets/seed` , 2026. 

- [23] S. Shin, J. Kim, E. Halilaj, and M. J. Black. Wham: Reconstructing world-grounded humans with accurate 3d motion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 2070–2080, 2024. 

- [24] Y. Wang, Z. Wang, L. Liu, and K. Daniilidis. Tram: Global trajectory and motion of 3d humans from in-the-wild videos. In _European Conference on Computer Vision_ , pages 467–487. Springer, 2024. 

- [25] Z. Shen, H. Pi, Y. Xia, Z. Cen, S. Peng, Z. Hu, H. Bao, R. Hu, and X. Zhou. World-grounded human motion recovery via gravity-view coordinates. In _SIGGRAPH Asia 2024 Conference Papers_ , pages 1–11, 2024. 

- [26] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, et al. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _arXiv preprint arXiv:2501.02116_ , 2025. 

- [27] J. Lin, A. Zeng, S. Lu, Y. Cai, R. Zhang, H. Wang, and L. Zhang. Motion-x: A large-scale 3d expressive whole-body human motion dataset. _Advances in Neural Information Processing Systems_ , 36:25268–25280, 2023. 

- [28] Y. Zhang, J. Lin, A. Zeng, G. Wu, S. Lu, Y. Fu, Y. Cai, R. Zhang, H. Wang, and L. Zhang. Motion-x++: A large-scale multimodal 3d whole-body human motion dataset. _arXiv preprint arXiv:2501.05098_ , 2025. 

- [29] J. Chung, C.-h. Wuu, H.-r. Yang, Y.-W. Tai, and C.-K. Tang. Haa500: Human-centric atomic action dataset with curated videos. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 13465–13474, 2021. 

- [30] Z. Cai, D. Ren, A. Zeng, Z. Lin, T. Yu, W. Wang, X. Fan, Y. Gao, Y. Yu, L. Pan, et al. Humman: Multi-modal 4d human dataset for versatile sensing and modeling. In _European Conference on Computer Vision_ , pages 557–577. Springer, 2022. 

11 

- [31] S. Tsuchida, S. Fukayama, M. Hamasaki, and M. Goto. Aist dance video database: Multigenre, multi-dancer, and multi-camera database for dance information processing. In _ISMIR_ , volume 1, page 6, 2019. 

- [32] K. Fan, S. Lu, M. Dai, R. Yu, L. Xiao, Z. Dou, J. Dong, L. Ma, and J. Wang. Go to zero: Towards zero-shot motion generation with million-scale data. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 13336–13348, 2025. 

- [33] J. Ni, Z. Wang, W. Lin, A. Bar, Y. LeCun, T. Darrell, J. Malik, and R. Herzig. From generated human videos to physically plausible robot trajectories. _arXiv preprint arXiv:2512.05094_ , 2025. 

- [34] Y. Wei, Z. Wang, K. Yin, Y. Hu, J. Wang, and S. Chen. Unveiling the impact of data and model scaling on high-level control for humanoid robots. _arXiv preprint arXiv:2511.09241_ , 2025. 

- [35] Y. Wang, Q. Zhao, Y. F. Lau, R. Yu, H. W. Tsui, Q. Chen, J. Wang, J. Pang, and P. Tan. Humanx: Toward agile and generalizable humanoid interaction skills from human videos. _arXiv preprint arXiv:2602.02473_ , 2026. 

- [36] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [37] Z. Luo, J. Cao, A. W. Winkler, K. Kitani, and W. Xu. Perpetual humanoid control for real-time simulated avatars. In _International Conference on Computer Vision (ICCV)_ , 2023. 

- [38] Z. Luo, J. Cao, J. Merel, A. Winkler, J. Huang, K. M. Kitani, and W. Xu. Universal humanoid motion representations for physics-based control. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id= OrOd8PxOO2` . 

- [39] S. Goel, G. Pavlakos, J. Rajasegaran, A. Kanazawa, and J. Malik. Humans in 4d: Reconstructing and tracking humans with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14783–14794, 2023. 

- [40] V. Ye, G. Pavlakos, J. Malik, and A. Kanazawa. Decoupling human and camera motion from videos in the wild. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 21222–21232, 2023. 

- [41] R. Yu, H. Park, and J. Lee. Human dynamics from monocular video with dynamic camera movements. _ACM Transactions on Graphics (TOG)_ , 40(6):1–14, 2021. 

- [42] N. Ugrinovic, B. Pan, G. Pavlakos, D. Paschalidou, B. Shen, J. Sanchez-Riera, F. MorenoNoguer, and L. Guibas. Multiphys: Multi-person physics-aware 3d motion estimation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 2331–2340, 2024. 

- [43] N. Wagener, A. Kolobov, F. Vieira Frujeri, R. Loynd, C.-A. Cheng, and M. Hausknecht. Mocapact: A multi-task dataset for simulated humanoid control. _Advances in Neural Information Processing Systems_ , 35:35418–35431, 2022. 

- [44] Z. Luo, R. Hachiuma, Y. Yuan, and K. Kitani. Dynamics-regulated kinematic policy for egocentric pose estimation. _Advances in Neural Information Processing Systems_ , 34:25019– 25032, 2021. 

- [45] N. Hansen, J. S. V, V. Sobal, Y. LeCun, X. Wang, and H. Su. Hierarchical world models as visual whole-body humanoid controllers. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL `https://openreview.net/forum?id=7wuJMvK639` . 

12 

- [46] A. Tirinzoni, A. Touati, J. Farebrother, M. Guzek, A. Kanervisto, Y. Xu, A. Lazaric, and M. Pirotta. Zero-shot whole-body humanoid control via behavioral foundation models. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL `https: //openreview.net/forum?id=9sOR0nYLtz` . 

- [47] Z. Zhang, S. Bashkirov, D. Yang, Y. Shi, M. Taylor, and X. B. Peng. Physics-based motion imitation with adversarial differential discriminators. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , pages 1–12, 2025. 

- [48] J. Zhang, H. Liang, R. Zhang, B. Li, J. Zhang, X. Chen, J. Wang, L. Xu, and J. Yu. Script: Scalable diffusion policy with multi-stage training for language-driven physics-based humanoid control. _arXiv preprint arXiv:2605.22894_ , 2026. 

- [49] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik. Learning humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2410.03654_ , 2024. 

- [50] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [51] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive whole-body control for humanoid robots. _Robotics: Science and Systems 2024_ , 2024. 

- [52] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [53] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [54] Y. Li, Y. Lin, J. Cui, T. Liu, W. Liang, Y. Zhu, and S. Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. _arXiv preprint arXiv:2506.08931_ , 2025. 

- [55] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [56] Y. Li, P. Zhi, Y. Wang, T. Liu, S. Yan, W. Liu, X. Wang, B. Jia, and S. Huang. Omnitrack: General motion tracking via physics-consistent reference. _arXiv preprint arXiv:2602.23832_ , 2026. 

- [57] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _Robotics: Science and Systems 2025_ , 2025. 

- [58] Y. Wang, S. Zhu, P. Zhi, Y. Li, J. Li, Y.-L. Li, Y. Xiao, X. Wang, B. Jia, and S. Huang. Omnixtreme: Breaking the generality barrier in high-dynamic humanoid control. _arXiv preprint arXiv:2602.23843_ , 2026. 

- [59] D. Rempe, M. Petrovich, Y. Yuan, H. Zhang, X. B. Peng, Y. Jiang, T. Wang, U. Iqbal, D. Minor, M. de Ruyter, et al. Kimodo: Scaling controllable human motion generation. _arXiv preprint arXiv:2603.15546_ , 2026. 

- [60] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [61] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [62] M. Gleicher. Retargetting motion to new characters. In _Proceedings of the 25th annual conference on Computer graphics and interactive techniques_ , pages 33–42, 1998. 

13 

- [63] C. M. Kim, B. Yi, H. Choi, Y. Ma, K. Goldberg, and A. Kanazawa. Pyroki: A modular toolkit for robot kinematic optimization. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. URL `https://arxiv.org/abs/2505.03728` . 

- [64] E. S. Ho, T. Komura, and C.-L. Tai. Spatial relationship preserving character motion adaptation. In _ACM SIGGRAPH 2010 papers_ , pages 1–8. 2010. 

- [65] J. Zhang, J. Weng, D. Kang, F. Zhao, S. Huang, X. Zhe, L. Bao, Y. Shan, J. Wang, and Z. Tu. Skinned motion retargeting with residual perception of motion semantics & geometry. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13864–13872, 2023. 

- [66] I. Radosavovic, B. Zhang, B. Shi, J. Rajasegaran, S. Kamat, T. Darrell, K. Sreenath, and J. Malik. Humanoid locomotion as next token prediction. _Advances in neural information processing systems_ , 37:79307–79324, 2024. 

- [67] S. Caron, Y. De Mont-Marin, R. Budhiraja, S. H. Bang, I. Domrachev, S. Nedelchev, peterd NV, and J. Vaillant. Pink: Python inverse kinematics based on Pinocchio, 2025. URL `https: //github.com/stephane-caron/pink` . 

- [68] Y. Ze, Z. Chen, J. P. Araujo, Z. ang Cao, X. B. Peng, J. Wu, and K. Liu. TWIST: Teleoperated whole-body imitation system. In _9th Annual Conference on Robot Learning_ , 2025. URL `https://openreview.net/forum?id=htgNQHa6Ta` . 

- [69] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [70] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, et al. Hover: Versatile neural whole-body controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9989–9996. IEEE, 2025. 

- [71] T. Cheynel, T. Rossi, B. Bellot-Gurlet, D. Rohmer, and M.-P. Cani. Sparse motion semantics for contact-aware retargeting. In _ACM SIGGRAPH Conference on Motion, Interaction and Games (MIG)_ , 2023. 

- [72] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa. Visual imitation enables contextual humanoid control. In _Proceedings of The Conference on Robot Learning_ , Proceedings of Machine Learning Research, 2025. 

- [73] Z. Chen, H. Zhang, D. Wang, J. Yu, H. Xu, Y. Wang, and R. Xiong. A whole-body motion imitation framework from human data for full-size humanoid robot. In _2025 IEEE International Conference on Real-time Computing and Robotics (RCAR)_ , pages 558–563. IEEE, 2025. 

- [74] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [75] C. Pan, C. Wang, H. Qi, Z. Liu, H. Bharadhwaj, A. Sharma, T. Wu, G. Shi, J. Malik, and F. Hogan. Spider: Scalable physics-informed dexterous retargeting. _arXiv preprint arXiv:2511.09484_ , 2025. 

- [76] X. Zhang, S. Haener, V. Madabushi, and M. Tucker. Kinodynamic motion retargeting for humanoid locomotion via multi-contact whole-body trajectory optimization. _arXiv preprint arXiv:2603.09956_ , 2026. 

- [77] H. Wang, Q. Liao, B. Zhang, K. Ren, K. Sreenath, and X. Xiong. Spark: Skeleton-parameter aligned retargeting on humanoid robots with kinodynamic trajectory optimization. _arXiv preprint arXiv:2603.11480_ , 2026. 

14 

- [78] D. M¨uller, A. Serifi, S. Christen, R. Grandia, E. Knoop, and M. B¨acher. Reactor: Reinforcement learning for physics-aware motion retargeting. _arXiv preprint arXiv:2605.06593_ , 2026. 

- [79] X. Chen, H. Wu, S. Wu, M. Zhou, D. Xiang, and H. Zhang. Implicit kinodynamic motion retargeting for human-to-humanoid imitation learning. _arXiv preprint arXiv:2509.15443_ , 2025. 

- [80] Q. Zhao, K. Yang, X. Wang, S. Zhao, Y. Lu, X. Zhang, Q. Shen, X.-X. Long, and X. Cao. Make tracking easy: Neural motion retargeting for humanoid whole-body control. _arXiv preprint arXiv:2603.22201_ , 2026. 

- [81] Unitree Robotics. Unitree g1 humanoid robot. `https://www.unitree.com/g1` , 2025. Accessed: 2025-09-25. 

- [82] Unitree Robotics. Unitree h1-2 humanoid robot. `https://www.unitree.com/h1` , 2025. Accessed: 2025-09-25. 

- [83] K. Zakka. Mink: Python inverse kinematics based on MuJoCo, May 2025. URL `https: //github.com/kevinzakka/mink` . 

- [84] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [85] O. Taheri, N. Ghorbani, M. J. Black, and D. Tzionas. Grab: A dataset of whole-body human grasping of objects. In _European conference on computer vision_ , pages 581–600. Springer, 2020. 

- [86] J. Han, W. Xie, J. Zheng, J. Shi, W. Zhang, T. Xiao, and C. Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

15 

## **Appendix** 

|**A **|**PH**|**UMA Dataset**|**17**|
|---|---|---|---|
||A.1|Data Preprocessing . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>17|
||A.2|Dataset Composition and Statistics . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>20|
|**B**|**Mot**|**ion Retargeting**|**20**|
||B.1|Comparison of Retargeting Methods . . . . . . . . . . . . . . . . . . .|. . . . . .<br>21|
||B.2|Computational Cost . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>21|
||B.3|PhySINK as Initialization for Dynamics-Aware Retargeting . . . . . . .|. . . . . .<br>22|
|**C **|**Mot**|**ion Imitation Learning**|**23**|
||C.1|Observation Space Compositions . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>23|
||C.2|Reward Function<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>25|
||C.3|PPO Hyperparameters<br>. . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>26|
||C.4|Domain Randomization . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>26|
|**D **|**Exp**|**eriment Details**|**28**|
||D.1|Self-Collected Video Dataset . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>28|
||D.2|Success Rate Threshold Analysis . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>28|
||D.3|Cross-Simulator Generalization Analysis. . . . . . . . . . . . . . . . .|. . . . . .<br>28|
||D.4|Evaluation on GMR-Retargeted References . . . . . . . . . . . . . . .|. . . . . .<br>29|
||D.5|Fall Rate of Humanoid-X and AMASS Policies . . . . . . . . . . . . .|. . . . . .<br>30|
|**E**|**Abl**|**ation Studies**|**30**|
||E.1|Mocap only and Video only data performance . . . . . . . . . . . . . .|. . . . . .<br>30|
||E.2|Physics-based Filtering . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>31|
||E.3|Impact of Motion Retargeting Quality on Policy Performance . . . . . .|. . . . . .<br>33|
||E.4|Leave-One-Out Ablation of PhySINK Losses . . . . . . . . . . . . . .|. . . . . .<br>34|
|**F**|**Pelv**|**is-Only Path Following Control Performance**|**34**|
|**G **|**Res**|**ults on H1-2 Robot**|**34**|
||G.1|PhySINK Ablation on H1-2. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>34|
||G.2|Retargeting Method Comparison on H1-2 . . . . . . . . . . . . . . . .|. . . . . .<br>34|
||G.3|Dataset Effectiveness on H1-2<br>. . . . . . . . . . . . . . . . . . . . . .|. . . . . .<br>35|


16 

### **A PHUMA Dataset** 

#### **A.1 Data Preprocessing** 

Before applying the retargeting procedure, it is essential to ensure that the human motion data is clean and robust, as this data serves as the target for the humanoid robot to follow. Raw motion data often contains noise from sensor errors, tracking inaccuracies, or estimation artifacts that can negatively impact retargeting. To address this, we apply the following preprocessing to filter and clean the motion data. 

#### **A.1.1 Low-Pass Noise Filtering for Motion Data** 

All motion sequences were resampled to 30 Hz. We smooth all motion channels with a zero-phase, 4th-order Butterworth low-pass filter. For root translation, the cutoff is 3 Hz; for global orientation and body pose, it is 6 Hz. 

#### **A.1.2 Extracting Ground Contact Information** 

To identify foot contact, we need foot indices from a human motion source. Therefore, we identify a subset of SMPL-X foot vertices that are most indicative of ground interaction. Specifically, we select the 22 vertically lowest vertices from each foot region (left heel, left toe, right heel, right toe) in the SMPL-X default pose, totaling 88 vertices. These vertices are illustrated in Figure 5. The vertex indices corresponding to these ground-contact points are provided in Table 6. 


Figure 5: **SMPL-X Foot Vertices for Ground-Contact Detection** . This figure illustrates the selected foot vertices on the SMPL-X model used to detect ground contact. Blue and green points denote the left heel and left toe, while yellow and red represent the right heel and right toe, respectively. The remaining foot vertices are shown in light-gray. The clusters of colored points correspond to the specific parts of the foot that are used to check for contact with the ground, making the process more accurate and robust than using a single point. 

Table 6: **SMPL-X foot vertex indices used for ground–contact detection.** 

|Region|Vertex indices||
|---|---|---|
|Left heel|8888, 8889, 8891, 8909,<br>8918, 8919, 8920, 8921,|8910, 8911, 8913, 8914, 8915, 8916, 8917,<br>8922, 8923, 8924, 8925, 8929, 8930, 8934|
|Left toe|5773, 5781, 5782, 5791,<br>5859, 5860, 5906, 5907,|5793, 5805, 5808, 5816, 5817, 5830, 5831,<br>5908, 5909, 5912, 5914, 5915, 5916, 5917|
|Right heel|8676, 8677, 8679, 8697,<br>8706, 8707, 8708, 8709,|8698, 8699, 8701, 8702, 8703, 8704, 8705,<br>8710, 8711, 8712, 8713, 8714, 8715, 8716|
|Right toe|8467, 8475, 8476, 8485,<br>8553, 8554, 8600, 8601,|8487, 8499, 8502, 8510, 8511, 8524, 8525,<br>8602, 8603, 8606, 8608, 8609, 8610, 8611|


To correctly place a motion, it is necessary to establish a single, consistent ground plane. Simple heuristics often fail: defining the ground by the lowest foot position in the sequence can cause floating, while per-frame adjustment introduces jitter and breaks down for motions where both feet leave 

17 


Figure 6: **Procedure of Majority-Vote Ground Estimation.** (1) shows how the foot-height distribution is obtained across all frames of a single human motion trajectory, and (2) shows how the ground height is selected from this distribution by majority vote. 

the ground, such as jumping or running. Our method instead uses a majority vote to find the ground height that maximizes the duration of foot contact. Specifically, we first collect the heights of the foot vertices (Figure 5) across all frames (Figure 6.1). Because the estimated root translation of SMPL-X is noisy, we then select the optimal ground height _g_<sup>_∗_</sup> as the one with the most foot vertices falling within the band ( _g − δ, g_ + _δ_ ) with _δ_ = 2 _._ 5 _cm_ (Figure 6.2): 


where _V_ is the set of foot vertices, _h_<sup>_f_</sup> _v_<sup>denotestheheightofvertex</sup><sup>_v_atframe</sup><sup>_f_,and</sup><sup>**1**[</sup><sup>_·_]isthe</sup> indicator function. Finally, the entire motion is shifted so that this ground sits at height zero. 

#### **A.1.3 Filtering Motion Data by Physical Information** 

To remove noisy data that cannot be corrected during retargeting, we evaluate each human motion clip using the following metrics: root jerk, foot contact score, pelvis height, and pelvis/spine-1 distance to the base of support (Table 7). Sub-clips that fail to meet these thresholds are discarded. 

**Root jerk** represents rapid changes in root acceleration, indicative of abrupt or unnatural motions. High root jerk segments are excluded to ensure smooth and physically plausible trajectories. 

**Foot contact score** measures the consistency and sufficiency of foot-ground interactions based on graded ground-contact signals defined by vertex proximity to the ground. Specifically, given a subclip with _T_ frames, the foot contact score is computed as: 


18 

Table 7: **Physics-aware data filtering metrics and thresholds.** 

|Metric|Threshold|
|---|---|
|Root jerk|_<_50m/s<sup>3</sup>|
|Foot contact score|_>_0_._6|
|Minimum pelvis height|_>_0_._6m|
|Maximum pelvis height|_<_1_._5m|
|Pelvis distance to base of support|_<_6cm|
|Spine1 distance to base of support|_<_11cm|


where _c_<sup>_LH_</sup> _t_ , _c_<sup>_LT_</sup> _t_ , _c_<sup>_RH_</sup> _t_ , and _c_<sup>_RT_</sup> _t_ represent the graded ground-contact ratio at frame _t_ for the left heel, left toe, right heel, and right toe, respectively; Figure 7 illustrates the ground-contact ratio in detail. A low foot contact score indicates significant penetration or floating, both of which are undesirable artifacts. Note that motions involving airborne phases, such as jumps, can easily satisfy this criterion as long as contact before and after the airborne phase is consistent. 


Figure 7: **Examples of Calculating the Ground-Contact Ratio.** This figure illustrates how the ground-contact ratio is computed, which is used in the foot-contact score for physics-aware curation and in the ground and skating losses for PhySINK. 

**Pelvis height** criteria exclude segments where the humanoid is unnaturally positioned. Specifically, the minimum height criterion filters out motions that involve the humanoid being excessively crouched or lying on the ground, while the maximum height criterion eliminates segments exhibiting unnatural floating. 

**Distance to the base of support** criteria ensure stable and physically plausible balance. Since the SMPL-X model’s center of mass typically lies between the pelvis and spine1 joints, deviations of these joints’ horizontal-plane projections from the base of support indicate imbalance or instability infeasible for humanoids. The base of support is defined as the convex hull formed by the horizontalplane projections of the left foot, right foot, left ankle, and right ankle joints. 

**Threshold selection.** We plot the distribution of each metric over Humanoid-X and inspect the motions along it, setting each threshold where motions stop being reproducible on flat ground (Figure 8). The root jerk and maximum pelvis height thresholds fall at the 94th and 99th percentiles and mainly remove reconstruction artifacts, while the other four are set lower to also exclude motions outside our scope, such as sitting and off-balance motions. 


Figure 8: **Distribution of Each Curation Metric over Humanoid-X.** The dashed line marks each threshold with its percentile, and motions in the shaded region marked with a cross are discarded. 

19 

#### **A.2 Dataset Composition and Statistics** 

This section presents the detailed motion statistics of PHUMA. Because we collect motion data from diverse sources, ranging from MoCap to video, PHUMA achieves a well-balanced motion distribution that is not dominated by any single motion type. As shown in Figure 9b, PHUMA exhibits substantially more balanced motion coverage than existing datasets. LaFAN1 and AMASS show uneven distributions: some motion categories are entirely absent (e.g., reach, bend, and squat), while others dominate (e.g., reach, turn, and walk). In contrast, PHUMA provides balanced coverage across all categories, with substantially more examples per motion type. The detailed composition of PHUMA is given in Table 8. 


Figure 9: **Comparison of Motion Distributions.** (a) Comparison between MoCap and Video sources in PHUMA. (b) Comparison with other existing datasets. 

Table 8: **Composition of the PHUMA dataset.** A summary of the number of clips and duration for each sub-dataset, categorized by source and scene. PHUMA aggregates these diverse sub-datasets, resulting in 73.0 hours of physically reliable motion clips. 

|Dataset|# Clip|# Frame|Duration|Source|Scene|
|---|---|---|---|---|---|
|LocoMuJoCo [21]|0.78K|0.93M|0.86h|Motion Capture|Indoor|
|GRAB [85]|1.73K|0.20M|1.88h|Motion Capture|Indoor|
|EgoBody [20]|2.12K|0.24M|2.19h|Motion Capture|Indoor|
|LAFAN1 [12]|2.18K|0.26M|2.40h|Motion Capture|Indoor|
|AMASS [13]|21.73K|2.25M|20.86h|Motion Capture|Indoor|
|HAA500 [29]|1.76K|0.11M|1.01h|Human Video|Outdoor|
|Motion-X Video [27]|33.04K|3.45M|31.98h|Human Video|Outdoor|
|HuMMan [30]|0.50K|0.05M|0.47h|Human Video|Indoor|
|AIST [31]|1.75K|0.18M|1.66h|Human Video|Indoor|
|IDEA400 [27]|9.94K|0.98M|9.10h|Human Video|Indoor|
|**PHUMA Video**|**0.50K**|**0.06M**|**0.56h**|Human Video|Outdoor|
|**PHUMA**|**76.01K**|**7.88M**|**72.96h**|||


### **B Motion Retargeting** 

This section compares PhySINK with other retargeting methods, reports its computational cost, and evaluates it as an initialization for dynamics-aware retargeting. The PhySINK loss terms are defined in Section 3.2. 

20 

#### **B.1 Comparison of Retargeting Methods** 

To provide an intuitive comparison of different retargeting approaches, we present qualitative results in Figure 10. Using a walking motion as an example, we demonstrate the distinct characteristics and limitations of each method. 

Traditional inverse kinematics (IK) prioritizes matching end-effector positions, such as hands and feet, from rigidly scaled human motions. However, this approach produces unnatural locomotion patterns where the humanoid appears to walk on a tightrope rather than exhibiting a natural humanlike gait. This occurs because the fixed scaling cannot account for the proportional differences between human and robot morphologies. 

Shape-adaptive inverse kinematics (SINK) generates more natural-looking walking motions compared to traditional IK by optimizing body proportions. However, SINK suffers from physical violations that compromise motion realism. Common issues include foot penetration through the ground surface and fixed ankle angles that result from the lack of explicit contact constraints during the retargeting process. 

In contrast, our proposed PhySINK method achieves both natural movement patterns and physical reliability. The resulting motions maintain appropriate ankle angles while ensuring proper ground contact, demonstrating that PhySINK successfully balances motion naturalness with physical constraints. This improvement stems from the incorporation of explicit physical constraint terms in the optimization objective. 

We further compare GMR [69], an optimization-based IK approach, with PhySINK. The two differ in how they generate the intermediate target motion. GMR scales the source motion by a heuristic: it estimates the subject’s height _Hsrc_ from the first SMPL shape component ( _β_ ), forms a ratio _r_ = _Hsrc/Href_ to a reference height _Href_ (e.g., 1.8m), and applies it to manually tuned per-limb scale factors. For a limb with relative position **v** _rel_ from the pelvis and manual scale _slimb_ , the scaled target is **v** _target_<sup>_′_=</sup><sup>_slimb×r×_</sup><sup>**v**</sup><sup>_rel_,whichastandardIKsolverthentracks.PhySINKinstead</sup> optimizes the SMPL shape parameters ( _β_ ) to match the humanoid in a shared T-pose and applies them to the original motion, preserving the original joint angles while adjusting limb lengths to the robot. 

This difference matters for generalization. GMR’s linear scaling works for average-sized humans but fails on diverse body shapes (Figure 11): short subjects yield undersized targets that force the robot to crouch even when standing, while tall subjects yield oversized targets beyond its reach, causing locked knees and floating feet. By applying the original joint angles with a robot-matched shape, PhySINK reproduces the intended motion regardless of the source subject’s proportions. 

This also affects policy training. We retarget the PHUMA sources with GMR (excluding the preretargeted LaFAN1 [12] and LocoMuJoCo [21]) and train a MaskedMimic policy under the same setup. As shown in Table 9, the PhySINK-retargeted policy outperforms it on both the PHUMA Test and Unseen Video benchmarks. 

Table 9: **Imitation Performance: GMR vs. PhySINK Retargeting on Unitree G1.** We evaluate the imitation performance of the MaskedMimic policy trained using datasets retargeted with GMR and PhySINK on the Unitree G1. 

||||PHUMA T|est||||Unseen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|GMR|84.0|92.1|77.8|77.1|89.1|75.2|**99.1**|77.8|**61.7**|52.7|
|PhySINK|**89.9**|**94.2**|**87.6**|**84.2**|**91.8**|**81.7**|97.4|**86.7**|**61.7**|**71.4**|


#### **B.2 Computational Cost** 

Table 10 reports retargeting throughput on a single RTX 3090 GPU. IK and GMR solve each frame independently, whereas SINK and PhySINK jointly optimize the entire trajectory to handle the 

21 


Figure 10: **Qualitative Comparison of Retargeting Methods** . This figure provides a visual comparison of human motion retargeted to a humanoid robot using the IK, SINK, and PhySINK methods. The top row shows the original human motion from the SMPL model, while the rows below show the resulting motions for each retargeting method. 

frame-level noise of video-reconstructed motion. Since PHUMA is constructed offline, we favor trajectory-level optimization over speed. 

Table 10: **Retargeting Throughput.** Frames per second of each retargeting method on a single RTX 3090 GPU. 

|Retarget|FPS|
|---|---|
|IK|38.4|
|GMR|25.3|
|SINK|0.95|
|PhySINK|0.92|


#### **B.3 PhySINK as Initialization for Dynamics-Aware Retargeting** 

SPIDER [75] consists of two steps: kinematic retargeting with GMR, followed by sampling-based optimization. We replace GMR with PhySINK in the first step and keep the second step unchanged. As shown in Table 11, starting from PhySINK raises the open-loop success rate on the Unseen Video motions from 4.6% to 10.7%. 

22 


Figure 11: **Qualitative Comparison of Motion Retargeting: GMR vs. PhySINK.** Comparison showing the limitations of GMR when handling extreme human heights. The top row illustrates retargeting from a short subject, where GMR causes excessive motion compression and crouching. The bottom row illustrates retargeting from a tall subject, where GMR generates infeasible targets, resulting in artifacts like joint locking (e.g., rigid knees) and loss of ground contact. PhySINK maintains kinematic feasibility in both cases. 

Table 11: **PhySINK as Initialization for Sampling-Based Retargeting.** Open-loop success rate (%) on the Unseen Video motions when the sampling-based optimization of SPIDER starts from GMR, as in SPIDER, or from PhySINK. 

|Retarget||Open-loop SR (%)|
|---|---|---|
|GMR+Sa|mpling (SPIDER)|4.6|
|**PhySINK**+|**Sampling**|**10.7**|


### **C Motion Imitation Learning** 

#### **C.1 Observation Space Compositions** 

This section provides detailed information about the observation space composition used in our experimental setup, as summarized in Table 12 and Table 13. The observation space consists of two main components: proprioceptive states and goal states. 

#### **C.1.1 MaskedMimic** 

**Proprioceptive States.** The proprioceptive information includes root height, body positions, body rotations, body velocities, and body angular velocities. The Unitree G1 and H1-2 robots have 33 and 25 bodies, respectively. For body positions, the root body is excluded from the position measurements. 

**Goal States.** The goal states comprise both relative and absolute body positions and rotations. The relative component represents the difference between the future 15 timesteps of reference motion states and the current proprioceptive state. The absolute component represents states relative to the reference motion’s root position, providing a root-relative coordinate frame for the target motion. 

#### **C.1.2 BeyondMimic** 

**Proprioceptive States.** The proprioceptive information includes the previous action, the base angular velocity in the body frame, and the DoF position and DoF velocity vectors. 

**Goal States.** The goal states comprise an instantaneous component and a future component. The instantaneous component provides the reference motion’s DoF position, DoF velocity, and 6D torso orientation. 

23 

Table 12: **Observation Space Dimensions of MaskedMimic.** 

||Dime|nsion||
|---|---|---|---|
|State|G1|H|1-2|
|(a) Proprioceptive State||||
|Root height|1||1|
|Body position|32_×_3|24|_×_3|
|Body rotation|33_×_6|25|_×_6|
|<br>Body velocity|33_×_3|25|_×_3|
|<br>Body angular velocity|33_×_3|25|_×_3|
|(b) Goal State||||
|Relative body position|33_×_15_×_3|25_×_|15_×_3|
|Absolute body position|33_×_15_×_3|25_×_|15_×_3|
|Relative body rotation|33_×_15_×_6|25_×_|15_×_6|
|Absolute body rotation|33_×_15_×_6|25_×_|15_×_6|
|Time|33_×_15_×_1|25_×_|15_×_1|
|**Total dim**|9898|74|98|


Unlike the original BeyondMimic, we augment the goal state with the reference motion’s future trajectory. At each future frame, we add the components listed in Table 13. We sample _K_ = 20 such frames, linearly spaced over a horizon of _H_ = 95 control steps (1 _._ 9 s at 50 Hz), forming a 20 _×_ 78 tensor. A separate motion encoder then projects this tensor to a 128-D embedding, which is concatenated with the rest of the observation. Including this future component yields a substantially higher success rate than relying on the instantaneous goal alone, in both IsaacSim and MuJoCo and on both the PHUMA Test and Unseen Video splits (Table 14). 

Table 13: **Observation Space Dimensions of BeyondMimic.** 

|State|Dimension (G1)|
|---|---|
|(a) Proprioceptive State||
|Previous action|29|
|Base angular velocity|3|
|DoF position|29|
|<br>DoF velocity|29|
|(b) Goal State||
|(b.1) Instantaneous||
|DoF position|29|
|DoF velocity|29|
|Torso rotation|6|
|(b.2) Future Motion Targets (|motion-encoder input)|
|Root height|20_×_1|
|Root roll/pitch|20_×_2|
|Base linear velocity|20_×_3|
|Base yaw rate|20_×_1|
|<br>DoF position|20_×_29|
|Local key-body position|20_×_14_×_3|
|**Total dim**|282|


24 

Table 14: **Sim-to-Sim Results of PHUMA-trained BeyondMimic Policies.** This table demonstrates the effect of the future-trajectory observation on the policy for the Unitree G1, evaluated on the PHUMA Test and Unseen Video splits. SR is the whole-body success rate at 0 _._ 5 m (%); _E_ g-mpjpe, _E_ l-mpjpe, _E_ acc, and _E_ vel are tracking errors (mm), following the convention of [9, 11, 37] and averaged over successful motions. 

|Future|||IsaacSim|||||MuJoCo|||
|---|---|---|---|---|---|---|---|---|---|---|
||SR_↑_|_E_g-mpjpe _↓_|_E_l-mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|SR_↑_|_E_g-mpjpe _↓_|_E_l-mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|
|(a) PHU|MA test||||||||||
|✗<br>✓|47.15<br>**78.77**|115.78<br>**112.00**|32.70<br>**28.28**|**1.15**<br>1.18|4.29<br>**4.14**|46.91<br>**76.02**|156.64<br>**142.79**|32.92<br>**28.98**|**1.22**<br>1.24|4.36<br>**4.18**|
|(b) Uns|een Video||||||||||
|✗|47.82|123.71|31.93|**1.07**|4.93|47.42|122.89|30.60|**1.09**|4.85|
|✓|**71.63**|**121.69**|**24.87**|1.11|**4.78**|**70.44**|**122.68**|**23.79**|1.14|**4.73**|


#### **C.2 Reward Function** 

The reward function used for training the tracking policy consists of multiple components, as detailed in Table 15 and Table 16. The overall reward structure comprises two main categories: motion tracking task rewards and regularization rewards. 

#### **C.2.1 MaskedMimic** 

**Motion Tracking Rewards.** These components encourage the policy to match the reference motion by providing higher rewards when the robot’s proprioceptive states closely resemble the target motion states. 

**Regularization Rewards.** To promote smooth and stable motion execution, we include regularization terms that penalize undesirable behaviors. Specifically, we augment the standard MaskedMimic reward formulation with action rate penalties that discourage large changes between consecutive actions, helping to ensure smooth joint movements and prevent abrupt motion transitions. 

Table 15: **Reward Function Terms of MaskedMimic.** 

|Term|Expression|Weight|
|---|---|---|
|(a) Task|||
|Global body position|exp(_−_100_· ∥pt −_ˆ_pt∥_<sup>2</sup><br>2<sup>)</sup><br><sup>ˆ</sup>|0.5|
|Root height|exp(_−_100_·_(_h_<sup>root</sup><br>_t_<br>_−h_<sup>root</sup><br>_t_<br>)<sup>2</sup>)<br>|0.2|
|Global body rotation|exp(_−_10_· ∥θt ⊖_<sup>ˆ</sup>_θt∥_<sup>2</sup><br>2<sup>)</sup><br>|0.3|
|Global body velocity|exp(_−_0_._5_· ∥vt −_ˆ_vt∥_<sup>2</sup><br>2<sup>)</sup><br>|0.1|
|Global body angular velocity|exp(_−_0_._1_· ∥ωt −_ˆ_ωt∥_<sup>2</sup><br>2<sup>)</sup>|0.1|
|(b) Regularization|||
|Power consumption|_∥F ⊙_˙_q∥_1<br>|-1e-05|
|Action rate|_∥at −at−_1_∥_<sup>2</sup><br>2|-0.2|


#### **C.2.2 BeyondMimic** 

**Motion Tracking Rewards.** BeyondMimic decomposes motion tracking into two components: tracking the global reference motion (position, rotation, and linear/angular velocity), and tracking the relative reference motion, which factors out the root’s global horizontal translation (and heading) and re-anchors the body targets to the robot’s own root. 

**Regularization Rewards.** To promote smooth and stable motion execution we use the same regularization terms used in BeyondMimic as in Table 16. 

25 

Table 16: **Reward Function Terms of BeyondMimic.** 

|Term|Expression|Weight|
|---|---|---|
|(a) Motion Tracking|||
|Reference body position|exp(_−∥p_<sup>ref</sup><br>_t _<sup>_−_ˆ</sup><sup>_p_ref</sup><br>_t _<sup>_∥_2</sup><br>2 <sup>_/_ 0</sup><sup>_._32)</sup><br><sup>ˆ</sup>|0.5|
|Reference body rotation|exp(_−∥θ_<sup>ref</sup><br>_t _<sup>_⊖θ_ref</sup><br>_t _<sup>_∥_2</sup><br>2 <sup>_/_ 0</sup><sup>_._42)</sup><br>|0.5|
|Global body linear velocity<br>Global body angular velocity<br>Relative body position|exp<br>�<br>_−_<sup>1</sup><br>_B_<br>�<br>_b_<sup>_∥vb_</sup><br>_t _<sup>_−_ˆ</sup><sup>_vb_</sup><br>_t_<sup>_∥_2</sup><br>2 <sup>_/_ 1</sup><sup>_._02�</sup><br>exp<br>�<br>_−_<sup>1</sup><br>_B_<br>�<br>_b_<sup>_∥ωb_</sup><br>_t _<sup>_−_ˆ</sup><sup>_ωb_</sup><br>_t_<sup>_∥_2</sup><br>2 <sup>_/ π_2�</sup><br>exp<br>�<br>_−_<sup>1</sup><br>_B_<br>�<br>_b_<sup>_∥pb_</sup><br>_t _<sup>_−_ˆ</sup><sup>_pb_</sup><br>_t_<sup>_∥_2</sup><br>2 <sup>_/_ 0</sup><sup>_._32�</sup><br><br>|1.0<br>1.0<br>1.0|
|Relative body rotation|exp<br>�<br>_−_<sup>1</sup><br>_B_<br>�<br>_b_<sup>_∥θb_</sup><br>_t _<sup>_⊖_ˆ</sup><sup>_θb_</sup><br>_t_<sup>_∥_2</sup><br>2 <sup>_/_ 0</sup><sup>_._42�</sup>|1.0|
|(b) Regularization|||
|Action rate|_∥at −at−_1_∥_<sup>2</sup><br>2<br><br><br><br>|-0.1|
|DoF position-limit violation|�<br>_j_<br>�<br>ReLU(_q_<sup>_j_</sup><br>_t _<sup>_−qj_</sup><br>max_,_0_._9<sup>) + ReLU(</sup><sup>_qj_</sup><br>min_,_0_._9 <sup>_−qj_</sup><br>_t_ <sup>)</sup><br>�<br><br><br>|-100|
|Undesired contacts|�<br>_b_ <sup>**1**</sup><br>�<br>_∥F _<sup>_b_</sup><br>_t _<sup>_∥_2</sup> <sup>_>_ 1 N</sup><br>�|-0.5|


#### **C.3 PPO Hyperparameters** 

The detailed hyperparameter configurations used for PPO training in MaskedMimic and BeyondMimic are provided in Table 17 and Table 18, respectively. 

Table 17: **PPO Hyperparameter Values for Model Training of MaskedMimic.** 

|**Hyperparameter**|**Value**|
|---|---|
|Optimizer|Adam|
|Num envs|8192|
|Mini Batches|32|
|Learning epochs|1|
|Entropy coefficient|0.0|
|Value loss coefficient|0.5|
|Clip param|0.2|
|Max grad norm|50.0|
|Init noise std|-2.9|
|Actor learning rate|2e-5|
|Critic learning rate|1e-4|
|GAE decay factor(_λ_)|0.95|
|GAE discount factor(_γ_)|0.99|
|Actor Transformer dimension|512|
|Actor layers|4|
|Actor heads|4|
|Critic MLP size<br>[1024,|1024, 1024, 1024]|
|Activation|ReLU|


#### **C.4 Domain Randomization** 

To bridge the simulation-to-reality gap and improve robustness to model and sensor inaccuracies, we apply domain randomization during training. The complete set of randomized parameters is summarized in Table 19. 

#### **C.4.1 BeyondMimic** 

We adopt the domain randomization scheme of BeyondMimic [18], covering actuator gains, base inertial properties, contact properties, external pushes, initial-pose perturbations, and observation 

26 

Table 18: **PPO Hyperparameter Values for Model Training of BeyondMimic.** 

|**Hyperparameter**|**Value**|
|---|---|
|Optimizer|AdamW|
|Num envs|8192|
|Steps per env|24|
|Mini batches|4|
|Learning epochs|8|
|Entropy coefficient|0.005|
|Value loss coefficient|1.0|
|Clip param|0.2|
|Max grad norm|1.0|
|Init noise std|1.0|
|Actor learning rate|1e-5|
|Critic learning rate|1e-5|
|GAE decay factor(_λ_)|0.95|
|GAE discount factor(_γ_)|0.99|
|Actor MLP size|[768, 512, 256]|
|Critic MLP size|[768, 512, 256]|
|Motion encoder hidden dim|60|
|Motion encoder output dim|128|
|Activation|SiLU|


noise. Noise is added only to the actor observation stream; the critic stream is noise-free. All randomization and noise are disabled at evaluation time. The exact ranges and schedules are listed in Table 19. 

Table 19: **Domain Randomization Ranges of BeyondMimic.** 

|**Parameter**|**Range**|
|---|---|
|P-gain scale_sP_|_U_(0_._9_,_1_._1)<br>|
|D-gain scale_sD_|_U_(0_._9_,_1_._1)|
|DoF position bias|_U_(_−_0_._025_,_0_._025)rad|
|Base CoM offset_x_|_U_(_−_0_._025_,_0_._025)m|
|Base CoM offset_y, z_|_U_(_−_0_._05_,_0_._05)m|
|Static friction|_U_(0_._3_,_1_._6)|
|Dynamic friction|_U_(0_._3_,_1_._2)|
|Restitution|_U_(0_._0_,_0_._5)|
|Push interval|_U_(1_._0_,_3_._0)s<br>|
|Push linear velocity|_U_(_±_0_._5_, ±_0_._5_, ±_0_._2)m/s|
|Push angular velocity|_U_(_±_0_._52_, ±_0_._52_, ±_0_._78)rad/s|
|Initial DoF position|_U_(_−_0_._1_,_0_._1)rad|
|Initial root position|_U_(_±_0_._05_, ±_0_._05_, ±_0_._01)m|
|Initial root rotation|_U_(_±_0_._1_, ±_0_._1_, ±_0_._2)rad|
|Initial root linear vel.|_U_(_±_0_._1_, ±_0_._1_, ±_0_._05)m/s|
|Initial root angular vel.|_U_(_±_0_._1_, ±_0_._1_, ±_0_._1)rad/s|
|Obs. noise: base angular vel. (_σ_)|0_._2rad/s|
|Obs. noise: DoF position (_σ_)|0_._01rad|
|Obs. noise: DoF velocity (_σ_)|0_._5rad/s|
|Obs. noise: motion ref orientation (_σ_)|0_._05|


27 

### **D Experiment Details** 

#### **D.1 Self-Collected Video Dataset** 

To ensure fair evaluation of imitation performance on unseen motions, we create a custom evaluation dataset using self-collected video recordings. This dataset contains motions uniformly distributed across the 11 motion types shown in Figure 9b, providing balanced coverage for comprehensive performance assessment. 

The dataset creation process follows three main steps: (1) recording videos of human performers executing each motion type, (2) converting videos into SMPL human motion parameters using a video-to-motion model, and (3) retargeting the human motions to humanoid robot motions using our PhySINK method. 

First, we record videos covering all 11 motion categories, collecting a uniform distribution for each type. We then apply the TRAM video-to-motion model [24] to extract SMPL motion parameters from the recorded videos. Finally, we process these SMPL motions with PhySINK retargeting to generate physically reliable humanoid motions. Example results from this dataset are illustrated in Figure 12. 

This self-collected evaluation set ensures that our performance assessments are conducted on completely unseen motions that were not influenced by any training data sources. Appendix D.4 repeats the main comparisons on evaluation motions retargeted with GMR. 


Figure 12: **Overview of the Self-collected Data Pipeline** . This figure illustrates the three main steps of our data collection pipeline: (left) a self-recorded video of a human motion, (center) the motion extracted using a video-to-motion model, and (right) the final motion retargeted to a humanoid robot. 

#### **D.2 Success Rate Threshold Analysis** 

To demonstrate the limitations of the conventional success rate threshold, we evaluate imitation performance using both the standard 0.5m threshold and our proposed stricter 0.15m threshold. This comparison reveals the true quality differences between policies trained on different datasets. 

Tables 20 and 21 present the results for both threshold settings. Under the loose 0.5m threshold, policies trained on different datasets show relatively similar success rates, with differences appearing modest. However, when evaluated with the stricter 0.15m threshold, performance differences become substantially more pronounced. 

These results confirm that PHUMA-trained policies achieve more precise motion tracking, producing imitations that remain accurate even under stringent evaluation criteria. The threshold analysis validates our choice to adopt the 0.15m threshold as a more meaningful measure of imitation quality. 

#### **D.3 Cross-Simulator Generalization Analysis** 

To evaluate whether PHUMA benefits cross-simulator transfer, we also trained the KungfuBot [86] policy in Isaac Gym. We compared two training configurations: one using AMASS with SINK 

28 

Table 20: **Performance Comparison based on Success Threshold in PHUMA Test.** 

||||Succe|ss Threshol|d=0.15m|||Succe|ss Thresho|ld=0.5m||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Hours|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|**(a) G1**||||||||||||
|LaFAN1|2.4|46.1|66.1|36.2|24.0|42.5|74.8|87.8|69.2|47.1|72.6|
|AMASS|20.9|76.2|88.5|72.1|56.8|66.8|90.2|95.0|87.9|81.1|83.7|
|Humanoid-X|231.4|50.6|78.4|43.0|26.0|31.8|78.4|91.3|72.9|59.5|65.9|
|**PHUMA**|73.0|**92.7**|**95.6**|**91.7**|**86.0**|**85.6**|**97.1**|**98.7**|**96.5**|**94.4**|**92.5**|
|**(b) H1-2**||||||||||||
|LaFAN1|2.4|62.0|79.3|54.7|26.6|58.9|70.8|92.4|66.7|56.4|68.2|
|AMASS|20.9|54.4|74.9|45.9|17.2|49.6|70.4|86.3|62.6|41.4|65.9|
|Humanoid-X|231.4|49.7|74.6|40.4|17.0|37.3|54.8|78.5|45.2|22.1|43.2|
|**PHUMA**|73.0|**82.7**|**91.5**|**79.5**|**68.1**|**68.4**|**92.0**|**96.6**|**89.7**|**85.6**|**79.4**|


Table 21: **Performance Comparison based on Success Threshold in Unseen Video.** 

||||Succe|ss Threshol|d=0.15m|||Succe|ss Threshol|d=0.5m||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Hours|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|**(a) G1**||||||||||||
|LaFAN1|2.4|28.4|46.9|28.4|19.6|10.5|78.2|85.5|70.8|76.3|80.8|
|AMASS|20.9|70.2|90.7|75.0|62.7|44.1|92.3|99.2|92.1|82.1|88.0|
|Humanoid-X|231.4|39.1|78.0|39.6|23.0|6.5|84.1|98.3|79.9|76.0|76.2|
|**PHUMA**|73.0|**82.9**|**96.7**|**88.0**|**71.8**|**67.1**|**93.7**|**100.0**|**96.8**|**85.9**|**84.7**|
|**(b) H1-2**||||||||||||
|LaFAN1|2.4|70.8|92.4|66.7|56.4|68.2|85.5|97.5|79.0|77.5|90.0|
|AMASS|20.9|64.3|87.3|59.7|46.0|63.9|80.4|93.3|69.9|72.8|89.0|
|Humanoid-X|231.4|60.5|88.3|60.0|48.7|39.7|68.7|93.3|65.1|60.2|50.5|
|**PHUMA**|73.0|**78.6**|**97.5**|**76.8**|**74.5**|**63.8**|**89.9**|**99.2**|**89.4**|**84.6**|**83.9**|


retargeting and another using PHUMA. For both configurations, we followed the standard KungfuBot [86] teacher-student training pipeline and evaluation metrics. Tables 22 and 23 present the teacher and student policy performance in the training simulator (Isaac Gym). The results show that policies trained with PHUMA achieve superior imitation performance, demonstrating that PHUMA’s benefits extend to other motion imitation algorithms. Importantly, this performance advantage also transfers to the evaluation simulator. Table 24 shows the zero-shot performance in MuJoCo, where the PHUMA-trained policy maintains its superiority across motion categories, indicating robust cross-simulator generalization. 

Table 22: **Imitation Performance of the KungfuBot Teacher Policy in Isaac Gym.** We evaluate the imitation performance of KungfuBot teacher policy with unseen motions on the Unitree G1. 

||||PHUMA T|est||||Unseen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|AMASS|77.8|90.8|71.2|58.3|84.7|83.5|**100.0**|83.3|74.5|72.5|
|PHUMA|**91.0**|**96.4**|**88.3**|**87.6**|**90.5**|**87.1**|99.1|**89.2**|**77.7**|**76.9**|


Table 23: **Imitation Performance of the KungfuBot Student Policy in Isaac Gym.** We evaluate the imitation performance of KungfuBot student policy with unseen motions on the Unitree G1. 

||||PHUMA T|est||||Unseen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|AMASS|66.6|86.7|58.8|41.8|68.4|67.7|**97.4**|68.0|59.6|37.4|
|PHUMA|**82.9**|**93.5**|**78.5**|**74.2**|**81.7**|**73.8**|**97.4**|**76.9**|**63.8**|**47.3**|


#### **D.4 Evaluation on GMR-Retargeted References** 

To test whether the results depend on the retargeting method used for the evaluation references, we retarget the PHUMA Test and Unseen Video motions with GMR [69] and repeat the retargeting and dataset comparisons with the conventional 0.5m success threshold. As shown in Tables 25 and 26, PhySINK and PHUMA achieve the highest success rates on both sets, and PHUMA also outperforms AMASS retargeted with PhySINK. 

29 

Table 24: **Sim-to-Sim transfer performance across motion dataset.** We evaluate the zero-shot motion tracking success rate of policies trained on PHUMA and AMASS when transferred from the source simulator (Isaac Gym) to the target simulator (MuJoCo). The results are demonstrated on the G1 humanoid to assess robustness against domain shifts in physics engines. 

||||PHUMA T|est||||Unseen Vid|eo||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|AMASS|62.1|81.4|54.2|38.8|64.3|64.3|86.2|68.5|54.3|37.4|
|**PHUMA**|**75.0**|**87.6**|**69.3**|**61.6**|**76.3**|**70.0**|**87.9**|**78.8**|**59.6**|**38.5**|


Table 25: **Imitation Performance on GMR-Retargeted References: Retargeting Methods.** Success rate (%) at the 0.5m threshold of policies trained on AMASS retargeted by each method, evaluated on the PHUMA Test and Unseen Video motions retargeted with GMR. Mean ( _±_ std) over three seeds. 

|Retarget|PHUMA Test (GMR)|Unseen Video (GMR)|
|---|---|---|
|IK|80.3 (_±_0.2)|81.6 (_±_0.6)|
|GMR|80.0 (_±_0.1)|81.1 (_±_0.3)|
|SINK|81.6 (_±_0.2)|79.8 (_±_0.6)|
|**PhySINK**|**83.4**(_±_0.2)|**83.7**(_±_0.4)|


Table 26: **Imitation Performance on GMR-Retargeted References: Datasets.** Success rate (%) at the 0.5m threshold of policies trained on each dataset, evaluated on the PHUMA Test and Unseen Video motions retargeted with GMR. Mean ( _±_ std) over three seeds. 

|Dataset|PHUMA Test (GMR)|Unseen Video (GMR)|
|---|---|---|
|LaFAN1|76.5 (_±_0.1)|81.6 (_±_0.9)|
|Humanoid-X|77.7 (_±_0.1)|79.6 (_±_0.5)|
|AMASS (SINK)|81.6 (_±_0.2)|79.8 (_±_0.6)|
|AMASS (PhySINK)|83.4 (_±_0.2)|83.7 (_±_0.4)|
|**PHUMA**|**95.5**(_±_0.2)|**89.4**(_±_0.4)|


#### **D.5 Fall Rate of Humanoid-X and AMASS Policies** 

We compare how often the policies trained on Humanoid-X and on AMASS fall in simulation, counting an episode as a fall when the pelvis height drops below 0.3m. As shown in Table 27, the Humanoid-X policy falls about three times as often on both evaluation sets, which poses a safety risk on the real robot. We therefore deploy only the AMASS policy as the real-world baseline. 

Table 27: **Fall Rate in Simulation.** Percentage of episodes in which the pelvis height drops below 0.3m, for policies trained on Humanoid-X and on AMASS retargeted with SINK. Lower is better. 

|Dataset<br>PHUMA|Test FR (%)_↓_<br>Unseen|Video FR (%)_↓_|
|---|---|---|
|Humanoid-X|18.6|13.1|
|AMASS (SINK)|**5.7**|**4.2**|


### **E Ablation Studies** 

#### **E.1 Mocap only and Video only data performance** 

To analyze the influence of the human motion source on the downstream motion tracking policy, we divide the PHUMA dataset into two distinct subsets: motions derived from motion capture (Mocap) and motions derived from video-to-motion estimation (Video-Sourced). 

We leverage these subsets to train the MaskedMimic policy using identical hyperparameters in Section C. As demonstrated in Table 29, the policy trained with video-sourced PHUMA consistently yielded superior imitation performance across all motion categories compared to the policy trained with the mocap-sourced subset. 

30 

Table 28: **Performance Evaluation of PHUMA based on Data Source (MoCap vs. Video).** We present a quantitative comparison evaluating the performance achieved using PHUMA data derived from motion capture (MoCap) versus video, concluding that both sources offer competitive results. 

||Motion Fidelity (%)|Joint Feasibility (%)|Non-Floating (%)|Non-Penetration (%)|Non-Skating (%)|
|---|---|---|---|---|---|
|MoCap|**96.7**|**100.0**|**99.9**|94.3|**92.1**|
|Video|93.8|**100.0**|**99.9**|**98.0**|88.3|


Table 29: **Imitation Performance of PHUMA based on Data Source (MoCap vs. Video).** We evaluate the imitation performance of MaskedMimic policy trained with PHUMA data derived from motion capture (MoCap) versus video on the Unitree G1. 

||||PHUMA T|est||||Unseen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|MoCap|75.2|88.2|68.4|49.0|86.9|73.0|96.6|73.9|56.4|58.2|
|Video|**85.7**|**92.9**|**81.8**|**75.5**|**89.5**|**76.2**|**100.0**|**76.4**|**59.6**|**62.6**|


We attribute this result primarily to the significantly larger and broader motion distribution of the video-sourced data. As illustrated in Figure 9a, the video-sourced dataset covers a much broader range of motion types and contains nearly two times more data than the mocap-sourced dataset. Furthermore, as shown in Table 28, the PhySINK retargeting method ensures competitive motion quality for both subsets. Because the retargeting quality is similar, the dominant factor leading to the higher imitation performance is the larger size and greater diversity of the video-sourced dataset. 

**Adding video to a mocap base.** We start from the mocap-sourced motions and add 33%, 66%, and 100% of the video-sourced motions, retargeting all of them with PhySINK. As shown in Table 30, performance on both evaluation sets is highest with the full video set. 

Table 30: **Imitation Performance When Adding Video to Mocap.** Success rate (%) at the 0.5m threshold on GMR-retargeted references, for policies trained on the mocap-sourced motions plus a growing fraction of the video-sourced motions. Mean ( _±_ std) over three seeds. 

|Data Source|PHUMA Test (GMR)|Unseen Video (GMR)|
|---|---|---|
|MoCap Only|82.2 (_±_0.2)|86.0 (_±_0.2)|
|+Video (33%)|82.1 (_±_0.1)|80.1 (_±_0.8)|
|+Video (66%)|92.8 (_±_0.1)|86.7 (_±_0.5)|
|+Video (100%)|**94.6**(_±_0.1)|**90.2**(_±_0.9)|


#### **E.2 Physics-based Filtering** 

This section provides ablation studies on the physics-based filtering criteria used in data curation (Table 7) and the physics-aware losses used in PhySINK. 

#### **E.2.1 Data Distribution Based on Physics-based Filtering** 

Figure 13 shows the filtering statistics when sequentially applying the physics-based criteria from Table 7 to Humanoid-X [1]. The filters are applied in the following order: (1) root jerk filter (jerk _<_ 50 m/s<sup>3</sup> ), (2) contact filter (foot contact score _>_ 0 _._ 6), (3) height filter (minimum pelvis height _>_ 0 _._ 6 m and maximum pelvis height _<_ 1 _._ 5 m), and (4) base of support (BoS) filter (pelvis distance to BoS _<_ 6 cm and spine1 distance to BoS _<_ 11 cm). After applying all filters sequentially, 27.1% of the original Humanoid-X dataset remains, representing motions that satisfy physical plausibility constraints. 

#### **E.2.2 PhySINK’s Robustness to Noisy Motion Sources** 

To evaluate how robustly PhySINK handles noisy human motion inputs, we retarget Humanoid-X motion sources with varying levels of filtering: (1) raw Humanoid-X (no filtering), (2) Humanoid- 

31 


Figure 13: **Dataset Statistics After Physics-based Filtering.** Distribution of motion sequences after applying physics-based filtering to the combined Humanoid-X, LaFAN1, and LocoMuJoCo datasets. 

Table 31: **PhySINK Retargeting Robustness to Noisy Motion Sources.** This figure presents an experiment to evaluate how robustly the PhySINK method retargets various noisy Humanoid-X motion sources. The six distinct motion source groups used for retargeting are compared: (1) Original Humanoid-X, and Humanoid-X motion sources sequentially refined by applying (2) Jerk filtering, <u>(3) Foot Contact filtering, (4) Height filtering, (5) BoS filtering, and (6) All filtering (PHUMA).</u> 

|Motion Source|Hours|Motion Fidelity (%)|Joint Feasibility (%)|Non-Floating (%)|Non-Penetration (%)|Non-Skating (%)|
|---|---|---|---|---|---|---|
|Humanoid-X|237.2|70.6|**100.0**|98.7|92.2|90.1|
|Jerk Filter|141.1|76.9|**100.0**|99.7|96.5|**92.0**|
|Foot Contact Filter|123.1|77.1|**100.0**|99.8|**96.8**|90.6|
|Height Filter|135.7|87.0|**100.0**|99.4|94.7|89.8|
|BoS Filter|110.3|90.7|**100.0**|99.4|94.9|90.0|
|All Filter|62.2|**94.8**|**100.0**|**99.9**|96.7|89.7|


X + jerk filtering, (3) Humanoid-X + foot contact filtering, (4) Humanoid-X + height filtering, (5) Humanoid-X + BoS filtering, and (6) Humanoid-X + all filters. We then apply PhySINK to each variant. Note that we exclude pre-retargeted datasets (LaFAN1 and LocoMuJoCo) from this analysis to isolate the effect of filtering on Humanoid-X. As shown in Table 31, PhySINK demonstrates robust retargeting performance across motion sources with varying noise levels, successfully handling physical implausibilities present in the raw data. 

#### **E.2.3 Leave-One-Out Ablation of Curation Filters** 

We remove one filter at a time from the full curation pipeline, retarget the remaining motions with PhySINK, and train a policy on each variant. As shown in Table 32, applying all filters yields the best performance, and removing the foot contact filter causes the largest drop. 

Table 32: **Leave-One-Out Ablation of Curation Filters.** Success rate (%) at the 0.5m threshold on GMR-retargeted references, for policies trained on motions curated with all filters or with one filter removed, all retargeted with PhySINK. Hours give the curated volume. Mean ( _±_ std) over three seeds. 

|Curation Filter|Hours|PHUMA Test (GMR)|Unseen Video (GMR)|
|---|---|---|---|
|**All Filters**|62|**94.6**(_±_0.1)|**90.2**(_±_0.9)|
|No Jerk Filter|75|91.8 (_±_0.1)|89.5 (_±_0.3)|
|No FC Filter|77|87.5 (_±_0.1)|80.0 (_±_0.5)|
|No Height Filter|73|89.2 (_±_0.3)|85.6 (_±_0.1)|
|No BoS Filter|88|89.5 (_±_0.1)|87.4 (_±_0.7)|


#### **E.2.4 Sensitivity to the Video Reconstruction Model** 

We reconstruct the Unseen Video motions with TRAM [24], used in PHUMA, and with GVHMR [25], then curate them and retarget the accepted motions with SINK and PhySINK. As 

32 

shown in Table 33, GVHMR yields a higher curation acceptance rate, yet the better reconstruction does not close the quality gap between SINK and PhySINK. 

Table 33: **Sensitivity to the Video Reconstruction Model.** Curation acceptance rate on the Unseen Video motions and retargeting quality of SINK and PhySINK, for motions reconstructed with TRAM and GVHMR. 

|Reconstruction|Acceptance|Retarget||Reta|rgeting Qu|ality||
|---|---|---|---|---|---|---|---|
||Rate (%)||MF (%)|JF (%)|NF (%)|NP (%)|NS (%)|
|TRAM|41.9|SINK<br>PhySINK|**95.9**<br>**95.9**|63.6<br>**100.0**|**100.0**<br>**100.0**|27.2<br>**99.7**|40.1<br>**93.8**|
|GHMR|**774**|SINK|**95.6**|78.7|99.9|27.3|64.8|
|V|**.**|PhySINK|**95.6**|**100.0**|**100.0**|**100.0**|**86.6**|


#### **E.3 Impact of Motion Retargeting Quality on Policy Performance** 

To investigate how physical artifacts in retargeted motion data affect policy learning, we train MaskedMimic policies on datasets generated using six retargeting methods with varying artifact levels. The methods are: (1) **IK** , which produces significant artifacts in motion fidelity, joint limits, grounding, and skating; (2) **GMR** , which reduces motion fidelity loss, grounding issues, and skating compared to IK; (3) **SINK** , which improves motion fidelity and joint limit violations; (4) **SINK + Joint Feasibility Loss** , which further reduces joint limit violations; (5) **SINK + Joint Feasibility + Grounding Loss** , which addresses all artifact types except skating; and (6) **PhySINK** , which minimizes all physical artifacts. To isolate the effect of retargeting quality, we exclude the LaFAN1 and LocoMuJoCo datasets from this analysis, as they were pre-retargeted and would not allow for fair comparison across methods. 

In Table 34, our results show that SINK-based methods, which first optimize the humanoid body shape before applying it to the original motion, consistently outperform IK-based methods that rely on heuristic scaling to bridge human-humanoid discrepancies. Notably, GMR achieves better performance than IK despite having similar joint limit issues, while the SINK variants further outperform GMR in tracking performance. However, across the SINK variants themselves (SINK, SINK + Joint Feasibility Loss, SINK + Joint Feasibility + Grounding Loss), we observe comparable performance despite their similar levels of motion fidelity, joint feasibility, and grounding quality, the main differences among these variants being penetration and skating artifacts. 

These results indicate that motion fidelity is the most critical factor affecting motion tracking performance. The substantial performance improvement of GMR over IK (achieved primarily through motion fidelity gains rather than joint feasibility improvements) demonstrates that preserving motion fidelity during retargeting has a greater impact on policy learning than other artifact types. However, once motion fidelity reaches a certain threshold (as in the SINK variants), further reductions in other artifact types yield diminishing returns for policy learning. 

Table 34: **Ablation Studies of Imitation Performance on Retargeting Loss.** We evaluate the imitation performance of MaskedMimic policies trained with and without the physical constraint loss <u>(Table 1) using the Unitree G1 robot.</u> 

||||PHUMA T|est||||Unseen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|IK|70.5|85.9|63.3|47.6|77.3|68.5|96.6|72.4|43.6|49.5|
|GMR|84.0|92.1|77.8|77.1|89.1|75.2|99.1|77.8|61.7|52.7|
|SINK|89.1|94.0|86.0|84.9|90.7|79.0|**100.0**|81.8|**62.8**|62.6|
|+ Joint Feasibility Loss|87.0|92.1|83.6|79.8|90.9|78.6|94.8|84.7|56.4|67.0|
|+ Grounding Loss|**90.0**|93.5|**87.9**|**85.6**|**92.0**|80.4|98.3|86.2|60.6|64.8|
|+ Skating Loss|89.9|**94.2**|87.6|84.2|91.8|**81.7**|97.4|**86.7**|61.7|**71.4**|


33 

#### **E.4 Leave-One-Out Ablation of PhySINK Losses** 

We remove one loss at a time from the full PhySINK objective and train a policy on each variant. As shown in Table 35, removing a loss degrades the retargeting metric that loss governs, while the full objective achieves the highest tracking performance. Removing the grounding loss causes the largest drop. 

Table 35: **Leave-One-Out Ablation of PhySINK Losses.** Retargeting quality, and success rate (%) at the 0.5m threshold on GMR-retargeted references, with each loss removed from the full objective. Mean ( _±_ std) over three seeds. 

|Retarget||Reta|rgeting Q|uality||Motion Trackin|g Performance|
|---|---|---|---|---|---|---|---|
||MF (%)|JF (%)|NF (%)|NP (%)|NS (%)|PHUMA Test (GMR)|Unseen Video (GMR)|
|**PhySINK**|94.8|**100.0**|**99.9**|96.8|89.7|**94.6**(_±_0.1)|**90.2**(_±_0.9)|
|No Joint Feasibility Loss|91.7|95.8|**99.9**|96.4|89.4|91.0 (_±_0.1)|85.8 (_±_0.6)|
|No Grounding Loss|91.8|**100.0**|96.4|14.6|**91.7**|90.5 (_±_0.1)|84.5 (_±_0.8)|
|No Skating Loss|**94.9**|**100.0**|**99.9**|**97.2**|53.6|94.2 (_±_0.1)|88.2 (_±_0.8)|


### **F Pelvis-Only Path Following Control Performance** 

We evaluate whether training on PHUMA enables better pelvis path-following control compared to the AMASS dataset. Using MaskedMimic’s partially-constrained protocol, we train two student policies: one distilled from an AMASS-trained teacher and another from a PHUMA-trained teacher. Both students receive only pelvis position and rotation as input. 

As shown in Table 36, policies trained on PHUMA outperform those trained on baseline datasets across all motion categories and humanoids, with the largest gap on dynamic motions. Figure 14 illustrates this, where AMASS-trained policies fail on running while PHUMA-trained policies remain robust. 

Table 36: **Pelvis path following peformance across motion dataset.** We evaluate the success rate of pelvis path-following control for policies trained on the AMASS and PHUMA datasets across various pelvis trajectories from the PHUMA Test and Unseen Video. 

||||PHUMA T|est||||Unseen Vi|deo||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|**(a) G1**|||||||||||
|AMASS|60.5|85.6|60.1|51.4|66.5|54.8|83.6|66.5|33.0|27.5|
|**PHUMA**|**84.5**|**94.6**|**86.1**|**83.7**|**90.2**|**74.6**|**98.3**|**83.3**|**54.3**|**57.1**|
|**(a) H1-2**|||||||||||
|AMASS|60.4|84.0|62.8|43.6|78.7|72.3|**96.6**|77.3|52.1|72.5|
|**PHUMA**|**73.9**|**91.2**|**76.5**|**66.9**|**84.8**|**78.1**|**96.6**|**77.8**|**60.6**|**78.0**|


### **G Results on H1-2 Robot** 

This appendix provides complete results on the Unitree H1-2 [82] robot, complementing the G1 results presented in the main text. 

#### **G.1 PhySINK Ablation on H1-2** 

Table 37 presents the ablation study of PhySINK retargeting on the H1-2 humanoid robot, showing the progressive impact of each physical constraint loss. 

#### **G.2 Retargeting Method Comparison on H1-2** 

Table 38 shows motion tracking performance across retargeting approaches on the H1-2 robot. 

34 


Figure 14: **Path following on running motion.** We visualize the robot’s trajectory in a running motion. The target pelvis path is visualized with a green line. Top row presents results from a policy trained on AMASS, while bottom row presents results from a policy trained on PHUMA. 

Table 37: **Quantitative comparison and ablation study of retargeting methods on H1-2.** Pro- <u>gressive impact of adding each physical constraint loss.</u> 

||Motion Fidelity (%)|Joint Feasibility (%)|Non-Floating (%)|Non-Penetration (%)|Non-Skating (%)|
|---|---|---|---|---|---|
|IK|36.3|80.9|57.7|45.2|56.1|
|GMR|58.0|71.8|6.0|**100.0**|62.3|
|SINK|93.9|15.3|42.2|81.4|47.9|
|+ Joint Feasibility Loss|**94.0**|99.5|44.4|79.9|50.7|
|+ Grounding Loss|93.9|**99.9**|**99.8**|98.1|49.3|
|+ Skating Loss = PhySINK|93.9|**99.9**|97.7|99.7|**87.7**|


Table 38: **Motion tracking performance across retargeting approaches on H1-2.** Success rates using two test sets. 

||||PH|UMA Test||||Unseen|Video||
|---|---|---|---|---|---|---|---|---|---|---|
|Retarget|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|IK|45.3|70.9|35.7|15.2|35.0|54.2|78.0|60.7|30.1|28.6|
|GMR|56.6|75.7|48.1|24.8|**65.9**|64.3|80.2|65.5|52.1|53.8|
|SINK|54.4|74.9|45.9|17.2|49.6|64.3|87.3|59.7|46.0|**63.9**|
|**PhySINK**|**64.3**|**83.6**|**57.0**|**27.7**|55.9|**72.4**|**99.2**|**66.3**|**57.4**|63.1|


#### **G.3 Dataset Effectiveness on H1-2** 

Table 39 presents motion tracking performance across training datasets on the H1-2 robot. 

Table 39: **Motion tracking performance across datasets on H1-2.** Success rates evaluated on two test sets. 

|||||PHUMA T|est||||Unseen Vid|eo||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|Hours|Total|Stationary|Angular|Vertical|Horizontal|Total|Stationary|Angular|Vertical|Horizontal|
|LaFAN1|2.4|62.0|79.3|54.7|26.6|58.9|70.8|92.4|66.7|56.4|**68.2**|
|AMASS|20.9|54.4|74.9|45.9|17.2|49.6|64.3|87.3|59.7|46.0|63.9|
|Humanoid-X|231.4|49.7|74.6|40.4|17.0|37.3|60.5|88.3|60.0|48.7|39.7|
|**PHUMA**|73.0|**82.7**|**91.5**|**79.5**|**68.1**|**68.4**|**78.6**|**97.5**|**76.8**|**74.5**|63.8|


35 

