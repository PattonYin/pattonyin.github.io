<!-- Add short notes alongside the media here. The title and summary live in portfolio/projects.json. -->

We replicated [KIWI](https://lingfeng.moe/KIWI/)’s design for this Generalist-style UMI setup and adapted it for our lab. [Souju](https://qsoujanya.com/) helped adapt the 3D design to make the setup work in our lab.

These clips show the gripper-camera views and the tracking visualization I use to inspect their motion.

## Motivation

Although our earlier [HandUMI setup](portfolio/hand-umi.html) worked reasonably well, its heavy equipment and lengthy calibration motivated this switch. A better collection experience and greater efficiency matters to scaling data collection!

## Tracking in a shared workspace

I use this view to inspect the pose tracking errors from the SLAM pipeline, with an external static ChArUco board as the ground truth reference. 

<figure>
  <video controls playsinline preload="none" poster="assets/portfolio/generalist-style-umi.jpg" aria-label="ArUco tracking visualization with wrist cameras and pose diagnostics">
    <source src="assets/portfolio/aruco-tracking.mp4" type="video/mp4">
    <a href="assets/portfolio/aruco-tracking.mp4">Download the tracking video</a>.
  </video>
  <figcaption>Wrist-camera observations, reconstructed motion, and tracking diagnostics shown together.</figcaption>
</figure>

## Through the gripper cameras

Two recordings from the gripper-mounted cameras, showing the fingers and nearby objects during collection.

<div class="portfolio-media-pair">
  <figure>
    <video controls playsinline preload="none" poster="assets/portfolio/gripper-view-01.jpg" aria-label="First egocentric recording from a handheld gripper">
      <source src="assets/portfolio/gripper-view-01.mp4" type="video/mp4">
      <a href="assets/portfolio/gripper-view-01.mp4">Download the first gripper recording</a>.
    </video>
    <figcaption>Screw & Nuts Picking Video</figcaption>
  </figure>
  <figure>
    <video controls playsinline preload="none" poster="assets/portfolio/gripper-view-02.jpg" aria-label="Second egocentric recording from a handheld gripper">
      <source src="assets/portfolio/gripper-view-02.mp4" type="video/mp4">
      <a href="assets/portfolio/gripper-view-02.mp4">Download the second gripper recording</a>.
    </video>
    <figcaption>Earbuds Clean Up Video</figcaption>
  </figure>
</div>

## Gripper on KUKA

<figure>
  <img src="assets/portfolio/umi-on-kuka.jpg" alt="Generalist-style UMI gripper and camera mounted on a KUKA robot arm" width="480" height="640" loading="lazy">
</figure>

## In the Wild UMI Cube Picking

After we have the UMI setup, with [Mingxi](https://mingxi-jia.github.io/), we collected UMI demonstrations against diverse backgrounds around the lab. The video below shows model's live predictions at varying poses.

<figure>
  <video controls playsinline preload="none" poster="assets/portfolio/umi-in-the-wild-cube.jpg" aria-label="UMI cube-picking inference after collecting demonstrations against diverse backgrounds around the lab">
    <source src="assets/portfolio/umi-in-the-wild-cube-clip.webm" type="video/webm">
    <a href="assets/portfolio/umi-in-the-wild-cube-clip.webm">Download the cube-picking inference video</a>.
  </video>
  <figcaption>Cube-picking inference with the Generalist-style UMI setup.</figcaption>
</figure>
