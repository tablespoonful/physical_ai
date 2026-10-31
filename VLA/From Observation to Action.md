---
title: "From Observation to Action: Latent Action-based Primitive Segmentation for VLA Pre-training in Industrial Settings"
date: "2025-11-26"
authors: "Jiajie Zhang; Sören Schwertfeger; Alexander Kleiner"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.21428
pdf: https://arxiv.org/pdf/2511.21428
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.21428)** / [論文ページ](https://arxiv.org/abs/2511.21428)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **From Observation to Action: Latent Action-based Primitive Segmentation for VLA Pre-training in Industrial Settings** 

Jiajie Zhang S¨oren Schwertfeger School of Information Science and Technology ShanghaiTech University, Shanghai, China 

_{_ zhangjj2023, soerensch _}_ @shanghaitech.edu.cn 

Alexander Kleiner School of Automation Hangzhou Dianzi University, China 

alexander.kleiner@gmail.com 

https://jiajiezhang7.github.io/latent-action-primitive-segmenter/ 

## **Abstract** 

_We present a novel unsupervised framework to unlock vast unlabeled human demonstration data from continuous industrial video streams for Vision-Language-Action (VLA) model pre-training. Our method first trains a lightweight motion tokenizer to encode motion dynamics, then employs an unsupervised action segmenter leveraging a novel ”Latent Action Energy” metric to discover and segment semantically coherent action primitives. The pipeline outputs both segmented video clips and their corresponding latent action sequences, providing structured data directly suitable for VLA pre-training. Evaluations on public benchmarks and a proprietary electric motor assembly dataset demonstrate effective segmentation of key tasks performed by humans at workstations. Further clustering and quantitative assessment via a Vision-Language Model confirm the semantic coherence of the discovered action primitives. To our knowledge, this is the first fully automated end-to-end system for extracting and organizing VLA pre-training data from unstructured industrial videos, offering a scalable solution for embodied AI integration in manufacturing._ 

## **1. Introduction** 

The pursuit of developing generalist agents, frequently embodied as Vision-Language-Action (VLA) models, constitutes a major objective within the robotics research community [2, 3, 32]. Pre-training these models on large-scale, diverse datasets, encompassing human video recordings [15] and robot trajectories from multiple embodiments [23], has proven crucial for enabling strong generalization and reliable instruction-following performance. Applying this approach for real-world deployment encounters a fundamental problem: the scarcity of training data. In contrast to the vast amounts of text and images available on the Internet, obtaining high-quality action-annotated robot data remains 


Figure 1. Example of our segmentation approach using _Latent Action Energy_ from a _Motion Tokenizer_ . Action boundaries (red circles) correspond to transitions from high energy to baseline, indicating action completion. The pipeline outputs the _Latent Action Sequence_ (bottom codes), providing structured representations for VLA pre-training. 

challenging and costly and typically necessitating expensive teleoperation [1, 17]. 

Our work focuses on the manufacturing domain, specifically on industrial environments characterized by constrained operational spaces where meaningful human actions comprise a finite, well-defined set. We introduce a fully unsupervised system that is able to extract a core ”vocabulary” of actions through passive observation. Many state-of-the-art VLA pretraining strategies [1, 2] adopt a hierarchical framework: (1) a high-level generalist module that encodes arbitrary action sequences into abstract latent action tokens, and (2) a low-level controller for task execution that is subsequently fine-tuned through supervised learning on these token sequences [9, 30]. Our work focuses on training the high-level generalist module, which shifts the data bottleneck earlier by requiring large collections of pre-segmented video clips paired with latent token sequences from curated datasets [15]. We are tackling the key challenge on how to automatically extract structured data from vast, unstructured video streams found online and in industrial settings. 

6750 

We are presenting a solution that allows robots to learn like humans through continuous, self-directed observation of actions and behaviors [3]. To this end, we introduce a novel unsupervised framework for automatically discovering and segmenting action primitives from continuous video streams. Our method first trains a lightweight motion tokenizer to encode motion dynamics, then employs an unsupervised action segmenter leveraging a novel metric named _Latent Action Energy_ to discover and segment semantically coherent action primitives. The pipeline outputs both segmented video clips and their corresponding latent action sequences, providing structured data directly suitable for VLA pre-training (see Figure 1). Our main contributions are summarized as follows: 

- We introduce a novel segmentation approach based on _Latent Action Energy_ , a metric defined in the abstract latent action space, to identify semantic action primitives from raw video data. This differs from conventional methods that focus on pixel-level or optical flow changes [12]. 

- We present an _end-to-end automated data pipeline_ that transforms hours-long industrial video footage into a structured repository of action primitives. This directly addresses the data sourcing bottleneck for industrial Vision-Language-Action (VLA) latent pretraining. 

- We are the first to validate this VLA data-sourcing methodology on publicly available benchmark datasets and a genuine and complex industrial data set from an assembly line. Section 4 provides strong quantitative and qualitative evidence demonstrating its practical feasibility and scalability. 

## **2. Related Work** 

Our research is positioned at the intersection of generalist robot policies, latent action representation, and unsupervised action segmentation from video, with a specific focus on industrial applications. In this section, we review the state-of-the-art in these areas to highlight the gap our work aims to fill. 

**Generalist Robot Policies.** The development of generalist robot policies is based on Vision-Language-Action (VLA) models [5, 18, 32], which are large-scale foundation models trained on web-scale data combined with action modalities for robot control. Notable examples include GR00T [2] and AgiBot GO-1 [1], both of which have recently made significant advances. To ensure that these models generalize over various tasks, they must be trained on huge amounts of heterogeneous data [15, 23]. However, this approach encounters a significant bottleneck since it requires a large dataset of _pre-segmented, action-labeled_ video clips, which are usually obtained through expensive teleoperation [1, 17]. 

**Latent Action Representation from Video Data.** A 

key strategy to overcome the labeled data bottleneck is to learn action priors from video data by leveraging _latent action representations_ , an abstract, embodiment-agnostic space for modeling behaviors [10]. Early pioneering works including LAPO and LAPA have demonstrated the effectiveness of latent action learning [26, 30]. Nevertheless, both approaches depend on pixel-level objectives, including next-frame prediction for simple game actions in LAPO and VQ-VAE-based reconstruction in LAPA. This can lead to capturing action-irrelevant background noise and may provide limited descriptive capacity. Importantly, these successful techniques typically assume access to curated short video clips (e.g., Ego4D [15]), and do not address the upstream challenge of discovering and segmenting action primitives from continuous video streams [1, 2]. Our work is unique in that it capitalizes on the utility of latent action representations while re-purposing them for identifying temporal boundaries of action primitives themselves. As described in the latter sections, this is carried out by utilizing keypoint-based dynamics [16] with a motion tokenizer [10]. Similarly, the recent Magma foundation model [29] leverages keypoint tracking (Trace-of-Mark) to extract motion trajectories for large-scale video data curation. However, while Magma utilizes these physical traces as surrogate action supervisions on pre-segmented clips, our pipeline distinctively projects motion dynamics into a latent space to automatically discover and segment the semantic boundaries of action primitives from unsegmented continuous streams. 

**Unsupervised Action Segmentation.** The task of Temporal Action Detection (TAD), which involves identifying the boundaries between actions, is commonly addressed using local boundary detectors [12]. While fully-supervised [27] and weakly-supervised [28], e.g., transcript-based methods, provide efficient architectures and alignment strategies, our approach operates in a completely unsupervised manner, requiring no labels. Unsupervised techniques such as ABD [13] detect change-points by locating local minima in the similarity of visual features, but they are often sensitive to non-semantic physical changes like lighting variations. More sophisticated methods like OTAS [20] address this issue by combining explicit features, for instance, by using object detectors and Graph Neural Networks (GNNs), which introduce significant complexity. Our method introduces for action primitive discovery a fundamentally different method based on _Latent Action Energy_ that is derived from the _latent action space_ of a VLA-oriented Motion Tokenizer. Instead of detecting visual similarity valleys or fusing object features, we identify primitives through sustained high-energy activations, implicitly capturing semantic motion without object detectors. This shift from ”visual change detection” to ”behavioral intent change detection” directly addresses the need for VLA 

6751 

pre-training data. 

**Robot Learning in Industrial Environments.** Prior work on generalist robots has predominantly focused on home and laboratory settings [3, 17] with diverse and unstructured task distributions. Industrial environments, however, present a distinct and highly valuable domain [4], characterized by structured, repetitive workflows and a finite, countable set of skilled actions. While large-scale efforts like AgiBot World [1] have begun to include industrial scenarios, the data remains primarily sourced through manual teleoperation. Our work specifically targets on this high-impact domain. By leveraging the inherent structured nature of industrial environments, we develop an automated VLA-centric data pipeline that can autonomously discover the complete ”action vocabulary” of workstations through passive observation. This approach offers a scalable solution for deploying and continuously enhancing VLA models within real-world manufacturing settings. 

## **3. System Methodology** 

Our system introduces a fully unsupervised pipeline that transforms continuous, unlabeled industrial video streams into a structured repository of action primitives suitable for VLA pre-training. Figure 2 depicts the LAPS (Latent Action-based Primitive Segmentation) pipeline which processes data through three sequential stages: (1) _Motion Tracking_ : Using point trackers such as CoTracker [16], dense motion trajectories are extracted from raw video streams and stored in a sliding window buffer of motion keypoints. (2) _Action Detection & Segmentation_ : The keypoints from the sliding window are fed into a motion tokenizer that generates a continuous _Latent Action Vector Stream_ . An action detector applies a hysteresis-based controller to this stream using our novel _Latent Action Energy_ metric to identify sustained action activations. The primitive segmentor then uses these detected activations to locate action boundaries and to extract action primitives consisting of _Segmented Latent Vectors_ along with their corresponding video clips and action codes. (3) _Semantic Action Clustering_ : The identified latent vectors are clustered via temporal embedding and _k_ -means to automatically discover the finite set of _Semantic Action Clusters_ , thereby determining the complete set of workstation tasks. 

### **3.1. Action Detection & Segmentation** 

The core of our segmentation approach relies on representing video content within an abstract, high-dimensional latent action space rather than operating directly on raw pixels. To accomplish this, we first train a lightweight motion tokenizer _Mθ_ . Our architecture is primarily derived from the temporal quantized autoencoder introduced in AMPLIFY [10], which comprises a Transformer-based encoder ( _Eθ_ ) and decoder ( _Dθ_ ), along with a Finite Scalar 


Figure 2. Overview of the LAPS pipeline: (1) _Motion Tracking_ extracts motion keypoints from raw video using a point tracker. (2) _Action Detection & Segmentation_ generates a latent vector stream via a motion tokenizer and identifies action boundaries to segment latent vectors, video clips, and action codes. (3) _Semantic Action Clustering_ groups the segmented latent vectors into meaningful semantic action clusters. 

Quantization (FSQ) [21] layer for discretization. The tokenizer is trained on a large dataset of short video clips, denoted as _D_ clips. For each clip, we first extract a dense grid of _N_ keypoint tracks using an off-the-shelf point tracker [16]. These tracks are then consolidated into a single tensor _κ ∈_ R<sup>_T ×N×_2</sup> , where _T_ indicates the temporal length (number of frames), _N_ is the number of tracked points, and 2 corresponds to the ( _x, y_ ) spatial coordinates. The encoder _Eθ_ transforms the velocities derived from these tracks into a latent sequence, which is then discretized into tokens _zt ∈Z_ using FSQ. Rather than reconstructing pixels, the decoder _Dθ_ is trained with a classification objective to predict the relative displacement of each track point. This is achieved by applying a cross-entropy loss over a discrete spatial grid, effectively modeling motion dynamics as a categorical distribution. A comprehensive description of the tokenizer’s architecture and training methodology is provided in the supplementary material. 

While AMPLIFY [10] employed this representation for policy learning, our work adapts it for a novel application: providing the primary signal for unsupervised temporal segmentation. Continuous video streams are processed by using a sliding-window approach, as illustrated in Figure 3. The Motion Tokenizer _Mθ_ generates two complementary representations for each window: 

- = 

- 1. A sequence of _continuous quantized vectors Sq {zq,_ 1 _, . . . , zq,T }_ , where each _zq,t ∈_ R<sup>_dm_</sup> corresponds to a vector prototype from the FSQ codebook. 

2. A sequence of _discrete code indices S_ d = _{c_ 1 _, . . . , cT }_ , where each _ct_ is an integer index. 

Although the _discrete_ code indices from the windowlevel _Sd_ are the components used to construct the final segment-level sequences _Si_ , the _continuous_ quantized vector sequence _Sq_ is critical for our pipeline’s internal operation. This continuous sequence _Sq_ preserves richer geo- 

6752 

metric and semantic information than the discrete indices alone. 

Consequently, the continuous window-level stream _Sq_ serves as the foundational signal for our segmentation framework, as its continuous nature is required for calculating our _Eaction_ metric via temporal differences by the _L_ 2 norm. Furthermore, the segment-level vectors derived from this stream denoted as _Sq,i_ serve as the input for our subsequent clustering analysis. This continuous representation enables meaningful distance computations within the latent space. 


Figure 3. Sliding-window tokenization: A motion tokenizer converts the video stream into a sequence of discrete latent action indices _ct ∈{_ 0 _, . . . ,_ 2047 _}_ , the main output for VLA pre-training. Action detection and clustering use the corresponding continuous quantized vectors. 

Traditional unsupervised segmentation methods which are based on low-level metrics such as optical flow[12] or visual similarity [13], capture physical motion. These signals are often volatile and sensitive to pixel-level variations that may not reflect a true change in the task’s semantic phase. In contrast, our approach targets _semantic intent_ as the driver of meaningful boundaries (e.g., transitions from ”reaching” to ”grasping”). Such intent-driven shifts induce distinct systematic changes in motion dynamics. Our _Motion Tokenizer_ (Section 3.1) is well-suited to this objective: its abstract Latent Action Sequence _S_ explicitly models these dynamics while suppressing low-level visual noise. 

#### **3.1.1. Mathematical Definition of Latent Action Energy** 

We introduce a novel metric termed _Latent Action Energy E_ action. This metric is defined directly on the dynamics of the continuous quantized vectors _Sq_ = _{zq,_ 1 _, . . . , zq,T }_ produced by the motion tokenizer. We formally define the Latent Action Energy as the _L_ 2 norm of the temporal difference within the quantized latent space: 


This formulation is resilient to appearance changes yet remains acutely responsive to shifts in latent motion dynamics. The energy metric _E_ action( _t_ ) remains low when the latent action token _zq,t_ is stable (e.g., during inactivity), and 

exhibits sustained high activation when tokens vary dynamically (i.e., throughout a continuous, coherent action primitive). A semantic shift—marking an action boundary—is detected when the energy signal returns to a low state, indicating the conclusion of the preceding action. 

#### **3.1.2. Unsupervised Action Detection** 

The _Action Detector_ operates as a causal state machine rather than a conventional peak-detection algorithm. Specifically, it implements a robust two-state (ON/OFF) controller with hysteresis that processes the onedimensional time-series signal _E_ action( _t_ ). This single-pass architecture enables real-time operation and facilitates online data curation. The segmentation procedure is as follows: 

1. _Causal Signal Smoothing:_ The raw energy signal _E_ action( _t_ ) is smoothed using an exponential moving average (EMA) to reduce high-frequency noise without future data leakage: 

      - _yt_ = _αE_ action( _t_ ) + (1 _− α_ ) _yt−_ 1 

   - where _yt_ is the smoothed signal and _α_ the smoothing factor. 

2. _Online Boundary Detection with Hysteresis:_ A twostate (ON/OFF) controller with hysteresis detects segment boundaries on _yt_ : 

   - _Activation (OFF → ON):_ Triggered when _yt > θ_ on for _u_ consecutive frames. 

   - _Deactivation (ON → OFF):_ Ends when _yt < θ_ off for _d_ consecutive frames, with _θ_ off _≤ θ_ on. 

   - This dual-threshold and debounce scheme ensures stable segmentation in noisy streaming data. 

3. _Primitive and Sequence Extraction:_ Upon OFF transition, the segment _Ai_ = _V_ [ _pi_ : _pi_ +1] is extracted from _V ∈D_ clips corresponding to the active interval. Additionally, the method outputs the corresponding discrete FSQ code indices _{ct}_ overlapping the segment form the sequence _Si_ = _{cpi, . . . , cpi_ +1 _}_ , preserving temporal dynamics for VLA pre-training. 

The primary threshold _θ_ on is determined through a fully unsupervised offline optimization procedure leveraging selfsupervised pseudo-labeling, eliminating the need for manual annotations. The process is as follows:s 

1. _Proxy Signal and Pseudo-Label Generation:_ We first compute a simple, low-level velocity energy from the temporal difference of velocity keypoints over a validation dataset to serve as a proxy signal. A heuristic method for auto thresholding [22] is applied to the proxy signal to automatically generate binary pseudo-labels, _y_ pseudo, which provide a coarse-grained distinction between ”motion” and ”non-motion” windows. 

2. _Threshold Optimization:_ With these noisy _y_ pseudo labels as the optimization target, we then perform a parameter 

6753 

sweep to find the optimal _θ_ on for our high-level _Latent Action Energy_ signal, _E_ action( _t_ ). We select the _θ_ on that maximizes the _F_ 1-score as quality metric between the thresholded _E_ action( _t_ ) and the pseudo-labels _y_ pseudo. This self-supervised, two-stage procedure enables the robust calibration of the threshold for our highly descriptive latent-space energy signal by leveraging a simple velocitybased signal. The resulting dataset-level threshold, _θ_ on, is fixed for all subsequent online segmentation tasks. The lower threshold, _θ_ off, is then computed as a fraction of this primary threshold ( _θ_ off = _r · θ_ on), where _r_ denotes the hysteresis factor (0 _< r ≤_ 1). 

### **3.2. Semantic Action Clustering** 

Following the segmentation of the continuous video stream into a collection of variable-length action primitives _A_ = _{A_ 1 _, . . . , AN }_ via our action segmentation method, the final step involves the unsupervised discovery of the finite set of actions intrinsic to the workstation. This is formulated as an unsupervised clustering task aimed at validating the semantic consistency of the segmented actions. 

Each primitive _Ai_ is represented by its corresponding Latent Action Sequence _Si_ . As detailed in [10], for clustering we utilize the continuous feature vectors obtained from the Motion Tokenizer’s quantization pipeline, denoted as 


where _Ti_ represents the variable sequence length of primitive _i_ , and _dm_ is the dimensionality of the descriptor (e.g., 768). The objective is to cluster these high-dimensional, variable-length time series into semantically coherent clusters without labels. 

#### **3.2.1. Temporal Embedding via Frozen Transformer** 

To capture the temporal dependencies within each sequence _Sq,i_ , we utilize a lightweight transformer encoder. Importantly, this model functions entirely in a training-free inference mode: all parameters, including projection layers and self-attention weights, remain at their randomly initialized values and are never updated [31]. This design choice is essential to achieve industrial scalability. This ensures generalization across domains, eliminates the need for manual annotations, minimizes computational requirements, and provides inherent robustness to domain shifts by avoiding overfitting to a particular training corpus. The architecture processes each sequence _Sq,i_ as follows: 

1. _Projection & Encoding:_ Input vectors _zq,t_ are linearly projected into the model dimension _d_ , and sinusoidal positional encodings _PEt_ are added. 

2. _Transformer Encoder:_ A stack of _L_ layers with _H_ multihead self-attention heads processes the token sequence. 

3. _Pooling:_ The final sequence of hidden states _H_<sup>(</sup><sup>_L_)</sup> _∈_ R<sup>_Ti×d_</sup> is aggregated into a single segment-level embedding _ei ∈_ R<sup>_d_</sup> . 

Through systematic hyperparameter search (detailed in the Experiments section), we select mean pooling ( _ei_ = _T_ <u>1</u> _i_ � _t_<sup>_h_</sup> _t_<sup>(</sup><sup>_L_)</sup> ) with _d_ = 256, _L_ = 4, and _H_ = 4. Empirically, in this frozen setting, mean pooling demonstrates superior stability and discriminative power compared to alternatives such as CLS [8] or attention pooling, which rely on parameters that would otherwise need to be learned. 

#### **3.2.2. Action Clustering via Cosine** _k_ **-means** 

Clustering high-dimensional embeddings with _d_ = 256 presents significant challenges, as vector orientation typically carries more discriminative information than magnitude in such spaces. Consequently, we adopt cosine geometry as the foundation for cluster separation. We employ _k_ -means as our primary clustering algorithm, making it compatible with cosine distance through a two-step preprocessing procedure. First, we standardize all embeddings _ei_ to zero mean and unit variance, then apply _L_ 2- normalization to obtain _e_ ˆ _i_ = _ei/∥ei∥_ 2. Applying standard _k_ -means (which minimizes Euclidean distance) on these normalized vectors _e_ ˆ _i_ is mathematically equivalent to optimizing cosine similarity, since 


A fundamental hypothesis of our work is that fixed industrial workstations exhibit a finite and countable set of core action primitives. Therefore, _k_ is not treated as a free parameter to be optimized by internal metrics. Instead, _k_ is set a priori based on domain expertise and empirical observation of the workstation’s operational tasks. The _k_ -means algorithm then partitions the segmented primitives _A_ into _k_ clusters _{C_ 1 _, . . . , Ck}_ . The success of our approach depends critically on whether these discovered clusters align with semantically meaningful action categories (e.g., “move the baffle,” “pick up a motor”). 

#### **3.2.3. Semantic Validation via Vision-Language Model** 

To quantitatively evaluate the semantic coherence of the discovered clusters, a task for which conventional internal metrics like the Silhouette score are insufficient due to their exclusive focus on spatial separation, a pre-trained VisionLanguage Model (VLM) [24] is deployed. We propose a metric, _Intra-Cluster Semantic Similarity (ICSS)_ , defined as follows: 

1. _Segment Embedding:_ For each video primitive _Ai_ , we compute a fixed-length embedding _vi_ . This is achieved by sampling multiple frames from _Ai_ , extracting their _ℓ_ 2-normalized visual features using the VLM’s encoder (e.g., CLIP ViT-B/32), and aggregating them via a _normweighted pooling_ strategy. This produces a final, _ℓ_ 2- normalized segment descriptor _vi_ that captures the holistic visual content. 

6754 

2. _Pairwise Similarity:_ For each cluster _Ck_ , we sample a large set of primitive pairs _Pk_ = _{_ ( _Ai, Aj_ ) _| Ai, Aj ∈ Ck, i̸_ = _j}_ . 

3. _Metric Calculation:_ The similarity for that cluster is the average cosine similarity of all sampled pairs: 


A high average ICSS score, especially when compared to a _random-pair baseline_ (computed by sampling the same number of pairs from the _entire_ dataset irrespective of clusters), indicates that our pipeline successfully groups semantically meaningful and similar actions. This validation serves a dual purpose: it confirms the precision of our action segmentor and the descriptive power of the temporal embedding (Section 3.2.1). 

lows: 1) The _Motion Tokenizer_ ( _Mθ_ ) [10] was trained exclusively on unlabeled clips drawn from the training partition of our dataset. 2) The parameters of the _Action Segmentor_ (including _θ_ on _, θ_ off _, u, d_ ) were tuned via the unsupervised calibration procedure described in Section 3.1.2. 3) For _Clustering_ (Section 3.2), latent sequences _Sq,i ∈_ R<sup>_Ti×_768</sup> were embedded using a frozen Transformer model with _L_ = 4 layers and _H_ = 4 heads, followed by mean pooling to obtain embeddings _ei ∈_ R<sup>256</sup> . This parameter-efficient encoder, containing approximately 2.3 million parameters without requiring pre-training, provides a computationally lightweight solution well-suited for large-scale deployment scenarios. Finally, we applied cosine _k_ -means clustering (Section 3.2.2) with a predefined number of clusters _k_ determined based on domain knowledge and empirical observation. 

