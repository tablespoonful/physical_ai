---
title: "HybridDriveVLA: Vision-Language-Action Model with Visual CoT reasoning and ToT Evaluation for Autonomous Driving"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Bassole_HybridDriveVLA_Vision-Language-Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Bassole_HybridDriveVLA_Vision-Language-Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Bassole_HybridDriveVLA_Vision-Language-Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Bassole_HybridDriveVLA_Vision-Language-Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **HybridDriveVLA: Vision-Language-Action Model with Visual CoT reasoning and ToT Evaluation for Autonomous Driving** 

Yipene Cedric Francois Bassole<sup>1</sup> Sungwoo Kim<sup>1</sup> Jiwoo Jung<sup>1</sup> Yunsick Sung<sup>1</sup><sup>_†_</sup> 

1 Dongguk University-Seoul, Korea 

cedric@dgu.ac.kr, sean1255@dgu.ac.kr, xhfl99@dgu.ac.kr, sung@dongguk.edu 


Figure 1. HybridDriveVLA is a vision–language–action model for autonomous driving that integrates visual anticipation and deliberative evaluation for selecting actions. During inference, it takes multi-view images, ego vehicle states, and instructions as input, then processes them using a vision encoder and text tokenizer. A Chain-of-Thought reasoning mechanism anticipates driving scene elements, while Treeof-Thought evaluates candidate waypoints based on safety, progress, and comfort to select the optimal trajectory. 

## **Abstract** 

_Vision-Language-Action (VLA) models are emerging as an important technology in autonomous driving, recognized for their sophisticated reasoning and interpretability. How-_ 

_ever, traditional VLA models often rely on image-to-text with Chain-of-Thought (CoT) reasoning, which converts sequential visual scenes into textual symbols, thereby underutilizing spatial context in visual information. Existing autonomous driving systems using VLA models predict only a single sequence of waypoints as a trajectory considering a given command and multiple aspects. However, we suggest_ 

> _†_ Corresponding author. Email: sung@dongguk.edu 

32421 

_evaluating each sequence of waypoints to reveal the importance of the corresponding aspect. We introduce HybridDriveVLA, a VLA model that integrates visual Chain-ofThought (V-Cot) reasoning and a proposed Tree-of-Thought (ToT)-inspired waypoint evaluation (ToT-evaluation). V- Cot reasoning anticipates future scenes, which serve as goals for ToT-evaluation. The ToT-evaluation generates and scores waypoints based each on safety, progress, and comfort aspects. The highest cumulated score of the waypoints based on the three aspects is optimal. To the best of our knowledge, we are the first to propose a unified method integrating both a CoT and a ToT approach in a VLA model. Experimental results demonstrated that HybridDriveVLA achieved strong performance on comfort, progress, and safety metrics with and average collision rate of 0.17% on the nuScenes benchmark, outperforming traditional VLA models._ 


## **1. Introduction** 

The evolution of autonomous driving is rapidly converging towards End-to-End systems powered by Vision-LanguageAction (VLA) models. VLA models [32, 34] have emerged as a promising world-model paradigm that maps raw sensor data and navigational commands directly to vehicle control actions. By leveraging their knowledge and reasoning capabilities, VLA models can interpret complex traffic scenarios and anticipate dynamic changes. Despite their advantages, traditional VLA approaches face several critical limitations that reduce their ability to reason effectively and take coherent decisions in complex driving environments. In fact, they under-utilise visual information by performing imageto-text with Chain-of-Thought (CoT) reasoning [28, 32] to improve interpretability. However, in the context of autonomous driving, traditional CoT [2, 13] that converts continuous and high-dimensional visual data into discrete textual representation, as shown in Figure 2 under-utilizes visual information. This linguistic abstraction inevitably degrades spatial information contained in visual information, which can be important for precision. Existing autonomous driving systems using VLA models predict only a single sequence of waypoints as a trajectory considering a given command and multiple aspects. However, we suggest evaluating each sequence of waypoints to reveal the importance of the corresponding aspect. Moreover, traditional VLA models [17] mostly predict only a single sequence of waypoints considering simultaneously multiple aspects, which leads to a single multi-aspect sequence of waypoints. These models predict one statistically likely sequence of waypoints that lacks individual aspect deliberation. Consequently, it may predict unsafe, uncomfortable, unprogressive waypoints especially in uncertain or multi-agent environments that require precise and flexible decision-making. 

Figure 2. Evolution from traditional VLA to our proposed HybridDriveVLA. (a) Direct action prediction. (b) CoT-based reasoning for textual explanations. (c) HybridDriveVLA as an autonomous driving world-model combining V-CoT for visual next scene anticipation/generation and ToT-Evaluation for evaluative trajectory planning on each specific aspect. 

