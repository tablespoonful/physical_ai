---
title: "VQ-VLA: Improving Vision-Language-Action Models via Scaling Vector-Quantized Action Tokenizers"
date: "2025-07-01"
authors: "Yating Wang; Haoyi Zhu; Mingyu Liu; Jiange Yang; Hao-Shu Fang; Tong He"
venue: "ICCV 2025"
url: https://arxiv.org/abs/2507.01016
pdf: https://arxiv.org/pdf/2507.01016
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.01016)** / [論文ページ](https://arxiv.org/abs/2507.01016)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This ICCV paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **VQ-VLA: Improving Vision-Language-Action Models via Scaling Vector-Quantized Action Tokenizers** 

Yating Wang<sup>12</sup> Haoyi Zhu<sup>23</sup> Mingyu Liu<sup>24</sup> Jiange Yang<sup>25</sup> Hao-Shu Fang<sup>6</sup> Tong He<sup>27†</sup> 1Shanghai Research Institute for Intelligent Autonomous Systems, Tongji University 2Shanghai AI Lab 3USTC 4ZJU 5NJU 6SJTU 7SII 

†Corresponding Author 

https://xiaoxiao0406.github.io/vqvla.github.io 

## **Abstract** 

_In this paper, we introduce an innovative vector quantization based action tokenizer built upon the largest-scale action trajectory dataset to date, leveraging over 100 times more data than previous approaches. This extensive dataset enables our tokenizer to capture rich spatiotemporal dynamics, resulting in a model that not only accelerates inference but also generates smoother and more coherent action outputs. Once trained, the tokenizer can be seamlessly adapted to a wide range of downstream tasks in a zero-shot manner, from short-horizon reactive behaviors to long-horizon planning. A key finding of our work is that the domain gap between synthetic and real action trajectories is marginal, allowing us to effectively utilize a vast amount of synthetic data during training without compromising real-world performance. To validate our approach, we conducted extensive experiments in both simulated environments and on real robotic platforms. The results demonstrate that as the volume of synthetic trajectory data increases, the performance of our tokenizer on downstream tasks improves significantly—most notably, achieving up to a 30% higher success rate on two real-world tasks in long-horizon scenarios. These findings highlight the potential of our action tokenizer as a robust and scalable solution for real-time embodied intelligence systems, paving the way for more efficient and reliable robotic control in diverse application domains._ 

## **1. Introduction** 

Tokenization plays a critical role in recent generative models, including large language models (LLMs) [1, 31], image and video generation models [17, 23, 39], and vision-languageaction (VLA) models [8, 26]. One of the key benefits of tokenization is that it compresses the input space. By reducing high-dimensional continuous data into a compact sequence 

of tokens, the complexity of the learning task is substantially reduced. Compared to image patches and language tokens, action sequences are inherently easier to compress because of their spatio-temporal continuity. 

Recently, several studies have started to explore action quantized tokenization for Vision-Language-Action (VLA) models [5, 35], demonstrating promising potential. Effective action tokenization not only significantly enhances the downstream performance of VLA models, especially for tasks involving long-horizon planning, but also markedly improves their training and inference efficiency. In this paper, we delve deeper into the potential of action tokenization, with a specific emphasis on its scalability and accuracy. We first find that the more precise the tokenization, the more pronounced the improvements in long-horizon action modeling. This motivates us to train the VQ tokenizer with well-scaled action trajectories to cover various tasks. Additionally, we observe that action trajectories, unlike visual and physical modalities, exhibit minimal domain gaps between real-world and simulated environments. This characteristic enables effective scaling of action tokenizers through the extensive use of synthetic action data. Moreover, training action tokenizers is computationally lightweight compared to scaling entire VLA models. Consequently, focusing on scaling action tokenization emerges as a highly cost-effective strategy, requiring fewer computational and data resources while delivering significant performance enhancements. 

Specifically, we propose a convolutional residual VQVAE [5, 28, 52] framework for training action tokenizers. To effectively train the model, we propose a progressive training strategy: Initially, we train the tokenizer on realworld robotic datasets, such as OpenX-Embodiment [34], which typically contain noisy and jittery trajectories. Subsequently, we gradually integrate cleaner and smoother synthetic data from large-scale simulated robotic datasets, such as LIBERO [29] and ManiSkill [33]. This progressive approach allows the VQ model to converge toward smoother 

11089 

and more stable representations. Compared to previous approaches that typically rely on training with single-task datasets, our method expands the tokenizer training dataset by more than 100 times, effectively covering a broad spectrum of downstream tasks. 

We conduct extensive experiments in both simulated and real-world environments. First, we evaluate our VQ-VAE action tokenizers in the LIBERO simulator, where the results demonstrate the effectiveness of the convolutional residual VQ-VAE and provide preliminary validation for the hypothesis that the VQ-VAE action tokenizer can leverage synthetic data for scaling. Additionally, real-world experiments with a Franka Research 3 robot further validate the superiority of our approach. Specifically, our findings are as follows: (1) as the amount of simulated action data increases, the VQ-VAE tokenizers exhibit linear scaling properties in improving VLA success rates; (2) the tokenizers significantly enhance inference speed and smoothness of VLA models; and (3) the tokenizers effectively reduce cumulative errors, enabling better performance in long-horizon tasks. 

   - In summary, our contributions are as follows: 

- We propose a general convolutional residual VQ-VAEbased framework for action tokenizers. 

- We demonstrate that action tokenizers can be effectively scaled by leveraging large-scale simulated action data. 

- We prove that our action tokenizers improve the performance, inference speed, and long-horizon capabilities of VLA models. 

## **2. Related Works** 

**Vision-Language-Action Models.** Vision-Language-Action (VLA) models[7, 9, 11, 18, 26, 41, 45, 46, 56, 57] bridge visual-language understanding with robot control by mapping multimodal inputs to action outputs. Based on visionlanguage models (VLM) [3, 10, 11, 15], VLAs represent robot actions (e.g., 6DoF motion, gripper control) as discrete tokens compatible with text-based output. For example, RT1[7] and RT-2[8] showed that dividing continuous actions into discrete bins allows integration with VLMs, enabling zero-shot generalization using web-scale pretraining. Recent works[26, 34] further leverage this approach, demonstrating improved task generalization through large VLM backbones. Building on this foundation, recent works have explored various approaches to improve VLA, such as leveraging 3D visual inputs [57], integrating chain-of-thought reasoning [51], and employing parallel decoding strategies [27]. In our work, we aim to simultaneously improve the performance and execution speed of VLA. 

**Tokenization.** The tokenizer is one of the fundamental components in language and vision generation tasks, especially for autoregressive transformer-based generation models. For language generation tasks, mainstream methods adopt byte pair encoding (BPE) [19, 36] to compress input text. For 

vision generation tasks, recent works [17, 30, 37, 39, 53, 54] mainly use vector quantization [42] for tokenization to map continuous visual signals into a discrete token sequence. Similarly, in robot learning, many works [7, 8, 28, 32, 35] model action prediction as a generative problem and tokenize the robot action modality to capture the multi-modal distribution within skills and adapt it to autoregressive generative policies. In our work, we propose a general convolutional residual VQ-VAE to tokenize robot action. Different from several releated works [28, 32] that use VQ-VAE to tokenize robot actions, our VQ-VAE is trained on large-scale data and is applicable to all tasks. 

**Action Representation.** Action representation is one of the core components in robot policy learning. Classic action representation schemes include high-level sub-tasks [2, 15], action primitives [22, 43], keypoints [14, 20], as well as low-level continuous end-effector pose [29, 34] or joint state [21]. Recently, imitation learning-based end-to-end approaches [7, 13, 55, 60, 61] often utilize the latter. Some works[6, 40, 45, 58] employ regression-based output layers or integrate new weights for diffusion decoding for action output. Additionally, some works extract corresponding predictive signals from action-less video data to represent actions, such as pixels [9, 47], trajectories [44, 48], and latent motion [12, 49, 50]. To represent complex multi-modal distributions and adapt to discrete generative models, many works discretize continuous low-level actions. Common approaches include per-dimension and per-timestep binning discretization [7, 26], which struggles to perform well in high-frequency tasks [35]. Another method is VQ-VAE based discretization [4, 5, 28, 32, 59]; a limitation here is the need to train a separate action tokenizer for each specific task. Fast [35] utilized a discrete cosine transform (DCT) to learn a non-learnable action tokenizer from real-robot data. In this work, we propose a novel approach: expanding largescale synthetic data to train the VQ-VAE action tokenizer, aiming to enhance its generalizability and efficiency. 

## **3. Methods** 

### **3.1. Preliminaries: VLA models.** 

We use OpenVLA[26] as our backbone model. OpenVLA’s origin formulation is to adopt a discrete tokenization strategy for robot action prediction through fine-tuning the Prismatic7B VLM backbone. The method frames action prediction as a vision-language task, mapping input observation images and natural language instructions to discrete robot action sequences. Specifically, continuous robot actions are discretized into 256 bins per dimension, with bin boundaries determined by the 1st and 99th percentiles of training data distributions rather than min-max ranges to mitigate outlier effects. This discretization converts N-dimensional actions into N discrete integers (0-255). To embed these into the 

11090 


Figure 1. **The VQ-VLA pipeline** , consisting of two main stages: (1) training a general convolutional residual VQ-VAE and (2) fine-tuning OpenVLA using the LoRA approach. Specifically, a general convolutional residual VQ-VAE is first trained on the Open X-Embodiment dataset, LIEBRO, and ManiSkill datasets. The trained VQ-VAE is then frozen and serves as an action tokenizer for OpenVLA, replacing the simple binning method. In the second stage, OpenVLA is fine-tuned using the LoRA technique to optimize its performance. 

LLM’s vocabulary, OpenVLA overwrites the 256 least-used tokens in the Llama tokenizer (last 256 tokens) rather than using special tokens, as the original tokenizer only reserves 100 special tokens. 

### **3.2. Action Tokenizer via Residual VQ-VAE** 

Based on Residual VQ-VAE [5, 28, 52], we design our encoder and decoder inspired by VAE in pyramidal flow matching [25]. Instead of the simple Multi-Layer Perceptron (MLP) used in Residual VQ-VAE [28, 52], we integrate 2D temporal convolutional layers, motivated by their ability to efficiently capture local relationships and hierarchical temporal dependencies, addressing the scaling limitations of MLPs. 

Given an input action sequence **a** _t_ : _t_ + _n ∈_ R<sup>_n×d_</sup> , where _n_ is the sequence length and _d_ the action dimensionality, the encoder _ϕ_ enc, composed of 2D temporal convolutional layers, transforms the sequence into a latent embedding **x** _∈_ R<sup>_k_</sup> , expressed as **x** = _ϕ_ enc( **a** _t_ : _t_ + _n_ ). To compress **x** , we apply Residual Vector Quantization (RVQ) [52], decomposing **x** into quantized residuals: **q** ( **x** ) =<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_q_</sup><sup>**q**</sup><sup>_i_(</sup><sup>**r**</sup><sup>_i_), where</sup> **r** 1 = **x** , **r** _i_ +1 = **r** _i −_ **q** _i_ ( **r** _i_ ), and _Nq_ denotes the number of quantization stages. 

The quantized embedding **q** ( **x** ) is passed through the decoder _ϕ_ dec, which uses 2D temporal deconvolutional layers to reconstruct the sequence **a** ˆ _t_ : _t_ + _n_ , ensuring temporal structure preservation: **a** ˆ _t_ : _t_ + _n_ = _ϕ_ dec( **q** ( **x** )). 

To train the framework, we minimize the total loss _L_ , a weighted combination of reconstruction loss _L_ rec, vector quantization (VQ) loss _L_ codebook, and commitment loss _L_ commit: 


where sg( _·_ ) denotes the stop-gradient operation, and _λ_ balances the loss components. We set _λ_ = 4 in our experiments. This design ensures efficient, scalable, and robust encoding of structured temporal data. 

### **3.3. Training Residual VQ-VAE** 

We train three versions of the Residual VQ-VAE to evaluate the scaling capability of our action tokenizer: (1) using only the Open X-Embodiment dataset[34], (2) combining Open X-Embodiment and Libero datasets[29], and (3) combining Open X-Embodiment, Libero, and ManiSkill[33] datasets. These experiments were designed to test our hypothesis that the action tokenizer can effectively scale with simulated ata. 

- To improve the encoder’s ability to process temporal and 

- spatial information, we introduced two types of embeddings before the action sequences are passed into the encoder: • **Time Embedding** : A sinusoidal time embedding was added to encode temporal information at varying frequencies. This embedding allows the model to capture both 

11091 

low-frequency and high-frequency temporal patterns in the input actions, improving its ability to represent finegrained temporal details. 

- **Action-Type Embedding** : Learnable embeddings were added for the different components of the action sequence (e.g., XYZ positions, Euler angles, and gripper states). Since the 7 dimensions of the action vector have distinct meanings, this embedding provides a strong prior for the model, helping it distinguish and process the unique roles of each dimension more effectively. 

The use of these embeddings enhances the encoder’s ability to process structured data, improving the quality of the latent representations and the overall performance of the tokenizer. 

To train a more universal robot action tokenizer and reduce computational overhead, the model is trained using only action sequences as input, without additional conditional inputs. This design reduces complexity while maintaining the generalizability of the tokenizer. All models are trained on a single A100 GPU. For example, training on the Open X-Embodiment dataset requires just one A100 GPU and is completed in one week. 

### **3.4. Integrating Residual VQ-VAE as Action Tokenizer in VLA** 

In this work, we replace the simple bin-based action tokenizer used in OpenVLA with a Residual VQ-VAE-based action tokenizer to improve the expressiveness and precision of action tokenization. Instead of discretizing action sequences into uniform bins, the action sequence **a** _t_ : _t_ + _n_ is first processed through a pre-trained and frozen Residual VQVAE encoder _ϕ_ ( _·_ ), generating latent representations. These representations are then quantized into discrete codebook indices (tokens) _{zq_<sup>_i}_</sup> _i_<sup>_N_</sup> =1<sup>_q_corresponding to</sup><sup>_Nq_Residual VQ</sup> layers. The quantized tokens _zq_<sup>_i_are used as the action tokens</sup> for training and prediction in the Vision-Language Model (VLM). 

Unlike OpenVLA, where all token IDs are mapped to the range [0 _,_ 255], the token IDs generated by different VQ layers in the Residual VQ-VAE are assigned unique, nonoverlapping ranges. Specifically, tokens from the _i_ -th VQ layer are offset by ( _i −_ 1) _×_ 256, ensuring that: 


For example, tokens from the first layer are in the range [0 _,_ 255], those from the second layer are in [256 _,_ 511], and so on. This design avoids conflicts between token IDs from different layers, as tokens with the same ID in different layers represent semantically different features of the action space. 

The Vision-Language Model (VLM) is trained to predict these tokens directly. The loss function is the standard next-token prediction loss, computed as the cross-entropy 

between the predicted token distribution _z_ ˆ _q_<sup>_i_and the ground</sup> truth token _zq_<sup>_i_produced by the frozen Residual VQ-VAE:</sup> 


where _ot−h_ : _t_ represents the input observation sequence, and _Nq_ is the number of Residual VQ layers. 

To further enhance computational efficiency, similar to OpenVLA, the least-used tokens in the vocabulary are replaced during fine-tuning. However, this replacement process respects the layer-specific token ID ranges, ensuring that the tokenization remains consistent and interpretable across all layers. 

This integration of a pre-trained and frozen Residual VQ-VAE as the action tokenizer in VLA enables a more expressive and scalable representation of actions. By leveraging hierarchical quantization with non-overlapping token ID ranges, the model achieves better action representation, avoids semantic confusion between layers, and ensures stable loss convergence during training. Furthermore, by using the VQ-VAE tokens to represent longer action sequences instead of predicting one action at a time, the model significantly reduces the number of tokens required for training and inference. This mechanism allows the model to predict more complex behavior sequences with fewer steps, leading to a substantial improvement in inference speed and computational efficiency. 

## **4. Experiments** 

In our experiments, we first validate the effectiveness and scalability of the action tokenizer in VLA models using LIBERO simulator[29]. Subsequently, real-world experiments are conducted to further verify our hypothesis. We also investigate the impact of action tokenizers on the performance, inference speed, and long-horizon capabilities of VLA models, alongside ablation studies to evaluate key design choices. 

### **4.1. Simulation Experiments** 

#### **4.1.1. Experiment Setup** 

We utilize the LIBERO benchmark[29] to validate and evaluate the effectiveness and scalability of the action tokenizer, using the Franka Panda robot. Specifically, the entire LIBERO task suite—including LIBERO-Spatial, LIBEROObject, LIBERO-Goal, LIBERO-10, and LIBERO-90—is used as the entire LIBERO dataset. Among these, LIBERO90 comprises 90 short-horizon tasks, while the other task suites each contain 10 tasks, with 50 demonstrations per task. For evaluation, testing is conducted on LIBERO-goal, LIBERO-10 and LIBERO-90. 

Following the approach in OpenVLA[26], we filter out all ”no-op” actions from the dataset. To preliminarily validate 

11092 

the effectiveness of using VQ-VAE as an action tokenizer in VLA models and its scalability, we train two versions of a convolutional residual VQ-VAE. The first version VQM is trained solely on the Maniskill dataset[33], and the second VQM+R is trained on a mixture of Maniskill dataset and RLBench dataset[24]. Both models are trained on a single A100 GPU with a batch size of 1024, which takes about only 1 week. 

We use two pre-trained VQ-VAE models as frozen action tokenizers for OpenVLA: VQM and VQM+R . LoRA is then applied to fine-tune OpenVLA on the LIBERO-90 dataset. Additionally, we fine-tune the original OpenVLA model on the LIBERO-90 dataset using LoRA as a baseline for comparison.For a fair comparison, all fine-tuning on the LIBERO-90 task suite is conducted for 400K gradient steps with a batch size of 4, using 4 A100-80GB GPUs and an action chunk length of K=5. 

#### **4.1.2. Effectiveness of Conv Residual VQ-VAE** 

In the early stages of the experiment, we selected two task suites, LIBERO-10 and LIBERO-GOAL, to conduct preliminary scaling validation experiments. Specifically, we used two variants of Residual VQ-VAE models: one with a simple MLP as the encoder and decoder, and the other with a larger 2D temporal convolutional network as the encoder and decoder. The results are summarized in Tab. 1. The findings indicate that using temporal convolutional networks as the encoder and decoder in the Residual VQ-VAE significantly outperforms the MLP-based architecture in terms of success rate. These results suggest that temporal convolutional networks can serve as an effective action tokenizer, capable of capturing temporal dependencies more effectively. 

Furthermore, when we increased the training data for the VQ-VAE model, transitioning from data solely derived from individual LIBERO tasks to the entire LIBERO dataset, the success rate consistently improved. This observation provides preliminary evidence supporting the scalability of our action tokenizer design. 

|**Training Dataset of VQ**<br>|<br>**LIBERO-10 (%)**<br>**L**<br>|**IBERO-GOAL (%)**<br>|
|---|---|---|
|Original OpenVLA<br>-|51.0|**75.8**|
|ALL-LIBERO|53.4|72.6|
|MLP Residual VQ-VAE<br>LIBERO-10<br>LIBERO-GOAL|53.2<br>-|-<br>65.2|
|ALL-LIBERO|**60.0**|75.2|
|Conv Residual VQ-VAE<br>LIBERO-10|54.0|-|
|LIBERO-GOAL|-|72.4|


Table 1. **The evaluation results of residual VQ-VAE architectures.** The results demonstrate that the Conv Residual VQ-VAE outperforms the MLP-based version, particularly when trained on the full LIBERO dataset (ALL-LIBERO), highlighting its ability to better capture temporal dependencies and improve success rates. 

#### **4.1.3. Scaling Data Improves VQ-VAE Action Tokenizer Performance** 

In the experiment, to avoid potential performance inflation from in-domain data during evaluation on LIBERO-90, we trained the VQ-VAE Action Tokenizer on completely outof-domain ManiSkill and RLBench simulation data, rather than LIBERO data. Specifically, ManiSkill contains 30,000 action sequences, and RLBench includes 10,000 action sequences. we compare three models: the baseline, which fine-tunes the original OpenVLA; VQM, which uses a VQVAE trained on the Maniskill dataset as the action tokenizer for OpenVLA; and VQM+R, which uses a VQ-VAE trained on a mixture of the Maniskill and RLBench datasets as the action tokenizer for OpenVLA. 

On LIBERO-90, VQM+R achieved 80 _._ 98%, a 7 _._ 45% improvement over the OpenVLA baseline (73 _._ 53%), Tab. 2. Furthermore, an ablation study using only ManiSkill data for training VQM resulted in substantially lower performance, underscoring the critical role of sufficient synthetic data scale. 

||**baseline**(%|)<br>**VQM**(%|)<br>**VQM+R**(%)|
|---|---|---|---|
|**LIEBRO-90**|73.53|14.38|**80.98**|


Table 2. **Effectiveness of VQ-VAE Action Tokenizers in Scaling Simulation Data.** The results demonstrate VQM+R reached 80.98%, outperforming the OpenVLA baseline by 7.45% 

### **4.2. Real-Word Experiment** 

#### **4.2.1. Experiment Setup** 

Our robotic platform consists of a single Franka Research3 arm equipped with a third-person-view RealSense D435 camera mounted in a fixed position to capture environmental observations. The system operates at 20 Hz (moderately reduced from the native 100 Hz control frequency to balance training efficiency and motion continuity), with actions defined as absolute end-effector poses in SE(3) space (3D position + quaternion orientation). 

Our experimental benchmark comprises six manipulation tasks (4 short-horizon tasks, 2 long-horizon tasks) designed to evaluate the model’s ability to handle varying task complexities. For each task, we collect 50 demonstrations and evaluate performance over 20 trials: 

1) **Pull out a tissue paper** : The robot need to grasp and pull out a single tissue paper. 

