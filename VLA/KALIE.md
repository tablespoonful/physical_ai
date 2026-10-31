---
title: "KALIE: Fine-Tuning Vision-Language Models for Open-World Manipulation Without Robot Data"
date: "2025"
venue: "ICRA 2025"
url: https://doi.org/10.1109/ICRA55743.2025.11128156
pdf: https://arxiv.org/pdf/2409.14066
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2409.14066)** / [論文ページ](https://doi.org/10.1109/ICRA55743.2025.11128156)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **KALIE: Fine-Tuning Vision-Language Models for Open-World Manipulation without Robot Data** 

Grace Tang<sup>_∗_1</sup> , Swetha Rajkumar<sup>_∗_1</sup> , Yifei Zhou<sup>1</sup> , Homer Rich Walke<sup>1</sup> , Sergey Levine<sup>_†_1</sup> , Kuan Fang<sup>_†_2</sup> 

https://kalie-vlm.github.io/ 

**_Abstract_ — Building generalist robotic systems involves effectively endowing robots with the capabilities to handle novel objects in an open-world setting. Inspired by the advances of large pre-trained models, we propose Keypoint Affordance Learning from Imagined Environments (KALIE), which adapts pre-trained Vision Language Models (VLMs) for robotic control in a scalable manner. Instead of directly producing motor commands, KALIE controls the robot by predicting pointbased affordance representations based on natural language instructions and visual observations of the scene. The VLM is trained on 2D images with affordances labeled by humans, bypassing the need for training data collected on robotic systems. Through an affordance-aware data synthesis pipeline, KALIE automatically creates massive high-quality training data based on limited example data manually collected by humans. We demonstrate that KALIE can learn to robustly solve new manipulation tasks with unseen objects given only 50 example data points. Compared to baselines using pre-trained VLMs, our approach consistently achieves superior performance.** 

## I. INTRODUCTION 

The capability to handle an open set of objects, behaviors, and task specifications is essential to the development of generalist robotic systems. Existing learning methods for robotic control can require extensive amounts of data collected on embodied systems [21, 29, 2]. The diversity and quality of the collected data determines the generalization capability that these methods can achieve, which is subject to robotics expertise and manual labor that humans can provide. How can we endow robots with generalizable skills for solving an open set of tasks in a scalable manner? 

Large pre-trained models offer promising tools with their generalist visual understanding and commonsense reasoning abilities [28, 35, 39, 49]. Prior works have shown that pre-trained Large Language Models (LLMs) and Vision Language Models (VLMs) can be directly applied to robotics control through prompt engineering in a zero-shot manner [23, 13, 10, 32]. However, despite the capability of generalizing to unseen tasks, such systems often suffer from instability and require significant hard-coded domain knowledge to compensate for the pre-trained models’ limited knowledge about robotic control. While fine-tuning on robotic data can mitigate this issue and proves more sampleefficient than training policies from scratch [3, 27], the largest available datasets [7, 15, 37] for robotic control are still far from comparable to the Internet-scale data used for 

> _∗_ Equal contribution. _†_ Equal advising. 

> 1University of California, Berkeley. 2Cornell University. 


Fig. 1: **Overview of KALIE** . By fine-tuning a pre-trained VLM, KALIE predicts the point-based affordance representation given the input task instruction and visual observation. Based on limited example data collected by humans, KALIE generates synthetic data with high diversity while preserving the task semantics and the keypoint annotations. The fine-tuned VLM can robustly generate motions for tasks with unseen objects and arrangements. 

pre-training the large models with billions of parameters. It remains a grand challenge to effectively employ and adapt pre-trained large models for robotic control. 

In this paper, we aim to study an alternative solution to this challenge by training large models for manipulation without data collected on robots. Our key insight is to use visual affordances to guide robotic control and leverage the broad knowledge incorporated in large pre-trained models to efficiently learn to predict the affordances. Built upon pointbased affordance representations defined on 2D images from Manuelli et al. [25] and Fang et al. [10], we fine-tune a VLM on labeled affordance data. Humans can easily collect such affordance data by randomizing scenes for a target task (e.g., cleaning a table), taking images through the camera, and annotating the affordances on the image, which bypasses the need for collecting demonstration trajectories through teleoperation of the robots or hard-coded policies. The main challenges are 1) how to repurpose the VLM pre-trained for visual-question answering for efficient affordance learning, 

and 2) how to efficiently utilize human supervisions to create training data that can cover diverse scenarios. 

