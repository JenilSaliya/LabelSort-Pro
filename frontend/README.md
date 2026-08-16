# LabelSort Pro — Frontend

> **Smart Label Sorting for E-commerce Sellers**  
> *Sort Hundreds of Shipping Labels in Seconds*

LabelSort Pro is a modern, high-performance web application designed for e-commerce sellers to upload shipping label PDFs, automatically extract marketplace & courier metadata, visually configure multi-tiered sorting rules (Courier Priority, SKU, Size), and generate clean print-ready sorted PDFs alongside companion Excel statistics.

---

## 🛠️ Technology Stack

- **Framework**: [React 18](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) + [Vite](https://vitejs.dev/)
- **Routing**: [React Router v7](https://reactrouter.com/)
- **State & Server Cache**: [TanStack Query v5](https://tanstack.com/query/latest)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) with centralized CSS theme tokens
- **Drag & Drop**: [@dnd-kit/core](https://dndkit.com/) + [@dnd-kit/sortable](https://dndkit.com/)
- **Icons & Visuals**: [Lucide Icons](https://lucide.dev/) + [Framer Motion](https://www.framer.com/motion/)
- **HTTP Client**: Typed [Axios](https://axios-http.com/) wrapper with progress events & error parsing
- **Notifications**: [Sonner](https://sonner.emilkowal.ski/) toast system

---

## 🚀 Quick Start

### 1. Prerequisites
- Node.js `v18+` or `v20+` / `v22+`
- LabelSort FastAPI backend running on `http://localhost:8000`

### 2. Installation
```bash
cd frontend
npm install
```

### 3. Environment Configuration
Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```
Default configuration:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Run Development Server
```bash
npm run dev
```
The application will be accessible at: `http://localhost:5173`

### 5. Build for Production
```bash
npm run build
```

---

## 📂 Project Architecture

```
frontend/src/
├── app/
│   ├── providers/              # ThemeProvider (Light/Dark/System), QueryProvider, Toaster
│   ├── router/                 # AppRouter with public landing & app workspace routes
│   └── App.tsx                 # Root application wrapper
│
├── components/
│   ├── ui/                     # Reusable design primitives (Button, Card, Badge, Modal, Tabs, Progress, Skeleton, Tooltip)
│   ├── layout/                 # AppShell, Topbar, Sidebar (desktop & mobile drawer), ThemeToggle, Footer
│   ├── upload/                 # UploadDropzone (drag-and-drop, 100MB limit, PDF validation), FileList, UploadProgressCard
│   ├── processing/             # ProcessingTimeline, ProcessingStageItem
│   ├── sorting/                # SortableFieldList, CourierPriorityList (@dnd-kit), SortDirectionToggle, ConfirmSortingModal
│   ├── analysis/               # AnalysisSummary, MarketplaceBadge, FieldStatisticsCard, CourierDistributionCard
│   ├── results/                # DownloadActions, ResultCard, PdfViewer, PdfPreviewModal
│   └── common/                 # PageHeader, StatCard, EmptyState, ErrorState, LoadingState, ComingSoonBadge
│
├── features/labelsort/
│   ├── api/                    # labelsortApi.ts: typed API methods for all FastAPI endpoints
│   ├── hooks/                  # useJob, useAnalysis, useSortingConfig, useProcessJob
│   ├── types/                  # Typed request/response models
│   └── utils/                  # downloadUtils (Blob download helper), formatters (bytes, dates, marketplace names)
│
├── pages/
│   ├── LandingPage.tsx         # High-converting SaaS landing page with interactive demo & roadmap
│   ├── WorkspacePage.tsx       # Session router
│   ├── UploadPage.tsx          # Multi-file PDF upload dropzone with upload progress
│   ├── AnalysisPage.tsx        # Deep label analytics (SKUs, courier distribution, size metrics)
│   ├── SortingPage.tsx         # Flagship drag-and-drop sorting & courier priority screen
│   ├── ResultPage.tsx          # Sorted PDF download, Excel export, and in-browser preview
│   ├── PreviewPage.tsx         # Fullscreen PDF inspection
│   ├── HistoryComingSoonPage.tsx
│   ├── AnalyticsComingSoonPage.tsx
│   ├── SettingsComingSoonPage.tsx
│   └── NotFoundPage.tsx
│
├── styles/
│   └── index.css               # Theme tokens, custom glassmorphism, and scrollbars
└── main.tsx
```

---

## 🔗 Connected Backend APIs

All API interactions map directly to the existing FastAPI backend routes:

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/health/` | Health check & connectivity indicator |
| `POST` | `/upload/` | Multi-file PDF upload with integrity check & automatic merge |
| `GET` | `/job/{job_id}` | Retrieve job metadata and processing status |
| `GET` | `/job/{job_id}/analysis` | Retrieve extracted SKUs, courier distribution, and size data |
| `GET` | `/jobs/{job_id}/sorting-options`| Retrieve sortable fields and courier priority options |
| `POST` | `/process/{job_id}` | Execute label sorting with specified hierarchy & courier order |
| `GET` | `/job/{job_id}/download` | Download reordered sorted PDF (`application/pdf`) |
| `GET` | `/job/{job_id}/statistics` | Download Excel statistics report (`.xlsx`) |
| `GET` | `/job/{job_id}/preview` | In-browser PDF stream preview |

---

## 🎨 Theme & Accessibility
- **Light & Dark Mode**: Persistent theme toggle supporting system preferences and CSS variable design tokens.
- **Accessibility**: Keyboard navigable drag-and-drop reordering with accessible button alternatives for mobile/screen readers, ARIA roles, and high-contrast status badges.
- **Responsive**: Fully responsive across mobile (320px+), tablet, and desktop (1920px+).

---

## 🗺️ Roadmap
- [x] Meesho shipping label auto-detection, parsing, and sorting
- [x] Multi-PDF merging & single-batch workflow
- [x] Multi-level drag-and-drop sorting (Courier $\rightarrow$ SKU $\rightarrow$ Size)
- [x] Vector PDF generation with high-resolution barcode preservation
- [x] Excel statistics export
- [ ] Flipkart Smart & Non-Smart label sorting
- [ ] Amazon Easy Ship ATS slot sorting
- [ ] Persistent user authentication & multi-tenant history
- [ ] Direct WMS / ERP Webhook API keys
