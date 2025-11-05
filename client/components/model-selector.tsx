import { useTestStore } from "@/lib/store";
import type { Model } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

export function ModelSelector() {
  const { models, selectedModels, toggleModel } = useTestStore();

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Select Models</h2>
      <div className="space-y-3">
        {models.map((model: Model) => (
          <div key={model.id} className="flex items-center space-x-3">
            <Checkbox
              id={model.id}
              checked={selectedModels.includes(model.id)}
              onCheckedChange={() => toggleModel(model.id)}
            />
            <Label
              htmlFor={model.id}
              className="flex-1 cursor-pointer font-medium"
            >
              <div>{model.name}</div>
              <div className="text-sm text-muted-foreground">
                {model.client}
              </div>
            </Label>
          </div>
        ))}
      </div>
    </Card>
  );
}
