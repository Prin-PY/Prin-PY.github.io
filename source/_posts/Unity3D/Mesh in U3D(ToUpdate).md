---
title: Mesh in U3D(ToUpdate)
date: 2020-6-1 17-44
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

Unity3D中的 **Mesh(网格)** 事实上就是我们所说的 **三角网格** 。   
三角网格就是由一系列三角形组成的多边形网格，主要用于模拟复杂物体的表面。

## 数据结构——索引三角网格

用c++语言模拟Unity3D中Mesh数据的存储结构。

```csharp 

//顶点表

//-----------------------------------

struct Vertex{ //由于存储三角形顶点级信息

Vector3 p; 

....... //其他信息 纹理映射坐标 法向量 光照信息 

}; 

//三角形表

//-----------------------------------

struct Triangle{ //保存三角形级信息

int vertex[3]; //三个顶点在顶点列表的索引

}; 

//存放三角网格的结构 维护两个表 定点表和三角形表

struct TriangleMesh{ 

int vertexCount; //顶点数

Vertex *vertexList; //顶点存放链表

int *uv; 

int triangleCount; //三角形数量

Triangle *triangleCount; //存放三角形的链表

........ 

}; 

``` 

### vertices

```csharp 

Vector3[] vertices; //所有的顶点。

``` 

每个三角形面三个顶点，面与面之间不一定共用顶点。   
法向量相同的两个面可以公用顶点，法向量不同的两个面，在同一个位置会分别有两个顶点数据，坐标相同，法向量不同。

每个顶点包含一个3D位置，一般也会包括 **纹理映射坐标(UV坐标)** ，表面 **法向量** ， **光照值** 等附加信息

#### 为何有冗余顶点

正方体6个面，每个面由2个三角形组成，所以共需要36个三角形顶点索引。但是正方体只有8个顶点，为什么需要24个顶点坐标数据呢？

答案是：Unity3D的Mesh.triangles是 **三角形索引数组** ，不仅依靠这个索引值 **索引三角形顶点坐标** ，而且 **索引纹理坐标** ， **索引法线向量** 。即正方体的 **每个顶点都参与了3个平面，而这3个平面的法线向量是不同的** ，该顶点在渲染这3个平面的时候需要索引到不同的法线向量。而由于顶点坐标和法线向量是由同一个索引值triangles[Index]取得的，例如，根据triangles[0],triangles[14],triangles[17]在vertices中索引到的顶点都为（0.5，－0.5，0.5），但是在normals中索引到的法向量值各不相同。这就决定了在正方体中一个顶点，需要有 **3份存储** 。（如果你需要创建其它模型，需要根据实际情况决定顶点坐标的冗余度。实质上顶点坐标的冗余正是方便了法线坐标、纹理坐标的存取。）

### triangles

```csharp 

int[] triangles // a list of triangles that contains indices into the vertex array

``` 

三角形的哪一面可见是由顶点序号的方向来确定的。如果顶点顺序是顺时针方向的话那么三角形是正面可见。

```csharp 

mesh.vertices = new Vector3[] {new Vector3(0, 0, 0), new Vector3(0, 1, 0), new Vector3(1, 1, 0)}; 

mesh.uv = new Vector2[] {new Vector2(0, 0), new Vector2(0, 1), new Vector2(1, 1)}; 

mesh.triangles = new int[] {0, 1, 2}; 

``` 

#### GetBaseVertex

The base vertex can be used to achieve meshes that are larger than 65535 vertices while using 16 bit index buffers.

Unity Mesh的indexFormat[ format of the mesh index buffer data ]默认是uint16，存储的数值最大为65536，也就是说，索引数组(Index buffer)中的索引值最大为65536，顶点数组的大小如果超过65536，就超出了index的表示范围。因此，Unity的解决方法是

  1. 对于这种情况，Submesh设置一个BaseVertex，其索引值为对这个值的偏移值。

  2. 设置indexFormat为32bit的intzhi

### normals

每个顶点对应一个法线，即顶点所在平面的法线

  * 法线是垂直于面的向量。我们通常使用单位长度的法向量，并向量指向面的外部，而不是内部。

  * 法线可以用于确定光线与顶点的夹角。这个细节的使用取决于Shader。

