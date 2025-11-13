import { useTestStore } from "@/lib/store";
import type { Model } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Zap } from "lucide-react";

export function ModelSelector() {
  const { models, selectedModels, toggleModel } = useTestStore();

  return (
    <Card className="p-6 bg-card border-border/50 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-2 mb-6">
        <Zap className="w-5 h-5 text-accent" />
        <h2 className="text-lg font-semibold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text">
          Select Models
        </h2>
      </div>
      <div className="space-y-3">
        {models.map((model: Model) => (
          <div
            key={model.id}
            className="flex items-center space-x-3 p-3 rounded-lg hover:bg-accent/5 transition-colors"
          >
            <Checkbox
              id={model.id}
              checked={selectedModels.includes(model.id)}
              onCheckedChange={() => toggleModel(model.id)}
            />
            <Label
              htmlFor={model.id}
              className="flex-1 cursor-pointer font-medium"
            >
              <div className="text-sm font-semibold">{model.name}</div>
              <div className="text-xs text-muted-foreground">
                {model.client}
              </div>
            </Label>
          </div>
        ))}
      </div>
    </Card>
  );
}
