---
title: "Enhancing Linguistic Generalization of VLA: Fine-Tuning OpenVLA via Synthetic Instruction Augmentation"
date: "2026-03-17"
authors: "Dongik Shin"
url: https://arxiv.org/abs/2603.16044
pdf: https://arxiv.org/pdf/2603.16044
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.16044)** / [論文ページ](https://arxiv.org/abs/2603.16044)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Enhancing Linguistic Generalization of VLA: Fine-Tuning OpenVLA via Synthetic Instruction Augmentation** 

## **Dongik Shin** 

i.dongik@utexas.edu 

## **Abstract** 

Generalization remains a core challenge in embodied AI, as robots must adapt to diverse environments. While OpenVLA represents the State-of-the-Art (SOTA) in Vision-LanguageAction models by leveraging large-scale pretraining, its zero-shot performance can be limited when encountering completely new environments. This paper proposes a parameterefficient fine-tuning strategy to enhance the linguistic generalization of OpenVLA by synthesizing a general instruction set for the Bridge Dataset V2. The paper leverages a Large Language Model (LLM) to generate a rich variety of semantically equivalent but structurally diverse commands for existing trajectories. In this experiment, Low-Rank Adaptation (LoRA) is implemented to fine-tune OpenVLA on augmented pairs, allowing the model to bridge the gap between complex natural language intent and robotic actions. Results demonstrate that the LoRA-enhanced model’s robustness, suggesting that enriching the linguistic space of specialized datasets is crucial for embodied agents. 

## **1 Introduction** 

The embodied AI has recently undergone a paradigm shift with the emergence of VisionLanguage-Action (VLA) models. Among these, **OpenVLA** (Kim et al., 2025) stands as a state-ofthe-art (SOTA) open-source model that bridges the gap between high-level linguistic reasoning and low-level robotic control. OpenVLA is built upon a vision encoder (SigLIP) (Zhai et al., 2023a) and a large language model backbone (Llama) (Touvron et al., 2023), and the model is pre-trained on the massive Open X-Embodiment dataset (Collaboration et al., 2023), which consists over 900,000 robot trajectories. This extensive training allows the model to exhibit remarkable zero-shot generalization capabilities across various robotic platforms and tasks (Kim et al., 2025). 

While OpenVLA shows outstanding physical task performance, its linguistic generalization is often limited by the quality of language annotations in its training data. Large-scale datasets such as the Bridge Dataset V2 (Walke et al., 2023b), which is a component of the Open X-Embodiment dataset (Collaboration et al., 2023), often lack natural language instructions. This lack of linguistic diversity hinders the model’s robustness to interpret varied human’s instructions. 

To handle this limitation, this paper proposes a method to enhance the linguistic generalization of OpenVLA (Kim et al., 2025) through a synthesized "General Instruction Set". This study leverages the reasoning capabilities of Large Language Models (LLMs) to generate a rich spectrum of semantically equivalent but general instructions for the trajectories in the Bridge Dataset V2 (Walke et al., 2023b). To adapt the massive OpenVLA model efficiently, Low-Rank Adaptation (LoRA) (Hu et al., 2021) is employed. This parameter-efficient fine-tuning strategy allows the model to align its general linguistic expressions without the prohibitive computational cost of full-parameter updates. 

The primary contribution of this study is the demonstration that enriching the linguistic space of a specialized robotic dataset can significantly improve the generalization of a VLA agent. By fine-tuning with a structured and diverse instruction set, the proposed model achieves higher scores. The remainder of this paper is organized as follows: Section 2 reviews related work in VLA and parameter-efficient tuning; Section 3 details the generation of the General Instruction Set and the LoRA (Hu et al., 2021) fine-tuning framework; Section 4 presents the experimental results on linguistic generalization; and Section 5 evaluates the results; and Section 6 concludes with future research directions. 

## **2 Related Works** 

### **2.1 Visually-Conditioned Language Models** 

Visually-conditioned language models (VLMs) are trained on large-scale data to generate human language from images and language prompts. The model commonly have been adopted for various applications from visual question answering (Goyal et al., 2017; Hudson and Manning, 2019; Singh et al., 2019). One of the key advances make recent VLMs feasible are model architectures that bridge representations from pretrained vision encoders with pretrained language models (Radford et al., 2021; Zhai et al., 2023b; Team et al., 2024a). Recent open-source VLMs have emcompassed on a simpler “patch as token” method, where patch representations from pretrained visual transformers are treated as tokens, then the patches are fed into the input space of a language model (Chen et al., 2023; Liu et al., 2023, 2024; Karamcheti et al., 2024). This simple approach makes it easy to utilize existing methods for training language models at scale for VLM training. For instance, VLMs from Karamcheti et al. (Karamcheti et al., 2024) are trained from multi-resolution visual features, fusing low-level spatial information from DINOv2 (Oquab et al., 2023) with higher-level semantics from SigLIP (Zhai et al., 2023b) to aid in visual generalization. 

### **2.2 Vision-Language-Action Models** 

Numerous works have explored the usage of VLMs for robotics, for object detection (Yitzhak Gadre et al., 2022), providing a feedback signal (Ma et al., 2023; Sontakke et al., 2023), and visual state representations (Nair et al., 2022). Likewise, a number of recent works have explored approaches which directly fine-tuned large pretrained VLMs for predicting robot actions (Kim et al., 2024; Collaboration et al., 2023; Huang et al., 2023). Such models are referred to as vision-language-action models (VLAs), since they fuse robot control actions directly into VLM backbones (Kim et al., 2024). Kim et al. state three key benefits of VLA: (1) it performs alignment of pretrained vision and language components on a large, Internet-scale visionlanguage dataset, (2) the use of a generic architecture, not custom-made for robot control, allows us to leverage the scalable infrastructure underlying modern VLM training (Dao, 2023; Zhao et al., 2023) and scale to training billion-parameter policies with minimal code modifications, and (3) it 

provides a direct pathway for robotics to benefit from the rapid improvements in VLMs. Recent researches on VLAs focus on training and evaluating in single robot or simulated setups (Huang et al., 2023; Zhen et al., 2024; Dorka et al., 2024) and thus lack generability. RT-2-X (Collaboration et al., 2023) trains a 55B-parameter VLA policy on the Open X-Embodiment dataset and demonstrates state-of-the-art generalist manipulation policy performance but it has high computation cost. OpenVLA (Kim et al., 2024) improves with a richer robot pretraining datasets, fit to new target setups, and shows effectiveness of parameter-efficient finetuning (PEFT) and quantization approaches for VLAs. In this study, OpenVLA is used as a base model for computational efficiency. 

### **2.3 Generalization in VLAs** 

A recent trend in robotics works towards training multi-task generalist robot policies on large diverse robot datasets, spanning many different robot embodiments (Kim et al., 2024; Brohan et al., 2022; Walke et al., 2023a; Kalashnikov et al., 2018, 2021; Ebert et al., 2021; Ehsani et al., 2024; Bharadhwaj et al., 2024; Pinto and Gupta, 2016; Mandlekar et al., 2018; Gupta et al., 2018; Dasari et al., 2019; Cabi et al., 2019; Jang et al., 2022; Fang et al., 2024; Devin et al., 2017; Hu et al., 2022; Yang et al., 2023; Reed et al., 2022; Radosavovic et al., 2023; Shah et al., 2022, 2023). A key difference between these approaches and OpenVLA is the model architecture. Prior works like Octo (Brohan et al., 2023; Team et al., 2024b; Walke et al., 2023b) typically consist of pretrained components such as language embeddings or visual encoders with additional model components initialized from scratch. OpenVLA adopts a more end-to-end approach, directly fine-tuning VLMs to generate robot actions by treating them as tokens in the language model vocabulary (Kim et al., 2024). In this experiment, experimental evaluation shows that with general instruction sets and generalization ability over prior generalist policies. 

## **3 Proposed Method** 

### **3.1 Problem Formulation** 

In this study, the pre-trained OpenVLA (Kim et al., 2025) model is fine-tuned on a subset of Bridge Dataset V2 (Walke et al., 2023b) _D_ = _{_ ( _oi, li, ai_ ) _}_<sup>_N_</sup> _i_ =1<sup>, where</sup><sup>_oi_represents the visual ob-</sup> servation, _li_ denotes the generated instruction, and 

_ai_ is the corresponding ground-truth action. To achieve efficient adaptation while fine-tuing, LowRank Adaptation (LoRA) (Hu et al., 2021) method is used. During fine-tuning, the original weights _W_ 0 are kept frozen, and the low-rank decomposition matrices are updated. The optimization objective is defined as follow: 


where _L_ vla is a default objective in the official OpenVLA implementation for discrete action token prediction (Kim et al., 2025). The objective target the query (Q), value (V), key (K), and output (O) projection matrices in the self-attention layers with a rank _r_ = 32 and _α_ = 64 to capture generated instructions set with motion patterns. 

Table 1: Top 5 representative instructions generated by the LLM for general task adaptation in Bridge Dataset V2 (Walke et al., 2023b). 

- **No. Instruction** 1 In order to pick up the object, the robot should 2 To move the object to a new location, the robot must 3 In order to grasp and relocate the item, the robot should 4 To manipulate the objects in front of it, the robot must 5 In order to complete the task of moving the utensils, the robot should 

### **3.2 Generate Instruction Set** 

To enhance the model’s adaptability and robustness across diverse environments, a method for generating a general instrcution set using a Large Language Model (LLM) is introduced in this project. Unlike conventional datasets that rely on fixed, human-annotated labels, this approach leverages the semantic reasoning capabilities of LLMs to synthesize a diverse instruction with linguistic variations for each trajectory. For each trajectory in the subset of BridgeData V2, the task’s metadata, including the objects involved and the final goal state are fed into the LLM. The LLM is then prompted to generate a comprehensive set of instructions that describe the same robotic action through various syntactic structures such as "In order to pick up the object, the robot should move it to the target" or "To relocate the item, the robot must execute a grasp and place action". 

By fine-tuning OpenVLA on this augmented instruction set, more robust mapping between visual observations and linguistic commands is used. This process allows the model to adapt to a general instruction space, preventing it from overfitting to 

specific, rigid phrasing. Consequently, the proposed method significantly improves the generalization capabilities of the agent, enabling it to execute commands successfully even when faced with paraphrased instructions that were not present in the original training distribution. 

Table 1 illustrates the top 5 representative instructions generated by the LLM for a single manipulation task. These generated instructions introduce significant linguistic variety, ranging from high-level (abstract) goal descriptions (e.g., "manipulate the objects") to specific item-based commands (e.g., "moving the utensils"). By providing a sequence of three key frames, initial, intermediate, and final images, the LLM by using prompt template described in Table 3 was able to infer the robot’s intent and generate semantically rich instructions. From the generated candidates, few instructions (5 instruction in this experiments) were manually curated the most contextually appropriate instruction sets to ensure high-quality supervision. Then, These selected instructions were then randomly paired with their corresponding trajectories during the training phase. This random mapping within the augmented set encourages the model to decouple specific linguistic patterns from rigid task labels, thereby fostering a more flexible and generalized policy. 

## **4 Experiments** 

### **4.1 Datasets** 

In this experiments, the scripted raw dataset from BridgeData V2 (Walke et al., 2023b), a large-scale dataset specifically designed for robotic manipulation in diverse environments was used. Unlike purely teleoperated demonstrations, this subset consists of 9,731 trajectories collected via a randomized scripted policy, and does not have human instructions. Although this autonomous collection process frequently results in suboptimal executions, data is particularly valuable for training robust behaviors. Therefore, subset of the data that aligns with objectives is manually curated. Moreover, due to the massive scale of the original scripted dataset in the BridgeData V2 (35GB), 100 trajectories were selected for simplicity. Each trajectories consists of an average of 25 sequential image-action pairs. 

### **4.2 Implementation Details** 

The model is trained based on the AdamW optimizer (Loshchilov and Hutter, 2019), and the learn- 

Table 2: Comparison of Action Prediction Accuracy between Zero-shot OpenVLA and Our Proposed Method (Fine-tuned with General Instruction Set). 

|Methods|Top-1 Acc (%)|5-Bin Acc (%)|
|---|---|---|
|OpenVLA (Kim et al.,2025)|**6.62**|40.76|
|Proposed Method|5.09|**42.47**|


ing rate is 5e-05. We fine-tuned a model on dataset described above. All experiments are performed on a single Nvidia A100 GPUs with 40GB of VRAM. 

## **5 Evaluation** 

### **5.1 Policy Evaluation** 

OpenVLA replaces the 256 tokens least frequently used tokens in the Llama tokenizer’s vocabulary with action tokens (Kim et al., 2025). To evaluate the precision of the model’s predicted actions, the predicted action tokens against the ground-truth values from the BridgeData V2 test set are used to compare. 

For the quantitative assessment, each continuous action dimension—comprising the end-effector’s Cartesian displacement (∆ _x,_ ∆ _y,_ ∆ _z_ ), orientation (∆ _roll,_ ∆ _pitch,_ ∆ _yaw_ ), and gripper state—is normalized to the range [ _−_ 1 _,_ 1] and assigned to one of the 256 discrete bins. Two metrics for performance analysis is used: Top-1 accuracy and 5-Bin tolerance accuracy. The accuracy for a given action dimension is formulated as follows: 

## **6 Conclusion and Limitation** 

This study demonstrates that fine-tuning the OpenVLA model with an LLM-generated general instruction set significantly enhances the robustness of robotic manipulation policies. While our results show a slight decrease in Top-1 accuracy, the substantial improvement in 5-bin tolerance accuracy indicates that the model has developed a more flexible and generalized understanding of the task, prioritizing functional success over rigid tokenwise memorization. However, several limitations remain. First, the increase in linguistic variety appears to introduce a slight trade-off in absolute precision. Second, the current evaluation is conducted on a curated subset of 100 trajectories, leaving the scalability to more complex, multi-stage tasks as a subject for future investigation. Future work will focus on refining the instruction generation process to mitigate precision loss and validating the proposed method in real-world environments with a broader range of robotic platforms. 


where _ai_ is the ground-truth token, ˆ _ai_ is the predicted token, and _k_ represents the tolerance threshold ( _k_ = 0 for Top-1 accuracy and _k_ = 5 for 5-bin tolerance accuracy).Experimental results indicate that while the Top-1 accuracy slightly decreased compared to the original OpenVLA, the 5-bin tolerance accuracy showed a significant improvement. This shift suggests that although the model’s exact token matching is more distributed, the predictions remain consistently within a narrow, physically plausible range of the target action. This result demonstrates that fine-tuning with a general instruction set enhances the robustness of the policy, allowing the model to prioritize functional success and motion consistency over rigid token-wise memorization. 

Table 3: Prompt template for instruction generation. 

[System Message] 

You are a linguistic expert specializing in robotic task annotation. Your goal is to provide diverse, natural language instructions based on visual observations of robot manipulation. 

[User Message] {Image 1: First frame of the trajectory} {Image 2: Intermediate frame of the trajectory} {Image 3: Last frame of the trajectory} 

### Task: 

1. Scene Analysis: Briefly identify the primary object and the robot’s objective from the provided image. 2. Instruction Generation: Synthesize exactly 5 distinct natural language instructions for the observed task. 

### Requirements: 

- Ensure linguistic variety: Use different sentence structures (Imperative, Goal-oriented, and Conditional). - Vary the level of abstraction: Include instructions ranging from low-level motor descriptions to high-level intent. 

- Vocabulary diversity: Use synonyms for objects (e.g., "item," "target," "utensil") and actions (e.g., "grasp," "pick up," "relocate"). - Format: Return only the 5 instructions, each on a new line starting with "No. [Number]". 

### [Output Example] 

No. 1 In order to pick up the object, the robot should... No. 2 To move the item to a new location, the robot must... 

## **References** 

- Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. 2024. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 4788–4795. IEEE. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, and 32 others. 2023. Rt-1: Robotics transformer for realworld control at scale. _Preprint_ , arXiv:2212.06817. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, and 1 others. 2022. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ . 

- Serkan Cabi, Sergio Gómez Colmenarejo, Alexander Novikov, Ksenia Konyushkova, Scott Reed, Rae Jeong, Konrad Zolna, Yusuf Aytar, David Budden, Mel Vecerik, and 1 others. 2019. Scaling data-driven robotics with reward sketching and batch reinforcement learning. _arXiv preprint arXiv:1909.12200_ . 

- Xi Chen, Xiao Wang, Lucas Beyer, Alexander Kolesnikov, Jialin Wu, Paul Voigtlaender, Basil Mustafa, Sebastian Goodman, Ibrahim Alabdulmohsin, Piotr Padlewski, and 1 others. 2023. Pali-3 vision language models: Smaller, faster, stronger. _arXiv preprint arXiv:2310.09199_ . 

- Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, and 275 others. 2023. Open X- Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/2310.08864. 

- Tri Dao. 2023. Flashattention-2: Faster attention with better parallelism and work partitioning. _arXiv preprint arXiv:2307.08691_ . 

- Sudeep Dasari, Frederik Ebert, Stephen Tian, Suraj Nair, Bernadette Bucher, Karl Schmeckpeper, Siddharth Singh, Sergey Levine, and Chelsea Finn. 2019. Robonet: Large-scale multi-robot learning. _arXiv preprint arXiv:1910.11215_ . 

- Coline Devin, Abhishek Gupta, Trevor Darrell, Pieter Abbeel, and Sergey Levine. 2017. Learning modular neural network policies for multi-task and multirobot transfer. In _2017 IEEE international conference on robotics and automation (ICRA)_ , pages 2169– 2176. IEEE. 

- Nicolai Dorka, Chenguang Huang, Tim Welschehold, and Wolfram Burgard. 2024. What matters in employing vision language models for tokenizing actions in robot control? In _First Workshop on VisionLanguage Models for Navigation and Manipulation at ICRA 2024_ . 

- Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. 2021. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. _arXiv preprint arXiv:2109.13396_ . 

- Kiana Ehsani, Tanmay Gupta, Rose Hendrix, Jordi Salvador, Luca Weihs, Kuo-Hao Zeng, Kunal Pratap Singh, Yejin Kim, Winson Han, Alvaro Herrasti, and 1 others. 2024. Spoc: Imitating shortest paths in simulation enables effective navigation and manipulation in the real world. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16238–16250. 

- Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. 2024. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 653–660. IEEE. 

- Yash Goyal, Tejas Khot, Douglas Summers-Stay, Dhruv Batra, and Devi Parikh. 2017. Making the v in vqa matter: Elevating the role of image understanding in visual question answering. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 6904–6913. 

- Abhinav Gupta, Adithyavairavan Murali, Dhiraj Prakashchand Gandhi, and Lerrel Pinto. 2018. Robot learning in homes: Improving generalization and reducing dataset bias. _Advances in neural information processing systems_ , 31. 

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. Lora: Low-rank adaptation of large language models. _Preprint_ , arXiv:2106.09685. 

- Edward S. Hu, Kun Huang, Oleh Rybkin, and Dinesh Jayaraman. 2022. Know thyself: Transferable visual control policies through robot-awareness. _Preprint_ , arXiv:2107.09047. 

- Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. 2023. An embodied generalist agent in 3d world. _arXiv preprint arXiv:2311.12871_ . 

- Drew A Hudson and Christopher D Manning. 2019. Gqa: A new dataset for real-world visual reasoning and compositional question answering. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 6700–6709. 

- Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. 2022. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991–1002. PMLR. 

- Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, Mrinal Kalakrishnan, Vincent Vanhoucke, and 1 others. 2018. Scalable deep reinforcement learning for vision-based robotic manipulation. In _Conference on robot learning_ , pages 651–673. PMLR. 

- Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. 2021. Mtopt: Continuous multi-task robotic reinforcement learning at scale. _arXiv preprint arXiv:2104.08212_ . 

- Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. 2024. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, and 1 others. 2024. Openvla: An opensource vision-language-action model. _arXiv preprint arXiv:2406.09246_ . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. 2025. Openvla: An open-source vision-language-action model. In _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 2679–2713. PMLR. 

- Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. 2024. Improved baselines with visual instruction tuning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 26296–26306. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. 2023. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892– 34916. 

- Ilya Loshchilov and Frank Hutter. 2019. Decoupled weight decay regularization. In _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net. 

- Yecheng Jason Ma, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. 2023. Liv: Language-image representations and rewards for robotic control. In _International Conference on Machine Learning_ , pages 23301–23320. PMLR. 

- Ajay Mandlekar, Yuke Zhu, Animesh Garg, Jonathan Booher, Max Spero, Albert Tung, Julian Gao, John Emmons, Anchit Gupta, Emre Orbay, and 1 others. 2018. Roboturk: A crowdsourcing platform for robotic skill learning through imitation. In _Conference on Robot Learning_ , pages 879–893. PMLR. 

- Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. 2022. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ . 

- Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, and 1 others. 2023. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ . 

- Lerrel Pinto and Abhinav Gupta. 2016. Supersizing self-supervision: Learning to grasp from 50k tries and 700 robot hours. In _2016 IEEE international conference on robotics and automation (ICRA)_ , pages 3406–3413. IEEE. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, and 1 others. 2021. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR. 

- Ilija Radosavovic, Baifeng Shi, Letian Fu, Ken Goldberg, Trevor Darrell, and Jitendra Malik. 2023. Robot learning with sensorimotor pre-training. In _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 683–693. PMLR. 

- Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, Tom Eccles, Jake Bruce, Ali Razavi, Ashley Edwards, Nicolas Heess, Yutian Chen, Raia Hadsell, Oriol Vinyals, Mahyar Bordbar, and Nando de Freitas. 2022. A generalist agent. _Preprint_ , arXiv:2205.06175. 

- Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, and Sergey Levine. 2022. GNM: A general navigation model to drive any robot. In _Deep Reinforcement Learning Workshop NeurIPS 2022_ . 

- Dhruv Shah, Ajay Sridhar, Nitish Dashora, Kyle Stachowicz, Kevin Black, Noriaki Hirose, and Sergey Levine. 2023. Vint: A foundation model for visual navigation. _Preprint_ , arXiv:2306.14846. 

- Amanpreet Singh, Vivek Natarajan, Meet Shah, Yu Jiang, Xinlei Chen, Dhruv Batra, Devi Parikh, and Marcus Rohrbach. 2019. Towards vqa models that can read. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 8317–8326. 

- Sumedh Sontakke, Jesse Zhang, Séb Arnold, Karl Pertsch, Erdem Bıyık, Dorsa Sadigh, Chelsea Finn, and Laurent Itti. 2023. Roboclip: One demonstration is enough to learn robot policies. _Advances in Neural Information Processing Systems_ , 36:55681–55693. 

- Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivière, Mihir Sanjay Kale, Juliette Love, and 1 others. 2024a. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ . 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. 2024b. Octo: An open-source generalist robot policy. _Preprint_ , arXiv:2405.12213. 

   - Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. 2023b. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975–11986. 

   - Yanli Zhao, Andrew Gu, Rohan Varma, Liang Luo, Chien-Chin Huang, Min Xu, Less Wright, Hamid Shojanazeri, Myle Ott, Sam Shleifer, and 1 others. 2023. Pytorch fsdp: experiences on scaling fully sharded data parallel. _arXiv preprint arXiv:2304.11277_ . 

   - Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 2024. 3d-vla: A 3d vision-languageaction generative world model. _arXiv preprint arXiv:2403.09631_ . 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, and 49 others. 2023. Llama 2: Open foundation and fine-tuned chat models. _Preprint_ , arXiv:2307.09288. 

- Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, and Moo Jin Kim. 2023a. Max du, abraham lee, kuan fang, chelsea finn, and sergey levine. bridgedata v2: A dataset for robot learning at scale. In _7th Annual Conference on Robot Learning_ . 

- Homer Rich Walke, Kevin Black, Tony Z. Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, Abraham Lee, Kuan Fang, Chelsea Finn, and Sergey Levine. 2023b. Bridgedata v2: A dataset for robot learning at scale. In _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 1723–1736. PMLR. 

- Jonathan Heewon Yang, Dorsa Sadigh, and Chelsea Finn. 2023. Polybot: Training one policy across robots while embracing variability. In _7th Annual Conference on Robot Learning_ . 

- Samir Yitzhak Gadre, Mitchell Wortsman, Gabriel Ilharco, Ludwig Schmidt, and Shuran Song. 2022. Cows on pasture: Baselines and benchmarks for language-driven zero-shot object navigation. _arXiv e-prints_ , pages arXiv–2203. 

- Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. 2023a. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 11975–11986. 

