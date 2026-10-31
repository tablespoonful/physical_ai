---
title: "TD-MPC-Opt: Distilling Model-Based Multi-Task Reinforcement Learning Agents"
date: "2025-07-02"
authors: "Dmytro Kuzmenko; Nadiya Shvai"
url: https://arxiv.org/abs/2507.01823
pdf: https://arxiv.org/pdf/2507.01823
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.01823)** / [論文ページ](https://arxiv.org/abs/2507.01823)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **TD-MPC-Opt: Distilling Model-Based Multi-Task Reinforcement Learning Agents** 

Dmytro Kuzmenko 

Department of Multimedia Systems, NaUKMA, Kyiv, Ukraine 

```
kuzmenko@ukma.edu.ua
```

Nadiya Shvai 

Department of Mathematics, NaUKMA, Kyiv, Ukraine 

```
n.shvay@ukma.edu.ua
```

This is a preprint. The manuscript has been submitted for peer review. 

#### **Abstract** 

We present a novel approach to knowledge transfer in model-based reinforcement learning, addressing the critical challenge of deploying large world models in resource-constrained environments. Our method efficiently distills a high-capacity multi-task agent (317M parameters) into a compact model (1M parameters) on the MT30 benchmark, significantly improving performance across diverse tasks. Our distilled model achieves a state-of-theart normalized score of 28.45, surpassing the original 1M parameter model score of 18.93. This improvement demonstrates the ability of our distillation technique to capture and consolidate complex multi-task knowledge. We further optimize the distilled model through FP16 post-training quantization, reducing its size by _∼_ 50%. Our approach addresses practical deployment limitations and offers insights into knowledge representation in large world models, paving the way for more efficient and accessible multi-task reinforcement learning systems in robotics and other resource-constrained applications. Code available at https://github.com/dmytro-kuzmenko/td-mpc-opt. 

**Keywords:** Model-based RL; knowledge distillation; multi-task learning. 

## **1 Introduction** 

Reinforcement learning (RL) has demonstrated remarkable progress in solving complex tasks across various domains, from playing Atari games<sup>23</sup> to robotic control.<sup>1,16,20</sup> However, developing agents capable of performing multiple tasks efficiently remains a significant challenge, particularly in resource-constrained environments typical in robotics and real-world applications. 

Model-based RL approaches<sup>3,10</sup> have emerged as a promising solution, offering improved sample efficiency and generalization capabilities. Recent advancements, such as DreamerV3<sup>11</sup> and PWM<sup>7</sup> have showcased the potential of large world models in capturing complex dynamics across diverse tasks. However, these approaches often require substantial computational resources, limiting their practical application in resource-constrained settings. 

Another development in this field is TD-MPC (Temporal Difference Model Predictive Control),<sup>13</sup> which combines elements of RL with model predictive control. This hybrid approach leverages a learned world model for both value estimation and short-horizon planning. The Temporal Difference<sup>30</sup> component allows the agent to learn and improve its model from experience, while the MPC component enables efficient action selection through online planning.<sup>6</sup> 

TD-MPC2,<sup>12</sup> an extension of TD-MPC, has shown remarkable performance in multi-task continuous control benchmarks. It learns a shared world model across multiple tasks, enabling 

1 

efficient knowledge transfer and generalization. However, the high-capacity models used in TDMPC2 (up to 317M parameters) may pose additional challenges for deployment in resourceconstrained environments such as robotic systems with limited onboard computing power. 

This work extends our preliminary results described in<sup>18</sup> and attempts to address this limitation by exploring knowledge transfer techniques to distill the capabilities of large multi-task agents into more compact and deployment-friendly models. We focus on the MT30 benchmark,<sup>12</sup> which comprises tasks from the DM Control,<sup>32</sup> presenting a diverse set of continuous control challenges with varying observation and action spaces (Figure 1). 

The primary contributions of our work are: 

- Development of an efficient reward-based knowledge distillation technique for model-based RL for multi-task offline learning 

- Achievement of state-of-the-art performance (28.45 normalized score) with a compact FP16-quantized 1M parameter model, surpassing the original model by a large margin (+48.5%) and improving over a model, trained with the original recipe from scratch (28.12 vs. 27.36, +2.77%) 

- Demonstration of the effectiveness of longer distillation periods (1M steps) in capturing complex multi-task knowledge 

- Exploration of the impact of _d_ _~~c~~ oef_ on model performance as well the effect of reduced batch size on efficient knowledge distillation for multi-task scenarios 

- Successful application of FP16 and other quantization types (mixed precision, INT8) to further reduce model size with minimal performance loss 

Our approach combines traditional teacher-student distillation with quantization techniques, addressing the growing need for lightweight RL models in robotics and real-world applications. In the following sections, we detail our methodology, present experimental results on the MT30 benchmark, and discuss the implications of our findings for the future of multi-task model-based RL. 

## **2 Related Work** 

RL has progressed immensely in recent years, with advancements in both model-free and modelbased approaches. Model-free methods, including Deep Q-Networks (DQN),<sup>24</sup> Policy Gradient techniques,<sup>31</sup> and Soft Actor-Critic (SAC),<sup>9</sup> have demonstrated success in various domains, yet they often struggle with sample efficiency and generalization. 

Model-based RL has addressed some of these challenges, offering improved sample efficiency and planning capabilities. Notable approaches include PETS,<sup>3</sup> MBPO,<sup>15</sup> and DreamerV3,<sup>11</sup> which leverage learned world models for decision-making. TD-MPC<sup>13</sup> and its successor TDMPC2<sup>12</sup> have further advanced the field by combining model-based RL with model predictive control, showing particular promise in continuous control tasks. 

Knowledge distillation, originally introduced by Hinton et al.<sup>14</sup> for supervised learning, has gained traction in the RL community as a means to transfer knowledge from complex models to simpler ones. In the context of RL, distillation faces unique challenges due to the sequential nature of decision-making and the potential instability of learning processes. Rusu et al.<sup>27</sup> proposed Policy Distillation, adapting the distillation framework to transfer knowledge between deep Q-networks. Their method demonstrated the ability to compress multiple task-specific policies into a single multi-task policy. Building on this, Teh et al. introduced Distral,<sup>33</sup> a framework for distilling common knowledge across multiple tasks, improving both multi-task and transfer learning performance. 

2 


**Figure 1:** Task visualizations. Visualization of a random initial state for 12 of the 30 tasks that we consider (MT30). The tasks have different action spaces, degrees of freedom, and objectives. 

Parisotto et al.<sup>26</sup> introduced the Actor-Mimic method, which uses policy distillation to transfer knowledge from multiple task-specific teacher networks to a single multi-task network. Czarnecki et al.<sup>4</sup> proposed an improved policy distillation technique that addresses some limitations of previous methods, such as the need for careful hyperparameter tuning. In the realm of model-based RL, Kurutach et al. explored model ensemble distillation<sup>17</sup> to improve the stability and performance of model-based policy optimization. Their approach distilled an ensemble of dynamics models into a single model, reducing the negative impact of model bias. More recently, Stooke et al. introduced Decoupled Distillation,<sup>29</sup> a technique that separates the distillation of the policy and value function in actor-critic methods, allowing for more efficient knowledge transfer in off-policy RL algorithms. 

Multi-task RL has emerged as a crucial area of research, aiming to develop agents capable of performing diverse tasks across different embodiments. Benchmarks such as MT10, MT50,<sup>34</sup> and more recently, the MT30 and MT80<sup>12</sup> benchmarks incorporating tasks from DM Control<sup>32</sup> and Meta-World<sup>34</sup> have been instrumental in evaluating multi-task capabilities of RL agents. These benchmarks present unique challenges, including varying observation and action spaces, which test an agent’s ability to generalize across different embodiments and task structures. 

Approaches to multi-task RL include shared representation learning,<sup>2</sup> policy distillation,<sup>27</sup> and model-agnostic meta-learning techniques like MAML.<sup>5</sup> However, these methods often face challenges such as negative transfer and task interference,<sup>36</sup> highlighting the complexity of balancing task-specific and shared knowledge. Recent work in curriculum learning for RL<sup>25</sup> has shown promise in addressing these challenges by structuring the learning process to gradually increase task complexity. 

The increasing complexity of RL models, particularly in multi-task settings, has led to a growing interest in model compression techniques. Knowledge distillation, as discussed earlier, is one approach to this challenge. Additionally, quantization methods, including post-training quantization and quantization-aware training,<sup>8</sup> offer ways to reduce model size while maintain- 

3 

ing relative performance. Shin et al.<sup>28</sup> explored the use of quantization for deep Q-networks, demonstrating that careful quantization can significantly reduce model size with minimal performance loss. 

Recent trends in RL include the exploration of multi-modal approaches combining vision, language, and control,<sup>19</sup> and advancements in offline RL.<sup>21</sup> These developments are pushing the boundaries of what’s possible in RL, but also raise new challenges in terms of computational resources and deployment feasibility. Efficient RL methods, such as Conservative Q-Learning,<sup>35</sup> have shown promise in improving sample efficiency and performance in offline settings, potentially complementing distillation approaches in resource-constrained environments. 

Our work builds upon these foundations, particularly in the realm of model-based multi-task RL, by addressing the critical challenge of deploying large world models in resource-constrained environments. By combining knowledge distillation and quantization techniques, we aim to bridge the gap between the impressive capabilities of large models and the practical limitations of real-world deployment across various embodiments and tasks. 

## **3 Methods** 

Our approach focuses on optimizing large model-based RL agents for efficient multi-task learning through knowledge distillation and model compression. We aim to transfer knowledge from a high-capacity TD-MPC2 model (317M parameters) to a compact 1M parameter model, suitable for deployment in resource-constrained environments. Our method combines traditional teacherstudent distillation with quantization techniques, aiming to create new efficient pipelines for lightweight RL models for robotics and real-world applications. 


**Figure 2:** Our distillation approach consists of two main loss function components: the original loss from TD-MPC2 (in red), calculated as a linear combination of consistency, reward, and value losses ( _α_ denotes a scaling coefficient for each respective loss); and the distillation loss (in teal) that calculates MSE between student’s (green) and teacher’s (blue) rewards produced from inferring the same state-action pair. The total loss is a linear combination of both losses, with the distillation loss scaled by the _d_ _~~c~~ oef_ . In our scenario, the student is trainable while the teacher’s weights are frozen. 

We employ a teacher-student distillation framework, adapting it to the specific challenges of model-based RL (Figure 2). This framework consists of two key components: the largest 

4 

available 317M-parameter TD-MPC2 checkpoint from<sup>12</sup> as the teacher; the 1M parameter TDMPC2 backbone designed to balance performance with deployment efficiency as the student. 

### **3.1 Loss Function Adaptation** 

We build upon the original TD-MPC2 loss functions (consistency, reward, and value losses) by introducing an additional reward distillation loss. This new loss is computed as the mean squared error (MSE) between the rewards predicted by the teacher and student models: 

_L_ distill = MSE( _R_ teacher( _s, a_ ) _, R_ student( _s, a_ )) 

where _R_ teacher and _R_ student are the reward predictions of the teacher and student models, respectively. 

We introduce a distillation coefficient ( _d_ _~~c~~ oef_ ) to balance the original TD-MPC2 loss with our new distillation loss: 

_total_ _~~l~~ oss_ = _original_ _~~l~~ oss_ + _d_ coef _∗ distillation_ _~~l~~ oss_ 

The _d_ _~~c~~ oef_ acts as a hyperparameter controlling the influence of the teacher model’s knowledge on the student model’s learning process. We empirically find that values close to 0.5 yield the best results, with 0.4 being optimal for most training setups (Table 1). 

### **3.2 Evaluation Metric** 

We use the normalized score as our primary evaluation metric, consistent with.<sup>12</sup> Each task is scored on a scale of 1 to 1000, with the average sum divided by the number of tasks, resulting in a final range of 1-100. This allows for a fair comparison across tasks with different reward scales and difficulties. 

### **3.3 Training Process** 

For training, we take a 317M parameter TD-MPC2 model checkpoint trained on the full MT30 dataset. We then train the 1M parameter student model using our distillation approach. The student is trained on the same dataset but with the additional reward distillation loss. We explore different distillation periods, from 200,000 steps to 1,000,000 steps, to understand the impact of extended distillation on performance, various batch sizes (from 128 to 1024), and multiple values of _d_ _~~c~~ oef_ . We retain the original architecture and planning hyperparameters adhering to the original idea expressed in TD-MPC2 work.<sup>12</sup> 

To further optimize our model for real-world deployment, we apply post-training FP16,<sup>22</sup> mixed precision, and INT8 quantization techniques to our distilled model. 

### **3.4 Experimental Setup** 

For the MT30 benchmark, we utilized the full available dataset of 690,000 episodes (345,690,000 transitions). This multi-task benchmark is particularly challenging as it comprises tasks with varying observation and action spaces, requiring the agent to adapt to diverse environments. We conducted our experiments on a desktop PC with a single RTX 3060 GPU (12GB VRAM). 

## **4 Results** 

We first reproduced the checkpoint of the 1M parameter model from TD-MPC2 by training from scratch for 200,000 steps with batch size 1024. This served as our primary point of comparison for the distilled models. 

5 

**Table 1:** Impact of _d_ _~~c~~ oef_ on student’s performance, 200K steps with 317M teacher and batch size of 256. The first two entries indicate attempts to model a next-state latent distillation and the respective mechanism to bridge the latent dimension gap between teacher and student models. 

|_Distillation coefficient_|_Normalized score_|
|---|---|
|reward + next-state (linear projection)|7.69|
|reward + next-state (PCA)|8.78|
|0.05|13.61|
|baseline (no distill)|14.04|
|0.25|14.49|
|**0.4**|**17.85**|
|0.55|16.08|
|0.6|14.83|
|0.9|13.79|


### **4.1 Short-term Distillation** 

We evaluate the sample efficiency of our distillation approach under various training regimes, summarized in Table 2. For the short-term setting, models were trained for 200,000 steps using different batch sizes. This number of steps was assumed from prior work on MT30<sup>12</sup> and allowed us to reproduce the reported performance of a 1M-parameter model trained from scratch (18.7 normalized score vs 18.93 reported). 

Our distilled model achieves a comparable score of 18.11 with the same training duration, though slightly underperforming the from-scratch baseline. However, when using smaller batch sizes (e.g., 256), distillation with an efficient _d_ _~~c~~ oef_ value provides a clear gain over training from scratch (17.85 vs 14.04). This highlights that the knowledge-distilled agent can reach high performance more efficiently under low-resource constraints. Notably, even at 200K steps and reduced batch size, the distilled policy achieves 17.37 score and approaches full-performance levels with significantly less data exposure. 

**Table 2:** Results of different setups of 1M-parameter model distillation vs training from scratch on MT30 benchmark. 

|_Method_|_Batch size_|_Training steps, _|_#_<br>_Score_|
|---|---|---|---|
|distill|128|200K|17.37|
|from scratch|256|200K|14.04|
|distill|256|200K|17.85|
|from scratch|1024|200K|18.7|
|distill|1024|200K|18.11|
|from scratch|1024|337K|26.94|
|distill|1024|337K|25.44|
|from scratch|256|1M|27.36|
|distill|256|1M|28.12|
|best FP16 quantized|256|1M|**28.45**|


### **4.2 Extended Distillation** 

We further extended distillation to match the full training length of the original model. For batch size 1024, this translates to approximately 337K steps – sufficient to cover all 690,000 

6 

episodes (or 349 million transitions) in the MT30 benchmark with one batch per step. The aim was to examine whether prolonged distillation allows the student to internalize complex task knowledge more effectively. 

While extended distillation closes the performance gap, it still lags behind the from-scratch baseline (25.44 vs 26.94). This suggests that long training alone is not sufficient, and student capacity and alignment with teacher dynamics may impose inherent limits. However, when distillation is extended with a batch size of 256 and 1M steps, the model slightly surpasses the baseline (28.12 vs 27.36), indicating that in some regimes, distillation is not only sample-efficient but can outperform direct training. The highest score (28.45) is achieved using FP16 quantization, demonstrating that sample efficiency and model compression can be jointly optimized. 

As illustrated in figure 3, we compared the performance trajectories of our knowledgedistilled model against a model trained from scratch. Each model with 1M parameters was trained using identical batch sizes of 256. We evaluated their performance at five equidistant checkpoints throughout 1M training steps. The distilled model, utilizing a _d_ _~~c~~ oef_ of 0.45, demonstrates consistently superior performance, particularly in the early stages of training (200K and 600K steps checkpoints). 


**Figure 3:** Performance comparison between a knowledge-distilled model ( _d_ _~~c~~ oef_ of 0.45) and a model trained from scratch. Both models have 1M parameters and were trained with a batch size of 256. The normalized scores are shown for five checkpoints, taken at 200K-step intervals up to 1M steps. 

### **4.3 Batch Size Study** 

We investigated how batch size influences the quality of knowledge transfer, convergence speed, and computational efficiency in the distillation of large world models for multi-task RL. Experiments were conducted with batch sizes of 128, 256, and 1024, across both short-term (200K steps) and extended (337K or 1M steps) training regimes (Table 2). A 128-batch run showed no advantage over 256, highlighting diminishing returns at very small batch sizes. For batch size 1024, we additionally ran a 337K-step setup, so that we cover the entire MT30 dataset and examine the effects of full dataset exposure on distillation quality. 

While 1M-step distillation with batch size 256 results in each observation being seen multiple times, we report the outcome as a reference for high-resource settings, leaving deeper analysis for future work. All models were evaluated on the MT30 benchmark using normalized scores for fair cross-task comparison. This design isolates the role of batch size in distillation performance and informs best practices for scalable, resource-aware deployment of distilled policies. 

7 

### **4.4 Teacher Size Impact** 

We compared the performance of student models distilled from two different teacher sizes (Table 1): the second-largest 48M parameter model and the largest 317M parameter model, conceptualizing the relationship between teacher model capacity and distillation effectiveness (Table 3). 

**Table 3:** Different teacher sizes’ effect on distillation. 200K steps, Batch Size 256 

|_Teacher config_|_Normalized score_|
|---|---|
|48M|13.61|
|317M|**17.85**|


### **4.5 Quantization Results** 

To further optimize our model for deployment, we applied FP16 quantization to our bestperforming distilled model. We then evaluated the quantized model’s performance across all tasks to assess the impact of quantization on both model size and task performance. 

A mixed precision approach, combining FP16 for sensitive layers and INT8 for others, achieved a 64.6% size reduction (to 2.8 MiB) but led to a significant performance decrease, with the normalized score dropping to 13.53. This suggests that while mixed precision offers size reduction benefits, it comes at a considerable cost to model performance in the RL context. INT8 (8-bit integer) quantization, a more aggressive compression, reduced the model size by 75.3% (to 1.95 MiB). However, this came at a substantial cost to performance, with the normalized score plummeting to 5.09. The results are depicted in Table 4. 

**Table 4:** Quantization Results on Distilled Model. 1M steps, Batch Size 256, d ~~c~~ oef=0.4 

|Metric|Original|FP16|Mixed|INT8|
|---|---|---|---|---|
|Normalized Score|28.12|**28.45**|13.53|5.09|
|Model Size (MiB)|7.9|3.9|2.8|1.95|


It is important to note that the effects of quantization on RL models may differ from those observed in supervised learning tasks. RL models often have complex dynamics and may be more sensitive to precision loss in certain layers. Therefore, careful evaluation and potentially layer-wise quantization strategies might be necessary for optimal results. 

### **4.6 Task-specific distillation** 

Our experiments reveal that incorporating next-state latent distillation alongside reward distillation presents a significant challenge due to the dimensional mismatch between the teacher (1376-dim) and student (128-dim) models. We attempt to bridge this mismatch with dimensionality reduction techniques, such as linear projection and PCA, which introduce substantial information loss and lead to poor generalization. Linear projection yields a normalized score of 7.69, while PCA marginally improves the score to 8.78, though both underperform the 17.85 achieved with reward-only distillation (Table 1). The additional computational overhead of PCA and its limited gains further underscored its inefficiency. 

Our finalized approach, **reward-only distillation** , proved effective across most tasks, especially in locomotion ( _walker-walk_ ) and manipulation ( _reacher-easy_ ). However, it struggled 

8 

in tasks requiring long-term planning, sparse rewards, or precise control (e.g. _acrobot-swingup_ , _cartpole-swingup-sparse_ , _cheetah-jump_ ) – all that require next-state prediction. 

Latent next-state prediction, a probable necessity for future efficient and robust multi-task agents, did not yield strong results in our experiments due to dimensionality mismatches between teacher and student representations. Further work is needed to address this challenge effectively. 

## **5 Discussion** 

We demonstrate that knowledge distillation is a viable and sample-efficient strategy for scaling model-based RL to multi-task domains. The strong performance of our distilled agents, especially in extended training settings, confirms that large world models encode rich, transferable representations of task dynamics and reward structures. Crucially, our batch size study revealed that smaller batches (e.g., 256) consistently outperformed larger ones (1024), even in long-horizon distillation. This result challenges the assumption that larger batch sizes are inherently better for sample-efficient knowledge transfer in deep learning. 

Our best model, a quantized 1M-parameter student trained for 1M steps with batch size 256, achieves a new state-of-the-art score of 28.45 on the MT30 benchmark (+50.2% over the previously reported 18.93), using only reward-level distillation. This highlights the high sample efficiency of our method: it compresses a large teacher into a lightweight, high-performing policy that is viable for deployment. Smaller batch sizes appear to enable more frequent model updates and fine-grained learning, particularly beneficial for complex or sparse-reward tasks. With FP16 quantization, we further reduced model size by _∼_ 50%, underscoring the practicality of our approach for real-world applications. 

We also examined how batch size and distillation length interact with task complexity, offering insights into when and how smaller models can be trained effectively. These findings inform new training pipelines, where a high-capacity teacher is trained once and distilled into smaller agents tailored for constrained settings, enabling scalable and cost-effective RL deployment. 

Despite promising results, our work has limitations. First, we did not validate the distilled models on physical systems. Bridging the gap between simulation and real-world deployment is essential for broader adoption. Second, while our study focused on the MT30 benchmark, evaluating on larger task suites (e.g., MT80) and assessing generalization to unseen tasks remain important directions. Additionally, we have not yet determined the minimum compute budget necessary for effective distillation under various constraints. 

Our current approach also relies solely on reward-based distillation. Integrating next-state latent prediction or richer behavioral objectives could be the next step to capturing deeper aspects of the teacher policy, especially for sophisticated control tasks. 

In summary, our method enables high-performance, quantized multi-task RL agents with strong sample efficiency. By combining reward distillation with lightweight architectures, we show that compact, deployable agents can retain the competence of large models. This work contributes a scalable and practical pathway toward real-world RL systems suited for diverse and resource-constrained environments. 

## **References** 

- [1] OpenAI Andrychowicz, Bowen Baker, Maciek Chociej, Rafal Jozefowicz, Bob McGrew, Jakub Pachocki, Arthur Petron, Matthias Plappert, Glenn Powell, Alex Ray, et al. Learning dexterous in-hand manipulation. _The International Journal of Robotics Research_ , 39(1):3– 20, 2020. 

- [2] Rich Caruana. Multitask learning. _Machine learning_ , 28(1):41–75, 1997. 

9 

- [3] Kurtland Chua, Roberto Calandra, Rowan McAllister, and Sergey Levine. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. In _Advances in Neural Information Processing Systems_ , pages 4754–4765, 2018. 

- [4] Wojciech M Czarnecki, Razvan Pascanu, Simon Osindero, Siddhant Jayakumar, Grzegorz Swirszcz, and Max Jaderberg. Distilling policy distillation. In _The 22nd International Conference on Artificial Intelligence and Statistics_ , pages 1331–1340. PMLR, 2019. 

- [5] Chelsea Finn, Pieter Abbeel, and Sergey Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In _International Conference on Machine Learning_ , pages 1126–1135. PMLR, 2017. 

- [6] Carlos E Garcia, David M Prett, and Manfred Morari. Model predictive control: Theory and practice—a survey. _Automatica_ , 25(3):335–348, 1989. 

- [7] Ignat Georgiev, Varun Giridhar, Nicklas Hansen, and Animesh Garg. Pwm: Policy learning with large world models. _arXiv preprint arXiv:2407.02466_ , 2024. 

- [8] Amir Gholami, Sehoon Kim, Zhen Dong, Zhewei Yao, Michael W Mahoney, and Kurt Keutzer. A survey of quantization methods for efficient neural network inference. _arXiv preprint arXiv:2103.13630_ , 2021. 

- [9] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor. _International conference on machine learning_ , pages 1861–1870, 2018. 

- [10] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2020. 

- [11] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [12] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2024. 

- [13] Nicklas Hansen, Xiaolong Wang, and Hao Su. Temporal difference learning for model predictive control. In _International Conference on Machine Learning_ , pages 8385–8406. PMLR, 2022. 

- [14] Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network. In _NIPS Deep Learning and Representation Learning Workshop_ , 2015. 

- [15] Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. In _Advances in Neural Information Processing Systems_ , pages 12519–12530, 2019. 

- [16] Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, Mrinal Kalakrishnan, Vincent Vanhoucke, et al. Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation. _arXiv preprint arXiv:1806.10293_ , 2018. 

- [17] Thanard Kurutach, Ignasi Clavera, Yan Duan, Aviv Tamar, and Pieter Abbeel. Modelensemble trust-region policy optimization. In _International Conference on Learning Representations_ , 2018. 

- [18] Dmytro Kuzmenko and Nadiya Shvai. Knowledge transfer in model-based reinforcement learning agents for efficient multi-task learning, 2025. 

10 

- [19] Jaekyeom Lee, Yeong-Joon Jang, and Kee-Eung Cho. Multimodal reinforcement learning: A survey and taxonomy. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2022. 

- [20] Sergey Levine, Chelsea Finn, Trevor Darrell, and Pieter Abbeel. End-to-end training of deep visuomotor policies. _The Journal of Machine Learning Research_ , 17(1):1334–1373, 2016. 

- [21] Sergey Levine, Aviral Kumar, George Tucker, and Justin Fu. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint arXiv:2005.01643_ , 2020. 

- [22] Paulius Micikevicius, Sharan Narang, Jonah Alben, Gregory Diamos, Erich Elsen, David Garcia, Boris Ginsburg, Michael Houston, Oleksii Kuchaiev, Ganesh Venkatesh, et al. Mixed precision training. _arXiv preprint arXiv:1710.03740_ , 2018. 

- [23] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Alex Graves, Ioannis Antonoglou, Daan Wierstra, and Martin Riedmiller. Playing atari with deep reinforcement learning, 2013. 

- [24] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al. Human-level control through deep reinforcement learning. _Nature_ , 518(7540):529–533, 2015. 

- [25] Sanmit Narvekar, Bei Peng, Matteo Leonetti, Jivko Sinapov, Matthew E Taylor, and Peter Stone. Curriculum learning for reinforcement learning domains: A framework and survey. _Journal of Machine Learning Research_ , 21(181):1–50, 2020. 

- [26] Emilio Parisotto, Jimmy Lei Ba, and Ruslan Salakhutdinov. Actor-mimic: Deep multitask and transfer reinforcement learning. _arXiv preprint arXiv:1511.06342_ , 2015. 

- [27] Andrei A Rusu, Sergio Gomez Colmenarejo, Caglar Gulcehre, Guillaume Desjardins, James Kirkpatrick, Razvan Pascanu, Volodymyr Mnih, Koray Kavukcuoglu, and Raia Hadsell. Policy distillation. _arXiv preprint arXiv:1511.06295_ , 2015. 

- [28] Seunghyun Shin, Donnie H Ko, and Taehoon Kwon. Deep q-learning with quantized neural networks. In _Proceedings of the 18th International Conference on Autonomous Agents and MultiAgent Systems_ , pages 1785–1787, 2019. 

- [29] Adam Stooke, Kimin Lee, Pieter Abbeel, and Michael Laskin. Decoupling representation learning from reinforcement learning. _arXiv preprint arXiv:2009.08319_ , 2020. 

- [30] Richard S Sutton. Learning to predict by the methods of temporal differences. _Machine learning_ , 3(1):9–44, 1988. 

- [31] Richard S Sutton, David A McAllester, Satinder P Singh, and Yishay Mansour. Policy gradient methods for reinforcement learning with function approximation. _Advances in neural information processing systems_ , 12, 2000. 

- [32] Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, et al. Dm ~~c~~ ontrol: Software and tasks for continuous control. _arXiv preprint arXiv:2006.12983_ , 2020. 

- [33] Yee Whye Teh, Victor Bapst, Wojciech M Czarnecki, John Quan, James Kirkpatrick, Raia Hadsell, Nicolas Heess, and Razvan Pascanu. Distral: Robust multitask reinforcement learning. In _Advances in Neural Information Processing Systems_ , pages 4496–4506, 2017. 

11 

- [34] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning_ , pages 1094–1100. PMLR, 2020. 

- [35] Tianhe Yu, Garrett Thomas, Lantao Yu, Stefano Ermon, James Zou, Sergey Levine, Chelsea Finn, and Tengyu Ma. Conservative q-learning for offline reinforcement learning. _Advances in Neural Information Processing Systems_ , 34:1179–1191, 2021. 

- [36] Yu Zhang and Qiang Yang. A survey on multi-task learning. _IEEE Transactions on Knowledge and Data Engineering_ , 34(8):3555–3569, 2021. 

12 

