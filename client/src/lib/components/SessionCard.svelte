<script lang="ts">
import { Portal } from "bits-ui";
import type { Competition, Session } from "$lib/types";
import { BASE_URL, fetchJson, formatCompetitionDate } from "$lib/utils";
import DateForm from "./DateForm.svelte";
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
		const originalOverflow = document.body.style.overflow;
		document.body.style.overflow = "hidden";
		return () => {
			document.body.style.overflow = originalOverflow;
		};
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

<div class="border border-gray-200 bg-white p-4 transition-colors hover:border-uoft-blue">
	<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
		<div class="flex items-center gap-3">
			<div
				class="flex h-8 w-8 shrink-0 items-center justify-center rounded-sm bg-gray-100 text-xs font-bold text-uoft-blue"
			>
				{session.name.charAt(0).toUpperCase()}
			</div>
			<div>
				{#if isEditing}
					<div class="flex flex-col gap-2 sm:flex-row sm:items-center">
						<input
							bind:value={editSessionName}
							onkeydown={(e) => e.key === "Enter" && handleSave()}
							class="h-[36px] rounded-sm border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
						/>
						<div class="w-40">
							<DateForm bind:selectedDate={editSessionDate} label="" />
						</div>
					</div>
				{:else}
					<span class="text-sm font-bold text-gray-900">{session.name}</span>
				{/if}
				<p class="text-[11px] text-gray-700">ID: {session.id} • Start Date: {session.start_date}</p>
			</div>
		</div>
		<div class="flex flex-wrap items-center gap-2">
			{#if isEditing}
				<button
					type="button"
					onclick={handleSave}
					disabled={!editSessionName.trim()}
					class="rounded-sm bg-uoft-blue px-2.5 py-1 text-xs font-medium text-white hover:bg-uoft-blue-80 disabled:opacity-50"
				>
					Save
				</button>
				<button
					type="button"
					onclick={cancelEdit}
					class="rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
				>
					Cancel
				</button>
			{:else}
				<button
					type="button"
					onclick={() => {
						showModal = true;
					}}
					class="rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
				>
					Competitions
				</button>
				<button
					type="button"
					onclick={startEdit}
					class="rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
				>
					Edit
				</button>
				<button
					type="button"
					onclick={() => onDelete(session.id)}
					class="rounded-sm border border-red-200 bg-white px-2.5 py-1 text-xs font-medium text-uoft-warm-red hover:bg-red-50"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>

{#if showModal}
	<Portal>
		<div
			class="fixed inset-0 z-50 flex h-full min-h-[100dvh] w-full items-center justify-center bg-black/50 p-4 backdrop-blur-xs"
			onclick={() => (showModal = false)}
			onkeydown={(e) => e.key === "Escape" && (showModal = false)}
			aria-label="Close modal"
			role="button"
			tabindex="0"
		>
			<div
				class="w-full max-w-lg border border-gray-300 bg-white"
				role="dialog"
				aria-modal="true"
				tabindex="0"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.key === "Escape" && (showModal = false)}
			>
				<div class="flex items-center justify-between border-b border-gray-200 bg-uoft-blue px-5 py-3 text-white">
					<h3 class="text-base font-bold text-white">{session.name}</h3>
					<button
						type="button"
						class="p-1 text-white/80 transition-colors hover:text-white"
						onclick={() => (showModal = false)}
						aria-label="Close"
					>
						<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>
				<div class="p-5 text-sm text-gray-900">
					{#if competitionsLoading}
						<LoadingScreen inline message="Loading Competitions..." minHeight="5rem" />
					{:else if sessionCompetitions.length > 0}
						<ul class="divide-y divide-gray-100">
							{#each sessionCompetitions as competition (competition.id)}
								<li class="py-2 text-xs">
									<span class="text-gray-700">{formatCompetitionDate(competition.date)}</span> —{" "}
									<span class="font-medium text-gray-900">{competition.name}</span>
								</li>
							{/each}
						</ul>
					{:else}
						<p class="text-xs text-gray-700">No competitions found for this session.</p>
					{/if}
				</div>
				<div class="flex justify-end border-t border-gray-100 px-5 py-3">
					<button
						type="button"
						class="rounded-sm border border-gray-200 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
						onclick={() => (showModal = false)}
					>
						Close
					</button>
				</div>
			</div>
		</div>
	</Portal>
{/if}
