---
title: "Generative Artificial Intelligence in Robotic Manipulation: A Survey"
date: "2025-03-05"
authors: "Kun Zhang; Peng Yun; Jun Cen; Junhao Cai; Didi Zhu; Hangjie Yuan"
url: https://arxiv.org/abs/2503.03464
pdf: https://arxiv.org/pdf/2503.03464
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.03464)** / [論文ページ](https://arxiv.org/abs/2503.03464)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Generative Artificial Intelligence in Robotic Manipulation: A Survey 

Kun Zhang<sup>_∗_</sup> , Peng Yun<sup>_∗_</sup> , Jun Cen, Junhao Cai, Didi Zhu, Hangjie Yuan, Chao Zhao, Tao Feng, Michael Yu Wang, Qifeng Chen, Jia Pan, Wei Zhang, Bo Yang<sup>_†_</sup> , Hua Chen<sup>_†_</sup> 

**_Abstract_ —This survey provides a comprehensive review on recent advancements of generative learning models in robotic manipulation, addressing key challenges in the field. Robotic manipulation faces critical bottlenecks, including significant challenges in insufficient data and inefficient data acquisition, long-horizon and complex task planning, and the multi-modality reasoning ability for robust policy learning performance across diverse environments. To tackle these challenges, this survey introduces several generative model paradigms, including Generative Adversarial Networks (GANs), Variational Autoencoders (VAEs), diffusion models, probabilistic flow models, and autoregressive models, highlighting their strengths and limitations. The applications of these models are categorized into three hierarchical layers: the Foundation Layer, focusing on data generation and reward generation; the Intermediate Layer, covering language, code, visual, and state generation; and the Policy Layer, emphasizing grasp generation and trajectory generation. Each layer is explored in detail, along with notable works that have advanced the state of the art. Finally, the survey outlines future research directions and challenges, emphasizing the need for improved efficiency in data utilization, better handling of long-horizon tasks, and enhanced generalization across diverse robotic scenarios. All the related resources, including research papers, open-source data, and projects, are collected for the community in https://github.com/GAI4Manipulation/AwesomeGAIManipulation** 

## I. INTRODUCTION 

Robotic manipulation is pivotal in empowering machines to physically interact with and modify their surrounding environment, which is a fundamental step in achieving intelligent autonomy. Ranging from assembling delicate electronic 

_∗_ denotes equal contribution, _†_ denotes corresponding author. 

Kun Zhang, Jia Pan, Wei Zhang, and Hua Chen are with LimX Dynamics, Shenzhen, China. Jia Pan is also with the Department of Computer Science, University of Hong Kong, Hong Kong, China. Wei Zhang is also with the School of System Design and Intelligent Manufacturing (SDIM), Southern University of Science and Technology, Shenzhen, China. Hua Chen is also with the ZJU-UIUC Institute, Zhejiang University, Haining, Zhejiang, 314400, China. Emails: kun.zhang@connect.ust.hk, jpan@cs.hku.hk, zhangw3@sustech.edu.cn, huachen@intl.zju.edu.cn Peng YUN and Bo YANG are with vLAR Group, The Hong Kong Polytechnic University, Hong Kong SAR, China. Emails: _{_ peng-aae.yun;bo.yang _}_ @polyu.edu.hk 

Jun Cen, Junhao Cai, Chao Zhao, and Qifeng Chen are with The Hong Kong University of Science and Technology, Hong Kong, China. Emails: _{_ jcenaa;jcaiaq;czhaobb _}_ @connect.ust.hk, cqf@ust.hk Didi Zhu, and Hangjie Yuan are with Zhejiang University, Zhejiang, China. Emails: _{_ didi_zhu;hj.yuan _}_ @zju.edu.cn 

Tao Feng is with the Department of Computer Science and Technology, Tsinghua University, Beijing, China. Emails: fengtao.hi@gmail.com Michael Yu Wang is with the School of Engineering, Great Bay University, Songshan Lake, Dongguan, Guangdong, China. Email: mywang@gbu.edu.cn 

devices in factories to performing assistive care in homes, robotic manipulation plays a crucial role in applications that significantly impact our society [1, 2]. Manipulation, as one of the most important problems in robotics, has long faced significant challenges in complex environments, especially in scenarios involving nontrivial interactions and intricate longhorizon decision making and planning [1, 3]. Such challenges prevent robotic systems from performing reliable and robust manipulation tasks across different scenarios, leaving a huge gap. 

In recent years, there has been a growing emphasis on datadriven approaches in robotic manipulation, which leverage large-scale data and machine learning techniques to enable robots to better perceive, adapt to, and interact with diverse environments. Thanks to these explosive advances, the aforementioned gap has been drastically closed. In particular, through exploiting the extraordinary abilities of generative learning models in scene understanding, reasoning, task planning and policy synthesis, manipulation skills including operating deformable materials and executing long-horizon task sequences that are widely considered formidably difficult before have been demonstrated. 

Generative learning models, as one of the most important classes of learning models in modern AI, have addressed several previously unresolved challenges in robotic manipulation, particularly in grasping tasks. First, their ability to synthesize diverse and high-quality data has significantly alleviated the reliance on extensive real-world datasets. By generating synthetic grasping scenarios and object variations, these models enable robots to train efficiently and handle a wider range of objects, even in data-scarce environments [4, 5]. Second, their capacity to model high-dimensional action and object spaces allows robots to predict feasible grasp configurations and trajectories for complex or unseen objects [6, 7, 8]. This improves the robot’s ability to adapt to novel tasks and environments, enhancing the robustness of grasp planning. Third, their strength in learning latent representations that capture object structure and interaction dynamics enables robots to generalize across diverse shapes, textures, and physical properties [9, 10]. This ensures more reliable performance in tasks requiring precise manipulation, even in unstructured or dynamic settings. These breakthroughs highlight the transformative potential of generative models in advancing robotic grasping and manipulation. 

In this survey, we focus on generative models due to their potential to address long-standing challenges in manipulation. Generative models offer promising solutions, such as improv- 

2 


Fig. 1. Overview of this survey. Versatile generative models in robotic manipulation. 

ing scene understanding, reasoning, and task planning, which effectively mitigate these issues. In the following paragraphs, we list the key challenges in manipulation and discuss the potential mechanisms through which generative models can overcome these obstacles. 

## _A. Major Challenges in Modern Manipulation_ 

First, **insufficient data and inefficient data acquisition remain critical bottlenecks** . Data-driven methods have been gradually becoming one of the dominant methodologies in solving manipulation problems. The data-driven methods, such as Reinforcement Learning (RL) and Imitation Learning (IL), are well known to be data hungry, requiring vast amounts of high-quality data to train effective models [11, 12]. Collecting high-quality data often necessitates either human intervention or extensive real-world robot experiments, which are time-consuming and difficult to scale to a large amount[13]. To simplify the data generation problem, some researchers have explored transfer learning from other tasks or domains [14, 15, 16], and techniques like domain randomization to mitigate data scarcity [4]. However, the reliance on highquality, task-specific data continues to hinder performance and scalability. Addressing these issues is essential for unlocking the full potential of data-driven robotic manipulation. 

Generative models like Stable Diffusion [17] and largescale pre-trained language models [18] have demonstrated remarkable capabilities in producing high-quality synthetic images, videos, annotations, and reward signals. These models enable the creation of abundant and diverse datasets, significantly alleviating the data insufficiency problem by providing scalable and efficient data generation pipelines. The synthetic 

data can be utilized to train and validate robotic manipulation models, enhancing their performance and generalization abilities. Additionally, the ability to generate rich reward functions facilitates more effective reinforcement learning by offering detailed feedback and enabling exploration in complex environments. This focus on data and reward <u>generation</u> lays the foundation for overcoming data scarcity and inefficient data acquisition, thus propelling the field of robotic manipulation forward. 

Second, **long-horizon task and complex task planning pose significant challenges** . Complex tasks, such as multistep assembly operations, object rearrangement in cluttered environments, and collaborative tasks with humans [19], require robots to plan and execute extended sequences of interdependent actions. Effective planning demands sophisticated modeling techniques and often assumes full observability of the environment [20]. However, in real-world scenarios, full observation is rarely feasible, necessitating that agents develop an intrinsic understanding of tasks, including causal relationships and the effects of their actions on the environment [9, 21]. Traditional deterministic models struggle to capture this complexity due to their inability to adequately represent the uncertainties and dynamic interactions inherent in longhorizon tasks [22]. 

Generative models contribute significantly to addressing long-horizon task planning by enabling the decomposition of complex tasks into manageable sub-goals through techniques like Chain-of-Thought reasoning [23]. Leveraging the capabilities of language <u>generation</u> and code <u>generation,</u> largescale generative models assist robots in planning intricate sequences of actions by breaking them down into simpler, 

3 

sequential steps [24, 25]. This approach allows agents to generate explicit chains of thought and action plans, enhancing their understanding and execution of complex tasks. By incorporating these generative techniques, robots can better handle the uncertainties and dynamic interactions inherent in longhorizon tasks, thereby improving their overall performance in manipulation scenarios. 

Furthermore, generative models enhance robots’ understanding of the physical world by enabling the development of world models and facilitating dynamics learning. By generating intermediate states-explicitly as visual representations, like consequence images [26, 27], or implicitly through <u>latent states</u> [28], these models allow robots to predict and plan for future events in their environment. The capability of visual generation of potential future states improves planning and decision-making processes in manipulation tasks. State generation captures the underlying dynamics essential for accurate task execution, addressing uncertainties and variability in complex environments. This empowers robots to anticipate and adapt to changes during manipulation tasks, enhancing their performance in dynamic settings. 

Third, **policy learning requires multi-modality reasoning abilities** . In robotic manipulation, the current state can correspond to multiple valid actions and outcomes due to task complexity and environmental variability. For example, a mug can be grasped either by the handle or the body, with the optimal choice depending on the subsequent task: grasping the handle is preferable for filling it with water, while grasping the body is better for handing it over to others. Deterministic models often map input observations to single outputs, failing to capture the inherent multi-modality present in many manipulation tasks. This limitation restricts adaptability and hampers performance in diverse situations. By relying on one-to-one mappings, these models struggle to represent the full spectrum of possible actions, thereby hindering the development of more flexible and generalizable robotic systems. 

Generative models have shown significant potential in policy learning, particularly in <u>grasp generation</u> and trajectory <u>generation</u> for robotic manipulation tasks [6, 29, 30, 31]. By modeling the action sequences of entire trajectories, generative models enable joint optimization of control policies. For instance, diffusion models have been applied to policy learning, allowing for the generation of smooth and feasible motion trajectories [29]. These models can incorporate constraints inherent in the robot’s operational space, such as SE(3) constraints for generating valid grasp poses in three-dimensional space [8]. This capability enhances the robot’s ability to perform precise and complex manipulation tasks by generating policies that are both efficient and physically plausible.Moreover, their ability to model multi-modal distributions allows them to capture the diverse possible grasp poses and motion trajectories essential for complex manipulation tasks. 

## _B. Structural Overview of the Survey_ 

In summary, generative models offer solutions across multiple layers of robotic manipulation: from foundational data 

and reward generation to advanced task planning and policy modeling. By addressing the key challenges of data insufficiency, complex task planning, low-level control, and representation learning, generative models pave the way for more autonomous, efficient, and capable robotic systems. Several surveys have explored topics related to robotics and generative models [3, 32, 33]. These works have examined foundational models in robotics and the progression towards general artificial intelligence. However, none have specifically concentrated on how generative models can address the key challenges in robotic manipulation. Our survey focuses on the application of generative models in manipulation tasks, trying to provide a unified yet specific perspective on the roles of generative models in robotic manipulation at different layers. In our survey, by emphasizing the benefits that generative models bring to these specific areas, we aim to fill the existing gap in the literature. Figure 1 shows the overall structure of our surveyed approaches. 

To systematically understand the role of generative models in robotic manipulation, we categorize their applications into three hierarchical layers: **Foundation Layer** , **Intermediate Layer** , and **Policy Layer** . This structure reflects the progressive flow from fundamental data synthesis to high-level decision-making to low-level control. The foundation layer focuses on generating essential resources, such as synthetic data to augment limited datasets and reward signals to guide reinforcement learning, forming the backbone for model training and evaluation. Building on this, the intermediate layer encompasses tasks like language, code, visual, and state generation, which enable robots to interpret instructions, process sensory data, and reason about their environment, bridging perception and action. Finally, the policy layer directly addresses the core robotic manipulation problem, including grasp generation and trajectory planning, translating insights from the lower layers into actionable control strategies. This layered framework highlights the interdependence of these components, ensuring a comprehensive and scalable approach to robotic learning and control. 

## II. BACKGROUND IN GENERATIVE LEARNING MODELS 

Generative models have emerged as a class of powerful tools in machine learning. Focusing on the problem of synthesizing complex data distributions, generative models offer core advantages such as capturing underlying patterns, generating diverse outputs, and enabling adaptive solutions across tasks. In the field of robotic manipulation, these models have been adopted to address various crucial challenges, such as generating realistic data, planning precise trajectories, and adapting to dynamic and unstructured environments. By leveraging their ability to model uncertainty and handle highdimensional data, generative models enhance robots’ capacity for generalization, decision-making, and task execution. In this section, we provide an overview of several foundational generative model paradigms, highlighting their principles and significance in robotic manipulation. 

4 


Fig. 2. Overview of generative models. 

## _A. Generative Adversarial Network (GAN)_ 

Generative Adversarial Networks (GANs) consist of two components: a generator and a discriminator. The generator aims to create realistic data samples from random noise, while the discriminator attempts to differentiate between real and generated samples. The two networks are trained simultaneously in a zero-sum game, where the generator tries to fool the discriminator and the discriminator improves at distinguishing real data from fake ones. This adversarial training process leads to high-quality generated data over time [34]. 

Mathematically, the objective function for GANs can be written as follows: 


where _p_ data( _x_ ) represents the distribution of real data and _pz_ ( _z_ ) is the prior distribution of the noise input. The generator _G_ aims to minimize the loss by producing data that can deceive the discriminator _D_ , which maximizes its ability to distinguish between real and fake data. 

In robotic manipulation, GAN can be leveraged to enhance a robot’s ability to perform complex tasks. By learning the distribution of successful manipulation strategies from realworld data, the generator can produce novel and feasible action sequences for tasks such as grasping, object handling, and tool use [35]. The discriminator ensures these generated actions are realistic by comparing them against actual manipulation examples. These approaches allow robots to adapt to new and unstructured environments by generating manipulation policies that are not only effective but also generalizable, thus improving their performance in tasks requiring fine motor skills and adaptability. 

## _B. Variational Autoencoder (VAE)_ 

Variational Autoencoder (VAE) [36] aims to learn a probabilistic mapping from a lower-dimensional latent space to 

the data space. By modeling the data distribution using an encoder-decoder structure, VAEs learn to generate new data by sampling from the learned latent space. One of the key features of VAEs is their ability to perform efficient inference and generation using variational inference. 

The training objective for VAEs is to maximize the Evidence Lower Bound (ELBO), which approximates the log-likelihood of the data: 


Here, _q_ ( _z|x_ ) is the approximate posterior distribution of the latent variables given the data, and _D_ KL represents the KullbackLeibler divergence between the approximate posterior and the prior distribution _p_ ( _z_ ). The first term encourages reconstruction of the data, while the second term regularizes the latent space to follow a specified prior. 

VAEs enable compact, probabilistic representations that bridge high-dimensional sensory inputs and task-specific outputs in robotic manipulation. Their ability to encode data into a structured latent space facilitates smooth trajectory generation, and adaptable grasp planning. In trajectory generation, VAEs allow robots to explore diverse paths by sampling from the latent space, maintaining continuity and adaptability in motion planning [31]. For grasp planning, VAEs generate diverse, physically plausible grasps by learning compact latent spaces, enabling adaptability to object variability and uncertainty [8, 37]. 

## _C. Diffusion Model_ 

The landscape of robotic manipulation has been significantly enriched by the advent of advanced generative models, particularly diffusion models. Among these, Denoising Diffusion Probabilistic Models (DDPM) [38] and Denoising Diffusion Implicit Models (DDIM) [39] have emerged as powerful frameworks that offer unique advantages for enhancing robotic capabilities in complex manipulation tasks. 

5 

These models that working by simulating a forward process where data is gradually corrupted with noise, followed by a reverse process that attempts to denoise the data and recover the original input. A neural network typically parameterizes the reverse process, and training the model involves learning to reverse the noise addition at each step. 

The forward and reverse processes can be described as 


Reverse: _pθ_ ( _xt−_ 1 _|xt_ ) = _N_ ( _xt−_ 1; _µθ_ ( _xt, t_ ) _, σθ_ ( _xt, t_ )) _._ 

In the forward process, noise is gradually added to the data _xt−_ 1 over multiple timesteps, parameterized by _βt_ . The reverse process aims to recover the data by learning the reverse conditional distribution _pθ_ ( _xt−_ 1 _|xt_ ), where _µθ_ ( _xt, t_ ) and _σθ_ ( _xt, t_ ) are learned by the model. 

DDPM operates by gradually adding noise to an input data distribution through a series of time steps, transforming it into a simple noise distribution. The model is then trained to reverse this process, gradually denoising the data to reconstruct the original input. This mechanism allows DDPM to generate diverse and realistic outputs that capture the nuances of realworld interactions, which is crucial for robotic manipulation tasks that require adaptability and precision. 

On the other hand, DDIM introduces an implicit approach to the diffusion process, allowing for more efficient sampling without compromising the quality of the generated outputs. By providing a deterministic mapping from the noise space back to the data space, DDIM enables faster inference times while maintaining the high fidelity of the generated trajectories. This is particularly beneficial in robotic applications where real-time implementation is essential, such as in dynamic environments where robots must adapt to changing conditions and execute tasks with minimal latency. 

## _D. Probabilistic Flow_ 

Probabilistic flows [40] are generative models that learn invertible transformations between a simple prior distribution (e.g., Gaussian) and the complex data distribution (e.g., Images). These models rely on an invertible mapping function, which allows for both efficient likelihood estimation and exact inference. The generative process can be described as applying a sequence of invertible transformations to a simple latent variable. The generative process is defined by 

Forward: _z_ = _fk_ +1( _hk_ ) _◦ fk_ ( _hk−_ 1) _◦· · · ◦ f_ 2( _h_ 1) _◦ f_ 1( _x_ ) _,_ Reverse: _x_ = _f_ 1<sup>_−_1(</sup><sup>_h_1)</sup><sup>_◦f_</sup> 2<sup>_−_1(</sup><sup>_h_2)</sup><sup>_◦· · · ◦f_</sup> _k_<sup>_−_1(</sup><sup>_hk_)</sup><sup>_◦f_</sup> _k_<sup>_−_</sup> +1<sup>1(</sup><sup>_z_)</sup><sup>_,_</sup> 

where _f_ is an invertible function, and _p_ ( _z_ ) is the prior distribution over the latent variable. The probabilistic flow model learns the invertible function so that it could gradually transforms the complex data distribution to the simple prior distribution, and uses the reverse function to generate the data. 

Unlike models such as GANs and VAEs, flow-based models explicitly learn the data distribution. This explicit learning enables the direct computation of exact log-likelihoods, simplifying model training and evaluation. Thanks to these characteristics, flow-based models have found broad application 

in robotics, including anomaly detection [41, 42], navigation [43], and manipulation [44]. 

## _E. Auto-regressive Model_ 

Auto-regressive Models become super popular after the large language model. ChatGPT [45] shows its strong zeroshot generalization ability in the natural language processing area. Auto-regressive models generate the tokens step by step, conditioning each step on the previous ones. Auto-regressive models factorize the likelihood of the data as a product of conditional distributions, where each data point is generated based on the previous ones. The likelihood factorization is given by 


Here, the probability _p_ ( _xi|x_ 1 _, . . . , xi−_ 1) is modeled by an auto-regressive model, which learns to capture the dependencies between the data points in the sequence. 

Auto-regressive models have shown their excellent generation ability in the natural language processing domain [18, 45, 46, 47, 48] and visual generation domain [49, 50, 51, 52], especially with the larger training data and larger model size [53]. In the robotics domain, auto-regressive models could serve as the middle module to generate languages or images for task decomposition. In addition, vision-language-action models [54, 55] extends the multi-modality large language model to involve the action generation in the whole autoregressive generation process. 

## III. FOUNDATION LAYER 

In robotic manipulation systems, the Foundation Layer serves as the underlying infrastructure that enables effective learning and decision-making. This layer is responsible for generating the essential building blocks required for training and evaluation. 

## _A. Data Generation_ 

Data generation is fundamental in advancing robotic manipulation and addressing data scarcity. In this subsection, we provide an overview of existing efforts categorized into three aspects. Data Generation via simulation, Data Generation via a Generative Model, and Data Augmentation using a Generative Model. As shown in Table I, we present a granular and layered classification of data generation in robotic manipulation tasks. Together, these techniques form a comprehensive strategy for equipping robotic systems to handle the complexity of realworld environments effectively. 

**Data Generation via Simulation.** Simulation-based data generation plays a vital role in expanding the availability and diversity of data for manipulation. Modern simulation platforms, powered by high-fidelity physics engines such as PyBullet [56], MuJoCo [57], CoppeliaSim [58], NVIDIA Omniverse and Unity, enable accurate modeling of physical interactions, including friction, contact, and collisions. These 

6 


Fig. 3. Overview of generative models for robotic manipulation. The taxonomy shows three main categories, each with detailed sub-categories describing specific approaches and methodologies in robotic manipulation. 

environments allow researchers to design low-cost, controllable training setups that support scalable data generation across various scenarios. 

Despite their advantages, simulation-based methods face Sim-to-Real [59], where there is a gap between simulated and real world environments. Researchers have developed techniques such as domain randomization to address this [60, 61], introducing variability in visual and physical properties (e.g., lighting, textures) to better align synthetic data distributions with real-world conditions. Dynamic simulation environments also allow fine-grained control over scene parameters such as object shapes, materials, and viewpoints, enabling researchers to curate robust datasets. These methods demonstrate significant success in improving real-world performance while reducing dependency on large datasets. 

**Data Generation via Generative Model.** Unlike simulations, generative models can produce realistic data without relying on physics engines. Some researchers have begun to utilize foundation models (such as VLM, and diffusion model) 

to generate data to address data scarcity. In this subsection, we will review scenario generation and presentation generation in manipulation tasks. 

_Scenario Generation:_ Scenario generation produces enriched data in the simulation for specific tasks. Recent investigation [62] summarizes two common categories for creating simulation scenes for manipulation tasks: (i) Real-toSim method, which uses generative models to convert realworld scenes into simulations. (ii) Task-specific method, which involves custom assets tailored to specific tasks. In the former, the 3D models of objects can be constructed from point clouds or images using the generative method. GRUtopia [63] further advances scenario generation by creating 100k interactive, finely annotated scenes within 3D society for various robots. While these methods can generate scenes directly based on predefined conditions, challenges remain in accurately capturing the material and physical properties of objects. In the latter, tailored assets offer greater flexibility, but these assets must be properly imported and configured. In most recent 

7 

TABLE I 

TAXONOMY OF DATA GENERATION IN ROBOTIC MANIPULATION TASK, ORGANIZED AROUND GENERATIVE AI. 

|Taxonomy|Category|Method|
|---|---|---|
|Data Generation via Simulation|Traditional Simulator|e.g. PyBullet, MuJoCo, CoppeliaSim, Unity|
|Data Generation via Generative Model|Scenario Generation|e.g. GRUtopia, Gen2Sim, RoboGen, HOLODECK, Sora, UniSim|
||Demonstration Generation|e.g. MimicGen, CyberDemo, RoboGen, DMD, DexMimicGen,<br>I-Gen, Skill Acquisition, GRRsidents, GRUtopia|
||LLM/VLM-based|e.g. ROSIE, RoVi-Aug, DIAL, RACER|
|Data Augmentation using Generative Model|Diffusion-based|e.g. GenAug, ROSIE, RoVi-Aug, CACATI, Roboagent,<br>ISAGrasp, DALL-E-Bot|
||Point-based|e.g. ExAug|


work, the diffusion model is used to develop a multi-gripper grasping scenario generation framework [64], which integrates 8 gripper types and over 1k objects to generate cluttered scenes. Gen2Sim [65] uses LLM and vision generative models to automatically generate 3D assets and task descriptions, providing a diverse asset repository for manipulation. Similarly, RoboGen [5] leverages LLM to first generate asset sizes and configurations, and then create the corresponding assets via text-to-image-to-3D technology. Recently, HOLODECK [66] system is proposed to generate diverse 3D scenes that match user-supplied prompts. Moreover, the world simulator is showing significant potential, such as Sora [67] and UniSim [68], to learn Internet-scale data to simulate diverse environments, further advancing simulation capabilities. 

_Demonstration Generation:_ Current demonstration generation methods expect to enhance manipulation using minimal human demonstrations. For example, MimicGen [69] introduces a data generation system that automatically creates new demonstrations for novel scenes, generating over 50k demonstrations across 18 tasks from just 200 human demonstrations. CyberDemo [70] simulates human demonstrations to perform real-world tasks, accounting for both visual and physical variations. On the other hand, DMD [71] leverages state-of-the-art diffusion models to synthesize enhanced expert demonstrations. RoboGen [5] proposes a full pipeline for generating endless skill demonstrations. DexMimicGen [72] proposes a large-scale generation system that creates 21k demonstrations from just 60 source human demonstrations, exploring the effects of grasping performance across several generation models. I-Gen [73] generates corrective intervention demonstration data from limited human interventions. And some work [74] leverage LLMs for language-guided skill acquisition, generating diverse and rich manipulation demonstrations. Meanwhile, GRResidents [63] employs an LLMdriven system for task generation and assignment, producing 300 episodes for loco-manipulation benchmarks. 

However, these methods still encounter limitations, such as insufficient diversity in assets and robotic forms. Additionally, data generated by these models may exhibit some lack of controllability and may fall short in physical consistency, particularly in complex scenarios involving physical interactions. 

**Data Augmentation using Generative Model.** A prevalent usage for data augmentation is leveraging generative models to enhance data diversity in manipulation. Traditional studies 

applied augmentation techniques in low-level visual spaces, such as color jittering, blurring, and cropping. As generative models demonstrate powerful content generation capabilities, e.g., text-to-image diffusion models and vision-language models, these advanced models are increasingly being utilized for broader data augmentation. 

In detail, diffusion models are commonly used for modifying or editing textures and shapes to perform augmentation procedures. For example, GenAug [75] uses a depthguided diffusion model to change backgrounds, object textures, or categories, and add distractors to perform scene augmentation. ROSIE [76] utilizes a T2I model to create a variety of unseen objects, backgrounds, and distractors based on an existing dataset. RoVi-Aug [77] uses state-of-the-art diffusion models to expand data with different viewpoints. ISAGrasp [78] proposes implicit shape-augmented grasping via a correspondence-aware generative model to extrapolate human demonstrations for dexterous manipulation. DALLE-Bot [79] can rearrange objects within a scene, generating images that represent natural, human-like object placements. Video painting is used to mask human hands [80] and replace them with grippers to augment the data [81]. Mirage [82] introduces a cross-painting method for unseen robots, which successfully achieves zero-shot transfer between different robotic arms and grippers. CACTI [83] leverages diffusion models and in-painting for controllable generation of scenes, enabling automated data augmentation. Similarly, RoboAgent [84] employs in-painting techniques to propose semantic augmentation, rapidly enriching existing datasets and equipping robots with multiple manipulation skills. And ExAug [85] utilizes point clouds to extract 3D information to create more complex and structured augmentations. Note that an important challenge of these approaches is to ensure that the augmented data is physically accurate while guaranteeing semantic and visual diversity. For example, in-painting techniques that edit the objects within the grasper may result in physically unrealistic grasps, leading to poor performance on downstream tasks. 

Moreover, LLM and VLM can also contribute to data augmentation in grasping tasks. ROSIE [76] first locates the augmented regions using an open vocabulary segmentation model, which is then edited. Similarly, RoVi-Aug [77] also uses VLM to perform segmentation procedures before 

8 

augmenting the data. RACER [86] proposed an automatic data enhancement pipeline for failure recovery and extended the expert demonstration with LLM. DIAL [87] acts as an automated annotator for robotic datasets, effectively importing semantic knowledge from CLIP into existing data. 

## _B. Reward Generation_ 

Reward generation refers to the process of learning a reward function that guides policy optimization to achieve the highest task success rate. Limitations before the usage of generative models primarily include the challenge of sparse rewards [88], where agents rarely reach the desired goal early in training, resulting in insufficient feedback to effectively optimize policies. The structure of this section focuses on two key applications of generative models in reward generation: providing supervision signals and offering policy scores. Providing supervision signals using generative models involves leveraging large-scale pre-trained models (e.g., Vision-Language Models, VLMs) to generate structured information, such as success indicators [89] or goal descriptions, which serve as detailed feedback for policy learning. Providing policy scores using generative models entails using generative models to evaluate policy performance online, such as measuring the distance between predicted actions and goals or generating constraints to optimize policy selection, thereby improving task execution efficiency and stability. 

**Providing Supervision with Generative Model.** The advancement of large-scale pre-trained foundation models has led to significant processes in the generalization ability of robotic manipulation skills. While it is challenging to generalize policy across complex tasks, the large-scale pre-trained foundation models achieve high accuracy in a zero-shot learning manner to unseen environments. Some work adopts largescale pre-trained foundation models to supervise adapting the manipulation policy. 

Ge _et al._ [90] proposed PAFF framework, which collects domain-specific data using pre-trained foundation models to provide feedback to relabel the domain-specific demonstrations. They cast the relabelling demonstrations as a visual-tolanguage retrieval tasks, and compare off-the-shelf pre-trained foundation models, including MoCo [91], DenseCL [92], MAE [93], GLIP [94], CLIP [95] and MDETR [96], in relabelling demonstrations. By harnessing the generalization capabilities inherent in large-scale vision-language foundation models, specifically in the context of recognizing visual content, they relabeled the recorded demonstrations for fine-tuning the policy in an automatic way and updated the policy in unseen environments with a test-time training strategy. Building upon the idea of leveraging foundation models for robotics, Vuong _et al._ [97] introduce GraspAnything++ dataset, which supports supervision at multiple levels of granularity, including scene-level, object-level, and part-level annotations. They use Stable Diffusion [17] to proceed text-to-image generation for scene generation, adopt OFA [98] and SAM [99] to provide object-level masking, and leverage VLPart [100] to provide part-level masking, and generate grasp poses with RAGT3/3 [101] pre-trained models. Blank _et al._ [102] propose a 

similar but object-centric automated labeling pipeline based on VLMs in a concurrent time. The downside of emsembling multiple foundation models is from the significant computational cost. 

During the early stage of training, rewards are often sparse as agents seldom accomplish the intended objective. Sumers _et al._ [103] treat generative vision-language models as relabelling functions and adopt the Hindsight Experience Replay (HER) [104] framework to densify rewards. They use a generative VLM (Flamingo [105]) to generate language instructions for failed trajectories and supervise the training of languageconditioned agents. It distillates the VLM’s domain-general language grounding into domain-specific embodied agents. Similarly under the HER framework with VLM as a relabelling function, DIAL employs a CLIP model fine-tuned on robotic demonstrations and autonomous data that has been hindsightlabeled by human annotators. This fine-tuned model is then used to further relabel a larger set of offline robotic trajectories, enabling the training of a language-conditioned policy through behavior cloning. 

Besides imitation learning, Xie _et al._ [106] adopt VLMs to generate reward code to train reinforcement-learning policies. Given the observation and action, the VLMs generate Pythonic representations for reward shaping. Background knowledge is injected with pre-defined helper functions. In order to improve the grounding of VLMs in specific tasks, They inject fewshot examples and human feedback into the prompts when training RL policies, and Ma _et al._ [88] further enhance the reward design process by leveraging an iterative evolutionary search mechanism, where reward candidates are sampled, evaluated and refined based on textual feedback summarizing training performance. This approach allows EUREKA to autonomously generate interpretable and task-specific dense reward functions that outperform human-designed rewards in most cases. 

Although VLMs are effective in providing meaningful signals, their inaccuracies can also lead to misleading outcomes. To address this reward misalignment issue, Fu _et al._ [107] thoroughly analyzed the problem and proposed a two-fold solution. First, they introduce lightweight projection layers combined with contrastive learning to align the rewards more effectively. Second, they incorporate a Relay RL mechanism, which employs an auxiliary SAC agent to assist exploration when the primary VLM agent gets stuck in local minima. This collaborative approach allows the agent to escape suboptimal regions and collect diverse samples, which in turn enhances reward alignment and policy learning. Experimental results show that their method significantly improves performance across various sparse reward tasks, demonstrating both the effectiveness of reward alignment and the critical role of Relay RL in addressing exploration challenges. 

**Providing Policy Scores with Generative Model.** The ability to score a policy in deploying in environments is the core of sample-based planning. A typical way is to measure the distance between the policy prediction and the goal in metric space [108, 109, 110, 111, 112]. The downside is the taskrelated hand-crafted distance function or objective function for constructing the metric space. It is very challenging for this 

9 

scoring approach to generalize beyond the pre-defined task space. 

Generative VLMs also act as reward functions online for policy selection in deployment. Zhao _et al._ [113] design reward functions with the assistance of VLMs for Model predictive control. Besides the typical pixel-distance cost between future predictions and goal images [114], they add constraints generated using VLMs to avoid collision with interference objects. The reward function is a combination of these two costs with an adaptive weight generated by VLMs. Even though it improves the efficiency, it still requires human-engineered design between the predicted images and goal images. Yu _et al._ [115] decompose the reward function generation into two stages: motion description, interprets the task description into a structured natural language description of the desired robot motion; and reward coding, generates code based on predefined functions and low-level motion description in a fewshot learning way. Without explicitly estimating future images, the VLMs directly estimate the reward instead. Its integration into the MPC framework improves the stability of the control system. 

Directly adopting generative VLMs as reward functions is challenging to ground the domain-general model to domainspecific tasks. It requires to be further grounded with specific task-related environment information [103, 116]. Zeng _et al._ [116] extend the bi-level optimization structure in inverse reinforcement learning [117]. The inner loop of the bi-level optimization contains a learned reward function scoring the sampled strategies and conducting the execution, which the outer loop updates this reward function by aligning the ranking between generative VLMs and the output of the reward function. Besides grounding to domain-specific tasks, it is token efficient than adopting VLMs as reward functions. Zhong _et al._ [118] propose a pipeline to adopt LLM to facilitate policy improvement. They use LLM to generate feedback sets to train a feedback model. By identifying desirable actions with the feedback model online, they update the policy. 

## IV. INTERMEDIATE LAYER 

In robotic manipulation paradigms, the Intermediate Layer serves as a crucial component that connects high-level task planning with low-level policy execution. Its primary role is to generate structured, interpretable representations that bridge the abstract commands from task planners and the executable actions required by robotic systems. Depending on the task and context, the Intermediate Layer involves various generation mechanisms, including natural language and code generation for task decomposition, visual and state generation for producing scene-level representations and future predictions. These intermediate outputs simplify the complexity of robotic decision-making by breaking down tasks into manageable sub-goals, ensuring that the robot can operate effectively in dynamic and uncertain environments. By modularizing these processes, the Intermediate Layer enhances the adaptability and scalability of robotic systems across diverse applications. 

## _A. Natural Language Generation_ 

Natural language generation has emerged as a powerful tool for creating executable tasks for robots in a linguistic format. While robots often struggle with complex, long-range tasks, decomposing these tasks into sequences of subtasks before execution has proven to be an effective strategy. Large Language Models (LLMs) have demonstrated remarkable task planning capabilities [25], making them ideal for this purpose. As a result, numerous studies [74, 119, 120, 121, 122, 123] have leveraged LLMs to break down long-horizon robotic tasks into manageable sequences of subtasks. This approach not only simplifies the execution process for robots but also enhances their ability to handle more sophisticated and varied tasks. 

This section explores the advancements brought by generative models and their applications in robotic task planning. Specifically, we discuss Natural Language Generation for task decomposition, which involves breaking down complex tasks into manageable sub-goals using language as an intermediary; physically-grounded language generation, where language outputs are tied to physical states or interactions in the environment, ensuring relevance to robotics; and Language Generation with External Memory, which leverages memoryaugmented architectures to enable reasoning over extended contexts and improve task planning in long-horizon scenarios. Figure 4 shows the structure of this section. 

**Natural language Generation for Task Decomposition.** The task planning capabilities of Large Language Models (LLMs) were first comprehensively evaluated in [25]. This study assessed the executability and correctness of GPT-2, GPT-3, and Codex, concluding that LLMs of sufficient size can generate mid-level tasks without fine-tuning. LLMs have advanced rapidly in recent years, particularly following the release of ChatGPT. A more recent evaluation of language plan generation abilities in popular LLMs is presented in [124], encompassing models such as Claude-3, Claude-3.5, Cohere Command R, Gemini 1.0, Gemini 1.5, GPT-3.5, GPT4, GPT-4o, Llama 3, Mistral, and o1. Table II demonstrates that o1-preview achieves the highest task success rate on both VirtualHome [125] and BEHAVIOR [126] datasets, as well as the best execution success rate on BEHAVIOR. OpenAI’s o1 model’s capacity to generate extended chain-of-thought reasoning prior to producing a final answer endows it with superior reasoning capabilities compared to GPT-4o. This underscores the critical importance of robust reasoning abilities in effective task decomposition. 

A large-scale language plan generation dataset is introduced in EmbodiedGPT [127] based on Ego4D dataset [128]. EmbodiedGPT also proposes a general framework that integrates both high-level language plan generation and low-level action generation. When multi-modality information are encountered, Matcha [129] agent is proposed to guide epistemic actions and to analyze the resulting multi-modal sensations (including vision, sound, haptics, and proprioception). Additionally, it facilitates the planning of entire task executions based on information acquired interactively. 

Although LLMs demonstrate robust language planning ca- 

10 


Fig. 4. Overview of natural language generative methods for manipulation. Natural language generation could be used for task decomposition, and external memory could be introduced to save and retrieve pre-defined skills. Physically-grounded language generation considers the available operations in the current space. Vision-language-action models generate the action along with the language. 

pabilities for manipulation tasks, they are too large to be deployed on a capacity-limited and off-the-shelf devices. To address this challenge, DEDER [130] proposes an innovative solution. This approach constructs a task decomposition dataset with an embodied knowledge graph using an LLM, and subsequently trains a compact language model to learn policies from this graph. Through this process, the reasoning abilities of the LLM are effectively distilled into a smaller language model, enabling real-time inference on edge devices. This method bridges the gap between the powerful capabilities of LLMs and the practical constraints of resource-limited hardware. 

**Physically-Grounded Language Generation.** LLMs often struggle to consider real-world conditions when decomposing tasks, potentially producing sub-plans that are not executable by embodied agents. Several approaches have been developed to address this issue. SayCan [24] employs temporaldifference-based (TD) reinforcement learning to train a value function model, estimating the achievability of each plan. Grounded Decoding [131] trains a grounded model to generate feasible actions, with final plans determined by both the LLM and the grounded model. Inner Monologue [132] incorporates various types of grounded closed-loop feedback into the robot planning pipeline, including success detection, passive scene description, and active scene description, demonstrating the 

TABLE II 

SUBGOAL DECOMPOSITION PERFORMANCE OF COMMON LLMS. V: VIRTUALHOME, B: BEHAVIOR. SR: SUCCESSFUL RATE. 

|Model|Task|SR|Execut|ion SR|
|---|---|---|---|---|
||V|B|V|B|
|Claude-3 Haiku|78.4|30.0|82.8|35.0|
|Claude-3 Sonnet|83.1|39.0|86.4|43.0|
|Claude-3 Opus|86.7|41.0|89.9|47.0|
|Claude-3.5 Sonnet|89.1|39.0|92.0|44.0|
|Cohere Command R|71.3|15.0|78.1|25.0|
|Cohere Command R+|77.8|25.0|83.7|37.0|
|Gemini 1.0 Pro|70.4|24.0|84.6|33.0|
|Gemini 1.5 Flash|89.1|34.0|94.1|42.0|
|Gemini 1.5 Pro|87.0|31.0|91.1|37.0|
|GPT-3.5-turbo|69.2|24.0|81.4|36.0|
|GPT-4-turbo|85.5|38.0|94.1|47.0|
|GPT-4o|87.6|49.0|91.1|55.0|
|Llama 3 8B Instruct|48.8|22.0|58.0|29.0|
|Llama 3 70B Instruct|78.4|21.0|87.3|30.0|
|Mistral Large|84.3|31.0|92.0|38.0|
|Mixtral 8x22B MoE|80.5|28.0|90.2|33.0|
|o1-mini|79.3|31.0|84.6|39.0|
|o1-preview|89.4|57.0|93.2|62.0|


significance of physically grounded feedback for task success. PhyGrasp [133] utilizes an LLM to generate part and physical information, integrating them to produce task-specific grasping pair matches. Ren et al. [134] gather diverse natural language descriptions for different tools and apply language-conditioned meta-learning to develop effective policies. These approaches aim to bridge the gap between language models and physical reality, enhancing the applicability of LLM-generated plans in real-world scenarios. 

**Language Generation with External Memory.** Several studies have explored the integration of external memory with Large Language Models (LLMs) to enhance task performance. SayPlan [135] leverages the hierarchical structure of 3D scene graphs (3DSG) to enable LLMs to perform semantic searches for task-relevant subgraphs from a condensed version of the full graph. RoboMP<sup>2</sup> [136] implements Retrieval Augmented Generation (RAG) [137, 138] to allow Multimodal Large Language Models (MLLMs) to select semantically similar plans from a codebase. Text2Motion [139] retrieves robot skills by conducting geometric feasibility planning [140] throughout its search process. These approaches demonstrate the potential of combining LLMs with external knowledge sources to improve language generation and task execution in various domains. 

## _B. Code Generation_ 

Building upon advancements in language generation, code generation aims to translate high-level natural language instructions into executable robot control programs. By leveraging LLMs or MLLMs, these approaches strive to make robot programming more accessible, allowing non-experts to specify tasks at a conceptual level while automated systems handle the complexities of translating those instructions into lowlevel commands. As shown in Figure 5, current research in robotic code generation can be broadly categorized into three approaches: direct code generation, decomposition-based code generation, and constraint-based code generation. 

11 


Fig. 5. Overview of code generation. Research in robotic code generation can be broadly categorized into three approaches: direct code generation, decomposition-based code generation, and constraint-based code generation. 

**Direct Code Generation.** Direct code generation methods leverage LLMs to produce executable code directly from natural language instructions without intermediate decomposition. Code as Policies [141] first demonstrated that LLMs can generate robot action sequences from high-level commands using predefined APIs, showing promising results in both manipulation and navigation tasks. Building on this, STEVE [142] employs a three-layer architecture—vision perception, language instruction, and code action—to translate multimodal inputs into executable code. RoboScript [143] further integrates perception (e.g., object detection, grasp planning) and motion planning tools into a unified framework, supporting deployment in simulation and on physical robots. RobotGPT [144] introduces decision and verification mechanisms to improve reliability and safety, while Instruct2Act [145] demonstrates adaptability to various instruction modalities by generating Python programs that encompass perception, planning, and control loops. Zhi et al. [146] propose a closedloop approach that continuously refines code execution based on feedback, enhancing resilience to environmental changes. Although direct methods are appealing for their simplicity and broad applicability, they may struggle when facing highly complex, long-horizon tasks that require intricate reasoning, precise motion control, or error recovery capabilities. 

**Decomposition-based Code Generation.** To improve the reliability and interpretability of code generation, decomposition-based approaches first break down complex tasks into simpler subtasks before generating code. ProgPrompt [147] proposes a two-stage framework with a Task Decomposition Agent (TDA) and a Script Generation Agent (SGA). The TDA analyzes the high-level task and decomposes it into a sequence of primitive actions, while the SGA generates specific code for each primitive action using predefined templates and APIs. RoboCodeX [148] takes a similar idea further, using a tree-structured framework to decompose tasks into object-centric manipulation units that incorporate physical preferences (e.g., grasp points, motion constraints). GenSim [149] leverages LLMs to automatically generate rich simulated environments and expert demonstrations, aiding multitask policy training and scaling task complexity. Octopus [150] and Alchemist [151] integrate real-time feedback and 

interactive dialogues, enabling users to refine generated code through natural language instructions and visualization tools. Such methods often show higher success rates and improved performance on complex, multi-step tasks. However, the additional complexity in framework design, data requirements, and runtime overhead can increase development costs. 

**Constraint-based Code Generation.** In real-world robotics, physical and spatial constraints cannot be ignored. Constraint-based approaches explicitly incorporate these factors into the code generation process to ensure the generated code respects real-world limitations and requirements. ReKep [152] introduces Relational Keypoint Constraints that specify spatial and temporal relationships between keypoints in the environment. These constraints guide the code generation process by ensuring that generated robot motions maintain desired spatial relationships and follow natural motion patterns. VoxPoser [153] proposes composable 3D value maps as constraints for robot manipulation. These maps encode spatial preferences and constraints, which are used to optimize robot trajectories and generate corresponding control code. Language to Rewards [115] presents a novel approach that translates natural language instructions into reward functions, which then serve as constraints for generating robot control code through reinforcement learning. When Prolog Meets Generative Models [154] introduces a hybrid approach that combines the logical reasoning capabilities of Prolog with the generative power of LLMs. The system uses Prolog to maintain a knowledge base of physical constraints and rules, which guides the LLM in generating code that respects these constraints. The framework also includes mechanisms for temporal parallel plan generation and automated translation of plans into executable code. By incorporating explicit constraints, these methods can better handle complex spatial relationships and physical interactions, producing more reliable and physically feasible robot behaviors. However, they may require more sophisticated constraint specification and optimization techniques compared to other approaches. 

Direct generation methods offer simplicity and endto-end solutions but may struggle with complex tasks. Decomposition-based methods provide better reliability and interpretability but require more sophisticated architectures. 

12 


Fig. 6. Typical pipelines of visual generation models utilized in robot manipulation. Note that the figures of RGB and RGB-D observations are from VIMA-Bench [155] and GNFactor [156], respectively. 

Constraint-based methods excel at handling physical constraints but may need more complex optimization techniques. Future research might focus on combining the strengths of these different approaches while addressing their respective limitations. 

## _C. Visual Generation_ 

Due to the evolution of the generation paradigm and largerscale pre-training, the quality of images, videos, and point clouds generated by visual generation systems [17, 157, 158, 159] has improved substantially. These advancements in visual generative models are transforming robotic manipulation, enabling robots to better interpret and interact with their environments through synthesized visual cues. By leveraging highly realistic visual outputs, robots can simulate and predict complex manipulation tasks in virtual settings before attempting them in the real world, as illustrated in Figure 6. This not only enhances the robot’s ability to learn and generalize across diverse tasks, but also complements recent progress in language and code generation, enabling robots to interpret and execute instructions across multiple modalities. As a result, these advancements pave the way for safer and more adaptable robot manipulation, contributing to a deeper understanding of multi-object interactions, physical constraints, and taskspecific movements. 

**Video Generation Models.** Video generation models focus on generating videos conditioned on text or images. They holds significant potential for robot manipulation because they enable robots to visualize and plan complex sequences of actions. Additionally, video generation models can incorporate temporal dynamics, offering a better understanding of how actions evolve over time, which is crucial for tasks involving movement, interaction with objects, or long-horizon planning. 

Du et al. [160] introduces an innovative approach UniPi to creating generalized agents by harnessing text-to-video diffusion models [159]. UniPi redefines sequential decisionmaking in robot manipulation as text-conditioned video gen- 

eration. By leveraging the planning capabilities inherent in video diffusion models, UniPi generates sequences of future frames that visually depict intended actions throughout the manipulation process. Control actions are subsequently derived directly from these generated frames, effectively guiding the agent in executing the task. 

Following this line of research, SLOWFAST-VGEN [161] incorporates episodic memory to enhance action-conditioned long video generation. VLP [162] extends this single-modal planning to multi-modal planning by introducing the collaboration of vision planning by Stable Video Diffusion [163] and language planning by ChatGPT. Similarly, HiP [164] utilizes multiple foundation models for hierarchical planning, where video diffusion models form the core of visual planning given a language subgoal and the initial observation. 

However, previous methods, such as UniPi, face limitations due to the open-loop nature of planning. As pointed out by Bu et al. [165], planned actions can deviate from actual trajectories if not verified, which can be especially problematic in long-horizon tasks and dynamic environments. To address this, CLOVER [165] proposes a feedback mechanism to improve the adaptability and accuracy of robotic control. 

These approaches typically rely on separate models for video generation and action planning, which can result in error accumulation due to the interplay between the models. GR-1 [166] addresses this limitation by introducing a unified GPT-style transformer designed for multi-task visual robot manipulation. By utilizing large-scale video generative pretraining, GR-1 successfully transfers generative capabilities to robot manipulation tasks. The follow-up work, GR-2 [167], builds on GR-1, significantly scaling up both the pre-training dataset and the range of tasks the model can handle, including complex scenarios like bin-picking with over 100 objects. 

**Image Generation Models.** In robot manipulation tasks, image generation models provide an alternative to video generation models. Black et al. [168] proposes SuSIE, which leverages an image diffusion model to reframe the planning 

13 

problem as an image editing task [169]. Using language commands, SuSIE’s image editing model generates intermediate subgoals that guide a low-level policy in executing the task. This approach focuses on generating discrete, action-relevant images, which can simplify task planning by providing clear, actionable visual cues. 

In a similar vein, CoTDiffusion [170] enhances image generation by incorporating multi-modal prompts through a semantic alignment module, enabling the generation of coherent subgoal images conditioned on various input signals. This follows a chain-of-thought approach, improving instructionfollowing in long-horizon manipulation tasks, where reasoning over extended action sequences is critical. 

Surfer [171] draws inspiration from I-JEPA [172], generating the next action frame by conditioning on the encoding of the current action frame and predictions of subsequent actions. This progressive reasoning model supports coherent decision-making over multiple steps, enhancing long-term task execution. 

**3D Generation Models.** In robot manipulation tasks, while traditional image and video generation models provide insights into 2D visual representations, 3D generation models are essential for capturing the spatial and semantic complexity of real-world environments. One approach, TAX-Pose [173], processes two segmented point clouds to predict a new point cloud, combining target points and residual corrections to generate accurate 3D structures. This enables more precise planning in environments where spatial relationships are critical. 

IMAGINATION POLICY [174] expands the use of generative models by predicting the movement of points in a 3D space. It employs an iterative velocity model to simulate the evolution of the scene and envision potential future states. These predicted states are then converted into actionable commands using rigid-body motion estimation, facilitating more dynamic and continuous task execution. 

Several approaches shift focus to 3D scene radiance, providing richer, more detailed representations of the environment. Dasgupta et al. [175] proposes an ensemble of partially constructed Neural Radiance Fields (NeRF) models to assess model uncertainty, enabling the selection of optimal actions—whether visual or re-orientational—by balancing informativeness and practicality. Another model, GNFactor [156], enhances NeRF’s generalizability by incorporating a reconstruction loss alongside behavior cloning. This method employs a Perceiver Transformer [176] for decision-making, which has shown strong performance in both simulated and real-world robotic manipulation tasks. 

Despite their advances, these methods often fail to account for the dynamic, interactive nature of scenes, particularly in tasks where objects interact over time. To address this limitation, ManiGaussian [177] introduces a dynamic Gaussian Splatting framework to model the spatiotemporal dynamics of the scene. By using a Gaussian world model, the system can parameterize the distribution of these dynamic interactions, enabling the robot to adapt and plan more effectively in complex and interactive environments. 


Fig. 7. Overview of state generative models. The latent state can represent the environment’s observation (top) or encode the dynamic information of the task (down). 

## _D. State Generation_ 

State Generation is the process of creating meaningful and compact representations of an environment or task dynamics, enabling robots to interpret and interact with their surroundings effectively. In contrast to generating visual predictions in input space, it is efficient and compact to generate predictions in latent space [178]. Compared to predictions in image space as discussed in Section IV-C, latent states possess a footprint with limited memory, thereby facilitating the capability to simulate thousands of trajectories concurrently. Before generative models, state representation often depended on explicit, highdimensional sensory data, which was not only computationally expensive but also struggled to generalize across complex or dynamic scenarios. 

This section explores two key aspects: how generative models can enhance observation modeling and dynamics modeling. Modeling observation leverages generative models to transform raw sensory inputs into structured latent representations, capturing essential features while reducing noise and redundancy, which streamlines downstream tasks like planning and control. Modeling dynamics, on the other hand, focuses on predicting state transitions and understanding action dependencies, allowing robots to anticipate future states and plan trajectories with greater accuracy and adaptability in evolving environments. 

**Modeling observation.** To effectively represent the environment for downstream tasks, modeling observation fo- 

14 

cuses on learning compact and meaningful visual or multimodal representations that capture relevant features from raw sensory inputs. Nair _et al._ [111] study how visual representations pre-trained on ego-centric human video data for downstream robotic manipulation tasks. Three solutions, time-contrastive learning, video-language alignment, and L1 penalty, are adopted to achieve this goal. The approach is evaluated on three simulation benchmarks and the real world setting. 

Ma _et al._ [179] propose an objective function for pretraining representation on human videos, and the distance in embedding space can be used for reward scoring. They pre-train an encoder on the Ego4D dataset and test in the simulation environment FrankaKitchen by comparing with CLIP and R3M. In the following work LIV _et al._ [109], they focus on language-image representation pretraining and propose an objective function for learning the multi-modal pretraining representation based on the EpicKitchen dataset. The authors also claim that this objective supports finetuning on domain-specific dataset and the learned representation can be used along with L2 norm distance function for calculating intermediate reward of a policy. 

Different from learning vision-language representation with contrastive learning, Mu _et al._ [180] get inspired from neural language processing and adopt emergent communication scheme to learn multi-modality representation. They pre-train a speaker and listener via an emergent communication game to generate emergent language, which could be considered as a domain-specific latent code. In the emergent communication game, a language model is also trained to predict masked trajectory, so that it can be used for policy generation following videos or language instructions. 

**Modeling Dynamics.** Modeling dynamics emphasizes capturing the dependencies between sequential states and actions, enabling the prediction of future states and transitions in a task, which is crucial for long-horizon planning and decisionmaking. Hafner _et al._ [9] propose Dreamer, which represents the state with latent code and generate future state in longhorizon latent imagination. The generated state is integrated in an actor critic RL framework which optimizes a parametric policy by propagating gradients through learned latent dynamics. The Dreamer pipeline has shown success in Artari [181], Minecraft games and Visual Control tasks [182]. Bauer _et al._ [10] extend the concept of latent space dynamics modeling to deformable object manipulation by encoding visual input into latent space and estimating dynamics with auto-regressive mechanisms. Their work goes beyond Dreamer by jointly modeling both geometrical and topological changes, enabling predictions of splitting and merging events in elastoplastic objects. This integration of topological reasoning complements Dreamer’s focus on long-horizon latent imagination, demonstrating the versatility of latent space modeling for tasks that require complex structural transformations. 

Learning dynamics from scratch without any preliminary knowledge demands substantial interactions with the environment. Build upon the success of large-scale pre-training approaches and contrastive learning, researchers adopt selfsupervised learning approaches to pre-train the model as a 

video prediction model [109, 111, 179, 183]. The states, generated by pre-training models, encapsulate the visual and language information and be used as reward or integrated in policy network in downstream tasks. These video prediction models capture the transition dependencies between sequential states, yet cannot depict the causality that connects these sequential states due to their lack of action modeling. To solve this problem, Zhang _et al._ [184] propose an action-conditional pre-training scheme with learnable action representations. They design an inverse dynamics encoder to predict action latent states from successive images and align this action latent space with real action representations. This approach bridges the gap between pre-training and fine-tuning, enabling the transfer of learned representations to downstream tasks effectively. 

## V. POLICY LAYER 

In robotic manipulation paradigms, the policy layer modules aim to generate the executable actions for the robotic hardware systems given the high-level task commands and observations including visual and proprioceptive measurements. In general, the resultant action space would be either target end-effector pose or a trajectory of the end-effector. 

## _A. Grasp Generation_ 

As the first instance of policy generation in robotic manipulation, the grasp generation class focuses on finding the target end-effector pose, often represented as a 4-D or 6-D coordinate in the robot’s space, given inputs including RGB images, depth images or point clouds, meshes, and more recently, implicit shape representations such as Neural Radiance Fields (NeRF) [185]. These inputs provide rich spatial and visual information about the object to be grasped, allowing models to reason about the geometry, appearance, and affordance of the object. 

In some cases, intermediate representations, such as grasp rectangles in the image space, are used to simplify the problem formulation. Some approaches predict grasp quality as output when the input includes both the observation and candidate poses, enabling the model to assess the likelihood of success for each candidate grasp. 

Learning-based grasp synthesis has been widely studied in the robotic community [196, 197, 198]. Various learning models have been proposed to solve the grasp synthesis problem. Deterministic models, for instance, map the input observations directly to a grasp pose or grasp quality score. These models aim to establish a mapping in which a specific observation corresponds to a determined output pose [13, 199]. While proven effective in many cases, deterministic models may struggle with multi-modal grasp pose distributions, where multiple distinct grasp solutions exist for a single object—essentially mapping a non-injective, non-surjective function. 

To address this limitation, generative models have gained popularity in recent years. Unlike deterministic approaches, generative models aim to learn a distribution over grasp poses. By mapping from a complex, multi-modal grasp distribution to simpler, more tractable distributions, generative models can 

15 

TABLE III 

GENERATIVE MODELS FOR GRASP GENERATION 

||**Ge**<br>**Fra**|**nerative**<br>**mework**|**Input**|**Obse**|**rvation**|**Data**||**Ha**|**nd T**|**ype**|**O**|**thers**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Diff|VAE<br>Other|2D<br>3D<br>Multi|Full|Partial|Real<br>Sim|Hybrid|Parallel-jaw|Multi-fingered|Human hand|Real-world<br>Experiment|Language-guided<br>Open-source|
|SE(3)-DiF [29]|✓||✓|✓|✓|✓||✓|||✓|✓|
|Singh et al. [30]|✓||✓|✓||✓||✓||||✓|
|Diffusion-EDFs [186]|✓||✓|✓||✓||✓|||✓|✓|
|Vuong et al. [97]|✓||✓||✓|✓||✓|||✓|✓<br>✓|
|Guo et al. [187]|✓||✓||✓||✓|✓|||✓||
|DexDiffuser [188]|✓||✓||✓|✓|||✓||✓|✓|
|DexGraspNet 2.0 [189]|✓||✓||✓|✓|||✓||✓||
|Freiberg et al. [64]|✓||✓||✓|✓|||✓||✓||
|S2HGrasp [190]|✓||✓||✓|✓||||✓||✓|
|G-HOP [191]|✓||✓|✓||✓||||✓|||
|GraspNet [37]||✓|✓||✓|✓||✓|||✓|✓|
|Contact-GraspNet [8]||✓|✓||✓|✓||✓|||✓|✓|
|Wu et al. [192]||✓|✓|✓||✓||||✓||✓|
|Jiang et al. [193]||✓|✓|✓||✓||||✓||✓|
|GrainGrasp [194]||✓|✓|✓||✓||||✓||✓|
|Wu et al. [195]||✓|✓||✓|✓|||✓|||✓|
|UniDexGrasp [44]||✓|✓||✓|✓|||✓|||✓|
|GraspAda [35]||✓|✓||✓|✓||✓|||✓||


better capture the inherent uncertainty and variety in grasping tasks. This is particularly beneficial for objects with complex shapes, where multiple valid grasp configurations may exist. The ability of generative models to represent such multi-modal distributions makes them well-suited for robotic grasping, as they naturally accommodate the variability and ambiguity present in real-world objects. 

In this section, we will focus on generative models in robotic grasping policy synthesis. Specifically, we will discuss recent works that leverage different generative approaches, following the order of variational autoencoders (VAEs), diffusion models, and other generative models. 

**VAE-based methods.** Variational Autoencoders (VAEs) have emerged as a powerful framework for addressing the inherent complexities and multimodal nature of robotic grasp generation. By learning compact latent representations and sampling from learned distributions, VAEs facilitate the generation of diverse and physically plausible grasps, making them particularly well-suited for tasks that require adaptability to object variability and uncertainty. One notable application of VAEs in grasp synthesis is proposed by Mousavian et al. [37], which frames grasp generation as a sampling problem. The model employs a VAE to generate a diverse set of stable grasp poses directly from partial 3D point clouds. The latent space captures the multimodal distribution of grasps, allowing for efficient exploration of feasible solutions. Sundermeyer et al. [8] introduce a simplified yet effective representation for 6-DOF grasp generation in cluttered environments. Unlike traditional VAEs, the method projects grasp poses into a reduced 4-DoF space by rooting grasp configurations in the object’s observed point cloud. 

Beyond pure robotic grasping, Wu et al. [192] extends the 

utility of VAEs to human grasp generation, focusing on wholebody interactions. The model employs a Conditional VAE (CVAE) to generate static grasping poses and detailed contact maps jointly. This integration enables the synthesis of realistic and diverse whole-body grasping motions, capturing both dexterous finger movements and full-body dynamics. Jiang et al. [193] further explores the role of contact consistency in human grasp generation through a novel CVAE architecture. The model ensures mutual consistency between hand-object contact points by introducing tailored loss functions that penalize misalignment between predicted hand configurations and object contact maps. 

In the context of dexterous grasping, Zhao et al. [194] proposed CVAE framework predicts individual contact maps for each finger, leveraging these detailed representations to optimize grasp configurations. Wu et al. [195] integrates VAE-based sampling with bilevel optimization to address the dual challenges of diversity and physical feasibility. Initial grasp configurations are sampled from the VAE, capturing the multimodal grasp distribution. These samples then seed a bilevel optimization framework that enforces constraints such as collision avoidance, wrench closure, and friction stability. Overall, the integration of VAEs into grasp synthesis underscores their ability to effectively capture the multimodal and uncertain nature of robotic and human grasping tasks by embedding task-specific constraints and leveraging latentvariable modeling. 

**Diffusion-based methods.** Urain et al. [29] utilize an energy-based diffusion model, taking object shape and noisy pose as inputs to output energy as the cost. For grasp pose generation, it employs auto differentiation to compute the score and inverse Langevin dynamics to denoise the 6D pose 

16 

represented in _se_ (3) space. Singh et al. [30] extend SE(3)DiF to enable region-constrained grasping by adopting a partguided diffusion approach, allowing efficient and dense grasp generation on complex object shapes without conditionally labeled datasets. To enhance data efficiency and generalizability, Ryu et al. [186] use a bi-equivariant diffusion-based generative model on SE(3), enabling effective grasp pose generation from point cloud observations with minimal demonstrations. In addition, Vuong et al. [97] present a language-driven approach for grasp detection, targeting grasp rectangles in image space. It introduces the open-vocabulary grasping dataset and a diffusion model with a contrastive training objective to improve denoising and grasp pose detection from language instructions. Guo et al. [187] propose a two-stage diffusion framework that utilizes score-based diffusion networks to generate 4D grasp poses and their corresponding residuals from top-down RGB images, improving the precision of pick-and-place operations in robotic tasks. 

The aforementioned works primarily apply diffusion models to two-finger grasping tasks, while recent studies have also extensively explored grasping with multi-finger end-effectors, including dexterous hands. Specifically, Weng et al. [188] use a conditional diffusion model based on Denoising Diffusion Probabilistic Models (DDPM) [38] to generate dexterous grasps on partial point clouds. They further leverage Mayer et al. [200] for quality assessment, with refinement strategies to enhance success rates. Zhang et al. [189] also employs DDPM to generate dexterous grasp poses in cluttered scenes, while the condition is based on local features extracted from the scene, and the target is a 12D vector representing the wrist pose, combining translation and flattened rotation matrices. To generalize the method to different hardware devices, Freiberg et al. [64] propose a gripper-agnostic approach for grasping using an equivariant diffusion model, which encodes scenes with graspable objects and decodes grasp poses by integrating gripper geometry, demonstrating generalizability across multiple grippers from parallel-jaw to dexterous hands. 

Besides, recent works have also focused on human hand modeling, aiming to achieve more natural and lifelike grasping behaviors. Among them, Wang et al. [190] proposes a framework for generating human grasps from single-view scene point clouds. They use a Global Perception module to perceive the global shape of partially visible objects and a DiffuGrasp module based on a conditional diffusion model. This model targets hand parameters, progressively denoising them to generate stable grasps. To avoid penetration during training, the model employs a penetration loss that penalizes collisions between the hand and the object, ensuring natural and feasible grasp generation. Ye et al. [191] turn to develop a denoising diffusion-based generative model that captures the joint 3D distribution of hands and objects during interaction. Given a category-conditioned description, the model can synthesize both plausible object shapes and the relative configuration and articulation of the human hand. 

**Other generative models.** Xu et al. [44] utilize probabilistic models to generate diverse pre-grasp poses from point cloud data, effectively decoupling rotation from translation and articulation. The rotation space is represented by Implicit- 

PDF [201], a probabilistic model over SO(3), while the conditional distributions of translation and articulation are modeled using a generative flow model [202]. Rather than directly modeling the data distribution, Chen et al. [35] employ a conditional Generative Adversarial Network (cGAN) [203] to adapt RGB-D data from new domains, aligning it with the training domain while preserving grasp feature consistency. By ensuring that image features conform to domain-specific grasp feature distributions, a pretrained grasp synthesis model can then be used to generate grasp poses, including angle, width, and quality score. 

## _B. Trajectory Generation_ 

Trajectory generation is another foundational aspect of robotic manipulation, directly impacting a robot’s ability to perform complex tasks accurately, efficiently, and safely. 

Different methods utilize various input formats to produce consistent and stable outputs. Besides using a singlestep observation [55] of the environment—whose patterns resemble those of grasp pose generation—as input for nextaction prediction, historical information, including sequential observations [204, 205], is widely employed to enhance action consistency. Moreover, multi-step action prediction is a common technique for generating stable and coherent trajectories by enabling the model to anticipate a sequence of future actions [204, 205, 206]. 

From a methodological perspective, traditional trajectory planning methods encounter significant limitations, including high computational demands in high-dimensional configuration spaces, limited adaptability to dynamic environments, insufficient generalization to novel tasks, and challenges in managing long-horizon, multi-stage planning. Generative models present a promising paradigm shift by enabling efficient and direct trajectory generation, improved adaptability through data-driven learning, and enhanced generalization across diverse tasks and environments. These models also support the integration of multi-modal inputs, such as vision and language, while producing smooth and temporally consistent trajectories. Despite these advancements, generative models face critical challenges, including real-time inference constraints, reliance on diverse and high-quality training data, incorporation of physical and dynamic constraints, robustness to uncertainty in real-world applications, and the need for safety and interpretability. Addressing these limitations is pivotal for advancing generative approaches to meet the rigorous demands of robotic manipulation in real-world scenarios. 

In this section, we categorize these models into three primary approaches based on their generation strategies: Sampling-based Generation, Large Pre-trained Model-based Generation, and Hybrid-mode Generation. Sampling-based Generation relies on probabilistic models, such as diffusion models or Gaussian Processes, to sample high-quality trajectories from a learned or predefined distribution, effectively handling high-dimensional spaces and complex constraints like obstacle avoidance. Large Pre-trained Model-based Generation leverages powerful pre-trained models, such as visionlanguage transformers or autoregressive architectures, to predict trajectories conditioned on high-level inputs like language 

17 


Fig. 8. Timeline of representative manipulation trajectory generation works. 

commands or task descriptions, demonstrating strong generalization across diverse tasks and environments. Hybrid-mode Generation combines multiple generative techniques, integrating latent variable representations, pre-trained knowledge, and video dynamics to achieve efficiency and adaptability in complex, multi-stage tasks. Together, these approaches address critical challenges in trajectory generation, from multi-modal integration to long-horizon task planning, advancing the capabilities of robots in dynamic and unstructured environments. 

**Sampling-based Generation** refers to approaches that generate robotic manipulation trajectories or policies by sampling from a learned or predefined distribution of possible actions or states. These methods often rely on probabilistic models, such as Gaussian Processes, Monte Carlo methods, or diffusion models, to explore the space of feasible solutions and optimize for task-specific objectives. Sampling-based techniques are particularly useful for handling high-dimensional state and action spaces, as well as complex constraints like obstacle avoidance or dynamic environments. 

ALOHA [31] is designed for fine-grained bimanual manipulation tasks that require high precision and coordination, employing off-the-shelf hardware and custom 3D-printed components to enhance accessibility. Its key innovation, the Action Chunking with Transformers (ACT) algorithm, leverages a conditional variational autoencoder (CVAE) framework, allowing the robot to learn and execute precise tasks through imitation learning with just 10 minutes of demonstration data, achieving high success rates in tasks like battery insertion and cup opening. RoboAgent [84] introduces MT-ACT, which enhances a small dataset of 7,500 trajectories through semantic augmentations and a novel policy architecture, outperforming baselines in multi-task settings and confirming the effectiveness of its design choices. The Chunking Causal Transformer (CCT) [207] extends autoregressive models to robotics, efficiently predicting multiple future action tokens and improving accuracy. In contrast, the Autoregressive Policy (ARP) model based on CCT demonstrates superior performance across various tasks. 

The Diffusion Policy [6] proposes a novel approach to learning visuomotor policies for robotic manipulation using a conditional diffusion model, framing the policy as a denoising diffusion process that effectively models multimodal action distributions and high-dimensional action sequences, 

enhancing stability during training and adapting well to tasks requiring temporal consistency. Key innovations include receding horizon control for continuous re-planning, visual conditioning for real-time observations, and a time-series diffusion transformer for managing high-frequency action changes, with empirical results showing a 46.9% average performance improvement over state-of-the-art methods across 15 tasks. The 3D Diffuser Actor [7] combines 3D scene representations and action diffusion for robot manipulation policies, utilizing tokenized 3D scene representations, language instructions, and noised robot pose trajectories as input, setting new state-of-theart results on RLBench [208] and CALVIN [209] benchmarks, although it has limitations such as requiring camera calibration and slower performance compared to non-diffusion policies. The Equivariant Diffusion Policy [210] leverages equivariant neural models to improve sample efficiency and generalization, showing higher success rates in simulations and real-world experiments, although it has limitations in symmetry matching. EquiBot [211] combines SIM(3)-equivariant neural networks with diffusion models to enhance generalization and data efficiency, performing well in both simulation and real-world tasks. Crossway Diffusion [212] improves diffusion-based visuomotor policy by integrating an auxiliary self-supervised objective, demonstrating consistent improvements over baseline methods. The Consistency Policy [213] addresses slow inference in diffusion models, achieving significant speedup while retaining performance, although it has drawbacks in multimodality. Lastly, ALOHA Unleashed [206] utilizes largescale data collection with a Transformer-based architecture and diffusion policies to tackle challenging bimanual manipulation tasks, demonstrating superior performance and laying the groundwork for future multi-task learning models. 

Addressing the challenges of multi-stage bimanual manipulation tasks, which demand efficient arm coordination and face issues like multi-modal demonstrations and per-step/per-stage reliability, BiKC [214] is a hierarchical IL framework with a high-level keypose predictor and a low-level trajectory generator. The key pose predictor identifies key poses using heuristics and a merging method for bimanual coordination and is trained to predict target key poses. The trajectory generator is a consistency model to generate action sequences conditioned on observations and key poses. Experiments on simulated and real-world tasks (Transfer, Insertion, Screwdriver Packing, 

18 

etc.) show BiKC outperforms baselines (ACT, DP) in success rate and operational efficiency, while also demonstrating multimodal modeling and inference speed advantages, though it has limitations like sample smoothness and key pose representation that could be improved in future research. 

**Large Pre-trained Model-based Generation** refers to approaches that leverage large-scale pre-trained models, such as Transformers or GPT-style architectures, to generate robotic manipulation policies or trajectories. These models are typically trained on massive datasets, often incorporating multimodal inputs like vision, language, and sensor data, enabling them to learn rich representations and generalize across diverse tasks. By fine-tuning on specific robotic tasks, these models can generate high-quality, context-aware actions or plans, even in complex and dynamic environments. VisionLanguage-Action (VLA) models regard actions as a set of language tokens, LLMs to generate actions and language simultaneously. RT-2 [54] introduced the VLA concept and developed two VLA models based on PaLI-X [215] and PaLME [216]. VLA models demonstrate enhanced generalization performance, leveraging the extensive pre-training knowledge of LLMs. 

RT-1 [217] and RT-2 utilize Transformer-based architectures for robust performance in various tasks, while RVT [218] and RVT-2 [219] focus on multi-view transformations to improve task execution efficiency and generalization in real-world applications. As RT-2 is not open-source, OpenVLA [55] was proposed as a publicly accessible alternative. OpenVLA is built upon the Prismatic multi-modality LLM [220] and utilizes DINOv2 [221] and SigLIP [222] as visual encoders. It directly outputs action tokens using the LLM. Pre-trained on the large-scale Open-X-Embodiment dataset [223], OpenVLA exhibits superior performance compared to RT-2. DeLTaCo [224] conditions robotic policies on task embeddings from visual demonstrations and language instructions, improving generalization and reducing the need for demonstrations. PERACT [176] is a language-conditioned behavior-cloning agent for multi-task manipulation, outperforming traditional methods, while PolarNet [225] integrates point cloud representations with language instructions, showing robustness in real-world tasks. 

Im2Flow2Act[226] enables robots to learn manipulation skills from diverse data using object flow, while Dreamitate[227] leverages video diffusion models for robust visuomotor policy learning. Gen2Act [228] combines zeroshot human video generation with limited robot demos, achieving high success rates in generalization. ReKep [152] employs relational keypoint constraints for task representation, while Surfer [171] decouples manipulation into action and scene prediction. The introduction of GemBench [229] provides a benchmark for evaluating generalization in vision-language robotic manipulation. GR-1 [166] and GR-2 [167] explore large-scale video generative pre-training to enhance visual robot manipulation, achieving state-of-the-art results. 

**Hybrid-mode Generation** refers to approaches that combine multiple generative techniques, such as latent variable models, pre-trained models, and video generation models, to enhance the robustness and versatility of robotic manipulation 

algorithms. By integrating the strengths of different methods, these approaches can address complex tasks that require both high-level planning and low-level control, while also handling multimodal inputs like vision, language, and sensor data. GenDP [230] framework addresses generalization limitations of diffusion-based policies by using 3D semantic fields generated from multi-view RGBD observations, significantly improving success rates on unseen instances and enabling category-level generalization. The Hierarchical Diffusion Policy (HDP) [231] factors the policy into a hierarchical structure for efficient visual manipulation, outperforming state-of-theart methods and demonstrating the importance of kinematics awareness, while facing challenges in long-horizon tasks. A novel approach called Large Language model Reinforcement Learning Policy (LLaRP) [232] adapts large language models (LLMs) to function as generalizable policies for embodied visual tasks, leveraging pre-trained LLMs through reinforcement learning to process text instructions and visual observations, achieving a 42% success rate on 1,000 new tasks and introducing the Language Rearrangement benchmark for evaluating language-conditioned rearrangement tasks. The Robotics Diffusion Transformer (RDT) [233] uses diffusion models to handle multi-modal action distributions with a scalable Transformer architecture, proposing a Physically Interpretable Unified Action Space to train on heterogeneous multi-robot data. Pre-trained on a large multi-robot dataset and fine-tuned on a self-collected bimanual dataset, RDT shows strong zeroshot generalization, effective instruction following, and fewshot learning capabilities in experiments on a real robot. Finally, _π_ 0 [205] presents a novel architecture for generalist robot control, leveraging a pre-trained vision-language model (VLM) as its backbone and integrating semantic understanding from vast datasets with a flow matching approach to generate continuous actions, achieving high-frequency control (up to 50 Hz). Trained on a diverse dataset across different robots and tasks, _π_ 0 enables zero-shot task performance and fine-tuning for complex tasks like folding laundry and assembling objects, positioning it as a significant step towards versatile, generalpurpose robot learning models comparable to large language models but focused on physically situated, multi-stage robotic tasks. 

Each generative approach provides distinct benefits based on the operational requirements of different robotic tasks. Most of the research has conducted extensive validation on the RLBench benchmark, as illustrated in the table IV. Latent space models offer smooth trajectory generation, favoring tasks where continuity and consistency of movement are critical. Sampling-based models are optimal where trajectory accuracy and control are paramount, particularly in structured environments with predictable obstacles. Hybrid generation in achieving a balanced trade-off, enabling versatile solutions across various robotic manipulation tasks. Generative models for robotic trajectory generation represent a trade-off between precision, adaptability, and efficiency. 

## VI. FUTURE DIRECTIONS 

As generative models continue to revolutionize robotic manipulation, several promising avenues emerge to address 

19 

TABLE IV 

TOP 10 ROBOT MANIPULATION WORKS ON RLBENCH(18 TASKS, 100 DEMO/TASK). 

|Rank|Model|GenAI|Framework|Successful Rate|Training Time|Inference Speed|Input Image Size|Year|
|---|---|---|---|---|---|---|---|---|
|1|APR+ [207]|✓|Autoregressive|86.0|-|-|-|2024|
|2|3D-LOTUS [229]|✓|Other|81.5|0.28 hours|9.5 fps|256 _×_ 256|2024|
|3|RVT-2 [219]|✓<br>|Other|81.4|0.83 hours|20.6 fps|128 _×_ 128|2024|
|4|3D Diffuser Actor [7]|✓|Diffusion|81.3|-|-|256 _×_ 256|2024|
|5|Act3D [234]|✓<br>|Other|65.0|5 hours|-|256 _×_ 256|2023|
|6|RVT [218]|✓|Other|62.9|1 hours|11.6 fps|128 _×_ 128|2023|
|7|PerAct [176]<sup>_∗_</sup>|✓|Other|49.4|16 hours|4.9 fps|128 _×_ 128|2022|
|8|PolarNet [225]|✓|Other|46.4|-|-|128 _×_ 128|2023|
|9|PerAct [176]|✓|Other|42.7|16 hours|-|128 _×_ 128|2022|
|10|C2FARM-BC [235]<sup>_∗_</sup>|_×_|-|20.1|-|-|128 _×_ 128|2021|


* (Evaluated in RVT) 

existing challenges and unlock new capabilities. First, grounding domain-general models to domain-specific constraints through hybrid explicit-implicit representation learning and task-centric adaptation, as exemplified by Robotic-CLIP [236] and ManiGaussian [177], will enable robots to inherit visual generalization while encoding action-specific dynamics. Second, establishing unified benchmarks with standardized tasks, datasets, and evaluation metrics is essential to facilitate fair comparisons and reproducibility across studies. Finally, enhancing physical law awareness through physics-augmented training, physics-constrained generation, and reinforcement learning with physical feedback will bridge the sim-to-real gap and improve generalization to real-world environments. By addressing these challenges, the field can achieve robust, adaptive, and efficient robotic manipulation systems capable of operating in complex, unstructured settings. 

_a) Grounding domain-general models to domain-specific data:_ One fundamental challenge in applying generative AI to robotic manipulation lies in grounding domain-general models to domain-specific constraints. While vision-language models (VLMs) [95, 99] demonstrate remarkable zero-shot generalization for object recognition and segmentation tasks, their representations lack crucial physical interaction features, like spatial relationships, force dynamics. This limitation stems from their training objectives being centered on static internetsource data rather than dynamic physical interactions. 

