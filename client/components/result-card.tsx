import type { StandardResponse } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { CheckCircle2, AlertCircle, Zap } from "lucide-react";

interface ResultCardProps {
  testName: string;
  result: StandardResponse | null;
}

export function ResultCard({ testName, result }: ResultCardProps) {
  if (!result) return null;

  return (
    <Card className="p-4 border border-border">
      <div className="space-y-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-sm">{testName}</h3>
          {result.success ? (
            <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
          ) : (
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          )}
        </div>

        <div className="bg-muted rounded p-3">
          <p className="text-xs text-muted-foreground mb-1">Response:</p>
          <p className="text-sm break-words line-clamp-4 font-mono">
            {result.response}
          </p>
        </div>

        {result.pixel && result.pixel.length > 0 && (
          <div className="bg-blue-50 dark:bg-blue-950 rounded p-3 border border-blue-200 dark:border-blue-800">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <p className="text-xs font-semibold text-blue-700 dark:text-blue-300">
                Pixel Calls
              </p>
            </div>
            <div className="space-y-1">
              {result.pixel.map((call, idx) => (
                <p
                  key={idx}
                  className="text-xs break-words line-clamp-3 font-mono text-blue-600 dark:text-blue-300"
                >
                  {call}
                </p>
              ))}
            </div>
          </div>
        )}

        {result.confirmation_response && (
          <div className="bg-emerald-50 dark:bg-emerald-950 rounded p-3 border border-emerald-200 dark:border-emerald-800">
            <p className="text-xs font-semibold text-emerald-700 dark:text-emerald-300 mb-1">
              Confirmation:
            </p>
            <p className="text-sm break-words line-clamp-3 text-emerald-700 dark:text-emerald-300">
              {result.confirmation_response}
            </p>
          </div>
        )}
      </div>
    </Card>
  );
}
