<script lang="ts">
import { eventNames, type ProfileRecordDetail, type WCAEvent } from "$lib/types";
import { renderTime } from "$lib/utils";

let { records }: { records: [string, ProfileRecordDetail][] } = $props();
</script>

<div class="mb-8 overflow-hidden rounded-lg bg-white shadow-sm">
	<div class="border-b border-gray-200 px-6 py-4">
		<h2 class="text-xl font-semibold text-gray-800">Personal Records</h2>
	</div>
	<div class="overflow-x-auto">
		<table class="min-w-full divide-y divide-gray-200">
			<thead class="bg-gray-50">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"> Event </th>
					<th class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"> Single </th>
					<th class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"> Average </th>
				</tr>
			</thead>
			<tbody class="divide-y divide-gray-200 bg-white">
				{#each records as [eventName, data] (eventName)}
					<tr class="transition-colors duration-100 ease-in-out hover:bg-gray-100">
						<td class="px-6 py-4 text-sm font-medium whitespace-nowrap text-gray-900">
							{eventNames[eventName as WCAEvent]}
						</td>
						<td class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap text-gray-900">
							{renderTime(data.single)}
						</td>
						<td class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap text-gray-900">
							{renderTime(data.average)}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
