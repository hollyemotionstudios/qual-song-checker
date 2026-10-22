# Song Match Prop

A mock song-recognition phone app for filming. It listens for about 3 seconds and reveals **Funiculì, Funiculà**. Tapping **Play full song** opens the lyrics screen, which scrolls the Neapolitan lyrics in time with a smaller English translation under each line, with play/pause and a progress bar you can drag. Everything runs in the browser; nothing is sent anywhere.

To end the flow at the song-found screen instead (a tap there starts over), set `SHOW_LYRICS = false` in `index.html`.

Sized for the Samsung Galaxy Z Fold 8. The app picks its layout from the screen's shape: the front screen (1048 × 948) gets the single-column layout, scaled up to fill it, and the unfolded screen (986 × 624), or any screen wider than about 1.3:1, gets the two-column layout. Narrow phone-sized screens get the single-column layout at normal size.

## On set

| Action | How |
| --- | --- |
| Start listening | Tap the orb, or press <kbd>Space</kbd> |
| Open the lyrics | Tap **Play full song**, or press <kbd>Space</kbd>. The song-found screen waits until then |
| Pause / play lyrics | Tap the play button, or press <kbd>Space</kbd> |
| Jump in the song | Tap or drag the progress bar |
| Step lyrics | <kbd>→</kbd> / <kbd>←</kbd>, or tap the lyrics in tap mode |
| Reset to start | Tap anywhere along the top of the screen, or press <kbd>R</kbd> / <kbd>Esc</kbd> |
| Crew settings | Hold the top-right corner of the start screen, or press <kbd>S</kbd> |

Crew settings (title, artist, timings, lyrics) are saved on the device that changed them. Each lyric row is `m:ss Neapolitan line | English translation`; the translation is optional.

## Files

- `index.html` is the whole app. It is written without `<html>`, `<head>` or `<body>` tags so it can also be published as a Claude Artifact.
- `build.py` wraps it into a standalone page.
- `.github/workflows/pages.yml` runs that build and deploys to GitHub Pages on every push to `main`.
- `vercel.json` tells Vercel to run the same build and serve `_site`, so the repo also deploys on Vercel.

To preview the standalone page locally:

```bash
python3 build.py index.html _site/index.html && open _site/index.html
```
