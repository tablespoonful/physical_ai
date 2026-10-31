> 出典: https://docs.omniverse.nvidia.com/materials-and-rendering/latest/rtx-renderer_pt.html
> 取得日: 2026-10-31

Is this page helpful?

# RTX – Interactive (Path Tracing) mode#

Omniverse RTX Renderer provides the RTX – Interactive (Path Tracing) mode, a cutting-edge rendering mode designed to accurately simulate the behavior of light in order to predict how illumination interacts with materials and environments in real-world scenarios.

RTX – Interactive (Path Tracing) mode is complemented by the RTX - Real-Time 2.0 mode, which can achieve similar results with some fidelity trade-offs, at real-time performance. See the RTX - Real-Time 2.0 mode documentation for more details.

Which render mode is enabled at startup can be modified.

- In the application’s Preferences UI’s under Edit -> Preferences -> Rendering -> RTX Renderers. By default none are specified, which results in the RTX Renderer determining its own default modes to enable. If any are enabled through this UI, upon restarting the application, only those will now be enabled.

- With commands at startup: --/persistent/rtx/modes/rt2/enabled=true for the RTX - Real-Time 2.0 mode, --/persistent/rtx/modes/pt/enabled=true for the RTX – Interactive (Path Tracing) mode, and --/persistent/rtx/modes/rt/enabled=true for the RTX Real-Time (Legacy) mode.

## Path Tracing#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Samples per Pixel per Frame (1 to 32)
 | 
/rtx/pathtracing/spp
 | 
Int 1
 | 
Total number of samples for each rendered pixel, per frame.
 | 

Total Samples per Pixel (0 = inf)
 | 
/rtx/pathtracing/totalSpp
 | 
Int 512
 | 
Maximum number of samples to accumulate per pixel. When this sample count is reached the rendering stops until a scene or setting change is detected, restarting the rendering process. Set to 0 to remove this limit.
 | 

Adaptive Sampling
 | 
/rtx/pathtracing/adaptiveSampling/enabled
 | 
Bool False
 | 
When enabled, noise values are computed for each pixel, and upon threshold level reached, the pixel is no longer sampled.
 | 

- Target Error

 | 
/rtx/pathtracing/adaptiveSampling/targetError
 | 
Float 0.001
 | 
The noise value threshold after which the pixel would no longer be sampled.
 | 

Max Bounces
 | 
/rtx/pathtracing/maxBounces
 | 
Int 4
 | 
Maximum number of ray bounces for any ray type. Higher values give more accurate results, but worse performance.
 | 

Max Specular and Transmission Bounces
 | 
/rtx/pathtracing/maxSpecularAndTransmissionBounces
 | 
Int 6
 | 
Maximum number of ray bounces for specular and transmission.
 | 

Max SSS Volume Scattering Bounces
 | 
/rtx/pathtracing/maxVolumeBounces
 | 
Int 64
 | 
Maximum number of ray bounces for SSS.
 | 

Max Fog Scattering Bounces
 | 
/rtx/pathtracing/ptfog/maxBounces
 | 
Int 2
 | 
Maximum number of bounces for volume scattering within a fog volume.
 | 

Fractional Cutout Opacity
 | 
/rtx/pathtracing/fractionalCutoutOpacity
 | 
Bool True
 | 
If enabled, fractional cutout opacity values are treated as a measure of surface ‘presence’, resulting in a translucency effect similar to alpha-blending. Path-traced mode uses stochastic sampling based on these values to determine whether a surface hit is valid or should be skipped.
 | 

Reset Accumulation on Time Change
 | 
/rtx/resetPtAccumOnAnimTimeChange
 | 
Bool False
 | 
If enabled, the Path-Tracer accumulation is restarted every time the MDL animation time changes. Settings this to false is useful to prevent accumulation reset at every frame when the ‘animation time’ is changing every frames using wall clock time (which can be the case when an animation is not being played, and wall clock time is used instead of animation time).
 | 

Note

While using a higher number of bounces increases accuracy of the final image, it may result in diminishing returns in terms of image quality relative to performance.

### About Adaptive Sampling#

The RTX – Interactive (Path Tracing) mode supports Adaptive Sampling. With Adaptive Sampling, samples are non-uniformly distributed where most beneficial for further convergence, which can result in less noise for the same number of samples and also provides a more consistent noise level across multiple frames.