Two critical issues compound this challenge. First, semantic-physical representation misalignment occurs when vision-language models (VLMs) optimized for web-scale visual understanding fail to encode robotic-relevant attributes. For instance, the image-text alignment in CLIP-based architectures [95] struggles with dynamic action semantics in manipulation videos, necessitating temporal-aware model structures and domain-specific fine-tuning on action sequences to bridge this gap. Second, data-induced physical bias arises from discrepancies between internet-scale pretraining data and realworld physical laws. This manifests in catastrophic operational failures when VLMs misinterpret material properties: robots may mistakenly classify soft rubber as rigid metal due to visual similarities in surface reflectivity, leading to inappropriate grasping strategies (e.g., excessive grip forces). Empirical evidence from VLBiasBench [237] reveals that VLMs achieve only 62% accuracy in distinguishing ”metal vs. plastic” mate- 

rials, with a 78% tendency to misclassify reflective surfaces as metals while ignoring mechanical characteristics like stiffness or compliance. Such biases originate from VLMs’ overreliance on static web imagery lacking physical interaction dynamics and multimodal annotations aligned with material science principles. 

To overcome these barriers, two emerging research directions show particular promise. On the one hand, hybrid explicit-implicit representation learning combines neural fields with foundation models to dynamically encode both geometric precision and task semantics. Recent extensions like ManiGaussian further demonstrate how Gaussian Splatting can regularize 3D Gaussian primitives for learning dynamics with visual foundation features [177]. On the other hand, taskcentric adaptation with interaction-aware datasets has gained traction. Robotic-CLIP [236] pioneers this paradigm by finetuning CLIP on 7.4 million action frames through contrastive learning, preserving original semantic alignment while significantly improving performance in language-driven robotic tasks. It introduces an Adapter Network that efficiently maps action-specific dynamics into the CLIP embedding space without altering the original model weights, enabling parameterefficient adaptation. Experimental results demonstrate that Robotic-CLIP outperforms other CLIP variants in tasks such as language-driven grasp detection and policy learning, achieving higher success rates and better alignment between textual instructions and visual frames. This approach enables robots to inherit visual generalization while encoding action-specific dynamics through parameter-efficient adaptation. 

