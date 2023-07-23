---
title: Unreal插件开发
date: 2022-3-4 18-40
categories:
- Unreal
tags:
- Unreal
catalog: true
---

## 目录结构

Engine /[UE4 Root]/Engine/Plugins/[Plugin Name]/

Game /[Project Root]/Plugins/[Plugin Name]/  
(will be detected and loaded at Engine or Editor start-up time)

Public/Classes的父目录名就是module名

### Plugin Descriptor Files

Plugin descriptor Files: `.uplugin`  
API: https://docs.unrealengine.com/4.27/en-US/API/Runtime/Projects/FPluginDescriptor/

Category：类目名即在插件浏览器中所属的类目。  
Installed：默认启用或禁用状态，在插件浏览器中可以控制加载卸载插件模块。  
Modules：描述模块名、运行类型、加载时机、支持平台等信息。  
Type：Runtime，RuntimeNoCommandlet，Developer，Editor，EditorNoCommandlet，Program。  
LoadingPhase：Default，PreDefault，PostConfigInit，PostConfigInit。  
WhitelistPlatforms：支持的平台  
BlacklistPlatforms：不支持的平台

## 操作方法

unreal的理念是开发工作都是在工程目录进行，包括插件开发

### 打包发布

https://blog.csdn.net/jxyb2012/article/details/88839224

```csharp "E:\Program Files\Epic Games\UE_4.25\Engine\Build\BatchFiles\RunUAT.bat" BuildPlugin Plugin="D:\work\UE4_25\PluginFactory\Plugins\MyNewPlugin\MyNewPlugin.uplugin" Package="D:\work\UE4_25\PluginPackaged" ``` 

## 插件编译执行过程

Plugins will automatically be compiled by UBT when compiling your game project.

```csharp #pragma once #include "CoreMinimal.h" #include "ModuleManager.h" class FPanoCamModule : public IModuleInterface { public: /** IModuleInterface implementation */ virtual void StartupModule() override; virtual void ShutdownModule() override; }; ``` 

每个独立模块都有一个类继承自 IModuleInterface，重写了插件加载卸载的方法。

.uplugin文件中Modules下的LoadingPhase字段说明了模块加载的时机，当满足这个时机时此模块StartupModule函数将被调用。此插件的功能入口就是从这里开始。当程序关闭或主动调用ShutdownModule函数时，模块将被卸载。

## 编辑器拓展开发接口

LevelEditorModule.GetToolBarExtensibilityManager()可以拓展关卡编辑器的工具栏，GetMenuExtensibilityManager()可以拓展菜单栏。  
GEditor->GetEditorSubsystem<UAssetEditorSubsystem>()->OnAssetOpenedInEditor()，可以监听UE中，任意编辑器打开的事件。  
FCoreUObjectDelegates::OnObjectPropertyChanged可以监听任意Object，任意属性的变化事件。

## 其他技巧

### Include

> unreal中所有头文件都可以include。只是ue建议只include public目录或Classes的头文件，不建议include private目录的。

#### Include public

在XXX.Build.cs文件中添加依赖Module：PublicDependencyModuleNames.AddRange  
然后在某个源码文件，直接include。（从Public/Classes开始算路径）

#### Include private

在当前插件模块的build.cs文件中添加Private目录:

```csharp var EngineDir = Path.GetFullPath(Target.RelativeEnginePath); PrivateIncludePaths.AddRange( new string[] { Path.Combine(EngineDir, "Source/Editor/AnimationBlueprintEditor/Private/"), }); ``` ```csharp // 用尖括号也可以 #include "AnimationBlueprintEditor.h" ``` 

### 添加第三方依赖库

PublicIncludePaths.Add(zlibPath + “include” + platform); //把（.h）头文件路径引入。  
PublicLibraryPaths.Add(zlibPath + “lib” + platform); //把（.lib）库文件路径引入。  
PublicAdditionalLibraries.Add(“zlibstatic.lib”); //把（.lib）库文件引入。

https://blog.csdn.net/jxyb2012/article/details/88839224

