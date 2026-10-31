---
title: "Object-Centric Prompt-Driven Vision-Language-Action Model for Robotic Manipulation"
date: "2025"
venue: "CVPR 2025"
url: https://openaccess.thecvf.com/content/CVPR2025/html/Li_Object-Centric_Prompt-Driven_Vision-Language-Action_Model_for_Robotic_Manipulation_CVPR_2025_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2025/papers/Li_Object-Centric_Prompt-Driven_Vision-Language-Action_Model_for_Robotic_Manipulation_CVPR_2025_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2025/papers/Li_Object-Centric_Prompt-Driven_Vision-Language-Action_Model_for_Robotic_Manipulation_CVPR_2025_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2025/html/Li_Object-Centric_Prompt-Driven_Vision-Language-Action_Model_for_Robotic_Manipulation_CVPR_2025_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Object-Centric Prompt-Driven Vision-Language-Action Model for Robotic Manipulation** 

Xiaoqi Li<sup>1,2</sup> , Jingyun Xu<sup>1</sup> , Mingxu Zhang<sup>1</sup> , Jiaming Liu<sup>1</sup> , Yan Shen<sup>1,2</sup> , Iaroslav Ponomarenko<sup>1,2</sup> , Jiahui Xu<sup>1</sup> , Liang Heng<sup>1,2</sup> , Siyuan Huang<sup>1</sup> , Shanghang Zhang<sup>1</sup> , Hao Dong<sup>1,2∗</sup> 1School of Computer Science, Peking University 2 PKU-Agibot Lab 

## **Abstract** 

_In robotic, task goals can be conveyed through various modalities, such as language, goal images, and goal videos. However, natural language can be ambiguous, while images or videos may offer overly detailed specifications. To tackle these challenges, we introduce CrayonRobo that leverages comprehensive multi-modal prompts that explicitly convey both low-level actions and high-level planning in a simple manner. Specifically, for each key-frame in the task sequence, our method allows for manual or automatic generation of simple and expressive 2D visual prompts overlaid on RGB images. These prompts represent the required task goals, such as the end-effector pose and the desired movement direction after contact. We develop a training strategy that enables the model to interpret these visual-language prompts and predict the corresponding contact poses and movement directions in SE(3) space. Furthermore, by sequentially executing all key-frame steps, the model can complete long-horizon tasks. This approach not only helps the model explicitly understand the task objectives but also enhances its robustness on unseen tasks by providing easily interpretable prompts. We evaluate our method in both simulated and real-world environments, demonstrating its robust manipulation capabilities._ 

## **1. Introduction** 

As thoughtful helpers for humans, it is crucial for robots to understand and successfully execute their assigned tasks. Various approaches exist to convey the goals that robots should achieve, such as language descriptions, goal images, or goal videos. Language instructions [2, 23, 24, 31, 33, 38, 41, 45, 46, 56] can be ambiguous and brief, making it challenging for the robot to understand the tasks, or they can be overly detailed, increasing the difficulty for the model to follow. Goal images [6, 7, 25, 39, 61], while providing an accurate target, often contain extraneous informa- 

> ∗Corresponding author. First author’s email: xl3062@columbia.edu. 

tion irrelevant to the task, such as background elements and non-interactive objects. Some methods use human demonstration videos [10] or generated videos [6, 13, 14, 57] to outline tasks step-by-step. However, human demonstration videos are burdensome to encode, and generated videos depend heavily on their quality. To address these challenges, several works propose using visual prompts as a convenient yet expressive modality for goal specification. These visual prompts are easy for users to create and can effectively convey the precise goals that the policy model should focus on. 

Among visual prompt-conditioned approaches, methods [20, 32, 42, 47, 59] have attempted to convey task goals more effectively. The RT-Sketch [49] method emphasizes drawing the target state of the most relevant object to represent the goal. However, it only depicts the final state and overlooks the intermediate key frames that are crucial for successful task execution. In contrast, RT-Trajectory [20] (Figure1.(c)) illustrates the entire movement path of the endeffector, which helps bridge the gap between task components and enhances generalization. Despite its advantages, they provide only positional information and neglect the action directional information, which is also critical for accurate task completion. Additionally, as trajectories become longer and overlap between key-frames, they can create confusion for the model regarding overall task planning. 

This leads us to consider: _is there any way to precisely and non-redundantly convey the goal while also clearly communicating the end-effector’s action?_ Since key-frames represent important or bottleneck steps of the gripper during the task execution [18, 19, 26, 46, 58], we propose **_CrayonRobo_** , an approach that automatically generates or draws crayonstyle visual prompts on images to effectively represent both low-level actions and high-level planning within key-frame sequences. As illustrated in Figure 1(a), these prompts can include contact point, end-effector z-axis direction, endeffector y-axis direction, and next moving direction after contact, conveying the objective of where and how to interact with the object. We further develop a training strategy and supervision objectives aimed at progressively enhancing 

27638 


Figure 1. (a) shows our expression of different color prompts. (b) shows that we utilize a sequence of images with crayon visual prompts to express the key-frame steps, with each step illustrating the required low-level task goals, _i.e._ , t1-pick, t2-place. Based on the input goal prompt, the model determines the 6 DoF contact pose, enabling it to interact with the object as required. When a yellow prompt is presented, the model also predicts 3D movement directions, guiding the movement after contact, _e.g._ , picking upward in t1. For simple steps, such as t2-place, there is no need to present the post-contact moving direction. By sequentially executing each step in the key-frame sequence, the overall task is completed. (c) shows its differences with RT-trajectory [9] 