> 作为三角面它永远是平的，因此它不应该需要被提供一个单独的法线信息。然而，我们需要造假。在现实中，顶点是不存在法线的，三角面才有。通过附加自定义顶点法线和三角面插着，我们可以奖状我们有一个平滑的曲面代替一堆平的三角面。这个错觉是令人信服的，只要你不去注意网格锋利的轮廓（锯齿）。

法线用于规定每个顶点，所以我们必须填充另一个向量数组。另一种选择，我们可以依据网格的三角面来计算出法线。

### Tangent

> tangent: 切线，切面，正切

法线贴图在切线空间中定义。   
所以切线是一个三维向量，但是在Unity中它是使用四维向量定义的。第四个值通常是1或者-1，用于控制第三切线空间唯独方向-朝前或朝后,这有助于展示法线贴图，通常用于左右对称的3D模型，像人一样。Untiy的shader执行此计算要求我们使用-1。

#### 法线贴图(Normal Map)

使用颜色值记录了法相向量

### UV坐标(纹理坐标)

UV mapping is the 3D modeling process of projecting a 2D image to a 3D model’s surface for **texture mapping**. 

> The letters “U” and “V” denote the axes of the 2D texture because “X”, “Y”, and “Z” are already used to denote the axes of the 3D object in model space, while “W” (in addition to XYZ) is used in calculating quaternion rotations, a common operation in computer graphics.

#### 工作原理

U3D中的 **纹理贴图的原理** 应该是你的模型坐标进过顶点变化到投影坐标系，然后在接下来的片段着色的时候通过传递过来的UV值用`tex2D(_texName, UV)`来获取颜色值，然后渲染到屏幕上。

UV坐标通常在(0,0)到(1,1)之间，它覆盖了整个纹理。超出范围的坐标将造成 **clamped** 或者 **Tiling** 平铺的效果，这去取决于纹理设置。

#### uv、uv2、uv3、uv4

如果在模型导入时就存在 uv2，uv3，uv4，那么这是因为在建模软件中添加了这些顶点属性。   
uv2通常被用于Lightmap，uv2可以在建模软件中添加，也可以在Unity中通过Generate Lightmap UVs的选项来生成。   
一般来说uv3和uv4的使用较为少见，通常是用来配合特殊的Shader实现特殊的效果。

### colors属性

在一些建模软件中导出的网格模型(Mesh)可能会带有colors属性，描述每个顶点的颜色。有些Shader可以使用这个属性进行运算与着色。然而很多时候colors属性是用不到的， **如Unity标准着色器就不使用这个属性** 。

> Most shaders choose to ignore vertex color, with exception of sprites shader.   
>  大多数着色器选择忽略顶点颜色，但精灵着色器除外   
>  <https://stackoverflow.com/questions/34460587/unity-changing-only-certain-part-of-3d-models-color>

colors属性与tangents属性一样，如果网格顶点拥有该属性，同样会对内存、物理体积和加载性能造成影响。

默认情况下，在3d建模软件中并不会导出Color属性。以3ds max为例，Color通常是通过modifier添加的，因此只需要在导出前将其删除即可。   
去除方法：<https://answer.uwa4d.com/question/5a8f77970b827e2c0bfdcfaf>

> 注意：切忌将不同属性的网格模型拼合在一起。举个例子 ，100个网格模型进行Static Batching，如果99个模型只有Position和UV两种属性，而剩下1个模型函数有Position、UV、Normal、Tangent和Color五种属性。那么引擎在进行拼合时，会将前99个模型的顶点属性补齐，然后再进行拼合。这样无形中会增加大量的内存占用，从而造成不必要的内存浪费。

### 无用属性的去除方法

1.如果有3dmax的源文件，可以直接在3dmax里操作，在那个channelinfo—清掉那个vc   
2.如果只有fbx，或者这类文件太多，可以直接下载一个fbx的sdk，拿里面的例子改一下，生成一个exe。然后在unity里直接调用就行了。   
其实从外包回来的fbx，一般都有问题，要么顶点色，要么会出现uv3、uv4。我这里附上工具和c++、及在unity调用的代码，你可以试一下。如果运行不了，缺dll，你就到网上找一下，多半可以用。 clear_fbx_clr_uv_tool.rar   
注意这个工具会清掉顶点色和uv3、uv4！！   
3.印象中在unity里也可以直接清顶点色，好像是meshfiter那里把colors直接置空，再重新保存回去。

