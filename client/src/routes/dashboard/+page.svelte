<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { BASE_URL } from '$lib/utils';
	import type { Competition } from '$lib/types';
	import authFetch from '$lib/authFetch';

	let competitions: Competition[] = $state([]);
	let loading = $state(true);
	let newCompName = $state('');
	let newCompDate = $state('');

	onMount(async () => {
		console.log(document.cookie);

		const loggedInRes = await authFetch(`${BASE_URL}/api/users/loginstatus/`);
		const loggedInData = await loggedInRes.json();

		if (!loggedInData.logged_in) {
			goto('/dashboard/signin');
			return;
		}

		const competitionRes = await authFetch(`${BASE_URL}/api/competitions/`);

		if (competitionRes.ok) {
			competitions = await competitionRes.json();
			loading = false;
		} else if (competitionRes.status === 401) {
			goto('/dashboard/signin');
		}
	});

	const deleteCompetition = async (id: number) => {
		if (confirm('Are you sure you want to delete this competition?')) {
			const response = await authFetch(`${BASE_URL}/api/competitions/${id}/`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				competitions = competitions.filter((c) => c.id !== id);
			} else {
				alert('Failed to delete competition');
			}
		}
	};

	const createCompetition = async () => {
		const response = await authFetch(`${BASE_URL}/api/competitions/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ name: newCompName, date: newCompDate })
		});

		if (response.ok) {
			const newCompetition: Competition = await response.json();
			goto(`/competition/${newCompetition.id}`);
		} else {
			alert('Failed to create competition');
		}
	};
</script>

{#if loading}
	<p>Loading</p>
{:else}
	{#if competitions.length === 0}
		<p>No competitions added</p>
	{:else}
		<ul>
			{#each competitions as competition (competition.id)}
				<li>
					<a href={`/dashboard/competition/${competition.id}`}>{competition.name}</a>
					<button onclick={() => goto(`/dashboard/competition/${competition.id}/edit`)}>Edit</button
					>
					<button onclick={() => deleteCompetition(competition.id)}>Delete</button>
				</li>
			{/each}
		</ul>
	{/if}

	<p>Add new competition</p>
	<label for="new-comp-name">Name:</label>
	<input id="new-comp-name" placeholder="name" bind:value={newCompName} />
	<label for="new-comp-date">Date:</label>
	<input id="new-comp-date" type="date" bind:value={newCompDate} />
	<button onclick={createCompetition}>Create</button>
{/if}
