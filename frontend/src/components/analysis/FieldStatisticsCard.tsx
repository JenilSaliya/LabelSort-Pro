import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { Search, ChevronDown, ChevronUp, Tag } from "lucide-react";

export interface FieldStatisticsCardProps {
  title: string;
  fieldId: string;
  values: Record<string, number>;
  totalLabels: number;
}

export function FieldStatisticsCard({
  title,
  fieldId,
  values,
  totalLabels,
}: FieldStatisticsCardProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);

  const sortedEntries = Object.entries(values).sort((a, b) => b[1] - a[1]);
  const filteredEntries = sortedEntries.filter(([key]) =>
    key.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const displayedEntries = isExpanded ? filteredEntries : filteredEntries.slice(0, 8);

  return (
    <Card className="border-border/80">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base flex items-center gap-2">
            <Tag className="h-4 w-4 text-primary" />
            <span>{title} Breakdown</span>
          </CardTitle>
          <Badge variant="secondary" size="sm">
            {sortedEntries.length} Unique
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Search input if more than 6 entries */}
        {sortedEntries.length > 6 && (
          <div className="relative">
            <Search className="h-3.5 w-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder={`Search ${title.toLowerCase()}...`}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 text-xs rounded-xl bg-secondary/70 border border-border/60 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
        )}

        {/* Item List */}
        <div className="space-y-1.5">
          {displayedEntries.length === 0 ? (
            <p className="text-xs text-muted-foreground py-2 text-center">
              No matching values found.
            </p>
          ) : (
            displayedEntries.map(([name, count]) => {
              const percentage =
                totalLabels > 0 ? Math.round((count / totalLabels) * 100) : 0;
              return (
                <div
                  key={name}
                  className="flex items-center justify-between p-2 rounded-xl bg-secondary/40 hover:bg-secondary/70 transition-colors text-xs"
                >
                  <span className="font-medium text-foreground truncate max-w-[200px] sm:max-w-[250px]">
                    {name || "(Empty)"}
                  </span>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className="font-mono text-muted-foreground">
                      {count}
                    </span>
                    <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-primary/10 text-primary">
                      {percentage}%
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Expand / Collapse Button */}
        {filteredEntries.length > 8 && (
          <button
            type="button"
            onClick={() => setIsExpanded((prev) => !prev)}
            className="w-full py-1.5 text-xs font-semibold text-primary hover:text-primary/80 transition-colors flex items-center justify-center gap-1"
          >
            {isExpanded ? (
              <>
                <ChevronUp className="h-3.5 w-3.5" />
                <span>Show Less</span>
              </>
            ) : (
              <>
                <ChevronDown className="h-3.5 w-3.5" />
                <span>View All ({filteredEntries.length})</span>
              </>
            )}
          </button>
        )}
      </CardContent>
    </Card>
  );
}
