// Shared, sitewide status and policy notice. Keep links root-relative for Vercel clean URLs.
(() => {
  const mount = () => {
    if (document.querySelector('[data-site-governance-notice]')) return;

    const notice = document.createElement('aside');
    notice.setAttribute('data-site-governance-notice', '');
    notice.setAttribute('aria-label', 'Site status and policies');
    notice.innerHTML = `
      <div style="max-width:1120px;margin:0 auto;padding:1rem 1.25rem;font:500 .78rem/1.55 system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#3a3a3a">
        <strong>Independent student resource.</strong>
        This site is maintained by a student leader for community convenience and is not an official statement of Northeastern University or its School of Law.
        Verify time-sensitive requirements and opportunities with the original source.
        <a href="/institutional-disclaimer" style="margin-left:.35rem">Status &amp; reliance notice</a>
        <span aria-hidden="true"> · </span>
        <a href="/privacy">Privacy</a>
        <span aria-hidden="true"> · </span>
        <a href="https://github.com/rn-collins/flexjd-site/blob/main/docs/source-verification-policy.md">Source policy</a>
      </div>`;
    notice.style.cssText = 'border-top:1px solid #d8d8d8;background:#f7f7f5;';

    const footer = document.querySelector('footer');
    if (footer) footer.before(notice);
    else document.body.appendChild(notice);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
