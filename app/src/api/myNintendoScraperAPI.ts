import { BACKEND_BASE_URL } from "../config";

export class MyNintendoScraperAPI {
  static async getItems() {
    const rawResponse = await fetch(BACKEND_BASE_URL);
    const response = await rawResponse.json();

    return response;
  }
}
