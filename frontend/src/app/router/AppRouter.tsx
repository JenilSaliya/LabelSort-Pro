import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { LandingPage } from "@/pages/LandingPage";
import { WorkspacePage } from "@/pages/WorkspacePage";
import { UploadPage } from "@/pages/UploadPage";
import { AnalysisPage } from "@/pages/AnalysisPage";
import { SortingPage } from "@/pages/SortingPage";
import { ResultPage } from "@/pages/ResultPage";
import { PreviewPage } from "@/pages/PreviewPage";
import { HistoryComingSoonPage } from "@/pages/HistoryComingSoonPage";
import { AnalyticsComingSoonPage } from "@/pages/AnalyticsComingSoonPage";
import { SettingsComingSoonPage } from "@/pages/SettingsComingSoonPage";
import { NotFoundPage } from "@/pages/NotFoundPage";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Landing Page */}
        <Route path="/" element={<LandingPage />} />

        {/* App / Workspace Shell */}
        <Route path="/app" element={<AppShell />}>
          <Route index element={<WorkspacePage />} />
          <Route path="upload" element={<UploadPage />} />
          <Route path="job/:jobId" element={<SortingPage />} />
          <Route path="job/:jobId/analysis" element={<AnalysisPage />} />
          <Route path="job/:jobId/sort" element={<SortingPage />} />
          <Route path="job/:jobId/result" element={<ResultPage />} />
          <Route path="job/:jobId/preview" element={<PreviewPage />} />
          <Route path="history" element={<HistoryComingSoonPage />} />
          <Route path="analytics" element={<AnalyticsComingSoonPage />} />
          <Route path="settings" element={<SettingsComingSoonPage />} />
          <Route path="api-docs" element={<SettingsComingSoonPage />} />
        </Route>

        {/* 404 Catch-All */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
