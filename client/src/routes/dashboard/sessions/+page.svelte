<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import AddSessionForm from "$lib/components/AddSessionForm.svelte";
import DashboardHeader from "$lib/components/DashboardHeader.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import SessionCard from "$lib/components/SessionCard.svelte";
import { createSession, deleteSession, fetchSessions, updateSession } from "$lib/competitionSessionService";
import type { Session } from "$lib/types";
import { checkLoginStatus } from "$lib/utils";

let sessions: Session[] = $state([]);
let loading = $state(false);
let isSearching = $state(false);

const loadSessions = async () => {
	loading = true;
	try {
		sessions = await fetchSessions();
	} catch (error) {
		console.error("Failed to load sessions:", error);
		sessions = [];
	} finally {
		loading = false;
		isSearching = false;
	}
};

onMount(async () => {
	const loggedIn = await checkLoginStatus();

	if (!loggedIn) {
		goto("/dashboard/signin");
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
			alert("Failed to add session");
		}
	} catch (error) {
		console.error("Failed to add session:", error);
		alert("Failed to add session");
	}
};

const handleSaveSession = async (sessionId: number, name: string, date: string) => {
	try {
		const response = await updateSession(sessionId, name, date);
		if (response.ok) {
			sessions = sessions
				.map((s) => (s.id === sessionId ? { id: s.id, name, start_date: date } : s))
				.toSorted((a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime());
		} else {
			alert("Failed to update session");
		}
	} catch (error) {
		console.error("Failed to update session:", error);
		alert("Failed to update session");
	}
};

const handleDeleteSession = async (sessionId: number) => {
	if (confirm("Are you sure you want to delete this session?")) {
		try {
			const response = await deleteSession(sessionId);
			if (response.ok) {
				sessions = sessions.filter((s) => s.id !== sessionId);
			} else {
				alert("Failed to delete session");
			}
		} catch (error) {
			console.error("Failed to delete session:", error);
			alert("Failed to delete session");
		}
	}
};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-4xl px-4">
		<div class="mb-6">
			<DashboardHeader title="Session Management" showBack />
		</div>

		<AddSessionForm onAddSession={handleAddSession} />

		{#if loading}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen message={isSearching ? "Searching..." : "Loading sessions..."} inline minHeight="10rem" />
			</div>
		{:else if sessions.length > 0}
			<div class="mt-6 space-y-3">
				<div class="flex items-center justify-between border-b border-gray-200 pb-2">
					<span class="text-xs font-semibold tracking-wider text-gray-700 uppercase">
						{isSearching ? `Search Results (${sessions.length})` : `All Sessions (${sessions.length} total)`}
					</span>
				</div>
				<div class="space-y-3">
					{#each sessions as session (session.id)}
						<SessionCard {session} onDelete={handleDeleteSession} onSave={handleSaveSession} />
					{/each}
				</div>
			</div>
		{:else}
			<div class="border border-gray-200 bg-white p-12 text-center text-xs text-gray-700">No sessions found</div>
		{/if}
	</div>
</div>
