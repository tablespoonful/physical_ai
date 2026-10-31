---
title: "Lifting Embodied World Models for Planning and Control"
date: "2026-04-28"
authors: "Alex N. Wang; Trevor Darrell; Pavel Izmailov; Yutong Bai; Amir Bar"
url: https://arxiv.org/abs/2604.26182
pdf: https://arxiv.org/pdf/2604.26182
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.26182)** / [論文ページ](https://arxiv.org/abs/2604.26182)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Lifting Embodied World Models for Planning and Control** 

Alex N. Wang<sup>1</sup> , Trevor Darrell<sup>2</sup> , Pavel Izmailov<sup>1</sup> , Yutong Bai<sup>2</sup><sup>_‡_</sup> , and Amir Bar<sup>3</sup><sup>_‡_</sup> 

> 1 Computer Science, New York University 

> 2 BAIR, UC Berkeley 

> 3 Imperial College London 

**Abstract.** World models of embodied agents predict future observations conditioned on an action taken by the agent. For complex embodiments, action spaces are high-dimensional and difficult to specify: for example, precisely controlling a human agent requires specifying the motion of each joint. This makes the world model hard to control and expensive to plan with as search-based methods like CEM scale poorly with action dimensionality. To address this issue, we train a lightweight policy that maps high-level actions to sequences of low-level joint actions. Composing this policy with the frozen world model produces a _lifted world model_ that predicts a sequence of future observations from a single high-level action. We instantiate this framework for a human-like embodiment, defining the high-level action space as a small set of 2D waypoints annotated on the current observation frame, each specifying a near-term goal position for a leaf joint (pelvis, head, hands). Waypoints are low-dimensional, visually interpretable, and easy to specify manually or to search over. We show that the lifted world model substantially outperforms searching directly in low-level joint space (3 _._ 8 _×_ lower mean joint error to the goal pose), while remaining more compute-efficient and generalizing to environments unseen by the policy. 

## **1 Introduction** 

World models are a promising approach to understanding the physical world from data [14,24,29,49]. They learn how actions affect the environment by predicting a future observation conditioned on a current observation and an action. World models have progressed from narrow settings like simple games [14, 18, 37] to diverse environments, with actions that span text [1], navigation [4, 21], and whole-body joint control [3]. 

As world models target richer embodiments [3,12,28,31], their action spaces have grown high-dimensional, which presents a challenge in planning and control. For a human-like embodiment [38], actions are specified by high-dimensional, 

> _‡_ Equally advised. Project page: `https://alexn.wang/lwm` 

2 A. N. Wang et al. 


**Fig. 1: Lifted World Model.** The lifted world model outputs a new observation _ot_ + _T_ given a high-level action _a_<sup>HL</sup> . First, the policy _π_ predicts a sequence of _T_ low-level actions _a_<sup>LL</sup> _t_ : _t_ + _T −_ 1<sup>.Thenthelow-levelworldmodelautoregressivelysamplesasequence</sup> of new observations, one for each low-level action, appending each to the observation context for the next step. 

per-joint parameters [6,11,31,45,46]. For example, reaching out with one hand requires coordinated extension of the shoulder, elbow, and wrist. This high dimensionality makes world models difficult to control and especially expensive to use for planning: search-based methods like the Cross-Entropy Method (CEM) [39] scale poorly in action dimensionality [5,36]. 

To address this, we train a lightweight policy that maps high-level actions to sequences of low-level actions (see Figure 1). Composing this policy with the frozen world model yields a _Lifted World Model_ (LWM) that predicts a sequence of observations from a single high-level action. Lifting reduces the effective dimensionality and length of the action sequence the planner must search over, without requiring any changes to the world model itself. 

In our experiments, we lift PEVA [3], a world model that predicts egocentric observations conditioned on human joint-angle displacements. Inspired by human visuomotor control, where visuospatial goals in the posterior parietal cortex are translated into joint-level commands by the motor cortex [27], we design our high-level action space around visual goals expressed in the agent’s current view. A waypoint is the 2D projection of a 3D goal position for a leaf joint of the embodiment (pelvis, head, or hand) that can be reached in a short sequence of joint-space actions (Figure 2). At training time, waypoints are obtained from ground-truth future poses via 3D _→_ 2D camera projection (Figure 3); at inference time, they can be specified manually or searched over with CEM. Figure 4 shows example LWM rollouts: given waypoints overlaid on the current frame, the policy generates a sequence of joint actions and the world model rolls them forward into future observations. 

In Section 4.1 we show that waypoints are an effective goal-conditioning signal for generating joint actions, while goal observations are not: in egocentric video the agent’s own body is mostly out of frame, so a goal image carries little information about the target pose, and conditioning on it barely improves over an unconditioned policy. Waypoints, by contrast, express goals directly in the input frame and meaningfully steer the generated actions toward the target. We further find that the policy responds sensibly to sparse and manually specified 

Lifting Embodied World Models for Planning and Control 

3 


**Fig. 2:** Specifying goals using waypoints. A subset of joints from goal pose _pg_ is drawn as waypoints on _ot_ to create _ot_<sup>ann</sup> _._ 


**Fig. 3:** To obtain waypoints, the goal pose _pg_ is projected onto current observation _ot_ seen by pose _pt_ . 

waypoints (Figure 6) and uses image context to interpret the same waypoints differently depending on the scene (Figure 7). 

In Section 4.2 we use the LWM for search-based planning with CEM on hybrid navigation and interaction tasks from the Nymeria dataset [25]. We find that searching in waypoint space yields solutions 3 _._ 8 _×_ closer to the goal in mean joint error than searching directly in low-level joint space. Planning with highlevel actions is more compute-efficient, performs better on long horizon tasks, and generalizes to environments not seen by the policy during training. 

In summary, our contributions are: 

1. We propose a method for lifting a low-level world model to a higher abstraction level by training a lightweight policy that maps high-level actions to sequences of low-level actions, without modifying the base world model. 

2. We instantiate this framework for a human-like embodiment with a new high-level action space of waypoints: 2D image-space goal positions for the agent’s leaf joints, which are low-dimensional, visually interpretable, and well-suited to search. 

3. We show that waypoints are a more effective goal-conditioning signal for egocentric policies on a human-like embodiment than goal observations. 

4. Using the resulting Lifted World Model, we improve CEM planning by 3.8× in mean joint error to the goal compared to CEM in joint space, at lower compute cost, and with generalization to environments unseen by the policy. 

4 A. N. Wang et al. 


**Fig. 4:** Visualization of LWM rollouts and paired actions<sup>4</sup> . Left _→_ right on each row: the input goal, the sequence of low-level actions predicted by the policy (upper row), and the observations generated by the world model (lower row). The goal is shown by waypoints (pelvis , head , left-hand , right-hand ) plotted on current observation _ot_ , where each dot represents the goal-position for that joint; the mesh is shown for visualization only. **Ex 1:** advancing through the doorway. **Ex 2:** agent walking up and grasping the doorknob. **Ex 3:** avoiding obstacles and moving forward holding a camera. 

## **2 Preliminaries** 

Here we define world models and the representations used for poses and actions. 

**World Models.** A world model predicts the future observation _ot_ +1 given an action _at_ and a current observation _ot_ . A model may condition on _K_ previous observations, **_o_** _t_ = _{ot−K, . . . , ot}_ ; we refer to _K_ as the _world model context length_ . The world model prediction is given by: 


_Notation._ We use bold symbols (e.g., **_o_** _t,_ **_p_** _t_ ) to denote sequences ending at time _t_ , and non-bold symbols (e.g., _ot, pt_ ) to denote individual elements at time _t_ . We also use non-bold symbols for vector-valued quantities at a single timestep (e.g., a 3D <u>position</u> _x_ or a vector of Euler angles _ϕ_ ). 

> 4 We render the mesh for illustration purposes only. The overlaid skeleton shows the exact pose of the embodied agent. 

Lifting Embodied World Models for Planning and Control 5 

**Pose representation.** The human-like embodiment is represented using the XSens [38] model following PEVA [3]. A pose _p_ consists of the 3D position _x_ pelvis of the pelvis and Euler angles _ϕ_ ( _·_ ) for each joint. In our experiments we use the upper-body PEVA checkpoint with 15 joints and the pose representation: 


The pelvis position _x_ pelvis localizes the pose in a reference frame while the Euler angles _ϕ_ ( _·_ ) describe the orientation of each joint. The model assumes rigid bones of constant length. 

A single pose _pt_ is defined with respect to its own pelvis frame; therefore at start time _t_ the position and Euler angles of the pelvis are both zero: _x_ pelvis _, ϕ_ pelvis = **0** . In contrast, a sequence of poses _pt, pt_ +1 _. . ._ are defined with respect to the pelvis frame of the first pose of the sequence. 

**Actions.** An action _at_ is the change between poses _pt, pt_ +1: 


Non-pelvis joints are defined in the frame of their parent joint, so only angular displacements are needed; their 3D positions are recovered via forward kinematics (Appendix H). 


R and R<sup>_−_1</sup> transform Euler angles to and from rotation matrices in SO(3). 

## **3 Lifting an Ego World Model** 

Here we introduce the three components of our method. In Section 3.1, we describe the high-level waypoint action space for controlling egocentric, embodied agents. In Section 3.2, we present the waypoint-conditioned policy that predicts sequences of low-level joint actions. Finally, in Section 3.3, we combine the policy with a low-level world model to form a _Lifted World Model_ (LWM) and describe its use in planning. 

### **3.1 High-level Action Space** 

The high-level action space should be effective, low-dimensional and intuitive. We express high-level actions _a_<sup>HL</sup> in the current observation _ot_ as a set of _waypoints_ . A waypoint is the 2D projection into the current observation _ot_ of a near-term 3D goal position for one leaf joint of the embodied agent. We incorporate them by annotating _ot_ with each waypoint to obtain _o_<sup>ann</sup> _t_ (see Figure 2). 

Defining high-level actions as 2D points in _ot_ makes them visually interpretable and easy to specify manually at test time. Even more importantly, 

6 A. N. Wang et al. 

because waypoints are finite and low dimensional, they avoid the exponential scaling with action dimensionality in search-based planning such as CEM. Our method is in contrast to specifying goals using a goal image _og_ as in NoMaD [42]. Their approach requires the availability of goal images while also being high dimensional and ill-suited to search. 

**Waypoints for a Human Embodiment.** For the XSens embodiment used by PEVA, we define _a_<sup>HL</sup> using four waypoints — for the pelvis, head, left and right hands: 


These are the leaf joints in the embodiment, affording navigation, interaction and camera control (see Figure 2). When plotting the waypoints on image _ot_ , we differentiate them by assigning each a unique color: pelvis , head , left hand , right hand . While 2D image points do not fully specify a 3D goal, the image _ot_ and the spacing between waypoints provide context for inferring the goal pose. 

**Computing Ground-truth Waypoints.** During training, high-level action labels are computed by projecting the ground-truth goal pose _pg_ onto the current image _ot_ . 3D positions are computed from the pose representation with forward kinematics (see Appendix H), which are then projected into the image plane with the camera matrix **P** (Figure 3) 


### **3.2 High-level Action Conditioned Policy** 

We train a lightweight policy to map high-level actions into the low-level action space. At time _t_ the policy predicts a sequence of low-level actions _a_<sup>LL</sup> _t_ : _t_ + _T −_ 1<sup>_∈_</sup> R<sup>_T ×_48</sup> conditioned on context observations **_o_** _t_ = _{ot−Kπ , . . . , ot} ∈_ [0 _,_ 1]<sup>(</sup><sup>_Kπ_+1)</sup><sup>_×CHW_</sup> , poses **_p_** _t_ = _{pt−Kπ , . . . , pt} ∈_ R<sup>(</sup><sup>_Kπ_+1)</sup><sup>_×_48</sup> , and high-level action _at_<sup>HL</sup> _∈_ [0 _,_ 1]<sup>8</sup> : 


We allow for sparse actions where waypoints are out-of-frame, requiring the policy to infer the final joint positions. Goal masking is used to hide goal conditioning to generate unconditioned actions _p_ ( _a_<sup>LL</sup> _t_ : _t_ + _T −_ 1<sup>_|_</sup><sup>**_o_**</sup><sup>_t,_</sup><sup>**_p_**</sup><sup>_t_).Thepolicycontext</sup> size _Kπ_ can be different from the world model context _K_ . By training a policy, we capture short-term motion patterns like locomotion, reaching and grasping. 

**Goal masking.** We explore removing goal-masking when training our final lifting policy to prioritize goal-conditioned generation. When trained without masking, our policy can generate unconditioned actions by using a goal image _~~og~~_ ~~without an~~ y waypoints. We explore waypoint masking in Appendix F. 5 Homogeneous coordinates and the camera frame transform are omitted for clarity. 

7 

Lifting Embodied World Models for Planning and Control 


**Fig. 5:** Planning using the Lifted World Model. The action prior, sampling, and updates to the distribution occur in high-level action space. In contrast, planning with the low-level world model operates in the low-level action space. 

**Architecture.** The policy _π_ ( _·_ ) is a diffusion policy that generates actions by denoising in joint action space. First, a goal image _o_<sup>ann</sup> _t_ is created by annotating each waypoint onto observation _ot_ . Then, images **_o_** _t_ and _o_<sup>ann</sup> _t_ are encoded using a DINOv3-S [41] encoder. The tokens are not pooled to preserve spatial information, producing embeddings [ _zt−Kπ_ : _t|zt_<sup>ann</sup> ] _∈_ R<sup>(</sup><sup>_Kπ_+2)</sup><sup>_×L×D_</sup> . Context poses **_p_** _t_ are linearly projected into _D_ dimensions and added to the image embeddings of the corresponding timestep: _z_ (<sup>_′_</sup> _·_ )<sup>=</sup><sup>_z_(</sup><sup>_·_) + proj(</sup><sup>_p_(</sup><sup>_·_)).Additional3Dpositional</sup> embeddings are added to tokens to preserve spatial as well as temporal ordering before processing with a vision transformer. The processed tokens are pooled to form context vector _ct ∈_ R<sup>_D_</sup> , which is used as input to condition the denoising UNet during generation. 

Our method adds pose context, a DINOv3 encoder, later spatial pooling, 3D positional embeddings, and a larger denoising network to a base diffusion policy [7,42]. See Appendix I for an architecture figure. 

### **3.3 Lifted World Model** 

Using the policy, we can lift the low-level world model to use inputs from the high-level action space (Figure 1). The _Lifted World Model_ (LWM) predicts a future observation _ot_ + _T_ from image, pose context, and a single high-level action: 


Internally, the policy predicts a sequence of low-level actions that are used to autoregressively sample a sequence of internal observations _ot_ +1: _t_ + _T −_ 1 from the low-level world model. 


for _τ ∈{t, . . . , t_ + _T −_ 1 _}_ . Generated observations are appended to the observation context **_o_** _τ_ for subsequent steps _τ > t_ . 

**Search-based Planning.** Now with the LWM, we can run cross-entropy method (CEM) in the high-level action space. Given a starting state and a goal, we sample a sequence of actions, simulate future observations using the world model 

8 A. N. Wang et al. 

and select the trajectory that arrives closest to the goal. Using a low-level world model, actions are sampled in the low-level space directly. The number of samples required for effective search grows exponentially with action dimensionality times sequence length. With a lifted world model, actions can be sampled in the smaller (8 vs. 48 dimensions per step), high-level action space _a_<sup>HL</sup> , greatly reducing both dimensionality and sequence length. The selected high-level action is then mapped to low-level joint actions via the policy for execution. See Figure 5 for a visualization. 

Formally, with a goal observation _og_ , perceptual similarity cost function _C_ ( _·_ ), and a distribution over low-level actions _p_ LL( _·_ ), the CEM planning objective can be formulated as: 


while planning with a lifted world model uses the high-level prior _p_ HL( _·_ ) and is written as 


Image inputs and autoregressive sampling for the world model and policy are omitted for clarity. _L_ indexes the high-level planning horizon. Optimization proceeds iteratively: at each iteration, _N_ action samples are drawn, simulated, and assigned a cost based on the perceptual distance to the goal at the final predicted frame. The _M_ samples with the lowest cost are used to update the prior distribution for the next iteration of the algorithm. 

## **4 Experiments** 

We present our quantitative and qualitative results for the policy conditioned on high-level actions and the Lifted World Model. Our experiments show the effectiveness of conditioning on the high-level action space compared to goal observations. We also demonstrate the improved performance and efficiency when planning in high-level action space using the LWM in comparison to PEVA. 

**Base World Model and Nymeria Dataset.** We use PEVA [3] trained on the Nymeria [25] dataset as a low-level world model. Nymeria consists of first-person videos recorded using Project Aria [9] glasses and XSens [38] motion capture suits in continuous 15-minute sessions in 50 indoor and outdoor environments. The XSens suits provide 3D body motion and joint angle data that are used as the low-level, high-dimensional action space. Compared to other datasets, Nymeria presents a combination of a flexible human-like embodiment and challenging hybrid navigation + interaction tasks. 

**Metrics.** We evaluate the policy and planning tasks by how closely the actions bring the initial pose _pt_ to the goal pose _pg_ . The distance between the final 

Lifting Embodied World Models for Planning and Control 9 

predicted pose _p_ ˆ _g_ and the ground-truth _pg_ is measured by the mean joint error (MJE) [22] in meters of the _leaf_ joints (pelvis, head, and hands), the _intermediate_ joints between them, and _all_ joints together. This provides a ground-truth physical metric for both policy and world model planning performance. 

To compute MJE we integrate the predicted actions starting from the initial pose _pt_ to obtain the predicted final pose _p_ ˆ _g_ : 


A forward kinematics procedure (Appendix H) computes 3D positions for every joint _{x_ pelvis _, . . . , x_ left_hand _}_ = forward_kinematics( _p_ ) for both _pg_ and _p_ ˆ _g_ . The per-joint distances are then computed and averaged over joints for MJE: 


**Implementation Details.** The policy is trained for 10 epochs with a learning rate of 5 _×_ 10<sup>_−_4</sup> using AdamW and a batch size of 256. The action sequence length is _T_ = 8 and the context length is _Kπ_ = 3. We increase the denoising diffusion network UNet dimensions from NoMaD’s [64 _,_ 128 _,_ 256] to [256 _,_ 384 _,_ 512] for all experiments. Nymeria data preparation matches PEVA [3]; sampling is at 4 Hz. Our experiments use the upper-body PEVA checkpoint with 15 joints and 48 action dimensions. World model planning uses up to 6 CEM iterations and 64 samples per iteration. The world model uses context length _K_ = 8 and 64 denoising iterations. The action prior is a Gaussian _N_ ( **_µ_** _, σ_<sup>2</sup> _I_ ) where _µ_ = 0 and _σ_ = 0 _._ 05 for _a_<sup>LL</sup> and _µ_ = 0 _._ 5 and _σ_ = 0 _._ 3 for _a_<sup>HL</sup> which were found by a hyperparameter sweep. Waypoints are expressed in normalized image coordinates with boundaries [0 _,_ 1]. The high-level planning horizon is fixed to _L_ = 1. The cost function is DreamSIM [10]. 

### **4.1 Goal-conditioned policy** 

Here we assess the actions generated using our policy trained on Nymeria. We ablate each addition made to a NoMaD-like diffusion policy in the quantitative results and report _leaf_ , _intermediate_ , and _all_ -joint MJE on the validation set. We also include additional experiments on waypoint visibility and on using depth to specify an exact 3D goal. Qualitative results show that the policy generalizes well to counterfactual waypoints that differ from the waypoints in the data. In addition, the policy can use image context to infer sensible actions from the same waypoints. Finally, we show that goal pose _pg_ cannot be identified from observation _og_ , limiting _og_ ’s usefulness as a goal for egocentric, embodied agents. 

**Quantitative Results.** We report policy performance in Table 1. “Unconditioned” uses no goal information; “goal-conditioned” is when either _og_ or _a_<sup>HL</sup> is used to condition the policy. “Initial distance” is the MJE between starting pose 

A. N. Wang et al. 

10 

**Table 1:** Policy Ablations. We evaluate each change applied to the Base Policy. Results are reported on the validation set. Mean joint error (MJE) is reported in meters. 

||**Uncon**|**ditioned **|**MJE**|**Goal-C**|**ondition**|**ed MJE**|
|---|---|---|---|---|---|---|
|**Model**|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|
|Initial Distance|0.445|0.419|0.426|0.445|0.419|0.426|
|Random Weights|0.749|0.707|0.718|0.735|0.692|0.703|
|Base Policy|0.427|0.397|0.405|0.414|0.384|0.392|
|+ architecture changes|0.406|0.375|0.384|0.388|0.359|0.367|
|+ pose context|0.359|0.329|0.337|0.343|0.316|0.323|
|+ waypoint conditioning|**0.353**|**0.323**|**0.331**|0.262|0.236|0.243|
|+ no masking|0.437|0.408|0.415|**0.243**|**0.219**|**0.226**|
|+ 3d conditioning|0.360|0.330|0.338|0.243|0.219|0.226|
|+ no masking|0.415|0.391|0.398|0.223|0.202|0.208|


_pt_ and goal pose _pg_ while “random weights” refers to actions sampled from an untrained policy. While the NoMaD baseline outperforms an untrained network, it reduces MJE by only 2 _._ 1cm from the initial distance and adding _og_ as goalconditioning reduces it by only another 1 _._ 3cm. Adding architectural changes and pose context **_p_** _t_ improve overall performance, but not goal conditioning. The policy learns coherent action sequences, but the goal observation _og_ does not meaningfully steer them toward the goal. 

Adding waypoint conditioning improves goal-conditioned MJE by 8 _._ 8cm over unconditioned generation. This improvement indicates that conditioning on _a_<sup>HL</sup> shifts the low-level action distribution towards actions that better reach goal pose _pg_ . Furthermore, removing masking improves goal-conditioned performance at the cost of unconditioned MJE. This tradeoff is acceptable since we prioritize goal-conditioned action generation to lift the world model in later experiments. Overall, we find that waypoints are an effective and interpretable high-level action space for goal-conditioned generation. 

**Qualitative Action Generations.** We visualize generated actions in the “Predicted actions” rows of Figure 4. Each action in the sequence is shown by projecting the resulting 3D pose onto _ot_ . The policy controls the agent to both navigate the environment and interact using its hands. In example 2, it reaches to grasp the doorknob, and in example 3, it raises its hand while holding a camera. 

In Figure 6, we evaluate the policy on counterfactual waypoints that do not match the ground truth. In counterfactual 1, the policy is given a sparse highlevel action of only a head waypoint. Using this waypoint, the policy moves the agent to the right while facing left, inferring reasonable positions for the unconditioned joints. In Figure 7 we evaluate the influence of scene context on the generated actions. Contexts 1 and 2 use the same waypoints yet result in different action sequences. We see that in context 1—in front of a stove—the 

Lifting Embodied World Models for Planning and Control 11 


**Fig. 6:** Generating actions from waypoints not seen in data. **Ground truth:** the agent walks down the path. **Ex 1:** head waypoint on the right _→_ agent moves right, faces left. **Ex 2:** four waypoints above the bench _→_ agent climbs onto the bench. 


**Fig. 7:** Contextually aware action generation. The policy predicts different actions from the same waypoints depending on the scene. **Context 1:** agent grasps the pot. **Context 2:** agent walks right and turns to the left. 

leftand right-hand waypoints prompt the agent to grasp the pot, while in context 2 the agent walks forward in the open room. 

**Waypoint visibility.** Since waypoints are defined in observation _ot_ , we investigate whether performance decreases when the joint is not visible. Table 2 separates goal-conditioned MJE by the visibility of the joint in _ot_ . We see a substantial 26 _._ 5cm increase in MJE for observation-conditioned policies when the joint is not visible in the current frame, compared to a modest 12 _._ 7cm increase for waypoint conditioning. This suggests that a waypoint-conditioned policy learns better whole-body motion patterns that generalize even when joints are not visible at test time. Furthermore, removing masking improves visible performance while reducing the not-visible performance drop to only 8 _._ 8cm. This shows that learning with visible waypoints improves performance when they are not inframe. 

**3D Waypoints.** We assess the efficacy of 2D waypoints by comparing with a policy trained using waypoints augmented with depth values. This uses privileged depth information to specify an exact 3D goal, increasing waypoint dimensionality by 50% (8 to 12 dimensions). Results are shown in the last two rows of 

12 A. N. Wang et al. 

**Table 2:** Goal-conditioned action generation with metrics separated based on the visibility of each joint in the current observation _ot_ . MJE in meters. 

||**V**|**isible M**|**JE**|**Not **|**Visible **|**MJE**|
|---|---|---|---|---|---|---|
|**Model**|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|
|Base Policy|0.360|0.297|0.314|0.605|0.705|0.678|
|+ architecture changes|0.340|0.278|0.295|0.566|0.659|0.634|
|+ pose context|0.305|0.254|0.268|0.483|0.551|0.533|
|+ waypoint conditioning|**0.260**|**0.207**|**0.222**|0.327|0.358|0.349|
|+ no masking|**0.251**|**0.200**|**0.213**|**0.284**|**0.307**|**0.301**|


**Table 3:** Decomposing goal-conditioned action generation into motion generation given a goal pose and predicting the goal pose given the goal observation. MJE in meters. 

|**Task**|**Leaf MJE** _↓_|**Int. MJE** _↓_|**All MJE** _↓_|
|---|---|---|---|
|Motion generation|0.115|0.101|0.105|
|Goal pose prediction|0.299|0.272|0.279|


Table 1, where 3D conditioning improves goal-conditioned _all_ MJE by at most 2cm. We further assess 3D waypoints for CEM planning in Section 4.2. 

**Decomposing Action Generation.** We further explore goal-conditioning for egocentric action generation by decomposing it into two separate tasks: motion generation and goal pose prediction. For _motion generation_ , we train a policy to predict joint action sequences with the goal pose _pg_ as input. This is a privileged setting where the policy is given the goal pose and must learn to predict the actions to reach it. For _goal pose prediction_ , we replace the denoising UNet with an MLP to directly predict the goal pose _pg_ conditioned on the goal observation _og_ . See Appendix I for policy architectures. 

Both models are evaluated using MJE between the predicted final pose _p_ ˆ _g_ and the ground-truth goal pose _pg_ . Table 3 shows that predicting an action sequence given the goal pose is easier than predicting the goal pose _pg_ from _og_ . This indicates that egocentric observations are insufficient to identify the goal pose _pg_ since the embodiment is seldom visible in observation _og_ — the hands may be visible, but the rest of the body is rarely seen. 

### **4.2 Lifted World Model Planning** 

Using the Lifted World Model, we perform planning for hybrid navigation + interaction tasks sampled from the Nymeria dataset. Each task consists of observations **_o_** _t_ , poses **_p_** _t_ , and a goal observation _og_ . Planning outputs a sequence of actions, and performance is measured by the MJE between the true goal pose _pg_ and the final pose reached by the planning output. Note that waypoints are not provided, and the task is to search for waypoints that reach the goal pose. 

Lifting Embodied World Models for Planning and Control 

13 

**Table 4:** Search-based planning results using Cross-Entropy Method on 128 tasks. 6 CEM iterations, 64 samples/iteration. Mean joint error shown in meters (m). 

|**Method**<br>**L**|**eaf MJE** _↓_|**Int. MJE** _↓_|**All MJE** _↓_|
|---|---|---|---|
|Initial Distance|0.724|0.697|0.704|
|Copy Baseline (1-NN)|0.696|0.663|0.672|
|Uncond. Policy|0.677|0.641|0.650|
|NoMaD|0.605|0.578|0.585|
|HDP|0.540|0.502|0.512|
|PEVA CEM|0.637|0.608|0.616|
|Lifted CEM (3D)|0.453|0.407|0.420|
|Lifted CEM (2D, ours)|**0.411**|**0.359**|**0.374**|


**Task Generation.** We randomly sample start and goal observation pairs from the Nymeria validation set to generate tasks. Tasks are constrained to have _≥_ 1 joint from the goal pose _pg_ visible in observation _ot_ to avoid goals in unseen areas and reduce world model hallucinations. We also filter tasks for _leaf_ MJE _≥_ 0 _._ 1m between _pt_ and _pg_ to avoid trivial stationary tasks. 

**Quantitative Results.** We report planning results in Table 4. As before, initial distance represents the MJE between _pt_ and _pg_ . We also include a 1-NN copy baseline, selecting the action based on nearest [ _pt_ ; _pg_ ]. PEVA CEM searches directly in low-level joint-action space, while Lifted CEM searches for waypoints that generate actions to reach the goal. PEVA CEM reduces all MJE by only 8 _._ 8cm, while Lifted CEM reduces it by 33cm. For each set of waypoints found by Lifted CEM, we sample 64 joint action sequences and report the average MJE values. To compare with a policy-only approach, we also evaluate the unconditioned policy, an image-conditioned NoMaD [42] policy, and a Hierarchical Diffusion Policy (HDP) [26]. Lifted CEM outperforms all policy-based methods, even ones trained on this goal-observation conditioned planning task. For ablations of the waypoint joints see Appendix C, and for experiments on dexterous manipulation using DexWM [13] see Appendix A. 

**Qualitative Planning Visualizations.** We visualize action and observation sequences using waypoints from CEM planning in Figure 8. Planning with Lifted CEM effectively reproduces the ground truth actions. In task 1, the agent moves to the right following the pelvis waypoint and faces left, while in task 2, it moves its hands over the counter to set down the plastic bag. We find that there are key waypoints that drive the action: (right hand , pelvis ) in task 1 and (left hand , right hand ) in task 2. Similar to how the policy can handle missing waypoints (Section 4.1), it can ignore outlier waypoints found by search: head in task 1 and pelvis in task 2. The policy in Lifted CEM is trained to produce realistic movements, while PEVA CEM may produce unnatural joint angles during planning. See Appendix K for PEVA planning visualizations. 

14 A. N. Wang et al. 


**Fig. 8:** Visualizations of planning solutions. Each row shows from left _→_ right: the current observation _ot_ with waypoints, visualized actions (upper row), the resulting observations (lower row), and the goal observation _og_ . **Task 1:** navigating around the room. **Task 2:** raising hands to set down the plastic bag on the counter. 

**Planning Efficiency.** Planning using CEM with a large world model can be computationally expensive. Thus, we compare the performance of searching over high-level (Lifted CEM) vs. low-level actions (PEVA CEM) for different levels of compute. We measure the MJE of both methods for varying CEM iterations and samples per iteration. For compute measurements see Appendix D. 

Results are shown in Figure 9. We show the cumulative min over CEM iterations, see Appendix G for without. Planning in high-level space outperforms planning in low-level joint action space for all numbers of samples and CEM iterations. Furthermore, we find that PEVA CEM worsens MJE after one step, which highlights the difficulty of naive search. In summary, lifting the abstraction of the world model yields better solutions with less compute. 

**Lifting Using 3D Waypoints.** We evaluate a world model lifted to use 3D waypoints in search-based planning. The results are plotted alongside Lifted CEM in Figure 9. 3D waypoints perform similarly after one CEM step, but lag behind with further iterations due to the larger action dimensionality (12 vs. 8) and the difficulty of finding a correct depth value. 

**Varying Goal Horizons.** We also report planning results for goals sampled from different timesteps into the future and different initial MJE distances. Figure 10 shows performance when goals are sampled from varying time horizons. 

Lifting Embodied World Models for Planning and Control 

15 


**Fig. 9:** Planning performance for different CEM budgets. Searching in our lifted action space scales better than in joint space. 3D waypoints are more difficult to search. 


**Fig. 10:** Planning results for varying goal horizons. The vertical line shows the policy training distribution. 

**Fig. 11:** Planning on tasks of varying inital MJE. Tasks are grouped using 20 quantile buckets. 

In this setting, PEVA CEM plans for actions of sequence length equal to the goal horizon whereas Lifted CEM is fixed at 8 due to fixed policy length. Despite this, we find that Lifted CEM outperforms PEVA CEM over all goal horizons. 

Figure 11 plots performance against initial MJE, with tasks grouped into 20 quantile buckets. The _y_ = _x_ line is a baseline where no action is taken, where the initial and final MJE are equal. Lifted CEM outperforms PEVA CEM at most initial distances while both methods perform worse when initial MJE _≤_ 0 _._ 3m. 

**Unseen Environments.** To test the generalization of our lifting methodology, we train a policy on a new training set where videos from Nymeria locations 6, 19, and 34 are replaced with videos from other locations. Then, we use this policy to lift the same PEVA model and evaluate the lifted model on tasks from held-out locations 6, 19, and 34. 

16 A. N. Wang et al. 

**Table 5:** Lifted CEM planning on tasks in unseen environments. MJE in meters. 

|**Method**|**Leaf MJE** _↓_|**Int. MJE** _↓_|**All MJE** _↓_|
|---|---|---|---|
|Initial Distance|0.618|0.589|0.597|
|PEVA CEM|0.572|0.546|0.553|
|Lifted CEM (ours)|0.373|0.318|0.333|
|Lifted CEM (held-out)|0.404|0.346|0.362|


Results are presented in Table 5. Lifted CEM using the held-out policy outperforms PEVA CEM and is only slightly worse than using the base policy trained on all environments. Therefore, the short-term lightweight policy design generalizes well to unseen environments. 

## **5 Related Work** 

**World Models and Planning.** Many world model works explore planning: PlaNet [16], TD-MPC2 [19], DINO-WM [52] and VJEPA-2 [2,29] plan in latent space, while UniSim [49] and NWM [4] are used downstream to plan in pixel space. Among these works, cross-entropy method [39] is the _de facto_ planning approach, while MPPI [47] also sees use. DINO-WM [52] and Parthasarathy et al. [35] explore using gradient-based methods. DynaGuide [8] guides a diffusion policy via gradients through a latent world model. The Dreamer [15,17,18] series learns a world model for policy training. PEVA [3] trains a whole-body conditioned world model, and DexWM [13] conditions on hands. To our knowledge, our work is the first to use a world model to plan for complex, egocentric, humanlike embodiments, and the first to lift a low-level world model to a higher level of abstraction to make this challenging task tractable. 

**Embodied, Egocentric, and Hierarchical Policies.** NoMaD [42] tackles navigation from an egocentric point of view with a point-robot embodiment while Diffusion Policy [7] uses a similar architecture for manipulation with articulated robots. Nachum et al. [30] and later HIQL [34] are works that learn hierarchical policies. iDP3 [50] controls a humanoid at a joint level from an egocentric 3D camera. Large-scale models include GR00T-N1 [6], which controls an articulated humanoid, and VLA approaches like OpenVLA [23] and Octo [32], which tend to focus on robotic arms and exocentric manipulation tasks. No prior works address navigation and manipulation for embodiments from an egocentric view, which is a key affordance of human-like agents, nor do they consider the use of a low-dimensional, finite, and searchable input space for goal conditioning. 

**Motion Generation.** Motion generation aims to learn a realistic distribution of human motion controlled by text, action labels, or keypoint constraints. MDM [46] and MotionDiffuse [51] use diffusion for text-conditioned motion generation and PriorMDM [40] extends this with dense end-effector and keypoint conditioning. OmniControl [48] supports sparse 3D keypoint conditioning over 

Lifting Embodied World Models for Planning and Control 

17 

arbitrary joints and timesteps. CLoSD [45] and MaskedMimic [44] both utilize a physics simulator: the former closes the generation loop with simulation, while the latter performs motion inpainting. GOAL [43] focuses on hand-object grasping for a target object in an open-loop setting. All of these works control a human embodiment, but do not address reaching a precise goal state in an environment from egocentric observations. Our waypoint approach shares some similarity with keypoint conditioning, but specifies sparse 2D joint positions for the final goal pose, relying on the policy to capture short-term motion patterns instead of a dense sequence of 3D joint positions. 

## **6 Limitations and Future Work** 

Currently, our method does not explicitly control head orientation. This allows the agent to look in various directions which can affect observations generated by the world model. Explicit control of the head pose may be helpful — specifying an orientation or marking a target to look at are possible approaches. 

Also, waypoints cannot specify goal poses that lie fully outside the current observation. This limitation is acceptable as world models often hallucinate when generating unseen spaces. However, as world models improve in consistency, waypoints that extend beyond the current observation may become an interesting direction. 

## **7 Conclusion** 

We present a method for lifting a low-level world model to a higher level of abstraction by training a goal-conditioned policy that maps high-level actions to sequences of low-level actions, and instantiate it for a human-like embodiment using waypoints as the high-level action space. We show that embodied, egocentric agents benefit from specifying goals as waypoints grounded in the present observation, and that search-based planning with the resulting Lifted World Model is 3 _._ 8 _×_ more effective than planning in low-level joint space, at lower compute cost, and generalizes to environments unseen by the policy. Notably, our approach is lightweight, scalable, and requires no additional data collection or annotation beyond what is already used to train the world model. Moving forward, we believe lifting is a promising direction for keeping world models controllable and plannable as they scale to richer embodiments and more complex tasks; exploring alternative high-level action spaces and embodiments is a natural next step. 

18 A. N. Wang et al. 

## **References** 

1. Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025) 

2. Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al.: V-jepa 2: Self-supervised video models enable understanding, prediction and planning. arXiv preprint arXiv:2506.09985 (2025) 

3. Bai, Y., Tran, D., Bar, A., LeCun, Y., Darrell, T., Malik, J.: Whole-body conditioned egocentric video prediction. In: The Thirty-ninth Annual Conference on Neural Information Processing Systems (2025), `https://openreview.net/forum? id=XDTTwmjhAg` 

4. Bar, A., Zhou, G., Tran, D., Darrell, T., LeCun, Y.: Navigation world models. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 15791–15801 (2025) 

5. Bharadhwaj, H., Xie, K., Shkurti, F.: Model-predictive control via cross-entropy and gradient-based optimization. In: Learning for Dynamics and Control. pp. 277– 286. PMLR (2020) 

6. Bjorck, J., Castañeda, F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al.: Gr00t n1: An open foundation model for generalist humanoid robots. arXiv preprint arXiv:2503.14734 (2025) 

7. Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S.: Diffusion policy: Visuomotor policy learning via action diffusion. The International Journal of Robotics Research **44** (10-11), 1684–1704 (2025) 

8. Du, M., Song, S.: Dynaguide: Steering diffusion policies with active dynamic guidance. In: Proceedings of the 39th Conference on Neural Information Processing Systems (NeurIPS) (2025) 

