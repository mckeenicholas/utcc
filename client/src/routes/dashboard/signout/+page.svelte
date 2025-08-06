<script lang="ts">
import { goto } from '$app/navigation';
import authFetch from '$lib/authFetch';
import { BASE_URL } from '$lib/utils';
import { onMount } from 'svelte';

let errorMsg = $state('');
let isLoading = $state(true);
let showFallback = $state(false);

const signOut = async () => {
	try {
		const response = await authFetch(`${BASE_URL}/api/users/auth/logout/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (response.ok) {
			setTimeout(() => {
				goto('/dashboard/signin');
			}, 1000);
		} else {
			const data = await response.json();
			errorMsg = data.message || 'Logout failed';
			isLoading = false;
			showFallback = true;
		}
	} catch {
		errorMsg = 'Network error during logout';
		isLoading = false;
		showFallback = true;
	}

	setTimeout(() => {
		showFallback = true;
		isLoading = false;
	}, 3000);
};

const goToLogin = () => {
	goto('/dashboard/signin');
};

onMount(signOut);
</script>

<div class="flex min-h-screen items-center justify-center">
	<div class="w-full max-w-md space-y-4 rounded-lg bg-gray-100 p-6 text-center shadow-md">
		<p class="text-lg font-medium">UofT Rubik's Cube Club</p>

		{#if isLoading}
			<div class="space-y-2">
				<p class="text-gray-600">Signing you out...</p>
				<div class="flex justify-center">
					<div
						class="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600"
					></div>
				</div>
			</div>
		{/if}

		{#if errorMsg !== ''}
			<p class="text-red-500">{errorMsg}</p>
		{/if}

		{#if showFallback}
			<div class="space-y-3">
				<p class="text-gray-600">You have been signed out.</p>
				<button
					onclick={goToLogin}
					class="w-full rounded-md bg-gray-600 px-4 py-2 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
				>
					Return to Login
				</button>
			</div>
		{/if}
	</div>
</div>
