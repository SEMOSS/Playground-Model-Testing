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
  deploymentUrl: string;
  accessKey: string;
  secretKey: string;

  // UI state
  isLoading: boolean;
  error: string | null;

  // Actions
  setModelsAndTests: (models: Model[], tests: string[]) => void;
  setDeploymentConfig: (
    url: string,
    accessKey: string,
    secretKey: string
  ) => void;
  toggleModel: (modelId: string) => void;
  toggleTest: (testName: string) => void;
  setConfirmerModel: (model: string) => void;
  setDeploymentUrl: (url: string) => void;
  setAccessKey: (key: string) => void;
  setSecretKey: (key: string) => void;
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
  deploymentUrl: "",
  accessKey: "",
  secretKey: "",
  isLoading: false,
  error: null,

  setModelsAndTests: (models, tests) => set({ models, availableTests: tests }),
  setDeploymentConfig: (url, accessKey, secretKey) =>
    set({ deploymentUrl: url, accessKey, secretKey }),

  toggleModel: (modelId) =>
    set((state) => ({
      selectedModels: state.selectedModels.includes(modelId)
        ? state.selectedModels.filter((id) => id !== modelId)
        : [...state.selectedModels, modelId],
    })),

  toggleTest: (testName) =>
    set((state) => ({
      selectedTests: state.selectedTests.includes(testName)
        ? state.selectedTests.filter((name) => name !== testName)
        : [...state.selectedTests, testName],
    })),

  setConfirmerModel: (model) => set({ confirmerModel: model }),
  setDeploymentUrl: (url) => set({ deploymentUrl: url }),
  setAccessKey: (key) => set({ accessKey: key }),
  setSecretKey: (key) => set({ secretKey: key }),
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
