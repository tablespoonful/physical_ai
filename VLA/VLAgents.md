---
title: "VLAgents: A Policy Server for Efficient VLA Inference"
date: "2026-01-16"
authors: "Tobias Jülg; Khaled Gamal; Nisarga Nilavadi; Pierre Krack; Seongjin Bien; Michael Krawez"
url: https://arxiv.org/abs/2601.11250
pdf: https://arxiv.org/pdf/2601.11250
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.11250)** / [論文ページ](https://arxiv.org/abs/2601.11250)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **VLAgents: A Policy Server for Efficient VLA Inference** 

Tobias J¨ulg<sup>1</sup> , Khaled Gamal<sup>1</sup> , Nisarga Nilavadi<sup>1</sup> , Pierre Krack<sup>1</sup> , Seongjin Bien<sup>1</sup> , Michael Krawez<sup>1</sup> , Florian Walter<sup>1</sup><sup>_,_2</sup> and Wolfram Burgard<sup>1</sup> 

> 1University of Technology Nuremberg 2Technical University of Munich 

**_Abstract_ — The rapid emergence of Vision-Language-Action models (VLAs) has a significant impact on robotics. However, their deployment remains complex due to the fragmented interfaces and the inherent communication latency in distributed setups. To address this, we introduce VLAgents, a modular policy server that abstracts VLA inferencing behind a unified Gymnasium-style protocol. Crucially, its communication layer transparently adapts to the context by supporting both zerocopy shared memory for high-speed simulation and compressed streaming for remote hardware. In this work, we present the architecture of VLAgents and validate it by integrating seven policies—including OpenVLA and** _π_ 0 **. In a benchmark with both local and remote communication, we further demonstrate how it outperforms the default policy servers provided by OpenVLA, OpenPi, and LeRobot. VLAgents is available at github.com/RobotControlStack/vlagents.** 


Fig. 1. The architecture of VLAgents. Each environment implements a thin wrapper that translates observations and actions into the expected data format (see Fig. 2). A central control loop takes the state and forwards it via either shared memory or a TCP connection with JPEG-encoding to the policy server. The policy server uses the interface from Fig. 2 to run an inference pass with the corresponding model. This yields an action, which is then returned and used by the environment loop to step the environment to obtain the next state. 

## I. INTRODUCTION 

The model landscape for open-source robotics foundation models is becoming increasingly rich. Many models come with their own custom interfaces. Evaluating, benchmarking, or extending a model, therefore, often entails writing custom deployment code to connect it to other systems and frameworks. This makes a unified model interface highly desirable. Yet, only a few open source solutions exist so far, most prominently LeRobot’s Asynchronous Inference [1], which already has several models integrated behind a common policy server. However, it only defines a loose dictionarybased communication interface. 

In addition to code complexity, there is also a large system complexity in robotics: AI models and robot controllers often need to run on separate physical machines, sometimes even at a remote location, as models demand more and more GPU resources. Furthermore, as evaluation in simulation [2], [3], [4] becomes increasingly popular, the robot backend should also be easily exchangeable with a simulator. However, complex software dependencies can mutually exclude the installation of the model and simulator in the same Python environment [5]. A policy server appears to be the natural design choice for addressing these challenges. Many models, such as OpenVLA [6] and _π_ 0 [7], already ship with their own policy server to facilitate the execution on a physical robot that runs on a different machine or in a different Python environment, but they are model-specific. While modelagnostic frameworks exist, they are still in their early stages of development and often lack rigid interfaces and data-aware compression. 

In this work, we introduce _VLAgents_ , a model-agnostic Python-based inference server that provides a communication 

interface between models and robots. It provides an API that is similar to Gymnasium environments [8] and is specifically tailored for Vision-Language-Action models (VLAs). But in principle, VLAgents can be used with any type of model. It is comprised of a flexible policy server and a corresponding client that can communicate both over the network or via efficient shared memory if executed on the same machine. In addition, VLAgents comes with Slurm-compatible [9] CLI tools for checkpoint evaluations on clusters during training. 

## II. RELATED WORK 

The need for an isolated model environment has led to diverse client/server protocols. Most common are simple synchronous raw request-response protocols. Examples include OpenVLA [6], which leverages an HTTP server implemented in FastAPI, and the OpenPi model suite [7], [10], [11] with WebSocket communication. While they work well for deploying the respective models on real robot hardware, they introduce a substantial communication overhead when used for parallel evaluation in simulation, as the payload needs to be serialized and travel through the whole network stack. Using such model-specific servers, moreover, requires writing model-specific code for both simulation evaluation and real-world experiments. 

LeRobot [1] provides an asynchronous gRPC-based policy server implementation with a dictionary-based communication protocol, which is implemented for several models. Although the framework addresses both the interface and the communication issue, it neither provides efficient shared memory-based communication nor does it perform dataaware compression. While the approach is flexible, it requires 

special consideration during implementation: Since the dictionary keys are not standardized, both robots and models can require arbitrary keys for their actions and observations and considerable effort may be needed to map the keys between robots and models. There is also no explicit protocol layer that would allow the user to define this mapping in code, which makes it difficult to apply important transformations, e.g., normalization, to the data. 

_VLAgents_ addresses these gaps by defining a lightweight interface that transparently switches between highperformance shared memory (for simulation) and network streaming (for hardware) without code changes. It is data-aware, allowing it to compress high-volume image data via fast JPEG encoding, while also providing the flexibility to support new data types for special use cases. 

## III. METHODOLOGY 

VLAgents’ architecture is driven by two main use cases: The batched simulation evaluations on the cluster during training and the evaluation on physical and simulated robots for benchmarking. Therefore, the main design objectives are to provide a unified communication interface between environments, i.e., simulations or physical robot platforms, and VLA policies, and to enable remote policy execution based on a client/server architecture. 

We define a policy interface (see Fig. 2) that wraps VLAs similar to the Gymnasium environment API. It consists of three functions that perform model loading, resetting, and inference. It further defines special data structures for observations and actions. Data types required for VLAs, such as RGB input or action output, have their own dedicated typed attributes. We also define an info dictionary that can, if required, hold any type of data. This allows for compressing large data objects, such as images, while maintaining the flexibility to add custom data to the info dictionary. 

A policy server exposes this interface via RPyC (a TCPbased Remote Procedure Call library for Python) to a remote 

1 class Obs: 2 cameras: dict[str, np.ndarray] = {} 3 gripper: float | None = None 4 info: dict[str, Any] = {} 5 6 class Act: 7 action: np.ndarray 8 done: bool = False 9 info: dict[str, Any] = {} 10 11 class Agent: 12 def initialize(self): 13 """heavy intitilzation e.g. model loading""" 14 15 def act(self, obs: Obs) -> Act: 16 """forward pass""" 17 18 def reset(self, obs: Obs, instruction: Any, **<sup>kwargs)->dict[str,Any]:</sup> 19 """reset state, e.g. history""" 


Fig. 3. Mean Round-Trip Time (RTT) for different policy servers with two 224 _×_ 224 RGB cameras. Localhost indicates that the client and server are running on the same machine, while network indicates execution across different machines. For the network setting, the machines were connected in a Local Area Network with a 1 Gbit Ethernet connection. 

client. The client is connection-aware and avoids serialization by using shared memory when running on the same host as the server. Otherwise, RGB data are serialized using JPEG compression to reduce the data size for transport. VLAgents can be used standalone for standard client/server communication. Additionally, it can be used for automated evaluations as it provides an environment loop, Slurm and video recording utilities, as shown in Fig. 1. A wrapper layer is available to translate actions and observations into the required communication format. 

## IV. RESULTS AND CONCLUSION 

VLAgents currently integrates seven different policies, including Octo [12], OpenVLA [6], the OpenPi suite [7], [10], [11], Diffusion Policy [13] and V-JEPA 2 [14]. Methods that augment the input or output of the model, such as ARRO [15], have also been successfully evaluated. The library comes with out-of-the-box support for Maniskill 3 [16] environments as well as for the Robot Control Stack (RCS) [4] ecosystem, which supports four different robot arms for real-world and MuJoCo-simulated experiments. We also used VLAgents for RL-based finetuning of VLAs [5], which requires batched forward passes and a low communication overhead to prevent slowing down the training speed. 

Fig. 3 shows a comparison of plain Round-Trip Times (RTT) for client requests. The experiment evaluates the efficiency of the serialization and the transport protocol, skipping the model’s inference step on the server side. Out of the four policy servers tested, VLAgents achieves the best performance, both in the local and the network setting. It allows up to 220 Hz inference speed in the network deployment and introduces only 0.3 ms delay for simulated evaluations. 

In conclusion, VLAgents is an efficient policy server that provides a communication interface between VLAs and robot environments, both simulated and physical, and uses dataaware compression. Due to the usage of JPEG encoding and shared memory, VLAgents is faster than other commonly used policy servers by a factor of three. 

Fig. 2. VLA policy interface. 

REFERENCES 

- [1] R. Cadene, S. Alibert, A. Soare, Q. Gallouedec, A. Zouitine, S. Palma, P. Kooijmans, M. Aractingi, M. Shukor, D. Aubakirova, M. Russi, F. Capuano, C. Pascal, J. Choghari, J. Moss, and T. Wolf, “LeRobot: State-of-the-art machine learning for real-world robotics in pytorch,” https://github.com/huggingface/lerobot, 2024. 

- [2] X. Li, K. Hsu, J. Gu, O. Mees, K. Pertsch, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani _et al._ , “Evaluating real-world robot manipulation policies in simulation,” in _Proc. of the Conf. on Robot Learning (CoRL)_ , 2025. 

- [3] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems_ , 2023. 

- [4] T. J¨ulg, P. Krack, S. Bien, Y. Blei, K. Gamal, K. Nakahara, J. Hechtl, R. Calandra, W. Burgard, and F. Walter, “Robot Control Stack: A lean ecosystem for robot learning at scale,” https://arxiv.org/abs/2509. 14932, 2025. 

- [5] T. J¨ulg, W. Burgard, and F. Walter, “Refined Policy Distillation: From VLA generalists to RL experts,” in _Proc. of the IEEE/RSJ Int. Conf. on Intelligent Robots and Systems (IROS)_ , 2025. 

- [6] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” in _Proc. of the Conf. on Robot Learning (CoRL)_ , 2025. 

- [7] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ 0: A vision-language-action flow model for general robot control,” https: //arxiv.org/abs/2410.24164, 2024. 

- [8] M. Towers, A. Kwiatkowski, J. Terry, J. U. Balis, G. D. Cola, T. Deleu, M. Goul˜ao, A. Kallinteris, M. Krimmel, A. KG, R. Perez-Vicente, A. Pierr´e, S. Schulhoff, J. J. Tai, H. Tan, and O. G. Younis, “Gymnasium: A standard interface for reinforcement learning environments,” https://arxiv.org/abs/2407.17032, 2024. 

- [9] A. B. Yoo, M. A. Jette, and M. Grondona, “Slurm: Simple linux utility for resource management,” in _Workshop on job scheduling strategies for parallel processing_ . Springer, 2003, pp. 44–60. 

- [10] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” https://arxiv.org/abs/2501.09747, 2025. 

- [11] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky, “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” https://arxiv.org/abs/2504.16054, 2025. 

- [12] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo, Y. L. Tan, L. Y. Chen, Q. Vuong, T. Xiao, P. R. Sanketi, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _Proc. of Robotics: Science and Systems (RSS)_ , 2024. 

- [13] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _Int. Journal of Robotics Research (IJRR)_ , 2023. 

- [14] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, Mojtaba, Komeili, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, S. Arnaud, A. Gejji, A. Martin, F. R. Hogan, D. Dugas, P. Bojanowski, V. Khalidov, P. Labatut, F. Massa, M. Szafraniec, K. Krishnakumar, Y. Li, X. Ma, S. Chandar, F. Meier, Y. LeCun, M. Rabbat, and N. Ballas, “V-JEPA 2: Self-supervised video models enable understanding, prediction and planning,” https://arxiv.org/abs/2506.09985, 2025. 

- [15] R. Mirjalili, T. J¨ulg, F. Walter, and W. Burgard, “Augmented Reality for RObots (ARRO): Pointing visuomotor policies towards visual robustness,” https://arxiv.org/abs/2505.08627, 2025. 

- [16] S. Tao, F. Xiang, A. Shukla, Y. Qin, X. Hinrichsen, X. Yuan, C. Bao, X. Lin, Y. Liu, T. kai Chan, Y. Gao, X. Li, T. Mu, N. Xiao, A. Gurha, V. N. Rajesh, Y. W. Choi, Y.-R. Chen, Z. Huang, R. Calandra, R. Chen, S. Luo, and H. Su, “ManiSkill3: GPU parallelized robotics simulation and rendering for generalizable embodied AI,” in _Proc. of Robotics: Science and Systems (RSS)_ , 2025. 

