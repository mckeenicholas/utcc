import authFetch from '$lib/authFetch';
import type { Paginated, User } from '$lib/types';
import { BASE_URL, fetchJson } from '$lib/utils';

export const fetchUsers = async (page: number = 1): Promise<Paginated<User>> =>
	await fetchJson(`${BASE_URL}/api/users/persons/?page=${page}`);

export const searchUsersByName = async (query: string): Promise<User[]> => {
	if (!query.trim()) {
		return [];
	}

	return await fetchJson(`${BASE_URL}/api/users/persons/search/?name=${encodeURIComponent(query)}`);
};

export const createUser = (name: string) => {
	return authFetch(`${BASE_URL}/api/users/persons/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name })
	});
};

export const updateUser = (userId: number, name: string) => {
	return authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		method: 'PATCH',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name })
	});
};

export const deleteUserById = (userId: number) => {
	return authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		method: 'DELETE'
	});
};
