---
title: UPM自定义资源包及相关规范
date: 2020-9-22 17-06
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

ByPrin@UWA

## UPM资源包介绍

作用：给Unity Package Manager制作自定义资源包，并上传至Github托管。使用PackageManager设定项目的依赖、解析资源包依赖、下载添加需要的资源包，将内容整合到项目中，以便在其他项目中使用，并与其他开发者共享。   
常用于

  * 编辑器工具——文本编辑器、动画查看器或文本框架、Physics API、图形管线

  * 内容库——纹理和动画资源集合

> **Unity 2018.3 及之后版本, Unity Package Manager (UPM) 开始支持 Git**

### 文件布局

UPM资源包是一个按特定标准排列的文件夹，是一个包含各种功能、资源的容器。必须遵循Unity的包格式标准才能正确运行（推荐的文件布局和版本号格式）。

```csharp 

<root>

├── package.json

├── README.md

├── CHANGELOG.md

├── LICENSE.md

├── Editor

│ ├── Unity.[YourPackageName].Editor.asmdef

│ └── EditorExample.cs

├── Runtime

│ ├── Unity.[YourPackageName].asmdef

│ └── RuntimeExample.cs

├── Tests

│ ├── Editor

│ │ ├── Unity.[YourPackageName].Editor.Tests.asmdef

│ │ └── EditorExampleTest.cs

│ └── Runtime

│ ├── Unity.[YourPackageName].Tests.asmdef

│ └── RuntimeExampleTest.cs

└── Documentation~

└── [YourPackageName].md

``` 

> 文件夹名称以~结尾不会显示在Editor的Project窗口

### Package manifest

可以在Unity - Inspector面板填写

crucial information

  * its registered name 

  * version number   
To User: 

  * a user-friendly name that appears in the list view on the Package Manager window.

  * a brief description of the package

  * the earliest version of Unity the package is compatible with.

#### Name

This name must conform to the Unity Package Manager naming convention, which uses reverse domain name notation.

  * Start with `com.<company-name>.`

  * Contain **only lowercase letters** , digits, hyphens (-), underscores (_), and periods (.)

#### Display Name

是在Package Manager窗口显示给用户的名称，也是在Project窗口显示的包的Root文件夹的名称。

#### 版本号规范

Major.Minor.Patch

#### the lowest Unity version

If omitted, the package is considered compatible with all Unity versions.   
A package that is not compatible with Unity will not appear in the Package Manager window.

#### Package manifest example

在包的根目录下创建文件`package.json`，只要格式符合规范，就能被UPM识别

```csharp 

{

"name": "com.unity.example",

"version": "1.2.3",

"displayName": "Package Example",

"description": "This is an example package",

"unity": "2019.1",

"unityRelease": "0b5",

"dependencies": {

"com.unity.some-package": "1.0.0",

"com.unity.other-package": "2.0.0"

},

"keywords": [

"keyword1",

"keyword2",

"keyword3"

],

"author": {

"name": "Unity",

"email": "unity@example.com",

"url": "https://www.unity3d.com"

}

}

``` 

### Assembly definition

Assembly definition files are the Unity equivalent to a C# project in the .NET ecosystem. You must set explicit references in the assembly definition file to other assemblies (whether in the same package or in external packages).

命名规则：   
Editor/MyCompany.MyFeature.Editor.asmdef   
Runtime/MyCompany.MyFeature.Runtime.asmdef

CompanyName.FeatureName与package.json文件一致   
文件的名称与文件中的”name”一致

> 使用asmdef的优势
> 
>   * 更短的编译时间
> 
>   * 发挥访问修饰符”internal”的作用
> 
>   * 允许使用 unsafe code
> 
>   * .dll 文件可以指定特定的程序集引用。
> 
> 

一些注意事项：

  1. Editor 文件夹下的 AssemblyDefinition 中 Platform 只能选择 Editor，并且 Reference 必须添加上 Runtime 中的那个 AssemblyDefiniion

### LICENSE相关（暂时忽略）

推荐添加Third Party Notices.md 和 LICENSE.md 

  * LICENSE.md：例如以MIT许可证为准的开源许可证MD文件

## 步骤

### 1\. 按照规范创建Package

### 分发

#### zip

压缩为zip文件   
Unity Package Manager窗口通过Add Package from Disk添加

#### Git代码库分发

添加到Git仓库中，包括meta文件

下载方式（使用者必须安装git）

  * 在PackageManager中通过Git URL直接下载

```csharp 

git tag 1.0.0 upm 

git push origin upm --tags 

``` 

## README文档

Developer package documentation. This is generally documentation to help developers who want to modify the package or push a new change on the package master source repository.

## Changelog规范

You can update the CHANGELOG.md file every time you publish a new version. Every new feature or bug fix should have a trace in this file.

**Added** for new features.   
**Changed** for changes in existing functionality.   
**Deprecated** for soon-to-be removed features.   
**Removed** for now removed features.   
**Fixed** for any bug fixes.   
**Security** in case of vulnerabilities.

> 轻量级的使用Fixed和Features就足够了

例如：

```csharp 

## [3.0.3] - 2018-04-05 

### Changed 

\- API Examples are now published on [Github](https://github.com/Unity-Technologies/ProBuilder-API-Examples). 

### Added 

\- Expose poly shape creation methods. Add API example. 

colors. 

\- New option to set edge and wireframe line width (not available on Metal). 

### Fixed 

\- Fix scene info not updating with selection changes. 

\- Fix `Apply Material` only applying to parent gameobjects if children are also selected. 

\- Fix `pb_Object.SetSelectedFaces` setting duplicate vertex indices. 

### Removed 

\- Remove update checking. 

``` 

> 原则   
>  Changelogs are for humans, not machines. 
> 
>   * There should be an entry for every single version.
> 
>   * The same types of changes should be grouped.
> 
>   * Versions and sections should be linkable.
> 
>   * The latest version comes first.
> 
>   * The release date of each version is displayed.
> 
>   * Mention whether you follow Semantic Versioning.
> 
> 

## Semantic Versioning规范

MAJOR.MINOR.PATCH

  * MAJOR introduces one or more breaking changes

  * MINOR introduces one or more **backward-compatible API changes**

  * PATCH only introduces bug fixes with no API changes at all

> When you begin to develop a package, start the version number at **0.1.0.** The MAJOR version number 0 is reserved for packages in their initial development phase. During initial development, package APIs change often, frequently in a breaking manner, so keep the MAJOR version number at 0 until you consider your package stable enough and ready for use in production.

PS: 该规范主要在开发提供给用户的API时有重要作用。先不深究，大致按照此标准进行即可。

## Ref

<https://docs.unity.cn/2019.4/Documentation/Manual/CustomPackages.html>   
<https://keepachangelog.com/en/1.0.0/>   
<https://semver.org/>   
<https://www.jianshu.com/p/153841d65846>

