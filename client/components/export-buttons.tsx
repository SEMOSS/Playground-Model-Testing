"use client";

import type { RunTestsResponse } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import * as XLSX from "xlsx";

interface ExportButtonsProps {
  results: RunTestsResponse;
}

export function ExportButtons({ results }: ExportButtonsProps) {
  const handleExportJSON = () => {
    const jsonString = JSON.stringify(results, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `test-results-${
      new Date().toISOString().split("T")[0]
    }.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleExportExcel = () => {
    const workbook = XLSX.utils.book_new();
    const sheetData: any[] = [];

    Object.entries(results).forEach(([modelName, testResults]) => {
      Object.entries(testResults).forEach(([testKey, result]) => {
        if (result) {
          sheetData.push({
            Model: modelName,
            Test: testKey.replace(/_/g, " "),
            Success: result.success ? "Yes" : "No",
            Response: result.response.substring(0, 100),
            Client: result.client,
            "Pixel Calls": result.pixel?.join("; ") || "-",
            "Confirmation Response": result.confirmation_response || "-",
          });
        }
      });
    });

    const worksheet = XLSX.utils.json_to_sheet(sheetData);
    XLSX.utils.book_append_sheet(workbook, worksheet, "Test Results");
    XLSX.writeFile(
      workbook,
      `test-results-${new Date().toISOString().split("T")[0]}.xlsx`
    );
  };

  return (
    <div className="flex gap-2">
      <Button
        onClick={handleExportJSON}
        variant="outline"
        size="sm"
        className="gap-2 bg-transparent"
      >
        <Download className="w-4 h-4" />
        Export JSON
      </Button>
      <Button
        onClick={handleExportExcel}
        variant="outline"
        size="sm"
        className="gap-2 bg-transparent"
      >
        <Download className="w-4 h-4" />
        Export Excel
      </Button>
    </div>
  );
}
