---
title: "ARIES-Mission2: A Zero-Shot Vision-Language-Action Framework for Fast Large-Scale Aerial Mission Generation"
date: "2026-08-13"
authors: "Junhao Wei; Yanxiao Li; Haochen Li; Yifu Zhao; Dexing Yao; Baili Lu"
url: https://arxiv.org/abs/2608.12763
pdf: https://arxiv.org/pdf/2608.12763
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.12763)** / [論文ページ](https://arxiv.org/abs/2608.12763)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ARIES-Mission2: A Zero-Shot Vision-Language-Action Framework for Fast Large-Scale Aerial Mission Generation 

|1<sup>st </sup>Junhao Wei|2<sup>nd </sup>Yanxiao Li|3<sup>rd </sup>Haochen Li|4<sup>th </sup>Yifu Zhao|
|---|---|---|---|
|_Faculty of Applied Sciences_<br>_Macao Polytechnic University_<br>|_Faculty of Applied Sciences_<br>_Macao Polytechnic University_<br>|_Faculty of Applied Sciences_<br>_Macao Polytechnic University_<br>|_Faculty of Applied Sciences_<br>_Macao Polytechnic University_<br>|
|Macao, China<br>p2312195@mpu.edu.mo|Macao, China<br>P2525981@mpu.edu.mo|Macao, China<br>p2523372@mpu.edu.mo|Macao, China<br>p2523269@mpu.edu.mo|
|5<sup>th </sup>Dexing Yao|6<sup>th </sup>Baili L|u|7<sup>th </sup>Zikun Li|
|_Faculty of Applied Sciences_|_Faculty of Applied S_|_ciences_<br>_School o_|_f Economics and Management_|
|_Macao Polytechnic University_<br>Macao, China<br>P2522978@mpu.edu.mo|_Macao Polytechnic U_<br>Macao, Chin<br>18023304003@16|_niversity_<br>a<br>3.com<br>_Sout_<br>201|_h China Normal University_<br>Guangzhou, China<br>90731013@m.scnu.edu.cn|
|8<sup>th </sup>Yapeng Wang|9<sup>th </sup>Sio-Kei Im|10<sup>th </sup>Dingcheng Yang|11<sup>th </sup>Xu Yang*|
|_Faculty of Applied Sciences_<br>|_Macao Polytechnic University_<br>_In_|_formation Engineering School_|_Faculty of Applied Sciences_|
|_Macao Polytechnic University_<br>Macao, China<br>yapengwang@mpu.edu.mo|Macao, China<br>marcusim@mpu.edu.mo|_Nanchang University_<br>Nanchang, China<br>yangdingcheng@ncu.edu.cn|_Macao Polytechnic University_<br>Macao, China<br>xuyang@mpu.edu.mo<br>*Corresponding author|


**_Abstract_ —Multimodal Large Language Models (MLLMs) have shown strong semantic understanding capabilities, but their direct use in low-altitude Unmanned Aerial Vehicle (UAV) mission generation remains limited by weak spatial optimization and inefficient route planning. To address this issue, we propose ARIESMission2, a zero-shot Vision-Language-Action (VLA) framework that decouples visual-semantic perception from physical route optimization. Given natural-language instructions and satellite imagery, ARIES-Mission2 first uses DeepSeek-V3 for task parsing and Molmo-7B for zero-shot target grounding, and then converts detected pixel locations into GPS waypoints through geospatial interpolation. To reduce the redundant backtracking caused by raw VLM-generated visiting orders, the back end formulates multi-target UAV traversal as a Traveling Salesperson Problem (TSP) and compares four candidate routes, including the raw VLM order and the routes optimized by PSO, GPSO, and IPSO. The minimum-cost closed-loop route is then selected for mission generation. Experiments on the UAV-VLPA-nano-30 benchmark show that ARIES-Mission2 achieves a total flight distance of 62.43 km, reducing the route length by 21.6% compared with the unoptimized VLA baseline (79.66 km) and by 9.5% compared with manual human planning (69.00 km). The complete 30-task workflow takes 575.40 s, averaging 19.18 s per task, which is approximately 3.6 times faster than human expert planning. Component-level timing shows that VLM inference dominates the runtime with 19.02 s per task, while the TSP solver requires only 0.16 s per task. Scalability analysis further indicates that the TSP module maintains lower growth in computation time** 

This work was supported by the grant from Macao Polytechnic University (RP/FCA-06/2026) and Macao Science and Technology Development Fund (FDCT-MOST: 0018/2025/AMJ). 

**as the number of targets increases. These results demonstrate that coupling zero-shot visual grounding with lightweight route optimization can improve both efficiency and route quality for large-scale UAV mission generation.** 

**_Index Terms_ —UAV, LLM, VLA, metaheuristics, mission generation** 

## I. INTRODUCTION 

In recent years, Unmanned Aerial Vehicles (UAVs) have become indispensable in the low-altitude economy and widearea inspections. To enable natural human-robot interaction, Vision-Language-Action (VLA) models have emerged to map multimodal inputs directly into physical actions. This has further evolved into Vision-Language Navigation (VLN), requiring UAVs to conduct precise spatial reasoning and longhorizon exploration in complex environments. 

Academic exploration of Large Language Models (LLMs) in UAV control has been intensive. For instance, TypeFly (2023) addressed LLM generation latency by integrating the MiniSpec language, reducing response times by 62% [1]. Similarly, CityNavAgent (2025) utilized a Hierarchical Semantic Planning Module (HSPM) to decompose long-horizon tasks [2]. However, the MM-UAVBench benchmark (2025) systematically evaluated 16 models and revealed significant bottlenecks in perception and planning, noting that current MLLMs often struggle to output physically feasible navigation strategies due to spatial biases [3]. 

This ’semantic-to-physical’ disconnect highlights a core deficiency in spatial operations research. While VLMs can extract target coordinates via zero-shot capabilities, they lack the geometric optimization needed for efficient visiting sequences, often resulting in redundant backtracking. Fundamentally, multi-target UAV traversal is a Traveling Salesperson Problem (TSP) [4]. To compensate for MLLMs’ shortcomings in combinatorial optimization, we introduce metaheuristic algorithms, which provide a robust framework for finding nearoptimal solutions to NP-Hard problems [5] [6] [7] [8] within reasonable computational overhead [9] [10] [11] [12] [13]. 

To bridge this loop, this paper proposes ARIES-Mission2, which adopts a decoupled ’front-end visual semantic inference + back-end physical optimization’ architecture. The front end utilizes an LLM/VLM pipeline for target extraction, while the back end integrates three metaheuristic algorithms (PSO, GPSO, and IPSO) for route planning. Our main contributions are: 

- **Proposed the ARIES-Mission2 framework:** We decouple VLM perception from a metaheuristic TSP optimizer to resolve LLMs’ inherent defects in geometric reasoning. 

- **Achieved breakthrough flight efficiency:** On the UAVVLPA-nano-30 benchmark, ARIES-Mission2 reduced total flight distance to 62.43 km, significantly outperforming the pure VLA baseline (79.66 km) and human experts (69 km). 

- **Realized highly efficient automated deployment:** The system completed 30 complex scenarios in under 10 minutes (VLM: 9.51 min, TSP: 0.08 min), operating far faster than the 35 minutes required by manual expert planning. 

II. THE PROPOSED FRAMEWORK 

To address the shortcomings of large multimodal models in geometric computation for complex long-horizon spatial reasoning, this paper proposes a rapid large-scale UAV mission generation framework (ARIES-Mission2), as shown in Fig. 1. This framework adopts a decoupled architecture, dividing the system into three core stages: front-end vision-language inference based on multimodal large models, back-end global path optimization by a TSP Solver based on metaheuristic algorithms, and the rapid automatic generation and deployment of low-level UAV actions. 

## _A. Vision-Language Semantic Inference_ 

The core task of the front-end module is to transform unstructured natural language instructions input by human operators into discrete target point coordinates with precise geographic information. Given a sequence of natural language instruction sets _U_ = _{w_ 1 _, w_ 2 _,..., wm}_ input by a human, the system first invokes a large language model (DeepSeek V3) as a semantic parser to extract the task targets: 


where _O_ represents the specific target categories (e.g., ’buildings’) extracted from the instructions, and _N_ is the total number of such targets subsequently detected in the image. 

Subsequently, the Vision-Language Model (Molmo-7B) receives the extracted targets _O_ and the corresponding satellite image _Isat_ , precisely locating the pixel coordinate set of all targets on the 2D image plane: **C**<sup>_pix_</sup> = Ψ _Molmo_ ( _O, Isat_ ) = _{_ ( _u_ 1 _, v_ 1) _,_ ( _u_ 2 _, v_ 2) _,...,_ ( _uN, vN_ ) _}_ (2) 

To eliminate physical computation deviations caused by image resolution and scale, the system extracts the geographic metadata (latitude and longitude boundaries) embedded in the satellite image and utilizes a linear interpolation function Γ _geo_ to map the 2D pixel coordinates into real-world Global Positioning System (GPS) coordinates: 


where _ϕi_ and _λi_ represent the true latitude and longitude of target _i_ , respectively. This step establishes a highly precise geographic baseline for subsequent physical-level optimal path planning. 

## _B. TSP Solver based on Metaheuristics_ 

The extracted target physical coordinate set **C**<sup>_gps_</sup> , combined with the UAV takeoff point (Home, denoted as _H_ ( _ϕ_ 0 _, λ_ 0)), constitutes a typical Traveling Salesperson Problem (TSP) network. Fig. 2 is a schematic diagram of the **_TSP Solver_** with metaheuristic algorithms for solving the TSP problem in the ARIES-Mission2 framework. To calculate the most realistic flight cost, the TSP Solver internally employs the Haversine formula to compute the Earth’s spherical physical distance. For any two points _A_ ( _ϕA, λA_ ) and _B_ ( _ϕB, λB_ ), their physical distance _Dhav_ ( _A, B_ ) is calculated as follows: 


where _R_ = 6371 _._ 0 km is the Earth’s radius.For any visiting sequence encoding **X** = [ _x_ 1 _, x_ 2 _,..., xN_ ] containing _N_ targets (decoded into a discrete sequence in ascending order via the Random Key representation), the overall cost function _F_ ( **X** ) of the closed-loop flight is defined as: 


Since TSP is a classic NP-Hard problem, the search space experiences a factorial explosion as the number of target nodes _N_ increases. Therefore, this study proposes two improved metaheuristic algorithms (GPSO and IPSO). The back-end TSP Solver of this framework integrates these two improved Particle Swarm Optimization algorithms (GPSO and IPSO) along with the basic PSO [14] to rapidly compute the global near-optimal flight path. 


Fig. 1: Overview of the proposed ARIES-Mission2 framework. The system decouples zero-shot visual-semantic perception from physical route optimization. Natural-language instructions and satellite imagery are first processed by a large language model and a vision-language grounding model to extract target categories and pixel-level target locations, which are then converted into GPS waypoints. The back-end TSP solver optimizes the visiting order using metaheuristic route search, and the resulting waypoint sequence is transformed into executable UAV mission actions. 


Fig. 2: Internal workflow of the TSP solver. Given the UAV home position and unordered GPS waypoints, the solver computes geographic route costs using the Haversine distance and decodes continuous random-key representations into discrete visiting sequences. Four competing candidate routes are evaluated, including the raw VLM visiting order and the optimized routes generated by PSO, GPSO, and IPSO. The final closedloop route is selected by minimizing the route cost over all candidates. 

## _C. PSO_ 

Within the integrated algorithmic architecture, each evolution of the particle swarm relies on the core velocity 

and position update equations. In each iteration, based on its personal historical best position **Pbest** _i_ and the current population’s global best position **Gbest** , the particle calculates a new velocity **V**<sup>(</sup> _i_<sup>_t_+1)</sup> and updates its position **X**<sup>(</sup> _i_<sup>_t_+1)</sup> : **V**<sup>(</sup> _i_<sup>_t_+1)</sup> = **V**<sup>(</sup> _i_<sup>_t_)+</sup><sup>_c_1</sup><sup>_r_1(</sup><sup>**Pbest**</sup><sup>_i −_</sup><sup>**X**(</sup> _i_<sup>_t_))+</sup><sup>_c_2</sup><sup>_r_2(</sup><sup>**Gbest**</sup><sup>_−_</sup><sup>**X**(</sup> _i_<sup>_t_))(7)</sup> 


where the learning factors are _c_ 1 = _c_ 2 = 2 _._ 0; _r_ 1 _, r_ 2 _∼ U_ (0 _,_ 1) are random perturbation matrices following a uniform distribution, which endow the algorithm with the randomness to continuously oscillate and avoid local extrema in the multidimensional space. The velocity and position are ultimately constrained within legitimate ranges through boundary constraint functions. 

## _D. The proposed GPSO_ 

To guarantee global exploration capability in the early search stages and accelerate local exploitation in the later stages, GPSO introduces a dynamic inertia weight _w_ ( _t_ ) that decreases linearly with the iteration count _t_ : 


where inertia weight is _wmax_ = 0 _._ 9, and the minimum inertia weight is _wmin_ = 0 _._ 4. 

GPSO refines the initialization phase by introducing a Distance-based Heuristic strategy. The normalized distance vector **D** _norm_ from all target points to the takeoff point _H_ is calculated: 


During initialization, GPSO forces half of the particles to adopt a heuristic distribution with distance priors, while retaining a uniform random perturbation of 0 _∼_ 0 _._ 3 to maintain population diversity; the other half of the particles remain in a purely random state: 


## _E. The proposed IPSO_ 

First, during the population initialization phase, a Tent Chaotic Map is introduced to completely replace pseudorandom numbers, ensuring that the initial particles possess a higher degree of ergodicity within the global search space. A minor perturbation of _U_ ( _−_ 0 _._ 001 _,_ 0 _._ 001) is superimposed to avoid fixed points: 


Second, after executing the conventional position update **X**<sup>(</sup> _i_<sup>_t_+1)</sup> = **X**<sup>(</sup> _i_<sup>_t_)+</sup><sup>**V**</sup> _i_<sup>(</sup><sup>_t_+1)</sup> , IPSO innovatively concatenates a nonlinear L´evy perturbation position update equation [15] [16]. The Mantegna algorithm is utilized to generate a random step size _step_ following a L´evy distribution: 


To protect excellent path structures that have already converged, the system applies a linearly decaying step size weight _α_ ( _t_ ) and a random mask matrix **M** _mask_ following a 25% probability, formulating the final secondary position perturbation equation: 


This mechanism ensures that while particles are engaged in local exploitation, they still retain the capability to execute long-range random jumps (L´evy Flight Mutation), thereby fundamentally suppressing the phenomenon of premature convergence. 

## _F. Optimal Selection Mechanism_ 

This framework innovatively introduces an algorithmic competition mechanism. The system records in parallel the convergence results of the original VLM sequence (Raw), PSO, GPSO, and IPSO. Through strict cost value comparison, the absolute optimal sequence with the shortest global distance is extracted: 


## _G. Action Generation and MAVLink Deployment_ 

After obtaining the optimal GPS coordinate sequence, unlike traditional VLA systems that rely on network-side large language models to generate control code (which easily leads to high latency and action hallucinations), the ARIESMission2 system constructs a local deterministic mission parsing function for the **_Mission Encapsulator_** . This module directly encapsulates the optimal physical coordinates with preset UAV flight parameters (e.g., cruising altitude of 100m, landing commands, etc.) to locally generate a standard MAVLink (QGC WPL 110) waypoint mission file within milliseconds. This purely localized deployment strategy not only guarantees extremely high computational efficiency but also achieves absolute physical safety in planning and control, allowing it to be directly uploaded to the UAV flight control system for execution. 

## III. EXPERIMENTS 

All experiments were conducted on a workstation equipped with an Intel Xeon E5-2698 v4 CPU (256 GB RAM) and a single NVIDIA Tesla V100 GPU (32 GB). To comprehensively evaluate the ARIES-Mission2 framework, we designed multidimensional comparative experiments. These benchmark the metaheuristic-integrated variants (PSO, GPSO, and IPSO) against both the pure vision-language-action baseline (ARIESMission2 w/o MAs) and manual planning by an experienced human expert (HumanPlan). Fig. 3 illustrates a manually planned flight trajectory. 


Fig. 3: One of the flight trajectories manually planned by a human expert (HumanPlan). 

To balance computational latency and global search capability, hyper-parameters for all metaheuristic algorithms within the TSP solver are uniformly configured. Specifically, the population size ( _Pop_ ) is empirically set to 30, and the maximum number of iterations ( _Itermax_ ) is strictly defined as 150. These settings guarantee sufficient swarm diversity to escape local optima while achieving sub-second convergence, aligning perfectly with the real-time mission generation demands of the ARIES-Mission2 framework. 

## _A. Data Description_ 

To validate the effectiveness of the ARIES-Mission2 framework, this study utilizes the UAV-VLPA-nano-30 benchmark 

dataset shown in Fig. 4 [17], which comprises 30 complex low-altitude flight tasks. Based on high-resolution real-world satellite imagery, this dataset encompasses diverse spatial topological structures of targets, including random distributions and dense clusters. Each task is paired with natural language instructions and precise geographic metadata (GPS boundaries), requiring the system to accurately extract target points and plan a closed-loop trajectory. The core evaluation metrics are the total flight distance ( _Total_ ) and the average single-task flight distance ( _Average_ ) required for the UAV to traverse all targets. These metrics objectively quantify the planning efficiency of the framework in realistic physical environments. 


(a) Task1 

Fig. 4: Task examples of high-resolution satellite imagery from the UAV-VLPA-nano-30 benchmark dataset. 

## _B. Results Analysis_ 

The comparative results are shown in Table I and Fig. 5. The pure VLA baseline without a TSP Solver (ARIESMission2 w/o MAs) yielded the poorest performance (79.66 km total distance). To illustrate, we take Task 6 as an example. Fig. 6 demonstrates the targets detected by the VLA model. Next, the VLA module sequentially connects the detected targets to form a closed-loop path, as shown in Fig. 7. This constitutes the tasks and trajectories generated by ARIESMission2 without MAs. The VLA baseline generates chaotic, backtracking trajectories, exposing MLLMs’ severe deficiencies in optimal physical routing despite strong semantic perception. Conversely, human experts (HumanPlan) used spatial intuition to constrain the distance to 69.00 km, as illustrated in Fig. 9d. However, the full ARIES-Mission2 scheme (with the metaheuristic TSP Solver) drastically compressed the total distance to 62.43 km (2.08 km/task average). This reduces flight distance by 21.6% compared to the VLA baseline and 9.5% against human experts, demonstrating the framework’s transcendence in complex spatial planning. 

Algorithmic ablation using Task 6 (Fig. 8) elucidates the solvers’ dynamical differences. Standard PSO (Fig. 9a) shows weak global search due to random initialization, falling into a local optimum (1.94 km) behind the human expert (1.86 km). GPSO (Fig. 9b), using a distance heuristic, converges rapidly to surpass human planning at 1.85 km but quickly 

TABLE I: Comparison of Trajectory Lengths (km) across 30 Tasks. _Total_ stands for total distance of each method. _Average_ stands for average distance of each method. 

|**Task**|**AM2-PSO**|**AM2-GPSO**|**AM2-IPSO**|**AM2 (Optimal)**|**AM2 w/o MAs**|**HumanPlan**|
|---|---|---|---|---|---|---|
|1|1.81|1.79|1.81|**1.79**|2.08|1.84|
|2|2.44|2.37|2.48|2.37|3.44|**2.08**|
|3|2.67|2.62|2.66|2.62|2.70|**2.49**|
|4|2.33|2.32|**2.13**|**2.13**|2.39|2.17|
|5|1.97|2.31|**1.97**|**1.97**|2.56|2.13|
|6|1.94|1.85|**1.76**|**1.76**|2.36|1.86|
|7|1.84|1.84|**1.84**|**1.84**|1.95|1.94|
|8|3.34|3.35|2.60|2.60|4.33|**2.31**|
|9|2.62|**2.49**|2.52|**2.49**|3.31|2.71|
|10|2.38|2.44|2.52|2.38|3.55|**2.31**|
|11|2.78|2.78|**2.69**|**2.69**|2.90|3.16|
|12|1.68|1.61|**1.55**|**1.55**|2.21|1.87|
|13|**2.03**|2.24|2.14|**2.03**|2.62|2.30|
|14|**1.07**|**1.07**|**1.07**|**1.07**|1.29|3.71|
|15|2.14|2.21|**2.11**|**2.11**|2.44|2.39|
|16|2.28|**2.22**|2.26|**2.22**|2.44|2.54|
|17|**2.01**|**2.01**|**2.01**|**2.01**|2.63|2.49|
|18|3.59|2.96|**2.93**|**2.93**|3.96|3.01|
|19|1.91|1.91|1.91|1.91|1.96|**1.77**|
|20|2.19|2.19|**2.18**|**2.18**|2.33|2.40|
|21|2.25|**2.21**|2.24|**2.21**|2.50|2.63|
|22|**0.67**|**0.67**|**0.67**|**0.67**|**0.67**|1.13|
|23|**2.01**|**2.01**|**2.01**|**2.01**|2.01|2.04|
|24|**1.35**|**1.35**|**1.35**|**1.35**|1.55|1.25|
|25|**1.94**|**1.94**|**1.94**|**1.94**|2.18|1.98|
|26|2.40|2.67|**2.28**|**2.28**|3.51|2.33|
|27|**1.90**|**1.90**|**1.90**|**1.90**|2.51|2.12|
|28|2.19|2.24|**2.15**|**2.15**|3.12|2.42|
|29|4.27|3.45|**3.33**|**3.33**|5.91|3.50|
|30|**1.94**|2.15|2.19|**1.94**|2.25|2.12|
|**Total**|65.95|65.17|63.20|**62.43**|79.66|69.00|
|**Average**|2.20|2.17|2.11|**2.08**|2.66|2.30|


* AM2 stands for ARIES-Mission2. 


Fig. 5: Quantitative comparison of trajectory lengths across 30 benchmark tasks. The chart contrasts the flight distances generated by the unoptimized pure VLA baseline (ARIESMission2 w/o MAs), the full ARIES-Mission2, and the manual expert baseline (HumanPlan). 


Fig. 6: Target detection and spatial anchoring results for Task 6 using the DeepSeek-Molmo VLM module. All buildings are accurately identified within the satellite imagery under openvocabulary conditions. 


Fig. 7: The chaotic and redundant flight trajectory generated by the pure VLA baseline (ARIES-Mission2 w/o MAs). 

stagnates. In contrast, IPSO (Fig. 9c) demonstrates outstanding anti-premature convergence. By leveraging Levy Flight’s nonlinear mutation, IPSO successfully escapes local extrema traps, securing the global absolute optimal trajectory of 1.76 km. This validates IPSO’s indispensability for high-dimensional flight tasks. 


Fig. 8: Comparative convergence curves of the metaheuristic algorithms (PSO, GPSO, and IPSO) in Task 6. 

TABLE II: Comparison of computational latency between ARIES-Mission2 components and human expert planning across 30 tasks. 

|**Method**|**Pipeline Component**|**Total Time (s)**<br>**Avg. **|**Time/Task (s)**|
|---|---|---|---|
|Human Expert|Manual Route Planning|2100.00|70.00|
||VLM Visual Inference|570.60|19.02|
|ARIES-Mission2|TSP Solver|4.80|0.16|
||Complete Framework|**575.40**|**19.18**|


To evaluate scalability, we analyzed the latency growth rate (Computation Ratio) of the VLM and TSP Solver modules as targets increase, using the minimum target count (4 points) as a baseline (Fig. 10). As targets scale to 20, VLM computation time shows steep linear growth, approaching a 300% latency increase. In contrast, the TSP solver’s overhead growth remains stable at around 160%. This disparity highlights that the front-end VLM’s visual inference is the core computational 


(c) ARIES-Mission2-IPSO 

Fig. 9: Optimized flight trajectories for Task 6 generated by different planning strategies. PSO denotes the trajectory obtained using the standard PSO-based TSP solver, GPSO and IPSO denote enhanced PSO variants, while HumanPlan represents a baseline trajectory manually planned by an experienced human operator based on spatial intuition. 

bottleneck for real-time performance. Conversely, the metaheuristic TSP solver maintains high efficiency and outstanding scalability, fully meeting the demands for large-scale, real-time mission planning in seconds. 


Fig. 10: Computational scalability analysis showing the computation ratio relative to the number of targets ( _N_ ). 

## IV. CONCLUSION 

Addressing the deficiencies of multimodal large models in spatial optimization capabilities during wide-area UAV 

missions, this paper proposes a novel VLA framework ARIESMission2 for fast aerial mission generation that decouples visual semantic perception from low-level physical optimization. The front end of the system utilizes a large model to accurately extract the true geographic coordinates of targets, while the back end innovatively integrates multiple metaheuristic algorithms to lock in the global optimal flight route through dynamic algorithmic competition, locally generating directly deployable MAVLink missions within seconds. Real-world benchmark tests demonstrate that with a total flight distance of 62.43 km, this system not only substantially rectifies the chaotic trajectory backtracking caused by the direct inference of the pure large model (79.66 km), but also significantly surpasses experienced human experts (69.00 km) in overall flight distance optimization. Furthermore, computational complexity analysis confirms that the back-end optimization solver exhibits exceptionally outstanding scalability, effectively circumventing the surging front-end computational bottleneck associated with an increasing number of targets. Overall, this paper provides a novel paradigm for the highly efficient realworld implementation of multimodal large models in complex physical spaces. Future work will further introduce 3D terrain [18] [19] [20] and dynamic obstacle avoidance mechanisms [21] [22] to advance the fully autonomous application of embodied intelligence in low-altitude airspaces [23] [24] [25] [26]. 

## ACKNOWLEDGMENT 

This work (MPU submission code: fca.13ea.330d.3) was supported by the Macao Polytechnic University (RP/FCA06/2026) and Macao Science and Technology Development Fund (FDCT-MOST: 0018/2025/AMJ). 

## REFERENCES 

- [1] Chen G, Yu X, Ling N, et al. Typefly: Flying drones with large language model[J]. arXiv preprint arXiv:2312.14950, 2023. 

- [2] Zhang W, Gao C, Yu S, et al. Citynavagent: Aerial vision-andlanguage navigation with hierarchical semantic planning and global memory[C]//Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2025: 3129231309. 

- [3] Dai S, Ma Z, Luo Z, et al. MM-UAVBench: How Well Do Multimodal Large Language Models See, Think, and Plan in Low-Altitude UAV Scenarios?[J]. arXiv preprint arXiv:2512.23219, 2025. 

- [4] Wei J, Li Y, Zhao Y, et al. Landscape-Aware Bandit Hyper-Heuristics for Online Operator Selection in UAV Inspection Routing[J]. arXiv preprint arXiv:2605.14620, 2026. 

   - [10] Wei J, Gu Y, Yan Y, et al. LSEWOA: an enhanced whale optimization algorithm with multi-strategy for numerical and engineering design optimization problems[J]. Sensors, 2025, 25(7): 2054. 

   - [11] Lu B, Xie Z, Wei J, et al. MRBMO: An Enhanced Red-Billed Blue Magpie Optimization Algorithm for Solving Numerical Optimization Challenges[J]. Symmetry, 2025, 17(8): 1295. 

   - [12] Wei J, Zhang R, Gu Y, et al. A Geometric Whale Optimization Algorithm with Triangular Flight for Numerical Optimization and Engineering Design[J]. Scientific Reports, 2026. 

   - [13] Li Y, Wei J, Zhao Y, et al. DHCRWOA: adaptive whale optimization algorithm with Cauchy-Rayleigh distribution for numerical and engineering design optimization[J]. Scientific Reports, 2026. 

   - [14] Kennedy J, Eberhart R. Particle swarm optimization[C]//Proceedings of ICNN’95-international conference on neural networks. ieee, 1995, 4: 1942-1948. 

   - [15] Wei J, Gu Y, Xie Z, Yan Y, Lu B, Li Z, Cheong N, et al. (2025) LSWOA: An enhanced whale optimization algorithm with Levy flight and Spiral flight for numerical and engineering design optimization problems. PLoS One 20(9): e0322058. 

   - [16] Li Z, Zhu W, Zhang R, et al. ASKSSA-CNN-BiLSTM: A Novel Time Series Forecasting Model for Stock Price Prediction Based on An Enhanced Sparrow Search Algorithm[C]//2026 2026 6th Asia Conference on Information Engineering (ACIE) ACIE. Nanyang Technological University, Singapore, 2026: 20-26. 

   - [17] Sautenkov O, Yaqoot Y, Lykov A, et al. UAV-VLA: Vision-languageaction system for large scale aerial mission generation[C]//2025 20th ACM/IEEE International Conference on Human-Robot Interaction (HRI). IEEE, 2025: 1588-1592. 

   - [18] Wei J, Zhu W, Xu Q, et al. GeoSSA: Geometric Sparrow Search Algorithm for UAV Path Planning and Engineering Design Optimization[J]. arXiv preprint arXiv:2601.19346, 2026. 

   - [19] Wu S, Li Q, Wei W. Application of ant colony optimization algorithm based on triangle inequality principle and partition method strategy in robot path planning[J]. Axioms, 2023, 12(6): 525. 

   - [20] Wei J, Li Y, Mirjalili S, et al. CICDWOA: A Collective Cognitive Sharing Whale Optimization Algorithm with Cauchy Inverse Cumulative Distribution for 2D/3D Path Planning and Engineering Design Problems[J]. arXiv preprint arXiv:2603.20501, 2026. 

   - [21] Xu Z, Han X, Shen H, et al. Navrl: Learning safe flight in dynamic environments[J]. IEEE Robotics and Automation Letters, 2025. 

   - [22] Yao D, Li H, Wei J, et al. KIO-planner: Attention-Guided Single-Stage Motion Planning with Dual Mapping for UAV Navigation[J]. arXiv preprint arXiv:2605.19703, 2026. 

   - [23] Zhou X, Wang Z, Ye H, et al. Ego-planner: An esdf-free gradient-based local planner for quadrotors[J]. IEEE Robotics and Automation Letters, 2020, 6(2): 478-485. 

   - [24] Wei J, Li Y, Yao D, et al. SAGA: A Robust Self-Attention and GoalAware Anchor-based Planner for Safe UAV Autonomous Navigation[J]. arXiv preprint arXiv:2605.02301, 2026. 

   - [25] Lu J, Zhang X, Shen H, et al. You only plan once: A learning-based onestage planner with guidance learning[J]. IEEE Robotics and Automation Letters, 2024, 9(7): 6083-6090. 

   - [26] Xie Z, Lu B, Gu Y, et al. Research on UAV Applications in Public Administration: Based on an Improved RRT Algorithm[J]. arXiv preprint arXiv:2508.14096, 2025. 

- [5] Gu Y, Wei J, Li Z, Lu B, Pan S, Cheong N (2025) GWOA: A multistrategy enhanced whale optimization algorithm for engineering design optimization. PLoS One 20(9). 

- [6] Wei J, Gu Y, Zhang R, et al. An Enhanced Whale Optimization Algorithm with Log-Normal Distribution for Optimizing Coverage ofWireless Sensor Networks[C]//AIIPCC 2025; AIIPCC 2025. VDE, 2025: 138147. 

- [7] Zhao Y, Zou X, Wei J, et al. WASHH: An Anchor-Aware WhaleGuided Selection Hyper-Heuristic for Continuous Optimization and SVC Configuration[J]. arXiv preprint arXiv:2605.28844, 2026. 

- [8] Wei J, Li Y, Zhao Y, et al. Low-Cost Labels, Reliable Choices: RolloutCalibrated Hyper-Heuristics for Job Shop Scheduling[J]. arXiv preprint arXiv:2605.23957, 2026. 

- [9] Wei J, Gu Y, Law K L E, et al. Adaptive position updating particle swarm optimization for UAV path planning[C]//2024 22nd International Symposium on Modeling and Optimization in Mobile, Ad Hoc, and Wireless Networks (WiOpt). IEEE, 2024: 124-131. 