To overcome these limitations, we propose HybridDriveVLA, a framework designed to reason through visual anticipation and deliberative planning evaluation. Our method is built upon two main processes: a Visual Chainof-Thought (V-CoT) and a proposed Tree-of-Thoughtinspired waypoint evaluation (ToT-Evaluation), as shown in Figure 1. HybridDriveVLA employs V-CoT for visual reasoning by sequentially generating next scenes. This visual anticipation generates the next scenes and use those as goal state representation that preserves spatial details and continuity. Moreover, rather than relying on a single deterministic sequence of waypoints, HybridDriveVLA reasons deliberately using ToT-Evaluation to plan, generate, and score multiple waypoint sequences based on explicit safety, progress, and comfort aspects, where the highest cumulated score across these three aspects is selected as optimal. This unified integration of CoT and ToT reasonings mimics human driver’s perception, anticipation, and evaluation of multiple future positions based on their safety, progress, and comfort to find the optimal trajectory [31]. 

To enable these reasoning abilities, HybridDriveVLA is trained on the nuScenes dataset [1]. We employ Supervised Fine-Tuning (SFT) for visual understanding and next scene generation to enable accurate V-CoT generation of future scenes. Then, Instruction Tuning (IT) to improve reason- 

32422 

ing efficiency, temporal coherence, and deliberative evaluation process within ToT-Evaluation by teaching HybridDriveVLA to learn multi-path planning and aspect-based evaluation effectively. We make the following contributions: 

- We propose HybridDriveVLA, an End-to-End VisionLanguage-Action framework that integrates both Visual Chain-of-Thought (V-CoT) and Tree-of-Thoughtinspired evaluation (ToT-Evaluation) reasoning for autonomous driving world-models. 

- We design ToT-Evaluation, a deliberative multi-waypoint evaluation module that scores multiple waypoint sequences based each on explicit safety, progress, or comfort aspects and selects the optimal sequence of waypoints with the highest cumulated score. 

- Experimental results demonstrated that HybridDriveVLA achieved strong performance on comfort, progress, and safety metrics on the nuScenes benchmark, outperforming traditional VLA models by achieving an average collision rate of 0.17%, demonstrating a significant improvement over existing models. 

## **2. Related Work** 

Our research is situated at the intersection of End-toEnd autonomous driving, large multimodal models as world models, future scene generation, and deliberative autonomous planning. This section reviews the key literature in these domains to contextualize the contributions of HybridDriveVLA. 

### **2.1. Vision-Language-Action Models in Driving** 

Recent advances in Large Multimodal Models (LMMs) have led to the emergence of Vision-Language-Action (VLA) frameworks for driving [19]. These models inherit strong reasoning and world-understanding capabilities from foundation models, enabling End-to-End perception and control. Early systems such as DriveGPT4 [26] demonstrated how multimodal models could generate textual driving rationales, while DriveVLM [23], DriveLM [20], and LingoQA [14] extended this idea by incorporating textual chain-of-thought (CoT) reasoning to justify high-level decisions. However, these text-based approaches introduce a modality gap, as visual and spatial information are discretized into tokens, leading to a loss of visual information. HybridDriveVLA diverges from these methods by performing reasoning entirely within the visual domain, thereby maintaining visual continuity and enabling interpretable deliberation. 

### **2.2. Chain-of-Thought and Tree-of-Thought Reasoning** 

Chain-of-Thought (CoT) prompting [32] has proven effective for structured reasoning in language models, and re- 

cent extensions into the visual domain [29] show promise for spatial reasoning tasks. In driving, however, CoT has been largely restricted to textual reasoning [16], limiting its ability to represent continuous scene evolution. Treeof-Thought (ToT) reasoning [27] further generalizes CoT by enabling multi-path exploration and self-evaluation, a paradigm inherently suited for rich driving contexts. HybridDriveVLA introduces a hybrid reasoning process that couples a Visual CoT for anticipatory next scene generation with an Evaluative ToT for multi-aspect waypoint deliberation, thus bridging visual prediction and action evaluation in a unified loop. 

### **2.3. Visual Prediction and End-to-End Planning** 

Future scene synthesis has become an emerging research frontier for autonomous driving. Generative models such as GAIA-1 [5] and DriveDreamer [25] can produce realistic future frames, yet they remain disconnected from downstream control. In parallel, End-to-End driving architectures like CIL [4], TransFuser [3], and UniAD [8] unify perception and planning but often lack explicit reasoning interpretability. HybridDriveVLA integrates its Visual Chainof-Thought (V-CoT) to perform next-frame anticipation as part of the reasoning process itself, while the Evaluative Tree-of-Thought (ToT-Evaluation) directly grounds this visual anticipation into aspect-aware waypoint selection. This synergy enables HybridDriveVLA to anticipate, deliberate, and act in a human-like reasoning loop. 

## **3. Methodology** 

The architecture of HybridDriveVLA is designed as a reasoning framework that integrates visual next scene generation and deliberative waypoint evaluation. As shown in Figure 3, HybridDriveVLA first encodes multi-modal driving inputs, performs Visual Chain-of-Thought (V-CoT) reasoning to predict the next scene visually, and subsequently applies a Tree-of-Thought-inspired waypoint evaluation (ToTEvaluation) mechanism to deliberate across multiple sequences of waypoints before selecting an optimal sequence. 

