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
import { Settings } from "lucide-react";

const COMMON_MODELS = ["gpt-4.1-nano", "gpt-4.1"];

export function ConfirmerModelSelector() {
  const { confirmerModel, setConfirmerModel } = useTestStore();

  return (
    <Card className="p-6 bg-card border-border/50 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-2 mb-6">
        <Settings className="w-5 h-5 text-accent" />
        <h2 className="text-lg font-semibold">Confirmer Model</h2>
      </div>
      <div className="space-y-2">
        <Label htmlFor="confirmer-model" className="font-medium text-sm">
          Model for confirmation
        </Label>
        <Select value={confirmerModel} onValueChange={setConfirmerModel}>
          <SelectTrigger
            id="confirmer-model"
            className="bg-input border-border/50"
          >
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