Adaptive Sampling can be enabled in the RTX – Interactive (Path Tracing)’s render settings, and its Target Error value can be adjusted there as well, which when reached will stop accumulating more samples.

An Adaptive Sampling Error debug view can be selected in the Debug View render settings, which allows visualizing the normalized standard deviation of the Monte Carlo estimator of the pixels: warm colors represent high variance, which indicate that additional samples would lead to improved convergence for those pixels.

Note that currently Movie Capture does not support ending the rendering of a frame earlier when the Target Error threshold has been reached, but it will be supported in a future release.

## Sampling & Caching#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Caching
 | 
/rtx/pathtracing/cached/enabled
 | 
Bool True
 | 
Enables caching path tracing results for improved performance at the cost of some accuracy.
 | 

Many-Light Sampling
 | 
/rtx/pathtracing/lightcache/cached/enabled
 | 
Bool True
 | 
Enables a technique that improves the sampling quality (and therefore rendering convergence) in scenes with many light primitives.
 | 

Mesh-Light Sampling
 | 
/rtx/pathtracing/ris/meshLights
 | 
Bool False
 | 
Enables direct illumination sampling of geometry with emissive materials.
 | 

## Anti-Aliasing#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Anti-Aliasing Sample Pattern
 | 
/rtx/pathtracing/aa/op
 | 
Int 1
 | 
Sampling pattern used for Anti-Aliasing. Select between Box (0), Triangle (1), Gaussian (2) and Uniform (3).
 | 

Anti-Aliasing Radius
 | 
/rtx/pathtracing/aa/filterRadius
 | 
Float 1.0
 | 
The sampling footprint radius, in pixels, when generating samples with the selected antialiasing sample pattern.
 | 

## Firefly Filtering#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Firefly Filtering
 | 
/rtx/pathtracing/fireflyFilter/enabled
 | 
Bool True
 | 
Enables image filtering to reduce the presence of excessively bright “firefly” pixel artifacts.
 | 

Max Ray Intensity Glossy
 | 
/rtx/pathtracing/fireflyFilter/maxIntensityPerSample
 | 
Float 3200
 | 
Clamps the maximum ray intensity for glossy bounces. Can help prevent fireflies, but may result in energy loss.
 | 

Max Ray Intensity Diffuse
 | 
/rtx/pathtracing/fireflyFilter/maxIntensityPerSampleDiffuse
 | 
Float 3200
 | 
Clamps the maximum ray intensity for diffuse bounces. Can help prevent fireflies, but may result in energy loss.
 | 

## Denoising#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Denoising
 | 
/rtx/pathtracing/optixDenoiser/enabled
 | 
Bool True
 | 
Enable to apply the OptiX Denoiser to the radiance image generated by the renderer. The OptiX denoiser results in an order of magnitude reduction in rendering times for a target image quality.
 | 

Optix Denoiser Temporal Mode
 | 
/rtx/pathtracing/optixDenoiser/temporalMode/enabled
 | 
Bool False
 | 
Can denoise multi-frame animation sequences without low-frequency denoiser artifacts commonly seen in animated frames denoised separately.
 | 

Optix Denoiser Blend Factor
 | 
/rtx/pathtracing/optixDenoiser/blendFactor
 | 
Float 1.0
 | 
A blend factor indicating how much to blend the denoised image with the original non-denoised image. 0 shows only the denoised image, 1.0 shows the image with no denoising applied.
 | 

Denoise AOVs
 | 
/rtx/pathtracing/optixDenoiser/AOV
 | 
Bool True
 | 
If enabled, the OptiX Denoiser will also denoise the AOVs.
 | 

## Non-uniform Volumes#

This feature enables path-traced volume rendering of both VDB files (internally converted to NanoVDB, a faster and more compact GPU-friendly volume representation) and procedural MDL based volumes.
VDB files can either contain a SDF (signed distance field/level set) or density volume. Currently, the VDB volume material can only be applied to a cube mesh, while procedural volume materials can be applied to any kind of mesh (cube, sphere, torus, etc.).
Volumes can also overlap with other volumes. The maximum number of overlaps between the volumes is currently limited to four.

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Non-uniform Volumes
 | 
/rtx/pathtracing/ptvol/enabled
 | 
Bool False
 | 
