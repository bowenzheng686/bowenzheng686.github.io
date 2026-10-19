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
      '<span class="image-viewer-zoom" aria-label="当前缩放比例">100%</span>' +
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
    var zoomLabel = dialog.querySelector(".image-viewer-zoom");
    var currentScale = 1;
    var scaleMode = "fit";

    function fitScale() {
      if (!fullImage.naturalWidth || !fullImage.naturalHeight) return 1;
      return Math.min(1, viewport.clientWidth / fullImage.naturalWidth,
        viewport.clientHeight / fullImage.naturalHeight);
    }

    function setScale(nextScale, mode, pointer) {
      if (!fullImage.naturalWidth || !fullImage.naturalHeight) return;
      var imageX = 0;
      var imageY = 0;
      if (pointer) {
        var before = fullImage.getBoundingClientRect();
        imageX = Math.max(0, Math.min(fullImage.naturalWidth,
          (pointer.clientX - before.left) / currentScale));
        imageY = Math.max(0, Math.min(fullImage.naturalHeight,
          (pointer.clientY - before.top) / currentScale));
      }

      currentScale = nextScale;
      scaleMode = mode;
      fullImage.style.maxWidth = "none";
      fullImage.style.maxHeight = "none";
      fullImage.style.width = fullImage.naturalWidth * currentScale + "px";
      fullImage.style.height = fullImage.naturalHeight * currentScale + "px";
      fitButton.setAttribute("aria-pressed", String(mode === "fit"));
      originalButton.setAttribute("aria-pressed", String(mode === "original"));
      zoomLabel.textContent = Math.round(currentScale * 100) + "%";

      if (pointer) {
        var after = fullImage.getBoundingClientRect();
        viewport.scrollLeft += after.left + imageX * currentScale - pointer.clientX;
        viewport.scrollTop += after.top + imageY * currentScale - pointer.clientY;
      } else {
        viewport.scrollLeft = mode === "original"
          ? Math.max(0, (viewport.scrollWidth - viewport.clientWidth) / 2) : 0;
        viewport.scrollTop = mode === "original"
          ? Math.max(0, (viewport.scrollHeight - viewport.clientHeight) / 2) : 0;
      }
    }

    fitButton.addEventListener("click", function () { setScale(fitScale(), "fit"); });
    originalButton.addEventListener("click", function () { setScale(1, "original"); });
    viewport.addEventListener("wheel", function (event) {
      if (!dialog.open || !fullImage.naturalWidth) return;
      event.preventDefault();
      var delta = event.deltaY * (event.deltaMode === 1 ? 16
        : event.deltaMode === 2 ? viewport.clientHeight : 1);
      var minScale = Math.max(0.1, fitScale() / 4);
      var nextScale = Math.max(minScale,
        Math.min(4, currentScale * Math.exp(-delta * 0.0012)));
      if (Math.abs(nextScale - currentScale) > 0.001) {
        setScale(nextScale, "custom", event);
      }
    }, { passive: false });
    fullImage.addEventListener("load", function () {
      if (dialog.open && scaleMode === "fit") setScale(fitScale(), "fit");
    });
    window.addEventListener("resize", function () {
      if (dialog.open && scaleMode === "fit") setScale(fitScale(), "fit");
    });
    closeButton.addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener("close", function () {
      fullImage.removeAttribute("src");
      fullImage.removeAttribute("style");
      currentScale = 1;
      scaleMode = "fit";
    });

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
        currentScale = 1;
        scaleMode = "fit";
        dialog.showModal();
        fullImage.src = img.currentSrc || img.src;
        fullImage.alt = img.alt || "放大图片";
        if (fullImage.complete && fullImage.naturalWidth) setScale(fitScale(), "fit");
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
