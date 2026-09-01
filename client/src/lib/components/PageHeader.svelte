<script lang="ts">
import type { Competition } from "$lib/types";
import { formatCompetitionDate } from "$lib/utils";

interface Props {
	competition: Competition | null;
	backUrl?: string;
	backText?: string;
}

const { competition, backUrl = "/dashboard", backText = "Back to Dashboard" }: Props = $props();
</script>

<div class="mb-6 flex flex-col gap-4 border-b border-gray-200 pb-5 sm:flex-row sm:items-center sm:justify-between">
	<div class="flex items-center gap-4">
		<a
			href={backUrl}
			class="inline-flex items-center rounded-sm border border-gray-200 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none"
		>
			<svg class="mr-1.5 h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			{backText}
		</a>

		{#if competition}
			<div>
				<h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">{competition.name}</h1>
				<p class="text-xs text-gray-700">
					{competition.session_name ? `${competition.session_name} • ` : ""}Date: {formatCompetitionDate(
						competition.date,
					)}
				</p>
			</div>
		{/if}
	</div>
</div>
