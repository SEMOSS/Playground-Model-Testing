"use client";

import { useRouter } from "next/navigation";
import { useTestStore } from "@/lib/store";
import { ModelResults } from "@/components/model-results";
import { ExportButtons } from "@/components/export-buttons";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

export default function ResultsPage() {
  const router = useRouter();
  const { results, resetSelections } = useTestStore();

  if (!results) {
    return (
      <div className="min-h-screen bg-background p-4 md:p-8">
        <div className="max-w-6xl mx-auto text-center py-20">
          <h1 className="text-2xl font-bold mb-2">No Results Available</h1>
          <p className="text-muted-foreground mb-6">
            Run some tests first to see results here
          </p>
          <Button onClick={() => router.push("/")}>Go Back</Button>
        </div>
      </div>
    );
  }

  const handleReset = () => {
    resetSelections();
    router.push("/");
  };

  return (
    <main className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">Test Results</h1>
            <p className="text-muted-foreground">
              Completed on {new Date().toLocaleString()}
            </p>
          </div>
          <ExportButtons results={results} />
        </div>

        <div className="space-y-6 mb-8">
          {Object.entries(results).map(([modelName, testResults]) => (
            <ModelResults
              key={modelName}
              modelName={modelName}
              results={testResults}
            />
          ))}
        </div>

        <div className="flex gap-2">
          <Button
            onClick={handleReset}
            variant="outline"
            className="gap-2 bg-transparent"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Test Selection
          </Button>
        </div>
      </div>
    </main>
  );
}
