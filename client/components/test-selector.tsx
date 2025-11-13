import { useTestStore } from "@/lib/store";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Layers } from "lucide-react";

export function TestSelector() {
  const { availableTests, selectedTests, toggleTest } = useTestStore();

  return (
    <Card className="p-6 bg-card border-border/50 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-2 mb-6">
        <Layers className="w-5 h-5 text-accent" />
        <h2 className="text-lg font-semibold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text">
          Select Tests
        </h2>
      </div>
      <div className="space-y-3">
        {availableTests.map((test: string) => (
          <div
            key={test}
            className="flex items-center space-x-3 p-3 rounded-lg hover:bg-accent/5 transition-colors"
          >
            <Checkbox
              id={test}
              checked={selectedTests.includes(test)}
              onCheckedChange={() => toggleTest(test)}
            />
            <Label
              htmlFor={test}
              className="flex-1 cursor-pointer font-medium text-sm"
            >
              {test}
            </Label>
          </div>
        ))}
      </div>
    </Card>
  );
}
