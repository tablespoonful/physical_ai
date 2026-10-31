---
title: "From World Models to World Action Models: A Concise Tutorial for Robotics"
date: "2026-07-01"
authors: "Xiaoxiong Zhang; Xiong Zeng; Wei Zhang"
url: https://arxiv.org/abs/2607.00836
pdf: https://arxiv.org/pdf/2607.00836
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.00836)** / [論文ページ](https://arxiv.org/abs/2607.00836)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **From World Models to World Action Models: A Concise Tutorial for Robotics** 

**Xiaoxiong Zhang**<sup>1</sup> , **Xiong Zeng**<sup>1</sup> , and **Wei Zhang**<sup>1 2</sup> 

## **Abstract** 

Rather than providing an exhaustive survey, this paper presents a concise tutorial on world models and world action models for robotics. After reading the tutorial, readers should have a clear understanding of what constitutes a ”world”, how world models and world action models are defined, and what roles they play within robotic AI systems. The tutorial also develops a unified perspective for comparing representative approaches, such as World Labs’ spatial intelligence models, Yann LeCun’s JEPA framework, and NVIDIA’s Cosmos platform, and clarifies how these models differ in their representations, predictive capabilities, and interaction mechanisms. 

Github page: World (Action) Models. 

## **1. Foundations: World, Task, Policy, and Models** 

Predicting how the world evolves under actions is a central capability for physical artificial intelligence (AI) and generative simulation. In these scenarios, the predictive models can support controller design, planning, decision making, and policy learning. Recently, the terms world model and world action model have been used to describe a broad range of methods, including latent dynamics models, video prediction models, physics-informed simulators, and action-conditioned generative models. However, these methods differ substantially in what they model, what they predict, and how their predictions are used. This motivates a unified definition and taxonomy of world (action) models. 

### **1.1. World** 

We define a _world_ as the set of task-relevant entities, including both the _robot_ and its _environment_ . The environment contains the _objects of interest_ and the _ambient environment_ , as shown in Fig. 1. 

1School of Automation and Intelligent Manufacturing, Southern University of Science and Technology, Shenzhen, China<sup>2</sup> LimX Dynamics, Shenzhen, China. Correspondence to: Xiaoxiong Zhang _<_ 12433017@mail.sustech.edu.cn _>_ . 


_Figure 1._ Illustration of the components of a world. 


_Figure 2._ Physical AI tasks: Autonomous driving and robotic tablecleaning. 

### **1.2. Physical AI Task and Policy** 

We define the _world state_ as the joint task-relevant state of the robot, objects, and the surrounding environment. A _physical AI task_ is to design a policy that drives the world from an initial state toward a goal set while satisfying task-specific constraints. Different tasks induce different choices of relevant entities, state variables, objectives, and constraints. Fig. 2 provides two examples of task-specific worlds: 

_Autonomous driving task._ In the autonomous driving task, the world consists of the vehicle, all relevant traffic participants, and the surrounding environment. The task is to design a driving policy that moves the vehicle from an initial location A to a target location B, while avoiding collision throughout the journey. 

_Robotic table-cleaning task._ In the robotic table-cleaning task, the world includes the robot and all relevant objects such as dishes, a rag, a table, and a household environment, and the objective is to rearrange objects into acceptable 

1 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 

states (e.g., dishes placed in a sink). 


sent object poses, object velocities, a latent state, or other variables relevant to the task. We discuss world models in more detail in Sec. 2. 


_Figure 3._ A policy framework for accomplishing physical AI tasks. 

_Figure 5._ Examples of world models. 

Fig. 3 illustrates a policy framework that maps human intent (e.g., driving from A to B in the autonomous driving task) and the current observation _ot_ to a robot action _at_ . This mapping may be realized by a modular decision–planning–control pipeline, a fast–slow architecture, or an end-to-end policy, depending on the task and the available data. Low-level control modules may use methods such as PID or MPC, whereas learned action-generation components may adopt architectures such as VLA models or world action models. These choices concern different architectural and methodological dimensions rather than different functional definitions of a policy. 

### **1.3. World Models and World Action Models** 

For a specified world, a world model predicts how the observation prediction ˆ _ot_ +1 or state prediction _xt_ +1 evolve under candidate actions _at_ , typically conditioned on the current observation _ot_ , as illustrated in Fig. 4. 


_Figure 4._ World (action) models. 

The world model (WM) may take different forms, including symbolic dynamics equations, neural network dynamics models, or diffusion-based video predictors, as shown in Fig. 5. The observation _ot_ and the observation preidction _o_ ˆ _t_ +1 may comprise the robot’s proprioceptive observations as well as environmental observations of the surrounding environment, such as RGB or RGB-D images or point clouds. The action _at_ might range from a concrete robot action to an abstract language-level instruction or a camera pose to observe the environment. The state prediction _xt_ may repre- 

A _world action model_ (WAM) is a policy whose action generation is coupled, during inference, with observation prediction, as shown in Fig. 4. This coupling may be explicit, latent, joint, or auxiliary. A world action model therefore need not contain a separate world model at inference time. 

### **The differences between WM and WAM** are summarized as follows: 

_Primary objective._ A world model aims to model the evolution of the environment by predicting future observations or states, typically conditioned on the current observation and the current action. In contrast, a world action model serves as a policy for accomplishing a physical AI task: it predicts actions that are expected to drive the world toward a desired future state or observation. 

_System role._ A world model primarily addresses environment modeling and prediction, whereas a world action model addresses decision-making and control. Although a world action model may internally use a world model for planning or action evaluation, this is not a necessary architectural requirement. 

_Architectural implication._ A world model does not, by itself, constitute a policy or controller. To complete a physical AI task, the predictive capability of a world model must therefore be coupled with an additional planning, decisionmaking, or control mechanism. 

Our taxonomy of world action models focuses primarily on recent video-based robotic policies, where future visual prediction is coupled with action generation. Classical modelbased control and model-based reinforcement learning are discussed only when they clarify this connection. 

Further details about world action models are provided in Sec. 3. 

**The differences between WAM and VLA:** A VLA typically learns a direct mapping from multimodal observations and language instructions to robot actions, emphasizing end-to-end policy learning. In contrast, a WAM explicitly reasons about how actions transform the world toward a desired future state, often leveraging predictive world rep- 

2 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 

resentations to evaluate, plan, or generate actions. Taking Fig. 4 as a comparison example, the VLA takes only the action _at_ as output and its output does not include the observation prediction ˆ _ot_ +1. 

## **2. A Design-Space View of World Models** 

While Sec. 1.3 shows a world model abstractly as an actionconditioned predictive model, existing world models can be broadly categorized according to the space in which prediction is performed. A one-step world model can be written as 


where _pθ_ denotes a parameterized predictive model, _yt_ +1 denotes the prediction target, which could be the observation prediction ˆ _ot_ +1 or the state prediction _xt_ +1. When _yt_ +1 = _o_ ˆ _t_ +1, we refer to the model as an _observation-space_ world model. Similarly, when _yt_ +1 = _xt_ +1, we call it a _statespace world model_ . More generally, the prediction target can be a prediction trajectory, such as _yt_ +1: _t_ + _H_ . 

### **2.1. Observation-space World Models** 

An observation-space world model predicts future observations directly in the observation space under a given action. Given the current observation _ot_ and an action _at_ , the model estimates the predictive distribution of the next observation: 


where _pθ_ is typically parameterized by a neural network. Under this formulation, the design space of observationspace world models can be largely characterized by two axes: the type of observation being predicted and the level of abstraction of the action conditioning, as illustrated in Fig. 6. 

**Observation representation.** Observation representations can be classified according to how explicitly they encode the spatial structure of a scene: 

_RGB images._ RGB images are the most common representation because they are easy to collect, require inexpensive and widely available sensors, and are abundant in Internetscale video data [1; 4; 8; 10; 11; 25; 33; 36; 39; 41; 48]. However, they encode the spatial structure of a scene only implicitly. 

_Multi-view RGB images._ Multi-view RGB images capture a scene from multiple viewpoints and provide additional geometric constraints for spatial understanding [9; 14; 18]. 

_RGB-D images._ RGB-D images augment visual appearance with explicit depth information, making them suitable for spatial reasoning and robotic manipulation [5; 13; 40; 54; 55]. Spatially explicit data are much less available at scale than ordinary RGB videos. A common compromise 

is to annotate large-scale RGB videos with depth estimated by monocular vision models, thereby constructing pseudoRGB-D training data [13; 40; 54; 55]. 

_Point clouds._ Point clouds directly represent the threedimensional geometry of a scene and provide a highly spatially explicit observation representation [19; 20]. 

**Action representation.** On the action side, the choice of action representation is closely tied to the intended role of the world model. While the observation type determines what form of future is predicted, the action type largely determines how the model can be used. A more concrete action representation usually makes the model suitable for control and simulation, whereas a more abstract action representation often shifts the model toward pretraining or planning. 

_Robot action._ At the most concrete level, actions correspond to low-level robot commands, such as joint commands, endeffector actions, or continuous control signals [11; 13; 14; 19; 20; 39; 40]. Since these actions are directly grounded in the embodiment of the robot, the resulting world model can predict the physical consequence of executing a specific control command. Such models are therefore commonly used as learned simulators for model-predictive control [13; 19; 20; 39], policy evaluation [14; 40], or synthetic data generation [14; 40]. 

_Interface action._ At the next level, interface actions provide a controllable way to interact with the visual world without specifying the low-level motor commands of a particular embodiment. For example, given an initial image or scene context, the model may take user-level control signals, camera-control commands, or viewpoint-control inputs, and then synthesize the corresponding future observations [1; 41; 48]. The purpose of this type of world model is not to predict robot dynamics, but to turn a static or partially observed scene into an interactive visual environment. It therefore serves as an interface-driven visual simulator, where users or robots can control how the scene is observed and obtain temporally consistent observations under different interactions. 

_Latent action._ Another line of work introduces latent actions, which are learned from unlabeled videos through reconstruction objectives with an information bottleneck [10; 11]. Here, the action is not provided by the dataset, but inferred as a compact variable that explains the visual transition between frames. This design is mainly motivated by pretraining: by replacing missing action labels with learned latent actions, the world model can exploit large-scale action-free video data and acquire general dynamics priors before being adapted to downstream tasks. 

_Language._ At the most abstract level, actions can be represented as language instructions. Language-conditioned world models are less grounded in precise low-level control, but they are useful for high-level visual planning. Given 

3 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 


_Figure 6._ Design space of observation-space world models. The vertical axis denotes the spatial explicitness of the observation, ranging from RGB images to multi-view RGB, RGB-D, and point clouds. The horizontal axis denotes the abstraction level of the action conditioning, ranging from low-level robot actions to interface actions, latent actions, and language instructions. Different choices along these two axes lead to different trade-offs between spatial understanding, data availability, and downstream usability. 

a task description, such models generate possible future observations that describe how the task may unfold or be completed, thereby providing visual guidance for downstream robots [4; 5; 8; 9; 18; 25; 33; 36; 54; 55]. 

These action representations form a hierarchy ranging from low-level motor control to high-level semantic instructions. 

### **2.2. State-space World Models** 

Predicting future observations directly in the observation space is a natural formulation, but it is often difficult to learn because raw observations are high-dimensional and contain many task-irrelevant variations, such as background changes, illumination, texture, or sensor noise. As a result, modeling dynamics directly in the observation space may force the model to explain unnecessary visual details rather than the task-relevant evolution of the world. Statespace world models address this issue by first abstracting observations into a more compact and structured state representation, and then predicting the future evolution in this state space: 

_xt_ +1 _∼ pθ_ ( _· | ot, at_ ) _,_ 

where _xt_ +1 denotes the state prediction of interest, which may be a latent vector, a set of tracked points, a collection of symbolic predicates, or physical state variables. Unlike observation-space world models, the transition model _pθ_ is not necessarily restricted to a neural network. Depending on the choice of state representation, the transition model 

may be implemented as a neural network, a symbolic or neural-symbolic operator model, or a physics-based simulator. By predicting structured states instead of raw observations, state-space world models reduce the complexity of dynamics learning and focus the prediction on task-relevant or physically meaningful aspects of the world. As illustrated in Fig. 7, existing state-space world models can be organized according to the type of state representation they use. 

**Latent state model.** A major class of state-space world models uses latent states, where observations are encoded into latent vectors by neural networks [2; 12; 15; 16; 21; 22; 35; 49; 52; 58]. These latent states can be obtained in different ways. Some methods learn the latent representation directly from the target domain, for example through reconstruction-based objectives [15; 49] or through predictive objectives that model future latent states without reconstructing pixels [2; 12; 16; 35]. Such representations are usually adapted to the specific environment, task distribution, and control setting. Other methods use pretrained visual or vision-language models to extract latent features as state representations [21; 22; 52; 58]. Since these encoders are trained on large-scale Internet data, the resulting states often provide more general semantic and visual abstractions. Latent-state world models are commonly paired with robot actions and are often used as compact learned simulators for reinforcement learning, or model-predictive control. 

4 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 


_Figure 7._ Design space of state-space world models. Instead of predicting future observations directly in the raw observation space, state-space world models abstract observations into structured state representations and model their future evolution under actions. Representative state choices include latent states, point tracks, neural-symbolic predicates, and physical states. Different state representations provide different trade-offs between compactness, semantic structure, physical interpretability, scalability, and downstream usability. 

**Point track model.** Another line of work represents the state as point tracks [46; 47; 50; 57]. These points can be two-dimensional [46; 47; 50] or three-dimensional [57], randomly sampled [47] or semantically selected [46; 50; 57], and their trajectories describe how task-relevant parts of the scene move over time. Compared with raw image prediction, point-track prediction removes much of the irrelevant background variation while preserving explicit motion information in the scene. This makes the future representation more compact and structured, without requiring the model to generate full visual observations. However, the choice of points also introduces an additional structural prior: although this prior can simplify learning, it may reduce scalability when the relevant scene elements are hard to define or vary significantly across tasks. In many applications, point-track world models are conditioned on language instructions and predict how key points in the scene should move in order to accomplish the task. The predicted tracks can then be used as reference trajectories or intermediate goals for a downstream controller. 

**Neural-symbolic model.** Neural-symbolic world models use a set of grounded predicates as the state representation [31; 32]. A neural-symbolic predicate is a symbolic Boolean fact whose truth value is grounded in raw perception by a neural model. This representation maps continuous visual observations into a compact set of logical facts that can support reasoning and planning. In this setting, actions are usually high-level skills rather than low-level motor commands. The transition model describes the preconditions and effects of these skills over the predicate state, similar in spirit to symbolic planning models such as PDDL, but with predicates grounded in perception. The goal of this type of world model is to learn a compact symbolic abstraction 

for long-horizon planning. By representing skills through their preconditions and effects, neural-symbolic world models support compositional reasoning, efficient search, and interpretable planning over high-level task structures. 

**Physical state model.** A further class of state-space world models is based on physical states and classical mechanics [23; 28; 43; 45]. Instead of learning arbitrary latent dynamics from data, these methods explicitly represent the world using physical variables such as object poses, velocities, contact states, masses, friction coefficients, or other dynamics parameters. This formulation incorporates strong human priors about how the physical world evolves, and is closely related to the modeling assumptions used in physics simulators. A typical pipeline first reconstructs the target scene in 3D, then aligns a simulated environment with the real scene by replaying real interaction trajectories and optimizing dynamics and rendering parameters. Once the simulator is aligned, future states can be predicted by solving physics-based transition equations conditioned on the current physical state and the robot action. Such world models are especially useful for model-predictive control, reinforcement learning, and synthetic data generation, where accurate physical rollouts are more important than directly generating raw visual observations. 

## **3. World Action Models** 

The previous section categorizes world models according to their prediction space. We focus on video-based world action models that incorporate future-oriented visual modeling in one of four ways: explicit future generation, conditioning on predictive video features, joint video-action generation, or auxiliary future prediction during policy training. In phys- 

5 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 

ical decision making, prediction alone is insufficient; the robot must also infer executable actions that can realize the predicted future. This motivates world action models, which couple visual future prediction with action generation: 


Existing approaches differ in how this coupling is implemented, leading to four representative paradigms summarized in Fig. 8. 

**Imagine-then-execute.** The most direct paradigm is a two-stage _imagine-then-execute_ formulation [4; 8; 9; 25; 29; 38; 47; 54]. In the first stage, a video prediction model generates visual subgoals: 


In the second stage, a separate inverse dynamics model or goal-conditioned policy, denoted by the parameterized distribution _qϕ_ , maps the current observation and a predicted visual subgoal into robot actions, 


The two modules together form a world action model: the video model imagines a possible future, and the inverse dynamics model grounds this future into executable actions. This decomposition has several practical advantages. Since the visual planner and the action grounding model are separated, they can be trained on different data sources: the video model can benefit from large-scale visual data, while the inverse dynamics model can be trained on robot trajectories with action labels. The modular design also allows additional structure to be injected into the action grounding process. For example, one can estimate intermediate quantities such as end-effector poses [29; 54], object poses [38], or dense optical flow [25] from the generated video, and then use these cues to derive or guide the corresponding robot actions. This decomposition provides flexibility, but it also makes action prediction dependent on the quality of the generated visual subgoals. Errors in the predicted subgoals may propagate to the inverse dynamics model, causing the predicted actions to deviate from the intended task execution. 

**Video-feature-conditioned action prediction.** A second paradigm keeps the two-stage structure but does not require the video model to generate a complete future observation sequence [17; 30; 34; 37; 44]. This design is motivated by the computational cost of diffusion-based models, where producing full future frames may require multiple iterative sampling steps. Instead of decoding a complete video rollout, these methods extract intermediate spatiotemporal features from the video prediction model and use them to 

condition an action prediction module: 


where _uθ_ denotes the neural backbone of the video prediction model, _H_ ( _·_ ) denotes a feature extraction operation, and _ft_ denotes the extracted spatiotemporal representation. The underlying assumption is that the internal representations of a video model already contain useful information about task intent, scene dynamics, and possible future evolution, even if the model does not explicitly decode the final video during policy inference. This can substantially reduce inference cost compared with full video generation, while still transferring predictive visual representations to the action model. The main limitation is that the interface between the video model and the policy becomes a latent feature rather than an explicit visual plan. As a result, the intermediate representation is less interpretable, harder to inspect, and may not expose whether the policy is using meaningful future information or merely exploiting task-correlated features. 

**Joint video-action modeling.** A third paradigm attempts to model future observations and robot actions jointly within a single generative model [7; 24; 26; 51]: 


In this formulation, video prediction and action prediction are not treated as two separate modules. Instead, the model learns a joint distribution over visual futures and the corresponding action sequences. A common strategy is to start from a video generation backbone pretrained on large-scale visual data [36; 42], modify the architecture or output space so that it can also produce robot actions, and then adapt the model on robot trajectories with action labels. This unified formulation has the advantage that future observations and actions are learned in a shared representational space, which can improve their consistency: the generated actions are trained together with the visual future they are supposed to induce. However, joint modeling also inherits the difficulties of both video generation and action learning. It requires robot data with action labels for adapting the action output, and such data are much scarcer than ordinary videos. In addition, the model must jointly handle highdimensional visual generation and precise action prediction, whose optimization objectives may not always be aligned. 

**Auxiliary video prediction for policy learning.** A fourth paradigm uses video prediction as an auxiliary training objective rather than as an explicit inference-time module [3; 6; 27; 53; 59]. In this setting, the policy is trained with an additional prediction branch that reconstructs or generates future observations from the policy’s internal representation. The purpose of this branch is not to produce an explicit visual plan for execution, but to encourage the 

6 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 


_Figure 8._ Taxonomy of world action models. Given the observation _ot_ and language instruction _l_ , world action models couple future observation prediction with robot action generation in different ways. Representative paradigms include imagine-then-execute, videofeature-conditioned action prediction, joint video-action modeling, and auxiliary video prediction for policy learning. 

policy backbone to encode spatiotemporal information related to future scene evolution. During training, the video prediction loss provides an auxiliary supervisory signal in addition to the action prediction loss. During inference, the auxiliary video branch can be removed, and only the action prediction head is used. This design avoids the cost of generating videos at test time while still using future prediction to shape the learned representation. Its limitation is that the predicted future is not explicitly used as a plan during execution. Therefore, the benefit of the video objective depends on whether the auxiliary prediction task induces representations that are useful for action selection. Balancing the action loss and the video prediction loss can also be nontrivial, since accurate visual prediction does not necessarily lead to better control. 

Overall, these four paradigms represent different ways of coupling world prediction with action generation. Imaginethen-execute methods provide modularity and interpretability, but may suffer from a visual-action grounding gap. Feature-conditioned methods reduce the computational cost of explicit video generation, but sacrifice the transparency of visual plans. Joint video-action models offer a unified formulation, but require action-labeled robot data and must jointly optimize visual and action prediction. Auxiliary prediction methods improve efficiency at inference time, but rely on the training objective to implicitly transfer predictive information into the policy. The central design trade-off is therefore how explicitly the future should be represented 

and how tightly this future representation should be coupled with action prediction. In addition, [56] provide an alternative perspective that categorizes video-based manipulation methods according to the interface through which temporal visual information is converted into control. 

## **References** 

- [1] Google DeepMind Blog. URL https://deepmind.google/blog/ genie-3-a-new-frontier-for-world-models/. Accessed: 2026-06-05. 

- [2] Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Komeili, M., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., Arnaud, S., Gejji, A., Martin, A., Hogan, F. R., Dugas, D., Bojanowski, P., Khalidov, V., Labatut, P., Massa, F., Szafraniec, M., Krishnakumar, K., Li, Y., Ma, X., Chandar, S., Meier, F., LeCun, Y., Rabbat, M., and Ballas, N. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- [3] Bi, H., Tan, H., Xie, S., Wang, Z., Huang, S., Liu, H., Zhao, R., Feng, Y., Xiang, C., Rong, Y., Zhao, H., Liu, H., Su, Z., Ma, L., Su, H., and Zhu, J. Motus: A unified latent action world model. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2026. 

7 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 

- [4] Black, K., Nakamoto, M., Atreya, P., Walke, H., Finn, C., Kumar, A., and Levine, S. Zero-shot robotic manipulation with pretrained image-editing diffusion models, 2023. URL https://arxiv.org/abs/2310. 10639. 

- [5] Bu, Q., Zeng, J., Chen, L., Yang, Y., Zhou, G., Yan, J., Luo, P., Cui, H., Ma, Y., and Li, H. Closed-loop visuomotor control with generative expectation for robotic manipulation, 2024. URL https://arxiv. org/abs/2409.09016. 

- [6] Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with task-centric latent actions. In _Robotics: Science and Systems (RSS)_ , 2025. Also at ICLR 2026. 

- [7] Cheang, C.-L., Chen, G., Jing, Y., Kong, T., Li, H., Li, Y., Liu, Y., Wu, H., Xu, J., Yang, Y., Zhang, H., and Zhu, M. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 

- [8] Du, Y., Yang, M., Dai, B., Dai, H., Nachum, O., Tenenbaum, J. B., Schuurmans, D., and Abbeel, P. Learning universal policies via text-guided video generation, 2023. URL https://arxiv.org/abs/2302. 00111. 

- [9] Feng, Y., Tan, H., Mao, X., Xiang, C., Liu, G., Huang, S., Su, H., and Zhu, J. Vidar: Embodied video diffusion model for generalist manipulation. _arXiv preprint arXiv:2507.12898_ , 2025. 

- [10] Gao, S., Zhou, S., Du, Y., Zhang, J., and Gan, C. Adaworld: Learning adaptable world models with latent actions, 2025. URL https://arxiv.org/abs/ 2503.18938. 

- [11] Gao, S., Liang, W., Zheng, K., Malik, A., Ye, S., Yu, S., Tseng, W.-C., Dong, Y., Mo, K., Lin, C.-H., Ma, Q., Nah, S., Magne, L., Xiang, J., Xie, Y., Zheng, R., Niu, D., Tan, Y. L., Zentner, K. R., Kurian, G., Indupuru, S., Jannaty, P., Gu, J., Zhang, J., Malik, J., Abbeel, P., Liu, M.-Y., Zhu, Y., Jang, J., and Fan, L. J. Dreamdojo: A generalist robot world model from large-scale human videos, 2026. URL https: //arxiv.org/abs/2602.06949. 

- [12] Goswami, R. G., Krishnamurthy, P., LeCun, Y., and Khorrami, F. Osvi-wm: One-shot visual imitation for unseen tasks using world-model-guided trajectory generation. _arXiv preprint arXiv:2505.20425_ , 2025. 

- [13] Guo, J., Ma, X., Wang, Y., Yang, M., Liu, H., and Li, Q. Flowdreamer: A rgb-d world model with flowbased motion representations for robot manipulation, 

2025. URL https://arxiv.org/abs/2505. 10075. 

- [14] Guo, Y., Shi, L. X., Chen, J., and Finn, C. Ctrl-world: A controllable generative world model for robot manipulation, 2026. URL https://arxiv.org/abs/ 2510.10125. 

- [15] Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [16] Hansen, N., Su, H., and Wang, X. Td-mpc2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [17] Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations. In _International Conference on Machine Learning (ICML)_ , 2025. Spotlight. 

- [18] Huang, S., Chen, L., Zhou, P., Chen, S., Jiang, Z., Hu, Y., Liao, Y., Gao, P., Li, H., Yao, M., and Ren, G. Enerverse: Envisioning embodied future space for robotics manipulation, 2025. URL https:// arxiv.org/abs/2501.01895. 

- [19] Huang, S., Chen, Q., Zhang, X., Sun, J., and Schwager, M. Particleformer: A 3d point cloud world model for multi-object, multi-material robotic manipulation, 2025. URL https://arxiv.org/abs/2506. 23126. 

- [20] Huang, W., Chao, Y.-W., Mousavian, A., Liu, M.-Y., Fox, D., Mo, K., and Fei-Fei, L. Pointworld: Scaling 3d world models for in-the-wild robotic manipulation, 2026. URL https://arxiv.org/abs/2601. 03782. 

- [21] Huang, Y., Zhang, J., Zou, S., Liu, X., Hu, R., and Xu, K. Ladi-wm: A latent diffusion-based world model for predictive manipulation. _arXiv preprint arXiv:2505.11528_ , 2025. 

- [22] Jeong, Y., Chun, J., Cha, S., and Kim, T. Object-centric world model for language-guided manipulation. _arXiv preprint arXiv:2503.06170_ , 2025. 

- [23] Jiang, H., Hsu, H.-Y., Zhang, K., Yu, H.-N., Wang, S., and Li, Y. Phystwin: Physics-informed reconstruction and simulation of deformable objects from videos. _arXiv preprint arXiv:2503.17973_ , 2025. 

- [24] Kim, M. J., Gao, Y., Lin, T.-Y., Lin, Y.-C., Ge, Y., Lam, G., Liang, P., Song, S., Liu, M.-Y., Finn, C., and Gu, J. Cosmos policy: Fine-tuning video models 

8 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 

   - for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. ICLR 2026. 

- [25] Ko, P.-C., Mao, J., Du, Y., Sun, S.-H., and Tenenbaum, J. B. Learning to act from actionless videos through dense correspondences, 2023. URL https: //arxiv.org/abs/2310.08576. 

- [26] Li, L., Zhang, Q., Luo, Y., Yang, S., Wang, R., Han, F., Yu, M., Gao, Z., Xue, N., Zhu, X., Shen, Y., and Xu, Y. Lingbot-va: Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- [27] Li, S., Gao, Y., Sadigh, D., and Song, S. Unified video action model. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [28] Li, W., Zhao, H., Yu, Z., Du, Y., Zou, Q., Hu, R., and Xu, K. Pin-wm: Learning physics-informed world models for non-prehensile manipulation. _arXiv preprint arXiv:2504.16693_ , 2025. 

- [29] Liang, J., Liu, R., Ozguroglu, E., Sudhakar, S., Dave, A., Tokmakov, P., Song, S., and Vondrick, C. Dreamitate: Real-world visuomotor policy learning via video generation. _arXiv preprint arXiv:2406.16862_ , 2024. 

- [30] Liang, J., Tokmakov, P., Liu, R., Sudhakar, S., Shah, P., Ambrus, R., and Vondrick, C. Video generators are robot policies, 2025. URL https://arxiv.org/ abs/2508.00795. 

- [31] Liang, Y., Kumar, N., Tang, H., Weller, A., Tenenbaum, J. B., Silver, T., Henriques, J. F., and Ellis, K. Visualpredicator: Learning abstract world models with neuro-symbolic predicates for robot planning. _arXiv preprint arXiv:2410.23156_ , 2024. 

- [32] Liang, Y., Nguyen, D., Yang, C., Li, T., Tenenbaum, J. B., Rasmussen, C. E., Weller, A., Tavares, Z., Silver, T., and Ellis, K. Exopredicator: Learning abstract models of dynamic worlds for robot planning. _arXiv preprint arXiv:2509.26255_ , 2025. Accepted to ICLR 2026. 

- [33] Luo, Y. and Du, Y. Grounding video models to actions through goal conditioned exploration, 2025. URL https://arxiv.org/abs/2411.07223. 

- [34] Ma, T., Zheng, J., Wang, Z., Jiang, C., Cui, A., Liang, J., and Yang, S. Dit4dit: Jointly modeling video dynamics and actions for generalizable robot control. _arXiv preprint arXiv:2603.10448_ , 2026. 

- [35] Maes, L., Le Lidec, Q., Scieur, D., LeCun, Y., and Balestriero, R. Leworldmodel: Stable end-to-end jointembedding predictive architecture from pixels. _arXiv preprint arXiv:2603.19312_ , 2025. 

- [36] NVIDIA, :, Ali, A., Bai, J., Bala, M., Balaji, Y., Blakeman, A., Cai, T., Cao, J., Cao, T., Cha, E., Chao, Y.-W., Chattopadhyay, P., Chen, M., Chen, Y., Chen, Y., Cheng, S., Cui, Y., Diamond, J., Ding, Y., Fan, J., Fan, L., Feng, L., Ferroni, F., Fidler, S., Fu, X., Gao, R., Ge, Y., Gu, J., Gupta, A., Gururani, S., Hanafi, I. E., Hassani, A., Hao, Z., Huffman, J., Jang, J., Jannaty, P., Kautz, J., Lam, G., Li, X., Li, Z., Liao, M., Lin, C.-H., Lin, T.-Y., Lin, Y.-C., Ling, H., Liu, M.-Y., Liu, X., Lu, Y., Luo, A., Ma, Q., Mao, H., Mo, K., Nah, S., Narang, Y., Panaskar, A., Pavao, L., Pham, T., Ramezanali, M., Reda, F., Reed, S., Ren, X., Shao, H., Shen, Y., Shi, S., Song, S., Stefaniak, B., Sun, S., Tang, S., Tasmeen, S., Tchapmi, L., Tseng, W.C., Varghese, J., Wang, A. Z., Wang, H., Wang, H., Wang, H., Wang, T.-C., Wei, F., Xu, J., Yang, D., Yang, X., Ye, H., Ye, S., Zeng, X., Zhang, J., Zhang, Q., Zheng, K., Zhu, A., and Zhu, Y. World simulation with video foundation models for physical ai, 2026. URL https://arxiv.org/abs/2511.00062. 

- [37] Pai, J., Achenbach, L., Montesinos, V., Forrai, B., Mees, O., and Nava, E. mimic-video: Video-action models for generalizable robot control beyond vlas. _arXiv preprint arXiv:2512.15692_ , 2026. 

- [38] Patel, S., Mohan, S., Mai, H., Jain, U., Lazebnik, S., and Li, Y. Robotic manipulation by imitating generated videos without physical demonstrations, 2026. URL https://arxiv.org/abs/2507. 00990. 

- [39] Qi, H., Yin, H., Zhu, A., Du, Y., and Yang, H. Inference-time enhancement of generative robot policies via predictive world modeling, 2026. URL https://arxiv.org/abs/2502.00622. 

- [40] Shang, Y., Zhang, X., Tang, Y., Jin, L., Gao, C., Wu, W., and Li, Y. Roboscape: Physics-informed embodied world model, 2025. URL https://arxiv.org/ abs/2506.23135. 

- [41] Team, R., Gao, Z., Wang, Q., Zeng, Y., Zhu, J., Cheng, K. L., Li, Y., Wang, H., Xu, Y., Ma, S., Chen, Y., Liu, J., Cheng, Y., Yao, Y., Zhu, J., Meng, Y., Zheng, K., Bai, Q., Chen, J., Shen, Z., Yu, Y., Zhu, X., Shen, Y., and Ouyang, H. Advancing open-source world models, 2026. URL https://arxiv.org/abs/ 2601.20540. 

- [42] Wan Team. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [43] Wang, B., Meng, X., Wang, X., Zhu, Z., Ye, A., Wang, Y., Yang, Z., Ni, C., Huang, G., and Wang, X. Embodiedreamer: Advancing real2sim2real transfer for 

9 

**From World Models to World Action Models: A Concise Tutorial for Robotics** 

policy training via embodied world modeling. _arXiv preprint arXiv:2507.05198_ , 2025. 

- [44] Wang, K., Ouyang, Z., Wu, X., Hong, J., Pan, W., Lu, H., Pan, J., Zhang, W., and Zheng, L. Ssi-policy: Learning structured scene interfaces for vision-language robotic manipulation. _arXiv preprint arXiv:2606.26800_ , 2026. 

- [45] Wang, M., Jin, W., Cao, K., Xie, L., and Hong, Y. Contactgaussian-wm: Learning physicsgrounded world model from videos. _arXiv preprint arXiv:2602.11021_ , 2026. 

- [46] Wang, S., You, J., Hu, Y., Li, J., and Gao, Y. Skil: Semantic keypoint imitation learning for generalizable data-efficient manipulation. _arXiv preprint arXiv:2501.14400_ , 2025. 

- [47] Wen, C., Lin, X., So, J., Chen, K., Dou, Q., Gao, Y., and Abbeel, P. Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ , 2024. 

- [48] World Labs Team. RTFM: A real-time frame model. World Labs Blog, October 2025. URL https: //www.worldlabs.ai/blog/rtfm. Accessed: 2026-06-05. 

- [49] Wu, P., Escontrela, A., Hafner, D., Goldberg, K., and Abbeel, P. Daydreamer: World models for physical robot learning. In _Conference on Robot Learning (CoRL)_ , 2022. 

   - [54] Zhang, C., Zhang, X., Pan, W., Zheng, L., and Zhang, W. Generative visual foresight meets task-agnostic pose estimation in robotic table-top manipulation, 2025. URL https://arxiv.org/abs/2509. 00361. 

   - [55] Zhen, H., Sun, Q., Zhang, H., Li, J., Zhou, S., Du, Y., and Gan, C. Tesseract: Learning 4d embodied world models, 2025. URL https://arxiv.org/abs/ 2504.20995. 

   - [56] Zheng, L., Ouyang, Z., Wang, C., Pan, J., and Zhang, W. From video to control: A survey of learning manipulation interfaces from temporal visual data. _arXiv preprint arXiv:2604.04974_ , 2026. 

   - [57] Zhi, H., Chen, P., Zhou, S., Dong, Y., Wu, Q., Han, L., and Tan, M. 3dflowaction: Learning crossembodiment manipulation from 3d flow world model. _arXiv preprint arXiv:2506.06199_ , 2025. 

   - [58] Zhou, G., Pan, H., LeCun, Y., and Pinto, L. Dino-wm: World models on pre-trained visual features enable zero-shot planning. _arXiv preprint arXiv:2411.04983_ , 2024. 

   - [59] Zhu, C., Yu, R., Feng, S., Burchfiel, B., Shah, P., and Gupta, A. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [50] Xu, M., Xu, Z., Xu, Y., Chi, C., Wetzstein, G., Veloso, M., and Song, S. Flow as the cross-domain manipulation interface. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [51] Ye, S., Ge, Y., Zheng, K., Gao, S., Yu, S., Kurian, G., Indupuru, S., Tan, Y. L., Zhu, C., Xiang, J., Malik, A., Lee, K., Liang, W., Ranawaka, N., Gu, J., Xu, Y., Wang, G., Hu, F., Narayan, A., Bjorck, J., Wang, J., Kim, G., Niu, D., Zheng, R., Xie, Y., Wu, J., Wang, Q., Julian, R., Xu, D., Du, Y., Chebotar, Y., Reed, S., Kautz, J., Zhu, Y., Fan, L., and Jang, J. Dreamzero: World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [52] Yin, T., Mei, Z., Sun, T., Zha, L., Zhou, E., Bao, J., Yamane, M., Shorinwa, O., and Majumdar, A. Womap: World models for embodied open-vocabulary object localization. _arXiv preprint arXiv:2506.01600_ , 2025. 

- [53] Yuan, T., Dong, Z., Liu, Y., and Zhao, H. Fast-wam: Do world action models need test-time future imagination? _arXiv preprint arXiv:2603.16666_ , 2026. 

10 

