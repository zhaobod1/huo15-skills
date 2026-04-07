---
type: concept
title: RAG（检索增强生成）
date: 2026-04-06
concepts: [检索, 知识库, 向量数据库, LLM]
---

# RAG（检索增强生成）

> Retrieval-Augmented Generation — 传统知识库方案

## 摘要

RAG 是过去 3 年给 LLM 提供私有数据访问的主流方案：通过向量数据库做相似性搜索。

## 工作原理

1. 文档切成任意"chunks"
2. 转成数学向量（embeddings）
3. 存入向量数据库
4. 用户提问时，做"相似性搜索"找相关 chunks
5. 把相关 chunks 喂给 LLM

## 缺点

- 黑盒：向量数据库不透明
- 检索噪音：相似性搜索不一定准确
- 维护复杂：需要手动更新向量库
- 可审计性低：难以追溯答案来源

## Karpathy 方案的对比

| | RAG | Karpathy 方案 |
|---|---|---|
| 存储 | 向量数据库 | Markdown 文件 |
| 检索 | 相似性搜索 | LLM 直接读摘要 |
| 维护 | 手动更新 | AI 自动维护 |
| 可审计性 | 低 | 高 |

## 相关概念

- [[Karpathy LLM Knowledge Bases 方案]] — RAG 的替代方案
- [[向量数据库]] — RAG 的底层存储

## 原始出处

- https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an
