---
name: pagemade-button
description: Button styling guidelines for PageMade project using emerald color scheme
---

# PageMade Button Skill

This skill defines the **standard button styling** for the PageMade project. All buttons must follow these guidelines to maintain visual consistency across the application.

## When to Use

- When creating new buttons in PageMade (frontend, website, or backend)
- When styling existing buttons
- When reviewing button implementations
- When building UI components that include buttons

## Design Specifications

### Color Palette (MANDATORY)

**Primary Colors - Emerald (Header Color):**
```css
/* Base/Default State */
--pm-btn-bg: #10b981;           /* emerald-500 */
--pm-btn-text: #ffffff;          /* white */

/* Hover State */
--pm-btn-bg-hover: #059669;     /* emerald-600 */

/* Active/Pressed State */
--pm-btn-bg-active: #047857;    /* emerald-700 */

/* Focus Ring */
--pm-btn-focus-ring: rgba(16, 185, 129, 0.5);  /* emerald-500 with opacity */
```

**Secondary/Outline Variant:**
```css
/* Base State */
--pm-btn-outline-border: #10b981;
--pm-btn-outline-text: #10b981;
--pm-btn-outline-bg: transparent;

/* Hover State */
--pm-btn-outline-bg-hover: rgba(16, 185, 129, 0.1);
--pm-btn-outline-text-hover: #059669;
--pm-btn-outline-border-hover: #059669;
```

### Restrictions (MUST FOLLOW)

#### NO Elevation Effects
```css
/* ❌ FORBIDDEN - Do NOT use these: */
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* No shadow */
transform: translateY(-2px);                /* No lift on hover */
transform: scale(1.05);                     /* No scale */
box-shadow: var(--shadow-lg);               /* No shadow variables */

/* ✅ ALLOWED - Only use: */
box-shadow: none;
transform: none;
```

#### NO Other Colors
```css
/* ❌ FORBIDDEN: */
background: #3b82f6;    /* blue */
background: #8b5cf6;    /* purple */
background: #ef4444;    /* red (except for danger buttons) */
background: #6366f1;    /* indigo */
background: var(--gradient-primary);  /* gradients */

/* ✅ ONLY USE: */
background: #10b981;    /* emerald-500 */
background: #059669;    /* emerald-600 */
background: #047857;    /* emerald-700 */
```

## Standard Button Styles

### Primary Button (Solid Emerald)

```css
.pm-btn-primary,
.btn-emerald {
  /* Base */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  
  /* Sizing */
  padding: 0.625rem 1.25rem;  /* py-2.5 px-5 */
  font-size: 0.875rem;        /* text-sm */
  font-weight: 500;           /* font-medium */
  line-height: 1.5;
  
  /* Shape */
  border-radius: 0.5rem;      /* rounded-lg */
  border: none;
  
  /* Colors */
  background-color: #10b981;
  color: #ffffff;
  
  /* Interaction */
  cursor: pointer;
  transition: background-color 0.2s ease;
  
  /* NO ELEVATION */
  box-shadow: none;
  transform: none;
}

.pm-btn-primary:hover,
.btn-emerald:hover {
  background-color: #059669;
  /* NO transform, NO shadow change */
}

.pm-btn-primary:active,
.btn-emerald:active {
  background-color: #047857;
}

.pm-btn-primary:focus,
.btn-emerald:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.5);
}

.pm-btn-primary:disabled,
.btn-emerald:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
  opacity: 0.6;
}
```

### Outline Button (Emerald Border)

```css
.pm-btn-outline,
.btn-emerald-outline {
  /* Base */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  
  /* Sizing */
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.5;
  
  /* Shape */
  border-radius: 0.5rem;
  border: 2px solid #10b981;
  
  /* Colors */
  background-color: transparent;
  color: #10b981;
  
  /* Interaction */
  cursor: pointer;
  transition: all 0.2s ease;
  
  /* NO ELEVATION */
  box-shadow: none;
  transform: none;
}

.pm-btn-outline:hover,
.btn-emerald-outline:hover {
  background-color: rgba(16, 185, 129, 0.1);
  border-color: #059669;
  color: #059669;
}

.pm-btn-outline:active,
.btn-emerald-outline:active {
  background-color: rgba(16, 185, 129, 0.2);
  border-color: #047857;
  color: #047857;
}
```

### Text/Link Button

