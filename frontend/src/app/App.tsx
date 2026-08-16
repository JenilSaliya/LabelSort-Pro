import { AppProviders } from "./providers";
import { AppRouter } from "./router/AppRouter";

export function App() {
  return (
    <AppProviders>
      <AppRouter />
    </AppProviders>
  );
}

export default App;
