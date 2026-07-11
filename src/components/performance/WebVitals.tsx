"use client";

import { useReportWebVitals } from "next/web-vitals";

export function WebVitalsReporter() {
  useReportWebVitals((metric) => {
    if (process.env.NODE_ENV === "development") {
      console.log(
        `[WebVitals] ${metric.name}: ${metric.value.toFixed(2)} (${metric.rating})`
      );
    }
  });

  return null;
}