2) **Pick up the [TOY NAME]** :The robot is required to pick up the specific toy, including the toy snake, the toy eggplant, and the toy chicken, resulting in a total of three tasks (with no other distractions). 

3) **Put the toy into the basket** : The robot need to pick up the toy(no other distractions) and put it into the basket. 

11093 


Figure 2. **All Evaluation environments** :We conduct comprehensive evaluations of VQ-VLA in both simulation and real-world settings. In simulation, evaluations are performed on the LIBERO90 benchmark within the LIBERO dataset. And six diverse tasks are designed for real-world testing. 

4) **Flip the pot upright** : We set a flipped pot on the platform, the robot need to flip and upright a fallen cooking pot. 

5) **Put all cups into the basket** : We place two different cups on the table and set a few other things(toys) as distractions. The robot need to sequentially put two cups into the basket, testing long-horizon task. 

6) **Put the toy into the drawer** : We place a toy on the table and set a few other things as distractions. The robot need to sequentially open the drawer,pick up the specific toy and put it into the drawer, and close the drawer, testing long-horizon task. 

We finetune each task separately for 100K gradient steps (batch size 4 across 4 A100-80GB GPUs) with action chunk length K=5. During deployment. 

#### **4.2.2. Performance on Short-Horizon Tasks** 

Based on the in the simulation experiments, we further incorporated 120k synthetic trajectories from the ManiSkill dataset, co-training VQO+L+M with Open X-Embodiment dataset and LIBERO dataset to evaluate the scaling capability of our action tokenizer. We evaluated the performance of the action tokenizer trained with different datasets on four carefully designed short-horizon tasks, focusing on multi-task learning, precision manipulation, and dynamic adjustment capabilities. The results are shown in Fig. 3. 