To this end, we propose Keypoint Affordance Learning from Imagined Environments (KALIE). As shown in Fig. 1, our approach fine-tunes a pre-trained VLM to a point-based affordance representation given the input task instruction and visual observation. Starting with limited example data of manually arranged scenes and annotated affordance labels, KALIE automatically creates a massive number of diverse synthetic images to scale up the training data. To stay faithful to the task semantics and keypoint annotations while diversifying the data distribution as much as possible, we propose an affordance-aware data synthesis pipeline using a pre-trained diffusion model [31, 47] with additional contexts. 

We evaluate KALIE on various manipulation tasks involving tool-use, articulated objects, and deformable objects. KALIE consistently solves target tasks with diverse unseen objects and initial arrangements and achieves superior performances compared to baselines using pre-trained VLMs [13, 10]. 

## II. RELATED WORK 

## _A. Robotic Control with Large Models_ 

An increasing number of works have employed foundation models in robotics through pre-training or fine-tuning on robot data manually collected through teleoperation or scripted policies [3, 9, 27, 33]. Due to the lack of datasets that can cover the vast complexity and diversity of robotics applications, most of the approaches focus on specific task categories such as grasping and object rearrangements. The generalization capability of the trained model is also constrained to the distribution of objects and environments covered by the manually collected datasets. Alternatively, other works have attempted to combine and prompt pretrained models to solve unseen tasks in zero-shot manners [23, 13, 10, 32, 12]. However, the performance of these works is usually subject to the capability of the pre-trained models, as well as non-trivial expert knowledge and manual labor to design prompts and in-context examples. In contrast to these approaches, the proposed method fine-tunes a VLM to robustly solve the target tasks. To avoid the need of collecting extensive amount of robot data, our model trains the VLM to predict the point-based affordance representation from [10] and employs a diffusion model to automatically synthesize massive, high-quality data. 

## _B. Adaptation of Vision Language Models_ 

Due to their versatile nature, Vision Language Models (VLMs) can be effectively fine-tuned to accommodate a variety of downstream tasks [11, 46, 4, 45]. Specifically, to facilitate the prediction of spatially grounded outputs, previous research has investigated methods such as sets of marks [42], scaffolding [28], and coordinate-based bounding boxes [38, 5, 39]. Of these methods, coordinate-based references are particularly adaptable, capable of pinpointing any location within an image. Thus, we employ this approach for predicting keypoints. Our contribution does not lie in 

proposing a new method for fine-tuning VLMs, but rather in integrating and adapting VLM fine-tuning for robotic control. 

## _C. Data Synthesis for Robot Learning_ 

To alleviate the data bottleneck in robot learning, prior works have investigated various approaches to augment and synthesize data. Data augmentation, especially random image transformations, have been widely used to improve generalization to unseen visual inputs [19, 20]. These random operations can effectively improve the models generalization capabilities to unseen visual inputs during test time, but cannot extend the model’s capabilities beyond the coverage of the training distribution. Domain randomization has also been broadly used to train robust models for robotic control [36, 26, 1, 30] when collecting simulated robot experiences. In contrast, our method directly diversifies the training data without the need for a physical simulator. Recent works in computer vision and robotics have leveraged deep generative models, such as diffusion models, to synthesize unseen environments by leveraging broad knowledge learned from Internet-scale images [14, 48, 40, 43, 44, 8, 41, 16, 22]. While the prior work can easily generate defected samples, we propose an affordance-aware data synthesis approach that enables the diffusion model to generate diverse data with much higher quality and consistent affordance annotations. 

## III. KEYPOINT AFFORDANCE LEARNING FROM IMAGINED ENVIRONMENTS 

We propose Keypoint Affordance Learning from Imagined Environments (KALIE) to adapt pre-trained Vision Language Models (VLMs) to acquire generalizable skills without robot experiences. In this section, we will first define the affordance prediction problem in the few-shot setting using point-based affordances labeled by human experts. Next, we will introduce a novel affordance-aware data synthesis recipe to diversify the training data, which automatically generates massive high-quality data based on the example data collected only for limited scenarios. Then, we will describe our VLM fine-tuning approach and discuss the key design options. Lastly, we summarize the overall system at the end of this section. 

## _A. Problem Statement_ 

We consider the problem of open-world robotic manipulation involving unseen objects and initial arrangements of the scenes. As shown in Fig. 1, each task is single-stage and is specified by a free-form language description _l_ , such as “ _Use the brush to sweep the snack package._ ” The robot observes an RGBD image from a third-person camera and performs a 6-DoF motion trajectory in open loop to complete the task. 

To tackle this problem, we employ a VLM _f_ pre-trained on Internet-scale data [39]. Following the practice of [10], we query the VLM to produce point-based affordance representations to guide a motion planner to generate motions. The VLM takes as inputs the prompt _ρ_ , the task instruction _l_ , and the input image _s_ and predict the affordance representation _y_ as: 


