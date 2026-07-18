<script lang="ts">
import { goto } from "$app/navigation";
import authFetch, { getCsrf } from "$lib/authFetch";
import { BASE_URL, checkLoginStatus } from "$lib/utils";
import { onMount } from "svelte";

let username = $state("");
let password = $state("");
let errrorMsg = $state("");

const logIn = async () => {
	const response = await authFetch(`${BASE_URL}/api/users/auth/login/`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ username, password }),
	});

	if (response.ok) {
		goto("/dashboard");
	} else {
		const data = await response.json();
		errrorMsg = data.error || "Login failed";
		password = "";
	}
};

const handleKeydown = (event: KeyboardEvent, nextElementId?: string) => {
	if (event.key === "Enter") {
		event.preventDefault();
		if (nextElementId) {
			const nextElement = document.querySelector(`#${nextElementId}`);
			nextElement?.focus();
		} else {
			// If no next element (login button), submit the form
			logIn();
		}
	}
};

onMount(async () => {
	getCsrf();

	const loggedIn = await checkLoginStatus();
	if (loggedIn) {
		goto("/dashboard");
	}
});
</script>

<div class="flex min-h-screen items-center justify-center">
	<div class="w-full max-w-md space-y-4 rounded-lg bg-gray-100 p-6 shadow-md">
		<p class="text-lg font-medium">UofT Rubik's Cube Club Login</p>
		{#if errrorMsg !== ""}
			<p class="text-red-500">{errrorMsg}</p>
		{/if}
		<div class="space-y-4">
			<div>
				<label for="username" class="block text-sm font-medium text-gray-700">Username</label>
				<input
					id="username"
					bind:value={username}
					onkeydown={(e) => handleKeydown(e, "password")}
					class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
				/>
			</div>
			<div>
				<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
				<input
					type="password"
					id="password"
					bind:value={password}
					onkeydown={(e) => handleKeydown(e, "login-button")}
					class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
				/>
			</div>
			<button
				id="login-button"
				onclick={logIn}
				onkeydown={(e) => handleKeydown(e)}
				class="w-full rounded-md bg-gray-600 px-4 py-2 text-white hover:bg-gray-700 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
			>
				Log in
			</button>
		</div>
	</div>
</div>