#### **4.1.2. Baselines and Metrics** 

## **4. EXPERIMENTS** 

To validate our proposed framework, we conduct a series of experiments designed to answer three key questions: (1) Does the proposed _Latent Action Energy_ provide a more effective signal for semantic action segmentation compared to traditional metrics? (2) How does our unsupervised action segmentor compare with state-of-the-art unsupervised temporal action detection (TAD) baselines? (3) Do the segmented action primitives form semantically coherent and finite clusters confirming their quality for VLA pre-training? 

### **4.1. Experimental Setup** 

For our experiments, the following datasets have been used: **GTEA** [14] is a dataset comprising 28 videos with a combined duration of approximately 35 minutes, recorded by 4 participants performing tasks in a single kitchen environment. The dataset encompasses 7 procedural activities, each averaging 1.5 minutes in length, captured using a head-mounted camera system. **Breakfast** [19] consists of 1,712 videos documenting 10 distinct cooking activities. This dataset presents several challenges, including substantial temporal variation in video length (ranging from 30 seconds to 7 minutes), frequent occlusions, and multiple camera viewpoints. **Industrial Motor Assembly Dataset** is a new, self-collected dataset from a real-world electro motor assembly line, containing _∼_ 10 hours of continuous videos from two synchronized views (top-down and exocentric). A two hour long test subset was created and annotated for quantitative comparison against traditional Temporal Action Detection (TAD) baselines. This annotated subset will be made publicly available to promote reproducibility and support future research. 

