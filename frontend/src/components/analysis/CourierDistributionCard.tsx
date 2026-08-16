import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { Truck } from "lucide-react";

export interface CourierDistributionCardProps {
  courierStats?: Record<string, number>;
  totalLabels: number;
}

export function CourierDistributionCard({
  courierStats = {},
  totalLabels,
}: CourierDistributionCardProps) {
  const entries = Object.entries(courierStats).sort((a, b) => b[1] - a[1]);

  if (entries.length === 0) return null;

  return (
    <Card className="border-border/80">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base flex items-center gap-2">
            <Truck className="h-4 w-4 text-primary" />
            <span>Courier Partner Distribution</span>
          </CardTitle>
          <span className="text-xs font-semibold text-muted-foreground">
            {entries.length} Couriers
          </span>
        </div>
      </CardHeader>

      <CardContent className="space-y-3.5">
        {entries.map(([courier, count]) => {
          const percent = totalLabels > 0 ? Math.round((count / totalLabels) * 100) : 0;
          return (
            <div key={courier} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-foreground">{courier}</span>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-muted-foreground">
                    {count} {count === 1 ? "label" : "labels"}
                  </span>
                  <span className="font-bold text-primary">{percent}%</span>
                </div>
              </div>
              {/* Distribution bar */}
              <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary rounded-full transition-all duration-500"
                  style={{ width: `${percent}%` }}
                />
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
