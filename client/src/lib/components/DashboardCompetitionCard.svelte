<script lang="ts">
import type { Competition } from "$lib/types";
import { formatCompetitionDate } from "$lib/utils";

interface Props {
	competition: Competition;
	onDeleteCompetition: (id: number) => unknown;
}

const { competition, onDeleteCompetition = () => null }: Props = $props();
</script>

<div class="border border-border bg-surface p-4 transition-colors hover:border-brand">
	<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
		<div>
			<a href="/dashboard/competitions/{competition.id}" class="transition-colors hover:text-brand">
				<h3 class="text-sm font-bold text-main">{competition.name}</h3>
			</a>
			<p class="text-xs text-secondary">
				{competition.session ? `${competition.session_name} • ` : ""}{formatCompetitionDate(competition.date)}
			</p>
		</div>
		<div class="flex flex-wrap items-center gap-2">
			<a
				href="/dashboard/competitions/{competition.id}"
				class="rounded-sm bg-uoft-blue px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 dark:border dark:border-blue-500/30 dark:hover:bg-blue-900"
			>
				Add Results
			</a>
			<a
				href="/dashboard/competitions/{competition.id}/scrambles"
				class="rounded-sm border border-border bg-surface px-2.5 py-1.5 text-xs font-medium text-secondary transition-colors hover:bg-surface-muted"
			>
				Scrambles
			</a>
			<a
				href="/dashboard/competitions/{competition.id}/edit"
				class="rounded-sm border border-border bg-surface px-2.5 py-1.5 text-xs font-medium text-secondary transition-colors hover:bg-surface-muted"
			>
				Edit
			</a>
			<button
				type="button"
				onclick={() => onDeleteCompetition(competition.id)}
				class="cursor-pointer rounded-sm border border-red-200 bg-surface px-2.5 py-1.5 text-xs font-medium text-uoft-warm-red transition-colors hover:bg-red-50 dark:border-red-900/50 dark:text-red-400 dark:hover:bg-red-950/40"
			>
				Delete
			</button>
		</div>
	</div>
</div>