The number of bounces is controlled by Max Heterogeneous Volume Scattering Bounces (under the Path Tracing section in Path-Traced Mode Settings). When set to 1: perform single scattering; fast, suitable for lowly scattering volumes like fog. Higher values result in multi-scattering; slower, suitable for highly scattering volumes like clouds.
 | 

Transmittance Method
 | 
/rtx/pathtracing/ptvol/transmittanceMethod
 | 
Int 0
 | 
Choose between Biased Ray Marching (0) or Ratio Tracking (1). Biased ray marching is the ideal option in all cases.
 | 

Max Collision Count
 | 
/rtx/pathtracing/ptvol/maxCollisionCount
 | 
Int 1024
 | 
Maximum delta tracking iterations. Increase to more than 32 for highly scattering volumes like clouds. Important: if set too low, parts of the volume will disappear.
 | 

Max Light Collision Count
 | 
/rtx/pathtracing/ptvol/maxLightCollisionCount
 | 
Int 32
 | 
Maximum ratio tracking iterations. Increase to more than 32 for highly scattering volumes like clouds. Important: if set too low, parts of the volume will disappear.
 | 

Max Non-Uniform Volume Scattering Bounces
 | 
/rtx/pathtracing/ptvol/maxBounces
 | 
Int 2
 | 
Maximum number of ray bounces for non-uniform volumes.
 | 

## Global Volumetric Effects#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Rayleigh Atmosphere
 | 
/rtx/pathtracing/ptvol/raySky
 | 
Bool False
 | 
Enables an additional medium of Rayleigh-scattering particles to simulate a physically based sky.
 | 

- Rayleigh Atmosphere Scale

 | 
/rtx/pathtracing/ptvol/raySkyScale
 | 
Float 1.0
 | 
Scales the size of the Rayleigh sky.
 | 

- Skip Background

 | 
/rtx/pathtracing/ptvol/raySkyDomelight
 | 
Bool False
 | 
If a domelight is rendered for the sky color, the Rayleight Atmosphere is applied to the foreground while the background sky color is left unaffected.
 | 

## AOV#

AOVs (Arbitrary Output Variables) are data known to the renderer and used to compute illumination. Typically, AOVs contain decomposed lighting information such as:

- Direction and indirect illumination

- Reflections and refractions

- Objects with self illumination

But they can also contain geometric and scene information, such as:

- Surface position in world-space

- Orientation of normals

- View-relative depth

As the final image is computed, the intermediate information used during rendering can be optionally written to disk, providing opportunities to modify the final image during compositing and additional insights through 2D analysis. The auxiliary images, called “passes” in Omniverse and “Render Products” in USD, are just named outputs. The AOV data used by the renderer is referred to as a “Render Variable” and defines what is written for each pass.

If the OptiX Denoiser is enabled (true by default) the AOVs will be denoised. An option to control this is available in Denoising settings.

Debug View contains a list of the AOV passes which can be displayed if enabled for previewing.

### AOV Common Settings#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Minimum Z-Depth
 | 
/rtx/pathtracing/zDepthMin
 | 
Float 1.0
 | 
The minimum z-depth for AOVs. The depth range can be shorted when necessary to increases the precision.
 | 

Maximum Z-Depth
 | 
/rtx/pathtracing/zDepthMax
 | 
Float 10000.0
 | 
The maximum z-depth for AOVs. The depth range can be shorted when necessary to increases the precision.
 | 

32-Bit Depth AOV
 | 
/rtx/pathtracing/depth32BitAov
 | 
Bool False
 | 
Uses a 32-bit format for the depth AOV.
 | 

### AOV Passes#

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Background
 | 
/rtx/pathtracing/backgroundAOV
 | 
Bool False
 | 
Shading of the background, such as the background resulting from rendering a Dome Light.
 | 

Diffuse Filter
 | 
/rtx/pathtracing/diffuseFilterAOV
 | 
Bool False
 | 
The raw color of the diffuse texture.
 | 

Direct Illumination
 | 
/rtx/pathtracing/diAOV
 | 
Bool False
 | 
Shading from direct paths to light sources.
 | 

Global Illumination
 | 
/rtx/pathtracing/giAOV
 | 
Bool False
 | 
Diffuse shading from indirect paths to light sources.
 | 

Illuminance
 | 