9. Engel, J., Somasundaram, K., Goesele, M., Sun, A., Gamino, A., Turner, A., Talattof, A., Yuan, A., Souti, B., Meredith, B., et al.: Project aria: A new tool for egocentric multi-modal ai research. arXiv preprint arXiv:2308.13561 (2023) 

10. Fu, S., Tamir, N., Sundaram, S., Chai, L., Zhang, R., Dekel, T., Isola, P.: Dreamsim: Learning new dimensions of human visual similarity using synthetic data. In: Advances in Neural Information Processing Systems. vol. 36, pp. 50742–50768 

11. Fu, Z., Zhao, Q., Wu, Q., Wetzstein, G., Finn, C.: Humanplus: Humanoid shadowing and imitation from humans. In: Conference on Robot Learning. pp. 2828–2844. PMLR (2025) 

12. Gao, S., Liang, W., Zheng, K., Malik, A., Ye, S., Yu, S., Tseng, W.C., Dong, Y., Mo, K., Lin, C.H., et al.: Dreamdojo: A generalist robot world model from large-scale human videos. arXiv preprint arXiv:2602.06949 (2026) 

13. Goswami, R.G., Bar, A., Fan, D., Yang, T.Y., Zhou, G., Krishnamurthy, P., Rabbat, M., Khorrami, F., LeCun, Y.: World models can leverage human videos for dexterous manipulation. arXiv preprint arXiv:2512.13644 (2025) 