where _y_ contains a set of keypoints, including the grasp keypoint, the function keypoint, the target keypoint, the precontact waypoint, and the post-contact waypoint, specified by 2D coordinates on the image (see Fig. 1). Additional properties such as the height and the orientation of the gripper will also be decided for each task. Based on the affordance representation, a low-level motion generator computes a motion trajectory to complete the task. We assume the desired motion to solve each task can be specified by the same subset of these points (e.g., the sweeping with a brush requires all five points, and drawer closing requires everything but the grasp point, as shown in Section IV-E), but the specific coordinates of these points depend on the objects and their poses with respect to the robot. 

In this work, we consider tasks and objects which are challenging for VLMs to handle in zero-shot. In contrast to [10], we consider a few-shot learning setting, in which we fine-tune the pre-trained VLM to acquire and improve skills for unseen scenarios on limited and non-robot data. Notably, the point-based representations enable us to outsource motion generation to the low-level motion planner and focus on only the affordance prediction problem. Therefore, training only requires data of pairs of an observed image _s_ and the ground truth keypoints _y_ collected by human experts or generated automatically as described below. We assume access to an example dataset _D_ containing a limited number of ( _s, y_ ) pairs for each target task. In our experiments, we assume the most extreme case, in which the data is collected on _a single set of_ objects for each task and the fine-tuned model is evaluated on unseen object sets. 

## _B. Affordance-Aware Data Synthesis_ 

To scale up the training of the VLM to enhance its generalization capabilities to unseen scenarios, we automatically synthesize a training dataset _D_<sup>_′_</sup> to cover a wide range of environments. Each of the new data points ( _s_<sup>_′_</sup> _, y_<sup>_′_</sup> ) _∈D_<sup>_′_</sup> is synthesized by modifying an existing data point ( _s, y_ ) _∈D_ collected by human experts. 

Following the practice of [44], we compute the segmentation mask of the object in the scene using open-vocabulary segmentation [18] and then inpaint the masked region with a diffusion model [31]. However, naively inpainting the masked region can lead to undesired results. Without a direct mechanism to specify the geometric properties of the object, it would be hard to diversify the inpainted images in a way that can cover the desired distribution of testing scenarios. Moreover, there is usually a discrepancy between the appearance of the inpainted object and the original keypoint annotation, introducing the need to manually re-label keypoints. To generate massive, high-quality data without additional manual labor, we need to ensure that the generated images stay faithful to the context of the target task and the annotated keypoints, while aggressively diversifying the environments as much as possible. 

To tackle this challenge, we design an affordance-aware data synthesis pipeline by leveraging additional context images to guide the generation process, as shown in Fig. 2. 


Fig. 2: **Affordance-aware data synthesis.** KALIE employs the inpainting capability of a diffusion model to generate synthetic data. To diversify the scenes while staying faithful to the task semantics and the keypoint annotations, KALIE computes and transforms the context, such as soft edges, to guide the generation process. 

Specifically, we employ the ControlNet [47] diffusion model _g_ , which takes inputs as the input image _s_ , the segmentation mask _m_ , a context image _c_ , and a language description of the object _o_ and generates the new image as _s_<sup>_′_</sup> _∼ g_ ( _·|s, m, c, o_ ). We would like _c_ to be a compact representation of the object’s geometric properties that provide clues about the affordances, while minimizing other detailed visual information to leave enough free reign for the diffusion model. By inpainting an image _s_<sup>_′_</sup> in accordance with _c_ , we hope to obtain new objects of the same point-based affordances. In this work, we choose to use a soft edge map as _c_ computed by an external image processing algorithm [34], which outlines the contours and parts of the object. 

To cover testing objects of unseen shapes, we introduce additional randomization operations to the geometry of the synthesized object. Directly modifying either the object’s appearance in the pixel space can easily affect other parts of the image and create artifacts. Instead, we propose to apply transformation _h_ ( _·_ ) on the compact context _c_ before calling the diffusion model _G_ to inpaint the image. The transformation function _h_ ( _·_ ) can include basic data augmentation operations such as random scaling, translation, and rotation, as well as additional operations such as elastic distortion. To modify the context _c_ , we transform the region under the masked as _h_ ( _m ∗ c_ ). The region to be inpainted on the original image now becomes _m_ + _h_ ( _m_ ), which includes the transformed silhouette of the object _h_ ( _m_ ) in addition to the white space left by removing the original object _m_ . Accordingly, we also apply the same transformation to the annotated keypoints _y_ with the context image to keep them consistent. Therefore, the sampling process with the transformation can be written as: 


where we slightly overload the notation by using _h_ ( _·_ ) to denote the transformation applied to both the images and the keypoint coordinates. 

## _C. Efficient Adaptation for Keypoint Affordance Prediction_ 

