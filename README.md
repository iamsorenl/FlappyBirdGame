# FlappyBirdGame

A simple Flappy Bird clone in Python with pygame.

**Play in browser:** https://iamsorenl.github.io/FlappyBirdGame/

Controls: `SPACE` or click to flap. After a game over, `SPACE` / click restarts.

## Run locally

```bash
pip install pygame
python flappybird.py
```

## How the web build works

The game targets pygame-ce via [pygbag](https://pypi.org/project/pygbag/), which
compiles it to WebAssembly (Pyodide). A GitHub Actions workflow
(`.github/workflows/deploy.yml`) builds the `build/web/` output and deploys it
to GitHub Pages on every push to `main`.