_b) Fragmented benchmarks hinder progress and fair comparisons:_ The lack of unified benchmarks in embodied manipulation algorithms poses a significant challenge, hindering fair performance comparisons and reproducibility across studies. Current issues include diverse task definitions [6, 7, 31, 208], inconsistent datasets [208, 209, 223], varying simulation platforms [56, 57, 238], and non-standardized evaluation metrics. To address this, future efforts should focus on establishing standardized tasks, datasets, and simulation environments, while developing comprehensive evaluation frameworks that incorporate success rate, completion time, energy efficiency, and generalization ability. Additionally, promoting open-source code, reproducibility challenges, and cross-platform compatibility will enhance transparency and 

20 

collaboration within the research community. By unifying benchmarks, the field can accelerate progress and enable more reliable advancements in embodied manipulation algorithms. 

_c) Limited physical law awareness:_ Limited physical law awareness is a significant challenge in embodied manipulation, particularly in bridging the sim2real gap and leveraging visual generation models. Many current approaches rely on simplified or incomplete representations of physical laws, such as friction, dynamics, and material properties, which leads to poor generalization from simulation to real-world environments. Sim-to-real gap means the difference in performance and behavior when transitioning from simulation (sim) to the real world (real). This gap can lead to models that work well in simulation failing to perform as expected in reality. It is caused by physics simulation limitations, sensor discrepancies between simulation and real world, actuator variability, environmental complexity, and unmodeled dynamics in the real world [239, 240, 241]. Some methods have been proposed to address this issue. Domain randomization is a common approach to apply randomizing physical parameters, lighting conditions, sensor noise in the simulation [242, 243, 244]. Sim-to-real transfer learning and domain adaptation techniques are also useful to address the sim-to-real gap [14, 245, 246]. Privileged distillation via teacher-student learning shows that learning to behave like the teacher model which is exposed to more information is also effective to address the simto-real gap problem [247, 248, 249]. While visual generation models, particularly in the domain of robotic manipulation, have made significant strides in producing realistic images and videos, they often lack a deep understanding of the underlying physical laws that govern real-world interactions [250, 251, 252, 253]. These models primarily focus on generating visually plausible sequences based on learned patterns from large datasets, but they are typically not trained with explicit awareness of concepts like gravity, momentum, collision dynamics, or material properties. As a result, the generated scenes may not always align with the constraints of the physical world, leading to unrealistic or physically infeasible visual cues. This limited physical awareness can degrade the quality of planning in robotic manipulation tasks. Consequently, robots relying on these models may struggle with tasks involving delicate object manipulation, dynamic interactions, or long-horizon planning, where understanding the consequences of physical actions is critical for success. To address this limitation, several avenues for future research could be explored, including 1) physics-augmented training that incorporates physical simulations to fine-tune generative models, 2) physics-constrained generation that incorporates physical constraints into the generation process, and 3) reinforcement learning with physical feedback that utilizes explicit physical feedback to improve the physical law awareness. 

