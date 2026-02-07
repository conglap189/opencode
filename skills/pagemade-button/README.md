# PageMade Button Skill

Button styling guidelines for the PageMade project.

## Overview

This skill provides standardized button styling rules that ensure visual consistency across the PageMade application. All buttons follow the **emerald color scheme** (matching the header) with **no elevation effects**.

## Key Rules

### Color: Emerald Only
- **Default**: `#10b981` (emerald-500)
- **Hover**: `#059669` (emerald-600) 
- **Active**: `#047857` (emerald-700)

### No Elevation Effects
- ❌ No `box-shadow`
- ❌ No `transform: translateY()`
- ❌ No `transform: scale()`

### Hover Behavior
- ✅ Only darken the background color
- ✅ Smooth transition (0.2s ease)

## Quick Copy-Paste

### CSS Class
```css
.btn-emerald {
  background-color: #10b981;
  color: white;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 0.2s ease;
  box-shadow: none;
}

.btn-emerald:hover {
  background-color: #059669;
}
```

### Tailwind Classes
```html
<button class="bg-emerald-500 hover:bg-emerald-600 text-white px-5 py-2.5 rounded-lg font-medium transition-colors">
  Button
</button>
```

## Files Modified

This skill applies to:
- `/frontend/css/style.css` - Editor buttons
- `/frontend/src/editor/styles/*.css` - PageMade editor components
- `/website/src/components/*.tsx` - Landing page buttons
- `/backend/static/pagemade/*.css` - Published page buttons

## See Also

Full documentation: [SKILL.md](./SKILL.md)