It can be observed that when synthetic trajectories are added for co-training, the performance of the action tokenizer improves significantly. The average success rate increased from the baseline of 23% to 46.25%, with a notable improvement of 30% in the ”Flip the pot upright” task. In the ”Pull out a tissue paper” task, which tests the robot’s performance in high-precision dynamic operations (as this task requires continuous, fine-grained grasping and pulling motions), the baseline model achieved only a 5% success rate, failing almost entirely. In contrast, models incorporating VQ achieved success rates of 20% or higher. 

Furthermore, comparing VQO+L with VQO, the average success rate on short-horizon tasks increased by only 0.5%. This may be attributed to the limited size of the LIBERO dataset, which has minimal impact on short-horizon tasks. However, the ManiSkill dataset is 50 times larger than LIBERO, leading to a significant improvement in success rates when used for training. 

#### **4.2.3. Performance on Long-Horizon Tasks** 

VQ-VLA demonstrates outstanding performance on longhorizon tasks (”Put all cups in the basket” and ”Put the toy into the drawer”), significantly outperforming baseline model in both success rate and efficiency. In scenarios where baseline models achieve success rates as low as 15% or nearly 0, the VQ _O_ + _L_ + _M_ model achieves significantly higher success rates of 50% and 30%, respectively (see Fig.3). For the ”Put the toy into the drawer” task, a representative longhorizon scenario, the baseline model was only able to complete the first step of opening the drawer in 15 out of 20 trials, failing to proceed further in most cases. In contrast, the VQ _O_ + _L_ + _M_ model successfully opened the drawer in all test cases, demonstrating its robustness and reliability in handling complex sequential tasks. 