## Unity Mesh API

### 重要属性

(1) vertices 网格顶点数组;   
(2) normals 网格的法线数组;   
(3) tangents 网格的切线数组;   
(4) uv 网格的基础纹理坐标;   
(5) uv2 网格设定的第二个纹理坐标;   
(6) bounds 网格的包围盒;   
(7) Colors 网格的顶点颜色数组;   
(8) triangles 包含所有三角形的顶点索引数组;   
(9) vectexCount 网格中的顶点数量(只读的);   
(10) subMeshCount 子网格的数量，每个材质都有一个独立的网格列表;   
(11) bonesWeights: 每个顶点的骨骼权重;   
(12) bindposes: 绑定姿势，每个索引绑定的姿势使用具有相同的索引骨骼;

### 重要方法

(1) Clear 清空所有的顶点数据和所有的三角形索引;   
(2) RecalculateBounds 重新计算网格的包围盒;   
(3) RecalculateNormals 重新计算网格的法线;   
(4) Optimze 显示优化的网格;   
(5) GetTriangles 返回网格的三角形列表;   
(6) SetTriangles 为网格设定三角形列表;   
(7) CominMeshes组合多个网格到同一个网格;

## Model Import Settings

### Mesh Compression（通常禁用，优化渲染和发布文件大小时启用）

启用网格压缩，unity会按照一定的级别来压缩网格数据，压缩级别越高，网格的精度越低，这对于渲染优化和发布时游戏文件大小的降低很有用，但可能会导致失真。官方的想法是，尽可能的压缩网格，只要模型看起来不至于太奇怪。

### Optimize Mesh

优化网格，如果开启，网格的定点和三角形会按照U3D既定的一套规则重新排序用以提高GPU性能。   
The Optimize Meshes option in a mesh’s import settings will reorganize the vertex data for quicker readability, and sometimes regenerate the low-level rendering style (down to the level of points versus tris versus strips) to optimize the rendering speed of the mesh.

该优化方法也可以在代码中调用：

```csharp 

Mesh mesh = gameObject.GetComponent<MeshFilter>().mesh; 

mesh.Optimize(); 

``` 

This function causes the geometry and vertices of the mesh to be reordered internally in an attempt to improve vertex cache utilisation on the graphics hardware and thus rendering performance.   
This operation can take a few seconds or more for complex meshes and should only be used where **the ordering of the geometry and vertices is not significant** as both will change.   
理论上如果模型对顶点和面片顺序没有要求的话，不会导致显示问题。

## 相关组件(Components)

### MeshFiler组件

MeshFilter 这个组件记录了你想要展示的网格数据

### MeshRender组件

MeshRenderer 使用这个组件告诉网格如何渲染，比如使用哪个材质球，是否接受阴影和其他设置。

## Mesh, SubMesh与Material

在Unity3D中一个Mesh里可以有多个SubMesh，引擎在渲染的时候，每个SubMesh都需要对应一个Material材质球来匹配做渲染。当Mesh有多个SubMesh时，Unity会默认Mesh有相应数量的Materials，Mesh与Material按照相应的顺序一一对应。

![Alt text](Mesh in U3D\(ToUpdate\)
_files/1618210128127.png)

![Alt text](Mesh in U3D\(ToUpdate\)
_files/1618210138491.png)

如果mesh没有submesh的话，多个材质球就是会渲染多遍，使用的对象就是当前的这个mesh。

### 拆分SubMesh的意义

  1. 3D模型制作人员在制作模型的时候，希望一个模型中一部分Mesh用一种材质球来表现效果，另一部分Mesh则用另一种材质球来表现效果，这时就需要将模型拆分开来。因为一个Mesh只能对应一个材质球做渲染，一个材质球只能表现一种效果，当他们需要表现两种完全不同的效果时就需要拆分。

  2. 模型中的某部分的贴图，在众多模型中共同使用的频率比较高，为了不重复制作以及减少重复劳动，那么就会让原本可以整体的模型单独拆分出来一部分公共材质的部分让它们都使用同一个材质球。

  3. 在制作动画时，由于动画过于复杂导致如果使用同一个模型去表现的话，骨骼数量就会成倍增加。为了能更好的表现动画，也为了能更节省骨骼的使用量，拆分出一部分模型让他们单独成为模型动画的一部分。

