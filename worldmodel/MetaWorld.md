---
title: "MetaWorld: Skill Transfer and Composition in a Hierarchical World Model for Grounding High-Level Instructions"
date: "2026-01-24"
authors: "Yutong Shen; Hangxu Liu; Kailin Pei; Ruizhe Xia; Tongtong Feng"
url: https://arxiv.org/abs/2601.17507
pdf: https://arxiv.org/pdf/2601.17507
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.17507)** / [論文ページ](https://arxiv.org/abs/2601.17507)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Under review as a workshop <u>paper at ICLR 2026</u> 

METAWORLD: SKILL TRANSFER AND COMPOSITION IN A HIERARCHICAL WORLD MODEL FOR GROUNDING HIGH-LEVEL INSTRUCTIONS 

**Yutong Shen**<sup>1</sup> **, Hangxu Liu**<sup>2</sup> **, Kailin Pei**<sup>1</sup> **, Ruizhe Xia**<sup>1</sup> **, Tongtong Feng**<sup>3</sup><sup>_,∗_</sup> 1Beijing University of Technology 2Fudan University 3Tsinghua University syt2004@emails.bjut.edu.cn 


Figure 1: This figure demonstrates the effectiveness of our hierarchical world model architecture on both the walking expert policy and the door-opening task. 

# ABSTRACT 

Humanoid robot loco-manipulation remains constrained by the semantic-physical gap. Current methods face three limitations: Low sample efficiency in reinforcement learning, poor generalization in imitation learning, and physical inconsistency in VLMs. We propose **MetaWorld** , a hierarchical world model that integrates semantic planning and physical control via expert policy transfer. The framework decouples tasks into a VLM-driven semantic layer and a latent dynamics model operating in a compact state space. Our dynamic expert selection and motion prior fusion mechanism leverages a pre-trained multiexpert policy library as transferable knowledge, enabling efficient online adaptation via a two-stage framework. VLMs serve as semantic interfaces, mapping instructions to executable skills and bypassing symbol grounding. Experiments on Humanoid-Bench show **MetaWorld** outperforms world model-based RL in task completion and motion coherence. Our code will be found at https: //anonymous.4open.science/r/metaworld-2BF4/ 

# 1 INTRODUCTION 

Humanoid robots, as quintessential embodiments of embodied intelligence, have long faced a fundamental challenge: executing semantically-driven loco-manipulation tasks within unstructured and dynamic environments. At the core of this challenge lies a significant “abstraction gap” in current robot control systems—the disconnect between high-level semantic understanding and low-level physical execution Kunze et al. (2011); Huang et al. (2024); Geng et al. (2024); Zhang et al. (2024). On one hand, large-scale models represented by Vision-Language Models (VLMs) demonstrate exceptional capabilities in high-level task planning and semantic reasoning, understanding “what to do”; on the other hand, low-level control methods based on imitation learning or reinforcement learning can generate precise joint-level actions, addressing “how to do it.” However, the absence 

1 

Under review as a workshop <u>paper at ICLR 2026</u> 


Figure 2: This illustrates the three-tier architecture of the **MetaWorld** framework: the semantic layer parses observation into executable skill sequences via a vision-language model; the skill transfer layer integrates expert policy priors through a hierarchical world model and enables dynamic adaptation; the physical layer performs precise control in a compact state space using a latent dynamics model. 

of a unified and scalable framework to bridge these disparate capabilities often results in semantic plans that are decoupled from physical constraints, conversely, low-level control policies often lack the versatility to generalize across complex, composed high-level tasks. 

Current mainstream approaches exhibit distinct limitations in addressing this problem. Although end-to-end reinforcement learning is theoretically capable of discovering optimal policies, it is often prohibitively sample-inefficient, rendering it impractical for real-world robotic platforms Song & Chen (2024). Imitation learning, while effective at acquiring natural motion patterns from human demonstrations, typically yields policies with limited robustness that remain highly sensitive to environmental fluctuations and external disturbances Lesort et al. (2024). Direct application of VLMs to robot control faces severe “symbol grounding” problems, with generated action plans often being kinematically or dynamically infeasible. While existing literature explores the integration of these methods, most approaches remain restricted to simplistic task concatenation or a loose coupling of independent modules, failing to establish a truly unified, hierarchical interaction architecture Pan et al. (2025); Li et al. (2025b); Shen et al. (2025). 

To systematically address these challenges, this paper presents **MetaWorld** , a hierarchical world model-based robot control framework. The proposed framework synergistically combines the semantic reasoning of VLMs, motion priors from imitation learning, and online adaptation mechanisms from model-based reinforcement learning, establishing a cohesive and scalable pipeline that bridges the gap between high-level semantic reasoning and low-level physical execution. **The main contributions of this paper include the following three aspects** : 

   - We propose a hierarchical, modular world model architecture that enables multi-scale decomposition of task representations. 

   - We introduce a dynamic expert selection and motion prior fusion mechanism that achieves efficient reuse and task-adaptive transfer of multi-expert policies. 

   - We establish a reliable interaction paradigm using VLMs as semantic interfaces, achieving feasible mapping from environmental semantics to physical actions. 

- 2 RELATED WORKS 

- 2.1 WORLD MODELS IN ROBOTICS 

World models facilitate policy learning by predicting environment state transitions, emerging as a critical tool for enhancing sample efficiency and generalization in robotics Li et al. (2025a). Mainstream approaches, such as the Dreamer series Hafner et al. (2020; 2021; 2025b;a), perform policy optimization through latent space prediction, while model-based reinforcement learning methods 

2 

Under review as a workshop <u>paper at ICLR 2026</u> 

like TD-MPC2 Hansen et al. (2024) further achieve high-performance control in complex dynamic environments. However, most existing world models lack hierarchical depth, hindering the decomposition of high-level semantic tasks into executable physical action sequences, thereby limiting their direct application to long-horizon, multi-step embodied tasks Fujii & Murata (2025). The hierarchical world model architecture proposed in this paper introduces explicit separation between the semantic planning layer and physical execution layer, enabling the world model to simultaneously handle semantic parsing of language instructions and dynamic prediction of physical environments, effectively bridging the gap between task planning and action generation. 

## 2.2 SKILL TRANSFER LEARNING 

Transfer learning facilitates robotic generalization through the systematic reuse of pre-acquired skills. Current robot control approaches include: domain adaptation (e.g., domain randomization) to bridge the sim-to-real gap Jiang et al. (2024); policy fine-tuning (e.g., progressive networks) for local adjustments Fehring et al. (2025); and meta-learning (e.g., MAML) for fast few-shot adaptation Finn et al. (2017); Kayaalp et al. (2022). However, these methods face two major bottlenecks: a heavy reliance on target-domain data or multi-stage training, both of which limit their practical deployment; and a failure to achieve real-time, millisecond-level adaptation in the face of dynamic disturbances. To address these issues, we propose a dynamic expert selection and motion prior fusion mechanism. By constructing a multi-expert policy library, our approach dynamically selects the most relevant strategies within a Model Predictive Control (MPC) framework to enable realtime policy adjustment. This approach maintains the efficiency of expert policies while significantly enhancing adaptability and generalization in unstructured environments. 

## 2.3 VLM APPLICATIONS IN REAL-TIME TASK PARSING 

Vision-Language Models (VLMs) have demonstrated remarkable proficiency in open-vocabulary perception, scene understanding, and high-level reasoning, and have been widely applied to highlevel task planning and semantic guidance in robotics. Representative works such as VIMA and RT-2 attempt to directly use VLMs to generate robot action sequences or serve as front-ends for symbolic planners Brohan et al. (2023); Huang et al. (2024). However, these methods commonly face the “symbol grounding” problem: VLM-generated plans often ignore the robot’s kinematic and dynamic constraints as well as environmental physics, resulting in infeasible plans. In this work, we mitigate the physical limitations of VLMs by restricting their role to high-level semantic parsing and mapping their outputs onto a set of pre-validated, physically feasible expert policies. Concurrently, our framework leverages the semantic understanding and task decomposition strengths of VLMs to process open-ended environmental semantics and achieve dynamic replanning through closed-loop feedback during training, guiding complex tasks to reference fundamental expert policies. 

# 3 METHOD 

## 3.1 METAWORLD HIERARCHICAL ARCHITECTURE 

The central idea of **MetaWorld** is to decompose the robotic control problem into two distinct layers: a semantic planning layer responsible for interpreting task intent, and a physical execution layer responsible for generating physically feasible actions. This hierarchical design can be formalized as: 


where _π_ sem maps the task description _T_ to a semantic plan, and _π_ phys generates specific actions _at_ based on the current state _st_ and the semantic plan. This architecture enables independent optimization of semantic understanding and physical control components while maintaining overall optimality. The optimization objective is to maximize the expected cumulative reward _J_ ( _π_ ) = E[<sup>�</sup> _γ_<sup>_t_</sup> _r_ ( _st, at_ )], where hierarchical optimization effectively addresses the distinct challenges at the semantic and physical levels. 

3 

Under review as a workshop <u>paper at ICLR 2026</u> 

## 3.2 SEMANTIC PLANNING AND SYMBOL GROUNDING 

The semantic planning layer employs a Vision-Language Model (VLM) to map natural language task descriptions to expert policy weights. Unlike traditional methods, we constrain the VLM output to an expert weight vector **w** rather than direct actions: 


the key innovation of this design lies in transforming the symbol grounding problem into a linear combination of expert policies. The VLM generates expert weights through carefully engineered prompts, with the response _R_ processed by a parsing function to obtain normalized weights _wi_ = exp(extract _i_ ( _R_ )) _/_<sup>�</sup> _j_<sup>exp(extract</sup><sup>_j_(</sup><sup>_R_)).Sinceeachexpertpolicy</sup><sup>_π_</sup> exp<sup>_i_isphysicallyfeasible,the</sup> generated semantic plan _π_ sem( _T_ ) =<sup>�</sup> _i_<sup>_wiπ_</sup> exp<sup>_i_naturally satisfies physical constraints.The symbol</sup> grounding error is bounded within the range of expert policy differences, significantly outperforming direct action generation methods. 

## 3.3 DYNAMIC ADAPTATION MECHANISM 

To address dynamic environmental changes, we introduce a state-aware expert selection mechanism. Based on the current state _st_ , we construct a selection probability distribution: 


where _ϕ_ is a state encoding function and _ψ_ is an expert feature extraction function. The VLMgenerated semantic weights _wi_ are fused with the dynamic selection probabilities _p_ ( _i|st_ ) to obtain the final weights _w_ ˜ _i_ ( _st, T_ ) = _αwi_ + (1 _− α_ ) _p_ ( _i|st_ ). This fusion mechanism theoretically combines the advantages of long-term task planning and short-term state adaptation. The parameter _α ∈_ [0 _,_ 1] controls the relative importance of semantic planning versus state awareness, enabling a balance between task consistency and environmental adaptability through appropriate adjustment of _α_ . The reference expert action _a_ ref =<sup>�</sup> _i_<sup>_w_˜</sup><sup>_i_(</sup><sup>_st, T_)</sup><sup>_π_</sup> exp<sup>_i_(</sup><sup>_st_) provides a high-quality initial solution for the</sup> physical execution layer. 

## 3.4 PHYSICAL EXECUTION AND ONLINE OPTIMIZATION 


the expert-guided action _a_ ref is incorporated into the optimization objective _L_ total = _L_ TD + _λ∥at − a_ ref _∥_<sup>2</sup> , where the Temporal-Difference (TD) learning loss _L_ TD = E[ _∥Q_ ( _zt, at_ ) _−_ ( _rt_ + _γQ_ ( _zt_ +1 _, π_ ( _zt_ +1))) _∥_<sup>2</sup> ] ensures accurate value function estimation. This design maintains online adaptation capabilities while leveraging expert knowledge to accelerate the learning process. TD-MPC2 employs quantile regression to learn the value function, achieving policy improvement through minimization of TD errors. 

## 3.5 THEORETICAL ANALYSIS AND IMPLEMENTATION 

Based on contraction mapping theory, we prove algorithm convergence under appropriate parameter selection. The value iteration operator _T_ satisfies the contraction property _∥T Q_ 1 _−T Q_ 2 _∥∞ ≤ γ∥Q_ 1 _− Q_ 2 _∥∞_ , guaranteeing convergence of the value function to the optimal solution. Compared to traditional methods, the sample complexity is reduced from _O_ ( _|S||A|/_ [(1 _− γ_ )<sup>2</sup> _ϵ_<sup>2</sup> ]) to _O_ (1 _/_ [(1 _− γ_ )<sup>2</sup> _ϵ_<sup>2</sup> ] + _K_ ), demonstrating the efficiency advantage of knowledge reuse. 

4 

Under review as a workshop <u>paper at ICLR 2026</u> 


Figure 3: We evaluate our method on locomotion (run, walk, stand) and manipulation (door) tasks against baselines TD-MPC2 and DreamerV3. 

# 4 EXPERIMENT 

We evaluate our method on HumanoidBench Sferrazza et al. (2024), a comprehensive benchmark for humanoid locomotion and manipulation. For locomotion, we select three tasks—walk, stand, and reach—and for manipulation, we include door opening. The locomotion tasks are learned via imitation learning from the AMASS Mahmood et al. (2019) expert dataset, shaped with trajectorytracking reward signals. Other skills in the base expert policy repository (e.g., reach) are inherited from TD-MPC2 and are therefore excluded from evaluation. We select two representative stateof-the-art (SOTA) model-based reinforcement learning algorithms as baselines: **TD-MPC2** , which emphasizes implicit modeling and cross-domain robustness, and **DreamerV3** , which excels at explicit world model construction and complex visual task planning. 

## 4.1 EXPERIMENTAL SETUP 

Our architecture employs the following hyperparameters: the VLM temperature parameter _τ_ = 0 _._ 3 controls the stochasticity in expert weight generation; the expert guidance weight _λ_ = 0 _._ 05 balances TD-learning and expert priors; the MPC planning horizon is set to _H_ = 3 to ensure real-time performance; the discount factor _γ_ = 0 _._ 99 trades off long-term rewards; the learning rate is fixed at 0 _._ 001 to ensure stable convergence; the batch size of 256 balances training efficiency and memory usage; and the fusion coefficient _α_ = 0 _._ 7 regulates the relative importance of semantic planning and state adaptation. For task success criteria, we follow the definitions provided in HumanoidBench. 

## 4.2 VALIDATION OF HIERARCHICAL ARCHITECTURE EFFECTIVENESS 

**Purpose of the experiment.** In this section, we evaluate the effectiveness of our hierarchical architecture against traditional model-based reinforcement learning methods. We first assess the performance of the base expert policy across three locomotion tasks: walk, reach, and stand. Subsequently, on the walk task, we further test the model’s capability to perform complex manipulation tasks after dynamic adaptation. 

**Result.** Based on the experimental results shown in Figure 3 and Table **??** , the **MetaWorld** framework’s comprehensive advantages across four tasks (average return improvement of 135.6%) demonstrate its hierarchical architecture’s effectiveness. For basic locomotion tasks (Stand, Walk, Run), the exceptional performance (especially Run’s 2456.3% improvement) benefits primarily from high-quality motion priors provided by the imitation-learned expert library, which supplies the VLM planner with a physically feasible action space. For the complex Door task, the 278.3% gain validates the hierarchical innovation: the VLM decomposes the ”open door” instruction into sub-actions, while the dynamic selection mechanism composes corresponding primitive experts for execution. The key insight is that complex tasks are achieved through semantic parsing and expert composition rather than end-to-end training. This strategy effectively resolves the symbol grounding 

5 

Under review as a workshop <u>paper at ICLR 2026</u> 

|**Task**|**Metric**|**DreamerV3**|**TD-MPC2**|**Ours**|**Imp. (%)**|
|---|---|---|---|---|---|
|**Stand**|Ret. _↑_(_±_Std)|699_._3_±_62_._7|749_._8_±_54_._3|**793**_._**4**_±_**13**_._**5**|5.8|
||Conv. _↓_(M)|5_._5|1_._9|**0**_._**8**|57.9|
|**Walk**|Ret. _↑_(_±_Std)|428_._2_±_14_._5|644_._2_±_162_._3|**701**_._**2**_±_**7**_._**6**|8.8|
||Conv. _↓_(M)|6_._0|1_._8|**1**_._**4**|22.2|
|**Run**|Ret. _↑_(_±_Std)|298_._5_±_84_._5|66_._1_±_4_._7|**1689**_._**9**_±_**13**_._**6**|2456.3|
||Conv. _↓_(M)|6_._0|2_._0|**1**_._**9**|5.0|
|**Door**|Ret. _↑_(_±_Std)|165_._8_±_50_._2|179_._8_±_52_._9|**680**_._**0**_±_**50**_._**0**|278.3|
||Conv. _↓_(M)|9_._0|2_._0|**1**_._**7**|15.0|
|**Avg**|Ret. _↑_|398_._0|410_._0|**966**_._**1**|135.6|
|**.**|Conv. _↓_(M)|6_._6|1_._9|**1**_._**5**|24.9|


Table 1: Performance comparison on locomotion and manipulation tasks. All values are reported to one decimal place. The **Ours** column is highlighted in light blue, and the rightmost column shows the percentage improvement. 

dilemma while simultaneously overcoming the sample efficiency bottleneck inherent in end-to-end RL paradigms, offering a novel paradigm for intelligent robot control. 

## 4.3 ABLATION STUDY AND STABILITY ANALYSIS 

**Purpose of the experiment.** To rigorously quantify the contribution of each module within the MetaWorld framework, we perform a systematic series of ablation experiments. First, we ablate semantic planning by uniformly weighting all tasks in the base skill library. Next, we ablate dynamic expert selection by fixing _α_ = 1 _._ 0 during training, thereby disabling state-aware expert selection. Finally, we ablate skill-expert guidance by setting _λ_ = 0 in the TD-MPC2 optimization objective, removing expert action guidance. We present experimental observations and analysis for each ablation. 


Figure 4: Ablation study results on the Door task (maximum reward and convergence steps). 

6 

Under review as a workshop <u>paper at ICLR 2026</u> 

**Result.** As shown in Figure 4, ablation studies on the Door task reveal how the **MetaWorld** framework bridges the semantic-physical gap. Removing the Vision-Language Model (VLM) causes a 72.7% performance collapse, indicating a failure in semantic planning, the robot cannot decompose ”open the door” into executable skills like ”approach handle–rotate–push/pull.” This highlights traditional RL’s inability to solve the symbol grounding problem. Ablating dynamic expert selection results in only a 15.4% performance drop, demonstrating the framework’s robustness: without online adaptation, the pre-trained expert base still provides basic motion priors. To rigorously quantify the contribution of each module within the MetaWorld framework, we perform a systematic series of ablation experiments. Removing expert guidance results in a 52.9% performance loss, highlighting the synergy between imitation learning and model-based RL. Expert policies provide feasible action bounds for online fine-tuning, with both components being essential. 

# 5 CONCLUSION 

This study presents **MetaWorld** , a hierarchical world model framework that bridges the semanticphysical gap in humanoid robot control via VLM-based semantic planning, dynamic expert policy transfer, and latent physical control. On Humanoid-Bench tasks, it achieves an average reward improvement of 135.6%, substantially enhancing task completion efficiency and motion coherence. While the framework includes a basic imitation learning module to build an expert policy repository, it currently depends on simple trajectory-matching reward mechanisms, which cannot dynamically weigh fine-grained aspects like joint-level motion errors. Furthermore, expert policy selection uses static weighted fusion rather than an intelligent routing mechanism under a Mixture-of-Experts (MoE) architecture, limiting precise skill composition and semantically conditioned switching. The system also lacks a few-shot generalization ability, shows constrained adaptability and scalability with novel complex task combinations, and does not explicitly address gradient interference from multi-skill coordination. Future work will iteratively upgrade the framework through dynamic reward shaping for imitation learning, an MoE-based semantic-aware routing mechanism, and enhanced few-shot transfer generalization, advancing toward a more robust and adaptive framework for complex control and manipulation demands. 

# REFERENCES 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _Science Robotics_ , 2023. 

- Lukas Fehring, Theresa Eimer, and Marius Lindauer. Growing with experience: Growing neural networks in deep reinforcement learning. In _2025 Multi-disciplinary Conference on Reinforcement Learning and Decision Making (RLDM)_ , 2025. 

- Chelsea Finn, Pieter Abbeel, and Sergey Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In _Proceedings of the 34th International Conference on Machine Learning (ICML)_ , volume 70 of _Proceedings of Machine Learning Research_ , pp. 1126–1135. PMLR, 2017. URL http://proceedings.mlr.press/v70/finn17a.html. 

- Kentaro Fujii and Shingo Murata. Real-world robot control by deep active inference with a temporally hierarchical world model. _IEEE Robotics and Automation Letters (RA-L)_ , 2025. 

- Haoran Geng, Songlin Wei, Congyue Deng, Bokui Shen, He Wang, and Leonidas Guibas. SAGE: Bridging Semantic and Actionable Parts for GEneralizable Articulated-Object Manipulation under Language Instructions. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations (ICLR)_ , 2020. 

- Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations (ICLR)_ , 2021. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Training agents inside of scalable world models. _arXiv preprint arXiv:2509.24527_ , 2025a. 

7 

Under review as a workshop <u>paper at ICLR 2026</u> 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 626:1108–1116, 2025b. 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Fei-Fei Li. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. In _Conference on Robot Learning (CoRL)_ , 2024. 

- Yuankun Jiang, Chenglin Li, Wenrui Dai, Junni Zou, and Hongkai Xiong. Variance reduced domain randomization for reinforcement learning with policy gradient. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- M. Kayaalp, S. Vlaski, and A. Sayed. Dif-maml: Decentralized multi-agent meta-learning. _IEEE Open Journal of Signal Processing_ , 3:71–93, 2022. doi: 10.1109/OJSP.2021.3140000. 

- Lars Kunze, Tobias Roehm, and Michael Beetz. Towards semantic robot description languages. In _2011 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 5589–5595, 2011. 

- Timoth´ee Lesort, Mirco Mutti, Pierluca D’Oro, Talay Norman, Stefano V. Albrecht, and Irina Rish. Evil: Evolution strategies for generalisable imitation learning. In _International Conference on Machine Learning (ICML)_ , 2024. 

- Chenhao Li, Andreas Krause, and Marco Hutter. Robotic world model: A neural network simulator for robust policy optimization in robotics. In _Proceedings of The 8th Conference on Robot Learning (CoRL)_ , 2025a. 

- Yi Li, Hongjie Chen, Zeyu Zhou, Yujia Zhang, and Song-Chun Zhu. Hamster: Hierarchical action models for open-world robot manipulation. In _International Conference on Learning Representations (ICLR)_ , 2025b. 

- Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. Amass: Archive of motion capture as surface shapes. In _IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2019. 

- Mingjie Pan, Yun-Hui Liu, Zheng Sun, Yang Li, and He Wang. Omnimanip: Towards general robotic manipulation via object-centric interaction primitives as spatial constraints. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. doi: 10.48550/arXiv.2403.10506. 

- Yutong Shen, Hangxu Liu, Lei Zhang, Penghui Liu, Ruizhe Xia, Tianyi Yao, and Tongtong Feng. Detach: Cross-domain learning for long-horizon tasks via mixture of disentangled experts, 2025. URL https://arxiv.org/abs/2508.07842. 

- Kai Tai Song and Hsiang Hsi Chen. Hagrasp: Hybrid action grasp control in cluttered scenes using deep reinforcement learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- Zichen Zhang, Yunshuang Li, Osbert Bastani, Abhishek Gupta, Dinesh Jayaraman, Yecheng Jason Ma, and Luca Weihs. Universal visual decomposer: Long-horizon manipulation made easy. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6973–6980. IEEE, 2024. 

8 

