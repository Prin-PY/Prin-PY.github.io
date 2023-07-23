---
title: Camera & Screen
date: 2020-7-21 14-55
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Screen

```csharp 

Screen.autorotateToLandscapeLeft = true; //自动旋转屏幕为向左 

Screen.autorotateToLandscapeRight = false; //自动旋转屏幕向右 

Screen.autorotateToPortrait = true; //自动旋转为纵向 

Screen.autorotateToPortraitUpsideDown = true; //自动旋转为纵向倒置 

print(Screen.currentResolution); //当前屏幕分辨率 

Screen.fullScreen = !Screen.fullScreen; //是否全屏 

print(Screen.height); //屏幕分辨率的高度 

Screen.lockCursor = !Screen.lockCursor; //是否锁定光标 

Screen.showCursor = !Screen.showCursor; //是否显示光标 

Screen.orientation = ScreenOrientation.Landscape; //屏幕取向 

Resolution[] resolutions = Screen.resolutions; //显示器支持的所有全屏分辨率 

foreach (Resolution res in resolutions) 

{ 

print(res.width + " " \+ res.height); 

} 

//参数1宽， 参数 2高， 参数3是否全屏 

Screen.SetResolution(resolutions[0].width, resolutions[0].height, true); 

``` 

## Camera

### View Frustum(视锥体)相关参数图解

#### 透视相机(Perspective)

![Alt text](assets/Camera%20&%20Screen/20180524230527942.jpg)

![Alt text](assets/Camera%20&%20Screen/20180524232513244.jpg)
   
nearClipPalneHeight(近截平面的高)=2*Near*tan(FOV/2)   
farClipPlaneHeight(远截平面)=2*Far*tan(FOV/2)   
Aspect(摄像机的纵横比)=nearClipPlaneWidth/nearClipPalneHeight=farClipPlaneWidth/farClipPlaneHeight

#### 正交相机(Orthographic)

![Alt text](assets/Camera%20&%20Screen/20180524230615918.jpg)

![Alt text](assets/Camera%20&%20Screen/20180524231957314.jpg)

nearClipPlaneHeight=2*Size   
farClipPlaneHeight=nearClipPlaneHeight   
Aspect=nearClipPlaneHeight/farClipPlaneWidth=nearClipPlaneHeight/nearClipPalneWidth

### 属性（Inspector可见）

#### Clear Flags

清除标识：确定了屏幕哪些部分将被清除，方便多个摄像机画不同的游戏元素

Skybox ：   
天空盒：这是默认设置。屏幕上的任何空的部分将显示当前相机的天空盒。   
如果当前的相机没有设置天空盒，它会默认在渲染设置（Render Settings ）选择天空盒   
Solid Color ：   
纯色，屏幕上的空白部分将显示当前摄像机的背景色   
Depth Only ：   
深度相机，只渲染采集到的画面   
如果你想绘制一个玩家的枪，又不让它内部环境被裁剪，你会设置深度为0的相机绘制环境，   
和另一个深度为1的相机单独绘制武器。武器相机的清除标志（Clear Flags ）应设置 为depth only。   
Don’t Clear ：   
不清除，此模式不清除颜色或深度缓存。每帧的渲染画面叠加在上一帧画面之上。

#### Background:背景色

#### Culling Mask

Culling Mask:包含或省略要由相机呈现的对象层。在检查器中将图层分配给您的对象。   
Nothing:什么层都不剔除   
Everything:什么层都剔除   
Default:默认层剔除   
TransparentFX:隐形层,系统不会渲染贴图和模型   
Ignore Raycast:射线层剔除   
Water:水层剔除   
UI：UI层剔除

原理：   
清除标记至少与渲染管线的两个步骤有关：深度测试和颜色混合。屏幕上每一个像素都至少有两个信息， **颜色信息** 和 **深度信息** ，当新的一帧的像素信息在屏幕呈现之前，先会将 **上一帧的缓存信息清除** 某些部分（或者不清除任何信息），然后和 **剩下的信息做深度测试和颜色混合得到最终结果** （还有其他步骤，这里只讨论着两个），把结果放在帧缓存区并显示在屏幕上。