拥有多个SubMesh一样可以有动画，另外它还能针对不同部分的Mesh选择有个性化的材质球来表现效果，从功能上来看比单个Mesh要灵活的多。

### 多个SubMesh的缺点

  * 由于每个SubMesh都多出了材质球，导致SubMesh越多，增加的Drawcall也越多。

  * Mesh中存在多个SubMesh，在动作和拆分材质球渲染上确实有很好的优势，但无法与其他Mesh合并，导致优化的一个重要环节被阻断。

### CombineMesh in Unity

```csharp 

void CombineMesh()

{ 

MeshFilter[] mfs = GetComponentsInChildren<MeshFilter>(); 

CombineInstance[] combine = new CombineInstance[mfs.Length]; 

Mesh newMesh = new Mesh(); 

for(int i= 0; i<mfs.Length; i++) 

{ 

combine[i].mesh = mfs[i].sharedMesh; 

combine[i].transform = mfs[i].transform.localToWorldMatrix; 

combine[i].subMeshIndex = i;//标识Material的索引位置，可以为0，1，2等

} 

newMesh.CombineMeshes(combine); 

AssetDatabase.CreateAsset(newMesh, "Assets/TestTRS/NewMesh.mesh"); 

} 

``` 

## Mesh的渲染

### Mesh的坐标与bounds

  * 每个Mesh都有Bounds属性，表示Mesh的包围盒。

  * Unity一个节点在Scene界面的坐标原点，取的是能包含所有子物体的bounds的bounds的中心。也就是对所有子物体的bounds进行Encapsulate后，求得一个大Bounds，取其中心。

  * 修改Mesh的vertices坐标后，Unity并不会重新计算bounds。将修改后的Mesh创建出来，Unity会采用修改前的bounds来计算坐标原点的位置。

![Alt text](Mesh in U3D\(ToUpdate\)
_files/1616555830226.png)   
**因此，修改了Mesh的vertices属性后，需要调用RecalculateBounds才能保证包围盒的正确性。**

![Alt text](Mesh in U3D\(ToUpdate\)
_files/1616555982837.png)

#### Mesh顶点整体偏移问题及Matrix4x4修正

如图，世界空间的坐标原点是Cube所在的位置，而将左边的物体A的Position设置为(0, 0, 0)，看起来却回不到世界坐标原点的位置。

![Alt text](Mesh in U3D\(ToUpdate\)
_files/1616556303175.png)

![Alt text](Mesh in U3D\(ToUpdate\)
_files/1616556368115.png)   
实质上，该GameObject的坐标值确实是世界坐标的原点，而由于Mesh的所有顶点都相对局部坐标原点有一个偏移，因此，Mesh显示的位置不在坐标原点，并且Scene界面的显示的模型坐标系采取的是Mesh的bounds的中心。

修正方法：修改Mesh的vertices，将顶点位置改变，是顶点的bounds的中心回到(0, 0, 0)。

求得当前的bounds的中心center，该center是相对坐标原点有一定的偏移的，使用`Matrix4x4.Translate(-center)`，即可将所有顶点都进行平移，抵消之前的偏移。

注意：Translate之后，需要重新计算bounds。

```csharp 

void ModifyMesh()

{ 

Mesh mesh = GetComponent<MeshFilter>().sharedMesh; 

mesh.RecalculateBounds(); 

Vector3 center = mesh.bounds.center; 

var m = Matrix4x4.Translate(-center); 

Vector3[] oldVertices = mesh.vertices; 

Vector3[] newVertices = new Vector3[oldVertices.Length]; 

for(int i=0; i<oldVertices.Length; i++) 

{ 

newVertices[i] = m.MultiplyPoint(oldVertices[i]); 

} 

mesh.vertices = newVertices; 

mesh.RecalculateBounds(); 

GetComponent<MeshFilter>().sharedMesh = mesh; 

AssetDatabase.CreateAsset(mesh, "Assets/MeshModified.mesh"); 

} 

``` 