## VII. CONCLUSION 

Generative models have emerged as powerful tools to address the critical challenges in robotic manipulation, including insufficient data, long-horizon task planning, and generalization across diverse environments. By leveraging paradigms 

such as GANs, VAEs, probabilistic flow models, diffusion models, and autoregressive models, researchers have made significant strides in enabling robots to generate data, infer states, and synthesize policies for grasping and trajectory planning. This survey categorizes these applications into foundational, intermediate, and policy layers, providing a structured perspective on their roles in data generation, language and visual modeling, and robotic control. Despite the progress, challenges such as improving data efficiency, handling complex tasks, and achieving robust generalization remain open problems. Future research should focus on developing scalable models, integrating multi-modal data sources, and enhancing realtime decision-making capabilities to push the boundaries of robotic intelligence. These efforts will pave the way for more adaptable, versatile, and autonomous robotic systems capable of tackling increasingly complex and dynamic environments. 

## REFERENCES 

- [1] A. Billard and D. Kragic, “Trends and challenges in robot manipulation,” _Science_ , vol. 364, no. 6446, p. eaat8414, 2019. 

- [2] M. T. Mason, “Toward robotic manipulation,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 1, pp. 1– 28, 2018. 

- [3] R. Firoozi, J. Tucker, S. Tian, A. Majumdar, J. Sun, W. Liu, Y. Zhu, S. Song, A. Kapoor, K. Hausman _et al._ , “Foundation models in robotics: Applications, challenges, and the future,” _The International Journal of Robotics Research_ , p. 02783649241281508, 2023. 

