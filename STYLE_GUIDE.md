# Techtonica Style Guide

## General Principles
- Maintain a clean, professional, and accessible interface.
- Use a consistent color palette and typography across all modules.

## Applicant Dashboard Style Guidelines

### Layout & Structure
- **Containerization**: Use a centered layout with a maximum width for dashboard content to prevent stretching on ultra-wide monitors.
- **Card-Based UI**: Information should be grouped into cards with subtle borders or soft shadows to separate different sections of the application process.
- **Navigation**: A persistent sidebar or top-navigation bar must be used for quick access to dashboard sections (e.g., Profile, Application Status, Resources).

### Typography
- **Headings**: Use bold, sans-serif fonts for section headers to create a clear visual hierarchy.
- **Body Text**: Maintain high contrast (WCAG AA compliant) for readability.
- **Status Indicators**: Use distinct font weights or colors to highlight application statuses (e.g., "Pending", "Approved", "Action Required").

### Color Palette (Dashboard Specific)
- **Primary Action Color**: Use the brand primary color for "Submit" or "Update" buttons.
- **Success/Positive**: Green tones for completed milestones.
- **Warning/Attention**: Amber/Yellow for pending actions.
- **Error/Critical**: Red tones for missing requirements or rejected items.

### Components
- **Forms**: Input fields should have clear labels and validation states (error/success).
- **Buttons**: 
    - Primary: Solid fill for the main action.
    - Secondary: Outlined for alternative actions.
- **Tables/Lists**: Use zebra-striping or hover effects for data-heavy lists to improve scannability.

### Responsiveness
- **Mobile First**: The dashboard must be fully responsive, collapsing sidebars into hamburger menus on screens smaller than 768px.
- **Touch Targets**: Ensure all interactive elements have a minimum size of 44x44px for mobile accessibility.