the model’s ability to comprehend each type of prompt. This allows the model to predict the corresponding SE(3) contact pose and the 3D next movement direction after contact, facilitating the completion of each sub-goal task. Furthermore, as illustrated in Figure 1(b), we use key-frame sequences as input to express the task planning procedure, with each image presented with crayon visual prompts indicating its key-frame task goal. We leverage the predicted 3D movement direction to connect each step sequentially, completing the overall long-horizon task. This approach enables us to instruct the model’s task objectives while also enhancing its robustness when encountering novel tasks by providing model-understandable prompts. 

Our experimental setup includes a diverse range of manipulation tasks, both familiar and novel, where our method achieves a promising success rate in manipulation. Additional demonstrations are available at https://sites.google.com/view/crayonrobo. 

In summary, our contributions are as follows: 

- 1) We propose employing a sequence of key-frames presented with prompts to explicitly convey the task objectives in both low-level action and high-level planning. 

- 2) We train a model that comprehends the visual-language prompts and predicts accurate contact poses along with moving directions in SE(3) space, ensuring the reliable completion of each key-frame task and the connection between steps to formulate a long-horizon task. 

- 3) Experiments at scale demonstrate its promising performance and robustness. 

## **2. Related Work** 

**Pure Vision-based Manipulation.** In vision-based robotic manipulation, numerous studies have employed a variety of solutions, including deep learning [8, 9, 18, 46], imitation learning [11, 27, 28, 60], and reinforcement learning [3, 12, 37, 43]. For example, in deep learning-based solutions, some methods design action policy networks [4, 15, 40, 52, 55] to calculate dense affordance maps and determine contact points and action poses. However, pure vision-based manipulation networks focus more on actionability than functionality, potentially failing when functional actions are required to meet human needs. 

**Language-conditioned Manipulation.** With advancements in language foundation models, language instructions are increasingly used for goal specification in goalconditioned policy learning, as seen in [8]. Other works, such as [2, 23, 31, 33, 38, 41, 45, 46, 54, 56], utilize templated or freeform language for task specification. Building on this, Belkhale et al. [5] introduces language motions as an intermediate layer between high-level goals and low-level actions. Despite progress, challenges remain: language instructions often struggle to specify detailed actions or convey spatial objectives, frequently requiring human assistance to work effectively. 

**Goal Image or Video-conditioned Manipulation.** To enhance goal specificity and detail, several image-conditioned policy representations have been developed, with goalimage conditioning being one of the most prominent techniques. In goal-image conditioning, a final goal image defines the desired end state of a task [6, 7, 25, 39, 61]. This approach inputs both the initial and target states of the ob- 

27639 

ject and outputs the actions needed to achieve the goal. In addition to static images, some methods use video or generated video [6, 13, 14, 57] to represent each step of the process frame by frame, offering a more detailed execution procedure. However, both solutions encode excessive information, much of which may be irrelevant to the task, such as background details or unrelated objects. 

**Visual Prompt-conditioned Manipulation.** To address the issue of redundant goal information, recent approaches have proposed using visual prompts as goals. Sundaresan et al. [49] suggests using goal sketches to indicate the target of the task-involved object, while Gu et al. [20] proposes drawing moving trajectories with key waypoints to specify the desired movement of the end-effector. Additionally, Nasiriany et al. [42] introduces a method that iteratively selects waypoints from a pool of potential options to form the overall trajectory, and Liu et al. [34], Stone et al. [47], Yang et al. [56] use external models to choose waypoints based on mark-based visual prompts to complete tasks. 

Different from them, we propose an innovative solution that allows manual drawing or automatic generating 2D prompts to represent both low-level action and high-level planning goals. This approach clearly conveys the objective of each key-frame step, _i.e._ , where and how to interact with the object, as well as the required task-planning procedure. 

## **3. Method** 

### 3.1. Problem Formulation 

The task is defined as follows: the model takes the visual input 퐼 ∈ R<sup>퐻×푊×3</sup> of an object presented with crayon visual prompts. This prompt utilizes four colors: blue, representing the contact point; red and green, indicating the z-axis and y-axis directions of the end-effector when contacting the object; and yellow, symbolizing the next moving direction after contacting. To eliminate ambiguities caused by visual prompts overlapping each other, we specify their numerical values in text inputs as a language prompt 푃, including the coordinates of the contact point denoted as 푎0<sup>푝∈R2,the</sup> gripper’s 2D z-axis direction 푎0<sup>푧and y-axis direction 푎</sup> 0<sup>푦, and</sup> the 2D moving direction 푎0<sup>푚,allrepresentedasunitvec-</sup> tors in R<sup>2</sup> . The objective of the model is to generate an action 푎0 = (푎0<sup>푝′, 푎</sup> 0<sup>푍, 푎푌</sup> 0<sup>, 푎</sup> 0<sup>푀),where푎</sup> 0<sup>푝′</sup> is mapped into 3D position 푎0<sup>푃usingthedepthinformationandcamera</sup> parameters, while 푎0<sup>푍,푎푌</sup> 0<sup>,and푎</sup> 0<sup>푀</sup> are unit vectors in R<sup>3</sup> representing the end-effector’s 3D z-axis, y-axis, and moving directions, respectively. 푎0<sup>푍and푎푌</sup> 0<sup>jointlydetermine</sup> the rotation for contacting the object, while 푎0<sup>푀controls the</sup> following movement after contact. Note that, the prediected 푎0<sup>푝′can be different from the 푎</sup> 0<sup>푝in the text prompt input due</sup> to potential input noise. 

### 3.2. Data Collection 