A key advantage of VQ-VLA in long-horizon tasks lies in its use of VQ-VAE as an action tokenizer, which enables the model to predict multiple actions in a single inference step. This design reduces the accumulation of errors over extended task sequences, making VQ-VLA particularly advantageous for tasks requiring long-term planning and execution. Additionally, in scenarios involving the consecutive execution of multiple subtasks, VQ-VLA not only achieves higher success rates but also significantly reduces task completion time 

11094 


Figure 3. **Real-world experimental results:** We compare the performance of Baseline, VQO, VQO+L, and VQO+L+M on both short-horizon and long-horizon tasks. In terms of the average success rate, all VQ-based models outperform the Baseline. The best-performing model, VQO+L+M, achieves a success rate that is 23.25% higher than the Baseline on both short-horizon and long-horizon tasks. Additionally, the results show that VQO+L+M outperforms VQO+L, which in turn outperforms VQO, indicating the effectiveness of incorporating synthetic data during training without compromising real-world performance. 

compared to baseline models, highlighting its superior execution efficiency and ability to handle long-horizon challenges effectively. 

#### **4.2.4. Sim&Real Domain Gap Analysis** 

To quantify the domain gap between synthetic data and realworld data, we trained a VQ-VAE model exclusively on the LIBERO dataset, referred to as VQL, for OpenVLA. The model was tested in three real-world tasks (one long-horizon and two short-horizon tasks), and the results are shown in Tab. 3. The results indicate that the performance of VQL is comparable to that of both VQO+L and VQO, suggesting that the domain gap between synthetic and real-world data is minimal. 

