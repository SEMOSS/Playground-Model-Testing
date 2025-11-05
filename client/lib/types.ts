export interface Model {
  name: string;
  type: string;
  id: string;
  client: string;
}

export interface StandardResponse {
  model_name: string;
  model_id: string;
  client: string;
  response: string;
  success: boolean;
  pixel: string[];
  confirmation_response: string | null;
}

export interface TestResults {
  standard_text_test: StandardResponse | null;
  prompt_with_image_urls: StandardResponse | null;
  basic_param_values: StandardResponse | null;
  tool_calling_with_tool_choice: StandardResponse | null;
  structured_json_test: StandardResponse | null;
  prompt_with_base64_images: StandardResponse | null;
}

export interface RunTestsResponse {
  [modelName: string]: TestResults;
}
