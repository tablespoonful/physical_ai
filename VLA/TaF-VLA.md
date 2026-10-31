---
title: "TaF-VLA: Tactile-Force Alignment in Vision-Language-Action Models for Force-aware Manipulation"
date: "2026-01-28"
authors: "Yuzhe Huang; Pei Lin; Wanlin Li; Daohan Li; Jiajun Li; Jiaming Jiang"
venue: "T-RO"
url: https://arxiv.org/abs/2601.20321
pdf: https://arxiv.org/pdf/2601.20321
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.20321)** / [論文ページ](https://arxiv.org/abs/2601.20321)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Tactile-Force Alignment in Vision-Language-Action Models for Force-aware Manipulation 

Yuzhe Huang<sup>1</sup><sup>_,_3</sup><sup>_⋆_</sup> , Pei Lin<sup>2</sup><sup>_,_3</sup><sup>_⋆_</sup> , Wanlin Li<sup>3</sup><sup>_⋆_</sup> , Daohan Li<sup>3</sup> , Jiajun Li<sup>3</sup><sup>_,_4</sup> , Jiaming Jiang<sup>2</sup><sup>_,_3</sup> , Chenxi Xiao<sup>2</sup><sup>_†_</sup> , Ziyuan Jiao<sup>1</sup><sup>_,_3</sup><sup>_†_</sup> 

> 1Beihang University 2ShanghaiTech University 

> 3Beijing Institute for General Artificial Intelligence 4The University of Hong Kong 

> _⋆_ equal contributors _†_ corresponding authors https://peilin-666.github.io/projects/TaF-VLA/ 

**_Abstract_ —Vision-Language-Action (VLA) models have recently emerged as powerful generalists for robotic manipulation. However, due to their predominant reliance on visual modalities, they fundamentally lack the physical intuition required for contact-rich tasks that require precise force regulation and physical reasoning. Existing attempts to incorporate vision-based tactile sensing into VLA models typically treat tactile inputs as auxiliary visual textures, thereby overlooking the underlying correlation between surface deformation and interaction dynamics. To bridge this gap, we propose a paradigm shift from tactile-vision alignment to tactile-force alignment. Here, we introduce TaF-VLA, a framework that explicitly grounds highdimensional tactile observations in physical interaction forces. To facilitate this, we develop an automated tactile-force data acquisition device and curate the TaF-Dataset, comprising over 10 million synchronized tactile observations, 6-axis force/torque, and matrix force map. To align sequential tactile observations with interaction forces, the central component of our approach is the Tactile-Force Adapter (TaF-Adapter), a tactile sensor encoder that extracts discretized latent information for encoding tactile observations. This mechanism ensures that the learned representations capture history-dependent, noise-insensitive physical dynamics rather than static visual textures. Finally, we integrate this force-aligned encoder into a VLA backbone. Extensive realworld experiments demonstrate that TaF-VLA policy significantly outperforms state-of-the-art tactile-vision-aligned and vision-only baselines on contact-rich tasks, verifying its ability to achieve robust, force-aware manipulation through cross-modal physical reasoning.** 

**_Index Terms_ —Foundation model, tactile and force sensing, force-aware manipulation.** 

## I. INTRODUCTION 

Recent advances in VLA models have driven significant progress in robotic manipulation by jointly modeling largescale visual representations and natural-language instructions [1–4]. While these models demonstrate strong generalization across open-ended tasks, reliance on vision alone remains fundamentally insufficient for force-sensitive scenarios, such as handling fragile objects [5, 6], precision assembly [7, 8], or interaction with thin, deformable objects [9]. Visual observations are susceptible to hand-object occlusion and inherently lack direct perception of interaction forces, which are critical for safe and robust execution [10–13]. This sensory gap restricts current VLA approaches from attaining the precision 

and stability required for contact-rich manipulation, where feeling the interaction is as critical as seeing it [14–16]. 

To bridge the gap left by vision-only policies, prior research has largely relied on global force feedback, typically acquired via wrist-mounted Force/Torque (F/T) sensors [15] or joint torque sensors [17, 18]. While these signals provide a useful measurement of total interaction load, they suffer from two critical shortcomings that limit their utility. First, from a hardware perspective, high-precision F/T sensors are expensive, fragile, and difficult to deploy at the scale required for great data-collection efforts, and are not broadly compatible with typical robot hardware [19]. Second, and more fundamentally, the data they provide is low-dimensional and spatially aggregated [20]. A single resultant force vector compresses complex contact interactions into a few scalar values, discarding the spatially distributed pressure patterns and local contact geometry that are essential for understanding how an object is being grasped or manipulated [21]. 

In contrast, Vision-based Tactile Sensors (VBTSs) have emerged as a low-cost, powerful multi-modal sensing element for capturing these missing local dynamics [22, 23]. Unlike resultant force vectors, these sensors can detect surface deformation [24, 25], offering rich, high-resolution feedback on geometry, texture, local pressure distribution, and slippage. This visual nature makes them uniquely compatible with modern vision-based learning methods [26]. By treating touch as an image, these sensors provide the dense, semantically rich information necessary to distinguish between stable grasps, slips, and intricate contact states, which are capabilities that global force sensors cannot achieve [24, 27]. 

Recent efforts to incorporate tactile feedback into VLA architectures typically implant tactile streams as raw visual tokens, effectively aligning them with language and scene images [28, 29]. However, this strategy overlooks the unique modality of tactile sensing: unlike scene vision, which captures remote photometric properties, tactile sensing captures local mechanical interactions. Treating tactile data solely as “more vision” fails to extract the contact force information critical for force-aware manipulation tasks. _We argue that to be effective, tactile representations must be grounded in the physical quantities they represent._ This motivates us to propose a paradigm shift from tactile-vision alignment to tactile-force 

2 


Fig. 1: **From Data to Policy: The TaF-VLA Pipeline.** To address the “force-blindness” of current Vision-Language-Action (VLA) models, we propose a paradigm shift from tactile-vision to tactile-force alignment, realized through three stages: (a) We deploy an automated data acquisition system (TaF-Device) to construct the TaF-Dataset, a large-scale collection of synchronized visuotactile images, 6-axis force/torque, and matrix force maps. Using this data, we pretrain the TaF-Adapter to align tactile observations with ground-truth force signals in a shared latent space. (b) We fuse the TaF-Adapter into a VLA backbone and fine-tune the policy on real-world demonstrations enriched with forceaware language instructions ( _i.e_ ., force-aware manipulation dataset). (c) This explicit tactile-force alignment empowers TaF-VLA to master complex force-aware manipulation tasks, such as tool-use and deformable object manipulation, where traditional vision-based baselines consistently fail. 

alignment. By explicitly grounding tactile representations in physical force measurements, we equip the policy with a true understanding of contact dynamics. 

To realize this paradigm shift, we propose TaF-VLA, a VLA model architecture that utilizes high-dimensional visuotactile observations aligned with physical interaction forces. Developing such a system, however, presents three fundamental challenges: 

- (Q1) **Scarcity of Tactile Data for Alignment:** VLA models require massive datasets to generalize. Existing datasets lack synchronized pairs of _visuotactile and ground-truth force_ data. How can we acquire such synchronized tactile-force alignment data at scale? 

- (Q2) **Representation Disparity:** Visuotactile inputs are highdimensional and geometric, whereas force signals are low-dimensional and dynamic. This modality gap raises a critical design choice: Should we rely on explicit force regression, which risks poor cross-sensor generalization? Or should we pursue implicit latent alignment? If the latter, the challenge lies in constructing a representation that captures history-dependent dynamics while maintaining robustness against sensor noise and hardware 

## variance. 

- (Q3) **Policy Integration:** From an architectural perspective, how do we fuse this tactile-force-aligned representation into large-scale VLA backbones, and without causing modality collapse or diluting the physical signal? 

To address these challenges, the development of TaF-VLA comprises three key steps (see Fig. 1). _First_ , we design an automated data acquisition device that addresses the scarcity of paired tactile data and force data required for alignment. Each collected sample includes time-synchronized visuotactile observations, 6-axis force/torque measurements, and matrix force maps. The device adopts a parallel actuation structure that applies forces of the same magnitude and direction simultaneously to both the tactile sensor and the force sensors. By adjusting the stiffness and geometry of the replaceable indenters, we further enrich the diversity of contact interactions represented in the dataset. Thanks to its modular design, we can easily swap in different VBTSs, and we collect data on six distinct sensors. The system operates efficiently, achieving a throughput of 100,000 synchronized tactile-force frames per hour. Using this setup, we construct the TaF-Dataset, a largescale real-world tactile dataset comprising over 10 million data 

3 

frames. 

_Second_ , to bridge the critical representation gap between visuotactile data and force, we propose the Tactile-Force Adapter (TaF-Adapter). The TaF-Adapter employs contrastive learning to construct a shared latent space where tactile embeddings are aligned with paired force profiles. Compared to explicit and direct force calibration methods [30], aligning only in the latent space without explicit reconstruction performs better when applied to new sensors (refer to experiments), which is crucial for practical deployment. Moreover, we found that the mapping relationship from tactile images to contact forces is history-dependent, meaning that a single static frame cannot accurately represent dynamic force interactions. To capture such dynamic forces, the TaF-Adapter aggregates historical observations to improve expressibility. Moreover, because forces during manipulation are often noisy, the latent space is quantized as a discrete codebook. These designs ensure that TaF-Adapter can capture physical dynamics robustly. 

_Finally_ , we integrate this tactile-force-aligned module into a pretrained VLA backbone, leading to the design of TaFVLA model. By interleaving these tactile-force-aligned tokens into the language-action stream, the model learns to condition its end-effector actions on both language and tactile feedback cues. Benchmarking across 7 force-critical daily manipulation tasks demonstrates that TaF-VLA achieves an average 22% improvement in success rate over the state-of-the-art visiontactile-aligned baseline, especially in contact-rich scenarios requiring precise force perception and regulation. 

In summary, the contributions of this work are threefold: 

- **Tactile-Force Data Acquisition Device (address Q1):** We develop a low-cost, automated device and pipeline for collecting aligned tactile-force data at scale (Sec. III). 

- **Tactile-Force Alignment (address Q2):** We introduce the TaF-Adapter, a module that maps sequential tactile observations into a force-aligned latent space using a contrastive learning framework. By constructing a vector-quantized shared latent space that aligns temporal visuotactile data with 6-axis force/torque signals and matrix pressure maps, our approach learns representations that are robust to force noise and cross-sensor variation, while capturing rich, history-dependent contact dynamics. (Sec. IV-A). 

- **TaF-VLA Policy (addressing Q3):** We developed the TaFVLA model, a VLA framework capable of incorporating tactile information. Experiments show that explicit force alignment enables VLA policies to successfully perform force-sensitive manipulation tasks that are otherwise intractable for vision-only or naive tactile-vision aligned baselines (Secs. IV-B and V). 

## II. RELATED WORK 

## _A. Vision-Language-Action Models and the Physical Gap_ 

The paradigm of VLA learning has fundamentally transformed robotic manipulation by unifying large-scale visual representation learning with natural language reasoning [31– 36]. Influential frameworks, ranging from transformer-based action predictors [2, 37, 38] to open-weight foundation models [3, 4, 39], leverage massive datasets of paired visual obser- 

vations, language instructions, and action demonstrations [40– 43]. Driven by the scaling laws of sequence modeling architectures, these systems have demonstrated remarkable generalization in complex contact-rich tasks such as grasping, manipulating articulated objects, cloth folding, and etc. [44, 45]. 

However, a critical gap exists between _semantic understanding_ and _physical interaction_ . While current VLAs excel at “what to do”, they struggle with “how to interact” in contactrich scenarios where visual feedback is insufficient [12, 46]. This limitation is twofold. First, RGB cameras suffer from occlusion and lack the direct perception of contact forces, friction, and compliance required for tasks like precise insertion [11, 18] or in-hand manipulation [47–50]. Second, standard robot datasets [51, 52] are dominated by high-level semantic labels ( _e.g_ ., “pick up the cup”) while omitting the fine-grained force directives ( _e.g_ ., “make a gentle press”, “grasp tightly”, “keep a compliant touch”) necessary to specify delicate interactions. Consequently, standard VLA policies are effectively “force-blind”, relying on visual priors that often fail during complex physical interaction. 

## _B. Force Perception via Vision-based Tactile Sensing_ 

To retrieve these missing physical cues, Vision-based Tactile Sensors (VBTSs) have emerged as a powerful solution, converting contact deformation into high-resolution images [22]. Accurately estimating contact forces from these images is a prerequisite for reliable control, and methodologies have evolved significantly in recent years [24, 26, 53, 54]. Early approaches relied on physics-driven calibration, inferring forces by tracking markers [55] or solving inverse finite element methods (FEM) based on deformation fields [25, 30, 56, 57]. While offering strong physical interpretability, these methods require precise knowledge of sensor geometry and are highly sensitive to material aging and manufacturing variability [54, 58]. Consequently, recent works have pivoted toward data-driven approaches, employing neural networks to regress forces from labeled data collected via external force/torque sensors [59, 60]. More importantly, recognizing that contact is inherently dynamic, researchers have adopted temporal modeling ( _e.g_ ., RNNs, Transformers) to capture history-dependent phenomena such as viscoelastic hysteresis, incipient slip, and stick-slip transitions [61–63]. These advances in temporal force estimation highlight a crucial insight: a tactile observation is not merely characterized by a static texture, but a snapshot of an evolving dynamical process. However, effectively transferring this insight into generalist VLA policies remains an open challenge. 

## _C. Tactile Integration in Generalist Policies_ 

Recent efforts to integrate tactile sensing into VLA frameworks have met with mixed success. Some approaches augment policies with global force feedback via wrist-mounted F/T sensors [15] or joint-torque estimates [17, 18]. While useful for collision detection, these signals aggregate interaction forces into a single vector, losing the spatial richness required to model local contact geometry. Conversely, visuotactile-based VLA policies attempt to leverage the high 

4 

resolution of vision-based tactile sensors [29]. However, the predominant strategy is to treat tactile frames as auxiliary visual textures, aligning tactile embeddings with scene images using standard Vision Transformers (ViT). We argue that this represents yet another limitation in semantic representation: it aligns tactile data with _visual appearance_ rather than _physical dynamics_ , which are characterized by a temporal process. By neglecting the temporal dependencies identified in the force estimation literature (Sec. II-B), the current tactile-vision alignment methods fail to distinguish between static surface features and dynamic force events. Furthermore, without force signals as anchors, contrastive representation learning cannot theoretically guarantee that the learned embedding space is organized in a force-aware or force-consistent manner [64, 65]. 

## _D. Distinction and Innovations of our TaF-VLA_ 

The advancement of TaF-VLA lies in synthesizing these insights into a unified framework for generalist policy learning. Compared to the conventional “tactile-vision alignment” paradigm, our approach introduces three key innovations. First, building on the dataset collected via our scalable acquisition pipeline, we propose a temporal adapter (TaF-Adapter) that fuses tactile observations across a receding horizon, enabling the policy to capture history-dependent dynamics such as incipient slip. Second, instead of explicitly regressing forces (an approach that introduces additional force encoding steps via networks), we employ contrastive learning to align the tactile latent space with ground-truth force trajectories during pretraining. This yields a “tactile-force” aligned representation that encodes richer contact dynamics while eliminating the need for a costly F/T sensor at deployment. Finally, we bridge the semantic gap by conditioning the policy on force-aware language instructions, allowing the model to perform precise, language-guided force modulation (a capability not commonly supported in current VLA models). 

## III. TAF-DATASET 

The proposed tactile-force alignment paradigm hinges on the availability of high-fidelity, synchronized multi-modal data, specifically the visuotactile observations and groundtruth force/torque measurements. However, existing robotic datasets typically lack this precise alignment, often omitting dense force labels. To bridge this data gap, we present the TaFDataset, a large-scale repository designed to enable physically grounded representation learning. In this section, we first detail the automated hardware platform developed to acquire this data at scale (Sec. III-A). Subsequently, we describe the dataset construction process, including the automated acquisition protocol and the diversification strategies used to cover the full spectrum of contact dynamics (Sec. III-B). 

## _A. Tactile-Force Data Acquisition Device_ 

Our goal is the concurrent collection of 6-axis force/torque, matrix force map, and VBTS tactile data for alignment. Nevertheless, directly placing VBTS on top of a pressure sensor or an F/T sensor can alter the force transmission path 

and introduce significant distortion to the sensor readings. Additionally, scalable dataset construction demands highly efficient data acquisition. To overcome these limitations, we developed an autonomous data-collection platform that records synchronized high-resolution tactile images together with multi-dimensional force measurements, all with minimal human intervention. The design and working principle of the proposed mechanism are detailed below. 

_1) Design Principle:_ To collect multiple sensor responses concurrently under identical indentation conditions, we designed a machine with two key characteristics. The core principle is to generate highly synchronized indentation motions onto two twin platforms. Specifically: 