Although real-world data may contain noise, the inclusion of Open X-Embodiment data as a real-world dataset expands the data sources and enriches the diversity of data types, which effectively enhances the model’s generalization and robustness. 

#### **4.2.5. Inference Speed Comparison** 

During the real-world experiments, we measured the action execution frequency of VQ-VLA and compared it with the original OpenVLA. The results are summarized in Tab. 4. As shown in the table, with a compression ratio of 5 in VQVAE, the inference speed is nearly tripled. This significant improvement greatly facilitates real-time performance in practical applications. 

||**Put the toy**<br>**into the drawer (%)**|**Flip the pot**<br>**upright (%)**|**Put the toy**<br>**into the basket (%)**|
|---|---|---|---|
|**baseline**|5.0|30.0|20.0|
|**VQO**|15.0|45.0|35.0|
|**VQL**|10.0|55.0|35.0|
|**VQO+L**|10.0|45.0|35.0|
|**VQO+L+M**|**25.0**|**60.0**|**45.0**|


Table 3. **Performance Comparison Across Real-World Tasks:** We observe that the performance of VQL is comparable to that of both VQO+L and VQO, indicating that the domain gap between synthetic and real-world data is minimal. 

||Frequency (Hz)|
|---|---|
|VQ-VLA|**11.84**|
|OpenVLA|4.16|


