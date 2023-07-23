---
title: Material
date: 2020-11-2 18-34
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

材质是一个数据集，主要功能就是给渲染器提供数据和光照算法。贴图就是其中数据的一部分，根据用途不同，贴图也会被分成不同的类型，比方说 Diffuse Map，Specular Map，Normal Map 和 Gloss Map 等等。另外一个重要部分就是光照模型 Shader ，用以实现不同的渲染效果。

将输入的贴图或者颜色，加上对应的Shader，以及对Shader的特定的参数设置，将这些打包在一起就是一个材质了。之后，我们便可以将材质赋予合适的renderer（渲染器）来进行渲染。

### Shader

所谓 **着色器(Shader)** 实际上就是一小段程序，它负责将输入的网格(Mesh)以指定的方式和输入的贴图或者颜色等组合作用，然后输出，绘图单元可以依据这个输出来将图像绘制到屏幕上。着色器是一种可以精确控制材质球的工具，通过贴图和着色器的配合开发人员可以创造出非常逼真的模型

### 特定类型

Ref: <https://blog.csdn.net/yuyingwin/article/details/80534970>

FX: Lighting and glass effects.( 灯光、玻璃)   
GUI and UI: For user interface graphics.(用于用户界面图形)   
Mobile: Simplified high-performance shader for mobile devices.(针对移动设备的简化的高性能着色器)   
Nature: For trees and terrain.(适用于树木和地形)   
Particles: Particle system effects.(粒子系统特效)   
Skybox: For rendering background environments behind all geometry(用于渲染所有几何背后的背景环境)   
Sprites: For use with the 2D sprite system(用于2D精灵系统)   
Toon: Cartoon-style rendering.(卡通 风格 渲染)   
Unlit: For rendering that entirely bypasses all light & shadowing(渲染完全绕过所有光影)   
Legacy: The large collection of older shaders which were superseded by the Standard Shader(被标准着色器取代的大型着色器集合)

### Standard Shader

#### Rendering Mode

Opaque(不透明的)：是默认设置，适用于没有透明区域的普通固体物体   
Cutout：允许您创建在不透明区域和透明区域之间具有坚硬边缘的透明效果。在这种模式下，没有半透明区域，纹理是100％不透明或不可见的。当使用透明度来创建材质的形状（例如树叶或带孔洞和布块的布料）时，此功能非常有用   
Transparent：适用于渲染逼真的透明材料，如透明塑料或玻璃。在这种模式下，材质本身会采用透明度值（基于纹理的alpha通道和色调的alpha），但反射和照明高光将以完全清晰的方式保持可见状态，就像真正的透明材质一样   
Fade：允许透明度值完全淡出对象，包括任何高光反射或可能有的反射。如果您想要将对象淡入或淡出，则此模式非常有用。它不适合渲染逼真的透明材料，如透明塑料或玻璃，因为反射和高光也会消失

#### Albedo基础贴图

需要一个“纹理”或是多个这个跟你所需要的Shder有关。

#### Metallic金属

Metallic 指出材料是否是金属材质。在金属材料的情况下，Albedo 颜色控制镜面反射的颜色，而大部分光纤将反射未镜面反射。非金属材料将具有与入射光线相同的颜色的镜面反射，并在表面时几乎不会反射。

纹理(Texture) Metallic 分配参数时，Metallic和smoothness 滑块将消失， 材质的金属级别由纹理的红色通道中的值控制(通道一般由 黑、白、灰构成，偏白反射越高)，材质的smoothness级别由纹理的Alpha通道控制.(这以为这 绿色 和 蓝色 通道 被忽略)

  * Specular/Metallic Alpha：曲面每个点的平滑度都是单个值，因此数据只需要图像纹理的单个通道。因此。平滑度数据被假定存储在用于Metallic或specular纹理贴图的相同图像纹理的Alpha通道中

  * Albedo Alpha: 减少纹理的总数，也可以使用不同分辨率的纹理进行Smoothness和Specular/Metallic

#### Map

HeightMap：高度映射图；灰度图。白色区域代表纹理的高区域，黑色代表低区域。白色的部分纹理偏移大。   
OcclussionMap: 遮挡贴图. 提供模型的哪些区域接收 高或低 间接光照的信息。OcclussionMap 是灰度图像. 白色表示应该接受完全间接照明的区域，而黑色表示没有间接照明。   
Emission：发光，控制从表面发射的光的颜色和强度。如果分配给了纹理贴图，则 纹理的全色值将用于发射颜色和亮度。Emission数字之字段仍然存在，可以将其用作乘数来提高或降低材料的整体发光水平。 该处纹理 贴图 必须 背景色是黑色，前景色是非黑色(充满 R,G,B)的才会叠加到Aledo的图片上。None：对象将显示为发射型，但附近物体的照明不受影响 。RealTime：来自此材质的发射光将被添加到场景的实时全局照明计算中，因此附近物体（甚至移动物体）的照明将受到发射光线的影响。 baked：来自这种材料的发射光将被烘焙成场景的静态光照贴图，因此其他附近的静态物体将显示为被该材料点亮，但动态物体不会受到影响。   
DetailMaps：在Aledo纹理贴图上增添细节贴图；DetailMask：给DetailMaps 添加遮罩，限制细节的显示位置 。 

#### 其他参数

  * Specular镜面反射：使用镜面特性模拟外观

  * Smoothness 光滑度：设置物体表面的光滑程度

  * Normal Map法线贴图：描述物体表面的凹凸程度

  * Emission自发光：控制物体表面自发光的颜色和贴图

    * None不影响环境

    * Realtime实时动态改变

  * Tiling平铺：沿着不同的轴，纹理平铺个数

  * Office偏移：滑动纹理

#### Standard(Specular setup)

为经典方法选择此着色器。镜面反射颜色用于控制材料中镜面单摄的颜色和强度。例如：这使得有可能具有漫反射不同的颜色的镜面反射。   
将纹理(Texture)分配给Specular参数时，Specular参数和Smoothness滑块均消失。相反，材质的镜面反射水平由纹理本身的红色，绿色和蓝色通道中的值控制，而光滑度材质的等级由相同纹理的Alpha通道控制。这里，镜面反射和平滑度由颜色和平滑度滑块定义。

tiling缩放：表示贴图在UV坐标的缩放倍数

### 加载Material

```csharp 

Material mat = Resources.Load<Material>("shader path"); 

``` ```csharp 

Material mat = new Material(Shader.Find("shadername")); 

``` 