### **3.1. Overview** 

**Inputs.** At a current time _t_ , HybridDriveVLA re= ceives a set of synchronized multi-view images _It {i_<sup>1</sup> _t_<sup>_, i_2</sup> _t_<sup>_, . . . , ih_</sup> _t_<sup>_}_,theego-vehiclestate</sup><sup>_lt_,anavigational</sup> command _ct_ , an instruction _ot_ and evaluation aspect _E_ = _{e_<sup>_safety_</sup> _, e_<sup>_progress_</sup> _, e_<sup>_comfort_</sup> _}_ . 

**Backbone VLA model.** HybridDriveVLA builds upon a pre-trained backbone Vision-Language-Action (VLA) model _M_ constituted of a vision encoder with a projector, a text tokenizer, and a text detokenizer. At the current time step _t_ , HybridDriveVLA reasons using all inputs to 

32423 


Figure 3. HybridDriveVLA architecture integrates a Vision Encoder, Language Model, MoVQGAN encoder-decoder for multimodal reasoning. Inputs include multi-view images, ego states, navigational commands, instructions, and evaluation aspects (Safety, Progress, Comfort) processed in Text Detokenizer. HybridDriveVLA outputs next scene images using MoVQGAN Decoder and sequences of waypoints as actions using a Text Detokenizer. 

predict and generate autoregressively next scene output image tokens. These tokens are decoded into images using a VQGAN Decoder _Dgan_ [30] to obtain the next scene image output, used as a goal to predict _n_ multi-waypoint sequences outputs _A_<sup>_n_</sup> , and each waypoint set of scores _St_<sup>_n_</sup> + _kα_<sup>=</sup><sup>_{sn,safety_</sup> _t_ + _kα , s_<sup>_n,progress_</sup> _t_ + _kα , s_<sup>_n,comfort_</sup> _t_ + _kα }_ . **Outputs.** Conditioned on textual input features, the backbone VLA model _M_ in HybridDriveVLA generates autoregressively the next scene image _I_<sup>ˆ</sup> _t_ +6 _α_ , and a multisequence waypoints _A_<sup>_n_</sup> with each waypoint set of scores _St_<sup>_n_</sup> + _kα_<sup>where</sup><sup>_n_isawaypointindexattimestep</sup><sup>_t_+</sup><sup>_kα_,</sup> _k_ is prediction step, and _α_ is a prediction interval between consecutive waypoints. 

### **3.2. Visual Chain-of-Thought (V-CoT)** 

The Visual Chain-of-Thought (V-CoT) reasoning enables HybridDriveVLA to anticipate future scene images before planning. Unlike conventional text-based reasoning, V-CoT unfolds entirely in the visual domain, generating structured visual predictions that reflect how a human driver mentally simulates the next maneuver. Starting from the input features, HybridDriveVLA autoregressively generate next scene representation, and uses that generated representation to plan multiple waypoint sequences and their scores as a unique autoregressive sequence _zi_ . To incorporate explicit visual reasoning before actions generation, Hybrid- 

DriveVLA first anticipates the next scene image at _t_ + 6 _α_ as a goal image: 


where _M_ denotes the backbone VLA. To enable predictive visual reasoning, the Visual Chain-of-Thought (V-CoT) is trained to reconstruct the next scene representation from discrete visual tokens autoregressively. During training, HybridDriveVLA minimizes the divergence between the predicted _I_<sup>ˆ</sup> _t_ +6 _α_ and a ground-truth _It_ +6 _α_ . Each predicted next scene image _I_<sup>ˆ</sup> _t_ +6 _α_ is represented as a sequence of _d_ discrete tokens, where _σ_ = 512 is the fixed dimension of the VQGAN Encoder. Let _{q_ 1 _, . . . , qσ}_ be the sequence of VQGAN-encoded visual tokens representing a ground-truth future scene _I_<sup>ˆ</sup> _t_ +6 _α_ . Given the preceding tokens the model predicts the conditional probability of the next token using _M_ . The training objective for the visual reasoning V-CoT is to minimise _LV_ -CoT defined as: 


where _qd_ denotes the ground-truth visual token at position _d_ , and _θ_ represents HybridDriveVLA parameters. Through this process, HybridDriveVLA learn visual next scenes images prediction and maintain temporal coherence across visual scenes. 

32424 

### **3.3. Tree-of-Thought-Evaluation (ToT-Evaluation)** 

While V-CoT anticipates a visual goal image _I_<sup>ˆ</sup> _t_ +6 _α_ , ToTEvaluation deliberates on the optimal sequence of waypoints to achieve it. Instead of predicting a single path, this module generates a set of _N_ candidate sequences of waypoints. Let _A_<sup>_n_</sup> = _{a_<sup>_n_</sup> _t_ + _α_<sup>_, an_</sup> _t_ +2 _α_<sup>_, . . . , a_</sup> _t_<sup>_n_</sup> +6 _α_<sup>_}_bethe</sup><sup>_n_-th</sup> sequence of waypoints, where _n ∈{_ 1 _, . . . , N }_ . For each waypoint _a_<sup>_n_</sup> _t_ + _kα_<sup>withinasequence,HybridDriveVLAalso</sup> predicts corresponding aspects set of scores _St_<sup>_n_</sup> + _kα_<sup>.The</sup> generation of all sequences and the scores of each waypoint is conditioned on the current state and a visual scene goal provided by V-CoT: 


