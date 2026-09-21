<script lang="ts">
import CubeViewer from "$lib/components/CubeViewer.svelte";
import type { WCAEvent } from "$lib/types";
import { formatScramble } from "$lib/utils";

interface Props {
	scrambles: string[];
	extras: string[];
	event: WCAEvent;
}

const { scrambles, extras, event }: Props = $props();

// Store heights for each row
const scrambleCellHeights: number[] = $state([]);
const extraCellHeights: number[] = $state([]);

const cubeImageMaxHeight = $derived(Math.max(...scrambleCellHeights, ...extraCellHeights, 180));
const cubeImageMaxWidth = $derived(cubeImageMaxHeight * 1.33);
</script>

<div>
	<table class="border-collapse border border-border">
		<tbody>
			{#each scrambles as scramble, idx (idx)}
				{@const scrambleFormatted = formatScramble(scramble, event)}
				<tr>
					<td class="w-12 border-r border-b border-border text-center font-mono text-xl text-main">{idx + 1}</td>
					<td class="border-r border-b border-border p-2 leading-6">
						<div bind:clientHeight={scrambleCellHeights[idx]}>
							{#each scrambleFormatted.lines as scrambleLine, i (i)}
								<p
									class="mb-1 ps-2 font-mono text-xl font-bold whitespace-pre text-main"
									class:bg-surface-muted={i % 2 !== 0 && scrambleFormatted.numLines > 4}
								>
									{scrambleLine}
								</p>
							{/each}
						</div>
					</td>
					<td class="border-r border-b border-border">
						<CubeViewer
							alg={scramble.toString()}
							eventId={event}
							width="{cubeImageMaxWidth}px"
							height="{cubeImageMaxHeight}px"
							class="m-2"
						/>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>

	<table class="mt-4 border-collapse border border-border">
		<tbody>
			{#each extras as scramble, idx (idx)}
				{@const scrambleFormatted = formatScramble(scramble, event)}
				<tr>
					<td class="w-12 border-r border-b border-border text-center font-mono text-xl text-main">E{idx + 1}</td>
					<td class="border-r border-b border-border p-2 leading-6">
						<div bind:clientHeight={scrambleCellHeights[idx]}>
							{#each scrambleFormatted.lines as scrambleLine, i (i)}
								<p
									class="mb-1 ps-2 font-mono text-xl font-bold whitespace-pre text-main"
									class:bg-surface-muted={i % 2 !== 0 && scrambleFormatted.numLines > 4}
								>
									{scrambleLine}
								</p>
							{/each}
						</div>
					</td>
					<td class="-m-2 border-r border-b border-border">
						<CubeViewer
							alg={scramble.toString()}
							eventId={event}
							width="{cubeImageMaxWidth}px"
							height="{cubeImageMaxHeight}px"
							class="m-2"
						/>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>
