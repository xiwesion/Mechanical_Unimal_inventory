# UI Design Documentation - Inventory System
## Soft Bright Elegant Theme with Graceful Gradations

---

## 🎨 Design Philosophy

Sistem Inventory menggunakan tema UI yang **lembut, cerah, dan elegan** tanpa kontras berlebihan. Desain ini terinspirasi dari:
- **Natural Colors** - Warna-warna alam yang menenangkan
- **Soft Gradations** - Gradasi halus antar warna
- **Elegant Simplicity** - Sederhana namun sophisticated
- **Eye-Friendly** - Aman untuk mata dalam penggunaan jangka panjang

---

## 🎨 Color Palette

### Primary Color Suite - Soft Green
```
Soft Green #E8F5E9  ← Very Soft (Backgrounds)
Soft Green #C8E6C9  ← Light
Soft Green #A5D6A7  ← Primary (Main color)
Soft Green #81C784  ← Medium
Soft Green #66BB6A  ← Dark (Active states)
```

**Usage:**
- `#E8F5E9` - Page backgrounds, very light elements
- `#A5D6A7` - Primary buttons, headers
- `#66BB6A` - Active states, important elements

### Secondary Color Suite - Soft Blue
```
Soft Blue #E3F2FD   ← Very Soft (Alternative backgrounds)
Soft Blue #BBDEFB   ← Light
Soft Blue #90CAF9   ← Secondary
Soft Blue #64B5F6   ← Medium
Soft Blue #42A5F5   ← Dark (Info elements)
```

**Usage:**
- `#E3F2FD` - Alternative sections, accents
- `#90CAF9` - Secondary buttons, info elements
- `#42A5F5` - Links, hover states

### Accent Colors - Complementary Palette
```
Soft Pink   #F8BBD0 - Accents, alerts
Soft Orange #FFE0B2 - Warnings, attention
Soft Purple #E1BEE7 - Special elements
```

### Status Colors - Semantic
```
Success/Active  #66BB6A - Green (Aktif)
Warning         #FFA726 - Orange (Maintenance)
Danger/Depleted #EF5350 - Red (Habis Pakai)
Info            #42A5F5 - Blue (Information)
Neutral/Archive #9E9E9E - Gray (Diarsipkan)
```

### Text & Backgrounds
```
Text Dark      #2C3E50 - Main text
Text Light     #7F8C8D - Secondary text
Border Light   #E8EAED - Light borders
Background     #FAFBFC - Off-white background
```

---

## 🏗️ Layout Structure

### Sidebar
- **Background**: Gradient from soft green to soft blue
- **Border**: Light border right
- **Font**: Clean, readable sans-serif
- **Items**: Rounded buttons with subtle hover effect

### Header
- **Title**: Gradient text (green to blue)
- **Subtitle**: Light gray text
- **Animation**: Fade in up (0.6s)