In this section, we elaborate on how to obtain the 2D prompt required for training. In the simulator, building upon some effective rule-based heuristic approaches [31, 40], we interact with objects and record the success contact pose of the end-effector including 3D contact point, z-axis direction 푎0<sup>푍′,and y-axisdirection푎푌</sup> 0<sup>′alongwiththe movingdirec-</sup> tion 푎0<sup>푀′</sup> of the object contact point. These are then served as ground-truth to guide the training. As for the input prompt, 3D contact point is unprojected onto a 2D image as 푎0<sup>푝=(푥, 푦).We then adopt 3D contact</sup> point as the center and locate other 3D points along 푎0<sup>푍′and</sup> 푎<sup>푌</sup> 0<sup>′.These points are then unprojected onto the 2D image.</sup> Subsequently, we connect these points with 푎0<sup>푝to calculate</sup> 2D vectors 푎0<sup>푧and푎</sup> 0<sup>푦,whileobtainingredandgreenlines</sup> respectively. We obtain the yellow moving direction line and obtain the 2D moving direction vector 푎0<sup>푚inthesame</sup> way utilizing 푎0<sup>푀′.Thesearethenservedasinformation</sup> embedded in the input language prompt. The corresponding visual prompts are generated by overlaying these elements in their respective colors onto the images. 

### 3.3. Training Strategy 

#### 3.3.1. Model Architecture 

Given both the visual and language prompts, we require the model to effectively interpret inputs from both modalities. Observing the robust language understanding and visual processing capabilities of Vision Language Action Models (VLAs) and inspired by their applications in prior robotic manipulation tasks [29–31, 35], we follow the backbone architecture of an open-source VLA model [31] and adopt its parameter updating strategy which only finetunes the injected adapters [21] within LLaMa [51], alongside the multi-modal projection module, while keeping the primary parameters frozen. This approach aims to preserve the inherent existing pre-trained knowledge, particularly in simto-real transfer, while enhancing the model’s ability to comprehend visual prompts and perform robotic manipulation in an efficient training time. Specifically, when presented with an RGB image containing visual prompts 퐼, we employ CLIP’s visual encoder [44] to extract visual features. Simultaneously, text prompts 푃 are encoded into text features using LLaMa’s pre-trained tokenizer [51]. The alignment of visual and text feature representations is achieved through the multi-modal projection module. 

#### 3.3.2. Policy Learning 

**Input pairs:** To help the model better understand the meaning of various prompts, we design a series of visual-textual input pairs that progressively convey different levels of information. This gradual progression enables the model to develop a deeper understanding of the physical significance 

27640 


Figure 2. We design training pairs that convey varying levels of information to enable the model to comprehend each type of prompt and introduce loss functions to guide it in predicting accurate poses. 

of each component. Specifically, as illustrated in (a)-(d) in Figure 2 input. We formulate the problem of pose prediction as a language modeling task, directly outputting 3D directions in textual form. Thus, we generate the ground-truth text as shown in Figure 2 to guide the training. The entire language description is shown in Appendix.1. 

**Training objectives:** Our model’s objective is to accurately predict 3D pose based on 2D visual-language prompts given different object and camera views. Therefore, we introduce the following losses to guide the policy training: 

_Text Supervision Loss_ L푇 _:_ This loss ensures the effective alignment of the model’s visual and linguistic input, making sure it can output the correct output pattern. We formulate pose prediction as a classification task by discretizing the continuous numbers in the normalized 3D direction vector into 100 discrete bins [-50,50], with each bin spanning 0.02, and adopt cross-entropy loss to supervise. 

_Orthogonal Loss_ L푂 _:_ The orthogonality of a rotation matrix necessitates that its components maintain orthogonal relationships between each pair of directions. However, formulating direction prediction as language predictions for 푎0<sup>푍and 푎푌</sup> 0<sup>does not explicitly consider their geometric rela-</sup> tion. To address this, we extract 푎0<sup>푍and 푎푌</sup> 0<sup>from the model’s</sup> output text and ensure their orthogonal relationship under Gram-Schmidt loss [17]. 

_Projection Loss_ L푃 _:_ 3D directional predictions should align with their corresponding 2D directional prompts when unprojected back to the 2D plane. To establish an explicit connection between the input 2D directional prompt and the output 3D directions, we introduce a projection loss designed to guide their correlation. Specifically, in the model’s output, we extract the contact point 푎0<sup>푃andmapitto3D</sup> space using the depth map and camera parameters. Subse- 

quently, leveraging the predicted 3D direction in the z-axis 푎0<sup>푍,welocate3Dpointsalongthedirectionwiththecon-</sup> tact point as the center. The 3D point are then unprojected back onto the 2D plane, and connecting with 푎0<sup>푃to generate</sup> predicted 2D directional vectors 푎0<sup>푧∗.We employ a similar</sup> approach to acquire 푎0<sup>푦∗and 푎</sup> 0<sup>푚∗, which are then supervised</sup> based on the 2D directional prompts 푎0<sup>푧,푎</sup> 0<sup>푦,and푎</sup> 0<sup>푚using</sup> cosine similarity loss , where · denotes the dot product: 


Note that, L푇 and L푂 are consistent across all input pairs, but L푃 varies based on the input prompts. For example, in Input(c) of Figure. 2 where does not include the 푎0<sup>푚,</sup> we will exclude the supervision for 푎0<sup>푚and푎</sup> 0<sup>푚∗</sup> in L푃. After completing the training process, the model, having been trained with dynamic input patterns, can understand each type of prompt and predict the required actions based on the provided prompts. The aforementioned losses are trained simultaneously under the total objective function: L = 휆1 ∗L푇 +휆2 ∗L푂+휆3 ∗L푃. 

### 3.4. Inference and Interaction 

#### 3.4.1. Model Inference 

