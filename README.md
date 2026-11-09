# OpinioJurisSearcher 部署指引

独立检索 Opinio Juris 公共 WordPress 站点。只访问 `opiniojuris.org`。

仓库：<https://github.com/HuiwowICCSkills/OpinioJurisSearcher>（公开）。

## 环境

Python 3.10+，依赖 `requests`、`beautifulsoup4`、`pypdf`；无需登录。

## 安装与自检

```powershell
git clone https://github.com/HuiwowICCSkills/OpinioJurisSearcher.git "$env:USERPROFILE\.codex\skills\OpinioJurisSearcher"
python -m pip install -r "$env:USERPROFILE\.codex\skills\OpinioJurisSearcher\requirements.txt"
& "$env:USERPROFILE\.codex\skills\OpinioJurisSearcher\run.ps1" doctor
```

## 使用

```powershell
$oj = "$env:USERPROFILE\.codex\skills\OpinioJurisSearcher\run.ps1"
& $oj search "state immunity" --limit 10 --out './oj.json'
& $oj fetch 'https://opiniojuris.org/2026/...' --out './post.json' --text-out './post.txt'
```

## 边界

- WordPress API 返回 `content.rendered` 公开正文；受保护文章可能只有元数据。
- `total` 依赖 `X-WP-Total` 响应头；缺失时为 `null`，不等于零命中。
- 博客文章是评论/学术观点，不是一手裁判或条约。

## 实测效果（2026-11-09）

以下命令与结果来自本机 `~/.codex/skills/OpinioJurisSearcher` 的实网运行；检索日期 2026-11-09（Asia/Shanghai），输出为该次运行实际返回的 JSON 报告。

```powershell
& .\run.ps1 search 'sovereign immunity' --limit 5
```

- 状态：`ok`；`X-WP-Total` 报告 `total = 271`；本次返回 5 条。
- 代表性结果：

| 题名 | 类型 / 日期 | 链接 |
| --- | --- | --- |
| Sovereign Immunity in the UK: Two Conventions, Two Answers | retrieved_text；2026-09-09T12:00:24 | https://opiniojuris.org/2026/09/09/sovereign-immunity-in-the-uk-two-conventions-two-answers/ |
| Who Gets Held Accountable? US Sanctions Against Albanese and ICC Judges and the Missing Corporate Accountability in Gaza | retrieved_text；2026-10-10T08:00:29 | https://opiniojuris.org/2026/10/10/who-gets-held-accountable-us-sanctions-against-albanese-and-icc-judges-and-the-missing-corporate-accountability-in-gaza/ |
| Attacking Foreign Bases in Self-Defence | retrieved_text；2026-08-27T11:00:39 | https://opiniojuris.org/2026/08/27/attacking-foreign-bases-in-self-defence/ |

> 说明：`total = 271` 取自 WordPress `X-WP-Total` 响应头，是被检索站点自报的命中数。`result_type = retrieved_text`：`text` 是该文的公开渲染正文（`content.rendered`），不是摘要，篇幅在 1 万至 2 万字符量级。但 WordPress 只按关键词出现做相关性排序，本次 5 条里只有“Sovereign Immunity in the UK: Two Conventions, Two Answers”直接讨论主权豁免，其余两条分别讨论企业刑事责任与外国军事基地，属关键词命中而非同主题结果——命中数不等于相关性。博客文章是评论/学术观点（次级材料），不是一手裁判或条约。