### Cards & Containers
- **Background**: White (#FFFFFF)
- **Border**: Light border (#E8EAED)
- **Corner**: Rounded 8px
- **Shadow**: Subtle shadow
- **Hover**: Light background color, slight lift effect

### Buttons
- **Primary**: Gradient background (soft green)
- **Secondary**: Gradient background (soft blue)
- **Hover**: Darker gradient + lifted effect
- **Active**: Solid color + pressed effect
- **Padding**: 10px 24px
- **Border Radius**: 8px
- **Font**: Bold, white text

### Input Fields
- **Border**: 1.5px light gray
- **Focus**: Green border + subtle glow
- **Radius**: 6px
- **Padding**: 8px 12px
- **Font**: Regular, 14px

### Tabs
- **Inactive**: Transparent, light gray text
- **Active**: Light background + green bottom border
- **Hover**: Background color change
- **Animation**: Smooth transition

---

## 🎬 Animations

### Available Animations

#### 1. Fade In Up
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
Duration: 0.6s
Timing: ease-out
Usage: Page loads, component entrance
```

#### 2. Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
Duration: 0.4s
Timing: ease-out
Usage: General fade effect
```

#### 3. Slide Down
```css
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
Duration: 0.4s
Timing: ease-out
Usage: Dropdowns, tabs
```

#### 4. Scale In
```css
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
Duration: 0.4s
Timing: ease-out
Usage: Cards, modals
```

#### 5. Pulse
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}
Duration: Continuous
Usage: Highlight important elements
```

#### 6. Glow
```css
@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px rgba(165, 214, 167, 0.3); }
  50% { box-shadow: 0 0 15px rgba(165, 214, 167, 0.5); }
}
Duration: Continuous
Usage: Focus states
```

### Animation Guidelines
- **Page Load**: Use `fadeInUp` (0.6s)
- **User Interactions**: Use `slideDown` (0.4s)
- **Card Entrance**: Use `scaleIn` (0.4s)
- **Status Changes**: Use `pulse` (continuous)
- **Hover States**: Use `glow` (continuous)

---

## 🎯 Component Styling

### 1. Buttons

#### Primary Button
```css
Background: linear-gradient(135deg, #A5D6A7 0%, #81C784 100%)
Color: White
Border: None
Border-Radius: 8px
Padding: 10px 24px
Font-Weight: 600
Box-Shadow: 0 2px 8px rgba(165, 214, 167, 0.25)

Hover:
  Background: linear-gradient(135deg, #81C784 0%, #66BB6A 100%)
  Box-Shadow: 0 4px 12px rgba(165, 214, 167, 0.4)
  Transform: translateY(-2px)
```

#### Secondary Button
```css
Background: linear-gradient(135deg, #90CAF9 0%, #64B5F6 100%)
Color: White
Similar styling to primary
```

#### Success Button (Green)
```css
Background: #66BB6A
Hover: Darken 10%
```

#### Warning Button (Orange)
```css
Background: #FFA726
Hover: Darken 10%
```

#### Danger Button (Red)
```css
Background: #EF5350
Hover: Darken 10%
```

### 2. Input Fields

```css
Border: 1.5px solid #E8EAED
Border-Radius: 6px
Background: White
Padding: 8px 12px
Font-Size: 14px
Color: #2C3E50

Focus:
  Border-Color: #66BB6A
  Box-Shadow: 0 0 0 3px rgba(165, 214, 167, 0.15)
  Outline: None

Placeholder:
  Color: #7F8C8D
```

### 3. Tabs

```css
Tab Button (Inactive):
  Background: Transparent
  Color: #7F8C8D
  Border-Bottom: 3px transparent
  Padding: 12px 24px
  
Tab Button (Active):
  Color: #66BB6A
  Background: rgba(165, 214, 167, 0.1)
  Border-Bottom: 3px #66BB6A

Tab Button (Hover):
  Color: #66BB6A
  Background: rgba(165, 214, 167, 0.1)
```

### 4. Cards

```css
Background: White
Border: 1px solid #E8EAED
Border-Radius: 8px
Padding: 16px
Box-Shadow: 0 1px 3px rgba(0, 0, 0, 0.1)
Animation: scaleIn 0.4s ease-out

Hover:
  Box-Shadow: 0 2px 8px rgba(0, 0, 0, 0.15)
  Transform: translateY(-2px)
```

### 5. Alerts & Messages

#### Success Alert
```css
Background: rgba(102, 187, 106, 0.1) to rgba(76, 175, 80, 0.05) gradient
Border-Left: 4px #66BB6A
Color: #2C3E50
Padding: 12px 16px
Border-Radius: 6px
```

#### Warning Alert
```css
Background: rgba(255, 152, 0, 0.1) to rgba(255, 193, 7, 0.05) gradient
Border-Left: 4px #FFA726
```

#### Error Alert
```css
Background: rgba(239, 83, 80, 0.1) to rgba(244, 67, 54, 0.05) gradient
Border-Left: 4px #EF5350
```

#### Info Alert
```css
Background: rgba(66, 165, 245, 0.1) to rgba(25, 103, 210, 0.05) gradient
Border-Left: 4px #42A5F5
```

### 6. Data Tables

```css
Header:
  Background: linear-gradient(135deg, #A5D6A7 0%, #90CAF9 100%)
  Color: White
  Font-Weight: 700
  Padding: 12px

Rows:
  Background: White
  Border: 1px #E8EAED
  
Row Hover:
  Background: rgba(165, 214, 167, 0.1)
```

### 7. Metric/Stat Box

```css
Background: linear-gradient(135deg, #E8F5E9 0%, rgba(227, 242, 253, 0.5) 100%)
Border: 1px #E8EAED
Padding: 16px
Border-Radius: 8px
Animation: scaleIn 0.4s ease-out

Value:
  Color: #66BB6A
  Font-Weight: 700
  Font-Size: 24px
  
Label:
  Color: #7F8C8D
  Font-Weight: 600
  Font-Size: 14px
```

---

## 📱 Responsive Design

### Breakpoints
```
Desktop  : ≥ 1200px (full layout)
Tablet   : 768px - 1199px (adaptive)
Mobile   : < 768px (optimized)
```

### Mobile Adjustments
```css
h1: 24px (from 28px)
h2: 20px (from 24px)
h3: 16px (from 20px)

Buttons: width 100% on mobile
Tabs: font-size reduced, padding reduced
Cards: full width, no margins
```

---

## ✨ Special Effects

### Gradient Backgrounds
```
Primary Gradient: 135deg, #E8F5E9 0% → #E3F2FD 100%
Secondary Gradient: 180deg, #E8F5E9 0% → #E3F2FD 100%
Text Gradient: #66BB6A 0% → #42A5F5 100%
```

### Box Shadows
```
Subtle: 0 1px 3px rgba(0, 0, 0, 0.1)
Small: 0 2px 8px rgba(165, 214, 167, 0.25)
Medium: 0 4px 12px rgba(165, 214, 167, 0.4)
Large: 0 8px 20px rgba(0, 0, 0, 0.15)
```

### Borders
```
Default: 1px solid #E8EAED
Focus: 1.5px solid #66BB6A
Divider: 1px gradient from transparent to #E8EAED to transparent
```

---

## 🎭 Transitions

```css
Default Transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)

Properties:
  - background-color
  - border-color
  - box-shadow
  - color
  - transform
  - opacity
```

---

## 📐 Spacing System

```
Margins: 0, 8px, 12px, 16px, 20px, 24px, 32px
Paddings: 8px, 12px, 16px, 20px, 24px, 32px
Border Radius: 4px (small), 6px (medium), 8px (buttons/cards)
```

---

## 🔤 Typography

### Font Family
```
Primary: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
Fallback: System fonts
```

### Font Sizes
```
h1: 2.8rem (44px)
h2: 2rem (32px)
h3: 1.5rem (24px)
Body: 1rem (16px)
Small: 0.875rem (14px)
Caption: 0.75rem (12px)
```

### Font Weights
```
Regular: 400
Medium: 600
Bold: 700
Extra Bold: 800 (titles)
```

### Line Heights
```
Headings: 1.2
Body: 1.5
Compact: 1.3
```

---

## 🎯 Best Practices

### Do's ✅
- Use soft colors consistently
- Apply animations sparingly
- Maintain adequate contrast for accessibility
- Keep shadows subtle
- Use gradients for depth, not decoration
- Ensure hover states are obvious

### Don'ts ❌
- Don't use harsh bright colors
- Don't animate too many elements
- Don't use too many different fonts
- Don't add heavy shadows
- Don't mix too many gradients
- Don't forget WCAG AA accessibility

---

## ♿ Accessibility

### WCAG AA Compliance
- **Color Contrast**: Text meets WCAG AA standards
- **Focus States**: Clear and visible
- **Typography**: Readable sizes (min 12px)
- **Animations**: Respects `prefers-reduced-motion`

### Keyboard Navigation
- ✅ All buttons focusable
- ✅ Tab order logical
- ✅ Form controls labeled
- ✅ Skip links available

---

## 🖥️ Browser Support
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

---

**Design Reference Document**  
Created: April 16, 2026  
Version: 1.0  
Status: ✅ Production Ready
