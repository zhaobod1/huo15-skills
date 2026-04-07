---
name: huo15-odoo
description: |
version: 1.0.0
  火一五欧度技能（辉火云企业套件 Odoo 19 接口访问指南）。提供 Odoo 19 系统访问的正确指导，包括 XML-RPC API 连接、客户（res.partner）、项目（project.project）、任务（project.task）等模型的正确查询和创建方式。
trigger:
  - patterns:
      - "odoo"
      - "辉火云"
      - "欧度"
      - "项目"
      - "任务"
      - "工时"
      - "库存"
      - "销售"
      - "project"
      - "task"
    type: fuzzy
---

# 火一五欧度技能（Odoo 19）

> 辉火云企业套件（Odoo 19）接口访问完整指南
> **重要**：公司系统使用 Odoo 19.0，必须使用 XML-RPC，odoorpc 库不兼容！

---

## 🏢 系统信息

| 项目 | 值 |
|------|-----|
| **地址** | https://www.huo15.com（默认） |
| **老系统** | https://huihuoyun.huo15.com |
| **数据库** | huo15 |
| **模式** | XML-RPC API |
| **Odoo版本** | 19.0 |

### 账号规则

| 操作类型 | 账号 | 说明 |
|----------|------|------|
| **API访问** | postmaster@huo15.com | 管理员，有读写权限 |
| **普通用户** | 645612509@qq.com | huo15.com |

---

## ⚠️ 重要：必须使用 XML-RPC

**Odoo 19 使用 XML-RPC，不支持 odoorpc 库！**

### 正确方式（XML-RPC）
```python
import xmlrpc.client

url = 'https://www.huo15.com'
db = 'huo15'

# 连接
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, 'postmaster@huo15.com', '198809011ab', {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# 查询
result = models.execute_kw(db, uid, '198809011ab', 'res.partner', 'search_read', 
    [[('name', 'ilike', '关键词')]], 
    {'fields': ['id', 'name'], 'limit': 10})
```

### 错误方式（odoorpc）
```python
# ❌ 不要使用 odoorpc 库，与 Odoo 19 不兼容！
from odoorpc import ODOO
odoo = ODOO('https://www.huo15.com', timeout=60)
odoo.login('huo15', 'postmaster@huo15.com', '198809011ab')
```

---

## 📋 Odoo 19 常用模型

### 联系人（res.partner）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'res.partner', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'res.partner', 'create', [values])` |
| 更新 | `execute_kw(db, uid, password, 'res.partner', 'write', [id, values])` |

### 项目（project.project）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'project.project', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'project.project', 'create', [values])` |

### 任务（project.task）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'project.task', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'project.task', 'create', [values])` |

---

## 🔧 常用操作示例

### 1. 登录并连接
```python
import xmlrpc.client

url = 'https://www.huo15.com'
db = 'huo15'
user = 'postmaster@huo15.com'
password = '198809011ab'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"登录成功! UID: {uid}")
```

### 2. 查询客户
```python
domain = [('name', 'ilike', '关键词')]
fields = ['id', 'name', 'vat', 'street', 'city', 'phone', 'email']
result = models.execute_kw(db, uid, password, 'res.partner', 'search_read', 
    [domain], {'fields': fields, 'limit': 10})
```

### 3. 创建客户公司
```python
values = {
    'name': '公司名称',
    'company_type': 'company',  # 公司
    'vat': '统一社会信用代码',
    'street': '注册地址',
    'city': '城市',
}
partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [values])
```

### 4. 创建联系人（关联到公司）
```python
values = {
    'name': '联系人姓名',
    'parent_id': partner_id,  # 所属公司ID
    'type': 'contact',        # 联系人类型
    'function': '职位',
    'phone': '电话',
    'email': '邮箱',
}
contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [values])
```

### 5. 查询项目
```python
domain = [('active', '=', True)]
fields = ['id', 'name', 'partner_id', 'user_id']
result = models.execute_kw(db, uid, password, 'project.project', 'search_read',
    [domain], {'fields': fields, 'limit': 20})
```

### 6. 创建项目
```python
values = {
    'name': '项目名称',
    'partner_id': partner_id,  # 客户ID
    'description': '项目描述',
}
project_id = models.execute_kw(db, uid, password, 'project.project', 'create', [values])
```

### 7. 查询任务（重要：必须加 active=True）
```python
domain = [
    ('active', '=', True),  # ⚠️ 必须过滤开放任务
    ('project_id', '=', project_id),
]
fields = ['id', 'name', 'user_ids', 'stage_id', 'priority']
result = models.execute_kw(db, uid, password, 'project.task', 'search_read',
    [domain], {'fields': fields, 'limit': 50})
```

