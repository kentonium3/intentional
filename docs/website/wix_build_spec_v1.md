---
id: wix-build-spec-v1
doc_type: implementation
owner: kent
status: draft
last_updated: 2025-11-06
tags: [website, wix, intentional, brand]
title: Wix Build Specification (v1)
---

# Wix Build Specification (v1)

## Purpose
Define the **layout, page structure, and design system mapping** for Intentional's website hosted on **Wix**.
This document connects approved brand identity elements and voice/tone guidelines to their on-site presentation, ensuring every page communicates the same sense of *clarity, trust, and expertise*.

---

## 1. Design System References

| Source | Reference File | Usage |
|---------|----------------|-------|
| Brand Identity | `docs/brand/brand-identity-brief.md` | Defines look, tone, formality, color energy |
| Branding Kit | `docs/brand/branding-kit-spec-v1.md` | Color, typography, grid, spacing rules |
| Voice & Tone | `docs/brand/brand-voice-and-tone.md` | Copywriting and microcopy guidelines |
| Values & Principles | `docs/brand/intentional-values-and-principles.md` | Behavioral anchors for message framing |

---

## 2. Overall Site Goals

1. **Establish credibility immediately** for PE/VC referrals and SaaS executives.
2. **Signal depth and discipline** in Support Operations expertise.
3. **Enable referrals to share the site confidently** ("See — he gets it").
4. **Allow future expansion** (Intentional Index online, thought leadership library).
5. **Demonstrate modern, frictionless user experience** — consistent with Intentional's consulting philosophy.

---

## 3. Site Map & Navigation Structure

| Page | Purpose | Key Sections | Notes |
|------|----------|---------------|-------|
| **Home** | Introduce Intentional's value proposition. | Hero, Proof Points, Approach, CTA | Must deliver "he gets it" message within first 5 seconds. |
| **About** | Founder story + credibility. | Founder Note, Experience Highlights, Values, CTA | Mirrors tone from `Intentional_About.md`. |
| **Services** | Define consulting offerings. | Overview, Intentional Index, Engagement Model, Outcomes | Emphasize measurable value. |
| **Insights** | Thought leadership articles. | Featured posts, categories, subscribe link | Placeholder for 2026 content cadence. |
| **Contact** | Lead capture & trust touchpoint. | Consultation form, Calendly, email, location | Low friction; form → HubSpot. |

**Top Navigation Order:** Home | About | Services | Insights | Contact
**Footer Navigation:** Privacy | Terms | LinkedIn | Email | Copyright

---

## 4. Layout Framework

**Grid:** 12-column responsive grid with 1280px max width.
**Section Height:** 70–90vh for hero; 60–80vh for standard sections.
**Whitespace:** 20–30% of vertical screen real estate per page.
**Padding:** 80px desktop / 40px mobile.
**Animation:** Minimal fade or slide-in, none on text-heavy blocks.

---

## 5. Page-by-Page Layout Mapping

### **Home Page**

**Purpose:**
Communicate expertise, credibility, and Intentional's core premise: Support as a strategic growth lever.

| Section | Content / Layout | Visual Mapping |
|----------|------------------|----------------|
| **Hero** | Headline: "Elevating Support into a Strategic Growth Engine"<br>Subhead: "Helping SaaS companies align customer, product, and service intentions to build enduring customer connections."<br>CTA: "See how Intentional measures what really matters." | Full-width; Intentional Blue CTA; Deep Slate background; Inter Bold type; subtle geometric overlay. |
| **Proof Points** | "30+ Years Leading Global SaaS Support," "The Intentional Index™," "Cross-functional alignment expertise." | Three horizontal blocks; minimal icons; light background. |
| **Approach Preview** | Visual of Intentional Index model; short text on "alignment of intentions." | Two-column layout: left image (Index diagram), right copy. |
| **Values / Trust Bar** | Logos or text placeholders (e.g., Acquia, global experience). | Light gray band; Inter Medium text; subdued tone. |
| **CTA Section** | "Start your alignment conversation." Button → Contact page. | Centered on soft gray background. |

---

### **About Page**

**Purpose:**
Tell the founder story and connect credibility to empathy and purpose.

