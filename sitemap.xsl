<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Sitemap - Arcade Games Hub</title>
        <style>
          body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#fff8e7;color:#1e1e2f;margin:0;padding:32px 20px;}
          .wrap{max-width:1000px;margin:0 auto;}
          h1{font-size:1.6rem;margin-bottom:4px;}
          .sub{color:#666;margin-bottom:22px;font-size:.95rem;}
          .count{display:inline-block;background:#ffd23f;border:3px solid #1e1e2f;border-radius:12px;padding:4px 16px;font-weight:700;box-shadow:3px 3px 0 #1e1e2f;margin-bottom:18px;}
          table{width:100%;border-collapse:collapse;background:#fff;border:3px solid #1e1e2f;border-radius:14px;overflow:hidden;box-shadow:5px 5px 0 #1e1e2f;}
          th{background:#1e1e2f;color:#ffd23f;text-align:left;padding:12px 14px;font-size:.9rem;}
          td{padding:11px 14px;border-top:2px solid #eee;font-size:.88rem;}
          tr:nth-child(even){background:#fbfbf6;}
          a{color:#7c4dff;text-decoration:none;word-break:break-all;}
          a:hover{text-decoration:underline;}
          .lang{display:inline-block;background:#3ec1f3;color:#fff;border-radius:6px;padding:1px 8px;font-size:.75rem;font-weight:700;margin-right:6px;}
          .foot{margin-top:18px;color:#888;font-size:.82rem;}
        </style>
      </head>
      <body>
        <div class="wrap">
          <h1>🕹️ Arcade Games Hub — Sitemap</h1>
          <p class="sub">This XML sitemap is for search engines. You are viewing a human-readable rendering.</p>
          <div class="count"><xsl:value-of select="count(sm:urlset/sm:url)"/> URLs</div>
          <table>
            <tr>
              <th>#</th>
              <th>URL</th>
              <th>Lang</th>
              <th>Last Modified</th>
              <th>Priority</th>
            </tr>
            <xsl:for-each select="sm:urlset/sm:url">
              <tr>
                <td><xsl:value-of select="position()"/></td>
                <td><a href="{sm:loc}"><xsl:value-of select="sm:loc"/></a></td>
                <td>
                  <span class="lang">
                    <xsl:choose>
                      <xsl:when test="contains(sm:loc, '/zh/') or substring(sm:loc, string-length(sm:loc)-2) = '/zh'">zh-CN</xsl:when>
                      <xsl:when test="contains(sm:loc, '/es/') or substring(sm:loc, string-length(sm:loc)-2) = '/es'">es</xsl:when>
                      <xsl:when test="contains(sm:loc, '/ar/') or substring(sm:loc, string-length(sm:loc)-2) = '/ar'">ar</xsl:when>
                      <xsl:when test="contains(sm:loc, '/ru/') or substring(sm:loc, string-length(sm:loc)-2) = '/ru'">ru</xsl:when>
                      <xsl:when test="contains(sm:loc, '/ja/') or substring(sm:loc, string-length(sm:loc)-2) = '/ja'">ja</xsl:when>
                      <xsl:when test="contains(sm:loc, '/ko/') or substring(sm:loc, string-length(sm:loc)-2) = '/ko'">ko</xsl:when>
                      <xsl:otherwise>en</xsl:otherwise>
                    </xsl:choose>
                  </span>
                </td>
                <td><xsl:value-of select="sm:lastmod"/></td>
                <td><xsl:value-of select="sm:priority"/></td>
              </tr>
            </xsl:for-each>
          </table>
          <p class="foot">Submit this sitemap to Google Search Console &amp; Bing Webmaster Tools.</p>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
