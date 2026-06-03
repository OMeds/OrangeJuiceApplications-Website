Orange Juice Applications — FTP upload (Fasthosts)
==================================================

1. Log in to Fasthosts → Web Hosting → File Manager (or FTP).

2. Open htdocs (your web root — NOT the website-deploy folder).

3. Upload EVERYTHING inside dist/ (after ./scripts/build.sh) into htdocs:
   - index.html (OJA project hub — FaceMatch + YCDA)
   - facematch/index.html (FaceMatch marketing site)
   - ycda/index.html (YCDA gateway — links to Vercel app)
   - 403.html, 404.html, 500.html, sitemap.xml, robots.txt, .htaccess
   - assets/ (style.css, site.js, ycda-launch.js, logos, icons, …)
   - contact-profile-picture-sync/ (privacy, terms, support, faq, security, guides)
   - facematch/oauth/ (hidden LinkedIn, Facebook & Instagram OAuth bridges)

4. Do NOT upload src/ to the server — edit src/, run scripts/build.sh, upload dist/ only.

5. Enable HTTPS / SSL for orangejuiceapplications.com.

6. Before upload — set your YCDA testing URL:
   Edit src/ycda/index.html (or ycda/index.html after build):
   - meta name="oja-ycda-app-url" content="https://YOUR-YCDA.vercel.app"
   - href on #ycda-open button (same URL)
   Then rebuild: ./scripts/build.sh
   See deploy/DEPLOY.md for FileZilla connection.

7. Test URLs:
   - https://www.orangejuiceapplications.com/ (project hub)
   - https://www.orangejuiceapplications.com/facematch/
   - https://www.orangejuiceapplications.com/ycda/ (opens Vercel YCDA app)
   - https://www.orangejuiceapplications.com/contact-profile-picture-sync/guides
   - https://www.orangejuiceapplications.com/does-not-exist (custom 404)
   - OAuth bridges under /facematch/oauth/…

8. YCDA Next.js app: deploy separately to Vercel (see you-can-dance-academy/website/DEPLOY.md).
   The static /ycda/ page on this host is a gateway for testing — not the full portal.

Rebuild locally after changes:
  ./scripts/build.sh