#### **4.1.1. Implementation Details** 

We implemented the pipeline following the approach detailed in Section 3. The implementation details are as fol- 

We evaluate the LAPS pipeline against the following three representative unsupervised action segmentation approaches: 

- _Optical Flow Baseline:_ Instantiates the traditional _physical motion_ paradigm. We apply the identical online statemachine architecture (Section 3.1.1) to standard _Optical Flow Magnitude_ features, enabling direct and controlled comparison of signal quality relative to our proposed _E_ action signal (Section 4.2). 

- _ABD [13]:_ A state-of-the-art method exemplifying the _local boundary detection_ paradigm, which identifies temporal change-points through local minima in visual feature similarity. 

- _OTAS [20]:_ A state-of-the-art method representing the _explicit feature-fusion_ paradigm, integrating global, objectinteraction, and object-relation features for boundary detection. 

**Evaluation Metrics:** Temporal segmentation accuracy is measured using strict boundary-level _F1-scores_ with 2 second and 5 second tolerances (F1@2s, F1@5s), consistent with [20]. Clustering quality (Section 4.4) is assessed via complementary unsupervised metrics: Silhouette Score [25], Calinski-Harabasz Index [6], and our proposed _Intra-Cluster Semantic Similarity (ICSS)_ metric. 

### **4.2. Effectiveness of the Latent Motion Energy** 

