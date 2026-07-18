---
name: Azure Chat Narrative
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#3e4850'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6e7881'
  outline-variant: '#bec8d2'
  surface-tint: '#006591'
  primary: '#006591'
  on-primary: '#ffffff'
  primary-container: '#0ea5e9'
  on-primary-container: '#003751'
  inverse-primary: '#89ceff'
  secondary: '#006686'
  on-secondary: '#ffffff'
  secondary-container: '#7ed4fd'
  on-secondary-container: '#005b78'
  tertiary: '#576065'
  on-tertiary: '#ffffff'
  tertiary-container: '#949da3'
  on-tertiary-container: '#2c3539'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c9e6ff'
  primary-fixed-dim: '#89ceff'
  on-primary-fixed: '#001e2f'
  on-primary-fixed-variant: '#004c6e'
  secondary-fixed: '#c0e8ff'
  secondary-fixed-dim: '#7bd1fa'
  on-secondary-fixed: '#001e2b'
  on-secondary-fixed-variant: '#004d66'
  tertiary-fixed: '#dbe4ea'
  tertiary-fixed-dim: '#bfc8ce'
  on-tertiary-fixed: '#141d21'
  on-tertiary-fixed-variant: '#3f484d'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-sm:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  message-text:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  sidebar-width: 320px
  max-content-width: 1200px
---

## Brand & Style

The design system is centered on clarity, flow, and digital serenity. The target audience includes professional teams and social communities seeking a focused environment for communication. The brand personality is dependable yet approachable—balancing the precision of a productivity tool with the warmth of a social platform.

The design style is **Minimalist with Soft Elevation**. It utilizes significant whitespace to reduce cognitive load during long chat sessions, combined with subtle glassmorphism and soft shadows to create a sense of organized depth. The interface feels light and airy, prioritizing the content (the messages) over the container.

## Colors

The palette is anchored by "Sky Blue" (#0ea5e9), used for primary actions and active states. 

- **Primary:** Sky Blue (#0ea5e9) for high-emphasis elements like "Send" buttons and active navigation icons.
- **Secondary:** Light Sky (#7dd3fc) for hover states and selection indicators.
- **Surface/Tertiary:** Azure Tint (#f0f9ff) for chat bubble backgrounds (incoming) and sidebar highlighting.
- **Neutral:** Slate Grays (#64748b) for secondary text and borders.
- **Background:** A crisp, off-white (#f8fafc) is used for the main application canvas to keep the interface feeling fresh and expansive.

## Typography

This design system uses **Hanken Grotesk** for structural elements like headers and titles to provide a modern, sharp edge. **Inter** is utilized for all body copy and message text due to its exceptional legibility and neutral tone, ensuring that long threads of text remain easy to scan.

For mobile devices, `display-lg` should be reduced to 24px to ensure headers do not wrap aggressively. All message bubbles use the `message-text` token, which is slightly tighter than standard body copy to allow for more content on screen without sacrificing readability.

## Layout & Spacing

The layout follows a **Fixed-Fluid Hybrid** model. The sidebar remains fixed at 320px for easy conversation switching, while the main chat window expands to fill the remaining viewport. 

- **Grid:** A 12-column grid is used for dashboard views and profile pages.
- **Padding:** A consistent 16px (md) gutter is maintained between major UI blocks. 
- **Mobile:** On mobile screens, the sidebar becomes a hidden drawer, and the chat area takes 100% of the viewport width with 12px horizontal margins.
- **Rhythm:** All vertical spacing should be a multiple of the 4px base unit to maintain a tight, professional rhythm.

## Elevation & Depth

Visual hierarchy is established through **Tonal Layering** and **Ambient Shadows**.

1.  **Level 0 (Base):** The main application background (#f8fafc).
2.  **Level 1 (Surface):** The Sidebar and Chat Header, using a white background with a 1px soft border (#e2e8f0).
3.  **Level 2 (Floating):** Chat bubbles and Input areas. Bubbles use a subtle 4px blur shadow with 5% opacity to separate them from the background.
4.  **Level 3 (Overlay):** Modals and User Profile cards. These use a more pronounced 12px blur shadow with a slight blue tint (rgba(14, 165, 233, 0.1)) to draw focus.

Glassmorphism is applied specifically to the chat header, using a `backdrop-blur(10px)` to provide a sense of continuity as messages scroll underneath.

## Shapes

The design system employs a **Rounded** shape language to reinforce the "friendly and professional" brand pillar. 

- **Standard Elements:** Buttons, input fields, and small cards use a 0.5rem (8px) radius.
- **Chat Bubbles:** These utilize a "rounded-lg" (16px) radius to create a soft, speech-like appearance. 
- **Avatars:** Always perfectly circular (pill-shaped) to distinguish human elements from functional UI components.
- **Action Icons:** Encased in circular or highly rounded containers to signify touch-friendliness.

## Components

### Buttons
- **Primary:** Solid Sky Blue with white text. High rounded corners (0.5rem).
- **Secondary:** Light Sky background with Sky Blue text. No shadow.
- **Ghost:** No background; Sky Blue text. Used for less frequent actions like "Mute."

### Chat Bubbles
- **Sent:** Sky Blue background with White text. Aligned right.
- **Received:** Azure Tint (#f0f9ff) background with Slate Gray text. Aligned left.
- **Radius:** 16px, with the corner closest to the sender slightly sharpened (4px) to indicate direction.

### Message Input
- A single-line container with 16px internal padding.
- Includes a "plus" icon for attachments on the left and a "send" icon on the right.
- Focus state: A 2px Sky Blue ring with 20% opacity.

### Sidebar
- Contains a list of "Conversation Cells."
- **Active State:** A vertical 4px Sky Blue "pill" on the far left edge and a light blue background tint.
- **Unread Indicator:** A small Sky Blue dot next to the timestamp.

### Lists & Chips
- Status chips (Online/Away) use the same roundedness as buttons but with smaller font (label-caps).
- Online status uses a Green (#10b981) accent, following the same soft-shadow rules.