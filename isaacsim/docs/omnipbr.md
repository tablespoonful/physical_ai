> 出典: https://docs.omniverse.nvidia.com/materials-and-rendering/latest/templates/OmniPBR.html
> 取得日: 2026-10-31

Is this page helpful?

# OmniPBR#

OmniPBR is the default Physically based material available in Omniverse. This material can describe most opaque dielectric or non-dielectric materials.

## Parameters#

Albedo 
Albedo defines the base color of a surface before lighting calculations. Unlike diffuse color in traditional materials, albedo represents only the pure color reflection
of a surface, excluding lighting, shadows, or reflective properties.

Parameters 

Display Name
 | 
Name
 | 
Type
 | 
Default
 | 

Base Color
 | 
diffuse_color_constant
 | 
color
 | 
0.2, 0.2, 0.2
 | 

Albedo Map
 | 
diffuse_texture
 | 
asset
 | 
 | 

Albedo Map Color Space
 | 
 | 
 | 
 | 

Albedo Desaturation
 | 
albedo_desaturation
 | 
float
 | 
0.0
 | 

Albedo Add
 | 
albedo_add
 | 
float
 | 
0.0
 | 

Albedo Brightness
 | 
albedo_brightness
 | 
float
 | 
1.0
 | 

Color Tint
 | 
diffuse_tint
 | 
color
 | 
1.0, 1.0, 1.0
 | 

Base Color

This parameter sets the diffuse color or tint of the material.

Base Color: 0.1, 0.27, 0.17#

 | 

Albedo Map

Accepts a texture file to define color values.

 | 

Albedo Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

Texture Gamma: Raw

 | 

Texture Gamma: sRGB

 | 

Albedo Desaturation

Removes color saturation. This can be used to create a more monochromatic look for the material.

The range is as follows:
- 0 = Unaffected

- 1 = Monochromatic.

Desaturation 0.0

 | 

Desaturation 0.5

 | 

Desaturation 1.0

 | 

Albedo Add

Add (or subtract) the Base Color from the albedo Map.

Albedo Add: 0.15#

 | 

Albedo Brightness

Adjusts the brightness of the albedo map.

Albedo Brightness: 2.0#

 | 

Color Tint

Color multiplier of the albedo Map.

Color Tint: 0.37, 0.3, 0.22#

 | 

Reflectivity 

Specular reflection represents light that bounces directly off a material’s surface, creating mirror like reflections. The reflection’s intensity depends on:
- Material Type: Metals reflect 60-100% of light, while non-metals (dielectrics) reflect 2-5%

- Surface Roughness: Smooth surfaces create sharp reflections; rough surfaces create blurred reflections

- Viewing Angle: Reflections become stronger at glancing angles (Fresnel effect)

Parameters 

Display Name
 | 
Name
 | 
Type
 | 
Default
 | 

Roughness Amount
 | 
reflection_roughness_constant
 | 
float
 | 
0.5
 | 

Roughness Map Influence
 | 
reflection_roughness_texture_influence
 | 
float
 | 
0.0
 | 

Roughness Map
 | 
reflectionroughness_texture
 | 
asset
 | 
 | 

Roughness Map Color Space
 | 
 | 
 | 
 | 

Metallic amount
 | 
metallic_constant
 | 
float
 | 
0.0
 | 

Metallic Map Influence
 | 
metallic_texture_influence
 | 
float
 | 
0.0
 | 

Metallic Map
 | 
metallic_texture
 | 
asset
 | 
 | 

Metallic Map Color Space
 | 
 | 
 | 
 | 

Specular
 | 
specular_level
 | 
float
 | 
0.5
 | 

Enable ORM texture
 | 
enable_ORM_texture
 | 
bool
 | 
false
 | 

ORM Map
 | 
ORM_texture
 | 
asset
 | 
 | 

ORM Map Color Space
 | 
 | 
 | 
 | 

Roughness Amount

Defines how rough or smooth a surface appears when viewed from any angle. A value of 0 creates perfect mirror-like reflections, while higher values (up to 1) create increasingly diffuse, blurred reflections. Unlike anisotropic roughness, this property affects light scattering uniformly in all directions.

The range is as follows:
- 0 = Perfectly reflective surface

- 1 = No reflectivity

Roughness 0.00

 | 

Roughness 0.25

 | 

Roughness 0.5

 | 

Roughness Map Influence

Mixes the Roughness Map power over the Roughness value.

The range is as follows:
- 0 = Roughness Value

