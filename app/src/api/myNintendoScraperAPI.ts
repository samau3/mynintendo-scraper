import { BACKEND_BASE_URL } from "../config";

export class MyNintendoScraperAPI {
  static async getItems() {
    const rawResponse = await fetch(BACKEND_BASE_URL);
    if (!rawResponse.ok) {
      let errorMessage = "An unexpected error occurred.";
      try {
        // Attempt to parse the error response as JSON
        const errorResponse = await rawResponse.json();

        if (errorResponse && errorResponse.message) {
          errorMessage = errorResponse.message;
        }
      } catch (jsonError) {
        // If parsing fails, attempt to use text response or fallback to default message
        const textError = await rawResponse.text();
        if (textError) {
          errorMessage = textError;
        }
      }
      throw new Error(errorMessage);
    }
    const response = await rawResponse.json();
    return response;
  }
}