To validate our central hypothesis that segmentation is most effectively performed within the latent semantic space, we begin by evaluating the segmentation signal _Eaction_ . The qualitative result, illustrated in Figure 4, confirms our hypothesis that the latent action space provides a more discriminative representation for semantic boundary detection compared to pixel-space and optical flow-based approaches. It effectively captures transitions in task-phase intent while suppressing the influence of spurious physical motion artifacts. 

6755 


Figure 4. Qualitative comparison of our _E_ action (blue) and Optical Flow (red) over 60 seconds. Our latent action energy shows clear, sustained peaks during actions and sharp drops at ground truth semantic boundaries (dashed lines), while optical flow is noisy and reflects only physical movement, not task phases. 

### **4.3. Unsupervised Action Segmentation** 

Quantitative comparisons against unsupervised TAD baselines are presented in Tables 1 and 2. On public benchmarks (Table 1), LAPS achieves performance comparable to state-of-the-art approaches despite using only lightweight training (approx. 25 mins) on raw video, contrasting with baselines reliant on extensive pre-training (e.g., I3D [7]). Crucially, on the industrial dataset (Table 2), LAPS demonstrates superior performance. While conventional methods like ABD [13] degrade due to sensitivity to physical motion variations in low-level features [11], our _Motion Tokenizer_ robustly captures semantic transitions. This capability is evidenced by high F1@2s scores, underscoring our precision in segmenting repetitive, countable actions inherent to industrial workflows. 

