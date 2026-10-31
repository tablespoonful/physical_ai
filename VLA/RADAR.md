---
title: "RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation"
date: "2026-02-11"
authors: "Yuhao Chen; Zhihao Zhan; Xiaoxin Lin; Zijian Song; Hao Liu; Qinhan Lyu"
url: https://arxiv.org/abs/2602.10980
pdf: https://arxiv.org/pdf/2602.10980
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.10980)** / [論文ページ](https://arxiv.org/abs/2602.10980)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation** 

Yuhao Chen<sup>1,*</sup> , Zhihao Zhan<sup>1,*</sup> , Xiaoxin Lin<sup>1</sup> , Zijian Song<sup>1</sup> , Hao Liu<sup>1</sup> , Qinhan Lyu<sup>1</sup> , Yubo Zu<sup>1</sup> , Xiao Chen<sup>1</sup> , Zhiyuan Liu<sup>1</sup> , Tao Pu<sup>1,3</sup> , Tianshui Chen<sup>3,4</sup> , Keze Wang<sup>1,2,3</sup> , Liang Lin<sup>1,2,3</sup> , Guangrun Wang<sup>1,2,3,†</sup> 

**Email:** {chenyh387, zhanzhh6} (at) mail2.sysu.edu.cn, wanggrun (at) gmail.com 

1Sun Yat-sen University; 2Guangdong Key Laboratory of Big Data Analysis and Processing; 

3X-Era AI Lab;4Guangdong University of Technology 

## **Abstract** 

Vision–Language–Action (VLA) models have achieved remarkable progress in embodied intelligence; however, their evaluation remains largely confined to simulations or highly constrained realworld settings. This mismatch creates a substantial _reality gap_ , where strong benchmark performance often masks poor generalization in diverse physical environments. We identify three systemic shortcomings in current benchmarking practices that hinder fair and reliable model comparison. **First** , existing benchmarks fail to model **real-world dynamics** , overlooking critical factors such as dynamic object configurations, robot initial states, lighting changes, and sensor noise. **Second** , current protocols neglect **spatial–physical intelligence** , reducing evaluation to rote manipulation tasks that do not probe geometric reasoning. **Third** , the field lacks scalable **fully autonomous evaluation** , instead relying on simplistic 2D metrics that miss 3D spatial structure or on human-in-the-loop systems that are costly, biased, and unscalable. 

To address these limitations, we introduce **RADAR** ( **R** eal-world **A** utonomous **D** ynamics **A** nd **R** easoning), a benchmark designed to systematically evaluate VLA generalization under realistic conditions. RADAR integrates three core components: (1) a principled suite of physical dynamics; (2) dedicated tasks that explicitly test spatial reasoning and physical understanding; and (3) a fully autonomous evaluation pipeline based on 3D metrics, eliminating the need for human supervision. 

We apply RADAR to audit multiple state-of-the-art VLA models and uncover severe fragility beneath their apparent competence. Performance drops precipitously under modest physical dynamics, with the expectation of 3D IoU declining from 0.261 to 0.068 under sensor noise. Moreover, models exhibit limited spatial reasoning capability. These findings challenge the assumption that high scores on traditional benchmarks imply robust embodied intelligence, and position RADAR as a necessary bench toward reliable and generalizable real-world evaluation of VLA models. 

## **CCS Concepts** 

### • **Computing methodologies** → **Vision for robotics** . 

## **Keywords** 

Vision-Language-Action Models (VLA), Embodied AI, Real-World Benchmarking, Spatial-Physical Intelligence, Autonomous Evaluation, Generalization, Robustness Analysis 


**Figure 1: A comparison of benchmarking paradigms. We categorize existing VLA evaluation into Simulation (scalable but lacks physical dynamics) and constrained Real-World setups (realistic but static, lacking spatial consideration, and often relying on manual evaluation). RADAR (Right) bridges these gaps by providing a unified bench that guarantees Real-World Dynamics via systematic dynamics, Spatial Reasoning via geometric tasks, and fully Autonomous Evaluation using high-precision 3D metrics.** 

## **1 Introduction** 

The pursuit of general-purpose embodied intelligence has reached a pivotal juncture with the emergence of Vision–Language–Action (VLA) models [1, 2, 8, 10, 16, 20, 21, 25]. By integrating the semantic reasoning capabilities of large language models with visual perception and robotic control, VLA systems promise agents that can follow natural language instructions in unstructured, realworld environments [4]. Recent studies report impressive results, often achieving near-perfect success rates on established benchmarks. However, a critical disconnect persists: despite strong performance in curated evaluations, these models frequently exhibit fragility and failure when deployed in the wild. We argue that this gap arises not only from a lack of modeling capacity, but also from a systemic failure in current evaluation methodologies. 

Existing benchmarks tend to fall into two extremes: **scalable yet oversimplified simulations** that lack physical dynamics [5, 6, 11, 13, 17, 22, 23] (see Fig. 1 (a)), or **constrained real-world setups** that offer limited dynamics and autonomy [19, 24] (see Fig. 1 (b)). Moreover, both paradigms fail to rigorously evaluate spatial reasoning. 

> ∗These two authors contributed equally and share first authorship. 

> †Corresponding author: Guangrun Wang 

KDD ’26, , 

Chen et al. 


**Figure 2: A comparison between current VLA benchmarks and the proposed RADAR bench. Existing benchmarks often rely on (1) static, simplified environments, (2) tasks that require only intuitive perception, and (3) manual or limited 2D evaluation. In contrast, RADAR introduces (1) complex real-world dynamics (e.g., lighting, backgrounds), (2) tasks designed for enhanced spatial-physical reasoning, and (3) a fully automated, 3D-based evaluation loop for infinite scaling.** 

This disconnect creates a substantial _reality gap_ , where high leaderboard scores mask severe overfitting to static conditions [19, 24]. To address this issue, we focus on **real-world** evaluation rather than simulation; as illustrated in Fig. 2, we identify three fundamental deficiencies in existing real-world VLA benchmarks that hinder scientific progress and prevent fair model comparison. 

_Insufficient modeling of real-world dynamics._ The physical world is inherently stochastic and dynamic, yet many so-called “real-world” benchmarks reduce it to a static stage. High-entropy factors that critically affect deployment viability—including dynamic object configurations, robot initial states, lighting variations, background texture noise, and sensor fluctuations—are often ignored or fixed. Without a principled formulation of these dynamics, benchmarks reward memorization of a specific laboratory configuration rather than robust generalization to realistic conditions [10]. 

_Neglect of spatial–physical intelligence._ True embodied intelligence requires more than executing rote pick-and-place behaviors; 

it demands an understanding of geometry, three-dimensional spatial relationships, and physical constraints. Current evaluation protocols rarely test whether a model genuinely understands a scene or merely exploits spurious 2D correlations. Dedicated tasks that probe spatial reasoning—such as reasoning about geometric, occlusion, and relative positioning—are largely absent, despite being prerequisites for complex manipulation and interaction [15]. 

_Lack of scalable autonomous evaluation._ Evaluation remains a major bottleneck in real-world robotics. Human-in-the-loop protocols (e.g., challenge-style evaluations) are costly, unscalable, and susceptible to observer bias, forcing researchers to wait for results and limiting experimental throughput [19]. In contrast, existing automated approaches typically rely on 2D object detection or heuristic success criteria, which lack the fidelity required to verify threedimensional spatial outcomes or nuanced physical interactions [24]. 

To bridge this gap, we introduce **RADAR** ( **R** eal-world **A** utonomous **D** ynamics **A** nd **R** easoning), a benchmark designed to systematically stress-test VLA generalization. RADAR moves beyond “happypath” evaluation by introducing controlled perturbations across four axes: manipulated objects, robot initial states, task instructions, and environmental conditions. Unlike standard benchmarks that focus solely on simple pick-and-place routines, RADAR incorporates dedicated spatial reasoning tasks to rigorously evaluate a model’s physical intelligence and geometric understanding. Crucially, the entire system is built upon a fully autonomous evaluation pipeline that employs rigorous 3D metrics, enabling largescale, reproducible testing without human intervention. 

Using RADAR, we conduct a comprehensive audit of state-ofthe-art VLA models and uncover striking brittleness beneath their apparent competence. Our analysis reveals that current models are largely over-fitting specialists that collapse under modest physical variation. In particular, performance is hypersensitive to realworld dynamics: sensor noise causes the expectation of 3D IoU to drop from **0.261** to below **0.068** . Moreover, even top-performing models struggle with tasks that require genuine 3D spatial reasoning and instruction following, exposing a fundamental limitation in their embodied understanding. 

In summary, our contributions are threefold: 

- We identify and formalize critical limitations of existing VLA benchmarks, particularly in their treatment of environmental dynamics, spatial–physical intelligence, and evaluation autonomy. 

- We introduce **RADAR** , a fully autonomous real-world benchmark that integrates systematic environmental dynamics, dedicated spatial reasoning tasks, and 3D evaluation metrics to rigorously assess robustness and generalization. 

- We provide a rigorous empirical analysis of state-of-the-art VLA models, quantifying their sensitivity to physical and linguistic variations and revealing critical deficiencies in spatial reasoning. 

## **2 Related Work** 

## **2.1 Vision-Language-Action Models** 

The paradigm of embodied AI has shifted significantly from specialized primitives to general-purpose Vision-Language-Action (VLA) 

KDD ’26, , 

RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation 

models. Early works demonstrated the efficacy of large-scale imitation learning [2], while subsequent approaches have focused on integrating the reasoning capabilities of Large Language Models (LLMs) directly into the control loop [1, 25]. Recent advances have further pushed the boundaries of these models by scaling up training data and model architecture [8, 10, 21]. Despite their impressive zero-shot generalization on semantic tasks, the generalization of these models against physical perturbations and geometric variations remains under-explored. While models like 𝜋0 [1] and others [16, 20] show promise, their evaluation is often confined to standard “happy-path” scenarios, leaving their performance in highentropy, dynamic environments an open question. 

## **2.2 Benchmarks in Robotic Manipulation** 

Benchmarking in robotics has historically bifurcated into two distinct streams: large-scale simulation and constrained real-world setups. 

_Simulation Benchmarks._ Simulated environments such as LIBERO family (LIBERO [11], LIBERO-Pro [23], LIBERO-Plus [7]), ManiSkill [17], VLABench [22], and RoboTwin [5, 13] provide scalable, reproducible platforms for training and evaluation. These benchmarks allow for rapid iteration and precise metric tracking. However, they suffer from a fundamental _reality gap_ : simplified physics engines and sterile visual rendering fail to capture the stochasticity of the real world—such as lighting artifacts, sensor noise, and complex friction dynamics. Consequently, policies that excel in simulation often fail to transfer effectively to physical hardware. 

_Real-World Benchmarks._ To address the fidelity gap, several realworld benchmarks have been proposed. However, these setups typically prioritize reproducibility at the cost of diversity. Benchmarks like RoboChallenge [19] and others [24] often utilize fixed tabletop settings with static lighting and background conditions. Beyond environmental constraints, current protocols frequently neglect spatial–physical intelligence, reducing evaluation to rote manipulation tasks that do not probe geometric reasoning or holistic scene understanding. Furthermore, the field lacks scalable fully autonomous evaluation, instead relying on simplistic 2D metrics that miss 3D spatial structure [24] or on human-in-the-loop systems that are inherently costly, biased, and unscalable. **RADAR** distinguishes itself by bridging these gaps: it introduces a unified framework that guarantees real-world dynamics, enforces spatial reasoning complexity, and enables high-precision autonomous 3D evaluation. 

## **2.3 Spatial and Physical Intelligence** 

The integration of Vision-Language Models (VLMs) into robotics has largely focused on semantic reasoning—interpreting high-level instructions like “pick up the apple.” However, genuine embodied intelligence requires _spatial-physical intelligence_ : the ability to reason about 3D geometry, occlusion, and relative positioning. Recent work has highlighted the deficiency of current VLAs in spatial reasoning [15], noting that models often rely on 2D pattern matching rather than 3D scene understanding. While some datasets focus on spatial relations in static images, there is a lack of dynamic benchmarks that require an agent to manipulate objects based on 

complex geometric constraints (e.g., “place the block behind the cylinder relative to the gripper”). RADAR addresses this by incorporating dedicated spatial reasoning tasks that cannot be solved via semantic intuition alone. 

## **2.4 Autonomous Evaluation in Robotics** 

Evaluating robotic policies in the real world is notoriously difficult. The “gold standard” remains human observation, which is unscalable, expensive, and prone to subjective bias. Recent efforts have attempted to automate this process using VLM-based judges [24] or 2D object detectors [24]. However, VLM judges are susceptible to hallucinations, and 2D detectors lack the depth information necessary to verify 3D success criteria (e.g., checking if an object is hovering above a target). By leveraging a fully autonomous pipeline underpinned by high-precision 3D metrics, RADAR eliminates the human bottleneck while ensuring that evaluation is grounded in physical reality rather than visual approximation. 

## **3 The proposed RADAR Bench** 

We now present the proposed RADAR benchmark. We begin by outlining the overall evaluation pipeline in Section 3.1. We then detail our protocols for modeling real-world dynamics in Section 3.2 and describe the design of our spatial intelligence reasoning tasks in Section 3.3. Finally, in Section 3.4, we present our methodology for scalable, autonomous 3D evaluation. 

**Input :** Control Policy 𝜋, Task Definition 𝒯𝑡𝑎𝑠𝑘 , Max Steps 𝑇𝑚𝑎𝑥 **Output:** Success Score 𝑆𝑒𝑣𝑎𝑙 , Trajectory 𝜏 𝜏←∅ **Client** sends Begin_eval request to **Worker for** 𝑡= 0 **to** 𝑇𝑚𝑎𝑥 **do** // Observation Step Receive observation 𝑜𝑡 = {𝐼𝑟𝑔𝑏, 𝐼𝑑𝑒𝑝𝑡ℎ, 𝑞𝑝𝑟𝑜𝑝𝑟𝑖𝑜} from Worker // Check Termination **if** _IsTerminated(_ 𝑜𝑡 , 𝒯𝑡𝑎𝑠𝑘 _)_ **then break end** // Policy Inference Compute action 𝑎𝑡 ←𝜋(𝑜𝑡 ) // Execution Send 𝑎𝑡 to Worker via Action interface Record tuple (𝑜𝑡 , 𝑎𝑡 ) to 𝜏 Wait for execution completion **end** // Automated Scoring Request Get_Score from Server 𝑆𝑒𝑣𝑎𝑙 ← CalculateIoU(FinalState, 𝒯𝑡𝑎𝑟𝑔𝑒𝑡 ) **return** 𝑆𝑒𝑣𝑎𝑙 **Algorithm 1:** RADAR Evaluation Protocol. 

KDD ’26, , 

Chen et al. 


**Figure 3: The RADAR Pipeline. RADAR operates as a centralized platform utilizing a client–server–worker architecture. Users submit requests to the central server, which manages authorization, task queuing, and scheduling strategies. The server then dispatches tasks to workers for execution—such as controlling robots or processing video—with the final evaluation results fed back to the user.** 

## **3.1 The RADAR Pipeline** 

The RADAR benchmark operates on a centralized automation platform designed to decouple policy submission from physical execution. As illustrated in Fig. 3, the system adopts a scalable clientserver-worker architecture. Users (Clients) act as the entry point, submitting authorization credentials, task specifications, and control policies to a central **RADAR Server** . This server functions as the system orchestrator; it handles authentication, manages a global task queue, and applies scheduling strategies to dispatch jobs to available **Worker** nodes. 

The specific communication protocols facilitating this workflow are detailed in Fig. 4. The interaction begins when the Server assigns a specific Worker to a Client via the Get_Worker interface. Once connected, the Client communicates directly with the Worker node to minimize latency. The evaluation loop is driven by the Client issuing Begin_eval requests, followed by high-frequency Action commands. The Worker executes these commands, returning dense geometric data and video logs, while simultaneously sending periodic Heartbeat signals to the Server to confirm system liveliness. 

To realize the goal of 24/7 autonomous evaluation within this architecture, the Worker node is implemented as a self-contained robotic cell—the core physical embodiment of the RADAR platform. This integrated hardware system is designed to execute manipulation tasks, reset its own state, and collect rich, multi-perspective sensor data entirely without human intervention. Its architecture is centered around a collaborative robot arm serving as the primary actuator, augmented with a comprehensive sensor suite and an actuated stage to enhance task diversity. The entire setup is orchestrated by a central computing unit, which synchronizes all components to enable seamless, continuous operation. The key components of this platform are detailed below. 

_Central Computing Unit (The Host PC)._ The brain of our system is a high-performance host PC. It runs the core evaluation software, including the task planner, the VLA model inference engine, and the communication middleware (e.g., ROS). This unit is responsible for processing visual data from all cameras, sending control commands to the robot arm and the movable platform, and logging all experimental data—from actuator states to timestamps and performance metrics. Its robust computational power ensures real-time decision-making and synchronization across the entire system. 


**Figure 4: RADAR Interface Protocols. A detailed view of the communication interfaces between the Client, Server, and Worker components. The Client initiates evaluation requests (Begin_eval, Action, Reset), which are routed to the Worker. The Server coordinates resource allocation via Get_Worker and monitors system health through Heartbeat signals from workers.** 

_Robot Arm with Wrist-Mounted Camera._ As the primary manipulation agent, we employ a collaborative robotic arm (e.g., 6-DOF UR5e), equipped with an adaptive gripper (e.g., Robotiq 2F-85). A key component for enabling closed-loop visual manipulation is a camera (e.g., Intel RealSense D435) mounted rigidly on the robot’s wrist. This eye-in-hand configuration provides a first-person view from the end-effector, which is crucial for fine-grained manipulation tasks like insertion and precise alignment, offering a perspective that closely matches the agent’s action space. 

_External Stereo Vision System._ To provide a global, third-person view of the workspace and to facilitate tasks requiring broader scene understanding, we integrate two fixed, high-resolution cameras (e.g., Intel RealSense D415). These cameras are strategically positioned at different vantage points around the workspace, forming a stereo vision system. This setup allows for accurate 3D reconstruction of the scene, which is used for initial object localization, tracking agent motion, and providing an objective, global perspective for scoring tasks that require long-horizon reasoning. 

_Actuated Task Platform._ A critical innovation for achieving full autonomy is our custom-designed actuated platform. This platform, which holds the task-specific objects and environment, is mounted on a mechanical stage (e.g., a linear servo slide or rotating turntable). Its primary function is to enable automatic scene reset. Upon task completion or failure, the host PC can command this platform to move—for instance, by sliding out to a designated ”reset position” where a simple mechanism can clear and rearrange objects, or by rotating to present a fresh, pre-configured task scene. This eliminates the single greatest source of manual intervention in realworld testing. 

To synthesize the architectural components and interaction protocols described above, we present the unified evaluation workflow in Algorithm 1. 

## **3.2 Modeling Real-World Dynamics** 

To rigorously assess the robustness of VLA models, RADAR moves beyond the sterile and static conditions typical of existing benchmarks. In real-world settings, embodied agents must contend with inherent entropy: lighting conditions vary, sensors drift, and human instructions are inconsistent. We operationalize _real-world dynamics_ not as a single nuisance factor, but as a principled injection 

KDD ’26, , 

RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation 

of stochastic perturbations across the physical, visual, and semantic domains during evaluation. We categorize these dynamics into three complementary pillars. 

mirroring the unpredictability of unstructured real-world environments. 

Unlike simulation environments that rely on approximation engines (e.g., MuJoCo, PyBullet) to estimate physical interactions, RADAR validates policies directly in the physical world. Our system implementation ensures that complex dynamic phenomena— such as non-linear friction, deformable object interaction, and contactrich manipulation—are inherently captured rather than simulated. We implement this through a three-tiered architecture focusing on physical actuation, temporal consistency, and sensory fidelity. 

_Environmental & Visual Dynamics._ The visual appearance of a workspace is rarely constant. We evaluate perceptual robustness by perturbing both photometric and geometric properties of the scene: 

- **Illumination Variance.** We introduce randomized lighting conditions to test invariance to shadows and color shifts, varying both light intensity (lux) and color temperature. This forces the agent to rely on geometric cues rather than overfitting to specific pixel intensity distributions. 

_Physical Actuation and Control Interface._ To model realistic contact dynamics, the Worker node operates the robotic manipulator using a high-frequency impedance control loop. Rather than assuming instantaneous state transitions (common in simulation), our implementation accounts for the robot’s physical inertia and joint limits. Let **a** 𝑡 be the action command (e.g., delta-pose Δ **p** ∈ ℝ<sup>6</sup> ) sent by the Client. The actual execution on the hardware follows: 

- **Background & Distractors.** To challenge segmentation and attention mechanisms, we alter the workspace background, ranging from changes in tabletop texture to the introduction of distractor objects. These distractors share visual attributes (e.g., color or shape) with the target object but are irrelevant to the task. 


- **Configurable Layouts.** We reject fixed-position initialization. For each evaluation episode, the initial pose of all objects **T** obj ∈𝑆𝐸(2) is randomized within workspace bounds. This encourages the model to reason over relative spatial relationships (e.g., “left of the mug”) rather than memorizing absolute coordinates. 

where 𝑓phys represents the true, unknown transition function of the physical world, **v** max denotes safety velocity constraints, and 𝜖𝑒𝑛𝑣 accounts for unmodeled disturbances (e.g., cable drag or surface friction). By enforcing velocity and acceleration limits, we ensure that the benchmark evaluates policies under realistic actuation constraints. 

_Agent-Centric & Physical Dynamics._ A robust policy should be insensitive to specific robot configurations and minor hardware imperfections. We therefore introduce perturbations that affect the agent’s physical interface with the environment: 

_Temporal Dynamics and Latency Modeling._ Real-world embodied AI often relies on remote inference (cloud robotics) or heavy onboard compute, both of which introduce latency. RADAR explicitly models these temporal dynamics through its asynchronous Client-Worker architecture (refer to Algorithm 1). The time gap Δ𝑡 between, an observation capture 𝑡𝑜𝑏𝑠 and action execution 𝑡𝑒𝑥𝑒𝑐 is non-zero and variable: 

- **Robot State Perturbation.** While standard benchmarks initialize the robot in a fixed “home” configuration **q** home, we instead sample the initial joint configuration as **q** init ∼ 𝒩( **q** home, Σ), where Σ is a covariance matrix chosen to ensure safe yet diverse starting poses. This prevents policies from overfitting to a single trajectory primitive. 


where 𝛿𝑛𝑒𝑡 is the network round-trip time, 𝛿inf is the model inference time, and 𝛿𝑡𝑟𝑎𝑛𝑠 is the hardware transmission latency. This implementation forces evaluated policies to be robust against timedelayed feedback, a critical failure mode in real-world deployment often ignored in zero-latency simulations. 

- **Sensor Noise Injection.** To simulate sensor degradation and calibration drift, we inject synthetic noise into the sensory stream, including Gaussian noise on depth maps and small rotational perturbations on extrinsic camera parameters. These perturbations test the resilience of the policy to imperfect state estimation. 

By feeding these raw, noisy signals directly to the agent without “oracle” denoising, RADAR evaluates the model’s ability to generalize across the imperfections inherent to physical hardware. 

_Semantic Dynamics._ Real-world instructions are inherently unstructured and variable. To evaluate robustness to linguistic variation, we employ a large language model (LLM) to paraphrase canonical task descriptions into linguistically diverse yet semantically equivalent prompts. For example, the instruction _“Pick up the red block”_ may be rewritten as _“Grasp the crimson cube”_ or _“Retrieve the scarlet object.”_ This forces the VLA model to ground its actions in semantic meaning rather than relying on specific lexical tokens. 

## **3.3 Spatial Intelligence Reasoning** 

A core objective of RADAR is to evaluate an agent’s ability to reason about 3D geometry, spatial relationships, and object affordances. Unlike 2D-centric benchmarks where tasks can often be solved via pixel-matching heuristics, our platform implements spatial intelligence reasoning through three key architectural pillars: multi-view sensory integration, explicit SE(3) action requirements, and volumetric task constraints. 

_Compound Perturbations (“Chaos” Test)._ Finally, we evaluate agents under _combined dynamics_ by sampling jointly from all aforementioned perturbation distributions. In this setting, an agent may encounter dim lighting, a non-canonical initial robot pose, paraphrased instructions, and slight camera miscalibration simultaneously. This “chaos” test represents the most challenging evaluation regime, closely 

_Multi-View Sensory Integration and Occlusion Handling._ Spatial reasoning requires understanding that objects persist and maintain geometry even when occluded. We implement this by positioning cameras at orthogonal viewpoints (e.g., front-down and 

KDD ’26, , 

Chen et al. 

side-angle). The benchmark provides agents with a stream of calibrated RGB-D data, requiring them to mentally fuse these disjoint perspectives into a coherent scene representation. To succeed, the agent must resolve ambiguities such as: 

- **Depth Disambiguation:** Distinguishing between an object’s scale and its distance from the camera. 

- **Occlusion Reasoning:** Predicting the location of a grasp point that is visible in View A but occluded by the robotic arm in View B. 

We facilitate this by providing precise extrinsic calibration matrices,<sup>𝑏𝑎𝑠𝑒</sup> 𝑇𝑐𝑎𝑚𝑖 ∈𝑆𝐸(3), allowing models to project features from 2D pixel space into the robot’s 3D base frame. 

_High-Precision SE(3) Action Space._ True spatial intelligence manifests in the ability to manipulate objects with 6-Degrees-of-Freedom (6-DoF). We reject simplified action spaces (such as top-down 4- DoF picking) in favor of full rigid-body transformations. The agent must predict an action **a** 𝑡= (Δ **p** , Δ **q** ), where Δ **p** ∈ℝ<sup>3</sup> represents translation and Δ **q** ∈𝑆𝑂(3) represents rotational alignment (represented as quaternions or Euler angles). This implementation forces the policy to reason about: 

Alignment Error = min **R** ∈𝑆𝑂(3)| **R** 𝑜𝑏𝑗− **R** 𝑡𝑎𝑟𝑔𝑒𝑡|𝐹 , (3) 

where the agent must align the object’s principal axes with the target slot (e.g., inserting a rectangular battery into a remote controller), a task impossible without understanding 3D rotational geometry. 

_Volumetric Task Constraints._ Finally, we implement spatial reasoning requirements through the task definitions themselves. As detailed in the metrics section, success is determined by 3D Volumetric Intersection (IoU) rather than 2D pixel overlap. This distinguishes “visual alignment” from “physical alignment.” For example, in a “mug hanging” task, a 2D policy might align the mug visually with the hook but fail to place the handle over the hook in depth space. Our evaluation pipeline reconstructs the scene point cloud at every step, ensuring that the agent is penalized for spatial hallucinations (e.g., placing an object behind the target rather than inside it). This strictly enforces that the agent learns a physically valid representation of the workspace. 

## **3.4 Autonomous Evaluation Metrics** 

To ensure standardized and reproducible benchmarking, we define a set of objective and fully automated evaluation metrics for realworld embodied manipulation. As illustrated in Fig. 5, our evaluation pipeline leverages multi-view RGB-D sensing to perform dense 3D reconstruction, enabling precise geometric comparisons between the achieved and target states. The metrics are organized into task-level success and geometric accuracy measures, all computed from real-world sensory observations and averaged over 𝑁 independent trials. 

_Task Success Rate._ We define task success based on the spatial consistency between the achieved object state and the target state. Specifically, we utilize the 3D Intersection over Union (3D IoU) between the resulting object bounding box and the target bounding box as the primary criterion. As depicted in Fig. 5(b), where aligned voxels are visually distinguished from discrepancies, this 


**(b) 3D Reconstruction Evaluation and Visualization Results** 

**Figure 5: Evaluation Metric Computation via 3D Reconstruction. (a) The system captures Multi-view RGB-D data from the external stereo cameras to create a comprehensive 4D visual representation of the workspace. (b) 3D Reconstruction and Evaluation. The system generates a dense 3D voxel reconstruction of the scene to compare the current object state against the target state.** 

metric captures the volumetric overlap between the agent’s result and the goal. Let 𝐵𝑟𝑒𝑠 denote the 3D bounding box of the object after task execution, and 𝐵𝑡𝑎𝑟𝑔𝑒𝑡 denote the ground-truth target bounding box. The 3D IoU is calculated as: 


where ∩ and ∪ represent the intersection and union of the two volumes, respectively. A trial is considered successful if its 3D IoU exceeds a task-specific threshold 𝜏 , chosen according to the required tolerance for spatial error. The overall success rate (SR) is defined as: 


_Translational Error._ To capture fine-grained control accuracy beyond binary success, we quantify the translational error (𝑒𝑡𝑟𝑎𝑛𝑠). This metric measures the Euclidean distance between the geometric centroids of the resulting and target bounding boxes: 


where **c** 𝑟𝑒𝑠 and **c** 𝑡𝑎𝑟𝑔𝑒𝑡∈ℝ<sup>3</sup> are the 3D centers of 𝐵𝑟𝑒𝑠 and 𝐵𝑡𝑎𝑟𝑔𝑒𝑡 , respectively. 

## **4 Experiments** 

## **4.1 Training Details** 

We use 𝜋0 [1], 𝜋0-FAST [14], 𝜋0.5 [8], RDT [12] and OpenVLA [9] as baseline models. For all baselines, we initialize from the official pretrained checkpoints released by the respective authors. Each 

KDD ’26, , 

RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation 

**Table 1: Comparison of different VLA models.** ℰ( **IoU3D** ) **is the expectation of IoU3D.** 𝜋0.5 **archive the best result.** 

|Models|SR|SingleBlo<br>IoU3D|ck<br>𝑒𝑡𝑟𝑎𝑛𝑠|SR|TwoBloc<br>IoU3D|k<br>𝑒𝑡𝑟𝑎𝑛𝑠|h<br>SR|ThreeBloc<br>IoU3D|hk<br>𝑒𝑡𝑟𝑎𝑛𝑠|SR|Spatial<br>IoU3D|𝑒𝑡𝑟𝑎𝑛𝑠|SR|Total<br>ℰ(IoU3D)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|𝜋0 [1]|2/4|0.3284|2.07|0/10|×|×|0/10|×|×|0/8|×|×|2/32|0.0411|
|𝜋0-FAST [14]|2/4|0.3797|1.83|0/10|×|×|0/10|×|×|0/8|×|×|2/32|0.0475|
|𝜋0.5 [8]|**4/4**|**0.5216**|**1.08**|**4/10**|**0.4608**|**1.88**|**6/10**|**0.4816**|**1.67**|**3/8**|**0.1261**|**3.8**|**17/32**|**0.2605**|
|RDT [12]|0/4|×|×|0/10|×|×|0/10|×|×|0/8|×|×|0/32|×|
|OpenVLA [9]|0/4|×|×|0/10|×|×|0/10|×|×|0/8|×|×|0/32|×|


**Table 2: Comparison of baseline models with different training strategy. Independent means training only with the corresponding data. Mix ALL means training with all the data. Mix Blocks means training without spatial data, which leads to significant failure in spatial task.** ℰ( **IoU3D** ) **is the expectation of IoU3D.** 

|dl||SingleBlo|ck||TwoBloc|k|h|ThreeBloc|hk||Spatial|||Total|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Moes|SR|IoU3D|𝑒𝑡𝑟𝑎𝑛𝑠|SR|IoU3D|𝑒𝑡𝑟𝑎𝑛𝑠|SR|IoU3D|𝑒𝑡𝑟𝑎𝑛𝑠|SR|IoU3D|𝑒𝑡𝑟𝑎𝑛𝑠|SR|ℰ(IoU3D)|
|Independent|4/4|0.5216|1.08|4/10|0.4608|1.88|6/10|0.4816|1.67|3/8|0.1261|3.8|17/32|0.2605|
|Mix Blocks|3/4|0.6240|0.48|3/10|0.4378|1.94|4/10|0.5334|1.42|0/8|×|×|10/32|0.2032|
|Mix ALL|4/4|0.6186|0.49|4/10|0.5711|0.77|2/10|0.4056|2.11|2/8|0.5655|1.22|12/32|0.2674|


**Table 3: Result of baseline models in different distract factors.** ℰ( **IoU3D** ) **is the expectation of IoU3D.** 

||SingleBlo|ck|TwoBlo|ck|ThreeBlock|Spatial|T|otal|
|---|---|---|---|---|---|---|---|---|
|Models|SR<br>IoU3D|𝑒𝑡𝑟𝑎𝑛𝑠|SR<br>IoU3D|𝑒𝑡𝑟𝑎𝑛𝑠|h<br>SR<br>IoU3D<br>𝑒𝑡𝑟𝑎𝑛𝑠|SR<br>IoU3D<br>𝑒𝑡𝑟𝑎𝑛𝑠|SR|ℰ(IoU3D)|
|Baseline|4/4<br>0.5216|1.08|4/10<br>0.4608|1.88|6/10<br>0.4816<br>1.67|3/8<br>0.1261<br>3.8|17/32|0.2605|
|Light|2/4<br>0.5676|0.97|0/10<br>×|×|2/10<br>0.4365<br>1.95|0/8<br>×<br>×|4/32|0.0928|
|Robot State|4/4<br>0.5145|1.13|3/10<br>0.5072|1.33|5/10<br>0.4584<br>1.74|0/8<br>×<br>×|12/32|0.2239|
|Instruction|3/4<br>0.3351|2.26|2/10<br>0.3849|2.85|0/10<br>×<br>×|0/8<br>×<br>×|5/32|0.0821|
|Background|0/4<br>×|×|0/10<br>×|×|0/10<br>×<br>×|0/8<br>×<br>×|0/32|0.0000|
|Sensor Noise|2/4<br>0.3677|1.93|1/10<br>0.3972|1.52|1/10<br>0.4713<br>1.68|0/8<br>×<br>×|4/32|0.0677|
|Exposure+|1/4<br>0.5409|1.02|0/10<br>×|×|1/10<br>0.4411<br>1.92|0/8<br>×<br>×|2/32|0.0448|
|Exposure-|1/4<br>0.5743|0.76|0/10<br>×|×|1/10<br>0.4027<br>2.36|0/8<br>×<br>×|2/32|0.0459|
|(a) Origin|(b) Ex|posure-|(c) Exp|osure+|(d) Light|(e) Background|(f)|Sensor Noise|


**Figure 6: Visualization of the different distraction factors.** 

model is fine-tuned on our collected real-robot dataset for approximately 20 hours using a single NVIDIA RTX 6000 GPU. All models are trained for a total of 20,000 optimization steps with a batch size of 32. 

We follow the official training configurations provided in the original implementations [1, 8, 14] whenever applicable. The learning rate is scheduled using a cosine decay strategy, with a warm-up period of 1,000 steps, a peak learning rate of 5 × 10<sup>−5</sup> , and a final learning rate of 5 × 10<sup>−6</sup> . We employ the AdamW optimizer with a gradient clipping norm of 1.0. 

KDD ’26, , 

Chen et al. 

In addition to the standard settings, we adopt several specific configurations to ensure stable real-robot control on the Franka manipulator during evaluation. For 𝜋0, we train the model with an action horizon of 50 and an action dimensionality of 32. During evaluation, however, we execute only the first 20 predicted action steps and retain the first 8 dimensions (corresponding to 7 joint commands and 1 gripper command). This truncation is applied to improve control stability and reduce compounding errors over long horizons on real hardware. For 𝜋0-FAST, we train and evaluate the model using an action horizon of 10 and an action dimensionality of 8, following the official design and directly aligning with the Franka control interface. For 𝜋0.5, we train the model with an action horizon of 10 and an action dimensionality of 32. At evaluation time, all 10 predicted action steps are executed, while only the first 8 dimensions are used to control the Franka robot, ensuring consistency with the physical action space. For RDT [12] and OpenVLA [9], we preprocess the data following the official pipeline to obtain the model-required format, and adopt the official training settings for all other configurations. 

## **4.2 Evaluation Settings** 

To comprehensively evaluate the robustness and generalization ability of the models, we construct the test set using four task splits with increasing scene complexity. 

_Task splits._ The **SingleBlock** split contains scenes with only one target object and evaluates basic perception and manipulation capability without relational ambiguity (Fig. 9). The **TwoBlock** split introduces pairwise object relations, requiring the model to correctly understand relative spatial configurations during task execution (Fig. 10). The **ThreeBlock** split further increases compositional difficulty by involving multiple objects and more complex interactions (Fig. 7). The **Spatial** split focuses on relational reasoning between blocks with varied layouts (Fig. 8). 

_Distractor factors._ For each split, we additionally construct several controlled disturbance conditions to evaluate robustness under appearance variations. Specifically, we consider changes in illumination ( **Light** ), scene layout ( **Background** ), sensor corruption ( **Sensor Noise** ), instruction ( **Instruction** ), as well as underexposed and over-exposed imaging conditions ( **Exposure-** and **Exposure+** ). All disturbance factors are applied consistently across different splits. (See Fig. 6) 

_Evaluation protocol._ During evaluation, we directly deploy the trained policy checkpoints. All models are tested under the same data preprocessing pipeline and identical environment configurations to ensure fair comparison. For each split and disturbance condition, multiple evaluation episodes are executed. 

## **4.3 In-Depth Analysis** 

Leveraging the RADAR benchmark, we conduct a comprehensive audit of state-of-the-art Vision–Language–Action (VLA) models. Although these models demonstrate strong performance on standard datasets, our stress-testing reveals notable brittleness under realistic perturbations. In particular, high success rates on static benchmarks often obscure a reliance on shallow heuristics rather than robust embodied understanding (Tabs. 1, 2, 3). For instance, 

under RADAR’s evaluation settings, several representative models— including RDT [12] and OpenVLA [9]—fail to complete any tasks successfully. Based on these observations, we summarize our findings into three primary failure modes: 

_Hypersensitivity to Physical and Geometric Variation._ Our analysis exposes that current state-of-the-art models operate largely as “geometric specialists”—overfitting to specific spatial configurations rather than learning generalizable manipulation skills. We observed extreme sensitivity to initial conditions. This suggests that these models are not “seeing” the object in a robust way, but rather memorizing specific pixel-to-action mappings that shatter when the scene geometry is perturbed. 

_Paradoxical Insensitivity to Language._ Despite being conditioned on natural language instructions, we observe a paradoxical “blindness” to semantic nuances. In many trials, models ignored the specific constraints of the prompt (e.g., “Pick up the _red_ block” vs. “Pick up the _blue_ block”), instead defaulting to interacting with the most visually salient object or the object closest to the gripper. This indicates a failure in semantic grounding—the models struggle to adapt their motor policies based on linguistic variation, treating the language input as a weak signal rather than a strict control constraint. 

_Deficiencies in Genuine Spatial Reasoning._ Finally, our evaluation reveals fundamental limitations in 3D spatial intelligence. While models often succeed at 2D planar tasks (such as pushing an object across a table), they struggle significantly with tasks requiring depth perception and volumetric reasoning (such as precise insertion or stacking). The high failure rate in these tasks highlights a critical gap: current VLA architectures lack a coherent internal 3D world model, relying instead on 2D pattern matching that is insufficient for complex, contact-rich manipulation in the real world. 

_Extra finding._ Finally, we observe that training with the full dataset yields the highest raw action accuracy, which can be observed through the IoU metrics. However, this improvement comes at the cost of increased hallucination, leading to degraded instruction following and reduced semantic fidelity. This trade-off highlights a tension between action imitation performance and reliable language grounding that remains unresolved in current training paradigms and the dataset buildings. 

## **5 Conclusion** 

In this work, we introduced RADAR, a rigorous auditing bench designed to bridge the gap between static evaluation metrics and dynamic real-world robustness. Our evaluation of state-of-the-art VLA models reveals a critical disconnect: despite high performance on traditional benchmarks, current agents exhibit severe fragility when subjected to modest environmental shifts. These findings suggest that current training paradigms prioritize surface-level pattern matching over grounded understanding. By establishing RADAR as a standard for evaluating embodied intelligence, we aim to shift the community’s focus from leaderboard optimization toward the development of agents that are genuinely reliable, generalizable, and robust to the stochastic nature of the real world. 

KDD ’26, , 

RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation 

## **References** 

- [1] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. 2024. 𝜋0: A Vision-Language-Action Flow Model for General Robot Control. _arXiv preprint arXiv:2410.24164_ (2024). 

- [2] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. 2022. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ (2022). 

- [3] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. 2024. LeRobot: State-of-the-art Machine Learning for Real-World Robotics in Pytorch. https://github.com/huggingface/lerobot. 

- [4] Hongyu Chen, Liang Lin, and Guangrun Wang. 2026. _OOWM: Structuring Embodied Reasoning and Planning via Object-Oriented World Modeling_ . Technical Report. Sun Yat-sen University. Technical Report. 

- [5] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. 2025. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ (2025). 

   - [21] Zhihao Zhan, Jiaying Zhou, Likui Zhang, Qinhan Lv, Hao Liu, Jusheng Zhang, Weizheng Li, Ziliang Chen, Tianshui Chen, Keze Wang, et al. 2025. ℰ0: Enhancing Generalization and Fine-Grained Control in VLA Models via Continuized Discrete Diffusion. _arXiv preprint arXiv:2511.21542_ (2025). 

   - [22] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, et al. 2025. Vlabench: A largescale benchmark for language-conditioned robotics manipulation with longhorizon reasoning tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 11142–11152. 

   - [23] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. 2025. LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization. _arXiv preprint arXiv:2510.03827_ (2025). 

   - [24] Zhiyuan Zhou, Pranav Atreya, You Liang Tan, Karl Pertsch, and Sergey Levine. 2025. Autoeval: Autonomous evaluation of generalist robot manipulation policies in the real world. _arXiv preprint arXiv:2503.24278_ (2025). 

   - [25] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. 2023. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ . PMLR, 2165–2183. 

- [6] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. 2025. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ (2025). 

- [7] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. 2025. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ (2025). 

- [8] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. [n. d.]. 𝜋0. 5: a vision-language-action model with open-world generalization, 2025. _URL https://arxiv. org/abs/2504.16054_ 1, 2 ([n. d.]), 3. 

- [9] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. 2024. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ (2024). 

- [10] Weiqi Li, Quande Zhang, Ruifeng Zhai, Liang Lin, and Guangrun Wang. 2025. VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling. _arXiv preprint arXiv:2512.02902_ (2025). 

- [11] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ 36 (2023), 44776–44791. 

- [12] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. 2024. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ (2024). 

- [13] Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Yude Zou, Mingkun Xu, Lunkai Lin, Zhiqiang Xie, Mingyu Ding, and Ping Luo. 2025. RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ . 27649–27660. 

- [14] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. 2025. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ (2025). 

- [15] Zijian Song, Xiaoxin Lin, Qiuming Huang, Guangrun Wang, and Liang Lin. 2025. SIRI-Bench: Challenging VLMs’ Spatial Intelligence through Complex Reasoning Tasks. _arXiv preprint arXiv:2506.14512_ (2025). 

- [16] Zijian Song, Sihan Qin, Tianshui Chen, Liang Lin, and Guangrun Wang. 2025. Physical autoregressive model for robotic manipulation without action pretraining. _arXiv preprint arXiv:2508.09822_ (2025). 

- [17] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse-kai Chan, et al. 2024. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _arXiv preprint arXiv:2410.00425_ (2024). 

- [18] Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, and Pieter Abbeel. 2024. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 12156–12163. 

- [19] Adina Yakefu, Bin Xie, Chongyang Xu, Enwen Zhang, Erjin Zhou, Fan Jia, Haitao Yang, Haoqiang Fan, Haowei Zhang, Hongyang Peng, et al. 2025. RoboChallenge: Large-scale Real-robot Evaluation of Embodied Policies. _arXiv preprint arXiv:2510.17950_ (2025). 

- [20] Zhihao Zhan, Yuhao Chen, Jiaying Zhou, Qinhan Lv, Hao Liu, Keze Wang, Liang Lin, and Guangrun Wang. 2026. Stable Language Guidance for Vision-LanguageAction Models. _arXiv preprint arXiv:2601.04052_ (2026). 

KDD ’26, , 

Chen et al. 

## **A Data Quality and Documentation** 

## **A.1 Data Collection** 

This benchmark is constructed from a curated collection of robot manipulation data covering a diverse set of tasks. Data is collected under clearly defined and standardized protocols to ensure consistency and reproducibility across tasks. Each data sample corresponds to a complete task episode, recorded from task initialization to termination. 

Data collection is conducted via teleoperation using the Gello [18] framework. The robotic platform (Franka) is equipped with three depth cameras, including two fixed cameras positioned in front of the robot to capture the task workspace and one wrist-mounted camera attached to the end-effector. In addition to visual observations, all robot state variables are synchronously recorded at each time step throughout data collection. Demonstrations are generated by trained human operators following task-specific guidelines. To capture natural variability, task instances are executed under different initial conditions, object configurations, and environmental states. All data collection procedures are applied uniformly across tasks to minimize uncontrolled variation. 

## **A.2 Data Organization and Structure** 

We adopt the LeRobotDataset format [3] to package our real-robot demonstrations into a unified representation. Following LeRobot’s convention, the dataset is organized as a repository containing a data/ folder for per-episode trajectories stored in Parquet files, and a meta/ folder that centralizes the dataset schema, indexing, task annotations, and statistics. Concretely, each episode is stored as a timeseries table with synchronized multi-modal observations and actions. 

_Modalities and temporal resolution._ Each timestep includes three RGB image streams and low-dimensional robot state/action vectors: 

- **Images:** image, wrist_image, second_image, all stored as raw RGB frames of size 640 × 480. 

- **Proprioception/state:** state ∈ℝ<sup>8</sup> (float32). 

- **Actions:** actions ∈ℝ<sup>8</sup> (float32). 

- **Indexing:** timestamp, frame_index, episode_index, and global index; plus task_index for language-conditioned supervision. 

We keep the original image resolution and leave resizing/cropping and other vision augmentations to the model-side preprocessing pipeline. This design improves compatibility with diverse VLA backbones that may require different image sizes and camera preprocessing policies. 

## **A.3 Metadata and Documentation** 

LeRobot uses a set of metadata files under meta/ to make datasets self-describing and easy to index/search/visualize. In our release, the following files are provided: 

meta/info.json _(dataset schema & paths)._ This is the central metadata file: it defines the complete feature schema (dtype/shape), FPS, codebase version, and path templates that locate data files. Such a schema-centric design enables downstream code to validate shapes/dtypes and to programmatically enumerate episodes without any external assumptions. 

meta/tasks.jsonl _(task inventory)._ It enumerates all language instructions (task strings) and maps each task to a unique integer task_index. This makes the dataset language-conditioned while allowing efficient filtering and stratified sampling by task. 

meta/episodes.jsonl _(per-episode annotations)._ It stores per-episode metadata such as: 

- episode_index: integer episode id. 

- tasks: a list of language instructions aligned with the episode (in our case typically one instruction per episode, e.g., “Pick up the red block and put in the target place.”). 

- length: number of timesteps/frames in the episode (variable across episodes). 

This file provides the primary index for dataset browsing and for sampling episodes by length/task. 

meta/episodes_stats.jsonl _(per-episode statistics)._ It contains per-episode summary statistics (e.g., min/max/mean) for selected modalities, which is useful for dataset sanity checks and debugging (e.g., detecting corrupted frames, constant signals, or abnormal ranges). LeRobot explicitly supports storing such statistics as part of the dataset metadata. 

norm_stats.json _(dataset-level normalization statistics)._ Following [1, 8] data processing protocol, after dataset conversion, we run a dedicated script to scan the entire dataset and compute global statistics for low-dimensional signals (state and actions). Specifically, we aggregate all frames across all episodes to obtain the per-dimension mean and standard deviation, together with robust percentiles (q01, q99). The resulting statistics are saved and are used to standardize or robustly clip inputs consistently across training runs and model variants. 

KDD ’26, , 

RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation 


**Figure 7: Visualization of two cases of ThreeBlocks split.** 


**Figure 8: Visualization of case of Spatial split.** 


**Figure 9: Visualization of case of SingleBlock split.** 


**Figure 10: Visualization of two cases of TwoBlocks split.** 

KDD ’26, , 

Chen et al. 


**Figure 11: Visualisation of two failed cases.** 

