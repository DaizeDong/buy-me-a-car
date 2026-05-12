# buy-me-a-car 🚗💸

> 🛒 **让 Claude Code 帮你买车。** 9 个网站平行抓库存、群发 30+ dealer 邮件、cron 监控收件箱、起草砍价回复、生成专业 OTD 提案 PDF —— 全自动。
>
> 🪶 **零依赖，零锁定。** 纯 Markdown skill + Python 脚本 + HTML 模板。换成 Codex、Cursor、Trae、自己的 agent 一样能跑。Fork 它、改它、为你的市场适配它。
>
> _💡 这不是平台，是工作流。买完你的车，把它带去下一个朋友的购车任务。🌱_

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![All 50 States](https://img.shields.io/badge/Tax%20Data-50%20States%20%2B%20DC-green?style=flat)](skills/buy-me-a-car/references/state_fees.md)
[![Roadmap](https://img.shields.io/badge/Roadmap-35%2B%20Ideas-purple?style=flat)](ROADMAP.md)

---

## 🎯 不止一次砍价

**Quick mode** — 一句话启动全流程：

```
help me buy a used compact SUV this week, budget $25k OTD, under 60k miles, near <ZIP>
```

Claude 自动 confirm 需求 → 9 个 subagent 并行抓 Carfax / CarMax / Carvana / Cars.com / AutoTrader / Edmunds / TrueCar / CarGurus / Enterprise → 汇总 top 30 候选 → 群发 lead form → 设 cron 每 15 分钟扫 Gmail 起草回复。

**砍价 mode** — Dealer 给了 OTD？锚定 + 反击：

```
the dealer asking $32,200 OTD, target $30k — write me a counter
```

Claude 用 3 种 anchor 起草 plain-ASCII 回信：(1) Dealer 自家库存内部价差、(2) 区域市场 comp（AutoTrader / KBB / CarGurus）、(3) 已锁的竞品 OTD。

**Dossier mode** — 试驾前打印一份专业市场调研：

```bash
cp assets/dossier_config_template.yaml my_offer.yaml
$EDITOR my_offer.yaml   # 填买方 + 目标车 + 竞品 OTD + 数据来源

python scripts/generate_dossier.py \
  --config my_offer.yaml \
  --output my_offer.html \
  --to-pdf my_offer.pdf
```

8-页 PDF（英文 + 中文模板），含市场均价、配置对比、CPO 价值、内部价差分析、报价结构、交易条件 —— Show to dealer 完全合格。

---

## 🚀 安装

```
/plugin install github:DaizeDong/buy-me-a-car
```

或手动 clone：

```bash
git clone https://github.com/DaizeDong/buy-me-a-car.git ~/.claude/plugins/buy-me-a-car
```

Skill 在 Claude Code 里说"帮我找车 / 买车 / help me buy a car"等任意触发短语时自动激活。

---

## ✨ 功能亮点

| | 内容 |
|---|---|
| 🔍 **多站点研究** | 9 站点并行 subagent + Carfax 主战场 |
| 📧 **群发邮件** | Plain-ASCII 模板 + 严格无 markdown 无 em-dash |
| ⏰ **Cron 监控** | 15-min Gmail 扫描 + 起草回复 + 跟踪 thread |
| 💰 **OTD 计算器** | 全 **50 州 + DC** tax/doc/title/reg 数据 |
| 📐 **里程折损计算** | Black Book / Manheim 标准（按 SUV/sedan/luxury 分段）|
| 📄 **PDF 分析** | CARFAX / 服务记录 / Dealer 报价 自动审 |
| 🎨 **Dossier 生成** | YAML 配置 → HTML → Chrome headless PDF（EN + CN）|
| 🚫 **Anti-bot 处理** | Playwright MCP 集成（CarGurus / Cars.com / AutoTrader 等）|

---

## 🛠 内置工具

```
buy-me-a-car/
├── skills/buy-me-a-car/
│   ├── SKILL.md                          # 8-phase 工作流
│   ├── references/                       # 加载时按需读
│   │   ├── outreach_strategy.md          # 群发策略 + anti-bot
│   │   ├── negotiation_playbook.md       # 3 种 anchor + walk-away
│   │   ├── pdf_review_checklist.md       # CARFAX / 报价 PDF 审核
│   │   ├── cron_monitoring.md            # Cron prompt 模板
│   │   ├── state_fees.md                 # 50 州 + DC
│   │   ├── email_format_rules.md         # 纯 ASCII 规则
│   │   └── subaru_cpo_program.md         # CPO 嵌入价值
│   ├── assets/                           # 复制 + 编辑模板
│   │   ├── dealer_reply_template.md      # 10+ 回信模板
│   │   ├── tracker_template.md           # Tracker 骨架
│   │   ├── dossier_template.html         # 英文 dossier
│   │   ├── dossier_template_cn.html      # 中文 dossier
│   │   ├── dossier_config_template.yaml  # 80+ placeholder 配置
│   │   └── negotiation_prep_template.md  # 私人砍价 prep
│   └── scripts/                          # 工具脚本
│       ├── otd_calculator.py             # 50 州 OTD 反推
│       ├── mileage_adjustment.py         # 里程折损
│       ├── generate_dossier.py           # YAML → HTML/PDF
│       └── html_to_pdf.sh                # 独立 HTML → PDF
├── ROADMAP.md                            # 35+ 候选 feature
└── LICENSE                               # MIT
```

---

## 📈 真实运行效果

> 这个 skill 用了 2 天完成一个真实购车流程的全部 outreach + 谈判工作。结果：

- **38 个 dealer** 自动联系 + cron 跟踪回复
- **4 份 written OTD** 从 $20,348 到 $32,200 区间
- **2 个 dealer** 礼貌 walk away（Circle / Freehold）— 没浪费成交时间
- **1 个本地 dealer** 通过非聚合渠道找到（同城关系价值）
- **节省估计 $5-9k** vs 单 dealer 冷买（保守估算）

详见 [process retrospective](#) 完整时间线 + lessons learned。

---

## 🔄 工作流（8 phase）

```
1. 定义需求           需求 + 车型 + 里程 + 预算 + ZIP
2. 多站点研究         9 subagent 并行 → 30 top 候选
3. 群发邮件           Carfax 主战场 + playwright 处理 anti-bot
4. Cron 收件箱监控    15-min Gmail 扫描 + 起草 + skip autoresponder
5. OTD 谈判           3 种 anchor + walk-away + 加价拒绝
6. PDF 分析           CARFAX / service / quote 审核
7. Dossier 生成       YAML → HTML → PDF（EN/CN）
8. 试驾 + 关单        检查表 + 决策矩阵 + 关单 checklist
```

完整 phase 说明见 [`SKILL.md`](skills/buy-me-a-car/SKILL.md)。

---

## 🤝 贡献

Roadmap 上有 **35+ ideas** 分 7 类（[ROADMAP.md](ROADMAP.md)）：

- A. 工作流增强（6） — thread dedup / playwright bundle / attachment 抽取
- B. 新车型（5） — Lease / 新车 / EV / trade-in tax
- C. 工具基建（7） — OEM CPO 数据库 / NHTSA recall API / VIN decoder
- D. 数据社区（5） — Shared transaction dataset / dealer ratings
- E. 多市场（4） — Spanish / Canadian / EU / 自动翻译
- F. 售后阶段（4） — Closing day / 30 天 guide / insurance
- G. 投机性（4） — Voice negotiation / multi-buyer 协作

挑一个 → 开 GitHub issue → PR。

---

## 📝 License

MIT — Fork it, ship it, sell cars with it.

---

## ✍️ Author

[@DaizeDong](https://github.com/DaizeDong) — 这个 skill 来自一次购车流程的总结。从 idea 到 plugin 上 GitHub 共 12 小时。如果它帮你省到了钱，🌟 一下 repo 就是最好的回报。
