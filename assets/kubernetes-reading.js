(function () {
  "use strict";
  var doc = document;

  function compactCopyButtons(article) {
    article.querySelectorAll("pre.has-copy-button").forEach(function (pre) {
      var button = pre.querySelector("button.code-copy");
      if (!button || pre.parentElement.classList.contains("k8-code-shell")) return;
      var shell = doc.createElement("div");
      shell.className = "k8-code-shell";
      pre.parentNode.insertBefore(shell, pre);
      shell.appendChild(pre);
      shell.appendChild(button);
    });
  }

  function linkifyBareUrls(article) {
    var candidates = [];
    var walker = doc.createTreeWalker(article, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!/https?:\/\//i.test(node.nodeValue || "")) return NodeFilter.FILTER_REJECT;
        if (node.parentElement && node.parentElement.closest("a, script, style, textarea")) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (walker.nextNode()) candidates.push(walker.currentNode);
    candidates.forEach(function (node) {
      var source = node.nodeValue;
      var matches = Array.from(source.matchAll(/https?:\/\/[^\s<>"']+/gi));
      if (!matches.length) return;
      var fragment = doc.createDocumentFragment();
      var offset = 0;
      matches.forEach(function (match) {
        var raw = match[0];
        var url = raw.replace(/[.,;:!?。，；：！？)\]\}]+$/u, "");
        if (!url) return;
        fragment.appendChild(doc.createTextNode(source.slice(offset, match.index)));
        var anchor = doc.createElement("a");
        anchor.href = url;
        anchor.textContent = url;
        fragment.appendChild(anchor);
        offset = match.index + url.length;
      });
      fragment.appendChild(doc.createTextNode(source.slice(offset)));
      node.replaceWith(fragment);
    });
    article.querySelectorAll("a[href]").forEach(function (anchor) {
      try {
        var url = new URL(anchor.href, location.href);
        if (/^https?:$/.test(url.protocol) && url.host !== location.host) {
          anchor.target = "_blank";
          anchor.rel = "noopener noreferrer";
        }
      } catch (error) { /* Preserve unusual local and fragment links. */ }
    });
  }

  function sizeImages(article) {
    article.querySelectorAll("img").forEach(function (img) {
      function setSize() {
        if (img.classList.contains("k8-image-wide") || img.classList.contains("k8-image-small")) return;
        var ratio = img.naturalWidth / Math.max(1, img.naturalHeight);
        if (ratio > 2.15) img.classList.add("k8-image-wide");
        else if (img.naturalWidth < 520) img.classList.add("k8-image-small");
      }
      if (img.complete) setSize();
      else img.addEventListener("load", setSize, { once: true });
    });
  }

  function initialize() {
    var article = doc.getElementById("post-content");
    if (!article) return;
    compactCopyButtons(article);
    window.requestAnimationFrame(function () { compactCopyButtons(article); });
    window.addEventListener("load", function () { compactCopyButtons(article); }, { once: true });
    linkifyBareUrls(article);
    sizeImages(article);
  }
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", initialize, { once: true });
  else initialize();
}());
