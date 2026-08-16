import { Link } from "react-router-dom";
import { Layers, Heart } from "lucide-react";
import { APP_ROUTES } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="w-full border-t border-border/70 bg-card text-muted-foreground transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Col */}
          <div className="space-y-4 md:col-span-1">
            <Link to={APP_ROUTES.HOME} className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-xl bg-primary flex items-center justify-center text-white shadow-sm">
                <Layers className="h-4 w-4" />
              </div>
              <span className="font-bold text-lg text-foreground">
                Label<span className="text-primary">Sort</span> Pro
              </span>
            </Link>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Smart shipping label sorting, merging, and intelligence for e-commerce sellers.
            </p>
          </div>

          {/* Product links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-foreground">
              Product
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to={APP_ROUTES.UPLOAD} className="hover:text-foreground transition-colors">
                  Upload & Sort Labels
                </Link>
              </li>
              <li>
                <Link to={APP_ROUTES.HOME} className="hover:text-foreground transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <span className="text-muted-foreground/60">Meesho Cropper & Sorter</span>
              </li>
            </ul>
          </div>

          {/* Roadmap links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-foreground">
              Roadmap
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to={APP_ROUTES.HISTORY} className="hover:text-foreground transition-colors">
                  Sorting History
                </Link>
              </li>
              <li>
                <Link to={APP_ROUTES.ANALYTICS} className="hover:text-foreground transition-colors">
                  Label Analytics
                </Link>
              </li>
              <li>
                <Link to={APP_ROUTES.SETTINGS} className="hover:text-foreground transition-colors">
                  Custom Sorter Rules
                </Link>
              </li>
            </ul>
          </div>

          {/* Marketplaces */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-foreground">
              Marketplaces
            </h4>
            <ul className="space-y-2 text-xs">
              <li className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-medium">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                Meesho (Supported)
              </li>
              <li className="text-muted-foreground/60">Flipkart (Coming Soon)</li>
              <li className="text-muted-foreground/60">Amazon Easy Ship (Coming Soon)</li>
              <li className="text-muted-foreground/60">Shopify (Coming Soon)</li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-border/50 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
          <p>© {new Date().getFullYear()} LabelSort Pro. All rights reserved.</p>
          <p className="flex items-center gap-1">
            Built for e-commerce efficiency <Heart className="h-3.5 w-3.5 text-rose-500 fill-rose-500 inline" />
          </p>
        </div>
      </div>
    </footer>
  );
}
