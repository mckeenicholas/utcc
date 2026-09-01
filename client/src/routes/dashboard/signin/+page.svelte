<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import authFetch, { getCsrf } from "$lib/authFetch";
import { BASE_URL, checkLoginStatus } from "$lib/utils";

let username = $state("");
let password = $state("");
let errrorMsg = $state("");

const logIn = async () => {
	const response = await authFetch(`${BASE_URL}/api/users/auth/login/`, {
		body: JSON.stringify({ password, username }),
		headers: {
			"Content-Type": "application/json",
		},
		method: "POST",
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
			const nextElement = document.querySelector<HTMLElement>(`#${nextElementId}`);
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

<div class="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12">
	<div class="w-full max-w-sm space-y-5 border border-gray-200 bg-white p-8">
		<div>
			<h1 class="text-xl font-bold tracking-tight text-gray-900">Admin Sign In</h1>
			<p class="mt-1 text-xs text-gray-700">Sign in to manage competitions, scrambles, and club results.</p>
		</div>
		{#if errrorMsg !== ""}
			<div class="rounded-sm border border-red-200 bg-red-50 p-2.5 text-xs font-medium text-uoft-warm-red">
				{errrorMsg}
			</div>
		{/if}
		<div class="space-y-4">
			<div>
				<label for="username" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase">Username</label
				>
				<input
					id="username"
					bind:value={username}
					onkeydown={(e) => handleKeydown(e, "password")}
					class="mt-1 block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
				/>
			</div>
			<div>
				<label for="password" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase">Password</label
				>
				<input
					type="password"
					id="password"
					bind:value={password}
					onkeydown={(e) => handleKeydown(e, "login-button")}
					class="mt-1 block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
				/>
			</div>
			<button
				id="login-button"
				onclick={logIn}
				onkeydown={(e) => handleKeydown(e)}
				class="w-full rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 focus:outline-none"
			>
				Sign In
			</button>
		</div>
	</div>
</div>
