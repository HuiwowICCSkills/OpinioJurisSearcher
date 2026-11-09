---
name: OpinioJurisSearcher
description: 独立检索 Opinio Juris 公共 WordPress 站点，按关键词返回文章题名、日期、作者和公开渲染正文；支持按 URL 读取文章页面。
---

# OpinioJurisSearcher

> **`<skill-dir>`** = 本 SKILL.md 所在目录。核心脚本为 `<skill-dir>/scripts/opiniojuris_search.py`；Windows 用 `<skill-dir>/run.ps1`，macOS/Linux 用 `<skill-dir>/run.sh`。部署与排错见 [README.md](README.md)。

这个 skill 只做 `opiniojuris.org` 一个站点，使用公开 WordPress REST API：

- `search`：`/wp-json/wp/v2/posts`，返回题名、链接、日期、作者 ID 和公开渲染正文；
- `fetch`：按文章 URL 读取页面文本；
- `doctor`：探测 WordPress API。

## 命令

```powershell
& '<skill-dir>/run.ps1' search "state immunity" --limit 10 --out './opinio.json'
& '<skill-dir>/run.ps1' fetch 'https://opiniojuris.org/2026/...' --out './post.json' --text-out './post.txt'
& '<skill-dir>/run.ps1' doctor
```

通用参数：`--out`、`--cache`、`--cache-ttl`、`--offline`、`--timeout`；`search` 另有 `--limit`、`--offset`；`fetch` 另有 `--text-out`。

## 结果边界

- WordPress API 的 `content.rendered` 是公开正文；受保护或插件限制的文章可能只返回元数据，`result_type` 会区分。
- `total` 来自 `X-WP-Total` 响应头（若站点提供）；没有该头时为 `null`，不能当作零命中。
- 博客文章是评论/学术观点，不是一手裁判或条约；引用时标明作者、日期和博客性质。

## 参考

- 2026-11-09 实测：WordPress API、`state immunity` 命中与正文读取：[references/opiniojuris-search.md](references/opiniojuris-search.md)
- 部署、环境与排错：[README.md](README.md)