During the inference stage, we provide both automated and manual drawing approach to extract these visual prompts, as illustrated in Figure 3(i) and (ii). For automatic generation approach, we first use Grounded-DINO [36] to detect the object’s bounding box and select its center, forming the blue circle. Then, we automatically generate 32 uniformly sampled 2D directional lines around the full 360-degree circle with the blue circle as the center or as the middle. 

27641 


Figure 3. Illustration of model inference with input generated in different ways. 

GPT-4 [1] is then prompted to select lines from all candidates to represent the gripper’s z-axis direction, y-axis direction, and moving direction, resulting in the red, green, and yellow lines, respectively. As shown in Figure 3(ii), for manual drawing approach, we allow users to draw crayon visual prompts on the image, which then serve as the visual input. 

The contact pose is always required, while whether the movement direction after contact is needed depending on the task characteristics. Specifically, Goyal et al. [18, 19], Johns [26], Shridhar et al. [46], Yuan et al. [58] observe that longhorizon tasks usually can be decomposed into several keyframe tasks. Meanwhile, different key-frame tasks exhibit distinct motion patterns: some require a specific moving direction to guide the subsequent movement after contact, while others end when executing contact pose. For example, _pick_ action requires moving along 푎0<sup>푀,which usually indi-</sup> cates an upward movement. Similarly, _pushing_ and _pulling_ actions require the robot to determine the direction in which to push or pull. In contrast, certain primitives, such as _place_ and _move_ , are simple motions that do not require additional movement after approaching the object. For example, given a pick-and-place task, once the object is picked up, the “preplace” pose is already established. Once the object is placed according to the contact pose prompt, the task is considered complete. Therefore, there is no need to draw a moving prompt for these primitives. For actions like _rotate_ , such as rotating a button, the movement typically does not involve translating the position after contact. Instead, it focuses on rotating the last joint. As a result, 푎0<sup>푚, which specifies trans-</sup> lation, is not needed. Instead, we provide two key-frames as prompts: one depicting the end effector pose at the moment of contact and the other after the rotation. From these 

two temporal prompts, the required rotation direction becomes evident. More visual details are demonstrated in the Appendix.4. After generating the visual prompt image, we automatically extract the coordinates of the contact point and the direction vectors based on the pixel RGB values and then incorporate them into the language prompt. Given the visual and language input, the model outputs the predicted action 푎0. 

Note that although 2D directions may overlap, the model does not require them to originate from the same point, as long as the direction is accurate and clearly visible in the image, the model can interpret it. Additionally, if the direction vector is perpendicular to the camera, it may be challenging to represent it as a 2D projection. In such cases, adding slight noise to the direction vector can enhance its visibility. Since the model is trained to interpret such situations, it can handle similar scenarios during inference, where the direction may be perpendicular to the camera. 

#### 3.4.2. Interaction Strategy 

We illustrate how we enable the robot to interact with objects given the predicted action 푎0. Same with other VLA models [22, 31, 35], 푎0<sup>푝is projected into 3D space utilizing</sup> depth information and camera parameters. The 푎0<sup>푍and푎푌</sup> 0 jointly contribute to determining the rotation matrix of the end-effector, facilitating the establishment of initial contact with the object. If provided with 푎0<sup>푚,wethenfollowthe</sup> predicted moving direction 푎0<sup>푀to determine the subsequent</sup> movements after contact. 

For the long-horizon tasks, we leverage a sequence of keyframes with visual prompts to serve as high-level planning, with each frame representing a sub-goal step. By executing 

27642 

the key-frame steps sequentially, we can complete the longhorizon tasks. The benefit of this approach revolves around breaking down the complexity of long-horizon tasks and allowing us to optimize the success rate of each key-frame step to ensure the overall task’s success. Meanwhile, regarding each key-frame step as compositions, we can group them into arbitrary combinations, enabling the model to handle diverse manipulation tasks. 

## **4. Experiment** 

In our experiments, we mainly focus on exploring the following questions: 

- Section 4.3.1: What is the effect of different types of prompts on model performance? 

- Section 4.3.2: How does the model handle noise in the input prompt, and is it user-friendly? 

- Section 4.4: Can the model perform specific tasks without prompts, given certain input distributions? 

### 4.1. Setup Details 

**Data Collection.** Following previous work [31, 40], we utilize SAPIEN [53] along with the PartNet-Mobility dataset to construct an environment, interacting with about 1500 object shapes under various camera view randomization. The tasks involve several actions that require changes in both translation and rotation, _e.g._ , pull the drawer, open the door, open the laptop lid, etc. The setup uses the flying Franka Panda Gripper for both the training and testing stages. We follow the procedure in Section 3.2 to collect prompts within the simulator, which takes about 6-8 hours to collect about 10,000 training samples. Details of the training and testing dataset split and camera view randomization can be found in Appendix.2. 

**Evaluation Metric.** We utilize the manipulation success rate to assess the effectiveness of the manipulation, calculated as the ratio of successfully manipulated samples to the total number of test samples. A successful sample is defined using a binary criterion, with success determined by thresholding the distance that the object part moves. 

### 4.2. Comparisons with Baselines 

To ensure fairness in comparison, all methods adhere to the same train and test split. 

_Pure vision model_ Flowbot3D [15]: It predicts motion direction on the point cloud, denoting it as _flow_ . The point with the largest flow magnitude serves as the interaction point, while the direction of the flow represents the endeffector’s orientation and moving direction. 

_Language conditioned model_ ManipLLM [31]: It takes the task description and the object’s initial image, and then outputs the end-effector pose. We use its predicted contact point and rotation to contact with the object and adopt its active adaptation policy for moving. 

_Vision Goal conditioned 3D model_ Implicit3D [61]: It develops a manipulation policy that utilizes the transporter to detect key-points for 3D objects. By providing the initial and target state point cloud of the object, key points are then used to determine the end-effector pose for manipulation. 

