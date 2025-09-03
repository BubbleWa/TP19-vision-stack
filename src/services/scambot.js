import api from "./api";

/**
 * Call the ScamBot endpoint.
 * @param {string} text - user message to check
 */
export async function detectScam(text) {
  const { data } = await api.post("/detect", { text });
  return data;
}