- 1 = Roughness Map

Roughness Influence 0.0

 | 

Roughness Influence 0.5

 | 

Roughness Influence 1.0

 | 

Roughness Map

Accepts a texture file to define roughness values.

 | 

Roughness Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

Metallic Amount

Metallic Amount

Determines if the surface is Dielectric (non-metallic) or Conductive (metallic).

The range is as follows:
- 0 = Dielectric (non metalallic)

- 1 = Conductive (metallic)

Metallic Amount: 0.0

 | 

Metallic Amount: 0.5

 | 

Metallic Amount: 1.0

 | 

Metallic Map Influence

Mixes the Metallic Map power over the Metallic amount.

The range is as follows:
- 0 = Metallic Amount

- 1 = Metallic Map

Metallic Map Influence: 0.0

 | 

Metallic Map Influence: 0.5

 | 

Metallic Map Influence: 1.0

 | 

Metallic Map

Enables the application of a texture map to define metallic areas on the surface.

 | 

Metallic Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

Specular

The specular reflectivity of the material.

Specular: 0.0

 | 

Specular: 0.5

 | 

Enable ORM Texture

Allows use of a “packed” Occlusion, Roughness and Metallic map instead of separate maps for each. Each channel of the texture is used as follows:
- Red: Occlusion

- Green: Roughness

- Blue: Metallic

ORM Map

“Packed” ORM map texture input.

ORM Map Influence: 0.0

 | 

ORM Map Influence: 0.5

 | 

ORM Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

AO 
A pre-computed ambient occlusion map that can be applied to the material.

Parameters 

Display Name
 | 
Name
 | 
Type
 | 
Default
 | 

Ambient Occlusion to Diffuse
 | 
ao_to_diffuse
 | 
float
 | 
0.0
 | 

Ambient Occlusion Map
 | 
ao_texture
 | 
asset
 | 
 | 

Ambient Occlusion Map Color Space
 | 
 | 
 | 
 | 

Ambient Occlusion to Diffuse

How much ambient occlusion influences the diffuse map in a range of 0-1.
- 0 = unaffected

- 1 = full effect.

Ambient Occlusion Map

Accepts a texture file to define ambient occlusion values. This is typically a pre computed texture from a DCC.

Ambient Occlusion: 0

 | 

Ambient Occlusion: 1

 | 

Ambient Occlusion Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

Emissive 
Emissivity defines how much light a surface emits independently of received light. This parameter creates self-illuminating effects like neon signs, screens, or bioluminescence materials.
Emissivity maintains physical accuracy by contributing to scene lighting and global illumination calculations.

Parameters 

Display Name
 | 
Name
 | 
Type
 | 
Default
 | 

Enable Emission
 | 
enable_emission
 | 
bool
 | 
false
 | 

Emissive Color
 | 
emissive_color
 | 
color
 | 
1.0, 1.0, 0.1
 | 

Emissive Color Map
 | 
emissive_color_texture
 | 
asset
 | 
 | 

Emissive Color Map Color Space
 | 
 | 
 | 
 | 

Emissive Mask Map
 | 
emissive_mask_texture
 | 
asset
 | 
 | 

Emissive Mask Map Color Space
 | 
 | 
 | 
 | 

Emissive Intensity
 | 
emissive_intensity
 | 
float
 | 
1.0
 | 

Enable Emission

Toggles light emission from the material surface

EnableEmissive 0

Enable Emission: false#

 | 

EnableEmissive 1

Enable Emission: true#

 | 

Emissive Color

Specifies the color of emitted light

Emission Color: .94, .89, .65#

 | 

Emissive Color Map

Accepts a texture file to define emission color values.

 | 

Emissive Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

Emissive Mask Map

Accepts a texture file to define emission mask values.

 | 

Emissive Mask Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

Emissive Intensity

Determines the intensity of emitted light.

EnableEmissive 0

 | 

EnableEmissive 800

 | 

EnableEmissive 5000

 | 

Opacity 
Opacity controls material transparency by specifying how much light passes through each point on a surface. These grayscale textures define transparency levels from 0 (fully transparent) to 1 (fully opaque)

Parameters 

Display Name
 | 
Name
 | 
Type
 | 
Default
 | 

Enable Opacity
 | 
enable_opacity
 | 
bool
 | 
false
 | 

Enable Opacity Texture
 | 
enable_opacity_texture
 | 
bool
 | 
false
 | 

Opacity Amount
 | 
opacity_constant
 | 
