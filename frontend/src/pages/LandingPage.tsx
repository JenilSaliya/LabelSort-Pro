import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  UploadCloud,
  FileSpreadsheet,
  ArrowRight,
  CheckCircle2,
  Layers,
  Sparkles,
  Zap,
  ShieldCheck,
  Truck,
  Scissors,
  Check,
  ChevronRight,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ThemeToggle } from "@/components/layout/ThemeToggle";
import { Footer } from "@/components/layout/Footer";
import { APP_ROUTES } from "@/lib/constants";

export function LandingPage() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<"sku" | "courier">("sku");

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground selection:bg-primary/20 selection:text-primary">
      {/* Navigation Bar */}
      <header className="sticky top-0 z-50 w-full border-b border-border/60 bg-card/85 backdrop-blur-md">
        <div className="max-w-7xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link to={APP_ROUTES.HOME} className="flex items-center gap-2.5 group">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-primary to-indigo-500 flex items-center justify-center text-white shadow-md shadow-primary/20 group-hover:scale-105 transition-transform">
              <Layers className="h-5 w-5" />
            </div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-xl tracking-tight text-foreground">
                Label<span className="text-primary">Sort</span>
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
                PRO
              </span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
            <a href="#how-it-works" className="hover:text-foreground transition-colors">
              How It Works
            </a>
            <a href="#benefits" className="hover:text-foreground transition-colors">
              Benefits
            </a>
            <a href="#marketplaces" className="hover:text-foreground transition-colors">
              Marketplaces
            </a>
            <a href="#workflow-demo" className="hover:text-foreground transition-colors">
              Interactive Demo
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <ThemeToggle />
            <Link to={APP_ROUTES.UPLOAD}>
              <Button
                variant="glow"
                size="default"
                rightIcon={<ArrowRight className="h-4 w-4" />}
              >
                Start Sorting
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 md:pt-20 md:pb-28 border-b border-border/50">
        {/* Subtle decorative background glow */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-primary/15 dark:bg-primary/20 blur-[120px] rounded-full pointer-events-none -z-10" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-primary/10 text-primary border border-primary/20 text-xs font-semibold animate-in fade-in duration-300">
              <Sparkles className="h-3.5 w-3.5" />
              <span>Smart Label Sorting for E-commerce Sellers</span>
            </div>

            <h1 className="text-4xl sm:text-5xl md:text-6xl font-black tracking-tight text-foreground leading-[1.1]">
              Sort Hundreds of Shipping Labels in{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-indigo-500 to-indigo-600">
                Seconds
              </span>
            </h1>

            <p className="text-base sm:text-lg md:text-xl text-muted-foreground leading-relaxed max-w-2xl mx-auto">
              Stop manually searching through messy label PDFs. LabelSort automatically extracts Meesho labels, sorts by Courier Partner & SKU, and exports print-ready PDFs with Excel analytics.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 pt-2">
              <Button
                variant="glow"
                size="xl"
                className="w-full sm:w-auto shadow-lg shadow-primary/25"
                onClick={() => navigate(APP_ROUTES.UPLOAD)}
                leftIcon={<UploadCloud className="h-5 w-5" />}
                rightIcon={<ArrowRight className="h-5 w-5" />}
              >
                Upload Labels Now — Free
              </Button>
              <a href="#how-it-works">
                <Button variant="outline" size="xl" className="w-full sm:w-auto">
                  See How It Works
                </Button>
              </a>
            </div>

            {/* Micro proof badges */}
            <div className="flex flex-wrap items-center justify-center gap-6 pt-4 text-xs font-medium text-muted-foreground">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                No Login Required
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                Multi-PDF Merge
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                Courier Handover Priority
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                Excel Report Included
              </span>
            </div>
          </div>

          {/* Interactive Hero Visual */}
          <div className="mt-14 max-w-5xl mx-auto">
            <div className="relative rounded-3xl border border-border/80 bg-card p-4 sm:p-6 shadow-2xl shadow-primary/10">
              <div className="flex items-center justify-between pb-4 border-b border-border/60 text-xs">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-rose-500" />
                  <div className="h-3 w-3 rounded-full bg-amber-500" />
                  <div className="h-3 w-3 rounded-full bg-emerald-500" />
                  <span className="font-mono text-muted-foreground ml-2">
                    labelsort-pipeline-preview
                  </span>
                </div>
                <Badge variant="success" size="sm">
                  Live Engine
                </Badge>
              </div>

              {/* Visual Pipeline Flow */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-6">
                {/* Step 1 */}
                <div className="p-4 rounded-2xl bg-secondary/60 border border-border/60 flex flex-col items-center text-center space-y-2">
                  <div className="p-3 rounded-xl bg-primary/10 text-primary">
                    <UploadCloud className="h-6 w-6" />
                  </div>
                  <h4 className="text-sm font-bold text-foreground">1. Upload Batch</h4>
                  <p className="text-xs text-muted-foreground">
                    Multiple messy PDF label files
                  </p>
                </div>

                {/* Step 2 */}
                <div className="p-4 rounded-2xl bg-secondary/60 border border-border/60 flex flex-col items-center text-center space-y-2">
                  <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">
                    <Zap className="h-6 w-6" />
                  </div>
                  <h4 className="text-sm font-bold text-foreground">2. Deep Extract</h4>
                  <p className="text-xs text-muted-foreground">
                    Auto-detect SKU, courier & size
                  </p>
                </div>

                {/* Step 3 */}
                <div className="p-4 rounded-2xl bg-secondary/60 border border-border/60 flex flex-col items-center text-center space-y-2">
                  <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                    <Truck className="h-6 w-6" />
                  </div>
                  <h4 className="text-sm font-bold text-foreground">3. Sort & Prioritize</h4>
                  <p className="text-xs text-muted-foreground">
                    Valmo $\rightarrow$ Delhivery $\rightarrow$ Shadowfax
                  </p>
                </div>

                {/* Step 4 */}
                <div className="p-4 rounded-2xl bg-secondary/60 border border-border/60 flex flex-col items-center text-center space-y-2">
                  <div className="p-3 rounded-xl bg-primary text-white shadow-sm">
                    <FileSpreadsheet className="h-6 w-6" />
                  </div>
                  <h4 className="text-sm font-bold text-foreground">4. Print & Export</h4>
                  <p className="text-xs text-muted-foreground">
                    Reordered PDF + Excel sheets
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-muted/20 border-b border-border/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-primary">
              Streamlined Workflow
            </h2>
            <h3 className="text-3xl font-extrabold text-foreground tracking-tight">
              From Chaos to Print-Ready in 4 Steps
            </h3>
            <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
              Designed specifically to save hours every day for warehouse packing teams.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Card 1 */}
            <Card className="p-6 border-border/80 relative">
              <div className="h-8 w-8 rounded-full bg-primary text-white font-extrabold text-sm flex items-center justify-center mb-4 shadow-sm">
                1
              </div>
              <h4 className="text-lg font-bold text-foreground mb-2">
                Upload Label PDFs
              </h4>
              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                Drag and drop your Meesho shipping label PDFs. You can upload multiple files at once — LabelSort merges and processes them into a single batch automatically.
              </p>
            </Card>

            {/* Card 2 */}
            <Card className="p-6 border-border/80 relative">
              <div className="h-8 w-8 rounded-full bg-primary text-white font-extrabold text-sm flex items-center justify-center mb-4 shadow-sm">
                2
              </div>
              <h4 className="text-lg font-bold text-foreground mb-2">
                Choose Sorting & Courier Rules
              </h4>
              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                Reorder courier partner handover sequence (Valmo, Delhivery, Shadowfax, Xpressbees) and group by SKU so your packing team picks all identical items together.
              </p>
            </Card>

            {/* Card 3 */}
            <Card className="p-6 border-border/80 relative">
              <div className="h-8 w-8 rounded-full bg-primary text-white font-extrabold text-sm flex items-center justify-center mb-4 shadow-sm">
                3
              </div>
              <h4 className="text-lg font-bold text-foreground mb-2">
                Preview & Download
              </h4>
              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                Inspect the reordered labels in the built-in PDF viewer, download your print-ready sorted PDF, and export a clean Excel summary with SKU counts.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Key Benefits Section */}
      <section id="benefits" className="py-20 border-b border-border/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-primary">
              Why E-commerce Sellers Choose LabelSort
            </h2>
            <h3 className="text-3xl font-extrabold text-foreground tracking-tight">
              Engineered for Speed, Accuracy & Zero Waste
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="p-6 border-border/80 hoverLift">
              <div className="p-3 rounded-xl bg-primary/10 text-primary w-fit mb-4">
                <Truck className="h-6 w-6" />
              </div>
              <h4 className="text-base font-bold text-foreground mb-2">
                Courier Handover Priority
              </h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Separate Delhivery, Xpressbees, Shadowfax, and Valmo into distinct sequential stacks for ultra-fast pickup handovers.
              </p>
            </Card>

            <Card className="p-6 border-border/80 hoverLift">
              <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 w-fit mb-4">
                <Layers className="h-6 w-6" />
              </div>
              <h4 className="text-base font-bold text-foreground mb-2">
                SKU Batch Packing
              </h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Group all orders of the same product together so your team packs 20 units of SKU A in one go without walking back and forth.
              </p>
            </Card>

            <Card className="p-6 border-border/80 hoverLift">
              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 w-fit mb-4">
                <FileSpreadsheet className="h-6 w-6" />
              </div>
              <h4 className="text-base font-bold text-foreground mb-2">
                Automated Excel Reports
              </h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Instantly download a companion spreadsheet detailing exact quantity counts per SKU, size distributions, and courier counts.
              </p>
            </Card>

            <Card className="p-6 border-border/80 hoverLift">
              <div className="p-3 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 w-fit mb-4">
                <UploadCloud className="h-6 w-6" />
              </div>
              <h4 className="text-base font-bold text-foreground mb-2">
                Multi-Account & Multi-PDF
              </h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Upload batches from multiple supplier accounts simultaneously. LabelSort combines and optimizes them seamlessly.
              </p>
            </Card>

            <Card className="p-6 border-border/80 hoverLift">
              <div className="p-3 rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 w-fit mb-4">
                <Scissors className="h-6 w-6" />
              </div>
              <h4 className="text-base font-bold text-foreground mb-2">
                Print Quality & Page Safety
              </h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Preserves vector barcodes and text sharpness so thermal barcode scanners read labels effortlessly on first attempt.
              </p>
            </Card>

            <Card className="p-6 border-border/80 hoverLift">
              <div className="p-3 rounded-xl bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 w-fit mb-4">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <h4 className="text-base font-bold text-foreground mb-2">
                Safe & Private Processing
              </h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Temporary session storage with automatic scheduled cleanup. Your customer data is never permanently stored or shared.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Interactive Workflow Demo Section */}
      <section id="workflow-demo" className="py-20 bg-muted/20 border-b border-border/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12 space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-primary">
              Interactive Preview
            </h2>
            <h3 className="text-3xl font-extrabold text-foreground tracking-tight">
              See How Sorting Transforms Packing
            </h3>
          </div>

          <div className="max-w-4xl mx-auto">
            <Card className="p-6 border-border/80 shadow-card">
              <div className="flex items-center justify-between pb-4 mb-6 border-b border-border/60">
                <div className="flex items-center gap-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                    Strategy Mode:
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setActiveTab("sku")}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        activeTab === "sku"
                          ? "bg-primary text-white shadow-sm"
                          : "bg-secondary text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      SKU Grouping
                    </button>
                    <button
                      type="button"
                      onClick={() => setActiveTab("courier")}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        activeTab === "courier"
                          ? "bg-primary text-white shadow-sm"
                          : "bg-secondary text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      Courier Priority
                    </button>
                  </div>
                </div>
                <Badge variant="outline" size="sm">
                  Simulated 248 Labels
                </Badge>
              </div>

              {activeTab === "sku" ? (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 animate-in fade-in">
                  <div className="p-4 rounded-xl border border-border/80 bg-secondary/40 space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-primary">SKU: TS-COTTON-BLK-M</span>
                      <span className="font-mono">42 labels</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Pages 1 to 42 • Printed sequentially for picking bin 01
                    </p>
                  </div>
                  <div className="p-4 rounded-xl border border-border/80 bg-secondary/40 space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-primary">SKU: DR-SILK-BLU-L</span>
                      <span className="font-mono">28 labels</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Pages 43 to 70 • Printed sequentially for picking bin 02
                    </p>
                  </div>
                  <div className="p-4 rounded-xl border border-border/80 bg-secondary/40 space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-primary">SKU: JN-DENIM-SLM-32</span>
                      <span className="font-mono">19 labels</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Pages 71 to 89 • Printed sequentially for picking bin 03
                    </p>
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 animate-in fade-in">
                  <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/5 space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-emerald-600 dark:text-emerald-400">
                        #1 Valmo Logistics
                      </span>
                      <span className="font-mono">124 labels</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Early morning pickup stack ready first
                    </p>
                  </div>
                  <div className="p-4 rounded-xl border border-border/80 bg-secondary/40 space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-foreground">#2 Delhivery</span>
                      <span className="font-mono">76 labels</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Afternoon pickup stack
                    </p>
                  </div>
                  <div className="p-4 rounded-xl border border-border/80 bg-secondary/40 space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-foreground">#3 Shadowfax</span>
                      <span className="font-mono">48 labels</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Evening pickup stack
                    </p>
                  </div>
                </div>
              )}
            </Card>
          </div>
        </div>
      </section>

      {/* Marketplaces Roadmap */}
      <section id="marketplaces" className="py-20 border-b border-border/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12 space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-primary">
              Marketplace Coverage
            </h2>
            <h3 className="text-3xl font-extrabold text-foreground tracking-tight">
              Supported Marketplaces & Roadmap
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            {/* Meesho */}
            <Card className="p-6 border-emerald-500/40 bg-card relative">
              <div className="flex items-center justify-between mb-4">
                <span className="font-extrabold text-lg text-foreground">
                  Meesho
                </span>
                <Badge variant="success" size="sm">
                  Active MVP
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Full support for Meesho tax-invoice labels, courier detection (Valmo, Delhivery, Shadowfax, Xpressbees), SKU parsing & statistics.
              </p>
            </Card>

            {/* Flipkart */}
            <Card className="p-6 border-border/80 bg-card/60 relative">
              <div className="flex items-center justify-between mb-4">
                <span className="font-bold text-lg text-muted-foreground">
                  Flipkart
                </span>
                <Badge variant="secondary" size="sm">
                  Coming Soon
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Flipkart Smart and Non-Smart shipping labels with Ekart barcode sorting.
              </p>
            </Card>

            {/* Amazon */}
            <Card className="p-6 border-border/80 bg-card/60 relative">
              <div className="flex items-center justify-between mb-4">
                <span className="font-bold text-lg text-muted-foreground">
                  Amazon Easy Ship
                </span>
                <Badge variant="secondary" size="sm">
                  Coming Soon
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Amazon ATS label support and slot-based handover sorting.
              </p>
            </Card>

            {/* Shopify */}
            <Card className="p-6 border-border/80 bg-card/60 relative">
              <div className="flex items-center justify-between mb-4">
                <span className="font-bold text-lg text-muted-foreground">
                  Shopify / D2C
                </span>
                <Badge variant="secondary" size="sm">
                  Coming Soon
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Custom Shiprocket, NimbusPost, and iThink Logistics label parsing.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="py-20 relative overflow-hidden">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-foreground tracking-tight">
            Ready to Sort Your Labels in Seconds?
          </h2>
          <p className="text-base text-muted-foreground max-w-xl mx-auto leading-relaxed">
            Upload your shipping label PDF now and prepare a clean, organized print-ready file with instant Excel statistics.
          </p>
          <div className="pt-2">
            <Link to={APP_ROUTES.UPLOAD}>
              <Button
                variant="glow"
                size="xl"
                className="shadow-xl shadow-primary/30"
                leftIcon={<UploadCloud className="h-6 w-6" />}
                rightIcon={<ArrowRight className="h-5 w-5" />}
              >
                Upload Labels Now
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
