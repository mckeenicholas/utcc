<script lang="ts">
import type { Competition, Session } from "$lib/types";
import { BASE_URL, fetchJson, formatCompetitionDate } from "$lib/utils";
import LoadingScreen from "./LoadingScreen.svelte";

interface Props {
	session: Session;
	onDelete: (id: number) => void;
	onSave: (id: number, name: string, date: string) => void;
}

let { session, onDelete, onSave }: Props = $props();

let isEditing = $state(false);
let editSessionName = $state("");
let editSessionDate = $state("");
let showModal = $state(false);
let sessionCompetitions: Competition[] = $state([]);
let competitionsLoading = $state(false);

$effect(() => {
	if (showModal) {
		fetchSessionCompetitions();
	}
});

const fetchSessionCompetitions = async () => {
	competitionsLoading = true;
	sessionCompetitions = await fetchJson<Competition[]>(`${BASE_URL}/api/session/${session.id}/competitions`);
	competitionsLoading = false;
};

const startEdit = () => {
	editSessionName = session.name;
	editSessionDate = session.start_date;
	isEditing = true;
};

const cancelEdit = () => {
	isEditing = false;
};

const handleSave = () => {
	if (editSessionName.trim()) {
		onSave(session.id, editSessionName.trim(), editSessionDate);
	}
	isEditing = false;
};
</script>

<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
	<div class="flex items-center justify-between">
		<div class="flex items-center space-x-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-lg font-medium text-blue-600"
			>
				{session.name.charAt(0).toUpperCase()}
			</div>
			<div>
				{#if isEditing}
					<input
						bind:value={editSessionName}
						onkeydown={(e) => e.key === "Enter" && handleSave()}
						class="rounded-md border border-gray-300 px-2 py-1 text-sm font-medium text-gray-900 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
					/>
					<input type="date" bind:value={editSessionDate} class="ms-2" />
				{:else}
					<span class="text-sm font-medium text-gray-900">{session.name}</span>
				{/if}
				<p class="text-xs text-gray-500">ID: {session.id} - Start Date: {session.start_date}</p>
			</div>
		</div>
		<div class="flex space-x-2">
			{#if isEditing}
				<button
					onclick={handleSave}
					disabled={!editSessionName.trim()}
					class="rounded-md bg-green-100 px-3 py-1 text-sm text-green-800 hover:bg-green-200 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-800 disabled:hover:bg-gray-200"
				>
					Save
				</button>
				<button onclick={cancelEdit} class="rounded-md bg-gray-100 px-3 py-1 text-sm text-gray-800 hover:bg-gray-200">
					Cancel
				</button>
			{:else}
				<button
					onclick={() => {
						showModal = true;
					}}
					class="rounded-md bg-blue-100 px-3 py-1 text-sm text-blue-800 hover:bg-blue-200"
				>
					View Competitions
				</button>
				<button
					onclick={startEdit}
					class="rounded-md bg-yellow-100 px-3 py-1 text-sm text-yellow-800 hover:bg-yellow-200"
				>
					Edit
				</button>
				<button
					onclick={() => onDelete(session.id)}
					class="rounded-md bg-red-100 px-3 py-1 text-sm text-red-800 hover:bg-red-200"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>

{#if showModal}
	<div
		class="bg-opacity-50 backdrop fixed inset-0 z-50 flex items-center justify-center p-4"
		onclick={() => (showModal = false)}
		onkeydown={(e) => e.key === "Escape" && (showModal = false)}
		aria-label="Close modal"
		role="button"
		tabindex="0"
	>
		<div
			class="w-full max-w-lg rounded-lg bg-white shadow-xl"
			role="dialog"
			aria-modal="true"
			tabindex="0"
			onclick={(e) => e.stopPropagation()}
			onkeydown={(e) => e.key === "Escape" && (showModal = false)}
		>
			<div class="border-b border-gray-200 px-6 py-4">
				<h3 class="text-lg font-semibold text-gray-900">{session.name}</h3>
			</div>
			<div class="px-6 py-2 text-gray-900">
				<ul>
					{#if competitionsLoading}
						<LoadingScreen inline message="Loading Competitions" minHeight="0" />
					{/if}
					{#each sessionCompetitions as competition (competition.id)}
						<li>
							{formatCompetitionDate(competition.date)} - {competition.name}
						</li>
					{/each}
				</ul>
			</div>
			<div class="flex justify-end border-t border-gray-200 px-6 py-4">
				<button
					class="inline-flex items-center rounded-md bg-gray-600 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
					onclick={() => (showModal = false)}
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}
