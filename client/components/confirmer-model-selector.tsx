"use client";

import { useTestStore } from "@/lib/store";
import { Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const COMMON_MODELS = ["gpt-4.1-nano", "gpt-4.1"];

export function ConfirmerModelSelector() {
  const { confirmerModel, setConfirmerModel } = useTestStore();

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Confirmer Model</h2>
      <div className="space-y-2">
        <Label htmlFor="confirmer-model" className="font-medium">
          Model for confirmation
        </Label>
        <Select value={confirmerModel} onValueChange={setConfirmerModel}>
          <SelectTrigger id="confirmer-model">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {COMMON_MODELS.map((model) => (
              <SelectItem key={model} value={model}>
                {model}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <p className="text-xs text-muted-foreground mt-2">
          Default model used to verify test results
        </p>
      </div>
    </Card>
  );
}
