# V3 — Premium Animated Profile

V3 replaces the previous “giant cyberpunk poster” layout with a tighter hierarchy:

1. One cinematic animated hero.
2. One slim animated signal strip.
3. One architecture animation.
4. Real Markdown sections for projects and engineering focus.
5. GitHub's own contribution/profile UI remains visible lower on the page.

## Install over your current profile repo

From the existing repository folder:

```bash
rm -rf assets
cp -R ../VineetBhatt_GitHub_Command_Center_V3/assets .
rm -rf .github
cp -R ../VineetBhatt_GitHub_Command_Center_V3/.github .
cp ../VineetBhatt_GitHub_Command_Center_V3/README.md .
git add -A
git commit -m "feat: redesign profile with premium animated system"
git push
```
