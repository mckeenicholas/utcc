<script lang="ts">
import type { Competition, Session } from "$lib/types";
import { BASE_URL, fetchJson, formatCompetitionDate } from "$lib/utils";
import LoadingScreen from "./LoadingScreen.svelte";

interface Props {
	session: Session;
	onDelete: (id: number) => void;
	onSave: (id: number, name: string, date: string) => void;
}

const { session, onDelete, onSave }: Props = $props();

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

<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-all duration-200 hover:shadow-md">
	<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
		<div class="flex items-center space-x-3">
			<div
				class="flex h-11 w-11 items-center justify-center rounded-full border border-blue-100 bg-blue-50 text-lg font-bold text-blue-600"
			>
				{session.name.charAt(0).toUpperCase()}
			</div>
			<div>
				{#if isEditing}
					<div class="flex flex-col gap-2 sm:flex-row sm:items-center">
						<input
							bind:value={editSessionName}
							onkeydown={(e) => e.key === "Enter" && handleSave()}
							class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
						/>
						<input
							type="date"
							bind:value={editSessionDate}
							class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
						/>
					</div>
				{:else}
					<span class="text-sm font-semibold text-gray-900">{session.name}</span>
				{/if}
				<p class="mt-1 text-xs font-medium text-gray-400">ID: {session.id} • Start Date: {session.start_date}</p>
			</div>
		</div>
		<div class="flex flex-wrap gap-2">
			{#if isEditing}
				<button
					onclick={handleSave}
					disabled={!editSessionName.trim()}
					class="rounded-lg bg-emerald-50 px-3.5 py-2 text-sm font-semibold text-emerald-700 transition-colors hover:bg-emerald-100 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400"
				>
					Save
				</button>
				<button
					onclick={cancelEdit}
					class="rounded-lg bg-gray-50 px-3.5 py-2 text-sm font-semibold text-gray-600 transition-colors hover:bg-gray-100"
				>
					Cancel
				</button>
			{:else}
				<button
					onclick={() => {
						showModal = true;
					}}
					class="rounded-lg bg-blue-50 px-3.5 py-2 text-sm font-semibold text-blue-700 transition-colors hover:bg-blue-100"
				>
					View Competitions
				</button>
				<button
					onclick={startEdit}
					class="rounded-lg bg-amber-50 px-3.5 py-2 text-sm font-semibold text-amber-700 transition-colors hover:bg-amber-100"
				>
					Edit
				</button>
				<button
					onclick={() => onDelete(session.id)}
					class="rounded-lg bg-red-50 px-3.5 py-2 text-sm font-semibold text-red-700 transition-colors hover:bg-red-100"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>

{#if showModal}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/40 p-4 backdrop-blur-sm"
		onclick={() => (showModal = false)}
		onkeydown={(e) => e.key === "Escape" && (showModal = false)}
		aria-label="Close modal"
		role="button"
		tabindex="0"
	>
		<div
			class="w-full max-w-lg overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-2xl"
			role="dialog"
			aria-modal="true"
			tabindex="0"
			onclick={(e) => e.stopPropagation()}
			onkeydown={(e) => e.key === "Escape" && (showModal = false)}
		>
			<div class="border-b border-gray-100 bg-gray-50/50 px-6 py-4">
				<h3 class="text-lg font-bold text-gray-900">{session.name}</h3>
			</div>
			<div class="max-h-[60vh] overflow-y-auto px-6 py-6 text-gray-900">
				<ul class="space-y-3">
					{#if competitionsLoading}
						<LoadingScreen inline message="Loading Competitions" minHeight="0" />
					{:else if sessionCompetitions.length === 0}
						<li class="py-4 text-center text-sm text-gray-500">No competitions in this session yet.</li>
					{/if}
					{#each sessionCompetitions as competition (competition.id)}
						<li
							class="flex items-center justify-between rounded-lg border border-gray-100 bg-white p-3 transition-colors hover:border-gray-200"
						>
							<span class="text-sm font-semibold text-gray-800">{competition.name}</span>
							<span class="rounded-md bg-gray-50 px-2 py-1 text-xs font-semibold text-gray-400"
								>{formatCompetitionDate(competition.date)}</span
							>
						</li>
					{/each}
				</ul>
			</div>
			<div class="flex justify-end border-t border-gray-100 bg-gray-50/50 px-6 py-4">
				<button
					class="inline-flex items-center justify-center rounded-lg bg-gray-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-gray-800 focus:ring-2 focus:ring-gray-500 focus:outline-none"
					onclick={() => (showModal = false)}
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}
