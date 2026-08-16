export interface SavedSortingPreferences {
  fieldIds?: string[];
  courierPriority?: string[];
  reverse?: boolean;
  includeExcelReport?: boolean;
}

const STORAGE_KEY = "labelsort_saved_sorting_rules";

export const storageUtils = {
  getSavedPreferences(): SavedSortingPreferences | null {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      if (!data) return null;
      return JSON.parse(data) as SavedSortingPreferences;
    } catch {
      return null;
    }
  },

  savePreferences(prefs: SavedSortingPreferences): void {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
    } catch (e) {
      console.warn("Failed to save sorting preferences to localStorage", e);
    }
  },

  clearPreferences(): void {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {
      console.warn("Failed to clear sorting preferences", e);
    }
  },
};