14. Ha, D., Schmidhuber, J.: Recurrent world models facilitate policy evolution. In: Advances in Neural Information Processing Systems 31, pp. 2451–2463. Curran Associates, Inc. (2018), `https://papers.nips.cc/paper/7512-recurrent-worldmodels-facilitate-policy-evolution` , `https://worldmodels.github.io` 

15. Hafner, D., Lillicrap, T., Ba, J., Norouzi, M.: Dream to control: Learning behaviors by latent imagination. In: International Conference on Learning Representations 

Lifting Embodied World Models for Planning and Control 19 

16. Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H., Davidson, J.: Learning latent dynamics for planning from pixels. In: International conference on machine learning. pp. 2555–2565. PMLR (2019) 

17. Hafner, D., Lillicrap, T.P., Norouzi, M., Ba, J.: Mastering atari with discrete world models. In: International Conference on Learning Representations 

18. Hafner, D., Pasukonis, J., Ba, J., Lillicrap, T.: Mastering diverse control tasks through world models. Nature **640** (8059), 647–653 (2025). `https://doi.org/10. 1038/s41586-025-08744-2` , `https://doi.org/10.1038/s41586-025-08744-2` 

19. Hansen, N., Su, H., Wang, X.: Td-mpc2: Scalable, robust world models for continuous control. In: The Twelfth International Conference on Learning Representations 

