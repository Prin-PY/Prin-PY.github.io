---
title: Build - UE CI
date: 2022-9-8 17-57
categories:
- Unreal
tags:
- Unreal
catalog: true
---

run Setup.bat for checking dependencies

run GenerateProjectFiles.bat for generating your project files

build engine in the configuration we needed

D:\UnrealEngineSource\Setup.bat

D:\UnrealEngineSource\GenerateProjectFiles.bat

"c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\MSBuild.exe" "D:\UnrealEngineSource\UE4.sln" -target:"Engine\UE4" -property:Platform=Win64;Configuration="Development Editor" -verbosity:diagnostic

"C:\Program Files\Microsoft Visual Studio\2022\Community\Msbuild\Current\Bin\MSBuild.exe" "D:\Unreal\UnrealEngine\UE_5\UE5.sln" -target:"Engine\UE5" -property:Platform=Win64;Configuration="Development Editor" -verbosity:diagnostic

<https://blog.mi.hdm-stuttgart.de/index.php/2017/02/11/uat-automation/>

<https://medium.com/@lifeexe/unreal-engine-ci-part-i-source-code-builds-8000ca1da723>

<https://www.cnblogs.com/WoodJim/p/15965121.html>
