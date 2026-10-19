// Portfolio entries and locally authored Markdown; main.js provides escapeHtml.
document.addEventListener('DOMContentLoaded', loadPortfolio);

async function loadPortfolio() {
    const content = document.getElementById('portfolio-content');
    const grid = document.getElementById('portfolio-grid');
    const container = content || grid;
    const pageSlug = document.body.dataset.project;
    const slug = content ? pageSlug || new URLSearchParams(window.location.search).get('project') : null;
    const backLink = document.getElementById('portfolio-back');
    if (backLink) backLink.hidden = !slug;

    try {
        const response = await fetch(siteUrl('portfolio/projects.json'));
        if (!response.ok) throw new Error('Could not load portfolio entries');
        const projects = await response.json();

        if (grid) {
            renderPortfolioTiles(projects, grid);
            return;
        }

        if (slug) {
            const project = projects.find(entry => entry.slug === slug);
            if (!project) {
                document.title = 'Snapshot not found | Jiyang (Patton) Yin';
                content.innerHTML = '<h1 class="page-title">Snapshot not found</h1><p class="page-subtitle">This entry is not in the collection. Use the link above to browse the available snapshots.</p>';
                return;
            }
            if (!pageSlug) {
                redirectLegacyPage(`portfolio/${encodeURIComponent(project.slug)}.html`, 'project');
                return;
            }
            await renderPortfolioPost(project, content);
        } else {
            renderPortfolioGallery(projects, content);
        }
    } catch (error) {
        console.error('Error loading portfolio:', error);
        container.innerHTML = '<p class="error" role="alert">Unable to load the snapshots. Please refresh to try again.</p>';
    } finally {
        container.setAttribute('aria-busy', 'false');
    }
}

function renderPortfolioGallery(projects, content) {
    content.innerHTML = `
        <header class="page-header">
            <h1 class="page-title">Robotics Snapshots</h1>
            <p class="page-subtitle">Photos, videos, and short notes from my robotics work.</p>
        </header>
        <div class="portfolio-grid"></div>
    `;
    renderPortfolioTiles(projects, content.querySelector('.portfolio-grid'));
}

function renderPortfolioTiles(projects, grid) {
    grid.innerHTML = '';
    const heading = grid.id === 'portfolio-grid' ? 'h3' : 'h2';
    if (!projects.length) {
        grid.innerHTML = '<p class="body-sm">Snapshots are coming soon.</p>';
        return;
    }

    const sortedProjects = [...projects].sort((a, b) => (b.date || '').localeCompare(a.date || ''));
    const visibleProjects = grid.id === 'portfolio-grid' ? sortedProjects.slice(0, 2) : sortedProjects;

    visibleProjects.forEach(project => {
        const card = document.createElement('a');
        card.className = 'portfolio-tile';
        card.href = siteUrl(`portfolio/${encodeURIComponent(project.slug)}.html`);

        const cover = document.createElement(project.cover ? 'img' : 'div');
        cover.className = 'portfolio-cover';
        if (project.cover) {
            cover.src = siteUrl(project.cover);
            cover.alt = project.coverAlt;
            cover.width = 960;
            cover.height = 540;
            cover.loading = 'lazy';
        } else {
            cover.classList.add('portfolio-cover-placeholder');
            cover.textContent = 'Preview coming soon';
        }
        card.append(cover);

        const details = document.createElement('div');
        details.className = 'portfolio-tile-body';
        details.innerHTML = `
            <div class="tag-list">${project.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}</div>
            <${heading} class="portfolio-tile-title">${escapeHtml(project.title)}</${heading}>
            ${renderPortfolioDate(project.date)}
            <p class="card-desc">${escapeHtml(project.description)}</p>
            <span class="portfolio-read">View snapshot <span aria-hidden="true">&rarr;</span></span>
        `;
        card.append(details);
        grid.append(card);
    });
}