The above three methods use suction gripper as the endeffector, which is compared with ours(s) in Table. 1 

_Visual prompt conditioned model_ RT-trajectory [20]: Since the RT-Trajectory code is not publicly available at the time of this paper’s submission, we replicate its method for comparisons with implementation details in Appendix.3. 

_Goal video conditioned model_ AVDC [57]: The generative model is trained on our training split. During testing, we employ Gemini-1.5 [50] to evaluate the quality of the generated videos by assessing whether they successfully complete the given tasks, _e.g.,_ open the door. The ratio of successfully generated tasks is 10.2%. Given that the performance of the generative video-based execution policy is highly dependent on the quality of the generated videos, we believe this score can somehow reflect its overall effectiveness during the following execution. 

In Table 1, both Ours(s) and Ours(f) demonstrate a substantial performance advantage over the baselines with manual generated prompts. For automatically generated prompts, the results are 0.64/0.62 on seen and unseen tasks, still outperforming the baselines. It is important to note that by selecting the center of the bounding box generated by GroundingDiNO as the contact point input, there may be misalignment with the actual contact point, introducing noise into the positional prompt. However, our results demonstrate the robustness of CrayonRobo in handling such input inaccuracies. This is because the model is trained to manipulate objects, it can, to some extent, correct the noise in the prompts. Simulator visualizations are shown in the left of Figure 4, illustrating the prompt input, the robot’s contact state with the object, and the final state after movement. We further conduct experiments involving tasks with multiple steps, such as pulling a door and subsequently pushing it. Our method results in satisfactory performance: 0.69 and 0.68 on seen and unseen tasks, showing its potential in handling long-horizon tasks. 

### 4.3. Ablation Study 

#### 4.3.1. Analysis on The Effect of Different Types of Prompt 

In Table 2 Ex1-Ex3, since our model is able to handle various input patterns thanks to the proposed training strategy, we progressively introduce each type of prompt during testing. When no 푎0<sup>푚is provided, we use rule-based approach [40] to</sup> determine the movement after contact. Beginning with Ex1, where only a 2D position prompt is provided, the model achieves impressive performance with scores of 0.42/0.37. We compare our results with using AnyGrasp [16] to pre- 

27643 

|||**Se**|**en Ta**|**sks**||
|---|---|---|---|---|---|
|Method||||||
|Flowbot<br>0.76 **0.86** 0.08|0.67 0.26 0.05|0.58 0.29|0.71|0.35 0.07 0.23 0.40 0.63|0.52 0.04|
|ManipLLM<br>0.68 0.64 0.36|0.77 0.26 0.62|0.65 0.61|0.38|0.52 0.53 0.40 0.64 0.71|0.83 0.64|
|Implicit3D<br>0.53 0.58 0.35|0.55 0.30 **0.66**|0.58 0.51|0.31|0.41 0.45 0.34 0.69 0.54|0.31 0.43|
|Ours(s)<br>**0.89**<br>0.85<br>**0.67**|**0.91**<br>**0.87**<br>0.50|**0.92**<br>**0.85**|**0.87**|**0.85**<br>**0.54**<br>**0.84**<br>**0.85**<br>**0.92**|**0.85**<br>**0.75**|
|RT-Traj<br>0.56 0.58 0.28|0.45 0.56 **0.50**|0.65 0.42|0.29|0.56 0.40 0.49 0.46 0.53|0.52 0.27|
|Ours(f)<br>**0.71**<br>**0.79**<br>**0.58**|**0.81**<br>**0.79**<br>0.43|**0.81**<br>**0.81**|**0.75**|**0.78**<br>**0.50**<br>**0.75**<br>**0.76**<br>**0.79**|**0.81**<br>**0.73**|
||**Seen Tasks**|||**Unseen Tasks**||
|Method|||**AVG**||**AVG**|
|Flowbot<br>0.18 0.10 0.39|0.10 0.10 0.61|0.34 0.19|0.43|0.12 0.60 0.21 0.51 0.10|0.22 0.38|
|ManipLLM<br>0.41 0.75 0.44|0.67 0.38 0.22|0.81 **0.86**|0.51|0.38 0.85 0.42 0.60 0.43|**0.65** 0.47|
|Implicit3D<br>0.27 0.65 0.20|0.33 0.45 0.17|0.80 0.53|0.55|0.15 0.41 0.57 0.39 0.28|0.52 0.39|
|Ours(s)<br>**0.65**<br>**0.90**<br>**0.78**|**0.79**<br>**0.68**<br>**0.91**|**0.94**<br>0.46|**0.80**|**0.47**<br>**0.88**<br>**0.83**<br>**0.70**<br>**0.76**|0.63<br>**0.79**|
|RT-Traj<br>0.32 0.46 0.40|0.31 0.37 0.68|0.58 **0.47**|0.57|0.25 0.39 0.48 0.57 0.13|0.59 0.52|
|Ours(f)<br>**0.63**<br>**0.67**<br>**0.48**|**0.78**<br>**0.67**<br>**0.74**|**0.83**<br>0.44|**0.74**|**0.46**<br>**0.88**<br>**0.82**<br>**0.63**<br>**0.61**|**0.61**<br>**0.72**|


Table 1. Comparison of our method against baseline methods. (s) and (f) denote suction gripper and finger gripper, respectively. Bold text indicates the highest score within each end-effector type. 


Figure 4. Visualization results in SAPIEN simulator and real world. 

