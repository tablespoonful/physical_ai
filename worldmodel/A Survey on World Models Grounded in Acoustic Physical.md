---
title: "A Survey on World Models Grounded in Acoustic Physical Information"
date: "2025-06-16"
authors: "Xiaoliang Chen; Le Chang; Xin Yu; Yunhe Huang; Xianling Tu"
url: https://arxiv.org/abs/2506.13833
pdf: https://arxiv.org/pdf/2506.13833
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.13833)** / [論文ページ](https://arxiv.org/abs/2506.13833)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **A Survey on World Models Grounded in Acoustic Physical Information** 

Xiaoliang Chen<sup>∗1</sup> , Le Chang<sup>1</sup> , Xin Yu<sup>1</sup> , Yunhe Huang<sup>1</sup> , and Xianling Tu<sup>1</sup> 

> 1SoundAI Technology Co., Ltd. 

##### **Abstract** 

This survey provides a comprehensive overview of the emerging field of world models grounded in the foundation of acoustic physical information. It examines the theoretical underpinnings, essential methodological frameworks, and recent technological advancements in leveraging acoustic signals for high-fidelity environmental perception, causal physical reasoning, and predictive simulation of dynamic events. The survey explains how acoustic signals, as direct carriers of mechanical wave energy from physical events, encode rich, latent information about material properties, internal geometric structures, and complex interaction dynamics. Specifically, this survey establishes the theoretical foundation by explaining how fundamental physical laws govern the encoding of physical information within acoustic signals. It then reviews the core methodological pillars, including Physics-Informed Neural Networks (PINNs), generative models, and self-supervised multimodal learning frameworks. Furthermore, the survey details the significant applications of acoustic world models in robotics, autonomous driving, healthcare, and finance. Finally, it systematically outlines the important technical and ethical challenges while proposing a concrete roadmap for future research directions toward robust, causal, uncertaintyaware, and responsible acoustic intelligence. These elements collectively point to a research pathway towards embodied active acoustic intelligence, empowering AI systems to construct an internal "intuitive physics" engine through sound. 

**Keywords:** World Model, Acoustic Physical Information, Physics-Informed AI, Acoustic Perception, Multimodal Learning, Dynamic Prediction, Embodied Intelligence, Causal Inference 

## **1 Introduction** 

The long-standing quest for Artificial General Intelligence (AGI), which has seen tremendous progress with large-scale foundation models [1, 2], has increasingly converged on the need to construct intelligent agents capable of understanding, predicting, and meaningfully interacting with their physical environments. This paradigm marks a notable shift away from traditional approaches grounded solely in statistical pattern recognition and data-driven correlations—a powerfully articulated in the context of ungrounded language models [3]—towards more sophisticated models that embody causal inference and internalize the physical laws governing our surroundings. Central to this transformation is the concept of _world models_ , internalized representations that are both generative and learnable. Such models enable agents to simulate their environments efficiently within compressed latent spaces, reason retrospectively and prospectively about events, and accurately predict outcomes resulting from their actions or from external changes and interventions [4–7]. 

Traditionally, visual perception, driven by breakthroughs in deep learning [8, 9], has dominated the sensory modalities used to construct these internal models. However, despite its ubiquity and intuitive appeal, visual information alone imposes fundamental constraints. Visual sensing is inherently susceptible to practical limitations including poor illumination conditions, occlusions, atmospheric disturbances, and adverse weather scenarios, significantly hindering robustness in real-world applications [10]. More fundamentally, visual perception predominantly captures surface-level phenomena, frequently failing to convey 

> ∗Corresponding author: chenxiaoliang@soundai.com 

1 

intrinsic properties such as mass, internal composition, temperature gradients, structural integrity, and contact forces. These intrinsic characteristics are often ambiguous or entirely inaccessible through visual data alone, underscoring the need for complementary modalities capable of addressing these fundamental gaps. 

In contrast, acoustic information provides a highly promising yet often overlooked complementary modality that can significantly augment and enrich world models. Sound, fundamentally, is a direct physical manifestation of mechanical interactions and events, arising from vibrations propagating through media and carrying explicit signatures of the underlying physical processes. Each acoustic signal encodes specific properties and dynamics of its originating phenomena—be it the resonant frequencies emitted by a struck object indicative of its material properties such as elasticity and density, or the characteristic turbulence sounds generated by fluids described by complex fluid dynamics. These acoustic signals inherently embed important information about material composition, internal structures, geometrical configurations, and dynamical interactions, deeply rooted in principles of auditory scene analysis [11, 12]. Thus, by decoding acoustic signals through physical reasoning, intelligent systems can cultivate a nuanced "physical intuition," acquiring rich insights into the environment that are inherently complementary and orthogonal to visual perception. 

This survey aims to provide a comprehensive and structured review of the emerging research field focused on acoustic-based physical world models. By integrating insights from acoustics, machine learning, signal processing, robotics, and cognitive science, we aim to present a comprehensive narrative highlighting theoretical underpinnings, methodological advancements, diverse application domains, and persistent challenges. We contend that interpreting sound through explicit physical frameworks significantly deepens AI’s capacity for causal understanding, ultimately enhancing its perceptual precision, reasoning capabilities, and predictive accuracy. To achieve this, this survey first establishes the theoretical foundations of how acoustic physics encodes rich, causal, and interpretable information. Subsequently, it delves into the methodological pillars, emphasizing advanced techniques like Physics-Informed Neural Networks and generative modeling that bridge theoretical physics and data-driven AI. The survey then showcases the significant applications in key domains such as robotics and healthcare, demonstrating the practical impact of acoustically-grounded world models. Finally, it offers an important analysis of prevailing challenges and prospective research directions, examining technical and ethical issues while outlining a robust research pathway towards causal and adaptive acoustic intelligence. 

Through this comprehensive review of existing state-of-the-art techniques, theoretical advancements, practical implementations, and forward-looking perspectives, we intend to foster deeper scholarly engagement and innovation in the field of acoustic world models. Ultimately, the insights presented aim to propel the development of next-generation AI systems endowed with a deep understanding of physical principles, capable of sophisticated environmental interaction, nuanced prediction, and genuinely intelligent, contextually aware decision-making. 

## **2 Theoretical Foundations: Acoustic Representation of Physical Laws** 

Acoustic technology, characterized by its unique sensitivity to the physical environment, exceptional penetrability, and direct causal linkage to physical processes, constitutes an essential perceptual modality for a acoustic world model. Acoustic signals are not superficial background noise but are direct, wave-based encodings of physical events, material properties, and environmental structures. They are the radiated mechanical energy from dynamic phenomena, governed by the fundamental laws of mechanics and thermodynamics. The physical information they contain far surpasses what casual listening can perceive, providing AI with the deep physical insights necessary for "identifying objects by sound" and "understanding environments by sound," as envisioned by early pioneers in auditory scene analysis [11, 12]. This section establishes the physical principles that enables this acoustic cognition. 

### **2.1 Estimating Physical Properties from Structure Vibrations** 

The acoustic signature of a solid object is a direct manifestation of its vibrational behavior upon excitation. This behavior is governed by the laws of elastodynamics, and for a linear, isotropic, and homogeneous elastic solid in the absence of body forces, the displacement vector field **u** ( _x, t_ ) is described by the generalized linear 

2 

wave equation: 


where _ρ_ is the density, and _λ_ and _µ_ are the Lamé parameters, which are functions of the material’s Young’s modulus _E_ and Poisson’s ratio _ν_ . This equation supports two types of waves: longitudinal (pressure) waves and transverse (shear) waves, whose speeds are determined by these material properties. When an object is struck, it vibrates in a superposition of its natural modes or _eigenmodes_ . These are the special solutions to the wave equation subject to the object’s specific geometry and boundary conditions (e.g., fixed, free, or simply supported). Each eigenmode, _ϕn_ ( _x_ ), has a corresponding natural frequency, or _eigenvalue_ , _ωn_ . For example, the natural frequencies of a uniform beam undergoing transverse vibration are given by: 


where _L_ is the length, _A_ is the cross-sectional area, _I_ is the area moment of inertia (a geometric property), and _βn_ are constants determined by the boundary conditions. 

- Material and Modal Inversion: The sound radiated by a vibrating object is a summation of tones at these natural frequencies, _ωn_ . The relative amplitudes and decay rates of these tones create the object’s unique timbre. This provides a rich, high-dimensional acoustic fingerprint for inferring physical properties. 

   - Material Properties: As seen in the equations, the frequencies are directly tied to material parameters like _E_ and _ρ_ . Therefore, by analyzing the spectrum of an impact sound, a model can work backward to infer these intrinsic material properties. This is the basis for a large body of work on material identification from sound [13, 14]. 

   - Damping and Internal Friction: The rate at which each modal vibration decays is determined by the material’s internal friction and energy radiation into the surrounding medium. This decay rate is quantified by the Quality factor (Q-factor) for each mode. A high Q-factor (e.g., in metals) leads to sustained, high-frequency, harmonic ringing, while a low Q-factor (e.g., in wood or plastic) leads to a rapidly decaying, dull thud. This temporal decay information is as important as the spectral content for material classification. 

   - Geometric Properties: The geometry of the object, encapsulated in terms like _L_ , _A_ , and _I_ , along with its boundary conditions, dictates the specific set of eigenfrequencies. While inverting for the full 3D shape from a single sound is a highly ill-posed problem, machine learning models can learn to recognize the acoustic signatures of specific shapes or estimate key geometric parameters [15]. Recent works have demonstrated that deep learning models can leverage these rich acoustic signatures to classify object materials with high accuracy [16], estimate the viscosity of liquids (which affects the damping of a container’s vibrations) [17], or even infer the particle size of granular materials from the statistical properties of many small impacts during shaking [18]. 

- Internal Structure and Defect Detection: The penetrative power of sound waves makes them fundamental to Non-Destructive Testing (NDT) and Non-Destructive Evaluation (NDE) [19]. When propagating through an object, sound waves are reflected, refracted, and scattered at interfaces between different media, such as voids, cracks, or foreign inclusions. The acoustic impedance mismatch at these interfaces governs the reflection and transmission coefficients. 

   - Pulse-Echo and Time-of-Flight Analysis: In active sensing, an ultrasonic pulse is emitted, and the time-of-flight and amplitude of returning echoes are analyzed. This allows for the precise localization of internal boundaries and defects, forming the basis of ultrasonic imaging (known as B-scans). 

   - Acoustic Resonance Spectroscopy (ARS): This passive technique analyzes the complete resonant spectrum of an object under wide-frequency excitation. The presence of an internal flaw, even a microscopic one, alters the object’s effective stiffness and mass distribution, causing a predictable 

3 

shift in its resonant peaks. By comparing the measured spectrum to a reference spectrum of a "healthy" object, minute internal flaws can be detected [20]. The application of deep learning to automate the analysis of these complex spectral shifts has greatly enhanced the efficiency of NDT in industrial settings, such as for identifying welding defects or composite material delamination [21, 22]. This "acoustic X-ray" capability allows a world model to perceive the physical state of an object "beneath the surface," moving beyond mere appearance to internal integrity. 

### **2.2 Decoding Acoustic Events from Contact to Aeroacoustics** 

Nearly all physical interactions involve the transfer and conversion of energy, a portion of which is radiated away as sound waves. These sounds are a direct, time-resolved record of the interaction’s dynamics. 

- Contact and Collision Dynamics: The sounds produced by object collisions and friction are direct manifestations of contact mechanics. For brief impacts, Hertzian contact theory models the deformation and forces between two curved surfaces. The duration and peak force of the contact, which directly influence the radiated sound, are functions of the objects’ materials (Young’s modulus, Poisson’s ratio), geometries, and impact velocity. The sound is not only generated by the object’s subsequent vibration but also by the rapid acceleration of the air at the contact point. The resulting sound’s spectral energy distribution, peak amplitude, and duration are closely related to the mass, relative velocity, hardness, and coefficient of restitution of the colliding bodies [23]. If the impact energy exceeds the elastic limit, plastic deformation and fracture can occur, generating distinct high-frequency acoustic emissions. This allows models to not only classify the "falling" event but also regressively estimate the drop height, object mass, and even diagnose damage [24, 25]. In robotic manipulation, analyzing subtle contact sounds can reveal the stability of a grasp, detect incipient slip, and characterize surface texture, enabling more refined force control and dexterous manipulation [26, 27]. 

- Fluid and Gas Dynamics (Aeroacoustics): The sounds of liquid flow and aerodynamic noise contain rich information about fluid dynamics. The foundational theory is Lighthill’s acoustic analogy, which recasts the Navier-Stokes equations into an inhomogeneous wave equation [28]: 


where _ρ_<sup>_′_</sup> is the density fluctuation, _c_ 0 is the sound speed in the stationary fluid, and _Tij_ is the Lighthill stress tensor. This powerful equation shows that fluid flow can be modeled as a source of sound (quadrupole in nature) within a stationary acoustic medium. A key extension is the Ffowcs WilliamsHawkings (FW-H) equation, which explicitly includes terms for sound generated by moving surfaces (monopole and dipole sources), making it essential for modeling noise from rotating blades or vehicles. A world model can leverage these principles to monitor pipeline flow regimes [29], detect gas or water leaks from the high-frequency turbulence they generate [30], or estimate the fill level of a container by analyzing the changing resonant frequencies of the sloshing liquid [31]. For autonomous vehicles, the noise generated by tire-road interaction provides real-time information on road conditions (e.g., dry, wet, icy) [32, 33], offering key safety information that is often ambiguous for vision or LiDAR systems. 

- Cyclostationary Analysis for Machine Health: Rotating machinery produces sounds that are not strictly stationary but are cyclostationary—their statistical properties vary periodically with the machine’s cycle. When faults like bearing wear or gear tooth cracks develop, they introduce periodic impulsive components or amplitude/frequency modulations into the acoustic signal. Advanced signal processing techniques like spectral correlation and envelope analysis can reveal these hidden periodicities, which are often buried in noise. Deep learning models can then be trained on these processed representations to perform highly sensitive fault diagnosis and prognostics, effectively creating a detailed acoustic physical model of a machine’s health state [34–36]. 

### **2.3 Mapping Spatial Geometry by Acoustic Cues** 

The propagation, reflection, diffraction, and reverberation of sound waves within a space create a complex sound field that acts as a sonic fingerprint of the environment’s geometry. By analyzing this sound field, an 

4 

AI can construct a three-dimensional cognitive map of its surroundings. 

- Room Impulse Response (RIR) as a Geometric Descriptor: The acoustic properties of an enclosed space are comprehensively described by its **Room Impulse Response (RIR)** , _h_ ( _t_ ). The signal received at a microphone, _y_ ( _t_ ), is the convolution of the source signal _s_ ( _t_ ) with the RIR: 


The RIR’s structure contains rich geometric information. The early part consists of the direct path sound followed by a series of distinct specular reflections from nearby surfaces. The arrival times and amplitudes of these reflections encode the path lengths and reflective properties of the surfaces, effectively creating an "echogram" of the local geometry. The later part of the RIR, the late reverberation tail, is a diffuse field of countless overlapping echoes. Its decay rate, quantified by the **Reverberation Time (** _T_ 60 **)** , is related to the room’s volume _V_ and total surface absorption. 


Here _S_ =<sup>�</sup> _i_<sup>_Si_isthetotalsurfacearea,</sup><sup>_Si_and</sup><sup>_αi_aretheareaandabsorptioncoefficientofthe</sup><sup>_i_-th</sup> surface, respectively, and _α_ ¯ is the average absorption coefficient. Equation (5) (Sabine) is accurate for rooms with low average absorption (¯ _α_ ≲ 0 _._ 2), whereas Equation (6) (Eyring) remains reliable when absorption is moderate to high (¯ _α_ ≳ 0 _._ 2) [31]. 

By analyzing a received sound signal and performing blind deconvolution to estimate the RIR, a model can infer the room’s volume, approximate dimensions, and even the types of materials on its surfaces (e.g., reflective glass vs. absorptive carpet) [37, 38]. 

- Binaural Acoustics and Spatial Hearing: For an agent with two microphones (ears), the brain (or an AI) exploits binaural cues to localize sound sources with remarkable precision. The key cues are: 

   - **Interaural Time Difference (ITD):** The difference in arrival time of a sound wave at the two ears, which depends on the source’s azimuth. 

   - **Interaural Level Difference (ILD):** The difference in sound intensity, which is caused by the acoustic shadowing effect of the head and is most prominent at high frequencies. 

The complete set of these spatial cues is captured by the **Head-Related Transfer Function (HRTF)** , which is the RIR from a source to each of the two ears, a function whose processing is mirrored in the neural representation of three-dimensional acoustic space within the human temporal lobe [39]. By learning a model of its own HRTF, an agent can perform highly accurate 3D sound source localization. 

- Acoustic SLAM and Scene Reconstruction: By combining source localization with agent motion, it’s possible to perform Acoustic Simultaneous Localization and Mapping (Acoustic SLAM). By moving through an environment and continuously localizing static sound sources (or using known sound sources as beacons to localize itself), the agent can incrementally build a map of both the sound sources and the primary acoustic reflectors (walls, obstacles) [40, 41]. Unlike visual SLAM which relies on optical features, Acoustic SLAM builds a map of the environment’s geometric and material properties as they pertain to sound, enabling navigation in complete darkness or visually featureless environments where vision-based systems would catastrophically fail [42]. This forms a direct pathway from raw sound to a functional spatial model of the world. 

5 

### **2.4 Modeling Nonlinear Sound Wave Interactions** 

While powerful, the linear models discussed so far operate under the assumption of small acoustic perturbations. This assumption breaks down in many real-world scenarios involving high-amplitude sound, such as biomedical ultrasound or close-range robotic interaction. In these regimes, nonlinear effects like harmonic generation and waveform distortion become dominant, requiring more advanced physical models [43]. A complete physical foundation for acoustic world models must therefore also encompass the principles of nonlinear acoustics. 

Nonlinear acoustic models extend linear theory by incorporating amplitude-dependent effects for highintensity fields. When acoustic pressure is large, linear approximations fail to capture the underlying physics [43]. By performing a perturbation expansion on the compressible Navier-Stokes equations for an irrotational, lossless flow, we can derive the governing nonlinear wave equations. Let the total pressure be _p_ = _p_ 0 + _ϵp_ 1 + _ϵ_<sup>2</sup> _p_ 2 + _· · ·_ , where _p_ 0 is ambient pressure and _ϵ_ is a small perturbation parameter. Retaining terms up to second order, _O_ ( _ϵ_<sup>2</sup> ), leads to the Westervelt Equation. 

The second-order perturbation expansion of the governing equations yields an intermediate form: 


where _ρ_ 0 is the ambient density, _c_ is the linear sound speed, and _β_ = 1 + 2<sup>_<u>B</u>_</sup> _A_<sup>is the coefficient of nonlinearity.</sup> Normalizing this expression leads to the canonical Westervelt Equation: 


where _α ∝ ρ_ 0 _<u>β c</u>_<sup>2encapsulatesthemedium’snonlinearresponse.Thisequationmodelskeynonlinearphe-</sup> nomena such as second-harmonic generation and waveform steepening, which are in high-amplitude acoustic fields. 

For directional acoustic beams, the Khokhlov-Zabolotskaya-Kuznetsov (KZK) equation models the combined effects of nonlinearity, diffraction, and absorption. It is derived using a paraxial approximation and a retarded time frame _τ_ = _t − z/c_ . The general form is: 


where _∇_<sup>2</sup> _⊥_<sup>isthetransverseLaplacian,</sup><sup>_β_NListhenonlinearitycoefficient,and</sup><sup>_δ_modelsthermoviscous</sup> absorption. Neglecting absorption ( _δ_ = 0) simplifies the equation. For an axisymmetric beam in cylindrical coordinates, the lossless KZK equation becomes: 


The KZK equation is fundamental for modeling phenomena like focused acoustic holography and other far-field, high-intensity applications [44]. 

## **3 Methodological Frameworks: Acoustic World Models** 

The inclusion of these nonlinear models highlights a key challenge: as physical models grow in fidelity, their analytical or numerical solutions become intractable, especially for the inverse problems central to building world models. This complexity necessitates a new computational paradigm. 

This is precisely the gap that modern AI methods are poised to fill. The core task is to develop a framework that can learn, represent, and reason with these intricate laws of acoustic physics—a problem of system identification and forward simulation. This requires an integration of data-driven machine learning and principle-driven physical modeling. The following section surveys the three key methodological pillars that form this foundation: physics-informed neural networks, generative forward models, and self-supervised multimodal learning. 

6 

### **3.1 Physics-Informed Neural Networks for Acoustic Inverse Problems** 

Physics-Informed Neural Networks (PINNs) represent a fundamental shift in scientific machine learning, moving beyond purely data-driven "black-box" models to create "gray-box" models that are constrained by known physical laws [45, 46]. A PINN is a neural network that is trained to not only fit observed data but also to satisfy a governing Partial Differential Equation (PDE) over the entire spatiotemporal domain of interest. 

#### **3.1.1 The Core PINN Formulation for Acoustics** 

In the context of acoustics, a PINN is typically a Multi-Layer Perceptron (MLP), _p_ ˆ( _x, t_ ; _θ_ ), that takes spatial coordinates _x_ and time _t_ as input and outputs the predicted acoustic pressure _p_ ˆ. The network’s parameters _θ_ are optimized by minimizing a composite loss function: 


where the terms are: 

- (i) Data Fidelity Loss ( _L_ data): This is a standard supervised loss that anchors the solution to real-world measurements. Given a set of _Ndata_ sensor measurements at points ( _xi, ti_ ), it is typically the Mean Squared Error (MSE): _L_ data = _Ndata_ <u>1</u> � _Ni_ =1 _data |p_ ˆ( _xi, ti_ ; _θ_ ) _− p_ measured( _xi, ti_ ) _|_<sup>2</sup> . 

- (ii) Physics Residual Loss ( _L_ phys): This is the heart of the PINN. It enforces the governing PDE, such as the acoustic wave equation, which, for a homogeneous and lossless free sound field, is expressed as the residual function _f_ ( _p_ ) = _∇_<sup>2</sup> _p − c_<sup><u>12</u></sup> _∂∂t_<sup>22</sup> _<u>p</u>_<sup>=0.ThelossistheMSEofthisresidual,evaluatedata</sup> large number of _N_ phys collocation points randomly sampled throughout the domain interior: _L_ phys = _Nphys_ <u>1</u> � _Nj_ =1 _phys |f_ (ˆ _p_ ( _xj, tj_ ; _θ_ )) _|_<sup>2</sup> . The important enabling technology here is automatic differentiation, which allows for the exact computation of the partial derivatives (<sup>_∂_</sup> _∂t_<sup>2 ˆ2</sup><sup>_<u>p</u>_,etc.)</sup> with respect to the network’s inputs, directly within the deep learning framework. 

- (iii) Boundary and Initial Condition Losses ( _L_ bc _, L_ ic): These terms enforce the problem’s boundary conditions (e.g., acoustically rigid walls, pressure-release surfaces) and initial state (e.g., pressure and velocity at _t_ = 0). For example, a Neumann boundary condition _∇p_ ˆ _·_ **n** = 0 is enforced via an additional MSE term evaluated on the boundary. 

The weights _wdata, wphys, . . ._ are hyperparameters that balance the different loss components, and their tuning is a important and non-trivial aspect of training PINNs. 

#### **3.1.2 Advantages, Limitations, and Comparative Analysis** 

The PINN framework offers profound advantages for acoustic modeling, particularly in data efficiency and solving inverse problems. By embedding physical constraints, PINNs act as a powerful regularizer, transforming ill-posed inverse problems (e.g., source localization from sparse sensors or for volumetric field reconstruction [47–49]) into well-posed ones. The physics loss provides "free" supervision, reducing the need for extensive labeled data and enabling mesh-free learning. 

However, PINNs are not without limitations. Their performance hinges on the availability of an accurate, analytically expressible PDE, which may not exist for highly complex, non-linear, or multi-physics phenomena. They can also struggle with sharp gradients or discontinuities in the solution. Compared to generative models, PINNs excel at inverse problems with sparse data but are less suited for open-ended synthesis of novel sounds. In contrast to self-supervised methods, which learn implicit physical rules from data correspondence, PINNs enforce explicit, pre-defined physical laws, offering stronger guarantees at the cost of flexibility. 

### **3.2 Generative Models for Acoustics Simulation and Synthesis** 

A core function of a world model is to act as a simulator, capable of "imagining" or predicting future sensory inputs. This forward prediction is the basis for planning and reasoning. In the acoustic domain, this translates to building models that can generate realistic audio corresponding to physical events. 

7 

#### **3.2.1 Differentiable Physics Simulation with Gradient Descent** 

**Differentiable simulation** is a powerful approach where the entire simulation pipeline is constructed from differentiable operations [50]. By re-implementing simulation algorithms (e.g., modal synthesis, FiniteDifference Time-Domain (FDTD) methods) in frameworks like PyTorch, gradients can be backpropagated from a loss function (e.g., the difference between simulated and real audio) all the way back to the initial physical parameters. This enables highly efficient, gradient-based optimization for system identification tasks (e.g., inferring a drum’s tension from its sound) and creates powerful data factories for training other models. 

#### **3.2.2 Implicit Neural Models for Acoustic Fields** 

Inspired by Neural Radiance Fields (NeRFs) [51], Neural Acoustic Fields (NAFs) learn a continuous, implicit representation of a scene’s acoustic response, typically by mapping a 3D coordinate to a Room Impulse Response (RIR) [52]. Once trained on sparse RIR measurements, a NAF can render a physically plausible RIR for any arbitrary point in the scene, providing a fully differentiable, compressed representation of the acoustic environment for applications in Virtual Reality (VR)/Augmented Reality (AR) and robotic path planning. The challenge of maintaining physical consistency under transformations is also addressed by related methods in equivariant neural rendering [53]. 

#### **3.2.3 Controllable Procedural Sound Synthesis** 

This approach uses deep generative models to directly synthesize raw audio waveforms conditioned on highlevel physical parameters. Architectures like Denoising Diffusion Probabilistic Models (DDPMs) [54] are particularly effective. By conditioning the generation process on a vector of physical parameters (e.g., [mass, material, velocity]), these models learn a direct, controllable mapping from a physical latent space to the audio domain, forming the predictive core of an acoustic world model [55, 56]. 

#### **3.2.4 Comparative Analysis of Generative Approaches** 

These generative models offer a powerful alternative to PINNs, particularly for forward prediction and synthesis. Unlike PINNs, which are constrained by a known PDE, generative models can learn to simulate complex phenomena directly from data, even when the underlying physics is poorly understood. However, this flexibility comes at a cost: they typically require significantly more data than PINNs and may generate physically implausible results if not properly regularized. Compared to self-supervised methods, which learn representations for discrimination, generative models learn the full data distribution, making them computationally more intensive but capable of synthesis and prediction. 

### **3.3 Self-Supervised Multimodal Learning from Unlabeled Data** 

To scale learning, an AI must learn from raw, unlabeled sensory data. Self-supervised and multimodal learning paradigms provide a powerful framework for this by leveraging the natural co-occurrence of sensory streams as a supervisory signal. 

#### **3.3.1 Audio-Visual Contrastive Learning** 

This paradigm, pioneered by seminal works like [57, 58], leverages the natural co-occurrence of audio and video. By training a model on a contrastive task—pulling representations of corresponding audio-visual pairs together in an embedding space while pushing non-corresponding pairs apart (e.g., in large-scale multimodal models like Contrastive Language-Image Pre-training (CLIP) [59] and Flamingo [60])—the model learns powerful, high-level semantic features. These pre-trained encoders can be fine-tuned for diverse downstream tasks like sound source localization [61] and audio-visual source separation [62]. 

#### **3.3.2 Action-Conditioned Predictive Learning in Latent Space** 

Inspired by frameworks like Dreamer [5], this approach trains an embodied agent in a closed perceptionaction loop. The agent learns an encoder to compress sensory input into a latent state, a transition model to 

8 

predict the next latent state based on an action, and a decoder to reconstruct the predicted sensory input. This process forces the agent to build a compact, internal model of the environment’s dynamics directly from interaction, enabling sample-efficient planning in latent space. 

#### **3.3.3 Comparative Analysis of Self-Supervised Learning** 

Self-supervised learning offers a powerful way to learn from vast amounts of unlabeled data, a key advantage over supervised methods and even some PINN formulations. Unlike PINNs, which require explicit physical equations, these methods learn implicit physical rules through data association. In contrast to generative models that learn the full data distribution for synthesis, self-supervised methods typically learn discriminative representations optimized for downstream tasks. This often makes them more computationally efficient to train and more effective for tasks like classification or retrieval, but they cannot inherently generate new sensory data. 

### **3.4 Comparative Analysis and Hybrid Approaches** 

The three methodological pillars—PINNs, generative models, and self-supervised learning—offer distinct trade-offs, summarized in Table 1. No single approach is universally superior; the optimal choice depends on the specific problem, data availability, and computational constraints. 

The future of acoustic world models likely lies in **hybrid approaches** that combine the strengths of these pillars. For instance, a self-supervised model could be used to pre-train a powerful feature extractor on vast unlabeled video data. A generative model could then be conditioned on these features to synthesize physically plausible sounds. Finally, a PINN-based loss term could be used during the generative model’s training to act as a physical regularizer, ensuring the synthesized audio does not violate known acoustic principles. Such a hybrid system would leverage the data-efficiency of PINNs, the expressive power of generative models, and the scalability of self-supervised learning. 

Table 1: Comparative analysis of core methodologies for acoustic world models 

|**Methodology**|**Data requirement**|**Computational cost**|**Physical fidelity**|**Primary use case**|
|---|---|---|---|---|
|**Physics-**<br>**informed**<br>**neural**<br>**networks**|Low (sparse labeled<br>data + collocation<br>points).|Moderate to high<br>(training involves PDE<br>evaluation).|High (explicitly<br>constrained by<br>physical laws).|Solving inverse problems<br>(e.g., source localization,<br>material identification).|
|**Generative**<br>**forward**<br>**models**|High (requires large<br>datasets, often<br>paired with physical<br>parameters).|High (especially for<br>training diffusion<br>models or complex<br>simulators).|Variable (can be high<br>with good data, but<br>may generate<br>implausible results).|Forward simulation,<br>controllable sound<br>synthesis, data<br>augmentation, virtual<br>environments.|
|**Self-**<br>**supervised**<br>**multimodal**<br>**learning**|Very high (unlabeled<br>multimodal data,<br>e.g., video).|High (training large<br>encoders like<br>transformers).|Implicit (learns<br>correlations, not<br>explicit laws).|Learning robust<br>representations for<br>downstream tasks<br>(classification, retrieval,<br>source separation).|


9 


Figure 1: A conceptual diagram illustrating the methodological framework for acoustic world models. 

_It showcases the interplay between three pillars: (1) Physics-Informed Learning (e.g., PINNs), which embeds physical laws as constraints; (2) Generative Forward Models (e.g., Differentiable Simulators, NAFs), which enable prediction and data synthesis; and (3) Self-Supervised Multimodal Learning, which learns rich representations from unlabeled data. The arrows indicate the flow of information, constraints, and learned representations, forming a cohesive system. With a solid understanding of the theoretical underpinnings and the core computational methodologies, we can now turn our attention to the tangible impact of these models. The next section will demonstrate how acoustic world models are being deployed in real-world systems, highlighting their transformative applications across robotics, autonomous driving, healthcare, and beyond._ 

## **4 Embodied Applications: Deploying Acoustic World Modes in Real World** 

Acoustic world models have the potential to drive significant advancements in various domains of embodied intelligence, where agents must perceive, reason, and act within the complex, dynamic, and often uncertain physical world. 

### **4.1 Robotics** 

In robotics, acoustic perception is not a luxury but a necessity for overcoming the limitations of vision and proprioception, enabling safer, more precise, and more intuitive interaction with the world. 

- **Robust Navigation and Mapping in Extreme Environments:** In visually degraded environments (e.g., smoke-filled rooms, complete darkness, dust clouds from drilling), robots can employ Acoustic SLAM for localization and mapping. By emitting active sonar pings or passively listening to environmental sounds, the robot can construct a geometric map of its surroundings where vision-based systems would completely fail, ensuring operational continuity in important scenarios like search-andrescue or mining [40, 42]. 

10 

- **Dexterous Manipulation through Acoustic Haptics:** By learning to "listen" to contact sounds, a robot can gain a rich, haptic-like understanding of its physical interactions. It can detect the precise moment of contact, estimate contact force from impact sound intensity, perceive surface textures from frictional sounds, and detect high-frequency transients that signal incipient slip during grasping, allowing for real-time grip adjustment [26, 27]. This acoustic feedback loop enables far more stable and delicate manipulation than is possible with low-frequency force sensors alone. Furthermore, robots can infer latent object properties, such as whether a container is full, empty, or contains a liquid, by shaking it and analyzing the resulting sloshing or rattling sounds, a task impossible for vision, building on a long history of behavior-grounded robotics where agents learn object properties through multimodal interaction [23, 63, 64]. 

- **Intuitive Human-Robot Collaboration:** In collaborative settings, acoustic cues are vital for fluid and safe interaction. A robot can understand a human’s activity and intent by listening to tool sounds (e.g., distinguishing drilling from sawing to anticipate the next step in an assembly task, a capability that relies on robust polyphonic sound event detection systems [65]). More subtly, it can interpret the paralinguistic and prosodic features of human speech (pitch, tone, speaking rate) to infer their cognitive load, confidence, or emotional state, leading to safer, more adaptive, and more socially aware Human-Robot Collaboration (HRC)[44, 66]. 

### **4.2 Autonomous Driving** 

While vision, LiDAR, and radar are the primary sensors for autonomous vehicles, acoustics provides a important, omnidirectional, and computationally inexpensive complementary channel for enhanced situational awareness and safety. 

- **360-Degree Hazard Perception and Safety Enhancement:** Microphone arrays can reliably detect and localize the sirens of emergency vehicles long before they are visible or detectable by directional sensors, allowing the vehicle to yield preemptively [67]. They can also identify potential threats in the vehicle’s blind spots, such as a nearby motorcycle engine, a bicycle’s bell, or a child’s shout, providing an essential layer of safety. Critically, by analyzing tire-road noise, an acoustic world model can classify road surface conditions (dry, wet, icy, gravel) in real-time by recognizing their distinct spectral signatures. This provides vital input for adaptive traction control and braking systems, a task where vision can be ambiguous [26, 32, 33]. 

- **Vehicle Prognostics and Health Monitoring (VPHM):** An onboard acoustic world model can continuously "listen" to the vehicle’s own sounds, monitoring the engine, brakes, suspension, and other electromechanical components. By building a model of the vehicle’s normal acoustic signature, it can detect subtle deviations—anomalous squeals, rattles, or hums—that are early indicators of mechanical failure, such as bearing wear or exhaust leaks. This enables predictive maintenance, improving overall vehicle safety and reliability [34, 35]. 

### **4.3 Healthcare and Personalized Care** 

Acoustic world models have the potential to transform ubiquitous devices like smartphones and smart speakers into powerful, non-invasive tools for continuous health monitoring and early disease diagnosis. 

- **Remote Digital Biomarkers for Disease Screening:** As previously mentioned, by modeling the acoustic physics of the respiratory system, AI models can analyze the spectral and temporal properties of coughs, breathing, and snoring sounds to screen for a wide range of conditions like COVID-19, asthma, pneumonia, and obstructive sleep apnea, enabling large-scale, low-cost public health initiatives [56, 68, 69]. The field is expanding to include gastrointestinal acoustics for digestive health and joint acoustics for osteoarthritis monitoring. 

- **Neurological and Mental Health Assessment:** The human voice is a rich source of physiological and neurological biomarkers. An acoustic model can quantify subtle changes in vocal features—such as pitch variability (jitter), amplitude variability (shimmer), speech rate, and harmonic-to-noise ratio—to 

11 

non-invasively monitor the progression of neurological conditions like Parkinson’s disease, enabling monitoring that can inform adaptive therapies [70], and detect mental health states such as depression, anxiety, and PTSD [71, 72]. 

- **Empathetic AI and Socially Assistive Agents:** For AI companions and virtual assistants, understanding the user’s emotional state is paramount for effective interaction. By analyzing the emotional prosody of speech—the "music" behind the words—an AI can infer joy, sadness, anger, or stress from pitch contours, intensity, and rhythm. This allows the AI to provide more empathetic, appropriate, and natural responses, fostering deeper human-machine trust and rapport in applications like elderly care and mental health support [73]. 

### **4.4 Financial Services** 

Acoustic data in the financial sector, particularly from earnings calls, client interactions, and trading floors, is rich in emotional, cognitive, and paralinguistic features. The acoustic world models offer a shift from passively "hearing" to actively "understanding" contextual and causal cues. 

- **Quantitative Investment and Alpha Generation:** Acoustic world models can extract nonconsensus alpha signals from public acoustic sources like quarterly corporate earnings calls. By analyzing subtle paralinguistic cues in executives’ voices—such as vocal stress (measured by jitter and shimmer), pitch modulation, hesitation rates, and response latencies—these models can generate quantitative metrics of managerial confidence, deception, or uncertainty. These acoustic biomarkers have been shown to be orthogonal to text-based sentiment analysis and predictive of future firm performance and stock returns [74]. 

- **Advanced Risk Management and Compliance:** In compliance and risk management, acoustic world models can enhance fraud detection by quantifying acoustic markers of deceptive or high-stress speech patterns in trader communications or client calls. This allows for proactive risk alerts that go beyond simple keyword spotting, providing a deeper layer of security and monitoring for detecting financial misreporting or market manipulation activities [75]. 

- **Customer Interaction and Knowledge Engineering:** In client-facing roles, acoustic world models can analyze conversational dynamics to optimize service quality. By understanding nuances in tone, turn-taking dynamics, and engagement levels from call center audio, financial institutions can automatically predict customer satisfaction, identify at-risk clients, and provide real-time feedback to agents, thereby improving operational efficiency and client retention [76]. 

Table 2: Summary of applications for acoustic world models 

|**Application**<br>**domain**|**Specific task**|**Key acoustic**<br>**information**|**Enabling**<br>**technology**|**Primary impact**<br>**/ advantage**|
|---|---|---|---|---|
|**Robotics**|Dexterous<br>manipulation|High-frequency<br>transients from<br>contact friction|Self-supervised;<br>anomaly detection|Enhanced<br>dexterity and<br>grasp stability;<br>prevention of<br>object damage.|
||Object property<br>inference|Sloshing/rattling<br>sounds from<br>shaking actions|Action-conditioned<br>predictive models|Perception of<br>latent properties<br>invisible to vision;<br>richer interaction.|


12 

**Table 2 – continued from** **<u>previous page</u>** 

|**Application**<br>**domain**|**Specific task**|**Key acoustic**<br>**information**|**Enabling**<br>**technology**|**Primary impact**<br>**/ advantage**|
|---|---|---|---|---|
||Navigation in<br>degraded<br>environments|Echoes from active<br>sonar or passive<br>environmental<br>sounds|Acoustic SLAM,<br>Differentiable<br>Simulation|Robust localization<br>and mapping in<br>darkness, smoke,<br>or dust where<br>vision fails.|
|**Autonomous**|Emergency vehicle<br>detection|Siren harmonics<br>and Doppler shift|Microphone array<br>processing,<br>beamforming|Enhanced safety<br>through early,<br>360-degree hazard<br>awareness.|
||Road surface<br>classification|Spectral signatures<br>of tire-road noise|Supervised<br>learning|Improved safety<br>via adaptive<br>traction control<br>and braking<br>systems.|
||Vehicle health<br>monitoring|Anomalous<br>squeals, rattles, or<br>hums from<br>components|Anomaly<br>detection,<br>cyclostationary<br>analysis|Predictive<br>maintenance,<br>increased vehicle<br>reliability and<br>safety.|
|**Healthcare**|Respiratory disease<br>screening|Spectral and<br>temporal features<br>of<br>coughs/breathing|Deep learning<br>classifiers,<br>generative models|Low-cost,<br>non-invasive, and<br>scalable public<br>health screening.|
||Neurological<br>health assessment|Vocal biomarkers<br>(jitter, shimmer,<br>prosody)|Regression and<br>classification<br>models on speech<br>features|Non-invasive<br>tracking of disease<br>progression and<br>mental state.|
||Empathetic AI<br>companions|Emotional prosody<br>in speech (pitch,<br>tone, rhythm)|Multimodal<br>emotion<br>recognition|More natural,<br>effective, and<br>supportive<br>human-machine<br>interaction.|
|**Financial**|Alpha generation<br>from earnings calls|Paralinguistic cues<br>of<br>stress/confidence<br>in executive voices|Regression models<br>on vocal features|Orthogonal<br>investment signals<br>not found in text;<br>enhanced<br>prediction.|
||Fraud detection<br>and compliance|Acoustic markers<br>of deceptive or<br>high-stress speech|Anomaly<br>detection,<br>behavioral<br>modeling|Proactive risk<br>management and<br>enhanced security<br>beyond keyword<br>spotting.|


13 

**Table 2 – continued from** **<u>previous page</u>** 

|**Application**<br>**domain**|**Specific task**|**Key acoustic**<br>**information**|**Enabling**<br>**technology**|**Primary impact**<br>**/ advantage**|
|---|---|---|---|---|
||Customer service<br>optimization|Conversational<br>dynamics,<br>turn-taking, vocal<br>engagement|Emotion<br>recognition,<br>conversational AI|Improved client<br>satisfaction,<br>retention, and<br>operational<br>efficiency.|


_The diverse applications showcased in this section underscore the immense practical value of acoustic intelligence. However, the path to widespread, robust, and ethical deployment is not without significant hurdles. Therefore, the final section of this survey provides a important examination of these challenges and outlines a forward-looking research agenda to guide the field’s future development._ 

## **5 Challenges, Ethics, and Future Outlook** 

Despite the immense potential of acoustic world models, their transition from laboratory concepts to robust, real-world deployments faces significant scientific challenges and serious ethical considerations. A clear-eyed assessment of these hurdles is essential for guiding future research and ensuring responsible innovation. This section first details the pressing technical and societal challenges, then synthesizes the state of the art to propose a detailed, multi-faceted research agenda for the next generation of acoustic intelligence. 

### **5.1 Broad Scientific and Technical Challenges** 

The core scientific challenges lie at the intersection of high-dimensional data processing, physical modeling, and resource-constrained computation. 

- **High-Dimensional and Asynchronous Multimodal Fusion:** The physical world provides a symphony of sensory data. Effectively fusing heterogeneous, asynchronous, and often noisy data streams from acoustics, vision, haptics, and other sensors into a cohesive representation remains a fundamental research problem [73]. The challenge is not merely concatenation. It involves learning the complex, non-linear correlations and causal dependencies between modalities. For example, the high-frequency transient of an impact sound occurs before the object’s visual motion ceases. Architectures must move beyond simple early, late, or hybrid fusion schemes towards models that can explicitly handle temporal asynchrony and learn a shared latent space where one modality can inform or correct another. Techniques like multimodal transformers with cross-attention mechanisms are promising, but efficiently scaling them and learning their alignment without massive supervision is an open question. 

- **Computational Complexity and Real-Time Edge Deployment:** A stark trade-off exists between physical fidelity and computational feasibility. High-fidelity acoustic simulations based on wave-based methods (e.g., FDTD, Boundary Element Method (BEM)) are computationally prohibitive for realtime applications, often requiring hours of computation on high-performance clusters for a few seconds of audio. Conversely, large deep learning models like diffusion models or large transformers, while powerful, are difficult to deploy on resource-constrained edge devices such as robots, wearables, or vehicles. This necessitates a multi-pronged research effort into: (a) **Model Compression** , including techniques like network pruning, structured weight matrices, trained quantization, and Huffman coding [77]; (b) **Knowledge Distillation** , where a large, complex "teacher" model (e.g., a full physics simulator) is used to train a smaller, faster "student" model (a neural network); and (c) **Efficient Architectures** , exploring alternatives like Spiking Neural Networks (SNNs) or state-space models that are inherently more computationally and power-efficient; and (d) **Hardware-Software Co-Design** , recognizing that model-centric optimizations are only one side of the equation. The co-design of learning algorithms with specialized, power-efficient silicon—such as Neural Processing Units (NPUs), Tensor Processing Units (TPUs), or custom ASICs—is paramount for achieving real-time inference on the edge. This 

14 

synergy is particularly important when leveraging advanced sensors like high-density MEMS (MicroElectro-Mechanical Systems) microphone arrays or highly sensitive fiber-optic acoustic sensors. While these sensors provide richer, higher-fidelity input data that enhances perceptual capabilities, they also intensify the data throughput and computational demand, demanding a holistic, system-level approach that tightly integrates sensor technology, hardware acceleration, and algorithmic efficiency. 

- **The Acoustic Sim-to-Real-to-Sim Gap:** A major hurdle in applying models trained on synthetic data is the discrepancy between clean, idealized simulated acoustics and noisy, complex, real-world recordings. The "sim-to-real" gap arises from unmodeled phenomena: ambient noise, non-linear material properties, complex reverberation patterns, and the specific frequency response of the microphone and data acquisition hardware. Bridging this gap requires advanced techniques like: (a) **Domain Randomization** , where simulation parameters (noise levels, reverberation times, material properties) are heavily randomized during training to force the model to learn robust, invariant features; (b) **System Identification** , where a short calibration phase is used to learn a model of the specific sensor’s transfer function, which can then be applied to the simulator’s output; and (c) **Unsupervised Domain Adaptation** , which attempts to align the feature distributions of the simulated and real domains without requiring paired data [78]. A further challenge is the "real-to-sim" problem: accurately capturing a real-world scene’s geometry and material properties to create a high-fidelity digital twin for simulation in the first place. 

### **5.2 Ethics and Regulation of Acoustic World Models** 

The power of acoustic sensing brings with it a corresponding responsibility. Failure to proactively address the ethical dimensions of this technology could lead to significant societal harm. In what follows, we examine four principal ethical pressure-points and articulate concrete governance mechanisms. For clarity and academic rigor, each item is structured into three cohesive components: (i) a concise thematic statement, (ii) an illustrative _Case Study_ , and (iii) a detailed discussion of _Response Strategies_ . This tripartite format not only sharpens the analytical lens but also furnishes practitioners with actionable guidance. 

- **Privacy, Monitoring, and Safety in Sound Space:** The “always-on” nature of pervasive microphones transforms every domestic or public venue into a potential data-collection node. Without guardrails, such ubiquity risks normalizing involuntary surveillance and eroding long-standing social expectations regarding private speech. 

_Case Study._ A smart-home device designed to detect a “glass-break” sound for security must inevitably process all ambient sounds. This includes the inadvertent capture of sensitive family conversations, private health discussions, or interpersonal disputes. If such raw data are stored or transmitted, they could be repurposed by third parties—for instance, to infer purchasing preferences, target advertising, or even facilitate state-level surveillance—well beyond the scope originally consented to. 

_Response Strategies._ A multi-layered, _privacy-by-design_ architecture is essential. (a) **Mandatory OnDevice Processing** : deploy specialized low-power hardware—e.g., Neural Processing Units (NPUs) or Tensor Processing Units (TPUs)—so that raw audio never exits the device. (b) **Event-Triggered Data Handling** : maintain a low-power, non-recording state until a local acoustic signature (“wake word” or event) is detected. (c) **Federated Learning** : improve models on-device, uploading only anonymized, aggregated parameter updates to a central server [79]. (d) **Differential Privacy** : employ formal guarantees ensuring that analysis outputs remain stable even if any single individual’s data are removed, thus preventing re-identification [80]. 

- **Algorithmic Bias, Fairness, and Acoustic Equity:** An AI model naturally mirrors the statistical distribution of its training data; when that data are unbalanced, inequitable outcomes can ensue. In health care, such biases can directly translate into life-altering disparities. 

   - _Case Study._ Consider an AI diagnostic tool trained to detect early signs of Parkinson’s disease from vocal tremors. If the training corpus consists predominantly of male speakers of North-American English, performance may degrade for female speakers, individuals with strong regional accents, or non-native speakers. The resultant misdiagnoses delay treatment for under-represented groups and exacerbate existing health inequities. 

15 

_Response Strategies._ A proactive, end-to-end strategy is required: (a) **Diverse and Representative Data Curation** that explicitly targets demographic balance (age, gender, ethnicity, accent). (b) **Bias Auditing** prior to deployment, employing fairness metrics such as equalized odds or demographic parity to assess subgroup performance. (c) **Fairness-Aware Algorithms** , e.g., adversarial debiasing or re-weighting loss functions to penalize performance disparities [81]. 

- **Accountability, Transparency, and Explainable AI:** In safety-critical domains, opaque “blackbox” outputs are ethically indefensible. Stakeholders—from system engineers to end-users—require intelligible justifications for model behavior in both nominal and failure modes. 

_Case Study._ An autonomous vehicle’s acoustic subsystem misclassifies an icy road patch as merely wet, failing to engage traction-control protocols and leading to an accident. Post-incident analysis hinges on understanding _why_ the model erred: was a salient frequency component misinterpreted, or did domain shift cause over-confidence? 

_Response Strategies._ Explainable AI tools for acoustic signals are indispensable: (a) **Saliency Maps and Feature Attribution** —e.g., Gradient-weighted Class Activation Mapping (Grad-CAM) on spectrogram inputs—to highlight influential time-frequency bins. (b) **Counterfactual Explanations** that articulate, in human-centric terms, how slight spectral perturbations would have altered the outcome (“Had the 2 kHz peak been 5 dB lower, the surface would have been labeled ‘icy.”’). (c) **Model-Level Explanations** offering global rule abstractions to expose systematic flaws rather than isolated misfires [82]. 

- **Risk of Exploitation and Harmful Use:** Technologies that sense affective vocal markers confer both empathetic benefits and coercive power. Unchecked, they may be weaponized in disinformation, exploitative marketing, or asymmetric warfare. 

   - _Case Study._ Vocal stress-detection algorithms—originally intended for fraud prevention in finance [74, 75]—could be re-deployed in coercive interrogations or micro-targeted political messaging, nudging individuals at their most vulnerable moments. 

_Response Strategies._ To neutralize dual-use threats, we advocate a trident approach: (a) **Robust Ethical Frameworks** codified in international standards; (b) **Regulatory Oversight** with mandatory auditing of high-risk applications; and (c) **Deliberative Public Discourse** that surfaces societal values and informs policy. 

### **5.3 Future Research Agenda for the Next Decade** 

Looking ahead, the field must move beyond descriptive pattern recognition towards a generative and causal understanding of the physical world through sound. We outline five interconnected, high-impact research pathways that will define the next generation of acoustic world models. 

#### **5.3.1 Pathway I: From Correlation to Causality — Building Causal Acoustic World Models** 

Current models excel at learning correlations. The next frontier is learning the underlying causal relationships to answer counterfactual and interventional questions. 

- **Integration with Structural Causal Models (SCMs):** The goal is to represent the world as a causal graph, thereby empowering acoustic systems to reason about _why_ events occur and to predict the outcome of hypothetical interventions. Such capability marks a decisive shift from passive observation to active, question-driven inference. 

_Technical Difficulty:_ The search space for causal graph structures is combinatorially explosive, and structures are often non-identifiable from purely observational data. Confronting these obstacles demands an innovation that collapses experimental effort while simultaneously expanding causal identifiability. 

_Breakthrough Point:_ Developing algorithms that can leverage minimal, targeted interventions (e.g., a robot actively tapping an object) to drastically prune the space of possible causal graphs. 

16 

- **Counterfactual Sound Synthesis:** Building generative models that can simulate interventions via the “do-operator” would allow researchers to ask, and answer, what-if questions about acoustic phenomena. Such models would form the basis of virtual laboratories for sound. To reach that goal, the field must overcome a set of fundamental representation-learning bottlenecks. 

_Technical Difficulty:_ This requires perfect disentanglement of the causal factors of sound generation (e.g., shape, material, action), which current generative models struggle with. Addressing this challenge will hinge on unifying disentangled latent learning with physically grounded generation. 

_Breakthrough Point:_ Combining Variational Autoencoders (VAEs) for disentanglement with physicsconstrained generative models (e.g., PINN-regularized Generative Adversarial Networks (GANs)) that enforce the plausibility of counterfactual outcomes. 

#### **5.3.2 Pathway II: From Determinism to Distributions — Probabilistic and Uncertainty-Aware Models** 

The next generation of world models must be probabilistic, predicting a full distribution over possible future sounds and quantifying their own uncertainty. 

- **Distinguishing Uncertainty Types:** Future acoustic agents must clearly differentiate between randomness in the world and ignorance in the model. Such nuance is important for risk-aware decisionmaking and for allocating computational resources to learning where it matters most. A principled decomposition, however, introduces non-trivial architecture and training-time complications. 

_Technical Difficulty:_ Decomposing these two sources of uncertainty within a single, efficient deep learning model is a standing challenge. Any viable solution must not only separate these uncertainties but also exploit them to drive safer interaction policies. 

_Breakthrough Point:_ Creating hybrid architectures, for instance, using Deep Ensembles to capture uncertainty while having each ensemble member output a full probabilistic distribution (e.g., via a mixture density network) to capture aleatoric uncertainty. 

- **Uncertainty-Informed Decision Making:** An intelligent agent should convert calibrated uncertainty into concrete behavioral choices—slowing down, gathering more data, or selecting conservative actions—thereby achieving a measurable reduction in risk. Translating scalar uncertainty into highdimensional control signals, however, is far from straightforward. 

_Technical Difficulty:_ Translating a raw uncertainty value into a concrete policy change (e.g., how much to slow down a robot arm) is non-trivial. Overcoming this barrier will require algorithms that couple prediction fidelity with action optimization in a single computational loop. 

_Breakthrough Point:_ Tightly integrating uncertainty quantification with model-based Reinforcement Learning (RL), where the planning algorithm explicitly seeks to minimize worst-case outcomes over the predicted distribution or chooses actions that reduce epistemic uncertainty. 

#### **5.3.3 Pathway III: From Single Modes to Unified Perception — Physics-Based Cross-Modal Generation** 

The ultimate goal is a model that can “imagine” across modalities in a physically consistent way (e.g., generate sound from a silent video and vice versa). 

- **A “Multimodal Turing Test” for Physics:** A rigorous benchmark should require fine-grained, physically plausible cross-modal generation—capturing not only appearance and timing but also material properties and energy dissipation. Delivering on this benchmark will necessitate an unprecedented synergy of generative learning and explicit physics priors. 

   - _Technical Difficulty:_ Ensuring precise temporal synchronization (e.g., sound of footstep at the exact frame of impact) and physical consistency (e.g., sound decay matches visual material properties) is extremely difficult. The key lies in embedding differentiable physics directly into the adversarial training loop, thus allowing the discriminator to penalize implausible patterns at train-time. 

_Breakthrough Point:_ Developing physics-constrained adversarial training loops, where a discriminator network is trained to judge not only the realism of a generated modality but also its consistency with physical laws, potentially guided by a differentiable physics engine as a third “umpire.” 

17 

- **Unified Latent Space Architectures:** Achieving modality-invariant representations will enable zero-shot transfer and few-shot learning across diverse sensory inputs. Yet building a shared latent manifold introduces its own representational pathologies. 

_Technical Difficulty:_ Naively sharing a latent space often leads to “modality collapse,” where one modality dominates the representation. A carefully structured latent hierarchy could offer a pathway to balanced, interpretable multimodal abstraction. 

_Breakthrough Point:_ Designing architectures with structured, factorized latent spaces and specialized cross-modal attention mechanisms that enforce a “common language” for abstract physical concepts (e.g., ‘rigidity‘, ‘impact_force‘) rather than just low-level features. 

#### **5.3.4 Pathway IV: From Passive Hearing to Active Perception — Physical and Exploratory Agents** 

The future lies with embodied agents that are active sensors, performing experiments to learn about the world, inspired by echolocating animals [38]. 

- **Information-Theoretic Action Selection:** An optimal agent strategically selects actions that maximize information gain, thereby turning the world into an adaptive curriculum for self-supervised learning. Unfortunately, the required information-gain computations are often intractable in continuous action spaces. 

_Technical Difficulty:_ Calculating the expected information gain for all possible actions in continuous action spaces is often intractable. Overcoming this bottleneck will involve new approximation paradigms that scale with dimensionality while preserving theoretical guarantees. 

_Breakthrough Point:_ Developing efficient approximation methods, such as learning a “value of information” function that directly predicts the utility of an action for model improvement, turning the information-gathering problem into a standard RL problem. 

- **The Perception-Action Loop Dilemma:** Building a refined world model and discovering informative actions are tightly coupled tasks, each dependent on the other for progress. Breaking this cycle requires mechanisms for staged acquisition of competence. 

_Technical Difficulty:_ This is a “chicken-and-egg” problem: a good world model is needed to select informative actions, but informative actions are needed to build a good model. Curriculum strategies that reward learning progress, rather than immediate task success, offer a promising escape from this loop. 

_Breakthrough Point:_ Employing curriculum learning and intrinsic motivation. The agent starts with simple, random “babbling” actions to build a crude initial model, then is rewarded for actions that lead to the largest improvement (i.e., highest prediction error) in its world model, driving it to explore the boundaries of its knowledge. 

#### **5.3.5 Pathway V: From Custom Models to General AI — Core Model Framework for Acoustic Physics** 

The grand challenge is to train a massive, multi-task, multimodal foundation model on the entirety of available acoustic-physical data. 

- **Unprecedented Data Scale and Heterogeneity:** Curating petabyte-scale corpora across simulation, robotics, and real-world recordings will supply the raw fuel required to train a genuinely world model. The logistical and engineering demands of such a corpus, however, are without historical precedent. 

_Technical Difficulty:_ Harmonizing these diverse data sources with varying labels, noise levels, and formats is a significant engineering challenge. Real progress will require pre-training objectives that thrive on noise and exploit complementary structure across modalities. 

_Breakthrough Point:_ Developing sophisticated self-supervised pre-training objectives that are robust to noise and can learn from multiple data modalities simultaneously, such as a physics-informed version of masked autoencoding across audio, video, and text tokens. 

18 

- **Architectural and Computational Scalability:** Scaling up from niche prototypes to a true foundation model demands both algorithmic ingenuity and hardware-software co-design tailored to continuous signals. The resource footprint of a naive transformer approach exceeds the budgets of even well-funded laboratories. 

_Technical Difficulty:_ The computational cost is extremely high, and standard transformer architectures may not be optimal for continuous, physical signals. Progress will hinge on a class of models whose capacity grows sub-linearly with compute while maintaining expressive power. 

_Breakthrough Point:_ Innovations in efficient model architectures (e.g., state-space models, mixtureof-experts) and specialized hardware/software co-design to make training such a model feasible. The ultimate vision is a single model that can be fine-tuned for a vast range of physical acoustic tasks with minimal new data. 


Figure 2: A proposed research roadmap for the next generation of acoustic world models. 

_The roadmap illustrates a progression through five key research pathways: (1) Causality, moving from correlation to causal understanding; (2) Uncertainty Quantification, advancing from deterministic to probabilistic models; (3) Cross-Modal Imagination, achieving unified physical perception; (4) Active Sensing, shifting from passive listening to embodied interaction; and (5) Foundation Models, aiming for a generalpurpose physical acoustic intelligence. The structure suggests how these pillars build upon each other towards more robust and generalizable AI._ 

## **6 Conclusions and Future Work** 

This survey has presented a comprehensive, in-depth overview of the principles, methodological frameworks, and applications of world models built upon the rich foundation of acoustic physical information. Our central thesis posits a paradigm shift: moving beyond treating sound as a mere sensory channel for event detection, and instead embracing it as a direct, physical medium for understanding the world. We have established that unlike vision, which primarily captures surface-level phenomena susceptible to occlusion 

19 

and illumination variance, acoustic signals are the radiated mechanical energy of physical events. Governed by the fundamental laws of elastodynamics and aeroacoustics, they carry intrinsic, latent "acoustic signatures" of material composition, internal geometry, contact dynamics, and fluid flow. This makes sound a powerful, penetrating modality for AI to develop a form of "physical intuition," enabling a deeper, more robust, and more causal grasp of its environment that is fundamentally complementary to other senses. 

The pathway to unlocking this potential lies in the synergistic integration of three core methodological pillars. We demonstrated how PINNs provide the important "gray-box" framework, embedding physical laws as strong regularizers to solve ill-posed inverse problems and ensure physical plausibility, even with sparse data. Complementing this, generative forward models—from differentiable simulators to neural acoustic fields—act as the AI’s "imagination," empowering it to predict future sensory inputs, synthesize physically-grounded audio for controllable worlds, and serve as powerful data factories for training. Finally, self-supervised and multimodal learning frameworks provide the scalability, learning from the natural co-occurrence of unlabeled sensory streams to build powerful, high-level representations that form the semantic bedrock for downstream tasks. It is the fusion of these approaches—the rigor of physics, the predictive power of generation, and the scalability of self-supervision—that forms the cohesive engine for acoustic intelligence. 

The transformative impact of these acoustically-grounded world models is already materializing across a broad spectrum of high-stakes domains. In robotics, they promise to endow machines with haptic-like sensitivity, enabling delicate manipulation and robust navigation in visually-denied environments. For autonomous driving, they offer a vital, omnidirectional safety layer, detecting non-line-of-sight hazards and classifying road conditions with a fidelity that vision alone cannot guarantee. In healthcare and finance, these models are democratizing diagnostics by turning everyday devices into non-invasive health monitors and uncovering subtle, non-consensus alpha signals in vocal biomarkers that transcend traditional text analysis. 

However, the path forward is paved with significant scientific, computational, and, most thoroughly, ethical challenges. As this survey has detailed, the power to listen is a dual-use capability. The pervasive nature of acoustic sensing demands a non-negotiable commitment to "privacy-by-design," robust on-device processing, and federated learning. Algorithmic bias in acoustic data can perpetuate and amplify societal inequities, mandating auditing and the development of fairness-aware algorithms. Moreover, in high-stakes decisions, the "black box" is unacceptable; the pursuit of explainable AI for acoustic models is not a mere academic exercise but a prerequisite for accountability and public trust. 

Looking ahead, the research pathways outlined—towards causal inference, probabilistic uncertainty quantification, unified cross-modal imagination, active embodied sensing, and ultimately, a foundational model for physical acoustics—provide a clear and ambitious roadmap. This is not simply a technical agenda; it is a blueprint for evolving AI from a sophisticated pattern-matcher into a nascent scientific reasoner, capable of forming hypotheses, performing experiments, and understanding the world through its underlying physical laws. Continued, dedicated research and, above all, responsible development in this area hold the promise of building safer, more capable, and more humane artificial intelligence. By learning to listen to the physics of the world, AI can lay an important and enduring cognitive foundation for the future of human-machine symbiosis, where technology understands our world not just by its appearance, but by its very substance. 

In summary, the key contributions of this survey are: 

- It defines and frames the emerging field of world models grounded in acoustic physical information. 

- It establishes the central role of acoustic signals in physical perception and causal reasoning, moving beyond surface-level correlations. 

- It provides a structured review and comparative analysis of the core methodologies that fuse physical principles with advanced machine learning techniques. 

- It details the significant real-world impact and future potential of acoustic world models across diverse, high-stakes application domains. 

- It analyzes the primary technical and ethical challenges with deep case studies, and proposes a concrete, forward-looking research roadmap with specified technical hurdles and breakthroughs to guide future innovation. 

20 

### **Next Steps in Our Research** 

Based on the framework and roadmap detailed in this survey, our own research group is actively pushing these frontiers. Our prior work has already laid a practical foundation for some of these concepts. For instance, in [44], we introduced a novel framework that integrates nonlinear acoustic computing with reinforcement learning to enhance human-robot interaction under severe noise and reverberation. By embedding physically informed wave equations like Westervelt and KZK into a reinforcement learning loop, our system adaptively optimizes parameters such as beamforming and absorption, demonstrating superior noise suppression and accuracy over traditional methods. 

Looking ahead, we plan to extend this line of inquiry in two primary directions. First, we will further develop the concept of the acoustic world model specifically for the challenging task of human vocal denoising in complex, dynamic scenes. Instead of treating this as a purely statistical signal separation problem, our goal is to build models that can physically reason about the environment—including room geometry, noise source characteristics, and multipath propagation—to "imagine" and reconstruct the clean vocal signal. Second, we will continue to deepen our exploration of these research ideas within the domain of robotics. The main goal is to move beyond passive sound perception and give robots a true physical understanding from sound, enabling more reliable navigation, safer human–robot teamwork, and finer object handling, thus advancing the human–machine partnership highlighted in this survey. 

### **Limitations in Our Survey** 

While we have strived for a comprehensive and structured overview, we acknowledge certain limitations inherent in this work. Firstly, our survey’s primary focus is on the computational and machine learning frameworks for acoustic world models. Consequently, the equally important domains of advanced acoustic sensor design, microphone array signal processing, and the nuances of physical acoustics theory itself were discussed primarily in service of the AI models, rather than as standalone topics. A deeper exploration of the co-design of novel sensing hardware and learning algorithms represents a vital area for future reviews. Secondly, in balancing breadth with depth, our review of methodologies necessarily provides a high-level synthesis. A deep, mathematical dive into the intricacies and variants of every discussed algorithm (e.g., different PINN formulations or diffusion model architectures) was beyond our scope. Lastly, the field of AI is advancing at a breathtaking pace. This survey serves as a foundational snapshot at a specific point in time. We encourage readers to view it as a starting point and to actively follow the latest developments in top-tier conferences, as new state-of-the-art approaches are continually emerging. These identified gaps represent fertile ground for future research and more specialized reviews. 

## **Acknowledgements** 

The authors would like to express their sincere gratitude to the broader research community for their pioneering work, which formed the foundation of this survey. We are particularly indebted to the researchers and faculty at the Institute of Acoustics, Chinese Academy of Sciences, Peking University, and The University of Hong Kong for their foundational contributions to acoustics, signal processing, and artificial intelligence. Their work and the insightful discussions they have fostered within the academic community have been a profound source of inspiration. We also thank the anonymous reviewers for their constructive comments and suggestions, which have significantly improved the quality and clarity of this paper. 

## **A A List of Benchmarks, Datasets, and Simulators** 

To facilitate further research and provide a practical starting point for newcomers to the field, this appendix lists key resources, including public datasets, simulation environments, and standardized benchmarks. These resources are foundational for developing, training, and evaluating acoustic world models. 

### **A.1 Public Datasets for Acoustic Perception and Modeling** 

- **AudioSet:** Developed by Google, this is one of the largest publicly available datasets for general sound event detection. It consists of over 2 million weakly-labeled 10-second video clips from YouTube, 

21 

annotated with an ontology of 632 sound event classes. It is invaluable for pre-training large-scale audio representation models [83]. 

- **FSD50K:** An open dataset of human-labeled sound events containing over 51,000 audio clips drawn from the Freesound database. Its high-quality manual annotations and permissive license make it a go-to resource for supervised sound event detection and classification tasks [84]. 

- **WHAM!:** A dataset designed for speech separation tasks. It generates mixtures by combining speech from the WSJ0 corpus in simulated anechoic and reverberant rooms. Its provision of clean source signals, mixtures, and the corresponding room impulse responses (RIRs) makes it highly suitable for research on acoustic propagation and dereverberation [85]. 

- **TAU Acoustic Scenes Series:** A collection of datasets released as part of the DCASE (Detection and Classification of Acoustic Scenes and Events) challenge. These datasets are meticulously recorded in various real-world locations (e.g., streets, parks, public transport) using standardized equipment, making them a primary benchmark for acoustic scene classification [86]. 

### **A.2 Simulation Environments for Embodied and Physical AI** 

- **AI Habitat (Habitat-Sim):** A high-performance 3D simulator with an emphasis on photorealism and speed, primarily for training embodied AI agents (e.g., robots) [87]. Its extension, Habitat-Sound, integrates physically-based sound rendering, enabling research on audio-visual navigation and acoustic mapping in complex indoor environments [88]. 

- **Isaac Gym / Isaac Sim:** A suite of simulation tools from NVIDIA that leverage GPU acceleration for large-scale, physics-based reinforcement learning. Its strength lies in simulating rigid and soft-body dynamics, articulations, and contact mechanics, making it an ideal platform for generating physically accurate interaction sounds for robotic manipulation tasks [89]. 

- **ThreeDWorld (TDW):** A multimodal, interactive, and physically realistic simulation platform [90]. TDW features a sophisticated procedural audio engine (PyImpact) that can synthesize physicallybased impact and contact sounds in real-time based on the objects’ material properties, geometry, and collision dynamics. It is exceptionally well-suited for studying the causal link between physical interactions and their acoustic signatures. 

- **SAPiEN:** A realistic and articulated object-centric simulator for robotics. It provides accurate physics simulation, which is important for tasks involving robotic manipulation and learning from interaction. It can serve as a powerful data generator for action-conditioned acoustic models [91]. 

### **A.3 Standardized Benchmarks and Challenges** 

- **DCASE Challenge:** The premier annual competition for the "Detection and Classification of Acoustic Scenes and Events". It provides well-defined tasks, public datasets, and a standardized evaluation framework, driving progress in a wide range of acoustic analysis problems [92]. 

- **Audio-Visual Navigation Benchmark:** A common task within embodied AI challenges (e.g., at the Conference on Computer Vision and Pattern Recognition (CVPR)). The agent is placed in a 3D environment and must navigate to a sounding object using both visual and auditory inputs. It serves as a key benchmark for multimodal perception and action, heavily popularized by simulators like Habitat-Sound [88]. 

- **HEAR Challenge:** A benchmark for the "Holistic Evaluation of Audio Representations" designed to evaluate the generalization of learned audio representations. Models are pre-trained and then evaluated on a diverse suite of 19 downstream tasks, providing a comprehensive assessment of a representation’s quality and robustness [93]. 

22 

## **B A Living Repository of Resources** 

For a comprehensive and continuously updated list of resources, including direct links to datasets, simulators, seminal papers, and open-source codebases relevant to this survey, please visit our curated repository on GitHub: `https://github.com/soundai2016/survey_acoustic_world_models` 

## **References** 

- [1] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell _et al._ , “Language models are few-shot learners,” _Advances in neural information processing systems_ , vol. 33, pp. 1877–1901, 2020. 

- [2] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei _et al._ , “Open foundation and fine-tuned chat models,” _arXiv preprint arXiv:2307.09288_ , 2023. 

- [3] E. M. Bender and A. Koller, “Climbing towards nlu: On meaning, form, and understanding in the age of data,” in _Proceedings of the 58th annual meeting of the association for computational linguistics_ , 2020, pp. 5185–5198. 

- [4] D. Ha and J. Schmidhuber, “World models,” _arXiv preprint arXiv:1803.10122_ , 2018. 

- [5] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” _arXiv preprint arXiv:1912.01603_ , 2019. 

- [6] Y. LeCun, “A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27,” _Open Review_ , vol. 62, no. 1, pp. 1–62, 2022. 

- [7] Y. Matsuo, Y. LeCun, M. Sahani, D. Precup, D. Silver, M. Sugiyama, E. Uchibe, and J. Morimoto, “Deep learning, reinforcement learning, and world models,” _Neural Networks_ , vol. 152, pp. 267–275, 2022. 

- [8] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification with deep convolutional neural networks,” _Communications of the ACM_ , vol. 60, no. 6, pp. 84–90, 2017. 

- [9] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly _et al._ , “An image is worth 16x16 words: Transformers for image recognition at scale,” _arXiv preprint arXiv:2010.11929_ , 2020. 

- [10] D. Hendrycks and T. Dietterich, “Benchmarking neural network robustness to common corruptions and perturbations,” _arXiv preprint arXiv:1903.12261_ , 2019. 

- [11] A. S. Bregman, _Auditory scene analysis: The perceptual organization of sound_ . MIT press, 1994. 

- [12] F. J. Vesely _et al._ , _Computational Physics_ . Springer, 1994. 

- [13] J. Traer and J. H. McDermott, “Statistics of natural reverberation enable perceptual separation of sound and space,” _Proceedings of the National Academy of Sciences_ , vol. 113, no. 48, pp. E7856–E7865, 2016. 

- [14] B. L. Giordano, “Material categorization and hardness scaling in real and synthetic impact sounds,” _The sounding object_ , pp. 73–94, 2003. 

- [15] R. Schwarz and J. Vuorinen, “Resonant ultrasound spectroscopy: applications, current status and limitations,” _Journal of Alloys and Compounds_ , vol. 310, no. 1-2, pp. 243–250, 2000. 

- [16] J. Jodhani, A. Handa, A. Gautam, R. Rana _et al._ , “Ultrasonic non-destructive evaluation of composites: A review,” _Materials Today: Proceedings_ , vol. 78, pp. 627–632, 2023. 

23 

- [17] S.-H. Park, S. Choi, and K.-Y. Jhang, “Porosity evaluation of additively manufactured components using deep learning-based ultrasonic nondestructive testing,” _International Journal of Precision Engineering and Manufacturing-Green Technology_ , vol. 9, no. 2, pp. 395–407, 2022. 

- [18] F. Guo, W. Li, P. Jiang, F. Chen, and Y. Liu, “Deep learning approach for damage classification based on acoustic emission data in composite materials,” _Materials_ , vol. 15, no. 12, p. 4270, 2022. 

- [19] P. R. Cook, “Sound production and modeling,” _IEEE Computer Graphics and applications_ , vol. 22, no. 4, pp. 23–27, 2002. 

- [20] F. Avanzini, D. Rocchesso _et al._ , “Controlling material properties in physical models of sounding objects,” in _ICMC_ , 2001. 

- [21] A. S. Bregnian, “Auditory scene analysis: Hearing in complex environments,” 1993. 

- [22] T. Wang, P. Zheng, S. Li, and L. Wang, “Multimodal human–robot interaction for human-centric smart manufacturing: a survey,” _Advanced Intelligent Systems_ , vol. 6, no. 3, p. 2300359, 2024. 

- [23] P. Chang, S. Liu, H. Chen, and K. Driggs-Campbell, “Robot sound interpretation: Combining sight and sound in learning-based control,” in _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2020, pp. 5580–5587. 

- [24] A. Fares, I. Tijani, Z. Rui, and T. Zayed, “Leak detection in real water distribution networks based on acoustic emission and machine learning,” _Environmental Technology_ , vol. 44, no. 25, pp. 3850–3866, 2023. 

- [25] M. Wang, M. Chen, Z. Wang, Y. Guo, Y. Wu, W. Zhao, and X. Liu, “Estimating rainfall intensity based on surveillance audio and deep-learning,” _Environmental Science and Ecotechnology_ , vol. 22, p. 100450, 2024. 

- [26] S.-K. Lee, J. Yoo, C.-H. Lee, K. An, Y.-S. Yoon, J. Lee, G.-H. Yeom, and S.-U. Hwang, “Road type classification using deep learning for tire-pavement interaction noise data in autonomous driving vehicle,” _Applied Acoustics_ , vol. 212, p. 109597, 2023. 

- [27] R. B. Randall, _Vibration-based condition monitoring: industrial, automotive and aerospace applications_ . John Wiley & Sons, 2021. 

- [28] M. J. Lighthill, “On sound generated aerodynamically i. general theory,” _Proceedings of the Royal Society of London. Series A. Mathematical and Physical Sciences_ , vol. 211, no. 1107, pp. 564–587, 1952. 

- [29] H. Shao, H. Jiang, H. Zhao, and F. Wang, “A novel deep autoencoder feature learning method for rotating machinery fault diagnosis,” _Mechanical Systems and Signal Processing_ , vol. 95, pp. 187–204, 2017. 

- [30] J. Cen, Z. Yang, X. Liu, J. Xiong, and H. Chen, “A review of data-driven machinery fault diagnosis using machine learning algorithms,” _Journal of Vibration Engineering & Technologies_ , vol. 10, no. 7, pp. 2481–2507, 2022. 

- [31] H. Kuttruff and M. Vorländer, _Room acoustics_ . Crc Press, 2024. 

- [32] Q. Song, C. Gu, and R. Tan, “Deep room recognition using inaudible echos,” _Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies_ , vol. 2, no. 3, pp. 1–28, 2018. 

- [33] M. Brandstein and D. Ward, _Microphone arrays: signal processing techniques and applications_ . Springer Science & Business Media, 2001. 

- [34] D. Desai and N. Mehendale, “A review on sound source localization systems,” _Archives of Computational Methods in Engineering_ , vol. 29, no. 7, pp. 4631–4642, 2022. 

- [35] C. Evers and P. A. Naylor, “Acoustic slam,” _IEEE/ACM Transactions on Audio, Speech, and Language Processing_ , vol. 26, no. 9, pp. 1484–1498, 2018. 

24 

- [36] M. Jiang, S. Song, Y. Li, W. Jin, J. Liu, and X. Feng, “A survey of underwater acoustic slam system,” in _Intelligent Robotics and Applications: 12th International Conference, ICIRA 2019, Shenyang, China, August 8–11, 2019, Proceedings, Part II 12_ . Springer, 2019, pp. 159–170. 

- [37] I. Dokmanić, R. Parhizkar, A. Walther, Y. M. Lu, and M. Vetterli, “Acoustic echoes reveal room shape,” _Proceedings of the National Academy of Sciences_ , vol. 110, no. 30, pp. 12 186–12 191, 2013. 

- [38] J. Steckel and H. Peremans, “Batslam: Simultaneous localization and mapping using biomimetic sonar,” _PloS one_ , vol. 8, no. 1, p. e54076, 2013. 

- [39] X. Zhang, Q. Zhang, X. Hu, and B. Zhang, “Neural representation of three-dimensional acoustic space in the human temporal lobe,” _Frontiers in Human Neuroscience_ , vol. 9, p. 203, 2015. 

- [40] L. Savioja and U. P. Svensson, “Overview of geometrical room acoustic modeling techniques,” _The Journal of the Acoustical Society of America_ , vol. 138, no. 2, pp. 708–730, 2015. 

- [41] D. Schwarz, “A system for data-driven concatenative sound synthesis,” in _Digital Audio Effects (DAFx)_ , 2000, pp. 97–102. 

- [42] P. Pertilä, _Acoustic source localization in a room environment and at moderate distances_ . Tampere University of Technology, 2009. 

- [43] Q. Zuwen, “Nonlinear acoustics in china,” _WULI-BEIJING-_ , vol. 28, no. 10, pp. 593–599, 1999. 

- [44] X. Chen, X. Yu, L. Chang, Y. Huang, J. He, S. Zhang, J. Li, L. Lin, Z. Zeng, X. Tu _et al._ , “A synergistic framework of nonlinear acoustic computing and reinforcement learning for real-world humanrobot interaction,” _arXiv preprint arXiv:2505.01998_ , 2025. 

- [45] M. Raissi, P. Perdikaris, and G. E. Karniadakis, “Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations,” _Journal of Computational physics_ , vol. 378, pp. 686–707, 2019. 

- [46] G. E. Karniadakis, I. G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang, and L. Yang, “Physics-informed machine learning,” _Nature Reviews Physics_ , vol. 3, no. 6, pp. 422–440, 2021. 

- [47] M. Zhang, T. Guo, G. Zhang, Z. Liu, and W. Xu, “Physics-informed deep learning for structural vibration identification and its application on a benchmark structure,” _Philosophical Transactions of the Royal Society A_ , vol. 382, no. 2264, p. 20220400, 2024. 

- [48] Y. Lee and J. Ryu, “A study on the auralization system using flexible rendering for virtual reality-based acoustic simulation,” _Journal of Advanced Mechanical Design, Systems, and Manufacturing_ , vol. 13, no. 5, pp. JAMDSM0094–JAMDSM0094, 2019. 

- [49] M. Olivieri, X. Karakonstantis, M. Pezzoli, F. Antonacci, A. Sarti, and E. Fernandez-Grande, “Physicsinformed neural network for volumetric sound field reconstruction of speech signals,” _EURASIP Journal on Audio, Speech, and Music Processing_ , vol. 2024, no. 1, p. 42, 2024. 

- [50] T. Hayes, S. Zhang, X. Yin, G. Pang, S. Sheng, H. Yang, S. Ge, Q. Hu, and D. Parikh, “Mugen: A playground for video-audio-text multimodal understanding and generation,” in _European Conference on Computer Vision_ . Springer, 2022, pp. 431–449. 

- [51] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, “Nerf: Representing scenes as neural radiance fields for view synthesis,” _Communications of the ACM_ , vol. 65, no. 1, pp. 99–106, 2021. 

- [52] J. Gao, H. Yang, M. Gong, and X. Li, “Audio–visual representation learning for anomaly events detection in crowds,” _Neurocomputing_ , vol. 582, p. 127489, 2024. 

- [53] E. Dupont, M. B. Martin, A. Colburn, A. Sankar, J. Susskind, and Q. Shan, “Equivariant neural rendering,” in _International Conference on Machine Learning_ . PMLR, 2020, pp. 2761–2770. 

25 

- [54] Z. Kong, W. Ping, J. Huang, K. Zhao, and B. Catanzaro, “Diffwave: A versatile diffusion model for audio synthesis,” _arXiv preprint arXiv:2009.09761_ , 2020. 

- [55] A. K. Dwivedi, S. A. Imtiaz, and E. Rodriguez-Villegas, “Algorithms for automatic analysis and classification of heart sounds–a systematic review,” _IEEE Access_ , vol. 7, pp. 8316–8345, 2018. 

- [56] A. M. Ismael and A. Şengür, “Deep learning approaches for covid-19 detection based on chest x-ray images,” _Expert Systems with Applications_ , vol. 164, p. 114054, 2021. 

- [57] R. Arandjelovic and A. Zisserman, “Look, listen and learn,” in _Proceedings of the IEEE international conference on computer vision_ , 2017, pp. 609–617. 

- [58] A. Owens and A. A. Efros, “Audio-visual scene analysis with self-supervised multisensory features,” in _Proceedings of the European conference on computer vision (ECCV)_ , 2018, pp. 631–648. 

- [59] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PMLR, 2021, pp. 8748–8763. 

- [60] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds _et al._ , “Flamingo: a visual language model for few-shot learning,” _Advances in neural information processing systems_ , vol. 35, pp. 23 716–23 736, 2022. 

- [61] A. Senocak, T.-H. Oh, J. Kim, M.-H. Yang, and I. S. Kweon, “Learning to localize sound source in visual scenes,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2018, pp. 4358–4366. 

- [62] R. Gao and K. Grauman, “Co-separating sounds of visual objects,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2019, pp. 3879–3888. 

- [63] J. Sinapov and A. Stoytchev, “Object category recognition by a humanoid robot using behaviorgrounded relational learning,” in _2011 IEEE International Conference on Robotics and Automation_ . IEEE, 2011, pp. 184–190. 

- [64] A. Bonarini, “Communication in human-robot interaction,” _Current Robotics Reports_ , vol. 1, no. 4, pp. 279–285, 2020. 

- [65] T. K. Chan and C. S. Chin, “A comprehensive review of polyphonic sound event detection,” _IEEE Access_ , vol. 8, pp. 103 339–103 373, 2020. 

- [66] U. Mittal and P. Chawla, “Acoustic based emergency vehicle detection using ensemble of deep learning models,” _Procedia Computer Science_ , vol. 218, pp. 227–234, 2023. 

- [67] M. Crocco, M. Cristani, A. Trucco, and V. Murino, “Audio surveillance: A systematic review,” _ACM Computing Surveys (CSUR)_ , vol. 48, no. 4, pp. 1–46, 2016. 

- [68] N. Cummins, S. Scherer, J. Krajewski, S. Schnieder, J. Epps, and T. F. Quatieri, “A review of depression and suicide risk assessment using speech analysis,” _Speech communication_ , vol. 71, pp. 10–49, 2015. 

- [69] J. Laguarta, F. Hueto, and B. Subirana, “Covid-19 artificial intelligence diagnosis using only cough recordings,” _IEEE Open Journal of Engineering in Medicine and Biology_ , vol. 1, pp. 275–281, 2020. 

- [70] L. di Biase, G. Tinkhauser, E. Martin Moraud, M. L. Caminiti, P. M. Pecoraro, and V. Di Lazzaro, “Adaptive, personalized closed-loop therapy for parkinson’s disease: Biochemical, neurophysiological, and wearable sensing systems,” _Expert review of neurotherapeutics_ , vol. 21, no. 12, pp. 1371–1388, 2021. 

- [71] S. G. Koolagudi and K. S. Rao, “Emotion recognition from speech: a review,” _International journal of speech technology_ , vol. 15, pp. 99–117, 2012. 

- [72] T. M. Wani, T. S. Gunawan, S. A. A. Qadri, M. Kartiwi, and E. Ambikairajah, “A comprehensive review of speech emotion recognition systems,” _IEEE access_ , vol. 9, pp. 47 795–47 814, 2021. 

26 

- [73] T. Baltrušaitis, C. Ahuja, and L.-P. Morency, “Multimodal machine learning: A survey and taxonomy,” _IEEE transactions on pattern analysis and machine intelligence_ , vol. 41, no. 2, pp. 423–443, 2018. 

- [74] W. J. Mayew and M. Venkatachalam, “The power of voice: Managerial affective states and future firm performance,” _The Journal of Finance_ , vol. 67, no. 1, pp. 1–43, 2012. 

- [75] J. L. Hobson, W. J. Mayew, and M. Venkatachalam, “Analyzing speech to detect financial misreporting,” _Journal of Accounting Research_ , vol. 50, no. 2, pp. 349–392, 2012. 

- [76] S. A. Chowdhury, E. A. Stepanov, G. Riccardi _et al._ , “Predicting user satisfaction from turn-taking in spoken conversations.” in _Interspeech_ , 2016, pp. 2910–2914. 

- [77] S. Han, H. Mao, and W. J. Dally, “Deep compression: Compressing deep neural networks with pruning, trained quantization and huffman coding,” _arXiv preprint arXiv:1510.00149_ , 2015. 

- [78] D. Wang and J. Chen, “Supervised speech separation based on deep learning: An overview,” _IEEE/ACM transactions on audio, speech, and language processing_ , vol. 26, no. 10, pp. 1702–1726, 2018. 

- [79] J. Konečn`y, H. B. McMahan, F. X. Yu, P. Richtárik, A. T. Suresh, and D. Bacon, “Federated learning: Strategies for improving communication efficiency,” _arXiv preprint arXiv:1610.05492_ , 2016. 

- [80] Y. Yang, P. Hu, J. Shen, H. Cheng, Z. An, and X. Liu, “Privacy-preserving human activity sensing: A survey,” _High-Confidence Computing_ , vol. 4, no. 1, p. 100204, 2024. 

- [81] Y. Jia, Y. Zhang, R. Weiss, Q. Wang, J. Shen, F. Ren, P. Nguyen, R. Pang, I. Lopez Moreno, Y. Wu _et al._ , “Transfer learning from speaker verification to multispeaker text-to-speech synthesis,” _Advances in neural information processing systems_ , vol. 31, 2018. 

- [82] W. Samek, G. Montavon, S. Lapuschkin, C. J. Anders, and K.-R. Müller, “Explaining deep neural networks and beyond: A review of methods and applications,” _Proceedings of the IEEE_ , vol. 109, no. 3, pp. 247–278, 2021. 

- [83] J. F. Gemmeke, D. P. Ellis, D. Freedman, A. Jansen, W. Lawrence, R. C. Moore, M. Plakal, and M. Ritter, “Audio set: An ontology and human-labeled dataset for audio events,” in _2017 IEEE international conference on acoustics, speech and signal processing (ICASSP)_ . IEEE, 2017, pp. 776–780. 

- [84] E. Fonseca, X. Favory, J. Pons, F. Font, and X. Serra, “Fsd50k: an open dataset of human-labeled sound events,” _IEEE/ACM Transactions on Audio, Speech, and Language Processing_ , vol. 30, pp. 829–852, 2021. 

- [85] G. Wichern, J. Antognini, M. Flynn, L. R. Zhu, E. McQuinn, D. Crow, E. Manilow, and J. L. Roux, “Wham!: Extending speech separation to noisy environments,” _arXiv preprint arXiv:1907.01160_ , 2019. 

- [86] A. Mesaros, T. Heittola, and T. Virtanen, “Tut database for acoustic scene classification and sound event detection,” in _2016 24th European Signal Processing Conference (EUSIPCO)_ . IEEE, 2016, pp. 1128–1132. 

- [87] M. Savva, A. Kadian, O. Maksymets, Y. Zhao, E. Wijmans, B. Jain, J. Straub, J. Liu, V. Koltun, J. Malik _et al._ , “Habitat: A platform for embodied ai research,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 9339–9347. 

- [88] C. Chen, U. Jain, C. Schissler, S. V. A. Gari, Z. Al-Halah, V. K. Ithapu, P. Robinson, and K. Grauman, “Soundspaces: Audio-visual navigation in 3d environments,” in _Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part VI 16_ . Springer, 2020, pp. 17–36. 

- [89] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

27 

- [90] C. Gan, J. Schwartz, S. Alter, D. Mrowca, M. Schrimpf, J. Traer, J. De Freitas, J. Kubilius, A. Bhandwaldar, N. Haber _et al._ , “Threedworld: A platform for interactive multi-modal physical simulation,” _arXiv preprint arXiv:2007.04954_ , 2020. 

- [91] F. Xiang, Y. Qin, K. Mo, Y. Xia, H. Zhu, F. Liu, M. Liu, H. Jiang, Y. Yuan, H. Wang _et al._ , “Sapien: A simulated part-based interactive environment,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 11 097–11 107. 

- [92] A. Mesaros, R. Serizel, T. Heittola, T. Virtanen, and M. D. Plumbley, “A decade of dcase: Achievements, practices, evaluations and future challenges,” in _ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ . IEEE, 2025, pp. 1–5. 

- [93] J. Turian, J. Shier, H. R. Khan, B. Raj, B. W. Schuller, C. J. Steinmetz, C. Malloy, G. Tzanetakis, G. Velarde, K. McNally _et al._ , “Hear: Holistic evaluation of audio representations,” in _NeurIPS 2021 Competitions and Demonstrations Track_ . PMLR, 2022, pp. 125–145. 

28 