**Highly Accurate Synchronized Indentation:** To ensure that the tactile and force signals are precisely aligned in both time and space, we enforce strict kinematic coherence between the two platforms. Each corresponding Degree of Freedom (DoF) is driven by an identical motor-gear pair, mechanically linking the platforms and eliminating relative phase errors. 

**Ease of Fabrication:** A second design goal is to enable broader replication by the research community. To this end, we adopted a modular architecture and prioritized accessibility. Aside from using standard off-the-shelf components (servomotors, springs, universal joints), the entire chassis is 3D-printed. We integrated self-aligning features to simplify assembly and used an open-frame lattice structure to preserve visibility during operation and installation. In addition, the modular, “plug-and-play” design supports flexible reconfiguration and customization for different contact scenarios. 

_2) System Architecture:_ As illustrated in Fig. 2, the device comprises five integrated subsystems: 

**Structural Chassis:** Overall, the device features a compact footprint (25 _×_ 20 _×_ 45 cm) compatible with standard optical tables (25 _×_ 25 cm grid). The 3D-printed chassis is optimized for rapid assembly, allowing the full unit to be constructed in under four hours. 

**Actuation Module:** Dynamic motion is driven by five Dynamixel XM540 servomotors, peripherally mounted via quick-release couplings. The kinematic chain is split into two stages: two upper motors actuate the Z-axis translation and Yaw rotation, while three lower motors drive a parallel mechanism to generate Roll and Pitch inclinations. High-speed communication and control loops are managed via a U2D2 interface, ensuring precise trajectory tracking. 

**Transmission Mechanism:** To achieve synchronized motion of the two acquisition platforms, we employ a custom gear-driven transmission system. The lower stage utilizes a simplified Stewart platform configuration [66] driven by camfollower mechanisms. Specifically, three vertical columns are arranged radially at 120<sup>_◦_</sup> intervals. Vertical displacement of each column is driven by a rotating cam and constrained by a return spring; simultaneous differential actuation of these columns induces Roll ( _±_ 15<sup>_◦_</sup> ) and Pitch ( _±_ 15<sup>_◦_</sup> ) variations in the pressing plane. The upper stage controls Yaw (360<sup>_◦_</sup> continuous) and Z-axis translation via a cam-gear assembly. Crucially, the Z-axis mechanism includes a compliant element 

5 


Fig. 2: **The hardware design of the tactile-force data acquisition device that autonomously captures synchronized paired frames.** (a) Overall view of the device. (b) Kinematics of the platforms. (c) Force and tactile sensors that mounted on the system. In particular, the vision-based tactile sensor includes four self-made sensors (each silicone surface carrying a distinct marker pattern) and two GelSight Mini supplied in both marker-printed and marker-free versions. (d) Example contact indenter samples with varying patterns, curvatures, and hardness. (e) Synchronized tactile-force frames. 