- [4] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2017, pp. 23–30. 

- [5] Y. Wang, Z. Xian, F. Chen, T.-H. Wang, Y. Wang, K. Fragkiadaki, Z. Erickson, D. Held, and C. Gan, “Robogen: Towards unleashing infinite data for automated robot learning via generative simulation,” _arXiv preprint arXiv:2311.01455_ , 2023. 

- [6] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , p. 02783649241273668, 2023. 

- [7] T.-W. Ke, N. Gkanatsios, and K. Fragkiadaki, “3d diffuser actor: Policy diffusion with 3d scene representations,” _Arxiv_ , 2024. 

- [8] M. Sundermeyer, A. Mousavian, R. Triebel, and D. Fox, “Contact-graspnet: Efficient 6-dof grasp generation in cluttered scenes,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , 2021, pp. 13 438–13 444. 

- [9] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _International Conference on Learning Representations_ . 

- [10] D. Bauer, Z. Xu, and S. Song, “DoughNet: A visual predictive model for topological manipulation of deformable objects.” 

- [11] S. Levine, C. Finn, T. Darrell, and P. Abbeel, “End-to-end training of deep visuomotor policies,” _Journal of Machine Learning Research_ , vol. 17, no. 39, pp. 1–40, 2016. 

- [12] Y. Zhu, Z. Wang, J. Merel, A. Rusu, T. Erez, S. Cabi, S. Tunyasuvunakool, J. Kram´ar, R. Hadsell, N. de Freitas, and N. Heess, “Reinforcement and imitation learning for diverse visuomotor skills,” 2018. [Online]. Available: https://arxiv.org/abs/1802.09564 

- [13] L. Pinto and A. Gupta, “Supersizing self-supervision: Learning to grasp from 50k tries and 700 robot hours,” in _2016 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2016, pp. 3406–3413. 

21 

- [14] S. James, P. Wohlhart, M. Kalakrishnan, D. Kalashnikov, A. Irpan, J. Ibarz, S. Levine, R. Hadsell, and K. Bousmalis, “Sim-to-real via sim-to-sim: Data-efficient robotic grasping via randomized-to-canonical adaptation networks,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2019, pp. 12 627–12 637. 

- [15] A. A. Rusu, M. Vecerik, T. Roth¨orl, N. Heess, R. Pascanu, and R. Hadsell, “Sim-to-real robot learning from pixels with progressive nets,” in _Conference on Robot Learning_ . PMLR, 2017, pp. 262–270. 

