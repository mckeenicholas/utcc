import authFetch from '$lib/authFetch';
import type { Session } from '$lib/types';
import { BASE_URL } from '$lib/utils';

const SESSIONS_API_URL = `${BASE_URL}/api/session/`;

export const fetchSessions = async (): Promise<Session[]> => {
	const response = await authFetch(SESSIONS_API_URL);
	if (!response.ok) {
		throw new Error(`Failed to fetch sessions: ${response.statusText}`);
	}
	return response.json();
};

export const createSession = async (name: string): Promise<Response> => {
	return authFetch(SESSIONS_API_URL, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ name })
	});
};

export const updateSession = async (id: number, name: string): Promise<Response> => {
	return authFetch(`${SESSIONS_API_URL}${id}/`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ name })
	});
};

export const deleteSession = async (id: number): Promise<Response> => {
	return authFetch(`${SESSIONS_API_URL}${id}/`, {
		method: 'DELETE'
	});
};