#### 链接错误的解决方法

  1. 确保：把所属module添加到PublicDependencyModuleNames中
  2. 确保：如果缺失的函数or类是某个插件中的，需要标识为API，在函数前加入对应API宏。

> 例如module名为SamplePlg，则API宏为：SAMPLEPLG_API

### 访问private或protected的UPROPERTY

```csharp USTRUCT() struct FAnimLinkableElement { GENERATED_USTRUCT_BODY() protected: /** The slot index we are currently using within LinkedMontage */ UPROPERTY(EditAnywhere, Category=AnimLink) int32 SlotIndex; }; ``` ```csharp int32* GetSlotIndex(void *pAnimLinkableElement) { static UScriptStruct* Struct = FindObjectSafe<UScriptStruct>(ANY_PACKAGE, TEXT("AnimLinkableElement")); auto Prop = Struct->FindPropertyByName(TEXT("SlotIndex")); check(Prop); return Prop->ContainerPtrToValuePtr<int32>(pAnimLinkableElement); } ``` 

## Build.cs

配置文件属性详细说明：https://blog.csdn.net/jxyb2012/article/details/88839224

```csharp using UnrealBuildTool; using System.IO; //路径获取需要用到IO public class TestPlugin : ModuleRules ｛ private string ModulePath //当前TestPlugin.Build.cs文件所在的路径 ｛ get ｛ return Path.GetDirectoryName(RulesCompiler.GetModuleFilename(this.GetType().Name)); ｝ ｝ private string ThirdPartyPath //这个插件引用的第三方库的目录 ｛ get ｛ return Path.GetFullPath(Path.Combine(ModulePath, "../../ThirdParty/")); ｝ ｝ private string MyTestLibPath //第三方库MyTestLib的目录 ｛ get ｛ return Path.GetFullPath(Path.Combine(ThirdPartyPath, "MyTestLib")); ｝ ｝ public TestPlugin(TargetInfo Target) ｛ PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs; PublicIncludePaths.AddRange( //公有文件搜索路径 new string[] ｛ "TestPlugin/Public" // ... add public include paths required here ... ｝ ); PrivateIncludePaths.AddRange( new string[] ｛ "TestPlugin/Private" //私有文件搜索路径 // ... add other private include paths required here ... ｝ ); PublicDependencyModuleNames.AddRange( new string[] ｛ "Core" // ... add other public dependencies that you statically link with here ... ｝ ); PrivateDependencyModuleNames.AddRange( new string[] ｛ "CoreUObject", "Engine", "Slate", "SlateCore", // ... add private dependencies that you statically link with here ... ｝ ); DynamicallyLoadedModuleNames.AddRange( new string[] ｛ // ... add any modules that your module loads dynamically here ... ｝ ); LoadThirdPartyLib(Target); //加载第三方库 ｝ public bool LoadThirdPartyLib(TargetInfo Target) ｛ bool isLibrarySupported = false; if ((Target.Platform == UnrealTargetPlatform.Win64) || (Target.Platform == UnrealTargetPlatform.Win32))//平台判断 ｛ isLibrarySupported = true; System.Console.WriteLine("\----- isLibrarySupported true"); string PlatformSubPath = (Target.Platform == UnrealTargetPlatform.Win64) ? "Win64" : "Win32"; string LibrariesPath = Path.Combine(MyTestLibPath, "Lib"); PublicAdditionalLibraries.Add(Path.Combine(LibrariesPath, PlatformSubPath, "TestLib.lib"));//加载第三方静态库.lib ｝ if (isLibrarySupported) //成功加载库的情况下，包含第三方库的头文件 ｛ // Include path System.Console.WriteLine("\----- PublicIncludePaths.Add true"); PublicIncludePaths.Add(Path.Combine(MyTestLibPath, "Include")); ｝ return isLibrarySupported; ｝ ｝ ``` 

## Ref

https://www.jianshu.com/p/ec0ae889f417  
https://www.jianshu.com/p/49684c1b6011  
https://gameinstitute.qq.com/community/detail/121298