20. Hoque, R., Huang, P., Yoon, D.J., Sivapurapu, M., Zhang, J.: Egodex: Learning dexterous manipulation from large-scale egocentric video (2025), `https://arxiv. org/abs/2505.11709` 

21. Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023) 

22. Ionescu, C., Papava, D., Olaru, V., Sminchisescu, C.: Human3.6m: Large scale datasets and predictive methods for 3d human sensing in natural environments. IEEE Transactions on Pattern Analysis and Machine Intelligence **36** (7), 1325–1339 (2014). `https://doi.org/10.1109/TPAMI.2013.248` 

23. Kim, M.J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E.P., Sanketi, P.R., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., Finn, C.: Openvla: An opensource vision-language-action model. In: Agrawal, P., Kroemer, O., Burgard, W. (eds.) Proceedings of The 8th Conference on Robot Learning. Proceedings of Machine Learning Research, vol. 270, pp. 2679–2713. PMLR (06–09 Nov 2025), `https://proceedings.mlr.press/v270/kim25c.html` 

24. LeCun, Y., et al.: A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. Open Review **62** (1), 1–62 (2022) 

25. Ma, L., Ye, Y., Hong, F., Guzov, V., Jiang, Y., Postyeni, R., Pesqueira, L., Gamino, A., Baiyya, V., Kim, H.J., et al.: Nymeria: A massive collection of multimodal egocentric daily motion in the wild. In: European Conference on Computer Vision. pp. 445–465. Springer (2024) 