| Section | Content / Layout | Visual Mapping |
|----------|------------------|----------------|
| **Intro Statement** | Pull quote from `Intentional_About.md` ("Support is a strategic driver of retention and growth."). | Serif accent; slate background. |
| **Founder Story** | Narrative from About doc; image of Kent (authentic, minimal). | Two-column: portrait left, copy right. |
| **Experience Summary** | Pull highlights from resume ("Built global orgs, led through acquisitions…"). | Grid layout with icons; Inter Medium. |
| **Values & Principles Section** | Summarized bullets: Integrity, Empathy, Clarity, Excellence. | Light background; subtle horizontal divider. |
| **CTA** | "Discuss your Support alignment challenges." → Contact. | Full-width Intentional Blue band. |

---

### **Services Page**

**Purpose:**
Define Intentional's differentiators and proprietary methodology.

| Section | Content / Layout | Visual Mapping |
|----------|------------------|----------------|
| **Intro** | Headline: "Consulting Services for Customer-Driven Growth." | White background, blue text highlights. |
| **Service Areas** | 3 columns: Assessment, Improvement, Enablement. | Icon + short paragraph each. |
| **Intentional Index Feature** | Visual of Index framework; summary text from `Intentional Index Explained.pptx`. | Graphic embed or simplified static image. |
| **Engagement Model** | Visual timeline (Discovery → Assessment → Roadmap → Execution). | Horizontal flow graphic in Signal Green. |
| **Outcomes Section** | Stack of quantified benefits: Retention + Satisfaction + Efficiency. | Graph-style layout, white background. |
| **CTA** | "Schedule a discovery call." | Full-width CTA bar, Deep Slate background. |

---

### **Insights Page**

**Purpose:**
Publish thought leadership and reinforce credibility.

| Section | Description | Layout |
|----------|--------------|--------|
| **Intro Header** | "Insights on Support, Intentions, and Growth." | Minimal hero, serif accent. |
| **Featured Articles Grid** | 3-up grid of posts (cards). | White background, 32px gutters. |
| **Subscribe / Follow CTA** | Encourage newsletter or LinkedIn follow. | Signal Green accent button. |

---

### **Contact Page**

**Purpose:**
Provide multiple low-friction ways to engage.

| Section | Description | Layout |
|----------|--------------|--------|
| **Intro Statement** | "Let's talk about aligning Support to customer intentions." | Centered text block. |
| **Contact Form** | Fields: Name, Company, Email, Message. | Direct → HubSpot form. |
| **Calendly Embed** | Inline meeting booking (kent@intentional.biz). | Right column desktop / stacked mobile. |
| **Footer** | Address, email, LinkedIn, copyright. | White background. |

---

## 6. System & Integration Notes

| Feature | Tool | Integration |
|----------|------|--------------|
| Analytics | Google Analytics 4 | Page tracking + conversion goals |
| Lead Capture | HubSpot | Sync form submissions |
| Scheduling | Calendly | Embed via HTML iframe |
| Newsletter | Mailchimp (future) | Integrated post-Jan 2026 |
| Feedback Form | Google Form | Linked in footer (soft launch feedback) |

---

## 7. Accessibility & QA Requirements

- Meet **WCAG AA** accessibility standards.
- Ensure color contrast ≥ 4.5:1 for body text.
- All images have descriptive alt text.
- Check responsiveness on desktop, tablet, mobile.
- Test all links, forms, and buttons pre-launch.
- Verify metadata and social sharing (OpenGraph + Twitter cards).

---

## 8. Launch Milestones

| Milestone | Target | Owner |
|------------|---------|--------|
| Copy & visual assets finalized | Nov 20 | Kent |
| Wix layout implemented | Dec 10 | Kent / Claude |
| QA + accessibility review | Dec 15 | ChatGPT |
| Site live (soft launch) | Dec 20 | Kent |

---

## References

- [Brand Identity Brief](../brand/brand-identity-brief.md)
- [Branding Kit Spec](../brand/branding-kit-spec-v1.md)
- [Voice & Tone](../brand/brand-voice-and-tone.md)
- [Intentional About](../content/intentional-about.md)
- [Consulting Core](../strategy/intentional-consulting-core.md)

---

> _This specification governs the first production iteration of Intentional.biz. Any deviation must be justified against brand coherence or functional necessity._