float
 | 
1.0
 | 

Opacity Map
 | 
opacity_texture
 | 
asset
 | 
 | 

Opacity Map Color Space
 | 
 | 
 | 
 | 

Opacity Map Mono Source
 | 
opacity_mode
 | 
enum
 | 
mono_average
 | 

Opacity Threshold
 | 
opacity_threshold
 | 
float
 | 
0.0
 | 

OmniPBR Enable Opacity

Enables overall opacity.

Enable Opacity: True

Opacity Amount: 0.5#

 | 

Enable Opacity: False

Opacity Amount: 0.5#

 | 

OmniPBR Enable Opacity Texture

Enables opacity mapping.

Enable Opacity Map: True

 | 

Enable Opacity Map: False

 | 

OmniPBR Opacity Amount

Opacity value of material. Works in conjunction with Opacity Threshold and Fractional Cutout Opacity

Opacity Amount 1.0

 | 

Opacity Amount 0.5

 | 

Opacity Amount 0.1

 | 

OmniPBR Opacity Map

Accepts a texture file to define an opacity mask.

 | 

OmniPBR Opacity Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

OmniPBR Opacity Map Mono Source

Valid Opacity Map Mono Source Values 

Specifies opacity channel or evaluation of the map for opacity.
- mono_alpha : Uses the alpha channel of the image as the source for evaluation.

- mono_average : Uses the average of the RGB channels as the source for evaluation.

- mono_luminance : Uses the luminance of the image as the source for evaluation.

- mono_maximum : Uses the max value of the RGB channels as the source for evaluation.

OmniPBR Opacity Threshold

Cutoff for determining object cutout opacity. If threshold is equal to 0, then use fractional opacity. If threshold is greater than 0, then object is opaque when opacity is greater than threshold.

Opacity Threshold: 0.2

 | 

Opacity Threshold: 0.3

 | 

Opacity Threshold: 0.35

 | 

Normals 
Normal maps encode surface detail by modifying how light interacts with a material’s surface. These maps store direction data as RGB values, allowing complex surface details like bumps,
scratches, and indentations to be rendered without additional geometry. Surface normals affect all lighting calculations including reflection, specular highlights, and shadow termination.

Parameters 

Display Name
 | 
Name
 | 
Type
 | 
Default
 | 

Normal Map Strength
 | 
bump_factor
 | 
float
 | 
1.0
 | 

Normal Map
 | 
normalmap_texture
 | 
asset
 | 
 | 

Normal Map Color Space
 | 
 | 
 | 
 | 

Detail Normal Strength
 | 
detail_bump_factor
 | 
float
 | 
0.3
 | 

Detail Normal Map
 | 
detail_normalmap_texture
 | 
asset
 | 
 | 

Detail Normal Map Color Space
 | 
 | 
 | 
 | 

Normal Map Flip U Tangent
 | 
flip_tangent_u
 | 
bool
 | 
false
 | 

Normal Map Flip V Tangent
 | 
flip_tangent_v
 | 
bool
 | 
true
 | 

OmniPBR Normal Map Strength

Adjusts intensity of the normal map.

Normal Map Strength: 0.0

 | 

Normal Map Strength: 0.5

 | 

Normal Map Strength: 1.5

 | 

OmniPBR Normal Map

Accepts a texture file to define surface details through normal mapping. For best results use the Direct X normal format.

Normal Map Strength: 0.0

 | 

Normal Map Strength: 1.0

 | 

OmniPBR Normal Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

OmniPBR Detail Normal Strength

Adjusts intensity of small surface detail.

Normal Map Strength: 1.0#

Detailed Normal Map Strength: 0.3

 | 

OmniPBR Detail Normal Map

Accepts a texture file to define micro surface details through normal mapping. For best results use the Direct X normal format .

Detailed Normal Map Strength: 0.3#

 | 

OmniPBR Detail Normal Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

OmniPBR Normal Map Flip U Tangent

Flips the U Tangent vector.

OmniPBR Normal Map Flip V Tangent

Flips the V Tangent vector. By Default, OmniPBR is setup for DirectX normal maps. Set Normal Map Flip V = false for OpenGL.

DirectX Normal Map

 | 

OpenGL Normal Map

 | 

DirectX Normal Map

Normal Map Flip U Tangent: false#

Normal Map Flip V Tangent: trie

 | 

OpenGL Normal Map

Normal Map Flip U Tangent: false#

Normal Map Flip V Tangent: false

 | 

