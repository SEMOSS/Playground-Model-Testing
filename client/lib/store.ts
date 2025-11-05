import { create } from "zustand";
import type { Model, RunTestsResponse } from "./types";

interface TestStore {
  // Data
  models: Model[];
  availableTests: string[];
  results: RunTestsResponse | null;

  // Selection state
  selectedModels: string[];
  selectedTests: string[];
  confirmerModel: string;

  // UI state
  isLoading: boolean;
  error: string | null;

  // Actions
  setModelsAndTests: (models: Model[], tests: string[]) => void;
  toggleModel: (modelId: string) => void;
  toggleTest: (testName: string) => void;
  setConfirmerModel: (model: string) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setResults: (results: RunTestsResponse) => void;
  clearResults: () => void;
  resetSelections: () => void;
}

export const useTestStore = create<TestStore>((set) => ({
  models: [],
  availableTests: [],
  results: null,
  selectedModels: [],
  selectedTests: [],
  confirmerModel: "gpt-4.1-nano",
  isLoading: false,
  error: null,

  setModelsAndTests: (models, tests) => set({ models, availableTests: tests }),

  toggleModel: (modelId) =>
    set((state) => ({
      selectedModels: state.selectedModels.includes(modelId)
        ? state.selectedModels.filter((id) => id !== modelId)
        : [...state.selectedModels, modelId],
    })),

  toggleTest: (testName) =>
    set((state) => ({
      selectedTests: state.selectedTests.includes(testName)
        ? state.selectedTests.filter((t) => t !== testName)
        : [...state.selectedTests, testName],
    })),

  setConfirmerModel: (model) => set({ confirmerModel: model }),

  setIsLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  setResults: (results) => set({ results }),

  clearResults: () => set({ results: null }),

  resetSelections: () =>
    set({
      selectedModels: [],
      selectedTests: [],
      confirmerModel: "gpt-4.1-nano",
      results: null,
    }),
}));