||푎<sup>푝</sup><br>0|푎<sup>푧</sup><br>0|푎<sup>푦</sup><br>0|푎<sup>푚</sup><br>0|Seen|Unseen|
|---|---|---|---|---|---|---|
|Ex1|✓|-|-|-|0.42|0.37|
|Ex2|✓|✓|-|-|0.55|0.50|
|Ex3|✓|✓|✓|-|0.70|0.68|
|Ours|✓|✓|✓|✓|0.74|0.72|
|Ours(w/o v.)|✓|✓|✓|✓|0.69|0.68|


Table 2. Ablation Study. 

dict rotation given the same pixel coordinate, which results in lower scores of 0.35/0.31. This shows even without directional prompts, our model can accurately predict 3D poses, showcasing its ability to comprehend objects and predict appropriate poses based on positional prompts. Moreover, comparing Ex2 and Ex3, we observe that by introducing more prompts during testing, the model achieves more ac- 

#### curate predictions. 

Additionally, to investigate the differential effects of visual and language prompts, in the last row of Table 2, we enable the model to learn from images capturing only the object (without visual prompt), along with language containing instructional prompts. This configuration results in a performance drop compared to inputting prompts from both modalities. The reduced performance can be attributed to the difficulty the model has in effectively linking the given language prompt to the relevant objects. Consequently, it becomes challenging to make accurate object-centric manipulation predictions when relying solely on language prompts. We thus conclude that prompts from both modalities work together to enhance the model’s understanding and improve its pose prediction capabilities. 

27644 


Figure 5. Robustness analysis on the noise in prompts. 

||Open the|Open|Lift|Wipe|Heat|
|---|---|---|---|---|---|
||trashcan|microwave*|lid|table*|toaster*|
|dra.|9/10|7/10|5/5|8/10|3/5|
|auto.|8/10|6/10|5/5|8/10|2/5|
|w/o P.|-|5/10|-|6/10|-|


Table 3. Real-world success rate. * contains multiple steps. 

#### 4.3.2. Tolerance Analysis of Prompt Noise 

We further introduce noise into the 2D directional prompt during testing while maintaining the accurate 2D contact point, in order to evaluate the model’s tolerance to input disturbances. Random noise with a uniform distribution is added to the directional prompt, ranging from 10%, 20%, 30%, to 40% of the original directional value. The results, shown in Figure 5, indicate that with 10% and 20% noise, our method achieves performance levels comparable to those of the noise-free scenario. This demonstrates the model’s ability to handle noisy inputs during testing. However, with 30% and 40% noise, performance degradation occurs as the directional values deviate significantly from their intended targets—deviations that would be unlikely to happen if drawn by a human, as they appear visibly unreasonable. Despite this, the model is still capable of successfully executing tasks, even when the directional inputs are imperfect or provided by a non-expert. This highlights the model’s resilience, not only to noise but also to imperfect or nonideal inputs, allowing it to perform effectively even when the prompts are not perfectly accurate. 

Ablation experiments regarding the effectiveness of each loss and failure case analysis are shown in Appendix.5 and Appendix.6. 

### 4.4. Real-world Experiment 

We conduct experiments involving interaction with various real-world objects without additional sim-to-real finetuning. Our setup includes a Franka Emika robotic arm equipped with its default parallel gripper, along with a RealSense 415 camera for capturing RGB images and depth maps. In our real-world experiment, we employ the workstation’s built-in 

image editor to directly draw crayon visual prompts on the images or automatic generating prompts, denoted as “dra.” and “auto.” in Table. 3 . We subsequently extract 2D vectors from the visual prompt, forming the text input. For each task, we select one or two shapes of objects and perform five trials each with a different camera view angle and object’s initial pose. If the task has been completed, we consider the execution successful. To avoid a collision, we introduce a “pre-move” waypoint before reaching the predicted contact pose. This waypoint is positioned along the end-effector’s z-axis, at a distance away from the predicted contact pose. Qualitative and quantitative results are presented in Table. 3 and the right part of Figure. 4. The results demonstrate that CrayonRobo possesses strong zero-shot capability on novel tasks, as it interprets task execution prompts rather than relying solely on images or language processing, which can be challenging to handle in novel scenarios. Meanwhile, it exhibits strong capability in long-horizon tasks, achieving a success rate comparable to that of single-step tasks. 

In the “w/o P.” row of Table. 3, we further explore whether it is possible to fine-tune the model using prompts provided during the first set of executions for a specific task, and enable the model to perform subsequent executions independently, without requiring additional prompts. To investigate this, we selected two multi-step tasks: opening the microwave and wiping the table. The model is finetuned for 20 epochs using key frames and the corresponding predicted 3D poses from successful trials in the previous experiment as ground truth (GT), without providing any visual or text prompt inputs. During fine-tuning, the image input includes only the object, while the language input excludes all 2D prompts but incorporates the current robot state to ensure temporal consistency. The output format remains consistent with Figure 2. The fine-tuned model is then evaluated on these tasks, achieving success rates of 5/10 and 6/10, respectively. 

## **5. Conclusion** 

We introduce a novel approach using comprehensive multimodal prompts that explicitly convey both low-level actions and high-level planning in a simple manner. We devise a training strategy that enables the model to comprehend the 2D visual-language prompt and predict accurate contact pose along with moving direction, ensuring the reliability of task execution. Such model-interpretable prompts show promising performance on both seen and unseen tasks, demonstrating its robustness. _Limitation:_ As for the limitation, though our method can not directly avoid obstacles, we can incorporate collision-free motion planner library like curobo [48] to realize this to some extent. 

27645 

## **Acknowledge** 

This project was supported by National Youth Talent Support Program (8200800081) and National Natural Science Foundation of China (62376006). 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 5 

- [2] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 1, 2 

- [3] Boshi An, Yiran Geng, Kai Chen, Xiaoqi Li, Qi Dou, and Hao Dong. Rgbmanip: Monocular image-based robotic manipulation through active object pose estimation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7748–7755. IEEE, 2024. 2 