深入理解见：<https://blog.csdn.net/mingyi2106/article/details/81606959>

#### Projection

切换相机的功能来模拟透视。

Perspective(透视): 相机将完整地呈现透视物体。拍摄角度为0-180°（最高）   
透视模式下，有远小近大的效果。呈现3D效果   
**Field of View** : 设置为“透视”时，“相机”的视口大小。

Orthographic(正交): 相机将统一渲染对象，没有视角。注：正交模式下不支持延迟渲染。正向渲染总是被使用。   
物体在视口的代销只与正交视口的大小有关，与摄像机到物体的距离无关，主要呈现2D效果。   
**Size** :设置为“正交”时，“相机”的视口大小。

orthographic :摄像机投影模式。若值为true,正交模式，反之投影模式。

#### Clipping Planes

剪切平面，从相机到开始和停止渲染的距离。   
Near ：相对于相机的最近点将出现绘图。   
Far ：相对于相机的最远点将出现绘图。

#### ViewportRect

视口矩形 四个值指示屏幕上的相机视图将被绘制的位置。在视口坐标中测量（值为0-1）。

#### Depth

相机的位置按照画图顺序。具有较大值的相机将被绘制在具有较小值的相机之上。

#### Rendering Path

渲染路径 ：定义什么绘制方法被用于相机的选项   
Use Graphics Settings 使用玩家设置：在玩家设置（Player Settings.）相机使用哪个渲染路径。   
Forward 用正向光照渲染：所有对象每材质渲染只渲染一次,快速渲染。基于着色器的渲染路径。支持逐像素计算光照（包括法线贴图和灯光Cookies）和来自一个平行光的实时阴影。   
Deferred 延迟照明：所有物体将在无光照的环境渲染一次，然后在渲染队列尾部将物体的光照一起渲染出来。支持实时阴影，计算消耗大，对硬件要求高，不支持移动设备，仅专业版可用。   
Legacy Vertex Lit :使用顶点光照。最低消耗的渲染路径，不支持实时阴影，适用于移动及老式设备。   
Legacy Deferred : 旧的延迟光照 

#### Target Texture

目标纹理:渲染纹理 （Render Texture）包含相机视图输出。这会使相机渲染在屏幕上的能力被禁止。可用于实现画中画或者画面特效。

#### Occlusion Culling（遮挡剔除）

是否剔除物体背向摄像机的部分

#### 其他

  * Allow HDR:高动态光照渲染，启动相机高动态范围渲染功能。让场景更真实。

  * Allow MSAA: 这台相机应该使用MSAA渲染目标吗？如果当前质量设置MSAA级别支持，将只使用MSAA。

  * Allow Dynamic Resolution：动态分辨率缩放。   
如果相机使用动态分辨率渲染，则为true，否则为false。即使此属性为true，动态分辨率也只能在当前图形设备支持的情况下使用。

  * Target Display:设置此摄像机的目标显示。   
此设置使摄像机呈现在指定的显示中。显示器（例如监视器）支持的最大数目是8. 

### 属性（Inspector不可见）

#### aspect ：Camera视口的宽高比（可获取，可设置）

获取或者设置Camera视口的宽高比例值。例如：camera.aspect =2.0f,则视口的宽度、高度 = 2.0f，当硬件显示器屏幕的宽度与高度比例不为2.0f时,视图的显示将会发生变形。aspect只处理摄像机camera可以看到的视图的宽高比例，而硬件显示屏的作用只是把摄像机camera看到的内容显示出来，当硬件显示屏的宽高比例与aspect的比例值不同时，视图将发生变形。

#### pixelRect

设置Camera被渲染到屏幕中的坐标位置。以实际像素大小来设置显示视口的位置。如下图：A为原始平面大小，B为变换后的视口大小，则X0的值为视口右移的像素大小，Y0的值为视口上移的像素大小，w为Camera.pixelWidth,h的值为Camera.pixelHeight。这里要注意：Screen.width和Screen.height为模拟硬件屏幕的宽高值，不随Camera.pixelWidth和Camera.pixelHeight的改变而改变。

