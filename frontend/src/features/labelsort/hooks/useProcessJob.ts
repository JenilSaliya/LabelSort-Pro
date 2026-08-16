import { useMutation, useQueryClient } from "@tanstack/react-query";
import { labelsortApi } from "../api/labelsortApi";
import { ProcessRequest, ApiResponse, ProcessResultData } from "@/types";

export function useProcessJob(jobId: string) {
  const queryClient = useQueryClient();

  return useMutation<ApiResponse<ProcessResultData>, Error, ProcessRequest>({
    mutationFn: (payload: ProcessRequest) => {
      return labelsortApi.processJob(jobId, payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["job", jobId] });
    },
  });
}
