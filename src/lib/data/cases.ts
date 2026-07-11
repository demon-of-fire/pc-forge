import casesData from "../../../public/data/cases.json";
import { Case } from "./types";

export async function getCases(): Promise<Case[]> {
  return casesData as Case[];
}

export async function getCaseBySlug(slug: string): Promise<Case | null> {
  return (casesData as Case[]).find((c) => c.slug === slug) || null;
}