```csharp 

public class PixelRect : MonoBehaviour

{ 

int which_change = -1; 

float temp_x = 0.0f, temp_y = 0.0f; 

void Update()

{ 

//Screen.width和Screen.height为模拟硬件屏幕的宽高值,

//其返回值不随camera.pixelWidth和camera.pixelHeight的改变而改变

Debug.Log("Screen.width:" \+ Screen.width); 

Debug.Log("Screen.height:" \+ Screen.height); 

Debug.Log("pixelWidth:" \+ Camera.main.pixelWidth); 

Debug.Log("pixelHeight:" \+ Camera.main.pixelHeight); 

//通过改变Camera的坐标位置而改变视口的区间

if (which_change == 0) 

{ 

if (Camera.main.pixelWidth > 1.0f) 

{ 

temp_x += Time.deltaTime * 20.0f; 

} 

//取消以下注释察看平移状况

//if (Camera.main.pixelHeight > 1.0f)

//{

// temp_y += Time.deltaTime * 20.0f;

//}

Camera.main.pixelRect = new Rect(temp_x, temp_y, Camera.main.pixelWidth, Camera.main.pixelHeight); 

} 

//通过改变Camera的视口宽度和高度来改变视口的区间

else if (which_change == 1)

{ 

if (Camera.main.pixelWidth > 1.0f) 

{ 

temp_x = Camera.main.pixelWidth - Time.deltaTime * 20.0f; 

} 

//取消以下注释察看平移状况

//if (camera.pixelHeight > 1.0f)

//{

// temp_y = camera.pixelHeight - Time.deltaTime * 20.0f;

//}

Camera.main.pixelRect = new Rect(0, 0, temp_x, temp_y); 

} 

} 

void OnGUI()

{ 

if (GUI.Button(new Rect(10.0f, 10.0f, 200.0f, 45.0f), "视口改变方式1")) 

{ 

Camera.main.rect = new Rect(0.0f, 0.0f, 1.0f, 1.0f); 

which_change = 0; 

temp_x = 0.0f; 

temp_y = 0.0f; 

} 

if (GUI.Button(new Rect(10.0f, 60.0f, 200.0f, 45.0f), "视口改变方式2")) 

{ 

Camera.main.rect = new Rect(0.0f, 0.0f, 1.0f, 1.0f); 

which_change = 1; 

temp_x = 0.0f; 

temp_y = Camera.main.pixelHeight; 

} 

if (GUI.Button(new Rect(10.0f, 110.0f, 200.0f, 45.0f), "视口还原")) 

{ 

Camera.main.rect = new Rect(0.0f, 0.0f, 1.0f, 1.0f); 

which_change = -1; 

} 

} 

} 

``` 

### 实用案例

#### cameraToWorldMatrix : 变换矩阵

```csharp 

using UnityEngine; 

public class cameratoworldmatrix : MonoBehaviour { 

// Use this for initialization

void Start () { 

Debug.Log("Camera旋转前位置" \+ transform.position); 

Matrix4x4 m = Camera.main.cameraToWorldMatrix; 

// 向量的位置转换为世界坐标中的位置

//v3 的值为沿着Camera局部坐标系的-z轴方向前移5个单位的位置在世界坐标系中的位置

Vector3 v3 = m.MultiplyPoint(Vector3.forward * 5.0f); 

//v4 的值为沿着Camera世界坐标系的-z轴方向前移5个单位的位置在世界坐标系中的位置

Vector3 v4 = m.MultiplyPoint(transform.forward * 5.0f); 

Debug.Log("旋转前，V3坐标值："+v3); 

Debug.Log("旋转前，V4坐标值："+v4); 

// 将摄像机沿着Y轴正向旋转90度（此时摄像机局部坐标系的z轴方向和世界坐标的X轴方向一致），

transform.Rotate(Vector3.up * 90f); 

m = Camera.main.cameraToWorldMatrix; 

v3 = m.MultiplyPoint(Vector3.forward * 5.0f); 

v4 = m.MultiplyPoint(transform.forward * 5.0f); 

Debug.Log("旋转后， v3坐标值"+v3); 

Debug.Log("旋转后， v4坐标值"+v4); 

} 

} 

``` 