- [16] Y. Zhu, R. Mottaghi, E. Kolve, J. J. Lim, A. Gupta, L. FeiFei, and A. Farhadi, “Target-driven visual navigation in indoor scenes using deep reinforcement learning,” in _2017 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2017, pp. 3357–3364. 

- [17] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer, “High-resolution image synthesis with latent diffusion models,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2022, pp. 10 684–10 695. 

- [18] T. B. Brown, “Language models are few-shot learners,” _arXiv preprint arXiv:2005.14165_ , 2020. 

- [19] S. Nikolaidis and J. A. Shah, “Efficient model learning from joint-action demonstrations for human-robot collaborative tasks,” in _Tenth Annual ACM/IEEE International Conference on Human-Robot Interaction_ . IEEE, 2015, pp. 189–196. 

- [20] L. P. Kaelbling and T. Lozano-P´erez, “Hierarchical task and motion planning in the now,” in _IEEE International Conference on Robotics and Automation_ . IEEE, 2011, pp. 1470–1477. 

- [21] L. G. Neuberg, “Causality: Models, reasoning, and inference, by judea pearl, cambridge university press, 2000,” _Econometric Theory_ , vol. 19, no. 4, p. 675–685, 2003. 

- [22] M. Toussaint, “Logic-geometric programming: An optimization-based approach to combined task and motion planning,” in _Twenty-Fourth International Joint Conference on Artificial Intelligence_ , 2015, pp. 1930–1936. 

- [23] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou _et al._ , “Chain-of-thought prompting elicits reasoning in large language models,” _Advances in neural information processing systems_ , vol. 35, pp. 24 824–24 837, 2022. 

- [24] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David, C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman, A. Herzog, D. Ho, J. Hsu, J. Ibarz, B. Ichter, A. Irpan, E. Jang, R. J. Ruano, K. Jeffrey, S. Jesmonth, N. J. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, K.-H. Lee, S. Levine, Y. Lu, L. Luu, C. Parada, P. Pastor, J. Quiambao, K. Rao, J. Rettinghouse, D. Reyes, P. Sermanet, N. Sievers, C. Tan, A. Toshev, V. Vanhoucke, F. Xia, T. Xiao, P. Xu, S. Xu, M. Yan, and A. Zeng, “Do as i can, not as i say: Grounding language in robotic affordances,” 2022. [Online]. Available: https://arxiv.org/abs/2204.01691 

- [25] W. Huang, P. Abbeel, D. Pathak, and I. Mordatch, “Language models as zero-shot planners: Extracting actionable knowledge for embodied agents,” in _International conference on machine learning_ . PMLR, 2022, pp. 9118–9147. 

- [26] C. Finn, I. Goodfellow, and S. Levine, “Unsupervised learning for physical interaction through video prediction,” _Advances in neural information processing systems_ , vol. 29, 2016. 

- [27] F. Ebert, C. Finn, S. Dasari, A. Xie, A. Lee, and S. Levine, “Visual foresight: Model-based deep reinforcement learning for vision-based robotic control,” _arXiv preprint arXiv:1812.00568_ , 2018. 

- [28] D. Ha and J. Schmidhuber, “World models,” _arXiv preprint arXiv:1803.10122_ , 2018. 

- [29] J. Urain, N. Funk, J. Peters, and G. Chalvatzaki, “Se (3)diffusionfields: Learning smooth cost functions for joint grasp and motion optimization through diffusion,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . 

IEEE, 2023, pp. 5923–5930. 

- [30] G. Singh, S. Kalwar, M. F. Karim, B. Sen, N. Govindan, S. Sridhar, and K. M. Krishna, “Constrained 6-dof grasp generation on complex shapes for improved dual-arm manipulation,” _arXiv preprint arXiv:2404.04643_ , 2024. 

- [31] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” in _Conference on Robot Learning (CoRL)_ , 2024. 

- [32] Y. Hu, Q. Xie, V. Jain, J. Francis, J. Patrikar, N. Keetha, S. Kim, Y. Xie, T. Zhang, H.-S. Fang, S. Zhao, 

   - S. Omidshafiei, D.-K. Kim, A. akbar Agha-mohammadi, K. Sycara, M. Johnson-Roberson, D. Batra, X. Wang, S. Scherer, C. Wang, Z. Kira, F. Xia, and Y. Bisk, “Toward general-purpose robots via foundation models: A survey and meta-analysis,” 2024. [Online]. Available: https://arxiv.org/abs/2312.08782 

- [33] R. McCarthy, D. C. H. Tan, D. Schmidt, F. Acero, N. Herr, Y. Du, T. G. Thuruthel, and Z. Li, “Towards generalist robot learning from internet video: A survey,” 2024. [Online]. Available: https://arxiv.org/abs/2404.19664 

- [34] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. WardeFarley, S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial nets,” _Advances in neural information processing systems_ , vol. 27, 2014. 

- [35] Y. Chen, J. Jiang, R. Lei, Y. Bekiroglu, F. Chen, and M. Li, “Graspada: Deep grasp adaptation through domain transfer,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 10 268–10 274. 

- [36] D. P. Kingma, “Auto-encoding variational bayes,” _arXiv preprint arXiv:1312.6114_ , 2013. 

- [37] A. Mousavian, C. Eppner, and D. Fox, “6-dof graspnet: Variational grasp generation for object manipulation,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 2901–2910. 

- [38] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in neural information processing systems_ , vol. 33, pp. 6840–6851, 2020. 

- [39] J. Song, C. Meng, and S. Ermon, “Denoising diffusion implicit models,” _arXiv preprint arXiv:2010.02502_ , 2020. 

- [40] D. Rezende and S. Mohamed, “Variational inference with normalizing flows,” in _International conference on machine learning_ . PMLR, 2015, pp. 1530–1538. 

- [41] D. Mantegazza, A. Giusti, L. M. Gambardella, and J. Guzzi, “An outlier exposure approach to improve visual anomaly detection performance for mobile robots,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 11 354–11 361, 2022. 

- [42] J. T. Brockmann, M. Rudolph, B. Rosenhahn, and B. Wandt, “The voraus-ad dataset for anomaly detection in robot applications,” _IEEE Transactions on Robotics_ , 2023. 

- [43] L. Wellhausen, R. Ranftl, and M. Hutter, “Safe robot navigation via multi-modal anomaly detection,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 1326–1333, 2020. 

- [44] Y. Xu, W. Wan, J. Zhang, H. Liu, Z. Shan, H. Shen, R. Wang, H. Geng, Y. Weng, J. Chen _et al._ , “Unidexgrasp: Universal robotic dexterous grasping via learning diverse proposal generation and goal-conditioned policy,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 4737–4746. 

- [45] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray _et al._ , “Training language models to follow instructions with human feedback,” _Advances in neural information processing systems_ , vol. 35, pp. 27 730–27 744, 2022. 

- [46] A. Radford, “Improving language understanding by generative pre-training,” 2018. 

- [47] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever _et al._ , “Language models are unsupervised multitask learners,” _OpenAI blog_ , vol. 1, no. 8, p. 9, 2019. 

- [48] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, 

22 

F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat _et al._ , “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

- [49] M. Chen, A. Radford, R. Child, J. Wu, H. Jun, D. Luan, and I. Sutskever, “Generative pretraining from pixels,” in _International conference on machine learning_ . PMLR, 2020, pp. 1691–1703. 

- [50] A. Ramesh, M. Pavlov, G. Goh, S. Gray, C. Voss, A. Radford, M. Chen, and I. Sutskever, “Zero-shot text-to-image generation,” in _International conference on machine learning_ . Pmlr, 2021, pp. 8821–8831. 

- [51] P. Sun, Y. Jiang, S. Chen, S. Zhang, B. Peng, P. Luo, and Z. Yuan, “Autoregressive model beats diffusion: Llama for scalable image generation,” _arXiv preprint arXiv:2406.06525_ , 2024. 

- [52] K. Tian, Y. Jiang, Z. Yuan, B. Peng, and L. Wang, “Visual autoregressive modeling: Scalable image generation via nextscale prediction,” _arXiv preprint arXiv:2404.02905_ , 2024. 

- [53] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei, “Scaling laws for neural language models,” _arXiv preprint arXiv:2001.08361_ , 2020. 

- [54] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” _arXiv preprint arXiv:2307.15818_ , 2023. 

- [55] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [56] E. Coumans and Y. Bai, “Pybullet, a python module for physics simulation for games, robotics and machine learning,” 2016. 

- [57] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2012. 

- [58] E. Rohmer, S. Singh, and M. C. Freese, “A versatile and scalable robot simulation framework,” in _Proceedings of the International Conference on Intelligent Robots and Systems (IROS)_ . 

- [59] H. Zhang, W. Du, J. Shan, Q. Zhou, Y. Du, J. B. Tenenbaum, T. Shu, and C. Gan, “Building cooperative embodied agents modularly with large language models,” _arXiv preprint arXiv:2307.02485_ , 2023. 

- [60] F. Ramos, R. C. Possas, and D. Fox, “Bayessim: adaptive domain randomization via probabilistic inference for robotics simulators,” _arXiv preprint arXiv:1906.01728_ , 2019. 

- [61] J. Lyu, C. Bai, J. Yang, Z. Lu, and X. Li, “Cross-domain policy adaptation by capturing representation mismatch,” _arXiv preprint arXiv:2405.15369_ , 2024. 

- [62] D. Li, Y. Jin, H. Yu, J. Shi, X. Hao, P. Hao, H. Liu, F. Sun, J. Zhang, B. Fang _et al._ , “What foundation models can bring for robot learning in manipulation: A survey,” _arXiv preprint arXiv:2404.18201_ , 2024. 

- [63] H. Wang, J. Chen, W. Huang, Q. Ben, T. Wang, B. Mi, T. Huang, S. Zhao, Y. Chen, S. Yang _et al._ , “Grutopia: Dream general robots in a city at scale,” _arXiv preprint arXiv:2407.10943_ , 2024. 

- [64] R. Freiberg, A. Qualmann, N. A. Vien, and G. Neumann, “Diffusion for multi-embodiment grasping,” _arXiv preprint arXiv:2410.18835_ , 2024. 

- [65] P. Katara, Z. Xian, and K. Fragkiadaki, “Gen2sim: Scaling up robot learning in simulation with generative models,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6672–6679. 

- [66] Y. Yang, F.-Y. Sun, L. Weihs, E. VanderBilt, A. Herrasti, W. Han, J. Wu, N. Haber, R. Krishna, L. Liu _et al._ , “Holodeck: Language guided generation of 3d embodied ai environments,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 16 227–16 237. 

- [67] T. Brooks, B. Peebles, C. Holmes, W. DePue, Y. Guo, L. Jing, D. Schnurr, J. Taylor, T. Luhman, E. Luhman _et al._ , “Video generation models as world simulators,” 2024. 

- [68] M. Yang, Y. Du, K. Ghasemipour, J. Tompson, D. Schuurmans, and P. Abbeel, “Learning interactive real-world simulators,” _arXiv preprint arXiv:2310.06114_ , 2023. 

- [69] A. Mandlekar, S. Nasiriany, B. Wen, I. Akinola, Y. Narang, L. Fan, Y. Zhu, and D. Fox, “Mimicgen: A data generation system for scalable robot learning using human demonstrations,” _arXiv preprint arXiv:2310.17596_ , 2023. 

- [70] J. Wang, Y. Qin, K. Kuang, Y. Korkmaz, A. Gurumoorthy, H. Su, and X. Wang, “Cyberdemo: Augmenting simulated human demonstration for real-world dexterous manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 17 952–17 963. 

- [71] X. Zhang, M. Chang, P. Kumar, and S. Gupta, “Diffusion meets dagger: Supercharging eye-in-hand imitation learning,” _arXiv preprint arXiv:2402.17768_ , 2024. 

- [72] Z. Jiang, Y. Xie, K. Lin, Z. Xu, W. Wan, A. Mandlekar, L. Fan, and Y. Zhu, “Dexmimicgen: Automated data generation for bimanual dexterous manipulation via imitation learning,” _arXiv preprint arXiv:2410.24185_ , 2024. 

- [73] R. Hoque, A. Mandlekar, C. R. Garrett, K. Goldberg, and D. Fox, “Interventional data generation for robust and dataefficient robot imitation learning,” in _First Workshop on Outof-Distribution Generalization in Robotics at CoRL 2023_ . 

- [74] H. Ha, P. Florence, and S. Song, “Scaling up and distilling down: Language-guided robot skill acquisition,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 3766–3777. 

- [75] Z. Chen, S. Kiami, A. Gupta, and V. Kumar, “Genaug: Retargeting behaviors to unseen situations via generative augmentation,” _arXiv preprint arXiv:2302.06671_ , 2023. 

- [76] T. Yu, T. Xiao, A. Stone, J. Tompson, A. Brohan, S. Wang, J. Singh, C. Tan, J. Peralta, B. Ichter _et al._ , “Scaling robot learning with semantically imagined experience,” _arXiv preprint arXiv:2302.11550_ , 2023. 

- [77] L. Y. Chen, C. Xu, K. Dharmarajan, M. Z. Irshad, R. Cheng, K. Keutzer, M. Tomizuka, Q. Vuong, and K. Goldberg, “Roviaug: Robot and viewpoint augmentation for cross-embodiment robot learning,” _arXiv preprint arXiv:2409.03403_ , 2024. 

- [78] Z. Q. Chen, K. Van Wyk, Y.-W. Chao, W. Yang, A. Mousavian, A. Gupta, and D. Fox, “Learning robust real-world dexterous grasping policies via implicit shape augmentation,” _arXiv preprint arXiv:2210.13638_ , 2022. 

- [79] I. Kapelyukh, V. Vosylius, and E. Johns, “Dall-e-bot: Introducing web-scale diffusion models to robotics,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, pp. 3956–3963, 2023. 

- [80] M. Lepert, R. Doshi, and J. Bohg, “Shadow: Leveraging segmentation masks for cross-embodiment policy transfer,” in _8th Annual Conference on Robot Learning_ . 

- [81] S. Bahl, A. Gupta, and D. Pathak, “Human-to-robot imitation in the wild,” _arXiv preprint arXiv:2207.09450_ , 2022. 

- [82] L. Y. Chen, K. Hari, K. Dharmarajan, C. Xu, Q. Vuong, and K. Goldberg, “Mirage: Cross-embodiment zeroshot policy transfer with cross-painting,” _arXiv preprint arXiv:2402.19249_ , 2024. 

- [83] Z. Mandi, H. Bharadhwaj, V. Moens, S. Song, A. Rajeswaran, and V. Kumar, “Cacti: A framework for scalable multitask multi-scene visual imitation learning,” _arXiv preprint arXiv:2212.05711_ , 2022. 

- [84] H. Bharadhwaj, J. Vakil, M. Sharma, A. Gupta, S. Tulsiani, and V. Kumar, “Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 4788–4795. 

- [85] N. Hirose, D. Shah, A. Sridhar, and S. Levine, “Exaug: Robot-conditioned navigation policies via geometric experience augmentation,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 4077– 

23 

4084. 

- [86] Y. Dai, J. Lee, N. Fazeli, and J. Chai, “Racer: Rich languageguided failure recovery policies for imitation learning,” _arXiv preprint arXiv:2409.14674_ , 2024. 

- [87] T. Xiao, H. Chan, P. Sermanet, A. Wahid, A. Brohan, K. Hausman, S. Levine, and J. Tompson, “Robotic skill acquisition via instruction augmentation with vision-language models,” _arXiv preprint arXiv:2211.11736_ , 2022. 

- [88] Y. J. Ma, W. Liang, G. Wang, D.-A. Huang, O. Bastani, D. Jayaraman, Y. Zhu, L. Fan, and A. Anandkumar, “Eureka: Human-level reward design via coding large language models.” in _CoRR_ , 2023. 

- [89] Y. Du, K. Konyushkova, M. Denil, A. Raju, J. Landon, F. Hill, N. de Freitas, and S. Cabi, “Vision-language models as success detectors.” in _CoRR_ , 2023. 

- [90] Y. Ge, A. Macaluso, L. E. Li, P. Luo, and X. Wang, “Policy adaptation from foundation model feedback,” in _2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, pp. 19 059–19 069. [Online]. Available: https://ieeexplore.ieee.org/document/10204201/ 

- [91] K. He, H. F. 0001, Y. Wu, S. Xie, and R. B. Girshick, “Momentum contrast for unsupervised visual representation learning.” in _CVPR_ , 2020. 

- [92] X. Wang, R. Zhang, C. Shen, T. Kong, and L. L. 0005, “Dense contrastive learning for self-supervised visual pre-training.” in _CVPR_ , 2021. 

- [93] O. Kraus, K. Kenyon-Dean, S. Saberian, M. Fallah, P. McLean, J. Leung, V. Sharma, A. Khan, J. Balakrishnan, S. Celik, M. Sypetkowski, C. V. Cheng, K. Morse, M. Makes, B. Mabey, and B. Earnshaw, “Masked autoencoders are scalable learners of cellular morphology.” in _CoRR_ , 2023. 

- [94] L. H. Li, P. Zhang, H. Zhang, J. Yang, C. Li, Y. Zhong, L. Wang, L. Yuan, L. Z. 0001, J.-N. Hwang, K.-W. Chang, and J. G. 0001, “Grounded language-image pre-training.” in _CVPR_ , 2022. 

- [95] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PMLR, 2021, pp. 8748–8763. 

- [96] A. Kamath, M. Singh, Y. LeCun, I. Misra, G. Synnaeve, and N. Carion, “Mdetr - modulated detection for end-to-end multimodal understanding.” in _CoRR_ , 2021. 