We fine-tune the VLM _f_ to predict point-based affordance representations. To adapt _f_ , which is pre-trained for visualquestion answering by predicting tokens, we need to make our design choices around two considerations. First, how to represent the point-based affordances so that we can 

effectively re-purpose or modify the VLM’s prediction head for affordance prediction. Second, how to perform sampleefficient fine-tuning to utilize the pre-trained VLM’s pretrained capabilities while endowing it with the additional knowledge from the new dataset _D_ . 

We investigate two design options for the prediction head. **Regression Head** [6] adds an additional linear layer on top of the last hidden state of the VLM to directly predict the _x − y_ coordinates of the keypoint affordances. The input to the VLM is the image along with the appropriate task instructions, and the last hidden state of the last token is used. **Natural Language Affordance Prediction** fine-tunes the VLM to output a well-formatted natural language that includes text-based keypoint affordances, with an example shown in Fig. 1. Each keypoint affordance is represented by the _x − y_ coordinates as integers normalized between a predefined range. 

These design options resort to the pre-trained weights and the new dataset in different manners. Empirically as shown in Fig. 6, we found that the two design choices achieve similar performances. As Natural Language Affordance Prediction aligns more closely with other applications of VLMs such as Visual Question Answering, we choose to use this design option as our main method. During training, we convert the ground truth affordance label _y_ into the corresponding format to compute the losses. For both design options, we use LowRank Adaptation (LoRA) [24] to fine-tune the VLM. We use an L2 regression loss for Regression Head and the cross entropy loss for Natural Language Affordance Prediction. 

## _D. System Summary_ 

The overall pipeline of KALIE is summarized in Algorithm 1. Starting with the original example dataset _D_ , KALIE automatically creates _D_<sup>_′_</sup> to fine-tune the VLM _f_ . The data synthesis pipeline operates in an object-centric manner, iteratively processing and inpainting each of the _M_ objects in the scene as explained in Section III-B, using each object’s segmentation mask _mi_ and description _oi_ . During this process, a VLM (which can be the same as _f_ or a different model) is used to sample an alternative description of the object to guide the inpainting process of the diffusion model _g_ . The generated data is combined with the example dataset to adapt _f_ by optimizing the weights _w_ as explained in Section III-C. 

## IV. EXPERIMENTS 

We design our experiments to investigate the following questions: 1) Can KALIE synthesize diverse and high-quality data for affordance prediction? 2) Can KALIE fine-tune pretrained VLMs to improve their performances on challenging manipulation tasks with unseen objects? 3) What design options are critical to the performance of KALIE? 

## _A. Experimental Setup_ 

**Environments and tasks.** Our experiments are conducted in a real-world table-top manipulation environment with a 7-DoF robot arm and a Robotiq 2F-85 gripper. A top-down 

**Algorithm 1** Keypoint Affordance Learning from Imagined Environments <u>(KALIE)</u> 

**Inputs** : Pre-trained VLM _f_ , task instruction _l_ , example dataset _D_ , desired dataset size _N_ . 

|1:|_D_<sup>_′ _</sup>_←_∅|
|---|---|
|2:|**while** _|D_<sup>_′_</sup>_| < N_ **do**|
|3:|Sample (_s, y_) from _D_.|
|4:|Compute the context image _c_ given _s_.|
|5:|_s_<sup>_′_</sup><br>0 <sup>_←s_</sup>|
|6:|**for** _i_= 1_, ..., M_ **do** ( Section III-B)|
|7:|Extract the description _oi_ given _s_ and _l_.|
|8:|Get the segmentation mask _mi_ given _s_ and _oi_.|
|9:|Sample a new description _o_<sup>_′_</sup><br>_i_ <sup>given</sup> <sup>_oi_.</sup>|
|10:|Transform the mask, context as_h_(_mi_),_h_(_mi∗c_).|
|11:|Transform the keypoints as _h_(_yi_).|
|12:|Inpaint_s_<sup>_′_</sup><br>_i _<sup>_∼G_(</sup><sup>_·|s′_</sup><br>_i−_1<sup>_, h_(</sup><sup>_mi_)+</sup><sup>_mi, h_(</sup><sup>_mi∗c_)</sup><sup>_, o′_</sup><br>_i_<sup>).</sup>|
|13:|**end for**|
|14:|Merge the transformed keypoints into _y_<sup>_′_</sup>.|
|15:|**end while**|
|16:|Fine-tune _f_ on _D ∪D_<sup>_′_ </sup>by optimizing the weights _w_<br>( Section III-C).|


RGBD camera is used to receive visual observation of the environment. We design 5 table-top manipulation tasks (table sweeping, drawer closing, towel hanging, trowel pouring, and usb unplugging) each with 3 different testing object sets unseen during training. 

