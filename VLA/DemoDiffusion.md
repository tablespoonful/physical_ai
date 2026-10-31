---
title: "DemoDiffusion: One-Shot Human Imitation Using Pre-Trained Diffusion Policy"
date: "2026"
venue: "ICRA 2026"
url: https://doi.org/10.1109/ICRA57385.2026.11696851
pdf: https://arxiv.org/pdf/2506.20668
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.20668)** / [論文ページ](https://doi.org/10.1109/ICRA57385.2026.11696851)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **_DemoDiffusion_ : One-Shot Human Imitation using pre-trained Diffusion Policy** 

Sungjae Park, Homanga Bharadhwaj, Shubham Tulsiani Carnegie Mellon University 


Fig. 1: **Overview of** **_DemoDiffusion_ .** We show how _generalist_ pre-trained diffusion policies can be used for following a generic human demonstration showing a manipulation task during deployment. Our real-world manipulation results encompass a wide diversity of manipulation tasks involving everyday objects. 

**_Abstract_ — We propose** **_DemoDiffusion_ , a simple method for enabling robots to perform manipulation tasks by imitating a single human demonstration, without requiring task-specific training or paired human-robot data. Our approach is based on two insights. First, the hand motion in a human demonstration provides a useful prior for the robot’s end-effector trajectory, which we can convert into a rough open-loop robot motion trajectory via kinematic retargeting. Second, while this retargeted motion captures the overall structure of the task, it may not align well with plausible robot actions in-context. To address this, we leverage a pre-trained** **_generalist_ diffusion policy to modify the trajectory, ensuring it both follows the human motion and remains within the distribution of plausible robot actions. Unlike approaches based on online reinforcement learning or paired human-robot data, our method enables robust adaptation to new tasks and scenes with minimal effort. In real-world experiments across 8 diverse manipulation tasks, DemoDiffusion achieves 83.8% average success rate, compared to 13.8% for the pre-trained policy and 52.5% for kinematic retargeting, succeeding even on tasks where the pre-trained** **_generalist_ policy fails entirely. Project page: https://demodiffusion.github.io/** 

## I. INTRODUCTION 

How do we build robot manipulation systems that can be readily deployed in unstructured human environments? One possible answer is to learn ‘generalist’ policies that are capable of accomplishing any generic task (specified via some description _e.g._ language or image goal) in any environment. Indeed, there is a general optimism about this paradigm, 

reflected in several ongoing efforts to collect large-scale demonstration datasets to train such policies. While these efforts have produced unified policies capable of diverse tasks [1]–[5], these policies still struggle to perform meaningfully when deployed zero-shot to novel environments or asked to perform unseen tasks. Deployment thus often requires additional fine-tuning using task-and-scene-specific robot demonstrations [1], but this is a non-trivial overhead as collecting robot demonstrations in the real world can be time-consuming and beyond the expertise of an average user. In this work, we propose an alternate deployment mechanism – leveraging a pre-trained generalist policy to perform a task via imitating a single _human_ demonstration. 

We are of course not the first to consider this goal of allowing robots to imitate any given human demonstration. One common approach [6]–[9] is to instantiate this as a kinematic retargeting task and compute open-loop robot actions that maximize a manually defined similarity between the achieved robot end-effector configuration and observed human hand poses ( _e.g._ matching locations of fingertips). However, the human-robot embodiment mismatch makes it difficult for the retargeted actions to achieve precisely the same effects as the human ones, and the open-loop execution further makes the approach brittle to noise and scene variations. Another line of work for human imitation attempts to learn robot policies through online reinforcement learning [10]–[14], where the human demonstration helps define reward functions. While 

this can overcome the embodiment gap, such test-time online RL requires hours of online interaction and resets, making it difficult to adopt for generic real-world manipulation tasks, especially in safety-critical scenarios. We seek an approach that, like kinematic retargeting, can be deployed one-shot ( _i.e._ without test-time training), but still benefits from learned priors for precise closed-loop interaction. 

Our approach builds on the insight that pre-trained diffusion policies can act as priors for robot action. Inspired by prior work in leveraging pre-trained diffusion models for image editing [15], we present _DemoDiffusion_ – a formulation to utilize a diffusion policy trained on robot interaction data for synthesizing coherent robot actions from a human demonstration. Specifically, we first perform kinematic retargeting by extracting human hand poses from the demonstration and obtain an open-loop robot action trajectory. While this trajectory is typically suboptimal due to embodiment differences and lack of closed-loop feedback, it serves as an effective initialization that can be improved via a diffusion policy. We do so by injecting Gaussian noise and applying the pre-trained diffusion policy to iteratively denoise the trajectory conditioned on robot observations, yielding a refined, executable sequence of robot actions. _DemoDiffusion_ thus enables the robot to use the pre-trained policy as a prior and adapt the human-derived trajectory to its own embodiment and environment in a closed-loop manner. 

In summary, we propose _DemoDiffusion_ : a framework for robotic manipulation that allows a robot to perform generic tasks in natural environments by following a human demonstration with guidance from a pre-trained diffusion policy. Importantly, our framework doesn’t require any robot demonstration of the target task within the target environment, online interaction, or fine-tuning. Our experiments across simulation and real-world environments show that _DemoDiffusion_ surpasses both the base policy and retargeted trajectory, achieving 83.8% success across 8 real-world tasks – even those where the pre-trained _generalist_ policy fails entirely. 

## II. RELATED WORK 

**_Generalist_ Manipulation Policies.** There has been a growing trend in developing ‘ _generalist_ ’ robotic policies that can perform multiple tasks based on a specified goal in the form of an image or a language instruction. Collecting largescale robot interaction datasets [16], [17] combined with behavior cloning and vision-language pre-training [1]–[5], [18], [19] is the predominant recipe for training such multitask policies. However, since collecting large-scale robot interaction datasets in natural settings like homes and offices is challenging due to operational constraints, current best models still struggle to perform manipulation tasks zeroshot and thus are not yet deployable in-the-wild. Our work enables using such _generalist_ diffusion policies for following a human demonstration, enabling it to perform tasks that the pre-trained policy struggles to zero-shot. 

**Robotic Manipulation with Non-Robot Datasets.** Instead of requiring large-scale robot interaction datasets, 

a growing body of works have begun utilizing human videos and large-scale web videos for robotics. These approaches have been enabled by recent advances in computer vision for representation learning [20]–[22], predicting tracks [23], [24], and reconstructing hand-object interactions from monocular videos [25]–[28], [28]. Earlier works learned self-supervised visual representations from such nonrobotic datasets [29]–[31], which can serve as the visual backbone of robotic policies [32]–[37]. Recent works in this paradigm predict manipulation-relevant cues from web videos in the form of motion trajectories [38]–[40] and object affordances [41]–[44] and combine these predictive models with a limited amount of robot interaction data for training policies via conditional behavior cloning. Our work is orthogonal to these approaches in that instead of using human videos for training, we require a single human demonstration during deployment for guiding a pre-trained generalist policy to perform a new task. 

**One-Shot Imitation from Robot Demonstration.** Oneshot imitation aims to enable robots to perform a new task with guidance from a single demonstration. Prior works have explored this in the context of a robot demonstration provided at test time, via training demonstration-conditioned policies [45]. Recent works have developed learning-based visual servoing systems [46] and algorithms for identifying object invariances [47] to replicate the robot end-effector actions from the demonstration onto novel configurations of objects. However, requiring a robot demonstration for imitation is restrictive for ubiquitous deployment as endusers might find it challenging to tele-operate the robot to collect demonstrations in natural human environments. 

**One-Shot Imitation from Human Demonstration.** To imitate a human demonstration for robot manipulation, a straightforward approach is kinematic retargeting of the human hand pose to the robot end-effector pose per timestep, as demonstrated by some recent works [6], [7], [48]. Although simple to implement, the human-robot embodiment mismatch typically introduces errors in the retargeting and the open-loop execution is brittle to object pose variations during deployment. To remedy this, another line of works seek to learn this retargeting implicitly by training a closedloop policy from paired human-robot datasets [49], [50] enabling more flexible deployments. Since such paired datasets are difficult to collect, other works [10]–[12], [51] perform reinforcement learning with reward functions derived from video comparison. However, such methods require online interaction and resets, limiting their practicality. We propose an alternate paradigm: given the human demonstration, we refine retargeted human behavior using a pre-trained robot policy, avoiding brittle replays and enabling closed-loop control. This formulation avoids both expensive paired humanrobot data collection and cumbersome test-time fine-tuning via interaction. 

## III. METHOD 

We target the problem of one-shot visual imitation. Given a human demonstration **D** depicting a manipulation task with 


Fig. 2: **Retargeted human hand trajectory to closed-loop robot action sequence, for the task** _T_ **:** **_“shut down the laptop”_** . The dotted line shows the trajectory of robot end-effector poses after kinematic retargeting. The olive contour plot depicts the distribution of trajectories from a pre-trained diffusion policy. Given a kinematic retargeting, we first perturb it with Gaussian noise and progressively remove the noise by simulating the reverse SDE with the diffusion policy. This process gradually projects a potentially unfeasible but approximately correct retargeting to the manifold of plausible robot actions that can perform real-world manipulation, in this case closing the laptop without missing the edge. 

description _T_ , we want a robot manipulator to perform the same task. Unlike prior work that relies on test-time RL training [10] or paired human-robot datasets [49], we wish to enable such imitation ‘one-shot’ assuming access to a closed-loop diffusion policy _π_ ¯ _θ_ ( **a** _t |_ **o** _≤t , T_ ) pre-trained on some broad robot interaction dataset _Drobot_ . Our assumption on the human demonstration **D** is also very minimal: it can either be an RGBD video or a multi-view video of a human doing a task, such that 3D hand poses per-timestep can be reliably extracted from it. 

## _A. Overview_ 

Our approach is based on two insights. The first is that the trajectory of the hand pose in the human demonstration **D** provides useful information of the approximate trajectory the robot end-effector should follow, and we can perform _kinematic retargeting_ of the hand trajectory _{_ **h** _t }t_<sup>_T_</sup> =0<sup>toan</sup> open-loop robot end-effector trajectory _{_ **a** ˆ _t }t_<sup>_T_</sup> =0<sup>.Thesecond</sup> insight is that the kinematically retargeted robot trajectory has the correct form of motion, but these actions may not be very precise in the distribution of plausible robot actions given the current observation. A diffusion policy models this likelihood, and we can use a pre-trained ‘ _generalist_ ’ diffusion policy _π_ ¯ _θ_ ( **a** _t |_ **o** _≤t , T_ ) to refine the retargeted robot actions in a closed loop manner, thus inferring actions that, while still similar to the human demonstration, are more likely under the policy and better aligned with the robot embodiment (see 

Fig. 2). We describe both these steps in detail below. 

_B. Kinematic retargeting of Human Hand Trajectories to Robot End-Effector Poses_ 

Given a human demonstration **D** of a manipulation task _T_ , our first step is to extract the 3D hand pose trajectory _{_ **h** _t }t_<sup>_T_</sup> =0<sup>.Eachhandpose</sup><sup>**h**</sup><sup>_t∈_R3</sup><sup>_×J_correspondstothe3D</sup> locations of _J_ keypoints (e.g., wrist and fingertips), which we estimate using a pre-trained monocular hand pose estimator applied to each video frame [52]. These keypoints encode the motion of the human performing the task and form the basis for retargeting to a robotic end-effector. 

To translate this human motion into a robot-executable trajectory, we define a simple geometric mapping function _f_ retarget : R<sup>3</sup><sup>_×J_</sup> _→_ R<sup>6</sup> that converts the human hand pose **h** _t_ into a robot configuration **a** ˆ _t_ = _f_ retarget( **h** _t_ ). The mapping aligns the wrist pose of the human to the robot end-effector pose. For a two-finger gripper, we use the distance between the thumb and the remaining fingers of the hand mesh to infer a binary robot grasp, and for a dexterous robotic hand we match the robot hand’s fingertip positions to those of a human hand using inverse kinematics. We set the initial configuration of the robot as the kinematically retargeted initial configuration from the human demonstration. 

This kinematic retargeting procedure yields a full trajectory _{_ **a** ˆ _t }t_<sup>_T_</sup> =0<sup>in the robot’s configuration space, which can be</sup> executed as an open-loop policy. However, due to differences 


Fig. 3: **Dexterous Grasping Results in Simulation.** (Left) A human demonstration and _DemoDiffusion_ rollout for dexterous grasping. (Right) Success rates (mean _±_ std over 3 seeds) as a function of diffusion step _s_<sup>_∗_</sup> . Here, _s_<sup>_∗_</sup> _/S_ = 0 corresponds to kinematic retargeting and _s_<sup>_∗_</sup> _/S_ = 1 corresponds to the robot policy. 

in morphology and embodiment between humans and robots, the absence of environment feedback, and the inaccuracy of the hand estimation module, this trajectory often leads to suboptimal or unstable behavior during open-loop execution. We thus treat this as the basis for searching for a plausible robot action trajectory via denoising with a (pre-trained) closed-loop diffusion policy. 

_C. Closed-Loop Denoising of Robot Actions with a PreTrained Diffusion Policy_ 

A diffusion policy _π_ ¯ _θ_ ( **a** _t |_ **o** _≤t , T_ ) [53], [54] pre-trained on diverse offline robot interaction data reliably models the distribution of plausible robot actions **a** _t_ given previous observations **o** _≤t_ . To predict actions **a** _t_ , diffusion policies start with Gaussian noise **a** ˜ _t_<sup>(</sup><sup>_S_)</sup> _∼_ **N** (0 _, I_ ) and iteratively denoise it at different diffusion steps _s_ : 


We use this to modify the kinematically retargeted trajectory _{_ **a** ˆ _t }t_<sup>_T_</sup> =0<sup>forobtainingrobotactionsthatfollowthe</sup> high-level motion in the human trajectory and still lie within the distribution of plausible actions under _π_ ¯ _θ_ . To do this, we modify this typical reverse diffusion process so that instead of starting with pure noise **a** ˜ _t_<sup>(</sup><sup>_S_)</sup> at step _S_ , we start from an intermediate diffusion step _s_<sup>_∗_</sup> such that 0 _< s_<sup>_∗_</sup> _< S_ . We define _{_ **a** ˜ _t_<sup>(</sup><sup>_s∗_)</sup> _}t_<sup>_T_</sup> =0<sup>tobeanoisyversionofthekinematically</sup> retargeted trajectory as follows: 


Here _α_ corresponds to the diffusion schedule of the pretrained policy. This procedure, inspired by SDEdit [15] which adopted a similar approach for image editing, relies on the assumption that _{_ **a** ˆ _t }t_<sup>_T_</sup> =0<sup>is an approximate version of the</sup> ideal action trajectory that should be executed by the robot, and it potentially lies outside the distribution of feasible actions under the pre-trained diffusion policy _π_ ¯ _θ_ . Intuitively, adding moderate noise to the retargeted trajectory and then 

|**Group**|Robot Policy|Kinematic|**_DemoDiffusion_**|
|---|---|---|---|
|_Small_|25.4|2.6|**31.8**|
|_Medium_|26.6|0.7|**31.6**|
|_Large_|27.4|1.5|**29.6**|
|**Average**|26.5|1.6|**31.0**|


TABLE I: **Simulated Dexterous Grasping Results.** The numbers show the average of success rates over 3 seeds. We use _s_<sup>_∗_</sup> _/S_ = 0 _._ 2, where the robot policy uses _S_ = 1000. _DemoDiffusion_ consistently outperforms both baselines, across all groups. 

denoising preserves the high-level structure of the human demonstration while allowing the policy to correct low-level infeasibilities from the embodiment gap. The diffusion policy _π_ ¯ _θ_ then performs iterative denoising steps, conditioned on the robot’s observations _o≤t_ , to refine this noisy trajectory into feasible robot actions, based on equation (2). 

After _s_<sup>_∗_</sup> denoising steps, the final output **a** _t_ = **a** ˜ _t_<sup>(0)</sup> is deployed on the robot. Importantly, this process is carried out in a closed-loop manner: the policy uses real-time observations from the cameras in the scene to iteratively improve its predictions, thereby compensating for embodiment mismatch and external perturbations (e.g., object slippage or occlusion). The key hyperparameter in this process for _DemoDiffusion_ is the diffusion step _s_<sup>_∗_</sup> that trades off between the faithfulness to the demonstration and the likelihood under the robot policy – in the limit _s_<sup>_∗_</sup> = _S_ we recover a rollout from the base policy _π_ ¯ _θ_ and in the limit _s_<sup>_∗_</sup> = 0 we recover the kinematically retargeted trajectory _{_ **a** ˆ _t }t_<sup>_T_</sup> =0<sup>. While</sup> derived in the context of diffusion, note that this iterative refinement perspective also applies to flow-matching [55], which we show in real-world experiments. 

## IV. EXPERIMENTS 

We evaluate our approach on dexterous grasping in simulation and across diverse real-world tasks comprising prehensile and non-prehensile table-top manipulation. Through 


Fig. 4: **Real-World Manipulation Tasks.** Human demonstrations for the 8 evaluation tasks, shown as two frames per task. Tasks span prehensile and non-prehensile manipulation, including grasping, pushing, closing, wiping, and placing. 

experiments, we aim to understand the following research questions: 

- Can _DemoDiffusion_ outperform pure kinematic retargeting from the human demonstration? 

- Do the human demonstrations allow _DemoDiffusion_ to perform new tasks where the pre-trained diffusion policy fails? 

- How to effectively tradeoff between faithfulness to the human demonstration and performing the task reliably, with varying noise level _s_<sup>_∗_</sup> _/S_ ? 

- How robust is _DemoDiffusion_ to noise in human demonstration, or different kinematic retargeting? 

## _A. Dexterous Grasping in Simulation_ 

To verify our intuition, we first consider a simulation environment where the target task is restricted to picking up a generic object with a 16-DOF four-fingered Allegro hand. Specifically, we train a dexterous grasping policy across a small set of generic objects in simulation, and test our method on human hand grasping trajectories on a different set of objects. This serves as the pre-trained diffusion model for this experiment. 

For training the robot policy, we collect a total of 985 grasping trajectories of Allegro hand over 58 training objects [56] (randomly sampled 26 and 32 objects from ShapeNet [57] and PartNet [58], respectively), resulting in 22.2% success rate. We use a variant of 3D Diffusion Policy [59], which takes 3D point tracks of an object instead of point clouds. At test time, we provide human grasping trajectories on a subset of Objaverse dataset [60], which are unseen during training. The test set contains 1220 objects, with 1 human grasping trajectory per object, provided by GraspXL [56]. Note that there is no error from hand estimation or the initial configuration of the object in this setup. We use ground-truth human hand 3D keypoints, and the object is located at the same location as the human demonstration. 

**Results.** As in GraspXL [56], we group the objects based on their size, resulting in small, medium, and large objects. We compare _DemoDiffusion_ with two baselines. The first is open-loop kinematic retargeting obtained from the human demonstration. The second is directly deploying the robot policy we trained. 


Fig. 5: **Workspace with 5 Cameras.** We use the four external cameras for triangulation to obtain the global pose of the hand mesh from a human demonstration. The pretrained policy uses the two cameras marked in purple. 

Table I shows the main results. Our method outperforms baselines, with the largest gains on small objects. We hypothesize this is because larger objects are easier to grasp, supported by base robot policy performance improving for larger objects. This experiment shows that even in a highly controlled setup where the robot environment is initialized identically to that of human demonstration, kinematic retargeting cannot solve the task, while slightly refining with a generalist grasping policy significantly improves the performance. Using kinematic retargeting to initiate the denoising process also helps the denoising process itself, outperforming the robot policy. Additionally, _DemoDiffusion_ achieves higher inference speed, by the factor of _S/s_<sup>_∗_</sup> . 

**Ablation studies.** We analyze the influence of _s_<sup>_∗_</sup> on _DemoDiffusion_ in Fig. 3. Overall, we observe a consistent trend of performance gain from _s_<sup>_∗_</sup> _/S_ = 1 to _s_<sup>_∗_</sup> _/S_ = 0 _._ 2, showing that _DemoDiffusion_ is robust to the choice of hyperparameter. 

## _B. Real-World Manipulation_ 

For the real-world experiments, we use a Franka Emika Panda arm equipped with a two-finger gripper from Robotiq. We use the publicly available pre-trained flow-matching policy _π_ ¯ _θ_ ( **a** _t |_ **o** _≤t , T_ ) called Pi-0 released by Physical In- 

|**Task**|Pi-0|Kinematic|**_DemoDiffusion_**|
|---|---|---|---|
|Shut Down Laptop|20|10|**60**|
|Close Microwave|10|80|**90**|
|Drag Basket|10|**80**|**80**|
|Wipe Table|50|0|**100**|
|Iron Curtain|20|70|**90**|
|Pick up Bear|0|40|**60**|
|Pick Place Bowl|0|70|**100**|
|Pick Place Banana|0|70|**90**|
|**Average**|13.8|52.5|**83.8**|


TABLE II: **Quantitative Results for Real-World Manipulation.** Success rates (%) are over 10 trials per task. 

telligence [1], trained on the DROID dataset [61]. This policy takes as input a language task specification _T_ , and observations from two cameras in the scene, and outputs per-timestep joint velocity. This policy was trained on a large offline dataset of tele-operated robot demonstrations, and is a _generalist_ policy that can perform a broad set of tasks. We do not fine-tune or adapt this policy in any way and directly use it for _DemoDiffusion_ . We use an off-theshelf monocular hand reconstruction model, Hamer [52] to obtain per-timestep hand mesh reconstructions from each of the external cameras given a human demonstration in the scene. Our experiments follow the protocol of a human first demonstrating an object manipulation in the scene, followed by robot execution after re-setting the scene. 

**Workspace.** Fig. 5 describes our real-robot manipulation setup. The scene has 5 cameras including 4 Realsense external cameras and 1 Zed-Mini wrist camera mounted on the robot gripper. We calibrate the four external cameras and use them for triangulating the 3D hand pose so that we can obtain the position and orientation of a human hand in the world coordinates, with origin at the base of the robot. The pre-trained policy Pi-0 requires just two cameras (marked in purple) and the policy does not use any calibration information. While Pi-0 uses Zed 2 camera for external view, we use Realsense camera due to hardware availability, which introduces additional difficulty. 

**Tasks.** We perform evaluations for 8 different manipulation tasks, the language description and the human demonstration for which are described in Fig. 4. Each of these tasks requires a different manipulation strategy involving either prehensile or non-prehensile manipulation. We collect just a single human demonstration per task but for robot execution, we make organic variations in the location of objects in the scene. Additionally, we add other objects in the scene as visual distractors, to see whether _DemoDiffusion_ can generalize under such settings. All variations are consistent across the baselines and our method. 

**Baselines.** For the real-world experiments we compare _DemoDiffusion_ with two baselines. The first is openloop kinematic retargeting obtained from the human demonstration. The second is directly deploying the Pi-0 model with the language instruction for the respective task. Since Pi-0 operates in the joint velocity space, for _DemoDiffusion_ we 


Fig. 6: **Qualitative comparisons for real-robot manipulation.** Rollout progressions (start, intermediate, final frame) for two tasks. Kinematic retargeting (top) produces plausible motion but loses contact before completing the task. Pi-0 (middle) performs general reaching but fails to manipulate the correct object. _DemoDiffusion_ (bottom) reaches the object and maintains contact through task completion. See project page for full videos. 

||Shut Laptop<br>Pick|Place Banana|
|---|---|---|
|**_DemoDiffusion_**|60|90|
|+5cm noise|40|70|
|with Thumb+Index|30|80|
|Thumb+Index|0|30|


TABLE III: **Robustness of** **_DemoDiffusion_ .** We ablate _DemoDiffusion_ under noisy 3D keypoints (2nd row) and with different kinematic retargeting (3rd row). For noisy 3D keypoints, we randomly shift the tracked hand 3D keypoints by 5cm. For different kinematic retargeting, we use the distance between the thumb tip and the index fingertip instead of all fingers. 

first convert the kinematically retargeted trajectory to the joint velocity space with IK and then add noise to the trajectory, followed by denoising with Pi-0. We deploy _DemoDiffusion_ with a heuristically selected noise level _s_<sup>_∗_</sup> _/S_ depending on the task – preferring the kinematic trajectory with _s_<sup>_∗_</sup> _/S_ = 0 _._ 2 when Pi-0 has a zero success rate and _s_<sup>_∗_</sup> _/S_ = 0 _._ 4 otherwise. Note that in the limit of 0 noise added, we recover the first baseline, kinematic retargeting, and in the limit of maximum noise 1 we obtain the second baseline Pi-0. 

**Qualitative Visualizations.** In Fig. 6, we show rollouts for two tasks across all the methods. We observe that Pi-0 can only perform general reaching behaviors: it either fails to follow the manipulation trajectory needed for the task or confuses the target object with a distractor. On the other hand, we observe that (open-loop) kinematic retargeting from the human demonstration has a plausible motion of the robot end-effector, but it completely misses grasping the iron, and loses contact with the laptop before fully closing it. Compared to these, _DemoDiffusion_ reaches the respective object and also follows the approximate motion of the retargeted trajectory while remaining in contact with the object to solve the tasks. 

**Quantitative Comparisons.** In Table II, we compare _DemoDiffusion_ and the baselines across all the realworld manipulation tasks. _DemoDiffusion_ matches or outperforms both baselines across all 8 tasks, with the largest gains on tasks requiring precise contact – e.g., 60% vs. 10–20% on shutting the laptop and 100% vs. 0–50% on wiping the table. Notably, even for tasks where both baselines fail, _DemoDiffusion_ succeeds by operating at an intermediate noise level _s_<sup>_∗_</sup> that combines the trajectory structure from the human demonstration with the policy’s closed-loop refinement. 

**Noisy Human Demonstrations.** To evaluate the robustness of _DemoDiffusion_ to imperfect inputs, we injected noise into the tracked human trajectories and evaluated _DemoDiffusion_ . Specifically, we place the object at the same location as the human demonstration, and randomly shift the tracked hand 3D keypoints by 5cm. The results in Table III indicate that _DemoDiffusion_ maintains high-quality performance despite the presence of tracking noise, thereby reducing the reliance on highly accurate 3D annotations in human demonstration. 

**Different Kinematic Retargeting.** Lastly, we further assessed the sensitivity of our method to the choice of retargeting by evaluating an alternative approach (‘Thumb+Index’). Specifically, we use the distance between thumb and index finger [48], instead of all fingers, to infer the grasp. Table III shows the results. While this alternative retargeting itself shows degraded performance compared to the previous retargeting, _DemoDiffusion_ consistently improves task performance despite suboptimal retargeting. 

## V. DISCUSSION 

We presented _DemoDiffusion_ , a simple approach to leverage _generalist_ diffusion models for imitating a human demonstration. By retargeting hand motion from the human demonstration into an approximate robot end-effector trajectory and modifying it through de-noising with a pretrained diffusion policy, _DemoDiffusion_ enables the robot to produce actions that are both aligned with the demonstrated intent and contextually plausible. Our method consistently outperforms both the base diffusion policy and the raw retargeted trajectory across diverse tasks in simulation and the real world, without requiring additional training, paired demonstrations, or reward functions. We envision that this can serve as a starting point for future efforts at human imitation across generic scenarios and perhaps also yield an improved exploration strategy for methods pursuing policy adaptation with online RL. 

## LIMITATIONS 

Our approach has several limitations. First, it assumes that the robot should act similarly to the human to successfully complete the task, which may not hold in scenarios requiring different strategies due to embodiment or environmental constraints. Second, while effective for one-shot imitation (not requiring training / test-time fine-tuning), the method does not produce a reusable task policy that can generalize 

across arbitrary variations of the task. Third, the quality of the retargeted trajectory is crucial: accurate 3D human motion capture is challenging and errors in retargeting can impact downstream performance, though our method shows a degree of robustness to such noise. Additionally, the method implicitly assumes that the timing and speed of human and robot actions are aligned; extending the approach to allow for temporal alignment at test time is a promising direction of future work. 

## ACKNOWLEDGEMENTS 

We appreciate the helpful discussions with Yanbo Xu, Qitao Zhao, and Lucas Wu. We would also like to thank Kenny Shaw, Tony Tao, Jiahui Yang, Andrew Wang, Jason Liu, Hengkai Pan, Mohan Kumar Srirama, Peiyuan Yang for helping set up the hardware. This work was supported by gift awards from CISCO, Google, and NSF Award IIS-2442282. 

## REFERENCES 

- [1] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. In _RSS_ , 2025. 

- [2] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt2: Vision-language-action models transfer web knowledge to robotic control. In _CoRL_ , 2023. 

- [3] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _CoRL_ , 2022. 

- [4] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. In _CoRL_ , 2024. 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. In _RSS_ , 2023. 

- [6] Jinhan Li, Yifeng Zhu, Yuqi Xie, Zhenyu Jiang, Mingyo Seo, Georgios Pavlakos, and Yuke Zhu. Okami: Teaching humanoid robots manipulation skills through single video imitation. In _CoRL_ , 2024. 

- [7] Georgios Papagiannis, Norman Di Palo, Pietro Vitiello, and Edward Johns. R+ x: Retrieval and execution from everyday human videos. In _ICRA_ , 2025. 

- [8] Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and C Karen Liu. Dexcap: Scalable and portable mocap data collection system for dexterous manipulation. In _RSS_ , 2024. 

- [9] Sirui Chen, Chen Wang, Kaden Nguyen, Li Fei-Fei, and C Karen Liu. Arcap: Collecting high-quality human demonstrations for robot learning with augmented reality feedback. In _ICRA_ , 2025. 

- [10] Shikhar Bahl, Abhinav Gupta, and Deepak Pathak. Human-to-robot imitation in the wild. In _RSS_ , 2022. 

- [11] Irmak Guzey, Yinlong Dai, Georgy Savva, Raunaq Bhirangi, and Lerrel Pinto. Bridging the human to robot dexterity gap through objectoriented rewards. In _ICRA_ , 2025. 

- [12] Yuanpei Chen, Chen Wang, Yaodong Yang, and C Karen Liu. Objectcentric dexterous manipulation from human motion data. In _CoRL_ , 2024. 

- [13] Xueyi Liu, Jianibieke Adalibieke, Qianwei Han, Yuzhe Qin, and Li Yi. Dextrack: Towards generalizable neural tracking control for dexterous manipulation from human references. In _ICLR_ , 2025. 

- [14] Xueyi Liu, Kangbo Lyu, Jieqiong Zhang, Tao Du, and Li Yi. Quasisim: Parameterized quasi-physical simulators for dexterous manipulations transfer. In _ECCV_ , 2024. 

- [15] Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun Wu, Jun-Yan Zhu, and Stefano Ermon. Sdedit: Guided image synthesis and editing with stochastic differential equations. In _ICLR_ , 2022. 

- [16] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A robotic dataset for learning diverse skills in one-shot. In _ICRA_ , 2024. 

- [17] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _CoRL_ , 2023. 

- [18] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _ICRA_ , 2024. 

- [19] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _CoRL_ , 2025. 

- [20] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Doll´ar, and Ross Girshick. Masked autoencoders are scalable vision learners. In _CVPR_ , 2022. 

- [21] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. In _ICLR_ , 2021. 

- [22] Lingting Zhu, Guying Lin, Jinnan Chen, Xinjie Zhang, Zhenchao Jin, Zhao Wang, and Lequan Yu. Large images are gaussians: High-quality large image representation with levels of 2d gaussian splatting. In _AAAI_ , 2025. 

- [23] Nikita Karaev, Ignacio Rocco, Benjamin Graham, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker: It is better to track together. In _ECCV_ , 2024. 

- [24] Carl Doersch, Ankush Gupta, Larisa Markeeva, Adri`a Recasens, Lucas Smaira, Yusuf Aytar, Jo˜ao Carreira, Andrew Zisserman, and Yi Yang. Tap-vid: A benchmark for tracking any point in a video. In _NeurIPS_ , 2022. 

- [25] Yu Rong, Takaaki Shiratori, and Hanbyul Joo. Frankmocap: A monocular 3d whole-body pose estimation system via regression and integration. In _CVPR_ , 2021. 

- [26] Georgios Pavlakos, Dandan Shan, Ilija Radosavovic, Angjoo Kanazawa, David Fouhey, and Jitendra Malik. Reconstructing hands in 3d with transformers. In _CVPR_ , 2024. 

- [27] Yufei Ye, Abhinav Gupta, and Shubham Tulsiani. What’s in your hands? 3d reconstruction of generic objects in hands. In _CVPR_ , 2022. 

- [28] Yufei Ye, Poorvi Hebbar, Abhinav Gupta, and Shubham Tulsiani. Diffusion-guided reconstruction of everyday hand-object interaction clips. In _ICCV_ , 2023. 

- [29] Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Sanja Fidler, Antonino Furnari, Evangelos Kazakos, Davide Moltisanti, Jonathan Munro, Toby Perrett, Will Price, et al. Scaling egocentric vision: The epic-kitchens dataset. In _ECCV_ , 2018. 

- [30] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _CVPR_ , 2022. 

- [31] Kristen Grauman, Andrew Westbury, Lorenzo Torresani, Kris Kitani, Jitendra Malik, Triantafyllos Afouras, Kumar Ashutosh, Vijay Baiyya, Siddhant Bansal, Bikram Boote, et al. Ego-exo4d: Understanding skilled human activity from first-and third-person perspectives. In _CVPR_ , 2024. 

- [32] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. In _CoRL_ , 2022. 

- [33] Simone Parisi, Aravind Rajeswaran, Senthil Purushwalkam, and Abhinav Gupta. The unsurprising effectiveness of pre-trained vision models for control. In _ICML_ , 2022. 

- [34] Siddharth Karamcheti, Suraj Nair, Annie S Chen, Thomas Kollar, Chelsea Finn, Dorsa Sadigh, and Percy Liang. Language-driven representation learning for robotics. In _RSS_ , 2023. 

- [35] Tete Xiao, Ilija Radosavovic, Trevor Darrell, and Jitendra Malik. Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ , 2022. 

- [36] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. Vip: Towards universal visual reward and representation via value-implicit pre-training. In _ICLR_ , 2023. 

- [37] Yecheng Jason Ma, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. Liv: Language-image representations and rewards for robotic control. In _ICML_ , 2023. 

- [38] Homanga Bharadhwaj, Roozbeh Mottaghi, Abhinav Gupta, and Shubham Tulsiani. Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation. In _ECCV_ , 2024. 

- [39] Kenneth Shaw, Shikhar Bahl, and Deepak Pathak. Videodex: Learning dexterity from internet videos. In _CoRL_ , 2023. 

- [40] Tony Tao, Mohan Kumar Srirama, Jason Jingzhou Liu, Kenneth Shaw, and Deepak Pathak. Dexwild: Dexterous human interactions for inthe-wild robot policies. _arXiv preprint arXiv:2505.07813_ , 2025. 

- [41] Mohan Kumar Srirama, Sudeep Dasari, Shikhar Bahl, and Abhinav Gupta. Hrp: Human affordances for robotic pre-training. In _RSS_ , 2024. 

- [42] Shikhar Bahl, Russell Mendonca, Lili Chen, Unnat Jain, and Deepak Pathak. Affordances from human videos as a versatile representation for robotics. In _CVPR_ , 2023. 

- [43] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. In _RSS_ , 2023. 

- [44] Junyao Shi, Zhuolun Zhao, Tianyou Wang, Ian Pedroza, Amy Luo, Jie Wang, Jason Ma, and Dinesh Jayaraman. Zeromimic: Distilling robotic manipulation skills from web videos. In _ICRA_ , 2025. 

- [45] Sudeep Dasari and Abhinav Gupta. Transformers for one-shot visual imitation. In _CoRL_ , 2020. 

- [46] Eugene Valassakis, Georgios Papagiannis, Norman Di Palo, and Edward Johns. Demonstrate once, imitate immediately (dome): Learning visual servoing for one-shot imitation learning. In _IROS_ , 2022. 

- [47] Xinyu Zhang and Abdeslam Boularias. One-shot imitation learning with invariance matching for robotic manipulation. In _RSS_ , 2024. 

- [48] Marion Lepert, Jiaying Fang, and Jeannette Bohg. Phantom: Training robots without robots using only human videos. In _CoRL_ , 2025. 

- [49] Vidhi Jain, Maria Attarian, Nikhil J Joshi, Ayzaan Wahid, Danny Driess, Quan Vuong, Pannag R Sanketi, Pierre Sermanet, Stefan Welker, Christine Chan, et al. Vid2robot: End-to-end videoconditioned policy learning with cross-attention transformers. In _RSS_ , 2024. 

- [50] Sungjae Park, Seungho Lee, Mingi Choi, Jiye Lee, Jeonghwan Kim, Jisoo Kim, and Hanbyul Joo. Learning to transfer human hand skills for robot manipulations. _arXiv preprint arXiv:2501.04169_ , 2025. 

- [51] Tyler Ga Wei Lum, Olivia Y Lee, C Karen Liu, and Jeannette Bohg. Crossing the human-robot embodiment gap with sim-to-real rl using one human demonstration. _arXiv preprint arXiv:2504.12609_ , 2025. 

- [52] Georgios Pavlakos, Dandan Shan, Ilija Radosavovic, Angjoo Kanazawa, David Fouhey, and Jitendra Malik. Reconstructing hands in 3d with transformers. In _CVPR_ , 2024. 

- [53] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _IJRR_ , 2023. 

- [54] Moritz Reuss, Maximilian Li, Xiaogang Jia, and Rudolf Lioutikov. Goal conditioned imitation learning using score-based diffusion policies. In _RSS_ , 2023. 

- [55] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. In _ICLR_ , 2023. 

- [56] Hui Zhang, Sammy Christen, Zicong Fan, Otmar Hilliges, and Jie Song. Graspxl: Generating grasping motions for diverse objects at scale. In _ECCV_ , 2024. 

- [57] Angel X Chang, Thomas Funkhouser, Leonidas Guibas, Pat Hanrahan, Qixing Huang, Zimo Li, Silvio Savarese, Manolis Savva, Shuran Song, Hao Su, et al. Shapenet: An information-rich 3d model repository. _arXiv preprint arXiv:1512.03012_ , 2015. 

- [58] Kaichun Mo, Shilin Zhu, Angel X Chang, Li Yi, Subarna Tripathi, Leonidas J Guibas, and Hao Su. Partnet: A large-scale benchmark for fine-grained and hierarchical part-level 3d object understanding. In _CVPR_ , 2019. 

- [59] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _RSS_ , 2024. 

- [60] Matt Deitke, Dustin Schwenk, Jordi Salvador, Luca Weihs, Oscar Michel, Eli VanderBilt, Ludwig Schmidt, Kiana Ehsani, Aniruddha Kembhavi, and Ali Farhadi. Objaverse: A universe of annotated 3d objects. In _CVPR_ , 2023. 

- [61] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In _RSS_ , 2024. 

- [62] Javier Romero, Dimitrios Tzionas, and Michael J Black. Embodied hands: Modeling and capturing hands and bodies together. In _Transcations on Graphics_ , 2017. 

## APPENDIX 

We provide additional experimental details, implementation details, and results for the real-world and simulation experiments. 

## REAL-WORLD MANIPULATION 

## _A. Hardware Setup_ 

We replicate DROID [61] setup for the hardware setup. Due to hardware availability, we use RealSense D455 instead of ZED 2 for the rear view camera. 

## _B. Task Setup Description_ 

The overview of scenes for each task at test time is shown in Fig. 7. During data collection, we mark the target object location with a tape. During evaluation, we randomize the target object location within the tape, which is consistent across all methods. Overall, kinematic retargeting may fail due to small misalignment of object placement, inaccurate 3D hand keypoints, or camera extrinsics, etc. Pi-0 may fail if it cannot identify the object to interact with and manipulate other objects in the scene. It may also reach the target object but fail to manipulate in the desired way. Note that previous approaches [6]–[9] use kinematic retargeting to transfer human demonstration to the robot. 

**Pick and Place the Banana.** The task is to pick up the toy banana and place on the plate on the right side of the table. The episode is considered successful if the banana is successfully placed on the plate. 

**Drag the Basket.** The task is to drag the basket to the right side of the table. The human demonstration grasps the edge of the basket and pulls it to the right. The episode is considered successful if the robot grasps the basket/ puts the gripper inside the basket and move it to any side of the table. 

**Pick Up the Teddy Bear.** The task is to pick up the teddy bear located at the center of the table. The human demonstration grasps the neck of the bear and picks it up. The episode is considered successful if the robot picks up the bear by the end of the episode. 

**Pick and Place the Bowl.** The task is to pick up the bowl and place on the stove on the right side of the table. The episode is considered successful if the bowl is successfully placed on the stove. 

**Iron Curtain.** The task is to grasp the ironing machine located at the center of the table and slide it to the right side of the curtain. The episode is considered successful if the robot grasps/pushes the ironing machine to any part of the curtain. 

**Shut Down the Laptop.** The task is to close the laptop located in front of the robot. The episode is considered successful if the angle of the laptop is smaller than 10 degrees at the end of the episode. 

**Close the Microwave.** The task is to close the microwave located at the corner of the table. The episode is considered successful if the handle part touches the body part of the microwave at the end of the episode. 

**Wipe the Table.** The task is to pinch/poke the given tissue and wipe the table. The episode is considered successful if 

the robot pinches/pokes the tissue and performs one stroke to any side of the table without missing it. 

## _C. Text Prompts_ 

We use the following text conditions for Pi-0 [1], which are also used for _DemoDiffusion_ . 

TABLE IV: Text prompts used for real-world manipulation tasks. 

|**Task**|**Prompt**|
|---|---|
|Pick and Place the Banana|_pick and place the banana on the_<br>_plate_|
|Drag the Basket|_drag the basket to the right_|
|Pick Up the Teddy Bear|_pick up the bear doll_|
|Pick and Place the Bowl|_pick and place the bowl on the_<br>_stove_|
|Iron the Curtain|_move the ironing machine to the_<br>_right_|
|Wipe the Table|_wipe the table_|
|Close the Microwave|_close the microwave_|
|Shut Down the Laptop|_close the laptop_|


## _D. Inference Details_ 

At each timestep _t_ , we index the human demonstration at same timestep _t_ , and compute the kinematically retargeted actions. As Pi-0 predicts a chunk of actions with length _H_ = 10, we also use the action chunk computed from human demonstration from timestep _t_ to _t_ + _H −_ 1. The episode length is set to be the same as the length(number of timesteps) of human demonstrations across all methods. 

## _E. Kinematic Retargeting Implementation Details_ 

A human demonstration **D** of a manipulation task _T_ consists of the 3D hand pose trajectory _{_ **h** _t }t_<sup>_T_</sup> =0<sup>.Eachhand</sup> pose **h** _t ∈_ R<sup>3</sup><sup>_×J_</sup> , which corresponds to the 3D locations of _J_ keypoints (e.g., wrist and fingertips). To kinematically retarget these 3D keypoints to a robotic end-effector, we use the human’s wrist position _A_ , thumb tip position _B_ , and the average of other fingertips _C_ . Specifically, _⃗ AB_ , along with the cross product of _⃗ AB_ and _⃗ AC_ define the orientation of the end effector, and the human’s wrist position is used as the position of the end effector. As Pi-0 uses joint velocity as action space, the end effector pose is further converted into joint velocity using inverse kinematics. For the gripper, we use the norm of _⃗ BC_ as its width. To stabilize grasping, we set the gripper action to be fully closed if the norm of _⃗ BC_ is smaller than 80% of the gripper’s maximum width, similar to [48]. 

## _F. Hyperparameters_ 

To show our method’s applicability across diverse setups, we do not change the speed of the given human demonstration when performing kinematic retargeting. At inference, we use the following hyperparameters for Pi0 and _DemoDiffusion_ , with only difference on the number of denoising steps, as _DemoDiffusion_ starts denoising 


Fig. 7: **Real-World Manipulation Tasks at Test Time.** Each image corresponds to an example of the scene for each task at test time. To test our method in a natural setup, we add other objects in the scene as visual distractors. For each rollout, we use the same set of distractors across methods. 

TABLE V: Hyperparameters in Real-world. 

|**Hyperparameter**|**Value**|
|---|---|
|Open Loop Horizon|8|
|Predict Action Horizon|10|
|Denoising Steps at Inference (Pi-0)|20|


from intermediate steps. Specifically, we use the following hyperparameters. Depending on the noise level _s_<sup>_∗_</sup> _/S_ , _DemoDiffusion_ uses 20 _× s_<sup>_∗_</sup> _/S_ denoising steps. 

## _G. Additional Results_ 

**Results with Different Hyperparameters.** We present the results of _DemoDiffusion_ using two different hyperparameter settings, _s_<sup>_∗_</sup> _/S_ = 0 _._ 2 and _s_<sup>_∗_</sup> _/S_ = 0 _._ 4. The results are summarized in Table VI. Overall, we observe a consistent trend based on the performance of the base diffusion policy ( _Pi0_ ): 

- When the base policy _Pi-0_ achieves a non-zero success rate, _s_<sup>_∗_</sup> _/S_ = 0 _._ 4 generally yields better performance. This is observed in tasks such as _shut laptop_ , _close microwave_ , _drag basket_ , _wipe table_ , and _iron curtain_ . 

- Conversely, when _Pi-0_ has a zero success rate, _s_<sup>_∗_</sup> _/S_ = 0 _._ 2 tends to perform better. This is the case for tasks including _pick up bear_ , _pick place banana_ , and _pick place bowl_ . We observe that while _s_<sup>_∗_</sup> _/S_ = 0 _._ 4 shows adaptive end effector motion, it tends to avoid activating the gripper at the correct timestep. 

These findings suggest that a more effective base policy enables _DemoDiffusion_ to benefit from a higher noise level, as it can leverage the base policy’s strengths more effectively. In contrast, when the base policy is less reliable, a lower noise level tends to show better performance. We believe this can serve as a guideline for choosing the noise level _s_<sup>_∗_</sup> _/S_ for _DemoDiffusion_ . 

**Zero-Shot Generalization to New Objects.** Lastly, we investigate whether _DemoDiffusion_ can achieve zero-shot 

generalization to new objects within the same category. We use the same human demonstration and text prompt we previously used while evaluating on a new object within the same category. Results are shown in Fig. 8. Although we only provide human demonstration on a different object, we observe that _DemoDiffusion_ can adapt its behavior to a new object. 

## DEXTEROUS GRASPING IN SIMULATION 

## _H. Task Setup Description_ 

In our simulation experiment, the task is to pick up the object. The rollout is considered success when the object’s z position is higher than 0.10 _m_ at the end of the episode. Similar to the real-world experiments, at each timestep of inference, we compute a kinematically retargeted action chunk computed from human demonstration at the same timestep. 

**Training Data.** As we don’t have a _generalist_ pre-trained diffusion policy in simulation, we first train a diffusion policy while constraining the target task to picking up generic objects. Specifically, we collected total 985 grasping trajectories of Allegro hand over 58 objects in the RaiSim simulator for training. The trajectories were generated by rolling out the expert Allegro RL policy with random grasping directions. The 58 objects are randomly sampled from ShapeNet [57] (26 objects) and PartNet [58] (32 objects). The training objects and expert Allegro RL policy are provided by GraspXL [56]. 

**Test Data.** At test time, we provide human grasping trajectories for a different set of objects. As it is challenging to provide human demonstration in simulation, we instead use MANO [62] hand RL policy to collect human demonstrations. The test set contains total 1220 objects, which is a subset of Objvaerse dataset [60]. The objects are divided in three groups based on its size: small scale _s ∈_ [3 _,_ 5] _cm_ medium scale _m ∈_ [5 _,_ 7] _cm_ , and large scale 


Fig. 8: **Zero-Shot Generalization to New Objects.** We evaluate _DemoDiffusion_ ’s generalization capabilities to new objects on 3 tasks - drag the basket, wipe the table, pick and place the bowl. While the objects have different colors and shapes from those of objects in the human demonstration, _DemoDiffusion_ adjusts its behavior to these new objects. Please refer to the website for detailed visualizations. 

TABLE VI: **Additional Quantitative Results for RealWorld Manipulation.** 

|**Task**|**Pi-0 **|<sup>**Kinematic**</sup><br>|**_DemoDiffusion_**<br>|**_DemoDiffusion_**<br>|
|---|---|---|---|---|
|||**Retargeting**|**(**0_._2**)**|**(**0_._4**)**|
|Shut Laptop|20|10|40|**60**|
|Close Microwave|10|80|80|**90**|
|Drag Basket|10|**80**|70|**80**|
|Wipe Table|50|0|60|**100**|
|Iron Curtain|20|70|70|**90**|
|Pick Up Bear|0|40|**60**|40|
|Pick Place Banana|0|70|**90**|20|
|Pick Place Bowl|0|70|**100**|0|
|**Average**|13.8|52.5|**71.3**|60.0|


_l ∈_ [7 _,_ 9] _cm_ . As the object meshes don’t contain material information, we assume fixed density, resulting in diverse mass. We additionally use the same friction coefficient for all objects. Again, test objects and expert MANO [62] RL policy are provided by GraspXL [56]. Additionally, we do not change the speed of the given human demonstration when performing kinematic retargeting. 

## _I. Kinematic Retargeting Implementation Details_ 

Following [8], we use inverse kinematics to match the fingertip positions between the human hand and the robot hand, ignoring the pinky finger. The pose of the robot hand base is initialized to be the same as that of a human hand. 

## _J. Robot Policy Implementation Details_ 

We train a hierarchical policy, where the high-level planner predicts the robot’s future goal state, and the low-level controller predicts the action given the desired future robot state. Both policies were trained using a variant of 3D Diffusion Policy [59], where we modify the point cloud encoder to take point tracks, for a richer representation of the object. Specifically, while the original point encoder takes object points at each timestep, the modified encoder takes a sequence of object points (object tracks) as input. 

High-level planner and low-level controller use a subset of the following as input and output. All rotations are represented in Euler angles. 

**Object state.** contains 3D points of its surface. For a history of robot state, we assume 3D point tracks to be given(i.e. each 3D point across timesteps corresponds to the same point of the object). 

**Robot goal state.** contains its wrist position in the local frame(wrist frame at previous timestep), rotation in the local frame, and relative hand joint angles to the previous timestep. 

**Action.** contains the desired robot’s wrist position in the local frame(previous wrist frame), desired rotation in the local frame, and desired relative hand joint angles to the previous timestep. Note that the action and the robot’s goal state are not the same. For instance, the desired hand joint angles can penetrate the object surface, while the robot’s state cannot. Such a difference creates contact force, enabling a stable grasp. 

**High-level Planner.** The high-level planner takes in a history of robot states and object states, and predicts a sequence of robot goal states. At test-time, we use the kinematic retargeting result as an initial estimate for the robot’s goal state. We then apply _DemoDiffusion_ to refine the robot goal state, and feed it to the low-level controller. 

**Low-level Controller.** The low-level controller takes in a history of robot states and a sequence of robot goal states, and predicts a sequence of robot actions. The goal state encoder has the same architecture to robot state encoder. Once it outputs the action, the action is used as a position target for a PD controller provided in the RaiSim simulator. 

## _K. Hyperparameters_ 

For policy training, we use the default hyperparameters provided in the 3D Diffusion Policy [59] with minimal modifications. For the simulation environment, we use the default hyperparameters provided by GraspXL [56]. Specifically, we use the following same parameters for both the high-level planner and low-level controller. 

TABLE VII: Hyperparameters in Simulation. 

|**Hyperparameter**|**Value**|
|---|---|
|_H_|4|
|_Nobs_|2|
|_Nact_|1|
|_Ngoal_|2|
|_Nlatency_|0|
|Number of Object Points|1024|
|Train Timesteps|1000|
|Inference Timesteps|10|
|Episode Length|155|
|Wrist Position Pgain|100.0|
|Wrist Position Dgain|0.1|
|Wrist Rotation Pgain|100.0|
|Wrist Rotation Dgain|0.2|
|Finger Rotation Pgain|100.0|
|Finger Rotation Dgain|0.2|


**Robot state.** contains its wrist position in the world frame, rotation in the world frame, and absolute hand joint angles. 

