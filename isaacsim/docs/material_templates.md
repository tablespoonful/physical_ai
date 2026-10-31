> 出典: https://docs.omniverse.nvidia.com/materials-and-rendering/latest/materials_templates.html
> 取得日: 2026-10-31

Is this page helpful?

# Omniverse Material Templates#

Omniverse provides a set of template materials, including physically based glass, general-purpose multi-lobed materials suitable for both dielectric and non-dielectric applications, as well as specialized materials for skin, hair, and liquids. These templates also support subsurface scattering and transmissive effects where required. Additionally, Omniverse includes the USD UsdPreviewSurface for defining basic material appearances.

Not all templates are available by default. You can enable them per installation or per user. To enable templates per user, add the following lines to the user.toml file located in the kit/shared directory under the user’s home directory. This example enables all templates, as shown in the following image. Wild cards can be used to broaden the allow list, as noted.

[exts."omni.kit.material.library"]
ui_show_list = ["*Omni*", "*Sim*", "USD*"]

This code block can also be added to the kit application configuration file, located in the _build/<os-build-name>/release/apps directory. The file name is based on the initial setup of the Omniverse template application. For example, the Composer’s kit application configuration file might be named my_company.my_usd_composer.kit. Adding the code here enables the templates for all users of the application. To disable the templates, set the ui_show_list to an empty list.

Template Name
 | 
General Use Case
 | 

UsdPreviewSurface
 | 

Native MDL material based on Pixar’s UsdPreviewSurface Specification

 | 

OpenPBR
 | 

MaterialX-based implementation of the OpenPBR Specification

 | 

OmniPBR
 | 

Multi-lobed physically based material for dielectric and non-dielectric materials

 | 

OmniPBR_Base [1]
 | 

A Material Graph friendly version of OmniPBR for use in building custom shading networks

 | 

OmniPBR_ClearCoat
 | 

Adds second glossy Bsdf to simulate a thin clear coating

 | 

OmniGlass
 | 

Transmissive, reflective, and refractive material

 | 

OmniEmissive
 | 

Simple emissive material.

 | 

OmniSurface
 | 

Multi-lobed physical material for modeling a wide variety of materials

 | 

OmniSurfaceBase [1]
 | 

A Material Graph friendly version of OmniSurface for use in building custom shading networks

 | 

OmniSurfaceBlend
 | 

Allows blending between two materials with masking

 | 

OmniSurfaceLite
 | 

Contains subset of OmniSurface and is designed to be more performant than the full implementation

 | 

OmniSurfaceLiteBase [1]
 | 

A Material Graph friendly version of OmniSurfaceLite for use in building custom shading networks

 | 

OmniHair
 | 

Hair material based on Disney’s Hair and Fur

 | 

OmniHairBase [1]
 | 

A Material Graph friendly version of OmniSurfaceHair for use in building custom shading networks

 | 

[1]
(1,2,3,4)
Base materials have simplified material inputs for use in building material graphs
