import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { APP_ROUTES } from "@/lib/constants";

export function WorkspacePage() {
  const navigate = useNavigate();

  useEffect(() => {
    const activeJobId = sessionStorage.getItem("labelsort_active_job_id");
    if (activeJobId) {
      navigate(APP_ROUTES.SORT(activeJobId), { replace: true });
    } else {
      navigate(APP_ROUTES.UPLOAD, { replace: true });
    }
  }, [navigate]);

  return null;
}