where _S_<sup>_n_</sup> represents the set of scores for a unique waypoint _a_<sup>_n_</sup> _t_ + _kα_<sup>inthesequence</sup><sup>_An_.Duringtraining,Hybrid-</sup> DriveVLA learns to predict these sequences and scores. At inference time, the optimal sequence of waypoints, _A_<sup>_∗_</sup> , is selected by identifying waypoints with the highest cumulative score across all aspects and time steps. We define a total score of a waypoint at _k_ as: 


with _j ∈{_ safety _,_ progress _,_ comfort _}_ . The index of the optimal waypoint, _n_<sup>_∗_</sup> at _t_ + _kα_ is then obtained by: 


This deliberation process, which is a reasoning-based beam search [15] where each node is a waypoint, enables HybridDriveVLA to reason beyond single-path to adaptively evaluate and select the most efficient waypoints. The training objective for this module, _L_ ToT-Eval, maximizes the log-probability of generating the ground-truth sequences of waypoints and each of these waypoints scores autoregressively. The objective is formulated as: 


This ensures that the predicted waypoints and their evaluations are temporally consistent. The total training objective for HybridDriveVLA combines both reasoning losses: 


This composite objective jointly optimizes visual prediction and evaluative planning, ensuring that the anticipated goals and the sequences of waypoints remain consistent. 

### **3.4. Supervised Fine-Tuning** 

HybridDriveVLA is first trained through Supervised FineTuning (SFT) to solidify its foundational visual reasoning and predictive abilities. Initialized from a large-scale VLA model, HybridDriveVLA is fine-tuned on paired samples of multi-view inputs, scene annotations, and corresponding next scene images. During SFT, both the next scene prediction objective and multiple waypoint sequences are optimized jointly. This dual-stage optimization enables HybridDriveVLA to learn causal visual-to-action dependencies and strengthen temporal coherence between scene synthesis and trajectory planning. During this phase, HybridDriveVLA is optimized to enhance the next scene generation and planning by minimizing _LHybridDriveV LA_ This unified design ensures consistent grounding between perception, prediction, and planning within a single generative reasoning stream. This process enables accurate reconstruction of lane layouts, object positions, and temporally coherent next-frame scenes. It also aligns the visual and linguistic token spaces, allowing HybridDriveVLA to reason spatially using the same sequential logic applied in text-based generative models. 

### **3.5. Instruction Tuning** 

After SFT, HybridDriveVLA undergoes Instruction Tuning to enhance interpretability, reasoning flexibility, and deliberation. HybridDriveVLA is trained on a visualinstruction corpus derived from nuScenes driving datasets, where each instance pairs a visual context with naturallanguage prompts guiding multi-step reasoning and evaluation. By conditioning our model on such prompts, HybridDriveVLA learns to generate reasoning-consistent multiple waypoint sequences and generate next scenes by minimizing _LHybridDriveV LA_ . This phase refines the ToTEvaluation’s performance, teaching HybridDriveVLA to refine its internal deliberations and to maintain coherent reasoning across time. While SFT teaches HybridDriveVLA to predict and plan through visual anticipation, Instruction Tuning extends this capability to reasoning under each aspect, transforming visual-driven prediction into deliberative planning 

### **3.6. Dataset Construction** 

To effectively train and evaluate the hierarchical reasoning capabilities of HybridDriveVLA, we construct two complementary datasets derived from the large-scale nuScenes [1] benchmark. Each dataset is designed to support a specific training stage, corresponding respectively to supervisedfine-tuning for visual generation and instruction-tuning reasoning. 

**nuScenes Overview.** The nuScenes dataset provides rich multimodal driving data, including 1,000 driving sequences (each approximately 20 seconds long) captured using a 360° 

32425 

camera suite and LiDAR sensors. It contains 28,130 training and 6,019 validation samples, each annotated with egovehicle states, object bounding boxes, and scene-level metadata. We leverage this dataset to construct training pairs that align with the reasoning and evaluative objectives of HybridDriveVLA. 

**Supervised-Fine-Tuning Visual Generation Dataset.** This dataset supports the Visual Chain-of-Thought (VCoT) training phase, which focuses on autoregressive future scene generation. For each temporal pair ( _t, t_ +6 _α_ ), we extract the multi-view camera frames _It_ and their corresponding future frame _It_ +6 _α_ , where _t_ + 6 _α_ denotes the prediction horizon. Each future scene image is tokenized via a pretrained MoVQGAN encoder [30], producing discrete visual tokens. Training samples take the form of prompt–response pairs where the input prompt includes _I_<sup>ˆ</sup> _t_ and a concise instruction (e.g., _“Given ego position, speed, previous trajectory, actual scene image, Generate the next scene view 3s seconds ahead.”_ ), while the response is a serialized sequence of ground truth visual tokens for _It_ +6 _α_ . This stage allows HybridDriveVLA to internalize visual causality and learn temporally consistent scene evolution. 