26. Ma, X., Patidar, S., Haughton, I., James, S.: Hierarchical diffusion policy for kinematics-aware multi-task robotic manipulation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 18081– 18090 (2024) 

27. Merel, J., Botvinick, M., Wayne, G.: Hierarchical motor control in mammals and machines. Nature Communications **10** (1), 5489 (2019). `https://doi.org/10. 1038/s41467-019-13239-6` , `https://doi.org/10.1038/s41467-019-13239-6` 

28. Mereu, R., Scannell, A., Hou, Y., Zhao, Y., Jitta, A., Dominguez, A., Acerbi, L., Storkey, A., Chang, P.: Generative world modelling for humanoids: 1x world model challenge technical report. arXiv preprint arXiv:2510.07092 (2025) 

29. Mur-Labadia, L., Muckley, M., Bar, A., Assran, M., Sinha, K., Rabbat, M., LeCun, Y., Ballas, N., Bardes, A.: V-jepa 2.1: Unlocking dense features in video self-supervised learning. arXiv preprint arXiv:2603.14482 (2026) 

30. Nachum, O., Gu, S.S., Lee, H., Levine, S.: Data-efficient hierarchical reinforcement learning. Advances in neural information processing systems **31** (2018) 

31. Nicklas Hansen, Jyothir S V, V.S.Y.L.X.W.H.S.: Hierarchical world models as visual whole-body humanoid controllers (2025) 

