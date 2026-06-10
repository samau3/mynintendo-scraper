import { BACKEND_BASE_URL } from "../config";
import type { IScrapeResults } from "../interfaces/interfaces";

async function parseErrorResponse(rawResponse: Response): Promise<string> {
  let errorMessage = "An unexpected error occurred.";
  try {
    const errorResponse = await rawResponse.json();
    if (errorResponse?.message) {
      errorMessage = errorResponse.message;
    }
  } catch {
    const textError = await rawResponse.text();
    if (textError) {
      errorMessage = textError;
    }
  }
  return errorMessage;
}

export class MyNintendoScraperAPI {
  static async getCachedItems(): Promise<IScrapeResults | null> {
    const rawResponse = await fetch(`${BACKEND_BASE_URL}api/items/latest`);
    if (rawResponse.status === 404) {
      return null;
    }
    if (!rawResponse.ok) {
      throw new Error(await parseErrorResponse(rawResponse));
    }
    return rawResponse.json();
  }

  static async scrapeItems(): Promise<IScrapeResults> {
    const rawResponse = await fetch(BACKEND_BASE_URL);
    if (!rawResponse.ok) {
      throw new Error(await parseErrorResponse(rawResponse));
    }
    return rawResponse.json();
  }
}
