[English](README.en.md) | 中文

# 小马绘画 · MLP G4 Skill

面向 AI 绘画的《小马宝莉》G4（Friendship is Magic）同人绘画规则包，可作为 Codex / ChatGPT Skill 使用。

它解决三个反复出现的问题：形体画错（多腿、前蹄画成人的手、翅膀从肋部长出）、角色画错（体色 / 发色 / Cutie Mark 被替换）、流程不可复现（每次生成的步骤、画风和验收标准都不一样）。

## 安装

1. 到 [Releases](../../releases) 下载最新的 `mlp-g4-official-style_vX.Y.zip`。
2. 解压到 Codex 的 skills 目录：Windows 为 `%USERPROFILE%\.codex\skills\`，其他平台为 `~/.codex/skills/`。
3. 确认路径为 `.../skills/mlp-g4-official-style/SKILL.md`。

升级：下载新版本 zip，直接覆盖同名目录即可，不需要先删除旧目录。

## 分层结构

规则按四层组织，层与层之间不重复同一句话，读取时按需加载：

| 层 | 内容 | 位置 |
|---|---|---|
| L0 | 小马基本形体：比例、四肢与前蹄、飞马双翼、Cutie Mark、身份常量、P0 判据 | `references/body-base.md` |
| L1 | 绘画基本流程：构图、骨架、体块、结构自检、线稿与光影、细节、验收 | `references/drawing-process.md` |
| L2 | 画风模块：官方 G4（默认）、国风·敦煌飞天 | `references/styles/` |
| L3 | 角色库：8 位角色，条目内按画风分子条目 | `references/characters/` |

另有一套独立的验收优先级：**P0** 形体与解剖、**P1** 角色身份与画风、**P2** 光影与装饰。P0 错误不能用画风或光影弥补。

## 目录

```text
mlp-g4-official-style/
├── SKILL.md                        入口：优先级、分层路由、画风隔离、生成前检查
├── CHANGELOG.md                    带版本号的更新记录
├── agents/openai.yaml              UI 元数据与调用策略
├── assets/icon.svg
└── references/
    ├── body-base.md                L0
    ├── drawing-process.md          L1
    ├── styles/
    │   ├── g4-official.md          L2 默认画风
    │   └── dunhuang-feitian.md     L2 国风·敦煌飞天
    └── characters/
        ├── _template.md            新增角色的模板
        ├── fluttershy.md           柔柔
        ├── rainbow-dash.md         云宝
        ├── twilight-sparkle.md     紫悦
        ├── rarity.md               珍奇
        ├── applejack.md            苹果嘉儿
        ├── pinkie-pie.md           碧琪
        ├── princess-celestia.md    塞拉斯蒂娅
        └── princess-luna.md        露娜
```

## 用法

安装后直接说需求即可，Skill 会自动接管；也可以显式点名：

```text
用 $mlp-g4-official-style 画云宝在敦煌飞天风格下回眸
```

出图后它会给出固定的 4 行自检输出（计数、身份、结构、判定），结构不过会直接判 REJECTED 并回退重做，而不是在错图上继续加细节。

## 扩展

- **加角色**：复制 `references/characters/_template.md`，填身份常量与常见错法；不需要改 `SKILL.md`。
- **加画风**：在 `references/styles/` 下新增一个文件，只描述该画风的线条、配色、材质与氛围。画风模块互相独立，不做混搭，也不覆盖 L0 的形体规则。
- **改规则**：形体规则只写在 L0，流程只写在 L1；同一句话只允许出现在一个文件里。

## 版本

发版流程：更新 `CHANGELOG.md` 的版本号 → 打包（本地文件名用 `小马绘画_vX.Y_覆盖安装版.zip`）→ 发布 Release → 删除本地 zip。历史版本见 [Releases](../../releases)。

注意：GitHub 的 Release 资产名不支持中文，上传时中文会被丢弃（`小马绘画_v2.1_覆盖安装版.zip` 会变成 `_v2.1_.zip`），因此资产统一上传为 ASCII 名 `mlp-g4-official-style_vX.Y.zip`，解压后的目录名不受影响。
