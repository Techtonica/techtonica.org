# Techtonica Style Guide

## General Principles
- Consistency across all modules.
- Accessibility (WCAG 2.1) compliance.
- Mobile-first responsive design.

## Color Palette
- Primary: # [Insert Primary Color]
- Secondary: # [Insert Secondary Color]
- Accent: # [Insert Accent Color]
- Backgrounds: # [Insert Background Colors]

## Typography
- Primary Font: [Insert Font Family]
- Headings: Bold, Sans-serif
- Body: Regular, Sans-serif

## Admin Dashboard Specific Guidelines (Added via #603)
The Admin Dashboard introduces specific UI patterns to handle complex data management and administrative tasks.

### 1. Layout & Structure
- **Sidebar Navigation**: Use a collapsible sidebar for primary navigation.
- **Content Area**: Use a light-grey background (`#F4F7F6` or equivalent) to contrast with white content cards.
- **Grid System**: Use a 12-column grid for dashboard widgets.

### 2. Components
- **Data Tables**: 
    - Use zebra-striping for readability.
    - Implement sticky headers for long lists.
    - Action buttons (Edit/Delete) should be grouped at the end of the row.
- **Forms**:
    - Use vertical stacking for labels and inputs.
    - Validation errors must appear in red text immediately below the input field.
- **Cards**:
    - Use a subtle box-shadow (`0 2px 4px rgba(0,0,0,0.1)`) and rounded corners (8px).

### 3. Interaction Patterns
- **Confirmation Modals**: Any destructive action (e.g., deleting a user) must trigger a confirmation modal with a red "Confirm" button.
- **Loading States**: Use skeleton screens for data-heavy tables during fetch operations.
- **Notifications**: Use toast notifications in the top-right corner for success/error feedback.

## Component Library
- [List of components used, e.g., Tailwind UI, Material UI, etc.]