**Pre-trained models.** We fine-tune CogVLM-17B [39] using LoRA [24] with 6 layers and rank 10. The data synthesis is conducted using GPT-4V [28], which has higher capacity but does not have open-sourced code and models. **Affordance representations and motion primitive.** KALIE follows the keypoint-based affordance representation defined in [10], which contains the grasp keypoint, function keypoint, target keypoint, pre-contact waypoint, and postcontact waypoint. Given the affordance representation, the motion trajectory is produced by the motion generator in the SE(3) space, which consists of a grasping phase and a manpulation phase [10]. 

**Training and evaluation.** To fine-tune the VLM, 50 example images are collected by humans through randomly setting up the scenes based on the context of the task and annotating the affordance representations with a graphical user interface. Through data synthesis with diffusion models, we generate an additional set of 500 pairs of images and keypoints to the 50 examples. We fine-tune the VLM using the Adam optimizer [17] with a weight decay of 5 _×_ 10<sup>_−_2</sup> and apply an annealing learning rate scheduler with a starting learning rate of 1 _×_ 10<sup>_−_5</sup> and a cosine learning rate style. We train our models for 6000 iterations using a batch size of 4. For each target task, we test the model on 15 trials with 3 sets of unseen objects. Empirically, fine-tuning takes around 8 hours on a single Nvidia A100 SXM 80GB GPU. 

**Data scalability.** Collecting each image and annotating the keypoints takes a few seconds, depending on the task 

Fig. 4: **Comparisons with alternative synthesis algorithms.** KALIE generates much more robust samples comparing with generation without conditioning on the original images or the context. 

Fig. 3: **Synthetic data examples.** In each column, we show example synthetic images generated based on an example image for each task. The original and transformed point-based affordances are plotted on top of the images. 

complexity, which is significantly faster and easier than collecting a robot trajectory as done in prior work on the same experimental setup [15]. Empirically, collecting and generating the 500 synthetic images takes 90 minutes in total on a single Nvidia A100 SXM 80GB GPU. 

## _B. Data Synthesis_ 

In Fig. 3, we show examples of the synthetic images. Each row contains the data for a task. The first row is the example data and the remaining rows are the synthetic data. KALIE demonstrates generating diverse samples while preserving the task context and the original affordance labels. The generated objects have diverse, realistic textures that are different from the original image, including the transparent surfaces of the drawers and the detailed bristles on the brushes. Most of the examples are indistinguishable from the real example data with only minor artifacts at the boundary of the masked original image. 

To demonstrate the difficulty of such synthesis problems and the importance of the design options in KALIE, we also analyze the results from alternative approaches as seen in Figure 4. We first directly apply the diffusion model to generate the image without grounding on the original example image. Not only is the generation irrelevant to the annotated keypoints, without further guidance the quantity and appearance of the generated objects are also misaligned with the input instruction. While the original ROSIE [44] does not have an open-source codebase and uses an internal diffusion model, we reimplement it with the non-contextual version of the same diffusion model [47] as in KALIE. Without the context information, the model ignores part of the prompt and inpaints an empty table surface for the brush and a completely different shape for the trash. We found that this issue is particularly common for more complex objects, such as tools, but less severe for simpler items like towels, as shown in [44] and our experiments. 

## _C. Comparative Results_ 

We compare KALIE with two baselines that employ VLMs for robotic manipulation, **VoxPoser** [13] and **MOKA** [10]. In contrast to KALIE, which fine-tunes a much smaller open-source VLM, the two baselines use the pretrained OpenAI GPT-4V[28]. We use the collected example data as the in-context examples for MOKA. 

||Table|Drawer|Towel|Trowel|USB|
|---|---|---|---|---|---|
|Methods|Sweeping|Closing|Hanging|Pouring|Unplugging|
|VoxPoser [13]|3/15|8/15|1/15|0/15|0/15|
|MOKA [10]|9/15|9/15|5/15|7/15|2/15|
|KALIE (Ours)|**14**/15|**15**/15|**13**/15|**13**/15|**9**/15|


TABLE I: **Task success rates.** We evaluate KALIE on five manipulation tasks involving tool use, deformable objects, and articulated objects. KALIE robustly solves these tasks and consistently achieves superior performances compared to baselines. 

We evaluate each method across 5 manipulation tasks involving tool objects, articulated objects, and deformable objects. Compared to the baseline methods using pre-trained VLMs, KALIE consistently achieves higher success rates. For comparison, MOKA [10] is subject to failures such as incorrect output formats and affordance reasoning, while Voxposer [13]’s failure cases are often due to perception errors and a lack of in-context examples for more complex tasks, such as tool use. The VLM fine-tuned by KALIE robustly solves the tasks without these issues, and has far fewer failures due to inaccurate point predictions. 

