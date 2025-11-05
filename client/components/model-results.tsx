import type { TestResults } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { ResultCard } from "./result-card";

interface ModelResultsProps {
  modelName: string;
  results: TestResults;
}

const TEST_DISPLAY_NAMES: Record<string, string> = {
  standard_text_test: "Standard Text Test",
  prompt_with_image_urls: "Prompt with Image URLs",
  basic_param_values: "Basic Param Values Test",
  tool_calling_with_tool_choice: "Tool Calling with Tool Choice",
  structured_json_test: "Structured JSON Output Test",
  prompt_with_base64_images: "Prompt with Base64 Images",
};

export function ModelResults({ modelName, results }: ModelResultsProps) {
  const testEntries = Object.entries(results).filter(
    ([_, result]) => result !== null
  );

  if (testEntries.length === 0) return null;

  return (
    <Card className="overflow-hidden border-2 border-primary/20">
      <div className="bg-gradient-to-r from-primary/10 to-primary/5 p-4 border-b">
        <h2 className="font-bold text-lg">{modelName}</h2>
      </div>
      <div className="p-6">
        <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
          {testEntries.map(([testKey, result]) => (
            <ResultCard
              key={testKey}
              testName={TEST_DISPLAY_NAMES[testKey] || testKey}
              result={result}
            />
          ))}
        </div>
      </div>
    </Card>
  );
}
