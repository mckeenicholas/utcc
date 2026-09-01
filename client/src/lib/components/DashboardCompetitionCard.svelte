<script lang="ts">
import type { Competition } from "$lib/types";
import { formatCompetitionDate } from "$lib/utils";

interface Props {
	competition: Competition;
	onDeleteCompetition: (id: number) => unknown;
}

const { competition, onDeleteCompetition = () => null }: Props = $props();
</script>

<div class="border border-gray-200 bg-white p-4 transition-colors hover:border-uoft-blue">
	<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
		<div>
			<a href="/dashboard/competitions/{competition.id}" class="transition-colors hover:text-uoft-blue">
				<h3 class="text-sm font-bold text-gray-900">{competition.name}</h3>
			</a>
			<p class="text-xs text-gray-700">
				{competition.session ? `${competition.session_name} • ` : ""}{formatCompetitionDate(competition.date)}
			</p>
		</div>
		<div class="flex flex-wrap items-center gap-2">
			<a
				href="/dashboard/competitions/{competition.id}"
				class="rounded-sm bg-uoft-blue px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80"
			>
				Add Results
			</a>
			<a
				href="/dashboard/competitions/{competition.id}/scrambles"
				class="rounded-sm border border-gray-200 bg-white px-2.5 py-1.5 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-50"
			>
				Scrambles
			</a>
			<a
				href="/dashboard/competitions/{competition.id}/edit"
				class="rounded-sm border border-gray-200 bg-white px-2.5 py-1.5 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-50"
			>
				Edit
			</a>
			<button
				type="button"
				onclick={() => onDeleteCompetition(competition.id)}
				class="cursor-pointer rounded-sm border border-red-200 bg-white px-2.5 py-1.5 text-xs font-medium text-uoft-warm-red transition-colors hover:bg-red-50"
			>
				Delete
			</button>
		</div>
	</div>
</div>