to maintain constant contact pressure between the indenter and the sensor, preventing overload during high-speed operation. 

**Contact Indenters:** Both the upper and lower platforms feature quick-release grooves to facilitate the rapid exchange of contact indenters. We fabricated a library of 3D-printed samples featuring diverse surface patterns, curvatures, and stiffness levels (see Fig. 2(d)). These samples are mounted in opposing pairs to simulate varied interaction scenarios, ranging from point contacts to conformal surface patches. 

**Force and Tactile Sensors:** The system integrates three distinct sensing modalities: 

- **VBTS:** The Device under test. This tactile sensor captures high-resolution surface deformation at 30 Hz. In this work, we employed four custom-built sensors (marker-free and featuring 4×4, 7×7, and 9×9 densities) alongside two GelSight Mini sensors, one marker-free and the other with a 7×9 marker pattern. The silicone pads of all sensors share identical hardness. 

- **6-Axis Force/Torque Sensing:** An ATI Axia80 sensor measures the 6D wrench at the contact interface. 

- **Matrix Force Sensor:** A calibrated piezoresistive array (12 _×_ 12 taxels) provides spatial force distribution. 

All sensors are connected to the PC via either USB or Ethernet cables. Given that the force sensors operate at frequencies much faster than VBTS, data collection was synchronized to the 30 Hz of the visuotactile sensor via resampling to enable paired data acquisition. 

## _B. TaF-Dataset Construction_ 

We leverage the hardware platform to construct athe TaFDataset, which is designed to establish a mapping between VBTS’s visual output and corresponding physical force measurements. To achieve this, one VBTS sensor is suspended above the right platform, while a 6-axis force/torque sensor, a silicone piece, and a matrix force sensor are mounted in sequence above the left platform. The two elastomer surfaces are manually aligned in height before data collection. For matrix force regions that fall outside the GelSight Mini, we pad them with zeros. Then, two identical indenters are placed on both platforms. This configuration ensures that the tactile and force sensors are subjected to forces of identical magnitude and direction, thereby yielding highly aligned multimodal data. Moreover, the system can record data while applying forces of varying magnitudes and directions to the sensors through indenters, enabling the collection of over 100K synchronized frames per hour and effectively overcoming the scalability limitations of manual data acquisition. 

_1) Automated Generation Protocol:_ The collection process requires human intervention only for swapping indenter sets and different visuotactile sensors. As illustrated in Fig. 2(b), the cycle begins by driving the Z-axis to establish contact between the sensor and the indenter. Once contact is made, the system executes a “press-and-perturb” strategy: it dynamically varies the Z-axis pressure while simultaneously driving the Pitch, Roll, and Yaw motors. This induces continuous and diverse trajectories that explore the full state space of the sensor, ranging from static indentation to incipient slip, and far more efficiently than discrete probing methods. 

6 


Fig. 3: **Overview of the TaF-VLA learning framework.** The architecture consists of two distinct stages: (a) Tactile-Force Alignment (TaFAdapter): We propose a self-supervised learning paradigm. The Force Encoder ( _fϕ′ , fϕ′′_ ) quantizes heterogeneous force signals, distributed pressure maps, and 6-axis F/T vectors, into two discrete codebooks via Vector Quantized Variational Autoencoder (VQ-VAE), creating stable physical anchors. The Tactile Encoder ( _f_ causal-TF) employs a Causal Transformer to process sequential tactile images. These branches are synchronized in a shared latent space via a contrastive InfoNCE objective ( _L_ NCE), effectively teaching the tactile encoder to infer force dynamics from visual deformation. (b) Policy Integration (TaF-VLA): The pre-trained, frozen TaF-Adapter is integrated into a VLA backbone. It injects force-aligned tactile tokens alongside visual and language embeddings, allowing the Action Expert to generate forceaware manipulation trajectories. 

_2) Contact Diversity:_ To ensure the learned representations are robust to the variability of the real world, we explicitly maximize diversity following three strategies: 1) Rather than using fixed position control, we modulate the torque of the Z-axis actuator. This generates temporally continuous contact pressures, allowing the acquisition of sensor response from the lightest touch to deep saturation. 2) By randomizing the rotational velocities of the parallel platform, the system introduces intricate shear forces and torsional moments. This ensures the dataset contains not just normal force data, but also the friction-dominated signals critical for manipulation stability. 3) We employ a diverse library of over 60 distinct indenters, comprising 40 rigid and 20 deformable samples. These range from standard geometric primitives to complex everyday objects with varying curvatures and hardness. This physical variety forces the model to learn generalized deformation features rather than overfitting to specific object shapes. 

_3) Dataset Scale and Statistics:_ The resulting TaF-Dataset is among the largest multi-modal tactile repositories available. To support the cross-sensor generalization claims in this work, we aggregated data across 6 distinct VBTS units, including 4 custom-built variants and 2 commercial GelSight sensors (see Sec. III-A2). In total, the dataset comprises over 10 million synchronized tactile-force pairs, providing the high-fidelity supervision necessary to align the visual and force domains. 

## IV. TACTILE-FORCE ALIGNMENT AND VLA INTEGRATION 

To leverage the collected dataset and integrate force perception into VLA models, we propose the TaF-Adapter. We depart from prior approaches such as direct force regression [30] which fall short in cross-sensor generalization, and tactilevision alignment [28, 67] which captures surface textures but 

neglects physical interaction forces. Instead, the TaF-Adapter employs an implicit alignment strategy, mapping tactile sequences and force signals into a shared latent space. 

To capture the dynamic nature of force, the TaF-Adapter employs historical observations, aligning tactile and force sequences via contrastive learning. Furthermore, to mitigate high-frequency sensor noise, we apply vector quantization, which discretizes the latent space into separate codebooks for 6-axis force/torque measurements and matrix-structured force maps. This design ensures the learning of stable, cross-sensor representations explicitly grounded in physical dynamics. 

We instantiate the TaF-VLA policy by integrating the TaFAdapter into a pretrained VLA backbone [39]. By interleaving force-aligned tactile tokens into the language-action stream, the policy conditions its execution on both semantic instructions and tactile feedback, enabling robust manipulation in contact-rich scenarios. 

## _A. TaF-Adapter: Tactile-Force Alignment_ 

The training architecture for TaF-Adapter (illustrated in Fig. 3(a)) consists of two encoding procedures. First, the force encoder (left) quantizes sequential force signals into a discrete codebook, capturing dynamic force primitives. Second, the tactile encoder (right) encodes temporal sequences of tactile images and is trained to map these visual inputs to their corresponding force tokens via contrastive learning. This design effectively “teaches” the model to perceive the interaction force from VBTS. 

**a) Force Quantization:** Force and pressure signals are typically high-bandwidth and exhibit noise with modalitydependent characteristics. Similar challenges have been widely studied in the speech recognition and action-generation 

7 

communities, where discretized latent representations from VQ-VAE [68] are used to mitigate noise and capture reusable dynamics [69–72]. Following this idea, we encode force within a continuous time window using a learnable VQ-VAE codebook. The resulting discretized tokens represent essential patterns of force primitives while providing compactness and semantic interpretability. 

Let the raw force measurement at time step _i_ be defined as a tuple _Fi_ = ( _Fi_<sup>_′, F_</sup> _i_<sup>_′′_),where:</sup> 

- _Fi_<sup>_′∈_R12</sup><sup>_×_12representsthespatialpressuremap(normal</sup> force distribution). 

- _Fi_<sup>_′′∈_R6representsthe6-axisforce/torquevector(global</sup> wrench). 

To capture temporal information, we operate on a sliding window of length _N_<sup>1</sup> . We employ two dedicated MLP encoders to project these sequences into latent space: 


We define two learnable codebooks, _C_<sup>_′_</sup> = _{c_<sup>_′_</sup> _k_<sup>_}K_</sup> _k_ =1<sup>_′_and</sup> _C_<sup>_′′_</sup> = _{c_<sup>_′′_</sup> _m_<sup>_}K_</sup> _m_ =1<sup>_′′_,correspondingtothepressureandwrench</sup> modalities, respectively. Each latent vector is quantized to its nearest neighbor in the codebook: 


The final force embedding _c_<sup>_∗_</sup> is the concatenation of these quantized tokens: 


The network is trained using the standard VQ-VAE [68] objective, combining reconstruction loss with the quantization loss: 


where sg[ _·_ ] denotes the stop-gradient operator and _β_ is the commitment weight. 

Crucially, relying solely on _L_ quant may lead to _codebook collapse_ [73], a degenerate scenario where the encoder maps diverse inputs to a trivial subset of the codebook. To explicitly prevent this and ensure the discrete tokens preserve highfidelity physical semantics, we introduce a reconstruction mechanism. We employ decoders _gψ′_ and _gψ′′_ to recover the original signal sequences from the quantized embeddings. The total force learning objective combines the reconstruction loss with the quantization regularization: 


By enforcing precise signal reconstruction, the codebook is compelled to span the variance of the force dynamics, thereby serving as a robust anchor for the subsequent tactile alignment. 

**b) Temporal Tactile Encoding:** The tactile encoder is responsible for inferring latent feature from sensor’s visual 

> 1Empirically set to 5 in this paper. 

output. Given a synchronized sequence of tactile images _{Ii_<sup>tac</sup> + _j_<sup>_}N_</sup> _j_ =0<sup>_−_1,wefirstextractper-framefeaturesusingaVision</sup> Transformer (ViT) [74] backbone: 


To aggregate temporal information, which is critical for distinguishing static deformation from slip or hysteresis, we append a learnable summary token _s_ and process the sequence with a causal Transformer encoder: 


The output embedding corresponding to _s_ serves as the holistic representation of the tactile event. 

**c) Cross-Modal Alignment:** To align the tactile representation _z_<sup>_∗_</sup> with the physical force code _c_<sup>_∗_</sup> , we employ a symmetric InfoNCE objective [75]. This contrastive framework enforces that the tactile embedding of a specific interaction event is maximally similar to its ground-truth force code, while being dissimilar to force codes from other time steps. 

