# Opinio Juris 实测记录（2026-11-09）

`https://opiniojuris.org/wp-json/wp/v2/posts`

参数：`search`、`per_page`、`offset`。

实测 `state immunity --limit 1` → `status=ok`、`total=574`、1 条；`content.rendered` 返回公开正文。`fetch` 文章页 → `text_characters=21901`。

边界：`X-WP-Total` 缺失时 `total=null`；受保护文章可能只有元数据。
