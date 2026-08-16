import { Badge } from "../ui/Badge";
import { MARKETPLACE_LABELS } from "@/lib/constants";
import { capitalizeMarketplace } from "@/features/labelsort/utils/formatters";
import { ShoppingBag } from "lucide-react";

export function MarketplaceBadge({
  marketplace = "meesho",
  className,
}: {
  marketplace?: string | null;
  className?: string;
}) {
  const normalized = (marketplace || "meesho").toLowerCase();
  const config = MARKETPLACE_LABELS[normalized] || {
    name: capitalizeMarketplace(marketplace),
    color: "#6366F1",
    bg: "rgba(99, 102, 241, 0.1)",
  };

  return (
    <Badge
      variant="outline"
      size="default"
      className={className}
      style={{
        borderColor: `${config.color}40`,
        backgroundColor: config.bg,
        color: config.color,
      }}
    >
      <ShoppingBag className="h-3.5 w-3.5 mr-1" />
      <span className="font-bold">{config.name}</span>
    </Badge>
  );
}
