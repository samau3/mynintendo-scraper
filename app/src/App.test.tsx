import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import App from "./App";
import { MyNintendoScraperAPI } from "./api/myNintendoScraperAPI";

vi.mock("react-loader-spinner", () => ({
  RotatingLines: () => <div data-testid="loading-spinner" />,
}));

vi.mock("./api/myNintendoScraperAPI", () => ({
  MyNintendoScraperAPI: {
    getCachedItems: vi.fn().mockResolvedValue(null),
    scrapeItems: vi.fn(),
  },
}));

describe("App", () => {
  it("shows scrape prompt when no cached listings exist", async () => {
    render(<App />);
    expect(
      await screen.findByText(/No cached listings found/i),
    ).toBeInTheDocument();
    expect(MyNintendoScraperAPI.getCachedItems).toHaveBeenCalled();
  });
});
