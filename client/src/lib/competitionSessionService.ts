import type { Session } from "$lib/types";
import authFetch from "$lib/authFetch";
import { BASE_URL, fetchJson } from "$lib/utils";

const SESSIONS_API_URL = `${BASE_URL}/api/session/`;

export const fetchSessions = (): Promise<Session[]> => fetchJson(SESSIONS_API_URL);

export const createSession = (name: string, start_date: string): Promise<Response> => {
	return authFetch(SESSIONS_API_URL, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ name, start_date }),
	});
};

export const updateSession = (id: number, name: string, start_date: string): Promise<Response> => {
	return authFetch(`${SESSIONS_API_URL}${id}/`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ name, start_date }),
	});
};

export const deleteSession = (id: number): Promise<Response> => {
	return authFetch(`${SESSIONS_API_URL}${id}/`, {
		method: "DELETE",
	});
};
