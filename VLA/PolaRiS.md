---
title: "PolaRiS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies"
date: "2025-12-18"
authors: "Arhan Jain; Mingtong Zhang; Kanav Arora; William Chen; Marcel Torne; Muhammad Zubair Irshad"
venue: "RSS 2026"
url: https://arxiv.org/abs/2512.16881
pdf: https://arxiv.org/pdf/2512.16881
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.16881)** / [論文ページ](https://arxiv.org/abs/2512.16881)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Robotics: Science and Systems 2026 Sydney, Australia, July 13–17, 2026** 

# POLARIS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies 

Arhan Jain<sup>_†_</sup> , Mingtong Zhang<sup>_‡_</sup> , Kanav Arora<sup>_†_</sup> , William Chen<sup>_§_</sup> , Marcel Torne<sup>_¶_</sup> , Muhammad Zubair Irshad<sup>_∥_</sup> , Sergey Zakharov<sup>_∥_</sup> , Yue Wang<sup>_∗∗_</sup> , Sergey Levine<sup>_§_,</sup><sup>_‡‡_</sup> , Chelsea Finn<sup>_¶_,</sup><sup>_‡‡_</sup> , Wei-Chiu Ma<sup>_††_</sup> , Dhruv Shah<sup>_‡_</sup> , Abhishek Gupta<sup>_†_,</sup><sup>_∥_</sup> , Karl Pertsch<sup>_§_,</sup><sup>_¶_,</sup><sup>_‡‡_</sup> 

_†_ University of Washington _‡_ Princeton University _§_ UC Berkeley _¶_ Stanford University 

_∥_ Toyota Research Institute _∗∗_ University of Southern California _††_ Cornell University _‡‡_ Physical Intelligence Email: arhanj@cs.washington.edu or alexmzhang@princeton.edu 

polaris-evals.github.io 

**_Abstract_ —A significant challenge for robot learning research is our ability to accurately measure and compare the performance of robot policies. Benchmarking in robotics is historically challenging due to the stochasticity, reproducibility, and timeconsuming nature of real-world rollouts. This challenge is exacerbated for recent generalist policies, which have to be evaluated across a wide variety of scenes and tasks. Evaluation in simulation offers a scalable complement to real world evaluations, but the visual and physical domain gap between existing simulation benchmarks and the real world has made them an unreliable signal for policy improvement. Furthermore, building realistic and diverse simulated environments has traditionally required significant human effort and expertise. To bridge the gap, we introduce Policy Evaluation and Environment Reconstruction in Simulation (POLARIS), a scalable real-to-sim framework for high-fidelity simulated robot evaluation. POLARIS utilizes neural reconstruction methods to turn short video scans of real-world scenes into interactive simulation environments. Additionally, we develop a simple simulation data co-training recipe that bridges remaining real-to-sim gaps and enables zero-shot evaluation in** **_unseen_ simulation environments. Through extensive paired evaluations, across 600 real-world rollouts and over 93,000 simulation rollouts, we demonstrate that POLARIS evaluations provide a much stronger correlation to real world,** **_non-finetuned_ generalist policy ranking than existing simulated benchmarks. Its simplicity also enables rapid creation of diverse simulated environments. As such, this work takes a step towards distributed and democratized evaluation for the next generation of robotic foundation models.** 

## I. INTRODUCTION 

Recently, _generalist robotic policies_ [1, 2, 3, 4, 5, 6, 7, 8], trained on diverse real-robot datasets, have shown an impressive degree of generalization to novel scenarios. However, with the advent of generalist policies comes a critical demand for large-scale empirical validation, since absolute guarantees are challenging to provide. To enable generalization, evaluations must be conducted across a large variety of tasks, environments and rollouts. While performing evaluations directly on real-world robots is the gold standard, this quickly becomes tedious, hard to control systematically, and impractical for individual groups to perform due to cost and labor constraints. 

Arhan Jain and Mingtong Zhang contributed equally. Abhishek Gupta and Karl Pertsch advised equally. 

Therefore, a more scalable paradigm for generalist robot policy evaluation becomes an emerging demand. 

Simulation provides an appealing alternative—cheap, safe, fast, and unburdened by physical hardware, making largescale policy evaluation far more feasible. However, despite considerable efforts [9, 10, 11, 12, 13, 14, 15, 16], these platforms have not been well suited for evaluating the aforementioned _generalist_ policies. To support a wide range of scenarios required to test generality, existing robot-simulation benchmarks typically sacrifice realism—including dynamics, visuals, and scene geometry—and thus fail to capture the visual complexity of the physical world [9, 17, 14, 11, 12]. Our experiments show that there remains a poor correlation between simulation and real world policy performance of state-of-the-art generalist policies. Moreover, as generalist policies get deployed across diverse environments, roboticists are often interested not only in _average_ model performance _across_ environments, but also in understanding a policy’s performance within a _specific target environment_ , which necessitates a tailored simulation of that scene. Constructing such an environment typically requires considerable manual effort. Effective simulated evaluation of generalist policies requires a new set of tools that allow us to rapidly construct high-fidelity targeted simulation environments, reflecting the diversity of real-world environments. 

To this end, we introduce POLARIS, a scalable real-to-sim framework for evaluating generalist robot policies. POLARIS leverages neural reconstruction such as Gaussian splatting [18, 19] and 3D object generation [20] to construct simulated evaluation environments that closely match their real-world counterparts with high visual and geometric fidelity (Figure 1). This enables advanced generalist policies to perform various tasks in POLARIS simulations out of the box. Additionally, our experiments show that lightweight finetuning of these policies with a small dataset of demonstrations in simulation can significantly boost real-to-sim correlation. Importantly, unlike existing simulation benchmarks, this simulation data is primarily used to align visual representations instead of teaching new tasks, and therefore does not have to be collected in the target environment or for the target task. As a result, 


Fig. 1: **Overview of POLARIS.** POLARIS is a real-to-sim approach that turns short videos of real-world scenes into high-fidelity simulated environments for scalable robot policy evaluation. We demonstrate that co-finetuning with simulation data for a small number of iterations enables generalist policies to be evaluated accurately in _unseen_ POLARIS environments _out of the box_ . As part of this work, we provide: (1) **tools** for quickly creating new POLARIS environments, (2) an open-source simulation **dataset** for finetuning generalist policies for POLARIS evaluation, (3) off-the-shelf **evaluation environments** with strong real-to-sim correlation, and (4) a **hub** for sharing new POLARIS environments with the community. 

once finetuned, policies can be evaluated _zero-shot_ in _unseen_ POLARIS environments, facilitating rapid development of simulated evaluations that are customized for individual deployments yet shared broadly to assess generalist competence. 

In our experiments across diverse real-world environments using the DROID platform [21], POLARIS evaluations match the real-world performance of state-of-the-art generalist policies with an average Pearson correlation of _r_ = 0 _._ 83. POLARIS evaluations also strongly correlate ( _r_ = 0 _._ 98) with policy scores in RoboArena [22], the most comprehensive realworld benchmark for generalist robot policies to date. As such, our experiments suggest that POLARIS takes a significant step towards rapid, scalable, simulated evaluation of generalist policies. 

The contributions of this paper are as follows: (1) we introduce POLARIS, a scalable framework for creating highfidelity simulated evaluation environments through neural scene reconstruction, (2) we develop a simple recipe for simulation data co-training that bridges the visual real-to-sim domain gap, ensuring that real-world generalist policies are accurately evaluatable in unseen simulation scenes without domain specific tuning, (3) we perform empirical evaluations across diverse real-world scenes demonstrating strong ranking correlation for widely used generalist policies between POLARIS simulation and the real world non-finetuned policies, (4) we conduct detailed ablations demonstrating key design decisions for faithful simulated evaluation. 

## II. RELATED WORK 

## _A. Robot Policy Evaluation_ 

Accurately evaluating the performance of robot policies is important for guiding research, yet faces challenges in practice: from reproducing initial environment conditions to robot wear and tear, and the tedium of supervising many hours 

of evaluations. Nevertheless, numerous real-robot benchmarks have been proposed over the years [23, 24, 25, 22]. With the rise of increasingly general policies that can perform many tasks across many environments [2, 1, 5, 6, 26], the challenges for performing comprehensive real-world evaluations are exacerbated. _Simulated_ evaluations pose a promising alternative: initial conditions in simulation are perfectly repeatable, simulated robots do not wear out, and evaluations can be rapidly scaled through parallelization. As a result, many simulated robot benchmarks have been proposed [9, 11, 12, 13, 17]. These benchmarks are invaluable for algorithmic development. However, due to large visual and physical domain gaps between these simulated environments and the real world, they struggle to evaluate the performance of _generalist_ policies, trained on real-world data. We instead design simulated environments that are capable of evaluating _real_ -robot, generalist policies. They share the aforementioned benefits of simulated evaluations with respect to usability, reproducibility, and scalability, but are also reflective of the real-world performance of the evaluated generalist policies. More recently, advances in world models have enabled the use of action-conditioned video models as an alternative tool for robot policy evaluation [27, 28, 29, 30]. Like “classic” simulation, video model evaluations can be run at scale. Yet, our experiments demonstrate that today’s (open) models struggle to reliably model physical interactions, and thus struggle to estimate policy performance. In contrast, our method leverages an accurate physics simulator together with high-fidelity neural rendering, making policy evaluation more faithful to realworld dynamics, reliable, efficient, and cost-effective. 

## _B. Real-to-sim Policy Evaluation_ 

A few recent works have recently explored whether increased visual and physical realism can improve the ability of 

simulated environments to be predictive of real-world policy performance: [31, 32] demonstrated that navigation policies can be evaluated in realistic reconstructions of indoor environments, and [33] demonstrated the same for autonomous driving policies. In robot manipulation, where policies closely _interact_ with their environment, the requirements for physical and visual realism of simulated evaluation environments increase: SIMPLER [9] first showed that simulation can be used for evaluation of real-robot manipulation policies, but it fails to deliver strong real-world performance correlation for recent generalist policies [8]. Additionally, the “green-screening” approach used by [9] and follow-up works [34], which copypastes background pixels from real-robot images, does not support evaluation for robot setups with moving cameras. Unfortunately, this excludes most generalist policies [5, 26, 2, 1], which feature moving wrist cameras attached to the robot’s end-effector. Our work uses 3D Gaussian splatting techniques to create high-fidelity simulation environments. The resulting environments show strong real-to-sim performance correlation _and_ support the evaluations of policies with wrist cameras. 

## _C. Real-to-sim Environment Creation_ 

A number of works have developed methods for digitizing real-world environments. Some approaches focus solely on room layout, and fill the scene by sampling from a large 3D object database [35], often lacking in visual realism. For higher visual quality, early approaches relied on specialized and expensive sensory equipment [36, 37], and more recently, learned models have been used to bypass such requirements and instead infer 3D models of environments from raw image or video inputs [38, 32]. In this context, Gaussian splatting has become a popular tool for inferring scene geometry and appearance from raw sensory observations [19, 39, 18, 40]. Multiple works have explored the use of Gaussian splatting techniques in robotics [41, 42, 43, 44, 45, 46, 47]. While these works have shown that splatting can produce environments that can be used for augmenting the training of robot policies, in this work we investigate the utility of real-to-sim techniques in the context of robot policy _evaluation_ . Most closely related to our work, [48, 49] used simulated environments created via Gaussian splatting for policy evaluation, but focused on evaluating narrow, single-task policies in environments seen in the training data. In contrast, comprehensive evaluation of modern _generalist_ policies requires evaluations across a large number of tasks in unseen environments [22]. Our work is the first to develop a pipeline that enables evaluation of realrobot policies in _unseen_ simulated environments, with strong performance correlation to real-world evaluations. 

III. PRELIMINARIES 

## _A. Correlation Metrics_ 

The goal of this work is to evaluate _real-world_ generalist robot policies in _simulated_ environments such that the simulated evaluation faithfully reflects real-world performance. Let Π = _{π_ 1 _, . . . , πN }_ denote a set of policies, each of which can be executed both in the real world and in simulation. Let 

_E_ real denote the real-world environment distribution, and _ES_ denote the corresponding simulated distribution constructed by a generative simulation pipeline _S_ . 

For each policy _πi ∈_ Π, we can define a metric of expected real-world performance (e.g., success rate) as _Ri_ = E _e∼E_ real� _r_ ( _e, πi_ ) �, where _r_ ( _e, πi_ ) denotes the episodic performance when executing policy _πi_ in environment _e_ . Analogously, we define the policy’s performance in simulation as _RS,i_ = E _e∼ES_ � _r_ ( _e, πi_ ) � _._ The goal of simulation-based evaluation is to design simulation environments _ES_ such that the ranking and relative performance of policies in simulation closely approximate their real-world behavior. We follow prior work [9] to quantify the _faithfulness_ of policy evaluation using two metrics. 

**(i) Pearson correlation coefficient (** _r_ **):** This measures the linear correlation between real and simulated performance: 


where _R_<sup>¯</sup> and _R_<sup>¯</sup> _S_ are the mean real and simulated scores. **(ii) Mean Maximum Rank Violation (MMRV):** This captures the severity of rank inversions between real and simulated evaluations. Intuitively, it measures the average worst-case real-world performance gap between any two policies that are mis-ranked under simulation: 


The ideal simulation pipeline _S_ has high Pearson correlation ( _r →_ 1) and a low MMRV ( _→_ 0). This indicates a wellcalibrated simulation, in which relative performance ordering and absolute success trends of real-world policies are faithfully preserved. Note that _Ri_ and _RS,i_ need not be computed with the exact same policy, so long as a fixed mapping determines the simulation policy from the real-world policy. 

## _B. 2D Gaussian Splatting for Scene Reconstruction_ 

To faithfully recover the scene geometry, we resort to recent neural reconstruction tools [19, 18, 50, 51, 39]. To achieve the best trade-off between high visual fidelity and accurate mesh geometry, we leverage 2D Gaussian Splatting (2DGS) [18], which represents a scene as a collection of oriented planar Gaussian disks embedded in 3D space, enabling improved geometric fidelity compared to other representations. A 2D Gaussian splat is represented as a tuple _gj_ = ( **_µ_** _j,_ **R** _j,_ **S** _j,_ **c** _j, αj_ ) _,_ where **_µ_** _j ∈_ R<sup>3</sup> is the disk center, **R** _j ∈_ SO(3) encodes its orientation, **S** _j ∈_ R<sup>3</sup><sup>_×_3</sup> defines its covariance in the disk plane, and ( **c** _j, αj_ ) denote its color and opacity. A full scene is represented as a collection of these Gaussian splats _D_ = _{gj}_<sup>_M_</sup> _j_ =1<sup>,optimizedsothatadifferen-</sup> tiable renderer reproduces the input views on aggregate. Once optimized, the resulting representation supports both realtime photorealistic rendering and accurate mesh extraction, making it well suited for physics-based simulation of robotic 

policies. Additional implementation details are provided in Appendix A. 

## _C. Generalist Robot Policies_ 

While _generalist_ policy is generally an ill-defined term, in this work we specifically use it to refer to a class of language-conditioned multi-task robot policies known as Vision-Language-Action models (VLAs) [5, 2, 1, 26]. VLAs are built on top of transformer based Vision-Language Models (VLMs), fine-tuned to produce robot actions conditioned on visual observations and textual instructions. We denote a generalist policy as _πθ_ : ( _O_ vis _, O_ lang) _→A_ , where _O_ vis is the space of observations, _O_ lang is the space of language instructions, and _A_ is the action space. 

## IV. SCALABLE SIMULATION EVALUATIONS WITH REAL-WORLD VIDEO SCANS 

In this section, we describe POLARIS, our real-to-sim system for scalable creation of high-fidelity simulated environments (Figure 2). We structure our discussion around two components: first, we detail the construction pipeline that transforms a video recording of the real-world scene into an interactive simulation using 2DGS and automatic articulation; second, we address remaining real-to-sim discrepancies by proposing a lightweight simulation data co-training strategy to ensure well-correlated evaluations. Together, these components enable _zero-shot_ evaluation of real-world generalist policies in previously unseen simulation environments. 

## _A. Environment Generation with_ POLARIS 

To create an environment with POLARIS, we take a compositional approach. We first construct the visuals and geometry of the environments, then construct the visuals, geometry, and articulation of the robot, and finally add object assets into the scene. We outline these steps below: 

**Environment Creation via Reconstruction:** We start by capturing a short (2–5 minutes) monocular video recording of the scene. We then run a reconstruction pipeline based on 2DGS [18] to reconstruct scene visuals and geometry. To facilitate compositional scene construction, we record separate video sequences for (i) the static background scene and (ii) the robot. To assist in automatically resolving global orientation and metric scale, a ChArUco board is placed in the environment (see Figure 2). This data acquisition process for a scene typically requires only 5–10 minutes. Following data capture, we run COLMAP [52] to obtain a sparse reconstruction and train a 2D Gaussian Splatting model _D_ = _{gj}_<sup>_M_</sup> _j_ =1<sup>;</sup><sup>_gj_=</sup> ( **_µ_** _j,_ **R** _j,_ **S** _j,_ **c** _j, αj_ ) for each recording by optimizing a standard photometric reconstruction loss as described in Appendix A. 

To enable closed-loop robotic evaluation in a physics-based simulator, we require the geometric and photometric components of the reconstructed scene. We obtain a Truncated Signed Distance Field (TSDF) using a combination of rasterizing the splats and volumetric depth fusion [53]. An explicit mesh representation _M_ is then extracted from the TSDF using 

marching cubes [54]. The resulting meshes are imported into IsaacSim [55] to enable realistic contact dynamics and object interactions, while the underlying Gaussian splats _D_ provides the corresponding photometric renders for high-fidelity visual effects. Please refer to Appendix B and C for implementation details. 

**Automatic Articulation:** While the environment remains static, the robot mesh and the corresponding Gaussian splats must be _articulated_ for interactive evaluation. To enable this, we anchor subsets of Gaussian splat primitives to the robot’s kinematic links, allowing them to move according to the robot’s joint configuration. Let the robot have links _{L_ 1 _, . . . , LL}_ with joint configuration **q** _∈_ R<sup>_d_</sup> . Each link _Lℓ_ is associated with a set of Gaussian primitives _Gℓ_ = _{gℓj}_<sup>_M_</sup> _j_ =1<sup>_ℓ_</sup> and a rigid-body transform _Tℓ_ ( **q** ) = [ _Rℓ_ ( **q** ) _|_ **t** _ℓ_ ( **q** )] _∈_ SE(3) obtained via forward kinematics. For a configuration **q** , the position and covariance of each Gaussian is updated with the corresponding transform: **_µ_**<sup>_′_</sup> _ℓj_<sup>=</sup><sup>_Rℓ_(</sup><sup>**q**)</sup><sup>**_µ_**</sup><sup>_ℓj_+</sup><sup>**t**</sup><sup>_ℓ_(</sup><sup>**q**)</sup><sup>_,_</sup> Σ<sup>_′_</sup> _ℓj_<sup>=</sup><sup>_Rℓ_(</sup><sup>**q**) Σ</sup><sup>_ℓj Rℓ_(</sup><sup>**q**)</sup><sup>_⊤._Thearticulatedrobotsplatisthen</sup> given by _G_ ( **q** ) =<sup>�</sup><sup>_L_</sup> _ℓ_ =1<sup>_{_(</sup><sup>**_µ_**</sup><sup>_′_</sup> _ℓj_<sup>_,_Σ</sup><sup>_′_</sup> _ℓj_<sup>_,_</sup><sup>**c**</sup><sup>_ℓj, αℓj_)</sup><sup>_}_</sup> _j_<sup>_M_</sup> =1<sup>_ℓ_,whichcan</sup> be rendered using the standard differentiable 2DGS pipeline. This enables interactive, photorealistic robots whose Gaussian splat components follow the true physical kinematics of the underlying mesh model. This allows the evaluation to be fully interactive in closed loop, while retaining the visual realism of Gaussian splatting. The fully scanned and articulated robot model can be reused across simulation environments, making this a one-time process per robot system. 

**Object Creation with Generative Models:** We find that directly extracting high-quality, watertight assets from real-world video is a time-consuming and tedious process. Although POLARIS is not tied to any specific object reconstruction methods, we employ the TRELLIS image-to-3D generative model [20] for simplicity and flexibility. TRELLIS introduces a structured representation that enables mapping from a single or a few multiview 2D images to diverse 3D representations (such as Gaussian splats, radiance fields, and meshes) with high fidelity, while recovering unobservable object regions. With multiview images captured with a standard camera as inputs, we feed the segmented views into TRELLIS to obtain a structured latent representation. This latent is decoded into a Gaussian splat for appearance and an untextured mesh for geometry, after which appearance is baked onto the mesh to produce a fully textured object for simulation. 

**Composing simulated evaluation scenes.** The final step is to assemble these components into an interactive evaluation scene. Since all components are represented as Gaussian primitives or textured meshes, the environment, robot and objects can be composed and transformed in Euclidean space. Moreover, we set standard physics parameters for contact dynamics using default values from IsaacSim, and use manufacturerprovided defaults for the robot arm. Object mass parameters are automatically approximated using a default density, or optionally hand-specified by user. Alongside scene composition, the user also defines a success criterion for scoring evaluation 


Fig. 2: **Environment creation in POLARIS.** A user first scans in a real-world environment, robot and objects. They then use POLARIS to create articulated Gaussian splat representations of the real-world environment that capture geometry and visual appearance of the environment. Finally, they compose the evaluation scene by combining scanned-in scene, objects and robot to use for policy evaluation. 

rollouts – e.g., whether a particular object is placed within a certain receptacle. 

The total human effort required for creating a new evaluation environment is typically **less than 20 minutes** , and the total wall time for creating a new evaluation environment, including training time of the Gaussian splats, is typically **less than one hour** . This is more scalable than prior simulated evaluation works [9], which require hand-defined construction of the environment geometry and extensive tuning of lighting and textures. 

An important facet of the constructed simulation is the ability to provide policies with rich sensor inputs. As opposed to prior work [9, 34] which copied image backgrounds in 2D via green-screen, POLARIS reconstructs the entire scene in 3D, providing full 3D rendering and novel view synthesis. This allows us to easily render third person views from any angle and provide wrist camera inputs to the policy. This opens up a new class of simulation evaluations for generalist policies that prior real-to-sim evaluation frameworks that rely on background inpainting [9, 34] were unable to support. 

## _B. Enabling High Correlation Policy Evaluation with_ POLARIS _using Co-Training_ 

While the pipeline outlined above allows for the creation of high-fidelity environments, our empirical validation in Section V shows that the resulting environments do not reliably lead to high real-to-sim correlation out-of-the-box. We hypothesize that this mainly stems from subtle domain gaps between the real world and simulation, such as minor lighting variations, artifacts of splats, or missing inter-object shadows. Although these differences may appear negligible to human observers, they make a considerable difference in policy performance. To better understand this effect, we conducted hardware-in-the-loop experiments which isolated distribution shifts of visuals and dynamics and suggested that visual mismatch is the dominant source of error (see Appendix G for details). To mitigate these gaps and improve real-to-sim 


Fig. 3: **POLARIS simulated co-training dataset environments.** We collect a small number of demonstrations in simulation and co-finetune policies with this data for improved real-to-sim evaluation correlation. Importantly, once finetuned, policies evaluated in POLARIS show strong real-to-sim correlation, even in _unseen_ environments. New simulated evaluation environments are easily added without needing to collect additional demonstrations. 

correlation, we propose a simple, policy-agnostic simulation data co-training scheme. 

Concretely, we collect a small simulation dataset via human teleoperation: _DS_ = _{_ ( _o_<sup>_S_</sup> _t_<sup>_, aS_</sup> _t_<sup>_, pS_</sup> _t_<sup>)</sup><sup>_}M_</sup> _t_ =1<sup>_,_consistingofsimu-</sup> lated visual observations and language instructions _o_<sup>_S_</sup> _t_<sup>,expert</sup> actions _a_<sup>_S_</sup> _t_<sup>,andproprioceptivestates</sup><sup>_pS_</sup> _t_<sup>,gatheredoveraset</sup> of simulated co-training environments _ES_<sup>train</sup> _⊂ES_ . Given a pretrained generalist policy _πθ_ with original training data _D_ pre, we update the policy parameters via _co-training_ by sampling batches that mix simulation data with the original pretraining data: 


where _L_ BC is a standard behavior cloning objective and _λ ∈_ [0 _,_ 1] controls the ratio of simulation to pretraining samples in each batch (in practice we use _λ_ = 0 _._ 1). Intuitively, co-training with simulation data improves the policy’s robustness to subtle visual gaps between simulation and the real world, leading to more reliable policy evaluation in simulation. In practice, we find that only a few hundred simulated episodes and a few hundred fine-tuning steps are sufficient to substantially improve real-to-sim correlation, typically completed in _<_ 25 mins. This 


Fig. 4: **Evaluation environments. Top** : real-world environments, **Bottom** : POLARIS simulated evaluation replicas. We create high visual fidelity environments utilizing Gaussian Splats for environment reconstruction and TRELLIS for object asset generation. 

is orders of magnitude less data and compute than what is used during generalist pretraining. Importantly, because simulation co-training aims to refine visual representations instead of acquire new task-specific skills, the simulated demonstrations _are not required_ to be collected in the target simulation environment(s) or task(s) _ES_<sup>test.Instead,theycanbecollected</sup> a priori, on a completely separate set of environments and tasks - in our experiments co-training environments ( _ES_<sup>train</sup> ) and evaluation environments ( _ES_<sup>test)aredisjoint.Asaresult,</sup> the co-trained policies can be evaluated _zero-shot_ in unseen simulation environments. 

## V. EXPERIMENTS 

Our experimental analysis aims to answer the following questions: (1) Does POLARIS enable zero-shot evaluation in _unseen_ simulation environments with strong correlation to real-world non-finetuned policy performance? (2) Which design decisions affect zero-shot real-to-sim correlation? (3) Does POLARIS provide stronger real-to-sim evaluation correlation than current simulated evaluation tools in robotics? 

## _A. Experimental Setup_ 

**Robot platform.** We perform our experiments using the DROID [21] platform–one of the most widely used robot platforms for generalist policies [56, 2, 22]–which consists of a 7-DoF Franka Panda robot arm, and a set of two ZED RGB cameras with one mounted to the robot’s wrist. While DROID offers both joint velocity and joint position action spaces, we focus on evaluating policies using joint _position_ actions, which we found easier to simulate accurately since they suffer from less accumulating error. 

**Policies.** We use a representative set of DROID VLAs from prior works for testing the efficacy of POLARIS as an evaluation tool: (1) **PaliGemma-binning** , an auto-regressive VLA with binning action tokenization from [56], (2) **_π_ 0** [1], a diffusion-based VLA, (3) **_π_ 0-100k** [1], an early checkpoint of **_π_ 0** , (4) **_π_ 0-FAST** [56], an auto-regressive VLA with the FAST action tokenizer, and (5) **_π_ 0** **_._ 5** [2], the current state-ofthe-art VLA on DROID [22]. 

**Tasks.** To enable precise evaluation of real-to-sim correlations, we set up 6 _paired_ real-world and simulated environments across multiple institutions (showcased in Figure 4). The environments span diverse visual scenes and a representative 

sample of rigid object manipulation tasks. We also create an additional 15 real-to-sim scenes through our pipeline, which we use to collect a dataset of around 350 simulation demonstrations for co-training (Section IV-B). We ensure that these “co-training environments” are _completely separate from our evaluation environments and tasks_ and none of the scenes or objects are shared. 

**POLARIS evaluation procedure.** We finetune all policies for 1k steps on the co-training dataset using supervised learning, then run 50 rollouts per task in simulation to compute the policy’s performance. Each task is automatically scored on a progress scale from [0 _. . ._ 1]. Scoring follows a convention of points awarded for reaching, lifting, and placing object(s) in their goal positions, normalized by the maximum possible score per task. We find POLARIS to be robust to different scoring criteria (Appendix H). For details on all tasks, progress scales, and hyperparameters, please see Appendix Tables I, II, III. 

**Comparisons.** We compare our real-to-sim evaluation approach to existing methods used for offline policy evaluation: **MSE** , which computes training / validation set action MSE for each policy; **Libero-Score** , which evaluates policies on the Libero simulation benchmark [11] that is often used in VLA benchmarking [57, 58, 8, 59]; and **Video model evaluation** , which rolls out policies in the open-source **Ctrl-World** [29] video model and uses humans to score the rollouts. For Libero, to get the highest-quality evaluations possible, we finetune all policies on Libero-90, the largest of the Libero datasets, for 50k steps and evaluate on all 90 tasks, running 50 rollouts per task or a total of 4,500 evaluations per policy. Notably, this is a more thorough evaluation than done by most existing VLA papers using Libero, which typically evaluate on much smaller Libero splits [57, 58, 8]. Additionally, we evaluate multiple Libero-finetuned checkpoints (1k, 10k, 50k) and report results for the best-correlated checkpoint in Figure 5. As a result, the Libero-Score approach uses approximately 10x more finetuning and evaluation compute than our simulated evaluation approach. We note that existing real-to-sim evaluation approaches [9, 34], including SIMPLER, do not support evaluation of policies with wrist cameras, and thus cannot even be used to evaluate most state of the art VLA models. 

**Metrics.** For each environment we run 20 real-world evaluation rollouts for each policy, without any finetuning, to establish a ground-truth ranking of policy performance. Real rollouts are scored by humans using the same progress scoring used in simulation, described in Appendix Table I. As described in Section III, we report Pearson correlation _r_ and MMRV between the real-world and simulation performance. Due to finite rollouts per policy, we report bootstrap confidence intervals for all correlation metrics by randomly sampling 50 episodes with replacement from our real-world and simulated evaluations, average performance per policy, then compute Pearson correlation and MMRV. We repeat this process 500 times and report the 95% confidence interval. 


Fig. 5: **Correlation of Evaluations between Real and Sim:** POLARIS achieves strong real-to-sim correlation in _unseen_ environments. Importantly, although the points don’t fall exactly on the ideal line, the simulation is able to fairly accurately rank policies with respect to their real world scores. 

## _B. Real-to-Sim Correlation in Unseen Environments_ 

We report real-world correlation results for all tested approaches in Figure 5 and Figure 6. In line with existing literature [9], we find that MSE is a poor metric for realworld policy performance and shows low correlation. Liberoscore too is poorly correlated with real-world performance, with nearly all tested policies scoring between 90 and 95% success in Libero, but spanning the full spectrum from highperforming to low-performing policies in the real world. Finally, we find that today’s open-source video models are not yet reliable enough for policy evaluation in diverse scenes: in our experiments, Ctrl-World often produces heavy hallucinations during object interaction, making accurate scoring challenging and ultimately leading to clear policy misrankings (MMRV: 0.23). While recent works have shown promising video model evaluation results in narrower scene settings [29, 30], our experiments suggest that more advances are needed for these models to be widely applicable tools for robot policy evaluation in diverse real-world tasks. 

In contrast, POLARIS achieves strong correlation results across all environments: in our experiments, differences in POLARIS scores closely reflect real-world performance differences, and rank the performance of policies accurately. Importantly, this result does not only hold in terms of _average_ performance, but holds _for each individual environment_ : the _worst-case_ correlation across all six tested environments is _r_ = 0 _._ 81 (without bootstrapping). See individual environment results in Appendix Figure 14. In contrast to hand-designed sim benchmarks, POLARIS’s pipeline can be used to estimate both: average performance of generalist policies and performance in specific deployment scenarios. 

Furthermore, we find that POLARIS scores exhibit strong correlation to RoboArena [22] real-world evaluation scores (see Figure 11). We report correlation to the average progress scores reported as part of the RoboArena evaluations. While 


Fig. 6: **Comparison of Evaluation Metrics:** We compare Pearson correlation coefficient and Mean Maximum Rank Violation (MMRV). We show the spread of correlations across environments, and estimate uncertainty in correlation metrics via bootstrap resampling over rollout trajectories. 

we find that scores correlate well, we emphasize that the simulated evaluations in our experiments only capture a small subset of the capabilities tested in RoboArena—particularly those involving non-rigid body dynamics, soft-body interactions, and complex contact behaviors remain challenging for current simulators. Thus, we believe that POLARIS can serve as a useful tool for cheaply and rapidly estimating VLA performance during research and development, but _does not_ entirely replace real-world evaluation. 

## _C. Ablation Studies and Analysis_ 

In this section, we investigate the importance of different components of our POLARIS framework. 

**Visual fidelity.** To ablate the impact of the visual fidelity of simulated environments on real-to-sim correlation, we create versions of our simulated evaluation scenes with different levels of visual quality (see Appendix Table V), using ray-tracing instead of Gaussian splatting, and removing background and foreground textures. We report real-to-sim correlation after co-training all policies with the respective simulated dataset in Figure 7, left. First, we find that after cotraining, all simulation variants can provide decently correlated results, suggesting that the simulation data co-training can alleviate some visual sensitivity observed in prior works [9]. Yet, we find that POLARIS with Gaussian splatting rendering leads to the strongest correlation. While these results suggest visual fidelity is not the _sole_ driver of high-quality simulated evaluations, the comparison to Libero-Score (Section V-B) underlines the benefit of real-to-sim evaluation techniques compared to hand-crafting low-fidelity simulated benchmarks: real-to-sim evaluation scans _real-world_ environments and thus allows evaluation in environments that are closer to the training distribution. 

**Co-training dataset.** We evaluate the impact of different simulation co-training data mixtures. In our original experiments, we collected data in 15 held-out simulation environ- 


Fig. 7: **Visual fidelity ablation:** High-fidelity Fig. 8: **Co-training dataset ablation:** Simularendering is key for strong real-to-sim correlation: tion data co-training is key for strong real-to-sim evaluations with texture-less simulation environevaluation correlation, but importantly, once coments or raytraced rendering underperform Gaustrained with our simulated demonstration dataset, sian splatting based rendering evaluations, even POLARIS provides strong correlation even for after simulation data co-training. unseen (“OOD”) simulation environments. 


Fig. 9: **Finetuning steps ablation:** Real-to-sim correlation across five finetuning seeds. POLARIS reliably achieves strong real-to-sim correlation after just a few hundred steps of simulation data co-finetuning. Finetuning policies for too long reduces real-to-sim correlation. 


Fig. 10: **Correlation with RoboArena [22]:** POLARIS evaluations show strong performance correlation with RoboArena [22] rankings. Although the POLARIS captures a small subset of the tasks from RoboArena (limited to rigid-body), this result signals POLARIS also being a useful tool for aggregated policy ranking. We exclude _π_ 0 _−_ 100k as there are no evaluations of the policy in RoboArena. 

ments. For this experiment, we additionally collect data in the 3 target environments, on both, the target tasks and non-target tasks. We then compare 3 settings: ” **OOD** ” uses only data from the 15 held-out environments (the setting from the previous sections); ” **Near Domain** ” additionally uses data from _nontarget tasks_ , collected in the _target environments_ ; ” **In Domain** ” combines the data from the held-out environments with data collected on the _target tasks_ in the _target environments_ . We also compare to directly evaluating the pre-trained checkpoints without any simulation data co-training (“ **Zeroshot** ”) (see Appendix Table IV for data mix details. We report real-tosim correlation across 5 seeds in Figure 8. First, we find that the base VLA models (“Zeroshot”) achieve non-trivial performance, but correlation is too low to accurately rank policy performance, underlining the importance of simulation co-training. Comparing the different simulation data mixes, we find that the “OOD” data mix (ours) leads to approximately comparable correlations to in-domain data. This underlines that the function of the simulation data is primarily to bridge subtle visual gaps between simulation and real-world environments, for which OOD scenes are sufficient. Notably, this result makes POLARIS evaluations scalable: we can add new 


Fig. 11: POLARIS retains strong real-to-sim evaluation correlation even under randomization of key physics parameters (object mass, friction, and controller gains). Run over 100 evaluations per policy-task pair. 

evaluation environments _without_ collecting targeted simulation data and _without_ needing to finetune generalist policies for every new scenario. Such ”out of the box” evaluation in unseen simulation environments makes sharing and accumulating of targeted simulated evaluations across the community feasible, like it is common-place e.g. for LLM research today. Lastly, we find that “Near Domain” data leads to slightly stronger correlations than target task demonstrations, possibly because the latter lead to quick overfitting. 

**Fine-tuning steps.** We evaluate the robustness of our pipeline to different number of finetuning steps. Concretely, we run five finetuning runs for all policies, training for 10k steps each. We then evaluate the mean and variance of Pearson correlation and MMRV across all checkpoints (see Figure 9). Our experiments suggest that 1k steps of co-finetuning consistently lead to strong real-to-sim correlation, but even just a few hundred steps of finetuning can significantly improve correlation results. Figure 9 shows that too much finetuning can lead to overfitting and worsen correlation. 

**Robustness to Physics Parameters** We evaluate the robustness of POLARIS to significant variation in physical system parameters. To show this, we randomize key physics parameters of our simulation around the base values we obtained 

via system identification on the real-world system: _±_ 10% for controller gains, _±_ 20% for object friction and mass. We report results in Figure 11. Even with significantly noised physics parameters, POLARIS produces strongly correlated evaluation results with _r ≥_ 0 _._ 76. As expected, the performance of _all_ policies decreases as a result of the randomized physics parameters, but importantly, POLARIS evaluations still correctly reflect the _relative_ performance of all policies. This suggests that POLARIS’s utility as a proxy for real-world evaluations is _robust_ to system identification noise. We also note that precise modeling of the _absolute_ performance of policies in simulation, while outside the scope of our work, may benefit from orthogonal improvements to system identification. 

## VI. CONCLUSION 

In this work, we introduce POLARIS, a system for developing scalable evaluation benchmarks in simulation from realworld videos. POLARIS allows for personalized environment creation in simulation, corresponding to particular real-world environments. With a small amount of policy co-training on simulation data, these simulated environments can be made directly usable for policy evaluation. We perform a thorough empirical investigation, demonstrating strong correlation between simulated and real evaluations, out of the box even in unseen simulation environments. These simulation environments can serve as a useful tool for scalable evaluations of generalist policies. As advances are made in the field of 3D reconstruction and generation, the POLARIS framework will benefit from higher fidelity environments and greater ease of use. 

While a promising step for policy evaluation, there are still several points of improvement for POLARIS. Although policy ranking is well correlated, there is lots of room for improvement in matching absolute policy performance between simulation and the real world. Additionally, some policies transfer better to these real-to-sim environments than others – the Paligemma policy has low transfer to sim compared to others, as shown in Figure 5. Our hypothesis is that this is due to the lack of robot data pretraining when initializing from Paligemma, but more detailed experiments and analysis remain to truly understand what makes VLAs robust to visual transfer. Going beyond Gaussian splat rendering to richer diffusion based renderings can further bridge the real-tosim visual gaps. Moreover, POLARIS performs a relatively simplistic identification of system dynamics. We can draw on a rich literature of system identification [60] to better identify the robot and environment dynamics. Lastly, we can consider hybrid simulation techniques, merging elements of world modeling with physics-based simulation to generate more scalable simulated evaluations, including more complex objects and scene configurations. 

## ACKNOWLEDGMENTS 

This research was partially support by Amazon Science Hub, Army Research Lab, the DARPA TIAMAT Program, and the Toyota Research Institute University 2.0 Program, with 

compute support from Microsoft. The authors would like to thank Alex Fang, Ludwig Schmidt, Masha Itkina, Junjie Ye, Jiawei Yang for the early discussion on the project, Mateo Guaman Castro for help and feedback on figures and presentation, and Apurva Badithela and Lihan Zha for feedback on an earlier draft of this paper. We also thank Aditya Shah and Daniel Gorbatov for helping with evaluations, and Jenai (Xuning) Yang for advice and support with simulation. 

## REFERENCES 

- [1] Physical Intelligence. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL https://arxiv. org/abs/2410.24164. 

- [2] Physical Intelligence. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL https://arxiv.org/abs/2504.16054. 

- [3] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 

- [4] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [5] Gemini Robotics Team. Gemini robotics 1.5: Pushing the frontier of generalist robots with advanced embodied reasoning, thinking, and motion transfer, 2025. URL https://arxiv.org/abs/2510.03342. 

- [6] TRI LBM Team. A careful examination of large behavior models for multitask dexterous manipulation. _arXiv preprint_ , 2025. URL https://arxiv.org/abs/2507.05331. 

- [7] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [8] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [9] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Oier Mees, Karl Pertsch, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in sim- 

ulation. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 3705– 3728. PMLR, 2024. URL https://proceedings.mlr.press/ v270/li25c.html. 

- [10] Pushkal Katara, Zhou Xian, and Katerina Fragkiadaki. Gen2sim: Scaling up robot learning in simulation with generative models. In _IEEE International Conference on Robotics and Automation, ICRA 2024, Yokohama, Japan, May 13-17, 2024_ , pages 6672–6679. IEEE, 2024. doi: 10. 1109/ICRA57147.2024.10610566. URL https://doi.org/ 10.1109/ICRA57147.2024.10610566. 

- [11] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: benchmarking knowledge transfer for lifelong robot learning. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. URL http://papers.nips.cc/paper <u>files/paper/2023/hash/</u> 8c3c666820ea055a77726d66fc7d447f-Abstract-Datasets and <u>Benchmarks.html.</u> 

- [12] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _CoRR_ , abs/2406.02523, 2024. doi: 10.48550/ARXIV.2406. 02523. URL https://doi.org/10.48550/arXiv.2406.02523. 

- [13] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics Autom. Lett._ , 5(2):3019–3026, 2020. doi: 10.1109/LRA. 2020.2974707. URL https://doi.org/10.1109/LRA.2020. 2974707. 

- [14] Oier Mees, Luk´as Hermann, Erick Rosete-Beas, and Wolfram Burgard. CALVIN: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics Autom. Lett._ , 7(3):7327– 7334, 2022. doi: 10.1109/LRA.2022.3180108. URL https://doi.org/10.1109/LRA.2022.3180108. 

- [15] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Metaworld: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 

- [16] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Mart´ın-Mart´ın, Chen Wang, Gabrael Levine, Wensi Ai, Benjamin Martinez, et al. Behavior-1k: A human-centered, embodied ai benchmark with 1,000 everyday activities and realistic simulation. _arXiv preprint arXiv:2403.09227_ , 2024. 

- [17] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta- 

world: A benchmark and evaluation for multi-task and meta reinforcement learning. In Leslie Pack Kaelbling, Danica Kragic, and Komei Sugiura, editors, _3rd Annual Conference on Robot Learning, CoRL 2019, Osaka, Japan, October 30 - November 1, 2019, Proceedings_ , volume 100 of _Proceedings of Machine Learning Research_ , pages 1094–1100. PMLR, 2019. URL http: //proceedings.mlr.press/v100/yu20a.html. 

- [18] Binbin Huang, Zehao Yu, Anpei Chen, Andreas Geiger, and Shenghua Gao. 2d gaussian splatting for geometrically accurate radiance fields. In _Proceedings of the 2024 ACM SIGGRAPH Conference on Computer Graphics and Interactive Techniques_ . Association for Computing Machinery, 2024. doi: 10.1145/3641519.3657428. URL https://dl.acm.org/doi/10.1145/3641519.3657428. 

- [19] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for realtime radiance field rendering. In _ACM SIGGRAPH 2023 Conference Proceedings_ . Association for Computing Machinery, 2023. doi: 10.1145/3592433. URL https://dl.acm.org/doi/10.1145/3592433. 

- [20] Jianfeng Xiang, Zelong Lv, Sicheng Xu, Yu Deng, Ruicheng Wang, Bowen Zhang, Dong Chen, Xin Tong, and Jiaolong Yang. Structured 3d latents for scalable and versatile 3d generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 21469–21480, 2025. 

- [21] DROID Team. DROID: A large-scale in-the-wild robot manipulation dataset. In _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. doi: 10.15607/RSS.2024.XX.120. URL https://doi.org/ 10.15607/RSS.2024.XX.120. 

- [22] Pranav Atreya, Karl Pertsch, Tony Lee, Moo Jin Kim, Arhan Jain, Artur Kuramshin, Clemens Eppner, Cyrus Neary, Edward Hu, Fabio Ramos, et al. Roboarena: Distributed real-world evaluation of generalist robot policies. In _Proceedings of the Conference on Robot Learning (CoRL 2025)_ , 2025. 

- [23] Berk C¸ alli, Aaron Walsman, Arjun Singh, Siddhartha S. Srinivasa, Pieter Abbeel, and Aaron M. Dollar. Benchmarking in manipulation research: The YCB object and model set and benchmarking protocols. _CoRR_ , abs/1502.03143, 2015. URL http://arxiv.org/abs/1502. 03143. 

- [24] Michael Ahn, Henry Zhu, Kristian Hartikainen, Hugo Ponte, Abhishek Gupta, Sergey Levine, and Vikash Kumar. ROBEL: robotics benchmarks for learning with lowcost robots. In Leslie Pack Kaelbling, Danica Kragic, and Komei Sugiura, editors, _3rd Annual Conference on Robot Learning, CoRL 2019, Osaka, Japan, October 30 - November 1, 2019, Proceedings_ , volume 100 of _Proceedings of Machine Learning Research_ , pages 1300– 1313. PMLR, 2019. URL http://proceedings.mlr.press/ v100/ahn20a.html. 

- [25] Zhiyuan Zhou, Pranav Atreya, You Liang Tan, Karl Pertsch, and Sergey Levine. Autoeval: Autonomous 

evaluation of generalist robot manipulation policies in the real world. _CoRR_ , abs/2503.24278, 2025. doi: 10.48550/ARXIV.2503.24278. URL https://doi.org/10. 48550/arXiv.2503.24278. 

- [26] NVIDIA. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL https://arxiv.org/ abs/2503.14734. 

- [27] Julian Quevedo, Percy Liang, and Sherry Yang. Evaluating robot policies in a world model. _arXiv preprint arXiv:2506.00613_ , 2025. 

- [28] Wei-Cheng Tseng, Jinwei Gu, Qinsheng Zhang, Hanzi Mao, Ming-Yu Liu, Florian Shkurti, and Lin Yen-Chen. Scalable policy evaluation with video world models. _arXiv preprint arXiv:2511.11520_ , 2025. 

- [29] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 

- [30] Gemini Robotics Team, Coline Devin, Yilun Du, Debidatta Dwibedi, Ruiqi Gao, Abhishek Jindal, Thomas Kipf, Sean Kirmani, Fangchen Liu, Anirudha Majumdar, Andrew Marmon, Carolina Parada, Yulia Rubanova, Dhruv Shah, Vikas Sindhwani, Jie Tan, Fei Xia, Ted Xiao, Sherry Yang, Wenhao Yu, and Allan Zhou. Evaluating gemini robotics policies in a veo world simulator, 2025. URL https://arxiv.org/abs/2512.10675. 

- [31] Gunjan Chhablani, Xiaomeng Ye, Muhammad Zubair Irshad, and Zsolt Kira. Embodiedsplat: Personalized realto-sim-to-real navigation with gaussian splats from a mobile device, 2025. URL https://arxiv.org/abs/2509.17430. 

- [32] Alejandro Escontrela, Justin Kerr, Arthur Allshire, Jonas Frey, Rocky Duan, Carmelo Sferrazza, and Pieter Abbeel. Gaussgym: An open-source real-to-sim framework for learning locomotion from pixels, 2025. URL https: //arxiv.org/abs/2510.15352. 

- [33] Ze Yang, Yun Chen, Jingkang Wang, Sivabalan Manivasagam, Wei-Chiu Ma, Anqi Joyce Yang, and Raquel Urtasun. Unisim: A neural closed-loop sensor simulator. _arXiv preprint arXiv:2308.01898_ , 2023. 

- [34] Yash Jangir, Yidi Zhang, Kashu Yamazaki, Chenyu Zhang, Kuan-Hsun Tu, Tsung-Wei Ke, Lei Ke, Yonatan Bisk, and Katerina Fragkiadaki. Robotarena _∞_ : Scalable robot benchmarking via real-to-sim translation, 2025. URL https://arxiv.org/abs/2510.23571. 

- [35] Matt Deitke, Rose Hendrix, Luca Weihs, Ali Farhadi, Kiana Ehsani, and Aniruddha Kembhavi. Phone2proc: Bringing robust robots into our chaotic world. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- [36] Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, and Vladlen Koltun. Habitat: A platform for embodied ai research. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2019. 

- [37] Fei Xia, Amir R Zamir, Zhiyang He, Alexander Sax, 

Jitendra Malik, and Silvio Savarese. Gibson env: Realworld perception for embodied agents. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 9068–9079, 2018. 

- [38] Marcel Torne, Anthony Simeonov, Zechu Li, April Chan, Tao Chen, Abhishek Gupta, and Pulkit Agrawal. Reconciling reality through simulation: A real-to-sim-to-real approach for robust manipulation. _Arxiv_ , 2024. 

- [39] Guikun Chen and Wenguan Wang. A survey on 3d gaussian splatting, 2025. URL https://arxiv.org/abs/2401. 03890. 

- [40] Muhammad Zubair Irshad, Mauro Comi, Yen-Chen Lin, Nick Heppert, Abhinav Valada, Rares Ambrus, Zsolt Kira, and Jonathan Tremblay. Neural fields in robotics: A survey. _arXiv preprint arXiv:2410.20220_ , 2024. 

- [41] Hongchi Xia, Entong Su, Marius Memmel, Arhan Jain, Raymond Yu, Numfor Mbiziwo-Tiapo, Ali Farhadi, Abhishek Gupta, Shenlong Wang, and Wei-Chiu Ma. Drawer: Digital reconstruction and articulation with environment realism, 2025. URL https://arxiv.org/abs/2504. 15278. 

- [42] Justin Yu, Kush Hari, Karim El-Refai, Arnav Dalil, Justin Kerr, Chung-Min Kim, Richard Cheng, Muhammad Z. Irshad, and Ken Goldberg. Persistent object gaussian splat (pogs) for tracking human and robot manipulation of irregularly shaped objects. _ICRA_ , 2025. 

- [43] Jad Abou-Chakra, Lingfeng Sun, Krishan Rana, Brandon B. May, Karl Schmeckpeper, Maria Vittoria Minniti, and Laura Herlant. Real-is-sim: Bridging the sim-to-real gap with a dynamic digital twin for real-world robot policy evaluation. _CoRR_ , abs/2504.03597, 2025. doi: 10.48550/ARXIV.2504.03597. URL https://doi.org/10. 48550/arXiv.2504.03597. 

- [44] Justin Yu, Kush Hari, Kishore Srinivas, Karim El-Refai, Adam Rashid, Chung Min Kim, Justin Kerr, Richard Cheng, Muhammad Zubair Irshad, Ashwin Balakrishna, et al. Language-embedded gaussian splats (legs): Incrementally building room-scale representations with a mobile robot. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 13326– 13332. IEEE, 2024. 

- [45] Mohammad Nomaan Qureshi, Sparsh Garg, Francisco Yand´un, David Held, George Kantor, and Abhisesh Silwal. Splatsim: Zero-shot sim2real transfer of RGB manipulation policies using gaussian splatting. In _IEEE International Conference on Robotics and Automation, ICRA 2025, Atlanta, GA, USA, May 19-23, 2025_ , pages 6502–6509. IEEE, 2025. doi: 10.1109/ICRA55743.2025. 11128339. URL https://doi.org/10.1109/ICRA55743. 2025.11128339. 

- [46] Prithwish Dan, Kushal Kedia, Angela Chao, Edward Weiyi Duan, Maximus Adrian Pace, Wei-Chiu Ma, and Sanjiban Choudhury. X-sim: Cross-embodiment learning via real-to-sim-to-real. _CoRR_ , abs/2505.07096, 2025. doi: 10.48550/ARXIV.2505.07096. URL https: //doi.org/10.48550/arXiv.2505.07096. 

- [47] Justin Yu, Letian Fu, Huang Huang, Karim ElRefai, Rares Andrei Ambrus, Richard Cheng, Muhammad Zubair Irshad, and Ken Goldberg. Real2render2real: Scaling robot data without dynamics simulation or robot hardware, 2025. URL https://arxiv.org/abs/2505.09601. 

- [48] Guangqi Jiang, Haoran Chang, Ri-Zhao Qiu, Yutong Liang, Mazeyu Ji, Jiyue Zhu, Zhao Dong, Xueyan Zou, and Xiaolong Wang. Gsworld: Closed-loop photorealistic simulation suite for robotic manipulation. _arXiv preprint arXiv:2510.20813_ , 2025. 

- [49] Kaifeng Zhang, Shuo Sha, Hanxiao Jiang, Matthew Loper, Hyunjong Song, Guangyan Cai, Zhuo Xu, Xiaochen Hu, Changxi Zheng, and Yunzhu Li. Realto-sim robot policy evaluation with gaussian splatting simulation of soft-body interactions. _arXiv preprint arXiv:2511.04665_ , 2025. 

- [50] Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. In _European Conference on Computer Vision (ECCV)_ , pages 405–421, 2020. 

10.48550/ARXIV.2502.19645. URL https://doi.org/10. 48550/arXiv.2502.19645. 

   - [59] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, Winson Han, Wilbert Pumacay, Angelica Wu, Rose Hendrix, Karen Farley, Eli VanderBilt, Ali Farhadi, Dieter Fox, and Ranjay Krishna. Molmoact: Action reasoning models that can reason in space, 2025. URL https://arxiv.org/abs/2508.07917. 

   - [60] Taeyoon Lee, Jaewoon Kwon, Patrick M. Wensing, and Frank C. Park. Robot model identification and learning: A modern perspective. _Annu. Rev. Control. Robotics Auton. Syst._ , 7(1), 2024. doi: 10.1146/ ANNUREV-CONTROL-061523-102310. URL https: //doi.org/10.1146/annurev-control-061523-102310. 

   - [61] Physical Intelligence. openpi, 2025. URL https://github. com/Physical-Intelligence/openpi. 

- [51] Lior Yariv, Peter Hedman, Christian Reiser, Dor Verbin, Pratul P. Srinivasan, Richard Szeliski, Jonathan T. Barron, and Ben Mildenhall. Bakedsdf: Meshing neural sdfs for real-time view synthesis. _arXiv_ , 2023. 

- [52] Johannes Lutz Sch¨onberger and Jan-Michael Frahm. Structure-from-motion revisited. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 4104–4113, 2016. 

- [53] Brian Curless and Marc Levoy. A volumetric method for building complex models from range images. In _Proceedings of the 23rd Annual Conference on Computer Graphics and Interactive Techniques (SIGGRAPH ’96)_ , pages 303–312. ACM, 1996. doi: 10.1145/237170.237269. 

- [54] William E. Lorensen and Harvey E. Cline. Marching cubes: A high resolution 3d surface construction algorithm. In _Proceedings of the 14th Annual Conference on Computer Graphics and Interactive Techniques (SIGGRAPH ’87)_ , pages 163–169. ACM, 1987. doi: 10.1145/37401.37422. 

- [55] NVIDIA. Isaac Sim. URL https://github.com/isaac-sim/ IsaacSim. 

- [56] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models, 2025. URL https://arxiv.org/abs/2501.09747. 

- [57] Huang Huang, Fangchen Liu, Letian Fu, Tingfan Wu, Mustafa Mukadam, Jitendra Malik, Ken Goldberg, and Pieter Abbeel. OTTER: A vision-language-action model with text-aware visual feature extraction. _CoRR_ , abs/2503.03734, 2025. doi: 10.48550/ARXIV.2503. 03734. URL https://doi.org/10.48550/arXiv.2503.03734. 

- [58] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success. _CoRR_ , abs/2502.19645, 2025. doi: 

