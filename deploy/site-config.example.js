/**
 * Copy values into src/assets/site-config.js before deploy.
 * Do not commit real Formspree IDs to public repos if you prefer env-only secrets —
 * for a static site, the form id is public by design (like a mailto address).
 */
window.OJA_SITE_CONFIG = {
  formspreeIntakeId: "YOUR_FORMSPREE_FORM_ID",
  calendlyUrl: "https://calendly.com/your-account/30min",
  plausibleDomain: "orangejuiceapplications.com",
  facematchAppStoreUrl: "https://apps.apple.com/app/idXXXXXXXXX",
  ycdaAppStoreUrl: "",
  supportEmail: "support@orangejuiceapplications.com",
  privacyEmail: "privacy@orangejuiceapplications.com",
};