**Instruction-Tuning Reasoning Dataset.** We construct an instruction tuning dataset by templating visual-language pairs with scene descriptions and aspect evaluation prompts derived from nuScenes metadata. This dataset targets the joint reasoning and deliberation abilities central to HybridDriveVLA’s architecture. Each sample contains a structured prompt combining the current camera view _It_ and recent ego-vehicle trajectory history, a navigational command (LEFT, RIGHT, FORWARD), and aspects _E_ specifying driving priorities and the predicted future scene _I_<sup>ˆ</sup> _t_ +6 _α_ The corresponding response contain ground truth _N_ sequences of waypoint at each _t_ + _kα_ associate with scores for safety, progress, and comfort. Each waypoint in the response is annotated with its ground-truth aspect score vector **s** _t_ + _kα_ computed in Section 3 following prior work on nuScenes [8], ensuring interpretable supervision. To generate the ground truth scores for training the ToT-Evaluation module, we normalize the ground truth waypoints at each step _t_ + _kα_ based on the nuScene dataset statistics. Let _s_<sup>_safety_</sup> _t_ + _kα_<sup>,</sup><sup>_scomfort_</sup> _t_ + _kα_ , and _s_<sup>_progress_</sup> _t_ + _kα_ be the ground truth scores at _t_ + _kα_ . These are computed as follows: 

- **Safety score:** At each time _t_ + _kα_ , let _dt_ + _kα_ be the minimum Euclidean distance from the ego-vehicle to any other object. Over the dataset, _d_<sup>min</sup> and _d_<sup>avg</sup> . The score _s_<sup>_safety_</sup> _t_ + _kα_ is normalized linearly, mapping _d_<sup>_min_</sup> to the lowest safety score and _d_<sup>_avg_</sup> to the maximum safety: 


Where higher values corresponding to high safety. 

- **Comfort score:** At each time _t_ + _kα_ , let _ct_ + _kα_ denote the 

steering rate of the ego-vehicle. Across the dataset, define _c_<sup>min</sup> and _c_<sup>avg</sup> . The comfort score _s_<sup>comfort</sup> _t_ + _kα_<sup>isnormalized</sup> such that _c_<sup>min</sup> maps to the highest comfort and _c_<sup>avg</sup> to the lowest comfort: 


Where higher values corresponding to smoother and more comfortable driving dynamics. 

- **Progress score:** At each time _t_ + _kα_ , let _vt_ + _kα_ be the speed of the ego-vehicle. Over the dataset, let _v_<sup>min</sup> and _v_<sup>avg</sup> . The progress score _s_<sup>progress</sup> _t_ + _kα_ is normalized such that _v_<sup>min</sup> maps to the lowest progress and _v_<sup>avg</sup> to the highest progress: 


These scores are used at each instant as the ground-truth targets for the score _s_<sup>_n,j_</sup> _t_ + _kα_<sup>thattheToT-Evaluationlearns</sup> to predict. This dataset enables HybridDriveVLA to align predictive visual reasoning with multi-aspect evaluation. 

## **4. Experiments** 

**Evaluation Metrics:** We report the following metrics under both the per-timestep style of UniAD [8] and the averaged style of ST-P3 [7] for comprehensive comparison. 

- L2 Displacement Error (m): The Euclidean distance between the predicted and ground-truth waypoints. 

- Collision Rate (%): The percentage of predicted trajectories that result in a collision with scene obstacles. 

- UniAD Metrics: We evaluate planning performance with per-timestep and overall L2 error and collision rates, using the official validation protocol. 

- ST-P3 Metrics: We compute the average L2 error and collision rate across all future waypoints for a fair comparison with prior work. 

For the NAVSIM benchmark, we report the standard metrics, where higher is better for all: 

- PDMS: The Planning Diversity and Motion Sickness score, which evaluates the quality and realism of the driving behavior. 

- Collision: The collision-free rate. 

- Area, Direction, Progress: Metrics measuring adherence to drivable areas, heading, and goal progress. 

- TTC: Time-to-Collision, a key safety metric. 

- Comfort: A score reflecting the smoothness of the trajectory (e.g., low jerk and acceleration). 

- **Implementation Details:** Our HybridDriveVLA was built upon the Qwen2-VL-2B model [22]. During supervised fine-tuning our model was trained for 20 epochs with a learning rate of 1 _._ 0 _×_ 10<sup>_−_4</sup> , a batch size of 8 per device, and 

32426 