Table 1. **Comparison on GTEA [14] and Breakfast [19].** 

||**GT**|**EA**|**Brea**|**kfast**|
|---|---|---|---|---|
|_Method_|_F1@5s_|_F1@2s_|_F1@5s_|_F1@2s_|
|ABD [13]|**81.92**|**74.23**|54.50|33.33|
|OTAS [20]|37_._68|36_._90|**62.13**|**39.49**|
|**LAPS (Ours)**|73_._12|63_._20|58_._82|36_._72|


Table 2. **Comparison on the Industrial Motor Assembly.** 

||**Top-dow**|**n View**|**Exocent**|**ric View**|
|---|---|---|---|---|
|_Method_|_F1@5s_|_F1@2s_|_F1@5s_|_F1@2s_|
|Optical Flow|56_._96|43_._68|66_._06|42_._54|
|ABD [13]|53_._00|34_._08|50_._32|29_._86|
|OTAS [20]|62_._24|40_._69|54_._56|33_._38|
|**LAPS (Ours)**|**84.26**|**81.27**|**84.75**|**81.93**|


### **4.4. Quality of Action Primitives** 

One of our central claims is that our segmented primitives are besides being well-bounded are also semanti- 

cally meaningful, thereby constituting a discrete and countable set of actions. We validate this claim by applying our clustering pipeline ( _Frozen Transformer + k-means_ ) to all primitives segmented from the training set. Fig- 


