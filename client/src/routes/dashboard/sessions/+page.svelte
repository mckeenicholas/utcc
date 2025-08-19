<script lang="ts">
import {
	fetchSessions,
	createSession,
	updateSession,
	deleteSession
} from '$lib/competitionSessionService';
import type { Session } from '$lib/types';
import { checkLoginStatus } from '$lib/utils';
import AddSessionForm from '$lib/components/AddSessionForm.svelte';
import SessionCard from '$lib/components/SessionCard.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import { onMount } from 'svelte';
import DashboardHeader from '$lib/components/DashboardHeader.svelte';
import { goto } from '$app/navigation';

let sessions: Session[] = $state([]);
let loading = $state(false);
let isSearching = $state(false);

const loadSessions = async () => {
	loading = true;
	try {
		sessions = await fetchSessions();
	} catch (error) {
		console.error('Failed to load sessions:', error);
		sessions = [];
	} finally {
		loading = false;
		isSearching = false;
	}
};

onMount(async () => {
	const loggedIn = await checkLoginStatus();

	if (!loggedIn) {
		goto('/dashboard/signin');
		return;
	}

	loadSessions();
});

const handleAddSession = async (name: string, date: string) => {
	try {
		const response = await createSession(name, date);
		if (response.ok) {
			await loadSessions();
		} else {
			alert('Failed to add session');
		}
	} catch (error) {
		console.error('Failed to add session:', error);
		alert('Failed to add session');
	}
};

const handleSaveSession = async (sessionId: number, name: string, date: string) => {
	try {
		const response = await updateSession(sessionId, name, date);
		if (response.ok) {
			sessions = sessions
				.map((s) => (s.id === sessionId ? { id: s.id, name: name, start_date: date } : s))
				.sort((a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime());
		} else {
			alert('Failed to update session');
		}
	} catch (error) {
		console.error('Failed to update session:', error);
		alert('Failed to update session');
	}
};

const handleDeleteSession = async (sessionId: number) => {
	if (confirm('Are you sure you want to delete this session?')) {
		try {
			const response = await deleteSession(sessionId);
			if (response.ok) {
				sessions = sessions.filter((s) => s.id !== sessionId);
			} else {
				alert('Failed to delete session');
			}
		} catch (error) {
			console.error('Failed to delete session:', error);
			alert('Failed to delete session');
		}
	}
};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-4xl px-4">
		<DashboardHeader title="Session Management" showBack />

		<AddSessionForm onAddSession={handleAddSession} />

		<div class="rounded-lg bg-white px-6 pt-2 pb-6 shadow-sm">
			{#if loading}
				<LoadingScreen message={isSearching ? 'Searching...' : 'Loading sessions...'} />
			{:else if sessions.length > 0}
				<div class="mt-4 space-y-2">
					<h3 class="text-sm font-medium text-gray-700">
						{isSearching ? `Search Results (${sessions.length})` : `All Sessions (${sessions.length} total)`}
					</h3>
					<div class="grid gap-4">
						{#each sessions as session (session.id)}
							<SessionCard
								session={session}
								onDelete={handleDeleteSession}
								onSave={handleSaveSession}
							/>
						{/each}
					</div>
				</div>
			{:else}
				<div class="py-4 text-center text-gray-500">No sessions found</div>
			{/if}
		</div>
	</div>
</div>