For a batch of _B_ synchronized pairs _{_ ( _zb_<sup>_∗, c∗_</sup> _b_<sup>)</sup><sup>_}B_</sup> _b_ =1<sup>,the</sup> alignment loss is defined as: 


where sim( _u, v_ ) = _u_<sup>_⊤_</sup> _v/_ ( _∥u∥∥v∥_ ) is the cosine similarity and _τ_ is a temperature hyperparameter. The total training objective for the TaF-Adapter is a weighted sum of the alignment and quantization losses: 


By adopting a sliding-window temporal sampling strategy, the model learns the temporal evolution of contact forces directly from sequential observations. As a result, temporally adjacent frames exhibit naturally emerging similarity in the latent space, eliminating the need for manually designed distance metrics or explicit adjacency constraints. 

## _B. Force-aware VLA Policy Integration_ 

We integrate the pre-trained TaF-Adapter into a state-ofthe-art VLA backbone to instantiate the TaF-VLA policy. We build upon the _π_ 0 _._ 5 architecture [39], a flow-matching-based generalist policy. 

Given a third-person image _I_ global, a wrist-mounted image _I_ wrist, and a language instruction _l_ , the encoder outputs a unified conditioning vector: 


which provides high-level task semantics and global scene context for action generation. 

To integrate tactile feedback, we fuse TaF-Adapter features with _φ_ . The adapter extracts local contact cues from a sliding window of VBTS tactile signals (see Eq. (9)). The tactileconditioned flow-matching objective is: 


8 


Fig. 4: Overview of the eight force-aware manipulation tasks. Blue arrows indicate end-effector trajectories. 

where _at_ is the ground-truth action, _u ∼N_ (0 _, I_ ) is noise, and _a_<sup>_τ_</sup> _t_<sup>=</sup><sup>_τat_+ (1</sup><sup>_−τ_)</sup><sup>_u_followsstandardconditionalflow-</sup> matching. Here, _qt_ denotes robot proprioception. The policy _πθ_ learns a velocity field that drives _a_<sup>_τ_</sup> _t_<sup>toward</sup><sup>_at_under</sup> conditioning from _φt, zt_<sup>tac</sup> _,_ and _qt_ . 

During inference, TaF-VLA generates an action by integrating the learned velocity field from noise to a clean action. Starting from _A_<sup>0</sup> _t_<sup>_∼N_(0</sup><sup>_, I_),theactionestimateisupdatedas:</sup> 


where _vθ_ is the learned velocity field and _δ_ = 0 _._ 1 (following _π_ 0 _._ 5). Integrating _τ ∈_ [0 _,_ 1] yields a noise-free action _A_<sup>1</sup> _t_ executed by the robot. 

By conditioning on the global visual–language features _φ_ and the local tactile latent _zt_<sup>tac</sup> , TaF-VLA generates actions that remain both controllable and contact-aware. This design enables real-time adjustment of manipulation behaviors based on tactile feedback while consistently following high-level task directives. 

## V. EXPERIMENTS 

To evaluate the efficacy of the proposed TaF-VLA framework and the underlying TaF-Adapter, we conduct a comprehensive suite of real-world, contact-rich manipulation experiments. Our analysis addresses four primary research questions: 

- (E1) **Performance Benchmarking:** Does the proposed explicit tactile-force alignment (TaF-Adapter) allow TaFVLA to outperform state-of-the-art vision-only and tactile-vision aligned baselines on diverse contact-rich tasks? (Sec. V-B) 

- (E2) **Generalization & Robustness:** Can the TaF-Adapter generalize across different sensor hardware, and does its “plug-and-play” nature benefit other policy architectures? (Sec. V-C) 

- (E3) **Training Efficiency:** Does integrating multi-modal feedback improve sample efficiency, allowing the model to outperform vision-only baselines with fewer demonstrations? (Sec. V-D) 

- (E4) **Ablation Studies:** What is the impact of specific design choices, such as using historical observations and discrete vector quantization, on system performance? (Sec. V-E) 

## _A. Experimental Setup_ 

_1) Training and Evaluation Settings:_ For policy training, we curated a dataset comprising over 10,000 force-aware episodes across more than 20 diverse scenarios, ranging from fragile object handling to complex tool use (see Appendix A). For quantitative evaluation, we defined a targeted suite of 8 real-world, contact-rich tasks, as shown in Fig. 4. These tasks were specifically selected to span different types of physical interactions, aiming to comprehensively evaluate the model’s force-reasoning capabilities. A detailed breakdown of the protocols and success criteria is provided in Appendix B. 

_2) Baselines:_ We compare TaF-VLA against five _opensource_ baselines representing the current state-of-the-art: 

- **Action Chunking with Transformers (ACT)** [76]: A standard Action Chunking with Transformers policy that relies solely on RGB images and proprioception. 

- **FreeTacMan** [29]: A representative _vision–tactile alignment_ baseline implemented on the ACT architecture. It treats tactile feedback as auxiliary visual tokens, lacking explicit physical grounding. 

- **ACT + TaF-Adapter** : The standard ACT policy augmented with our pre-trained TaF-Adapter, validating the benefit of tactile-force alignment over tactile-vision alignment (FreeTacMan) on the same backbone. 

- **Diffusion Policy (DP)** [77]: A generative behavior cloning policy based on denoising diffusion, trained using only RGB images and proprioception. 

- **DP + TaF-Adapter** : The standard Diffusion Policy augmented with our TaF-Adapter, demonstrating the adapter’s generalization to generative frameworks. 

- **_π_ 0** **_._ 5** [39]: A state-of-the-art VLA foundation model finetuned on our dataset using only visual observations, serving as the vision-only backbone for our proposed TaF-VLA. 

9 

TABLE I: Quantitative comparison of task success rates (%) across seven manipulation tasks for all evaluated methods. Bold numbers denote the best-performing policy, while underlined numbers indicate the second-best-performing policy. 

|**Task**||**ACT Back**<br>|**bone**<br>|**Diffu**<br>|**sion Backbone**<br>|**VL**|**A(****_π_) Backbone**<br>|
|---|---|---|---|---|---|---|---|
||ACT|FreeTacMan|+TaF-Adapter|DP|+TaF-Adapter|_π_0_._5|TaF-VLA (Ours)|
|Tube Insertion|26.7|53.3|46.7|33.3|46.7|53.3|**66.7**|
|Tweezer Weight Pick|0.0|6.7|13.3|0.0|6.7|0.0|**33.3**|
|Power Bank Extraction|26.7|33.3|53.3|20.0|40.0|33.3|**66.7**|
|Whiteboard Erasing|13.3|26.7|33.3|20.0|33.3|33.3|**60.0**|
|Jelly Slicing|13.3|26.7|26.7|13.3|33.3|13.3|**53.3**|
|Heavy Part Lifting|40.0|66.7|73.3|46.7|66.7|53.3|**80.0**|
|Chocolate Grasping|66.7|86.7|86.7|73.3|86.7|73.3|**93.3**|
|**Average Success**|26.7|42.8|47.6|29.5|44.7|37.1|**64.8**|


All models (including baselines and TaF-VLA) are trained using the same dataset, and all real-world evaluations run with inference on an NVIDIA RTX 4090 workstation. Task performance is measured using _success rate_ (the criteria are described in Appendix B). Each model is given 15 rollout trials per task, and the success rate is computed as the proportion of successful attempts. Success criteria are task-dependent and represented as binary completion conditions (whether the task is successfully completed). 

## _B. Comparison with Baselines_ 

To highlight the advantages of our force-aware policy, we benchmarked it against several baselines on the aforementioned tasks. Tab. I summarizes the quantitative results. Specifically, TaF-VLA achieves the highest success rate across all scenarios. The performance advantage is most pronounced in force-critical tasks, where TaF-VLA outperforms the strongest baseline by a substantial margin. 

**Comparison to Vision-only Policies:** Overall, performance advantages are evident for TaF-VLA compared to visiononly policies, as shown in Tab. I. Furthermore, we observed that task performance varies substantially depending on the task content. In tasks dominated by geometric constraints, such as _Tube Insertion_ where the initial alignment is paramount, vision-only baselines ( _e.g_ ., _π_ 0 _._ 5) already perform well (53 _._ 3%), confirming that visual servoing is sufficient when spatial alignment is the primary objective. In these scenarios, the addition of tactile sensing yields only marginal gains. However, the disparity becomes evident in tasks requiring dynamic force modulation. For heavier or frictiondependent objects, such as _Tweezer Weight Pick_ and _Power Bank Extraction_ , vision-only baselines frequently fail ( _e.g_ ., DP, ACT, and _π_ 0 _._ 5 all achieve 0% on _Tweezer Weight Pick_ ). We observed that beyond pre-contact errors, these policies fail to apply sufficient grasp force to prevent incipient slip. This occurs because micro-slip cues are visually imperceptible until the object has already been dropped. Similarly, in _Whiteboard Erasing_ and _Jelly Slicing_ , vision-only policies struggle to regulate contact pressure, leading to either trajectory drift or substrate damage. TaF-VLA excels in these regimes, achieving 60 _._ 0% on _Whiteboard Erasing_ and 53 _._ 3% on _Jelly Slicing_ . By 

grounding tactile feedback in physical force, the policy detects contact transitions and shear resistance successfully, enabling stable closed-loop control. 

**Impact of Tactile-Force Alignment:** We compared TaFVLA with other tactile-based policies to evaluate the effect of our tactile-force alignment design. The results show that TaF-VLA outperforms FreeTacMan by a substantial margin ( _e.g_ ., +26.6% on _Tweezer Weight Pick_ and +33.3% on _Whiteboard Erasing_ ). These findings collectively validate our core hypothesis: treating tactile data merely as “auxiliary vision” is insufficient for force-aware tasks. While FreeTacMan captures the _appearance_ of contact, it lacks the calibrated understanding of _magnitude_ necessary to regulate interactions. In contrast, by grounding tactile embeddings in physical force and pressure, TaF-VLA successfully handles force-sensitive tasks, such as detecting stiffness boundaries in _Jelly Slicing_ and managing binding friction in _Power Bank Extraction_ with significantly higher success rates. Visualizations of successful rollouts are shown in Fig. 5. 