Figure 5. UMAP visualization of action primitive embeddings colored by k-means cluster ID. Distinct, well-separated clusters that correspond to real workstation tasks confirmed through manual inspection. 

ure 5 presents a UMAP visualization of the action primitive embeddings, where each point represents an action primitive segmented by our pipeline, embedded via the _Frozen Transformer_ (Section 3.2.1), and colored according to its _k_ - means-assigned cluster identity. The visualization reveals distinct, well-separated clusters that, upon manual inspection, correspond to semantically coherent groupings within the discrete and countable set of workstation tasks. As can be seen from the data, this effectively disambiguates coarsegrained action types such as Cluster 1: ‘Move Baffle’, Cluster 2: ‘Replace Motor’, and Cluster 3: ‘Grasp Motor’. 

This analysis provides compelling qualitative evidence supporting our claim. The _Transformer_ embeddings of the primitives form dense, well-separated clusters that _k_ -means reliably identifies, demonstrating that our pipeline automatically discovers and organizes the inherent action vocabulary of the workstation in an unsupervised manner. 

Table 3. Clustering results on the Exocentric View dataset (6,444 segments, _k_ = 3), comparing our Frozen Transformer embedding with a strong non-temporal aggregation baseline. 

|_Embedding Method_|_Silhouette_|_Calinski-Harabasz_|
|---|---|---|
|Attention-Norm Pooling|0.498|3523.6|
|**Ours (Frozen Transformer)**|**0.588**|**3919.2**|