## _D. Ablative Study_ 

We conduct an in-depth ablation study to study the performance of KALIE as seen in Figure 5 and Figure 6. Detailed analysis and discussions are provided below. 

**Comparisons with vanilla data augmentation.** In Fig. 5, we quantify the impact of both vanilla image augmentations and the synthetic data by KALIE on the VLM’s performance. The standard set of image augmentations includes rotations, random resized crops, horizontal/vertical flipping, and color jittering, which are added in the main training loop. We compare the performance of our model fine-tuned using KALIE with vanilla augmentation ( **full method** ) to that only using vanilla augmentations ( **only standard augmentations** ) and without any augmentations ( **no augmentations** ). We report the test mean square error (MSE) on a held-out set of 50 real images with unseen objects. We observe that using both sets of augmentations yields the best results in the VLM’s prediction of keypoint affordances. 

**Comparisons of prediction heads.** In Fig. 6, we analyze the choice of Natural Language Affordance Prediction ( **full method** ) against Regression Head ( **w/ regression head** ). We report the MSE on a held-out set with unseen objects and ground-truth annotations. The coordinates are normalized between 0 and 999 with respect to the actual height and width of the image. The train set consists of 50 real images collected on the robot and 500 synthesized images, and the test set consists of 50 real images of novel objects excluded 


Fig. 5: **Comparisons with vanilla data augmentation.** Mean Square Error (MSE) for each keypoint affordance on a test set of novel objects is reported for the table sweeping task. 


Fig. 6: **Ablative study.** The ablation experiments are carried out on the sweeping task. Mean Square Error (MSE) for each keypoint affordance on a test set of novel objects is reported. 

from the train set. We observe that Imagined Environments significantly improve the test MSE and our method with Natural Language Affordance Prediction works comparably with Regression Head, while staying consistent with the language interface of VLMs for vision-language tasks. 

**Comparisons with alternative context types.** We examine two alternative types of context information, depth mapping and segmentation masking, to provide ControlNet with the context image. In Fig. 6 we include MSE values on the same test set when using both these preprocessors, which we refer to as **w/ depth preprocessor** and **w/ seg mask preprocessor** , respectively. We found that both the depth map and the segmentation mask preprocessor models have inferior performances. We hypothesize that while these preprocessors yield the correct general shape of the objects, they do not capture enough detail for ControlNet [47] to be effective. Conversely, the softedge preprocessing allows for a generalization of the shape of each object while maintaining sufficient details of the object shape. 

**Scalability with example data.** We further investigated the results of training on 550 generated data points from 10 real images, as well as training a model on only the 10 real images. We refer to these as **10 examples** and **10 examples w/o imagination** respectively. As shown in Fig. 6, while 10 examples w/o imagination clearly performs worse than our other methods, we do not see any major difference between the MSEs of the 10 examples and 50 examples (full method). This further shows that our method is easily scalable, as a dataset with only 10 expert-annotated examples is able to perform at the level of a dataset with 50 such examples. 

## _E. Task Execution_ 

We show examples of affordance predictions and task execution in Fig. 7. The VLM fine-tuned by KALIE successfully predicts the affordance and solves each of the tasks. As shown in the figure, the robot successfully solve the tasks 


Fig. 7: **Affordance prediction and task execution.** We show examples of the predicted affordance representations and the key frames of task execution. Across 5 manipulation tasks, each with 3 sets of unseen objects, KALIE robustly solves the task. 

through interactions with the environment given the predicted keypoint-based affordance representations. 

## V. CONCLUSION 

In this work, we propose KALIE to fine-tune pre-trained VLMs to predict affordances for robotic manipulation with open sets of objects and initial arrangements of scenes. Using the proposed affordance-aware data synthesis pipeline, we generate massive high-quality data to scale up training without extensive manual labor or domain expertise with robots. We fine-tune the VLM on the generated data to predict the point-based affordance representations. Across various manipulation tasks involving tool use, deformable objects, and articulated objects, we demonstrate KALIE can robustly solve the task and consistently outperform baselines. We hope KALIE will inspire future research towards adapting vision-language models for open-world robotic control. 

**Limitations and future work.** The current affordance representation in KALIE is still limited to single-arm tabletop manipulation. To apply KALIE to more complicated scenarios, such as dynamic manipulation and whole-body control, we would need to extend the design of the affordance representation. In addition, there is still a large discrepancy between the open-source VLM fine-tuned by KALIE and the state-of-the-art VLMs without accessible fine-tuning APIs. Lastly, we have only discussed few-shot generalization in this paper, and would need to train KALIE on more diverse set of tasks to generalize to unseen target tasks in a zeroshot manner. In the future, we hope to apply KALIE to more powerful VLMs to further improve its performance. 

