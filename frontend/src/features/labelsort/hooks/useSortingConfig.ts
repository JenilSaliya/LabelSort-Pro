import { useQuery } from "@tanstack/react-query";
import { labelsortApi } from "../api/labelsortApi";
import { SortingConfigResponse } from "@/types";

export function useSortingConfig(jobId?: string) {
  return useQuery<SortingConfigResponse, Error>({
    queryKey: ["sorting-config", jobId],
    queryFn: () => {
      if (!jobId) throw new Error("Job ID is required");
      return labelsortApi.getSortingOptions(jobId);
    },
    enabled: !!jobId,
    staleTime: 60000,
  });
}