## Mesh编程

### 画面片

```csharp 

using UnityEngine; 

using UnityEditor; 

using System.Collections; 

public class GenMesh

{ 

[MenuItem("MeshEditor/GenMesh")] 

static public void GenMeshM()

{ 

Mesh m1 = CreateRect(); 

AssetDatabase.CreateAsset(m1, "Assets/models/m1.asset"); 

} 

public static Mesh CreateRect()

{ 

Mesh mesh = new Mesh(); 

int particleNum = 10; 

//顶点坐标

Vector3[] verts = new Vector3[4 * particleNum]; 

//uv坐标

Vector2[] uvs = new Vector2[4 * particleNum]; 

//三角形索引

int[] tris = new int[2 * 3 * particleNum]; 

Vector3 position; 

for (int i = 0; i < particleNum; i++) 

{ 

int i4 = i * 4; 

int i6 = i * 6; 

position.x = 5 * i; 

position.y = 5 * i; 

position.z = 0; 

//顶点坐标

verts[i4 + 0] = position; 

verts[i4 + 1] = position + new Vector3(2, 0, 0); 

verts[i4 + 2] = position + new Vector3(2, 2, 0); 

verts[i4 + 3] = position + new Vector3(0, 2, 0); 

//四个顶点在UV坐标系中的位置

uvs[i4 + 0] = new Vector2(0.0f, 0.0f); 

uvs[i4 + 1] = new Vector2(1.0f, 0.0f); 

uvs[i4 + 2] = new Vector2(1.0f, 1.0f); 

uvs[i4 + 3] = new Vector2(0.0f, 1.0f); 

//顺时针绘制三角形0 1 2 / 0 2 3

tris[i6 + 0] = i4 + 0; 

tris[i6 + 1] = i4 + 1; 

tris[i6 + 2] = i4 + 2; 

tris[i6 + 3] = i4 + 0; 

tris[i6 + 4] = i4 + 2; 

tris[i6 + 5] = i4 + 3; 

} 

mesh.vertices = verts; 

mesh.triangles = tris; 

mesh.uv = uvs; 

mesh.RecalculateBounds(); 

return mesh; 

} 

} 

``` 

### 画圆

```csharp 

#region 画圆

/// <summary>

/// 画圆

/// </summary>

/// <param name="radius">圆的半径</param>

/// <param name="segments">圆的分割数</param>

/// <param name="centerCircle">圆心得位置</param>

void DrawCircle(float radius, int segments, Vector3 centerCircle)

{ 

gameObject.AddComponent<MeshFilter>(); 

gameObject.AddComponent<MeshRenderer>(); 

gameObject.GetComponent<MeshRenderer>().material = mat; 

//顶点

Vector3[] vertices = new Vector3[segments + 1]; 

vertices[0] = centerCircle; 

float deltaAngle = Mathf.Deg2Rad * 360f / segments; 

float currentAngle = 0; 

for (int i = 1; i < vertices.Length; i++) 

{ 

float cosA = Mathf.Cos(currentAngle); 

float sinA = Mathf.Sin(currentAngle); 

vertices[i] = new Vector3(cosA * radius + centerCircle.x, sinA * radius + centerCircle.y, 0); 

currentAngle += deltaAngle; 

} 

//三角形

int[] triangles = new int[segments * 3]; 

for (int i = 0, j = 1; i < segments * 3 \- 3; i += 3, j++) 

{ 

triangles[i] = 0; 

triangles[i + 1] = j + 1; 

triangles[i + 2] = j; 

} 

triangles[segments * 3 \- 3] = 0; 

triangles[segments * 3 \- 2] = 1; 

triangles[segments * 3 \- 1] = segments; 

Vector2[] uvs = new Vector2[vertices.Length]; 

for (int i = 0; i < vertices.Length; i++) 

{ 

uvs[i] = new Vector2(vertices[i].x / radius / 2 \+ 0.5f, vertices[i].y / radius / 2 \+ 0.5f); 

} 

Mesh mesh = GetComponent<MeshFilter>().mesh; 

mesh.Clear(); 

mesh.vertices = vertices; 

mesh.triangles = triangles; 

mesh.uv = uvs; 

} 

#endregion

``` 