Table 4. **The Results of Frequencies.** We report the comparison results of our VQ-VLA and baseline OpenVLA. 

### **4.3. Ablation Studies** 

In this section, we report some ablation studies to show the effectiveness of the design choices of our method. 

#### **4.3.1. Action Chunking via VQ-VAE and Autoregressive Output** 

The original OpenVLA model generates a single action per inference step based solely on the current observation, resulting in a step-by-step execution approach. To improve efficiency and handle longer action sequences, we extend 

11095 

OpenVLA to output a sequence of five actions in an autoregressive manner, similar to the action chunking mechanism in VQ-VLA. Specifically, the model predicts the next action based on the current observation and previously generated actions, allowing it to generate a sequence of actions in a single inference step. This autoregressive approach serves as an alternative action chunking strategy by grouping multiple actions for execution. 

To evaluate the effectiveness of different action chunking strategies, we design ablation experiments comparing the autoregressive output of OpenVLA to the VQ-based action chunking method in VQ-VLA. The results, shown in Tab. 5, indicate that the use of the autoregressive approach for action chunking in the original OpenVLA leads to a significant drop in success rate compared to the baseline. In real-world experiments, when using the autoregressive approach as a form of action chunking, the spatial magnitude of each action chunk is relatively small, resulting in slower overall execution of actions. Compared to the Action Chunking via VQ-VAE method, even with the same action chunk size, the time required to reach the same target location is significantly longer. Additionally, this approach tends to exhibit shortcut learning, where the model directly copies previous actions within the same action chunk. By analyzing the output values of each action chunk, it is observed that multiple actions within a single chunk have remarkably similar values, indicating a lack of diversity in the predicted actions. 

Overall, Action Chunking via VQ-VAE not only improves inference speed but also enhances the performance of VLA by generating more effective and diverse action sequences. This makes it a more suitable approach for addressing realworld long-horizon tasks. 

|**Action Chunking**|**LIBERO-90 (%)**|**Flip the pot**<br>**upright (%)**|**Put the toy**<br>**into the basket (%)**|
|---|---|---|---|
|**baseline**|74.76|30.0|20.0|
|**Autoregressive Output**|66.53|10.0|0.0|
|**VQ-based (VQO+L+M)**|**86.61**|**60.0**|**45.0**|


Table 5. **Comparison of action chunking methods:** We evaluate the performance on three tasks (one simulator task and two realworld tasks). The results show that the Autoregressive Output used in OpenVLA performs poorly as an action chunking method, with a significant gap compared to the VQ-based approach. This indicates that the VQ-based method is more effective. 

#### **4.3.2. Embedding Integration Effectiveness** 

To evaluate the impact of embeddings, we conducted an ablation study comparing the model’s performance with and without embeddings. Specifically, the baseline model processes raw action sequences directly, while the enhanced model incorporates both time embedding and action-type embedding. 

As shown in Tab. 6, the model with embeddings significantly outperforms the baseline in terms of success rate. This 

demonstrates that the integration of embeddings improves the encoder’s ability to represent structured action sequences, leading to better overall performance. 

||**LIBERO-90 (%)**|<br>**Flip the pot**<br>**upright (%)**<br>|**Put the toy**<br>**into the basket (%)**|
|---|---|---|---|
|**VQO+L (w.o. Embeddings)**|85.17|40.0|35.0|
|**VQO+L (w Embeddings)**|**86.16**|**45.0**|**35.0**|


Table 6. **Embedding integration improves performance.** The table compares models with and without embeddings across three tasks, showing that embeddings enhance success rates, especially for ”Flip the pot upright.” 

## **5. Limitations and Future Works** 

In our work, a series of extensive experiments demonstrate that our proposed action tokenizers can improve VLA performance and inference speed while achieving scalability on simulated data. Despite these promising results, there still remain some limitations and opportunities for future work. First, our action tokenizers can be further extended to larger-scale simulated datasets. Second, our work improves inference speed by decoding multi-step action sequences, which can be further combined with techniques such as distillation [38] and quantization [16] of VLMs in the future. Fially, the architecture design of our action tokenizers can be further improved, for example, by incorporating the frequency of action data as a extra condition. In summary, we hope that our work can serve as a strong baseline and inspire future research. 

## **6. Conclusions** 

