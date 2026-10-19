<!-- Add short notes alongside the media here. The title and summary live in portfolio/projects.json. -->

## Motivation


During data collections, I found the handheld [UMI gripper](https://umi-gripper.github.io/) too heavy to hold comfortably for dexterous manipulation. Because of our camera limitations, our tracking setup also required a large ArUco tag. It occupied too much of the egocentric view, creating a large visual gap between human demonstrations and robot observations.

<div class="portfolio-media-pair">
  <figure>
    <svg class="umi-example-frame" viewBox="27 46 837 467" width="837" height="467" role="img" aria-label="Ego RGB view of the earlier handheld UMI setup, with a large ArUco tag occupying much of the view">
      <image href="assets/portfolio/hand-umi-earlier-umi-example.png" width="1966" height="571"></image>
    </svg>
    <figcaption>Earlier UMI setup: ego RGB view with gaze rendered.</figcaption>
  </figure>
  <figure>
    <svg class="umi-example-frame" viewBox="1239 92 671 375" width="671" height="375" role="img" aria-label="Exo tracking view of the earlier handheld UMI setup with detected ArUco tags">
      <image href="assets/portfolio/hand-umi-earlier-umi-example.png" width="1966" height="571"></image>
    </svg>
    <figcaption>Earlier UMI setup: exo tracking view.</figcaption>
  </figure>
</div>

HandUMI is much smaller and uses Quest for pose tracking as part of its design. Seeing Quest used in many teleoperation setups gave me confidence in its tracking quality and helped motivate my choice of HandUMI.

So I adapted [HandUMI](https://github.com/murobotics-ai/handumi-hw) for egocentric manipulation data collection in our lab, with a matching gripper setup on the KUKA.

## Gripper on KUKA

I made extensive changes to the HandUMI design to fit our setup and mount it on the KUKA. Our earlier gripper is built based on [aloha4franka](https://github.com/TUM-LSY/aloha4franka), I adapted the design to match the gripper’s appearance and camera setup between data collection and robot deployment.

<div class="portfolio-media-pair">
  <figure>
    <img src="assets/portfolio/hand-umi-kuka-construction.jpg" alt="HandUMI gripper mount under construction on the KUKA wrist" loading="lazy" style="width: 100%; aspect-ratio: 16 / 9; object-fit: cover; object-position: center 55%;">
    <figcaption>The gripper mount during construction.</figcaption>
  </figure>
  <figure>
    <img src="assets/portfolio/hand-umi-kuka-replay.jpg" alt="Completed HandUMI grippers and cameras mounted on the KUKA arms, captured at 9 seconds in the trajectory replay" width="1280" height="720" loading="lazy">
    <figcaption>The completed grippers and cameras mounted on the KUKA arms.</figcaption>
  </figure>
</div>

## Data collection in the lab

The video shows the collection setup: handheld grippers, .

<figure>
  <video controls playsinline preload="none" poster="assets/portfolio/hand-umi-data-collection.jpg" aria-label="HandUMI demonstration collection at the lab workbench">
    <source src="assets/portfolio/hand-umi-data-collection.mp4" type="video/mp4">
    <a href="assets/portfolio/hand-umi-data-collection.mp4">Download the data-collection video</a>.
  </video>
  <figcaption>A short recording of the HandUMI data-collection setup in use.</figcaption>
</figure>

## A closer look at the recording

<figure>
  <video controls playsinline preload="none" poster="assets/portfolio/hand-umi.jpg" aria-label="HandUMI data recording played back in the Rerun viewer">
    <source src="assets/portfolio/hand-umi.mp4" type="video/mp4">
    <a href="assets/portfolio/hand-umi.mp4">Download the HandUMI demo</a>.
  </video>
  <figcaption>The table below matches the recording’s panel layout.</figcaption>
</figure>

<!-- Replace the bracketed names below. The two rows refer to the eight main views, excluding Rerun's sidebars. -->

<table class="recording-panel-map" aria-label="Recording panel layout">
  <tbody>
    <tr>
      <td>RealSense depth</td>
      <td>RGB with human gaze</td>
      <td>RealSense left IR</td>
      <td>RealSense right IR</td>
    </tr>
    <tr>
      <td>Left wrist cam rgb</td>
      <td>Right wrist cam rgb</td>
      <td>Gripper openess</td>
      <td>3D trajectory</td>
    </tr>
  </tbody>
</table>
