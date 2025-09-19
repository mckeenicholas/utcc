<script lang="ts">
import CubeViewer from '$lib/components/CubeViewer.svelte';
import type { WCAEvent } from '$lib/types';

interface Props {
	scrambles: string[];
	extras: string[];
	event: WCAEvent;
}

const { scrambles, extras, event }: Props = $props();

const cubeMovesPerLine = 12;
const sq1ClockMovesPerLine = 5;
const cubeMaxMoveLength = 4; // Maximum length of a move (e.g., "3Rw'")
const sq1ClockMaxMoveLength = 8;

// Store heights for each row
let scrambleCellHeights: number[] = $state([]);
let extraCellHeights: number[] = $state([]);

const formatScramble = (scrambleStr: string) => {
	if (event == 'minx') {
		const lines = scrambleStr.split('\n').map((line) => line + ' ');
		return { lines, numLines: lines.length };
	}

	const splitChar = event == 'sq1' ? ' / ' : ' ';
	const moves = scrambleStr.split(splitChar);
	const lines = [];

	const movesPerLine = event == 'sq1' || event == 'clock' ? sq1ClockMovesPerLine : cubeMovesPerLine;
	const maxMoveLength =
		event == 'sq1' || event == 'clock' ? sq1ClockMaxMoveLength : cubeMaxMoveLength;

	for (let i = 0; i < moves.length; i += movesPerLine) {
		const lineMoves = moves.slice(i, i + movesPerLine);
		const paddedMoves = lineMoves.map((move) => {
			if (event === 'sq1') {
				// Split the tuple (e.g., "(1, -5)") into its numbers
				const [top, bottom] = move
					.slice(1, -1)
					.split(',')
					.map((s) => s.trim());

				// Add a space before positive numbers for alignment
				const paddedTop = top.startsWith('-') ? top : ` ${top}`;
				const paddedBottom = bottom.startsWith('-') ? bottom : ` ${bottom}`;

				return `(${paddedTop},${paddedBottom})`;
			}
			return move.padEnd(maxMoveLength);
		});
		lines.push(paddedMoves.join(splitChar));
	}

	return { lines: lines, numLines: lines.length };
};

const cubeImageMaxHeight = $derived(Math.max(...scrambleCellHeights, ...extraCellHeights, 180));
const cubeImageMaxWidth = $derived(cubeImageMaxHeight * 1.33);
</script>

<div>
	<table class="border-collapse border">
		<tbody>
			{#each scrambles as scramble, idx (idx)}
				<tr>
					<td class="w-12 border-r border-b text-center font-mono text-xl">{idx + 1}</td>
					<td class="border-r border-b p-2 leading-6">
						<div bind:clientHeight={scrambleCellHeights[idx]}>
							{#each formatScramble(scramble).lines as scrambleLine, i (i)}
								<p
									class="mb-1 ps-2 font-mono text-xl font-bold whitespace-pre"
									class:bg-neutral-300={i % 2 !== 0 && (formatScramble(scramble).numLines > 4)}
								>
									{scrambleLine}
								</p>
							{/each}
						</div>
					</td>
					<td class="border-r border-b">
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

	<table class="mt-4 border-collapse border">
		<tbody>
			{#each extras as scramble, idx (idx)}
				<tr>
					<td class="w-12 border-r border-b text-center font-mono text-xl">E{idx + 1}</td>
					<td class="border-r border-b p-2 leading-6">
						<div bind:clientHeight={scrambleCellHeights[idx]}>
							{#each formatScramble(scramble).lines as scrambleLine, i (i)}
								<p
									class="mb-1 ps-2 font-mono text-xl font-bold whitespace-pre"
									class:bg-neutral-300={i % 2 !== 0 && formatScramble(scramble).numLines > 4}
								>
									{scrambleLine}
								</p>
							{/each}
						</div>
					</td>
					<td class="-m-2 border-r border-b">
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