### 画圆环

```csharp 

#region 画圆

/// <summary>

/// 画圆

/// </summary>

/// <param name="radius">圆的半径</param>

/// <param name="segments">圆的分割数</param>

/// <param name="centerCircle">圆心得位置</param>

void DrawCircle(float radius, int segments, Vector3 centerCircle)

{ 

gameObject.AddComponent<MeshFilter>(); 

gameObject.AddComponent<MeshRenderer>(); 

gameObject.GetComponent<MeshRenderer>().material = mat; 

//顶点

Vector3[] vertices = new Vector3[segments + 1]; 

vertices[0] = centerCircle; 

float deltaAngle = Mathf.Deg2Rad * 360f / segments; 

float currentAngle = 0; 

for (int i = 1; i < vertices.Length; i++) 

{ 

float cosA = Mathf.Cos(currentAngle); 

float sinA = Mathf.Sin(currentAngle); 

vertices[i] = new Vector3(cosA * radius + centerCircle.x, sinA * radius + centerCircle.y, 0); 

currentAngle += deltaAngle; 

} 

//三角形

int[] triangles = new int[segments * 3]; 

for (int i = 0, j = 1; i < segments * 3 \- 3; i += 3, j++) 

{ 

triangles[i] = 0; 

triangles[i + 1] = j + 1; 

triangles[i + 2] = j; 

} 

triangles[segments * 3 \- 3] = 0; 

triangles[segments * 3 \- 2] = 1; 

triangles[segments * 3 \- 1] = segments; 

Vector2[] uvs = new Vector2[vertices.Length]; 

for (int i = 0; i < vertices.Length; i++) 

{ 

uvs[i] = new Vector2(vertices[i].x / radius / 2 \+ 0.5f, vertices[i].y / radius / 2 \+ 0.5f); 

} 

Mesh mesh = GetComponent<MeshFilter>().mesh; 

mesh.Clear(); 

mesh.vertices = vertices; 

mesh.triangles = triangles; 

mesh.uv = uvs; 

} 

#endregion

``` 

### Mesh顶点编辑器

摘自：<https://gameinstitute.qq.com/community/detail/129174>   
思路：获取mesh上的所有顶点，然后在每个顶点位置创建一个控制点，控制点可以是任意你喜欢的物体，通过判断控制点的位置信息来修改mesh的顶点位置。   
把每个顶点的坐标转为字符串，使用该坐标的字符串作为 **key** 来把 **控制点** 与 **顶点数据** 联系起来。

* * *

控制点：

```csharp 

using System.Collections; 

using System.Collections.Generic; 

using UnityEngine; 

public class MeshEditorPoint : MonoBehaviour ｛ 

//顶点id，（顶点初始位置转字符串）

[HideInInspector] public string pointid; 

//记录坐标点上一次移动的位置，用于判断控制点是否移动

[HideInInspector] private Vector3 lastPosition; 

public delegate void MoveDelegate(string pid,Vector3 pos); 

//控制点移动时的回调

public MoveDelegate onMove = null; 

// Use this for initialization

void Start () ｛

lastPosition = transform.position; 

｝ 

// Update is called once per frame

void Update () ｛

if(transform.position != lastPosition)｛

if(onMove != null) onMove(pointid, transform.localPosition); 

lastPosition = transform.position; 

｝ 

｝ 

｝ 

``` 

* * *

顶点编辑器

