import { useTestStore } from "@/lib/store";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

export function TestSelector() {
  const { availableTests, selectedTests, toggleTest } = useTestStore();

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Select Tests</h2>
      <div className="space-y-3">
        {availableTests.map((test: string) => (
          <div key={test} className="flex items-center space-x-3">
            <Checkbox
              id={test}
              checked={selectedTests.includes(test)}
              onCheckedChange={() => toggleTest(test)}
            />
            <Label htmlFor={test} className="flex-1 cursor-pointer font-medium">
              {test}
            </Label>
          </div>
        ))}
      </div>
    </Card>
  );
}
