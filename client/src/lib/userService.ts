// src/lib/services/userService.ts

import authFetch from '$lib/authFetch';
import type { User, Paginated } from '$lib/types';
import { BASE_URL } from '$lib/utils';

/**
 * Fetches a paginated list of all users.
 */
export const fetchUsers = async (page: number = 1): Promise<Paginated<User>> => {
	const response = await fetch(`${BASE_URL}/api/users/persons/?page=${page}`);
	if (!response.ok) {
		throw new Error('Failed to fetch users');
	}
	return response.json();
};

/**
 * Searches for users by name.
 */
export const searchUsersByName = async (query: string): Promise<User[]> => {
	if (!query.trim()) {
		return [];
	}
	const response = await fetch(
		`${BASE_URL}/api/users/persons/search/?name=${encodeURIComponent(query)}`
	);
	if (!response.ok) {
		throw new Error('Search failed');
	}
	const data = await response.json();
	return data.results || data || [];
};

/**
 * Creates a new user.
 */
export const createUser = (name: string) => {
	return authFetch(`${BASE_URL}/api/users/persons/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name })
	});
};

/**
 * Updates an existing user.
 */
export const updateUser = (userId: number, name: string) => {
	return authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		method: 'PATCH',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name })
	});
};

/**
 * Deletes a user by their ID.
 */
export const deleteUserById = (userId: number) => {
	return authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		method: 'DELETE'
	});
};
