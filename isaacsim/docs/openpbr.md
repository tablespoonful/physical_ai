> 出典: https://docs.omniverse.nvidia.com/materials-and-rendering/latest/templates/OpenPBR.html
> 取得日: 2026-10-31

Is this page helpful?

# OpenPBR#

OpenPBR is a new material template that provides a comprehensive shader solution for representing the majority of digital material twins. OpenPBR Surface is an open standard hosted by the Academy Software Foundation (ASWF) and is increasingly adopted in Digital Content Creation tools, so is an excellent choice for cross-application material portability and authoring.

## OpenPBR Base#

The OpenPBR Surface model in Omniverse makes use of the reference implementation written in MaterialX. It is translated to MDL using the code generator offered by the MaterialX SDK.

The specification along with a comprehensive description of the model and its parameters is available on the ASWF website at OpenPBR Specification.

This base material is ideal for simple use cases and as a foundation for building material graphs.

## OpenPBR#

This is a more advanced graph-based material with OpenPBR Base as the foundational layer.
It includes additional texture maps for more complex materials, such as clear coats and metallic maps.
This material is ideal for users who want to create more complex materials with additional texture maps.

For portability, the material graph is created as a class at the root of the stage and is instantiated for each material prim.
Overrides to the material parameters are made on the instance, while the master class holds the graph and default parameter values.
Note that if the class is changed, all instances will be updated to reflect the change.
Newly added OpenPBR materials will create a new class that is used as base whenever an existing class is altered.

## OpenPBR in RTX Real-Time 2.0 Mode#

While the RTX – Interactive (Path Tracing) mode supports the full OpenPBR Surface model, there are current limitations in the RTX – Real-Time 2.0 mode.

Effects that are currently not supported are:

- Sheen

- Thin film

Effects that require adjusting the RTX Real-Time 2.0 Settings:

- Subsurface Scattering (SSS) needs to be enabled.

- Refractive materials might require increasing the Max Ray Bounces accurate rendering.

 On this page
