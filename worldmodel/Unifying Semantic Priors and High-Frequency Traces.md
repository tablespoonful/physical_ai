---
title: "Unifying Semantic Priors and High-Frequency Traces: Enhancing V-JEPA with Mixture-of-Experts for Robust Synthetic Image Forensics"
date: "2026-09-15"
authors: "Simone Teglia; Irene Amerini"
url: https://arxiv.org/abs/2609.16778
pdf: https://arxiv.org/pdf/2609.16778
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.16778)** / [論文ページ](https://arxiv.org/abs/2609.16778)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Unifying Semantic Priors and High-Frequency Traces: Enhancing V-JEPA with Mixture-of-Experts for Robust Synthetic Image Forensics** 

**Simone Teglia, Irene Amerini** Sapienza University of Rome 

_{teglia, amerini}@diag.uniroma1.it_ 

## **Abstract** 

_The unchecked proliferation of manipulated images on social media platforms has increased the spread of misinformation, posing a severe threat to public trust and information integrity. Modern deepfake detectors typically rely on Vision Transformers (ViTs) to capture the low-level inconsistencies that characterize fully synthetic or locally tampered images. However, the global understanding of such foundation models is not enough to discriminate alone between real and fake multimedia content, especially in challenging scenarios where images are compressed or transmitted through social media. In this paper we pioneer the application of Joint-Embedding Predictive Architecture (JEPA) models to deepfake detection, taking advantage of the generalized representation of visual reality that such World Models have exhibited. We hypothesize, and empirically demonstrate, that the intrinsic world understanding of JEPA models can be used as a strong prior for a deepfake detector. To fully exploit JEPA capabilities, we propose MoE-JEPA, a dual-stream architecture for deepfake detection. By enhancing a V-JEPA 2 backbone with a Residual Mixture-of-Experts (MoE) mechanism, along with a noise stream branch, our model dynamically internalizes forensic knowledge. Furthermore, a Gated Attention Multiple Instance Learning (MIL) module is employed to ensure precise spatial semantic understanding. Evaluated on the SIDSet benchmark, comprising 300K AI-generated, tampered and authentic images, MoE-JEPA establishes a new stateof-the-art with an accuracy of 95.54%, successfully outperforming vastly larger models._ 

## **1. Introduction** 

With the rapid advancements of Generative Artificial Intelligence, the creation of artificial multimedia content has witnessed explosive growth. State-of-the-art models like DALL-E 3 [9], FLUX [25] and Nano Banana Pro [34], have 

democratized the access to such powerful tools, making the generation of highly realistic images, commonly known as deepfakes, no longer a research novelty, but an everyday technology. However, the same technological progress that enables creative expression and productivity gains, also introduces profound societal risks. Alongside these technological breakthroughs, society has witnessed an unprecedented wave of digital disinformation propagating across social media platforms [3, 14, 31]. Synthetic multimedia content is regularly weaponized to manipulate public perception, posing a severe threat to public trust, democratic processes, and overall information integrity. Fabricated images depicting sensitive geopolitical conflicts, such as those in Ukraine or Gaza, can rapidly go viral on social media, potentially altering narrative and concretely influencing people’s beliefs, driving real-world actions [13]. These concerns have intensified research efforts in multimedia forensics, prompting the release of massive deepfake datasets and the development of increasingly powerful detection architectures. Modern detectors, often built upon large-scale vision backbones, aim to discern authentic images from AIgenerated or manipulated ones by learning discriminative artifacts introduced during the generation process. In particular, foundation Vision Transformers (ViTs) [16] have emerged as powerful general-purpose feature extractors, achieving remarkable performance across a wide range of visual recognition tasks. By modeling long-range dependencies through self-attention, ViTs primarily learn global semantic representations of the image. While this property is advantageous for high-level understanding, it may limit their ability to capture fine-grained, localized inconsistencies that are critical in forensic analysis. When applied to the field of deepfake detection, such models can effectively capture global generative patterns that characterize fully synthetic images, but their strong semantic abstraction often suppresses subtle forensic cues that fine-grained detectors rely upon [38]. At the same time, recent progress in selfsupervised learning have further improved the transformerbased backbones. In particular Joint-Embedding Predictive 

Architecture (JEPA) [26] models propose a new learning paradigm that involves the encoder to learn to anticipate the representation of masked regions of the images in the latent space, rather than the actual raw pixels. Architectures of this kind serve as a foundational component for building World Models, as their predictive module aims to capture the underlying semantic structure and constraints of the visual world. We hypothesize that this learned generalized understanding of images can act as a fundamental prior to capture the synthetic inconsistencies of AI-generated imagery. To harness this capability, we introduce MoE-JEPA (see Figure 1), a dual-stream architecture for deepfake detection based on the World Model V-JEPA 2 [6], a selfsupervised vision model that excel at both video and image tasks. Specifically, we employ the V-JEPA 2 backbone to exploit its robust visual representations, and augment its capabilities by injecting into the latest layers a Residual Mixture-of-Experts (MoE) mechanism, allowing the architecture to internalize forensic features the backbone was not trained to extract. Furthermore, to prevent the semantic dilution caused by global pooling that can influence the correct detection of localized forgeries, MoE-JEPA implements a Gated Attention Multiple Instance Learning (MIL) module to ensure precise, unsupervised spatial routing to manipulated regions. Furthermore, we extend the architecture with a low-level noise branch, enabling a richer understanding of the image and making the detection more robust, especially against the aggressive degradations introduced by social media sharing, resizing, and transmission. By explicitly capturing localized generative and sensor artifacts, this parallel noise stream compensates for the semantic abstraction of the foundation model, providing a resilient defense against in-the-wild media degradation. 

In summary, our main contributions are: 

- To the best of our knowledge, we are the first to pioneer the usage of JEPA World Models for deepfake detection. We empirically demonstrate that the intrinsic understanding of physical and structural visual reality learned by these models naturally captures generative inconsistencies. 

- We propose **MoE-JEPA** , a deepfake detector combining a semantic branch with a noise branch. By integrating a Residual Mixture-of-Experts (MoE) and a Gated Attention Multiple Instance Learning (MIL) module, the architecture dynamically internalizes forensic traces and mitigates background semantic dilution without catastrophic forgetting of the foundation model’s pre-trained knowledge. 

- We design a robust dual-stream framework with an Adaptive Gated Fusion technique. We demonstrate that while V-JEPA 2 excel at global contextual verification, coupling them with a constrained BayarConv noise branch is critical for isolating semantically coherent, microscopic local 

manipulations. 

- MoE-JEPA achieves a new state-of-the-art on the SID-Set benchmark, with a **95.54%** overall accuracy. Tested on the RRDataset, it achieves the second best accuracy overall and the best accuracy on re-digitalized real images. 

## **2. Related Work** 

### **2.1. Deepfake Detection** 

In recent years, the emergence of powerful generative artificial intelligence models like GANs [19] and Diffusion Models [20] has called for the development of reliable and effective deepfake detectors. Early deepfake detection methods primarily relied on Convolutional Neural Networks (CNNs) to expose spatial artifacts, blending boundaries, and frequency-domain inconsistencies. [2, 28, 33, 42] As generative models advanced, researcher started to adopt foundation Vision Transformers (ViTs) [16] as base model for their architectures [15, 35, 41, 44]. Latest approaches leverage more complex architectures to extract image embeddings, like Large Vision Language Models [21] or Q- Former [27]. These approaches take advantage of the global context understanding to achieve superior face forgery detection performance. However, these large models introduce prohibitive computational costs, making real-time inference for social media filtering impractical. To overcome these deployment hurdles we explore the usage of the JointEmbedding Predictive Architecture as vision encoder, comprising only of 0.3B parameters, providing a remarkable lightweight and efficient foundation model. 

### **2.2. Mixture of Experts** 

Mixture-of-Experts (MoE) [22] aim to increase the model capacity without affecting the computational demand, by dynamically routing input tokens to a specialized subset of feed-forward sub-networks (experts). To drastically scale up the model capacity, without affecting the inference costs, Shazeer et al. [32] proposed the sparsely-gated Mixtureof-Experts, that select only the _top-k_ most relevant experts for each given token. This allows the overall parameter count of the architecture to scale significantly, while the computational complexity remains equivalent to a much smaller dense model. Moreover, to protect the foundation model’s universal knowledge, the Residual Mixtureof-Experts [39] paradigm introduced a set of frozen shared experts, responsible to maintain the pretrained knowledge of the model, alongside a dynamically routed trainable experts. This allows for a more stable training, enabling the specialization of routed experts without losing the core semantic understanding of the model. While traditional MoEs utilize a Softmax routing function, recent advancements like DeepSeekMoE [29] have demonstrated that Normalized Sigmoid Gating prevents the possible routing collapse. 

In the field of multimedia forensics, works like MoE-FFD [24] and Forensic-MoE [17] have successfully utilized expert modules to extract generalized face forgery clues and aggregate diverse synthetic traces from multiple generators. 

### **2.3. Joint-Embedding Predictive Architectures** 

The Joint-Embedding Predictive Architecture (JEPA), originally proposed by LeCun as a foundational step toward Autonomous Machine Intelligence [26], represents a paradigm shift in self-supervised representation learning world. Unlike traditional generative approaches which attempt to reconstruct missing patches at the exact pixel or token level, JEPA models operate entirely within an abstract latent space, by predicting the representation of missing parts of the inputs. Extending the base capabilities of JEPA models, I-JEPA [5] and V-JEPA [7] demonstrated that this abstract prediction strategy yields highly scalable and semantically rich representations even for images and videos respectively, by predicting latent visual features rather than raw pixels. Building upon this foundation, V-JEPA 2 [6] extends the V-JEPA framework, successfully obtaining a new state-of-the-art for vision JEPA models. Because JEPA models are explicitly trained to understand the underlying physical rules, motion dynamics, and structural consistencies of visual reality, we hypothesize that their latent spaces inherently capture the anomalous and physically inconsistent nature of synthetic media. 

## **3. Methodology** 

We propose MoE-JEPA, a deepfake detection architecture that leverages the natural vision understanding of the World Model V-JEPA 2. By combining a semantic branch, devoted to extracting high-level structural anomalies and profound physical inconsistencies from the latent space, and a noise branch, responsible for isolating microscopic, highfrequency generative traces, our architecture is able to evaluate the image in its entirety, comprehending both high and low-level information at the same time. 

### **3.1. The Semantic Branch** 

#### **3.1.1. Pre-trained Vision Backbone** 

Given an input image _I ∈_ R<sup>_H×W ×C_</sup> , we first adapt the input for the temporal requirement of V-JEPA by duplicating the frame to simulate a video stream across a synthetic temporal dimension _T_ . Then we process it through a frozen V-JEPA Encoder model _E_ , which outputs a sequence of unpooled spatial patch tokens: 


where _N_ is the number of spatial patches and _D_ is the embedding dimension. The first layers of the Vision Encoder 

_E_ are kept frozen to prevent catastrophic forgetting of general visual representations and to preserve its large-scale pretraining knowledge. 

#### **3.1.2. Residual Mixture-of-Experts** 

Rather than completely relying on the generalized visual understanding of the pre-trained backbone, which is inherently optimized for semantic invariance rather than forensic sensitivity, we intervene in the latest transformer blocks to increase adaptability to forensic cues. Specifically we replace the last Multi Layer Perceptron (MLP) of the latest encoder blocks of the vision backbone with a Residual Mixture-of-Experts (MoE) module. Concretely, each MoE layer consists of a set of _M_ trainable experts _{E_ 1 _, E_ 2 _, . . . , EM }_ , together with a single fully frozen shared expert _E_ shared, following a Residual Mixture-ofExperts formulation. The shared expert remains always active and provides a stable semantic pathway, while the trainable experts are dynamically routed to model input-specific variations. To control the routing dynamic we adopt a Normalized Sigmoid Gating mechanism, following recent studies [29] that prove that this kind of routing allows for a more uniform saturation across layers than the softmax-gated alternative, promoting a more balanced expert utilization and faster router stabilization. 

Formally, let _zi ∈_ R<sup>_D_</sup> denote a spatial patch token. A learnable router network parameterized by a weight matrix _WR ∈_ R<sup>_D×M_</sup> first computes raw affinity logits for all trainable experts _s_ ( _zi_ ) = _WRzi_ . Let then _Tk_ ( _zi_ ) denote the selected subset of the Top- _k_ most relevant experts, and let _gm_ ( _zi_ ) represent their corresponding normalized sigmoid gating weights. The final adapted token _zi_<sup>out</sup> is computed as the sum of the deterministic shared expert representation and the dynamically routed trainable experts: 


To encourage diversity among experts and avoid degenerate specialization, we perturb the weights of the trainable experts at initialization by injecting small stochastic noise. This controlled perturbation promotes heterogeneous adaptation trajectories, enabling the model to better capture diverse input distributions. To prevent routing collapse and ensure that all the trainable experts are equally utilized, we employ an auxiliary load balancing loss _Lbal_ . Given a batch of _B_ tokens and _M_ trainable experts, we first compute the routing density _dm_ for each expert _m_ as the mean routing probability across all tokens: 


where _pi,m_ represents the routing probability of token _i_ to expert _m_ . The load balancing loss is then computed as the 


Figure 1. Overview of the MoE-JEPA architecture. The semantic branch (top) uses a V-JEPA 2 backbone, a MoE module, and a Gated Attention MIL module to semantically suppress pristine backgrounds and isolate localized tampering ( _H_ semantic). In parallel, the noise branch (bottom) applies a constrained BayarConv layer to extract high-frequency generative and sensor artifacts ( _H_ noise). These complementary features are joined using an Adaptive Gated Multimodal Fusion module and classified via an MLP head. 

scaled sum of the squared densities: 


The total optimization objective of the network is thus _Ltotal_ = _LCE_ + _λbalLbal_ , where _LCE_ is the primary CrossEntropy loss and _λbal_ is the balancing coefficient. 

#### **3.1.3. Gated Attention MIL Pooling** 

Finally, to isolate the tampered regions and mitigate semantic dilution, we apply a Gated Attention Multiple Instance Learning (MIL) module over the adapted tokens. This module acts as a spatial circuit breaker, dynamically learning to assign near-zero attention weights to pristine background patches, making the model attend more easily to synthetically forged patches. The attention score _ai_ for each adapted patch token _zi_<sup>out</sup> is computed via a dual-branch network: 


with _V_ and _U_ as learnable projection matrices that map the token into a forensic feature space and a relevance gate, respectively. The tanh activation models complex feature interactions, while the Sigmoid gate _σ_ explicitly masks out irrelevant semantic content via element-wise multiplication ( _⊙_ ). The final localized semantic representation _Hsemantic_ is the attention-weighted sum of the tokens: 


### **3.2. The Noise Branch** 

While the semantic branch demonstrates strong capabilities in isolating spatial and contextual anomalies, relying exclusively on high-level semantic features can limit the model robustness. For example, many sophisticated forgeries are designed to be semantically coherent: manipulated regions may exhibit perfectly blended boundaries, consistent lighting, and plausible object structure. Moreover, common post-processing steps, such as resizing, recompression, and platform-specific social media pipelines, can attenuate the semantic inconsistencies that detectors often rely on. To enhance the overall architecture robustness and enable a more comprehensive understanding of the forgeries, we introduce a parallel noise branch. Rather than processing the latent patch tokens, this branch operates directly on the raw input image _I ∈_ R<sup>_H×W ×C_</sup> to extract a purely high-frequency residual map. 

To extract the noise residuals we employ a constrained convolutional layer, commonly known as BayarConv [8]. This layer exploits a learnable convolutional kernel _W ∈_ R<sup>_K×K_</sup> that is forced to predict the center pixel value, based only on its neighborhood pixels. This suppresses dominant semantic structures, effectively filtering out the image semantic and revealing the subtle high-frequency noise patterns beneath. The resulting residual map _R_ is subsequently processed through a lightweight stack of standard convolutional blocks. These blocks serve to hierarchically pool the localized high-frequency discrepancies into a dense, abstract frequency fingerprint _H_ noise _∈_ R<sup>_d_</sup> . 

By fusing this frequency-based fingerprint with the spa- 

tially localized semantic representation, the architecture achieves a comprehensive, disentangled view of the image: the semantic branch evaluates contextual integrity and semantic coherence, while the noise branch provides a more robust verification of physical and generative consistency. Together, they provide a more comprehensive understanding of the image, improving the detection of both fully synthetic images and carefully crafted local manipulations. 

#### **3.2.1. Adaptive Gated Multimodal Fusion and Classification** 

Rather than just relying on a simple concatenation strategy, we employ an Adaptive Gated Residual Fusion mechanism. After processing the image _I_ through the semantic branch and the noise branch, to dynamically regulate the contribution of the the two vectors _H_ semantic _∈_ R<sup>_D_</sup> and _H_ noise _∈_ R<sup>_d_</sup> , we compute a modulating gate vector _α_ . This is achieved by concatenating the normalized representations and passing them through a learnable dense projection followed by a Sigmoid activation: 


where _⊕_ denotes concatenation. 

Finally the multimodal representation is constructed by applying the learned gate _α_ via element-wise multiplication ( _⊙_ ) to the noise embedding, which is then added to the semantic embedding: 


This gated formulation allows the network to autonomously decide when to rely purely on spatial anomalies and when to inject microscopic generative noise. Later _H_ fused is fed to a linear classifier to predict the target classes. 

## **4. Experimental Setup** 

### **4.1. Dataset** 

To fully evaluate the discriminative capabilities and crossdomain robustness of the proposed architecture we conduct extensive experiments across two different benchmarks. The following datasets have been chosen due to their complementary nature and their ability to extensively reflect the modern landscape of manipulated content shared across social media platforms. SID-Set offers a comprehensive collection of contemporary AI-generated and tampered media, required to required to test baseline detection accuracy, while RRDataset focuses on severe image degradation techniques, allowing to evaluate model resilience against realworld conditions. 

#### **4.1.1. SID-Set** 

For our primary evaluation we employ the Social Media Image Detection Dataset (SID-Set) [21]. SID-Set is specifically designed to mimic the complexity of the modern social media landscape, containing highly realistic images uniformly distributed across three categories: Authentic ( _Real_ ), Fully Synthetic ( _Fake_ ), and Locally Manipulated ( _Tampered_ ), making it one of the most comprehensive and up to date deepfake benchmark. Crucially, because its content is sourced directly from various social media platforms, the dataset inherently captures the real-world degradations such as aggressive algorithmic compression, dynamic resizing, and multiple transmission artifacts that deepfake detectors must overcome ”in-the-wild.” We employ the official dataset splits, utilizing 210k images for the training phase, 30k for validation, and 60k for testing. 

#### **4.1.2. RRDataset** 

To further asses the forensics capabilities of our framework against real-world degradation and unseen forensic cues, we evaluate MoE-JEPA using the RRDataset. This dataset is explicitly designed to test detector resilience against the aggressive post-processing procedures commonly encountered in social-media environment. RRDataset is categorized into three subsets of images: the _Original_ split containing pristine images, the _Transmission_ split containing images that have been shared through popular messaging and social-media platforms for multiple rounds, and _ReDigitalization_ split comprising of images that have been physically recaptured from screens. Moreover, RRDataset comprehends different levels of image sensitivity, involving war, political, religious and disaster scenarios. Testing across these three specific distributions allows us to rigorously measure the capacity of the architecture to survive severe artifact attenuation and complex domain shifts. 

### **4.2. Implementation Details** 

**Architecture Configuration:** We instantiate MoE-JEPA using the large-scale V-JEPA 2 foundation model, specifically the facebook/vjepa2-vitl-fpc64-256 checkpoint<sup>1</sup> . To introduce forensic adaptability, we inject Residual MoE modules exclusively into the final 3 transformer blocks. Each MoE layer is configured with 1 frozen shared expert and _M_ = 6 trainable experts. The router utilizes a Top- _k_ selection strategy with _k_ = 2, meaning each token is processed by the shared expert and the 2 most relevant trainable experts. While the entire architecture consists of 480.46M parameters, the Residual MoE layers allow the model to only activate 379.73M parameters during each forward pass, leaving over 100M parameters inactive per token. This allows MoE-JEPA to comfortably 

1https://huggingface.co/facebook/vjepa2- vitlfpc64-256 


Figure 2. Visual examples from the SIDSet and RRDataset. The top row presents images from the SID-Set benchmark across the three categories: _Real, Fully Synthetic_ and _Tampered_ , while the bottom row displays an image of RRDataset in the three degradation split present in the benchmark: the pristine _Original_ format, the _Transmission_ split (subject to social media compression), and the _Re-Digitalization_ split (captured via screen recapture). 

process media on standard consumer hardware, and enables it to outperform massive Vision-Language Models while utilizing a fraction of their active inference parameters. 

**Training Setup:** The network is optimized using the AdamW optimizer, along with a learning rate scheduler featuring 10% linear warmup phase. The joint optimization objective dynamically balances the primary Cross-Entropy loss with the MoE Load Balancing auxiliary loss scaled by a coefficient of _λbal_ = 0 _._ 01. All experiments were conducted on a single NVIDIA RTX 5090 GPU. The architecture was trained for a maximum of 20 epochs. To prevent overfitting and ensure optimal generalization, we implemented an early stopping callback with a patience of 3 epochs, strictly monitoring the validation accuracy to determine the best model checkpoint. 

## **5. Results** 

In this section, we present a comprehensive evaluation of MoE-JEPA, benchmarking its performance against stateof-the-art deepfake detection architectures across diverse forensic scenarios. We first evaluate MoE-JEPA on the SIDSet benchmark, specifically testing its ability on detecting pristine, fully synthetic and tampered images. 

As clearly visible in Table 1, our proposed architecture achieves a new state-of-the-art performance, with an overall accuracy of 95.54% and F1-score of 94.21%, outperforming greatly larger models such as SIDA-13B. Crucially, MoEJEPA exhibits unparalleled balance across the three different categories. While highly specialized models like LGrad [33] and Gram-Net [28] achieve marginally higher accuracy on the Tampered class (98.90% and 98.60%, respectively), they suffer from severe mode collapse, failing catastrophically on the Real and Fake distributions. This indicates a 

Table 1. Detailed Accuracy and F1-Score breakdown across **SID-Set** categories: Real, Fully Synthetic and Tampered. MoE-JEPA achieves a new state-of-the-art surpassing all the previous approaches tested on the benchmark. Best results are highlighted in **bold** , and second best are underlined. 

|**Model**|**Re**|**al**|**Fully**|**Synth.**|**Tam**|**pered**|**To**|**tal**|
|---|---|---|---|---|---|---|---|---|
||Acc.|F1|Acc.|F1|Acc.|F1|Acc.|F1|
|AntifakePrompt [11]|88.90|89.10|97.50|97.90|90.90|80.40|92.40|89.10|
|CNNSpot [36]|89.00|90.80|90.70|88.10|68.10|64.00|82.60|85.40|
|FreDect [18]|46.00|47.60|60.90|66.00|37.10|53.00|47.60|55.40|
|Fusing [23]|89.20|92.07|88.10|89.10|27.00|31.40|68.10|71.00|
|Gram-Net [28]|89.20|91.70|97.90|98.60|89.90|86.90|92.10|92.40|
|UnivFD [30]|68.03|68.50|86.40|98.00|92.50|90.00|82.40|85.40|
|LGrad [33]|62.00|76.10|58.00|67.30|**98.90**|**98.80**|73.00|80.60|
|LNP [10]|14.40|23.00|36.20|35.60|93.30|94.60|48.00|51.10|
|SIDA-7B [21]|89.10|91.00|98.70|98.60|92.70|91.00|93.50|93.50|
|SIDA-13B [21]|89.60|91.10|98.50|98.70|92.90|91.20|93.60|93.50|
|**MoE-JEPA (Ours)**|**91.61**|**93.06**|**99.98**|**99.67**|95.12|93.50|**95.54**|**94.21**|


high sensitivity to local noise, making them not robust for real-world environment deployment. Conversely, our dualstream architecture is able to extract semantics and noise, making it highly accurate on all types of images. This proves that the Gated Attention MIL and the MoE router effectively prevent the semantic dilution that plagues traditional global pooling methods. 

To assess the architecture ability in even more challenging real-world scenarios, we evaluate MoE-JEPA on the RRDataset benchmark. Following the training protocol proposed by the authors, we pre-train the architecture using 162,000 images from GenImage-SDv1.4 [43] and 162,000 images from ImageNet. Later, we finetune the best checkpoint on the training split of RRDataset. To ensure a rigorous comparison, all the baselines, including the VLMs, are reported from the official RRDataset benchmark. As shown in Table 2, MoE-JEPA demonstrate incredible stability across the different post-processing splits of RRDataset, achieving an overall accuracy of 84.11%, outperforming frontier Vision-Language Models like GPT-4o-latest and Claude-3.7.sonnet. This empirical result underscores the importance of specialized forensic adaptation via Residual MoE when applied to smaller models. 

Evaluation against specialized deepfake detectors highlights the challenging nature of the RRDataset, revealing a strongly fragmented landscape with no single architecture dominating across all different splits. DIRE [37], DRCTConvB [12], and MoE-JEPA effectively lead the leaderboard, each exhibiting distinct trade-offs. MoE-JEPA secures a highly competitive second position overall, achieving the best accuracy on the Re-Digitalization _Real_ split, successfully resisting the physical noise introduced by such alteration thanks to the robust V-JEPA world model initialization. Ultimately, this demonstrates that our dualstream approach provides a reliable, balanced, and structurally aware verification for localized noise reconstruction. 

### **5.1. Ablation Studies** 

To empirically validate the architectural design choices of MoE-JEPA, we conduct a comprehensive ablation study on the SID-Set benchmark. By systematically enabling and disabling core modules, we isolate the specific performance contributions of the Mixture-of-Experts (MoE) layers, the Gated Attention MIL pooling, and the highfrequency Noise Stream. The results are summarized in Table 3. We first evaluate a naive baseline using only the intrinsic knowledge of the frozen V-JEPA encoder. This configuration yields an overall accuracy of 80.27%. Introducing the noise stream directly into this architecture improves the detection of manipulated images by more than +10% points, underlining the importance of such branch for detecting high-frequency anomalies that the semantic branch alone misses. However, the introduction of the MoE mechanism triggers a massive performance improvement, with the overall accuracy that spikes by nearly +15% points. Most notably, the accuracy on the _Real_ class jumps to 91.16% and _Tampered_ detection leaps to 93.83%. This proves that the Residual MoE successfully allows the network to internalize domain-specific forensic cues without suffering from the catastrophic forgetting of its pre-trained visual priors. We then replace the standard average pooling with out Gated Attention MIL pooling module. This introduction boosts the performance of the model across all categories, revealing the importance of spatial routing. By attending to only relevant semantic anomalies, the architecture achieves a highly competitive accuracy and sets the maximum score for the _Real_ category. Finally, while the semantic only branch of MoE-JEPA already excels at global understanding, the addition of the noise branch allow the network to peak on the _Tampered_ class, reaching 95.12%, while simultaneously securing the highest overall accuracy across all variants at 95.54%. Although there is a minor trade-off in 

Table 2. Detailed Performance Comparison on the **RRDataset** Categories. All metrics are reported as Accuracy (%). Among the detectors, best results are highlighted in **bold** , and second best are underlined 

|||||**RRDataset**||||
|---|---|---|---|---|---|---|---|
|**Model**|**Orig**|**inal**|**Trans**|**mission**|**Re-Digit**|**alization**|**Overall**|
||_Real_|_Fake_|_Real_|_Fake_|_Real_|_Fake_||
|_Vision-Language Models_|_(Evaluated_|_in a Zero-Sh_|_ot configura_|_tion)_||||
|Grok-2-vision [40]|46_._15|91_._84|52_._12|94_._03|48_._01|81_._63|69_._96|
|Gemini-2-flash [34]|71_._10|98_._43|52_._19|97_._41|46_._11|97_._41|77_._28|
|Claude-3.7-sonnet [4]|85_._12|94_._57|71_._26|96_._17|62_._34|85_._41|82_._48|
|GPT-4o-latest [1]|96_._30|92_._68|79_._41|90_._01|69_._23|76_._92|84_._09|
|_Detectors (Train on Gen_|_Image-SDv1_|_.4 & fine-tun_|_e on RRDat_|_aset)_||||
|LGrad [33]|51_._00|81_._29|18_._86|92_._54|14_._71|88_._27|57_._78|
|UnivFD [30]|64_._79|64_._90|44_._61|70_._80|36_._15|75_._69|59_._49|
|Fusing [23]|87_._24|92_._46|7_._38|**99.04**|30_._79|73_._97|65_._15|
|FreDect [18]|79_._60|75_._93|58_._13|82_._11|46_._34|69_._95|68_._68|
|LNP [10]|83_._14|89_._26|38_._23|89_._30|31_._91|91_._05|70_._48|
|CNNSpot [36]|72_._42|89_._09|65_._72|88_._78|43_._12|86_._72|74_._31|
|Gram-Net [28]|81_._34|74_._65|79_._49|75_._69|79_._45|62_._02|75_._44|
|DIRE [37]|89_._72|**98.25**|90.34|97.87|1_._42|**98.89**|79_._42|
|DRCT-ConvB [12]|**93.52**|95.52|**92.82**|95_._09|64.34|96.22|**89.59**|
|**MoE-JEPA (Ours)**|91.36|94_._51|81_._16|84_._18|**91.55**|61_._89|84.11|


Table 3. Ablation Study on SID-Set. Impact of architectural components on class-specific and overall test accuracy. 

|**Model Variant**|**Pooling**|**MoE**|**Noise**|**Real**|**Fake**|**Tampered**|**Acc.**|
|---|---|---|---|---|---|---|---|
|Baseline 1|Avg. Pooling|_×_|_×_|71.59|96.77|72.46|80.27|
|Baseline 2|Avg. Pooling|_×_|✓|69.90|99.25|85.47|84.87|
|Variant A1|Avg. Pooling|✓|_×_|91.16|99.83|93.83|95.09|
|Variant B|Avg. Pooling|✓|✓|92.76|99.80|92.88|95.15|
|MoE-JEPA (Sem.)|Gated MIL|✓|_×_|**93.43**|**99.90**|93.17|95.50|
|**MoE-JEPA (Full)**|Gated MIL|✓|✓|91.61|**99.90**|**95.12**|**95.54**|


_Real_ image accuracy, it is outweighed by the enhanced sensitivity to local forgeries and the boost in comprehensive detection. This final configuration proves that the parallel noise stream is strictly necessary to reliably isolate microscopic, semantically coherent local manipulations, yielding the most robust and accurate overall detector. 

## **6. Conclusions and Future Works** 

In this paper we presented MoE-JEPA, a dual-stream architecture for deepfake detection that pioneers the usage of the world model V-JEPA as semantic backbone. By integrating a Residual Mixture-of-Expert mechanism and Gated Attention Multiple Instance Learning (MIL) pooling, MoE-JEPA successfully internalizes domain-specific forensic cues without compromising its robust pre-trained visual world model knowledge. Furthermore, the parallel noise stream extracts high-frequency generative and sensor artifacts, improving the detection of localized forgeries. Our extensive evaluation on the SID-Set benchmark demonstrates the excellent capability of our architecture to distinguish between real, fully-synthetic and tampered images, establishing a new state-of-the-art with an overall accuracy of 95.54%. The ablation studies systemati- 

cally confirm the architectural choices, demonstrating the importance of each module of MoE-JEPA and confirming the necessity of both the dynamic expert routing and the dual-stream formulation. For future works, we plan to enhance the interpretability of MoE-JEPA by extracting spatial information directly from the processed routed patch tokens, providing localization maps for tampered images. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 8 

- [2] Darius Afchar, Vincent Nozick, Junichi Yamagishi, and Isao Echizen. Mesonet: a compact facial video forgery detection network. In _2018 IEEE international workshop on information forensics and security (WIFS)_ , pages 1–7. IEEE, 2018. 2 

- [3] Irene Amerini, Mauro Barni, Sebastiano Battiato, Paolo Bestagini, Giulia Boato, Vittoria Bruni, Roberto Caldelli, Francesco De Natale, Rocco De Nicola, Luca Guarnera, 

Sara Mandelli, Taiba Majid, Gian Luca Marcialis, Marco Micheletto, Andrea Montibeller, Giulia Orr`u, Alessandro Ortis, Pericle Perazzo, Giovanni Puglisi, Nischay Purnekar, Davide Salvi, Stefano Tubaro, Massimo Villari, and Domenico Vitulano. Deepfake media forensics: Status and future challenges. _Journal of Imaging_ , 11(3), 2025. 1 

- [4] Anthropic. Introducing the next generation of claude., 2024. 

   - 8 

- [5] Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a joint-embedding predictive architecture, 2023. 3 

- [6] Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba, Komeili, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, and Nicolas Ballas. V-jepa 2: Self-supervised video models enable understanding, prediction and planning, 2025. 2, 3 

- [7] Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video, 2024. 3 

- [8] Belhassen Bayar and Matthew C Stamm. A deep learning approach to universal image manipulation detection using a new convolutional layer. In _Proceedings of the 4th ACM workshop on information hiding and multimedia security_ , pages 5–10, 2016. 4 

- [9] James Betker, Gabriel Goh, Li Jing, Tim Brooks, Jianfeng Wang, Linjie Li, Long Ouyang, Juntang Zhuang, Joyce Lee, Yufei Guo, et al. Improving image generation with better captions. _Computer Science. https://cdn. openai. com/papers/dall-e-3. pdf_ , 2(3):8, 2023. 1 

- [10] Xiuli Bi, Bo Liu, Fan Yang, Bin Xiao, Weisheng Li, Gao Huang, and Pamela C Cosman. Detecting generated images by real images only. _arXiv preprint arXiv:2311.00962_ , 2023. 7, 8 

- [11] You-Ming Chang, Chen Yeh, Wei-Chen Chiu, and Ning Yu. Antifakeprompt: Prompt-tuned vision-language models are fake image detectors. _arXiv preprint arXiv:2310.17419_ , 2023. 7 

- [12] Baoying Chen, Jishen Zeng, Jianquan Yang, and Rui Yang. Drct: Diffusion reconstruction contrastive training towards universal detection of diffusion generated images. In _Fortyfirst International Conference on Machine Learning_ , 2024. 7, 8 

- [13] Didier Ching, John Twomey, Matthew P. Aylett, Michael Quayle, Conor Linehan, and Gillian Murphy. Can deepfakes manipulate us? assessing the evidence via a critical scoping review. _PLOS ONE_ , 20(5):1–19, 2025. 1 

- [14] Dr Dhiman. Exploding ai-generated deepfakes and misinformation: A threat to global concern in the 21st century. _Qeios_ , 2023. 1 

- [15] Xiaoyi Dong, Jianmin Bao, Dongdong Chen, Ting Zhang, Weiming Zhang, Nenghai Yu, Dong Chen, Fang Wen, and 

   - Baining Guo. Protecting celebrities from deepfake with identity consistency transformer. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 9468–9478, 2022. 2 

- [16] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In _International Conference on Learning Representations_ , 2021. 1, 2 

- [17] Mingqi Fang, Ziguang Li, Lingyun Yu, Quanwei Yang, Hongtao Xie, and Yongdong Zhang. Forensic-moe: Exploring comprehensive synthetic image detection traces with mixture of experts. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 17772–17782, 2025. 3 

- [18] Joel Frank, Thorsten Eisenhofer, Lea Sch¨onherr, Asja Fischer, Dorothea Kolossa, and Thorsten Holz. Leveraging frequency analysis for deep fake image recognition. In _International conference on machine learning_ , pages 3247–3258. PMLR, 2020. 7, 8 

- [19] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial networks. _Commun. ACM_ , 63(11):139–144, 2020. 2 

- [20] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems_ , pages 6840–6851. Curran Associates, Inc., 2020. 2 

- [21] Zhenglin Huang, Jinwei Hu, Xiangtai Li, Yiwei He, Xingyu Zhao, Bei Peng, Baoyuan Wu, Xiaowei Huang, and Guangliang Cheng. Sida: Social media image deepfake detection, localization and explanation with large multimodal model. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 28831–28841, 2025. 2, 5, 7 

- [22] Robert A. Jacobs, Michael I. Jordan, Steven J. Nowlan, and Geoffrey E. Hinton. Adaptive mixtures of local experts. _Neural Computation_ , 3(1):79–87, 1991. 2 

- [23] Yan Ju, Shan Jia, Lipeng Ke, Hongfei Xue, Koki Nagano, and Siwei Lyu. Fusing global and local features for generalized ai-synthesized image detection. In _2022 IEEE International Conference on Image Processing (ICIP)_ , pages 3465–3469. IEEE, 2022. 7, 8 

- [24] Chenqi Kong, Anwei Luo, Peijun Bao, Yi Yu, Haoliang Li, Zengwei Zheng, Shiqi Wang, and Alex C Kot. Moe-ffd: Mixture of experts for generalized and parameter-efficient face forgery detection. _IEEE Transactions on Dependable and Secure Computing_ , 2025. 3 

- [25] Black Forest Labs, Stephen Batifol, Andreas Blattmann, Frederic Boesel, Saksham Consul, Cyril Diagne, Tim Dockhorn, Jack English, Zion English, Patrick Esser, et al. Flux. 1 kontext: Flow matching for in-context image generation and editing in latent space. _arXiv preprint arXiv:2506.15742_ , 2025. 1 

- [26] Yann LeCun. A Path Towards Autonomous Machine Intelligence Version. _OpenReview_ , 2022. 2, 3 

- [27] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pages 19730– 19742. PMLR, 2023. 2 

- [28] Zhengzhe Liu, Xiaojuan Qi, and Philip HS Torr. Global texture enhancement for fake face detection in the wild. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 8060–8069, 2020. 2, 6, 7, 8 

- [29] Huy Nguyen, Thong T Doan, Quang Pham, Nghi DQ Bui, Nhat Ho, and Alessandro Rinaldo. On deepseekmoe: Statistical benefits of shared experts and normalized sigmoid gating. _arXiv preprint arXiv:2505.10860_ , 2025. 2, 3 

- [30] Utkarsh Ojha, Yuheng Li, and Yong Jae Lee. Towards universal fake image detectors that generalize across generative models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 24480– 24489, 2023. 7, 8 

- [31] Jeannie Marie Paterson. Ai deepfakes on the web: The ’wicked’ challenges for ai ethics, law and technology. In _Proceedings of the ACM Web Conference 2024_ , page 3, New York, NY, USA, 2024. Association for Computing Machinery. 1 

   - [39] Lemeng Wu, Mengchen Liu, Yinpeng Chen, Dongdong Chen, Xiyang Dai, and Lu Yuan. Residual mixture of experts, 2022. 2 

   - [40] xAI. Grok-2, 2025. 8 

   - [41] Ziyu Xue, Qingtong Liu, Haichao Shi, Ruoyu Zou, and Xiuhua Jiang. A transformer-based deepfake-detection method for facial organs. _Electronics_ , 11(24), 2022. 2 

   - [42] Nan Zhong, Yiran Xu, Sheng Li, Zhenxing Qian, and Xinpeng Zhang. Patchcraft: Exploring texture patch for efficient ai-generated image detection. _arXiv preprint arXiv:2311.12397_ , 2023. 2 

   - [43] Mingjian Zhu, Hanting Chen, Qiangyu Yan, Xudong Huang, Guanyu Lin, Wei Li, Zhijun Tu, Hailin Hu, Jie Hu, and Yunhe Wang. Genimage: A million-scale benchmark for detecting ai-generated image. _Advances in neural information processing systems_ , 36:77771–77782, 2023. 7 

   - [44] Wanyi Zhuang, Qi Chu, Zhentao Tan, Qiankun Liu, Haojie Yuan, Changtao Miao, Zixiang Luo, and Nenghai Yu. Uiavit: Unsupervised inconsistency-aware method based on vision transformer for face forgery detection. In _Computer Vision – ECCV 2022_ , pages 391–407, Cham, 2022. Springer Nature Switzerland. 2 

- [32] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixtureof-experts layer. _arXiv preprint arXiv:1701.06538_ , 2017. 2 

- [33] Chuangchuang Tan, Yao Zhao, Shikui Wei, Guanghua Gu, and Yunchao Wei. Learning on gradients: Generalized artifacts representation for gan-generated images detection. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12105–12114, 2023. 2, 6, 7, 8 

- [34] Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 1, 8 

- [35] Junke Wang, Zuxuan Wu, Wenhao Ouyang, Xintong Han, Jingjing Chen, Yu-Gang Jiang, and Ser-Nam Li. M2tr: Multi-modal multi-scale transformers for deepfake detection. In _Proceedings of the 2022 International Conference on Multimedia Retrieval_ , page 615–623, New York, NY, USA, 2022. Association for Computing Machinery. 2 

- [36] Sheng-Yu Wang, Oliver Wang, Richard Zhang, Andrew Owens, and Alexei A Efros. Cnn-generated images are surprisingly easy to spot... for now. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 8695–8704, 2020. 7, 8 

- [37] Zhendong Wang, Jianmin Bao, Wengang Zhou, Weilun Wang, Hezhen Hu, Hong Chen, and Houqiang Li. Dire for diffusion-generated image detection. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 22445–22455, 2023. 7, 8 

- [38] Zhikan Wang, Zhongyao Cheng, Jiajie Xiong, Xun Xu, Tianrui Li, Bharadwaj Veeravalli, and Xulei Yang. A timely survey on vision transformer for deepfake detection, 2024. 1 

