# Team Codezilla - Urban Flood Risk Analytics Portal

A beautiful landing page with animated background that leads to the Urban Flood Risk Analytics Streamlit dashboard.

## Features

- ✨ Animated background using UnicornStudio React
- 🎨 Beautiful fade-in animations
- 🔤 Custom Google Fonts (Bricolage Grotesque, Darker Grotesque, Montserrat, Poppins)
- 📱 Fully responsive design
- 🎯 Direct navigation to dashboard
- ⚡ Built with Next.js 14, TypeScript, and Tailwind CSS
- 🎨 shadcn/ui components

## Project Structure

```
src/
├── app/
│   ├── dashboard/          # Full-screen Streamlit iframe
│   │   └── page.tsx
│   ├── globals.css         # Global styles and Tailwind
│   ├── layout.tsx          # Root layout with Google Fonts
│   └── page.tsx           # Landing page with animations
├── components/
│   ├── ui/
│   │   ├── button.tsx      # shadcn/ui Button component
│   │   └── open-ai-codex-animated-background.tsx  # Animated background
│   └── demo.tsx           # Demo component
└── lib/
    └── utils.ts           # Utility functions
```

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the landing page.

### Routes

- `/` - Landing page with animated background and "Team Codezilla" branding
- `/dashboard` - Full-screen iframe displaying the Streamlit dashboard

## Components

### Animated Background Component
Located at `src/components/ui/open-ai-codex-animated-background.tsx`

- Uses UnicornStudio React for animations
- Responsive window sizing
- Project ID: `1grEuiVDSVmyvEMAYhA6`

### Landing Page Features
- Fade-in animation on page load
- Square container showcasing the animation
- Team Codezilla branding with custom fonts
- Call-to-action button leading to dashboard

## Technologies Used

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality component library
- **UnicornStudio React** - Interactive animations
- **Google Fonts** - Typography

## Fonts

The project includes four Google Fonts:
- Bricolage Grotesque (primary)
- Darker Grotesque
- Montserrat
- Poppins

Use CSS classes: `.font-bricolage`, `.font-darker-grotesque`, `.font-montserrat`, `.font-poppins`

## Deployment

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Integration with Streamlit Dashboard

The dashboard route (`/dashboard`) displays the Streamlit app at:
`https://urban-flood-analytics.streamlit.app/`

This provides a seamless transition from the landing page to the analytics dashboard.

## Team

**Team Codezilla**
- Nikhil Sharma
- Shwetank Pandey  
- Rayyan Khan

Built for Deep Data Hackathon 2.0
