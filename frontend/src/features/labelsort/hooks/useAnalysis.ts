import { useQuery } from "@tanstack/react-query";
import { labelsortApi } from "../api/labelsortApi";
import { AnalysisResult } from "@/types";

export function useAnalysis(jobId?: string) {
  const query = useQuery<AnalysisResult, Error>({
    queryKey: ["analysis", jobId],
    queryFn: () => {
      if (!jobId) throw new Error("Job ID is required");
      return labelsortApi.getAnalysis(jobId);
    },
    enabled: !!jobId,
    staleTime: 60000,
  });

  return query;
}
