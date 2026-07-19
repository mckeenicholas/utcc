<script lang="ts">
import type { Competition } from "$lib/types";
import { formatCompetitionDate } from "$lib/utils";

interface Props {
	competition: Competition;
	onDeleteCompetition: (id: number) => unknown;
}

const { competition, onDeleteCompetition = () => null }: Props = $props();
</script>

<div
	class="overflow-hidden rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-all duration-200 hover:shadow-md"
>
	<div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
		<div>
			<h3 class="text-lg font-bold text-gray-900">{competition.name}</h3>
			<p class="mt-1 text-sm font-medium text-gray-500">
				{competition.session && `${competition.session_name} - `}{formatCompetitionDate(competition.date)}
			</p>
		</div>
		<div class="flex flex-wrap gap-2">
			<a href="/dashboard/competitions/{competition.id}/scrambles">
				<div
					class="rounded-lg bg-emerald-50 px-3.5 py-2 text-sm font-semibold text-emerald-700 transition-colors hover:bg-emerald-100"
				>
					Manage Scrambles
				</div>
			</a>
			<a href="/dashboard/competitions/{competition.id}">
				<div
					class="rounded-lg bg-blue-50 px-3.5 py-2 text-sm font-semibold text-blue-700 transition-colors hover:bg-blue-100"
				>
					Add Results
				</div>
			</a>
			<a href="/dashboard/competitions/{competition.id}/edit">
				<div
					class="rounded-lg bg-amber-50 px-3.5 py-2 text-sm font-semibold text-amber-700 transition-colors hover:bg-amber-100"
				>
					Edit Info
				</div>
			</a>
			<button
				onclick={() => onDeleteCompetition(competition.id)}
				class="rounded-lg bg-red-50 px-3.5 py-2 text-sm font-semibold text-red-700 transition-colors hover:bg-red-100"
			>
				Delete
			</button>
		</div>
	</div>
</div>
