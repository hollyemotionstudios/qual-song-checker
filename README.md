# Song Match Prop

A mock song-recognition phone app for filming. It listens for about 3 seconds, then reveals **Funiculì, Funiculà**. Tapping the song-found screen goes back to the start. Everything runs in the browser; nothing is sent anywhere.

A synced-lyrics screen is built in but switched off. To bring it back, set `SHOW_LYRICS = true` in `index.html`.

Sized for the Samsung Galaxy Z Fold 8: the cover screen (about 416 × 658) and the unfolded screen (about 816 × 616) get their own layouts.

## On set

| Action | How |
| --- | --- |
| Start listening | Tap the orb, or press <kbd>Space</kbd> |
| Start over from song found | Tap anywhere on the song-found screen, or press <kbd>Space</kbd> |
| Reset to start | Tap anywhere along the top of the screen, or press <kbd>R</kbd> / <kbd>Esc</kbd> |
| Crew settings | Hold the top-right corner of the start screen, or press <kbd>S</kbd> |

Crew settings (title, artist, detail line, listening time) are saved on the device that changed them.

## Files

- `index.html` is the whole app. It is written without `<html>`, `<head>` or `<body>` tags so it can also be published as a Claude Artifact.
- `build.py` wraps it into a standalone page.
- `.github/workflows/pages.yml` runs that build and deploys to GitHub Pages on every push to `main`.
- `vercel.json` tells Vercel to run the same build and serve `_site`, so the repo also deploys on Vercel.

To preview the standalone page locally:

```bash
python3 build.py index.html _site/index.html && open _site/index.html
```
