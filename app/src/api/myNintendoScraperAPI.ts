import axios from "axios";

import { BACKEND_BASE_URL } from "../config";

export class MyNintendoScraperAPI {
  static async getItems() {
    const response = (await axios({ method: "GET", url: BACKEND_BASE_URL }))
      .data;

    return response;
  }
}
