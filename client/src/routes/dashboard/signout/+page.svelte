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
	<div class="w-full max-w-sm space-y-4 border border-border bg-surface p-8 text-center">
		<h1 class="text-xl font-bold tracking-tight text-main">U of T Cube Club</h1>

		{#if isLoading}
			<div class="space-y-3">
				<div class="flex justify-center">
					<div
						class="h-6 w-6 animate-spin rounded-full border-2 border-border border-t-uoft-blue dark:border-t-blue-400"
					></div>
				</div>
				<p class="text-xs text-secondary">Signing you out...</p>
			</div>
		{/if}

		{#if errorMsg !== ""}
			<p class="text-xs text-uoft-warm-red dark:text-red-400">{errorMsg}</p>
		{/if}

		{#if showFallback}
			<div class="space-y-4">
				<p class="text-xs text-secondary">You have been signed out.</p>
				<a href="/dashboard/signin">
					<div
						class="w-full rounded-sm bg-uoft-blue px-4 py-2 text-center text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 dark:border dark:border-blue-500/30 dark:hover:bg-blue-900"
					>
						Return to Login
					</div>
				</a>
			</div>
		{/if}
	</div>
</div>