- [97] A. D. Vuong, M. N. Vu, B. Huang, N. Nguyen, H. Le, T. Vo, and A. Nguyen, “Language-driven grasp detection,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 17 902–17 912. 

- [98] P. Wang, A. Yang, R. Men, J. Lin, S. Bai, Z. Li, J. Ma, C. Zhou, J. Zhou, and H. Yang, “Ofa: Unifying architectures, tasks, and modalities through a simple sequence-to-sequence learning framework,” in _International conference on machine learning_ . PMLR, 2022, pp. 23 318–23 340. 

- [99] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W.-Y. Lo _et al._ , “Segment anything,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 4015– 4026. 

- [100] P. Sun, S. Chen, C. Zhu, F. Xiao, P. L. 0002, S. Xie, and Z. Yan, “Going denser with open-vocabulary part segmentation.” in _CoRR_ , 2023. 

- [101] B. Cao, X. Zhou, C. Guo, B. Zhang, Y. Liu, and Q. Tan, “Nbmod: Find it and grasp it in noisy background,” _arXiv preprint arXiv:2306.10265_ , 2023. 

- [102] N. Blank, M. Reuss, M. R¨uhle, O.<sup>¨</sup> E. Ya˘gmurlu, F. Wenzel, O. Mees, and R. Lioutikov, “Scaling robot policy learning via zero-shot labeling with foundation models,” _arXiv preprint arXiv:2410.17772_ , 2024. 

- [103] T. Sumers, K. Marino, A. Ahuja, R. Fergus, and I. Dasgupta, “Distilling internet-scale vision-language models 

into embodied agents,” in _Proceedings of the 40th International Conference on Machine Learning_ . PMLR, pp. 32 797–32 818, ISSN: 2640-3498. [Online]. Available: https://proceedings.mlr.press/v202/sumers23a.html 

- [104] M. Andrychowicz, F. Wolski, A. Ray, J. Schneider, R. Fong, P. Welinder, B. McGrew, J. Tobin, O. Pieter Abbeel, and W. Zaremba, “Hindsight experience replay,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [105] J.-B. Alayrac, J. Donahue, and Others, “Flamingo: a visual language model for few-shot learning.” in _CoRR_ , 2022. 

- [106] T. Xie, S. Zhao, C. H. Wu, Y. Liu, Q. Luo, V. Zhong, Y. Yang, and T. Y. 0009, “Text2reward: Automated dense reward function generation for reinforcement learning.” in _CoRR_ , 2023. 

- [107] Y. Fu, H. Zhang, D. W. 0044, W. Xu, and B. Boulet, “Furl: Visual-language models as fuzzy rewards for reinforcement learning.” in _CoRR_ , 2024. 

- [108] M. Alakuijala, G. Dulac-Arnold, J. Mairal, J. Ponce, and C. Schmid, “Learning reward functions for robotic manipulation by observing humans.” in _CoRR_ , 2022. 

- [109] Y. J. Ma, W. Liang, V. Som, V. Kumar, A. Z. 0001, O. Bastani, and D. Jayaraman, “Liv: Language-image representations and rewards for robotic control.” in _CoRR_ , 2023. 

- [110] Y. Hu, V. K. Keloth, K. Raja, Y. C. 0016, and H. X. 0001, “Towards precise pico extraction from abstracts of randomized controlled trials using a section-specific learning approach.” in _Bioinform._ , 2023. 

- [111] S. N. 0003, A. Rajeswaran, V. Kumar, C. Finn, and A. G. 0001, “R3m: A universal visual representation for robot manipulation.” in _CoRL_ , 2022. 

- [112] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation.” in _CoRR_ , 2021. 

- [113] W. Zhao, J. Chen, Z. Meng, D. Mao, R. Song, and W. Zhang, “Vlmpc: Vision-language model predictive control for robotic manipulation,” _arXiv preprint arXiv:2407.09829_ , 2024. 

- [114] C. Finn and S. Levine, “Deep visual foresight for planning robot motion,” in _2017 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2017, pp. 2786– 2793. 

- [115] W. Yu, N. Gileadi, C. Fu, S. Kirmani, K.-H. Lee, M. G. Arenas, H.-T. L. Chiang, T. Erez, L. Hasenclever, J. Humplik, B. Ichter, T. Xiao, P. Xu, A. Z. 0001, T. Zhang, N. Heess, D. Sadigh, J. Tan, Y. Tassa, and F. Xia, “Language to rewards for robotic skill synthesis.” in _CoRR_ , 2023. 

- [116] Y. Zeng, Y. M. 0001, and L. S. 0002, “Learning reward for robot skills using large language models via self-alignment.” in _CoRR_ , 2024. 

- [117] L. Ke, S. Choudhury, M. Barnes, W. Sun, G. Lee, and S. Srinivasa, “Imitation learning as f-divergence minimization,” in _Algorithmic Foundations of Robotics XIV: Proceedings of the Fourteenth Workshop on the Algorithmic Foundations of Robotics 14_ . Springer, 2021, pp. 313–329. 

- [118] V. Zhong, D. Misra, X. Yuan, and M.-A. Cˆot´e, “Policy improvement using language feedback models.” [Online]. Available: http://arxiv.org/abs/2402.07876 

- [119] M. Dalal, T. Chiruvolu, D. Chaplot, and R. Salakhutdinov, “Plan-seq-learn: Language model guided rl for solving long horizon robotics tasks,” _arXiv preprint arXiv:2405.01534_ , 2024. 

- [120] Z. Zhao, W. S. Lee, and D. Hsu, “Large language models as commonsense knowledge for large-scale task planning,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [121] Z. Liu, A. Bahety, and S. Song, “Reflect: Summarizing robot experiences for failure explanation and correction,” _arXiv preprint arXiv:2306.15724_ , 2023. 

- [122] L.-H. Lin, Y. Cui, Y. Hao, F. Xia, and D. Sadigh, “Gestureinformed robot assistance via foundation models,” in _7th Annual Conference on Robot Learning_ , 2023. 

24 

- [123] J. Wang, Z. Wu, Y. Li, H. Jiang, P. Shu, E. Shi, H. Hu, C. Ma, Y. Liu, X. Wang _et al._ , “Large language models for robotics: Opportunities, challenges, and perspectives,” _arXiv preprint arXiv:2401.04334_ , 2024. 

- [124] M. Li, S. Zhao, Q. Wang, K. Wang, Y. Zhou, S. Srivastava, C. Gokmen, T. Lee, L. E. Li, R. Zhang _et al._ , “Embodied agent interface: Benchmarking llms for embodied decision making,” _arXiv preprint arXiv:2410.07166_ , 2024. 

- [125] X. Puig, K. Ra, M. Boben, J. Li, T. Wang, S. Fidler, and A. Torralba, “Virtualhome: Simulating household activities via programs,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2018, pp. 8494–8502. 

- [126] S. Srivastava, C. Li, M. Lingelbach, R. Mart´ın-Mart´ın, F. Xia, K. E. Vainio, Z. Lian, C. Gokmen, S. Buch, K. Liu _et al._ , “Behavior: Benchmark for everyday household activities in virtual, interactive, and ecological environments,” in _Conference on robot learning_ . PMLR, 2022, pp. 477–490. 

- [127] Y. Mu, Q. Zhang, M. Hu, W. Wang, M. Ding, J. Jin, B. Wang, J. Dai, Y. Qiao, and P. Luo, “Embodiedgpt: Vision-language pre-training via embodied chain of thought,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [128] K. Grauman, A. Westbury, E. Byrne, Z. Chavis, A. Furnari, R. Girdhar, J. Hamburger, H. Jiang, M. Liu, X. Liu _et al._ , “Ego4d: Around the world in 3,000 hours of egocentric video,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022, pp. 18 995–19 012. 

- [129] X. Zhao, M. Li, C. Weber, M. B. Hafez, and S. Wermter, “Chat with the environment: Interactive multimodal perception using large language models,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 3590–3596. 

- [130] W. Choi, W. K. Kim, M. Yoo, and H. Woo, “Embodied cot distillation from llm to off-the-shelf agents,” in _Forty-first International Conference on Machine Learning_ . 

- [131] W. Huang, F. Xia, D. Shah, D. Driess, A. Zeng, Y. Lu, P. Florence, I. Mordatch, S. Levine, K. Hausman _et al._ , “Grounded decoding: Guiding text generation with grounded models for embodied agents,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [132] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar _et al._ , “Inner monologue: Embodied reasoning through planning with language models,” _arXiv preprint arXiv:2207.05608_ , 2022. 

- [133] D. Guo, Y. Xiang, S. Zhao, X. Zhu, M. Tomizuka, M. Ding, and W. Zhan, “Phygrasp: Generalizing robotic grasping with physics-informed large multimodal models,” _arXiv preprint arXiv:2402.16836_ , 2024. 

- [134] A. Z. Ren, B. Govil, T.-Y. Yang, K. R. Narasimhan, and A. Majumdar, “Leveraging language for accelerated learning of tool manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1531–1541. 

- [135] K. Rana, J. Haviland, S. Garg, J. Abou-Chakra, I. Reid, and N. Suenderhauf, “Sayplan: Grounding large language models using 3d scene graphs for scalable robot task planning,” in _7th Annual Conference on Robot Learning_ , 2023. 

- [136] Q. Lv, H. Li, X. Deng, R. Shao, M. Y. Wang, and L. Nie, “Robomp<sup>2</sup> : A robotic multimodal perception-planning framework with multimodal large language models,” _arXiv preprint arXiv:2404.04929_ , 2024. 

- [137] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. K¨uttler, M. Lewis, W.-t. Yih, T. Rockt¨aschel _et al._ , “Retrieval-augmented generation for knowledgeintensive nlp tasks,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 9459–9474, 2020. 

- [138] J. Liu, D. Shen, Y. Zhang, B. Dolan, L. Carin, and W. Chen, “What makes good in-context examples for gpt-3?” _arXiv preprint arXiv:2101.06804_ , 2021. 

- [139] K. Lin, C. Agia, T. Migimatsu, M. Pavone, and J. Bohg, “Text2motion: From natural language instructions to feasible 

   - plans,” _Autonomous Robots_ , vol. 47, no. 8, pp. 1345–1365, 2023. 

- [140] C. Agia, T. Migimatsu, J. Wu, and J. Bohg, “Stap: Sequencing task-agnostic policies,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 7951– 7958. 

- [141] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 9493–9500. 

- [142] Z. Zhao, W. Chai, X. Wang, L. Boyi, S. Hao, S. Cao, T. Ye, and G. Wang, “See and think: Embodied agent in virtual environment,” _arXiv preprint arXiv:2311.15209_ , 2023. 

- [143] J. Chen, Y. Mu, Q. Yu, T. Wei, S. Wu, Z. Yuan, Z. Liang, C. Yang, K. Zhang, W. Shao _et al._ , “Roboscript: Code generation for free-form manipulation tasks across real and simulation,” _arXiv preprint arXiv:2402.16117_ , 2024. 

- [144] Y. Jin, D. Li, Y. A, J. Shi, P. Hao, F. Sun, J. Zhang, and B. Fang, “Robotgpt: Robot manipulation learning from chatgpt,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 3, pp. 2543–2550, 2024. 

- [145] S. Huang, Z. Jiang, H. Dong, Y. Qiao, P. Gao, and H. Li, “Instruct2act: Mapping multi-modality instructions to robotic actions with large language model,” _arXiv preprint arXiv:2305.11176_ , 2023. 

- [146] P. Zhi, Z. Zhang, M. Han, Z. Zhang, Z. Li, Z. Jiao, B. Jia, and S. Huang, “Closed-loop open-vocabulary mobile manipulation with gpt-4v,” _arXiv preprint arXiv:2404.10220_ , 2024. 

- [147] I. Singh, V. Blukis, A. Mousavian, A. Goyal, D. Xu, J. Tremblay, D. Fox, J. Thomason, and A. Garg, “Progprompt: Program generation for situated robot task planning using large language models,” in _Autonomous Robots_ , vol. 47, 2023, pp. 999–1012. 

- [148] Y. Mu, J. Chen, Q. Zhang, S. Chen, Q. Yu, C. Ge, R. Chen, Z. Liang, M. Hu, C. Tao _et al._ , “Robocodex: Multimodal code generation for robotic behavior synthesis,” _arXiv preprint arXiv:2402.16117_ , 2024. 

- [149] L. Wang, Y. Ling, Z. Yuan, M. Shridhar, C. Bao, Y. Qin, B. Wang, H. Xu, and X. Wang, “Gensim: Generating robotic simulation tasks via large language models,” _International Conference on Learning Representations_ , 2024. 

- [150] J. Yang, Y. Dong, S. Liu, B. Li, Z. Wang, H. Tan, C. Jiang, J. Kang, Y. Zhang, K. Zhou _et al._ , “Octopus: Embodied visionlanguage programmer from environmental feedback,” _arXiv preprint arXiv:2402.14623_ , 2024. 

- [151] U. B. Karli, J.-T. Chen, V. N. Antony, and C.-M. Huang, “Alchemist: Llm-aided end-user development of robot applications,” pp. 361–370, 2024. 

- [152] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” _arXiv preprint arXiv:2409.01652_ , 2024. 

- [153] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” _arXiv preprint arXiv:2307.05973_ , 2023. 

- [154] E. Saccon, A. Tikna, D. De Martini, E. Lamon, L. Palopoli, and M. Roveri, “When prolog meets generative models: a new approach for managing knowledge and planning in robotic applications,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 17 065– 17 071. 

- [155] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. Fei-Fei, A. Anandkumar, Y. Zhu, and L. Fan, “Vima: General robot manipulation with multimodal prompts,” in _Fortieth International Conference on Machine Learning_ , 2023. 

- [156] Y. Ze, G. Yan, Y.-H. Wu, A. Macaluso, Y. Ge, J. Ye, N. Hansen, L. E. Li, and X. Wang, “Gnfactor: Multi-task real robot learn- 

25 

- ing with generalizable neural feature fields,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 284–301. 

- [157] T. Karras, S. Laine, M. Aittala, J. Hellsten, J. Lehtinen, and T. Aila, “Analyzing and improving the image quality of stylegan,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 8110–8119. 

- [158] J. Wang, H. Yuan, D. Chen, Y. Zhang, X. Wang, and S. Zhang, “Modelscope text-to-video technical report,” _arXiv preprint arXiv:2308.06571_ , 2023. 

- [159] J. Ho, T. Salimans, A. Gritsenko, W. Chan, M. Norouzi, and D. J. Fleet, “Video diffusion models,” _arXiv preprint arXiv:2204.03458_ , 2022. 

- [160] Y. Du, S. Yang, B. Dai, H. Dai, O. Nachum, J. Tenenbaum, D. Schuurmans, and P. Abbeel, “Learning universal policies via text-guided video generation,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [161] Y. Hong, B. Liu, M. Wu, Y. Zhai, K.-W. Chang, L. Li, K. Lin, C.-C. Lin, J. Wang, Z. Yang _et al._ , “Slowfast-vgen: Slowfast learning for action-driven long video generation,” _arXiv preprint arXiv:2410.23277_ , 2024. 

- [162] J. Cen, C. Wu, X. Liu, S. Yin, Y. Pei, J. Yang, Q. Chen, N. Duan, and J. Zhang, “Using left and right brains together: Towards vision and language planning,” _arXiv preprint arXiv:2402.10534_ , 2024. 

- [163] A. Blattmann, T. Dockhorn, S. Kulal, D. Mendelevitch, M. Kilian, D. Lorenz, Y. Levi, Z. English, V. Voleti, A. Letts _et al._ , “Stable video diffusion: Scaling latent video diffusion models to large datasets,” _arXiv preprint arXiv:2311.15127_ , 2023. 

- [164] A. Ajay, S. Han, Y. Du, S. Li, A. Gupta, T. Jaakkola, J. Tenenbaum, L. Kaelbling, A. Srivastava, and P. Agrawal, “Compositional foundation models for hierarchical planning,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [165] Q. Bu, J. Zeng, L. Chen, Y. Yang, G. Zhou, J. Yan, P. Luo, H. Cui, Y. Ma, and H. Li, “Closed-loop visuomotor control with generative expectation for robotic manipulation,” _arXiv preprint arXiv:2409.09016_ , 2024. 

- [166] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” in _International Conference on Learning Representations_ , 2024. 

- [167] C.-L. Cheang, G. Chen, Y. Jing, T. Kong, H. Li, Y. Li, Y. Liu, H. Wu, J. Xu, Y. Yang _et al._ , “Gr-2: A generative videolanguage-action model with web-scale knowledge for robot manipulation,” _arXiv preprint arXiv:2410.06158_ , 2024. 

- [168] K. Black, M. Nakamoto, P. Atreya, H. Walke, C. Finn, A. Kumar, and S. Levine, “Zero-shot robotic manipulation with pretrained image-editing diffusion models,” _arXiv preprint arXiv:2310.10639_ , 2023. 

- [169] T. Brooks, A. Holynski, and A. A. Efros, “Instructpix2pix: Learning to follow image editing instructions,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 18 392–18 402. 

- [170] F. Ni, J. Hao, S. Wu, L. Kou, J. Liu, Y. Zheng, B. Wang, and Y. Zhuang, “Generate subgoal images before act: Unlocking the chain-of-thought reasoning in diffusion model for robot manipulation with multimodal prompts,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 13 991–14 000. 

- [171] P. Ren, K. Zhang, H. Zheng, Z. Li, Y. Wen, F. Zhu, M. Ma, and X. Liang, “Surfer: Progressive reasoning with world models for robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2306.11335 

- [172] M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. Rabbat, Y. LeCun, and N. Ballas, “Self-supervised learning from images with a joint-embedding predictive architecture,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 15 619–15 629. 

- [173] C. Pan, B. Okorn, H. Zhang, B. Eisner, and D. Held, “Tax- 

pose: Task-specific cross-pose estimation for robot manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1783–1792. 

