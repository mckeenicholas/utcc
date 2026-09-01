<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import authFetch from "$lib/authFetch";
import { BASE_URL } from "$lib/utils";

let errorMsg = $state("");
let isLoading = $state(false);
let showFallback = $state(true);

const signOut = async () => {
	try {
		const response = await authFetch(`${BASE_URL}/api/users/auth/logout/`, {
			headers: {
				"Content-Type": "application/json",
			},
			method: "POST",
		});

		if (response.ok) {
			setTimeout(() => {
				goto("/dashboard/signin");
			}, 1000);
		} else {
			const data = await response.json();
			errorMsg = data.message || "Logout failed";
			isLoading = false;
			showFallback = true;
		}
	} catch {
		errorMsg = "Network error during logout";
		isLoading = false;
		showFallback = true;
	}

	setTimeout(() => {
		showFallback = true;
		isLoading = false;
	}, 3000);
};

onMount(signOut);
</script>

<div class="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12">
	<div class="w-full max-w-sm space-y-4 border border-gray-200 bg-white p-8 text-center">
		<h1 class="text-xl font-bold tracking-tight text-gray-900">U of T Cube Club</h1>

		{#if isLoading}
			<div class="space-y-3">
				<div class="flex justify-center">
					<div class="h-6 w-6 animate-spin rounded-full border-2 border-gray-200 border-t-uoft-blue"></div>
				</div>
				<p class="text-xs text-gray-700">Signing you out...</p>
			</div>
		{/if}

		{#if errorMsg !== ""}
			<p class="text-xs text-uoft-warm-red">{errorMsg}</p>
		{/if}

		{#if showFallback}
			<div class="space-y-4">
				<p class="text-xs text-gray-700">You have been signed out.</p>
				<a href="/dashboard/signin">
					<div
						class="w-full rounded-sm bg-uoft-blue px-4 py-2 text-center text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80"
					>
						Return to Login
					</div>
				</a>
			</div>
		{/if}
	</div>
</div>
