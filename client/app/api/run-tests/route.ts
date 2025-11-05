import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const { models, tests, confirmer_model } = await request.json();

    const backendUrl =
      process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8888";
    const response = await fetch(`${backendUrl}/api/run-tests`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        models,
        tests,
        confirmer_model,
      }),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to run tests" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error running tests:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