|||||**ST-P3**|**Metrics**|||||||**UniAD**|**Metrics**|||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**||**L2 (**|**m)**_↓_|||**Collisio**|**n (%)**|_↓_||**L2 (**|**m)**_↓_|||**Collisio**|**n (%)**|_↓_|**Model**|
||1s|2s|3s|Avg.|1s|2s|3s|Avg.|1s|2s|3s|Avg.|1s|2s|3s|Avg.||
|||||||**_Non-_**|**_Autoreg_**|**_ressive M_**|**_ethods_**|||||||||
|ST-P3 [7][ECCV 2022]|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|–|–|–|–|–|–|–|–|–|
|VAD [9][ICCV 2023]|0.17|0.34|0.60|0.37|0.07|0.10|0.24|0.14|–|–|–|–|–|–|–|–|–|
|UniAD [8][CVPR 2023]|0.44|0.67|0.96|0.69|0.04|0.08|0.23|0.12|0.48|0.96|1.65|1.03|0.05|0.17|0.71|0.31|–|
|GenAD [31][CVPR 2024]|0.28|0.49|0.78|0.52|0.08|0.14|0.34|0.19|–|–|–|–|–|–|–|–||
|||||||**_Au_**|**_toregres_**|**_sive Met_**|**_hods_**|||||||||
|OminiDrive [24][CVPR 2025]|0.40|0.80|1.32|0.84|0.04|0.46|2.32|0.94|–|–|–|–|–|–|–|–|LLaVA-7B|
|DriveVLM [23][arXiv 2024]|0.18|0.34|0.68|0.40|0.10|0.22|0.45|0.27|–|–|–|–|–|–|–|–|Qwen-VL-7B Visual|
|RDA-Driver [18][ECCV 2024]|0.17|0.37|0.69|0.40|**0.01**|**0.05**|0.26|**0.10**|0.23|0.73|1.54|0.80|0.00|0.13|0.83|0.32|LLaVa-7B|
|GPT-Driver [13][NeurIPS 2023]|0.20|0.40|0.70|0.44|0.04|0.12|0.36|0.17|0.27|0.74|1.52|0.84|0.07|0.15|1.10|0.44|GPT-3.5|
|OpenDriveVLA [32][arxiv 2024]|**0.14**|0.30|0.55|0.33|0.02|0.07|**0.22**|**0.10**|0.19|0.58|1.24|0.67|**0.02**|0.18|0.70|0.30|Qwen2.5-3B|
|HybridDriveVLA (ToT-Evaluation)|**0.14**|0.37|0.41|0.30|0.09|0.12|0.27|0.16|0.23|0.38|0.61|0.40|0.09|0.25|0.57|0.30|Qwen2-VL-2B|
|HybridDriveVLA(Full)|0.19|**0.24**|**0.36**|**0.26**|0.04|0.16|0.24|0.14|**0.18**|**0.34**|**0.43**|**0.31**|0.06|**0.08**|**0.45**|**0.19**|Qwen2-VL-2B|


Table 1. Trajectory planning on the nuScenes validation set. 

|**Method**|**PDMS**_↑_|**Collision**_↑_|**Area**_↑_|**Direction**_↑_|**Progress**_↑_|**TTC**_↑_|**Comfort**_↑_|
|---|---|---|---|---|---|---|---|
|TransFuser [3]|83.88|97.78|92.63|97.97|78.88|92.89|99.98|
|DRAMA [12]|86.87|98.19|95.18|**98.03**|81.33|94.17|**100.00**|
|Hydra-MDP [11]|91.26|99.07|98.29|95.79|85.20|96.56|**100.00**|
|Centaur [21]|92.10|99.23|**98.72**|96.77|85.96|97.17|99.97|
|TrajHF [10]|93.95|99.30|97.51|91.72|90.39|98.02|99.81|
|AutoVLA [33][NeurIPS 2025]|92.12|99.14|97.08|95.51|87.55|97.12|99.98|
|HybridDriveVLA (Safety)|**94.89**|**99.62**|97.69|97.50|**92.74**|98.73|97.91|
|HybridDriveVLA (Comfort)|91.73|92.75|96.41|97.31|91.34|94.18|97.72|
|HybridDriveVLA (Progress)|93.12|90.75|93.41|97.31|96.82|97.18|92.53|
|HybridDriveVLA (Optimal)|94.62|97.63|96.38|95.43|96.56|**99.42**|96.85|


Table 2. Testing Results on the NAVSIM Benchmark 

16 gradient accumulation steps to learn visual token generation. Then during instruction tuning, we trained HybridDriveVLA for 20 epochs with the same configuration using LoRA [6]. Key hyperparameters included a waypoint prediction interval _α_ of 0.5s, and a cosine learning rate scheduler. The vision tower of the backbone Language model was kept frozen throughout this instruction tuning to preserve its learned features, while the language model and LoRA adapters were updated. For visual tokenization, we utilized a pre-trained MoVQGAN. 

### **4.1. Main Results** 

