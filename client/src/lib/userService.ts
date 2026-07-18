import type { Paginated, User } from "$lib/types";
import authFetch from "$lib/authFetch";
import { BASE_URL, fetchJson } from "$lib/utils";

export const fetchUsers = (page = 1): Promise<Paginated<User>> =>
	fetchJson(`${BASE_URL}/api/users/persons/?page=${page}`);

export const searchUsersByName = (query: string): Promise<User[]> => {
	if (!query.trim()) {
		return Promise.resolve([]);
	}

	return fetchJson(`${BASE_URL}/api/users/persons/search/?name=${encodeURIComponent(query)}`);
};

export const createUser = (name: string, studentStatus: boolean) => {
	const data: Omit<User, "id" | "sessions"> = {
		is_uoft_student: studentStatus,
		name,
	};

	return authFetch(`${BASE_URL}/api/users/persons/`, {
		body: JSON.stringify(data),
		headers: { "Content-Type": "application/json" },
		method: "POST",
	});
};

export const updateUser = (userId: number, name: string, studentStatus: boolean) => {
	const data: Omit<User, "id" | "sessions"> = {
		is_uoft_student: studentStatus,
		name,
	};

	return authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		body: JSON.stringify(data),
		headers: { "Content-Type": "application/json" },
		method: "PATCH",
	});
};

export const deleteUserById = (userId: number) =>
	authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
		method: "DELETE",
	});
