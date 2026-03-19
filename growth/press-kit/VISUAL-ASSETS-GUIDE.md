# Visual Assets Guide - Faintech Lab Beta Launch

**Document Purpose**: Guidelines for creating, naming, and deploying visual assets across all beta launch channels

**Target Audience**: faintech-content-creator, faintech-marketing-lead, designers, external press

**Date**: 2026-03-19

---

## Logo Usage Guidelines

### Primary Logo

**Files:**
- `faintech-lab-logo-primary.svg` - Full color logo for light backgrounds
- `faintech-lab-logo-dark.svg` - Light logo for dark backgrounds
- `faintech-lab-logo-mono.svg` - Single color for limited contexts

**Usage Rules:**
- **Minimum size**: 120px width for digital, 1 inch for print
- **Clear space**: Maintain padding equal to the height of the "F" in "Faintech" on all sides
- **Background contrast**: Ensure 4.5:1 contrast ratio minimum
- **No modifications**: Do not stretch, rotate, add effects, or change colors
- **No competing logos**: Do not place other brand logos within clear space

### Logo Variations

**Wordmark Only:**
- `faintech-lab-wordmark.svg` - Text only, no icon
- Use when space is extremely limited (e.g., social media avatars)

**Icon Only:**
- `faintech-lab-icon.svg` - Logo mark without text
- Use for favicons, app icons, small UI elements

### Incorrect Usage Examples

❌ **Don't:**
- Stretch or compress logo proportions
- Place logo on busy or low-contrast backgrounds
- Add drop shadows, glows, or 3D effects
- Rotate or flip the logo
- Change brand colors arbitrarily
- Place logo inside a container (unless transparent background)

✅ **Do:**
- Use provided logo files as-is
- Maintain clear space around logo
- Test contrast on intended background before publishing
- Contact design team for custom applications

---

## Color Palette

### Primary Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Faintech Blue** | `#0066CC` | 0, 102, 204 | Primary brand color, CTAs, links |
| **Deep Navy** | `#0A1628` | 10, 22, 40 | Text, dark backgrounds |
| **Clean White** | `#FFFFFF` | 255, 255, 255 | Backgrounds, text on dark |

### Secondary Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Success Green** | `#00C853` | 0, 200, 83 | Positive metrics, success states |
| **Warning Amber** | `#FFB300` | 255, 179, 0 | Caution, attention, beta labels |
| **Neutral Gray** | `#6B7280` | 107, 114, 128 | Secondary text, borders, dividers |

### Usage Guidelines

- **Primary colors**: Use for brand elements, main CTAs, key information
- **Secondary colors**: Use for supporting elements, status indicators, hierarchy
- **Backgrounds**: Prefer clean white or deep navy for high contrast
- **Accessibility**: All text must meet WCAG AA contrast standards (4.5:1 for body text)

---

## Typography

### Primary Font: Inter

**Weights:**
- **Regular (400)**: Body text, descriptions
- **Medium (500)**: Subheadings, labels
- **Semibold (600)**: Headings, emphasis
- **Bold (700)**: Hero text, CTAs

### Usage Rules

- **Headings**: Inter Semibold or Bold, sentence case
- **Body text**: Inter Regular, 16px minimum for digital
- **Code/technical**: JetBrains Mono or Fira Code for code snippets
- **Line height**: 1.5 for body text, 1.2 for headings

### Fallback Fonts

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
```

---

## Screenshot Checklist

### Required Screenshots for Beta Launch

**1. Dashboard/Overview**
- [ ] Clean state with sample data
- [ ] Dark mode version (if supported)
- [ ] Mobile responsive version
- [ ] Highlight key metrics prominently

**2. API Documentation**
- [ ] Code example with syntax highlighting
- [ ] Response payload example
- [ ] Error handling example
- [ ] Authentication flow

**3. Memory Management Interface**
- [ ] List view with search/filter
- [ ] Detail view with semantic context
- [ ] Multi-agent memory coordination
- [ ] Bulk operations (if applicable)

**4. Agent Context View**
- [ ] Active agents dashboard
- [ ] Memory distribution across agents
- [ ] Real-time activity feed
- [ ] Debug/observability panel

**5. Onboarding/First-Run**
- [ ] Welcome screen
- [ ] API key generation flow
- [ ] First memory creation
- [ ] Quick start guide

### Screenshot Guidelines

- **Resolution**: 2x for retina displays (minimum 2560px width)
- **Format**: PNG for UI screenshots, JPEG for photographs
- **Background**: Use realistic data (not "Lorem ipsum")
- **Privacy**: No real user data, PII, or API keys
- **Annotations**: Use subtle arrows or highlights for key features
- **Consistency**: Same browser window size across all screenshots

### Naming Convention

```
[feature]-[view]-[variant]-[size].[format]