- 20 A. N. Wang et al. 

32. Octo Model Team, Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Xu, C., Luo, J., Kreiman, T., Tan, Y., Chen, L.Y., Sanketi, P., Vuong, Q., Xiao, T., Sadigh, D., Finn, C., Levine, S.: Octo: An open-source generalist robot policy. In: Proceedings of Robotics: Science and Systems. Delft, Netherlands (2024) 

33. Oquab, M., Darcet, T., Moutakanni, T., Vo, H.V., Szafraniec, M., Khalidov, V., Fernandez, P., HAZIZA, D., Massa, F., El-Nouby, A., et al.: Dinov2: Learning robust visual features without supervision. Transactions on Machine Learning Research 

34. Park, S., Ghosh, D., Eysenbach, B., Levine, S.: Hiql: offline goal-conditioned rl with latent states as actions. In: Proceedings of the 37th International Conference on Neural Information Processing Systems. pp. 34866–34891 (2023) 

35. Parthasarathy, A., Kalra, N., Agrawal, R., LeCun, Y., Bounou, O., Izmailov, P., Goldblum, M.: Closing the train-test gap in world models for gradient-based planning. arXiv preprint arXiv:2512.09929 (2025) 

36. Psenka, M., Rabbat, M., Krishnapriyan, A., LeCun, Y., Bar, A.: Parallel stochastic gradient-based planning for world models. arXiv preprint arXiv:2602.00475 (2026) 

37. Robine, J., Höftmann, M., Uelwer, T., Harmeling, S.: Transformer-based world models are happy with 100k interactions. arXiv preprint arXiv:2303.07109 (2023) 

38. Roetenberg, D., Luinge, H., Slycke, P., et al.: Xsens mvn: Full 6dof human motion tracking using miniature inertial sensors. Xsens Motion Technologies BV, Tech. Rep **1** (2009), 1–7 (2009) 

39. Rubinstein, R.Y.: Optimization of computer simulation models with rare events. European Journal of Operational Research **99** (1), 89–112 (1997). `https:// doi.org/https://doi.org/10.1016/S0377-2217(96)00385-2` , `https://www. sciencedirect.com/science/article/pii/S0377221796003852` 

40. Shafir, Y., Tevet, G., Kapon, R., Bermano, A.H.: Human motion diffusion as a generative prior. In: The Twelfth International Conference on Learning Representations 

41. Siméoni, O., Vo, H.V., Seitzer, M., Baldassarre, F., Oquab, M., Jose, C., Khalidov, V., Szafraniec, M., Yi, S., Ramamonjisoa, M., et al.: Dinov3. arXiv preprint arXiv:2508.10104 (2025) 

42. Sridhar, A., Shah, D., Glossop, C., Levine, S.: Nomad: Goal masked diffusion policies for navigation and exploration. In: 2024 IEEE International Conference on Robotics and Automation (ICRA). pp. 63–70. IEEE (2024) 

43. Taheri, O., Choutas, V., Black, M.J., Tzionas, D.: Goal: Generating 4d whole-body motion for hand-object grasping. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 13263–13273 (2022) 

44. Tessler, C., Guo, Y., Nabati, O., Chechik, G., Peng, X.B.: Maskedmimic: Unified physics-based character control through masked motion inpainting. ACM Transactions On Graphics (TOG) **43** (6), 1–21 (2024) 

45. Tevet, G., Raab, S., Cohan, S., Reda, D., Luo, Z., Peng, X.B., Bermano, A.H., van de Panne, M.: CLoSD: Closing the loop between simulation and diffusion for multi-task character control. In: The Thirteenth International Conference on Learning Representations (2025), `https://openreview.net/forum?id= pZISppZSTv` 

46. Tevet, G., Raab, S., Gordon, B., Shafir, Y., Cohen-Or, D., Bermano, A.H.: Human motion diffusion model. In: The Eleventh International Conference on Learning Representations 

47. Williams, G., Aldrich, A., Theodorou, E.A.: Model predictive path integral control: From theory to parallel computation. Journal of Guidance, Control, and Dynamics **40** (2), 344–357 (2017) 

Lifting Embodied World Models for Planning and Control 21 

48. Xie, Y., Jampani, V., Zhong, L., Sun, D., Jiang, H.: Omnicontrol: Control any joint at any time for human motion generation. In: The Twelfth International Conference on Learning Representations 

49. Yang, S., Du, Y., Ghasemipour, S.K.S., Tompson, J., Kaelbling, L.P., Schuurmans, D., Abbeel, P.: Learning interactive real-world simulators. In: The Twelfth International Conference on Learning Representations (2024), `https://openreview. net/forum?id=sFyTZEqmUY` 

50. Ze, Y., Chen, Z., Wang, W., Chen, T., He, X., Yuan, Y., Peng, X.B., Wu, J.: Generalizable humanoid manipulation with 3d diffusion policies. In: 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). pp. 2873– 2880. IEEE (2025) 

51. Zhang, M., Cai, Z., Pan, L., Hong, F., Guo, X., Yang, L., Liu, Z.: Motiondiffuse: Text-driven human motion generation with diffusion model. IEEE transactions on pattern analysis and machine intelligence **46** (6), 4115–4128 (2024) 

52. Zhou, G., Pan, H., LeCun, Y., Pinto, L.: DINO-WM: World models on pretrained visual features enable zero-shot planning. In: Forty-second International Conference on Machine Learning (2025), `https://openreview.net/forum?id= D5RNACOZEI` 

22 A. N. Wang et al. 

## **A Lifting a Dexterous Manipulation World Model** 

We apply our lifting approach to DexWM [13]. Frames are sampled over 2 seconds at 2Hz for a total of 4 frames. The high-level actions are defined as the: 


for a total of 8 dimensions. We increase the denoising Unet to [512 _,_ 768 _,_ 1024] dimensions and 30 denoising timesteps. 

We follow the same procedure for planning with CEM using _σ_ = 60px in observation _ot ∈_ [0 _,_ 1]<sup>224</sup><sup>_×_224</sup> . We use a latent L2 cost 


instead of DreamSIM because DexWM predicts DINOv2 [33] latents. Instead of sampling autoregressively using DexWM, we combine the 4 action steps into a single-step action due to rollout instability (see Appendix A.2). 

### **A.1 Planning results** 

We present our preliminary planning results on 256 tasks sampled from EgoDex [20]. 8 CEM iterations were performed with 256 samples per iteration. Surprisingly, Base CEM is unable to find any solution in an 142 dimensional action space. 

|**Method**<br>**All **|**MJE (cm)** _↓_|
|---|---|
|Initial Distance|10.46|
|Base CEM|13.81|
|Lifted CEM|**7.98**|


**Table 6:** All-MJE for dexterous manipulation using DexWM 

### **A.2 Rollout instability** 

We find that DexWM exhibits rollout instability. Sampling autoregressively for 4 or 8 steps over 2 seconds produces a higher L2 loss than summing the action sequence over all timesteps and performing a single prediction. Over 256 tasks, the L2 latent loss from predicting the final state using the ground-truth actions is shown in Table 7. 

|1-step<br>0.818|4-step<br>0.868|8-step<br>0.994|
|---|---|---|


**Table 7:** Goal state L2 error from ground truth actions 

Lifting Embodied World Models for Planning and Control 

23 

## **B Cost-function convergence during world model planning** 


**Fig. 12:** Cost function convergence with respect to CEM iterations and number of samples. 

