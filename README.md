# OpinioJurisSearcher 部署指引

独立检索 Opinio Juris 公共 WordPress 站点。只访问 `opiniojuris.org`。

仓库：<https://github.com/HuiwowICCSkills/OpinioJurisSearcher>（私有）。

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
