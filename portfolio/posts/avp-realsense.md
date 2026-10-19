<!-- Add short notes alongside the media here. The title and summary live in portfolio/projects.json. -->

I paired Apple Vision Pro (AVP) with a head-mounted RealSense (RS) camera for gaze experiments and point-cloud reconstruction. Below are the mounting setup and a reconstruction preview.

## Head-mounted RealSense for gaze

I mounted a RealSense camera on the front of the AVP headset for my gaze experiments.

[Ivy](https://ivyyyy24381.github.io/) helped with the mounting design!

<figure>
  <img src="assets/portfolio/avp-realsense-head-mount.jpg" alt="Apple Vision Pro worn with a RealSense camera mounted in front and an orange bracket around the headset" width="480" height="640" loading="lazy">
  <figcaption>The AVP and head-mounted RealSense setup I used for gaze experiments.</figcaption>
</figure>

## Use AVP poses and mounted RealSense for 3D reconstruction 

After calibrating the AVP–RealSense setup, I remapped movement data from AVP into the RealSense camera frame. This puts the motion and camera observations into a common frame for reconstructing the scene. 

<figure>
  <video controls playsinline preload="none" poster="assets/gallery/pointcloud-recon.jpg" aria-label="Point-cloud reconstruction after remapping calibrated AVP movement data to RealSense">
    <source src="assets/gallery/pointcloud-recon.mp4" type="video/mp4">
    <a href="assets/gallery/pointcloud-recon.mp4">Download the reconstruction video</a>.
  </video>
  <figcaption>Point-cloud reconstruction using AVP movement data remapped to RealSense after calibration.</figcaption>
</figure>

