# docs/ — 仓库级记忆与经验

> 本目录存放 huo15-skills 仓库级的**记忆、经验、重要聊天摘要**等 Markdown 文件。
> 不存放各 skill 自身的 changelog（那个在 `<slug>/docs/changelog.md`）。

## 文件索引

| 文件 | 内容 |
|---|---|
| [experience.md](experience.md) | 开发经验与踩坑记录（长期维护） |
| [changelog.md](changelog.md) | 仓库级重要变更（新 skill 上架、架构调整等） |

## 使用约定

- `experience.md` — 每次踩坑或有值得沉淀的教训，追加一条到对应章节
- `changelog.md` — 每次有仓库级（非 skill 级）的重大变更时记录
- `chats/` — 可在此存放重要对话摘要（`.md` 格式，按日期命名：`YYYY-MM-DD-<topic>.md`）
- `memory/` — 可在此存放跨 session 的项目记忆条目

## 不存放于此的内容

- 各 skill 版本历史 → `<slug>/docs/changelog.md`
- 凭据 / token → 见 `~/CLAUDE.md §2`
- 个人笔记与草稿 → `docs/private/`（已加入 `.gitignore`）
