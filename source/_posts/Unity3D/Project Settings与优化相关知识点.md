---
title: Project Settings与优化相关知识点
date: 2021-3-21 21-56
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Managed code stripping

unused code from a build ->

  * decrease the final build size

  * while using the IL2CPP - decrease build time because less code needs to be converted to C++ and compiled.

**statically analyzing** the code in a Project to detect classes, members of classes, and even portions of functions that can never be reached during execution. 

> When your code (or code in a plugin) looks up classes or members dynamically using reflection, the code stripping tool cannot always detect that the Project is using those classes or members, and might remove them. To declare that a Project is using such code, use link.xml files or Preserve attributes.

