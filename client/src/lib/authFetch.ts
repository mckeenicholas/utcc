import Cookies from "js-cookie";
import { BASE_URL } from "./utils";

export const getCsrf = async () => {
	await fetch(`${BASE_URL}/api/users/auth/csrf/`, {
		credentials: "include",
	});
};

const authFetch = (url: string | URL, options: RequestInit = {}): Promise<Response> => {
	const csrftoken: string = Cookies.get("csrftoken") ?? "";

	const headers = new Headers(options.headers);
	if (csrftoken) {
		headers.set("X-CSRFToken", csrftoken);
	}

	const config: RequestInit = {
		...options,
		headers,
		credentials: "include",
		// Mode: 'same-origin'
	};

	return fetch(url, config);
};

export default authFetch;