## OmniPBR ClearCoat#

OmniPBR_ClearCoat is similar to OmniPBR but with an additional glossy bsdf layer. Ideal for car paint or any surface with a thin clear finish.

## Parameters#

Clearcoat 
Clearcoat simulates an additional transparent layer on top of a base material, common in automotive paints, polished wood, and plastic coatings. This layer adds a second specular reflection
with its own roughness and intensity values, independent of the underlying material properties.

Parameters 

Display Name
 | 
Name
 | 
Type
 | 
Default
 | 

Enable Clearcoat Layer
 | 
enable_clearcoat
 | 
bool
 | 
false
 | 

Clearcoat Tint
 | 
clearcoat_tint
 | 
color
 | 
1.0, 1.0, 1.0
 | 

Clearcoat Transparency
 | 
clearcoat_transparency
 | 
float
 | 
1.0
 | 

Clearcoat Roughness
 | 
clearcoat_reflection_roughness
 | 
float
 | 
0.0
 | 

Clearcoat Weight
 | 
clearcoat_weight
 | 
float
 | 
1.0
 | 

Clearcoat Flatten
 | 
clearcoat_flatten
 | 
float
 | 
1.0
 | 

Clearcoat IOR
 | 
clearcoat_ior
 | 
float
 | 
1.56
 | 

Clearcoat Normal Map Strength
 | 
clearcoat_bump_factor
 | 
float
 | 
1.0
 | 

Clearcoat Normal Map
 | 
clearcoat_normalmap_texture
 | 
asset
 | 
 | 

Clearcoat Normal Map Color Space
 | 
 | 
 | 
 | 

OmniPBR Enable Clearcoat Layer

Enables clear coat layer.

Enable Clearcoat Layer: false

 | 

Enable Clearcoat Layer: true

 | 

OmniPBR Clearcoat Tint

Base color of the clearcoat layer.

Enable Clearcoat Layer: false

Clearcoat Tint: 1.0, 1.0, 1.0#

 | 

Enable Clearcoat Layer: true

Clearcoat Tint: 0.3, 0.16, 0.16#

 | 

OmniPBR Clearcoat Transparency

Weighted blend between the material and the clearcoat.
- 0 = Clearcoat

- 1 = Base material with clearcoat on top

Clearcoat Transparency: 1.0

Clearcoat Tint: 1.0, 1.0, 1.0#

 | 

Clearcoat Transparency: 0.5

Clearcoat Tint: 0.3, 0.16, 0.16#

 | 

Clearcoat Transparency: 0.0

Clearcoat Tint: 0.3, 0.16, 0.16#

 | 

OmniPBR Clearcoat Roughness

Isotropic roughness of the clearcoat. Usually 0.

Clearcoat Roughness: 0.0

 | 

Clearcoat Roughness: 0.1

 | 

Clearcoat Roughness: 0.2

 | 

OmniPBR Clearcoat Weight

The specular reflectivity of the clearcoat layer.

Clearcoat Weight: 1.0

 | 

Clearcoat Weight: 0.5

 | 

Clearcoat Weight: 0.2

 | 

OmniPBR Clearcoat Flatten

Blends between the smooth normal and the bumped base normal.

Clearcoat Flatten: 1.00

 | 

Clearcoat Flatten: 0.55

 | 

Clearcoat Flatten: 0.00

 | 

OmniPBR Clearcoat IOR

Index of Refraction of the clearcoat layer.

Clearcoat IOR: 1.0

 | 

Clearcoat IOR: 1.56

 | 

Clearcoat IOR: 2.5

 | 

OmniPBR Clearcoat Normal Map Strength

Scalar multiplier of the Clearcoat Normal Map.

Normal Map Strength: 0.0

 | 

Normal Map Strength: 0.5

 | 

Normal Map Strength: 1.0

 | 

OmniPBR Clearcoat Normal Map

Normal map for the clearcoat layer.

 | 

OmniPBR Clearcoat Normal Map Color Space

Valid Texture Gamma Values 

- raw : Use texture data as it was read from the texture and do not mark it as using a specific color space.

- sRGB : Mark texture as sRGB when reading.

- auto : Check for gamma/color space metadata in the texture file itself; if metadata is indicative of sRGB, mark texture as sRGB. If no relevant metadata is found, mark texture as sRGB if it is either 8-bit and has 3 channels or if it is 8-bit and has 4 channels. Otherwise, do not mark texture as sRGB and use texture data as it was read from the texture.

 On this page
