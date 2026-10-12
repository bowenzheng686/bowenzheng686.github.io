---
layout: default
title: 首页
home: true
---

<main id="main-content">
  <section id="top" class="hero section-shell" aria-labelledby="hero-title">
    <div class="hero-copy">
      <p class="eyebrow hero-kicker"><span class="status-dot" aria-hidden="true"></span>BOWEN / NOTES &amp; EXPERIMENTS</p>
      <h1 id="hero-title" class="hero-title">Bowen 的<br><span>技术笔记。</span></h1>
      <p class="hero-description">记录编程实践、网络探索与日常思考。<br>让每次学习，都留下可以回看的轨迹。</p>
      <div class="hero-actions">
        <a class="button button-primary" href="#writing">阅读文章 <span aria-hidden="true">→</span></a>
        <a class="button button-secondary" href="#subjects">浏览专题 <span aria-hidden="true">↘</span></a>
        <a class="button button-secondary" href="#about">关于我 <span aria-hidden="true">↘</span></a>
      </div>
      <div class="hero-footnote">
        <a href="https://github.com/bowenzheng686" target="_blank" rel="noopener noreferrer">在 GitHub 继续探索 <span aria-hidden="true">↗</span></a>
      </div>
    </div>

    <div class="hero-visual" aria-hidden="true">
      <div class="holo-aura"></div>
      <div class="holo-grid"></div>
      <div class="holo-stage" id="holo-stage">
        <div class="holo-orbit holo-orbit-one"></div>
        <div class="holo-orbit holo-orbit-two"></div>
        <div class="holo-orbit holo-orbit-three"></div>
        <div class="holo-cube">
          <div class="cube-face cube-front"><span>&lt;/&gt;</span><small>CREATE</small></div>
          <div class="cube-face cube-back"><span>∞</span><small>EXPLORE</small></div>
          <div class="cube-face cube-right"><span>01</span><small>BUILD</small></div>
          <div class="cube-face cube-left"><span>⌘</span><small>THINK</small></div>
          <div class="cube-face cube-top"><span>✦</span><small>DISCOVER</small></div>
          <div class="cube-face cube-bottom"><span>{ }</span><small>LEARN</small></div>
        </div>
        <span class="holo-node holo-node-one"></span>
        <span class="holo-node holo-node-two"></span>
        <span class="holo-node holo-node-three"></span>
      </div>
      <div class="holo-coordinate holo-coordinate-top">BOWEN / DIGITAL SPACE <span>001</span></div>
      <div class="holo-coordinate holo-coordinate-bottom"><span class="holo-live"></span> IDEAS IN MOTION <span>● ● ●</span></div>
    </div>
    <a class="hero-scroll" href="#writing" aria-label="向下浏览文章"><span>SCROLL TO EXPLORE</span><span aria-hidden="true">↓</span></a>
  </section>

  <section id="subjects" class="section-shell writing" aria-labelledby="subjects-title">
    <div class="section-heading">
      <div>
        <p class="eyebrow">SUBJECTS</p>
        <h2 id="subjects-title">专题内容</h2>
      </div>
      <p class="section-intro">按主题循序阅读，每个章节都可独立打开。</p>
    </div>
    <ul class="post-grid">
      <li class="post-item">
        <a class="post-card subject-spotlight" href="{{ '/subjects/Linux/' | relative_url }}">
          <div class="subject-content">
            <div class="post-meta"><span class="post-category">LINUX / FIELD NOTES</span><span>18 个章节</span></div>
            <h3 class="post-title">从命令行开始，<br>理解整个系统。</h3>
            <p class="post-excerpt">从发行版、文件系统与权限，到服务、存储、容器和故障排查。</p>
            <div class="post-card-footer"><span>探索 Linux 学习笔记</span><span aria-hidden="true">↗</span></div>
          </div>
          <div class="subject-preview" aria-hidden="true">
            <div class="preview-toolbar"><span class="preview-dots"><i></i><i></i><i></i></span><span>linux / field-notes</span></div>
            <div class="preview-code"><p><span>$</span> cat learning-path.md</p><p>01&nbsp; 发行版与文件系统</p><p>02&nbsp; 用户、权限与进程</p><p>03&nbsp; 服务、存储与网络</p><p>04&nbsp; 容器与故障排查</p><strong>18 CHAPTERS&nbsp; ↗</strong></div>
          </div>
        </a>
      </li>
    </ul>
    <p><a class="text-link" href="{{ '/subjects/' | relative_url }}">查看专题目录 →</a></p>
  </section>
  {% assign post_count = site.posts | size %}
  <section id="writing" class="section-shell writing" aria-labelledby="writing-title">
    <div class="section-heading">
      <div>
        <p class="eyebrow">WRITING</p>
        <h2 id="writing-title">最新文章 <span class="count-badge" aria-label="{{ post_count }} 篇文章">{{ post_count }}</span></h2>
      </div>
      <p class="section-intro">把过程写下来，把问题想明白。</p>
    </div>

    {% if post_count > 0 %}
    <div class="writing-toolbar">
      <div class="search-field">
        <label class="accessible" for="post-search">搜索文章标题、摘要或分类</label>
        <span class="search-icon" aria-hidden="true">⌕</span>
        <input id="post-search" type="search" name="q" placeholder="搜索标题、摘要或分类…" autocomplete="off" spellcheck="false" aria-controls="post-grid" aria-describedby="filter-status">
      </div>
      <div id="post-filters" class="filter-list" role="group" aria-label="按文章分类筛选">
        <button class="filter-button" type="button" data-filter="all" aria-pressed="true">全部</button>
        {% assign sorted_categories = site.categories | sort %}
        {% for category in sorted_categories %}
        <button class="filter-button" type="button" data-filter="category" data-category="{{ category[0] | escape }}" aria-pressed="false">{{ category[0] | escape }}</button>
        {% endfor %}
      </div>
    </div>
    <p id="filter-status" class="filter-status" role="status" aria-live="polite">共 {{ post_count }} 篇文章</p>
    <ul id="post-grid" class="post-grid">
      {% for post in site.posts %}
      {% assign post_excerpt = post.excerpt | strip_html | strip_newlines | strip %}
      {% capture post_search %}{{ post.title }} {{ post_excerpt }} {{ post.categories | join: ' ' }}{% endcapture %}
      <li class="post-item" data-search="{{ post_search | escape }}" data-categories='{{ post.categories | jsonify | escape }}'>
        <a class="post-card" href="{{ post.url | relative_url }}">
          <div class="post-meta">
            <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y.%m.%d" }}</time>
            <span class="post-category">{{ post.categories | first | default: '随笔' | escape }}</span>
          </div>
          <h3 class="post-title">{{ post.title | escape }}</h3>
          <p class="post-excerpt">{% if post_excerpt != '' %}{{ post_excerpt | truncate: 140 | escape }}{% else %}点击阅读全文。{% endif %}</p>
          <div class="post-card-footer"><span>阅读全文</span><span aria-hidden="true">↗</span></div>
        </a>
      </li>
      {% endfor %}
    </ul>
    <p id="no-results" class="empty-state filter-empty" hidden>没有找到匹配的文章。试试其他关键词，或切换到“全部”分类。</p>
    {% else %}
    <div class="empty-state">
      <span class="empty-state-icon" aria-hidden="true">✦</span>
      <p class="eyebrow">FIRST PAGE</p>
      <h3>故事，从下一篇开始。</h3>
      <p>这里还没有发布的文章。<br>新的想法，会在写下时慢慢成形。</p>
      <a class="text-link" href="https://github.com/bowenzheng686" target="_blank" rel="noopener noreferrer" aria-label="先去 GitHub 看看，在新标签页打开">先去 GitHub 看看 <span aria-hidden="true">↗</span></a>
    </div>
    {% endif %}
  </section>

  <section id="about" class="section-shell about" aria-labelledby="about-title">
    <div class="about-heading">
      <p class="eyebrow">ABOUT THIS SPACE</p>
      <h2 id="about-title">在探索中，<br>不断更新自己。</h2>
      <p class="about-signature">BOWENZHENG686</p>
    </div>
    <div class="about-copy">
      <p class="about-lead">这是一个用来记录、整理与分享的地方。</p>
      <p>把遇到的问题拆开，把实践里的发现写下，也给尚未想清楚的事留一点空间。</p>
      <p>这里用来收集技术学习与日常思考中的笔记：记录问题、理解过程，再把有用的发现整理成可以回看的文字。</p>
      <ul class="topic-tags" aria-label="关注的话题">
        <li>编程与开发</li>
        <li>系统与网络</li>
        <li>学习与思考</li>
      </ul>
    </div>
  </section>

  <section class="section-shell contact-strip" aria-labelledby="contact-title">
    <div>
      <p class="eyebrow">KEEP EXPLORING</p>
      <h2 id="contact-title">更多探索，在 GitHub。</h2>
    </div>
    <a class="button button-primary" href="https://github.com/bowenzheng686" target="_blank" rel="noopener noreferrer" aria-label="访问 GitHub，在新标签页打开">访问 GitHub <span aria-hidden="true">↗</span></a>
  </section>
</main>