#### CullingMask设置

CullingMask 按层渲染，此属性用于按层（GameObject.layer）有选择性地渲染场景中的物体。通过cullingMask可以使得当前摄像机有选择性地渲染场景中的部分物体，默认cullingMask =-1即渲染场景中的任何物体，cullingMask = 0时不渲染场景中的任何物体。若只渲染2,3,4，可以使用cullingMask = （1<<2）+ (1<<3)+(1<<4)来进行。

#### eventMask属性（待研究）

按层响应事件，选择哪个层（layer）的物体可以响应鼠标事件

必须满足两个条件：

  1. 物体在摄像机的视野范围内。

  2. 在2的layer次方的值与eventMask进行运算（&）后结果仍为2的layer次方的值，如：defalult ,layer值为0，2的0次方=1，如果1与eventMask进行与运算后扔为1，则此物体响应鼠标事件。由于EventMask为奇数时，与1的与运算结果都为1，所以若物体层为defalut并且eventMask为奇数时物体会响应鼠标事件。

如果想要多个不同层的物体响应鼠标事件，则需要把所有层的2的layer次方值相加，再与eventMask做与运算。例如，2个物体，layer值分贝为1,3，当event与9进行与运算后结果仍为9，则这两个物体都会响应鼠标事件。

此属性有一个特殊情况，但固体layer选择IgnoreRaycast(其为系统内置，值为2)时，无论EventMask值为多少，物体都无法响应鼠标事件。

```csharp 

using UnityEngine; 

using System.Collections; 

public class EventMask_ts : MonoBehaviour

{ 

bool is_rotate = false;//控制物体旋转

public Camera c;//指向场景中摄像机

//记录摄像机的eventMask值，可以在程序运行时在Inspector面板中修改其值的大小

public int eventMask_now = -1; 

//记录当前物体的层

int layer_now; 

int layerTemp;//记录2的layer次方的值

int ad;//记录与运算（&）的结果

string str = null; 

void Update()

{ 

//记录当前对象的层，可以在程序运行时在Inspector面板中选择不同的层

layer_now = gameObject.layer; 

//求2的layer_now次方的值

layerTemp= (int)Mathf.Pow(2.0f, layer_now); 

//与运算（&）

ad = eventMask_now & layerTemp; 

c.eventMask = eventMask_now; 

//当is_rotate为true时旋转物体

if (is_rotate) 

{ 

transform.Rotate(Vector3.up * 15.0f * Time.deltaTime); 

} 

} 

//当鼠标左键按下时，物体开始旋转

void OnMouseDown()

{ 

is_rotate = true; 

} 

//当鼠标左键抬起时，物体结束旋转

void OnMouseUp()

{ 

is_rotate = false; 

} 

void OnGUI()

{ 

GUI.Label(new Rect(10.0f, 10.0f, 300.0f, 45.0f), "当前对象的layer值为：" \+ layer_now + " , 2的layer次方的值为" \+ layerTemp); 

GUI.Label(new Rect(10.0f, 60.0f, 300.0f, 45.0f), "当前摄像机eventMask的值为：" \+ eventMask_now); 

GUI.Label(new Rect(10.0f, 110.0f, 500.0f, 45.0f), "根据算法，当eventMask的值与" \+ layerTemp+ "进行与运算（&）后， 若结果为" \+ tp + "，则物体相应OnMousexxx方法，否则不响应！"); 

if (ad == tp) 

{ 

str = " ,所以物体会相应OnMouseDown方法！"; 

} 

else

{ 

str = " ,所以物体不会相应OnMouseDown方法！"; 

} 

GUI.Label(new Rect(10.0f, 160.0f, 500.0f, 45.0f), "而当前eventMask与" \+ layerTemp+ "进行与运算（&）的结果为" \+ ad + str); 

} 

} 

``` 

#### LayerCullDistances:层消隐的距离