In this paper, we propose a general convolutional residual VQ-VAE framework for action tokenizers that can seamlessly integrate with state-of-the-art VLA models. Our VQVAE is trained on 100 times more data than previous methods and can be directly transferred to downstream both realworld and simulated robotic manipulation tasks. Extensive experiments conducted in both simulated and real-world environments validate that the proposed convolutional residual VQ-VAE framework not only enhances the performance of VLA policies but also accelerates inference. Finally, our VQ-VAE also demonstrates the ability to scale effectively with large-scale simulated data. 

## **Acknowledgments** 

This work is supported by the National Key R&D Program of China (NO.2022ZD0160102) and Shanghai Artificial Intelligence Laboratory. 

11096 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 1 

- [2] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 2 

- [3] Jean-Baptiste Alayrac, Jeffrey Donahue, Pauline Luc, Alexis Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, et al. Flamingo: A visual language model for few-shot learning. _Advances in Neural Information Processing Systems (NeurIPS)_ , 35:23716–23736, 2022. 2 

- [4] Arthur Allshire, Roberto Mart´ın-Mart´ın, Charles Lin, Shawn Manuel, Silvio Savarese, and Animesh Garg. Laser: Learning a latent action space for efficient reinforcement learning. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6650–6656, 2021. 2 

- [5] Suneel Belkhale and Dorsa Sadigh. Minivla: A better vla with a smaller footprint. _https://ai.stanford.edu/blog/minivla/_ , 2024. 1, 2, 3 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 2 

- [7] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 1, 2 

- [9] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 2 

- [10] Wei Chen, Yifeng Zhang, Hao Li, Xufeng Wang, and Ming Liu. Anyvlm: Unified vision-language model for any robot morphology. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1–8. IEEE, 2024. 2 

- [11] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023. 2 

- [12] Xiaoyu Chen, Junliang Guo, Tianyu He, Chuheng Zhang, Pushi Zhang, Derek Cathera Yang, Li Zhao, and Jiang Bian. Igor: Image-goal representations are the atomic control 

units for foundation models in embodied ai. _arXiv preprint arXiv:2411.00785_ , 2024. 2 

- [13] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 2 

- [14] Norman Di Palo and Edward Johns. Keypoint action tokens enable in-context imitation learning in robotics. _arXiv preprint arXiv:2403.19578_ , 2024. 2 

- [15] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: an embodied multimodal language model. In _Proceedings of the 40th International Conference on Machine Learning_ , pages 8469– 8488, 2023. 2 

- [16] Kazuki Egashira, Mark Vero, Robin Staab, Jingxuan He, and Martin Vechev. Exploiting llm quantization. _Advances in Neural Information Processing Systems_ , 37:41709–41732, 2025. 8 

- [17] Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 12873–12883, 2021. 1, 2 

- [18] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. _arXiv preprint arXiv:2307.00595_ , 2023. 2 

- [19] Philip Gage. A new algorithm for data compression. _The C Users Journal_ , 12(2):23–38, 1994. 2 

- [20] Theophile Gervet, Zhou Xian, Nikolaos Gkanatsios, and Katerina Fragkiadaki. Act3d: 3d feature field transformers for multi-task robotic manipulation. In _7th Annual Conference on Robot Learning_ . 2 

- [21] Abhishek Gupta, Vikash Kumar, Corey Lynch, Sergey Levine, and Karol Hausman. Relay policy learning: Solving longhorizon tasks via imitation and reinforcement learning. _arXiv preprint arXiv:1910.11956_ , 2019. 2 

- [22] Matthew Hausknecht and Peter Stone. Deep reinforcement learning in parameterized action space. _arXiv preprint arXiv:1511.04143_ , 2015. 2 

- [23] Wenyi Hong, Ming Ding, Wendi Zheng, Xinghan Liu, and Jie Tang. Cogvideo: Large-scale pretraining for text-to-video generation via transformers. _arXiv preprint arXiv:2205.15868_ , 2022. 1 

- [24] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 5 

- [25] Yang Jin, Zhicheng Sun, Ningyuan Li, Kun Xu, Hao Jiang, Nan Zhuang, Quzhe Huang, Yang Song, Yadong Mu, and Zhouchen Lin. Pyramidal flow matching for efficient video generative modeling. _arXiv preprint arXiv:2410.05954_ , 2024. 3 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An 

11097 

open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 4 

- [27] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 2 

- [28] Seungjae Lee, Yibin Wang, Haritheja Etukuru, H Jin Kim, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. Behavior generation with latent actions. _arXiv preprint arXiv:2403.03181_ , 2024. 1, 2, 3 

- [29] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 1, 2, 3, 4 

- [30] Zhuoyan Luo, Fengyuan Shi, Yixiao Ge, Yujiu Yang, Limin Wang, and Ying Shan. Open-magvit2: An open-source project toward democratizing auto-regressive visual generation. _arXiv preprint arXiv:2409.04410_ , 2024. 2 

- [31] Ben Mann, N Ryder, M Subbiah, J Kaplan, P Dhariwal, A Neelakantan, P Shyam, G Sastry, A Askell, S Agarwal, et al. Language models are few-shot learners. _arXiv preprint arXiv:2005.14165_ , 1:3, 2020. 1 

- [32] Atharva Mete, Haotian Xue, Albert Wilcox, Yongxin Chen, and Animesh Garg. Quest: Self-supervised skill abstractions for learning continuous control. _Advances in Neural Information Processing Systems_ , 37:4062–4089, 2025. 2, 12 

- [33] Tongzhou Mu, Zhan Ling, Fanbo Xiang, Derek Yang, Xuanlin Li, Stone Tao, Zhiao Huang, Zhiwei Jia, and Hao Su. Maniskill: Generalizable manipulation skill benchmark with large-scale demonstrations. _arXiv preprint arXiv:2107.14483_ , 2021. 1, 3, 5 

