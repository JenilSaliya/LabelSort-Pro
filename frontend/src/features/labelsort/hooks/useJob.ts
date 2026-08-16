import { useQuery } from "@tanstack/react-query";
import { labelsortApi } from "../api/labelsortApi";
import { JobMetadata } from "@/types";

export function useJob(jobId?: string) {
  const query = useQuery<JobMetadata, Error>({
    queryKey: ["job", jobId],
    queryFn: () => {
      if (!jobId) throw new Error("Job ID is required");
      return labelsortApi.getJob(jobId);
    },
    enabled: !!jobId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === "sorting" || data?.status === "processing") {
        return 1500;
      }
      return false;
    },
    staleTime: 5000,
  });

  return query;
}