Table 3 provides quantitative validation of our approach. The results clearly indicate that our _Frozen Transformer encoder_ significantly outperforms the mean-pooling baseline across both unsupervised metrics. This improvement con- 

6756 

firms our hypothesis: explicitly modeling temporal dynamics through self-attention capabilities, which is unachievable by simple mean-pooling, is essential for distinguishing subtle action patterns that are obscured by naive aggregation strategies. The ability to capture fine-grained dependencies enables the formation of semantically coherent action clusters, which are critical for effective downstream learning tasks. 

### **4.5. Semantic Coherence Validation via VLM** 

We now quantitatively validate the semantic coherence of the discovered clusters using our _Intra-Cluster Semantic Similarity (ICSS)_ metric (Section 3.2.3). As shown in Table 4, we compare the average ICSS _within_ each discovered cluster to a _random-pair_ baseline. The results in Table 4 

Table 4. VLM-based Semantic Coherence (ICSS): Mean intracluster similarity (± std) for discovered clusters. The baseline samples random pairs from the entire dataset irrespective of clusters and thus, by definition, only provides a single _Overall_ metric for comparison. 

|_Metric_|_Baseline_|_Ours (k-means)_|
|---|---|---|
|Cluster_K_1|–|0_._919_±_0_._040|
|Cluster_K_2|–|0_._929_±_0_._029|
|Cluster_K_3|–|0_._922_±_0_._036|
|**Overall ICSS**|**0**_._**804**_±_**0**_._**127**|**0**_._**926**_±_**0**_._**033**|


show that the mean similarity _within_ our discovered clusters (Overall ICSS: 0 _._ 926 _±_ 0 _._ 033) is substantially higher than the similarity of random pairs drawn from the entire dataset (Baseline: 0 _._ 804 _±_ 0 _._ 127). Furthermore, the tight standard deviations of our cluster scores, compared to the baseline’s much wider variance, provide strong quantitative evidence that our pipeline successfully discovers and groups semantically coherent action primitives. This automated semantic validation confirms the output is a structured, high-quality dataset of ”countable” actions, perfectly suited for the downstream task of VLA pre-training. 

### **4.6. Ablation Studies** 

We perform ablation studies to rigorously evaluate the impact of our key design choices within the pipeline. Table 5 summarizes these results. First, substituting our specialized motion tokenizer _Mθ_ with generic CLIP features results in a severe degradation in both segmentation and clustering performance, confirming that a domain-specific motion tokenizer is critical for capturing the fine-grained nuances of industrial tasks. Second, the effectiveness of our _E_ action metric is contingent upon its computation in the _quantized_ space ( _Sq_ ); applying it to raw velocities or latent representations prior to quantization yields poor results. This finding validates the importance of discretization for accurately 

capturing semantic intent. Finally, in the clustering stage, the Frozen Transformer encoder outperforms simple meanpooling, demonstrating that explicitly modeling temporal dynamics is essential for discovering coherent and semantically meaningful action vocabularies. 

Table 5. Ablation study on pipeline components, showing their impact on segmentation and clustering. Segmentation is evaluated using the strict **F1@2s** metric. Results are from the Exocentric View test set. 

|_Configuration_|F1@2s (%)|Cluster ICSS|
|---|---|---|
|**Full Pipeline (Ours)**|**87.5**|**0.92**|
|_Signal Source Ablation:_|||
|_E_action from Pre-Quant. Latents<br>_E_action from Raw Velocities|25.2<br>24.9|–<br>–|
|_Encoder Ablation:_<br>w/o Transformer (Mean-pool)|–|0.84|
|_Representation Ablation:_<br>w/o_Mθ_ (e.g., CLIP)|27.2|0.75|


## **5. Conclusion and Discussion** 

In this work, we addressed the critical data bottleneck for industrial VLA models by introducing Latent Actionbased Primitive Segmentation (LAPS), the first unsupervised pipeline to discover finite sets of actions from passive video streams. Our core novelty is a segmentation paradigm shifted into an abstract latent action space, where our _Latent Action Energy_ ( _Eaction_ ) metric robustly captures ”behavioral intent” over physical movement. Validated on a realworld motor assembly dataset, LAPS significantly outperformed TAD baselines. Furthermore, our unsupervised discovery pipeline identified the finite action primitives, whose semantic coherence was quantitatively confirmed by our VLM-based ICSS metric. LAPS transforms raw observational data into a structured and learnable knowledge base, paving a scalable pathway for deploying embodied AI. At the current stage, our method is limited to highly repetitive tasks as they are found in the manufacturing domain. 