摄像机可以通过基于层（GameObject.layer）的方式来设置不同层物体的消隐距离，但这个距离必须小于或者等于摄像机的farClipPlane才有效。

#### layerCullSpherical:基于球面距离剔除

基于球面距离的剔除方式。属性默认为false，即不使用球面剔除，表示只要有一点没有超出物体所在层的远视口平面，物体就是可见的。当设置此属性为True时，只要物体的世界坐标点Position与摄像机的距离大于所在层的剔除距离，物体就不可见。

#### Shader相关

  * RenderWithShader:使用其他shader渲染   
使用指定shader来代替当前物体的shader渲染一帧。当replacementTag为空时会替换视口中所有物体的shader

  * SetReplacementShader 使用指定的shader来替换物体当前的shader,被替换后每一帧都会替换shader来渲染物体,与上面的方法刚好不同。

```csharp 

public class RenderWithShader : MonoBehaviour

{ 

bool is_use = false; 

void OnGUI()

{ 

if (is_use) 

{ 

//使用高光shader：Specular来渲染Camera

Camera.main.RenderWithShader(Shader.Find("Specular"), "RenderType"); 

} 

if (GUI.Button(new Rect(10.0f, 10.0f, 300.0f, 45.0f), "使用RenderWithShader启用高光")) 

{ 

//RenderWithShader每调用一次只渲染一帧，所以不可将其直接放到这儿

//camera.RenderWithShader(Shader.Find("Specular"), "RenderType");

is_use = true; 

} 

if (GUI.Button(new Rect(10.0f, 60.0f, 300.0f, 45.0f), "使用SetReplacementShader启用高光")) 

{ 

//SetReplacementShader方法用来替换已有shader，调用一次即可

Camera.main.SetReplacementShader(Shader.Find("Specular"), "RenderType"); 

is_use = false; 

} 

if (GUI.Button(new Rect(10.0f, 110.0f, 300.0f, 45.0f), "关闭高光")) 

{ 

Camera.main.ResetReplacementShader(); 

is_use = false; 

} 

} 

} 

``` 

#### 更多

见：<https://www.jianshu.com/p/547ef7f4a313>

## 编辑器模式下修改屏幕分辨率

