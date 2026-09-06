'use strict';
// Progressive enhancement only: content and primary links do not depend on JS.
(() => {
  const header = document.querySelector('.site-header');
  const toggle = header?.querySelector('.nav-toggle');
  const navigation = header?.querySelector('.navigation');
  if (header && toggle && navigation) {
    const closeNavigation = (returnFocus = false) => {
      header.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open navigation');
      if (returnFocus) toggle.focus();
    };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      header.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    });
    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeNavigation();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && header.classList.contains('nav-open')) closeNavigation(true);
    });
    document.addEventListener('click', (event) => {
      if (!header.contains(event.target)) closeNavigation();
    });
    const desktop = matchMedia('(min-width: 768px)');
    desktop.addEventListener('change', () => closeNavigation());
    header.classList.add('enhanced');
    toggle.hidden = false;
  }

  const dialog = document.querySelector('#photo-dialog');
  if (dialog && typeof dialog.showModal === 'function') {
    let returnFocus;
    const closeButton = dialog.querySelector('.dialog-close');
    document.querySelectorAll('[data-lightbox]').forEach((link) => {
      link.addEventListener('click', (event) => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
        event.preventDefault();
        const image = dialog.querySelector('img');
        image.src = link.href;
        image.alt = link.querySelector('img')?.alt || link.dataset.caption || '';
        dialog.querySelector('#photo-caption').textContent = link.dataset.caption || '';
        returnFocus = link;
        dialog.showModal();
        document.body.classList.add('dialog-open');
        closeButton.focus();
      });
    });
    closeButton.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('dialog-open');
      returnFocus?.focus();
    });
  }

  const tools = document.querySelector('.menu-tools');
  const search = document.querySelector('#menu-search');
  const items = [...document.querySelectorAll('.menu-item')];
  if (tools && search && items.length) {
    const filters = [...tools.querySelectorAll('[data-filter]')];
    const status = document.querySelector('.menu-result-count');
    const empty = document.querySelector('.menu-empty');
    const valid = new Set(filters.map((button) => button.dataset.filter));
    let selected = valid.has(location.hash.slice(1)) ? location.hash.slice(1) : 'all';
    const update = () => {
      const term = search.value.trim().toLocaleLowerCase('en');
      let count = 0;
      items.forEach((item) => {
        const matches = (selected === 'all' || item.dataset.category === selected) && item.dataset.search.includes(term);
        item.hidden = !matches;
        if (matches) count += 1;
      });
      filters.forEach((button) => {
        const active = button.dataset.filter === selected;
        button.classList.toggle('active', active);
        button.setAttribute('aria-pressed', String(active));
      });
      status.textContent = `${count} ${count === 1 ? 'highlight' : 'highlights'}${term ? ' matching your search' : ''}`;
      empty.hidden = count !== 0;
    };
    filters.forEach((button) => button.addEventListener('click', () => {
      selected = button.dataset.filter;
      update();
    }));
    search.addEventListener('input', update);
    document.querySelector('#reset-menu')?.addEventListener('click', () => {
      selected = 'all'; search.value = ''; update(); search.focus();
    });
    window.addEventListener('hashchange', () => {
      const category = location.hash.slice(1);
      if (valid.has(category)) { selected = category; search.value = ''; update(); }
    });
    tools.hidden = false; status.hidden = false; update();
  }

  const copy = document.querySelector('.copy-address');
  if (copy && navigator.clipboard?.writeText && window.isSecureContext) {
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      const status = document.querySelector('.copy-status');
      const address = document.querySelector('address').innerText.replace(/\s+/g, ' ').trim();
      try {
        await navigator.clipboard.writeText(address);
        status.textContent = 'Address copied. See you at Soy Yum.';
      } catch {
        status.textContent = 'Clipboard unavailable. You can select and copy the address above.';
      }
    });
  }
  // No tracker/network call. Events are only available for a future reviewed integration.
  document.querySelectorAll('[data-action]').forEach((link) => link.addEventListener('click', () => {
    document.dispatchEvent(new CustomEvent('soy:action', {detail: {
      action: link.dataset.action, placement: link.dataset.placement || 'page', path: location.pathname
    }}));
  }));
})();