### 8. 创建任务
```python
values = {
    'name': '任务名称',
    'project_id': project_id,
    'user_ids': [(6, 0, [user_id])],  # 负责人
    'description': '任务描述',
    'priority': '0',  # 0=普通, 1=紧急
}
task_id = models.execute_kw(db, uid, password, 'project.task', 'create', [values])
```

---

## 📊 execute_kw 参数说明

```python
models.execute_kw(db, uid, password, model_name, method, args, kwargs)
```

| 参数 | 说明 |
|------|------|
| db | 数据库名，如 'huo15' |
| uid | 登录后的用户ID（authenticate 返回） |
| password | 密码 |
| model_name | 模型名，如 'res.partner' |
| method | 方法名：'search_read', 'create', 'write', 'unlink' |
| args | 位置参数，通常是 domain 列表 |
| kwargs | 关键字参数，如 {'fields': [...], 'limit': 10} |

---

## ⚠️ 注意事项

1. **必须使用 XML-RPC**：Odoo 19 不兼容 odoorpc 库
2. **路径**：`/xmlrpc/2/common` 和 `/xmlrpc/2/object`
3. **认证**：使用 `authenticate()` 获取 uid
4. **任务查询**：必须使用 `('active', '=', True)` 过滤
5. **联系人类型**：`company`=公司，`contact`=联系人
6. **关联字段**：使用 ID 而非名称

---

---

## 📚 知识库 (Knowledge) 操作

### 核心模型

| 模型 | 说明 |
|------|------|
| `knowledge.article` | 知识库文章 |
| `knowledge.article.member` | 文章成员（权限管理） |

### 创建知识库文章

```python
import xmlrpc.client

url = 'https://www.huo15.com'
db = 'huo15'
user = 'postmaster@huo15.com'
password = '198809011ab'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# 创建文章（body 使用 HTML 格式）
article_id = models.execute_kw(db, uid, password, 'knowledge.article', 'create', [{
    'name': '文章标题',
    'body': '<h1>文章内容</h1><p>这里是正文</p>',
    'internal_permission': 'write',
}])
```

### 重要字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | Char | 文章标题 |
| `body` | Html | 文章内容（HTML格式） |
| `parent_id` | Many2one | 父文章ID |
| `internal_permission` | Selection | 内部权限: 'write', 'read', 'none' |
| `article_member_ids` | One2many | 成员列表 |

### 权限规则

| 权限 | 说明 |
|------|------|
| `write` | 可以编辑 |
| `read` | 只读 |
| `none` | 仅成员可见 |

### ⚠️ 常见错误

1. **Invalid field 'article_type'**：Odoo 19 没有这个字段，不要设置
2. **需要至少一个 writer**：当 `internal_permission='none'` 时，必须添加 write 权限的成员

### Markdown 转 HTML

```python
def markdown_to_html(text):
    html = text.replace('\n\n', '</p><p>')
    return f'<p>{html}</p>'
```

---

## 🐳 Odoo Docker 本地开发

### Docker 配置仓库

**地址**：https://cnb.cool/huo15/tools/odoo19_docker

**本地路径**：`~/workspace/study/odoo_study/odoo19_docker`

### 启动命令

```bash
cd ~/workspace/study/odoo_study/odoo19_docker
docker compose -p <项目名称> up --build
```

### 本地项目开发流程

#### 1. 建立项目目录

```
~/workspace/projects/<公司>/
  └── <公司>_addons/      ← 项目 addons 源码
```

#### 2. 创建软链接

```bash
ln -s ~/workspace/projects/<公司>/<公司>_addons \
       ~/workspace/study/odoo_study/odoo19_docker/<公司>_addons
```

#### 3. 修改 docker-compose.yml

```yaml
services:
  web:
    build: .
    volumes:
      - ./<公司>_addons:/usr/lib/python3/dist-packages/odoo/<公司>_addons
```

#### 4. 重启项目

```bash
docker compose -p <项目名称> down && \
docker compose -p <项目名称> up --build
```

---

## 📂 Odoo 源码位置

| 版本 | 路径 |
|------|------|
| Odoo 19 企业版 | `~/workspace/study/odoo_study/enterprise` |
| Odoo 19 社区版 | `~/workspace/study/odoo_study/odoo` |
| Docker 配置 | `~/workspace/study/odoo_study/odoo19_docker` |

---

## 🔗 相关技能

- **huo15-doc-template**：文档生成