In future work we want to elaborate how our pipeline can be extended towards other domains such as tasks in domestic households and hospitals. Furthermore, our next immediate step will be to bridge the gap from highlevel task understanding towards task execution. To this end, we want to train a dual-arm manipulator to perform tasks from the manufacturing domain by teleoperation and to correlate those skills with our discovered latent space. Finally, to enable the transformation of structured latent knowledge into real-world task execution. 

## **References** 

[1] AgiBot-World-Contributors, Qingwen Bu, Jisong Cai, Li 

6757 

Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. AgiBot World Colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 1, 2, 3 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2 

- [3] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _9th Annual Conference on Robot Learning_ , 2025. 1, 2, 3 

- [4] Andrea Bonci, Pangcheng David Cen Cheng, Marina Indri, Giacomo Nabissi, and Fiorella Sibona. Human-robot perception in industrial environments: A survey. _Sensors_ , 21 (5):1571, 2021. 3 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [6] Tadeusz Cali´nski and Jerzy Harabasz. A dendrite method for cluster analysis. _Communications in Statistics-theory and Methods_ , 3(1):1–27, 1974. 6 

- [7] Joao Carreira and Andrew Zisserman. Quo vadis, action recognition? a new model and the kinetics dataset. In _proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_ , pages 6299–6308, 2017. 7 

- [8] Haw-Shiuan Chang, Ruei-Yao Sun, Kathryn Ricci, and Andrew McCallum. Multi-cls bert: An efficient alternative to traditional ensembling. _arXiv preprint arXiv:2210.05043_ , 2022. 5 

- [9] Yi Chen, Yuying Ge, Weiliang Tang, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 19752– 19763, 2025. 1 

- [10] Jeremy A Collins, Lor´and Cheng, Kunal Aneja, Albert Wilcox, Benjamin Joffe, and Animesh Garg. Amplify: Actionless motion priors for robot learning from videos. _arXiv preprint arXiv:2506.14198_ , 2025. 2, 3, 5, 6 

- [11] Navneet Dalal, Bill Triggs, and Cordelia Schmid. Human detection using oriented histograms of flow and appearance. In _European conference on computer vision_ , pages 428–441. Springer, 2006. 7 

- [12] Guodong Ding, Fadime Sener, and Angela Yao. Temporal action segmentation: An analysis of modern techniques. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 46(2):1011–1030, 2024. 2, 4 

- [13] Zexing Du, Xue Wang, Guoqing Zhou, and Qing Wang. Fast and unsupervised action boundary detection for action segmentation. In _Proceedings of the IEEE/CVF Conference_ 

_on Computer Vision and Pattern Recognition_ , pages 3323– 3332, 2022. 2, 4, 6, 7 

- [14] Alireza Fathi, Xiaofeng Ren, and James M Rehg. Learning to recognize objects in egocentric activities. In _CVPR 2011_ , pages 3281–3288. IEEE, 2011. 6, 7 

- [15] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18995–19012, 2022. 1, 2 

- [16] Nikita Karaev, Yuri Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker3: Simpler and better point tracking by pseudolabelling real videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6013–6022, 2025. 2, 3 

- [17] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 1, 2, 3 

- [18] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2 

- [19] Hilde Kuehne, Ali Arslan, and Thomas Serre. The language of actions: Recovering the syntax and semantics of goaldirected human activities. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 780–787, 2014. 6, 7 

- [20] Yuerong Li, Zhengrong Xue, and Huazhe Xu. Otas: unsupervised boundary detection for object-centric temporal action segmentation. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pages 6437–6446, 2024. 2, 6, 7 

- [21] Fabian Mentzer, David Minnen, Eirikur Agustsson, and Michael Tschannen. Finite scalar quantization: Vq-vae made simple. _arXiv preprint arXiv:2309.15505_ , 2023. 3 

- [22] Nobuyuki Otsu. A threshold selection method from graylevel histograms. _IEEE Transactions on Systems, Man, and Cybernetics_ , 9(1):62–66, 1979. 4 

- [23] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 1, 2 

- [24] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR, 2021. 5 

6758 

- [25] Peter J Rousseeuw. Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. _Journal of computational and applied mathematics_ , 20:53–65, 1987. 6 

- [26] Dominik Schmidt and Minqi Jiang. Learning to act without actions. _arXiv preprint arXiv:2312.10812_ , 2023. 2 

- [27] Peiyao Wang, Yuewei Lin, Erik Blasch, Haibin Ling, et al. Efficient temporal action segmentation via boundary-aware query voting. _Advances in Neural Information Processing Systems_ , 37:37765–37790, 2024. 2 

- [28] Angchi Xu and Wei-Shi Zheng. Efficient and effective weakly-supervised action segmentation via actiontransition-aware boundary alignment. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18253–18262, 2024. 2 

- [29] Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, et al. Magma: A foundation model for multimodal ai agents. In _Proceedings of the computer vision and pattern recognition conference_ , pages 14203–14214, 2025. 2 

- [30] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 1, 2 

- [31] Ziqian Zhong and Jacob Andreas. Algorithmic capabilities of random transformers. _Advances in Neural Information Processing Systems_ , 37:104357–104382, 2024. 5 

- [32] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1, 2 

6759 

