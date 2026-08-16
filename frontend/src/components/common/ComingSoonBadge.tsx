import { Badge } from "../ui/Badge";
import { Sparkles } from "lucide-react";

export function ComingSoonBadge({ text = "Coming Soon" }: { text?: string }) {
  return (
    <Badge
      variant="secondary"
      size="sm"
      className="bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20 text-[10px] uppercase font-bold tracking-wider"
    >
      <Sparkles className="h-2.5 w-2.5 mr-0.5 inline-block" />
      {text}
    </Badge>
  );
}
