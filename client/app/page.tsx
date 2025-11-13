"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useTestStore } from "@/lib/store";
import { ModelSelector } from "@/components/model-selector";
import { TestSelector } from "@/components/test-selector";
import { ConfirmerModelSelector } from "@/components/confirmer-model-selector";
import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AlertCircle, Loader2, Zap } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function Home() {
  const router = useRouter();
  const {
    models,
    availableTests,
    selectedModels,
    selectedTests,
    confirmerModel,
    isLoading,
    error,
    setModelsAndTests,
    setIsLoading,
    setError,
    setResults,
  } = useTestStore();

  const [isLoadingInitial, setIsLoadingInitial] = useState(true);

  useEffect(() => {
    const fetchModelsAndTests = async () => {
      try {
        const response = await fetch("/api/get-models-and-tests");
        if (!response.ok) throw new Error("Failed to fetch models and tests");
        const data = await response.json();
        setModelsAndTests(data.models, data.available_tests);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch data");
      } finally {
        setIsLoadingInitial(false);
      }
    };

    fetchModelsAndTests();
  }, [setModelsAndTests, setError]);

  const handleRunTests = async () => {
    if (selectedModels.length === 0 || selectedTests.length === 0) {
      setError("Please select at least one model and one test");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/run-tests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          models: selectedModels,
          tests: selectedTests,
          confirmer_model: confirmerModel,
        }),
      });

      if (!response.ok) throw new Error("Failed to run tests");
      const data = await response.json();
      setResults(data);
      router.push("/results");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to run tests");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingInitial) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="sticky top-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Zap className="w-6 h-6 text-accent" />
            <h1 className="text-xl font-bold">Test Runner</h1>
          </div>
          <ThemeToggle />
        </div>
      </div>

      {/* Main content */}
      <div className="p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          {/* Header section */}
          <div className="mb-8">
            <p className="text-muted-foreground max-w-2xl">
              Select models and tests to run and analyze results
            </p>
          </div>

          {error && (
            <Alert
              variant="destructive"
              className="mb-6 bg-destructive/10 border-destructive/30 text-destructive"
            >
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ModelSelector />
              <TestSelector />
            </div>
            <ConfirmerModelSelector />

            {/* Summary and controls section */}
            <div>
              <Card className="p-8 bg-card border-border/50 shadow-sm">
                <div className="space-y-8 flex-1">
                  <div>
                    <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                      <Zap className="w-5 h-5 text-accent" />
                      Summary
                    </h2>
                    <div className="space-y-4 bg-muted/40 rounded-lg p-5 border border-border/50">
                      <div className="flex justify-between items-center pb-4 border-b border-border/50">
                        <span className="text-muted-foreground">
                          Models selected:
                        </span>
                        <span className="font-semibold text-lg text-accent">
                          {selectedModels.length}
                        </span>
                      </div>
                      <div className="flex justify-between items-center pb-4 border-b border-border/50">
                        <span className="text-muted-foreground">
                          Tests selected:
                        </span>
                        <span className="font-semibold text-lg text-accent">
                          {selectedTests.length}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-muted-foreground">
                          Confirmer model:
                        </span>
                        <span className="font-mono text-xs bg-primary/10 text-primary px-3 py-1 rounded-md font-semibold">
                          {confirmerModel}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-2">
                    <p className="text-sm text-muted-foreground mb-6">
                      {selectedModels.length === 0 || selectedTests.length === 0
                        ? "Please select at least one model and one test to run"
                        : `Ready to run ${
                            selectedModels.length * selectedTests.length
                          } test combinations`}
                    </p>
                    <Button
                      onClick={handleRunTests}
                      disabled={
                        isLoading ||
                        selectedModels.length === 0 ||
                        selectedTests.length === 0
                      }
                      size="lg"
                      className="w-full gap-2 bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all"
                    >
                      {isLoading && (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      )}
                      {isLoading ? "Running Tests..." : "Run Tests"}
                    </Button>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