- [174] H. Huang, K. Schmeckpeper, D. Wang, O. Biza, Y. Qian, H. Liu, M. Jia, R. Platt, and R. Walters, “Imagination policy: Using generative point cloud models for learning manipulation policies,” _arXiv preprint arXiv:2406.11740_ , 2024. 

- [175] S. Dasgupta, A. Gupta, S. Tuli, and R. Paul, “Uncertaintyaware active learning of NeRF-based object models for robot manipulators using visual and re-orientation actions.” [Online]. Available: http://arxiv.org/abs/2404.01812 

- [176] M. Shridhar, L. Manuelli, and D. Fox, “Perceiver-actor: A multi-task transformer for robotic manipulation,” in _Proceedings of the 6th Conference on Robot Learning (CoRL)_ , 2022. 

- [177] G. Lu, S. Zhang, Z. Wang, C. Liu, J. Lu, and Y. Tang, “Manigaussian: Dynamic gaussian splatting for multi-task robotic manipulation,” in _European Conference on Computer Vision_ . Springer, 2025, pp. 349–366. 

- [178] Y. LeCun, “A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27,” _Open Review_ , vol. 62, no. 1, pp. 1–62, 2022. 

- [179] Y. J. Ma, S. Sodhani, D. Jayaraman, O. Bastani, V. Kumar, and A. Zhang, “VIP: Towards universal visual reward and representation via value-implicit pre-training.” [Online]. Available: http://arxiv.org/abs/2210.00030 

- [180] Y. Mu, S. Yao, M. Ding, P. Luo, and C. Gan, “Ec2: Emergent communication for embodied control,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 6704–6714. 

- [181] D. Hafner, T. P. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” in _International Conference on Learning Representations_ . 

- [182] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

- [183] Y. Seo, K. Lee, S. L. James, and P. Abbeel, “Reinforcement learning with action-free pre-training from videos,” in _International Conference on Machine Learning_ . PMLR, 2022, pp. 19 561–19 579. 

- [184] L. Zhang, M. Kan, S. Shan, and X. Chen, “PreLAR: World model pre-training with learnable action representation.” 

- [185] G. Wang, L. Pan, S. Peng, S. Liu, C. Xu, Y. Miao, W. Zhan, M. Tomizuka, M. Pollefeys, and H. Wang, “Nerf in robotics: A survey,” _arXiv preprint arXiv:2405.01333_ , 2024. 

- [186] H. Ryu, J. Kim, H. An, J. Chang, J. Seo, T. Kim, Y. Kim, C. Hwang, J. Choi, and R. Horowitz, “Diffusion-edfs: Biequivariant denoising generative modeling on se (3) for visual robotic manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 18 007–18 018. 

- [187] S.-W. Guo, T.-C. Hsiao, Y.-L. Liu, and C.-Y. Lee, “Precise pick-and-place using score-based diffusion networks,” _arXiv preprint arXiv:2409.09725_ , 2024. 

- [188] Z. Weng, H. Lu, D. Kragic, and J. Lundell, “Dexdiffuser: Generating dexterous grasps with diffusion models,” _arXiv preprint arXiv:2402.02989_ , 2024. 

- [189] J. Zhang, H. Liu, D. Li, X. Yu, H. Geng, Y. Ding, J. Chen, and H. Wang, “Dexgraspnet 2.0: Learning generative dexterous grasping in large-scale synthetic cluttered scenes,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [190] Y.-K. Wang, C. Xing, Y.-L. Wei, X.-M. Wu, and W.-S. Zheng, “Single-view scene point cloud human grasp generation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 831–841. 

- [191] Y. Ye, A. Gupta, K. Kitani, and S. Tulsiani, “G-hop: Generative hand-object prior for interaction reconstruction and grasp synthesis,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 1911– 1920. 

26 

- [192] Y. Wu, J. Wang, Y. Zhang, S. Zhang, O. Hilliges, F. Yu, and S. Tang, “Saga: Stochastic whole-body grasping with contact,” in _European Conference on Computer Vision_ . Springer, 2022, pp. 257–274. 

- [193] H. Jiang, S. Liu, J. Wang, and X. Wang, “Hand-object contact consistency reasoning for human grasps generation,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2021, pp. 11 107–11 116. 

- [194] F. Zhao, D. Tsetserukou, and Q. Liu, “Graingrasp: Dexterous grasp generation with fine-grained contact guidance,” _arXiv preprint arXiv:2405.09310_ , 2024. 

- [195] A. Wu, M. Guo, and C. K. Liu, “Learning diverse and physically feasible dexterous grasps with generative model and bilevel optimization,” _arXiv preprint arXiv:2207.00195_ , 2022. 

- [196] J. Bohg, A. Morales, T. Asfour, and D. Kragic, “Data-driven grasp synthesis—a survey,” _IEEE Transactions on robotics_ , vol. 30, no. 2, pp. 289–309, 2013. 

- [197] G. Du, K. Wang, S. Lian, and K. Zhao, “Vision-based robotic grasping from object localization, object pose estimation to grasp estimation for parallel grippers: a review,” _Artificial Intelligence Review_ , vol. 54, no. 3, pp. 1677–1734, 2021. 

- [198] R. Newbury, M. Gu, L. Chumbley, A. Mousavian, C. Eppner, J. Leitner, J. Bohg, A. Morales, T. Asfour, D. Kragic _et al._ , “Deep learning approaches to grasp synthesis: A review,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3994–4015, 2023. 

- [199] Y. Qin, R. Chen, H. Zhu, M. Song, J. Xu, and H. Su, “S4g: Amodal single-view single-shot se (3) grasp detection in cluttered scenes,” in _Conference on robot learning_ . PMLR, 2020, pp. 53–65. 

- [200] V. Mayer, Q. Feng, J. Deng, Y. Shi, Z. Chen, and A. Knoll, “Ffhnet: Generating multi-fingered robotic grasps for unknown objects in real-time,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 762–769. 

- [201] K. A. Murphy, C. Esteves, V. Jampani, S. Ramalingam, and A. Makadia, “Implicit-pdf: Non-parametric representation of probability distributions on the rotation manifold,” in _International Conference on Machine Learning_ . PMLR, 2021, pp. 7882–7893. 

- [202] D. P. Kingma and P. Dhariwal, “Glow: Generative flow with invertible 1x1 convolutions,” _Advances in neural information processing systems_ , vol. 31, 2018. 

- [203] M. Mirza, “Conditional generative adversarial nets,” _arXiv preprint arXiv:1411.1784_ , 2014. 

- [204] J. Yang, Y. Dong, S. Liu, B. Li, Z. Wang, H. Tan, C. Jiang, J. Kang, Y. Zhang, K. Zhou _et al._ , “Octopus: Embodied vision-language programmer from environmental feedback,” in _European Conference on Computer Vision_ . Springer, 2025, pp. 20–38. 

- [205] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [206] T. Z. Zhao, J. Tompson, D. Driess, P. Florence, K. Ghasemipour, C. Finn, and A. Wahid, “Aloha unleashed: A simple recipe for robot dexterity,” 2024. [Online]. Available: https://arxiv.org/abs/2410.13126 

- [207] X. Zhang, Y. Liu, H. Chang, L. Schramm, and A. Boularias, “Autoregressive action sequence learning for robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2410.03132 

- [208] S. James, Z. Ma, D. Rovick Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robotics and Automation Letters_ , 2020. 

- [209] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 7, no. 3, pp. 7327–7334, 2022. 

- [210] D. Wang, S. Hart, D. Surovik, T. Kelestemur, H. Huang, 

H. Zhao, M. Yeatman, J. Wang, R. Walters, and R. Platt, “Equivariant diffusion policy,” 2024. [Online]. Available: https://arxiv.org/abs/2407.01812 

- [211] J. Yang, Z. ang Cao, C. Deng, R. Antonova, S. Song, and J. Bohg, “Equibot: Sim(3)-equivariant diffusion policy for generalizable and data efficient learning,” 2024. [Online]. Available: https://arxiv.org/abs/2407.01479 

- [212] X. Li, V. Belagali, J. Shang, and M. S. Ryoo, “Crossway diffusion: Improving diffusion-based visuomotor policy via self-supervised learning,” 2024. [Online]. Available: https: //arxiv.org/abs/2307.01849 

- [213] A. Prasad, K. Lin, J. Wu, L. Zhou, and J. Bohg, “Consistency policy: Accelerated visuomotor policies via consistency distillation,” _arXiv preprint arXiv:2405.07503_ , 2024. 

- [214] D. Yu, H. Xu, Y. Chen, Y. Ren, and J. Pan, “Bikc: Keypose-conditioned consistency policy for bimanual robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/ 2406.10093 

- [215] X. Chen, J. Djolonga, P. Padlewski, B. Mustafa, S. Changpinyo, J. Wu, C. R. Ruiz, S. Goodman, X. Wang, Y. Tay _et al._ , “Pali-x: On scaling up a multilingual vision and language model,” _arXiv preprint arXiv:2305.18565_ , 2023. 

- [216] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu _et al._ , “Palme: An embodied multimodal language model,” _arXiv preprint arXiv:2303.03378_ , 2023. 

- [217] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, J. Ibarz, B. Ichter, A. Irpan, T. Jackson, S. Jesmonth, N. J. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, K.-H. Lee, S. Levine, Y. Lu, U. Malla, D. Manjunath, I. Mordatch, O. Nachum, C. Parada, J. Peralta, E. Perez, K. Pertsch, J. Quiambao, K. Rao, M. Ryoo, G. Salazar, P. Sanketi, K. Sayed, J. Singh, S. Sontakke, A. Stone, C. Tan, H. Tran, V. Vanhoucke, S. Vega, Q. Vuong, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich, “Rt-1: Robotics transformer for real-world control at scale,” 2023. [Online]. Available: https://arxiv.org/abs/2212.06817 

- [218] A. Goyal, J. Xu, Y. Guo, V. Blukis, Y.-W. Chao, and D. Fox, “Rvt: Robotic view transformer for 3d object manipulation,” 2023. [Online]. Available: https://arxiv.org/abs/2306.14896 

- [219] A. Goyal, V. Blukis, J. Xu, Y. Guo, Y.-W. Chao, and D. Fox, “Rvt-2: Learning precise manipulation from few demonstrations,” 2024. [Online]. Available: https://arxiv.org/ abs/2406.08545 

- [220] S. Karamcheti, S. Nair, A. Balakrishna, P. Liang, T. Kollar, and D. Sadigh, “Prismatic vlms: Investigating the design space of visually-conditioned language models,” _arXiv preprint arXiv:2402.07865_ , 2024. 

- [221] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. ElNouby _et al._ , “Dinov2: Learning robust visual features without supervision,” _arXiv preprint arXiv:2304.07193_ , 2023. 

- [222] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, “Sigmoid loss for language image pre-training,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 11 975–11 986. 

- [223] A. O’Neill, A. Rehman, A. Gupta, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models,” _arXiv preprint arXiv:2310.08864_ , 2023. 

- [224] A. Yu and R. J. Mooney, “Using both demonstrations and language instructions to efficiently learn robotic tasks,” 2023. [Online]. Available: https://arxiv.org/abs/2210.04476 

- [225] S. Chen, R. Garcia, C. Schmid, and I. Laptev, “Polarnet: 3d point clouds for language-guided robotic manipulation,” 2023. [Online]. Available: https://arxiv.org/abs/2309.15596 

- [226] M. Xu, Z. Xu, Y. Xu, C. Chi, G. Wetzstein, M. Veloso, and S. Song, “Flow as the cross-domain manipulation interface,” 

27 

- in _8th Annual Conference on Robot Learning_ , 2024. [Online]. Available: https://openreview.net/forum?id=cNI0ZkK1yC 

- [227] J. Liang, R. Liu, E. Ozguroglu, S. Sudhakar, A. Dave, P. Tokmakov, S. Song, and C. Vondrick, “Dreamitate: Real-world visuomotor policy learning via video generation,” 2024. 

- [228] H. Bharadhwaj, D. Dwibedi, A. Gupta, S. Tulsiani, C. Doersch, T. Xiao, D. Shah, F. Xia, D. Sadigh, and S. Kirmani, “Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation,” _arXiv preprint arXiv:2409.16283_ , 2024. 

- [229] R. Garcia, S. Chen, and C. Schmid, “Towards generalizable vision-language robotic manipulation: A benchmark and llm-guided 3d policy,” 2024. [Online]. Available: https: //arxiv.org/abs/2410.01345 

- [230] Y. Wang, G. Yin, B. Huang, T. Kelestemur, J. Wang, and Y. Li, “Gendp: 3d semantic fields for category-level generalizable diffusion policy,” 2024. [Online]. Available: https://arxiv.org/abs/2410.17488 

- [231] X. Ma, S. Patidar, I. Haughton, and S. James, “Hierarchical diffusion policy for kinematics-aware multi-task robotic manipulation,” _CVPR_ , 2024. 

- [232] A. Szot, M. Schwarzer, H. Agrawal, B. Mazoure, W. Talbott, K. Metcalf, N. Mackraz, D. Hjelm, and A. Toshev, “Large language models as generalizable policies for embodied tasks,” 2024. [Online]. Available: https://arxiv.org/abs/2310.17722 

- [233] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2410.07864 

- [234] T. Gervet, Z. Xian, N. Gkanatsios, and K. Fragkiadaki, “Act3d: 3d feature field transformers for multi-task robotic manipulation,” in _7th Annual Conference on Robot Learning_ , 2023. 

- [235] S. James, K. Wada, T. Laidlow, and A. J. Davison, “Coarseto-fine q-attention: Efficient learning for visual robotic manipulation via discretisation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022, pp. 13 739–13 748. 

- [236] N. Nguyen, M. N. Vu, T. D. Ta, B. Huang, T. Vo, N. Le, and A. Nguyen, “Robotic-clip: Fine-tuning clip on action data for robotic applications,” _arXiv preprint arXiv:2409.17727_ , 2024. 

   - [244] J. Huber, F. H´el´enon, H. Watrelot, F. B. Amar, and S. Doncieux, “Domain randomization for sim2real transfer of automatically generated grasping datasets,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 4112–4118. 

   - [245] D. Liu, Y. Chen, and Z. Wu, “Digital twin (dt)-cyclegan: Enabling zero-shot sim-to-real transfer of visual grasping models,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 5, pp. 2421–2428, 2023. 

   - [246] K. Chen, R. Cao, S. James, Y. Li, Y.-H. Liu, P. Abbeel, and Q. Dou, “Sim-to-real 6d object pose estimation via iterative self-training for robotic bin picking,” in _European Conference on Computer Vision_ . Springer, 2022, pp. 533–550. 

   - [247] H. He, P. Wu, C. Bai, H. Lai, L. Wang, L. Pan, X. Hu, and W. Zhang, “Bridging the sim-to-real gap from the information bottleneck perspective,” in _8th Annual Conference on Robot Learning_ , 2024. 

   - [248] D. Chen, B. Zhou, V. Koltun, and P. Kr¨ahenb¨uhl, “Learning by cheating,” in _Conference on Robot Learning_ . PMLR, 2020, pp. 66–75. 

   - [249] H. Nguyen, A. Baisero, D. Wang, C. Amato, and R. Platt, “Leveraging fully observable policies for learning under partial observability,” _arXiv preprint arXiv:2211.01991_ , 2022. 

   - [250] B. Kang, Y. Yue, R. Lu, Z. Lin, Y. Zhao, K. Wang, G. Huang, and J. Feng, “How far is video generation from world model: A physical law perspective,” _arXiv preprint arXiv:2411.02385_ , 2024. 

   - [251] H. Bansal, Z. Lin, T. Xie, Z. Zong, M. Yarom, Y. Bitton, C. Jiang, Y. Sun, K.-W. Chang, and A. Grover, “Videophy: Evaluating physical commonsense for video generation,” _arXiv preprint arXiv:2406.03520_ , 2024. 

   - [252] Z. Wang, S. Li, L. Hao, B. Song, and X. Hu, “What you see is what matters: A novel visual and physics-based metric for evaluating video generation quality,” _arXiv preprint arXiv:2411.13609_ , 2024. 

   - [253] H. Wu, F. Xu, C. Chen, X.-S. Hua, X. Luo, and H. Wang, “Pastnet: Introducing physical inductive biases for spatiotemporal video prediction,” in _Proceedings of the 32nd ACM International Conference on Multimedia_ , 2024, pp. 2917– 2926. 

- [237] J. Zhang, S. Wang, X. Cao, Z. Yuan, S. Shan, X. Chen, and W. Gao, “Vlbiasbench: A comprehensive benchmark for evaluating bias in large vision-language model,” _arXiv preprint arXiv:2406.14194_ , 2024. 

- [238] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [239] E. Salvato, G. Fenu, E. Medvet, and F. A. Pellegrino, “Crossing the reality gap: A survey on sim-to-real transferability of robot controllers in reinforcement learning,” _IEEE Access_ , vol. 9, pp. 153 171–153 187, 2021. 

- [240] A. Pitkevich and I. Makarov, “A survey on sim-to-real transfer methods for robotic manipulation,” in _2024 IEEE 22nd Jubilee International Symposium on Intelligent Systems and Informatics (SISY)_ . IEEE, 2024, pp. 000 259–000 266. 

- [241] W. Zhao, J. P. Queralta, and T. Westerlund, “Sim-to-real transfer in deep reinforcement learning for robotics: a survey,” in _2020 IEEE symposium series on computational intelligence (SSCI)_ . IEEE, 2020, pp. 737–744. 

- [242] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-to-real transfer of robotic control with dynamics randomization,” in _2018 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2018, pp. 3803–3810. 

- [243] R. Garcia, R. Strudel, S. Chen, E. Arlaud, I. Laptev, and C. Schmid, “Robust visual sim-to-real transfer for robotic manipulation,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . ieee, 2023, pp. 992– 999. 