/rtx/pathtracing/illuminanceAOV
 | 
Bool False
 | 
The amount of light falling onto (illuminating) and spreading over a given surface area.
 | 

Luminance
 | 
/rtx/pathtracing/luminanceAOV
 | 
Bool False
 | 
The intensity of light emitted from a surface per unit area in a given direction.
 | 

Motion Vectors
 | 
/rtx/pathtracing/motionAOV
 | 
Bool False
 | 
Motion vectors.
 | 

Reflections
 | 
/rtx/pathtracing/reflectionsAOV
 | 
Bool False
 | 
Shading from indirect reflection paths to light sources.
 | 

Reflection Filter
 | 
/rtx/pathtracing/reflectionFilterAOV
 | 
Bool False
 | 
The raw color of the reflection, before being multiplied for its final intensity.
 | 

Refractions
 | 
/rtx/pathtracing/refractionsAOV
 | 
Bool False
 | 
Shading from refraction paths to light sources.
 | 

Refraction Filter
 | 
/rtx/pathtracing/refractionFilterAOV
 | 
Bool False
 | 
The raw color of the refraction, before being multiplied for its final intensity.
 | 

Self-Illumination
 | 
/rtx/pathtracing/selfIllumAOV
 | 
Bool False
 | 
Shading of the surface’s own emission value.
 | 

Subsurface Filter
 | 
/rtx/pathtracing/subsurfaceFilterAOV
 | 
Bool False
 | 
The raw color of the subsurface scattering texture.
 | 

View Normal
 | 
/rtx/pathtracing/viewNormalsAOV
 | 
Bool False
 | 
The surface’s normal in view-space.
 | 

Volumes
 | 
/rtx/pathtracing/volumesAOV
 | 
Bool False
 | 
Shading from VDB volumes.
 | 

World Normal
 | 
/rtx/pathtracing/worldNormalsAOV
 | 
Bool False
 | 
The surface’s normal in world-space.
 | 

World Position
 | 
/rtx/pathtracing/worldPosAOV
 | 
Bool False
 | 
The surface’s position in world-space.
 | 

Z-Depth
 | 
/rtx/pathtracing/zDepthAOV
 | 
Bool False
 | 
The surface’s depth relative to the view position.
 | 

## Multi Matte#

Multi Matte extends AOV support by enabling rendering masked mesh geometry and materials to AOVs.

The Multi Matte channel count defines the total number of channels available, and each is assigned to a Multi Matte AOV’s color channel (red, green, or blue). Each channel has an index, and Mesh geometry or materials with a matching Multi Matte ID index will be rendered to the first Multi Matte AOV channel found with a matching index.

If a geometry has a Multi Matte ID set, and has a material assigned with a Multi Matte ID set, then the ID on the geometry takes precedence.

In order to set a Multi Matte ID on a material, add the attribute uniform int multimatte_id to the Material prim.

Debug View contains a list of all Multi Matte AOV passes which can be previewed.

Warning

Note that when capturing RenderProducts other than the Viewport RenderProduct, the attributes int omni:rtx:pt:multimatte:channel<N> and int omni:rtx:pt:multimatte:channelCount must be set on each RenderProduct to be captured, otherwise no Multi Matte outputs will be generated.

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Channel Count
 | 
/rtx/pathtracing/multimatte/channelCount
 | 
Int 0
 | 
Multimatte allows rendering AOVs of meshes which have a Multimatte ID index matching a Multimatte AOV’s channel index. Channel Count determines how many channels can be used, which are distributed among the Multimatte AOVs’ color channels. You can preview a Multimatte AOV by selecting one in the Debug View render settings.
 | 

Multimatte AOV
 | 
 | 
 | 
 | 

- Red Channel Multimatte ID Index

 | 
/rtx/pathtracing/multimatte/channel(+index)
 | 
Int -1
 | 
The Multimatte ID index to match for the red channel of this Multimatte AOV.
 | 

- Green Channel Multimatte ID Index

 | 
/rtx/pathtracing/multimatte/channel(+index)
 | 
Int -1
 | 
The Multimatte ID index to match for the green channel of this Multimatte AOV.
 | 

- Blue Channel Multimatte ID Index

 | 
/rtx/pathtracing/multimatte/channel(+index)
 | 
Int -1
 | 
The Multimatte ID index to match for the blue channel of this Multimatte AOV.
 | 

