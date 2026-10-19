// Robot-specific video galleries. Add recordings in data/rollouts.json.
document.addEventListener('DOMContentLoaded', loadRollouts);

async function loadRollouts() {
    const grid = document.getElementById('rollouts-grid');
    const title = document.getElementById('rollouts-title');
    const description = document.getElementById('rollouts-description');
    const pageRobot = document.body.dataset.robot;
    const robot = pageRobot || new URLSearchParams(window.location.search).get('robot');

    try {
        const response = await fetch(siteUrl('data/rollouts.json'));
        if (!response.ok) throw new Error('Could not load rollout videos');
        const systems = await response.json();
        const system = Object.hasOwn(systems, robot) ? systems[robot] : null;
        if (!system) {
            title.textContent = 'Robot system not found';
            description.textContent = 'Use the link above to choose a robot system.';
            grid.replaceChildren();
            return;
        }

        if (!pageRobot) {
            redirectLegacyPage(`rollouts/${encodeURIComponent(robot)}.html`, 'robot');
            return;
        }

        title.textContent = system.title;
        description.textContent = system.description;
        document.title = `${system.title} | Jiyang (Patton) Yin`;
        document.querySelector('meta[name="description"]').content = system.description;

        grid.replaceChildren();
        if (!system.videos.length) {
            grid.innerHTML = '<p class="rollout-empty body-sm">Rollout videos coming soon.</p>';
            return;
        }

        system.videos.forEach(recording => {
            const figure = document.createElement('figure');
            figure.className = 'rollout-video';
            const video = document.createElement('video');
            video.controls = true;
            video.playsInline = true;
            video.preload = 'none';
            video.src = siteUrl(recording.src);
            video.setAttribute('aria-label', recording.title);
            if (recording.poster) video.poster = siteUrl(recording.poster);
            const download = document.createElement('a');
            download.href = siteUrl(recording.src);
            download.textContent = 'Download the rollout video';
            video.append(download);

            const caption = document.createElement('figcaption');
            const heading = document.createElement('h2');
            const titleUrl = recording.project || recording.snapshot;
            if (titleUrl) {
                const link = document.createElement('a');
                link.href = siteUrl(titleUrl);
                link.textContent = recording.title;
                heading.append(link);
            } else {
                heading.textContent = recording.title;
            }
            caption.append(heading);
            if (recording.description) {
                const text = document.createElement('p');
                text.className = 'body-sm';
                text.textContent = recording.description;
                caption.append(text);
            }
            figure.append(video, caption);
            grid.append(figure);
        });
    } catch (error) {
        console.error('Error loading rollouts:', error);
        grid.innerHTML = '<p class="error" role="alert">Unable to load the videos. Please refresh to try again.</p>';
    } finally {
        grid.setAttribute('aria-busy', 'false');
    }
}
