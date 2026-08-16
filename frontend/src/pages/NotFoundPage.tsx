import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { APP_ROUTES } from "@/lib/constants";
import { FileQuestion, ArrowLeft, Home } from "lucide-react";

export function NotFoundPage() {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center p-6 text-center">
      <div className="p-4 rounded-3xl bg-secondary text-primary mb-4 shadow-sm">
        <FileQuestion className="h-12 w-12" />
      </div>
      <h1 className="text-3xl font-extrabold text-foreground mb-2">
        Page Not Found
      </h1>
      <p className="text-sm text-muted-foreground max-w-sm mb-6 leading-relaxed">
        The page or sorting session you are looking for does not exist, has expired, or has moved.
      </p>
      <div className="flex items-center gap-3">
        <Link to={APP_ROUTES.HOME}>
          <Button variant="outline" leftIcon={<Home className="h-4 w-4" />}>
            Home
          </Button>
        </Link>
        <Link to={APP_ROUTES.UPLOAD}>
          <Button variant="glow" leftIcon={<ArrowLeft className="h-4 w-4" />}>
            Start New Job
          </Button>
        </Link>
      </div>
    </div>
  );
}
