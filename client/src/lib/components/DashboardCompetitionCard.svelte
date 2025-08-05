<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Competition } from '$lib/types';

	interface Props {
		competition: Competition;
		onDeleteCompetition: (id: number) => unknown;
	}

	const { competition, onDeleteCompetition = () => null }: Props = $props();
</script>

<div class="rounded-lg bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
	<div class="flex items-center justify-between">
		<div>
			<h3 class="font-medium text-gray-900">{competition.name}</h3>
			<p class="text-sm text-gray-500">
				{new Date(competition.date).toLocaleDateString()}
			</p>
		</div>
		<div class="flex space-x-2">
			<a
				href={`/dashboard/competitions/${competition.id}`}
				class="rounded-md bg-blue-100 px-3 py-1 text-sm text-blue-800 hover:bg-blue-200"
			>
				Add Results
			</a>
			<button
				onclick={() => goto(`/dashboard/competitions/${competition.id}/edit`)}
				class="rounded-md bg-yellow-100 px-3 py-1 text-sm text-yellow-800 hover:bg-yellow-200"
			>
				Edit Info
			</button>
			<button
				onclick={() => onDeleteCompetition(competition.id)}
				class="rounded-md bg-red-100 px-3 py-1 text-sm text-red-800 hover:bg-red-200"
			>
				Delete
			</button>
		</div>
	</div>
</div>