## ACKNOWLEDGMENT 

This research was supported by the AI Institute, AFOSR FA9550-22-1-0273, and the NSF under IIS-2246811. We would like to thank Sudeep Dasari, Ria Doshi, Stefanie Gschwind, Fangchen Liu, Cyprien Noel, Karl Pertsch, and Paul Zhou for valuable supports with the infrastructure. 

REFERENCES 

- [1] Ilge Akkaya, Marcin Andrychowicz, Maciek Chociej, Mateusz Litwin, Bob McGrew, Arthur Petron, Alex Paino, Matthias Plappert, Glenn Powell, Raphael Ribas, et al. Solving rubik’s cube with a robot hand. _arXiv preprint arXiv:1910.07113_ , 2019. 

- [2] Anthony Brohan et al. Rt-1: Robotics transformer for real-world control at scale, 2023. 

- [3] Anthony Brohan et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 

- [4] Baian Chen, Chang Shu, Ehsan Shareghi, Nigel Collier, Karthik Narasimhan, and Shunyu Yao. Fireact: Toward language agent fine-tuning, 2023. 

- [5] Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, and Rui Zhao. Shikra: Unleashing multimodal llm’s referential dialogue magic, 2023. 

- [6] William Chen, Oier Mees, Aviral Kumar, and Sergey Levine. Vision-language models provide promptable representations for reinforcement learning, 2024. 

- [7] Embodiment Collaboration. Open x-embodiment: Robotic learning datasets and rt-x models, 2024. 

- [8] Jeevan Devaranjan, Amlan Kar, and Sanja Fidler. Metasim2: Unsupervised learning of scene structure for synthetic data generation. In _Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part XVII 16_ , pages 715– 733. Springer, 2020. 

- [9] Danny Driess, F. Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Ho Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Peter R. Florence. Palm-e: An embodied multimodal language model. In _International Conference on Machine Learning_ , 2023. URL https://api.semanticscholar. org/CorpusID:257364842. 

- [10] Kuan Fang, Fangchen Liu, Pieter Abbeel, and Sergey Levine. Moka: Open-world robotic manipulation through mark-based visual prompting. 2024. 

- [11] Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxuan Zhang, Juanzi Li, Bin Xu, Yuxiao Dong, Ming Ding, and Jie Tang. Cogagent: A visual language model for gui agents, 2023. 

- [12] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. Look before you leap: Unveiling the power of gpt4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ , 2023. 

- [13] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 

- [14] Amlan Kar, Aayush Prakash, Ming-Yu Liu, Eric Cam- 

eracci, Justin Yuan, Matt Rusiniak, David Acuna, Antonio Torralba, and Sanja Fidler. Meta-sim: Learning to generate synthetic datasets. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 4551–4560, 2019. 

- [15] Alexander Khazatsky et al. Droid: A large-scale in-thewild robot manipulation dataset, 2024. 

- [16] Seung Wook Kim, Bradley Brown, Kangxue Yin, Karsten Kreis, Katja Schwarz, Daiqing Li, Robin Rombach, Antonio Torralba, and Sanja Fidler. Neuralfieldldm: Scene generation with hierarchical latent diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 8496–8506, 2023. 

- [17] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization, 2017. 

- [18] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Doll´ar, and Ross B. Girshick. Segment anything. _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 3992–4003, 2023. URL https://api.semanticscholar. org/CorpusID:257952310. 

- [19] Ilya Kostrikov, Denis Yarats, and Rob Fergus. Image augmentation is all you need: Regularizing deep reinforcement learning from pixels. _ArXiv_ , abs/2004.13649, 2020. URL https://api.semanticscholar. org/CorpusID:216562627. 

- [20] Misha Laskin, Kimin Lee, Adam Stooke, Lerrel Pinto, Pieter Abbeel, and Aravind Srinivas. Reinforcement learning with augmented data. _Advances in neural information processing systems_ , 33:19884–19895, 2020. 

- [21] Sergey Levine, Peter Pastor, Alex Krizhevsky, and Deirdre Quillen. Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection. _The International Journal of Robotics Research_ , 37:421 – 436, 2016. 

- [22] Daiqing Li, Huan Ling, Seung Wook Kim, Karsten Kreis, Sanja Fidler, and Antonio Torralba. Bigdatasetgan: Synthesizing imagenet with pixel-wise annotations. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21330–21340, 2022. 

- [23] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. In _IEEE International Conference on Robotics and Automation_ , pages 9493–9500. IEEE, 2023. 

- [24] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, and Lei Zhang. Grounding dino: Marrying dino with grounded pre-training for open-set object detection, 2023. 

