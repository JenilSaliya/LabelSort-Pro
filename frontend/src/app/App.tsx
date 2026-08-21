import { AppProviders } from "./providers";
import { AppRouter } from "./router/AppRouter";
import { useDesktopUpdater } from "@/features/desktop/useDesktopUpdater";

export function App() {
  useDesktopUpdater();

  return (
    <AppProviders>
      <AppRouter />
    </AppProviders>
  );
}

export default App;
