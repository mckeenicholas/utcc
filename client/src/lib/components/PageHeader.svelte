<script lang="ts">
import type { Competition } from '$lib/types';
import { formatCompetitionDate } from '$lib/utils';

interface Props {
	competition: Competition | null;
	backUrl?: string;
	backText?: string;
}

let { competition, backUrl = '/dashboard', backText = 'Back to Dashboard' }: Props = $props();
</script>

<div class="mb-8 flex items-center justify-between">
	<div class="flex items-center space-x-4">
		<a href={backUrl}>
			<div
				class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
			>
				<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M15 19l-7-7 7-7"
					/>
				</svg>
				{backText}
			</div>
		</a>

		{#if competition}
			<div>
				<h1 class="text-3xl font-bold text-gray-900">{competition.name}</h1>
				<p class="text-gray-600">
					{competition.session_name ? `${competition.session_name} Session - ` : ""}Date: {formatCompetitionDate(competition.date)}
				</p>
			</div>
		{/if}
	</div>
</div>
