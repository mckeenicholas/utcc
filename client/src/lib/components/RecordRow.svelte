<script lang="ts">
	import { getMeanType, renderTime } from '$lib/utils';
	import type { RecordInstance, WCAEvent } from '$lib/types';

	let {
		record,
		eventKey,
		type
	}: { record: RecordInstance; eventKey: WCAEvent; type: 'Single' | 'Average' } = $props();

	let recordType = $derived.by(() => {
		if (type == 'Single') {
			return 'Single';
		}

		return getMeanType(eventKey);
	});
</script>

<tr
	class="cursor-pointer hover:bg-gray-50"
	onclick={() => (window.location.href = `/results/${record.competition_id}`)}
>
	<td class="px-4 py-2 text-center font-semibold">{recordType}</td>
	<td class="px-4 py-2 text-center">{record.person}</td>
	<td class="px-4 py-2 text-center">
		{record.competition_name}
	</td>
	<td class="px-4 py-2 text-center">
		{renderTime(record.result)}
	</td>
	{#each record.times_list as time, timeIdx (timeIdx)}
		<td class="hidden px-4 py-2 text-center md:table-cell">
			{renderTime(time)}
		</td>
	{/each}
</tr>