Across all methods, more samples leads to a lower DreamSIM perceptual distance. However, Lifted CEM has the highest perceptual distance while PEVA has the lowest perceptual distance. This suggests a mismatch between our MJE metric and the perceptual distance metric. This makes sense as the goal observation in general is often not informative of the present pose of the embodiment. This means the body can be in any manner of incorrect poses despite a good DreamSIM, or the body can be in the correct pose but have a higher perceptual distance due to a slightly altered head pose. 

### **B.1 Policy as a regularizer** 

In general this presents the interesting possibility that a good policy acts as a regularizer for the planning procedure, limiting it to only plausible human actions. It may be possible that CEM in low-level joint space on a per-timestep level might be hacking the perceptual similarity objective. 

24 A. N. Wang et al. 

## **C Waypoint Joint Ablation** 

We ablate the choice of joints for both goal-conditioned policy training as well as planning. See Table 8 for results. We find that our method is robust to the choice of joints used for high-level waypoint actions. Planning was performed with 6 iterations, 8 samples for 64 tasks. 

||**Goal-**|**Conditi**|**oned**||**Plann**|**ing**|
|---|---|---|---|---|---|---|
|**Method**|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|
|Pelvis|0.280|0.247|0.255|0.482|0.451|0.460 _±_0.043|
|Head|0.299|0.266|0.275|0.395|0.353|0.365 _±_0.039|
|Hands|0.256|0.235|0.240|0.430|0.380|0.394 _±_0.039|
|Pelvis+Head|0.268|0.233|0.242|0.467|0.432|0.442 _±_0.034|
|Pelvis+Hands|0.250|0.227|0.233|0.422|0.371|0.385 _±_0.036|
|Head+Hands|0.247|0.224|0.230|0.406|0.357|0.371 _±_0.038|
|Pelvis+Head+Hands|0.243|0.219|0.226|0.431|0.394|0.405 _±_0.035|


**Table 8:** Goal-conditioned waypoints is robust to choice of joints. 

## **D Policy and PEVA Compute Measurements** 

See Table 9 for model compute differences. 

|**Model**|**Params (M)**|**Wall-clock **|**(ms)**|**FLOPs (GFLOPs)**|
|---|---|---|---|---|
|Policy _πθ_|58.1||63.9|605.4|
|PEVA|1,060.1|48,|203.9|12,438,305.4|


**Table 9:** Policy vs. World Model Compute 

## **E Generalization of the Lifted World Model** 

We evaluate the generalization of our lifting method in subsection 4.2 by performing planning in environments held out during policy training. We find that our policy performs well and samples reasonable actions even in unseen environments. 

We note that PEVA has been trained on these environments, but neither model has seen the planning tasks which come from validation videos. This is important as using a world model to simulate unseen environments amounts to planning by imagination. Furthermore, our contribution is the proposed lifting procedure which only involves training the lifting policy. 

Lifting Embodied World Models for Planning and Control 

25 

## **F Waypoint Masking Experiments** 

We preliminarily explore masking waypoints during training so the policy can better handle sparse inputs at inference. For example, only a pelvis waypoint can be used to navigate, leaving the other joint targets unspecified. Masking also teaches the policy to infer the target joint position when a waypoint is missing, such as when it is out of frame. During training, half the time no waypoints are masked, and half the time each waypoint is independently masked with probability 0.5. 

In our limited training run, waypoint masking sacrifices some goal-conditioned policy performance and performs better on unconditioned action generation. However, interestingly, in planning, the waypoint masking policy performs better, particularly on the Leaf joints, by a whole 1.1cm. This indicates the possibility that randomly masking waypoints teaches the model to better-infer missing waypoints. CEM planning often only finds a subset of correctly situated waypoints and the waypoint masked policy is better able to infer the remaining ones. 

It is possible that further training and more policy capacity may help close the goal-conditioned gap which we leave for future works. 

**Table 10:** Waypoint masking policy performance compared to no masking. 

||**Uncon**|**ditioned **|**MJE**|**Goal-C**|**ondition**|**ed MJE**|
|---|---|---|---|---|---|---|
|**Model**|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|**Leaf** _↓_|**Int.** _↓_|**All** _↓_|
|Initial Distance|0.445|0.419|0.426|0.445|0.419|0.426|
|no masking|0.415|0.391|0.398|0.223|0.202|0.208|
|waypoint masking|0.364|0.335|0.343|0.263|0.236|0.243|


**Table 11:** Planning results with waypoint masking compared to no masking with 64 samples per task for 64 tasks. 

|**Method**|**Leaf MJE** _↓_|**Int. MJE** _↓_|**All MJE** _↓_|
|---|---|---|---|
|Initial Distance|0.724|0.697|0.704|
|Lifted CEM (2D, ours)|0.399|**0.349**|**0.364**|
|Waypoint Masking|**0.388**|**0.349**|**0.360**|


26 A. N. Wang et al. 

## **G CEM iteration graphs without cumulative min for each step** 


**Fig. 13:** MJE over CEM iterations without cumulative minimum. 

**Fig. 14:** Cost function convergence with respect to CEM iterations and number of samples without cumulative minimum. 

We do not take the cumulative minimum over these steps. Lifted CEM is still much more effective than PEVA CEM. While noisier, Lifted CEM also outperforms Lifted CEM with a 3D-augmented policy. 

Lifting Embodied World Models for Planning and Control 

27 

## **H Forward Kinematics** 

We use a forward kinematics computation based on the XSens [38] human model to compute joint positions in 3D space. The pose representation used in our paper directly specifies the pelvis position in 3D space as the root of our embodiment _x_ pelvis. The 3D position of a child joint is computed in a world frame. 


The Euler angle _ϕ_ parent is the parent orientation in the world frame. _∆x_ parent,child is the spatial offset representing the bone defined in the parent frame. The individual bone lengths vary for each participant. 

The kinematic parent-child relationships are shown in Table 12. 


**Table 12:** Kinematic tree parent-child relationships 

28 A. N. Wang et al. 

## **I Policy Architecture** 

Below are the policy architectures used in this paper. We also present the motion generation and goal prediction models used in Section 4.1. 


**Fig. 16:** Motion Generation model architecture; changes highlighted in blue. 


**Fig. 17:** Goal prediction model architecture; changes highlighted in blue. 

Lifting Embodied World Models for Planning and Control 

29 

## **J Additional Planning Visualizations** 

Additional planning visualizations. 


**Fig. 18:** Waypoint CEM with additional tasks, and no SMPL mesh. 

30 A. N. Wang et al. 


**Fig. 19:** Waypoint CEM with additional tasks, with mesh. 

Lifting Embodied World Models for Planning and Control 

31 

## **K PEVA Planning Visualizations** 


**Fig. 20:** Additional PEVA CEM Planning visualizations without meshes 

32 A. N. Wang et al. 


**Fig. 21:** Additional PEVA CEM Planning visualizations 

Note that when planning with PEVA there can be unrealistic body movements. See Task 2, where the left shoulder contorted at timesteps 7 and 8. Also see Task 3 where the torso and right shoulder are in unnatural positions at timesteps 3 through 8. 

Lifting Embodied World Models for Planning and Control 

33 

## **L Additional Policy Visualizations** 


**Fig. 22:** Additional visualizations of waypoint actions and rollout. 


**Fig. 23:** Extra Counterfactual Visualizations 1 

34 A. N. Wang et al. 


**Fig. 24:** Extra Counterfactual Visualizations 2 

