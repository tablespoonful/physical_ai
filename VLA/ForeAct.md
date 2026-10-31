---
title: "ForeAct: Steering Your VLA with Efficient Visual Foresight Planning"
date: "2026-02-12"
authors: "Zhuoyang Zhang; Shang Yang; Qinghao Hu; Luke J. Huang; James Hou; Yufei Sun"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2602.12322
pdf: https://arxiv.org/pdf/2602.12322
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.12322)** / [論文ページ](https://arxiv.org/abs/2602.12322)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**ForeAct: Steering Your VLA with Efficient Visual Foresight Planning** 

Zhuoyang Zhang<sup>1* †</sup> Shang Yang<sup>1* †</sup> Qinghao Hu<sup>1</sup> Luke J. Huang<sup>1</sup> James Hou<sup>1</sup><sup>_,_3</sup> Yufei Sun<sup>1</sup> Yao Lu<sup>2</sup> Song Han<sup>1</sup><sup>_,_2</sup> 1MIT 2NVIDIA 3Caltech 

**https://github.com/mit-han-lab/foreact** 


Figure 1. **Illustration of Visual Foresight Planning (ForeAct).** Instead of relying on a single high-level human instruction, our visual foresight planner guides the VLA step-by-step using imagined future observations and subtask descriptions. This design allows the VLA to concentrate on visuo-motor inference rather than high-level semantic reasoning, leading to improved accuracy and better generalization. 

# **Abstract** 

_Vision-Language-Action (VLA) models convert high-level language instructions into concrete, executable actions, a task that is especially challenging in open-world environments. We present Visual Foresight Planning (ForeAct), a general and efficient planner that guides a VLA step-bystep using imagined future observations and subtask descriptions. With an imagined future observation, the VLA can focus on visuo-motor inference rather than high-level semantic reasoning, leading to improved accuracy and gen-_ 

> *Equal Contribution. 

> †Part of the work done during an internship at NVIDIA. 

_eralization. Our planner comprises a highly efficient foresight image generation module that predicts a high-quality 640×480 future observation from the current visual input and language instruction within only 0.33s on an H100 GPU, together with a vision-language model that reasons over the task and produces subtask descriptions for both the generator and the VLA. Importantly, state-of-the-art VLAs can integrate our planner seamlessly by simply augmenting their visual inputs, without any architectural modification. The foresight generator is pretrained on over 1 million multi-task, cross-embodiment episodes, enabling it to learn robust embodied dynamics. We evaluate our framework on a benchmark that consists of 11 diverse, multi-step realworld tasks. It achieves an average success rate of 87.4%,_ 

1 

_demonstrating a +40.9% absolute improvement over the π_ 0 _baseline (46.5%) and a +30.3% absolute improvement over π_ 0 _augmented with textual subtask guidance (57.1%)._ 

# **1. Introduction** 

People have been working hard to enhance the physical intelligence of embodied systems, aiming to develop robust and general robots to help humans solve a wide range of tasks in the real world. A truly general robot should be capable of handling complex, diverse, unstructured environments and performing tasks that go far beyond preprogrammed routines. For example, it should be able to manipulate a variety of household objects, assist with daily chores such as cooking, cleaning, or organizing spaces, and adapt its behavior when encountering new tools or unfamiliar layouts. 

Recently, vision-language-action (VLA) models [5–7, 9– 11, 25, 27, 29, 32, 35, 37, 44, 46, 47, 54, 57] have emerged as a promising direction for developing general-purpose robots. These models learn a direct mapping from visual observations and language instructions to robotic actions in an end-to-end manner. However, most existing VLAs still excel only at simple tasks (e.g., picking up an object and placing it in a designated location), falling short of the broad capabilities we ultimately expect. We posit that one key factor underlying this limitation is the difficulty VLAs face in grounding high-level language instructions into concrete, executable action sequences. 

This raises the question: what if we provide VLAs with visual instructions rather than relying solely on language? Instead of merely telling a robot what to do, could we show it how to do it? For instance, when asking a robot to clean a table, supplying an image of the table after cleaning offers richer guidance, potentially simplifying task execution. Yet, in real-world settings, a fully final state may not always be attainable, and even when available, it often remains too abstract, omitting the intermediate steps necessary for execution. For example, cleaning a table including picking up the coke can, the water bottle, and the crumpled tissue, and then disposing of them in the trash bin one by one. This motivates a further inquiry: is it possible to provide robots with step-by-step visual instructions, enabling them to follow a visually guided sequence toward task completion? 

To this end, we propose _Visual Foresight Planning (ForeAct)_ , a general and efficient planning framework that instructs the VLA with visual guidance step-by-step. At the core of our approach is an efficient foresight image generator. It acts as a world model that conditions on the current observation and the language instruction to predict future observations. The generator is pretrained on over 1 million multi-task, cross-embodiment episodes curated from opensource datasets [9, 27, 48, 50], enabling it to learn robust em- 

bodied dynamics. Complementing this generator, we incorporate a vision-language model [3] to reason about complex tasks and infer appropriate subtasks, which are then provided to both the foresight generator and the VLA. These two components constitute our _ForeAct_ framework. By supplying imagined future observations, our method substantially reduces the difficulty for VLAs in grounding highlevel language instructions into concrete actions. Consequently, the VLA model can focus solely on visuo-motor inference rather than high-level semantic reasoning, leading to improved accuracy and generalization. Notably, state-ofthe-art VLAs can seamlessly integrate our visual guidance simply by augmenting their visual inputs, without requiring any architectural modifications. 

We highlight the efficiency of our visual foresight planner. Running on an H100 GPU, the foresight image generation takes only 0.33s. This demonstrates the practicality of our planner for real-world closed-loop control. To assess its effectiveness, we conduct comprehensive evaluations across 11 diverse real-world tasks. Our method achieves an average success rate of 87.4%, demonstrating a +40.9% absolute improvement over the _π_ 0 [7] baseline (46.5%) and a +30.3% absolute improvement over _π_ 0 augmented with textual subtask guidance (57.1%). 

# **2. Related Work** 

**Vision-Language-Action Models.** Vision-language-action (VLA) models integrate vision, language and action in a single policy, enabling robots to interpret human instructions and act on them. Early approaches [1, 8, 14] demonstrated the potential of multimodal policies for instruction-guided manipulation. More recently, state-of-the-art methods [5– 7, 9–11, 25, 27, 29, 32, 35, 37, 44, 46, 47, 54, 57] have advanced by fine-tuning pretrained vision-language models on large-scale robotic datasets, enabling direct mapping from visual-language instructions to robot actions. Representative works including RT-2 [57], OpenVLA [29], _π_ 0 [7], _π_ 0 _._ 5 [25], GR00T-N1 [5], Gemini Robotics [46] have shown unprecedented capabilities and achieved remarkable performance on real-world robot tasks. However, they still struggle with complex tasks and generalizing to novel scenarios. Our proposed Visual Foresight Planning method can enhance the VLA’s accuracy and generalization. **Robotic Planning and Reasoning.** Instead of directly mapping human instructions to robot actions, recent works try to decompose the complex tasks into a sequence of simpler sub-tasks before action execution. One line of research unify planning and control within a single model [17, 25, 38, 52]. However, such unification introduces significant challenges: (1) VLA models typically employ relatively small vision-language backbones (e.g., 3B parameters) to reduce latency, which limits their capacity for complex reasoning; and (2) fine-tuning these models on robot data often leads to 

2 


Figure 2. **Overview of our ForeAct framework.** The VLMbased subtask planner takes the robot’s head-camera observation and generates a subtask instruction for the Foresight Image Generation (ImGen) module. ImGen then predicts the future observation, which is fed into the VLA model together with the subtask instruction and the robot’s three camera views. These modules operate jointly to enable closed-loop control. 

catastrophic forgetting, thereby compromising their generalpurpose capabilities. Another line of research adopts a hierarchical framework [21, 23, 24, 34, 38, 42, 43, 45, 52, 53] that delegates planning and reasoning to a separate model. This design mitigates the risk of catastrophic forgetting and enables planning and reasoning to be performed by more capable models. However, it does not fundamentally alleviate the intrinsic challenge faced by VLA models in grounding high-level language instructions into concrete actions. In contrast, our planner provides a more detailed visual guidance, let the VLA focus on visuomotor inference. 

**Visual Prediction for Robot Control.** Integrating visual prediction into the control loop is a key advance to enable lookahead planning. Earlier works [16, 39] first investigated the benefit of visual prediction in model-based RL. SuSIE [6] generates goal images that guide diffusion policy models. COT-VLA [55] generates goal images and actions inside a unified model. More recently, with the development of video generation, people start to explore the use of video generation for robot control [2, 4, 15, 18, 22, 26, 30, 56]. While conceptually appealing, existing video-generationbased methods face key limitations: (1) slow and computationally expensive inference, (2) predominantly openloop designs that ignore environmental feedback, and (3) incompatibility with state-of-the-art pretrained VLAs. Our method is efficient and general, that can be integrated with the state-of-the-art VLAs in a closed-loop manner. 

# **3. Method** 

In this section, we first present ForeAct with a structured formulation in Section 3.1. We then introduce the efficient foresight image generation model, which is the core of our method, in Section 3.2. After that, we illustrate how we use VLM for reasoning and monitoring in Section 3.3. Finally, 

we show how to seamlessly integrate our method with VLA models in Section 3.4 and how we deploy the whole system in Section 3.5. 

## **3.1. Visual Foresight Planning (ForeAct)** 

**VLA.** Modern state-of-the-art VLAs are generally implemented as language-conditioned models, which aim to learn the conditional distribution 


where **_A_** _t_ = [ _at, at_ +1 _, · · · , at_ + _H−_ 1] is a chunk of actions of length H, **_I_** _t_ = [ _It_<sup>1</sup><sup>_, I_</sup> _t_<sup>2</sup><sup>_, · · ·, I_</sup> _t_<sup>_K_] is the current visual ob-</sup> servation from multiple cameras, **_q_** _t_ is the proprioceptive states from the robot, and _l_ is the language instruction. **VLA with ForeAct.** Our key insight is to introduce a visual foresight planner to enhance the VLA model. With ForeAct, the conditional distribution is reformulated as follows: 


_πh_ is our visual foresight planner, it provides the predicted future observation **_G_** _t_ and subtask description _lt_ conditioned on the current observation and the overall task description. _πl_ is the VLA model, it takes the predicted future observation **_G_** _t_ as an additional visual input and the subtask description _lt_ as the language condition to generate actions. Specifically, _πh_ is implemented with two components: 


At the core is the foresight image generation model _πg_ , which grounds the high-level language instruction into a concrete predicted future observation. Complementing this, _πv_ is a VLM to reason over the complex task and infer the subtask. Figure 2 illustrates the overall pipeline of our ForeAct framework. 

## **3.2. Efficient Foresight Image Generation** 

Our core idea is to predict an imagined future observation that clearly guides the VLA model, rather than relying on solely language instructions. We design the foresight image generation model to closely approximate the actual future observation. To preserve generalization across heterogeneous robotic platforms, the model is conditioned solely on visual observations and language instructions, excluding other modalities such as robot proprioceptive states. For better adaptability and efficiency, we generate the foresight image only for the head camera, which captures the global scene and thus provides the most informative context. **Model Architecture.** Modern robots typically employ high-resolution cameras (e.g., 640 _×_ 480 or even 1280 _×_ 720) to capture detailed visual information. Consequently, our 

3 


Figure 3. **Foresight image generation model.** The current observation is first encoded into compact visual tokens and concatenated with a noise input, then fed into the efficient linear DiT model to generate the predicted visual tokens, which are subsequently decoded into the future observation. In addition, the instruction and a specially designed system prompt are incorporated to guide the model’s attention toward the robot’s actions. 

foresight image generation model must also support highresolution outputs to preserve fine details and subtle movements. Moreover, the generation must be efficient to be engaged in the real-world closed-loop control. Inspired by recent advances in efficient image generation, we adopt the architectural design of the state-of-the-art model SANA [51]. SANA employs a 32 _×_ deep compression autoencoder [12] to encode images into a compact latent space, substantially reducing the number of latent tokens. It also utilizes a linear DiT architecture to enable efficient attention computation at high resolutions. However, SANA is originally designed for text-to-image generation and thus cannot directly process image conditions. To address this limitation, we concatenate the conditioned image with the noise input, thereby transforming the denoising process into a conditional denoising task. The detailed model architecture of our foresight image generation model is illustrated in Figure 3. 

**Pre-training Dataset.** We collect a large and diverse opensource cross-embodiment dataset for pre-training, allowing the model to learn generalizable embodied dynamics through foresight image generation. Specifically, we collect data from the AgiBot-World Colosseo [9], RoboMind [50], Galaxea Open-World [27], and Bridge [48] datasets. We exclude datasets such as Open-X-Embodiment [41] and DROID [28] due to their relatively low camera resolution. Our collected dataset covers a wide range of robot embodiments as shown in the right panel of Figure 4. 

**Data Preprocessing.** After collecting the datasets, we preprocess the data to suit our requirements. Tasks in AgiBotWorld Colosseo, RoboMind, and Galaxea Open-World are typically complex and long-horizon, so we decompose them into subtasks. They already provide detailed subtask segmentations, which we directly adopt for task splitting. In contrast, the Bridge dataset contains relatively simple tasks, so we use the provided task descriptions directly without further subdivision. After preprocessing, the number of subtasks from each dataset is shown in the left panel of Figure 


Figure 4. (a) **Number of subtasks from each dataset.** Our data comes from a wide range of sources, and preprocessing yields a total of 1.16 million subtasks. (b) **Diverse robot embodiments in the pre-training dataset.** The collected dataset covers a wide range of robot embodiments. 

4, with a total number of 1.16 million subtasks. 

Within each subtask, we sample condition frames at 1- second intervals. For each condition frame, we choose a future frame that comes half a subtask’s length later in time. We set this offset to half the subtask length because it gives frame pairs that clearly show meaningful action changes. The paired language instruction is the description of the robot’s action of the subtask. After sampling, we get a total of approximately 10 million data pairs for pre-training. **Training Details.** Following SANA, we adopt flow matching as our training objective. All images are resized to 640Œ480 during training. We initialize our model with SANA-1.6B-512px’s pre-trained weights to leverage its strong image-generation priors. The global batch size is set to 512, and training is conducted for 800K steps on 64 H100 GPUs. We leverage a constant learning rate of 5e-5 with 5K steps warmup. 

## **3.3. VLM for Reasoning and Monitoring** 

In our ForeAct framework, the VLM operates in a _reason-execute-monitor_ cycle. Given the overall task description and the current observation, it first reasons by generating an immediate, actionable subtask. After the VLA executes the actions, the VLM monitors by assessing the updated state, tracking progress, and re-planning the next subtask if the current subtask is completed. This hierarchy enables the VLA model to dynamically recover from execution failures and adapt to environmental uncertainties, yielding robust and scalable performance across complex real-world tasks. 

## **3.4. Adapt to VLA Models** 

When integrating ForeAct, the VLA model requires no architectural modifications as we only augment the visual input. During VLA fine-tuning, we concatenate the current observation with a future observation to form the visual input. During inference, the generated foresight image is ap- 

4 


Figure 5. **Examples of tasks in our real-world dataset.** 

pended to the current observation to serve as the visual input, while the generated subtask instruction serves as the language input to the fine-tuned VLA model. This design requires minimal adjustments, thereby enabling seamless integration of our ForeAct with existing VLA models. 

## **3.5. Cloud-Edge Closed-Loop Deployment** 

To achieve responsive, closed-loop control for real-world robotics, we design a hierarchical cloud-edge deployment pipeline. The workflow begins with the edge host responsible for reactive local control, which captures and sends the observation to the remote cloud server. This server, specialized for reasoning and foresight generation (hosting the VLM and image generator with vLLM [31]), performs highlevel planning and distills the result into a dual-guidance packet (textual _lt_ , visual **_G_** _t_ ). This packet is then returned to the edge host, where the local VLA policy performs rapid inference to dispatch the final action. In our setting, we deploy the visual foresight planner on an H100 GPU, and the VLA on a RTX 5090 GPU. 

# **4. Experiments** 

## **4.1. Setups** 

**Robot System.** We collect our real-world data on the Galaxea R1 Lite [19], a dual-arm mobile manipulator equipped with 23 degrees of freedom (6-DoF chassis, 3- DoF torso, and two 7-DoF arms). The platform also features a comprehensive multi-view perception suite, including a head-mounted stereo camera and two wrist-mounted monocular depth cameras. 

**Comprehensive Real-World Dataset.** We collect a comprehensive and challenging real-world dataset consisting of 11 tasks that simulate activities in _Kitchen_ , _Workspace_ , and _Factory_ with varying levels of difficulty. 

- **Kitchen:** Tasks involve diverse object manipulation in kitchen environments, ranging from simple conditional placements ( _e.g., pick one of five vegetables on a plate_ ) to multi-stage sequential operations ( _e.g., stack three bowls on a plate_ ) and complex dual-arm sorting ( _e.g., classify tabletop waste into bins using single or dual arms_ ). 

- **Workspace:** Tasks emphasize typical office organization routines, scaling from basic interactions ( _e.g_ ., _put a pen in a drawer_ ) to complex, multi-step arrangements involving multiple objects ( _e.g., organize a study desk_ by placing pens, staplers, and tape into their designated containers). 

- **Factory:** Tasks simulate industrial kitting and assembly procedures, including basic tool retrieval ( _e.g., place a specified tool into a box_ ), item packing ( _e.g., pack flowers into a box_ ) and instance-level sorting ( _e.g., separate different masks into different boxes_ ). 

We provide example tasks of our real-world dataset in Figure 5. In total, we collect 420 episodes. Each episode is then decomposed into subtasks, resulting in 2,312 subtask-level episodes. We randomly sample 50 episodes to construct the in-distribution test set, the remaining 370 episodes are used for finetuning the foresight image generation model and the VLA model. 

## **4.2. Efficient Foresight Image Generation** 

We have already pretrained the foresight image generation model on a comprehensive and diverse dataset. For deployment in our specific setting, we perform lightweight finetuning to adapt to our specific robot type and the new environment. We finetune the foresight image generation model on our collected real-world data. We use a batch size of 32 and run for 5 epochs. We leverage a constant learning rate of 1e-5 with no warmup. 

**Effectiveness of Large-scale Pre-training.** To demonstrate the effectiveness of the pretraining, we also conduct an experiment in which the foresight image generation model is trained using only our self-collected data without robot data pretraining. For fair comparison, the from scratch training follows the same settings as the finetuning. 

We evaluate the generated images under both indistribution and out-of-distribution test settings. The indistribution setting corresponds to tasks and environments that match those seen during training, although the object layouts may differ. Since layout variations are also present in the training data, we consider these cases as in-distribution. The out-of-distribution setting involves changes to either the task or the environment. For example, the robot may be required to manipulate a different object within the same environment, such as picking the corn in the packing flower environment. For the in-distribution evaluation, we sample 50 observations from the test split of our dataset; for the out-of-distribution evaluation, we design and collect 50 new observations. 

5 

Table 1. **Quantitative results of foresight image generation.** The scores are averaged over 50 images for both in-distribution and outof-distribution tasks. 

||**In distr**|**ibution**|**Out of di**|**stribution**|
|---|---|---|---|---|
|**Type**|**Fidelity **|**Quality **|**Fidelity**|**Quality**|
|w/o pretraining|0.18|0.24|0.00|0.00|
|w/ pretraining|1.00|1.00|0.88|0.96|


Figure 6. **Qualitative results of foresight image generation.** The first row shows the model without pretraining and the second row shows the model with pretraining. The task is to pick up the corn. We generate four images for each model with different random seeds. 

We assess generation performance from two perspectives: (1) image fidelity, which measures whether the generated image accurately follows the subtask instruction and lies on the correct path toward task completion; and (2) image quality, which evaluates whether the generated image preserves the detailed information of the original image without introducing significant distortions. Both criteria are scored via human evaluation, where each image is scored as 1 if it satisfies the requirement and 0 otherwise. As shown in Table 1, the foresight image generation model with pretraining achieves substantially better performance than the model trained from scratch. Without pretraining, the model completely fails on out-of-distribution tasks and obtains only very low scores on in-distribution tasks, indicating that it learns virtually no generalizable capability. In contrast, our pretrained model consistently attains high scores on both in-distribution and out-of-distribution tasks, demonstrating the effectiveness of the pretraining. 

We also provide a qualitative example for an out-ofdistribution task in Figure 6. The task is to pick up the corn. We generate four images for each model with different random seeds. The first row shows the model without pretraining, which can not generate the correct predicted image. The second row shows the model with pretraining, which generates the correct predicted image across all the four images, showing the effectiveness of the pretraining. **Discussion with Image Editing Models.** Our foresight image generation model conditions on the current observation (image) and a subtask instruction (text) to produce the predicted next-step image. This workflow is closely related to that of image-editing models, which raises the ques- 


Figure 7. **Qualitative results of image editing models.** State-ofthe-art image-editing models lack an understanding of the underlying real-world physics and object dynamics. They can not generate the correct predicted image with correct robot action. 


_step=1, latency=0.13s step=2, latency=0.16s step=4, latency=0.20s step=8, latency=0.33s_ 

Figure 8. **Latency measurement of foresight image generation.** Our foresight image generation model is able to generate a highquality 640 _×_ 480 imagined future observation in 0.33 seconds on an H100 GPU. 

tion: Can state-of-the-art image-editing models handle our task? To investigate this, we provide a qualitative comparison in Figure 7 and evaluate several state-of-the-art imageediting models, including Gemini 2.5 Flash Image [13], GPT-Image [40], and Qwen-Edit [49]. As shown in the first example, all three models make almost no meaningful modifications to the scene. In the second example, although the first model slightly adjusts the arm, it produces an unnatural grasp of the carrot, while the other two models directly hallucinate a carrot on the plate instead of manipulating the existing one. These failure cases indicate that state-of-the-art image-editing models lack an understanding of the underlying real-world physics and object dynamics, thus can not be used to handle our task. Moreover, due to their large parameter sizes, these models incur substantial inference latency, making them impractical for use in closed-loop control. **Latency Measurement.** We evaluate the latency of our foresight image generation model on an H100 GPU, where the planner is deployed. Because latency is critical for closed-loop control, minimizing generation time is essential. A straightforward approach is to reduce the number of denoising steps. As shown in Figure 8, extremely small step counts (e.g., 1-2) lead to severe artifacts, whereas using 8 steps yields visually reliable predictions. Increasing the step count beyond 8 provides negligible quality improvements. Therefore, in our real-world experiments, we set the number of steps to 8, resulting in a latency of only 0.33 s. 

6 


Figure 9. **Real-world evaluation of ForeAct framework** . Our system consistently outperforms baselines without visual guidance across all benchmarking tasks. It achieves an average success rate of 87.4%, representing a +30.3% improvement over the VLM-augmented baseline (VLM + _π_ 0) and a +40.9% improvement over the vanilla _π_ 0 baseline. Furthermore, it maintains an average success rate of over 70% across all benchmark tasks, demonstrating the robustness of our proposed method. 

This demonstrates the efficiency of our foresight image generator and highlights its practicality for real-world closedloop control. Although we have not yet incorporated acceleration techniques such as distillation or quantization, we believe further reductions in latency are possible and leave this exploration for future work. 

## **4.3. Real-World Benchmark Evaluation** 

**Baselines.** We set up end-to-end real-world evaluation on the Galaxea R1 Lite platform [19] with the _π_ 0 [7] architecture and finetuning it on our self-collected data for realworld adaptation. We compare with the following systems to illustrate the effectiveness of ForeAct: 

- _π_ 0: A 3.3B VLA model pretrained on over 10k hours of robot data. We finetune it on our self-collected data on Galaxea R1 Lite platform for real-world adaptation. 

- _VLM + π_ 0: _π_ 0 model augmented with Qwen-3-VL-8BInstruct [3] model for subtask planning and monitoring. We finetune the _π_ 0 model on the subtask-level episodes of our self-collected data, in accordance with the VLM planning granularity. 

- _Ours_ : _π_ 0 model enhanced with our ForeAct framework. In our visual foresight planner, we also employ Qwen3-VL-8B-Instruct as the VLM for subtask planning and monitoring. We fine-tune the _π_ 0 model on the subtasklevel episodes from our self-collected dataset, augmenting the visual input with a future observation. Specifically, we use the final frame of each subtask episode as the future observation. 

**Metrics.** We evaluate the performance of the systems across 11 diverse tasks. Please refer to Sec. A.3 for detailed description of all our real-world tasks with visual examples. For each task, we break down the task into "atomic actions" at the granularity of "approach and grasp" and "move and place". Then, we score the systems success rate of the whole task as the ratio of the number of successful "atomic actions" to the total number of "atomic actions". Mean- 

while, if the robot performs any undesired action, such as picking up any object that is not targeted in the task, we deduct the score by the value of a single atomic action. If any atomic action cannot be completed within 5 trials, or the robot ruins the whole task setting through undesired actions, we consider the uncompleted "atomic actions" in the task as failed. For each task, we repeat the evaluation with at least 5 different initial settings (e.g., different object layouts) and report the average score of each model. 

**Results.** In Figure 9, we demonstrate the evaluation results on our real-world benchmark. Across all the 11 tasks, our system achieves the highest success rate, with a +30.3% improvement over the VLM + _π_ 0 baseline and a +40.9% improvement over the vanilla _π_ 0 baseline, demonstrating the effectiveness of our ForeAct. 

Particularly, for the tasks such as Pack_Flower and Toy_Blocks, where the robot need to distinguish different objects and take different actions according to the object type, our system surpasses the baseline systems by a great margin. We attribute this improvement to our visual foresight guidance, which provides the robot with the additional goal state information rather than brief text instructions. As a result, the VLA model does not bother to reason which is the aimed object and what is the intended action, and the visual guidance helps the VLA model to learn generalizable visuo-motor skills. 

Additionally, to demonstrate the generality and scalability of our framework, we also evaluate it with the stronger _π_ 0 _._ 5 backbone. As detailed in Table 2, our method consistently outperforms the vanilla _π_ 0 _._ 5 baseline. Overall, the average success rate increases from 70.3% to 88.2%, confirming that our visual foresight planning provides essential enhancement for general VLA models. 

## **4.4. Simulation Benchmark Evaluation** 

We further validate our method with the LIBERO simulation benchmark [36] with _π_ 0 _._ 5 [25] model. We evaluated the 

7 

Table 2. **Real-world evaluation with** _π_ 0 _._ 5 **.** On a representative set of real-world tasks, our method boosts the average success rate of the highly capable _π_ 0 _._ 5 model from 70.3% to 88.2%. 

|**Task Name**|_π_**0**_._**5**|**Ours**|**Task Name**|_π_**0**_._**5**|**Ours**|
|---|---|---|---|---|---|
|Pick_Veg|60.0|86.6|Office_Desk|76.0|85.4|
|Place_Bowl|75.0|83.3|Pick_Tool|50.0|96.7|
|Pen_Drawer|68.8|81.3|Pack_Flower|91.8|95.8|


Table 3. **Simulation evaluation on LIBERO.** We evaluate the success rate (%) of our method integrated with _π_ 0 _._ 5 against stateof-the-art VLA baselines including vanilla _π_ 0 _._ 5. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|OpenVLA [29]|84.7|88.4|79.2|53.7|76.5|
|CoT-VLA [55]|87.5|91.6|87.6|69.0|83.9|
|_π_0 [7]|96.8|98.8|95.8|85.2|94.2|
|_π_0_._5 [25]|97.3|98.8|96.9|94.2|96.8|
|CogVLA [33]|**98.6**|98.8|96.6|95.4|97.4|
|Ours (w/_π_0_._5)|97.3|**99.8**|**97.3**|**95.4**|**97.5**|


performance across four standard task suites: Spatial, Object, Goal, and Long-horizon (LIBERO_10). The success rate is averaged over 500 trials for each suite. As shown in Table 3, our method consistently improves the performance upon _π_ 0 _._ 5 baseline that already achieves near-perfect success rates, raising the average success rate from 96.8% to 97.5%. 

## **4.5. Generalization to OOD Tasks** 

We design OOD (Out-Of-Distribution) variants of the Pick_Veg task to evaluate the generalization capability of our ForeAct framework. As shown in Figure 10, our ForeAct framework remains robust in OOD settings, whereas baseline models suffer a substantial performance drop. 

To better illustrate this, we provide a qualitative example in Figure 12. The task requires the robot to put three different vegetables (a carrot, a bok choy, and an eggplant) into the plate, a composition of subtasks never seen during training, where only single-vegetable picking was demonstrated. As a result, the baseline model (VLM + _π_ 0, Figure 12 (a)) fails to adapt. It gets stuck in a loop, repeatedly attempting to grasp the same region where the carrot was, even though it is now empty. In contrast, the model augmented with our ForeAct framework successfully completes this complex OOD task, as shown in Figure 12 (b). Our framework correctly monitors the task progress and provides corresponding visual foresight, allowing the VLA to robustly execute all three distinct subtasks in sequence. 

## **4.6. Data Efficiency** 

We evaluate data efficiency on the challenging Clean_Rubb task by varying the size of the training 


Figure 10. **Quantitative evaluation on OOD variants of the Pick_Veg task.** The x-axis denotes increasingly difficult evaluation settings. Specifically, Original refers to the in-distribution setting. + Spatial OOD introduces spatial permutations of objects that is unseen in the training data. + Comp.OOD assesses compositional generalization by requiring the model to manipulate two objects, whereas training only involves single-object tasks. Finally, + Joint OOD combines both spatial and compositional shifts. 


Figure 11. **Data efficiency analysis on the Clean_Rubb task.** We compare the success rates of our method (red) versus the VLMaugmented baseline (gray) when trained on data subsets ranging from 20% to 100%. Our method consistently outperforms the baseline across all data regimes. 

set. As shown in Figure 11, our method exhibits strong sample efficiency: with only 60% of the data, it attains a >90% success rate, and with just 20% of the data, it still achieves 79%, substantially outperforming the baseline. Although the baseline method shows performance gains as the dataset grows, its rate of improvement is considerably slower, underscoring the superior data efficiency of our ForeAct approach. Note that for this ablation, we construct training subsets solely from the Clean_Rubb task data. Therefore, the success rate at 100% data usage here is slightly lower than the main benchmark result reported in the main paper, which benefits from multi-task co-training. 

Furthermore, limited fine-tuning data severely constrains baseline performance. As shown in Fig. 9, while our system achieves a 93.4% success rate in the Pick_Tool task, baselines fall below 30%. Since there are 5 distinct tools forming 5! = 120 spatial permutations, and the task requires manipulating any one of these five tools within each 

8 


Figure 12. **Qualitative results for a compositional OOD task.** The overall instruction is to "put the carrot, bok choy, and eggplant into the plate," a sequence not seen in training. (a) The baseline (VLM + _π_ 0) gets lost in this task, repeatedly trying to grasp the first object’s location even after it is gone. (b) Our method robustly executes all three subtasks with the augmentation of visual guidance for each step. 

Table 4. **Ablation on instruction modalities for the Pick_Tool task** . We compare standard semantic instructions with spatialbased text prompts. "Spatial Text" provides location of the target object, simplifying the task by removing the need for object grounding. 

|Method|Instruction Type|Success Rate (%)_↑_|
|---|---|---|
|Single_π_0|Semantic Text|20.0|
|Single_π_0|Spatial Text|46.8|
|Ours|Semantic Text + Goal Image|93.4|


layout, the total number of unique configurations reaches 120 _×_ 5 = 600. Collecting teleoperation trajectories for every permutation within the finetuning data for the single task is sub-optimal and practically infeasible. Therefore, we hypothesize that baselines fail to generalize in this data-scarce regime because they struggle to ground task prompts to specific tool objects. 

To further investigate this, Table 4 presents an ablation where semantic instructions (e.g., "Pick up the hammer") are replaced with spatial ones (e.g., "Pick up the object on the bottom right") in both finetuning and inference. This modification significantly improves baseline accuracy by decoupling semantic recognition from action execution. By bypassing the need for the VLA to infer object semantics from visual observations, the model can dedicate its limited capacity to action prediction. Nevertheless, these baselines still lag behind our ForeAct framework, as spatial text remains a coarser and more ambiguous modality compared to the fine-grained image-based guidance we introduce. These results collectively suggest that our visual foresight mechanism fundamentally enhances data efficiency: by converting abstract semantic instructions into concrete visual targets, it reduces the reliance on exhaustive demonstration coverage and enables robust generalization even when fine-tuning data is far too sparse to cover the full combinatorial space of task configurations. 

# **5. Conclusion** 

In this work, we present Visual Foresight Planning (ForeAct), a general and efficient planner that instructs VLA models with step-by-step imagined future observations and subtask guidance. By providing imagined future observations, it allows VLAs to focus on visuo-motor execution, leading to improved accuracy and generalization. The foresight image generation inside our planner is efficient, running at 0.33s to produce a 640Œ480 future observation on an H100 GPU. We evaluate our method across 11 diverse real-world tasks, it achieves an average success rate of 87.4%, outperforming both vanilla and VLM-augmented baselines by large margins. Furthermore, it demonstrates strong performance in out-of-distribution scenarios. Overall, our results show that ForeAct is a powerful and practical direction for enabling more capable and reliable embodied intelligence. 

# **Acknowledgements** 

We thank MIT-IBM Watson AI Lab, Amazon and National Science Foundation for supporting this research. We thank NVIDIA for donating the DGX server. 

# **References** 

- [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 2 

- [2] Anurag Ajay, Seungwook Han, Yilun Du, Shuang Li, Abhi Gupta, Tommi Jaakkola, Josh Tenenbaum, Leslie Kaelbling, Akash Srivastava, and Pulkit Agrawal. Compositional foundation models for hierarchical planning. _Advances in Neural Information Processing Systems_ , 36:22304–22325, 2023. 3 

- [3] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo, Qidong Huang, Jie Huang, Fei Huang, Binyuan Hui, Shutong Jiang, Zhao- 

9 

hai Li, Mingsheng Li, Mei Li, Kaixin Li, Zicheng Lin, Junyang Lin, Xuejing Liu, Jiawei Liu, Chenglong Liu, Yang Liu, Dayiheng Liu, Shixuan Liu, Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui Men, Lingchen Meng, Xuancheng Ren, Xingzhang Ren, Sibo Song, Yuchong Sun, Jun Tang, Jianhong Tu, Jianqiang Wan, Peng Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang, Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu, Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen Yu, Fei Zhang, Hang Zhang, Xi Zhang, Bo Zheng, Humen Zhong, Jingren Zhou, Fan Zhou, Jing Zhou, Yuanzhi Zhu, and Ke Zhu. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 2, 7 

- [4] Homanga Bharadhwaj, Debidatta Dwibedi, Abhinav Gupta, Shubham Tulsiani, Carl Doersch, Ted Xiao, Dhruv Shah, Fei Xia, Dorsa Sadigh, and Sean Kirmani. Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation. _arXiv preprint arXiv:2409.16283_ , 2024. 3 

- [5] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 2 

- [6] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained imageediting diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 3 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 2, 7, 8 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [9] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 2, 4 

- [10] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- [11] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 2 

- [12] Junyu Chen, Han Cai, Junsong Chen, Enze Xie, Shang Yang, Haotian Tang, Muyang Li, Yao Lu, and Song Han. Deep compression autoencoder for efficient high-resolution diffusion models. _arXiv preprint arXiv:2410.10733_ , 2024. 4 

- [13] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: 

Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 6 

- [14] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. Palm-e: An embodied multimodal language model. In _International Conference on Machine Learning_ , 2023. 2 

- [15] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36: 9156–9172, 2023. 3 

- [16] Frederik Ebert, Chelsea Finn, Sudeep Dasari, Annie Xie, Alex Lee, and Sergey Levine. Visual foresight: Model-based deep reinforcement learning for vision-based robotic control. _arXiv preprint arXiv:1812.00568_ , 2018. 3 

- [17] Huang Fang, Mengxi Zhang, Heng Dong, Wei Li, Zixuan Wang, Qifeng Zhang, Xueyun Tian, Yucheng Hu, and Hang Li. Robix: A unified model for robot interaction, reasoning and planning. _arXiv preprint arXiv:2509.01106_ , 2025. 2 

- [18] Yao Feng, Hengkai Tan, Xinyi Mao, Chendong Xiang, Guodong Liu, Shuhe Huang, Hang Su, and Jun Zhu. Vidar: Embodied video diffusion model for generalist manipulation. _arXiv preprint arXiv:2507.12898_ , 2025. 3 

- [19] Galaxea Team. R1 Lite Hardware Introduction. https:// docs.galaxea-ai.com/Guide/R1Lite/R1Lite_ Hardware_Introduction/, 2024. 5, 7 

- [20] Gemini Team. Gemini 3 Website. https://deepmind. google/models/gemini/, 2025. 13 

- [21] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. Look before you leap: Unveiling the power of gpt4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ , 2023. 3 

- [22] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 3 

- [23] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, YuChiang Frank Wang, and Fu-En Yang. Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 3 

- [24] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, et al. Inner monologue: Embodied reasoning through planning with language models. _arXiv preprint arXiv:2207.05608_ , 2022. 3 

- [25] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0. 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 2, 7, 8 

- [26] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 3 

10 

- [27] Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, Huazhe Xu, and Hang Zhao. Galaxea open-world dataset and g0 dualsystem vla model. _arXiv preprint arXiv:2509.00576_ , 2025. 2, 4 

- [28] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

   - 4 

- [29] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2, 8 

- [30] Po-Chen Ko, Jiayuan Mao, Yilun Du, Shao-Hua Sun, and Joshua B Tenenbaum. Learning to act from actionless videos through dense correspondences. _arXiv preprint arXiv:2310.08576_ , 2023. 3 

- [31] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention. In _Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles_ , 2023. 5 

- [32] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 2 

- [33] Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ , 2025. 8 

- [34] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. _arXiv preprint arXiv:2209.07753_ , 2022. 3 

- [35] Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 2 

- [36] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 7 

- [37] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 2 

- [38] Oier Mees, Jessica Borja-Diaz, and Wolfram Burgard. Grounding language with visual affordances over unstructured data. _arXiv preprint arXiv:2210.01911_ , 2022. 2, 3 

- [39] Suraj Nair and Chelsea Finn. Hierarchical foresight: Selfsupervised learning of long-horizon tasks via visual subgoal generation. _arXiv preprint arXiv:1909.05829_ , 2019. 3 

- [40] OpenAI. GPT Image 1 Model Card. https : //platform.openai.com/docs/models/gptimage-1, 2025. 6 

- [41] Abby ONeill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 4 

- [42] Pratyusha Sharma, Antonio Torralba, and Jacob Andreas. Skill induction and planning with latent language. In _Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 1713–1726, 2022. 3 

- [43] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, et al. Hi robot: Open-ended instruction following with hierarchical visionlanguage-action models. _arXiv preprint arXiv:2502.19417_ , 2025. 3 

- [44] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 2 

- [45] Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. Progprompt: Generating situated robot task plans using large language models. _arXiv preprint arXiv:2209.11302_ , 2022. 3 

- [46] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 2 

- [47] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2 

- [48] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 2, 4 

- [49] Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin, Kaiyuan Gao, Kun Yan, Sheng ming Yin, Shuai Bai, Xiao Xu, Yilei Chen, Yuxiang Chen, Zecheng Tang, Zekai Zhang, Zhengyi Wang, An Yang, Bowen Yu, Chen Cheng, Dayiheng Liu, Deqing Li, Hang Zhang, Hao Meng, Hu Wei, Jingyuan Ni, Kai Chen, Kuan Cao, Liang Peng, Lin Qu, Minggang Wu, Peng 

11 

Wang, Shuting Yu, Tingkun Wen, Wensen Feng, Xiaoxiao Xu, Yi Wang, Yichang Zhang, Yongqiang Zhu, Yujia Wu, Yuxuan Cai, and Zenan Liu. Qwen-image technical report, 2025. 6 

- [50] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multiembodiment intelligence normative data for robot manipulation. _arXiv preprint arXiv:2412.13877_ , 2024. 2, 4 

- [51] Enze Xie, Junsong Chen, Junyu Chen, Han Cai, Haotian Tang, Yujun Lin, Zhekai Zhang, Muyang Li, Ligeng Zhu, Yao Lu, et al. Sana: Efficient high-resolution image synthesis with linear diffusion transformers. _arXiv preprint arXiv:2410.10629_ , 2024. 4 

- [52] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 2, 3 

- [53] Andy Zeng, Maria Attarian, Brian Ichter, Krzysztof Choromanski, Adrian Wong, Stefan Welker, Federico Tombari, Aveek Purohit, Michael Ryoo, Vikas Sindhwani, et al. Socratic models: Composing zero-shot multimodal reasoning with language. _arXiv preprint arXiv:2204.00598_ , 2022. 3 

- [54] Andy Zhai, Brae Liu, Bruno Fang, Chalse Cai, Ellie Ma, Ethan Yin, Hao Wang, Hugo Zhou, James Wang, Lights Shi, et al. Igniting vlms toward the embodied space. _arXiv preprint arXiv:2509.11766_ , 2025. 2 

- [55] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 3, 8 

- [56] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 3 

- [57] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 2 

# **A. Appendix** 

## **A.1. Table of Contents** 

- Sec. A.2: We present additional qualitative foresight generation results, particularly in out-of-distribution scenarios to highlight the strong generalization of our model. 

- Sec. A.3: The detailed descriptions of all our real-world tasks with visual examples. 

- Sec. A.4: Evaluation on different VLMs’ performance as the high-level task planner. 

- Sec. A.5: The prompt we use for the VLM model. 

- Sec. A.6: A video demo. 

## **A.2. Qualitative Foresight Generation Results** 

Figure 14 presents further qualitative results of our foresight image generation model. All scenarios shown are outof-distribution, highlighting the strong capability and generalization of our model. This further demonstrates the effectiveness of our large-scale pretraining. We provide a detailed discussion of these scenarios below. 

- **First Row** : While all the objects are present in our dataset, they have never been co-located within the same scene. Although the dataset contains bowls, we do not include any scenes in which objects are placed inside a bowl. 

- **Second Row** : This scenario is similar to Pick_Veg; however, we introduce fruits (an apple and a banana) into the scene. Notably, neither apples nor bananas are present in our dataset. 

- **Third Row** : There is already an apple on the plate. In the Pick_Veg task, however, we place only a single object onto the plate. 

- **Fourth Row** : This scenario represents a completely unseen setting: all objects, including the new vegetables, fruits, and the glass bowl, are not present in our dataset. 

- **Fifth Row** : This scenario is similar to Clean_Rubb; however, instead of placing rubbish into the bin, we place fruits into it. 

- **Sixth Row** : This task is entirely novel and includes new objects such as a knife, a fork, and a paper cup. The paper cup has never been positioned on a plate in our dataset. 

## **A.3. Detailed Task Descriptions** 

In Table 6 and 7, we provide a comprehensive breakdown, with visual examples, of the 11 real-world robotic tasks used in our evaluation suite. To rigorously evaluate the models’ performance, we intentionally introduce distributional shifts between training and inference in some of the testbenches, such as increasing the number of objects, randomizing initial poses, or introducing novel distractors. Please refer to the tables for a summary of the operational protocol and data distribution for each task. 

12 


Figure 13. **Subtask Planning Accuracy across Different VLMs.** 

Table 5. **The prompt template used for the VLM planner.** The variable {Task} represents the high-level human instruction. 

#### **SYSTEM / INITIAL PROMPT (** _t_ = 0 **)** 

You are a robot controller. Please plan to finish the task in several steps. And give instruction for each step in a concise way. 

7B model validates the discriminative nature of our benchmark. 

## **A.5. VLM Prompt** 

To ensure reproducibility, we include the exact prompt templates we used for the VLM. The interaction is divided into two stages: the Initial Planning Phase ( _t_ = 0) and the Closed-Loop Monitoring Phase ( _t >_ 0). At _t_ = 0, upon receiving the first observation, the system applies the _Initial Prompt_ to specify the task and generate the first subtask. For all subsequent steps ( _t >_ 0), the system transitions to the _Follow-up Prompt_ , where the VLM uses the latest observation to assess progress on the previous instruction and produce the next one. The full templates for both phases are provided in Table 5. 

## **A.6. Demo Videos** 

The task is to “{Task}”. 

#### **RULES:** 

- During the job, I will continuously give you an observation image of the current state. 

- Based on the observation, please judge if the last instruction has been finished. 

- If yes, give me the instruction for the next step. 

- If no, repeat the instruction of the ongoing subtask. 

- You’re not required to describe the observation. Only output the instruction for each subtask. 

Now, you are only required to output instruction for the first step. 

**VISUAL INPUT** : [Initial Observation Image] 

#### **FOLLOW-UP PROMPT (** _t >_ 0 **)** 

#### **VISUAL INPUT** : [Current Observation Image] 

Pay attention to the latest observation. Firstly, judge if the last instruction has been finished. Secondly, if yes, give me the instruction for the next step; if no, repeat the instruction of the ongoing subtask. 

To provide a more intuitive understanding of our system’s real-world robustness, we include three video demonstrations corresponding to the Out-of-Distribution (OOD) scenarios as we mentioned in Section 4.3 of the main paper. These demos showcase how our Visual Foresight Planning framework successfully generalizes to unseen scenarios where baseline methods typically fail. 

- **Demo 1: Complex Compositions.** The robot is tasked with picking multiple vegetables sequentially, despite being trained only on single-object manipulation. 

- **Demo 2: Novel Objects.** The robot is tasked with picking fruits and placing them on a plate, whereas the training data only contained vegetable manipulation. 

- **Demo 3: New Configurations.** The robot performs the Clean_Rubb task under unseen spatial layouts and background settings. This highlights the planner’s robustness to novel environmental conditions and object positions. All videos are available at https://github.com/mit-han- 

- lab/foreact. 

Your answer should be concise and deterministic. Remember, your Overall Task is “{Task}”. 

## **A.4. Evaluating Performance of VLMs** 

To assess the generalization capability of our planner, we employ a rigorous LLM-as-a-Judge protocol. Specifically, we utilize Gemini-3-pro-preview [20] to evaluate the semantic correctness of the VLM-predicted subtasks on our long-horizon real-world video benchmark. As illustrated in Figure 13, our framework demonstrates strong model scalability. Both Qwen2.5-VL-32B and Qwen3-VL8B achieve competitive performance, effectively steering the robot through complex tasks. Conversely, the significant performance drop observed with the smaller Qwen2.5-VL- 

13 


Figure 14. **Qualitative Foresight Image Generation Results.** 

14 

Table 6. **Overview of robot tasks and descriptions in our real-world dataset** (Part I). 

### **Task Example** 

### **Detailed Description** 


**Data:** The task involves individual object placements, including a whiteboard eraser, a stapler, and a pen. The robot is required to sort all three objects in both training and evaluation. 

15 

Table 7. **Overview of robot tasks and descriptions in our real-world dataset** (Part II). 

### **Task Example** 

### **Detailed Description** 


**Protocol:** The robot retrieves designated tools, put them in the toolkit, and then closes the toolkit lid. 

**Data:** Both training and evaluation involve two target objects. Unseen objects were introduced during the evaluation to test zero-shot abilities. 


**Protocol:** The robot picks up flowers on the desk and place them into a box. **Data:** Both training and evaluation involve 2 to 3 flowers. Additional distractors, such as corn and grapes, are added to the workspace during evaluation. 

16 