```csharp 

#if UNITY_EDITOR

using System; 

using System.Reflection; 

using UnityEditor; 

using UnityEngine; 

public static class GameViewUtils

{ 

static object gameViewSizesInstance; 

static MethodInfo getGroup; 

static GameViewUtils()

{ 

// gameViewSizesInstance = ScriptableSingleton<GameViewSizes>.instance;

var sizesType = typeof(Editor).Assembly.GetType("UnityEditor.GameViewSizes"); 

var singleType = typeof(ScriptableSingleton<>).MakeGenericType(sizesType); 

var instanceProp = singleType.GetProperty("instance"); 

getGroup = sizesType.GetMethod("GetGroup"); 

gameViewSizesInstance = instanceProp.GetValue(null, null); 

} 

public enum GameViewSizeType 

{ 

AspectRatio, FixedResolution 

} 

[MenuItem("Test/AddSize")] 

public static void AddTestSize()

{ 

AddCustomSize(GameViewSizeType.AspectRatio, GameViewSizeGroupType.Standalone, 123, 456, "Test size"); 

} 

[MenuItem("Test/SizeTextQuery")] 

public static void SizeTextQueryTest()

{ 

Debug.Log(SizeExists(GameViewSizeGroupType.Standalone, "Test size")); 

} 

[MenuItem("Test/Query16:9Test")] 

public static void WidescreenQueryTest()

{ 

Debug.Log(SizeExists(GameViewSizeGroupType.Standalone, "16:9")); 

} 

[MenuItem("Test/Set16:9")] 

public static void SetWidescreenTest()

{ 

SetSize(FindSize(GameViewSizeGroupType.Standalone, "16:9")); 

} 

[MenuItem("Test/SetTestSize")] 

public static void SetTestSize()

{ 

int idx = FindSize(GameViewSizeGroupType.Standalone, 123, 456); 

if (idx != -1) 

SetSize(idx); 

} 

public static void SetSize(int index)

{ 

var gvWndType = typeof(Editor).Assembly.GetType("UnityEditor.GameView"); 

var selectedSizeIndexProp = gvWndType.GetProperty("selectedSizeIndex", 

BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic); 

var gvWnd = EditorWindow.GetWindow(gvWndType); 

selectedSizeIndexProp.SetValue(gvWnd, index, null); 

} 

[MenuItem("Test/SizeDimensionsQuery")] 

public static void SizeDimensionsQueryTest()

{ 

Debug.Log(SizeExists(GameViewSizeGroupType.Standalone, 123, 456)); 

} 

public static void AddCustomSize(GameViewSizeType viewSizeType, GameViewSizeGroupType sizeGroupType, int width, int height, string text)

{ 

// GameViewSizes group = gameViewSizesInstance.GetGroup(sizeGroupTyge);

// group.AddCustomSize(new GameViewSize(viewSizeType, width, height, text);

var group = GetGroup(sizeGroupType); 

var addCustomSize = getGroup.ReturnType.GetMethod("AddCustomSize"); // or group.GetType().

var gvsType = typeof(Editor).Assembly.GetType("UnityEditor.GameViewSize"); 

var ctor = gvsType.GetConstructor(new Type[] { typeof(int), typeof(int), typeof(int), typeof(string) }); 

var newSize = ctor.Invoke(new object[] { (int)viewSizeType, width, height, text }); 

addCustomSize.Invoke(group, new object[] { newSize }); 

} 

public static bool SizeExists(GameViewSizeGroupType sizeGroupType, string text)

{ 

return FindSize(sizeGroupType, text) != -1; 

} 

public static int FindSize(GameViewSizeGroupType sizeGroupType, string text)

{ 

// GameViewSizes group = gameViewSizesInstance.GetGroup(sizeGroupType);

// string[] texts = group.GetDisplayTexts();

// for loop...

var group = GetGroup(sizeGroupType); 

var getDisplayTexts = group.GetType().GetMethod("GetDisplayTexts"); 

var displayTexts = getDisplayTexts.Invoke(group, null) as string[]; 

for (int i = 0; i < displayTexts.Length; i++) 

{ 

string display = displayTexts[i]; 

// the text we get is "Name (W:H)" if the size has a name, or just "W:H" e.g. 16:9

// so if we're querying a custom size text we substring to only get the name

// You could see the outputs by just logging

// Debug.Log(display);

int pren = display.IndexOf('('); 

if (pren != -1) 

display = display.Substring(0, pren - 1); // -1 to remove the space that's before the prens. This is very implementation-depdenent

if (display == text) 

return i; 

} 

return -1; 

} 

public static bool SizeExists(GameViewSizeGroupType sizeGroupType, int width, int height)

{ 

return FindSize(sizeGroupType, width, height) != -1; 

} 

public static int FindSize(GameViewSizeGroupType sizeGroupType, int width, int height)

{ 

// goal:

// GameViewSizes group = gameViewSizesInstance.GetGroup(sizeGroupType);

// int sizesCount = group.GetBuiltinCount() + group.GetCustomCount();

// iterate through the sizes via group.GetGameViewSize(int index)

var group = GetGroup(sizeGroupType); 

var groupType = group.GetType(); 

var getBuiltinCount = groupType.GetMethod("GetBuiltinCount"); 

var getCustomCount = groupType.GetMethod("GetCustomCount"); 

int sizesCount = (int)getBuiltinCount.Invoke(group, null) + (int)getCustomCount.Invoke(group, null); 

var getGameViewSize = groupType.GetMethod("GetGameViewSize"); 

var gvsType = getGameViewSize.ReturnType; 

var widthProp = gvsType.GetProperty("width"); 

var heightProp = gvsType.GetProperty("height"); 

var indexValue = new object[1]; 

for (int i = 0; i < sizesCount; i++) 

{ 

indexValue[0] = i; 

var size = getGameViewSize.Invoke(group, indexValue); 

int sizeWidth = (int)widthProp.GetValue(size, null); 

int sizeHeight = (int)heightProp.GetValue(size, null); 

if (sizeWidth == width && sizeHeight == height) 

return i; 

} 

return -1; 

} 

static object GetGroup(GameViewSizeGroupType type)

{ 

return getGroup.Invoke(gameViewSizesInstance, new object[] { (int)type }); 

} 

//[MenuItem("Test/LogCurrentGroupType")]

//public static void LogCurrentGroupType()

//{

// Debug.Log(GetCurrentGroupType());

//}

public static GameViewSizeGroupType GetCurrentGroupType()

{ 

var getCurrentGroupTypeProp = gameViewSizesInstance.GetType().GetProperty("currentGroupType"); 

return (GameViewSizeGroupType)(int)getCurrentGroupTypeProp.GetValue(gameViewSizesInstance, null); 

} 

public static void switchOrientation()

{ 

int width = Screen.height; 

int height = Screen.width; 

int index = FindSize(GetCurrentGroupType(), width, height); 

if (index == -1) 

{ 

AddCustomSize(GameViewSizeType.FixedResolution, GetCurrentGroupType(), width, height, ""); 

index = FindSize(GetCurrentGroupType(), width, height); 

} 

if (index != -1) 

{ 

SetSize(index); 

} 

else

{ 

Debug.LogError("switchOrientation failed, can not find or add resoulution for " \+ width.ToString() + "*" \+ height.ToString()); 

} 

} 

} 

#endif

``` 

