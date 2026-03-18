# Visual Assets Guide — Faintech Lab Beta Press Kit

**Created:** 2026-03-18
**Purpose:** Guidelines for logo usage, screenshots, and visual assets in press and marketing materials

---

## Logo Usage

### Primary Logo

**File:** `faintech-lab-logo-primary.svg`
**Format:** SVG (vector), PNG (raster fallback)
**Background:** Light/white backgrounds
**Clear Space:** Minimum 1x logo height on all sides
**Minimum Size:** 120px width for digital, 1 inch for print

### Logo Variants

| Variant | File | Use Case |
|---------|------|----------|
| Primary | `logo-primary.svg` | Light backgrounds, primary branding |
| Inverse | `logo-inverse.svg` | Dark backgrounds, headers |
| Mark Only | `logo-mark.svg` | Favicons, small applications |
| Wordmark | `logo-wordmark.svg` | Text-only contexts |

### Color Specifications

| Color | Hex | RGB | Use |
|-------|-----|-----|-----|
| Primary Blue | `#0066FF` | 0, 102, 255 | Logo, CTAs, links |
| Secondary Purple | `#7C3AED` | 124, 58, 237 | Accents, gradients |
| Dark Gray | `#1F2937` | 31, 41, 55 | Text, dark backgrounds |
| Light Gray | `#F9FAFB` | 249, 250, 251 | Backgrounds, cards |

### Logo Don'ts

- Don't stretch or distort the logo
- Don't change the logo colors outside brand palette
- Don't add effects (shadows, outlines, gradients) to logo
- Don't place logo on busy or low-contrast backgrounds
- Don't use logo smaller than minimum size

---

## Screenshot Checklist

### Required Screenshots

| Screenshot | Size | Format | Description |
|------------|------|--------|-------------|
| Hero/Dashboard | 1920x1080 | PNG | Main interface view |
| Memory View | 1920x1080 | PNG | Semantic memory panel |
| Agent List | 1920x1080 | PNG | Multi-agent overview |
| Settings | 1920x1080 | PNG | Configuration panel |
| Mobile | 390x844 | PNG | iOS/Android mobile view |

### Screenshot Guidelines

1. **Clean Data:** Use realistic but non-sensitive demo data
2. **Consistent Theme:** All screenshots in light mode for consistency
3. **No Personal Info:** Redact any real user names, emails, or API keys
4. **High Resolution:** 2x for retina displays
5. **Consistent Browser:** Use Chrome with default UI, no extensions visible

### Screenshot Don'ts

- Don't show real user data or credentials
- Don't include browser extensions or bookmarks
- Don't use low-resolution or compressed images
- Don't show error states or loading screens (unless specifically needed)
- Don't include personal desktop backgrounds

---

## Naming Convention

### File Naming Pattern

```
faintech-[category]-[description]-[variant]-[size].[ext]
```

### Examples

| File | Pattern |
|------|---------|
| `faintech-logo-primary.svg` | `faintech-logo-primary-[n/a].svg` |
| `faintech-screenshot-dashboard-1920x1080.png` | `faintech-screenshot-dashboard-[1920x1080].png` |
| `faintech-social-linkedin-1200x627.png` | `faintech-social-linkedin-[1200x627].png` |
| `faintech-press-hero-featured.png` | `faintech-press-hero-featured.png` |

### Category Prefixes

| Prefix | Use |
|--------|-----|
| `faintech-logo-*` | Logo files |
| `faintech-screenshot-*` | Product screenshots |
| `faintech-social-*` | Social media graphics |
| `faintech-press-*` | Press kit images |
| `faintech-icon-*` | Icons and marks |

### Variant Suffixes

| Suffix | Use |
|--------|-----|
| `-primary` | Default/light version |
| `-inverse` | Dark background version |
| `-@2x` | Retina/high-DPI version |
| `-thumbnail` | Small preview version |
| `-featured` | Hero/featured placement |

---

## Asset Directory Structure

```
/press-kit/
├── logos/
│   ├── faintech-logo-primary.svg
│   ├── faintech-logo-primary.png
│   ├── faintech-logo-inverse.svg
│   ├── faintech-logo-inverse.png
│   ├── faintech-logo-mark.svg
│   └── faintech-logo-wordmark.svg
├── screenshots/
│   ├── faintech-screenshot-dashboard-1920x1080.png
│   ├── faintech-screenshot-memory-1920x1080.png
│   ├── faintech-screenshot-agents-1920x1080.png
│   ├── faintech-screenshot-settings-1920x1080.png
│   └── faintech-screenshot-mobile-390x844.png
├── social/
│   ├── faintech-social-linkedin-1200x627.png
│   ├── faintech-social-twitter-1200x675.png
│   └── faintech-social-twitter-square-1200x1200.png
└── press/
    ├── faintech-press-hero-featured.png
    └── faintech-press-founder-headshot.jpg
```

---

## Export Settings

### PNG Export (Screenshots/Social)

- **Resolution:** 72 DPI for web, 300 DPI for print
- **Color Space:** sRGB
- **Compression:** Medium (balance quality and size)
- **Transparency:** Non-transparent backgrounds (white/brand color)

### SVG Export (Logos/Icons)

- **Outline Text:** Yes (convert fonts to paths)
- **Minify:** Yes (reduce file size)
- **Responsive:** Yes (use viewBox)

### JPG Export (Photos)

- **Quality:** 85% (balance quality and size)
- **Color Space:** sRGB
- **Progressive:** Yes (for web loading)

---

## Third-Party Usage

### Press Usage

- Credit line required: "Image courtesy of Faintech Lab"
- No modification of logos or brand elements
- Contact press@faintech-lab.com for high-resolution assets

### Partner Usage

- Written approval required for logo usage
- Must follow brand guidelines
- Annual review of usage compliance

---

**Created:** 2026-03-18
**Status:** Ready for review
**Owner:** faintech-content-creator