Table 1 showed the trajectory planning performance of HybridDriveVLA on the nuScenes validation dataset. Our model demonstrated state-of-the-art performance among language model-based autoregressive methods, particularly in reducing collision rates. When compared to other autoregressive models like DriveVLM and OpenDriveVLA, HybridDriveVLA achieved a significant reduction in collisions under both ST-P3 and UniAD metrics. For instance, our final model, HybridDriveVLA (CoT + ToT), achieved an average collision rate of 0.17% (ST-P3) and 0.19% (UniAD). This result is highly competitive even with nonautoregressive methods and highlights the effectiveness of 

our V-CoT and ToT-Evaluation reasoning, which allowed the HybridDriveVLA to anticipate next scene images and deliberate on optimal trajectories. The low L2 error further confirmed the planning accuracy. 

### **4.2. Ablation Studies** 

We conducted ablation studies to validate the core components of HybridDriveVLA. All ablations used UniAD-style metrics and excluded ego vehicle states unless specified. Table 2 showcased our model’s ability to adapt its driving style based on the prioritized aspect of the NAVSIM benchmark. When guided to prioritize Safety, the model achieved the highest Time-to-Collision (TTC) score of 98.73, indicating safer behavior. When focused on comfort, it yields the best Comfort score of 97.72. The Optimal sequence, which balances all aspects, achieved a strong overall PDMS score of 94.62 and a high collision-free rate of 97.63. This confirms that our ToT-Evaluation successfully evaluates the waypoints in an interpretable manner. To quantify the impact of our reasoning components, we analyzed the results in Table 1. HybridDriveVLA (ToT-Evaluation) model, which performs deliberation without visual anticipation from V-CoT, achieves an average collision rate of 0.23% on the ST-P3 benchmark. By integrating V-CoT, our 

32427 


Figure 4. Qualitative analysis of HybridDriveVLA on the nuScenes dataset. The red trajectory is the predicted optimal sequence of waypoints, and the green is the ground truth. 

full HybridDriveVLA model reduced this collision rate to 0.17%, a relative improvement of 26%. This result empirically proved that while deliberative evaluation was effective on its own, its performance has significantly enhanced when grounded to an anticipated future visual scene. It confirmed that V-CoT and ToT-Evaluation are complementary and crucial for achieving efficiency. 

**Qualitative Analysis.** In Table 1, HybridDriveVLA (vToT), which represents training without the initial SFT stage for V-CoT, has a significantly higher collision rate of 0.23% for ST-P3 compared to the full HybridDriveVLA that had 0.17% for ST-P3. This demonstrated that equipping the model with an understanding of visual scenes via SFT was critical before it can effectively reason and deliberate during instruction tuning. Figure 4 provided qualitative examples of HybridDriveVLA’s deliberative process. In Figure 4 scenario, a direct path following the command without deliberative evaluation leads to a potential conflict with another vehicle. The baseline model, lacking deliberation, committed to this dangerous trajectory. In contrast, HybridDriveVLA’s ToT-Evaluation generated and evaluated multiple trajectories and correctly assigned a lower score to the unsafe, uncomfortable and unprogressive waypoints and selected an optimal sequence of waypoints, showcasing its ability to navigate complex interactions through deliberative reasoning. 

## **5. Conclusion** 

In this paper, we introduced HybridDriveVLA, a novel Vision-Language-Action model designed to address limitations in current autonomous driving models. We identified that traditional VLA models relied on Text-to-Image reasoning, leading to visual information under-usage. They also just predict a single sequence of waypoints as a trajectory, considering simultaneously multiple aspects. To overcome these challenges, we proposed a paradigm shift inspired by human cognition, integrating in a baseline VLA model a Visual Chain-of-Thought (V-CoT) and a ToTinspired evaluation (ToT-Evaluation) to reveal the importance of each aspect. Through extensive experiments on the nuScenes benchmark, we demonstrated that Hybrid- 

DriveVLA achieves state-of-the-art performance among autoregressive VLA models. Most notably, it reduces the average collision rate to 0.17%, confirming that the generation of visual next scenes as goal and a deliberative evaluation to reveal the importance of driving aspects is crucial for autonomous driving systems. Our ablation studies further validated the effectiveness of our approach, confirming that the integration of V-CoT and ToT-Evaluation improves the reliability of autonomous driving systems. 

## **6. Acknowledgement** 

This research was supported by the ”Regional Innovation System & Education (RISE)” through the Seoul RISE Center, funded by the Ministry of Education (MOE) and the Seoul Metropolitan Government. (2026-RISE-01-00704) and the National Research Foundation of Korea(NRF) grant funded by the Korea government(MSIT) (RS-202516068981). 

## **References** 

- [1] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11621–11631, 2020. 2, 5 

- [2] Long Chen, Oleg Sinavski, Jan H¨unermann, Alice Karnsund, Andrew James Willmott, Danny Birch, Daniel Maund, and Jamie Shotton. Driving with llms: Fusing object-level vector modality for explainable autonomous driving. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 14093–14100. IEEE, 2024. 2 

- [3] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE transactions on pattern analysis and machine intelligence_ , 45(11):12878–12895, 2022. 3, 7 

- [4] Felipe Codevilla, Matthias M¨uller, Antonio L´opez, Vladlen Koltun, and Alexey Dosovitskiy. End-to-end driving via conditional imitation learning. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 4693– 4700. IEEE, 2018. 3 