Examples:
dashboard-overview-light-2x.png
api-docs-code-example-dark-2x.png
memory-list-filters-mobile-1x.png
agent-context-realtime-desktop-2x.png
```

---

## Social Media Assets

### Profile Images

**Platforms:**
- Twitter/X: 400x400px
- LinkedIn: 400x400px
- GitHub: 500x500px
- Discord: 512x512px

**Use**: Faintech Lab icon or wordmark (platform-dependent)

### Cover Images

**Twitter/X Header:**
- Size: 1500x500px
- Content: Logo + tagline + hero visual
- Variant: Dark and light background

**LinkedIn Banner:**
- Size: 1584x396px
- Content: Logo + tagline + CTA
- Include: Website URL or GitHub link

### Post Images

**Blog Post Thumbnails:**
- Size: 1200x630px (Open Graph standard)
- Content: Title + relevant visual + logo
- Text: Readable at small sizes (avoid dense text)

**Twitter/LinkedIn Post Images:**
- Size: 1200x675px (16:9 aspect ratio)
- Content: Single key message + visual
- Text: Maximum 20% of image area

### Naming Convention

```
[platform]-[type]-[variant]-[date].[format]

Examples:
twitter-profile-icon-20260319.png
linkedin-banner-launch-20260319.jpg
og-image-beta-launch-20260319.png
twitter-post-announcement-dark-20260319.jpg
```

---

## Presentation Assets

### Slide Deck Template

**Title Slide:**
- Logo (centered or top-left)
- Title (Inter Bold, 48pt)
- Subtitle/date (Inter Regular, 24pt)
- Background: Clean white or deep navy

**Content Slide:**
- Title (Inter Semibold, 36pt)
- Body text (Inter Regular, 18pt minimum)
- Maximum 6 bullet points per slide
- Use icons or visuals to break text

**Code Slide:**
- JetBrains Mono or Fira Code
- Dark background (#0A1628)
- Syntax highlighting enabled
- Maximum 10 lines of code per slide

### Naming Convention

```
presentation-[topic]-[date]-[slide-number].[format]

Examples:
presentation-beta-launch-20260319-01.png
presentation-api-overview-20260319-12.png
presentation-architecture-20260319-08.png
```

---

## Video Assets

### Demo Video Guidelines

**Length**: 2-3 minutes maximum
**Resolution**: 1920x1080 (1080p) minimum
**Format**: MP4 (H.264 codec)
**Frame rate**: 30fps

**Structure:**
1. **Hook (0-10s)**: Problem statement
2. **Solution (10-60s)**: AMC overview
3. **Demo (60-150s)**: Key features walkthrough
4. **CTA (150-180s)**: Apply for beta

**Requirements:**
- Clear audio (no background noise)
- Screen recording with cursor visible
- Subtitles/captions for accessibility
- Thumbnail image (1280x720px)

### Thumbnail Guidelines

- **Size**: 1280x720px
- **Content**: Key visual + text overlay
- **Text**: Readable at small sizes
- **Branding**: Include logo subtly

### Naming Convention

```
video-[type]-[variant]-[date].[format]

Examples:
video-demo-walkthrough-20260319.mp4
video-thumbnail-overview-20260319.jpg
video-tutorial-api-basics-20260319.mp4
```

---

## Icon Set

### Custom Icons Needed

- **Memory icon**: Brain/database hybrid
- **Agent icon**: Robot/AI symbol
- **Search icon**: Magnifying glass with semantic indicator
- **Context icon**: Connected nodes/network
- **API icon**: Code brackets with arrow

### Icon Guidelines

- **Style**: Outline or filled, consistent across set
- **Size**: 24x24px base, scalable to 48x48px
- **Color**: Single color (Faintech Blue or Deep Navy)
- **Format**: SVG for scalability, PNG fallback

---

## File Organization

```
faintech-lab-assets/
├── logos/
│   ├── primary/
│   │   ├── faintech-lab-logo-primary.svg
│   │   ├── faintech-lab-logo-dark.svg
│   │   └── faintech-lab-logo-mono.svg
│   ├── wordmark/
│   │   └── faintech-lab-wordmark.svg
│   └── icon/
│       └── faintech-lab-icon.svg
├── screenshots/
│   ├── dashboard/
│   ├── api-docs/
│   ├── memory-management/
│   ├── agent-context/
│   └── onboarding/
├── social/
│   ├── profiles/
│   ├── covers/
│   └── posts/
├── presentations/
│   └── templates/
├── video/
│   ├── demos/
│   └── thumbnails/
└── icons/
    └── custom/
```

---

## Asset Request Process

**For new assets:**
1. Open GitHub issue with `asset-request` label
2. Specify: type, size, format, deadline, use case
3. Attach wireframes or references if possible
4. Assign to `faintech-content-creator` or design team

**Turnaround time:**
- **Logos/icons**: 3-5 business days
- **Screenshots**: 1-2 business days
- **Social media**: 1-2 business days
- **Video**: 5-10 business days

---

## Quality Checklist

Before publishing any visual asset:

- [ ] Correct logo usage (no modifications)
- [ ] Color palette compliance
- [ ] Typography consistency
- [ ] Accessibility contrast standards met
- [ ] File naming convention followed
- [ ] Correct file format (SVG/PNG/MP4)
- [ ] Resolution appropriate for use case
- [ ] No PII or sensitive data visible
- [ ] Brand guidelines reviewed

---

**Document Version**: 1.0
**Date**: 2026-03-19
**Status**: Draft - Ready for Review
**Task**: CONTENT-20260318133800-PRESS-KIT (AC4/5)
**Next Owner**: faintech-content-creator (create missing assets)