## LPEs#

Light Path Expressions (LPEs) are a special type of AOV that work as filters on the types of light transport paths which are simulated.
When rendering USD RenderVars of sourceType lpe, the expression provided in sourceName will control the contributions to the respective buffer.

See the online documentation for LPE details.

## Multi-GPU#

Multi-GPU mode distributes the image across the GPUs while automatically balancing the workload. Automatic Load Balancing can improve performance, particularly at high resolution and with mixed GPU models of varying capacity.

The primary GPU performs various tasks, such as: rendering pixels, sample aggregation, denoising, post processing, UI rendering. The default GPU 0 Weight value is usually ideal.

Display Name
 | 
Setting Name
 | 
Type and Default Value
 | 
Description
 | 

Multi-GPU
 | 
/rtx/pathtracing/mgpu/enabled
 | 
Bool True
 | 
Enables using multiple GPUs (when available). This splits the rendering of the image into a large tile per GPU with a small overlap region between them.
 | 

Automatic Load Balancing
 | 
/rtx/pathtracing/mgpu/autoLoadBalancing/enabled
 | 
Bool True
 | 
Automatically balances the amount of total path tracing work to be performed by each GPU in a multi-GPU configuration.
 | 

GPU (index) Weight
 | 
/rtx/pathtracing/mgpu/weightGpu(+index)
 | 
Float Auto
 | 
The amount of total Path Tracing work (between 0 and 1) to be performed by the first GPU in a Multi-GPU configuration. A value of 1 means the first GPU will perform the same amount of work assigned to any other GPU. Ignored if Automatic Load Balancing is enabled.
 | 

Compress Radiance
 | 
/rtx/pathtracing/mgpu/compressRadiance
 | 
Bool False
 | 
Enables lossy compression of per-pixel output radiance values.
 | 

Compress Albedo
 | 
/rtx/pathtracing/mgpu/compressAlbedo
 | 
Bool True
 | 
Enables lossy compression of per-pixel output albedo values (needed by OptiX denoiser).
 | 

Compress Normals
 | 
/rtx/pathtracing/mgpu/compressNormals
 | 
Bool True
 | 
Enables lossy compression of per-pixel output normal values (needed by OptiX denoiser).
 | 

Multi-Threading
 | 
/rtx/multiThreading/enabled
 | 
Bool True
 | 
Enabling multi-threading improves UI responsiveness.
 | 

Note

In simple scenes, Automatic Load Balancing may not make a significant difference, and may take more time in scenes with low frame rates.

### Limitations#

Multi-GPU rendering lowers the cost of rendering more pixels and is ideal for high-resolution rendering, particularly for the RTX Interactive (Path Tracing) mode. It will not improve performance for animations, physics, etc.

For efficiency’s sake, in some contexts rendering will switch to single-GPU automatically until conditions warrant multi-GPU rendering, for example when rendering at low resolution.

Multi-GPU rendering is enabled by default if the system has multiple NVIDIA RTX-enabled GPUs of the same model.

Per-GPU memory usage is limited to 48GB.

Multi-GPU is disabled for mixed-GPU configurations. This can be overridden with a setting. Note that the GPU with the lowest memory capacity will limit the amount of memory the other GPUs can leverage.

GPUs which don’t support ray tracing are skipped automatically.

Note that LDA (SLI) configurations are only supported on DX12, not on Vulkan.

Note

A GPU information table is logged to the omniverse .log file under [gpu.foundation] listing which GPUs are set as Active. Each GPU has a device index assigned and this index can be used with the multi-GPU settings below.

Setting Name
 | 
Type and Default Value
 | 
Description
 | 

/renderer/multiGpu/enabled
 | 
Bool True
 | 
Specifies if multi-GPU is enabled, but multi-GPU is disabled if the NVIDIA RTX-enabled GPUs are not of the same model; setting this to true will enable multi-GPU anyway.
 | 

/renderer/multiGpu/activeGpus
 | 
String Auto
 | 
Enables only a subset of GPUs, specified by a comma-separated list of device indices.
 | 

/renderer/multiGpu/maxGpuCount
 | 
Int Auto
 | 
Specifies the maximum number of NVIDIA RTX-enabled GPUs. GPUs which don’t support ray tracing are skipped automatically.
 | 

 On this page
