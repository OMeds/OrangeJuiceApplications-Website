/**
 * Site-wide integration settings (edit before deploy).
 * Empty strings disable optional features and fall back to email / mailto.
 */
window.OJA_SITE_CONFIG = {
  /** Formspree form id for /start-a-project/ (e.g. "abcdwxyz" from formspree.io/f/abcdwxyz) */
  formspreeIntakeId: "",

  /** 30-minute discovery call — Calendly event URL */
  calendlyUrl: "",

  /** Plausible analytics — set domain to enable (cookieless) */
  plausibleDomain: "orangejuiceapplications.com",

  /** App Store product URLs — leave empty until live */
  facematchAppStoreUrl: "",
  ycdaAppStoreUrl: "",

  supportEmail: "support@orangejuiceapplications.com",
  privacyEmail: "privacy@orangejuiceapplications.com",
};
