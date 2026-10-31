---
title: "AutoBio: A Simulation and Benchmark for Robotic Automation in Digital Biology Laboratory"
date: "2025-05-20"
authors: "Zhiqian Lan; Yuxuan Jiang; Ruiqi Wang; Xuanbing Xie; Rongkui Zhang; Yicheng Zhu"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2505.14030
pdf: https://arxiv.org/pdf/2505.14030
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.14030)** / [論文ページ](https://arxiv.org/abs/2505.14030)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **AutoBio: A Simulation and Benchmark for Robotic Automation in Digital Biology Laboratory** 

**Zhiqian Lan**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **Yuxuan Jiang**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **Ruiqi Wang**<sup>3</sup> **Xuanbing Xie**<sup>1</sup> **Rongkui Zhang**<sup>3</sup> **Yicheng Zhu**<sup>4</sup> **Peihang Li**<sup>1</sup> **Tianshuo Yang**<sup>1</sup> **Tianxing Chen**<sup>1</sup> **Haoyu Gao**<sup>3</sup> **Xiaokang Yang**<sup>4</sup> **Xuelong Li**<sup>2</sup> **Hongyuan Zhang**<sup>2</sup> **Yao Mu**<sup>4</sup> **Ping Luo**<sup>1</sup><sup>_,_5</sup><sup>_†_</sup> 1HKU 2TeleAI 3THU 4SJTU 5HKU Shanghai Intelligent Computing Center 

## **Abstract** 

Vision-language-action (VLA) models have shown promise as generalist robotic policies by jointly leveraging visual, linguistic, and proprioceptive modalities to generate action trajectories. While recent benchmarks have advanced VLA research in domestic tasks, professional science-oriented domains remain underexplored. We introduce AutoBio, a simulation framework and benchmark designed to evaluate robotic automation in biology laboratory environments—an application domain that combines structured protocols with demanding precision and multimodal interaction. AutoBio extends existing simulation capabilities through a pipeline for digitizing real-world laboratory instruments, specialized physics plugins for mechanisms ubiquitous in laboratory workflows, and a rendering stack that support dynamic instrument interfaces and transparent materials through physically based rendering. Our benchmark comprises biologically grounded tasks spanning three difficulty levels, enabling standardized evaluation of language-guided robotic manipulation in experimental protocols. We provide infrastructure for demonstration generation and seamless integration with VLA models. Baseline evaluations with two SOTA VLA models reveal significant gaps in precision manipulation, visual reasoning, and instruction following in scientific workflows. By releasing AutoBio, we aim to catalyze research on generalist robotic systems for complex, high-precision, and multimodal professional environments. The simulator and benchmark are publicly available to facilitate reproducible research. 

## **1 Introduction** 

Vision-language-action (VLA) model architectures jointly leverage vision, language, and proprioception modalities to generate action trajectories in an end-to-end manner. By aligning capabilities more closely with how humans perceive and interact with the world, these models hold promise as a pathway toward generalist robotic policies. Recent VLA models [2, 10, 21, 12, 1, 8] have demonstrated impressive results in real-world scenarios, including table bussing, clothing folding, and household manipulation. However, current benchmarks remain largely confined to domestic settings, leaving a critical gap in evaluating VLA models for professional, science-oriented scenarios. 

Biology laboratories represent a uniquely promising yet challenging environment for robotic automation. Experiments in these environments follow clear, rigorous protocols [18], making them well-suited for language-guided robots to interpret and execute. Additionally, the repetitive and time-consuming nature of many laboratory tasks presents opportunities for automation to reduce researcher workload and enhance efficiency. Existing solutions, such as automated sample preparation platforms [13], often prioritize throughput at the expense of flexibility, whereas robotic systems could 

> _∗_ Equal contribution. _†_ Correspondence to pluo@cs.hku.hk Repo: github.com/autobio-bench/AutoBio 

Preprint. Under review. 


Figure 1: AutoBio framework. AutoBio decomposes complex experiments into fundamental biological primitives. These are then implemented via robotic motion primitives within a specialized simulation environment. AutoBio simulator features instrument digitization pipeline, custom physics plugins for lab mechanisms, and rendering stack supporting dynamic interfaces and transparent materials. This enables creation of biologically grounded benchmark tasks to evaluate VLA models on precision control, instruction following, and visual reasoning capabilities in scientific workflows. 

achieve human-level adaptability. Nevertheless, biological experiments impose distinct challenges on robotic intelligence: Long-horizon workflows require perception and interaction with diverse interfaces (e.g., digital displays, control panels, and articulated mechanisms). Precision-dependent tasks like slot alignment are ubiquitous, while transparent liquids and containers complicate visual reasoning. These characteristics make biology laboratories an ideal benchmark for evaluating VLA capabilities in language grounding, visual understanding, and high-precision manipulation. 

To realize this potential, however, it is critical to first address the challenges of simulating biology laboratories—a task that demands advanced asset modeling, physics simulation, and rendering capabilities. Robotic simulations typically use physics engines such as MuJoCo [22], Bullet [5], and PhysX to provide a foundation for physics-based interaction. Building upon these engines, each simulator offers its own set of features tailored to specific focus areas. For instance, robosuite [26] and MuJoCo Playground [25] primarily target reinforcement learning (RL) [19] algorithms through standardized tasks involving pick-and-place operations, articulated object manipulation, and locomotion. RoboTwin [15] emphasizes dual-arm coordination and proposes an automated pipeline for data synthesis. These simulations generally address out-of-the-box contact-based rigid body interactions, and lack specialized capabilities required for biological experimentation. 

In the AutoBio simulator, we extend asset modeling, physics simulation, and rendering capabilities to streamline the entire pipeline of biological experiment simulation, specifically targeting the biological primitives outlined in Figure 1. In biological experiments, many operations rely on specialized instruments such as centrifuges, thermal cyclers, and mixers. We develop a workflow to transform real-world instruments into manipulable assets within AutoBio through 3D Gaussian Splatting [9], CAD refinement, and texture baking. These transformed instruments are then paired with self-contained logic to faithfully replicate their real-world characteristics. Regarding physics simulation, while the physical world operates under universal laws, physics engines typically provide only generalized implementations, leaving finer-grained interactions to be extended by users. To address this, we develop a suite of MuJoCo plugins supporting interactions prevalent in biological experiments—including thread mechanisms, detent mechanisms, eccentric mechanisms, and quasistatic liquid computation—that are rarely addressed in existing simulators. Finally, rendering fidelity proves crucial as vision serves as the primary input modality for VLA models. The prevalence of transparent materials in laboratory environments poses particular challenges, as conventional blendmode rasterization engines handle transparency poorly. We integrate our simulation with Blender’s Physically Based Rendering (PBR) pipeline to achieve visually accurate transparency effects for containers and liquids. In addition, we implement dynamic texture rendering for instrument displays, enabling interactive UI manipulation—a critical feature for tasks involving digital interfaces. 

2 

Table 1: Comparison of AutoBio with related robotic manipulation benchmarks 

|Benchmark<br>(Simulator)|Target<br>domain|#Tasks|Interactive<br>instrument|Threaded<br>object|Fluid|Reactive<br>display|Render<br>backend|Demo<br>synthesis|VLA model<br>train & eval|
|---|---|---|---|---|---|---|---|---|---|
|Meta-world [24]|-|50|_×_|_×_|_×_|_×_|MuJoCo|✓|_×_|
|Robosuite [26]|-|9|_×_|_×_|_×_|_×_|Isaac Sim|_×_|_×_|
|Factory [16]|Factory|8|_×_|✓|_×_|_×_|Isaac Gym|_×_<br>|_×_|
|Maniskill 2 [6]|-|20|_×_|_×_|_×_|_×_|SAPIEN|✓|_×_|
|Robotwin [15]|-|14|_×_|_×_|_×_<br>|_×_|SAPIEN|✓|✓|
|Chemistry3D [11]|Chemistry|5|_×_|_×_|✓|_×_|Isaac Sim|_×_|_×_|
|AutoBio (ours)|Biology|16|✓|✓|✓|✓|Blender|✓|✓|


By combining the above-mentioned simulation features, we propose the AutoBio benchmark, which distills robotic manipulation primitives into practical biological experiment tasks. We provide comprehensive infrastructure to facilitate trajectory synthesis, demonstration generation, and standardized data interfaces for VLA model integration. Our benchmark comprises tasks across three difficulty levels, where we evaluate two open-source SOTA VLA models ( _π_ 0 [1] and RDT [12]). This evaluation reveals critical limitations in current approaches and suggests potential improvements in model architecture and training methodologies. 

Our key contributions summarize as follows: (1) A simulator designed for biology labs, featuring instrument digitization, physics plugins (thread/detent mechanisms, quasi-static liquids), and PBR rendering for transparency and reactive displays. (2) A benchmark with biologically grounded tasks, enabling standardized evaluation of robotic automation in lab protocols, with support for trajectory synthesis and VLA integration. (3) Systematic evaluation of VLA models in science-oriented settings, revealing critical gaps in precision manipulation, instruction following and visual reasoning. 

## **2 Related Works** 

**Vision-Language-Action Model.** Recent generalist policies integrate vision, language, and control for broad task generalization. RT-2 [2] leverages web-scale vision-language data for robotic control, while OpenVLA [10]—trained on 1M real-world demos—surpasses larger closed models on various manipulation tasks. RDT [12] extends diffusion transformers to bimanual manipulation, enabling zero-shot generalization to novel objects and scenes. _π_ 0 [1] (and its successor _π_ 0 _._ 5 [8]) combines VLMs with flow matching for smooth, cross-embodiment action generation. However, the benchmark tasks typically involve coarse manipulation (picking, placing, folding) rather than precise lab procedures. Long-horizon, high-precision tasks and interacting with digital interfaces are rarely evaluated. AutoBio is intended to fill this gap by focusing on lab-specific objects and instruments, explicitly testing fine-grained vision-language-action reasoning not covered by prior work. 

**Robotic Manipulation Benchmark.** Existing benchmarks like ManiSkill [6], Meta-World [24], robosuite [26], ARMBench [14], and Factory [16] focus on rigid-object manipulation (e.g., pick/place, assembly) in home, warehouse or factory settings. While Chemistry3D [11] introduces scienceoriented tasks for chemical experiments, most lack support for fluids, digital interfaces, or lab-specific precision. AutoBio addresses this gap by simulating biological workflows with fluid handling, transparent materials, and interactive instrument UIs—challenges absent in prior benchmarks. A feature comparison with related benchmarks can be found in Table 1. 

**Robotic Automation in Laboratory.** A parallel research thread builds specialized “self-driving” labs for science. Szymanski et al. [20] describe A-Lab that fully automates solid-state materials synthesis with fixed hardware pipelines tailored to inorganic chemistry. In their system, robotic arms dose powders, handle furnaces, and transfer samples between instruments while ML algorithms propose recipes. Similarly, other efforts have automated enzyme engineering or pharmaceutical screens [7, 17, 23]. However, these platforms typically prioritize throughput: each piece of equipment is specialized for a specific protocol, and human oversight is still needed for setup or maintenance [7]. AutoBio targets the complementary goal of flexible, human-like manipulation in the lab. Instead of crafting one-purpose machines, AutoBio’s framework is designed to move toward handling novel protocols end-to-end: reading digital instructions, applying proper tools, and adapting on the fly, that lie beyond the scope of existing lab automation work. 

3 


Figure 2: Digitized instruments for fundamental biological experiment operations, with an example taken from vortex mixer demonstrating the proposed workflow for digitizing real-world instruments. 

## **3 AutoBio Simulator** 

### **3.1 AutoBio Assets** 

With reference to a real-world biomedical laboratory, AutoBio constructs dimensionally accurate digital models of common biological experimental assets and integrates them into a virtual environment. To support robotic manipulation, AutoBio meticulously preserves the physical interaction properties of these digital assets—including collision characteristics and articulated relationships—to ensure physical fidelity in simulation. All digital assets, along with their associated physical and visual properties, are formally described using the MJCF modeling language. 

Table 2: Categories of AutoBio assets 

|Type|Function|Asset|
|---|---|---|
|Instrument|Perform experimental procedures|Centrifuge, Thermal Cycler, Mixer, Pipette, ...|
|Container|Handle and store samples|Centrifuge tube, Cryovial, Pipette tip, ...|
|Rack|Host containers and tools|Multiple-slot rack, Pipette rack, Tip box|
|Robot|Execute manipulation|UR5e, Aloha, Robotiq gripper, DexHand|


Our assets are broadly categorized into four classes, as listed in Table 2. To ensure the visual and geometrical fidelity of the instrument models, we propose a pipeline that incorporates 3D Gaussian Splatting (3DGS) [9] for modeling laboratory assets. As illustrated in Figure 2, the process begins with multi-view video capture of real-world instruments. We then apply the PGSR algorithm [4] to reconstruct high-quality 3DGS assets. Coarse 3D meshes are subsequently extracted to achieve surface reconstruction. The raw mesh from 3DGS often contains redundant vertices and irregular topology due to the discrete nature of Gaussian splats. To optimize the mesh for physical simulation, we refine it in CAD modeling software, producing a simplified, watertight low-poly version while preserving critical geometric features. Articulations are also annotated during this stage through mating constraints. The simplified model then undergoes an automated pipeline that UV-unwraps the mesh, bakes vertex colors from the original high-poly mesh onto a UV texture map, and organizes the output as a digital asset compatible with MuJoCo. 

### **3.2 AutoBio Physics** 

AutoBio employs MuJoCo as its physics engine to simulate rigid-body dynamics, including interactions among robots, labware and instruments. This framework supports accurate multi-articulated system modeling with rich contact, which are essential for replicating laboratory operations such as pipetting, tube handling, and instrument manipulation. In addition to MuJoCo’s native physics features, AutoBio incorporates customized plugins to efficiently simulate laboratory-specific physical behaviors. As depicted in Figure 3, these plugins include: 

**Thread mechanism** models the assembly and mechanical properties of mating threads (e.g., the cap-body assemblies of centrifuge tubes). Inspired by the separation design of collision and visual 

4 


Figure 3: AutoBio physics plugins 


Figure 4: AutoBio rendering features 

geometry, we propose the use of _circular helix’s_ signed distance function (SDF) to substitute meshes in the collision computation of threads. A parameterized circular helix in space can be expressed as 

_H_ ( _t_ ; _r_ 1 _, p_ ) = [ _x, y, z_ ]<sup>_⊤_</sup> = [ _r_ 1 cos _t, r_ 1 sin _t, pt_ ]<sup>_⊤_</sup> _._ 

An SDF calculates the orthogonal distance of a given point _P ∈_ R<sup>3</sup> to the boundary of a geometric shape, which is an implicit representation for 3D geometry. For an unbounded helix, we provide an approximation to its SDF since there is no analytical solution: 

_t_ 0 = atan2( _Py, Px_ ) _, k_ = _⌊_ ( _Pz − t_ 0 _p_ ) _/_ (2 _πp_ ) _⌉ , SDF_ ( _P_ ) = _∥H_ (2 _kπ_ + _t_ 0; _r_ 1 _, p_ ) _− P ∥_ 2 We refer to the appendix for the bounded case. Contact between threads is enabled by assigning a gauge radius _r_ 2 for each helix. The resultant SDF of the composite shape is computed by offsetting the helix’s SDF by _−r_ 2. Finally, a helical thread can be configured by a tuple ( _r_ 1 _, r_ 2 _, p, l, h_ ). The screw motion can be achieved by rigidly attaching mating helical threads to the nut-bolt pair. 

**Detent mechanism** simulates incremental motion with discrete "click" positions in lab instruments, such as stepped knobs or handles. Specifically, the detent mechanism provides tactile feedback via passive spring force generated through relative displacement with the nearest gear position. 

**Eccentric mechanism** generates oscillating motion through off-axis rotation, enabling realistic simulation of mixers (e.g., vortex mixer). The plugin achieves eccentric orbital motion through negatively coupled rotations about two parallel joint axes. 

**Quasi-static liquid** provides an approximate yet efficient simulation of liquid shape deformation within containers, complementing MuJoCo’s limitation in fluid modeling. Specifically, this module treats the liquid surface as a planar interface, neglecting wave propagation and pouring effects. This simplification allows us to describe liquid deformation using only two states: the liquid level height and the surface normal vector. The motion of the surface normal is governed by a damped spherical pendulum system in reponse to external container acceleration. We derive the ODE system of the surface normal through analytical mechanics and Euler-Lagrange equation (see appendix for details). After the normal vector acquired, the liquid body is computed as the intersection of the oriented halfspace and container inner surface. We compute the surface height through volume conservation constraint, thereby generating liquid geometry within the container. 

### **3.3 AutoBio Rendering** 

AutoBio adopts a flexible rendering strategy, offering two rendering backends to accommodate both fast visualization and photorealistic rendering, as summarized by Figure 4a. Our simulation features 

5 


Figure 5: Task progression across three difficulty levels. Each step includes a bordered inset (top-left) showing supplementary camera perspectives for contextual clarity. 

are equally supported by two backends, but with different visual fidelity. Additionally, it implements real-time texture rendering for reactive panel interfaces in laboratory instruments. 

**Basic render** directly utilizes MuJoCo’s native OpenGL renderer, which offers fast but limited visualization. Rendering artifacts would occur when visualizing nested transparent objects, such as transparent tubes containing liquids, due to depth sorting errors. So, we fallback to mark some surfaces as opaque for more meaningful results. 

**Advanced render** bridges MuJoCo simulation state to Blender’s rendering pipeline, leveraging its physically based rendering (PBR) shaders to achieve photorealistic materials grounded in real-world light behavior. Particularly for container-associated manipulation tasks, this solution enables accurate rendering of transparent materials—including polyethylene, glass, and liquids—through configurable optical parameters such as transmission coefficients, refractive indices, and surface roughness. 

**Reactive user interface** employs dynamically loaded texture maps to render control panels and displays for some lab instruments, providing visual feedback for robotic manipulation, as shown in Figure 4b. This module maintains full compatibility with both rendering backends described previously. 

## **4 AutoBio Benchmark** 

Building upon the capabilities of the AutoBio simulator, we develop the AutoBio benchmark, a suite of biologically grounded tasks designed to evaluate robotic automation in laboratory settings. This benchmark focuses on assessing the performance of VLA models in executing common experimental protocols that demand precision, multimodal understanding, and complex manipulation. 

To systematically evaluate VLA models, AutoBio consists of 16 tasks that are categorized into three difficulty levels (Figure 5), characterized by progressively increasing demands on precision, language understanding, and visual reasoning: 

- **Level 1 (Easy):** These tasks feature low demands on vision and manipulation precision, exemplified by straightforward actions like closing a thermal cycler lid (5a). Task requirements and language instructions are generally static, making them suitable for initial system integration and basic policy verification. 

- **Level 2 (Medium):** Tasks at this level, such as unscrewing a centrifuge tube cap (5b), present increased challenges in visual perception and manipulation precision. Language instructions may 

6 

vary based on randomized task parameters (e.g., target position), requiring models to exhibit basic generalization and instruction following capability beyond memorization. These tasks are designed to evaluate fundamental VLA model performance. 

- **Level 3 (Hard):** High-demand tasks like operating a thermal mixer panel (5c) require visual reasoning, fine-grained manipulation, and robust instruction interpretation. Successful completion often necessitates effective closed-loop control and the ability to perform complex cross-modal reasoning. These tasks are intended to rigorously challenge the capabilities of state-of-the-art VLA models in scientifically relevant scenarios. 

Each benchmark task includes: 

- **Scene Initialization and Randomization:** Logic for setting up the initial environment and introducing variations to task parameters and object configurations, promoting generalization. 

- **Demonstration Synthesis:** Logic for synthesizing expert trajectories. 

- **Status Checking:** Mechanisms to determine task success, or progress based on predefined criteria. 

- **VLA Model Interfacing:** Prompts, along with clearly defined mappings for proprioceptive inputs, action spaces, and camera feeds, to simplify integration with diverse VLA architectures. 

Task executions, whether from expert demonstrations or learned policies, can be serialized into a compact format. This enables reproducible replays and facilitates offline rendering or analysis, crucial for standardized benchmarking. 

The AutoBio benchmark currently supports two primary robotic arm configurations: 

- **Aloha:** This arm is equipped with its native gripper. Characterized by a smaller reach and lower payload capacity, it is primarily employed in tasks involving lighter objects, such as handling individual centrifuge tubes. 

- **UR5e:** This arm offers greater reach and payload. We provide two end-effector options for the UR5e: (a) **UR5e-Robotiq:** The UR5e paired with a Robotiq 2F-85 parallel gripper. This configuration is suited for tasks requiring interaction with larger instruments or a wider operational range. (b) **UR5e-DexHand:** The UR5e equipped with a DexHand 021, a 19-DOF dexterous hand. This setup is intended for tasks demanding more dexterity, such as precise pipette operation. Recognizing that current VLA models are often optimized for simpler, low-DOF end-effectors, we offer a simplified control mode for the DexHand. In this mode, most of its DOFs are pre-configured and fixed, with only the metacarpophalangeal (MCP) joint of the thumb actuated collectively to mimic a gripper-like open/close action. 

Our motion planning utilities are designed to be robot-agnostic, facilitating the future integration of additional robotic platforms and end-effector configurations. We plan to expand support for full dexterous manipulation, including synthesis and training for dexterous hands, in upcoming releases. 

AutoBio benchmark tasks are organized into two main scene layouts: single-arm and dual-arm. In single-arm tasks, the placement of the arm relative to target objects and instruments is flexible, allowing for optimized setups for specific operations. For tasks utilizing two robotic arms, typically positioned at opposite ends of a wide laboratory workbench, mimicking collaborative human workflows. For visual perception, all tasks include multiple camera views. In dual-arm setups, this typically comprises a fixed front-facing global camera and two wrist-mounted cameras (one on each arm) providing egocentric views. Single-arm tasks also use a combination of fixed and wrist-mounted cameras, adaptable to the specific task requirements. 

## **5 Experiments** 

### **5.1 Baselines and Experimental Settings** 

We choose 3 tasks from each difficulty level (Table 3) to evaluate VLA capabilities. For each task, we generate 100 demonstration trajectories at a frequency of 50 Hz formatted as a LeRobot [3] dataset. The total training set consists of over 792k frame of data, equivalent to 4.4 hours of continuous recording<sup>1</sup> . All tasks except **Operate thermal mixer panel** are scored binarily (1 for success, 0 

> 1The datasets are published at HuggingFace ( `https://huggingface.co/autobio-bench` ), with two variants for MuJoCo and Blender flavor rendering. 

7 

Table 3: VLA evaluation score measured over 100 episodes on AutoBio tasks with increasing level of difficulty. The score is reported in percentage by computing the value and the standard error of the mean over three runs. 

|# Demo|20|100|20|100|20|100|
|---|---|---|---|---|---|---|
||||**Easy level**||||
|_π_0|**Close ther**<br>96_._3_±_0_._7|**mal cycler lid**<br>99_._7_±_0_._3|**Open ther**<br>73_._0_±_3_._1|**mal cycler lid**<br>96_._0_±_2_._1|**Pick up cen**<br>13_._3_±_0_._9|**trifuge tube**<br>53_._7_±_5_._9|
|RDT|100_._0_±_0_._0|100_._0_±_0_._0|100_._0_±_0_._0|99_._0_±_0_._6|45_._3_±_6_._8|57_._7_±_1_._2|
||||**Medium lev**|**el**|||
|_π_0|**Unscrew cent**<br>1_._3_±_1_._3|**rifuge tube cap**<br>21_._3_±_1_._5|**Aspirate**<br>4_._3_±_0_._3|**with pipette**<br>42_._7_±_1_._8|**Transfer cen**<br>2_._0_±_0_._6|**trifuge tube**<br>40_._7_±_5_._4|
|RDT|2_._0_±_1_._5|2_._7_±_1_._2|0_._0_±_0_._0|0_._3_±_0_._3|0_._3_±_0_._3|2_._0_±_1_._2|
||||**Hard leve**|**l**|||
||**Screw on cent**|**rifuge tube cap**|**Operate ther**|**mal mixer panel**|**Load centr**|**ifuge rotor**|
|_π_0|0_._7_±_0_._3|2_._0_±_0_._6|0_._8_±_0_._2|7_._5_±_0_._6|2_._0_±_0_._6|14_._7_±_1_._3|
|RDT|3_._3_±_1_._2|8_._3_±_4_._4|0_._2_±_0_._1|1_._6_±_0_._5|1_._7_±_1_._2|1_._0_±_1_._0|


for failure). For **Operate thermal mixer panel** , we use a relative progress score to better reflect performance difference due to observed policy difficulties. Task details are provided in the appendix. 

We evaluate two open-source VLAs: _π_ 0 [1] and RDT [12]. We adapt our data to each model’s requirements (proprioception dimensions, image history, normalization), then finetune with default fine-tuning configurations starting with their pretrained checkpoints ( _π_ 0-base and RDT-1B). Adaptation details and model differences can be found in the appendix. 

To examine data scaling effects, we train each model on both full (100 episodes) and reduced (20 episodes) datasets while maintaining consistent normalization. Each configuration undergoes three seeded runs, trained for 30000 steps with batch size 32. A single run takes between 10 to 14 hours on an NVIDIA H800 GPU, resulting in a total runtime of approximately 1,500 GPU hours. 

### **5.2 Experimental Results** 

Policies are evaluated over 100 episodes per task, with final scores (mean ± SEM across runs) reported as percentages in Table 3. Our results reveal distinct characteristics of both VLAs from algorithmic and task-specific perspectives. While neither model demonstrates clear superiority, RDT shows more consistent performance on easy tasks, whereas _π_ 0 excels in challenging scenarios. This likely stems from _π_ 0’s PaliGemma-style architecture with joint attention across modalities and fully trainable weights, compared to RDT’s static pretrained encoders. This architectural advantage enables _π_ 0 to better adapt to complex tasks like **Operate thermal mixer panel** . 

Data scaling effects differ markedly: _π_ 0 benefits from more data across most tasks, while RDT shows limited improvement. This aligns with their architectures - _π_ 0’s 3B trainable parameters are more data-hungry, whereas RDT’s frozen backbones constrain its learning capacity. 

Task difficulty rankings are validated by results. Easy task failures primarily involve gripper slippage, while medium and hard tasks reveal precision limitations in current VLAs’ imitation learning approach. Compounding errors in precise manipulations (e.g., screwing/unscrewing) highlight the need to explore reinforcement learning or similar approaches for improved closed-loop performance. 

Language understanding limitations emerge in **Transfer centrifuge tube** , where policies frequently select incorrect slots. The challenge intensifies in **Operate thermal mixer panel** , where models struggle to connect language instructions with visual feedback, exacerbated by low input resolutions that obscure display numbers, leading to more oscillating loss curves (see appendix) than other tasks. This suggests the need for more efficient high-resolution vision processing pipeline. 

Visual reasoning demands in **Aspirate with pipette** (liquid level sensing) and **Load centrifuge rotor** (symmetry maintenance) expose current VLA limitations. The models fail to adapt to visual 

8 

cues effectively, and current memoryless architecture faces difficulty when reasoning targets leave the camera view. This indicates the necessity for visual chain-of-thought reasoning and memory mechanisms to maintain execution consistency. 

### **5.3 Concatenation for Long-Horizon Task** 

Human operators naturally decompose complex experiments into atomic subtasks, and execute step by step—a capability we test by combining **Close/Open thermal cycler lid** episodes (200 in total) to evaluate trajectory concatenation. We assess performance by executing one subtask to completion before switching prompts (Table 4). 

Table 4: Trajectory concatenation evaluation result 

||**Close**|**Open**|**Close-Open**|**Open-Close**|
|---|---|---|---|---|
|_π_0|100_._0_±_0_._0|96_._0_±_0_._6|3_._0_±_1_._2|87_._3_±_2_._7|
|RDT|98_._7_±_0_._3|88_._0_±_3_._2|4_._3_±_2_._8|8_._7_±_2_._2|


After training on mixed data, the performance of RDT drops slightly on the two original tasks **Close** and **Open** , while _π_ 0’s performance mostly remains the same. Regarding concatenated tasks, since the terminal robot pose of **Open** aligns well with **Close** ’s trajectory, _π_ 0 could achieve reasonable transition in **Open-Close** , yet RDT fails to effectively interpolate in-between. **Close-Open** fails more frequently for both models, due to handle grip orientation differences in demonstration at transition location. This suggests current VLAs primarily memorize trajectories during fine-tuning, with limited ability to generalize or smoothly transition between related tasks. 

## **6 Limitations and Future Work** 

Our work has several limitations that highlight directions for future research. 

**Simulation Fidelity and Efficiency.** The reliance on Blender Cycles for photorealistic rendering introduces a computational bottleneck, with rendering times _∼_ 100× slower than MuJoCo renderer. This is mitigated by the low-resolution inputs of current VLA models, enabling feasible data collection (e.g., 100k frames in hours). However, as tasks like **Operate thermal mixer panel** reveal, highresolution perception may be critical for fine-grained manipulation. Future work will explore optimizations such as hybrid EEVEE-Cycles pipelines to balance speed and visual fidelity. 

**Task and Asset Scalability.** While AutoBio includes biologically grounded tasks, the manual effort required for asset digitization and protocol design limits the diversity of instruments and workflows. We plan to (1) standardize digitization workflow and task templates, (2) employ generative methods for automated asset and task synthesis, and (3) compose long-horizon tasks from modular primitives to support complex, reusable experimental workflows. 

**Real-World Transfer.** AutoBio’s physics models and rendering, though carefully designed, may not fully capture the stochasticity and perceptual noise of real-world labs. Bridging this sim-to-real gap will require improvements in material modeling, actuator dynamics, and domain randomization. 

## **7 Summary** 

This paper introduce AutoBio, a simulation framework and benchmark designed to evaluate robotic automation in biology laboratory environments. By extending laboratory asset modeling, physics simulation, and rendering capabilities, the AutoBio simulator streamlines the biological experiment simulation inspired by practical operation primitives. Built upon this simulator, we propose the AutoBio benchmark with manipulation tasks across three levels of difficulty, to systematically assess the capabilities of vision-language-action (VLA) models. The experimental results show critical limitations of current VLA models in precision manipulation, instruction following and visual reasoning, and suggest potential improvements in model architecture and training methodologies. 

9 

## **References** 

- [1] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [2] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- [3] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, and Thomas Wolf. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. `https: //github.com/huggingface/lerobot` , 2024. 

- [4] Danpeng Chen, Hai Li, Weicai Ye, Yifan Wang, Weijian Xie, Shangjin Zhai, Nan Wang, Haomin Liu, Hujun Bao, and Guofeng Zhang. Pgsr: Planar-based gaussian splatting for efficient and high-fidelity surface reconstruction. _IEEE Transactions on Visualization and Computer Graphics_ , 2024. 

- [5] Erwin Coumans and Yunfei Bai. Pybullet, a python module for physics simulation for games, robotics and machine learning. `http://pybullet.org` , 2016–2021. 

- [6] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, Xiaodi Yuan, Pengwei Xie, Zhiao Huang, Rui Chen, and Hao Su. Maniskill2: A unified benchmark for generalizable manipulation skills. In _International Conference on Learning Representations_ , 2023. 

- [7] Ian Holland and Jamie A Davies. Automation in the life science research laboratory. _Frontiers in bioengineering and biotechnology_ , 8:571777, 2020. 

- [8] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _pi_ 0 _._ 5: a visionlanguage-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [9] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Trans. Graph._ , 42(4):139–1, 2023. 

- [10] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [11] Shoujie Li, Yan Huang, Changqing Guo, Tong Wu, Jiawei Zhang, Linrui Zhang, and Wenbo Ding. Chemistry3d: Robotic interaction benchmark for chemistry experiments. _arXiv preprint arXiv:2406.08160_ , 2024. 

- [12] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1b: a diffusion foundation model for bimanual manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [13] Mike May. Automated sample preparation. _Science_ , 351(6270):300–302, 2016. 

- [14] Chaitanya Mitash, Fan Wang, Shiyang Lu, Vikedo Terhuja, Tyler Garaas, Felipe Polido, and Manikantan Nambi. Armbench: An object-centric benchmark dataset for robotic manipulation, 2023. 

- [15] Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Yude Zou, Mingkun Xu, et al. Robotwin: Dual-arm robot benchmark with generative digital twins. _arXiv preprint arXiv:2504.13059_ , 2025. 

- [16] Yashraj S. Narang, Kier Storey, Iretiayo Akinola, Miles Macklin, Philipp Reist, Lukasz Wawrzyniak, Yunrong Guo, Ádám Moravánszky, Gavriel State, Michelle Lu, Ankur Handa, and Dieter Fox. Factory: Fast contact for robotic assembly. In _Robotics: Science and Systems_ , 2022. 

10 

- [17] Jacob T Rapp, Bennett J Bremer, and Philip A Romero. Self-driving laboratories to autonomously navigate the protein fitness landscape. _Nature chemical engineering_ , 1(1):97–107, 2024. 

- [18] Marcel Schilling, Andrea C Pfeifer, Sebastian Bohl, and Ursula Klingmüller. Standardizing experimental protocols. _Current Opinion in Biotechnology_ , 19(4):354–359, 2008. 

- [19] Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ , volume 1. MIT press Cambridge, 1998. 

- [20] Nathan J Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E Kumar, Tanjin He, David Milsted, Matthew J McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, et al. An autonomous laboratory for the accelerated synthesis of novel materials. _Nature_ , 624(7990):86–91, 2023. 

- [21] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [22] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033. IEEE, 2012. 

- [23] Gary Tom, Stefan P Schmid, Sterling G Baird, Yang Cao, Kourosh Darvish, Han Hao, Stanley Lo, Sergio Pablo-García, Ella M Rajaonson, Marta Skreta, et al. Self-driving laboratories for chemistry and materials science. _Chemical Reviews_ , 124(16):9633–9732, 2024. 

- [24] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning (CoRL)_ , 2019. 

- [25] Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A. Kahrs, Carmelo Sferrazza, Yuval Tassa, and Pieter Abbeel. Mujoco playground, 2025. 

- [26] Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Martín-Martín, Abhishek Joshi, Soroush Nasiriany, Yifeng Zhu, and Kevin Lin. robosuite: A modular simulation framework and benchmark for robot learning. In _arXiv preprint arXiv:2009.12293_ , 2020. 

## **A AutoBio Simulation** 

- **A.1 Simulation-ready assets** 


Figure 6: The overview of AutoBio’s simulation-ready digital assets. 

11 

### **A.2 Thread Mechanism** 

A parameterized circular helix in three-dimensional space can be mathematically expressed as: 


In practical applications, a helix is always bounded. For the above helix formulation, we denote these bounds 2 _πl ≤ t ≤_ 2 _πh_ , where _l_ and _h_ represent the starting and ending thread counts measured from the zero position. Within this framework, the approximate SDF becomes: 


where _dP_ ( _t_ ) represents the Euclidean distance between point _P_ and the corresponding position on the helix parameterized by _t_ : 


This approximation remains valid when the helix angle is sufficiently small. 

In practical implementation, the plugin has been adapted to MuJoCo as an `sdf` extension. While alternative methods exist to approximate screw motion—such as parenting the nut to the bolt within a kinematic tree and adding a coupled hinge joint and slide joint constrained by screw motion—these approaches present two significant limitations: (1) The self-locking mechanism does not naturally emerge from such couplings and proves challenging to implement artificially; (2) Modeling transitional states between fully coupled and completely free bolt-nut pairs becomes problematic. By employing SDF to characterize these interactions in a manner more faithful to real-world physics, we address both challenges gracefully. 

### **A.3 Detent Mechanism** 

The detent mechanism is modeled using a passive force function _f_ ( _q, q_ ˙)that depends exclusively on the generalized position and velocity—states intrinsic to any dynamic system. For a knob with _n_ discrete positions, the force calculation follows: 


where the target position index is determined by: 


In practical implementation, this mechanism is adapted to MuJoCo as a `passive force` extension. 

### **A.4 Eccentric Mchanism** 

Planar eccentric motion can be mathematically represented through a planar transformation matrix, which admits the following decomposition: 


where _t_ denotes the throw of the eccentric. The right-hand side matrices correspond to the motions of two negatively-coupled hinge joints. Instruments employing eccentric mechanisms, such as vortex mixers, typically operate at high RPMs. Under these conditions, coupling two joints through equality constraints proves more robust than alternative solutions. 

12 

### **A.5 Quasi-static Liquid** 

The surface normal dynamics are governed by a damped spherical pendulum system. Following analytical mechanics conventions, we present the system’s Lagrangian and generalized force as: 


[ _ϕ, θ_ ] are the spherical coordinates of the normal vector and the generalized coordinates of the system. _l_ represents the characteristic length, and _m_ is system mass (which ultimately cancels out in the final equations). The vector _g_ = [ _gx, gy, gz_ ]<sup>_⊤_</sup> captures time-varying accelerations resulting from both gravity and inertial forces. _λϕ, λθ_ are configurable damping coefficients. Applying the Euler-Lagrange equation: 


we derive the following system of ordinary differential equations: 

In practical implementation, to avoid numerical instabilities when the system approaches simple pendulum behavior, we modify the denominator in the dd _t_<sup>_ϕ_˙ equation to</sup><sup>_ml_2 max</sup><sup>_{_sin2</sup><sup>_θ, ϵ}_.The</sup> system initializes with states aligned to gravity direction and zero velocity. The normal direction components are computed as: 


Following surface normal determination at each timestep, we compute the liquid body as the intersection between the oriented halfspace and the container’s inner surface. This implementation involves computing triangle-plane relations for the manifold mesh. Surface height computation proceeds through volume conservation constraints, employing the previous height as an initial guess before refining via Newton-Bisect search. 

### **A.6 Rendering** 

The MuJoCo renderer utilizes the legacy OpenGL fixed-function pipeline for scene rendering, which offers limited customization capabilities. Notably, its reliance on fixed-function lighting creates visual inconsistencies between textured and untextured surfaces under specular and ambient lighting conditions. For this renderer, we provide best-effort support, with certain scene elements (such as liquid representations) appearing in simplified forms to minimize visual artifacts. 

We develop a bridging mechanism to translate MuJoCo’s scene definition ( `MjModel` ) and simulation state ( `MjData` ) into Blender’s environment. While conceptually similar to MuJoCo’s ongoing USD (Universal Scene Description) exporter, our solution specifically accommodates our workflow by enabling: (1) Importation of tuned assets from Blender gallery files, and (2) Direct generation of fully configured Blender scenes capable of rendering features beyond MuJoCo’s representational capacity. 

### **A.7 Reactive UI** 

Our user interfaces currently operate in retained mode, meaning it only repaints when changes occur. For the MuJoCo renderer, UI updates in the 3D environment are achieved through calls to `mjr_uploadTexture` following repainting. In the Blender renderer, the UI is passed to the `Image Texture` node as either static images or video streams. 

13 

## **B Experiment Details** 

### **B.1 Demonstration Synthesis** 

For motion planning, AutoBio integrates inverse kinematics (IK) solvers with time-optimal path parameterization (TOPP) to produce collision-free trajectories that respect dynamic constraints. Robot control for these demonstrations is achieved via proportional-derivative (PD) controllers with tunable gains, balancing precision and stability. 

For the Aloha arm, since it forms a spherical wrist, we implement an analytical IK solver to improve robustness. For UR5e arm, we use our optimization-based IK solver due to its larger joint range. 

### **B.2 Benchmark Tasks** 

In the experiment section, we evaluated VLA capabilities across 9 AutoBio tasks. Below we describe the details of each task. 


**Close thermal cycler lid** (easy, _∼_ 20 s): _“close the lid of the thermal cycler”_ Close and lock the thermal cycler lid using a _UR5e-Robotiq_ robot, testing trajectory following for articulated object manipulation. The joint angles of the robotic arms are perturbed to add randomness to the task. This randomization also applies to all tasks below. 


**Open thermal cycler lid** (easy, _∼_ 17 s): _“open the lid of the thermal cycler”_ Unlock and open the thermal cycler lid using a _UR5e-Robotiq_ robot, testing trajectory following for articulated object manipulation. 


**Pick up centrifuge tube** (easy, _∼_ 10 s): _“pick up the centrifuge tube on the rack”_ Pick up a centrifuge tube from its rack using an _Aloha_ robot, focusing on basic visual positioning. The tube is placed in a random rack slot to promote generalization. This also applies to all tasks below involving tubes and racks. 

14 


**Unscrew centrifuge tube cap** (medium, _∼_ 27 s): _“dual-Aloha arms unscrewing centrifuge tube cap: one stabilizes tube while the other twists cap”_ Remove the centrifuge tube cap using two _Aloha_ robots. This evaluates dual-arm coordination and manipulation precision. 


**Aspirate with pipette** (medium, _∼_ 14 s): _“dual-UR5e pipetting: one arm lifts centrifuge tube, the other aligns pipette tip and aspirates liquid”_ Aspirate liquid from a tube using a _UR5e-Robotiq_ (holder) and _UR5e-DexHand_ (pipette operator). This tests dual-arm coordination, precision, and visual reasoning. The liquid volume in the tube is randomized to test liquid level sensing capabilities. 


**Transfer centrifuge tube** (medium, _∼_ 11 s): _“pick up the centrifuge tube and move it to the other rack, row_ _`{target_row}` , column_ _`{target_col}` ”_ Transfer a tube to a specified rack slot using a _UR5e-Robotiq_ robot, requiring precise manipulation, visual positioning, and language instruction following. The target rack slot is randomized to verify instruction following. 


**Screw on centrifuge tube cap** (hard, _∼_ 31 s): _“dual-Aloha arms screwing on centrifuge tube cap: one grips tube while the other twists cap”_ The inverse of unscrewing, but with stricter precision requirements for proper alignment. 

15 


**Operate thermal mixer panel** (hard, _∼_ 16 s): _“Adjust thermal mixer parameters, with speed set to_ _`{set_rpm}` rpm, temperature set to_ _`{set_temp}` °C, and time set to_ _`{set_time}` seconds”_ Set parameters (time, temperature, frequency) on a mixer panel using a _UR5e-Robotiq_ robot following language instruction and UI feedback, evaluating visual reasoning, language understanding, and high-precision manipulation. The parameters are randomized to test cross-modal reasoning. 


**Load centrifuge rotor** (hard, _∼_ 11 s): _“Insert a second centrifuge tube into the slot that is symmetrically opposite to the currently placed tube”_ Load a tube into the correct rotor slot while maintaining symmetry with the existing tube, testing advanced visual reasoning and precise positioning. The target rotor slot are randomized by setting the currently placed tube to different slots, and the rotor angle are also randomized. 

The evaluation time limits extended by approximately 50 % compared to demonstration horizon to accommodate imperfect policy execution. All tasks except **Operate thermal mixer panel** are scored binarily (1 for success, 0 for exceeding time limit) based on pose and contact requirements at checkpoints and terminal states. For **Operate thermal mixer panel** , we implement a weighted relative progress score to better reflect performance difference due to observed policy difficulties: 


normalized to [0 _,_ 1]. 

### **B.3 Baselines** 

We summarize key differences of our baselines ( _π_ 0 and RDT) in Table 5, where some of them (proprioception dimensions, image history, normalization) lead to difference in data adaptation. 

Table 5: Key differences between _π_ 0 and RDT baselines 

||_π_0|RDT|
|---|---|---|
|Architecture|Decoder-only|Encoder-decoder|
|Vision backbone|SigLIP So400m/14 224|SigLIP So400m/14 384|
|Language backbone|Gemma 2B+300M|T5 v1.1 XXL|
|Trainable weights|Full|V & L backbone frozen|
|Action sampling|Flow matching|Diffusion|
|Normalization|All|Gripper width only|
|State dimension|32|128|
|Action horizon|50|64|
|Image history|0 (None)|1|


16 


Figure 7: Loss curves of _π_ 0 on 9 tasks evaluated. The solid line shows the mean over 3 runs; the shaded region indicates the _±_ 1 _σ_ confidence interval. 

### **B.4 Training curves** 

Figures 7, 8, and 9 present the training loss curves for _π_ 0, RDT, and the task concatenation experiment, respectively. Several observations can be made: 

- The training loss curves of _π_ 0 generally exhibit smoother convergence compared to those of RDT. 

- The **Operate thermal mixer panel** task induces noticeable oscillations in the training curves for both _π_ 0 and RDT. 

- For _π_ 0, dual-arm tasks—particularly those involving the two screw operations—tend to overfit more easily when trained on limited data. 

17 


Figure 8: Loss curves of RDT on 9 tasks evaluated. The solid line shows the mean over 3 runs; the shaded region indicates the _±_ 1 _σ_ confidence interval. 

18 


Figure 9: Loss curves for the task concatenation experiment. The solid line shows the mean over 3 runs; the shaded region indicates the _±_ 1 _σ_ confidence interval. 

19 

