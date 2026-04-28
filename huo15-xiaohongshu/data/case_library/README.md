# 案例库（v3.5 新建）

> 把 Allen 教学 + 蕉下案例 + 用户的冬日 5 篇，做成可逐个调阅学习的案例库。
> 配 `scripts/case_study.py`，对每个案例做"苏格拉底式拆解" — 先你自己回答，
> 再看范本分析。

---

## 目录结构

```
data/case_library/
├── README.md              # 本文件
├── allen_jinxing.md       # Allen 人生尽兴指南（综合）
├── allen_lingqu.md        # 案例 11 — 惊蛰·领取春日礼（动词意境）
├── allen_zhouwen.md       # 案例 4 — 周三存档（栏目化）
├── allen_chunfen.md       # 案例 8 — 春分·什么也不赶（节气借势）
├── jiaoxia_brand.md       # 蕉下品牌方法论（不是…而是…）
└── winter_*.md            # 冬日 5 篇（用户填充）
```

每个 `.md` 文件遵循统一 schema（见下文），让 case_study.py 能自动解析。

## 文件 Schema

```markdown
---
case_id: <唯一标识>
title: <案例标题>
source: <来源：Allen / 蕉下 / 用户>
date: <日期>
tags: [关键词1, 关键词2]
key_techniques: [技法1, 技法2]
---

## 原文 / 范本

<文案原文>

## 关键技法

- 技法 1：...
- 技法 2：...

## 苏格拉底问题（学习模式用）

1. 这个文案的开头第一句，你觉得是在做什么？
2. 中段的画面用了几个意象？这些意象哪里来？
3. 结尾如果换成"希望大家..."，效果会怎样？

## 范本解读（先回答上面再看）

<答案 / 老师视角分析>

## 你能学到的

- ...

## 关联案例

- [[other_case_id]]
```

## 怎么用

```bash
# 列所有案例
python3 scripts/case_study.py list

# 学习一个案例（苏格拉底模式：先问你，再给答）
python3 scripts/case_study.py study allen_lingqu

# 跳过提问直接看范本
python3 scripts/case_study.py show allen_lingqu

# 找相关案例
python3 scripts/case_study.py related "动词"
```
