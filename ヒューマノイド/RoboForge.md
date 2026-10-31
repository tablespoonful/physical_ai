---
title: "RoboForge: Physically Optimized Text-guided Whole-Body Locomotion for Humanoids"
date: "2026-03-18"
authors: "Xichen Yuan; Zhe Li; Bofan Lyu; Kuangji Zuo; Yanshuo Lu; Gen Li"
url: https://arxiv.org/abs/2603.17927
pdf: https://arxiv.org/pdf/2603.17927
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.17927)** / [論文ページ](https://arxiv.org/abs/2603.17927)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RoboForge: Physically Optimized Text-guided Whole-Body Locomotion for Humanoids** 

**Xichen Yuan***<sup>1</sup> , **Zhe Li***<sup>1</sup> , **Bofan Lyu**<sup>1</sup> , **Kuangji Zuo**<sup>1</sup> , **Yanshuo Lu**<sup>1</sup> , **Gen Li**<sup>1</sup> , **Jianfei Yang**<sup>1</sup><sup>_,†_</sup> 

> 1MARS Lab, Nanyang Technological University 

While generative models have become effective at producing human-like motions from text descriptions, transferring these motions to humanoid robots for physical execution remains a major challenge. Existing pipelines are often fractured by the retargeting bottleneck, where kinematic elegance is compromised by physical infeasibility, contact-transition errors, and the prohibitive cost of real-world dynamical data. We present a unified, latent-driven framework that bridges the gap between natural language and whole-body locomotion through a retarget-free and physics-optimized pipeline. Rather than treating generation and control as disconnected steps, our core insight lies in their bidirectional coupling, where both steps are optimized jointly subject to physical constraints. We introduce the Physical Plausibility Optimization (PP-Opt) module as a coupled interface. In the forward direction, it refines a teacher-student distillation policy using a plausibility-centric reward to suppress non-physical artifacts such as floating, skating and penetration; in the backward direction, PP-Opt converts reward-optimized simulation rollouts into high-quality explicit motion data, which is then used to fine-tune the motion generator so that it learns a more physically plausible latent distribution. The bidirectional design establishes a self-improving cycle, where the generator learns to encode motion within a physically grounded latent space, while the controller learns to execute latent-conditioned behaviors with dynamical integrity. Extensive experiments on the Unitree G1 humanoid validate that our bidirectional optimization yields gains in tracking errors and success rates. Across IsaacLab and MuJoCo, our implicit latent-driven approach consistently outperforms conventional explicit retargeting pipelines in both precision and stability. By coupling the “imagination” of diffusion models with the physical plausibility optimization, our work offers a robust path toward deployable, text-guided humanoid intelligence. **The project page:** https://xichen-001.github.io/RoboForge/ 

**Correspondence:** Jianfei Yang at jianfei.yang@ntu.edu.sg 


## **1 Introduction** 

Turning text into robot motion means generating sequences that remain capable under contacts, torques, and hardware limits—not just plausible in a renderer. Modern generative models have made significant progress in the generation of motions from linguistic descriptions Xie et al. (2023); Li et al. (2025d). In particular, diffusion-based motion generators have demonstrated remarkable performance in text-to-motion synthesis, generating sequences that are increasingly fluid, diverse, and semantically coherent Chen et al. (2023); Tevet et al. (2022b). However, there is a significant gap between visual animation and robotic execution Yuan et al. (2023); Li et al. (2025e); He et al. (2024b). While animation models focus on visual plausibility, humanoid robots must prioritize physical feasibility. This difference in objectives requires that the generated motions for robotics 

fall within a dynamically stable subset of human-like motions, strictly limited by balance, contact, and hardware capabilities Ma et al. (2025); He et al. (2025, 2024a). Neglecting these fundamental differences in design objectives leads to physical inconsistencies, such as foot skating and loss of contact Yuan et al. (2023); Han et al. (2025); Li et al. (2025e); He et al. (2024b), which ultimately cause the robot to become unstable when performing these motions in the real world. 

Generative models often maintain a sense of visual smoothness by allowing feet to skate through or penetrate into the terrain, effectively sacrificing the abrupt impact and absolute stasis required by physical laws. In the physical world, contacts are discrete, mode-switching events that dictate the exchange of momentum between the robot and its environment. This discrepancy is important at the interface of contact dynamics. Conversely, current generative 

1 


**Figure 1 RoboForge.** aims to perform physically plausible motions. **(a)** performed a series of three martial arts kicks. **(b)** turned around and threw the javelin with great force. **(c)** squats to avoid, then kicks, and finally punches. 

paradigms are fundamentally continuous in nature Li et al. (2024b,a); Zhang et al. (2024); they prioritize smooth trajectory fitting but lack the analytical rigor to guarantee that discrete contact constraints remain valid over long horizons. The conventional decode–retarget–track pipeline introduces small errors in each stages, and these errors often spike during contact transitions Luo et al. (2023a); Araujo et al. (2025); Yang et al. (2025). Importantly, errors occurring at these contact transitions do not accumulate in a linear fashion. Minor errors might seem harmless in early stages, but they may be swiftly magnified when contact constraints are engaged, leading to root drift, locomotion gait collapse, and incremental error Li et al. (2025b,c). 

Parallel to these architectural flaws is the data scarcity problem: real-robot data are expensive and costly, limiting the scalability of robotics learning Kalaria et al. (2025). While latent-space diffusion offers a more efficient alternative by compressing high-dimensional MoCap data into dense representations Chen et al. (2023); Yuan et al. (2023). A critical gap remains: generated latent motion representations are not inherently grounded in the robot’s physically plausible space. A common workaround is to decode latents into joint trajectories and then retarget them, which reintroduces non-physical artifacts and incremental errors. Therefore, we argue 

that robustness requires closing the loop: generation must be constrained by physical laws, and execution must be conditioned directly by text prompts via a latent-to-action interface Li et al. (2025b). 

In this work, we propose RoboForge, an end-toend framework that unifies text-to-latent generation, physics-based optimization, and latent-driven tracking for humanoid robots. Our core technical contribution is the physical plausibility optimization (PP-Opt) module, a bidirectional interface that refines both the generator and the controller. By tracking motion latents directly, our pipeline bypasses the retargeting stage entirely and utilizes PP-Opt to fine-tune physically plausible distribution back into the generative latent space. This ensures that motions synthesized from text prompts are grounded in physical robotic reality. The contributions of this work are summarized as follows: 

- We present a unified, latent-driven humanoid control framework that replaces conventional explicit retargeting with direct latent-to-action mapping, significantly reducing the accumulation of kinematic drift at contact transitions. 

- We introduce the PP-Opt module, a bidirectional optimization bridge that iteratively enhances both the generation quality and the tracking stability by coupling generative semantics with 

2 

physics-based reward functions. 

- We demonstrate robust, text-guided whole-body locomotion on the Unitree G1 humanoid robot across diverse scenarios. Evaluations in IsaacLab and MuJoCo validate that our approach can substantially reduce non-physical artifacts and outperform traditional retargeting-based baselines in both success rates and tracking errors. 

## **2 Related works** 

### **2.1 Text-to-Motion Generation and Latent Diffusion** 

Text-to-motion generation seeks to create extended human motion sequences from language prompts. Initial autoregressive and VAE-based approaches struggled with maintaining coherence and diversity over long durations Petrovich et al. (2022). Recent diffusion-based approaches substantially improve text– motion alignment and motion realism via iterative denoising, but sampling in high-dimensional motion space can be expensive Tevet et al. (2022b,a). Latent diffusion mitigates this by learning a compact encoder–decoder representation and performing denoising in latent space, improving efficiency and reducing sensitivity to high-frequency noise Chen et al. (2023); Rombach et al. (2022). Importantly, the latent also serves as a concise, information-rich conditioning signal for downstream control, enabling implicit (retarget-free) interfaces Li et al. (2025b,a,c) where policies track motion intent without explicitly consuming full reference trajectories. 

### **2.2 Physics-Grounded Generation and Refinement** 

Motions that are visually plausible are not necessarily physically executable: common failures include ground penetration, floating, and foot skating Han et al. (2025); Yuan et al. (2023); Li et al. (2025e). Existing work Han et al. (2025); Li et al. (2025e); Luo et al. (2023a); Peng et al. (2021, 2018); Yuan et al. (2023) improves physical consistency from three complementary angles. (i) _Physics-guided generation_ incorporates contact and dynamics priors (using hand-crafted penalties or learned critics) into the generative objective to steer outputs toward feasible areas, though ensuring feasibility in contact-rich scenarios remains challenging. (ii) _Simulator iterative optimization_ treats executability as an explicit objective and uses physics feedback (e.g., RL reward function) to steer behaviors toward physics plausible 

solutions, at the cost of higher computation and careful stability design. (iii) _Post-generation refinement_ follows a generate-then-correct paradigm, projecting motions into executable trajectories using a simulator and a tracking/optimization module. A key takeaway is that the most scalable direction is to close the loop: use simulation-based refinement not only to fix samples, but also to improve the generator’s distribution over time Li et al. (2025e). 

### **2.3 Humanoid Motion Tracking and Retargetfree Inference Pipeline** 

Physics-based humanoid tracking policies have become a standard route to long-horizon, contact-rich whole-body control Luo et al. (2023b); He et al. (2024b,a). Conventional pipelines rely on explicit reference motions He et al. (2025); Araujo et al. (2025); Peng et al. (2022); Peng (2025); Liao et al. (2025): human data are retargeted to the robot and then tracked, but retargeting can introduce systematic misalignment that amplifies around contacts and degrades transfer. Recent work Li et al. (2025b) explores implicit interfaces where a latent directly conditions the policy, simplifying inference and reducing multi-stage incremental error. However,simplifying the interface alone does not guarantee executability; effective deployment still requires simulator-based optimization to align motion intent with dynamics and contact constraints. 

### **2.4 Positioning of Our Work** 

Our work advances this line of research along a unified direction. We adopt a latent-space diffusion-based motion generator (MG) Chen et al. (2023) to provide motion representation. We introduce PP-Opt as a bidirectional interface between the MG and the whole-body tracker Li et al. (2025b): on the one hand, PP-Opt improves tracker physical plausibility through a physics-simulation; on the other hand, it constructs high-quality refined data via refinement and filtering, which is then used to feed back and improve the generator. At the same time, we combine teacher–student distillation and DAgger Ross et al. (2011) to build a latent-driven, retarget-free inference pipeline. 

Unlike methods that treat physical consistency merely as a one-shot post-processing step, or methods that still depend on explicit retargeted references to finetune our Motion Generator, our framework couples generation and control through a closed-loop process of generate _→_ execute _→_ filter _→_ re-generate. In this way, physical plausibility becomes a jointly 

3 

optimized objective shared by both motion generation and control, rather than an isolated correction module. 

## **3 METHODOLOGY** 

We propose an end-to-end framework as illustrated in Fig. 2. The framework is composed of four key modules. (i) Motion Generation Chen et al. (2023), which produces a motion latent representation from text prompts; (ii) Physical Plausibility Optimization Module, which enforces physics plausibility via objective reward functions during policy training; (iii) Training Pipeline, which realizes latent-driven whole-body tracking control via a teacher–student distillation with DAgger; and (iv) Sim-to-Real Deployment, which exports the trained policy to ONNX and supports both sim-to-sim transfer in MuJoCo and real-robot execution via the Unitree SDK. 

### **3.2 Motion Latent Diffusion-Based Human Motion Generation** 

Following Chen et al. (2023), we train the motion generator on the HumanML3D Guo et al. (2022) and KIT-ML Plappert et al. (2016) datasets. Given a text condition _τ_ , the objective is to model a temporal human motion sequence _x_ 1: _T_ and produce a motion latent _z_ that can be consumed by the downstream control policy. We first learn an expressive and reconstructable latent space using an encoder–decoder objective. The encoder compresses the motion sequence into a latent representation, while the decoder reconstructs the motion to enforce semantic consistency. 

After learning the latent space, we freeze the encoder and train a conditional diffusion model to capture the text-conditioned distribution _p_ ( _z | τ_ ). Specifically, a forward noising process is defined in the latent space, and a Transformer-based denoising network is trained to predict noise conditioned on the text condition _τ_ , thereby learning the reverse generative process: 


### **3.1 Problem Formulation** 

At each control step _t_ , the system receives the robot’s proprioceptive observations _ot_ together with a motion latent _lt_ produced by the motion generator. The teacher policy takes privileged information, proprioception, and reference motion data as inputs, and outputs a control action _at_ , which is executed in simulation to obtain the next state _st_ +1. Then, we apply DAgger to distill the teacher’s behavior distribution into a student diffusion policy, enabling robust control at inference time using only deployable observations. 

To improve both the physical plausibility and tracking ability of the generated motions, we introduce a _Physics Plausibility Optimization Module_ (PP-Opt module). This module optimizes the tracking policy using a physical plausibility objective reward function _J_ ( _ξ_ ) computed from the physics simulation. In addition, failure cases are collected to perform motion quality control, producing higher-quality motion data that are used to fine-tune the motion generator. 

This formulation aims to address two key questions: (1) whether a purely implicit, latent-driven inference pipeline can replace explicit retargeted references during deployment; and (2) whether physics-based optimization within the PP-Opt module can systematically improve both the motion generator and the tracking policy. 

where the loss function is defined as: 


At inference time, we start from Gaussian noise and iteratively denoise to obtain a sampled motion latent _z_ ˆ, which captures the semantics specified by the input text _τ_ . 

### **3.3 Physics-Plausibility Optimization Module** 

The PP-Opt module connects the motion generator (MG) with the whole-body tracker. It uses physics simulation to train a tracking policy that executes and effectively “corrects” MG-conditioned motion intents, while providing plausibility feedback to improve both the tracker and MG. Specifically, PP-Opt establishes a closed-loop process where generated motions are executed and refined in simulation, unreliable outcomes are filtered, and the remaining physically plausible motions are leveraged to further improve the generator. 

_Forward optimization of the tracker_ In the forward direction, PP-Opt treats the tracker as a control policy optimized in the simulator. The resulting policy shares the same architecture and training pipeline as the teacher tracker and can be directly reused as the teacher policy for DAgger distillation.Following Han 

4 


**Figure 2** The RoboForge end-to-end framework. The framework is composed of four key modules: (i) Motion Generation module, (ii) Physical Plausibility Optimization Module, (iii) Training Pipeline, and (iv) Sim-to-Real Deployment. 

et al. (2025), We denote an executed trajectory produced in simulation as _ξ_ = _{·}_<sup>_T_</sup> _t_ =1<sup>anddefinea</sup> sequence-level physical plausibility objective reward function as the sum of per-frame objectives reward: 


At each time step, physical plausibility is evaluated by penalizing three common non-physical artifacts: foot skating, floating, and ground penetration: 


The penetration term penalizes foot–ground interpenetration when the foot falls below the ground plane: 


Under these physical plausibility objective reward functions, PP-Opt employs reinforcement learning within a closed-loop physics simulation to optimize the whole-body tracker. When conditioned on MG outputs ( _i.e._ , latent-driven motion intents), the optimized tracker exhibits fewer non-physical behaviors such as skating, floating, and ground penetration, resulting in a more physically executable controller. 

The skating term penalizes unrealistic foot displacement during contact, measured using the foot position difference gated by a contact indicator: 


The floating term penalizes cases where the foot is above the ground while still expected to be in contact, where _zf_<sup>_t_denotes the foot height and</sup><sup>_zg_is the ground</sup> height: 


_Motion quality control and Backward fine tune_ In the backward direction, PP-Opt is employed to finetune the upstream motion generator using refined motion data as high-quality supervision. After PPOpt refinement, we perform motion quality control to curate the final fine-tuning dataset for the motion generator . For each motion clip, we compute the average _E_ mpjpe between the motion before and after physical refinement. A fixed acceptance threshold _η_ = 0 _._ 5 is applied. If the _E_ mpjpe is below _η_ , the refinement is considered stable and the refined motion is retained; otherwise, it is regarded as an imitation mismatch or a refinement failure and discarded from the finetuning set. We further remove motions that involve 

5 

object interactions or non-grounded behaviors ( _e.g._ , playing the violin, swimming, or carrying boxes), as these violate the flat-ground, non-interactive, groundcontact assumptions and often lead to unreliable outcomes in physics simulation. 

MG is then fine-tuned on the filtered high-quality motion set, biasing its generation distribution toward an executable region. As a result, subsequent sampling produces higher-quality latents and further reduces the burden on the downstream tracker. 

Overall, PP-Opt establishes a bidirectional optimization interface between MG and the tracker: in the forward direction, it improves the tracker’s physical plausibility via _J_ ( _ξ_ ), while in the backward direction, it enhances MG through iterative refinement and fine-tuning, leading to mutually reinforcing gains in both motion generation and control. 

## **4 Experiments** 

This section evaluates the proposed framework and addresses three questions corresponding to its core design choices. **(1) Is physical plausibility optimization necessary?** We quantify the effect of PP-Opt on motion generation by comparing MG before and after applying PP-Opt, reporting standard text-to-motion quality metrics alongside physics-based plausibility measures. **(2) How does iterative PP-Opt refinement affect MG?** We investigate the impact of iterative PP-Opt cycles on the generator. Each cycle consists of: (i) sampling motions from MG, (ii) refining them with PP-Opt in simulation, (iii) applying motion quality control to retain high-quality refined motions, and (iv) fine-tuning MG on the filtered set. We repeat this process for one, two, and three cycles, and evaluate MG after each stage using both generation quality and physical plausibility metrics. **(3) Is implicit latent conditioning beneficial?** We compare our latent-driven, retarget-free control interface with a conventional pipeline based on explicit retargeted reference motions, and evaluate tracking performance and execution stability under both settings. 

### **4.1 Experimental Settings** 

_Datasets_ We conduct training and evaluate on the HumanML3D Guo et al. (2022) and KIT-ML Plappert et al. (2016) datasets. For policy training, only the index-0 clip for each motion name ( _e.g._ , 00000_0.npy) is used, and mirrored variants are removed to reduce redundancy. Motions involving non-planar terrain or physically infeasible contacts are filtered to enforce a flat-ground setting. The resulting set is 


**Figure 3** Text-guided examples in simulation. The humanoid performs diverse motions including boxing, jumping jacks, and martial arts kicking under different text prompts. 

split into training and test sets with an 8:2 ratio using stratified category balance. For motion generator training, the full datasets are used. 

_Evaluation metrics_ Motion generation performance is evaluated via PP-Opt and downstream tracking results. Following Guo et al. (2022); Zhang et al. (2024),we report R-Precision (RTOP-1, RTOP-2, RTOP-3) to measure text-to-motion retrieval accuracy, Frechet Inception Distance (FID) to assess distributional similarity between generated and groundtruth motions, and Diversity (Div) to quantify sample diversity. Following Han et al. (2025),physical plausibility is further evaluated using physics-based metrics Han et al. (2025), including Penetrate (ground penetration), Float (floating above ground), Skate (foot sliding), which measures the realism of foot– ground interactions. Tracking performance is evaluated in physics simulators following standard protocols He et al. (2024a); Luo et al. (2023a). We report success rate , together with _E_ mpjpe and _E_ mpkpe, where success reflects both accuracy and execution stability. 

### **4.2 Ablation Studies on PP-Opt Module** 

#### **4.2.1 Evaluation of physics-optimized motion generation** 

As shown in Table 1, PP-Opt improves both generation quality and physical plausibility without notice- 

6 

**Table 1** Evaluation of physics-optimized motion generation: MG with/without PP-Opt. 

|||Com|mon MG M|etrics||Physics Pl|ausibility M|etrics|
|---|---|---|---|---|---|---|---|---|
|Methods||R-Precision|_↑_|FID_↓_|Div_→_|Penetrate_↓_|Float_↓_|Skate_↓_|
||Top1_↑_|Top2_↑_|Top3_↑_||||||
|Ground-Truth|0.552|0.733|0.782|0.008|9.553|–|–|–|
|MLD|0.523|0.703|0.761|0.484|9.734|0.042|1.744|0.064|
|MLD&PP-Opt|0.531|0.709|0.766|0.462|9.682|0.000|0.713|0.061|


**Table 2** Tracking policy with/without PP-Opt training optimization. 

|Methods|IsaacL|ab||MuJoC|o|
|---|---|---|---|---|---|
|Succ_↑_|_E_mpjpe _↓_|_E_mpkpe|_↓_Succ_↑_|_E_mpjpe _↓_|_E_mpkpe _↓_|
|MLD<br>0.94|0.14|0.11|0.63|0.26|0.24|
|MLD&PP-Opt 0.96|0.11|0.09|0.71|0.21|0.20|


ably sacrificing diversity. Compared to the original MLD, text–motion consistency increases modestly but consistently (e.g., Top-1 rises from 0.523 to 0.531), and distribution alignment gets closer to real data (FID drops from 0.484 to 0.462), while diversity remains essentially preserved (Div changes slightly from 9.734 to 9.682). More importantly, PP-Opt systematically suppresses contact-related artifacts: penetration is reduced from 0.042 to 0.000, and floating decreases substantially from 1.744 to 0.713; skating also shows a minor improvement (0.064 to 0.061). Overall, PPOpt mainly cleans up physically implausible details while maintaining semantic usability and a reasonable motion distribution. 

#### **4.2.2 Evaluation of physics-optimized tracking policy** 

Table 2 shows that improving the physical quality of generated motions also pays off downstream. Training the tracker on MLD+PP-Opt consistently yields higher success and lower tracking errors in both simulators. In IsaacLab, success improves from 0.94 to 0.96, while _E_ mpjpe drops from 0.14 to 0.11 and _E_ mpkpe from 0.11 to 0.09. The gains are more pronounced in MuJoCo, where success increases from 0.63 to 0.71 with errors reduced from 0.26 to 0.21 and from 0.24 to 0.20, respectively. This pattern suggests that PP-Opt does not merely overfit the training setup; by removing physically inconsistent artifacts in the training distribution, it produces trackers that are both more accurate and less sensitive to contact mismatch across simulators. 

#### **4.2.3 Evaluation of multi-cycle PP-Opt refinement on MG** 

Table 3 evaluates the effect of running PP-Opt in a closed loop for multiple cycles. Each additional cycle brings small but consistent improvements. From One-Round to Two-Round, FID drops from 0.462 to 0.456 and R-Precision Top-1 increases from 0.531 to 0.535, while physical artifacts continue to shrink (Float 0.713 to 0.709, Skate 0.061 to 0.059). After Three-Round, the gains persist but start to saturate: Top-1 reaches 0.537 and FID further decreases to 0.454, with Float and Skate improving to 0.707 and 0.058. Penetration stays at 0.000 throughout, and diversity does not collapse (Div remains around 9.7). Overall, the closed-loop refinement behaves as intended: PP-Opt cleans the data used to update MG, and the improved MG in turn provides better samples for the next PP-Opt cycle, producing cumulative gains with diminishing returns after about three rounds. 

### **4.3 Evaluation of Latent-Driven Pipeline** 

Table 4 compares two downstream control interfaces: a conventional explicit chain that retargets a reference motion with GMR Araujo et al. (2025) and then tracks it, and our implicit latent-driven interface that guides the policy directly via the latent. The outcome is consistent across both simulators: the implicit interface performs better. In IsaacLab, success rates increase from 0.91 to 0.96, while tracking errors drop substantially, with _E_ mpjpe decreasing from 0.23 to 0.11 and _E_ mpkpe from 0.17 to 0.09. The gap becomes more pronounced in MuJoCo sim-to-sim transfer, where success rates improve from 0.62 to 0.71 and errors reduce from 0.26 to 0.21 and from 0.31 to 0.20. The results indicate that explicit retargeting inevitably introduces incremental errors, which accumulate throughout the reference motion and manifest as inconsistent guidance for the tracker. Conversely, the implicit latent-driven approach effectively eliminates this fragile step, enabling the policy 

7 

**Table 3** Evaluation of the effects of multiple rounds of PP-Opt on MG. 

||Co|mmon MG|Metrics|||Physics Pl|ausibility|Metrics|
|---|---|---|---|---|---|---|---|---|
|_MLD&PP-Opt_||R-Precision|_↑_|FID_↓_|Div_→_|Penetrate_↓_|Float_↓_|Skate_↓_|
||Top1|Top2|Top3||||||
|One-Round|0.531|0.709|0.766|0.462|9.682|0.000|0.713|0.061|
|Two-Round|0.535|0.712|0.769|0.456|9.701|0.000|0.709|0.059|
|Three-Round|**0.537**|**0.714**|**0.770**|**0.454**|**9.711**|**0.000**|**0.707**|**0.058**|


**Table 4** Evaluation of Implicit/Explicit interface for tracking. 

|Methods|IsaacL|ab||MuJo|Co|
|---|---|---|---|---|---|
|Succ_↑_|_E_mpjpe _↓_|_E_mpkpe|_↓_Succ_↑_|_E_mpjpe _↓_|_E_mpkpe _↓_|
|Ours-Implicit 0.96|0.11|0.09|0.71|0.21|0.20|
|Ours-Explicit 0.91|0.23|0.17|0.62|0.26|0.31|


to directly incorporate motion latents under physical constraints and subsequently execute the action. 

## **5 Conclusions** 

We present an end-to-end framework that bridges text-guided motion generation and humanoid wholebody locomotion with a latent-driven, retarget-free inference pipeline. Central to our approach is PP-Opt, a physics-plausibility optimization module that (i) improves tracker plausibility via physical plausibility objective reward functions and (ii) refines and filters generated motions to fine-tune the motion generator. Experiments show that PP-Opt consistently improves motion generation quality and physical plausibility, and that iterative refinement yields cumulative gains with diminishing returns after a few cycles. Moreover, the implicit latent interface outperforms a conventional explicit retargeting pipeline, reducing tracking errors and improving success rates in both IsaacLab and MuJoCo sim-to-sim evaluation. 

## **References** 

- Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- Xin Chen, Biao Jiang, Wen Liu, Zilong Huang, Bin Fu, Tao Chen, and Gang Yu. Executing your commands via motion diffusion in latent space. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18000–18010, 2023. 

- Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 5152–5161, 2022. 

- Gaoge Han, Mingjiang Liang, Jinglei Tang, Yongkang Cheng, Wei Liu, and Shaoli Huang. Reindiffuse: Crafting physically plausible motions with reinforced diffusion model. In _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , pages 2218–2227. IEEE, 2025. 

- Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024a. 

- Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning human-to-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944– 8951. IEEE, 2024b. 

- Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- Dvij Kalaria, Sudarshan S Harithas, Pushkal Katara, Sangkyung Kwak, Sarthak Bhagat, Shankar Sastry, Srinath Sridhar, Sai Vemprala, Ashish Kapoor, and Jonathan Chung-Kuan Huang. Dreamcontrol: Human-inspired whole-body humanoid control for scene interaction via guided diffusion. _arXiv preprint arXiv:2509.14353_ , 2025. 

- Zhe Li, Yisheng He, Lei Zhong, Weichao Shen, Qi Zuo, Lingteng Qiu, Zilong Dong, Laurence Tianruo Yang, and Weihao Yuan. Mulsmo: Multimodal stylized motion generation by bidirectional control flow. _arXiv preprint arXiv:2412.09901_ , 2024a. 

- Zhe Li, Weihao Yuan, Yisheng He, Lingteng Qiu, Shenhao Zhu, Xiaodong Gu, Weichao Shen, Yuan Dong, Zilong Dong, and Laurence T Yang. Lamp: Language-motion 

8 

pretraining for motion generation, retrieval, and captioning. _arXiv preprint arXiv:2410.07093_ , 2024b. 

- Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Tao Huang, Zhenguo Sun, Yibo Peng, Pengwei Wang, Zhongyuan Wang, Fangzhou Liu, et al. Do you have freestyle? expressive humanoid locomotion via audio control. _arXiv preprint arXiv:2512.23650_ , 2025a. 

- Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, and Chang Xu. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. _arXiv preprint arXiv:2510.14952_ , 2025b. 

- Zhe Li, Cheng Chi, Boan Zhu, Yangyang Wei, Shuanghao Bai, Yuheng Ji, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, et al. Robomirror: Understand before you imitate for video to humanoid locomotion. _arXiv preprint arXiv:2512.23649_ , 2025c. 

- Zhe Li, Weihao Yuan, Weichao Shen, Siyu Zhu, Zilong Dong, and Chang Xu. Omnimotion: Multimodal motion generation with continuous masked autoregression. _arXiv preprint arXiv:2510.14954_ , 2025d. 

- Zhuo Li, Mingshuang Luo, Ruibing Hou, Xin Zhao, Hao Liu, Hong Chang, Zimo Liu, and Chen Li. Morph: A motion-free physics optimization framework for human motion generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14580–14589, 2025e. 

- Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023a. 

- Zhengyi Luo, Jinkun Cao, Josh Merel, Alexander Winkler, Jing Huang, Kris Kitani, and Weipeng Xu. Universal humanoid motion representations for physics-based control. _arXiv preprint arXiv:2310.04582_ , 2023b. 

- Boyu Ma, Zongwu Xie, Zainan Jiang, Yang Liu, Yiming Ji, Baoshi Cao, Zhengpu Wang, and Hong Liu. Robotic redundancy via arm angle self-adaptation through nullspace resolution: Offset poses a challenge. _The International Journal of Robotics Research_ , page 02783649251371735, 2025. 

- Xue Bin Peng. Mimickit: A reinforcement learning framework for motion imitation and control. _arXiv preprint arXiv:2510.13794_ , 2025. 

- Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. 

_ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ , 41(4):1–17, 2022. 

- Mathis Petrovich, Michael J Black, and Gül Varol. Temos: Generating diverse human motions from textual descriptions. In _European conference on computer vision_ , pages 480–497. Springer, 2022. 

- Matthias Plappert, Christian Mandery, and Tamim Asfour. The kit motion-language dataset. _Big data_ , 4(4): 236–252, 2016. 

- Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10684–10695, 2022. 

- Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- Guy Tevet, Brian Gordon, Amir Hertz, Amit H Bermano, and Daniel Cohen-Or. Motionclip: Exposing human motion generation to clip space. In _European Conference on Computer Vision_ , pages 358–374. Springer, 2022a. 

- Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ , 2022b. 

- Yiming Xie, Varun Jampani, Lei Zhong, Deqing Sun, and Huaizu Jiang. Omnicontrol: Control any joint at any time for human motion generation. _arXiv preprint arXiv:2310.08580_ , 2023. 

- Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- Ye Yuan, Jiaming Song, Umar Iqbal, Arash Vahdat, and Jan Kautz. Physdiff: Physics-guided human motion diffusion model. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 16010– 16021, 2023. 

9 

- Mingyuan Zhang, Zhongang Cai, Liang Pan, Fangzhou Hong, Xinying Guo, Lei Yang, and Ziwei Liu. Motiondiffuse: Text-driven human motion generation with diffusion model. _IEEE transactions on pattern analysis and machine intelligence_ , 46(6):4115–4128, 2024. 

10 

