# Sticker edit prompt

Use this prompt for each curated source image:

```text
Use case: background extraction.
Asset type: modern static chat reaction sticker.

Preserve the exact original subject, pose, expression, colors, crop, and texture from the supplied source image. Isolate the existing subject cleanly and add only a smooth opaque white die-cut outline of moderate thickness that follows the nontransparent silhouette.

Keep the surrounding canvas genuinely transparent. Keep small silhouette details when they remain readable at chat size.

Do not add or redraw objects. Do not add text, a scene, a background, a drop shadow, a colored glow, a watermark, or a checkerboard. Do not turn the subject into a new illustration. Do not change the expression, anatomy, clothing, or recognizable visual details.
```

If a source already has clean transparency, keep its cutout and add the border. If it has a simple background, remove only that background. Reject the result if the model materially redraws the subject.
