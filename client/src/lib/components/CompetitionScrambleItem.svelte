<script lang="ts">
import { slide } from "svelte/transition";
import { Collapsible } from "bits-ui";
import { eventNames, type ScrambleKey } from "$lib/types";
import { scrambleOrder } from "$lib/utils";
import CubeIcon from "./CubeIcon.svelte";

type ScrambleEvent = {
	event: string;
	rounds: {
		roundNum: number;
		sets: {
			num: number;
			scrambles: {
				num: string;
				scramble: string;
			}[];
		}[];
	}[];
};

const { eventScramble }: { eventScramble: ScrambleEvent } = $props();

let isOpen = $state(false);
</script>

<div class="overflow-hidden rounded-lg bg-white shadow-sm">
	<Collapsible.Root bind:open={isOpen}>
		<Collapsible.Trigger class="w-full bg-white transition-colors duration-100 ease-in-out hover:bg-gray-100">
			<div class="flex items-center justify-between px-4 py-2">
				<div class="flex items-center space-x-3">
					<CubeIcon event={eventScramble.event} />
					<h3 class="text-lg font-semibold text-gray-800">
						{eventNames[eventScramble.event]}
					</h3>
				</div>
				<svg
					class="h-5 w-5 text-gray-400 transition-transform duration-200 ease-in-out"
					class:rotate-180={isOpen}
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
				</svg>
			</div>
		</Collapsible.Trigger>

		<Collapsible.Content class="border-t border-gray-200" forceMount>
			{#if isOpen}
				<div class="space-y-6 px-6 py-4" transition:slide>
					{#each eventScramble.rounds as scrambleRound (scrambleRound.roundNum)}
						<p class="text-md font-medium text-gray-700">
							Round {scrambleRound.roundNum}
						</p>

						<div class="space-y-4">
							{#each scrambleRound.sets as scrambleSet (scrambleSet.num)}
								<div>
									<h5 class="border-b border-gray-200 pb-2 align-middle text-sm font-medium text-gray-600">
										Scramble Set {scrambleSet.num}
									</h5>

									{#each scrambleSet.scrambles as scramble (scramble.num)}
										<div class="border-b border-gray-200 p-3">
											<div class="flex flex-col gap-2 sm:flex-row sm:items-start">
												<span
													class="me-8 w-4 min-w-fit text-center align-middle text-xs font-medium tracking-wider text-gray-500 uppercase"
												>
													{scrambleOrder[scramble.num.toString() as ScrambleKey].name}
												</span>
												<code class="align-middle font-mono text-sm break-all whitespace-pre-wrap text-gray-800">
													{scramble.scramble}
												</code>
											</div>
										</div>
									{/each}
								</div>
							{/each}
						</div>
					{/each}
				</div>
			{/if}
		</Collapsible.Content>
	</Collapsible.Root>
</div>
