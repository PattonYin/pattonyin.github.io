# Jiyang (Patton) Yin — personal website

A static research portfolio built with HTML, CSS, and JavaScript.

## Preview

Run `python serve.py` and open <http://127.0.0.1:8000>. No build step or package
installation is required. Use an HTTP server rather than opening `index.html`
directly, because publications load from JSON.
The preview server supports video seeking; restart it after updating `serve.py`.

## Edit

- `index.html`: biography, navigation, and profile links.
- `css/style.css`: responsive layout and light/dark themes.
- `data/content.json`: publications; retained gallery entries are not displayed.
- `assets/publications/`: publication teaser images.
- `js/robots.js`, `data/trajectories.json`: interactive robot viewers and motion tracks.
- `assets/robots/`: compact robot meshes, kinematics, and model licenses.
- `assets/gallery/`: retained compressed media, including the reconstruction clip used in the AVP + RealSense project.
- `portfolio.html`: Robotics Snapshots gallery and source layout for individual entries.
- `portfolio/*.html`, `rollouts/*.html`: generated pages with distinct paths for analytics.
- `portfolio/projects.json`: note titles, dates, descriptions, tags, and cover images.
- `portfolio/posts/`: short editable Markdown descriptions alongside images and videos.
- `assets/portfolio/`: compressed portfolio videos and cover images.
- `js/analytics.js`: shared Cloudflare Web Analytics token and loader.

Keep raw recordings outside the repository. The old `Gallary/` source folder,
MOV files, WebM captures, `data/portfolio/`, and `data/rollouts/` are ignored; use small MP4 exports
in `assets/portfolio/` for the site. The compressed `umi-in-the-wild-cube-clip.webm`
is also included for the cube-picking inference demo. Aim for less than 5 MB per clip.

Deploy the repository root on any static host, including GitHub Pages.

## Visitor statistics

Cloudflare Web Analytics uses the public beacon token in `js/analytics.js` for
`pattonyin.github.io`. Deploy the updated files to begin collecting visits and
page views, then open **Cloudflare > Web Analytics**. Filter by **Path** to compare
snapshots and robot galleries. Visits are not unique people; new vs returning
visitors are not measured. Homepage section anchors count as the same page.

The shared script loads one beacon per page, skips localhost previews, and
skips old query-string pages that redirect to their new URLs. Use manual JS
snippet installation in Cloudflare without also enabling automatic injection.
To disable tracking, set the token to an empty string.

Snapshot and rollout URLs are real static HTML files, so direct links and reloads
work on GitHub Pages without server rewrites. Old `portfolio.html?project=...`
and `rollouts.html?robot=...` links redirect, preserving section anchors and
other query parameters.

After changing `portfolio.html`, `rollouts.html`, or project/robot names, titles,
or descriptions in the JSON lists, regenerate the pages and include them in deployment:

```sh
python tools/generate_pages.py
python tools/generate_pages.py --check
```

Markdown notes and video lists load directly; editing those does not require
regeneration. Commit generated pages with the site so hosting needs no build
service or additional packages.

See [Cloudflare setup](https://developers.cloudflare.com/web-analytics/get-started/)
and [available metrics](https://developers.cloudflare.com/web-analytics/data-metrics/high-level-metrics/).

## Robotics Snapshots

Media tiles appear directly below Publications on the homepage. Open
<http://127.0.0.1:8000/portfolio.html> for the dedicated gallery. Each tile opens
a shareable entry, for example `portfolio/hand-umi.html`.
The homepage shows the two latest entries. "View all snapshots" opens the full
gallery. Entries sort by date, newest first; matching dates keep JSON array order.

Each note groups related photos and videos with a short description of what
I’ve been working on. Edit its file in `portfolio/posts/`, using Markdown for
text and images and HTML for videos. Keep the context brief and add captions
where useful. Editing is done in these files, not in the browser.

Each entry's `date` is shown on its tile and note page. Edit it in
`portfolio/projects.json` using `YYYY-MM-DD` (for example, `2026-08-01`). The four
newer entries use `2026-10-17` as a placeholder date; replace these with the
actual dates to update the gallery order.
Live Hand Detection Preview uses `2026-03-01` as a placeholder for its date in March.

To add a note:

1. Add a record to `portfolio/projects.json` with a unique `slug`, `title`, `date`,
   `description`, and a `tags` array. Add `cover` and `coverAlt` when a teaser image
   is ready; otherwise the tile shows "Preview coming soon".
2. Create `portfolio/posts/your-slug.md`. The page supplies the title, so start
   the file with a paragraph and use `##` for section headings.
3. Put web-ready media in `assets/portfolio/` and reference it from the note.
   Media paths are relative to the site root page, **not** the Markdown file.
4. Run `python tools/generate_pages.py` to create the entry's static page.

```markdown
## A closer look

Describe what you’ve been working on and what the media shows.

![Describe the image](assets/portfolio/your-image.jpg)

<video controls playsinline preload="none" poster="assets/portfolio/your-image.jpg" aria-label="Describe the demo">
  <source src="assets/portfolio/your-demo.mp4" type="video/mp4">
  <a href="assets/portfolio/your-demo.mp4">Download the demo</a>.
</video>
```

Use locally authored, trusted Markdown: HTML is supported so media embeds work.
Videos load only when played; the gallery uses still images. MP4/H.264 exports
work across modern browsers. The original recordings in `data/portfolio/` are
kept locally and are not required to deploy the site.

## Publication images

To add a teaser, save the image in `assets/publications/` and add these fields
to its publication entry in `data/content.json`:

```json
"image": "assets/publications/your-paper.jpg",
"imageAlt": "A short description of the figure."
```

Leave `image` out for a text-only entry. Images appear beside the publication
on desktop and above it on mobile; figures are shown without cropping.

## Robot rollout videos

Each robot system has a "View rollout videos" button linking to its gallery:
`rollouts/kuka.html` or `rollouts/franka.html`. The Franka gallery includes
two Nutella picking videos, the intervention timing rollout, and a coffee-making video. Galleries without
videos show "Rollout videos coming soon".

To add videos, put web-ready MP4 files and optional poster images in
`assets/rollouts/`, then add records to the matching `videos` array in
`data/rollouts.json`. Paths are relative to the website root. For example:

```json
{
  "title": "Your rollout title",
  "src": "assets/rollouts/your-rollout.mp4",
  "poster": "assets/rollouts/your-rollout.jpg",
  "description": "Describe the task and what the policy is doing."
}
```

`title` and `src` are required; `poster` and `description` are optional.
For a video featured in a snapshot, add `snapshot` with its site-relative URL
(and optional section anchor) to make the video title link to that snapshot.
Existing videos in `assets/portfolio/` can be reused directly, including WebM clips.
Videos use native playback controls and load only when played.

## Robot models

The Franka uses a Robotiq 2F-85. Both KUKA arms use the supplied KIWI gripper
and camera assembly; the left arm is orange and gray, and the right is white. Only compact
GLBs are needed to serve the site. See [model attribution and regeneration](assets/robots/ATTRIBUTION.md)
for sources and conversion commands.
