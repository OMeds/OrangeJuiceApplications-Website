"""Shared error page content for the marketing site."""
from __future__ import annotations

ERROR_PAGES: dict[str, dict[str, str]] = {
    "403": {
        "title": "Access denied",
        "code": "403",
        "lead": "You don’t have permission to view this page, or the file isn’t published here.",
        "detail": "If you manage this site, check that files are uploaded to your web root (htdocs) and that folder permissions are correct.",
        "primary_label": "Back to home",
        "primary_href": "/",
        "secondary_label": "Contact support",
        "secondary_href": "mailto:support@orangejuiceapplications.com",
    },
    "404": {
        "title": "Page not found",
        "code": "404",
        "lead": "That link doesn’t exist or may have moved.",
        "detail": "Try the homepage, user guides, or support page below.",
        "primary_label": "Back to home",
        "primary_href": "/",
        "secondary_label": "User guides",
        "secondary_href": "/contact-profile-picture-sync/guides/",
    },
    "500": {
        "title": "Something went wrong",
        "code": "500",
        "lead": "The server had trouble loading this page.",
        "detail": "Please try again in a few minutes. If the problem continues, email support with the time it happened.",
        "primary_label": "Back to home",
        "primary_href": "/",
        "secondary_label": "Email support",
        "secondary_href": "mailto:support@orangejuiceapplications.com",
    },
}

ERROR_HELP_LINKS = """
<ul class="error-help-links">
  <li><a href="/contact-profile-picture-sync/guides/">User guides</a></li>
  <li><a href="/contact-profile-picture-sync/guides/troubleshooting/">Troubleshooting</a></li>
  <li><a href="/contact-profile-picture-sync/support/">Support</a></li>
  <li><a href="/contact-profile-picture-sync/faq/">FAQ</a></li>
</ul>
"""
