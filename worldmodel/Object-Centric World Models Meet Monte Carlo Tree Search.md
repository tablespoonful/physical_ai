---
title: "Object-Centric World Models Meet Monte Carlo Tree Search"
date: "2026-01-10"
authors: "Rodion Vakhitov; Leonid Ugadiarov; Aleksandr Panov"
url: https://arxiv.org/abs/2601.06604
pdf: https://arxiv.org/pdf/2601.06604
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.06604)** / [論文ページ](https://arxiv.org/abs/2601.06604)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Object-Centric World Models Meet Monte Carlo Tree Search** 

**Rodion Vakhitov** MIPT Moscow, Russia `rodionvahitoff@yandex.ru` 

**Leonid Ugadiarov** AIRI & MIPT Moscow, Russia 

**Aleksandr Panov** AIRI & MIPT & FRC CSC RAS Moscow, Russia 

## **Abstract** 

In this paper, we introduce ObjectZero, a novel reinforcement learning (RL) algorithm that leverages the power of object-level representations to model dynamic environments more effectively. Unlike traditional approaches that process the world as a single undifferentiated input, our method employs Graph Neural Networks (GNNs) to capture intricate interactions among multiple objects. These objects, which can be manipulated and interact with each other, serve as the foundation for our model’s understanding of the environment. We trained the algorithm in a complex setting teeming with diverse, interactive objects, demonstrating its ability to effectively learn and predict object dynamics. Our results highlight that a structured world model operating on object-centric representations can be successfully integrated into a model-based RL algorithm utilizing Monte Carlo Tree Search as a planning module. 

## **1 Introduction** 

Research in cognitive neuroscience and psychology shows that our minds naturally segment sensory input into discrete objects, aiding perception, generalization, and adaptability Ferraro et al. [2023b], Hawkins et al. [2017]. Unlike traditional approaches that encode whole scenes Hafner et al. [2019], object-centric models focus on interactions between elements. Advances in unsupervised learning now allow automatic discovery and separation of objects from raw input Jiang et al. [2023], Chakravarthy et al. [2023], Kirilenko et al. [2024], embedding a bias toward objectness. This leads to more interpretable and generalizable representations, aligning with cognitive principles and improving performance in downstream tasks. 

Interest in model-based reinforcement learning (MBRL) approaches Moerland et al. [2020] has been steadily growing, driven by their ability to improve sample efficiency and generalization in reinforcement learning. The success of MBRL depends on model quality - especially in complex environments. By decomposing environments into objects and their interactions, factorized world models offer more accurate and generalizable dynamics than monolithic, entangled models. This structure supports compositionality, task transfer, and aligns with human cognitive principles. 

Object-centric representations offer significant advantages in robotics and MBRL by providing structured views of the environment that enhance perception and decision-making Ugadiarov et al. [2025a]. In robotics, agents need to identify and distinguish objects and their properties to interact effectively. Such representations help robots generalize to new contexts, manipulate unfamiliar objects, and reason about action consequences Devin et al. [2018]. By embedding such structured 


Figure 1: ObjectZero training overview. The slots extractor encodes observations into object-centric representations. Separate GNN models predict next-state slots, rewards, policy and value outputs. Gumbel search generates target policy _πt_ and value _zt_ . 

representations, also referred to as slots, robots gain improved autonomy and robustness, which is especially useful in complex, dynamic environments like robotic manipulation, autonomous driving, and embodied AI. 

This paper introduces ObjectZero, an object-centric reinforcement learning algorithm that integrates a structured world model with online policy learning. The world model utilizes a pretrained, frozen object-centric encoder (i.e., slots extractor) based on the SLATE Singh et al. [2022a] or DINOSAUR Seitzer et al. [2023] architecture, which employ Slot Attention Locatello et al. [2020] to extract sets of object representations from high-dimensional visual inputs. The choice depends on the visual complexity of the environment: SLATE is preferred for synthetic or stylized settings, while DINOSAUR is used for more realistic visual environments. A GNN aggregates information across these object representations to predict environment rewards, state values, dynamics and policy. 

## **2 Related Work** 

### **2.1 Object-Centric Representation Learning** 

In recent years, object-centric representation learning methods have gained significant traction, aiming to extract and track individual entities from raw visual input without supervision. A central component in many of these approaches is Slot Attention Locatello et al. [2020], Frolov et al. [2025], which employs a normalized cross-attention mechanism to iteratively bind slots to different regions in the input. Building on this foundation, SAVi Kipf et al. [2022] and SAVi++ Elsayed et al. [2022] are extensions of Slot Attention for processing video data, introducing temporal consistency by predicting optical flow and depth, respectively. SLATE and STEVE Singh et al. [2022b] achieve high-quality reconstruction through hybrid architectures.The SLATE incorporates a dVAE Van Den Oord et al. [2017] for internal feature extraction, a GPT-like transformer Ramesh et al. [2021] for decoding, and a slot-attention module to group features associated with the same object. STEVE differs from SLATE in that it operates on real-world video. DINOSAUR is trained to reconstruct not the original image based on the slots obtained using Slot Attention, but rather some encoded features of this image using the pretrained DINO ViT Amir et al. [2021]. 

2 

### **2.2 Object-Centric Representations and RL** 

Modern model-based reinforcement learning methods—such as MuZero Schrittwieser et al. [2020], EfficientZeroV2 Wang et al. [2024], DreamerV3 Hafner et al. [2023], TD-MPC Hansen et al. [2024] and STORM Zhang et al. [2023] – have significantly improved sample efficiency and planning in visual environments. These methods achieve this by learning internal dynamics models and leveraging techniques such as Monte Carlo Tree Search (MCTS) Coulom [2006], Model Predictive Path Integral control Williams et al. [2015], and transformer-based architectures. Recent work explores the integration of object-centric representations into MBRL. COBRA Watters et al. [2019] trains a dynamics model on the slot space learned by the MONet Burgess et al. [2019] model, integrating intrinsically motivated exploration to optimize data acquisition and subsequent training. FOCUS Ferraro et al. [2023a] decomposes observations into separate latent object representations via an object encoder and decoder that learn to segment the scene using masking. OC-STORM Zhang et al. [2025] predicts dynamics using a spatiotemporal transformer that handles both object and visual representations. We do not compare our method with COBRA, as it does not account for interactions between objects, which are essential for our task. FOCUS and OC-STORM are also excluded due to their reliance on manually annotated object masks, which contradicts our setting. Nevertheless, these approaches highlight the growing recognition of structured representations as a key component for scalability and interpretability of MBRL. In contrast, ROCA Ugadiarov et al. [2025b] is closely aligned with our setting: it learns an object-centric world model from unsupervised slot representations and explicitly models object interactions via graph neural networks integrated into the critic. 

In parallel to these model-based approaches, recent research has also explored model-free reinforcement learning with object-centric representations. In OCRL Yoon et al. [2023] authors introduce a novel approach where a transformer encoder serves as a pooling mechanism within the PPO algorithm Schulman et al. [2017], enabling the integration of object-level representations derived from input images by diverse object-centric models. In another study Stani´c et al. [2023], the authors propose the OC-CA and OC-SA algorithms, which employ Slot Attention as an object-centric feature extractor and investigate their performance and generalization abilities. 

## **3 Background** 

### **3.1 Reinforcement Learning** 

Reinforcement Learning can be formulated as a Markov Decision Process (MDP) Bellman [1957]. An MDP in this context is formalized as a tuple ( _S, A, T, R, γ_ ), where _s ∈S_ represents states, _a ∈A_ denotes actions, _T_ : _S × A →S_ is the transition function, _R_ : _S × A →_ R is the reward function associated with a particular task, and _γ_ is the discount factor. The goal of reinforcement learning is to find the optimal policy _π_<sup>_∗_</sup> = arg max _π_ E _st_ +1 _∼T_ ( _·|st,at_ ) _, at_ +1 _∼π_ ( _·|st_ +1) �� _iτ_ =0<sup>_γiR_(</sup><sup>_st, at_)</sup> � for all _s_ 0 where _τ_ is the number of time steps. 

### **3.2 EfficientZeroV2** 

Table 1: Comparison of component models and implementations in EZ-V2 and ObjectZero 

|**Component**|**Model**|||**Implementation**|
|---|---|---|---|---|
||||**EZ-V**|**2**|
|Dynamics model<br>Encoder|ˆ_st_+1 _∼pϕ_(<br>_st ∼pθ_(_st |_|ˆ_st_+1 _|_<br>_ot_)|_st, at_)|CNN<br>CNN|
|Reward model|_rt ∼pψ_(_rt _|_| st_)||CNN and MLP|
|Value model<br>Policymodel|_vt ∼pξ_(_vt |_<br>_pt ∼pω_(_pt _|_st_)<br> _| st_)|**Object**|CNN and MLP<br>CNN and MLP<br>**Zero**|
|Dynamics model<br>Encoder|ˆ_s_<sup>_i_</sup><br>_t_+1 <sup>_∼pϕ_(</sup><br>¯_st_ =Slots E|<sup>ˆ</sup><sup>_si_</sup><br>_t_+1 <sup>_|_</sup><br>xtrac|<sup>ˆ</sup><sup>_si_</sup><br>_t_<sup>_, at_)</sup><br>tor(_ot_)|GNN<br>SLATE (frozen) or DINOSAUR (frozen)|
|Reward model<br>Value model|_rt ∼pψ_(_rt _<br>_vt ∼pξ_(_vt |_|_|_ ¯_st_)<br> ¯_st_)||GNN and MLP<br>GNN and MLP|
|Policymodel|_pt ∼pω_(_pt _|_|_ ¯_st_)||GNN and MLP|


3 

Our model builds on top of the EfficientZeroV2, a model-based reinforcement learning algorithm that significantly improves upon its predecessor, EfficientZero Ye et al. [2021], by extending its capabilities to continuous action spaces, enhancing planning efficiency, and introducing more accurate value estimation methods. Like EfficientZero, EZ-V2 is based on the MuZero-style framework and learns a latent model of the environment, which is used both for planning and for learning policy and value functions. The EfficientZero family of algorithms uses MCTS as a planning module to simulate future trajectories and guide decision-making, leveraging a learned model rather than the true environment. 

All the main components of EZ-V2 and ObjectZero are presented in Table 1. The current observation is represented by _ot_ , _st_ is the current latent state. The encoder learns a compact state representation of the input _ot_ . The dynamic function predicts the next state ˆ _st_ +1 based on the _st_ current state and the action taken _at_ . The policy model outputs the current policy _pt_ , the value predictor provides the value estimation ˆ _vt_ at the current state and reward predictor estimates ˆ _rt_ . All parameters of the components are trained jointly to match the target policy, value, and reward. 


where _ut_ denotes the environment reward, _πt_ is the target policy from the search and _zt_ represents the target value from the search. _LR_ , _LP_ and _LV_ all represent supervised learning losses. _LG_ is the temporal consistency loss, which is calculated through the negative cosine similarity. _λ_ 1 _, λ_ 2 _, λ_ 3 _, λ_ 4 are total loss function coefficients. _Lt_ is the objective function to be optimized. The agent’s interaction experience with the environment is collected into a replay buffer. The ground truth data used in the loss functions is sampled from this buffer. 

Key to EZ-V2’s sample efficiency are its planning and value estimation techniques. Firstly, for continuous action spaces EfficientZeroV2 generates target policies _zt_ by sampling _M_ candidate actions from a mixture of the current policy _pt_ and a prior. For discrete action spaces each action is selected as _A_ = arg max _a_ ( _g_ ( _a_ ) + logits( _a_ )), where _ga_ is a vector of Gumbel variables and logits( _a_ ) is the logit of action _a_ . The candidates are ranked using Sequential Halving, which progressively discards weaker actions, i.e., actions with lower Q-values, allocating computation to the most promising ones. This enables efficient policy improvement in continuous action spaces. 

To improve learning stability, EZ-V2 use Search-based Value Estimation (SVE), which computes the target value as the empirical average over simulated trajectories: 


where _N_ denotes the number of simulations, _V_<sup>ˆ</sup> _n_ ( _s_ 0) is the bootstrapped estimation of the _n_ -th node expansion, _H_ ( _n_ ) is a search depth of _n_ -th iteration. 

However, early in training or when using stale data, model error may degrade SVE accuracy. We therefore use a mixed value target, combining multi-step TD and SVE: 


In this context, _l_ denotes the horizon for the multi-step temporal difference (TD) method. The variable _it_ represents the current training iteration, while _T_ 1 corresponds to the initial training phase. The index _is_ refers to the position of the sampled data from the replay buffer. The size of the buffer is given by _|D|_ , and _T_ 2 defines the threshold used to evaluate the staleness of the sampled data. 

## **4 ObjectZero** 

Figure 1 illustrates the architectures of ObjectZero. It is composed of modular components designed around object-centric representations, enabling structured reasoning and improved generalization. Each module operates on object representations, allowing the agent to model dynamics, policy, and rewards at the level of individual entities. 

4 

### **4.1 Slots Extractor** 

The slots extractor takes an image-based observation _ot_ as input and extracts object representations as an unordered set of low-dimensional vectors ¯ _st_ = _{s_<sup>1</sup> _t_<sup>_, . . . , sK_</sup> _t_<sup>_}_, where</sup><sup>_K_is a non-learned parameter</sup> which equals to the maximum possible number of objects in the image. The SLATE or DINOSAUR model can not guarantee the fixed order of object representations due to the stochastic nature of the slot-attention module. To enforce the order of object representation during the episode, we preinitialize the slots of the slots extractor model for the next step _t_ + 1 with the current object representations ¯ _st_ . We pretrain the SLATE and DINOSAUR on the dataset of observations collected in the environment by a uniform random policy and freeze it. Appendix A and Appendix B provide information on the hyperparameters of SLATE and DINOSAUR, respectively. 

### **4.2 Dynamics Model** 

We define the dynamics model like a graph neural network architecture, following an approach similar to that of C-SWMs Kipf et al. [2020]. The network consists of two components: an edge model edge _T_ and a node model node _T_ . These models take as input a factored state representation _st_ = ( _s_<sup>1</sup> _t_<sup>_, . . . , sK_</sup> _t_<sup>) and an action</sup><sup>_at_, and predict the next state.The MSE is used as the consistency</sup> loss. 


### **4.3 Policy model, Reward model and Value model** 

The policy, reward and value model have almost the same architecture as the dynamics model, but they do not depend on actions in their edge models or node models. We sum up object embeddings returned by the node models and feed the result into the MLP to produce the scalar value. 


The indices V, P and R refer to the value model, the policy model and the reward model, respectively. For continuous action spaces, the policy output _pt_ is further processed to parameters of a Gaussian distribution. 

## **5 Environments** 

**Causal World** We conduct experiments on the Object Reaching task in the CausalWorld Ahmed et al. [2021] environment. In this task, a fixed target object and several distractor objects are placed randomly within the scene. The agent operates a tri-finger robot, where only one finger is moveable and must be used to reach the target object to earn a positive reward and complete the task. If the finger touches a distractor object first, the episode ends with zero reward. The action space is defined by the three continuous joint positions of the moveable finger. The agent does not receive any proprioceptive input, so it must learn to control the finger solely from visual observations. 

**Robosuite** In the Block Lifting task in Robosuite framework Zhu et al. [2020], a cube is positioned on a tabletop in front of a single robotic arm. The objective for the agent is to manipulate the arm to lift the cube above a predefined height. We use a setup with a dense reward function. Our experiments utilize the Panda robot model. 

5 

## **6 Experiments** 


Figure 2: Success rate and return averaged over 30 episodes and three seeds for ObjectZero, EZ-V2, DreamerV3, ROCA, OCRL, OC-CA and OC-SA in the Object Reaching Task in Causal World and the Block Lifting Task in Robosuite. Shaded areas indicate standard deviation 


Figure 3: Examples of observations and attention maps produced by the SLATE model in the Causal World Object Reaching task. 


Figure 4: Examples of observations and attention maps produced by the DINOSAUR model in the Robosuite Block Lifting task. 

We evaluate ObjectZero by comparing it to a model-free object-centric approach built on PPO, utilizing the same pre-trained and frozen SLATE and DINOSAUR model for extracting features. To aggregate the individual object representations into a format compatible with PPO’s value and policy networks, we employ a Transformer encoder Vaswani et al. [2017] as a pooling mechanism. For this setup, we adopt the Transformer-based PPO architecture from the OCRL baseline Yoon et al. [2023]. Additionally, we include other object-centric model-free baselines, specifically the self-attention OC-SA and cross-attention OC-CA variants proposed in Stani´c et al. [2023]. These methods train object-centric feature extractors online during policy learning. 

As monolithic MBRL baselines, we include DreamerV3 Hafner et al. [2023] and EfficientZeroV2 Wang et al. [2024]. For the object-centric MBRL baseline, we consider ROCA Ugadiarov et al. [2025b], which also leverages the same pre-trained and frozen SLATE and DINOSAUR model for object representation. For the DreamerV3 baseline, we use the `medium` preset for configuration parameters, with the `train_ratio` parameter increased to 128. For OCRL, OC-SA, and OC-CA, we perform a grid search over a set of hyperparameters to improve performance. For ROCA, we use the hyperparameters proposed by the authors for this task in the paper. For the baseline EZ-V2, we employ the default hyperparameters specified in the original paper. ObjectZero uses the same 

6 

hyperparameters as the monolithic EZ-V2, except for `max_grad_norm` , which is decreased to 0.5. Additionally, for Block Lifting task in ObjectZero `learning_rate` is is set to 0.02. ObjectZero’s implementation is directly based on the codebase of EZ-V2. For Object Reaching task in ObjectZero, ROCA and OCRL we use SLATE model (Figure 3), whereas in Block Lifting, we use DINOSAUR (Figure 4). 

Figure 2 presents how the success rate and return depends on the number of training steps for ObjectZero and the baseline methods on the Object Reaching and Block Lifting task. In the Object Reaching task ObjectZero demonstrates faster convergence compared to all baselines, with the exception of EZ-V2, whose performance is comparable. In the Block Lifting task, ObjectZero outperforms OC-SA, OC-CA, and OCRL, slightly surpasses DreamerV3 and ROCA, and achieves nearly the same performance as EZ-V2. 

## **7 Limitations** 

Despite the advances in modern unsupervised object-centric learning, most state-of-the-art approaches still face significant challenges when it comes to decomposing complex, realistic scenes into distinct objects. We consider this limitation a major barrier to deploying our algorithm in arbitrary, realworld environments. Additionally, since we represent the environment’s state as a fully connected graph of object states, which is processed by graph neural networks, the computational complexity of ObjectZero becomes quadratic with respect to the number of slots produced by the objectcentric extractor. Both of these factors can significantly slow down training in practical, object-rich scenarios—particularly in real-world robotics settings, where efficiency and scalability are crucial for learning from interaction. 

## **8 Conclusion** 

In this work, we introduced ObjectZero, a model-based reinforcement learning algorithm that integrates object-centric representations with a structured world model built upon a pretrained SLATE and DINOSAUR encoder and Graph Neural Networks. We demonstrated that ObjectZero effectively learns policy, outperforms existing object-centric approaches, and performs on par with the monolithic baseline in the task requiring reasoning over objects. We show that structured dynamics and policy models operating on object-centric representations can be learned within MCTS-based MBRL algorithms. As future work, we plan to explore the joint training of the object-centric encoder and world model components, as well as the application of ObjectZero in more realistic and high-dimensional environments where object discovery remains a major challenge. 

## **9 Acknowledgments** 

The research was carried out using the infrastructure of the Shared Research Facilities «High Performance Computing and Big Data» (CKP «Informatics») of FRC CSC RAS (Moscow). 

## **References** 

- Ossama Ahmed, Frederik Träuble, Anirudh Goyal, Alexander Neitz, Manuel Wuthrich, Yoshua Bengio, Bernhard Schölkopf, and Stefan Bauer. Causalworld: A robotic manipulation benchmark for causal structure and transfer learning. In _International Conference on Learning Representations_ , 2021. 

- Shir Amir, Yossi Gandelsman, Shai Bagon, and Tali Dekel. Deep vit features as dense visual descriptors. _arXiv preprint arXiv:2112.05814_ , 2021. 

- Richard Bellman. A markovian decision process. _Journal of mathematics and mechanics_ , pages 679–684, 1957. 

- Christopher P Burgess, Loic Matthey, Nicholas Watters, Rishabh Kabra, Irina Higgins, Matt Botvinick, and Alexander Lerchner. Monet: Unsupervised scene decomposition and representation. _arXiv preprint arXiv:1901.11390_ , 2019. 

7 

- Ayush Chakravarthy, Trang Nguyen, Anirudh Goyal, Yoshua Bengio, and Michael C Mozer. Spotlight attention: Robust object-centric learning with a spatial locality prior. _arXiv preprint arXiv:2305.19550_ , 2023. 

- Rémi Coulom. Efficient selectivity and backup operators in monte-carlo tree search. In _International conference on computers and games_ , pages 72–83. Springer, 2006. 

- Coline Devin, Pieter Abbeel, Trevor Darrell, and Sergey Levine. Deep object-centric representations for generalizable robot learning. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7111–7118. IEEE, 2018. 

- Gamaleldin Elsayed, Aravindh Mahendran, Sjoerd Van Steenkiste, Klaus Greff, Michael C Mozer, and Thomas Kipf. Savi++: Towards end-to-end object-centric learning from real-world videos. _Advances in Neural Information Processing Systems_ , 35:28940–28954, 2022. 

- Stefano Ferraro, Pietro Mazzaglia, Tim Verbelen, and Bart Dhoedt. FOCUS: Object-centric world models for robotic manipulation. In _Intrinsically-Motivated and Open-Ended Learning Workshop @NeurIPS2023_ , 2023a. 

- Stefano Ferraro, Toon Van de Maele, Tim Verbelen, and Bart Dhoedt. Symmetry and complexity in object-centric deep active inference models. _Interface Focus_ , 13(3):20220077, 2023b. 

- Vladimir Frolov, Vitaliy Vorobyov, Leonid Ugadiarov, and Aleksandr Panov. RAPID: Robust Adaptive Probabilistic Inference with DINO Features. In _Hybrid Artificial Intelligent Systems. Lecture Notes in Computer Science_ , 2025. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-MPC2: Scalable, robust world models for continuous control. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- Jeff Hawkins, Subutai Ahmad, and Yuwei Cui. A theory of how columns in the neocortex enable learning the structure of the world. _Frontiers in neural circuits_ , 11:295079, 2017. 

- Jindong Jiang, Fei Deng, Gautam Singh, and Sungjin Ahn. Object-centric slot diffusion. _Advances in Neural Information Processing Systems_ , 36:8563–8601, 2023. 

- Thomas Kipf, Elise van der Pol, and Max Welling. Contrastive learning of structured world models. In _International Conference on Learning Representations_ , 2020. 

- Thomas Kipf, Gamaleldin Fathy Elsayed, Aravindh Mahendran, Austin Stone, Sara Sabour, Georg Heigold, Rico Jonschkowski, Alexey Dosovitskiy, and Klaus Greff. Conditional object-centric learning from video. In _International Conference on Learning Representations_ , 2022. 

- Daniil Kirilenko, Vitaliy Vorobyov, Alexey Kovalev, and Aleksandr Panov. Object-Centric Learning with Slot Mixture Module. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id=aBUidW4Nkd` . 

- Francesco Locatello, Dirk Weissenborn, Thomas Unterthiner, Aravindh Mahendran, Georg Heigold, Jakob Uszkoreit, Alexey Dosovitskiy, and Thomas Kipf. Object-centric learning with slot attention. _Advances in neural information processing systems_ , 33:11525–11538, 2020. 

- Thomas M. Moerland, Joost Broekens, and Catholijn M. Jonker. Model-based reinforcement learning: A survey. _CoRR_ , abs/2006.16712, 2020. URL `https://arxiv.org/abs/2006.16712` . 

- Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever. Zero-shot text-to-image generation. In _International conference on machine learning_ , pages 8821–8831. Pmlr, 2021. 

8 

- Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Maximilian Seitzer, Max Horn, Andrii Zadaianchuk, Dominik Zietlow, Tianjun Xiao, Carl-Johann Simon-Gabriel, Tong He, Zheng Zhang, Bernhard Schölkopf, Thomas Brox, and Francesco Locatello. Bridging the gap to real-world object-centric learning. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Gautam Singh, Fei Deng, and Sungjin Ahn. Illiterate DALL-e learns to compose. In _International Conference on Learning Representations_ , 2022a. 

- Gautam Singh, Yi-Fu Wu, and Sungjin Ahn. Simple unsupervised object-centric learning for complex and naturalistic videos. _Advances in Neural Information Processing Systems_ , 35:18181–18196, 2022b. 

- Aleksandar Stani´c, Yujin Tang, David Ha, and Jürgen Schmidhuber. Learning to generalize with object-centric agents in the open world survival game crafter. _IEEE Transactions on Games_ , 2023. 

- Leonid Ugadiarov, Vitaliy Vorobyov, and Aleksandr Panov. Object-Centric Dreamer. In _Artificial Neural Networks and Machine Learning – ICANN 2025. Lecture Notes in Computer Science_ , 2025a. 

- Leonid Ugadiarov, Vitaliy Vorobyov, and Aleksandr Panov. Relational Object-Centric Actor-Critic. In _Proceedings of the Fourth Conference on Causal Learning and Reasoning, PMLR_ , volume 275, pages 1450–1476, 2025b. 

- Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Shengjie Wang, Shaohuai Liu, Weirui Ye, Jiacheng You, and Yang Gao. Efficientzero v2: Mastering discrete and continuous control with limited data. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Nicholas Watters, Loic Matthey, Matko Bosnjak, Christopher P Burgess, and Alexander Lerchner. Cobra: Data-efficient model-based rl through unsupervised object discovery and curiosity-driven exploration. _arXiv preprint arXiv:1905.09275_ , 2019. 

- Grady Williams, Andrew Aldrich, and Evangelos Theodorou. Model predictive path integral control using covariance variable importance sampling, 2015. URL `https://arxiv.org/abs/1509. 01149` . 

- Weirui Ye, Shaohuai Liu, Thanard Kurutach, Pieter Abbeel, and Yang Gao. Mastering atari games with limited data. _Advances in neural information processing systems_ , 34:25476–25488, 2021. 

- Jaesik Yoon, Yi-Fu Wu, Heechul Bae, and Sungjin Ahn. An investigation into pre-training objectcentric representations for reinforcement learning. _arXiv preprint arXiv:2302.04419_ , 2023. 

- Weipu Zhang, Gang Wang, Jian Sun, Yetian Yuan, and Gao Huang. Storm: Efficient stochastic transformer based world models for reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:27147–27166, 2023. 

- Weipu Zhang, Adam Jelley, Trevor McInroe, and Amos Storkey. Objects matter: object-centric world models improve reinforcement learning in visually complex environments. _arXiv preprint arXiv:2501.16443_ , 2025. 

- Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Martín-Martín, Abhishek Joshi, Kevin Lin, Abhiram Maddukuri, Soroush Nasiriany, and Yifeng Zhu. robosuite: A modular simulation framework and benchmark for robot learning. In _arXiv preprint arXiv:2009.12293_ , 2020. 

9 

## **A SLATE** 

Table 2: Hyperparameters for the SLATE 

||Training dataset size|1000000|
|---|---|---|
||Temp. cooldown<br>Temp. cooldown steps|1.0 to 0.1<br>30000|
||LR for DVAE|0.0003|
||LR for CNN Encoder|0.0001|
|Learning|LR for Transformer Decoder<br>LR warm-up steps|0.0003<br>30000|
||LR half time|250000|
||Dropout|0.1|
||Clip|0.05|
||Batch size|32|
||Epochs|100|
|DVAE|Vocabulary size|4096|
|CNN Encoder|Hidden size|64|
||Iterations|3|
|Slt Attti|Slot heads|1|
|o enon|Slot dim.|192|
||MLP hidden dim.|192|
||Layers|4|
|Transformer Decoder|Heads|4|
||Hidden dim.|192|


## **B DINOSAUR** 

Table 3: Hyperparameters for DINOSAUR 

||Training dataset size|300000|
|---|---|---|
||Training steps<br>|500000<br>|
||Batch size|64|
||LR warm-up steps|10000|
||Peak LR|0.0004|
||Exp. decay half-life|100000|
|Learning|ViT Architecture|ViT-B|
||Feature dim.<br>|768|
||Patch size|8|
||Gradient norm clipping|1.0|
||Image/Crop size|224|
||Cropping strategy<br>|Full|
||Tokens|784|
||Type|MLP<br>|
|Decoder|Layers<br>|4<br>|
||MLP hidden dim.|1024|
||Iterations<br>|3<br>|
|Slot Attention|Slots|5|
||Slot dim.|64|
||MLP hidden dim.|512|


10 