## 屏幕比例与摄像机设置

### 宽高比（aspect）

Screen.witdh和Screen.heigh表示模拟硬件设备的宽高值，不受camera等相关组件在软件层面的代码影响。   
Unity在Screen界面可以设置Screen的比例和像素，但是没有提供相应的接口用代码设置屏幕比例，因为硬件的屏幕就是不可设置的。

**aspect** ：获取和设置屏幕的 **宽高比** 。

Viewport Rect：视口框。指的是在Screen上，显示图像的方框。X、Y为偏移值，W、H为实际视口宽/高与Screen宽/高的比例值。

aspect默认和screen的宽高比保持一致，摄像机渲染的图像填满screen。   
当Viewport Rect宽高比发生变化时，aspect与之保持一致。   
即默认情况下，aspect是由屏幕的宽高比以及Viewport Rect一起决定的。

当在脚本中手动更改aspect的值时，aspect的值即为手动设置的值，相机的宽高比也就是人手动设置的。

此时，Viewport宽高比不变，相机会把自己的视口当中的图像渲染到Viewport当中，由于宽高比不一致会导致变形。

### 可见区域形状

#### Perspective

透视视图下，可见区域是一个四棱台。   
Aspect决定了宽高比，即棱台上下底、截面的宽高比。   
Field of View：相机视野角度，由FOV Axis确定的轴向上的角度值(degree)

> 宽高比决定了，改变Field of View，视口截面的形状会成比例缩放。从角度的层面来看，棱台的侧棱与高之间的夹角随FoV的变大而变大，直观来看，就是视角的放大与缩小。   
>  （调整Screen或Viewport或aspect，只能改变相机视口的宽度，不能改变高度，就是因为Field of View把高度值定死了）   
>  Clipping Planes：剪裁面片，指的是可视区域棱台的上下底面 距离camera坐标点的位置（近截面和远截面）

以上所有参数，共同决定了camera可见范围的形状以及它与屏幕渲染的图像的关系。

> **aspect值在代码中设置过一次，就会固定。如果没有设置过，就默认与Screen宽高比一致。**

#### Orthographic

较容易理解。size参数相当于Perspective模式下的FoV。

摄像机高度 = 摄像机orthographicSize * 2   
摄像机实际宽度 = 摄像机高度 * 屏幕宽高比   
摄像机实际宽度 = 摄像机orthographicSize * 2 * 屏幕宽高比

## Ref

<https://www.cnblogs.com/unity-carry/p/9512662.html>   
<https://www.jianshu.com/p/547ef7f4a313>   
<https://www.jianshu.com/p/95cb4621206e>