**Plug-and-Play Capability:** A key finding is that simply attaching the TaF-Adapter to an existing policy yields immediate performance gains. We evaluated the _ACT + TaF-Adapter_ and _DP + TaF-Adapter_ variants, both of which consistently outperform their vanilla counterparts across all tasks, with absolute improvements ranging from 6.7% to 33.3%. For example, on _Jelly Slicing_ , the success rate of DP increases from 13.3% to 33.3% when augmented with the TaF-Adapter. Interestingly, when the standard ACT baseline is equipped with our TaFAdapter, it surpasses its previous tactile-enhanced variant FreeTacMan in force-critical scenarios ( _e.g_ ., +20.0% on _Power Bank Extraction_ ). These results demonstrate that the TaFAdapter functions as a general-purpose module capable of injecting physical tactile intuition into standard visuomotor policies. 

## _C. Cross-sensor Robustness_ 

A fundamental design question in tactile perception is how to utilize the extracted information better. While our TaFAdapter aligns tactile representations with force in a latent space, a commonly explored alternative is to explicitly regress force values from tactile images [63, 78] and feed these 

10 


Fig. 5: **Successful execution sequences across the evaluated task suite:** (a) Tube Insertion; (b) Tweezer Weight Pick; (c) Power Bank Extraction; (d) Whiteboard Erasing; (e) Jelly Slicing; (f1) Heavy Part Lifting (Buckle); (f2) Heavy Part Lifting (Door Handle); (h) Tongs Food Pick; (i) Chocolate Grasping. 

predictions into the policy. To validate our design choice, we conducted a comparative study between two pipelines: 1) **TaF-Adapter (Ours):** The VLA policy receives highdimensional latent tokens that are contrastively aligned with force dynamics; 2) **Force Prediction:** We train a supervised encoder-decoder on the TaF-dataset to regress 6-axis force/torque and matrix force maps directly from tactile images. These predicted values are then fed as input to the same VLA backbone. We evaluate both methods on four diverse 

tasks ( _Chocolate Grasping_ , _Heavy Part Lifting_ , _Tongs Food Pick_ , and _Whiteboard Erasing_ ), assessing both in-distribution performance and cross-sensor robustness. The results are summarized in Tab. II. 

**a) Performance on Seen Sensors:** We first evaluate performance on sensors encountered during pre-training (CUSTOM-BUILT A and GELSIGHT, denoted as “Seen” sensors). As shown in Table II, the TaF-Adapter consistently outperforms the explicit prediction baseline. Specifically, on 

11 

TABLE II: Performance (success rates, %) comparison of different tactile encoding methods across sensors. “Seen” denotes sensors used during training; “Unseen” denotes out-of-distribution sensors. 

||**Custom**|**-built A (Seen)**|**Custom**|**-built B (Unseen)**|**GelS**|**ight (Seen)**|**GelSi**|**ght (Unseen)**|
|---|---|---|---|---|---|---|---|---|
|**Task**|Ours|Force Pred.|Ours|Force Pred.|Ours|Force Pred.|Ours|Force Pred.|
|Whiteboard Erasing|**60.0**|**60.0**|**53.3**|13.3|**46.7**|40.0|**33.3**|6.67|
|Heavy Part Lifting|**80.0**|66.7|**67.7**|40.0|**73.3**|60.0|**66.7**|33.3|
|Tongs Food Pick|**66.7**|53.3|**46.7**|0.0|**53.3**|46.7|**40.0**|0.0|
|Chocolate Grasping|**93.3**|86.7|**73.3**|66.7|**86.7**|**86.7**|**73.3**|53.3|


the CUSTOM-BUILT A sensor, the TaF-Adapter achieves an average success rate of 75.0%, compared to 66.7% for the force-prediction baseline (an absolute gain of +8 _._ 3%). Similarly, on the GELSIGHT sensor, our method achieves 65.0% versus 58.3% (+6 _._ 7%). 

**Analysis:** These results indicate that TaF-adapter generates representations that are more informative for downstream manipulation than the force-prediction strategy. We attribute this robustness to the adapter’s ability to preserve richer visual–tactile structure relevant to contact-rich manipulation, rather than collapsing the signal into low-dimensional force estimates that may discard task-critical information. In addition, task-specific fine-tuning enables the encoder to capture manipulation-relevant tactile cues, further improving its downstream effectiveness. 

**b) Cross-Sensor Generalization (Unseen Sensors):** We also highlight that our TaF-Adapter exhibits strong zero-shot generalization to sensors not encountered during pre-training, as shown in Table II. When directly evaluated on the CUSTOMBUILT B (UNSEEN) sensor, which did not appear in the TaFAdapter’s pre-training phase (denoted as “unseen”; see Fig. 6). On CUSTOM-BUILT B, the TaF-Adapter maintains a robust mean success rate of 60.3%. In sharp contrast, the forceprediction baseline suffers a catastrophic performance drop, falling to 30.0%. A similar trend is observed on the unseen GELSIGHT unit, where our method achieves 53.3% compared to just 23.3% for the baseline. 

**Analysis:** Explicit force regression models are insensitive to minor domain shifts ( _e.g_ ., lighting changes, gel wear, or marker displacement), as they rely on precise pixel-level mappings to output force values. When these mappings drift, the predicted force becomes noisy or erroneous, misleading the policy. The TaF-Adapter, however, aligns representations in a semantic latent space. This contrastive alignment encourages the model to learn force-relevant features that are invariant to low-level sensor noise, resulting in significantly superior cross-sensor transferability. 

## _D. Pretrained TaF-Adapter Improves Data Efficiency_ 

We further demonstrate that initializing the VLA backbone with our pre-trained TaF-Adapter yields substantial gains in _data efficiency_ . To quantify this, we evaluated TaF-VLA against the vision-only baseline ( _π_ 0 _._ 5) across three representative contact-rich tasks ( _Tongs Food Pick_ , _Power Bank Extraction_ , and _Chocolate Grasping_ ), training on data subsets 


Fig. 6: Three VBTS configurations. 


Fig. 7: **Effect of training data amount on task performance.** This figure compares the performance of TaF-VLA with that of the visiononly baseline _π_ 0 _._ 5 under varying training data budgets. 

of 100, 150, and 200 demonstrations. The quantitative trends are visualized in Fig. 7. 

As expected, the vision-only _π_ 0 _._ 5 relies heavily on dataset scale: its success rate improves incrementally from 13.3% _→_ 40.0% on _Tongs Food Pick_ , 13.3% _→_ 33.3% on _Power Bank Extraction_ , and 60.0% _→_ 73.3% on _Chocolate Grasping_ as the dataset increases from 100 to 200 episodes. Crucially, TaF-VLA achieves equivalent or superior performance using only 100 demonstrations—effectively matching the baseline’s best performance while using half the data. This confirms that the force-aligned tactile codebook provides structured physical priors, significantly reducing the number of demonstrations required to learn complex, force-sensitive manipulation skills. 

12 

## _E. Ablation Studies_ 

TaF-VLA relies on specific architectural choices to ensure robust alignment. To quantify the contribution of each component, we conducted ablation studies across three representative tasks: _Whiteboard Erasing_ , _Tweezer Weight Pick_ , and _Jelly Slicing_ . The results are summarized in Tab. III. 

**Necessity of Temporal Context:** We found that incorporating historical observations is essential for force-aware manipulation. Reducing the receding horizon window from _N_ = 5 to a single frame ( _N_ = 1) leads to substantial performance degradation (refer to “No History” in Tab. III). This sensitivity arises because physical interaction is inherently history-dependent: a static grasp and a grasp undergoing incipient slip often yield identical instantaneous deformation images. Disambiguating these states requires temporal context to estimate the rate of change in the deformation field. 

**Impact of Codebook Capacity:** We find that the capacity of the codebook plays a critical role in overall model performance (refer to “Small Codebook” in Tab. III). Reducing the codebook size leads to a decline in success rates. This degradation occurs because an undersized codebook forces different tactile–visual features to collapse into the same codebook entries, causing a loss of representational granularity. Consequently, the encoder fails to preserve subtle cues that are necessary to distinguish fine-grained interaction states. 

**Benefits of Decoupled Modalities:** Using two separate codebooks is also essential for achieving high success rates. To validate this, we evaluated a variant in which both the pressure maps and the global 6-DoF force vectors are projected into a single shared codebook (refer to “Shared Codebook” in Tab. III). This configuration performs poorly across all three benchmark tasks. This degradation underscores that global F/T vectors (low-dimensional, high-magnitude signals) and pressure maps (high-dimensional, spatial signals) exhibit fundamentally different latent distributions. Forcing them into a unified latent space causes modality-specific information to be aliased or lost. In contrast, our decoupled design preserves both the spatial geometry captured by pressure maps and the global dynamics encoded in force–torque vectors. 

**Quality of Tactile Data:** Model performance also depends heavily on the quality of tactile data collected by our hardware platform (Sec. III-A). When the force signals are perturbed, performance decreases substantially. To illustrate this effect, we trained a variant in which the ground-truth force labels were artificially corrupted with Gaussian noise. As shown by the “w/ Noise” configuration in Tab. III, this variant exhibits degraded performance. We attribute this drop to the difficulty of learning a meaningful alignment when the force modality is anchored to noisy or inconsistent labels. These results highlight the necessity of a stable and low-disturbance data acquisition pipeline, such as the one enabled by our device. 

## VI. DISCUSSION AND LIMITATIONS 

## _A. Key Findings_ 

The experimental evaluation yields three critical insights regarding the integration of tactile perception into generalist policies: 

