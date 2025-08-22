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

export const createUser = (name: string, studentStatus: boolean) => {
	const data: Omit<User, 'id'> = { name, is_uoft_student: studentStatus };

	return authFetch(`${BASE_URL}/api/users/persons/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(data)
	});
};

export const updateUser = (userId: number, name: string, studentStatus: boolean) => {
	const data: Omit<User, 'id'> = { name, is_uoft_student: studentStatus };

	return authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		method: 'PATCH',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(data)
	});
};

export const deleteUserById = (userId: number) => {
	return authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		method: 'DELETE'
	});
};
