import authFetch from "#lib/authFetch.js";
import type { Session } from "#lib/types.js";
import { BASE_URL, fetchJson } from "#lib/utils.js";

const SESSIONS_API_URL = `${BASE_URL}/api/session/`;

export const fetchSessions = (): Promise<Session[]> => fetchJson(SESSIONS_API_URL);

export const createSession = (name: string, start_date: string): Promise<Response> =>
	authFetch(SESSIONS_API_URL, {
		body: JSON.stringify({ name, start_date }),
		headers: {
			"Content-Type": "application/json",
		},
		method: "POST",
	});

export const updateSession = (id: number, name: string, start_date: string): Promise<Response> =>
	authFetch(`${SESSIONS_API_URL}${id}/`, {
		body: JSON.stringify({ name, start_date }),
		headers: {
			"Content-Type": "application/json",
		},
		method: "PUT",
	});

export const deleteSession = (id: number): Promise<Response> =>
	authFetch(`${SESSIONS_API_URL}${id}/`, {
		method: "DELETE",
	});
