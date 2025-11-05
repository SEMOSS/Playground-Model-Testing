"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useTestStore } from "@/lib/store";
import { ModelSelector } from "@/components/model-selector";
import { TestSelector } from "@/components/test-selector";
import { ConfirmerModelSelector } from "@/components/confirmer-model-selector";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AlertCircle, Loader2 } from "lucide-react";
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
    <main className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Test Runner</h1>
          <p className="text-muted-foreground">
            Select models and tests to run and analyze results
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="grid gap-6 grid-cols-1 lg:grid-cols-3 mb-8">
          <div className="lg:col-span-1 space-y-6">
            <ModelSelector />
            <TestSelector />
            <ConfirmerModelSelector />
          </div>

          <div className="lg:col-span-2">
            <Card className="p-6 h-full">
              <div className="space-y-6">
                <div>
                  <h2 className="text-lg font-semibold mb-2">Summary</h2>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">
                        Models selected:
                      </span>
                      <span className="font-semibold">
                        {selectedModels.length}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">
                        Tests selected:
                      </span>
                      <span className="font-semibold">
                        {selectedTests.length}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">
                        Confirmer model:
                      </span>
                      <span className="font-semibold font-mono text-xs">
                        {confirmerModel}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="pt-6 border-t">
                  <p className="text-sm text-muted-foreground mb-4">
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
                    className="w-full gap-2"
                  >
                    {isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
                    {isLoading ? "Running Tests..." : "Run Tests"}
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </main>
  );
}