```csharp 

using System.Collections; 

using System.Collections.Generic; 

using UnityEngine; 

using System.Text; 

using System; 

public class ModelMeshEditor : MonoBehaviour ｛ 

//控制点的大小

public float pointScale = 1.0f; 

private float lastPointScale = 1.0f; 

Mesh mesh; 

//顶点列表

List<Vector3> positionList = new List<Vector3>(); 

//顶点控制物体列表

List<GameObject> positionObjList = new List<GameObject>(); 

/// <summary>

/// key:顶点字符串

/// value:顶点在列表中的位置

/// </summary>

Dictionary<string, List<int>> pointmap = new Dictionary<string, List<int>>(); 

// Use this for initialization

void Start () ｛

lastPointScale = pointScale; 

mesh = GetComponent<MeshFilter>().sharedMesh; 

CreateEditorPoint(); 

｝ 

//创建控制点

public void CreateEditorPoint()｛

positionList = new List<Vector3>(mesh.vertices); 

for (int i = 0; i < mesh.vertices.Length; i++) 

｛ 

string vstr = Vector2String(mesh.vertices[i]); 

if(!pointmap.ContainsKey(vstr))｛ 

pointmap.Add(vstr,new List<int>()); 

｝ 

pointmap[vstr].Add(i); 

｝ 

foreach (string key in pointmap.Keys) 

｛ 

GameObject editorpoint = (GameObject)Resources.Load("Prefabs/MeshEditor/MeshEditorPoint"); 

editorpoint = Instantiate(editorpoint); 

editorpoint.transform.parent = transform; 

editorpoint.transform.localPosition = String2Vector(key); 

editorpoint.transform.localScale = new Vector3(1f, 1f, 1f); 

MeshEditorPoint editorPoint = editorpoint.GetComponent<MeshEditorPoint>(); 

editorPoint.onMove = PointMove; 

editorPoint.pointid = key; 

positionObjList.Add(editorpoint); 

｝ 

｝ 

//顶点物体被移动时调用此方法

public void PointMove(string pointid,Vector3 position)｛

if(!pointmap.ContainsKey(pointid))｛

return; 

｝ 

List<int> _list = pointmap[pointid]; 

for (int i = 0; i < _list.Count; i ++)｛ 

positionList[_list[i]] = position; 

｝ 

mesh.vertices = positionList.ToArray(); 

mesh.RecalculateNormals(); 

｝ 

// Update is called once per frame

void Update () ｛

//检测控制点尺寸是否改变

if (Math.Abs(lastPointScale - pointScale) > 0.1f)｛

lastPointScale = pointScale; 

for (int i = 0; i < positionObjList.Count; i ++)｛ 

positionObjList[i].transform.localScale = new Vector3(pointScale, pointScale, pointScale); 

｝ 

｝ 

｝ 

string Vector2String(Vector3 v)｛

StringBuilder str = new StringBuilder(); 

str.Append(v.x).Append(",").Append(v.y).Append(",").Append(v.z); 

return str.ToString(); 

｝ 

Vector3 String2Vector(string vstr)

｛

try｛

string[] strings = vstr.Split(','); 

return new Vector3(float.Parse(strings[0]), float.Parse(strings[1]), float.Parse(strings[2])); 

｝catch(Exception e)｛ 

Debug.LogError(e.ToString()); 

return Vector3.zero; 

｝ 

｝ 

｝ 

``` 

## 相关知识

### 3D建模软件

1:Autodesk 3D Studio Max 支持mac os windows;   
2: Autodesk 3D Maya 支持windows   
3: Cinema4D 支持mac os windows   
4: Blender 开源跨平台的全能三维制作软件, 支持mac os windows, linux;   
5: Cheetah3D: 支持mac os   
6: Unity与建模软件的单位比例:

软件 | 内部米 | 导入unity后的尺寸/m | 与Unity单位的比例关系  
---|---|---|---  
3Dmax | 1 | 0.01 | 100:1  
Maya | 1 | 0.01 | 1:100  
Cinema 4D | 1 | 0.01 | 1:100  
Light Wave | 1 | 0.01 | 100:1  
  
## Refs

<https://www.cnblogs.com/zhanghaipeng-Unity3D/p/4714973.html>   
<https://blog.csdn.net/qq_29579137/article/details/77369734>   
<https://www.bbsmax.com/A/QV5ZQvObJy/>   
<https://blog.csdn.net/nanggong/article/details/54728823>   
<https://answer.uwa4d.com/question/5a8f77970b827e2c0bfdcfaf>

<http://www.luzexi.com/2018/08/03/Unity3D%E9%AB%98%E7%BA%A7%E7%BC%96%E7%A8%8B%E4%B9%8B%E8%BF%9B%E9%98%B6%E4%B8%BB%E7%A8%8B-3D%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8A%A8%E7%94%BB2>

