<script lang="ts">
	import { goto } from '$app/navigation';
	import authFetch, { getCsrf } from '$lib/authFetch';
	import { BASE_URL } from '$lib/utils';
	import { onMount } from 'svelte';

	let username = $state('');
	let password = $state('');

	let errrorMsg = $state('');

	const logIn = async () => {
		const response = await authFetch(`${BASE_URL}/api/users/login/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, password })
		});

		if (response.ok) {
			goto('/dashboard');
		} else {
			const data = await response.json();
			errrorMsg = data.detail || 'Login failed';
		}
	};

	onMount(async () => {
		getCsrf();
		const loginResonse = await fetch(`${BASE_URL}/api/users/loginstatus/`);
		const loginStatus = await loginResonse.json();
		if (loginStatus.logged_in == true) {
			goto('dashboard');
		}
	});
</script>

{#if errrorMsg !== ''}
	<p class="text-red-500">{errrorMsg}</p>
{/if}
<label for="username">Username</label>
<input id="username" bind:value={username} />
<label for="password">Password</label>
<input type="password" id="password" bind:value={password} />
<button onclick={logIn}>Log in</button>