async function renderPortfolioPost(project, content) {
    const response = await fetch(siteUrl(`portfolio/posts/${encodeURIComponent(project.slug)}.md`));
    if (!response.ok) throw new Error('Could not load project notes');
    const markdown = await response.text();

    // Notes use site-root-relative media paths. Resolve them before attaching the HTML.
    const prose = document.createElement('template');
    prose.innerHTML = marked.parse(markdown, { gfm: true });
    prose.content.querySelectorAll('[src], [poster], [href]').forEach(element => {
        for (const attribute of ['src', 'poster', 'href']) {
            const value = element.getAttribute(attribute);
            if (value && !/^(#|\/|[a-z][a-z\d+.-]*:)/i.test(value)) {
                element.setAttribute(attribute, siteUrl(value));
            }
        }
    });

    document.title = `${project.title} | Jiyang (Patton) Yin`;
    document.querySelector('meta[name="description"]').content = project.description;
    content.innerHTML = `
        <article class="portfolio-post">
            <header class="page-header">
                <div class="tag-list">${project.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}</div>
                <h1 class="page-title">${escapeHtml(project.title)}</h1>
                ${renderPortfolioDate(project.date)}
                <p class="page-subtitle">${escapeHtml(project.description)}</p>
            </header>
            <div class="prose">${prose.innerHTML}</div>
            <a class="back-link portfolio-bottom-link" href="${escapeHtml(siteUrl('portfolio.html'))}">&larr; All snapshots</a>
        </article>
    `;

    await renderPortfolioOutline(content);
}

async function renderPortfolioOutline(content) {
    const outline = document.getElementById('portfolio-outline');
    const headings = Array.from(content.querySelectorAll('.prose h2'));
    const list = outline.querySelector('ul');
    list.replaceChildren();
    outline.hidden = !headings.length;
    if (!headings.length) return;

    headings.forEach(heading => {
        const label = heading.textContent.trim();
        if (!heading.id) {
            const slug = label.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '') || 'section';
            let id = slug;
            let suffix = 2;
            while (document.getElementById(id)) id = `${slug}-${suffix++}`;
            heading.id = id;
        }
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#${encodeURIComponent(heading.id)}`;
        link.textContent = label;
        item.append(link);
        list.append(item);
    });

    const links = Array.from(list.querySelectorAll('a'));
    const updateActive = () => {
        const offset = parseFloat(getComputedStyle(headings[0]).scrollMarginTop) || 0;
        let active = headings[0];
        headings.forEach(heading => {
            if (heading.getBoundingClientRect().top <= offset + 1) active = heading;
        });
        // Short final sections cannot always reach the top of the viewport.
        if (window.scrollY > 0 && window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 1) {
            const target = headings.find(heading => `#${encodeURIComponent(heading.id)}` === window.location.hash);
            active = target && target.getBoundingClientRect().top >= offset - 1
                ? target : headings[headings.length - 1];
        }
        links.forEach((link, index) => {
            if (headings[index] === active) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
        });
    };
    window.addEventListener('scroll', updateActive, { passive: true });
    window.addEventListener('resize', updateActive);
    window.addEventListener('hashchange', updateActive);
    new ResizeObserver(updateActive).observe(content);
    updateActive();

    // Wait for media above the target so late-loading posters do not shift a direct link.
    const hash = window.location.hash;
    const target = headings.find(heading => `#${encodeURIComponent(heading.id)}` === hash);
    if (target) {
        const media = Array.from(content.querySelectorAll('img, video[poster]'))
            .filter(element => element.compareDocumentPosition(target) & Node.DOCUMENT_POSITION_FOLLOWING);
        await Promise.all(media.map(element => {
            const image = new Image();
            image.src = element.poster || element.src;
            return image.decode().catch(() => {});
        }));
        if (window.location.hash === hash) target.scrollIntoView({ behavior: 'instant' });
        updateActive();
    }
}

function renderPortfolioDate(date) {
    if (!date) return '';
    const parsed = new Date(`${date}T00:00:00Z`);
    const label = parsed.toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', timeZone: 'UTC'
    });
    return `<time class="portfolio-date" datetime="${parsed.toISOString().slice(0, 10)}">${label}</time>`;
}