TABLE III: Ablation study results. The full pipeline achieves the highest overall performance, whereas each ablated variant exhibits a measurable reduction. 

|**Task**|**No**<br>**History**|**Small**<br>**Codebook**|**Shared**<br>**Codebook**|**w/**<br>**Noise**|**Ours**<br>**(Full)**|
|---|---|---|---|---|---|
|Whiteboard Erase|26.7|46.7|13.3|13.3|**60.0**|
|Weight Pick|20.0|20.0|13.3|0.0|**33.3**|
|Jelly Slice|26.7|20.0|6.7|6.7|**53.3**|


**When Manipulation Requires Force Knowledge:** Our results show that the necessity of force sensing is highly taskdependent. For tasks involving lightweight objects where only gentle or bounded forces are required ( _e.g_ ., _Chocolate Grasping_ ), the vision-only baseline ( _e.g_ ., _π_ 0 _._ 5) performs comparably to tactile-based approaches. However, for _force-critical_ tasks that require active modulation of contact forces ( _e.g_ ., _Heavy Part Lifting_ , _Power Bank Extraction_ ), relying solely on vision leads to significantly degraded performance. For example, in the _Tweezer Weight Pick_ task, the vision-only baseline fails completely regardless of how the language instructions are configured, as RGB observations do not contain information sufficient to infer stiffness, friction, or shear forces that are essential for successful manipulation. In contrast, the TaFAdapter overcomes this limitation by providing an explicit, force-aware representation that enables the policy to regulate physical interactions effectively. 

**Discrete Representations Enable Generalization:** Our evaluation shows that representing tactile features in a discrete space is critical for achieving strong generalization performance. The discrete codebook representation consistently outperforms continuous latent embeddings, despite the widespread use of continuous spaces in previous tactile learning research [28]. We found that discretization suppresses high-frequency noise and hardware-specific artifacts while retaining the essential physical cues needed for downstream reasoning. This is further supported by our zero-shot generalization results on sensors that are visually similar but structurally different, demonstrating that discrete quantization is a key mechanism for hardware-agnostic tactile perception. 

## _B. Limitations and Future Work_ 

**Failure Modes:** Failures were observed during our experiments. Most failures for TaF-VLA occurred during the precontact phase. A predominant failure mode involves errors in manipulator control during free motion, where the manipulator fails to accurately reach the desired position. This is particularly critical in tasks requiring high precision, such as _Tweezer Weight Pick_ , where the end-effector stops millimeters short of the target surface. This “air gap” prevents the establishment of initial contact necessary to trigger the tactile–force feedback loop. Additionally, despite the involvement of the TaF-adapter, some failures still arise from insufficient force applied during the interaction process. Examples of these failure cases are illustrated in Fig. 8. 

**Inference Frequency:** Our approach leverages recedinghorizon action output. While predicting a long horizon of future actions ensures trajectory smoothness, it inherently 

13 


Fig. 8: **Failure cases arising from insufficient force perception.** Examples highlight critical failures caused by inadequate grounding of physical forces: (a) The policy fails to maintain adequate clamping force, causing the tweezers to slip and drop the weight during transport. (b) When handling heavy objects, the system fails to exert sufficient force to counteract gravity, leading to the object dropping. 

limits the frequency of closed-loop corrections. As a result, the policy exhibits latency and is prone to failure during high-frequency dynamic events, such as handling force spikes in _Jelly Slicing_ , where physical dynamics evolve faster than the reactive replanning cycle. Moreover, force interactions are inherently fast, highlighting the need for architectures capable of faster inference to meet the demands of high-frequency force control. 

**Generalization Scope:** Our approach demonstrates generalizability across sensors. However, the cross-sensor evaluation is limited to sensors that are relatively similar. The sensors we tested operate on the same visuotactile sensing mechanism and incorporate visual markers on their elastomer. It remains inconclusive how well the approach generalizes to sensors that are highly different, such as those based on capacitive, magnetic, or piezoresistive arrays, which rely on non-visual encoding mechanisms. 

**Data Acquisition Hardware:** The current TaF-Dataset is collected using custom TaF-device that are primarily fabricated through 3D printing. Due to the inherent precision constraints of consumer-grade additive manufacturing, the captured force signals and corresponding ground-truth measurements inevitably contain small structural and geometric deviations. These fabrication-induced inconsistencies may introduce minor biases into the learned tactile-force representations. Future iterations of the hardware could incorporate redesigned transmission mechanisms ( _e.g_ ., direct drive) and high-precision machining ( _e.g_ ., CNC milling or lathe finishing) to improve sensor fidelity and yield more accurate ground-truth force measurements. 

**Alternative Architecture Designs:** In our current design, the TaF-Adapter is integrated as input to the action expert. This choice facilitates easier fine-tuning and faster inference. However, it may not be optimal, as humans use tactile information not only to adjust their grip but also to update their understanding of the environment ( _e.g_ ., realizing a surface is slippery and modifying their plan entirely). A model with deeper tactile integration could support far richer semantic reasoning. Therefore, exploring a fully unified Vision-Tactile- 

Language-Action backbone is meaningful. Nevertheless, we anticipate that this approach would require scaling up data collection efforts well beyond current limits and remains unexplored in the present work. 

## VII. CONCLUSION 

In this paper, we present TaF-VLA, a framework designed to address the fundamental “force-blindness” of current generalist robot policies. Our core insight is that directly using tactile images from VBTS may omit the underlying force priors they convey. To capture this force-semantic information, we propose the TaF-Adapter, a neural encoder trained to align VBTS latent codes with those from a separate force and pressure sensor array via contrastive learning. 

To support this training, we developed an automated, scalable data acquisition device to collect tactile-force-aligned data, which are otherwise scarce. This resulted in the TaFDataset, providing over 10 million synchronized frames of VBTS images, 6D force/torque measurements, and matrix pressure maps—serving as a valuable resource for the research community. 

We then demonstrated the integration of the TaF-Adapter into the TaF-VLA VLA model and conducted comprehensive evaluations. TaF-VLA achieves an average success rate of 64.8%, roughly doubling the performance of state-of-the-art vision-only baselines and outperforming existing vision–tactile methods by 19–22 percentage points. Furthermore, we show that this force-aligned representation enables new capabilities in language-conditioned manipulation, allowing the robot to execute fine-grained force-modulation commands that were previously intractable. These results suggest that TaF-VLA advances the acquisition of dexterous, generalist tactile-based skills and highlights the importance of explicitly grounding tactile perception with physical forces. 

## APPENDIX 

## _A. Force-aware Manipulation Dataset Construction_ 

To facilitate the learning of force-aware manipulation policies, we curate the force-aware manipulation dataset. As illus- 

14 


Fig. 9: **Overview of the force-aware manipulation dataset construction pipeline.** We utilize a high-fidelity master-puppet teleoperation system (middle figure) to collect over 10,000 real-world manipulation episodes across 20+ diverse tasks, ranging from fragile object handling to tool use (left figure). To bridge the semantic gap between high-level goals and low-level control, we employ an LLM-based prompting framework (right figure) to generate force-aware task instructions. This process empowers force-aware directives, providing the hierarchical supervision necessary for force-aware downstream policy learning. 

trated in Fig. 9, the dataset included real-world demonstrations featuring high-fidelity visual and tactile modalities. 

_1) Teleoperation Interface:_ An overview of the data collection pipeline is presented in Fig. 2 (middle figure). We developed a teleoperation interface to control the arm motion. The system leverages a full-scale exoskeleton controller that is mechanically isomorphic to the Franka Research 3 (FR3) robot arm. Equipped with high-resolution joint encoders, the exoskeleton streams joint-space commands directly to the robot with low latency. 

_2) Selection of Force-aware Manipulation Tasks:_ The dataset spans a broad range of physical interactions with objects of different stiffness, weight, and geometry, requiring the robot to modulate grip force according to object compliance and mass. Tasks include fragile items that demand minimal force to avoid damage and heavy, low-friction objects that require higher force to prevent slippage. Across these diverse conditions, the model must infer the appropriate force level from physical feedback to maintain a stable grasp. 

In addition to direct grasping, the dataset includes tool-use scenarios such as using tweezers to lift weights. These tasks introduce extended kinematic chains in which the robot acts indirectly on the environment. The tool functions as a lever, amplifying rotational moments at the fingertips, so the policy must actively stabilize the tool during transport and reason about the dynamics of the coupled tool–hand system rather than a single contact point. 

The dataset also contains tasks defined by dynamic surface interaction, where the objective is continuous regulation of contact rather than object retention. In the whiteboard-cleaning task, the robot must guide an eraser across the surface while maintaining steady normal force and compensating for shear to prevent skipping. In the precision-cutting task (slicing jelly on a balloon), the robot must detect the sharp change in resistance when the blade transitions from jelly to balloon and terminate the motion immediately. These scenarios evaluate the policy’s ability to operate as a responsive feedback controller, adapting its trajectory in real time as physical conditions change. 

_3) Force-aware Instruction Generation:_ A common limitation of existing manipulation datasets is the lack of language descriptions of tactile data. To address this, the forceaware manipulation dataset augments every demonstration with force-grounded language annotations. We employ an automated annotation pipeline driven by a pretrained Large Language Model (LLM) via a physics-informed Chain-ofThought (CoT) prompting strategy. The prompt template used for generating the TaF-Dataset is showcased in Fig. 10. 

## _B. Description of Task Suite_ 

This section details the contact-rich manipulation tasks used in our evaluation. 

**(a) Tube Insertion:** Insert a test tube into a tight slot. As the tube is relatively slippery, the primary challenge is precise pose alignment. Force regulation is also required to prevent jamming caused by lateral contact forces. _Success:_ Full insertion without jamming or forceful collision. 

**(b) Tweezer Weight Pick:** A tool-use task involving tweezers that introduces an extended kinematic chain. The policy must manage delicate force transmission and counterrotational moments at the tool tips. _Success:_ Transport and place at least two weights without dropping. 

**(c) Power Bank Extraction:** Extract a unit from a frictionfit slot. The task requires a stable grasp and precise directional pulling to overcome friction without binding or slip. _Success:_ Complete extraction and placement without slippage or collision. 

**(d) Whiteboard Erasing:** Guide an eraser along a specified trajectory while regulating normal and shear forces. Insufficient pressure causes intermittent contact; excessive force increases friction and may impede motion. _Success:_ Successfully remove all marks along the trajectory. 

**(e) Jelly Slicing:** Slice soft jelly placed atop a balloon. The robot must detect the stiffness transition via torque feedback and halt immediately upon reaching the balloon surface. _Success:_ Fully slice the jelly without rupturing the balloon. 

**(f) Heavy Part Lifting:** Lift and transport a heavy automotive component. The task requires a sustained high grip 

15 

**System message** : You are a domain expert in robotic manipulation and physical interaction. Your task is to translate a high-level manipulation instruction into a concise, executable command that specifies how the action should be performed. Your output must use only abstract force descriptors ( _e.g_ ., “gently”, “apply light pressure”, “use minimal force”) and must never include numerical force values. Keep the final instruction brief, actionable, and focused on force-aware execution. **Original task instruction:** A robot arm is tasked to Task Instruction. **Physical Analysis:** Provide a concise assessment of the object’s key physical properties relevant to manipulation ( _e.g_ ., fragility, stiffness, deformability, compliance, surface friction, mass distribution). Focus only on attributes that directly influence how the object should be handled. Keep this section brief and factual. **Strategy Derivation:** Provide a concise, high-level manipulation strategy that specifies how the object should be handled using only qualitative force descriptors. Do not include numerical forces, detailed step-by-step procedures, or multi-stage reasoning. Keep this strategy brief and focused on the underlying force principles. **Force-aware task instruction:** Rewrite the original instruction as a concise, execution-ready, and force-aware command. Use only abstract, qualitative force terms ( _e.g_ ., “gently secure”, “apply minimal pressure”, “lift softly”), and avoid enumerated steps, procedural detail, or any numerical force specification. **Output Format:** Please generate output following the JSON format below: { "physical analysis": "...", "strategy derivation": "...", "force-aware instruction": "...", } 

Fig. 10: Prompt templates used for annotating the force-aware manipulation dataset. 

force to counter gravity and prevent incipient slip. _Success:_ Transport to the target location without slippage or loss of contact. 

**(g) Tongs Food Pick:** Manipulate irregular food items using compliant tongs. The policy must account for tool compliance and variable surface friction to maintain stability. _Success:_ Securely grip, transport, and place the item without dropping. 

**(h) Chocolate Grasping:** Grasp and transport a brittle chocolate object. The robot must balance slip prevention against fracture risk. _Success:_ Transport without breakage or surface damage. 

**(i) Crisp Grasping:** Grasp a crisp, representing an extreme fragility case with near-zero tolerance for force overshoot. _Success:_ Transport the crisp intact without cracking or shattering. 

## REFERENCES 

- [1] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. Fei-Fei, A. Anandkumar, Y. Zhu, and L. Fan, “Vima: General robot manipulation with multimodal prompts,” _arXiv preprint arXiv:2210.03094_ , 2022. 

- [2] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [3] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [4] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, _et al._ , “Openvla: An opensource vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [5] Y. Zhu, D. Yang, and Y. Lee, “Deformable and fragile object manipulation: A review and prospects,” _Sensors_ , vol. 25, no. 17, p. 5430, 2025. 

- [6] W. Li, P. Lin, M. Wang, C. Xiao, K. Althoefer, Y. Su, Z. Jiao, and H. Liu, “R-tac0: A rounded high-frequency transferable monochrome vision-based tactile sensor for shape reconstruction,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 10400–10407, 2025. 

- [7] Z. Zhu and H. Hu, “Robot learning from demonstration in robotic assembly: A survey,” _Robotics_ , vol. 7, no. 2, p. 17, 2018. 

- [8] J. Zhao, Y. Ma, L. Wang, and E. Adelson, “Transferable tactile transformers for representation learning across diverse sensors and tasks,” in _Proceedings of Conference on Robot Learning (CoRL)_ , pp. 3766–3779, PMLR, 2025. 

- [9] P. Lin, Y. Huang, W. Li, J. Ma, C. Xiao, and Z. Jiao, “Pp-tac: Paper picking using tactile feedback in dexterous robotic hands,” _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [10] B. Wen, C. Mitash, S. Soorian, A. Kimmel, A. Sintov, and K. E. Bekris, “Robust, occlusion-aware pose estimation for objects grasped by adaptive hands,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , pp. 6210–6217, IEEE, 2020. 

- [11] P. Hao, C. Zhang, D. Li, X. Cao, X. Hao, S. Cui, and S. Wang, “Tla: Tactile-language-action model for contact-rich manipulation,” _arXiv preprint arXiv:2503.08548_ , 2025. 

- [12] J. Bi, K. Y. Ma, C. Hao, M. Z. Shou, and H. Soh, “Vla-touch: Enhancing vision-language-action models with dual-level tactile feedback,” _arXiv preprint arXiv:2507.17294_ , 2025. 

- [13] S. Yu, K. Lin, and H. Soh, “Demonstrating the octopi-1.5 visual-tactilelanguage model,” _arXiv preprint arXiv:2507.09985_ , 2025. 

- [14] Y. Chen, A. Sipos, M. Van der Merwe, and N. Fazeli, “Visuo-tactile transformers for manipulation,” _arXiv preprint arXiv:2210.00121_ , 2022. 

- [15] J. Yu, H. Liu, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai, _et al._ , “Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation,” _arXiv preprint arXiv:2505.22159_ , 2025. 

- [16] L. Pei, H. Yuzhe, L. Wanlin, X. Chenxi, and J. Ziyuan, “Dexmove: Learning tactile-guided non-prehensile manipulation with dexterous hands,” in _The Fourteenth International Conference on Learning Representations_ , 2026. 

- [17] J. J. Liu, Y. Li, K. Shaw, T. Tao, R. Salakhutdinov, and D. Pathak, “Factr: Force-attending curriculum training for contact-rich policy learning,” _arXiv preprint arXiv:2502.17432_ , 2025. 

- [18] Z. Zhang, H. Xu, Z. Yang, C. Yue, Z. Lin, H.-a. Gao, Z. Wang, and H. Zhao, “Ta-vla: Elucidating the design space of torque-aware visionlanguage-action models,” _arXiv preprint arXiv:2509.07962_ , 2025. 

- [19] M. Y. Cao, S. Laws, and F. R. y Baena, “Six-axis force/torque sensors for robotics applications: A review,” _IEEE Sensors Journal_ , vol. 21, no. 24, pp. 27238–27251, 2021. 

- [20] N. F. Lepora, “Soft biomimetic optical tactile sensing with the tactip: A review,” _IEEE Sensors Journal_ , vol. 21, no. 19, pp. 21131–21143, 2021. 

- [21] R. Calandra, A. Owens, M. Upadhyaya, W. Yuan, J. Lin, E. H. Adelson, and S. Levine, “The feeling of success: Does touch sensing help predict grasp outcomes?,” _arXiv preprint arXiv:1710.05512_ , 2017. 

- [22] S. Luo, N. F. Lepora, W. Yuan, K. Althoefer, G. Cheng, and R. Dahiya, “Tactile robotics: An outlook,” _Transactions on Robotics (T-RO)_ , 2025. 

- [23] R. Calandra, A. Owens, D. Jayaraman, J. Lin, W. Yuan, J. Malik, E. H. Adelson, and S. Levine, “More than a feeling: Learning to grasp and regrasp using vision and touch,” _Robotics and Automation Letters (RAL)_ , vol. 3, no. 4, pp. 3300–3307, 2018. 

- [24] W. Yuan, S. Dong, and E. H. Adelson, “Gelsight: High-resolution robot tactile sensors for estimating geometry and force,” _Sensors_ , vol. 17, no. 12, p. 2762, 2017. 

- [25] D. Ma, E. Donlon, S. Dong, and A. Rodriguez, “Dense tactile force estimation using gelslim and inverse fem,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , pp. 5418–5424, IEEE, 2019. 

- [26] M. Lambeta, P.-W. Chou, S. Tian, B. Yang, B. Maloon, V. R. Most, D. Stroud, R. Santos, A. Byagowi, G. Kammerer, _et al._ , “Digit: A novel design for a low-cost compact high-resolution tactile sensor with application to in-hand manipulation,” _Robotics and Automation Letters (RA-L)_ , vol. 5, no. 3, pp. 3838–3845, 2020. 

- [27] W. Yuan, R. Li, M. A. Srinivasan, and E. H. Adelson, “Measurement of shear and slip with a gelsight tactile sensor,” in _Proceedings of_ 

16 

- _International Conference on Robotics and Automation (ICRA)_ , pp. 304– 311, IEEE, 2015. 

- [28] S. Yu, K. Lin, A. Xiao, J. Duan, and H. Soh, “Octopi: Object property reasoning with large tactile-language models,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [29] L. Wu, C. Yu, J. Ren, L. Chen, Y. Jiang, R. Huang, G. Gu, and H. Li, “Freetacman: Robot-free visuo-tactile data collection system for contactrich manipulation,” _arXiv preprint arXiv:2506.01941_ , 2025. 

- [30] E. Helmut, L. Dziarski, N. Funk, B. Belousov, and J. Peters, “Learning force distribution estimation for the gelsight mini optical tactile sensor based on finite element analysis,” _arXiv preprint arXiv:2411.03315_ , 2024. 

- [31] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, _et al._ , “Palm-e: an embodied multimodal language model,” in _Proceedings of International Conference on Machine Learning (ICML)_ , pp. 8469–8488, 2023. 

- [32] J. Gao, Z. Tao, N. Jaquier, and T. Asfour, “K-vil: Keypoints-based visual imitation learning,” _Transactions on Robotics (T-RO)_ , vol. 39, no. 5, pp. 3888–3908, 2023. 

- [33] J. Luo, C. Xu, X. Geng, G. Feng, K. Fang, L. Tan, S. Schaal, and S. Levine, “Multistage cable routing through hierarchical imitation learning,” _Transactions on Robotics (T-RO)_ , vol. 40, pp. 1476–1491, 2024. 

- [34] P. Lin, “Handdiffuse: Generative controllers for two-hand interactions via diffusion models,” _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 39, pp. 5280–5288, Apr. 2025. 

- [35] P. Li, Y. Wu, Z. Xi, W. Li, Y. Huang, Z. Zhang, Y. Chen, J. Wang, S.-C. Zhu, T. Liu, _et al._ , “Controlvla: Few-shot object-centric adaptation for pre-trained vision-language-action models,” _arXiv preprint arXiv:2506.16211_ , 2025. 

- [36] K. Kawaharazuka, J. Oh, J. Yamada, I. Posner, and Y. Zhu, “Visionlanguage-action models for robotics: A review towards real-world applications,” _IEEE Access_ , 2025. 

- [37] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of Conference on Robot Learning (CoRL)_ , pp. 2165–2183, PMLR, 2023. 

- [38] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, _et al._ , “Octo: An open-source generalist robot policy,” _arXiv preprint arXiv:2405.12213_ , 2024. 

- [39] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, _et al._ , “ _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [40] J. Gu, F. Xiang, X. Li, Z. Ling, X. Liu, T. Mu, Y. Tang, S. Tao, X. Wei, Y. Yao, X. Yuan, P. Xie, Z. Huang, R. Chen, and H. Su, “Maniskill2: A unified benchmark for generalizable manipulation skills,” in _Proceedings of International Conference on Learning Representations (ICLR)_ , 2023. 

- [41] S. Dasari, F. Ebert, S. Tian, S. Nair, B. Bucher, K. Schmeckpeper, S. Singh, S. Levine, and C. Finn, “Robonet: Large-scale multi-robot learning,” in _Proceedings of Conference on Robot Learning (CoRL)_ , pp. 885–897, PMLR, 2020. 

- [42] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. HansenEstruch, A. W. He, V. Myers, M. J. Kim, M. Du, _et al._ , “Bridgedata v2: A dataset for robot learning at scale,” in _Proceedings of Conference on Robot Learning (CoRL)_ , pp. 1723–1736, PMLR, 2023. 

- [43] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 36, pp. 44776–44791, 2023. 

- [44] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 30, 2017. 

- [45] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 33, pp. 6840–6851, 2020. 

- [46] C. Zhang, P. Hao, X. Cao, X. Hao, S. Cui, and S. Wang, “Vtla: Visiontactile-language-action model with preference learning for insertion manipulation,” _arXiv preprint arXiv:2505.09577_ , 2025. 

- [47] H. Yousef, M. Boukallel, and K. Althoefer, “Tactile sensing for dexterous in-hand manipulation in robotics—a review,” _Sensors and Actuators A: physical_ , vol. 167, no. 2, pp. 171–187, 2011. 

- [48] O. M. Andrychowicz, B. Baker, M. Chociej, R. Jozefowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert, G. Powell, A. Ray, _et al._ , “Learning dexterous in-hand manipulation,” _International Journal of Robotics Research (IJRR)_ , vol. 39, no. 1, pp. 3–20, 2020. 

- [49] Q. Liu, Y. Cui, Z. Sun, G. Li, J. Chen, and Q. Ye, “Vtdexmanip: A dataset and benchmark for visual-tactile pretraining and dexterous manipulation with reinforcement learning,” in _Proceedings of International Conference on Learning Representations (ICLR)_ , 2025. 

- [50] S. Li, Z. Huang, T. Chen, T. Du, H. Su, J. B. Tenenbaum, and C. Gan, “Dexdeform: Dexterous deformable object manipulation with human demonstrations and differentiable physics,” in _Proceedings of International Conference on Learning Representations (ICLR)_ , 2023. 

- [51] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903, IEEE, 2024. 

- [52] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, _et al._ , “Droid: A large-scale in-the-wild robot manipulation dataset,” _arXiv preprint arXiv:2403.12945_ , 2024. 

- [53] A.-H. Shahidzadeh, G. M. Caddeo, K. Alapati, L. Natale, C. Fermüler, and Y. Aloimonos, “Feelanyforce: Estimating contact force feedback from tactile sensation for vision-based tactile sensors,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , pp. 251– 257, IEEE, 2025. 

- [54] S. Dong, W. Yuan, and E. H. Adelson, “Improved gelsight tactile sensor for measuring geometry and slip,” in _Proceedings of International Conference on Intelligent Robots and Systems (IROS)_ , pp. 137–144, IEEE, 2017. 

- [55] M. A. Mirzaee and A. Sadighi, “Multiphysics simulation and design framework for developing a vision-based tactile sensor with force estimation and slip detection capabilities,” _Sensors and Actuators A: Physical_ , vol. 378, p. 115761, 2024. 

- [56] W. Li, A. Alomainy, I. Vitanov, Y. Noh, P. Qi, and K. Althoefer, “F-touch sensor: Concurrent geometry perception and multi-axis force measurement,” _IEEE Sensors Journal_ , vol. 21, no. 4, pp. 4300–4309, 2020. 

- [57] W. Li, M. Wang, J. Li, Y. Su, D. K. Jha, X. Qian, K. Althoefer, and H. Liu, “L3f-touch: A wireless gelsight with decoupled tactile and threeaxis force sensing,” _Robotics and Automation Letters (RA-L)_ , vol. 8, no. 8, pp. 5148–5155, 2023. 

- [58] C. Zhao, J. Ren, H. Yu, and D. Ma, “In-situ mechanical calibration for vision-based tactile sensors,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , pp. 10387–10393, IEEE, 2023. 

- [59] Z. Lu, Z. Liu, X. Zhang, Y. Liang, Y. Dong, and T. Yang, “3d force identification and prediction using deep learning based on a gelsight-structured sensor,” _Sensors and Actuators A: Physical_ , vol. 367, p. 115036, 2024. 

- [60] R. Chen, H. Qian, and J. Xu, “Generalizable force estimation based on graph networks for thin lensless vision-based tactile sensor,” in _Proceedings of International Conference on Robotics and Biomimetics (ROBIO)_ , pp. 1178–1183, IEEE, 2024. 

- [61] C. Lin, H. Zhang, J. Xu, L. Wu, and H. Xu, “9dtact: A compact vision-based tactile sensor for accurate 3d shape reconstruction and generalizable 6d force estimation,” _RA-L_ , vol. 9, no. 2, pp. 923–930, 2023. 

- [62] W. Mandil, K. Nazari, _et al._ , “Action conditioned tactile prediction: case study on slip prediction,” _arXiv preprint arXiv:2205.09430_ , 2022. 

- [63] B. Fang, J. Zhao, N. Liu, Y. Sun, S. Zhang, F. Sun, J. Shan, and Y. Yang, “Force measurement technology of vision-based tactile sensor,” _Advanced Intelligent Systems_ , vol. 7, no. 1, p. 2400290, 2025. 

- [64] S. Ge, S. Mishra, C.-L. Li, H. Wang, and D. Jacobs, “Robust contrastive learning using negative samples with diminished semantics,” _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 34, pp. 27356–27368, 2021. 

- [65] V. Dave, F. Lygerakis, and E. Rueckert, “Multimodal visual-tactile representation learning through self-supervised contrastive pre-training,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , pp. 8013–8020, IEEE, 2024. 

- [66] B. Dasgupta and T. Mruthyunjaya, “The stewart platform manipulator: a review,” _Mechanism and Machine Theory_ , vol. 35, no. 1, pp. 15–40, 2000. 

- [67] R. Feng, J. Hu, W. Xia, T. Gao, A. Shen, Y. Sun, B. Fang, and D. Hu, “Anytouch: Learning unified static-dynamic representation across multiple visuo-tactile sensors,” _arXiv preprint arXiv:2502.12191_ , 2025. 

- [68] A. Van Den Oord, O. Vinyals, _et al._ , “Neural discrete representation learning,” _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 30, 2017. 

17 

- [69] A. Van Den Oord, O. Vinyals, _et al._ , “Neural discrete representation learning,” _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 30, 2017. 

- [70] A. Baevski, S. Schneider, and M. Auli, “vq-wav2vec: Self-supervised learning of discrete speech representations,” in _Proceedings of International Conference on Learning Representations (ICLR)_ , 2020. 

- [71] D. Lee, S. Malacarne, and E. Aune, “Vector quantized time series generation with a bidirectional prior model,” in _Proceedings of the International Conference on Artificial Intelligence and Statistics (AISTATS)_ , pp. 7665–7693, PMLR, 2023. 

- [72] S. Sadok, S. Leglaive, and R. Séguier, “A vector quantized masked autoencoder for speech emotion recognition,” in _International Conference on Acoustics, Speech, and Signal Processing Workshops (ICASSPW)_ , pp. 1–5, IEEE, 2023. 

- [73] A. Razavi, A. Van den Oord, and O. Vinyals, “Generating diverse high-fidelity images with vq-vae-2,” _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 32, 2019. 

- [74] A. Dosovitskiy, “An image is worth 16x16 words: Transformers for image recognition at scale,” _arXiv preprint arXiv:2010.11929_ , 2020. 

- [75] A. v. d. Oord, Y. Li, and O. Vinyals, “Representation learning with contrastive predictive coding,” _arXiv preprint arXiv:1807.03748_ , 2018. 

- [76] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [77] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _International Journal of Robotics Research (IJRR)_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [78] Z. Chen, N. Ou, X. Zhang, and S. Luo, “Transforce: Transferable force prediction for vision-based tactile sensors with sequential image translation,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , pp. 237–243, IEEE, 2025. 

