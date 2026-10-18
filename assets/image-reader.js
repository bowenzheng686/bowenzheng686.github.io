(function () {
  "use strict";

  function initialize() {
    var article = document.getElementById("post-content") || document.querySelector("main.container, .container");
    if (!article) return;
    var images = Array.from(article.querySelectorAll("img"));
    if (!images.length) return;

    var dialog = document.createElement("dialog");
    dialog.className = "image-viewer";
    dialog.setAttribute("aria-label", "查看原尺寸图片");
    dialog.innerHTML = '<div class="image-viewer-toolbar">' +
      '<span class="image-viewer-label">图片查看</span>' +
      '<button type="button" data-image-fit aria-pressed="true">适应窗口</button>' +
      '<button type="button" data-image-original aria-pressed="false">原始大小</button>' +
      '<button type="button" data-image-close aria-label="关闭图片">关闭</button>' +
      '</div><div class="image-viewer-viewport"><img alt=""></div>';
    document.body.appendChild(dialog);

    var viewport = dialog.querySelector(".image-viewer-viewport");
    var fullImage = viewport.querySelector("img");
    var fitButton = dialog.querySelector("[data-image-fit]");
    var originalButton = dialog.querySelector("[data-image-original]");
    var closeButton = dialog.querySelector("[data-image-close]");

    function setScale(original) {
      fullImage.classList.toggle("image-viewer-original", original);
      fitButton.setAttribute("aria-pressed", String(!original));
      originalButton.setAttribute("aria-pressed", String(original));
      window.requestAnimationFrame(function () {
        viewport.scrollLeft = original ? Math.max(0, (viewport.scrollWidth - viewport.clientWidth) / 2) : 0;
        viewport.scrollTop = original ? Math.max(0, (viewport.scrollHeight - viewport.clientHeight) / 2) : 0;
      });
    }

    fitButton.addEventListener("click", function () { setScale(false); });
    originalButton.addEventListener("click", function () { setScale(true); });
    closeButton.addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener("close", function () { fullImage.removeAttribute("src"); });

    images.forEach(function (img) {
      try {
        var pathname = decodeURIComponent(new URL(img.src, location.href).pathname);
        var subjectIndex = pathname.indexOf("/subjects/");
        var imagePath = subjectIndex < 0 ? "" : pathname.slice(subjectIndex + 1);
        var displayWidths = window.bowenImageOriginalWidths || {};
        var logicalWidth = displayWidths[imagePath];
        if (typeof logicalWidth === "number" && logicalWidth > 0) {
          img.style.width = logicalWidth + "px";
          img.style.maxWidth = "100%";
        }
      } catch (error) { /* Unknown image URLs keep their browser default size. */ }

      var existing = img.closest("a[href]");
      if (existing) {
        try {
          if (new URL(existing.href, location.href).href !== new URL(img.src, location.href).href) return;
        } catch (error) { return; }
      }
      var anchor = existing || document.createElement("a");
      if (!existing) {
        anchor.href = img.getAttribute("src") || img.src;
        img.parentNode.insertBefore(anchor, img);
        anchor.appendChild(img);
      }
      anchor.classList.add("image-reader-link");
      anchor.setAttribute("aria-label", "查看原尺寸图片：" + (img.alt || "插图"));
      anchor.addEventListener("click", function (event) {
        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        if (typeof dialog.showModal !== "function") return;
        event.preventDefault();
        fullImage.src = img.currentSrc || img.src;
        fullImage.alt = img.alt || "放大图片";
        setScale(false);
        dialog.showModal();
        closeButton.focus();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
}());