- [34] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 1, 2, 3 

- [35] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 1, 2, 12 

- [36] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language models are unsupervised multitask learners. _OpenAI blog_ , 1(8):9, 2019. 2 

- [37] Fengyuan Shi, Zhuoyan Luo, Yixiao Ge, Yujiu Yang, Ying Shan, and Limin Wang. Taming scalable visual tokenizer for autoregressive image generation. _arXiv preprint arXiv:2412.02692_ , 2024. 2 

- [38] Sharath Turuvekere Sreenivas, Saurav Muralidharan, Raviraj Joshi, Marcin Chochowski, Ameya Sunil Mahabaleshwarkar, Gerald Shen, Jiaqi Zeng, Zijia Chen, Yoshi Suhara, Shizhe Diao, et al. Llm pruning and distillation in practice: The minitron approach. _arXiv preprint arXiv:2408.11796_ , 2024. 

8 

- [39] Peize Sun, Yi Jiang, Shoufa Chen, Shilong Zhang, Bingyue Peng, Ping Luo, and Zehuan Yuan. Autoregressive model 

beats diffusion: Llama for scalable image generation. _arXiv preprint arXiv:2406.06525_ , 2024. 1, 2 

- [40] Andrew Szot, Bogdan Mazoure, Harsh Agrawal, R Devon Hjelm, Zsolt Kira, and Alexander Toshev. Grounding multimodal large language models in actions. _Advances in Neural Information Processing Systems_ , 37:20198–20224, 2024. 2 

- [41] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2 

- [42] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 2 

- [43] Sai H Vemprala, Rogerio Bonatti, Arthur Bucker, and Ashish Kapoor. Chatgpt for robotics: Design principles and model abilities. _Ieee Access_ , 2024. 2 

- [44] Chuan Wen, Xingyu Lin, John So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ , 2023. 2 

- [45] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 2 

- [46] Jiange Yang, Wenhui Tan, Chuhao Jin, Keling Yao, Bei Liu, Jianlong Fu, Ruihua Song, Gangshan Wu, and Limin Wang. Transferring foundation models for generalizable robotic manipulation. _arXiv preprint arXiv:2306.05716_ , 2023. 2 

- [47] Jiange Yang, Bei Liu, Jianlong Fu, Bocheng Pan, Gangshan Wu, and Limin Wang. Spatiotemporal predictive pre-training for robotic motor control. _arXiv preprint arXiv:2403.05304_ , 2024. 2 

- [48] Jiange Yang, Haoyi Zhu, Yating Wang, Gangshan Wu, Tong He, and Limin Wang. Tra-moe: Learning trajectory prediction model from multiple domains for adaptive policy conditioning. _arXiv preprint arXiv:2411.14519_ , 2024. 2 

- [49] Jiange Yang, Yansong Shi, Haoyi Zhu, Mingyu Liu, Kaijing Ma, Yating Wang, Gangshan Wu, Tong He, and Limin Wang. Como: Learning continuous latent motion from internet videos for scalable robot learning. _arXiv preprint arXiv:2505.17006_ , 2025. 2 

- [50] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 2 

- [51] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 2 

- [52] Neil Zeghidour, Alejandro Luebs, Ahmed Omran, Jan Skoglund, and Marco Tagliasacchi. Soundstream: An end-toend neural audio codec. _IEEE/ACM Transactions on Audio, Speech, and Language Processing_ , 30:495–507, 2021. 1, 3 

- [53] Canyu Zhao, Mingyu Liu, Wen Wang, Weihua Chen, Fan Wang, Hao Chen, Bo Zhang, and Chunhua Shen. Moviedreamer: Hierarchical generation for coherent long visual sequence. _arXiv preprint arXiv:2407.16655_ , 2024. 2 

11098 

- [54] Canyu Zhao, Mingyu Liu, Huanyi Zheng, Muzhi Zhu, Zhiyue Zhao, Hao Chen, Tong He, and Chunhua Shen. Diception: A generalist diffusion model for visual perceptual tasks. _arXiv preprint arXiv:2502.17157_ , 2025. 2 

- [55] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with lowcost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 2 

- [56] Wei Zhao, Pengxiang Ding, Min Zhang, Zhefei Gong, Shuanghao Bai, Han Zhao, and Donglin Wang. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. _arXiv preprint arXiv:2502.13508_ , 2025. 2 

- [57] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 2 

- [58] Jinliang Zheng, Jianxiong Li, Dongxiu Liu, Yinan Zheng, Zhihao Wang, Zhonghong Ou, Yu Liu, Jingjing Liu, Ya-Qin Zhang, and Xianyuan Zhan. Universal actions for enhanced embodied foundation models, 2025. 2, 13 

- [59] Wenxuan Zhou, Sujay Bajracharya, and David Held. Plas: Latent action space for offline reinforcement learning, 2020. 2 

- [60] Haoyi Zhu, Yating Wang, Di Huang, Weicai Ye, Wanli Ouyang, and Tong He. Point cloud matters: Rethinking the impact of different observation spaces on robot learning. _Advances in Neural Information Processing Systems_ , 37: 77799–77830, 2024. 2 

- [61] Haoyi Zhu, Honghui Yang, Yating Wang, Jiange Yang, Limin Wang, and Tong He. Spa: 3d spatial-awareness enables effective embodied representation. _arXiv preprint arXiv:2410.08208_ , 2024. 2 

11099 