- [25] Lucas Manuelli, Wei Gao, Peter R. Florence, and Russ Tedrake. kpam: Keypoint affordances for 

category-level robotic manipulation. In _International Symposium of Robotics Research_ , 2019. URL https: //api.semanticscholar.org/CorpusID: 80628296. 

- [26] Bhairav Mehta, Manfred Diaz, Florian Golemo, Christopher J Pal, and Liam Paull. Active domain randomization. In _Conference on Robot Learning_ , pages 1162–1176. PMLR, 2020. 

- [27] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. https://octo-models.github.io, 2023. 

- [28] OpenAI. Gpt-4 technical report, 2024. 

- [29] Lerrel Pinto and Abhinav Kumar Gupta. Supersizing self-supervision: Learning to grasp from 50k tries and 700 robot hours. _2016 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3406–3413, 2015. 

- [30] Haozhi Qi, Brent Yi, Sudharshan Suresh, Mike Lambeta, Yi Ma, Roberto Calandra, and Jitendra Malik. General in-hand object rotation with vision and touch. In _Conference on Robot Learning_ , pages 2549–2564. PMLR, 2023. 

- [31] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models, 2022. 

- [32] Dhruv Shah, Blazej Osinski, Brian Ichter, and Sergey Levine. Lm-nav: Robotic navigation with large pretrained models of language, vision, and action. In _Conference on Robot Learning_ , 2022. 

- [33] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Cliport: What and where pathways for robotic manipulation. In _Conference on Robot Learning_ , pages 894–906. PMLR, 2022. 

- [34] Xavier Soria, Yachuan Li, Mohammad Rouhani, and Angel D. Sappa. Tiny and efficient model for the edge detection generalization. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) Workshops_ , pages 1364–1373, October 2023. 

- [35] Gemini Team. Gemini: A family of highly capable multimodal models, 2024. 

- [36] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE, 2017. 

- [37] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale, 2024. 

      - Chang Zhou. One-peace: Exploring one general representation model toward unlimited modalities, 2023. 

   - [39] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan Song, Jiazheng Xu, Bin Xu, Juanzi Li, Yuxiao Dong, Ming Ding, and Jie Tang. Cogvlm: Visual expert for pretrained language models, 2024. 

   - [40] Yufei Wang, Zhou Xian, Feng Chen, Tsun-Hsuan Wang, Yian Wang, Katerina Fragkiadaki, Zackory Erickson, David Held, and Chuang Gan. Robogen: Towards unleashing infinite data for automated robot learning via generative simulation. _arXiv preprint arXiv:2311.01455_ , 2023. 

   - [41] Erroll Wood, Tadas Baltruˇsaitis, Charlie Hewitt, Sebastian Dziadzio, Thomas J Cashman, and Jamie Shotton. Fake it till you make it: face analysis in the wild using synthetic data alone. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 3681–3691, 2021. 

   - [42] Jianwei Yang, Hao Zhang, Feng Li, Xueyan Zou, Chunyuan Li, and Jianfeng Gao. Set-of-mark prompting unleashes extraordinary visual grounding in gpt-4v. _arXiv preprint arXiv:2310.11441_ , 2023. 

   - [43] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 

   - [44] Tianhe Yu, Ted Xiao, Austin Stone, Jonathan Tompson, Anthony Brohan, Su Wang, Jaspiar Singh, Clayton Tan, Meredith Dee, Jodilyn Peralta, Brian Ichter, Karol Hausman, and F. Xia. Scaling robot learning with semantically imagined experience. _ArXiv_ , abs/2302.11550, 2023. 

   - [45] Aohan Zeng, Mingdao Liu, Rui Lu, Bowen Wang, Xiao Liu, Yuxiao Dong, and Jie Tang. Agenttuning: Enabling generalized agent abilities for llms, 2023. 

   - [46] Yuexiang Zhai, Hao Bai, Zipeng Lin, Jiayi Pan, Shengbang Tong, Yifei Zhou, Alane Suhr, Saining Xie, Yann LeCun, Yi Ma, and Sergey Levine. Fine-tuning large vision-language models as decision-making agents via reinforcement learning, 2024. 

   - [47] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models, 2023. 

   - [48] Yuxuan Zhang, Huan Ling, Jun Gao, Kangxue Yin, Jean-Francois Lafleche, Adela Barriuso, Antonio Torralba, and Sanja Fidler. Datasetgan: Efficient labeled data factory with minimal human effort. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 10145–10155, 2021. 

   - [49] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing visionlanguage understanding with advanced large language models, 2023. 

- [38] Peng Wang, Shijie Wang, Junyang Lin, Shuai Bai, Xiaohuan Zhou, Jingren Zhou, Xinggang Wang, and 