```css
.pm-btn-text,
.btn-emerald-text {
  /* Base */
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  
  /* Sizing */
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  
  /* Shape */
  border: none;
  border-radius: 0.375rem;
  
  /* Colors */
  background-color: transparent;
  color: #10b981;
  
  /* Interaction */
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
  
  /* NO ELEVATION */
  box-shadow: none;
}

.pm-btn-text:hover,
.btn-emerald-text:hover {
  background-color: rgba(16, 185, 129, 0.1);
  color: #059669;
}
```

## Tailwind CSS Classes

When using Tailwind CSS, use these class combinations:

### Primary Button
```html
<button class="inline-flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-medium text-white bg-emerald-500 hover:bg-emerald-600 active:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 rounded-lg transition-colors duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed">
  Button Text
</button>
```

### Outline Button
```html
<button class="inline-flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-medium text-emerald-500 border-2 border-emerald-500 hover:bg-emerald-500/10 hover:text-emerald-600 hover:border-emerald-600 rounded-lg transition-colors duration-200 bg-transparent">
  Button Text
</button>
```

### Text Button
```html
<button class="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-emerald-500 hover:bg-emerald-500/10 hover:text-emerald-600 rounded-md transition-colors duration-200 bg-transparent border-none">
  Button Text
</button>
```

## Dark Mode Support

```css
/* Dark mode adjustments */
.dark .pm-btn-primary,
.dark .btn-emerald {
  background-color: #10b981;
  color: #ffffff;
}

.dark .pm-btn-primary:hover,
.dark .btn-emerald:hover {
  background-color: #34d399;  /* emerald-400 - slightly lighter in dark mode */
}

.dark .pm-btn-outline,
.dark .btn-emerald-outline {
  border-color: #34d399;
  color: #34d399;
}

.dark .pm-btn-outline:hover,
.dark .btn-emerald-outline:hover {
  background-color: rgba(52, 211, 153, 0.15);
  border-color: #6ee7b7;
  color: #6ee7b7;
}
```

## Size Variants

```css
/* Small */
.pm-btn-sm {
  padding: 0.375rem 0.75rem;  /* py-1.5 px-3 */
  font-size: 0.75rem;          /* text-xs */
}

/* Medium (default) */
.pm-btn-md {
  padding: 0.625rem 1.25rem;  /* py-2.5 px-5 */
  font-size: 0.875rem;         /* text-sm */
}

/* Large */
.pm-btn-lg {
  padding: 0.75rem 1.5rem;    /* py-3 px-6 */
  font-size: 1rem;             /* text-base */
}
```

## Icon Buttons

```css
.pm-btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  border-radius: 0.5rem;
  background-color: #10b981;
  color: #ffffff;
  transition: background-color 0.2s ease;
  box-shadow: none;
}

.pm-btn-icon:hover {
  background-color: #059669;
}

.pm-btn-icon i,
.pm-btn-icon svg {
  font-size: 1rem;
  width: 1rem;
  height: 1rem;
}
```

## Usage Examples

### In GrapesJS/PageMade Editor
```javascript
// When adding button blocks
editor.BlockManager.add('pm-button', {
  label: 'Button',
  content: `<button class="pm-btn-primary">Click me</button>`,
  category: 'Basic',
});
```

### In React/Next.js (Website)
```tsx
// Button component
const Button = ({ variant = 'primary', children, ...props }) => {
  const baseClass = "inline-flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-medium rounded-lg transition-colors duration-200";
  
  const variants = {
    primary: "bg-emerald-500 hover:bg-emerald-600 text-white",
    outline: "bg-transparent border-2 border-emerald-500 text-emerald-500 hover:bg-emerald-500/10 hover:text-emerald-600 hover:border-emerald-600",
    text: "bg-transparent text-emerald-500 hover:bg-emerald-500/10 hover:text-emerald-600 px-3 py-2"
  };
  
  return (
    <button className={`${baseClass} ${variants[variant]}`} {...props}>
      {children}
    </button>
  );
};
```

## Checklist Before Implementation

- [ ] Button uses emerald color (#10b981 base)
- [ ] Hover state uses darker emerald (#059669)
- [ ] No box-shadow or elevation effects
- [ ] No transform effects (translateY, scale)
- [ ] Transition only on background-color (and border/color for outline)
- [ ] Focus state has ring/outline for accessibility
- [ ] Disabled state is visually distinct

## Quick Reference

| State | Solid Background | Text/Border Color |
|-------|------------------|-------------------|
| Default | `#10b981` | `white` / `#10b981` |
| Hover | `#059669` | `white` / `#059669` |
| Active | `#047857` | `white` / `#047857` |
| Disabled | `#d1d5db` | `#9ca3af` |

---

*This skill ensures consistent button styling across the PageMade project, matching the emerald header color without elevation effects.*