- [4] Shikhar Bahl, Russell Mendonca, Lili Chen, Unnat Jain, and Deepak Pathak. Affordances from human videos as a versatile representation for robotics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13778–13790, 2023. 2 

- [5] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. _arXiv preprint arXiv:2403.01823_ , 2024. 2 

- [6] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zeroshot robotic manipulation with pretrained image-editing diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 1, 2, 3 

- [7] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Akhil Raju, et al. Robocat: A selfimproving foundation agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ , 2023. 1, 2 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 2 

- [10] Elliot Chane-Sane, Cordelia Schmid, and Ivan Laptev. Learning video-conditioned policies for unseen manipulation tasks. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 909–916. IEEE, 2023. 1 

- [11] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffu- 

sion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 2 

- [12] Josef Dai, Xuehai Pan, Ruiyang Sun, Jiaming Ji, Xinbo Xu, Mickel Liu, Yizhou Wang, and Yaodong Yang. Safe rlhf: Safe reinforcement learning from human feedback. _arXiv preprint arXiv:2310.12773_ , 2023. 2 

- [13] Yilun Du, Mengjiao Yang, Pete Florence, Fei Xia, Ayzaan Wahid, Brian Ichter, Pierre Sermanet, Tianhe Yu, Pieter Abbeel, Joshua B Tenenbaum, et al. Video language planning. _arXiv preprint arXiv:2310.10625_ , 2023. 1, 3 

- [14] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in Neural Information Processing Systems_ , 36, 2024. 1, 3 

- [15] Ben Eisner, Harry Zhang, and David Held. Flowbot3d: Learning 3d articulation flow to manipulate articulated objects. _arXiv preprint arXiv:2205.04382_ , 2022. 2, 6 

- [16] Hao-Shu Fang, Chenxi Wang, Hongjie Fang, Minghao Gou, Jirong Liu, Hengxu Yan, Wenhai Liu, Yichen Xie, and Cewu Lu. Anygrasp: Robust and efficient grasp perception in spatial and temporal domains. _IEEE Transactions on Robotics_ , 2023. 6 

- [17] Luc Giraud, Julien Langou, and Miroslav Rozloznik. The loss of orthogonality in the gram-schmidt orthogonalization process. _Computers & Mathematics with Applications_ , 50 (7):1069–1075, 2005. 4 

- [18] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. In _Conference on Robot Learning_ , pages 694– 710. PMLR, 2023. 1, 2, 5 

- [19] Ankit Goyal, Valts Blukis, Jie Xu, Yijie Guo, Yu-Wei Chao, and Dieter Fox. Rvt-2: Learning precise manipulation from few demonstrations. _arXiv preprint arXiv:2406.08545_ , 2024. 1, 5 

- [20] Jiayuan Gu, Sean Kirmani, Paul Wohlhart, Yao Lu, Montserrat Gonzalez Arenas, Kanishka Rao, Wenhao Yu, Chuyuan Fu, Keerthana Gopalakrishnan, Zhuo Xu, et al. Rt-trajectory: Robotic task generalization via hindsight trajectory sketches. _arXiv preprint arXiv:2311.01977_ , 2023. 1, 3, 6 

- [21] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 3 

- [22] Siyuan Huang, Haonan Chang, Yuhan Liu, Yimeng Zhu, Hao Dong, Peng Gao, Abdeslam Boularias, and Hongsheng Li. A3vlm: Actionable articulation-aware vision language model. _arXiv preprint arXiv:2406.07549_ , 2024. 5 

- [23] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 1, 2 

- [24] Yueru Jia, Jiaming Liu, Sixiang Chen, Chenyang Gu, Zhilue Wang, Longzan Luo, Lily Lee, Pengwei Wang, Zhongyuan Wang, Renrui Zhang, et al. Lift3d foundation policy: Lifting 2d large-scale pretrained models for robust 3d robotic manipulation. _arXiv preprint arXiv:2411.18623_ , 2024. 1 

27646 

- [25] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. Vima: General robot manipulation with multimodal prompts. _arXiv preprint arXiv:2210.03094_ , 2(3):6, 2022. 1, 2 

- [26] Edward Johns. Coarse-to-fine imitation learning: Robot manipulation from a single demonstration. In _2021 IEEE international conference on robotics and automation (ICRA)_ , pages 4613–4619. IEEE, 2021. 1, 5 

- [27] Yuanchen Ju, Kaizhe Hu, Guowei Zhang, Gu Zhang, Mingrun Jiang, and Huazhe Xu. Robo-abc: Affordance generalization beyond categories via semantic correspondence for robot manipulation. _arXiv preprint arXiv:2401.07487_ , 2024. 2 

- [28] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina Fragkiadaki. 3d diffuser actor: Policy diffusion with 3d scene representations. _arXiv preprint arXiv:2402.10885_ , 2024. 2 

- [29] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 3 

- [30] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- [31] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18061–18070, 2024. 1, 2, 3, 5, 6 

- [32] Yi Li, Yuquan Deng, Jesse Zhang, Joel Jang, Marius Memme, Raymond Yu, Caelan Reed Garrett, Fabio Ramos, Dieter Fox, Anqi Li, et al. Hamster: Hierarchical action models for openworld robot manipulation. _arXiv preprint arXiv:2502.05485_ , 2025. 1 

- [33] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9493–9500. IEEE, 2023. 1, 2 

- [34] Fangchen Liu, Kuan Fang, Pieter Abbeel, and Sergey Levine. Moka: Open-vocabulary robotic manipulation through markbased visual prompting. _arXiv preprint arXiv:2403.03174_ , 2024. 3 

