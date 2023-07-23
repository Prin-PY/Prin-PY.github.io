---
title: Assembly Definition File & Package Manager
date: 2020-5-6 16-21
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

[https://blog.csdn.net/weixin_34329187/article/details/86016256?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-6&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-6](https://blog.csdn.net/weixin_34329187/article/details/86016256?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-6&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-6)>

## Assembly Definition File(XXX.asmdef)

> Unity 2017.3中的新功能   
>  使用该特性，开发者可以在一个文件夹中自定义托管程序集。定义明晰的依赖文件，可以确保脚本被更改后，只会重新生成必需的程序集，提高工作效率，减少编译时间。

Unity自动定义脚本编译为 **托管程序集** 的方式。Unity编辑器中进行脚本更改迭代的编译时间会随脚本数量的增加而增加。   
你可以使用新的 **程序集定义文件特性** ，基于文件夹中的脚本定义你自己的托管程序集。如果你将项目脚本分为多个程序集，并进行良好的依赖定义，可以确保你在 **更改某个脚本时，只会重新生成必需的程序集。** 这减少了编译时间，因此你可以在Unity项目中将 **每个托管程序集看做是单个的库** 。

![Alt text](assets/Assembly%20Definition%20File%20&%20Package%20Manager/0ba13fb88d2746f6bd2ed681d1324d8c.png)

### 格式

都是JSON文件，包含以下字段:

Field | Type  
---|---  
name | string  
references(optional) | string array  
includePlatforms(optional) | string array  
excludePlatforms(optional) | string array  
  
字段includePlatforms和 excludePlatforms不能在同一个程序集定义文件中使用

### 使用方法

  * 将一个程序集定义文件添加到Unity项目中的一个文件夹里，对该文件夹里所有的脚本进行编译，然后在检视窗口中对程序集名称进行设置。

  * 你还可以使用检视窗口添加对项目中其它程序集定义文件的引用。编译程序集和定义程序集间的依赖时会用到这些引用。

  * Unity使用引用来编译程序集，以及定义程序集之间的依赖关系。你可以在检视窗口中设置程序集定义文件的平台兼容性，也可以选择排除或包括特定平台。

> 假设你有一个Assets/ExampleFolder/MyLibrary.asmdef和一个Assets/ExampleFolder/ExampleFolder2/Utility.asmdef文件，那么：
> 
>   * Assets > ExampleFolder > ExampleFolder2文件夹中的所有脚本将会被编译到Assets/ExampleFolder/ExampleFolder2/Utility.asmdef定义的程序集中。
> 
>   * Assets > ExampleFolder文件夹中的所有脚本，除Assets > ExampleFolder> ExampleFolder2中的脚本之外，将会被编译到Assets/ExampleFolder/MyLibrary.asmdef定义的程序集中。
> 
> 

> 
> 程序集定义文件不属于程序集生成文件。它们不支持在生成系统中常见的条件化生成规则。这也是程序集定义文件不支持预处理指令（定义）的原因，因为它们一直是静态的。

### 向后兼容和隐式依赖

程序集定义文件向后兼容Unity中现存的 **[预定义编译系统]（Predefined Compilation System）** 。   
**预定义程序集** 总是依赖于每个 **程序集定义文件的程序集** 。   
这与Unity中 **所有脚本** 都依赖于所有和当前生成目标兼容的 **预编译程序集** （插件/.dll）的情况相似。

![Alt text](assets/Assembly%20Definition%20File%20&%20Package%20Manager/48350069f86f4fa59e4fdd25dbc6e399.png)
   
Unity给予程序集定义文件的优先级要比[预定义编译系统](http://CompileOrderFolders)高。   
这意味着，任何来自程序集定义文件文件夹内的预定义编译的特殊文件夹名，都不会对编译产生任何影响。Unity只将它们视为常规文件夹。

> 强烈建议你对项目中的所有脚本使用程序集定义文件，或完全不使用。否则，没有使用程序集定义文件的脚本会在每次程序集定义文件重新编译时也被重新编译。这会减少你在项目中程序集定义文件所带来的好处。

### API

要获取平台名，可使用：   
`CompilationPipeline.GetAssemblyDefinitionPlatforms`   
在`UnityEditor.Compilation`命名空间中，有一个静态的`CompilationPipeline`类，你可用它获取程序集定义文件以及所有由Unity生成的程序集的信息。

## Package Manager

一个包是一个容器，它可以包含各种资源的组合：shader、纹理、插件、图标、脚本等，可以增强项目的各个部分。

> 优点：相对于Asset Store的包，Package Manager提供了更新，更容易集成的包管理方案，能够为Unity提供各种增强功能。

### 用法

Window > Package Manager 查看，安装，删除，更新   
官方包名称会以 com.unity开头   
一些包在版本号旁边显示标签。这些标签传达有关该包版本的信息。

标签 | 含义  
---|---  
verified | Unity的质量保证团队已正式确认此包可与编辑器的特定版本配合使用。  
preview | 该包处于发布周期的早期阶段，可能尚未被开发团队或Unity的质量保证团队记录和完全验证。  
  
### package manifest file包清单文件

#### project manifests: manifest.json

tell the Package Manager which packages and versions are available to the project.

#### package manifests: package.json

determine which version of the package to load, and what information to display in the Package Manager window.

> name必须纯小写，否则是invalid

```csharp 

{ 

"name": "com.unity.package-4", 

"displayName": "Package Number 4", 

"version": "2.5.1", 

"unity": "2018.1", 

"description": "This package provides X, Y, and Z. \n\nTo find out more, click the \"View Documentation\" link.", 

"keywords": ["key X", "key Y", "key Z"], 

"category": "Controllers", 

"dependencies": { 

"com.unity.package-1": "1.0.0", 

"com.unity.package-2": "2.0.0", 

"com.unity.package-3": "3.0.0"

} 

} 

``` 

### The Package Registry

Unity maintains a central registry of official packages that are available for distribution(可供分发的官方包的中央注册表。). When Unity loads, the Package Manager communicates with the registry, checks the project manifest file, and displays the status of each available package in the Package Manager window.

When you remove a package from the project, the Package Manager updates the project manifest to exclude that package from the list in In Project mode but it is still available in All mode because it is still on the registry.

When you install or update a package, the Package Manager downloads the package from the registry.