32428 

- [5] Anthony Hu, Lloyd Ling, Soroush Goli, Brandon Chen, and Alexander Tontsch. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 3 

- [6] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 7 

- [7] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _European Conference on Computer Vision_ , pages 533–549. Springer, 2022. 6, 7 

- [8] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 17853–17862, 2023. 3, 6, 7 

- [9] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8340–8350, 2023. 7 

- [10] Derun Li, Jianwei Ren, Yue Wang, Xin Wen, Pengxiang Li, Leimeng Xu, Kun Zhan, Zhongpu Xia, Peng Jia, Xianpeng Lang, et al. Finetuning generative trajectory model with reinforcement learning from human feedback. _arXiv preprint arXiv:2503.10434_ , 2025. 7 

- [11] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, et al. Hydra-mdp: End-to-end multimodal planning with multitarget hydra-distillation. _arXiv preprint arXiv:2406.06978_ , 2024. 7 

- [12] Srikanth Malla, Chiho Choi, Isht Dwivedi, Joon Hee Choi, and Jiachen Li. Drama: Joint risk localization and captioning in driving. In _Proceedings of the IEEE/CVF winter conference on applications of computer vision_ , pages 1043–1052, 2023. 7 

- [13] Jiageng Mao, Yuxi Qian, Junjie Ye, Hang Zhao, and Yue Wang. Gpt-driver: Learning to drive with gpt. _arXiv preprint arXiv:2310.01415_ , 2023. 2, 7 

- [14] Ana-Maria Marcu, Long Chen, Jan H¨unermann, Alice Karnsund, Benoit Hanotte, Prajwal Chidananda, Saurabh Nair, Vijay Badrinarayanan, Alex Kendall, Jamie Shotton, et al. Lingoqa: Visual question answering for autonomous driving. In _European Conference on Computer Vision_ , pages 252–269. Springer, 2024. 3 

- [15] Clara Meister, Tim Vieira, and Ryan Cotterell. Best-first beam search. _Transactions of the Association for Computational Linguistics_ , 8:795–809, 2020. 5 

- [16] Long Nie, Yuxuan Li, Yifeng Chen, Linfeng Xu, and An Liu. Driving with llms: Fusing object-level vector modality for explainable autonomous driving. _arXiv preprint arXiv:2402.15934_ , 2024. 3 

- [17] Yunpeng Pan, Ching-An Cheng, Kamil Saigol, Keuntaek Lee, Xinyan Yan, Evangelos Theodorou, and Byron Boots. 

   - Agile autonomous driving using end-to-end deep imitation learning. _arXiv preprint arXiv:1709.07174_ , 2017. 2 

- [18] Shuofei Qiao, Honghao Gui, Chengfei Lv, Qianghuai Jia, Huajun Chen, and Ningyu Zhang. Making language models better tool learners with execution feedback. _arXiv preprint arXiv:2305.13068_ , 2023. 7 

- [19] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 11993– 12003, 2025. 3 

- [20] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Jens Beißwenger, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with graph visual question answering. In _European conference on computer vision_ , pages 256–274. Springer, 2024. 3 

- [21] Chonghao Sima, Kashyap Chitta, Zhiding Yu, Shiyi Lan, Ping Luo, Andreas Geiger, Hongyang Li, and Jose M Alvarez. Centaur: Robust end-to-end autonomous driving with test-time training. _arXiv preprint arXiv:2503.11650_ , 2025. 7 

- [22] Qwen Team et al. Qwen2 technical report. _arXiv preprint arXiv:2407.10671_ , 2(3), 2024. 6 

- [23] et al. Tian, Xiaoyu. Drivevlm: The convergence of autonomous driving and large vision-language models. _arXiv preprint arXiv:2402.12289_ , 2024. 3, 7 

- [24] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M Alvarez. Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22442–22452, 2025. 7 

- [25] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-worlddrive world models for autonomous driving. In _European conference on computer vision_ , pages 55–72. Springer, 2024. 3 

- [26] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _IEEE Robotics and Automation Letters_ , 2024. 3 

- [27] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. _Advances in neural information processing systems_ , 36:11809–11822, 2023. 3 

- [28] Zhuosheng Zhang, Aston Zhang, Mu Li, Hai Zhao, George Karypis, and Alex Smola. Multimodal chain-ofthought reasoning in language models. _arXiv preprint arXiv:2302.00923_ , 2023. 2 

- [29] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 3 

32429 

- [30] Chuanxia Zheng, Tung-Long Vuong, Jianfei Cai, and Dinh Phung. Movq: Modulating quantized vectors for highfidelity image generation. pages 23412–23425, 2022. 4, 6 

- [31] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. pages 87–104, 2024. 2, 7 

- [32] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C Knoll. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. _arXiv preprint arXiv:2503.23463_ , 2025. 2, 3, 7 

- [33] Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A visionlanguage-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025. 7 

- [34] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 2 

32430 

