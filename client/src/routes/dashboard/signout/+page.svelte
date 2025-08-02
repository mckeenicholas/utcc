<script lang="ts">
	import { goto } from '$app/navigation';
	import authFetch from '$lib/authFetch';
	import { BASE_URL } from '$lib/utils';
	import { onMount } from 'svelte';

	let errorMsg = $state('');

	const signOut = async () => {
		const response = await authFetch(`${BASE_URL}/api/users/logout/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (response.ok) {
			goto('/dashboard/signin');
		} else {
			const data = await response.json();
			errorMsg = data.message || 'Logout failed';
		}
	};

	onMount(signOut);
</script>

{#if errorMsg !== ''}
	<p class="text-red-500">{errorMsg}</p>
{/if}