- [35] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv preprint arXiv:2406.04339_ , 2024. 3, 5 

- [36] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. _arXiv preprint arXiv:2303.05499_ , 2023. 4 

- [37] Jianlan Luo, Zheyuan Hu, Charles Xu, You Liang Tan, Jacob Berg, Archit Sharma, Stefan Schaal, Chelsea Finn, Abhishek Gupta, and Sergey Levine. Serl: A software suite for sample-efficient robotic reinforcement learning. _arXiv preprint arXiv:2401.16013_ , 2024. 2 

- [38] Corey Lynch and Pierre Sermanet. Language conditioned imitation learning over unstructured data. _arXiv preprint arXiv:2005.07648_ , 2020. 1, 2 

- [39] Corey Lynch, Mohi Khansari, Ted Xiao, Vikash Kumar, Jonathan Tompson, Sergey Levine, and Pierre Sermanet. Learning latent plans from play. In _Conference on robot learning_ , pages 1113–1132. PMLR, 2020. 1, 2 

- [40] Kaichun Mo, Leonidas J Guibas, Mustafa Mukadam, Abhinav Gupta, and Shubham Tulsiani. Where2act: From pixels to actions for articulated 3d objects. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6813–6823, 2021. 2, 3, 6 

- [41] Suraj Nair, Eric Mitchell, Kevin Chen, Silvio Savarese, Chelsea Finn, et al. Learning language-conditioned robot behavior from offline data and crowd-sourced annotation. In _Conference on Robot Learning_ , pages 1303–1315. PMLR, 2022. 1, 2 

- [42] Soroush Nasiriany, Fei Xia, Wenhao Yu, Ted Xiao, Jacky Liang, Ishita Dasgupta, Annie Xie, Danny Driess, Ayzaan Wahid, Zhuo Xu, et al. Pivot: Iterative visual prompting elicits actionable knowledge for vlms. _arXiv preprint arXiv:2402.07872_ , 2024. 1, 3 

- [43] Hai Nguyen and Hung La. Review of deep reinforcement learning for robot manipulation. In _2019 Third IEEE international conference on robotic computing (IRC)_ , pages 590–595. IEEE, 2019. 2 

- [44] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 3 

- [45] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Cliport: What and where pathways for robotic manipulation. In _Conference on robot learning_ , pages 894–906. PMLR, 2022. 1, 2 

- [46] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , pages 785–799. PMLR, 2023. 1, 2, 5 

- [47] Austin Stone, Ted Xiao, Yao Lu, Keerthana Gopalakrishnan, Kuang-Huei Lee, Quan Vuong, Paul Wohlhart, Sean Kirmani, Brianna Zitkovich, Fei Xia, et al. Open-world object manipulation using pre-trained vision-language models. _arXiv preprint arXiv:2303.00905_ , 2023. 1, 3 

- [48] Balakumar Sundaralingam, Siva Kumar Sastry Hari, Adam Fishman, Caelan Garrett, Karl Van Wyk, Valts Blukis, Alexander Millane, Helen Oleynikova, Ankur Handa, Fabio Ramos, et al. Curobo: Parallelized collision-free robot motion generation. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8112–8119. IEEE, 2023. 8 

27647 

- [49] Priya Sundaresan, Quan Vuong, Jiayuan Gu, Peng Xu, Ted Xiao, Sean Kirmani, Tianhe Yu, Michael Stark, Ajinkya Jain, Karol Hausman, et al. Rt-sketch: Goal-conditioned imitation learning from hand-drawn sketches. 2023. 1, 3 

- [50] Gemini Team, Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 6 

- [51] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 3 

- [52] Chuan Wen, Xingyu Lin, John So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ , 2023. 2 

- [53] Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, He Wang, Li Yi, Angel X. Chang, Leonidas J. Guibas, and Hao Su. SAPIEN: A simulated part-based interactive environment. In _The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2020. 6 

- [54] Ted Xiao, Harris Chan, Pierre Sermanet, Ayzaan Wahid, Anthony Brohan, Karol Hausman, Sergey Levine, and Jonathan Tompson. Robotic skill acquisition via instruction augmentation with vision-language models. _arXiv preprint arXiv:2211.11736_ , 2022. 2 

- [55] Zhenjia Xu, Zhanpeng He, and Shuran Song. Universal manipulation policy network for articulated objects. _IEEE Robotics and Automation Letters_ , 7(2):2447–2454, 2022. 2 

- [56] Jiange Yang, Wenhui Tan, Chuhao Jin, Bei Liu, Jianlong Fu, Ruihua Song, and Limin Wang. Pave the way to grasp anything: Transferring foundation models for universal pickplace robots. _arXiv preprint arXiv:2306.05716_ , 2023. 1, 2, 

   - 3 

- [57] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 1, 3, 6 

- [58] Wentao Yuan, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. M2t2: Multi-task masked transformer for object-centric pick and place. In _7th Annual Conference on Robot Learning_ , 2023. 1, 5 

- [59] Wentao Yuan, Jiafei Duan, Valts Blukis, Wilbert Pumacay, Ranjay Krishna, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. Robopoint: A vision-language model for spatial affordance prediction for robotics. _arXiv preprint arXiv:2406.10721_ , 2024. 1 

- [60] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy. _arXiv preprint arXiv:2403.03954_ , 2024. 2 

- [61] Chengliang Zhong, Yuhang Zheng, Yupeng Zheng, Hao Zhao, Li Yi, Xiaodong Mu, Ling Wang, Pengfei Li, Guyue Zhou, Chao Yang, et al. 3d implicit transporter for temporally consistent keypoint discovery. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 3869–3880, 2023. 1, 2, 6 

27648 

